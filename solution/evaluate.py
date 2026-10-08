"""Staged evaluation: select on development, then inspect a locked holdout.

    python -m solution.evaluate --phase develop
    python -m solution.evaluate --phase validate

No acceptance policy is calibrated at this stage: all predictions use review.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import asdict, replace
from pathlib import Path

import pandas as pd
from sklearn.model_selection import StratifiedGroupKFold

from score import Prediction, build_report
from solution import baseline
from solution.catalog import DEFAULT_DATA_DIR, load_catalog
from solution.normalization import normalize_text
from solution.ranking import CandidateRanker, RankingWeights
from solution.retrieval import CatalogRetriever


def make_split(queries: pd.DataFrame) -> pd.DataFrame:
    """Keep equivalent description/year pairs together, including repeated cases."""
    groups = queries.description.map(normalize_text) + "|" + queries.year
    splitter = StratifiedGroupKFold(n_splits=4, shuffle=True, random_state=42)
    development, validation = next(splitter.split(queries, queries.segment, groups))
    split = queries[["query_id", "segment"]].copy()
    split["group"] = groups
    split["subset"] = "development"
    split.iloc[validation, split.columns.get_loc("subset")] = "validation"
    assert set(groups.iloc[development]).isdisjoint(set(groups.iloc[validation]))
    return split


def summarize(details: list[dict]) -> dict:
    frame = pd.DataFrame(details)
    predictions = {
        row["query_id"]: Prediction(row["query_id"], row["top1_code"], tuple(row["top3_codes"].split("|")), 0.0, "review")
        for row in details
    }
    labels = {row["query_id"]: row["expected_code"] for row in details}
    official = build_report(predictions, labels)
    retrieved = frame.expected_in_50
    return {
        "n": len(details), "top1_correct": int(frame.top1_correct.sum()),
        "top3_correct": int(frame.expected_in_top3.sum()), "retrieved_at_50": int(retrieved.sum()),
        "accuracy_top1": official.top1_accuracy, "recall_top3": official.top3_recall,
        "recall_at_50": float(retrieved.mean()),
        "ranking_accuracy_given_retrieved": float(frame.loc[retrieved, "top1_correct"].mean()) if retrieved.any() else 0.0,
        "review_all_utility": official.mean_utility,
    }


def baseline_details(queries: pd.DataFrame, versions: pd.DataFrame) -> list[dict]:
    """Exact shipped top-3 plus a diagnostic extension of its search to 50 codes.

    The original script returns only three rows. Diagnostic recall@50 extends
    its same scoring and tie-break; it does not change the official baseline.
    """
    codes, tokens, frequency = baseline.build_index(versions)
    n_docs = max(1, len(codes))
    details = []
    for row in queries.to_dict("records"):
        top = baseline.rank(row["description"], codes, tokens, frequency, n_docs)
        query_tokens = baseline.tokenize(row["description"])
        scored = []
        for code, document in zip(codes, tokens):
            overlap = query_tokens & document
            if overlap:
                score = sum(1 / (1 + frequency[token] / n_docs) for token in overlap)
                scored.append((score, code))
        scored.sort(key=lambda item: (-item[0], item[1]))
        pool = list(dict.fromkeys(code for _, code in scored))[:50] if scored else list(dict.fromkeys(codes))[:50]
        details.append(_detail(row, top, pool))
    return details


def _detail(query: dict, top: list[str], pool: list[str]) -> dict:
    expected = query["expected_code"]
    return {
        "query_id": query["query_id"], "description": query["description"],
        "segment": query["segment"], "expected_code": expected,
        "top1_code": top[0], "top3_codes": "|".join(top),
        "top1_correct": top[0] == expected, "expected_in_top3": expected in top,
        "expected_in_50": expected in pool,
        "expected_retrieval_rank": pool.index(expected) + 1 if expected in pool else None,
    }


class EvaluationRunner:
    def __init__(self, retriever: CatalogRetriever):
        self.retriever = retriever
        self.ranker = CandidateRanker(retriever)
        self.cache = {}

    def run(self, queries: pd.DataFrame, char_weight: float, weights: RankingWeights) -> list[dict]:
        details = []
        for row in queries.to_dict("records"):
            # Remove the answer before calling either matching component.
            observable = {key: value for key, value in row.items() if key != "expected_code"}
            key = (row["query_id"], char_weight)
            if key not in self.cache:
                self.cache[key] = self.retriever.retrieve(observable, 50, char_weight)
            candidates = self.cache[key]
            ranked = self.ranker.rank(observable, candidates, weights)
            result = _detail(row, [item.code for item in ranked], [item.code for item in candidates])
            result.update({
                "top1_score": ranked[0].score,
                "top1_conflicts": "|".join(ranked[0].conflicts),
                "top1_catalog_ambiguous": ranked[0].catalog_ambiguous,
                "top1_source_row": ranked[0].source_row,
                "top1_contributions": json.dumps(ranked[0].contributions, sort_keys=True),
            })
            details.append(result)
        return details


def _key(metrics: dict) -> tuple:
    # All-review utility is monotonic in top-3 recall; top-1 breaks equal utility.
    return metrics["top3_correct"], metrics["top1_correct"]


def develop(queries, versions, runner, out, digest):
    split = make_split(queries)
    split.to_csv(out / "split.csv", index=False)
    development_ids = split.loc[split.subset.eq("development"), "query_id"].tolist()
    validation_ids = split.loc[split.subset.eq("validation"), "query_id"].tolist()
    development = queries.loc[queries.query_id.isin(development_ids)]
    baseline_metrics = summarize(baseline_details(development, versions))
    current = RankingWeights(
        tfidf=1, fuzzy=0, year_bonus=0, year_penalty=0,
        manufacturer_bonus=0, manufacturer_penalty=0,
        submodel_bonus=0, submodel_penalty=0, type_bonus=0, type_penalty=0,
    )
    char_weight = 0.0
    current_metrics = summarize(runner.run(development, char_weight, current))
    ledger = [{"experiment": "E0_word_tfidf", "kept": True, "char_weight": char_weight,
               "weights": asdict(current), "metrics": current_metrics, "reason": "Starting integrated-catalog reference"}]
    selected_name = "E0_word_tfidf"
    # Each addition is tested against the currently retained configuration.
    experiments = (
        ("E1_hybrid_tfidf", {"char_weight": 0.35}),
        ("E2_rapidfuzz", {"tfidf": 0.70, "fuzzy": 0.30}),
        ("E3_year_compatibility", {"year_bonus": 0.12, "year_penalty": 0.20}),
        ("E4_manufacturer_submodel", {"manufacturer_bonus": 0.10, "manufacturer_penalty": 0.60,
                                      "submodel_bonus": 0.08, "submodel_penalty": 0.20}),
        ("E5_vehicle_type", {"type_bonus": 0.04, "type_penalty": 0.15}),
        ("E6_stronger_year_penalty", {"year_penalty": 0.60}),
        ("E7_light_rapidfuzz", {"tfidf": 0.90, "fuzzy": 0.10}),
        ("E8_light_manufacturer_submodel", {"manufacturer_bonus": 0.02, "manufacturer_penalty": 0.10,
                                            "submodel_bonus": 0.02, "submodel_penalty": 0.05}),
        ("E9_light_vehicle_type", {"type_bonus": 0.01, "type_penalty": 0.05}),
    )
    for name, changes in experiments:
        candidate_char = changes.get("char_weight", char_weight)
        candidate_weights = replace(current, **{key: value for key, value in changes.items() if key != "char_weight"})
        metrics = summarize(runner.run(development, candidate_char, candidate_weights))
        kept = _key(metrics) > _key(current_metrics)
        ledger.append({"experiment": name, "kept": kept, "char_weight": candidate_char,
                       "weights": asdict(candidate_weights), "metrics": metrics,
                       "reason": "Higher development utility, then top-1" if kept else "Reverted: no improvement in development utility/top-1"})
        print(name, "KEEP" if kept else "REVERT", json.dumps(metrics), flush=True)
        if kept:
            current, char_weight, current_metrics, selected_name = candidate_weights, candidate_char, metrics, name
    selection = {
        "labeled_sha256": digest, "seed": 42, "split_method": "First StratifiedGroupKFold fold, 4 folds",
        "grouping": "normalized description + year", "development_ids": development_ids,
        "validation_ids": validation_ids, "selected_experiment": selected_name,
        "char_weight": char_weight, "weights": asdict(current),
        "development_baseline": baseline_metrics, "development_selected": current_metrics,
        "experiments": ledger,
    }
    (out / "ranking_selection.json").write_text(json.dumps(selection, indent=2), encoding="utf-8")
    print("Locked selection", selected_name, "development", len(development_ids), "validation", len(validation_ids), flush=True)


def validate(queries, versions, runner, out, digest):
    selection = json.loads((out / "ranking_selection.json").read_text(encoding="utf-8"))
    if selection["labeled_sha256"] != digest:
        raise ValueError("Labeled data changed after configuration selection")
    weights = RankingWeights(**selection["weights"])
    details, baseline_rows, metrics = [], [], {}
    for subset, ids in (("development", selection["development_ids"]), ("validation", selection["validation_ids"])):
        frame = queries.loc[queries.query_id.isin(ids)]
        selected_details = runner.run(frame, selection["char_weight"], weights)
        original_details = baseline_details(frame, versions)
        metrics[subset] = {"selected": summarize(selected_details), "baseline": summarize(original_details)}
        for row in selected_details:
            row["subset"] = subset
        for row in original_details:
            row["subset"] = subset
        details.extend(selected_details)
        baseline_rows.extend(original_details)
    metrics["all_descriptive"] = {"selected": summarize(details), "baseline": summarize(baseline_rows)}
    metrics["by_segment"] = {
        segment: {"selected": summarize([row for row in details if row["segment"] == segment]),
                  "baseline": summarize([row for row in baseline_rows if row["segment"] == segment])}
        for segment in sorted(queries.segment.unique())
    }
    pd.DataFrame(details).to_csv(out / "ranking_details.csv", index=False)
    pd.DataFrame(baseline_rows).to_csv(out / "baseline_details.csv", index=False)
    predictions = pd.DataFrame(details)[["query_id", "top1_code", "top3_codes"]]
    predictions["confidence"] = 0.0  # Uncalibrated; not the ranking score.
    predictions["decision"] = "review"
    predictions.to_csv("dev_predictions.csv", index=False)
    baseline_predictions = pd.DataFrame(baseline_rows)[["query_id", "top1_code", "top3_codes"]]
    baseline_predictions["confidence"] = 0.50
    baseline_predictions["decision"] = "review"
    baseline_predictions.to_csv(out / "baseline_predictions.csv", index=False)
    (out / "ranking_metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(json.dumps(metrics, indent=2), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", choices=("develop", "validate"), required=True)
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR)
    parser.add_argument("--out-dir", type=Path, default=Path("evaluation"))
    args = parser.parse_args()
    labeled_path = args.data_dir / "queries_labeled.csv"
    queries = pd.read_csv(labeled_path, dtype=str, keep_default_na=False)
    if queries.query_id.duplicated().any() or queries.expected_code.eq("").any():
        raise ValueError("Labeled queries must have unique IDs and nonempty answers")
    catalog = load_catalog(args.data_dir)
    if not set(queries.expected_code) <= set(catalog.by_code):
        raise ValueError("Some labeled answers are not valid catalog codes")
    versions = pd.read_csv(args.data_dir / "versions.csv", dtype=str, keep_default_na=False)
    runner = EvaluationRunner(CatalogRetriever(catalog))
    args.out_dir.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256(labeled_path.read_bytes()).hexdigest()
    if args.phase == "develop":
        develop(queries, versions, runner, args.out_dir, digest)
    else:
        validate(queries, versions, runner, args.out_dir, digest)


if __name__ == "__main__":
    main()
