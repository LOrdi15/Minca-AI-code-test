# Auditoría de confianza y decisión

**Todo review es coherente con la política guardada; no es un fallo del pipeline.**
La configuración tiene `threshold: null` porque la selección anterior no aprobó
automatización. Además, incluso activando 0.80 con las protecciones actuales,
ninguna cohorte supera el límite inferior de precisión exigido.

La política sí es deliberadamente conservadora. La alternativa de aceptar por
confianza central 0.80 genera más utilidad observada, pero todavía no demuestra
una mejora suficientemente confiable bajo nuestros criterios previos. Mantener
review sacrifica esa ganancia potencial; no se afirma que maximice el promedio
observado ni que sea óptimo para toda distribución futura.

## Métricas de los 233 registros

| Política | Accuracy top-1 | Recall top-3 | Auto-accept | Precisión auto | Mean utility |
|---|---:|---:|---:|---:|---:|
| Actual / todo review | 60.94% | 80.26% | 0 | No estimable | +0.110515 |
| Confianza central 0.80, simulación | 60.94% | 80.26% | 53 | 88.68% (47/53) | +0.203433 |

La segunda fila combina calibración fuera de fold para los 174 casos de
desarrollo con calibración solo en desarrollo para los 59 casos de validación.
Es un resumen descriptivo de la simulación, no una nueva validación de 233 casos
ni una política activada. Ranking no cambia: cambiar decisión no altera top-1/top-3.

## Cómo se compararon umbrales

Se fijaron 0.80, 0.85, 0.90 y 0.95 antes de medir. Se reprodujo el ranking y se
comprobó igualdad con las últimas predicciones. Desarrollo conserva 174 filas:
cuatro folds por grupos de descripción/año; cada grupo recibe confianza de un
calibrador que no vio sus etiquetas. Los 59 casos restantes usan exclusivamente
la calibración de desarrollo. Se bloqueó la elección diagnóstica antes de calcular
sus resultados. No se leyó el conjunto blind.

Con la regla vigente de **límite inferior Wilson**, los cuatro umbrales devuelven
todo review: utilidad desarrollo +0.110920 y validación +0.109322. La tabla siguiente
muestra la alternativa diagnóstica que usa la estimación central, manteniendo
los bloqueos por atributos, score, margen y mínimo de 20 grupos de calibración.

| Política | Auto desarrollo OOF | Precisión desarrollo | Utilidad desarrollo | Auto validación | Precisión validación | Utilidad validación |
|---|---:|---:|---:|---:|---:|---:|
| Todo review | 0 | — | +0.110920 | 0 | — | +0.109322 |
| Central 0.80 | 44 | 86.36% | **+0.191379** | 9 | 100% | **+0.238983** |
| Central 0.85 | 25 | 80.00% | +0.121552 | 0 | — | +0.109322 |
| Central 0.90 | 0 | — | +0.110920 | 0 | — | +0.109322 |
| Central 0.95 | 0 | — | +0.110920 | 0 | — | +0.109322 |

**0.80 es la mejor alternativa según utilidad observada**, y sus ganancias en los
cuatro folds son positivas: +0.0352, +0.1023, +0.0070 y +0.1779. Eso respalda
investigarla; no elimina la incertidumbre debida a los seis errores y la muestra pequeña.

0.85 acepta algunos casos OOF porque el calibrador de cada fold tiene una mezcla
de aciertos distinta. El calibrador final de desarrollo estima 0.8444 para strong,
por eso 0.85 no acepta ninguno en validación. No hay una contradicción de implementación.

## Por qué la ganancia todavía no habilita producción

La ganancia de 0.80 en desarrollo es +0.08046 por consulta. Bootstrap pareado por
grupos, 20000 muestras: intervalo 95% **[−0.02862, +0.17725]**. Ajustando por las
cuatro comparaciones: **[−0.06264, +0.20029]**. Ambos incluyen pérdida frente a review.
La precisión aceptada observada 86.36% tiene límite inferior Wilson 72.74% por
grupos, inferior al requisito previo de 80%.

Validación ofrece 9/9 aciertos aceptados, pero son solo nueve casos: su límite
inferior de precisión es 70.08%. No se usa ese 100% para fijar un umbral después
de observarlo. El conjunto ya había sido inspeccionado en fases anteriores.

Como orientación económica, si review acertara siempre dentro del top-3,
aceptar tendría ventaja cuando `4p − 3 > 0.15`, es decir `p > 0.7875`.
El requisito de 0.80 es cercano a ese punto; la diferencia importante es exigir
respaldo de incertidumbre, en lugar de confiar solo en la estimación central.
Ese cálculo es una referencia bajo la condición indicada, no una calibración nueva.

El bootstrap no reajusta calibradores ni corrige la selección previa de ranking;
por eso sus intervalos son descriptivos. Con estos datos no se concluye una
garantía de generalización. **No cambiamos el umbral ni el modelo operativo.**

## Distribución de confianza y bloqueos

| Cohorte | Consultas | Confidence guardada | Límite inferior | Aciertos top-1 |
|---|---:|---:|---:|---:|
| blocked | 117 | 46.07% | 35.90% | 53/117 |
| moderate | 63 | 68.18% | 53.97% | 42/63 |
| strong | 53 | 84.44% | 72.74% | 47/53 |

**53 consultas sí superan confidence 0.80; ninguna supera 0.80 en el límite
inferior.** Confidence no es la similitud TF-IDF ni una probabilidad individual
demostrada: cada cohorte comparte una estimación suavizada obtenida de desarrollo.
Strong se apoya en 37 grupos correctos de 43; hay 44 filas porque existen repeticiones.
La escasa granularidad produce únicamente tres valores. Es una limitación explícita.

Los bloqueos se superponen: margen pequeño 71, score bajo 43, conflicto de atributos
31, ningún atributo confirmado 30, año no confirmado 3, descripción no informativa
1 y código ambiguo 1. No se suman como casos independientes.

Los seis errores simulados de aceptación 0.80 son q0014, q0015, q0074, q0093,
q0134 y q0180. Persisten versiones/carrocerías confundidas y el código genérico
Z0000M: similitud alta, margen y compatibilidad básica no prueban versión correcta.
`simulated_auto_accept_errors.csv` conserva códigos, señales y pérdida por consulta.

## Reproducción y resultado de la etapa

```bash
python -m solution.audit_confidence
python -m unittest discover -s tests -v
```

`plan.json`: protocolo previo; `development_selection.json`: elección antes de
validación; `thresholds.csv`/`metrics.json`: comparación e incertidumbre;
`confidence_distribution.csv`: evidencia por consulta; `confidence_buckets.csv`:
distribución; `policy_predictions.csv`: decisiones simuladas con origen de calibración.

**95 pruebas aprobadas**. Calibración recalculada igual al modelo guardado y ranking
idéntico al pipeline auditado. No se cambiaron predict, decision, configuración,
score.py ni submission_check.py. El blind no participó en este análisis.
