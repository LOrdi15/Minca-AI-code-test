"""TF-IDF candidate retrieval over all catalog variants, grouped by code."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from solution.catalog import Catalog
from solution.normalization import normalize_catalog, normalize_text


@dataclass(frozen=True)
class Candidate:
    code: str
    # Every variant of the retrieved code, with its own TF-IDF score.
    variant_scores: tuple[tuple[int, float], ...]
    score: float


def query_text(query: Mapping[str, str]) -> str:
    """Only observable input fields; never expected_code, IDs or derived labels."""
    return " ".join(filter(None, (
        normalize_text(query.get(field, "")) for field in ("description", "marca", "submarca")
    )))


class CatalogRetriever:
    """One reusable catalog index. Fitting uses catalog text, not query labels."""

    def __init__(self, catalog: Catalog):
        if not catalog.by_code:
            raise ValueError("Cannot index an empty catalog")
        self.catalog = catalog
        self.rows = normalize_catalog(catalog).reset_index(drop=True)
        self.texts = (
            self.rows.marca_normalized + " " + self.rows.submarca_normalized + " "
            + self.rows.descveh_normalized
        ).str.strip().tolist()
        self.word_vectorizer = TfidfVectorizer(
            lowercase=False, token_pattern=r"(?u)\b[A-Z0-9]+(?:\.[0-9]+)*\b",
            ngram_range=(1, 2), sublinear_tf=True, dtype=np.float32,
        )
        self.char_vectorizer = TfidfVectorizer(
            lowercase=False, analyzer="char_wb", ngram_range=(3, 5),
            sublinear_tf=True, dtype=np.float32,
        )
        self.word_matrix = self.word_vectorizer.fit_transform(self.texts)
        self.char_matrix = self.char_vectorizer.fit_transform(self.texts)
        self.codes = sorted(catalog.by_code)
        positions = {code: i for i, code in enumerate(self.codes)}
        self.row_code_positions = np.array([positions[code] for code in self.rows.code])
        self.code_rows: dict[str, list[int]] = {code: [] for code in self.codes}
        for index, code in enumerate(self.rows.code):
            self.code_rows[code].append(index)

    def retrieve(self, query: Mapping[str, str], k: int = 50, char_weight: float = 0.35) -> list[Candidate]:
        """Return up to k distinct codes, without year or brand exclusion filters.

        Similarities are cosine values because TF-IDF vectors are L2 normalized.
        A code's retrieval score is its best variant, preserving all variants
        for subsequent ranking. Code order resolves ties deterministically.
        """
        if k < 1:
            raise ValueError("k must be positive")
        if not 0 <= char_weight <= 1:
            raise ValueError("char_weight must be in [0, 1]")
        text = query_text(query)
        word = (self.word_matrix @ self.word_vectorizer.transform([text]).T).toarray().ravel()
        char = (self.char_matrix @ self.char_vectorizer.transform([text]).T).toarray().ravel()
        scores = (1 - char_weight) * word + char_weight * char
        code_scores = np.zeros(len(self.codes), dtype=np.float32)
        np.maximum.at(code_scores, self.row_code_positions, scores)
        order = np.argsort(-code_scores, kind="stable")[:k]
        return [
            Candidate(
                code=self.codes[position], score=float(code_scores[position]),
                variant_scores=tuple((i, float(scores[i])) for i in self.code_rows[self.codes[position]]),
            )
            for position in order
        ]
