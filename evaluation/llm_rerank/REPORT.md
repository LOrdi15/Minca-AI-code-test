# Experimento aislado de reranking OpenAI

**Resultado: ejecución inconclusa por HTTP 429. No incorporado a producción.**
Se realizó un intento real con la clave existente, tras autorización explícita
del usuario para reutilizarla y compartir los datos mínimos de validación/catálogo.
La API respondió `RateLimitError`, HTTP 429, en la primera consulta, q0003.
No se recibió ninguna respuesta válida ni información de uso de tokens.
No repetimos llamadas. La causa concreta (cuota, créditos o velocidad) no quedó
registrada en el primer intento; no se afirma una de ellas sin evidencia.
La [documentación oficial de errores](https://developers.openai.com/api/docs/guides/error-codes)
distingue varias causas de 429; el estado HTTP por sí solo no basta para clasificarlas.

## Protocolo fijado antes de llamar

- Solo los 59 IDs de validación anteriores; nunca blind.
- Ruta ambigua: margen entre primero y segundo <0.08 o conflicto explícito de
  atributos. Produce 38 consultas elegibles sin utilizar sus etiquetas.
- Recuperación TF-IDF existente de 50 códigos; shortlist de diez códigos del
  ranking local. No se añaden códigos por conocimiento del LLM ni por etiquetas.
- Todas las variantes de esos diez códigos, con fabricante, submodelo, descripción,
  tipo y años explícitos por código. Candidatos presentados en orden alfabético
  para no inducir el orden local. No se combinan atributos de variantes diferentes.
- Se envían únicamente atributos observables de consulta y candidatos. No se
  envían query_id, expected_code, respuestas del experto ni el catálogo completo.
- Una configuración: `gpt-4.1-mini-2025-04-14`, temperatura 0, máximo 180 tokens,
  JSON estricto con códigos restringidos por enum; validación adicional de tres
  códigos distintos. El modelo puede abstenerse, conservando el orden local.
- Todo review; confidence experimental cero porque el calibrador del modelo
  local no valida órdenes producidos por otro método.
- Sin cambios de prompt/modelo después de observar resultados. Promoción exige
  evaluación completa y límite inferior positivo de utilidad pareada por grupos;
  aun así necesitaría validación nueva antes de cualquier automatización.

El [modelo documentado](https://developers.openai.com/api/docs/models/gpt-4.1-mini)
soporta salidas estructuradas y tiene tarifa de USD 0.40/M tokens de entrada y
USD 1.60/M de salida. Se usó el SDK 3.26.0, compatible con el mínimo del reto.
`store=False` evita habilitar almacenamiento de respuestas para recuperación;
no se afirma que suprima todas las retenciones del proveedor. La autorización
del usuario, no ese parámetro, permitió el envío.

## Presupuesto y errores

Límite local USD 1.90, inferior al presupuesto de USD 2. Reserva conservadora por
llamada antes de enviar: bytes UTF-8 de mensajes/esquema, margen de 4096 tokens y
salida máxima. La suma para las 38 llamadas planeadas era **USD 0.141524**.
Sin reintentos del SDK, ejecución secuencial, timeout 20 segundos y tope de 420
segundos. Errores conservan la predicción local. El ledger persistente evita
repetir llamadas pendientes o realizadas y detiene nuevas llamadas tras errores
de acceso/cuota/rate limit, incluso al volver a ejecutar.

Se intentó **una llamada**, con cero éxitos y duración de 1.54 s. Al no recibir
usage, el costo facturado no pudo medirse: el ledger conserva la reserva máxima
de **USD 0.0039368**. El cero en costo estimado por usage significa ausencia de
uso reportado, no una verificación de factura. No se excedió el presupuesto.
La clave y cuerpos de error nunca se imprimen ni se guardan en los resultados.

## Comparación sobre validación

| Resultado, 59 consultas | Modelo local | Experimento con fallback |
|---|---:|---:|
| Accuracy top-1 | 35/59 = 59.32% | 35/59 = 59.32% |
| Recall top-3 | 47/59 = 79.66% | 47/59 = 79.66% |
| Mean utility | +0.109322 | +0.109322 |
| Respuestas válidas del LLM | No aplica | **0** |

**Esta igualdad solo verifica el fallback; no mide la calidad del LLM.** El
intervalo pareado [0,0] también refleja salidas locales idénticas. La ejecución
está marcada `inconclusive_incomplete_api_run`. No afirmamos que OpenAI empeore,
iguale o mejore el modelo. Se excluye de la entrega operativa por falta de una
mejora demostrada y para priorizar la solución reproducible.

## Reproducibilidad y entrega

```bash
# Reproduce el informe desde el registro, sin API ni clave:
python -m experiments.llm_rerank
python score.py --predictions evaluation/llm_rerank/llm_predictions.csv --labels evaluation/llm_rerank/validation_labels.csv
python submission_check.py --predictions evaluation/llm_rerank/llm_predictions.csv --queries evaluation/llm_rerank/validation_queries.csv
python -m unittest discover -s tests -v
```

Las etiquetas del scorer deben cubrir esos 59 IDs, no las 233 filas completas:
las ausencias se penalizan en el scorer oficial. Se conservan CSV específicos
del subconjunto para evitar ese error de evaluación.

Para una ejecución desde cero, `--prepare` genera plan y solicitudes sin API,
y `--live --env-file .env` requiere autorización explícita de datos/credenciales.
El experimento registrado rechaza sobrescribir su ledger o reanudar llamadas
tras el 429; una prueba futura requiere resolver el acceso y conservar este
registro. Producción no lee `.env` ni importa `experiments`.

Resultados reales en `plan.json`, `manifest.json`, `calls.json`, `metrics.json`
y `details.csv`. `requests.json` conserva payloads locales confidenciales y no
contiene la clave. Pruebas: **103 aprobadas**, incluidas ocho de restricciones,
presupuesto, errores y reanudación sin nuevas llamadas. El pipeline local y el
CSV ciego permanecen iguales; no se modificaron score.py ni submission_check.py.
