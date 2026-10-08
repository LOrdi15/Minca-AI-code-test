"""Meaningful retrieval/ranking checks on a small deliberately conflicting catalog."""
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

import pandas as pd

from solution.catalog import DEFAULT_DATA_DIR, load_catalog
from solution.evaluate import make_split, summarize
from solution.ranking import CandidateRanker, RankingWeights, vehicle_category
from solution.retrieval import Candidate, CatalogRetriever


class RankingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        data = Path(cls.temp.name)
        pd.DataFrame([("M1", "FORD"), ("M2", "HONDA")], columns=["code", "marca"]).to_csv(data / "manufacturers.csv", index=False)
        pd.DataFrame([("S1", "M1", "ALPHA"), ("S2", "M2", "BETA"), ("S3", "M1", "GAMMA")],
                     columns=["code", "manufacturer_key", "submarca"]).to_csv(data / "submodels.csv", index=False)
        pd.DataFrame([
            ("A", "S1", "M1", "SEDAN 2.0L AUT", "AUTO", "SEDAN"),
            ("B", "S2", "M2", "PICKUP 4X4 AUT", "PICK UP", "CARGA"),
            ("C", "S1", "M1", "SEDAN 2.0L AUT", "AUTO", "SEDAN"),
            ("D", "S3", "M1", "CAMION 9 TON", "CAMION", "CARGA"),
            ("DUP", "S1", "M1", "DESCRIPCION PARECIDA", "AUTO", "SEDAN"),
            ("DUP", "S2", "M2", "OTRA DESCRIPCION", "PICK UP", "CARGA"),
            ("N", "S3", "M1", "SIN ANOS", "CAMION", "CARGA"),
        ], columns=["code", "submodel_key", "manufacturer_key", "descveh", "tipveh", "cvesegm"]).to_csv(data / "versions.csv", index=False)
        pd.DataFrame([("A", "2009"), ("B", "2010"), ("C", "2020"), ("D", "2009"), ("DUP", "2009")],
                     columns=["code", "modelo"]).to_csv(data / "version_years.csv", index=False)
        cls.catalog = load_catalog(data)
        cls.retriever = CatalogRetriever(cls.catalog)
        cls.ranker = CandidateRanker(cls.retriever)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def candidate(self, code, score):
        return Candidate(code, tuple((index, score) for index in self.retriever.code_rows[code]), score)

    def test_retrieval_returns_distinct_codes_and_keeps_all_variants(self):
        candidates = self.retriever.retrieve({"description": "DESCRIPCION PARECIDA"}, k=50)
        self.assertEqual(len(candidates), len(self.catalog.by_code))
        self.assertEqual(len({candidate.code for candidate in candidates}), len(candidates))
        duplicate = next(candidate for candidate in candidates if candidate.code == "DUP")
        self.assertEqual(len(duplicate.variant_scores), 2)

    def test_exact_text_is_retrievable(self):
        candidates = self.retriever.retrieve({"description": "HONDA BETA PICKUP 4X4 AUT"})
        self.assertEqual(candidates[0].code, "B")

    def test_year_breaks_an_otherwise_identical_text_tie(self):
        ranked = self.ranker.rank({"description": "FORD ALPHA SEDAN 2.0L AUT", "year": "2009"},
                                  [self.candidate("C", 0.8), self.candidate("A", 0.8)])
        self.assertEqual(ranked[0].code, "A")
        self.assertIn("year", ranked[1].conflicts)
        self.assertTrue(ranked[1].needs_review)

    def test_manufacturer_contradiction_can_outweigh_text_similarity(self):
        ranked = self.ranker.rank({"description": "PICKUP AUT", "marca": "FORD"},
                                  [self.candidate("B", 0.95), self.candidate("A", 0.30)],
                                  replace(RankingWeights(), manufacturer_penalty=0.60))
        self.assertEqual(ranked[0].code, "A")
        self.assertIn("manufacturer", ranked[1].conflicts)

    def test_known_submodel_incompatibility_is_visible(self):
        ranked = self.ranker.rank({"marca": "FORD", "submarca": "ALPHA"}, [self.candidate("D", 0.8)])
        self.assertIn("submodel", ranked[0].conflicts)
        self.assertLess(ranked[0].contributions["submodel"], 0)

    def test_type_incompatibility_is_penalized(self):
        ranked = self.ranker.rank({"tipveh": "AUTOMOVIL"}, [self.candidate("B", 0.8)],
                                  replace(RankingWeights(), type_penalty=0.15))
        self.assertIn("vehicle_type", ranked[0].conflicts)
        self.assertLess(ranked[0].contributions["vehicle_type"], 0)

    def test_unknown_or_missing_metadata_is_neutral(self):
        ranked = self.ranker.rank({"marca": "UNRECOGNIZED", "submarca": "UNRECOGNIZED", "year": "?", "tipveh": "TOLVA"},
                                  [self.candidate("A", 0.8)])
        self.assertEqual(ranked[0].conflicts, ())
        for field in ("manufacturer", "submodel", "year", "vehicle_type"):
            self.assertEqual(ranked[0].contributions[field], 0)

    def test_no_catalog_years_is_unknown_instead_of_incompatible(self):
        ranked = self.ranker.rank({"year": "2009"}, [self.candidate("N", 0.8)])
        self.assertNotIn("year", ranked[0].conflicts)
        self.assertEqual(ranked[0].contributions["year"], 0)

    def test_variants_do_not_borrow_metadata_from_each_other(self):
        indices = self.retriever.code_rows["DUP"]
        candidate = Candidate("DUP", ((indices[0], 0.9), (indices[1], 0.1)), 0.9)
        weights = replace(RankingWeights(), tfidf=1.0, fuzzy=0.0,
                          manufacturer_penalty=0.60, submodel_penalty=0.20, type_penalty=0.15)
        ranked = self.ranker.rank({"marca": "HONDA", "submarca": "BETA", "tipveh": "PICKUP"}, [candidate], weights)
        selected = ranked[0]
        self.assertEqual(selected.source_row, self.retriever.rows.iloc[indices[1]].source_row)
        self.assertEqual(selected.tfidf_score, 0.1)
        self.assertTrue(selected.catalog_ambiguous)
        self.assertTrue(selected.needs_review)

    def test_top_three_are_distinct_even_if_candidates_repeat(self):
        candidates = [self.candidate(code, 0.5) for code in ("A", "A", "B", "C", "D")]
        ranked = self.ranker.rank({}, candidates)
        self.assertEqual(len(ranked), 3)
        self.assertEqual(len({item.code for item in ranked}), 3)

    def test_empty_query_is_deterministic_and_requires_review(self):
        candidates = self.retriever.retrieve({"description": "*"}, 3)
        ranked = self.ranker.rank({"description": "*"}, candidates)
        self.assertEqual([item.code for item in ranked], ["A", "B", "C"])
        self.assertTrue(all(item.needs_review for item in ranked))

    def test_answers_and_ids_cannot_influence_retrieval_or_ranking(self):
        query = {"description": "FORD ALPHA", "year": "2009"}
        extra = {**query, "expected_code": "B", "query_id": "anything"}
        original = self.retriever.retrieve(query)
        self.assertEqual(original, self.retriever.retrieve(extra))
        self.assertEqual(self.ranker.rank(query, original), self.ranker.rank(extra, original))

    def test_invalid_retrieval_parameters_are_rejected(self):
        with self.assertRaises(ValueError):
            self.retriever.retrieve({}, k=0)
        with self.assertRaises(ValueError):
            self.retriever.retrieve({}, char_weight=2)

    def test_wrong_variant_code_is_rejected(self):
        index = self.retriever.code_rows["B"][0]
        with self.assertRaisesRegex(ValueError, "does not belong"):
            self.ranker.rank({}, [Candidate("A", ((index, 0.5),), 0.5)])

    def test_type_alignment_does_not_assume_ambiguous_categories(self):
        self.assertEqual(vehicle_category("TRACTO CAMION"), "TRACTO")
        self.assertEqual(vehicle_category("SEMIREMOLQUE"), "REMOLQUE")
        self.assertEqual(vehicle_category("CAMIONES (HASTA 7.5 TONS.)"), "CAMION")
        self.assertIsNone(vehicle_category("CAMIONETA"))
        self.assertIsNone(vehicle_category("TOLVA"))

    def test_disabled_type_scoring_still_flags_incompatibility(self):
        ranked = self.ranker.rank({"tipveh": "AUTOMOVIL"}, [self.candidate("B", 0.8)])
        self.assertEqual(ranked[0].contributions["vehicle_type"], 0)
        self.assertIn("vehicle_type", ranked[0].conflicts)
        self.assertTrue(ranked[0].needs_review)


