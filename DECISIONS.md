# Decisiones de implementación

Estado: pipeline integrado en `make predict`, 155 predicciones ciegas generadas
y **SUBMISSION VALID**. Se priorizó una solución local, reproducible y explicable
dentro de tres horas. La ejecución ciega tomó 20.35 segundos incluyendo arranque,
catálogo e índices, con cero fallbacks y gasto de API USD 0. Una copia aislada
reprodujo el CSV sin etiquetas, `.env` o reportes. GNU Make no está instalado aquí;
se validó el comando del target con Python, no el binario Make.

## Qué conservamos y qué rechazamos

Conservamos todas las variantes de versiones, asociadas a sus propios atributos.
Los años se agrupan por código sin completar huecos. Recuperamos 50 códigos con
TF-IDF de palabras y caracteres; ordenamos con 90% TF-IDF, 10% RapidFuzz y ajustes
de año, fabricante y submodelo. No inventamos alias ni corregimos etiquetas.

RapidFuzz al 30%, penalizaciones fuertes de marca/submodelo y puntuar el tipo
empeoraron desarrollo y se desactivaron. Los conflictos de tipo siguen visibles
para revisión. Aumentar la penalización del año no dio beneficio. Los experimentos,
incluidos los fallidos, están en `EVAL.md`.

No incorporamos un LLM: no identificamos todavía un beneficio medido que justifique
añadir costo, latencia e integración. Tampoco añadimos el código recurrente
`Z0000M` como fallback para mejorar artificialmente el score; su uso requiere
explicación de dominio.

## Cómo elegimos la aceptación automática

La utilidad esperada de aceptar es `4p−3`; revisar puede valer hasta 0.15, así que
la aceptación necesita `p>0.7875`. La similitud no es esa probabilidad.

La confianza se estima con aciertos en tres cohortes fijas de evidencia: bloqueada,
moderada y fuerte. Se utilizan score, margen frente al segundo, año y otros
atributos confirmados. Agrupamos consultas equivalentes para que las repeticiones
no inflen el soporte y suavizamos la tasa con Beta(1,1).

Comparamos umbrales 0.80, 0.85, 0.90 y 0.95 con cuatro folds agrupados de los 174
casos de desarrollo. Cada caso recibe confianza de un calibrador que no vio su
grupo. Exigimos soporte de al menos 20 grupos, límite inferior Wilson suficiente,
mejor utilidad y ningún fold perjudicado. El ranking se mantuvo congelado.

Ningún umbral pasó: seleccionamos **review general**. La cohorte fuerte tiene
37/43 grupos correctos, confianza 84.4% y límite inferior 72.7%. Ignorar el
intervalo y usar solo confianza >=0.80 daría utilidad +0.1914, pero seis errores
en 44 aceptaciones; ese resultado no respalda todavía automatización conservadora.
Review obtiene +0.1109 en desarrollo agrupado y +0.1093 en los 59 casos reservados,
frente a +0.0347 del baseline en estos últimos.

La validación anterior ya fue inspeccionada. El fuera de fold valida calibración,
no todo el proceso de selección del ranking. Las cohortes son amplias y Wilson
no protege frente a cambio de distribución o errores sistemáticos de etiquetas.
No afirmamos que la confianza sea una probabilidad individual bien calibrada.

## Entradas que no determinan una respuesta

Devolvemos tres códigos distintos y revisión. Contradicciones, catálogo ambiguo,
relaciones incompletas, año no confirmado, descripción vacía o margen pequeño
bloquean la aceptación. La falta de motor, tracción, puertas o versión requiere
pedir información; un desempate determinista no aporta certeza.

## Qué haríamos con dos semanas adicionales

Primero verificar etiquetas y la semántica de códigos genéricos comerciales.
Después extraer capacidad, tracción, motor, transmisión y carrocería, midiendo
contradicciones y pérdidas de recuperación. Ampliar el conjunto etiquetado y
reservar una evaluación nueva por grupos/origen; estudiar calibración por segmento
y curvas de utilidad/cobertura con más soporte. Evaluar un LLM solo sobre errores
concretos y compararlo contra el sistema local, incluyendo costo y tiempo.

## Cómo utilizaríamos cuatro horas de un experto

- 90 minutos: revisar el significado de `Z0000M` y casos comerciales que explica.
- 60 minutos: resolver contradicciones de los diez fallos y seis aceptaciones
  simuladas; distinguir errores de etiqueta de reglas reales de cotización.
- 60 minutos: definir qué atributos mínimos identifican una versión y cuáles
  requieren abstención; verificar ejemplos difíciles adicionales.
- 30 minutos: documentar taxonomías, abreviaturas y reglas aceptables, con ejemplos.

Ese conocimiento resuelve ambigüedades que más ingeniería no puede inferir con
seguridad y produce etiquetas útiles para medir automatización de forma honesta.
