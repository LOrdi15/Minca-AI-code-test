# Follow-up topics and working memory

The final model is frozen: local TF-IDF retrieval, RapidFuzz/attribute reranking,
grouped confidence and review-only decisions. Hashes and verified environment are
recorded under evaluation/final. No production model changes were made at closure.

## Findings to revisit

- Preserve catalog variants; years are known by code, not by individual variant.
- Z0000M occurs in 33 labels and explains 23 of 29 retrieval misses. Ask whether
  it is a generic business classification before changing labels or adding rules.
- Investigate capacity, drivetrain, engine, doors, transmission and body style.
  Missing attributes cannot be inferred from a high lexical score.
- Normalization intentionally avoids semantic aliases and preserves numbers,
  decimals, measurement marks and drivetrain tokens.
- Six point-confidence 0.80 false accepts span four commercial vehicles and two
  SUVs. None is blocked by the current recognized attributes. Review remains
  selected; no post-hoc segment exclusions were introduced.
- Confidence has only three cohort values. It is not an individual probability.
  More verified groups and fresh evaluation are needed before automation.
- The validation split has already been inspected. Development also informed
  ranking selection; calibrator OOF results are not nested pipeline evaluation.
- The decimal/unit tokenizer trial gained three top-1 cases, but no utility or
  validation improvement. It was not deployed.
- OpenAI received one authorized request and returned HTTP 429. No usable LLM
  results exist. Do not present fallback metrics as LLM quality. Preserve its ledger.
- Original scripts and data are retained. Secrets and caches are excluded from
  delivery. The user confirmed the repository is private and authorized pushes.
- GNU Make execution must be distinguished from equivalent Python command checks.

Detailed failure evidence remains in ERRORES_PENDIENTES.md and evaluation CSV/JSON
artifacts. Earlier working notes remain in real Git history. This file is a record
of unresolved issues, not a request to continue experiments before submission.
