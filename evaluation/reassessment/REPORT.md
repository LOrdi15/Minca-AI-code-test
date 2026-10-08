# Reevaluación reproducible

Hay **233 registros etiquetados**, no 223. Se ejecutaron de nuevo el pipeline
actual y el baseline. Se conserva la separación: 174 desarrollo y 59 validación.
Ambos conjuntos ya se han usado/inspeccionado; esto no es un test independiente nuevo.

| Métrica, 233 consultas | Baseline original | Solución actual |
|---|---:|---:|
| Recall@50 | 157/233 = 67.38% | 204/233 = 87.55% |
| Accuracy top-1 | 72/233 = 30.90% | 142/233 = 60.94% |
| Recall top-3 | 101/233 = 43.35% | 187/233 = 80.26% |
| Utilidad promedio oficial | +0.036695 | +0.110515 |
| Auto-accept | 0 | 0 |
| Precisión de auto-accept | No estimable | No estimable |
| Revisión | 100% | 100% |

Recall@50 del baseline es una extensión diagnóstica de su mismo cálculo y
desempate; su CLI solo emite tres candidatos. Se comprobó igualdad de top-1/top-3
contra el CLI original. El scorer imprime precisión 0% sin aceptaciones; no es
una precisión observada, porque no hay denominador. Nuestro JSON guarda `null`.

En los 59 casos de validación anterior: solución top-1 59.32%, top-3 79.66%,
recall@50 89.83%, utilidad +0.109322; baseline 27.12%, 42.37%, 61.02%, +0.034746.
La política actual coincide con enviar todo a review. Aceptar todos daría
utilidad −0.562232: la similitud no justifica automatización.

## Diez errores comprobados

De 91 fallos top-1: 29 no recuperan el esperado entre 50, 17 lo recuperan pero
queda fuera de top-3 y 45 lo incluyen pero no primero. Z0000M representa 23 de
los 29 fallos de recuperación; aclarar su uso con experto antes de crear reglas.
Las causas son hipótesis fundamentadas; no prueban etiquetas incorrectas.

| Consulta | Esperado → devuelto | Por qué fallamos |
|---|---|---|
| q0005 | U0003D → P00000 | Pide 28000 LBS y elegimos 30000. Falta reconocer capacidad y equiparar 28,000 con 28000. Correcto segundo. |
| q0016 | Z0000M → S0008A | Pide plataforma y devolvemos plataforma; etiqueta caja cerrada. Posible regla genérica del negocio por confirmar. Correcto puesto 43. |
| q0024 | Q00046 → U0003Y | Tanque con texto muy parecido, pero años hasta 2022; consulta 2023. Esperado válido fuera de 50: el ranking no puede recuperarlo. |
| q0035 | Q0004P → R00034 | S3 sedán: elegimos 3 puertas en vez de 4. No interpretamos carrocería/puertas. Correcto segundo. |
| q0050 | Z0000M → W0008G | Pide caja refrigerada; etiqueta caja cerrada. Seguimos el texto; falta aclarar criterio de negocio. Correcto puesto 34. |
| q0085 | Z0000M → J0007M | Pide tolva y recuperamos tolva; etiqueta caja cerrada. Discrepancia semántica, esperado fuera de 50. |
| q0094 | O0005H → R0002P | DODEGE RAM 400 tiene marca con errata. El 400 favorece ISUZU ELF 400; se espera RAM 2500. Correcto puesto 10; confirmar modelo. |
| q0095 | C0006Z → T000CA | Descripción 35451 con DODGE DURANGO no especifica versión/motor. GT PLUS 3.6L frente a RT 5.7L. Correcto segundo; faltan datos. |
| q0132 | T0001Y → Q0008J | F150 sin tracción: XL 4X4 frente a XL 4X2. Correcto segundo; no podemos deducir atributo ausente. |
| q0186 | X0001T → B0003G | Entrada 4400/250HP/4X2; devuelto 4400/250HP/6X2; esperado 4300/210HP/4X2, puesto 28. Atributos cruzados y falta puntuar tracción. |

`ten_errors.csv` conserva texto, atributos, códigos, descripciones del catálogo,
años, posiciones y señales del ranking. Los diez fallos se validan en cada ejecución.

## Experimento R1: motores como una sola palabra

Se escribió la hipótesis antes de medir: conservar 2.0L como un token TF-IDF en
vez de 2 y 0L. Solo cambió el índice experimental en memoria; pesos, normalización
y caracteres permanecieron fijos. Sin alias ni excepciones por consulta.

| Resultado, 233 consultas | Actual | R1 |
|---|---:|---:|
| Top-1 correcto | 142 | 145 |
| Top-3 correcto | 187 | 187 |
| Recuperado entre 50 | 204 | 206 |
| Utilidad promedio, review | +0.110515 | +0.110515 |

Cambian 14 listas, pero ninguna cambia la presencia del esperado en top-3.
Los tres aciertos top-1 y dos recuperaciones adicionales ocurren en desarrollo;
validación no mejora. Delta de utilidad 0 en ambos subconjuntos; intervalo
bootstrap pareado por grupos [0, 0]. Es incertidumbre descriptiva, no datos nuevos.

**Rechazado para producción:** no mejora utilidad. Se conserva el experimento para
investigación futura. No se reutilizó el calibrador para afirmar confianza del
índice modificado: se midió con review general. No cambió el modelo operativo.

## Reproducción y comprobación

```bash
python -m solution.audit_evaluation
python -m unittest discover -s tests -v
python -m solution.baseline --queries data/queries_labeled.csv --versions data/versions.csv --out evaluation/reassessment/baseline_cli_predictions.csv
python score.py --predictions evaluation/reassessment/current_predictions.csv --labels data/queries_labeled.csv
python score.py --predictions evaluation/reassessment/baseline_cli_predictions.csv --labels data/queries_labeled.csv
python -m solution.predict --queries data/queries_blind.csv --out predictions.csv
python submission_check.py --predictions predictions.csv --queries data/queries_blind.csv
```

`metrics.json`: resultados, incertidumbre y decisión del experimento.
`current_details.csv`, `baseline_details.csv`: recuperación/ranking separados.
`R1_details.csv`, `R1_changed_queries.csv`: cambios observados.
`verification.json`: comprobaciones oficiales y contrato adicional.

Pasaron **92 pruebas**. La solución tuvo cero fallbacks por consulta y calibración.
El validador aceptó los 233 casos etiquetados. No se modificaron score.py,
submission_check.py ni componentes operativos. Make sigue sin estar disponible;
se ejecutaron comandos Python directamente.

Se regeneraron las 155 consultas ciegas: **SUBMISSION VALID**, cero fallbacks,
17.38 s dentro del pipeline (catálogo e índices incluidos), 1.27 s procesando
consultas. El CSV es idéntico byte a byte al de la integración anterior. Se
verificaron además orden/cobertura de IDs, cinco columnas exactas, tres códigos
distintos existentes, top-1 primero y confianza finita entre 0 y 1.
