# Evaluación — recuperación y ranking

Estado actual: recuperación, ranking y confianza por grupos de evidencia
implementados. La política seleccionada conserva `review` porque ningún umbral
superó los requisitos de incertidumbre y soporte. En la etapa original de ranking
la confianza era `0.0`; ahora se exporta una estimación empírica suavizada. El score
de ranking no es una probabilidad. `make predict` sigue ejecutando el baseline hasta
la etapa de integración final; esta no es todavía la entrega ciega.

## 1. Resultados y separación de componentes

Hay **233 consultas etiquetadas**, no 223. Separamos 174 para desarrollo y 59 para
validación. Usamos el primer fold de `StratifiedGroupKFold`, cuatro folds y semilla
42; la agrupación por descripción normalizada + año evita distribuir consultas
repetidas equivalentes entre ambos conjuntos. La estratificación por segmento es
aproximada al respetar esos grupos. El detalle de pertenencia está en
`evaluation/split.csv`.

Los índices se ajustan exclusivamente con el catálogo. Las respuestas esperadas
no entran en recuperación ni ranking. Los pesos se seleccionaron utilizando
desarrollo; después se congelaron en `evaluation/ranking_selection.json` antes de
abrir las métricas de validación. No hubo ajustes posteriores sobre validación.
Los diez fallos se analizaron después de congelar la configuración.

| Conjunto / sistema | Top-1 | Recall top-3 | Recall@50 | Utilidad, todo a revisión |
|---|---:|---:|---:|---:|
| Desarrollo, baseline original (174) | 56/174 = 32.2% | 76/174 = 43.7% | 121/174 = 69.5%* | +0.0374 |
| Desarrollo, seleccionado (174) | 107/174 = 61.5% | 140/174 = 80.5% | 151/174 = 86.8% | +0.1109 |
| Validación, baseline original (59) | 16/59 = 27.1% | 25/59 = 42.4% | 36/59 = 61.0%* | +0.0347 |
| Validación, seleccionado (59) | 35/59 = 59.3% | 47/59 = 79.7% | 53/59 = 89.8% | +0.1093 |
| Total descriptivo, baseline (233) | 72/233 = 30.9% | 101/233 = 43.3% | 157/233 = 67.4%* | +0.0367 |
| Total descriptivo, seleccionado (233) | 142/233 = 60.9% | 187/233 = 80.3% | 204/233 = 87.6% | +0.1105 |

\* El baseline original solo devuelve tres filas. Su recall@50 es una extensión
diagnóstica de la misma fórmula y desempate a 50 códigos distintos; no es una
métrica que produzca el script original. Top-1 y top-3 sí reproducen exactamente
el baseline incluido, sin modificarlo. Se comprobó también con `score.py`.

El recall@50 se mide **antes del ranking**, sobre códigos distintos. Entre las 53
consultas de validación cuyo código esperado fue recuperado, el ranking acertó
35: **66.0%**. En los 233 casos, tenemos 29 fallos de recuperación, 17 casos con
respuesta recuperada pero fuera del top-3, y 45 casos con respuesta en top-3 pero
no en primera posición. Son problemas diferentes.

El total mezcla desarrollo y validación: es descriptivo, no una estimación
independiente. La validación es pequeña y proviene del conjunto etiquetado; no
garantiza la misma utilidad sobre las consultas ciegas, con más peso comercial.

### Configuración seleccionada

- Recuperación: texto de fabricante + submodelo + descripción, sobre cada
  variante; TF-IDF de palabras/unigramas-bigramas (65%) y caracteres 3–5 (35%).
- Se conserva el mejor score por código para recuperar 50 códigos distintos;
  todas sus variantes siguen disponibles para ranking, sin filtros previos de
  marca, año o tipo.
- Ranking base: **90% TF-IDF + 10% RapidFuzz WRatio**.
- Año: +0.12 si está registrado, −0.20 si el catálogo conoce años y no lo incluye.
- Fabricante reconocido: +0.02 si coincide, −0.10 si contradice.
- Submodelo reconocido: +0.02 si coincide, −0.05 si contradice.
- Tipo: incompatibilidad detectada y registrada, pero aporte al score desactivado
  porque perjudicó desarrollo. Los valores genéricos o desconocidos son neutros.

Los nombres se reconocen con el vocabulario del catálogo, coincidencias explícitas
y, para pequeñas erratas, ratio >=90 con margen >=10 sobre la segunda opción.
No hay diccionario manual de marcas. La equivalencia de tipos es una traducción
limitada entre taxonomías, separada de la normalización textual. `TOLVA`, `CAJA`
y `CAMIONETA` no determinan un tipo por sí mismas.