class EvaluationTests(unittest.TestCase):
    def test_split_is_reproducible_exhaustive_and_grouped(self):
        queries = pd.read_csv(DEFAULT_DATA_DIR / "queries_labeled.csv", dtype=str, keep_default_na=False)
        first = make_split(queries)
        pd.testing.assert_frame_equal(first, make_split(queries))
        self.assertEqual(len(first), len(queries))
        self.assertEqual(first.query_id.nunique(), len(queries))
        self.assertEqual(int(first.groupby("group").subset.nunique().max()), 1)
        self.assertEqual(set(first.subset), {"development", "validation"})

    def test_retrieval_and_ranking_metrics_have_separate_denominators(self):
        details = [
            {"query_id": "1", "expected_code": "A", "top1_code": "B", "top3_codes": "B|A",
             "top1_correct": False, "expected_in_top3": True, "expected_in_50": True},
            {"query_id": "2", "expected_code": "C", "top1_code": "B", "top3_codes": "B|A",
             "top1_correct": False, "expected_in_top3": False, "expected_in_50": False},
        ]
        result = summarize(details)
        self.assertEqual(result["accuracy_top1"], 0)
        self.assertEqual(result["recall_top3"], 0.5)
        self.assertEqual(result["recall_at_50"], 0.5)
        self.assertAlmostEqual(result["review_all_utility"], 0.05)


if __name__ == "__main__":
    unittest.main()
