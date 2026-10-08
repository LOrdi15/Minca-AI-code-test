"""Evidence-based confidence and conservative review/auto-accept decisions.

Confidence is a smoothed observed success rate in a fixed evidence bucket, not
the ranking similarity. Acceptance additionally requires independent-group
support and a Wilson lower confidence bound exceeding the chosen threshold.
"""
from __future__ import annotations

import json
import math
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Mapping, Sequence

from solution.normalization import normalize_text
from solution.ranking import RankedCandidate


DEFAULT_MODEL_PATH = Path(__file__).with_name("decision_config.json")
MIN_CALIBRATION_GROUPS = 20
THRESHOLDS = (0.80, 0.85, 0.90, 0.95)
EVIDENCE_RULES = {"min_score": 0.55, "min_margin": 0.03, "strong_score": 0.75, "strong_margin": 0.08}


@dataclass(frozen=True)
class DecisionFeatures:
    score: float
    margin: float
    tfidf_score: float
    conflicts: tuple[str, ...] = ()
    catalog_ambiguous: bool = False
    description_informative: bool = True
    candidate_count: int = 3
    year_match: bool = False
    manufacturer_match: bool = False
    submodel_match: bool = False
    vehicle_type_match: bool = False
    catalog_relations_complete: bool = True

    def __post_init__(self):
        if not all(math.isfinite(value) for value in (self.score, self.margin, self.tfidf_score)):
            raise ValueError("Decision scores must be finite")
        if self.margin < 0 or self.tfidf_score < 0 or self.candidate_count < 1:
            raise ValueError("Invalid ranking evidence")

    @classmethod
    def from_ranked(cls, query: Mapping[str, str], ranked: Sequence[RankedCandidate]) -> DecisionFeatures:
        if not ranked:
            raise ValueError("Cannot decide without candidates")
        if len({item.code for item in ranked}) != len(ranked):
            raise ValueError("Decision candidates must have distinct codes")
        if any(left.score < right.score for left, right in zip(ranked, ranked[1:])):
            raise ValueError("Decision candidates must be ranked best first")
        top = ranked[0]
        normalized_description = normalize_text(query.get("description", ""))
        compatibility = top.compatibility
        return cls(
            score=top.score, margin=top.score - ranked[1].score if len(ranked) > 1 else 0.0,
            tfidf_score=top.tfidf_score,
            conflicts=tuple(sorted(set(top.conflicts) | {name for name, state in compatibility.items() if state == "conflict"})),
            catalog_ambiguous=top.catalog_ambiguous,
            description_informative=bool(re.search(r"[A-Z]", normalized_description)),
            candidate_count=len(ranked), year_match=compatibility.get("year") == "match",
            manufacturer_match=compatibility.get("manufacturer") == "match",
            submodel_match=compatibility.get("submodel") == "match",
            vehicle_type_match=compatibility.get("vehicle_type") == "match",
            catalog_relations_complete=top.catalog_relations_complete,
        )

    def blockers(self) -> tuple[str, ...]:
        """Predefined safety rules, independent of query answers or segment labels."""
        reasons = []
        if self.conflicts:
            reasons.append("attribute_conflict")
        if self.catalog_ambiguous:
            reasons.append("ambiguous_catalog")
        if not self.catalog_relations_complete:
            reasons.append("incomplete_catalog_relations")
        if not self.description_informative:
            reasons.append("missing_informative_description")
        if self.candidate_count < 2:
            reasons.append("missing_runner_up")
        if self.tfidf_score <= 0:
            reasons.append("no_text_evidence")
        if not self.year_match:
            reasons.append("year_not_confirmed")
        if not (self.manufacturer_match or self.submodel_match or self.vehicle_type_match):
            reasons.append("no_confirmed_attribute")
        if self.score < EVIDENCE_RULES["min_score"]:
            reasons.append("low_score")
        if self.margin < EVIDENCE_RULES["min_margin"]:
            reasons.append("small_margin")
        return tuple(reasons)

    def bucket(self) -> str:
        if self.blockers():
            return "blocked"
        return "strong" if self.score >= EVIDENCE_RULES["strong_score"] and self.margin >= EVIDENCE_RULES["strong_margin"] else "moderate"


