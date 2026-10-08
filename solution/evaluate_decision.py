"""Select a conservative decision policy using grouped out-of-fold calibration.

    python -m solution.evaluate_decision

Ranking is frozen. The previously inspected ranking holdout is reported as a
secondary check, not as a new untouched test set. No blind queries are read.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import asdict, dataclass, replace
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedGroupKFold

from score import Prediction, build_report
from solution.catalog import DEFAULT_DATA_DIR, load_catalog
from solution.decision import (
    DEFAULT_MODEL_PATH, MIN_CALIBRATION_GROUPS, THRESHOLDS,
    CalibrationObservation, ConfidenceModel, Decision, DecisionFeatures, DecisionPolicy, wilson_lower,
)
from solution.normalization import normalize_text
from solution.ranking import CandidateRanker, RankingWeights
from solution.retrieval import CatalogRetriever


@dataclass(frozen=True)
class EvaluationCase:
    query_id: str
    group: str
    segment: str
    expected_code: str
    top3_codes: tuple[str, ...]
    features: DecisionFeatures

    @property
    def correct(self) -> bool:
        return self.top3_codes[0] == self.expected_code

    def observation(self) -> CalibrationObservation:
        return CalibrationObservation(self.features, self.correct, self.group)


def summarize_policy(cases: list[EvaluationCase], decisions: list[Decision]) -> dict:
    if len(cases) != len(decisions) or not cases:
        raise ValueError("Need one decision per nonempty evaluation case")
    predictions = {
        case.query_id: Prediction(case.query_id, case.top3_codes[0], case.top3_codes,
                                  decision.confidence, decision.decision)
        for case, decision in zip(cases, decisions)
    }
    report = build_report(predictions, {case.query_id: case.expected_code for case in cases})
    accepted_groups = {}
    accepted_rows = 0
    errors = 0
    for case, decision in zip(cases, decisions):
        if decision.decision == "auto_accept":
            accepted_groups.setdefault(case.group, []).append(case.correct)
            accepted_rows += 1
            errors += not case.correct
    correct_groups = sum(all(values) for values in accepted_groups.values())
    return {
        "n": len(cases), "mean_utility": report.mean_utility,
        "auto_accept_count": accepted_rows, "auto_accept_errors": errors,
        "auto_accept_precision": report.auto_accept_precision if accepted_rows else None,
        "auto_accept_rate": report.auto_accept_rate, "review_rate": 1 - report.auto_accept_rate,
        "top3_recall": report.top3_recall, "top1_accuracy": report.top1_accuracy,
        "auto_accept_groups": len(accepted_groups),
        "auto_accept_precision_lower_bound": wilson_lower(correct_groups, len(accepted_groups)),
    }


def grouped_calibration_validation(cases: list[EvaluationCase]):
    """Predict each validation fold with a calibrator that did not see its groups."""
    segments = [case.segment for case in cases]
    groups = [case.group for case in cases]
    splitter = StratifiedGroupKFold(n_splits=4, shuffle=True, random_state=17)
    fold_ids = np.full(len(cases), -1, dtype=int)
    decisions = {threshold: [None] * len(cases) for threshold in (None, *THRESHOLDS)}
    assignments = []
    for fold, (train, validation) in enumerate(splitter.split(np.zeros(len(cases)), segments, groups)):
        train_groups = {groups[i] for i in train}
        assert train_groups.isdisjoint(groups[i] for i in validation)
        model = ConfidenceModel.fit([cases[i].observation() for i in train])
        for i in validation:
            fold_ids[i] = fold
            assignments.append({"query_id": cases[i].query_id, "group": cases[i].group, "fold": fold})
            for threshold in decisions:
                decisions[threshold][i] = DecisionPolicy(model, threshold).decide(cases[i].features)
    assert all(fold_ids >= 0)
    return decisions, fold_ids, assignments


def select_threshold(cases, decisions_by_threshold, fold_ids):
    """Prefer review unless gains and independently grouped support agree.

    Thresholds and evidence buckets are fixed before evaluation, not searched
    against individual cases. Use few thresholds; do not optimize raw-score cuts.
    """
    review_metrics = summarize_policy(cases, decisions_by_threshold[None])
    ledger = []
    selected = None
    best = (review_metrics["mean_utility"], 0.0, 0.0)
    for threshold, decisions in decisions_by_threshold.items():
        metrics = summarize_policy(cases, decisions)
        fold_gains = []
        for fold in sorted(set(fold_ids)):
            indices = np.flatnonzero(fold_ids == fold)
            subset = [cases[i] for i in indices]
            candidate = summarize_policy(subset, [decisions[i] for i in indices])
            reference = summarize_policy(subset, [decisions_by_threshold[None][i] for i in indices])
            fold_gains.append(candidate["mean_utility"] - reference["mean_utility"])
        supported = (
            threshold is not None
            and metrics["auto_accept_groups"] >= MIN_CALIBRATION_GROUPS
            and metrics["auto_accept_precision_lower_bound"] >= 0.80
            and min(fold_gains) >= -1e-12
            and metrics["mean_utility"] > review_metrics["mean_utility"] + 1e-12
        )
        ledger.append({"threshold": threshold, **metrics, "min_fold_utility_gain": min(fold_gains),
                       "fold_utility_gains": fold_gains, "empirically_supported": supported})
        # Equal utility favors fewer automatic decisions, then the stricter cutoff.
        key = (metrics["mean_utility"], -metrics["auto_accept_rate"], threshold or 0.0)
        if supported and key > best:
            best, selected = key, threshold
    return selected, ledger


def load_cases(queries, ranking_selection):
    catalog = load_catalog(DEFAULT_DATA_DIR)
    retriever = CatalogRetriever(catalog)
    ranker = CandidateRanker(retriever)
    weights = RankingWeights(**ranking_selection["weights"])
    cases = []
    for row in queries.to_dict("records"):
        observable = {key: value for key, value in row.items() if key != "expected_code"}
        ranked = ranker.rank(observable, retriever.retrieve(observable, 50, ranking_selection["char_weight"]), weights)
        cases.append(EvaluationCase(
            row["query_id"], normalize_text(row["description"]) + "|" + row["year"],
            row["segment"], row["expected_code"], tuple(item.code for item in ranked),
            DecisionFeatures.from_ranked(observable, ranked),
        ))
    return cases


def _review_reference(cases, model):
    return summarize_policy(cases, [DecisionPolicy(model).decide(case.features) for case in cases])


def point_estimate_reference(cases, protected_decisions, threshold):
    """Diagnostic only: quantify what trusting the point estimate would do.

    This deliberately omits the Wilson-bound check; it is never selectable as
    the production policy. Attribute, score, margin and sample-size guards stay.
    """
    return [
        replace(decision, decision="auto_accept", reason="diagnostic_point_estimate_only")
        if not case.features.blockers() and decision.calibration_groups >= MIN_CALIBRATION_GROUPS
        and decision.confidence >= threshold else decision
        for case, decision in zip(cases, protected_decisions)
    ]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evaluation-dir", type=Path, default=Path("evaluation"))
    parser.add_argument("--model-out", type=Path, default=DEFAULT_MODEL_PATH)
    args = parser.parse_args()
    out = args.evaluation_dir
    selection = json.loads((out / "ranking_selection.json").read_text(encoding="utf-8"))
    labeled_path = DEFAULT_DATA_DIR / "queries_labeled.csv"
    digest = hashlib.sha256(labeled_path.read_bytes()).hexdigest()
    if digest != selection["labeled_sha256"]:
        raise ValueError("Labeled data differs from frozen ranking evaluation")
    queries = pd.read_csv(labeled_path, dtype=str, keep_default_na=False)
    cases = load_cases(queries, selection)
    old_ranking = pd.read_csv(out / "ranking_details.csv", dtype=str, keep_default_na=False).set_index("query_id")
    for case in cases:
        if "|".join(case.top3_codes) != old_ranking.loc[case.query_id, "top3_codes"]:
            raise ValueError("Ranking changed: do not silently reuse its evaluation")
    dev_ids = set(selection["development_ids"])
    val_ids = set(selection["validation_ids"])
    development = [case for case in cases if case.query_id in dev_ids]
    validation = [case for case in cases if case.query_id in val_ids]
    assert len(development) + len(validation) == len(cases)
    assert {case.group for case in development}.isdisjoint(case.group for case in validation)
    oof_decisions, fold_ids, assignments = grouped_calibration_validation(development)
    threshold, ledger = select_threshold(development, oof_decisions, fold_ids)
    point_references = [
        {"threshold": cutoff, **summarize_policy(development, point_estimate_reference(development, oof_decisions[cutoff], cutoff)),
         "reason": "Diagnostic only: ignores conditional calibration uncertainty; not selected"}
        for cutoff in THRESHOLDS
    ]
    model = ConfidenceModel.fit([case.observation() for case in development])
    policy = DecisionPolicy(model, threshold)
    reason = "Grouped validation supports automation" if threshold is not None else "Review retained: no threshold passed evidence and utility requirements"
    ranking_signature = hashlib.sha256(json.dumps({"weights": selection["weights"], "char_weight": selection["char_weight"]}, sort_keys=True).encode()).hexdigest()
    policy.save(args.model_out, {
        "labeled_sha256": digest, "ranking_signature": ranking_signature,
        "calibration_source": "174 ranking-development rows, grouped evidence counts",
        "selection_source": "four grouped out-of-fold calibration folds, seed 17",
        "ranking_holdout_previously_inspected": True, "selection_reason": reason,
    })
    baseline = pd.read_csv(out / "baseline_predictions.csv", dtype=str, keep_default_na=False).set_index("query_id")
    def baseline_metrics(subset):
        baseline_cases = [EvaluationCase(case.query_id, case.group, case.segment, case.expected_code,
                          tuple(baseline.loc[case.query_id, "top3_codes"].split("|")), case.features) for case in subset]
        return _review_reference(baseline_cases, model)
    metrics = {
        "selected_threshold": threshold, "selection_reason": reason,
        "development_grouped_oof": {
            "selected": summarize_policy(development, oof_decisions[threshold]),
            "review_all": summarize_policy(development, oof_decisions[None]),
            "baseline_review_all": baseline_metrics(development),
        },
        "previously_inspected_holdout": {
            "selected": summarize_policy(validation, [policy.decide(case.features) for case in validation]),
            "review_all": _review_reference(validation, model),
            "baseline_review_all": baseline_metrics(validation),
        },
        "all_descriptive_includes_calibration_rows": {
            "selected": summarize_policy(cases, [policy.decide(case.features) for case in cases]),
            "review_all": _review_reference(cases, model),
            "baseline_review_all": baseline_metrics(cases),
        },
        "threshold_experiments": ledger,
        "diagnostic_point_estimate_only": point_references,
        "calibration_bins": {
            name: {**asdict(bin_), "confidence": bin_.confidence, "lower_bound": bin_.lower_bound}
            for name, bin_ in model.bins.items()
        },
    }
    oof_by_id = {case.query_id: decision for case, decision in zip(development, oof_decisions[threshold])}
    diagnostic_by_id = {
        case.query_id: decision for case, decision in zip(
            development, point_estimate_reference(development, oof_decisions[0.80], 0.80)
        )
    }
    diagnostic = []
    predictions = []
    for case in cases:
        decision = policy.decide(case.features)
        predictions.append({"query_id": case.query_id, "top1_code": case.top3_codes[0],
                            "top3_codes": "|".join(case.top3_codes), "confidence": decision.confidence,
                            "decision": decision.decision})
        diagnostic.append({
            "query_id": case.query_id, "subset": "development" if case.query_id in dev_ids else "previously_inspected_holdout",
            "expected_code": case.expected_code, "top1_code": case.top3_codes[0], "correct": case.correct,
            **asdict(decision), "features": json.dumps(asdict(case.features)),
            "oof_decision": oof_by_id[case.query_id].decision if case.query_id in oof_by_id else "",
            "oof_confidence": oof_by_id[case.query_id].confidence if case.query_id in oof_by_id else "",
            "oof_calibration_groups": oof_by_id[case.query_id].calibration_groups if case.query_id in oof_by_id else "",
            "oof_precision_lower_bound": oof_by_id[case.query_id].precision_lower_bound if case.query_id in oof_by_id else "",
            "diagnostic_point_only_0_80_decision": diagnostic_by_id[case.query_id].decision if case.query_id in diagnostic_by_id else "",
        })
    pd.DataFrame(predictions).to_csv("dev_predictions.csv", index=False)
    pd.DataFrame(diagnostic).to_csv(out / "decision_details.csv", index=False)
    diagnostic_errors = [
        {**row, "description": queries.set_index("query_id").loc[row["query_id"], "description"]}
        for row in diagnostic if row["diagnostic_point_only_0_80_decision"] == "auto_accept" and not row["correct"]
    ]
    pd.DataFrame(diagnostic_errors, columns=[*diagnostic[0].keys(), "description"]).to_csv(
        out / "decision_diagnostic_errors.csv", index=False,
    )
    pd.DataFrame(assignments).sort_values("query_id").to_csv(out / "decision_calibration_folds.csv", index=False)
    pd.DataFrame([
        *({"policy_kind": "guarded", **row} for row in ledger),
        *({"policy_kind": "diagnostic_point_estimate_only", **row} for row in point_references),
    ]).to_csv(out / "decision_thresholds.csv", index=False)
    (out / "decision_metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(json.dumps(metrics, indent=2), flush=True)


if __name__ == "__main__":
    main()
