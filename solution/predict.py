"""End-to-end inference with frozen ranking and decision configuration.

    python -m solution.predict --queries data/queries_blind.csv --out predictions.csv

No labels, evaluation artifacts, environment secrets or external APIs are read.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
import time
from dataclasses import asdict
from pathlib import Path
from typing import Mapping

import pandas as pd

from solution.catalog import load_catalog
from solution.decision import DEFAULT_MODEL_PATH, ConfidenceModel, DecisionFeatures, DecisionPolicy
from solution.normalization import QUERY_TEXT_COLUMNS, normalize_text
from solution.ranking import CandidateRanker, RankingWeights
from solution.retrieval import CatalogRetriever


OUTPUT_COLUMNS = ("query_id", "top1_code", "top3_codes", "confidence", "decision")
QUERY_FIELDS = ("description", "year", "marca", "submarca", "tipveh", "segment")
CHAR_WEIGHT = 0.35


def ranking_signature(weights: RankingWeights, char_weight: float, integral_values: bool = False) -> str:
    """Allow numerically equivalent JSON weights (0 and 0.0) in saved metadata."""
    values = asdict(weights)
    if integral_values:
        values = {key: int(value) if float(value).is_integer() else value for key, value in values.items()}
    text = json.dumps({"weights": values, "char_weight": char_weight}, sort_keys=True)
    return hashlib.sha256(text.encode()).hexdigest()


def _validate_ids(queries: pd.DataFrame) -> None:
    if "query_id" not in queries:
        raise ValueError("Queries must contain query_id")
    if queries.empty:
        raise ValueError("Queries CSV contains no rows")
    if not queries.query_id.map(lambda value: isinstance(value, str)).all():
        raise ValueError("query_id values must be strings")
    stripped = queries.query_id.str.strip()
    if stripped.eq("").any() or stripped.duplicated().any():
        raise ValueError("query_id values must be nonempty and unique, including after trimming")


def read_queries(path: str | Path) -> pd.DataFrame:
    """Preserve string IDs and only retain observable input fields."""
    queries = pd.read_csv(path, dtype=str, keep_default_na=False, encoding="utf-8-sig")
    _validate_ids(queries)
    for field in QUERY_FIELDS:
        if field not in queries:
            queries[field] = ""
    return queries[["query_id", *QUERY_FIELDS]].copy()


def prepare_query(row: Mapping) -> dict[str, str]:
    """Apply the shared, idempotent rules; omit IDs, labels and extra columns."""
    observable = {field: normalize_text(row.get(field, "")) for field in QUERY_TEXT_COLUMNS}
    observable["year"] = row.get("year", "")
    return observable


class PredictionPipeline:
    def __init__(self, data_dir: str | Path = "data", decision_model: str | Path = DEFAULT_MODEL_PATH):
        start = time.perf_counter()
        self.catalog = load_catalog(data_dir)
        if len(self.catalog.by_code) < 3:
            raise ValueError("At least three distinct catalog codes are needed for a valid top-3")
        catalog_end = time.perf_counter()
        self.retriever = CatalogRetriever(self.catalog)
        self.ranker = CandidateRanker(self.retriever)
        self.weights = RankingWeights()
        self.valid_codes = set(self.catalog.by_code)
        self.fallback_codes = sorted(self.valid_codes)[:3]
        self.initialization_seconds = {
            "catalog": catalog_end - start,
            "indexes_and_ranker": time.perf_counter() - catalog_end,
        }
        self.model_warning = ""
        try:
            metadata = json.loads(Path(decision_model).read_text(encoding="utf-8")).get("metadata", {})
            signatures = {ranking_signature(self.weights, CHAR_WEIGHT, integral) for integral in (False, True)}
            if metadata.get("ranking_signature") not in signatures:
                raise ValueError("Decision model does not match the frozen ranking weights")
            self.policy = DecisionPolicy.load(decision_model)
        except (OSError, ValueError, KeyError, TypeError) as error:
            # A missing/stale calibrator never enables automation or prevents
            # valid predictions; report it and use an unsupported-prior review.
            self.model_warning = f"{type(error).__name__}: {error}"
            self.policy = DecisionPolicy(ConfidenceModel({}))
        self.fallbacks: list[dict[str, str]] = []

    def _check_codes(self, codes: list[str]) -> None:
        if len(codes) != 3 or len(set(codes)) != 3 or not set(codes) <= self.valid_codes:
            raise ValueError("Prediction must contain three distinct valid catalog codes")

    def _fallback(self, query_id: str, ranked, retrieved, error: Exception) -> dict:
        codes = []
        # Keep useful candidates already produced, then fill deterministic valid
        # codes. This is formatting continuity, not an evidence-based match.
        ranked_items = ranked if isinstance(ranked, (list, tuple)) else []
        retrieved_items = retrieved if isinstance(retrieved, (list, tuple)) else []
        for item in [*ranked_items, *retrieved_items, *self.fallback_codes]:
            code = item if isinstance(item, str) else getattr(item, "code", None)
            if isinstance(code, str) and code in self.valid_codes and code not in codes:
                codes.append(code)
            if len(codes) == 3:
                break
        self._check_codes(codes)
        self.fallbacks.append({"query_id": query_id, "error": f"{type(error).__name__}: {error}"})
        return {"query_id": query_id, "top1_code": codes[0], "top3_codes": "|".join(codes),
                "confidence": 0.0, "decision": "review"}

    def predict(self, queries: pd.DataFrame) -> pd.DataFrame:
        """Produce exactly one row per input, in original order, using one index."""
        _validate_ids(queries)
        self.fallbacks = []
        predictions = []
        for row in queries.to_dict("records"):
            ranked, retrieved = [], []
            try:
                observable = prepare_query(row)
                retrieved = self.retriever.retrieve(observable, k=50, char_weight=CHAR_WEIGHT)
                ranked = self.ranker.rank(observable, retrieved, self.weights, top_k=3)
                codes = [candidate.code for candidate in ranked]
                self._check_codes(codes)
                features = DecisionFeatures.from_ranked(observable, ranked)
                decision = self.policy.decide(features)
                confidence = float(decision.confidence)
                if not math.isfinite(confidence) or not 0 <= confidence <= 1:
                    raise ValueError("Decision confidence must be finite and in [0, 1]")
                if decision.decision not in {"auto_accept", "review"}:
                    raise ValueError("Unknown decision")
                if decision.decision == "auto_accept" and (features.blockers() or self.policy.threshold is None):
                    raise ValueError("Acceptance contradicts the configured policy")
                predictions.append({
                    "query_id": row["query_id"], "top1_code": codes[0], "top3_codes": "|".join(codes),
                    "confidence": confidence, "decision": decision.decision,
                })
            except Exception as error:
                # A row-level failure is visible in the summary, never silently
                # skipped, and cannot result in an automatic acceptance.
                predictions.append(self._fallback(row["query_id"], ranked, retrieved, error))
        return pd.DataFrame(predictions, columns=OUTPUT_COLUMNS)


def main() -> None:
    started = time.perf_counter()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--queries", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--data-dir", type=Path, default=Path("data"))
    parser.add_argument("--decision-model", type=Path, default=DEFAULT_MODEL_PATH)
    args = parser.parse_args()
    protected_inputs = [args.queries, args.decision_model, *(args.data_dir / name for name in (
        "versions.csv", "manufacturers.csv", "submodels.csv", "version_years.csv",
    ))]
    if args.out.resolve() in {path.resolve() for path in protected_inputs}:
        parser.error("Output must not overwrite a query, catalog or decision-model input")
    try:
        queries = read_queries(args.queries)
        pipeline = PredictionPipeline(args.data_dir, args.decision_model)
        inference_started = time.perf_counter()
        predictions = pipeline.predict(queries)
        inference_seconds = time.perf_counter() - inference_started
        args.out.parent.mkdir(parents=True, exist_ok=True)
        predictions.to_csv(args.out, index=False, encoding="utf-8")
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.exit(1, f"Prediction failed: {error}\n")
    if pipeline.model_warning:
        print(f"Calibration fallback: {pipeline.model_warning}", file=sys.stderr)
    for fallback in pipeline.fallbacks[:5]:
        print(f"Row fallback: {fallback['query_id']}: {fallback['error']}", file=sys.stderr)
    print(json.dumps({
        "out": str(args.out), "rows": len(predictions),
        "decisions": predictions.decision.value_counts().to_dict(),
        "fallback_rows": len(pipeline.fallbacks), "calibration_fallback": bool(pipeline.model_warning),
        "seconds": {**pipeline.initialization_seconds, "inference": inference_seconds,
                    "total": time.perf_counter() - started},
        "llm_calls": 0,
    }, indent=2))


if __name__ == "__main__":
    main()
