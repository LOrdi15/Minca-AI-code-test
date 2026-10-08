"""Vehicle information that basic normalization must preserve.

Run from the project directory:
    python -m unittest discover -s tests -p test_normalization.py -v
"""

import unittest

import pandas as pd

from solution.catalog import DEFAULT_DATA_DIR, load_catalog
from solution.normalization import (
    CATALOG_TEXT_COLUMNS, QUERY_TEXT_COLUMNS,
    normalize_catalog, normalize_columns, normalize_queries, normalize_text,
)


class NormalizeTextTests(unittest.TestCase):
    def test_missing_text_returns_empty_string(self):
        self.assertEqual(normalize_text(None), "")

    def test_non_text_is_rejected_instead_of_becoming_a_description(self):
        for value in (2009, 0, float("nan"), False, [], {}):
            with self.subTest(value=value):
                with self.assertRaises(TypeError):
                    normalize_text(value)

    def test_fullwidth_letters_and_digits_are_comparable(self):
        self.assertEqual(normalize_text("ＦＯＲＤ ４ｘ４ ２.０Ｌ"), "FORD 4X4 2.0L")

    def test_typographic_measurement_marks_are_preserved(self):
        self.assertEqual(normalize_text("CAJA 40\u2032 RIN 20\u2033"), "CAJA 40' RIN 20\"")
        self.assertEqual(normalize_text("CAJA 40\u2019 RIN 20\u201d"), "CAJA 40' RIN 20\"")

    def test_quotes_around_words_are_separators(self):
        self.assertEqual(normalize_text("\u201cDENALI\u201d 'AUT'"), "DENALI AUT")

    def test_decimal_dots_are_different_from_abbreviation_dots(self):
        self.assertEqual(normalize_text("2.0L A.C. 1.5T AUT..."), "2.0L AC 1.5T AUT")
        self.assertNotEqual(normalize_text("MOTOR 2.0L"), normalize_text("MOTOR 20L"))

    def test_dotted_initials_are_compacted_without_inventing_words(self):
        self.assertEqual(normalize_text("V.W. 130 H.P. E.E. AUT. STD."),
                         "VW 130 HP EE AUT STD")
        self.assertEqual(normalize_text("220 H.P.FL7033K"), "220 HP FL7033K")
        self.assertEqual(normalize_text("CAMION DE-P.B.V."), "CAMION DE PBV")

    def test_uppercase_and_accents(self):
        self.assertEqual(normalize_text("Citroën camión año versión"),
                         "CITROEN CAMION ANO VERSION")

    def test_decomposed_unicode_accents(self):
        self.assertEqual(normalize_text("Citroe\u0308n camio\u0301n"), "CITROEN CAMION")

    def test_whitespace_including_nonbreaking_spaces(self):
        self.assertEqual(normalize_text(" \tFORD\n\r  FIESTA\u00a0\u00a0AUT \t"),
                         "FORD FIESTA AUT")

    def test_punctuation_separates_instead_of_concatenating_words(self):
        self.assertEqual(normalize_text("(FORD),FIESTA;AUT./STD:BASE"),
                         "FORD FIESTA AUT STD BASE")

    def test_drivetrain_tokens_remain_intact(self):
        self.assertEqual(normalize_text("4x4 / 4x2, AWD; FWD"), "4X4 4X2 AWD FWD")

    def test_engine_decimals_and_suffixes_remain_intact(self):
        self.assertEqual(normalize_text("Motor 2.0L, 1.5T; V6 3.5."),
                         "MOTOR 2.0L 1.5T V6 3.5")

    def test_model_numbers_are_not_dropped_or_joined(self):
        self.assertEqual(normalize_text("FORD F-350 / LK-1417/34 / CF600"),
                         "FORD F 350 LK 1417 34 CF600")

    def test_years_and_leading_zeros_remain_intact(self):
        self.assertEqual(normalize_text("Modelo 2009 (1993), serie 001"),
                         "MODELO 2009 1993 SERIE 001")

    def test_power_capacity_and_transmission_remain_intact(self):
        self.assertEqual(normalize_text("Cummins 200 HP, 9 TON; 6VEL AUT."),
                         "CUMMINS 200 HP 9 TON 6VEL AUT")

    def test_measurement_marks_are_not_lost_as_generic_punctuation(self):
        self.assertEqual(normalize_text("CAJA 40' / RIN 20\""), "CAJA 40' RIN 20\"")

    def test_no_aliases_or_spelling_corrections(self):
        self.assertEqual(normalize_text("Mercedez GMOTORS AUT STD 5P"),
                         "MERCEDEZ GMOTORS AUT STD 5P")

    def test_empty_or_only_separators_returns_empty_text(self):
        for text in ("", " \t\n", " ,;()/---. ", "*"):
            with self.subTest(text=text):
                self.assertEqual(normalize_text(text), "")

    def test_normalization_is_idempotent(self):
        for text in ("Citroën C3 1.6L 4x2", "FORD F-350 (2020) AUT.", "CAJA 40'"):
            with self.subTest(text=text):
                once = normalize_text(text)
                self.assertEqual(normalize_text(once), once)

    def test_important_vehicle_differences_do_not_become_identical(self):
        pairs = (
            ("PICKUP 4x4", "PICKUP 4x2"),
            ("MOTOR 2.0L", "MOTOR 3.0L"),
            ("FORD F-350", "FORD F-450"),
            ("MODELO 2009", "MODELO 2010"),
            ("VERSION AUT", "VERSION STD"),
            ("CARGA 9 TON", "CARGA 19 TON"),
            ("CAJA 40'", "CAJA 40\""),
        )
        for first, second in pairs:
            with self.subTest(first=first, second=second):
                self.assertNotEqual(normalize_text(first), normalize_text(second))


