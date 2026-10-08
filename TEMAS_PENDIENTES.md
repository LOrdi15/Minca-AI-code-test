# Memoria de trabajo y temas para revisar al terminar

Este archivo conserva los temas de la conversación y los hallazgos del proyecto.
Se actualizará al cerrar cada etapa. Registrar una posible mejora no significa
implementarla: primero se prioriza la entrega funcional, medible y explicable.

**Prioridad especial del usuario: conservar los errores con detalle para revisarlos
al terminar.** `ERRORES_PENDIENTES.md` contiene las 91 fichas de fallos top-1 de la
etapa actual: entrada original, etiqueta, top-3, etapa del fallo, variantes y años,
conflictos, contribuciones del score e investigación propuesta. De esos casos,
24 pertenecen a validación. Los hechos se separan de las hipótesis; no se corrigen
etiquetas por suposición. Actualizar el seguimiento sin borrar diagnósticos previos.

## Contexto y acuerdos

- Plazo de trabajo acordado: tres horas; el reto original permite cinco horas.
- Trabajar paso a paso y explicar cada componente con ejemplos sencillos.
- Respetar el contrato del README, el evaluador oficial y el baseline original.
- Usar Python, pandas, NumPy, scikit-learn y RapidFuzz. OpenAI queda como opción
  solo si un experimento demuestra valor; actualmente no hay llamadas a LLM.
- Conservar variantes del catálogo, datos originales e identificadores como texto.
- Registrar experimentos que empeoran los resultados y desactivar sus cambios.
- Hacer commit y push al terminar cada etapa en
  `https://github.com/LOrdi15/Minca-AI-code-test.git`, rama `main`.
- El catálogo es confidencial según el README; no incluir credenciales en Git.

## Pendientes necesarios para la entrega

- [x] Diseñar y evaluar confianza y política `auto_accept` / `review` mediante
  utilidad. Se seleccionó review general: la calibración no respalda automatizar.
- [x] Impedir aceptación automática ante contradicciones, variantes ambiguas,
  relaciones incompletas, ausencia de evidencia o alternativas casi empatadas.
- [x] Integrar la solución en `make predict`; genera las 155 predicciones ciegas
  sin pasos manuales con `python -m solution.predict`.
- [x] Validar el CSV final con el validador oficial y comprobaciones adicionales:
  códigos existentes, tres códigos distintos y top-1 como primer candidato.
- [x] Escribir `DECISIONS.md` y actualizar `EVAL.md` con confianza, decisiones,
  experimentos y limitaciones. Revisar su estado final al integrar ejecución ciega.
- [x] Comprobar código portátil desde una copia aislada, tiempo y gasto del proceso
  ciego: 20.35 segundos de proceso, 1.25 de matching, USD 0. Copia aislada idéntica
  sin `.env`, etiquetas o reportes; dependencias ya instaladas. Make no disponible
  localmente: se validó su comando de Python, no se ejecutó el binario.
- [ ] Preparar ZIP incluyendo `.git`, siguiendo las instrucciones de devolución.

## Hallazgos y preguntas para revisar detenidamente

### Confianza y decisión: hallazgo de esta etapa

Se implementó `solution/decision.py`. Usa score, margen contra el segundo y
compatibilidad, y estima confianza con aciertos por grupos de evidencia. No
convierte similitud en probabilidad. Calibración solo sobre desarrollo, con
selección por cuatro folds agrupados; el ranking permanece congelado. La antigua
validación de 59 casos ya fue inspeccionada y no se presenta como un test nuevo.

La cohorte fuerte tiene 37/43 grupos correctos, confianza suavizada 84.4% y límite
inferior Wilson 72.7%. Ningún umbral protegido 0.80/0.85/0.90/0.95 habilitó
aceptaciones. Se conserva review general. Una referencia que ignora incertidumbre
y usa confianza central >=0.80 aceptaría 44 casos, con seis errores y utilidad
+0.1914, pero no tiene respaldo suficiente en el límite inferior de precisión.
La política seleccionada obtiene +0.1109 en validación agrupada de desarrollo y
+0.1093 en la antigua validación; revisión 100%. No confundir ausencia de errores
automáticos con precisión 100%: sin aceptaciones, esa precisión no es estimable.

