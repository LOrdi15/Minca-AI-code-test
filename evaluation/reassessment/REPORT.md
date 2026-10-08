# Frozen model reassessment

The dataset contains 233 labeled rows, not 223. The original baseline CLI was
reproduced and its predictions matched the evaluation implementation.

| Metric | Baseline | Frozen model |
|---|---:|---:|
| Top-1 accuracy | 30.90% | 60.94% |
| Top-3 recall | 43.35% | 80.26% |
| Recall@50 | 67.38% | 87.55% |
| Mean utility | +0.036695 | +0.110515 |

Baseline recall@50 is a diagnostic extension of its original scoring, not an
output of the shipped three-result CLI. Both policies review all cases; acceptance
precision is undefined. Development 174 and previously inspected validation 59
remain separate. Overall results are descriptive, not independent generalization.

R1 kept engine tokens such as 2.0L together. It improved top-1 from 142 to 145 and
recall@50 from 204 to 206, but top-3 remained 187 and utility +0.110515. No validation
gain occurred. Fourteen lists changed without changing expected-code inclusion.
The paired utility delta was zero. The trial was rejected for production.

metrics.json contains actual results and uncertainty. R1_changed_queries.csv
preserves changes; ten_errors.csv preserves source texts, variants, years and
failure evidence. EVAL.md contains the ten English technical analyses.

Reproduce: `python -m solution.audit_evaluation`. Source vehicle descriptions
remain in their original language to preserve evidence and matching behavior.
