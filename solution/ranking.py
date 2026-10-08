"""Explainable reranking. Scores are not probabilities or auto-accept decisions."""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Mapping, Sequence

from rapidfuzz import fuzz, process

from solution.normalization import normalize_text
from solution.retrieval import Candidate, CatalogRetriever, query_text


@dataclass(frozen=True)
class RankingWeights:
    # Selected on development: TF-IDF leads; fuzzy similarity is a small nudge.
    tfidf: float = 0.90
    fuzzy: float = 0.10
    year_bonus: float = 0.12
    year_penalty: float = 0.20
    manufacturer_bonus: float = 0.02
    manufacturer_penalty: float = 0.10
    submodel_bonus: float = 0.02
    submodel_penalty: float = 0.05
    # Type scoring hurt development. Still flag incompatibilities for review.
    type_bonus: float = 0.0
    type_penalty: float = 0.0

    def __post_init__(self):
        if any(value < 0 for value in self.__dict__.values()):
            raise ValueError("Weights cannot be negative")
        if abs(self.tfidf + self.fuzzy - 1.0) > 1e-9:
            raise ValueError("Text weights must sum to 1")


@dataclass(frozen=True)
class RankedCandidate:
    code: str
    score: float
    tfidf_score: float
    fuzzy_score: float
    source_row: int
    contributions: dict[str, float]
    conflicts: tuple[str, ...]
    catalog_ambiguous: bool

    @property
    def needs_review(self) -> bool:
        return bool(self.conflicts or self.catalog_ambiguous or self.tfidf_score == 0)


def vehicle_category(text: str) -> str | None:
    """Coarse taxonomy alignment, not text aliases. Unknown values stay unknown.

    TOLVA, CAJA and CAMIONETA are deliberately not assumed to be one type.
    """
    tokens = set(normalize_text(text).split())
    if tokens & {"TRACTO", "TRACTOCAMION", "TRACTOCAMIONES"}:
        return "TRACTO"
    if tokens & {"REMOLQUE", "REMOLQUES", "SEMIREMOLQUE"}:
        return "REMOLQUE"
    if "PICKUP" in tokens or {"PICK", "UP"} <= tokens:
        return "PICKUP"
    if tokens & {"AUTO", "AUTOS", "AUTOMOVIL"}:
        return "AUTO"
    if tokens & {"CAMION", "CAMIONES"}:
        return "CAMION"
    return None


def _resolve_name(raw: str, choices: Sequence[str]) -> str | None:
    """Recognize known names conservatively, without a hand-written alias map."""
    text = normalize_text(raw)
    if not text or not choices:
        return None
    if text in choices:
        return text
    contained = [name for name in choices if len(name) >= 3 and f" {name} " in f" {text} "]
    if len(contained) == 1:
        return contained[0]
    if len(contained) > 1:
        return None  # e.g. CHRYSLER - JEEP: do not invent a single manufacturer.
    closest = process.extract(text, choices, scorer=fuzz.ratio, limit=2)
    if closest and closest[0][1] >= 90 and (len(closest) == 1 or closest[0][1] - closest[1][1] >= 10):
        return closest[0][0]
    return None


class CandidateRanker:
    def __init__(self, retriever: CatalogRetriever):
        self.retriever = retriever
        self.rows = list(retriever.rows.itertuples(index=False))
        self.manufacturers = sorted({row.marca_normalized for row in self.rows if row.marca_normalized})
        self.models_by_manufacturer: dict[str, list[str]] = {}
        for manufacturer in self.manufacturers:
            self.models_by_manufacturer[manufacturer] = sorted({
                row.submarca_normalized for row in self.rows
                if row.marca_normalized == manufacturer and row.submarca_normalized
            })
        self.all_models = sorted({row.submarca_normalized for row in self.rows if row.submarca_normalized})

    def rank(
        self, query: Mapping[str, str], candidates: Sequence[Candidate],
        weights: RankingWeights = RankingWeights(), top_k: int = 3,
    ) -> list[RankedCandidate]:
        """Score whole variants, then choose the best variant per code.

        Never combine a description from one variant with metadata from another.
        Missing/uncertain input is neutral. Known contradictions incur penalties
        and remain visible to any future acceptance policy.
        """
        if top_k < 1:
            raise ValueError("top_k must be positive")
        text = query_text(query)
        manufacturer = _resolve_name(query.get("marca", ""), self.manufacturers)
        models = self.models_by_manufacturer.get(manufacturer, self.all_models)
        submodel = _resolve_name(query.get("submarca", ""), models)
        year_text = query.get("year", "")
        year = int(year_text) if isinstance(year_text, str) and re.fullmatch(r"[0-9]{4}", year_text) else None
        category = vehicle_category(query.get("tipveh", ""))
        if category is None:
            category = vehicle_category(query.get("segment", ""))
        ranked: dict[str, RankedCandidate] = {}
        for candidate in candidates:
            for index, tfidf_score in candidate.variant_scores:
                row = self.rows[index]
                if row.code != candidate.code:
                    raise ValueError("Candidate variant does not belong to its code")
                fuzzy_score = fuzz.WRatio(text, self.retriever.texts[index]) / 100 if text else 0.0
                contributions = {"tfidf": weights.tfidf * tfidf_score, "fuzzy": weights.fuzzy * fuzzy_score}
                conflicts = []
                for name, expected, actual, bonus, penalty in (
                    ("manufacturer", manufacturer, row.marca_normalized, weights.manufacturer_bonus, weights.manufacturer_penalty),
                    ("submodel", submodel, row.submarca_normalized, weights.submodel_bonus, weights.submodel_penalty),
                    ("vehicle_type", category, vehicle_category(row.tipveh), weights.type_bonus, weights.type_penalty),
                ):
                    contributions[name] = 0.0
                    if expected and actual:
                        matches = expected == actual
                        contributions[name] = bonus if matches else -penalty
                        if not matches:
                            conflicts.append(name)
                contributions["year"] = 0.0
                if year is not None and row.valid_years:
                    matches = year in row.valid_years
                    contributions["year"] = weights.year_bonus if matches else -weights.year_penalty
                    if not matches:
                        conflicts.append("year")
                entry = self.retriever.catalog.by_code[candidate.code]
                ambiguous = len(entry.manufacturers) > 1 or len(entry.submodels) > 1 or len(entry.vehicle_types) > 1
                result = RankedCandidate(
                    candidate.code, sum(contributions.values()), tfidf_score, fuzzy_score,
                    row.source_row, contributions, tuple(conflicts), ambiguous,
                )
                previous = ranked.get(candidate.code)
                if previous is None or result.score > previous.score:
                    ranked[candidate.code] = result
        return sorted(ranked.values(), key=lambda item: (-item.score, item.code))[:top_k]