Se evalúa cada variante completa y luego se toma la mejor por código: no se toma
la descripción de una variante y el fabricante de otra. Los conflictos conocidos,
catálogo ambiguo y ausencia de evidencia textual quedan expuestos para revisión.
En esta etapa no se acepta automáticamente ningún caso.

### Segmentos, total descriptivo

| Segmento | n | Top-1 | Top-3 | Recall@50 |
|---|---:|---:|---:|---:|
| AUTO | 67 | 77.6% | 92.5% | 98.5% |
| CAMION | 41 | 53.7% | 80.5% | 82.9% |
| OTHER | 55 | 63.6% | 90.9% | 96.4% |
| PICKUP | 18 | 61.1% | 88.9% | 100.0% |
| REMOLQUE | 35 | 25.7% | 31.4% | 48.6% |
| TRACTO | 17 | 76.5% | 88.2% | 94.1% |

REMOLQUE es la principal debilidad. El código `Z0000M` aparece como etiqueta en 33
consultas y concentra 23 de los 29 fallos de recuperación. Su descripción es
`RM CAJA CERRADA 2 EJES 40`, pero aparece en consultas de tolvas, plataformas e
incluso camiones. Esto puede reflejar una regla del dominio o etiquetas discutibles;
no se corrigieron etiquetas ni se introdujo ese código como fallback para elevar
la métrica. Es una pregunta prioritaria para el experto de dominio.

### Confianza y política de decisión

Se congeló el ranking E8. La calibración usa solo los 174 casos de desarrollo;
los 59 casos reservados no se usan para ajustarla ni seleccionar umbrales. Para
seleccionar la política se ejecutan cuatro folds agrupados por descripción + año
(semilla 17): cada caso recibe confianza de un calibrador que no vio su grupo.
Esto es validación fuera de fold **del calibrador**. Los pesos del ranking ya
fueron seleccionados con ese desarrollo: no es validación anidada del sistema
entero. Además, los 59 casos ya se habían inspeccionado en la etapa anterior;
su comparación secundaria no se presenta como un nuevo test intacto.

Antes de observar resultados de esta etapa se fijaron tres grupos de evidencia:

- Bloqueado: contradicciones, relaciones incompletas, catálogo ambiguo, descripción
  no informativa, falta de segundo candidato, similitud TF-IDF nula, año no
  confirmado, ningún otro atributo confirmado, score <0.55 o margen <0.03.
- Fuerte: sin bloqueos, score >=0.75 y margen contra el segundo >=0.08.
- Moderado: sin bloqueos, pero sin cumplir ambos requisitos del grupo fuerte.

La confianza es `(grupos correctos + 1) / (grupos observados + 2)`, con suavizado
Beta(1,1). Un grupo repetido cuenta una vez por cohorte; si alguna de sus filas
falla, se cuenta como fallo del grupo. Así las repeticiones no inflan soporte.
No es similitud ni una probabilidad individual garantizada. Un grupo no observado
recibe prior 0.5, soporte cero y revisión obligatoria.

| Cohorte, calibrador final sobre desarrollo | Grupos correctos / total | Confianza | Límite inferior Wilson 95% |
|---|---:|---:|---:|
| Bloqueado | 40/87 | 46.1% | 35.9% |
| Moderado | 29/42 | 68.2% | 54.0% |
| Fuerte | 37/43 | 84.4% | 72.7% |

Para aceptar se requieren al menos 20 grupos de calibración y que el **límite
inferior**, no solo la estimación central, supere el umbral. La utilidad esperada
de aceptar es `4p−3`; la revisión puede valer hasta 0.15. Superar esa alternativa
requiere `p>0.7875`. Elegimos 0.80 como mínimo conservador y comparamos 0.80,
0.85, 0.90 y 0.95 sin buscar cortes específicos para consultas individuales.

Para seleccionar una política además exigimos 20 grupos distintos aceptados en
validación agrupada, precisión con límite inferior >=0.80, utilidad mayor que
revisar todo y ningún fold con utilidad inferior a esa referencia. Empates
favorecen menor automatización. Ningún umbral cumplió las condiciones.

| Política protegida, validación agrupada de desarrollo (174) | Aceptados | Precisión auto | Revisión | Top-3 recall | Utilidad |
|---|---:|---:|---:|---:|---:|
| Review general, seleccionado | 0 | No estimable | 100% | 80.5% | +0.1109 |
| Umbral 0.80, con soporte y Wilson | 0 | No estimable | 100% | 80.5% | +0.1109 |
| Umbral 0.85, con soporte y Wilson | 0 | No estimable | 100% | 80.5% | +0.1109 |
| Umbral 0.90, con soporte y Wilson | 0 | No estimable | 100% | 80.5% | +0.1109 |
| Umbral 0.95, con soporte y Wilson | 0 | No estimable | 100% | 80.5% | +0.1109 |
| Baseline original, review general | 0 | No estimable | 100% | 43.7% | +0.0374 |

