"""Conservative confidence, utility, support and decision validation checks."""
import tempfile
import unittest
import json
from dataclasses import replace
from pathlib import Path

import numpy as np

from solution.decision import (
    CalibrationBin, CalibrationObservation, ConfidenceModel,
    Decision, DecisionFeatures, DecisionPolicy, THRESHOLDS, wilson_lower,
)
from solution.evaluate_decision import (
    EvaluationCase, grouped_calibration_validation, point_estimate_reference,
    select_threshold, summarize_policy,
)
from solution.ranking import RankedCandidate


def strong_features(**changes):
    base = DecisionFeatures(score=0.9, margin=0.12, tfidf_score=0.8,
                            year_match=True, manufacturer_match=True)
    return replace(base, **changes)


class ConfidenceTests(unittest.TestCase):
    def test_confidence_comes_from_observed_outcomes_not_similarity(self):
        features = strong_features(score=0.8)
        model = ConfidenceModel.fit([
            CalibrationObservation(features, True, str(i)) for i in range(30)
        ])
        estimate = model.estimate(features)
        self.assertAlmostEqual(estimate.confidence, 31 / 32)
        self.assertNotEqual(estimate.confidence, features.score)
        self.assertLess(estimate.confidence, 1)
        self.assertGreater(estimate.lower_bound, 0.85)

    def test_duplicates_do_not_inflate_calibration_support(self):
        model = ConfidenceModel.fit([
            CalibrationObservation(strong_features(), True, "same-query") for _ in range(100)
        ])
        estimate = model.estimate(strong_features())
        self.assertEqual(estimate.groups, 1)
        self.assertEqual(DecisionPolicy(model, 0.8).decide(strong_features()).decision, "review")

    def test_a_group_with_any_error_is_not_counted_as_a_success(self):
        model = ConfidenceModel.fit([
            CalibrationObservation(strong_features(), True, "same-query"),
            CalibrationObservation(strong_features(), False, "same-query"),
        ])
        self.assertEqual(model.estimate(strong_features()).correct_groups, 0)

    def test_unseen_bucket_has_a_prior_but_no_empirical_support(self):
        estimate = ConfidenceModel({}).estimate(strong_features())
        self.assertEqual(estimate.confidence, 0.5)
        self.assertEqual(estimate.lower_bound, 0)
        self.assertEqual(estimate.groups, 0)

    def test_wilson_bound_and_invalid_counts(self):
        self.assertEqual(wilson_lower(0, 0), 0)
        self.assertLess(wilson_lower(5, 5), 0.8)
        self.assertGreater(wilson_lower(30, 30), 0.85)
        for correct, total in ((2, 1), (-1, 5), (0, -1)):
            with self.subTest(correct=correct, total=total):
                with self.assertRaises(ValueError):
                    wilson_lower(correct, total)


