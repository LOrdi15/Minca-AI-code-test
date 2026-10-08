"""Audit decision thresholds on labeled data only, without changing production.

python -m solution.audit_confidence
"""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from dataclasses import asdict
from pathlib import Path

import numpy as np
import pandas as pd

from score import Prediction, score_row
from solution.decision import ConfidenceModel, DecisionPolicy, THRESHOLDS
from solution.evaluate_decision import (
    grouped_calibration_validation, load_cases, point_estimate_reference,
    select_threshold, summarize_policy,
)


def utility_delta(case, candidate, review) -> float:
    def outcome(decision):
        prediction = Prediction(case.query_id, case.top3_codes[0], case.top3_codes,
                                decision.confidence, decision.decision)
        return score_row(prediction, case.expected_code).utility
    return outcome(candidate) - outcome(review)


def paired_utility_interval(cases, decisions, reviews, comparisons=4) -> dict:
    frame = pd.DataFrame({"group": [case.group for case in cases],
                          "delta": [utility_delta(*values) for values in zip(cases, decisions, reviews)]})
    groups = frame.groupby("group", sort=True).delta.agg(["sum", "count"])
    rng = np.random.default_rng(20261008)
    positions = rng.integers(0, len(groups), size=(20000, len(groups)))
    sampled = groups["sum"].to_numpy()[positions].sum(axis=1) / groups["count"].to_numpy()[positions].sum(axis=1)
    alpha = .05 / comparisons
    return {"delta_mean_utility": float(frame.delta.mean()),
            "paired_group_95_interval": np.quantile(sampled, [.025, .975]).tolist(),
            "multiplicity_adjusted_interval": np.quantile(sampled, [alpha / 2, 1 - alpha / 2]).tolist(),
            "comparisons": comparisons, "groups": len(groups), "resamples": 20000,
            "seed": 20261008}


