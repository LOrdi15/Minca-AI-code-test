# Running the submission

Work from the directory containing Makefile, data and solution. Production needs
only the four catalog CSV files, the query CSV and solution/decision_config.json.
It never reads .env, labels, evaluation artifacts or external APIs.

```bash
make setup
make predict
make check
make test
```

PowerShell equivalents, with Python installed:

```powershell
python -m pip install -r requirements.txt
python -m solution.predict --queries data/queries_blind.csv --out predictions.csv
python submission_check.py --predictions predictions.csv --queries data/queries_blind.csv
python -m unittest discover -s tests -v
```

Use `make PYTHON=python predict` when your interpreter is named python rather than
python3. GNU Make was not available in the local Windows environment; direct
Python commands were tested. See evaluation/final for fresh-environment checks.

```bash
python -m solution.predict --queries data/queries_labeled.csv --out dev_predictions.csv
python score.py --predictions dev_predictions.csv --labels data/queries_labeled.csv
python -m solution.audit_evaluation
python -m solution.audit_confidence
```

Output columns: query_id,top1_code,top3_codes,confidence,decision. Top-3 codes are
distinct, catalog-valid, pipe-separated and ordered, with top1 first. Confidence
is finite in [0,1]. The frozen policy returns review for every query. Fallbacks
retain rows, assign confidence zero and are reported. Invalid IDs fail explicitly.

The optional LLM trial is not required for submission. Replay its real stored
results without network or credentials: `python -m experiments.llm_rerank`.
It is inconclusive after HTTP 429, not evidence that LLM quality equals the local
model. Do not run new live requests without permission to share confidential data.

The ZIP includes tracked source/data/documents, predictions.csv and real Git history.
It excludes .env files, secrets, environments and caches. The original data remain
confidential; use the challenge owner's approved return channel.