También medimos referencias diagnósticas que conservan bloqueos y mínimo de
soporte pero **ignoran el intervalo** y confían solo en la estimación central:

| Referencia diagnóstica, no desplegada | Aceptados / errores | Precisión auto | Revisión | Top-3 recall | Utilidad |
|---|---:|---:|---:|---:|---:|
| Confianza central >=0.80 | 44 / 6 | 86.4% | 74.7% | 80.5% | +0.1914 |
| Confianza central >=0.85 | 25 / 5 | 80.0% | 85.6% | 80.5% | +0.1216 |
| Confianza central >=0.90 | 0 / 0 | No estimable | 100% | 80.5% | +0.1109 |
| Confianza central >=0.95 | 0 / 0 | No estimable | 100% | 80.5% | +0.1109 |

**No afirmamos que review maximice la utilidad observada sin restricciones.** La
referencia 0.80 obtiene una media mayor, pero su precisión agrupada tiene límite
inferior 72.7%, insuficiente frente al mínimo de negocio conservador. La de 0.85
es inestable y su límite inferior cae a 60.9%. No se habilitó automatización para
perseguir esos números con una muestra pequeña. Los seis errores de la primera
referencia quedan en `evaluation/decision_diagnostic_errors.csv`; no son errores
automáticos de la política desplegada, que conserva revisión.

En los 59 casos previamente reservados, la política seleccionada mantiene utilidad
+0.1093, top-3 79.7% y revisión 100%; el baseline obtiene +0.0347 y top-3 42.4%.
El top-3 no cambia al cambiar decisiones: los candidatos son los mismos.

Limitaciones: tres cohortes amplias no capturan diferencias por segmento; los
límites Wilson suponen grupos aproximadamente independientes y no protegen ante
cambio de distribución o errores sistemáticos de etiquetas. El ranking tuvo ajuste
previo sobre desarrollo. La confianza final de desarrollo es interna a calibración;
la evidencia para escoger el umbral es la evaluación fuera de fold. Hacen falta
más etiquetas verificadas, especialmente comerciales, para habilitar aceptación.

## 2. Registro de experimentos

Todas las decisiones se tomaron con los **174 casos de desarrollo**, priorizando
recall top-3 (equivalente a utilidad con revisión general), y top-1 como desempate.
Cada experimento parte de la última configuración conservada. El registro exacto
incluye pesos y métricas en `evaluation/ranking_selection.json`.

| Experimento | Cambio | Top-1 | Top-3 | @50 | Decisión |
|---|---|---:|---:|---:|---|
| Baseline original | Descripción únicamente, solapamiento | 56 | 76 | 121* | Referencia |
| E0 | Catálogo integrado, TF-IDF palabras | 60 | 100 | 145 | Conservar como inicio |
| E1 | 35% caracteres + 65% palabras | 66 | 106 | 151 | Conservar |
| E2 | Ranking con 30% RapidFuzz | 67 | 103 | 151 | Revertir: pierde tres top-3 |
| E3 | Año +0.12 / −0.20 | 105 | 139 | 151 | Conservar |
| E4 | Penalizaciones fuertes de marca/submodelo | 104 | 136 | 151 | Revertir: metadatos ruidosos |
| E5 | Tipo +0.04 / −0.15 | 104 | 137 | 151 | Revertir: pierde dos top-3 |
| E6 | Año incompatible −0.60 | 105 | 139 | 151 | Revertir: sin beneficio |
| E7 | RapidFuzz reducido al 10% | 107 | 139 | 151 | Conservar: mejor top-1 |
| E8 | Marca/submodelo con ajustes pequeños | 107 | 140 | 151 | Conservar: mejora top-3 |
| E9 | Tipo reducido a +0.01 / −0.05 | 106 | 139 | 151 | Revertir: sigue perjudicando |

La configuración final es E8. La mejora incremental de marca/submodelo es pequeña
(un caso); no se interpreta como evidencia de una calibración sólida. Las
configuraciones rechazadas siguen reproducibles en el evaluador, pero no están
activas por defecto.

Experimentos de decisión: D0, tres cohortes fijas y confianza suavizada; D1–D4,
umbrales protegidos 0.80/0.85/0.90/0.95, sin evidencia para automatizar; D5–D8,
referencias de estimación central sin Wilson, solo diagnósticas y rechazadas para
producción. Se conserva review general. Los conteos y métricas exactos están en
`evaluation/decision_thresholds.csv` y `evaluation/decision_metrics.json`.

## 3. Diez fallos concretos de validación

El campo `devuelto` muestra el top-1. La lista completa de tres candidatos,
posición inicial de la etiqueta y señales están en `evaluation/ranking_details.csv`.
Las causas siguientes son hipótesis fundamentadas en los textos, no nuevas
etiquetas ni hechos confirmados por un experto.

