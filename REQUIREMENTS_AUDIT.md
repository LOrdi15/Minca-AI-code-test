# Final requirements audit

The original brief is preserved in CHALLENGE.md. Evidence is stored under
evaluation/final; archive membership and reproduction are checked when packaging.

| Requirement | Status | Evidence or limitation |
|---|---|---|
| 155 blind predictions, one per query | PASS | Official SUBMISSION VALID; IDs/order checked |
| Exactly five required columns | PASS | Additional CSV contract checks |
| Three distinct catalog-valid codes, top1 first | PASS | Every output row checked against versions.csv |
| Finite confidence in [0,1], valid decisions | PASS | Every row checked; frozen review policy |
| Preserve codes/IDs as strings | PASS | dtype=str and dedicated tests |
| Retrieval and ranking metrics reported separately | PASS | EVAL section 1; recall@50 and conditional ranking accuracy |
| Utility and original baseline comparison | PASS | Official scorer: +0.110515 versus +0.036695, labeled data |
| Experiment ledger, including rejected changes | PASS | EVAL section 2; real CSV/JSON evidence retained |
| Ten specific failures with expected/returned code and actions | PASS | EVAL section 3; ten validation query IDs |
| DECISIONS covers every required topic, concise length | PASS | Architecture, rejection, thresholds, ambiguity, two weeks, four expert hours |
| English project documentation | PASS | Current Markdown and technical explanations are English |
| Original source evidence preserved | PASS | Original vehicle text and measured LLM prompt remain verbatim |
| Complete tests | PASS | 103 tests in the fresh virtual environment |
| Clean dependency installation and Python execution | PASS | Fresh environment, pinned direct dependencies, pip setup check and inference |
| GNU Make binary execution | NOT VERIFIED | Make is unavailable locally; equivalent commands tested |
| make predict target integration | PASS | Calls the verified module CLI with relative paths |
| Official scripts unchanged | PASS | Original Git blobs and frozen hashes compared |
| Original catalog/query files unchanged | PASS | Six original data files checked against initial commit |
| No inference dependency on .env, labels or local private configuration | PASS | Isolated execution without these inputs; byte-identical CSV |
| Blind labels never used for optimization | PASS | No blind labels exist locally; whitelisted observable fields and leakage tests |
| Blind run under ten minutes | PASS | Measured complete local process well below 600 seconds |
| Production LLM budget below USD 2 | PASS | Zero production calls; optional trial stopped after one error |
| Exact optional trial invoice cost | NOT VERIFIED | No usage reported after HTTP 429; conservative reservation USD 0.0039368 |
| No secrets or .env in tracked files/history/archive | PASS | Key-pattern and history checks; archive exclusion assertions |
| No public catalog publication | PASS | Repository privacy explicitly confirmed by user; only authorized private push |
| Source, data, predictions, docs, tools and real .git packaged | PASS | ZIP membership assertions and delivery manifest |
| Archive opened and prediction reproduced | PASS | Archive integrity check and extracted-copy execution |
| Blind utility exceeds baseline | NOT VERIFIED | Blind labels are evaluator-owned; labeled comparison exceeds baseline |
| Five-hour sitting / within-one-week return | NOT VERIFIED | Receipt/start schedule is user-managed and not independently available |
| Email sent to challenge owner | NOT VERIFIED | ZIP prepared for user; no email authorization or sending performed |

No retrieval/ranking/decision changes were made at closure. Only documentation,
dependency pins, cleanup and verification artifacts changed. The OpenAI trial is
inconclusive and excluded from inference. Validation was already inspected;
calibrator OOF estimates do not provide nested evaluation of ranking selection.

The ZIP contains confidential challenge data; use only the challenge owner's
approved return channel. Its manifest records the final Git commit and prediction hash.
