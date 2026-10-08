# Vehicle catalog matching

A local Python pipeline maps inconsistent broker vehicle descriptions to insurer
catalog codes. It returns three distinct ranked codes, evidence-based confidence,
and a review decision. The original brief is preserved verbatim in [CHALLENGE.md](CHALLENGE.md).

## Architecture

`catalog.py` joins manufacturers, submodels and versions once, retaining every
description variant. Years belong to codes; missing years are not filled.
`normalization.py` shares conservative normalization between catalog and queries.
`retrieval.py` builds word/character TF-IDF indexes once and retrieves 50 distinct
codes. `ranking.py` scores complete variants using TF-IDF, RapidFuzz and observed
manufacturer, submodel and year compatibility. `decision.py` estimates confidence
from grouped calibration evidence and applies conservative acceptance guards.
`predict.py` orchestrates these components and writes one output row per query.

TF-IDF provides inexpensive, explainable retrieval without external services.
Character features handle spelling variation. RapidFuzz contributes a small
lexical adjustment; structured matching prevents known attribute contradictions
from being hidden by similar descriptions. Scores are not probabilities.

The frozen policy sends every query to review: no tested protected threshold had
adequate evidence for automation. OpenAI is optional experiment code only; its
single live trial returned HTTP 429 and produced no usable reranking results.
It is excluded from production. See [EVAL.md](EVAL.md) and [DECISIONS.md](DECISIONS.md).

## Installation and execution

Python 3.12 was tested. `requirements.txt` pins the tested direct dependencies,
all meeting the challenge minimums. GNU Make and a Python interpreter are needed
for the Make interface; the default interpreter name is `python3`.

```bash
make setup
make predict
make check
make test
```

Windows PowerShell equivalents:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m solution.predict --queries data/queries_blind.csv --out predictions.csv
.\.venv\Scripts\python.exe submission_check.py --predictions predictions.csv --queries data/queries_blind.csv
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

If Make is installed on Windows, `make PYTHON=python setup predict check` selects
the interpreter explicitly. Production does not require an API key, `.env`,
evaluation outputs, absolute paths or external services. Run from the repository
root; catalog paths are relative and the versioned calibration file ships with code.

## Evaluation

```bash
python -m solution.predict --queries data/queries_labeled.csv --out dev_predictions.csv
python score.py --predictions dev_predictions.csv --labels data/queries_labeled.csv
python -m solution.audit_evaluation
python -m solution.audit_confidence
```

`make evaluate` reproduces the original development experiment ledger and grouped
calibration. Audit commands evaluate the frozen configuration. Labels are never
used as inference features. The previously inspected validation split is not a
new independent test. Blind labels are unavailable and were not used for tuning.

## Repository layout

| Path | Purpose |
|---|---|
| `solution/` | Catalog, normalization, retrieval, ranking, decision and CLI |
| `tests/` | Component, decision, pipeline and optional experiment tests |
| `data/` | Original catalog, labeled queries and blind queries |
| `evaluation/` | Real experiment results, failure evidence and final verification |
| `experiments/` | Isolated OpenAI trial; never imported by production |
| `score.py`, `submission_check.py` | Unmodified official evaluation tools |
| `CHALLENGE.md` | Unmodified original challenge brief |
| `EVAL.md`, `DECISIONS.md`, `RUN.md` | Results, engineering decisions and execution guide |

## Output and delivery

The CSV contains exactly `query_id,top1_code,top3_codes,confidence,decision`.
Codes are strings from `versions.csv`, three distinct alternatives separated by
`|`, with top1 first. Confidence is finite in [0,1]; decisions are `auto_accept`
or `review`. Row failures retain the query with valid codes, zero confidence and
review, and are reported. Invalid or duplicate query IDs fail explicitly.

The delivery ZIP includes `predictions.csv`, source, original data, documentation,
official scripts and the real `.git` history. Keys, virtual environments, caches
and temporary files are excluded. The original catalog is confidential: return
the archive only through the challenge owner's approved channel; do not publish it.
