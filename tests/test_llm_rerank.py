import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

from experiments import llm_rerank as experiment


class LLMRerankingTests(unittest.TestCase):
    def request(self, identifier="q1", reserve=.01):
        return {"query_id": identifier, "eligible": True, "request_sha256": "frozen",
                "pool_codes": ["A", "B", "C"], "reserved_max_usd": reserve,
                "messages": [{"role": "user", "content": "vehicle data"}],
                "response_format": experiment.schema(["A", "B", "C"])}

    def test_output_rejects_invented_duplicate_or_nonstring_codes(self):
        for codes in (["A", "B", "FAKE"], ["A", "A", "B"], ["A", "B"], [1, "B", "C"]):
            with self.subTest(codes=codes), self.assertRaises(ValueError):
                experiment.validate_response({"top3_codes": codes, "use_local_order": False}, ["A", "B", "C"])

    def test_abstention_keeps_local_order_and_does_not_claim_confidence(self):
        self.assertIsNone(experiment.validate_response({"top3_codes": ["B", "A", "C"], "use_local_order": True}, ["A", "B", "C"]))
        self.assertEqual(experiment.validate_response({"top3_codes": ["B", "A", "C"], "use_local_order": False}, ["A", "B", "C"]), ["B", "A", "C"])

    def test_schema_limits_response_to_supplied_codes(self):
        schema = experiment.schema(["0001", "B", "C"])["json_schema"]
        self.assertTrue(schema["strict"])
        self.assertEqual(schema["schema"]["properties"]["top3_codes"]["items"]["enum"], ["0001", "B", "C"])

    def test_input_reservation_counts_unicode_bytes_and_schema(self):
        base = experiment.reserve_cost([], experiment.schema(["A", "B", "C"]))
        larger = experiment.reserve_cost([{"role": "user", "content": "Ã¡" * 500}], experiment.schema(["A", "B", "C"]))
        self.assertGreater(larger, base)

    def test_budget_prevents_a_request_before_any_spend(self):
        client = Mock()
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as temp, patch.object(experiment, "OUT", Path(temp)), \
             patch.object(experiment, "load_key", return_value="test-only"), patch("openai.OpenAI", return_value=client):
            experiment.run([self.request(reserve=2.1)], None)
            client.chat.completions.create.assert_not_called()
            self.assertFalse((Path(temp) / "calls.json").exists())

    def test_reservation_precedes_request_and_replay_never_calls_twice(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as temp, patch.object(experiment, "OUT", Path(temp)), \
             patch.object(experiment, "load_key", return_value="test-only"), patch("openai.OpenAI") as sdk:
            def respond(**kwargs):
                record = json.loads((Path(temp) / "calls.json").read_text())["q1"]
                self.assertEqual(record["status"], "pending")
                self.assertEqual(record["budget_charge_usd"], .01)
                self.assertFalse(kwargs["store"])
                self.assertNotIn("query_id", json.dumps(kwargs["messages"]))
                return SimpleNamespace(usage=SimpleNamespace(prompt_tokens=100, completion_tokens=20),
                                       choices=[SimpleNamespace(finish_reason="stop", message=SimpleNamespace(
                                           refusal=None, content='{"top3_codes":["B","A","C"],"use_local_order":false}'))])
            sdk.return_value.chat.completions.create.side_effect = respond
            with contextlib.redirect_stdout(io.StringIO()):
                experiment.run([self.request()], None)
                experiment.run([self.request()], None)
            sdk.return_value.chat.completions.create.assert_called_once()
            record = json.loads((Path(temp) / "calls.json").read_text())["q1"]
            self.assertEqual(record["status"], "success")
            self.assertLess(record["budget_charge_usd"], .01)

    def test_quota_error_stops_without_retry_or_secret_in_logs(self):
        class QuotaError(Exception):
            status_code = 429
            code = "insufficient_quota"
        output = io.StringIO()
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as temp, patch.object(experiment, "OUT", Path(temp)), \
             patch.object(experiment, "load_key", return_value="test-only"), patch("openai.OpenAI") as sdk:
            sdk.return_value.chat.completions.create.side_effect = QuotaError("SECRET_BODY")
            with contextlib.redirect_stdout(output):
                experiment.run([self.request(), self.request("q2")], None)
                experiment.run([self.request(), self.request("q2")], None)
            sdk.return_value.chat.completions.create.assert_called_once()
            self.assertNotIn("SECRET_BODY", output.getvalue())
            record = json.loads((Path(temp) / "calls.json").read_text())["q1"]
            self.assertEqual(record["budget_charge_usd"], .01)
            self.assertEqual(record["status"], "error")
            self.assertEqual(record["api_error_code"], "insufficient_quota")

    def test_invalid_response_retains_usage_and_falls_back(self):
        response = SimpleNamespace(usage=SimpleNamespace(prompt_tokens=100, completion_tokens=20),
                                   choices=[SimpleNamespace(finish_reason="stop", message=SimpleNamespace(
                                       refusal=None, content='{"top3_codes":["FAKE","B","C"],"use_local_order":false}'))])
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as temp, patch.object(experiment, "OUT", Path(temp)), \
             patch.object(experiment, "load_key", return_value="test-only"), patch("openai.OpenAI") as sdk:
            sdk.return_value.chat.completions.create.return_value = response
            with contextlib.redirect_stdout(io.StringIO()):
                experiment.run([self.request()], None)
            record = json.loads((Path(temp) / "calls.json").read_text())["q1"]
            self.assertEqual(record["status"], "error")
            self.assertIsNone(record["top3_codes"])
            self.assertGreater(record["actual_estimated_usd"], 0)