class NormalizeColumnsTests(unittest.TestCase):
    def test_original_values_and_nulls_are_untouched(self):
        table = pd.DataFrame({
            "description": [" Citroën 2.0L ", None, float("nan"), pd.NA],
            "year": ["2009", "2010", "001", ""],
        }, index=[8, 4, 2, 1])
        original = table.copy(deep=True)
        result = normalize_columns(table, ["description"])
        pd.testing.assert_frame_equal(table, original)
        pd.testing.assert_frame_equal(result[original.columns], original)
        self.assertEqual(result.description_normalized.tolist(), ["CITROEN 2.0L", "", "", ""])

    def test_missing_columns_are_reported(self):
        with self.assertRaisesRegex(ValueError, "Missing text columns"):
            normalize_columns(pd.DataFrame({"code": ["001"]}), ["description"])

    def test_normalizing_a_table_twice_has_the_same_result(self):
        original = pd.DataFrame({"description": ["130 H.P. 2.0L", "CAMIÓN 4x2"]})
        once = normalize_columns(original, ["description"])
        twice = normalize_columns(once, ["description"])
        pd.testing.assert_frame_equal(once, twice)


class RealNormalizationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = load_catalog(DEFAULT_DATA_DIR)
        cls.queries = {
            name: pd.read_csv(DEFAULT_DATA_DIR / name, dtype=str, keep_default_na=False)
            for name in ("queries_labeled.csv", "queries_blind.csv")
        }

    def test_catalog_normalization_preserves_rows_variants_and_years(self):
        original = self.catalog.variants.copy(deep=True)
        normalized = normalize_catalog(self.catalog)
        pd.testing.assert_frame_equal(self.catalog.variants, original)
        pd.testing.assert_frame_equal(normalized[original.columns], original)
        self.assertEqual(len(normalized), 13298)
        self.assertEqual(normalized.code.nunique(), 13140)
        self.assertEqual(len(normalized.loc[normalized.code.eq("A0003D")]), 2)
        for column in CATALOG_TEXT_COLUMNS:
            self.assertIn(f"{column}_normalized", normalized)

    def test_query_normalization_preserves_ids_years_and_labels(self):
        for name, queries in self.queries.items():
            with self.subTest(file=name):
                normalized = normalize_queries(queries)
                pd.testing.assert_frame_equal(normalized[queries.columns], queries)
                for column in QUERY_TEXT_COLUMNS:
                    self.assertIn(f"{column}_normalized", normalized)

    def test_actual_catalog_descriptions(self):
        examples = {
            "A0002U": "CAVALIER Z24 2 PTAS AUT FI",
            "A0004N": "MERCEDES BENZ FREIGHTLINER DIESEL ABS 220 HP FL7033K 12TN",
            "A0003D": "KICKS EXCLUSIVE 1.6L 5P CVT",
        }
        for code, expected in examples.items():
            with self.subTest(code=code):
                raw = self.catalog.by_code[code].variants[0].descveh
                self.assertEqual(normalize_text(raw), expected)

    def test_actual_broker_descriptions(self):
        examples = {
            "queries_labeled.csv": {
                "q0002": "CR V EX PREMIUM 2.4",
                "q0003": "DODGE RAM 2500 QUAD CAB SLT 4X2",
                "q0360": "VW SAVEIRO ROJO",
            },
            "queries_blind.csv": {
                "q0004": "DODGE RAM 4000 CHASIS CABINA STD C A AC",
                "q0190": "CAMION GRUA CAB 4200 175 33000 LBS DE PBV",
                "q0103": "",
            },
        }
        for filename, cases in examples.items():
            queries = self.queries[filename].set_index("query_id")
            for query_id, expected in cases.items():
                with self.subTest(file=filename, query_id=query_id):
                    self.assertEqual(normalize_text(queries.loc[query_id, "description"]), expected)

    def test_real_descriptions_preserve_numbers_decimals_and_drivetrains(self):
        import re

        descriptions = self.catalog.variants.descveh.tolist()
        for queries in self.queries.values():
            descriptions.extend(queries.description.tolist())
        for raw in descriptions:
            normalized = normalize_text(raw)
            self.assertEqual(re.findall(r"[0-9]+", raw), re.findall(r"[0-9]+", normalized), msg=raw)
            for token in re.findall(r"[0-9]+\.[0-9]+", raw):
                self.assertIn(token, normalized, msg=raw)
            for token in re.findall(r"[0-9]+[xX][0-9]+", raw):
                self.assertIn(token.upper(), normalized, msg=raw)
            self.assertEqual(normalize_text(normalized), normalized, msg=raw)


if __name__ == "__main__":
    unittest.main()
