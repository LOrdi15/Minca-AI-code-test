import unittest
from dataclasses import replace

from solution.audit_confidence import paired_utility_interval, utility_delta
from solution.decision import Decision, DecisionFeatures
from solution.evaluate_decision import EvaluationCase


class ConfidenceAuditTests(unittest.TestCase):
    def setUp(self):
        self.review = Decision(.85, "review", "test", "strong", 40, .72)
        self.auto = replace(self.review, decision="auto_accept")

    def case(self, identifier, correct):
        return EvaluationCase(identifier, identifier, "AUTO", "A", ("A", "B", "C") if correct else ("B", "A", "C"),
                              DecisionFeatures(.9, .1, .8))

    def test_delta_uses_official_asymmetric_penalties(self):
        self.assertAlmostEqual(utility_delta(self.case("1", True), self.auto, self.review), .85)
        self.assertAlmostEqual(utility_delta(self.case("2", False), self.auto, self.review), -3.15)

    def test_review_reference_has_zero_uncertainty(self):
        cases = [self.case("1", True), self.case("2", False)]
        result = paired_utility_interval(cases, [self.review] * 2, [self.review] * 2)
        self.assertEqual(result["multiplicity_adjusted_interval"], [0, 0])

    def test_adjusted_interval_is_wider_and_reproducible(self):
        cases = [self.case(str(i), i != 0) for i in range(12)]
        result = paired_utility_interval(cases, [self.auto] * 12, [self.review] * 12)
        self.assertLessEqual(result["multiplicity_adjusted_interval"][0], result["paired_group_95_interval"][0])
        self.assertGreaterEqual(result["multiplicity_adjusted_interval"][1], result["paired_group_95_interval"][1])
        self.assertEqual(result, paired_utility_interval(cases, [self.auto] * 12, [self.review] * 12))
