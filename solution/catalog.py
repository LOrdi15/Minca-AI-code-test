"""Integrate the insurer's catalog without discarding version variants.

Run ``python solution/catalog.py`` to print the data-quality report.
Years belong to a code, not to an individual description: the source cannot
tell us which years apply to each variant of a repeated code.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path

import pandas as pd


DEFAULT_DATA_DIR = Path(__file__).resolve().parents[1] / "data"
VERSION_FIELDS = ("manufacturer_key", "submodel_key", "descveh", "tipveh", "cvesegm")


@dataclass(frozen=True)
class CatalogVariant:
    """One original version row with its own related manufacturer and submodel."""

    source_row: int  # CSV record number, counting the header as record 1.
    manufacturer_key: str
    submodel_key: str
    marca: str
    submarca: str
    descveh: str
    tipveh: str
    cvesegm: str
    manufacturer_found: bool
    submodel_found: bool
    manufacturer_consistent: bool | None


@dataclass(frozen=True)
class CatalogEntry:
    """One answer code; plural fields deliberately expose conflicting variants."""

    code: str
    manufacturers: tuple[str, ...]
    submodels: tuple[str, ...]
    vehicle_types: tuple[str, ...]
    descriptions: tuple[str, ...]
    segments: tuple[str, ...]
    valid_years: tuple[int, ...]
    variants: tuple[CatalogVariant, ...]


@dataclass
class Catalog:
    by_code: dict[str, CatalogEntry]
    variants: pd.DataFrame  # Every version row, enriched; original order retained.
    year_records: pd.DataFrame  # All original year records, including any issues.
    report: dict[str, int]
    duplicate_details: pd.DataFrame  # Repeated codes and fields that differ.


def _read_table(data_dir: Path, filename: str, columns: tuple[str, ...]) -> pd.DataFrame:
    """Keep identifiers and text as supplied; reject a broken file contract."""
    path = data_dir / filename
    table = pd.read_csv(path, dtype=str, keep_default_na=False)
    missing = set(columns) - set(table.columns)
    if missing:
        raise ValueError(f"{filename}: missing columns {sorted(missing)}")
    if table["code"].str.strip().eq("").any():
        raise ValueError(f"{filename}: empty code")
    return table


def _check_dimension(table: pd.DataFrame, name: str) -> None:
    """Fail rather than multiply rows or silently choose a duplicate lookup key."""
    repeated = table.loc[table["code"].duplicated(keep=False), "code"].unique()
    if len(repeated):
        raise ValueError(f"{name}: duplicate lookup codes {list(repeated[:5])}")


def _distinct(values: pd.Series) -> tuple[str, ...]:
    """Convenience summary only; the full original rows remain in variants."""
    return tuple(value for value in values.unique() if value != "")


def load_catalog(data_dir: str | Path = DEFAULT_DATA_DIR) -> Catalog:
    """Left-join catalog relationships and group variants by valid answer code.

    Unmatched version rows are kept and flagged. Year records with missing
    catalog codes or invalid year text remain inspectable in year_records.
    No description normalization or matching is performed here.
    """
    data_dir = Path(data_dir)
    versions = _read_table(data_dir, "versions.csv", ("code", *VERSION_FIELDS))
    manufacturers = _read_table(data_dir, "manufacturers.csv", ("code", "marca"))
    submodels = _read_table(data_dir, "submodels.csv", ("code", "manufacturer_key", "submarca"))
    years = _read_table(data_dir, "version_years.csv", ("code", "modelo"))
    _check_dimension(manufacturers, "manufacturers.csv")
    _check_dimension(submodels, "submodels.csv")

    enriched = versions.copy()
    enriched["source_row"] = range(2, len(versions) + 2)
    enriched = enriched.merge(
        manufacturers[["code", "marca"]].rename(columns={"code": "manufacturer_key"}),
        on="manufacturer_key", how="left", sort=False, validate="many_to_one",
        indicator="manufacturer_relation",
    )
    enriched = enriched.merge(
        submodels[["code", "manufacturer_key", "submarca"]].rename(
            columns={"code": "submodel_key", "manufacturer_key": "submodel_manufacturer_key"}
        ),
        on="submodel_key", how="left", sort=False, validate="many_to_one",
        indicator="submodel_relation",
    )
    enriched["manufacturer_found"] = enriched["manufacturer_relation"].eq("both")
    enriched["submodel_found"] = enriched["submodel_relation"].eq("both")
    enriched["manufacturer_consistent"] = (
        enriched["manufacturer_key"].eq(enriched["submodel_manufacturer_key"])
        .astype("boolean").where(enriched["submodel_found"])
    )
    enriched[["marca", "submarca", "submodel_manufacturer_key"]] = enriched[
        ["marca", "submarca", "submodel_manufacturer_key"]
    ].fillna("")

    # Aggregate years before attaching them: a raw join would duplicate versions.
    years = years.copy()
    years["code_found"] = years["code"].isin(versions["code"])
    years["year_valid"] = years["modelo"].str.fullmatch(r"[0-9]{4}")
    years["year"] = pd.to_numeric(years["modelo"].where(years["year_valid"]), errors="coerce").astype("Int64")
    usable_years = years.loc[years["code_found"] & years["year_valid"]]
    years_by_code = {
        code: tuple(sorted(int(year) for year in group["year"].unique()))
        for code, group in usable_years.groupby("code", sort=False)
    }
    enriched["valid_years"] = enriched["code"].map(lambda code: years_by_code.get(code, ()))

    by_code: dict[str, CatalogEntry] = {}
    duplicate_details: list[dict] = []
    for code, group in enriched.groupby("code", sort=False):
        variants = tuple(
            CatalogVariant(
                source_row=row.source_row,
                manufacturer_key=row.manufacturer_key, submodel_key=row.submodel_key,
                marca=row.marca, submarca=row.submarca, descveh=row.descveh,
                tipveh=row.tipveh, cvesegm=row.cvesegm,
                manufacturer_found=bool(row.manufacturer_found),
                submodel_found=bool(row.submodel_found),
                manufacturer_consistent=None if pd.isna(row.manufacturer_consistent) else bool(row.manufacturer_consistent),
            )
            for row in group.itertuples(index=False)
        )
        by_code[code] = CatalogEntry(
            code=code, manufacturers=_distinct(group["marca"]),
            submodels=_distinct(group["submarca"]), vehicle_types=_distinct(group["tipveh"]),
            descriptions=_distinct(group["descveh"]), segments=_distinct(group["cvesegm"]),
            valid_years=years_by_code.get(code, ()), variants=variants,
        )
        if len(group) > 1:
            duplicate_details.append({
                "code": code, "row_count": len(group),
                "changed_fields": tuple(field for field in VERSION_FIELDS if group[field].nunique() > 1),
            })

    duplicates = pd.DataFrame(duplicate_details, columns=["code", "row_count", "changed_fields"])
    report = {
        "version_rows": len(versions),
        "integrated_rows": len(enriched),
        "unique_codes": len(by_code),
        "manufacturer_rows": len(manufacturers),
        "submodel_rows": len(submodels),
        "year_rows": len(years),
        "duplicate_codes": len(duplicates),
        "extra_version_rows": int(versions["code"].duplicated().sum()),
        "exact_duplicate_version_rows": int(versions.duplicated().sum()),
        "unmatched_manufacturer_rows": int((~enriched["manufacturer_found"]).sum()),
        "unmatched_submodel_rows": int((~enriched["submodel_found"]).sum()),
        "rows_with_any_unmatched_relation": int((~enriched["manufacturer_found"] | ~enriched["submodel_found"]).sum()),
        "manufacturer_disagreement_rows": int(enriched["manufacturer_consistent"].eq(False).sum()),
        "orphan_year_rows": int((~years["code_found"]).sum()),
        "invalid_year_rows": int((~years["year_valid"]).sum()),
        "duplicate_year_pairs": int(years.duplicated(["code", "modelo"]).sum()),
        "codes_without_valid_years": sum(not entry.valid_years for entry in by_code.values()),
    }
    for field in VERSION_FIELDS:
        report[f"duplicate_codes_changing_{field}"] = sum(
            field in detail["changed_fields"] for detail in duplicate_details
        )
    return Catalog(by_code, enriched, years, report, duplicates)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR)
    args = parser.parse_args()
    print(json.dumps(load_catalog(args.data_dir).report, indent=2))


if __name__ == "__main__":
    main()
