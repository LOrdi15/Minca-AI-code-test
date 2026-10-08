"""End-to-end output, component reuse, portability and safe fallback checks."""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import pandas as pd

from solution.catalog import load_catalog
from solution.decision import CalibrationBin, ConfidenceModel, Decision, DecisionPolicy
from solution.predict import (
    CHAR_WEIGHT, OUTPUT_COLUMNS, PredictionPipeline, ranking_signature, read_queries,
)
from solution.ranking import RankingWeights
from solution.retrieval import CatalogRetriever


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class PredictionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)
        self.data_dir = self.folder / "data"
        self.data_dir.mkdir()
        pd.DataFrame([("M1", "FORD")], columns=["code", "marca"]).to_csv(self.data_dir / "manufacturers.csv", index=False)
        pd.DataFrame([("S1", "M1", "F350"), ("S2", "M1", "F150")],
                     columns=["code", "manufacturer_key", "submarca"]).to_csv(self.data_dir / "submodels.csv", index=False)
        pd.DataFrame([
            ("001", "S1", "M1", "F350 XLT 4X4 2.0L", "PICK UP", "CARGA"),
            ("001", "S1", "M1", "F350 XLT 4X4 MOTOR 2.0L", "PICK UP", "CARGA"),
            ("002", "S1", "M1", "F350 BASE 4X2 3.0L", "PICK UP", "CARGA"),
            ("003", "S2", "M1", "F150 XL 4X2 5.0L", "PICK UP", "CARGA"),
        ], columns=["code", "submodel_key", "manufacturer_key", "descveh", "tipveh", "cvesegm"]).to_csv(self.data_dir / "versions.csv", index=False)
        pd.DataFrame([("001", "2009"), ("002", "2009"), ("003", "2010")],
                     columns=["code", "modelo"]).to_csv(self.data_dir / "version_years.csv", index=False)
        self.model_path = self.folder / "decision_config.json"
        model = ConfidenceModel({name: CalibrationBin(40, 30) for name in ("blocked", "moderate", "strong")})
        DecisionPolicy(model).save(self.model_path, {"ranking_signature": ranking_signature(RankingWeights(), CHAR_WEIGHT)})
        self.queries = pd.DataFrame([
            {"query_id": "0001", "description": "Ford F350 XLT 4x4 2.0L", "year": "2009", "marca": "FORD"},
            {"query_id": "NA", "description": "*", "year": "", "marca": ""},
        ])

    def pipeline(self, model_path=None):
        return PredictionPipeline(self.data_dir, model_path or self.model_path)

    def assert_valid(self, result):
        self.assertEqual(result.columns.tolist(), list(OUTPUT_COLUMNS))
        self.assertEqual(result.query_id.tolist(), self.queries.query_id.tolist())
        for row in result.to_dict("records"):
            codes = row["top3_codes"].split("|")
            self.assertEqual(len(codes), 3)
            self.assertEqual(len(set(codes)), 3)
            self.assertTrue(set(codes) <= {"001", "002", "003"})
            self.assertEqual(row["top1_code"], codes[0])
            self.assertTrue(0 <= row["confidence"] <= 1)
            self.assertIn(row["decision"], {"review", "auto_accept"})

    def test_csv_ids_and_codes_remain_strings_and_optional_fields_are_filled(self):
        path = self.folder / "queries.csv"
        self.queries.to_csv(path, index=False)
        loaded = read_queries(path)
        self.assertEqual(loaded.query_id.tolist(), ["0001", "NA"])
        self.assertEqual(loaded.submarca.tolist(), ["", ""])
        pipeline = self.pipeline()
        self.assertEqual(pipeline.model_warning, "")
        self.assert_valid(pipeline.predict(loaded))

    def test_catalog_and_index_are_built_once_and_reused_across_rows(self):
        with patch("solution.predict.load_catalog", wraps=load_catalog) as load, \
             patch("solution.predict.CatalogRetriever", wraps=CatalogRetriever) as index:
            pipeline = self.pipeline()
            word_matrix = pipeline.retriever.word_matrix
            char_matrix = pipeline.retriever.char_matrix
            result = pipeline.predict(self.queries)
            self.assert_valid(result)
            self.assertEqual(load.call_count, 1)
            self.assertEqual(index.call_count, 1)
            self.assertIs(pipeline.retriever.word_matrix, word_matrix)
            self.assertIs(pipeline.retriever.char_matrix, char_matrix)

    def test_labels_and_extra_columns_do_not_influence_predictions(self):
        pipeline = self.pipeline()
        first = self.queries.assign(expected_code=["003", "001"], hidden_label="anything")
        second = self.queries.assign(expected_code=["001", "003"], hidden_label="other")
        pd.testing.assert_frame_equal(pipeline.predict(first), pipeline.predict(second))
        with patch.object(pipeline.retriever, "retrieve", wraps=pipeline.retriever.retrieve) as retrieve:
            pipeline.predict(first)
            for call in retrieve.call_args_list:
                self.assertNotIn("expected_code", call.args[0])
                self.assertNotIn("hidden_label", call.args[0])
                self.assertNotIn("query_id", call.args[0])

    def test_failure_in_each_stage_keeps_every_row_and_forces_review(self):
        for stage in ("retrieve", "rank", "decide"):
            with self.subTest(stage=stage):
                pipeline = self.pipeline()
                owner = {"retrieve": pipeline.retriever, "rank": pipeline.ranker, "decide": pipeline.policy}[stage]
                with patch.object(owner, stage, side_effect=RuntimeError("simulated error")):
                    result = pipeline.predict(self.queries)
                self.assert_valid(result)
                self.assertEqual(len(pipeline.fallbacks), 2)
                self.assertTrue(result.decision.eq("review").all())
                self.assertTrue(result.confidence.eq(0).all())

    def test_bad_description_only_falls_back_its_own_row(self):
        pipeline = self.pipeline()
        queries = self.queries.copy()
        queries.loc[0, "description"] = 123
        result = pipeline.predict(queries)
        self.assert_valid(result)
        self.assertEqual(len(pipeline.fallbacks), 1)
        self.assertEqual(result.loc[0, "confidence"], 0)
        self.assertEqual(result.loc[0, "decision"], "review")

    def test_empty_or_malformed_rank_output_still_has_valid_top_three(self):
        for invalid in ([], None):
            with self.subTest(invalid=invalid):
                pipeline = self.pipeline()
                with patch.object(pipeline.ranker, "rank", return_value=invalid):
                    result = pipeline.predict(self.queries)
                self.assert_valid(result)
                self.assertEqual(len(pipeline.fallbacks), 2)

    def test_invalid_confidence_or_decision_cannot_reach_the_csv(self):
        invalids = (
            Decision(float("nan"), "review", "test", "strong", 40, 0.9),
            Decision(float("inf"), "auto_accept", "test", "strong", 40, 0.9),
            Decision(1.1, "review", "test", "strong", 40, 0.9),
            Decision(0.8, "accept", "test", "strong", 40, 0.9),
            Decision(0.8, "auto_accept", "test", "strong", 40, 0.9),
        )
        for invalid in invalids:
            with self.subTest(invalid=invalid):
                pipeline = self.pipeline()
                with patch.object(pipeline.policy, "decide", return_value=invalid):
                    result = pipeline.predict(self.queries)
                self.assert_valid(result)
                self.assertTrue(result.decision.eq("review").all())
                self.assertTrue(result.confidence.eq(0).all())

    def test_missing_or_stale_calibrator_fails_closed_to_review(self):
        stale = self.folder / "stale.json"
        payload = json.loads(self.model_path.read_text())
        payload["metadata"]["ranking_signature"] = "wrong-ranking"
        stale.write_text(json.dumps(payload))
        for path in (self.folder / "missing.json", stale):
            with self.subTest(path=path):
                pipeline = self.pipeline(path)
                self.assertTrue(pipeline.model_warning)
                result = pipeline.predict(self.queries)
                self.assert_valid(result)
                self.assertTrue(result.decision.eq("review").all())

    def test_ids_that_cannot_be_scored_are_rejected_before_inference(self):
        for ids in (["", "NA"], ["1", " 1 "], ["1", "1"]):
            with self.subTest(ids=ids):
                path = self.folder / "queries.csv"
                self.queries.assign(query_id=ids).to_csv(path, index=False)
                with self.assertRaisesRegex(ValueError, "nonempty and unique"):
                    read_queries(path)

    def test_cli_runs_without_openai_key_and_writes_exact_schema(self):
        queries_path = self.folder / "queries.csv"
        out = self.folder / "result.csv"
        self.queries.to_csv(queries_path, index=False)
        env = {key: value for key, value in os.environ.items() if key != "OPENAI_API_KEY"}
        result = subprocess.run([
            sys.executable, "-m", "solution.predict", "--queries", str(queries_path), "--out", str(out),
            "--data-dir", str(self.data_dir), "--decision-model", str(self.model_path),
        ], cwd=PROJECT_ROOT, env=env, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        summary = json.loads(result.stdout)
        self.assertEqual(summary["fallback_rows"], 0)
        self.assertFalse(summary["calibration_fallback"])
        self.assertEqual(summary["llm_calls"], 0)
        loaded = pd.read_csv(out, dtype={"query_id": str, "top1_code": str, "top3_codes": str}, keep_default_na=False)
        self.assert_valid(loaded)


if __name__ == "__main__":
    unittest.main()
