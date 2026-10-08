"""Conservative text normalization shared by catalog and queries.

This module contains no aliases, spelling corrections, attribute extraction,
or matching. Decimal dots and numeric measurement marks are meaningful.
"""
from __future__ import annotations

import re
import unicodedata
from typing import TYPE_CHECKING, Sequence

import pandas as pd

if TYPE_CHECKING:
    from solution.catalog import Catalog

CATALOG_TEXT_COLUMNS = ("marca", "submarca", "descveh", "tipveh", "cvesegm")
QUERY_TEXT_COLUMNS = ("description", "marca", "submarca", "tipveh", "segment")

# Equivalent typography, not vehicle aliases. Keep feet/inches distinguishable.
MEASUREMENT_MARKS = str.maketrans({
    "\u2018": "'", "\u2019": "'", "\u2032": "'",
    "\u201c": '"', "\u201d": '"', "\u2033": '"',
})
SEPARATORS = re.compile(
    r"(?<![0-9])\.|\.(?![0-9])|(?<![0-9])['\"]|[^A-Z0-9.'\"]+"
)
DOTTED_INITIALS = re.compile(r"(?<![A-Z0-9])(?:[A-Z]\.){2,}")


def normalize_text(text: str | None) -> str:
    """Uppercase, remove accents and standardize separators.

    Keep decimal dots between digits, and feet/inch marks following digits.
    Other punctuation becomes spaces, so F-350 becomes F 350, not F350.
    Compact dotted initials (H.P. -> HP), but do not expand abbreviations or
    correct names. Preserve alphanumeric tokens, years and leading zeros.
    None represents missing text; other non-string inputs are rejected so that
    accidental numbers or NaN values do not become fake vehicle descriptions.
    """
    if text is None:
        return ""
    if not isinstance(text, str):
        raise TypeError("normalize_text expects a string or None")

    text = unicodedata.normalize("NFKD", text.translate(MEASUREMENT_MARKS))
    text = "".join(
        char for char in text
        if not unicodedata.combining(char)
    )

    text = text.upper()
    # A trailing separator also protects strings such as H.P.FL7033K:
    # normalize to HP FL7033K, rather than inventing the token HPFL7033K.
    text = DOTTED_INITIALS.sub(lambda match: match.group().replace(".", "") + " ", text)
    text = SEPARATORS.sub(" ", text)
    return " ".join(text.split())


def normalize_columns(table: pd.DataFrame, columns: Sequence[str]) -> pd.DataFrame:
    """Return a copy with <column>_normalized fields; retain every source row.

    Null cells become empty normalized text. Original values, identifiers,
    labels and years are untouched. Non-null text fields must contain strings.
    """
    missing = set(columns) - set(table.columns)
    if missing:
        raise ValueError(f"Missing text columns for normalization: {sorted(missing)}")
    result = table.copy()
    for column in columns:
        result[f"{column}_normalized"] = table[column].map(
            lambda value: normalize_text(None if pd.isna(value) else value)
        )
    return result


def normalize_catalog(catalog: Catalog) -> pd.DataFrame:
    """Normalize every integrated variant, preserving its code and valid years."""
    return normalize_columns(catalog.variants, CATALOG_TEXT_COLUMNS)


def normalize_queries(queries: pd.DataFrame) -> pd.DataFrame:
    """Use the same rules for broker descriptions and their text metadata."""
    return normalize_columns(queries, QUERY_TEXT_COLUMNS)