| query_id | Esperado | Devuelto | Diagnóstico y acción propuesta |
|---|---|---|---|
| q0005 | U0003D | P00000 | El correcto quedó segundo. Consulta FORD F700 de 28000 LBS; devolvimos la variante de 30000 LBS. La representación `28000` frente a `28,000` y la similitud general no protegen capacidad. Probar extracción contextual de capacidad y separadores de miles en una siguiente etapa de desarrollo. |
| q0016 | Z0000M | S0008A | Recuperamos el esperado en posición 43, pero la consulta dice PLATAFORMA y el esperado CAJA CERRADA. La opción devuelta dice PLATAFORMA. Consultar si la etiqueta representa un código genérico de negocio; no forzar ese código sin explicación. |
| q0024 | Q00046 | U0003Y | El esperado no apareció en 50. Consulta TANQUE A.INOX de 31000 LTS, año 2023; el devuelto coincide mucho con texto pero solo tiene años hasta 2022. El esperado es SEMIREMOLQUE TANQUE ELIPTICO y sí incluye 2023. Mantener conflicto de año visible y evaluar recuperación alternativa por categoría/atributos, sin excluir primero los candidatos. |
| q0035 | Q0004P | R00034 | Esperado en segundo lugar. Consulta AUDI S3 SEDAN; devuelto S3 de 3 puertas, esperado A3 S3 de 4 puertas. Falta incorporar carrocería/puertas y reconocer el significado de SEDAN. Pedir datos adicionales o revisar hasta validar esa señal. |
| q0050 | Z0000M | W0008G | Esperado recuperado en posición 34, fuera del top-3. Consulta CAJA REFRIGERADA; devuelto CAJA REFRIGERADORA CON EQUIPO, esperado CAJA CERRADA. Posible regla de clasificación genérica del dominio. Revisar con experto, sin convertir similitud textual en certeza. |
| q0085 | Z0000M | J0007M | Fallo de recuperación. Consulta TOLVA / DALTO; devolvimos una tolva granelera, mientras la etiqueta es CAJA CERRADA. Hay insuficiencia de atributos y discrepancia semántica. Preguntar por reglas para fabricantes no reconocidos y etiquetas genéricas. |
| q0094 | O0005H | R0002P | Correcto recuperado en posición 10, fuera del top-3. Consulta DODEGE RAM 400; el devuelto es ISUZU ELF 400 y la etiqueta es RAM 2500. La errata de marca no se reconoce con suficiente seguridad y el número 400 favorece otra familia. Marcar incompatibilidad de tipo, revisar marca y confirmar el modelo antes de introducir alias. |
| q0095 | C0006Z | T000CA | Correcto quedó segundo. Descripción `35451`, marca DODGE y submodelo DURANGO: no especifica RT ni motor. Devuelto GT PLUS 3.6L; esperado RT 5.7L. El texto disponible no permite justificar una única versión; pedir versión/motor o mantener revisión. |
| q0132 | T0001Y | Q0008J | Correcto quedó segundo. Consulta F150 con marca FORD (ROJA); opciones XL cabina regular 4X2 y 4X4 del mismo año. No hay tracción en la entrada. Mantener ambas opciones y solicitar 4X2/4X4; no resolver por un desempate arbitrario con aceptación automática. |
| q0186 | X0001T | B0003G | Esperado recuperado en posición 28. Consulta MOD4400, 250, 4X2; devuelto 4400 250HP 6X2, esperado 4300 210HP 4X2. Hay señales cruzadas y discrepancias entre entrada/etiqueta. Evaluar contradicciones explícitas de tracción y consultar al experto por modelo/potencia. |

### Reproducción y comprobaciones

```bash
python -m unittest discover -s tests -v
python -m solution.evaluate --phase develop
python -m solution.evaluate --phase validate
python -m solution.evaluate_decision
python score.py --predictions dev_predictions.csv --labels data/queries_labeled.csv
python submission_check.py --predictions dev_predictions.csv --queries data/queries_labeled.csv
```

También se añadieron `make evaluate`, `make evaluate-decision` y `make test`. El baseline original se
conserva intacto. Recuperación/ranking no usan APIs ni gasto de LLM.

En la etapa de ranking pasaron 56 pruebas; con decisión hay 79 pruebas y todas
pasaron. Se reprodujo la fase de validación de ranking (incluyendo carga del
catálogo, índices y evaluación de los 233 casos) en 24.73 segundos en esta máquina.
Esto es tiempo de evaluación local, no una medición del futuro proceso ciego.
Se verificó igualdad de las predicciones del baseline frente a su script original,
y cobertura, códigos válidos, tres códigos distintos y top-1 en primera posición
para las 233 predicciones. `submission_check.py` las acepta.
