"""Repeatable audit and one predeclared tokenizer experiment; no production edits.

Run from the repository root: python -m solution.audit_evaluation
The old validation set has already been inspected; it is not a fresh test set.
"""
from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

from score import build_report, load_labels, load_predictions
from solution.evaluate import EvaluationRunner, baseline_details, summarize
from solution.predict import CHAR_WEIGHT, PredictionPipeline, read_queries


DECIMAL_TOKEN_PATTERN = r"(?u)\b[A-Z0-9]+(?:\.[0-9]+[A-Z0-9]*)*\b"

ERROR_ANALYSIS = {
    "q0005": "Capacidad 28000 frente a 30000 LBS; el esperado queda segundo. No puntuamos capacidad explícitamente y 28,000 se separa en tokens.",
    "q0016": "La entrada dice PLATAFORMA; la etiqueta Z0000M describe CAJA CERRADA. Recuperada en posición 43. Posible clasificación genérica de negocio por confirmar.",
    "q0024": "Tanque inoxidable de 31000 LTS, 2023. El candidato textual más cercano termina en 2022; el esperado genérico sí incluye 2023, pero queda fuera de 50.",
    "q0035": "AUDI S3 SEDAN: devolvemos 3 puertas y se espera 4 puertas. Falta usar carrocería y puertas; el esperado queda segundo.",
    "q0050": "CAJA REFRIGERADA coincide con el devuelto; etiqueta CAJA CERRADA en posición 34. Falta confirmar una posible regla genérica de negocio.",
    "q0085": "TOLVA DALTO conduce a tolva, mientras la etiqueta es CAJA CERRADA. El esperado no aparece en 50; discrepancia semántica pendiente de experto.",
    "q0094": "DODEGE RAM 400: marca con errata y número 400 favorecen ISUZU ELF 400. Se espera RAM 2500, recuperado en posición 10; confirmar texto/etiqueta.",
    "q0095": "Descripción 35451 con DODGE DURANGO no especifica motor ni versión. GT PLUS 3.6L frente a RT 5.7L; esperado segundo. Información insuficiente.",
    "q0132": "F150 no especifica tracción. XL 4X4 frente a XL 4X2 del mismo año; esperado segundo. No se puede inferir el atributo ausente.",
    "q0186": "Entrada 4400 250HP 4X2: devuelto 4400 250HP 6X2; esperado 4300 210HP 4X2 en posición 28. Hay señales cruzadas y falta puntuar tracción.",
}


def export_errors(current: pd.DataFrame, queries: pd.DataFrame, pipeline, out: Path) -> None:
    examples = current.set_index("query_id").loc[list(ERROR_ANALYSIS)].reset_index()
    if examples.top1_correct.any():
        raise ValueError("The selected error examples no longer describe current failures")
    examples = examples.merge(queries[["query_id", "year", "marca", "submarca", "tipveh"]],
                              on="query_id", validate="one_to_one")
    for prefix, column in (("expected", "expected_code"), ("returned", "top1_code")):
        examples[f"{prefix}_descriptions"] = examples[column].map(
            lambda code: json.dumps(pipeline.catalog.by_code[code].descriptions, ensure_ascii=False))
        examples[f"{prefix}_years"] = examples[column].map(
            lambda code: json.dumps(pipeline.catalog.by_code[code].valid_years))
    examples["analysis_hypothesis"] = examples.query_id.map(ERROR_ANALYSIS)
    examples.to_csv(out / "ten_errors.csv", index=False)


def paired_group_interval(rows: pd.DataFrame, repetitions: int = 5000) -> dict:
    """Paired bootstrap of description/year groups, retaining row weighting.

    This describes uncertainty on observed cases; it is not independent testing.
    """
    grouped = rows.groupby("group", sort=True).delta.agg(["sum", "count"])
    rng = np.random.default_rng(20261007)
    indices = rng.integers(0, len(grouped), size=(repetitions, len(grouped)))
    values = grouped["sum"].to_numpy()[indices].sum(axis=1)
    counts = grouped["count"].to_numpy()[indices].sum(axis=1)
    low, high = np.quantile(values / counts, [0.025, 0.975])
    return {"delta_mean_utility": float(rows.delta.mean()),
            "group_bootstrap_95_interval": [float(low), float(high)],
            "groups": len(grouped), "repetitions": repetitions, "seed": 20261007}


def actual_metrics(path: Path, labels: dict) -> dict:
    report = build_report(load_predictions(path), labels)
    accepted = [row for row in report.outcomes if row.decision == "auto_accept"]
    return {"n": report.n, "accuracy_top1": report.top1_accuracy,
            "recall_top3": report.top3_recall, "mean_utility": report.mean_utility,
            "auto_accept_count": len(accepted), "review_rate": 1 - report.auto_accept_rate,
            "auto_accept_precision": report.auto_accept_precision if accepted else None}