def wilson_lower(correct: int, total: int, z: float = 1.96) -> float:
    """Lower endpoint of a 95% Wilson interval; not a distribution-shift guarantee."""
    if total < 0 or correct < 0 or correct > total:
        raise ValueError("Invalid calibration counts")
    if total == 0:
        return 0.0
    rate = correct / total
    z2 = z * z
    return max(0.0, (
        rate + z2 / (2 * total) - z * math.sqrt(rate * (1 - rate) / total + z2 / (4 * total * total))
    ) / (1 + z2 / total))


@dataclass(frozen=True)
class CalibrationBin:
    groups: int
    correct_groups: int

    def __post_init__(self):
        if self.groups < 0 or not 0 <= self.correct_groups <= self.groups:
            raise ValueError("Invalid calibration bin counts")

    @property
    def confidence(self) -> float:
        # Beta(1,1) smoothing prevents claiming confidence 1.0 from finite data.
        return (self.correct_groups + 1) / (self.groups + 2)

    @property
    def lower_bound(self) -> float:
        return wilson_lower(self.correct_groups, self.groups)


@dataclass(frozen=True)
class CalibrationObservation:
    features: DecisionFeatures
    correct: bool
    group: str


@dataclass
class ConfidenceModel:
    bins: dict[str, CalibrationBin]

    @classmethod
    def fit(cls, observations: Sequence[CalibrationObservation]) -> ConfidenceModel:
        # Repeated queries cannot inflate support. A group is a success only if
        # every observed row of that group in this bucket was correct.
        grouped: dict[str, dict[str, list[bool]]] = {}
        for observation in observations:
            bucket = observation.features.bucket()
            grouped.setdefault(bucket, {}).setdefault(observation.group, []).append(observation.correct)
        return cls({
            bucket: CalibrationBin(len(groups), sum(all(outcomes) for outcomes in groups.values()))
            for bucket, groups in grouped.items()
        })

    def estimate(self, features: DecisionFeatures) -> CalibrationBin:
        return self.bins.get(features.bucket(), CalibrationBin(0, 0))


@dataclass(frozen=True)
class Decision:
    confidence: float
    decision: str
    reason: str
    bucket: str
    calibration_groups: int
    precision_lower_bound: float


@dataclass
class DecisionPolicy:
    model: ConfidenceModel
    threshold: float | None = None  # Safe default: review everything.
    min_groups: int = MIN_CALIBRATION_GROUPS

    def __post_init__(self):
        if self.threshold is not None and not 0.80 <= self.threshold <= 1:
            raise ValueError("Acceptance threshold must be in [0.80, 1]")
        if self.min_groups < 1:
            raise ValueError("Calibration support must be positive")

    def decide(self, features: DecisionFeatures) -> Decision:
        estimate = self.model.estimate(features)
        blockers = features.blockers()
        if blockers:
            reason = "|".join(blockers)
        elif self.threshold is None:
            reason = "review_only_selected"
        elif estimate.groups < self.min_groups:
            reason = "insufficient_calibration_groups"
        elif estimate.lower_bound < self.threshold:
            reason = "precision_lower_bound_below_threshold"
        else:
            return Decision(estimate.confidence, "auto_accept", "supported_acceptance",
                            features.bucket(), estimate.groups, estimate.lower_bound)
        return Decision(estimate.confidence, "review", reason, features.bucket(),
                        estimate.groups, estimate.lower_bound)

    def save(self, path: str | Path = DEFAULT_MODEL_PATH, metadata: dict | None = None) -> None:
        payload = {
            "schema_version": 1, "threshold": self.threshold, "min_groups": self.min_groups,
            "bins": {name: asdict(bin_) for name, bin_ in self.model.bins.items()},
            "evidence_rules": EVIDENCE_RULES,
            "metadata": metadata or {},
        }
        Path(path).write_text(json.dumps(payload, indent=2), encoding="utf-8")

    @classmethod
    def load(cls, path: str | Path = DEFAULT_MODEL_PATH) -> DecisionPolicy:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        if payload.get("schema_version") != 1:
            raise ValueError("Unsupported decision model schema")
        if payload.get("evidence_rules") != EVIDENCE_RULES:
            raise ValueError("Decision model rules differ from the current implementation")
        model = ConfidenceModel({name: CalibrationBin(**counts) for name, counts in payload["bins"].items()})
        return cls(model, payload["threshold"], payload["min_groups"])