def main() -> None:
    out = Path("evaluation/confidence_audit")
    out.mkdir(parents=True, exist_ok=True)
    plan = {
        "thresholds": list(THRESHOLDS),
        "families": ["review_all", "protected_wilson", "point_estimate_diagnostic"],
        "development": "174 rows, grouped 4-fold out-of-fold calibration, seed 17",
        "validation": "59 previously inspected cases; development-only calibrator; never used for selection",
        "selection": "Choose the highest development OOF observed utility only for diagnostic comparison; assess original safety requirements and paired grouped utility uncertainty.",
        "uncertainty": "20000 paired group bootstrap samples; 95% and Bonferroni-adjusted intervals for four point thresholds. Descriptive evidence, not a fresh nested evaluation.",
        "limitations": "Ranking already selected using development labels. Holdout already inspected. Bootstrap ignores calibrator refit/threshold-selection uncertainty. No blind data read.",
    }
    (out / "plan.json").write_text(json.dumps(plan, indent=2), encoding="utf-8")
    selection = json.loads(Path("evaluation/ranking_selection.json").read_text(encoding="utf-8"))
    data = Path("data/queries_labeled.csv")
    if hashlib.sha256(data.read_bytes()).hexdigest() != selection["labeled_sha256"]:
        raise ValueError("Labeled data changed")
    queries = pd.read_csv(data, dtype=str, keep_default_na=False)
    cases = load_cases(queries, selection)
    expected = pd.read_csv("evaluation/reassessment/current_predictions.csv", dtype=str).set_index("query_id")
    if any("|".join(case.top3_codes) != expected.loc[case.query_id, "top3_codes"] for case in cases):
        raise ValueError("Ranking differs from the last audited production pipeline")
    development = [case for case in cases if case.query_id in selection["development_ids"]]
    validation = [case for case in cases if case.query_id in selection["validation_ids"]]
    if {case.group for case in development} & {case.group for case in validation}:
        raise ValueError("Split leaks repeated description/year groups")
    model = ConfidenceModel.fit([case.observation() for case in development])
    saved = DecisionPolicy.load()
    if model.bins != saved.model.bins:
        raise ValueError("Recomputed calibration differs from saved model")
    protected, folds, assignments = grouped_calibration_validation(development)
    selected, ledger = select_threshold(development, protected, folds)
    point = {cut: point_estimate_reference(development, protected[cut], cut) for cut in THRESHOLDS}
    point_metrics = {cut: summarize_policy(development, values) for cut, values in point.items()}
    best_point = max(THRESHOLDS, key=lambda cut: (
        point_metrics[cut]["mean_utility"], -point_metrics[cut]["auto_accept_count"], cut))
    # Freeze the diagnostic choice before computing holdout results.
    locked = {"protected_selected": selected, "point_best_observed_oof": best_point,
              "point_is_production_selected": False, "original_selection_ledger": ledger}
    (out / "development_selection.json").write_text(json.dumps(locked, indent=2), encoding="utf-8")
    rows = []
    errors = []
    per_query = []
    for subset, subset_cases in (("development_oof", development), ("previously_inspected_validation", validation),
                                 ("all_full_fit_descriptive", cases), ("all_crossfit_descriptive", cases)):
        if subset == "development_oof":
            decisions_by_cut = protected
        else:
            decisions_by_cut = {cut: [DecisionPolicy(model, cut).decide(case.features) for case in subset_cases]
                                for cut in (None, *THRESHOLDS)}
            if subset == "all_crossfit_descriptive":
                for cut in decisions_by_cut:
                    oof_map = dict(zip((case.query_id for case in development), protected[cut]))
                    decisions_by_cut[cut] = [oof_map.get(case.query_id, decision)
                                            for case, decision in zip(subset_cases, decisions_by_cut[cut])]
        review = decisions_by_cut[None]
        for family, cutoff in (("review_all", None), *(("protected_wilson", cut) for cut in THRESHOLDS),
                               *(("point_estimate_diagnostic", cut) for cut in THRESHOLDS)):
            decisions = decisions_by_cut[cutoff]
            if family == "point_estimate_diagnostic":
                decisions = point_estimate_reference(subset_cases, decisions, cutoff)
            result = {"subset": subset, "family": family, "threshold": cutoff,
                      **summarize_policy(subset_cases, decisions),
                      **paired_utility_interval(subset_cases, decisions, review)}
            if subset == "development_oof":
                result["fold_utility_gains"] = [
                    float(np.mean([utility_delta(case, decision, reference)
                                   for case, decision, reference, assigned in zip(subset_cases, decisions, review, folds)
                                   if assigned == fold])) for fold in sorted(set(folds))]
            rows.append(result)
            if subset in ("development_oof", "previously_inspected_validation"):
                for case, decision, reference in zip(subset_cases, decisions, review):
                    detail = {"query_id": case.query_id, "subset": subset, "family": family, "threshold": cutoff,
                              "expected_code": case.expected_code, "top1_code": case.top3_codes[0],
                              "top3_codes": "|".join(case.top3_codes), "correct": case.correct,
                              "utility_delta_vs_review": utility_delta(case, decision, reference), **asdict(decision)}
                    per_query.append(detail)
                    if decision.decision == "auto_accept" and not case.correct:
                        errors.append(detail)
    distribution = []
    blockers = Counter()
    for case in cases:
        estimate = model.estimate(case.features)
        reasons = case.features.blockers()
        blockers.update(reasons)
        distribution.append({"query_id": case.query_id,
                             "subset": "development" if case.query_id in selection["development_ids"] else "validation",
                             "bucket": case.features.bucket(), "correct": case.correct,
                             "confidence": estimate.confidence, "wilson_lower": estimate.lower_bound,
                             "calibration_groups": estimate.groups, "blockers": "|".join(reasons),
                             "score": case.features.score, "margin": case.features.margin})
    distribution = pd.DataFrame(distribution)
    bucket_summary = distribution.groupby(["subset", "bucket"]).agg(
        count=("query_id", "size"), correct=("correct", "sum"), accuracy=("correct", "mean"),
        confidence=("confidence", "first"), wilson_lower=("wilson_lower", "first")).reset_index()
    metrics = {"plan": plan, "production_threshold": saved.threshold,
               "best_observed_point_threshold_development": best_point,
               "protected_selected": selected, "threshold_results": rows,
               "confidence_buckets": bucket_summary.to_dict("records"),
               "blocker_counts_overlapping": dict(blockers),
               "confidence_at_least_0_80": int(distribution.confidence.ge(.8).sum()),
               "wilson_lower_at_least_0_80": int(distribution.wilson_lower.ge(.8).sum()),
               "ranking_unchanged": True, "production_model_unchanged": True,
               "blind_used": False}
    (out / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    pd.DataFrame(rows).to_csv(out / "thresholds.csv", index=False)
    pd.DataFrame(assignments).to_csv(out / "calibration_folds.csv", index=False)
    distribution.to_csv(out / "confidence_distribution.csv", index=False)
    bucket_summary.to_csv(out / "confidence_buckets.csv", index=False)
    pd.DataFrame(per_query).to_csv(out / "policy_predictions.csv", index=False)
    pd.DataFrame(errors).to_csv(out / "simulated_auto_accept_errors.csv", index=False)
    print(bucket_summary.to_string(index=False))
    print(pd.DataFrame(rows).loc[lambda f: f.subset.isin(("development_oof", "previously_inspected_validation")),
                                ["subset", "family", "threshold", "auto_accept_count", "auto_accept_precision", "mean_utility", "paired_group_95_interval"]].to_string(index=False))
    print("Selected production:", selected, "Best observed diagnostic:", best_point)


if __name__ == "__main__":
    main()