def main() -> None:
    started = time.perf_counter()
    out = Path("evaluation/reassessment")
    out.mkdir(parents=True, exist_ok=True)
    plan = {
        "experiment": "R1_decimal_with_unit_token",
        "hypothesis": "Keep decimal engines such as 2.0L in one word token instead of 2 and 0L.",
        "token_pattern": DECIMAL_TOKEN_PATTERN,
        "fixed_parameters": "Existing ranking weights, character weight, normalization and catalog.",
        "promotion_rule": "Positive development paired-group 95% lower bound and positive old-validation utility delta; recalibrate before any deployment.",
        "limitations": "Development informed earlier selection; validation already inspected. No new independent labels.",
        "experimental_decision": "All review; saved confidence model is not transferable to changed retrieval.",
    }
    # Write the plan before measuring any candidate result.
    (out / "experiment_plan.json").write_text(json.dumps(plan, indent=2), encoding="utf-8")
    queries = pd.read_csv("data/queries_labeled.csv", dtype=str, keep_default_na=False)
    split = pd.read_csv("evaluation/split.csv", dtype=str, keep_default_na=False)
    if set(queries.query_id) != set(split.query_id):
        raise ValueError("Frozen split does not cover exactly the current queries")
    pipeline = PredictionPipeline()
    predictions = pipeline.predict(read_queries("data/queries_labeled.csv"))
    predictions.to_csv(out / "current_predictions.csv", index=False)
    runner = EvaluationRunner(pipeline.retriever)
    current = pd.DataFrame(runner.run(queries, CHAR_WEIGHT, pipeline.weights)).merge(
        split[["query_id", "subset", "group"]], on="query_id", validate="one_to_one")
    versions = pd.read_csv("data/versions.csv", dtype=str, keep_default_na=False)
    original = pd.DataFrame(baseline_details(queries, versions)).merge(
        split[["query_id", "subset", "group"]], on="query_id", validate="one_to_one")
    baseline_predictions = original[["query_id", "top1_code", "top3_codes"]].copy()
    baseline_predictions["confidence"] = 0.5
    baseline_predictions["decision"] = "review"
    baseline_predictions.to_csv(out / "baseline_predictions.csv", index=False)
    for name, frame in (("current_details", current), ("baseline_details", original)):
        frame.to_csv(out / f"{name}.csv", index=False)
    export_errors(current, queries, pipeline, out)
    labels = load_labels(Path("data/queries_labeled.csv"))
    metrics = {"labeled_sha256": hashlib.sha256(Path("data/queries_labeled.csv").read_bytes()).hexdigest(),
               "baseline": actual_metrics(out / "baseline_predictions.csv", labels),
               "current": actual_metrics(out / "current_predictions.csv", labels),
               "subsets": {}, "fallback_rows": pipeline.fallbacks,
               "calibration_warning": pipeline.model_warning,
               "baseline_recall50_note": "Diagnostic extension of the same original scoring; baseline CLI only returns three codes."}
    for subset in ("development", "validation", "all"):
        metrics["subsets"][subset] = {
            name: summarize((frame if subset == "all" else frame.loc[frame.subset.eq(subset)]).to_dict("records"))
            for name, frame in (("current", current), ("baseline", original))}
    print("Current and baseline measured", json.dumps(metrics["subsets"]["all"]), flush=True)
    # Only the word tokenizer/index changes. No corpus/label-specific alias.
    retriever = pipeline.retriever
    retriever.word_vectorizer = TfidfVectorizer(
        lowercase=False, token_pattern=DECIMAL_TOKEN_PATTERN, ngram_range=(1, 2),
        sublinear_tf=True, dtype=np.float32)
    retriever.word_matrix = retriever.word_vectorizer.fit_transform(retriever.texts)
    trial = pd.DataFrame(EvaluationRunner(retriever).run(queries, CHAR_WEIGHT, pipeline.weights))
    trial = trial.merge(split[["query_id", "subset", "group"]], on="query_id", validate="one_to_one")
    trial.to_csv(out / "R1_details.csv", index=False)
    paired = current[["query_id", "subset", "group", "top1_code", "top3_codes", "expected_in_top3"]].merge(
        trial[["query_id", "top1_code", "top3_codes", "expected_in_top3"]], on="query_id", suffixes=("_current", "_trial"), validate="one_to_one")
    paired["delta"] = 0.2 * (paired.expected_in_top3_trial.astype(int) - paired.expected_in_top3_current.astype(int))
    changed = paired.loc[paired.top3_codes_current.ne(paired.top3_codes_trial)]
    changed.to_csv(out / "R1_changed_queries.csv", index=False)
    experiment = {**plan, "metrics": {}, "paired_uncertainty": {}}
    for subset in ("development", "validation", "all"):
        frame = trial if subset == "all" else trial.loc[trial.subset.eq(subset)]
        pair = paired if subset == "all" else paired.loc[paired.subset.eq(subset)]
        experiment["metrics"][subset] = summarize(frame.to_dict("records"))
        experiment["paired_uncertainty"][subset] = paired_group_interval(pair)
    supported = (experiment["paired_uncertainty"]["development"]["group_bootstrap_95_interval"][0] > 0
                 and experiment["paired_uncertainty"]["validation"]["delta_mean_utility"] > 0)
    experiment["supported_for_recalibration"] = supported
    experiment["deployed"] = False
    experiment["changed_query_count"] = len(changed)
    experiment["reason"] = "Needs separate recalibration before promotion" if supported else "Rejected: no sufficiently supported utility improvement"
    metrics["experiment"] = experiment
    metrics["seconds"] = time.perf_counter() - started
    (out / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(json.dumps(metrics, indent=2), flush=True)


if __name__ == "__main__":
    main()