Pasaron las 79 pruebas. El modelo guardado reproduce las 233 confianzas y
decisiones. `DECISIONS.md` documenta el razonamiento, mejoras rechazadas, uso del
experto y trabajo futuro. Al integrar predicción, comprobar que calibrador y
ranking corresponden a la misma configuración (firma guardada en el modelo).

Prioridad para la revisión final: estudiar los seis errores automáticos **simulados**
de `evaluation/decision_diagnostic_errors.csv`. No suceden bajo la política actual.
La ejecución ciega quedó integrada y validada; la revisión final y el empaquetado
siguen pendientes.

### Integración final: estado y límites para revisar

Se creó `solution/predict.py` y el paquete `solution/__init__.py`. Catálogo e índices
se cargan una vez. Se verificó la firma de pesos del calibrador, considerando la
equivalencia JSON `0`/`0.0`. No se cambiaron algoritmos, pesos o política. Pasaron
las 89 pruebas. Ambas ejecuciones completas tuvieron cero fallbacks de filas o
calibrador. El validador oficial reportó SUBMISSION VALID para 233 y 155 filas.

Los fallos simulados por consulta producen tres códigos válidos/distintos,
confianza cero y review. Si la entrada no tiene IDs válidos/únicos o el catálogo
no permite tres códigos, se informa un error global; no se fabrican IDs ni
alternativas duplicadas. El fallback preserva formato, no garantiza calidad del
match. Las limitaciones de remolques, etiquetas, confianza y revisión 100% siguen.

Registro reproducible: `evaluation/integration_metrics.json`. No se puede puntuar
la entrega ciega sin etiquetas. Pendiente de verificación ambiental: `make setup`
en un entorno completamente nuevo y el binario GNU Make, no disponible aquí.

### 1. Códigos duplicados y coherencia del catálogo

Se conservaron las 13,298 filas agrupadas en 13,140 códigos únicos. Hay 151 códigos
repetidos y 158 filas adicionales; ninguna fila es una copia exacta de otra.
Cambian descripción (138 códigos), submodelo (8), fabricante (3), tipo (11) y
segmento (10); los grupos se superponen. Los códigos con distintos fabricantes
son `H0003E`, `T0008F` y `T000DV`.

Pregunta: ¿son alternativas legítimas, revisiones históricas o errores del origen?
No elegir una versión arbitrariamente ni combinar atributos de variantes distintas.
Las relaciones actuales encuentran correspondencia y no hay fabricantes
inconsistentes entre una fila de versión y su submodelo relacionado.

### 2. Años: disponibilidad explícita y datos faltantes

Los años se agrupan por código para evitar multiplicar filas. Todos los códigos
actuales tienen años válidos. Un año ausente dentro de una lista conocida se trata
de forma diferente a no disponer de ninguna lista. No completar huecos: `A0003D`
tiene 2017–2024 y 2026, pero no 2025. El origen no relaciona años con cada variante.

### 3. Normalización conservadora

Se uniforman mayúsculas, acentos, espacios y puntuación. Se mantienen decimales,
tracción, números de modelo, años, ceros iniciales y marcas de pies/pulgadas.
`H.P.` se compacta a `HP`; `V.W.` a `VW`. No se expanden `AUT`/`STD` ni se corrigen
marcas mediante alias manuales. Catálogo y consultas usan las mismas reglas y
conservan sus columnas originales.

Pendiente de estudiar: separadores de miles (`28000` frente a `28,000`), modelos
con guiones (`F-150` frente a `F150`) y atributos escritos con espacios (`4 X 2`).
Cada regla nueva debe demostrar que no elimina distinciones importantes.

### 4. Entradas sin información suficiente

La consulta ciega `q0103` tiene descripción `*`, que normaliza a texto vacío.
Habrá que aprovechar otros campos disponibles y contemplar abstención/revisión.
No confundir un desempate determinista con evidencia de una coincidencia.

### 5. Metadatos del corredor ruidosos

Marca y submodelo pueden contener erratas, palabras genéricas o descripciones
completas. Un valor desconocido no equivale a una contradicción. La resolución
actual usa el vocabulario del catálogo, coincidencias explícitas y fuzzy >=90 con
margen >=10. Pregunta: ¿necesitamos equivalencias de dominio verificadas por experto?

