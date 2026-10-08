import unittest

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

from solution.audit_evaluation import DECIMAL_TOKEN_PATTERN, paired_group_interval


class AuditEvaluationTests(unittest.TestCase):
    def test_trial_keeps_engine_units_and_drivetrain(self):
        tokenize = TfidfVectorizer(token_pattern=DECIMAL_TOKEN_PATTERN, lowercase=False).build_tokenizer()
        self.assertEqual(tokenize("2.0L 5.7L 4X4 2023 F 350"), ["2.0L", "5.7L", "4X4", "2023", "F", "350"])

    def test_paired_interval_does_not_invent_improvement(self):
        result = paired_group_interval(pd.DataFrame({"group": ["A", "A", "B"], "delta": [0, 0, 0]}))
        self.assertEqual(result["group_bootstrap_95_interval"], [0, 0])
        self.assertEqual(result["groups"], 2)

    def test_repeated_rows_keep_their_original_weight(self):
        frame = pd.DataFrame({"group": ["A", "A", "B"], "delta": [.2, .2, -.2]})
        result = paired_group_interval(frame)
        self.assertAlmostEqual(result["delta_mean_utility"], .2 / 3)
        self.assertEqual(result, paired_group_interval(frame))
