"""Catalog contract checks. Run: python -m unittest discover -s tests -v"""

import csv
import tempfile
import unittest
from pathlib import Path

from solution.catalog import DEFAULT_DATA_DIR, load_catalog


class CatalogFixtureTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.data_dir = Path(self.temp.name)
        self.write("manufacturers.csv", ["code", "marca"], [["M1", "MARCA UNO"], ["M2", "MARCA DOS"]])
        self.write("submodels.csv", ["code", "manufacturer_key", "submarca"],
                   [["S1", "M1", "MODELO UNO"], ["S2", "M2", "MODELO DOS"]])
        self.version_columns = ["code", "submodel_key", "manufacturer_key", "descveh", "tipveh", "cvesegm"]
        self.write("versions.csv", self.version_columns, [
            ["001", "S1", "M1", "VERSION 2.0 AUT", "AUTO", "SEDAN"],
            ["001", "S1", "M1", "VERSION 2.0 AUTOMATICA", "AUTO", "SEDAN"],
            ["002", "S2", "M2", "OTRA VERSION", "CAMION", "CARGA"],
        ])
        self.write("version_years.csv", ["code", "modelo"],
                   [["001", "2009"], ["001", "2008"], ["001", "2009"], ["002", "2010"]])

    def write(self, filename, columns, rows):
        with (self.data_dir / filename).open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(columns)
            writer.writerows(rows)

    def test_variants_and_years_are_preserved_without_cartesian_expansion(self):
        catalog = load_catalog(self.data_dir)
        entry = catalog.by_code["001"]
        self.assertEqual(len(catalog.variants), 3)
        self.assertEqual(len(entry.variants), 2)
        self.assertEqual(entry.manufacturers, ("MARCA UNO",))
        self.assertEqual(entry.submodels, ("MODELO UNO",))
        self.assertEqual(entry.vehicle_types, ("AUTO",))
        self.assertEqual(entry.descriptions, ("VERSION 2.0 AUT", "VERSION 2.0 AUTOMATICA"))
        self.assertEqual(entry.valid_years, (2008, 2009))
        self.assertEqual([v.source_row for v in entry.variants], [2, 3])
        self.assertEqual(catalog.report["duplicate_year_pairs"], 1)
        self.assertEqual(len(catalog.year_records), 4)
        self.assertEqual(catalog.duplicate_details.iloc[0].changed_fields, ("descveh",))

    def test_conflicting_variants_keep_their_own_relationships(self):
        self.write("versions.csv", self.version_columns, [
            ["001", "S1", "M1", "DESCRIPCION A", "AUTO", "SEDAN"],
            ["001", "S2", "M2", "DESCRIPCION B", "CAMION", "CARGA"],
        ])
        catalog = load_catalog(self.data_dir)
        entry = catalog.by_code["001"]
        self.assertEqual(entry.manufacturers, ("MARCA UNO", "MARCA DOS"))
        self.assertEqual(entry.vehicle_types, ("AUTO", "CAMION"))
        self.assertEqual([(v.marca, v.submarca, v.descveh) for v in entry.variants], [
            ("MARCA UNO", "MODELO UNO", "DESCRIPCION A"),
            ("MARCA DOS", "MODELO DOS", "DESCRIPCION B"),
        ])
        self.assertEqual(catalog.report["duplicate_codes_changing_manufacturer_key"], 1)

    def test_missing_relationships_do_not_discard_versions(self):
        self.write("versions.csv", self.version_columns, [
            ["001", "UNKNOWN", "UNKNOWN", "SIN RELACION", "AUTO", ""],
            ["002", "S2", "M2", "CON RELACION", "CAMION", ""],
        ])
        catalog = load_catalog(self.data_dir)
        self.assertEqual(len(catalog.by_code), 2)
        variant = catalog.by_code["001"].variants[0]
        self.assertFalse(variant.manufacturer_found)
        self.assertFalse(variant.submodel_found)
        self.assertIsNone(variant.manufacturer_consistent)
        self.assertEqual(catalog.report["unmatched_manufacturer_rows"], 1)
        self.assertEqual(catalog.report["unmatched_submodel_rows"], 1)
        self.assertEqual(catalog.report["rows_with_any_unmatched_relation"], 1)

    def test_manufacturer_disagreement_is_visible(self):
        self.write("versions.csv", self.version_columns,
                   [["001", "S1", "M2", "INCONSISTENTE", "AUTO", ""]])
        catalog = load_catalog(self.data_dir)
        variant = catalog.by_code["001"].variants[0]
        self.assertEqual(variant.marca, "MARCA DOS")
        self.assertEqual(variant.submarca, "MODELO UNO")
        self.assertFalse(variant.manufacturer_consistent)
        self.assertEqual(catalog.report["manufacturer_disagreement_rows"], 1)

    def test_orphan_and_invalid_years_are_reported_and_kept(self):
        self.write("version_years.csv", ["code", "modelo"],
                   [["001", "2009"], ["001", "unknown"], ["999", "2000"]])
        catalog = load_catalog(self.data_dir)
        self.assertNotIn("999", catalog.by_code)
        self.assertEqual(catalog.by_code["001"].valid_years, (2009,))
        self.assertEqual(catalog.by_code["002"].valid_years, ())
        self.assertEqual(len(catalog.year_records), 3)
        self.assertEqual(catalog.report["orphan_year_rows"], 1)
        self.assertEqual(catalog.report["invalid_year_rows"], 1)
        self.assertEqual(catalog.report["codes_without_valid_years"], 1)

    def test_even_identical_version_rows_remain_available(self):
        row = ["001", "S1", "M1", "IDENTICA", "AUTO", ""]
        self.write("versions.csv", self.version_columns, [row, row])
        catalog = load_catalog(self.data_dir)
        self.assertEqual(len(catalog.by_code["001"].variants), 2)
        self.assertEqual(catalog.report["exact_duplicate_version_rows"], 1)
        self.assertEqual(catalog.duplicate_details.iloc[0].changed_fields, ())

    def test_duplicate_dimension_key_fails_instead_of_multiplying_rows(self):
        self.write("manufacturers.csv", ["code", "marca"], [["M1", "A"], ["M1", "B"]])
        with self.assertRaisesRegex(ValueError, "duplicate lookup codes"):
            load_catalog(self.data_dir)

    def test_missing_required_column_is_explained(self):
        self.write("versions.csv", ["code", "descveh"], [["001", "VERSION"]])
        with self.assertRaisesRegex(ValueError, "versions.csv: missing columns"):
            load_catalog(self.data_dir)


class SuppliedCatalogTests(unittest.TestCase):
    def test_real_catalog_preserves_every_version_and_all_codes(self):
        catalog = load_catalog(DEFAULT_DATA_DIR)
        self.assertEqual(len(catalog.by_code), 13140)
        self.assertEqual(len(catalog.variants), 13298)
        self.assertEqual(sum(len(entry.variants) for entry in catalog.by_code.values()), 13298)
        self.assertEqual(catalog.report["duplicate_codes"], 151)
        self.assertEqual(catalog.report["rows_with_any_unmatched_relation"], 0)
        self.assertEqual(catalog.report["manufacturer_disagreement_rows"], 0)
        self.assertEqual(catalog.report["orphan_year_rows"], 0)
        self.assertEqual(catalog.report["invalid_year_rows"], 0)
        self.assertEqual(catalog.report["codes_without_valid_years"], 0)
        self.assertEqual(catalog.by_code["A0003D"].descriptions,
                         ("KICKS EXCLUSIVE 1.6L 5P CVT", "KICKS EXCLUSIVE 1.6L 5 PUERTAS CVT"))


if __name__ == "__main__":
    unittest.main()
