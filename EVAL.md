# Final evaluation

## 1. Results, retrieval and ranking evaluated separately

We ship frozen local configuration E8 with review-only decisions. The 155 blind
predictions meet the format contract. Blind utility cannot be measured without
the evaluator's labels. OpenAI is excluded: its isolated trial returned HTTP 429
before any valid response.

### Protocol and baseline comparison

There are **233 labeled queries**: 174 development, 59 validation. We use the first
StratifiedGroupKFold split, four folds, seed 42, grouping normalized description
and year. Equivalent groups do not cross subsets. Indexes fit catalog text only;
expected_code is never an inference feature. Ranking weights were selected on
development and frozen before the first validation evaluation. Subsequent audits
reuse previously inspected data; they are not new independent tests. Blind data
were never used to optimize weights, thresholds or routing rules.

| Subset / system | Top-1 accuracy | Top-3 recall | Recall@50 | Mean utility |
|---|---:|---:|---:|---:|
| Development baseline (174) | 56/174 = 32.18% | 76/174 = 43.68% | 121/174 = 69.54%* | +0.037356 |
| Development solution (174) | 107/174 = 61.49% | 140/174 = 80.46% | 151/174 = 86.78% | +0.110920 |
| Validation baseline (59) | 16/59 = 27.12% | 25/59 = 42.37% | 36/59 = 61.02%* | +0.034746 |
| Validation solution (59) | 35/59 = 59.32% | 47/59 = 79.66% | 53/59 = 89.83% | +0.109322 |
| Overall descriptive baseline (233) | 72/233 = 30.90% | 101/233 = 43.35% | 157/233 = 67.38%* | +0.036695 |
| Overall descriptive solution (233) | 142/233 = 60.94% | 187/233 = 80.26% | 204/233 = 87.55% | +0.110515 |

Both policies review 100%. Auto-accept precision is **undefined**, because neither
accepts any cases; the scorer prints zero by convention. Accepting all our results
would yield utility -0.562232.

*The original baseline returns three rows. Its diagnostic recall@50 extends the
same scoring/tie-break to 50 distinct codes. Top-1/top-3 match its unmodified CLI.

Recall@50 is measured **before ranking**. Conditional ranking top-1 accuracy when
the expected code was retrieved: 35/53 = **66.04%** on validation, 142/204 =
**69.61%** overall. The 91 top-1 failures comprise 29 retrieval misses, 17 recovered
codes outside top-3 and 45 expected codes in top-3 but not first. Reranking cannot
repair the first category without changing retrieval.

### Frozen configuration

The integrated catalog retains 13298 rows and 13140 distinct codes, with complete
description variants and no unmatched relationships. Years belong to codes, not
individual variants; missing years are not filled. Retrieval combines 65% word
TF-IDF (unigrams/bigrams) with 35% character TF-IDF (3–5), taking the maximum by
code and retrieving 50 distinct codes without hard attribute filters.

Ranking uses 90% TF-IDF, 10% RapidFuzz WRatio and year +0.12/-0.20, manufacturer
+0.02/-0.10 and submodel +0.02/-0.05 adjustments. Vehicle-type scoring was disabled
after development regressions; recognized conflicts still block acceptance.
Complete variants are scored, never mixing descriptions and attributes across rows.
No manual semantic aliases were added.

REMOLQUE is the weakest segment: 35 rows, top-3 31.43%, recall@50 48.57%. Z0000M
occurs in 33 labels and explains 23/29 retrieval misses, although it describes a
closed box while some queries describe platforms, hoppers or trucks. This may be
a business rule or disputed labeling. We did not relabel or add a frequency-based fallback.

### Confidence, thresholds and final decision

Confidence is a Beta(1,1)-smoothed cohort success rate:
`(correct groups+1)/(groups+2)`. A repeated group counts once per cohort and is
correct only if all its rows are correct. This is not similarity or a guaranteed
individual probability. Blockers include recognized attribute conflicts, ambiguous
or incomplete catalog relations, uninformative descriptions, no runner-up/text
evidence, unconfirmed year, no other confirmed attribute, score <0.55 or margin <0.03.
Without blockers, strong evidence requires score >=0.75 and margin >=0.08.

| Development-only calibration | Correct groups / total | Confidence | Wilson 95% lower precision bound |
|---|---:|---:|---:|
| Blocked | 40/87 | 46.07% | 35.90% |
| Moderate | 29/42 | 68.18% | 53.97% |
| Strong | 37/43 | 84.44% | 72.74% |