### 6. Tipos de vehículo y taxonomías distintas

Se alinean categorías claras como AUTOMOVIL/AUTO y SEMIREMOLQUE/REMOLQUE.
TOLVA, CAJA y CAMIONETA son ambiguos. Puntuar compatibilidad de tipo perjudicó
desarrollo incluso con pesos pequeños, así que ese aporte está desactivado.
Los conflictos siguen registrados para revisión. Investigar si el problema es
la taxonomía, el campo recibido o las etiquetas antes de imponer filtros.

### 7. Recuperación frente a ranking

Se recuperan 50 códigos distintos con TF-IDF de palabras (65%) y caracteres (35%),
conservando todas sus variantes. Ranking seleccionado: 90% TF-IDF, 10% RapidFuzz,
año +0.12/−0.20, fabricante +0.02/−0.10 y submodelo +0.02/−0.05.
El aumento principal provino del año. RapidFuzz al 30% y penalizaciones fuertes de
metadatos se rechazaron. No perder la separación entre recuperar el código correcto
y ordenarlo bien.

### 8. Validación y límites de la evidencia

Hay 233 etiquetas, no 223. Se usaron 174 para desarrollo y 59 para validación,
agrupando descripción normalizada + año, con semilla 42. La configuración se
congeló antes de abrir resultados de validación.

Validación: top-1 59.3%, top-3 79.7%, recall@50 89.8%, utilidad con revisión +0.1093.
Baseline: 27.1%, 42.4%, 61.0% y +0.0347, respectivamente. El @50 del baseline es
una extensión diagnóstica de su búsqueda; el original solo devuelve tres filas.
Los resultados de los 233 casos completos son descriptivos porque incluyen
desarrollo. La validación es pequeña y el conjunto ciego tiene otra distribución.
Una vez inspeccionados sus fallos, no reutilizar esta validación para ajustar y
seguir presentándola como evidencia independiente.

### 9. Remolques y etiqueta recurrente Z0000M

REMOLQUE es el segmento más débil: top-3 31.4% y recall@50 48.6% en el total
descriptivo. `Z0000M` aparece como etiqueta en 33 consultas y explica 23 de los 29
fallos de recuperación. Su descripción es CAJA CERRADA, pero también etiqueta
tolvas, plataformas y camiones.

Pregunta prioritaria al experto: ¿existe una regla de código genérico/fallback o
son etiquetas discutibles? No cambiar etiquetas ni introducir un fallback basado
solo en su frecuencia para subir el score.

### 10. Atributos que el ranking aún no interpreta

Analizar capacidad, tracción, puertas, carrocería, transmisión y motor como señales
explícitas. Ejemplos: `q0005` (28000 frente a 30000 LBS), `q0035` (sedán y puertas),
`q0132` (4X2 frente a 4X4 sin tracción en la consulta), `q0186` (modelo, potencia y
tracción cruzados). No inventar atributos ausentes ni asumir que todas las etiquetas
son incorrectas. Los diez análisis específicos están en `EVAL.md`.

### 11. Posible aporte de OpenAI

Evaluar únicamente si hay tiempo y un patrón de errores que lo justifique: ordenar
una lista corta o interpretar abreviaturas difíciles. Restringir códigos permitidos,
permitir ambigüedad y medir utilidad, tiempo y costo. Un LLM no puede justificar
información que no aparece en la entrada. La solución actual funciona localmente.

### 12. Reproducibilidad y Git

Git está inicializado en `main`, conectado a `origin`; `.env`, cachés y predicciones
generadas quedan ignorados. El kit no fija versiones exactas de dependencias.
Los comandos de evaluación se probaron mediante Python; `make` no estaba disponible
en esta máquina durante la etapa de ranking. Comprobar el contrato final en un
entorno con Make, especialmente por `python3` y las diferencias de Windows.

## Forma de revisión al cierre

Para cada tema: explicar el ejemplo, identificar evidencia, distinguir lo ya
resuelto de las hipótesis y decidir si es necesario para entregar, una pregunta
para el experto o una mejora para dos semanas adicionales. No convertir todos
los pendientes en trabajo inmediato.