class DecisionTests(unittest.TestCase):
    def setUp(self):
        self.model = ConfidenceModel({"strong": CalibrationBin(50, 50), "blocked": CalibrationBin(50, 50)})

    def test_safe_default_is_review_even_with_high_confidence(self):
        result = DecisionPolicy(self.model).decide(strong_features())
        self.assertEqual(result.decision, "review")
        self.assertEqual(result.reason, "review_only_selected")

    def test_supported_compatible_case_can_be_accepted(self):
        result = DecisionPolicy(self.model, 0.9).decide(strong_features())
        self.assertEqual(result.decision, "auto_accept")
        self.assertEqual(result.calibration_groups, 50)

    def test_high_similarity_without_support_requires_review(self):
        model = ConfidenceModel({"strong": CalibrationBin(5, 5)})
        result = DecisionPolicy(model, 0.8).decide(strong_features(score=1.1))
        self.assertEqual(result.decision, "review")
        self.assertEqual(result.reason, "insufficient_calibration_groups")

    def test_point_estimate_above_threshold_is_not_enough(self):
        model = ConfidenceModel({"strong": CalibrationBin(20, 18)})
        result = DecisionPolicy(model, 0.8).decide(strong_features())
        self.assertGreater(result.confidence, 0.8)
        self.assertLess(result.precision_lower_bound, 0.8)
        self.assertEqual(result.decision, "review")

    def test_each_known_attribute_conflict_blocks_acceptance(self):
        for attribute in ("year", "manufacturer", "submodel", "vehicle_type"):
            with self.subTest(attribute=attribute):
                result = DecisionPolicy(self.model, 0.8).decide(strong_features(conflicts=(attribute,)))
                self.assertEqual(result.decision, "review")
                self.assertIn("attribute_conflict", result.reason)

    def test_missing_or_ambiguous_evidence_blocks_acceptance(self):
        variations = (
            {"catalog_ambiguous": True}, {"description_informative": False},
            {"catalog_relations_complete": False},
            {"candidate_count": 1}, {"tfidf_score": 0}, {"year_match": False},
            {"manufacturer_match": False}, {"score": 0.54}, {"margin": 0.029},
        )
        for changes in variations:
            with self.subTest(changes=changes):
                self.assertEqual(DecisionPolicy(self.model, 0.8).decide(strong_features(**changes)).decision, "review")

    def test_score_and_margin_both_define_evidence_bucket(self):
        self.assertEqual(strong_features().bucket(), "strong")
        self.assertEqual(strong_features(score=0.65).bucket(), "moderate")
        self.assertEqual(strong_features(margin=0.04).bucket(), "moderate")

    def test_invalid_parameters_and_scores_are_rejected(self):
        for threshold in (0.5, 1.1, float("nan")):
            with self.assertRaises(ValueError):
                DecisionPolicy(self.model, threshold)
        with self.assertRaises(ValueError):
            DecisionPolicy(self.model, 0.8, min_groups=0)
        for changes in ({"score": float("nan")}, {"margin": -1}, {"tfidf_score": float("inf")}):
            with self.assertRaises(ValueError):
                strong_features(**changes)

    def test_saved_policy_round_trips(self):
        policy = DecisionPolicy(self.model, 0.85)
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "policy.json"
            policy.save(path, {"note": "test"})
            loaded = DecisionPolicy.load(path)
            self.assertEqual(loaded.decide(strong_features()), policy.decide(strong_features()))

    def test_a_model_with_different_bucket_rules_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "policy.json"
            DecisionPolicy(self.model, 0.85).save(path)
            payload = json.loads(path.read_text())
            payload["evidence_rules"]["min_score"] = 0.1
            path.write_text(json.dumps(payload))
            with self.assertRaisesRegex(ValueError, "rules differ"):
                DecisionPolicy.load(path)

    def test_features_use_distinct_runner_up_and_structured_compatibility(self):
        top = RankedCandidate("A", 0.9, 0.8, 0.9, 2, {}, (), False,
                              {"year": "match", "vehicle_type": "match"})
        second = RankedCandidate("B", 0.8, 0.7, 0.9, 3, {}, (), False)
        features = DecisionFeatures.from_ranked({"description": "FORD F350"}, [top, second])
        self.assertAlmostEqual(features.margin, 0.1)
        self.assertTrue(features.year_match)
        self.assertTrue(features.vehicle_type_match)
        self.assertEqual(features.blockers(), ())
        empty = DecisionFeatures.from_ranked({"description": "*"}, [top, second])
        self.assertIn("missing_informative_description", empty.blockers())
        with self.assertRaises(ValueError):
            DecisionFeatures.from_ranked({}, [top, top])
        with self.assertRaises(ValueError):
            DecisionFeatures.from_ranked({}, [second, top])

    def test_compatibility_conflict_cannot_be_hidden_by_an_empty_conflicts_list(self):
        top = RankedCandidate("A", 0.9, 0.8, 0.9, 2, {}, (), False,
                              {"year": "match", "manufacturer": "conflict", "vehicle_type": "match"})
        second = RankedCandidate("B", 0.7, 0.6, 0.9, 3, {}, (), False)
        features = DecisionFeatures.from_ranked({"description": "FORD PICKUP"}, [top, second])
        self.assertIn("manufacturer", features.conflicts)
        self.assertEqual(DecisionPolicy(self.model, 0.8).decide(features).decision, "review")