Across 233 cases: blocked 117, moderate 63, strong 53. Those 53 exceed confidence
0.80; no cohort exceeds 0.80 in its precision lower bound.

Thresholds were evaluated using four grouped calibration folds inside development,
seed 17. Each group receives calibration without its own labels. Protected acceptance
requires blockers to pass, at least 20 calibration groups, sufficient Wilson lower
bound, at least 20 accepted groups, greater utility and no harmful fold. Protected
0.80/0.85/0.90/0.95 all accept zero cases, with utility +0.110920.

We also measured point-confidence policies that omit Wilson while retaining other guards:

| Diagnostic policy | Development accepts/errors | Precision | Development utility | Validation accepts/errors | Validation utility |
|---|---:|---:|---:|---:|---:|
| Review all, selected | 0/0 | Undefined | +0.110920 | 0/0 | +0.109322 |
| Point >=0.80 | 44/6 | 86.36% | **+0.191379** | 9/0 | **+0.238983** |
| Point >=0.85 | 25/5 | 80.00% | +0.121552 | 0/0 | +0.109322 |
| Point >=0.90 | 0/0 | Undefined | +0.110920 | 0/0 | +0.109322 |
| Point >=0.95 | 0/0 | Undefined | +0.110920 | 0/0 | +0.109322 |

Point 0.80 maximizes observed utility, but fails our predefined evidence requirements.
Development gain +0.08046 has paired group bootstrap 95% interval
[-0.02862,+0.17725], four-comparison-adjusted [-0.06264,+0.20029]. Both include losses.
Nine validation successes have precision lower bound 70.08%. Fold-specific calibration
varies, explaining why 0.85 accepts some OOF cases but none under the final calibrator.

Final error review: q0014/q0015 are trailers, q0093 a truck, q0134 a tractor truck
(coarse segment OTHER), q0074/q0180 SUVs. **Four of six are commercial, two are
SUVs; none triggers current conflict guards.** Three labels are Z0000M. Cascadia
125 versus 116 is a textual discrepancy not captured by basic attributes; the SUV
queries omit version details. We add no post-hoc segment exclusions or ID rules.
We retain **review**, acknowledging the potential utility sacrificed.

The economic reference `4p-3 > 0.15` gives p>0.7875 if review always includes the
correct code. It does not establish that a point estimate safely exceeds that value.
OOF evaluates calibration, not the entire development-informed ranking selection.
The holdout was already inspected. Bootstrap does not refit calibrators or remove
selection uncertainty; Wilson does not protect against distribution shift or systematic
label errors. Overall figures are descriptive; the blind mix is more commercial.

### Reproducibility

```bash
make setup
make predict
make check
make test
python -m solution.predict --queries data/queries_labeled.csv --out dev_predictions.csv
python score.py --predictions dev_predictions.csv --labels data/queries_labeled.csv
```

`make evaluate` reproduces the development ledger. Frozen audits:
`python -m solution.audit_evaluation` and `python -m solution.audit_confidence`.
Stored LLM replay: `python -m experiments.llm_rerank`, without network.
Final verification records live in evaluation/final, including tested versions,
source hashes, 103 tests, official scoring and isolated execution. A previously
verified isolated blind process took 19.60 seconds including startup, with zero
fallbacks/API calls and byte-identical predictions. GNU Make was unavailable locally:
equivalent Python commands were tested, not the Make binary. Official scripts are unchanged.

## 2. Real experiment ledger

E0–E9 used 174 development cases, each starting from the last retained configuration.
Selection prioritized top-3/review utility, then top-1. Exact settings and metrics:
evaluation/ranking_selection.json. Development baseline: 56/76/121*.

| ID | Change | Development top-1 / top-3 / @50 | Decision |
|---|---|---|---|
| E0 | Integrated catalog, word TF-IDF | 60/100/145 | Starting reference |
| E1 | 35% character TF-IDF | 66/106/151 | Keep |
| E2 | RapidFuzz 30% | 67/103/151 | Revert: loses three top-3 |
| E3 | Year +0.12/-0.20 | 105/139/151 | Keep |
| E4 | Strong manufacturer/submodel penalties | 104/136/151 | Revert: noisy metadata |
| E5 | Type +0.04/-0.15 | 104/137/151 | Revert: loses two top-3 |
| E6 | Incompatible year -0.60 | 105/139/151 | Revert: no gain |
| E7 | RapidFuzz 10% | 107/139/151 | Keep |
| E8 | Small manufacturer/submodel adjustments | 107/140/151 | Keep; one-case gain is limited evidence |
| E9 | Type +0.01/-0.05 | 106/139/151 | Revert: regression |

