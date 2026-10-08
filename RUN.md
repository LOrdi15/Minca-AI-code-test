# Ejecutar la entrega

Trabajar desde la raíz que contiene `Makefile`, `data/` y `solution/`.

```bash
make setup
make predict
make check
```

La alternativa directa, útil cuando Make no está disponible, es:

```bash
python -m pip install -r requirements.txt
python -m solution.predict --queries data/queries_blind.csv --out predictions.csv
python submission_check.py --predictions predictions.csv --queries data/queries_blind.csv
```

No se requiere `.env`, clave de OpenAI, caché, etiquetas de consultas ni directorio
de evaluación. Se necesita el catálogo de cuatro CSV y el modelo versionado
`solution/decision_config.json`. Los índices se construyen localmente una vez por
ejecución. El Makefile conserva `PYTHON ?= python3`; si el intérprete disponible
se llama `python`, usar `make PYTHON=python predict`.

## Comprobar y evaluar

```bash
python -m unittest discover -s tests -v
python -m solution.predict --queries data/queries_labeled.csv --out dev_predictions.csv
python score.py --predictions dev_predictions.csv --labels data/queries_labeled.csv
```

`make evaluate` reproduce los experimentos de ranking y calibración sobre las
etiquetas disponibles. No es necesario para `make predict` y no se usa durante
inferencia. Las limitaciones de validación se explican en `EVAL.md`.

## Archivo de salida y fallbacks

Columnas, exactamente en este orden:

```text
query_id,top1_code,top3_codes,confidence,decision
```

Se generan tres códigos distintos del catálogo, unidos con `|`, con top-1 primero.
La política conservadora actual envía todo a review. Los tiempos y los fallbacks
se muestran al terminar; los primeros errores de fila también aparecen en stderr.
Un fallo individual conserva la consulta, asigna confianza cero y review. Un
calibrador ausente/incompatible deshabilita automatización y se informa. IDs
vacíos/duplicados o un catálogo insuficiente son errores globales explícitos.

La predicción ciega se validó: 155 filas, SUBMISSION VALID, unos 20.35 segundos
totales y sin llamadas a LLM. GNU Make no estaba instalado localmente; se ejecutó
el comando equivalente de Python. Las predicciones están ignoradas por Git y se
regeneran con el comando anterior; incluir `predictions.csv` en el ZIP de entrega.
