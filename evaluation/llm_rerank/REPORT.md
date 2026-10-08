# Isolated OpenAI reranking trial

**Inconclusive: the first real API request returned HTTP 429.** No valid model
response was received. The local fallback was retained and OpenAI was excluded
from production. Equal fallback metrics do not establish equal LLM quality.

The user authorized sending minimal validation/catalog attributes and reusing the
existing credential. The frozen protocol routed margin <0.08 or recognized
attribute conflicts: 38 eligible queries among the existing 59 validation IDs.
Each request used ten locally ranked codes from the unchanged 50-code retrieval.
Variants and explicit years were included; labels, query IDs, full catalog and blind
queries were not sent. Candidate presentation order was alphabetical.

Model: gpt-4.1-mini-2025-04-14, temperature zero, at most 180 output tokens,
strict JSON restricted to supplied codes. Three distinct codes are checked locally.
The model may abstain. Experimental decisions are review with confidence zero;
local calibration is not transferred to changed ranking. store=False was used,
without claiming it eliminates all provider retention.

One configuration was fixed before evaluation. Local budget cap USD 1.90;
conservative reservation for all 38 planned requests USD 0.141524. SDK retries
disabled; sequential requests, 20-second timeout, 420-second execution cap. The
persistent ledger reserves cost before requests and prevents repeated failed or
pending calls. Fatal access/quota/rate errors also stop subsequent invocations.

One request, q0003, failed with RateLimitError/HTTP 429 after 1.54 seconds. Usage
was unavailable: the ledger retains USD 0.0039368 as an upper reservation; actual
invoice cost was not measured. Zero reported usage is not verified zero billing.
The initial error code was not retained, so quota exhaustion and throttling are
not distinguished without evidence. Keys and error bodies are never logged.

| Validation metric, 59 cases | Local | Trial with fallback |
|---|---:|---:|
| Top-1 accuracy | 59.32% | 59.32% |
| Top-3 recall | 79.66% | 79.66% |
| Mean utility | +0.109322 | +0.109322 |
| Valid LLM responses | Not applicable | 0 |

The trial is marked incomplete; the [0,0] paired interval describes identical
fallbacks only. No claim of LLM improvement, degradation or equivalence is made.
Original prompt and payloads remain unchanged as experimental evidence.

Replay without network: `python -m experiments.llm_rerank`. Score only against
validation_labels.csv, not all 233 labels, because missing predictions are penalized.
The production CLI does not import experiments or read .env. Eight tests cover
output constraints, budget reservations, errors and replay without extra calls.

Official references: [model and prices](https://developers.openai.com/api/docs/models/gpt-4.1-mini),
[structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs),
[error codes](https://developers.openai.com/api/docs/guides/error-codes).