class DecisionEvaluationTests(unittest.TestCase):
    def case(self, query_id, correct=True, in_top3=True, group=None):
        return EvaluationCase(query_id, group or query_id, "AUTO", "A",
                              ("A", "B", "C") if correct else (("B", "A", "C") if in_top3 else ("B", "C", "D")),
                              strong_features())

    def test_utility_matches_the_four_official_outcomes(self):
        cases = [self.case("1"), self.case("2", False), self.case("3", False), self.case("4", False, False)]
        decisions = [Decision(0.9, decision, "test", "strong", 50, 0.8)
                     for decision in ("auto_accept", "auto_accept", "review", "review")]
        metrics = summarize_policy(cases, decisions)
        self.assertAlmostEqual(metrics["mean_utility"], (1 - 3 + 0.15 - 0.05) / 4)
        self.assertEqual(metrics["auto_accept_precision"], 0.5)
        self.assertEqual(metrics["review_rate"], 0.5)
        self.assertEqual(metrics["top3_recall"], 0.75)

    def test_small_lucky_validation_sample_does_not_enable_automation(self):
        cases = [self.case(str(i)) for i in range(5)]
        model = ConfidenceModel({"strong": CalibrationBin(50, 50)})
        decisions = {threshold: [DecisionPolicy(model, threshold).decide(case.features) for case in cases]
                     for threshold in (None, *THRESHOLDS)}
        selected, _ = select_threshold(cases, decisions, np.array([0, 1, 2, 3, 0]))
        self.assertIsNone(selected)

    def test_point_estimate_diagnostic_does_not_change_protected_decisions(self):
        cases = [self.case("1")]
        model = ConfidenceModel({"strong": CalibrationBin(20, 18)})
        protected = [DecisionPolicy(model, 0.8).decide(cases[0].features)]
        diagnostic = point_estimate_reference(cases, protected, 0.8)
        self.assertEqual(protected[0].decision, "review")
        self.assertEqual(diagnostic[0].decision, "auto_accept")
        self.assertEqual(diagnostic[0].reason, "diagnostic_point_estimate_only")

    def test_a_harmful_fold_prevents_selection_despite_positive_average_gain(self):
        cases = [self.case(str(i), correct=i not in (0, 4, 8)) for i in range(40)]
        model = ConfidenceModel({"strong": CalibrationBin(50, 50)})
        decisions = {threshold: [DecisionPolicy(model, threshold).decide(case.features) for case in cases]
                     for threshold in (None, *THRESHOLDS)}
        selected, ledger = select_threshold(cases, decisions, np.arange(40) % 4)
        candidate = next(row for row in ledger if row["threshold"] == 0.8)
        self.assertGreater(candidate["mean_utility"], 0.15)
        self.assertGreater(candidate["auto_accept_precision_lower_bound"], 0.80)
        self.assertLess(candidate["min_fold_utility_gain"], 0)
        self.assertIsNone(selected)

    def test_supported_consistent_validation_gains_can_enable_automation(self):
        cases = [self.case(str(i)) for i in range(40)]
        model = ConfidenceModel({"strong": CalibrationBin(50, 50)})
        decisions = {threshold: [DecisionPolicy(model, threshold).decide(case.features) for case in cases]
                     for threshold in (None, *THRESHOLDS)}
        selected, _ = select_threshold(cases, decisions, np.arange(40) % 4)
        self.assertEqual(selected, 0.9)

    def test_grouped_oof_never_counts_validation_groups_as_training_support(self):
        cases = [self.case(str(i), group=str(i // 2)) for i in range(80)]
        decisions, folds, assignments = grouped_calibration_validation(cases)
        groups = {}
        for assignment in assignments:
            groups.setdefault(assignment["group"], set()).add(assignment["fold"])
        self.assertTrue(all(len(group_folds) == 1 for group_folds in groups.values()))
        self.assertTrue(all(decision.calibration_groups < 40 for decision in decisions[0.8]))
        self.assertEqual(len(folds), len(cases))


if __name__ == "__main__":
    unittest.main()
