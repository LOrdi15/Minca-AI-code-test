# Confidence and threshold audit

Review-only behavior is consistent with the saved null threshold. Fifty-three
labeled queries have confidence 0.8444, but no cohort has a Wilson lower precision
bound >=0.80. Counts: blocked 117, moderate 63, strong 53. Their confidence values
are 0.4607, 0.6818 and 0.8444; lower bounds 0.3590, 0.5397 and 0.7274.

Four grouped calibration folds cover 174 development rows; the remaining 59
previously inspected cases use a development-only calibrator. Ranking remains
frozen. No blind queries were read for this audit.

| Point threshold | Development accepts/errors | Precision | Development utility | Validation accepts/errors | Validation utility |
|---|---:|---:|---:|---:|---:|
| Review all | 0/0 | Undefined | +0.110920 | 0/0 | +0.109322 |
| 0.80 | 44/6 | 86.36% | +0.191379 | 9/0 | +0.238983 |
| 0.85 | 25/5 | 80.00% | +0.121552 | 0/0 | +0.109322 |
| 0.90 | 0/0 | Undefined | +0.110920 | 0/0 | +0.109322 |
| 0.95 | 0/0 | Undefined | +0.110920 | 0/0 | +0.109322 |

All four protected Wilson policies accept zero cases. Point 0.80 gives the largest
observed utility, but its paired development gain interval includes losses:
95% [-0.02862,+0.17725], four-comparison-adjusted [-0.06264,+0.20029]. Nine correct
validation accepts have lower precision bound 70.08%. We retain review, recognizing
the potential gain sacrificed. No post-hoc exclusions were added.

The six simulated errors are q0014, q0015, q0074, q0093, q0134 and q0180. Raw
source evidence and decisions remain in the CSV/JSON artifacts. This is calibrator
OOF evaluation, not nested validation of ranking selection. The holdout was already
inspected; bootstrap does not refit the calibrator or remove selection uncertainty.

Reproduce: `python -m solution.audit_confidence`.
