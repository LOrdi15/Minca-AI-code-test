# Memoria de trabajo y temas para revisar al terminar

Este archivo conserva los temas de la conversación y los hallazgos del proyecto.
Se actualizará al cerrar cada etapa. Registrar una posible mejora no significa
implementarla: primero se prioriza la entrega funcional, medible y explicable.

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

- [ ] Diseñar y evaluar confianza y política `auto_accept` / `review` mediante
  utilidad, no solo accuracy. El score de ranking no es una probabilidad.
- [ ] Definir cómo impedir aceptación automática ante contradicciones, variantes
  ambiguas, ausencia de evidencia o alternativas casi empatadas.
- [ ] Integrar la solución en `make predict`; por ahora ese objetivo sigue usando
  el baseline. Debe generar las 155 predicciones ciegas sin pasos manuales.
- [ ] Validar el CSV final con el validador oficial y comprobaciones adicionales:
  códigos existentes, tres códigos distintos y top-1 como primer candidato.
- [ ] Completar `DECISIONS.md` (máximo dos páginas) y actualizar `EVAL.md` al estado
  final, incluyendo resultados, experimentos y diez fallos.
- [ ] Comprobar ejecución desde una copia limpia, tiempo y gasto del proceso ciego.
  La evaluación local de esta etapa tardó 24.73 segundos; eso no es todavía una
  medición de la futura ejecución ciega.
- [ ] Preparar ZIP incluyendo `.git`, siguiendo las instrucciones de devolución.

## Hallazgos y preguntas para revisar detenidamente

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
