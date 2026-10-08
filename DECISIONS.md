# Engineering decisions

We ship a frozen, local, explainable pipeline: 155 valid blind predictions and no
production API calls. On 233 labeled cases: top-1 60.94%, top-3 80.26%, recall@50
87.55%, mean utility +0.110515 versus baseline +0.036695. These are descriptive
results, not a guarantee of blind utility.

## Architecture and rejected alternatives

We retain complete catalog variants and explicit years per code. Shared conservative
normalization preserves vehicle details. Word/character TF-IDF retrieves 50 codes
cheaply and handles spelling variation. Reranking uses 90% TF-IDF, 10% RapidFuzz
and small manufacturer, submodel and year adjustments. Each variant is scored
as a whole; metadata is never borrowed from another variant.

RapidFuzz at 30%, strong brand penalties and vehicle-type scoring reduced development
top-3 recall. Stronger year penalties did not help. Keeping 2.0L as one TF-IDF token
improved three top-1 cases but not utility or validation; we rejected it. We did
not relabel data, add manual aliases or favor the frequent Z0000M label.

An authorized, isolated OpenAI trial used ten existing candidates. Its first
request returned HTTP 429, with no usable responses. This is inconclusive, not
evidence of equal model quality. OpenAI is excluded from production. The unknown
billing usage retains a conservative USD 0.0039368 reservation.

## Confidence and acceptance policy

Similarity is not correctness probability. Confidence is a Beta(1,1)-smoothed
success rate in three fixed evidence cohorts, counting repeated description/year
groups once per cohort. We compare 0.80/0.85/0.90/0.95 using four grouped folds
within 174 development cases; each group receives calibration that did not see it.

Acceptance requires attribute guards, at least 20 calibration groups, sufficient
Wilson lower precision bound, higher utility and no harmful fold. No protected
threshold passes: we retain **review**, with auto-accept precision undefined.

Point-confidence 0.80 maximizes observed utility: +0.191379, 44 accepts, six errors,
86.36% precision, versus review +0.110920. However, the development utility-gain
95% interval [-0.02862,+0.17725] includes losses and the precision lower bound is
72.74%, below 80%. The inspected validation set has nine correct accepts, too few
to establish safety. Four errors are commercial vehicles and two SUVs; none trips
the current guards. We add no segment or query-specific exclusions after seeing
these errors, and acknowledge the potential utility sacrificed by retaining review.

Ranking was already selected on development. Out-of-fold validation covers the
calibrator, not the entire selection process. The 59-case holdout was previously
inspected; broad cohorts and Wilson bounds do not protect against distribution
shift. Blind data contain a harder commercial mix.

## Underdetermined inputs

Return three valid, distinct codes and review. Recognized conflicts, ambiguous or
incomplete catalog relations, empty descriptions, unconfirmed years and small
margins block acceptance. Missing engine, drivetrain or trim should be requested;
a deterministic tie-break provides no certainty. Fallbacks retain the query with
zero confidence and review, with visible diagnostics.

## Two additional weeks

Clarify generic business codes and verify commercial labels first. Then extract
capacity, engine, drivetrain, doors and transmission, measuring retrieval and utility
regressions. Obtain new labels and independent evaluation by source/group. Refine
calibration only with adequate support. Revisit LLMs only with measurable gains.

## Four hours with a domain expert

- 90 minutes: Z0000M semantics and commercial classification rules.
- 60 minutes: resolve the ten failures and six simulated false accepts.
- 60 minutes: minimum attributes distinguishing versions and when to abstain.
- 30 minutes: accepted taxonomies and abbreviations with verified examples.

This knowledge addresses ambiguities that the available text cannot resolve.