| ID | Change | Actual result | Decision |
|---|---|---|---|
| D0 | Three cohorts, grouped confidence | Strong 37/43; confidence 84.44%, lower bound 72.74% | Keep estimate |
| D1 | Protected 0.80 | Zero accepts, utility +0.110920 | Review |
| D2 | Protected 0.85 | Zero accepts, utility +0.110920 | Review |
| D3 | Protected 0.90 | Zero accepts, utility +0.110920 | Review |
| D4 | Protected 0.95 | Zero accepts, utility +0.110920 | Review |
| D5 | Point 0.80 without Wilson | 44 accepts/6 errors, utility +0.191379 | Reject: uncertainty |
| D6 | Point 0.85 without Wilson | 25 accepts/5 errors, utility +0.121552 | Reject |
| D7 | Point 0.90 without Wilson | Zero accepts, utility +0.110920 | No gain |
| D8 | Point 0.95 without Wilson | Zero accepts, utility +0.110920 | No gain |
| R1 | Keep engine 2.0L as a single TF-IDF token | Overall 145 top-1, 187 top-3, 206 @50; utility +0.110515 | Reject: no utility/validation gain |
| C1 | Paired threshold and six-error audit | 0.80 best observed mean; interval includes losses | Review, no new rules |
| L1 | GPT-4.1 mini, ten candidates, 38 ambiguous validation cases | First request HTTP 429; zero valid responses | Inconclusive, excluded |

L1 used frozen snapshot gpt-4.1-mini-2025-04-14, one predeclared configuration.
The user authorized minimal data sharing and credential reuse; no IDs, labels or
blind data were sent. Local cap USD 1.90; planned reservation USD 0.141524. One
attempt, no retries, USD 0.0039368 reserved because usage was absent; actual invoice
cost was not measured. Its top-3 79.66% and utility +0.109322 describe the local
fallback only, not LLM quality. The specific 429 cause was not inferred without an
error code. Actual records are preserved under evaluation/decision_metrics.json,
reassessment, confidence_audit and llm_rerank.

## 3. Ten specific failures by query_id

These are actual frozen top-1 failures, all from validation. Explanations are
evidence-based hypotheses, not corrected labels. Source texts, years, top-3 and
signals are preserved in evaluation/reassessment/ten_errors.csv.

| query_id | Expected | Returned | Likely cause and action |
|---|---|---|---|
| q0005 | U0003D | P00000 | FORD F700 28000 versus 30000 LBS. Expected second. Capacity is not scored and 28,000 splits differently. Next step: contextual capacity extraction with regression measurement. |
| q0016 | Z0000M | S0008A | Platform query versus closed-box label, expected retrieval rank 43. Ask an expert about generic classification; do not force a frequent code. |
| q0024 | Q00046 | U0003Y | 2023 stainless tank, 31000 LTS; nearest text has years through 2022. Valid expected code is outside 50. Investigate attribute-aware retrieval later; keep year conflict visible. |
| q0035 | Q0004P | R00034 | S3 sedan: selected three doors, expected four doors second. Body/doors are not extracted. Validate sedan evidence and request distinguishing attributes. |
| q0050 | Z0000M | W0008G | Refrigerated-box query versus closed-box label, retrieval rank 34. Clarify generic business classification without invented aliases. |
| q0085 | Z0000M | J0007M | Hopper query versus closed-box label absent from 50. Semantic disagreement; clarify commercial rules/manufacturers with an expert. |
| q0094 | O0005H | R0002P | DODEGE RAM 400 typo and number favor ISUZU ELF 400; expected RAM 2500 at rank 10. Confirm model/label and resolve brand only with sufficient evidence. |
| q0095 | C0006Z | T000CA | Numeric 35451 description and DODGE DURANGO omit trim/engine. Selected GT PLUS 3.6L; expected RT 5.7L second. Review and request missing attributes. |
| q0132 | T0001Y | Q0008J | F150 lacks drivetrain; selected XL 4X4, expected XL 4X2 second. Do not infer absent attributes; show alternatives and request drivetrain. |
| q0186 | X0001T | B0003G | Query 4400/250HP/4X2; returned 4400/250HP/6X2; expected 4300/210HP/4X2 at rank 28. Crossed evidence; investigate drivetrain and verify model/power with an expert. |
