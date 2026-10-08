# Registro detallado de errores para la revisión final

Este archivo documenta la configuración congelada de la etapa de recuperación y ranking (E8).
No constituye un cambio de etiquetas ni una lista de correcciones confirmadas.
Las métricas y los diez análisis específicos están en `EVAL.md`.

Hay **91 fallos top-1** en 233 consultas: **29** sin respuesta en los 50 candidatos,
**17** con respuesta recuperada pero fuera de los tres primeros, y
**45** con respuesta entre los tres primeros pero no en primera posición.
Primero aparecen los fallos de validación; después los de desarrollo.

Cada ficha conserva hechos observables y propone una investigación. No se afirma que
una etiqueta sea incorrecta solo porque discrepe del texto. Todas las predicciones de
esta etapa se enviaron a revisión; ninguno de estos errores se aceptó automáticamente.

La validación ya fue inspeccionada: cualquier mejora motivada por estas fichas necesita
una nueva estrategia de evaluación antes de atribuirle generalización independiente.

## Fichas de errores

### Seguimiento especial: errores de aceptación automática simulada

En la etapa de confianza se comparó, solo como diagnóstico, aceptar con estimación
central >=0.80 sin comprobar el intervalo Wilson. En validación agrupada de los
174 casos de desarrollo aceptaría 44 filas y cometería estos seis errores.
**La política seleccionada mantiene revisión: ninguno se acepta automáticamente.**
Los detalles numéricos están en `evaluation/decision_diagnostic_errors.csv` y las
fichas originales por query_id permanecen abajo, sin sobrescribirlas.

| Consulta | Esperado | Devuelto | Qué debemos investigar al cierre |
|---|---|---|---|
| q0014 | Z0000M | S0008A | PLATAFORMA de dos ejes frente a etiqueta CAJA CERRADA. Confirmar si existe una regla genérica de negocio; año y tipo compatibles no resuelven la semántica de la etiqueta. |
| q0015 | Z0000M | S0008A | Mismo patrón de plataforma/caja, con otro año. No contar el parecido de casos como prueba de que la confianza individual sea fiable. |
| q0074 | G00001 | I0007V | WRANGLER SAHARA: esperado UNLIMITED, cuatro puertas; devuelto toldo duro, dos puertas. La entrada no identifica esas diferencias con suficiente claridad. |
| q0093 | Z0000M | W000CD | VOLTEO DINA: el candidato es un camión de volteo y la etiqueta describe caja cerrada. Preguntar por reglas de catálogo genérico o discrepancias de etiquetado. |
| q0134 | N0001W | U0008Z | CASCADIA con DD13: esperado NEW CASCADIA EURO V FULLER 18VEL, devuelto CASCADIA 116. Investigar configuración y el dato CASCADIA 125 de la submarca; la coincidencia de marca no distingue la variante. |
| q0180 | G0003R | K000B7 | QX56 AWD: opciones muy similares; esperado especifica siete velocidades y ocho ocupantes. Pedir atributos de versión y verificar qué diferencia los códigos de catálogo. |

El grupo fuerte del calibrador tiene confianza suavizada 84.4%, pero límite
inferior 72.7%. Este contraste, y los seis casos anteriores, son evidencia para
conservar review mientras no haya soporte suficiente. No afirmar que review
maximiza la utilidad observada: es la opción elegida bajo los requisitos de
incertidumbre y respaldo definidos. Revisar primero estos casos en la sesión final.

### q0005 — validation — CAMION

**Consulta original:** FORD F 700 GASOLINA 28000 LBS CHASIS CABIN

- Año recibido: 2000.
- Marca recibida: vacía.
- Submarca recibida: vacía.
- Tipo recibido: CAMIONES (HASTA 7.5 TONS.).
- Top-3 devuelto, en orden: `P00000|U0003D|B00052`.
- Etapa del fallo: Ranking: el esperado sí está en el top-3, pero otra alternativa quedó primera.
- Posición de recuperación del esperado: 2.0.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 7667.

**Respuesta esperada según la etiqueta: `U0003D`**

- Variante 1: EQ FORD F-700 GASOLINA 28,000 LBS CHASIS CABINA
  Fabricante: FORD; submodelo: F-700; tipo: CAMION; segmento: CAMION HASTA 14 TONELADAS.

Años registrados por código: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000.

**Primera respuesta devuelta: `P00000`**

- Variante 1: EQ FORD F-700 GASOLINA 30,000 LBS CHASIS CABINA
  Fabricante: FORD; submodelo: F-700; tipo: CAMION; segmento: CAMION HASTA 14 TONELADAS.

Años registrados por código: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.08539325842696631, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.7094414949417115, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Comparar atributos que distinguen las opciones y comprobar si aparecen en la entrada. Si faltan motor, versión, capacidad o tracción, pedir esa información y mantener revisión.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0016 — validation — REMOLQUE

**Consulta original:** PLATAFORMA 2 EJES REVUELTA

- Año recibido: 2006.
- Marca recibida: vacía.
- Submarca recibida: vacía.
- Tipo recibido: vacío.
- Top-3 devuelto, en orden: `S0008A|U0007I|D0006V`.
- Etapa del fallo: Ranking: el esperado fue recuperado, pero quedó fuera de los tres primeros.
- Posición de recuperación del esperado: 43.0.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 9501.

**Respuesta esperada según la etiqueta: `Z0000M`**

- Variante 1: RM CAJA CERRADA 2 EJES 40
  Fabricante: SEMIRREMOLQUES; submodelo: CAJA SECA; tipo: SEMIREMOLQUE; segmento: SEMIREMOLQUE.

Años registrados por código: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.

**Primera respuesta devuelta: `S0008A`**

- Variante 1: RM PLATAFORMA 2 EJES 40
  Fabricante: SEMIRREMOLQUES; submodelo: PLATAFORMA ALTA; tipo: SEMIREMOLQUE; segmento: SEMIREMOLQUE.

Años registrados por código: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.5317389249801636, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Inspeccionar las señales del esperado frente a las alternativas superiores; comprobar si similitud, año o metadatos favorecieron una opción incompatible. No asumir que aumentar el número de candidatos corrige este ordenamiento.

**Pregunta adicional al experto:** este código se repite en 33 etiquetas y describe
una caja cerrada. Confirmar si existe una regla genérica de negocio que explique su
uso en consultas diferentes. No añadirlo como fallback ni corregir la etiqueta por suposición.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0024 — validation — REMOLQUE

**Consulta original:** TANQUE A.INOX ANILLADO 2 EJES 31,000 LTS MEDIA. AUT.

- Año recibido: 2023.
- Marca recibida: -.
- Submarca recibida: vacía.
- Tipo recibido: REMOLQUE.
- Top-3 devuelto, en orden: `U0003Y|W0008B|Z0005M`.
- Etapa del fallo: Recuperación: el código esperado no entró en los 50 candidatos.
- Posición de recuperación del esperado: fuera de los 50.
- Conflictos detectados en top-1: year.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 10367.

**Respuesta esperada según la etiqueta: `Q00046`**

- Variante 1: SEMIREMOLQUE TANQUE ELIPTICO
  Fabricante: SEMIRREMOLQUES; submodelo: TANQUE; tipo: SEMIREMOLQUE; segmento: SEMIREMOLQUE.

Años registrados por código: 2014, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024.

**Primera respuesta devuelta: `U0003Y`**

- Variante 1: RM TANQUE A.INOX ANILLADO 2 EJES 31,000 LTS
  Fabricante: SEMIRREMOLQUES; submodelo: TANQUE; tipo: SEMIREMOLQUE; segmento: SEMIREMOLQUE.

Años registrados por código: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.08444444444444445, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.76396404504776, "vehicle_type": 0, "year": -0.2}`

**Investigación propuesta:** Comparar la representación textual del esperado con la consulta; comprobar campos faltantes, vocabulario y posibles reglas de dominio. Modificar solo el ranking no puede rescatar un candidato que no se recuperó.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0035 — validation — AUTO

**Consulta original:** AUDI S3 SEDAN

- Año recibido: 2016.
- Marca recibida: AUDI.
- Submarca recibida: vacía.
- Tipo recibido: AUTOS.
- Top-3 devuelto, en orden: `R00034|Q0004P|J000B5`.
- Etapa del fallo: Ranking: el esperado sí está en el top-3, pero otra alternativa quedó primera.
- Posición de recuperación del esperado: 4.0.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 8802.

**Respuesta esperada según la etiqueta: `Q0004P`**

- Variante 1: AUDI A3 S3, 2.0T, 4 PUERTAS, S TRONIC
  Fabricante: AUDI; submodelo: A3; tipo: AUTO; segmento: LUJO.

Años registrados por código: 2016, 2017, 2018, 2019.

**Primera respuesta devuelta: `R00034`**

- Variante 1: S3 2.0L STRONIC QUATTRO L4 FSI AUT 3P CA CE PIEL CQ CB
  Fabricante: AUDI; submodelo: S3; tipo: AUTO; segmento: DEPORTIVO.

Años registrados por código: 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2018.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.0855, "manufacturer": 0.02, "submodel": 0.0, "tfidf": 0.3962739586830139, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Comparar atributos que distinguen las opciones y comprobar si aparecen en la entrada. Si faltan motor, versión, capacidad o tracción, pedir esa información y mantener revisión.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0050 — validation — REMOLQUE

**Consulta original:** CAJA REFRIGERADA

- Año recibido: 2015.
- Marca recibida: CAJA.
- Submarca recibida: vacía.
- Tipo recibido: REMOLQUES.
- Top-3 devuelto, en orden: `W0008G|I00083|M0009R`.
- Etapa del fallo: Ranking: el esperado fue recuperado, pero quedó fuera de los tres primeros.
- Posición de recuperación del esperado: 34.0.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 11556.

**Respuesta esperada según la etiqueta: `Z0000M`**

- Variante 1: RM CAJA CERRADA 2 EJES 40
  Fabricante: SEMIRREMOLQUES; submodelo: CAJA SECA; tipo: SEMIREMOLQUE; segmento: SEMIREMOLQUE.

Años registrados por código: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.

**Primera respuesta devuelta: `W0008G`**

- Variante 1: CAJA REFRIGERADORA CON EQUIPO
  Fabricante: SEMIRREMOLQUES; submodelo: CAJA REFRIGERADA; tipo: SEMIREMOLQUE; segmento: SEMIREMOLQUE.

Años registrados por código: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.09000000000000001, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.5754315733909607, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Inspeccionar las señales del esperado frente a las alternativas superiores; comprobar si similitud, año o metadatos favorecieron una opción incompatible. No asumir que aumentar el número de candidatos corrige este ordenamiento.

**Pregunta adicional al experto:** este código se repite en 33 etiquetas y describe
una caja cerrada. Confirmar si existe una regla genérica de negocio que explique su
uso en consultas diferentes. No añadirlo como fallback ni corregir la etiqueta por suposición.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0085 — validation — REMOLQUE

**Consulta original:** TOLVA

- Año recibido: 2022.
- Marca recibida: DALTO.
- Submarca recibida: vacía.
- Tipo recibido: TOLVA.
- Top-3 devuelto, en orden: `J0007M|Q0001C|Z0005P`.
- Etapa del fallo: Recuperación: el código esperado no entró en los 50 candidatos.
- Posición de recuperación del esperado: fuera de los 50.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 4883.

**Respuesta esperada según la etiqueta: `Z0000M`**

- Variante 1: RM CAJA CERRADA 2 EJES 40
  Fabricante: SEMIRREMOLQUES; submodelo: CAJA SECA; tipo: SEMIREMOLQUE; segmento: SEMIREMOLQUE.

Años registrados por código: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.

**Primera respuesta devuelta: `J0007M`**

- Variante 1: RM TOLVA GRANELERA 2 EJES NAC
  Fabricante: SEMIRREMOLQUES; submodelo: TOLVA GRANELERA; tipo: SEMIREMOLQUE; segmento: SEMIREMOLQUE.

Años registrados por código: 2020, 2021, 2022, 2023.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.3192595839500427, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Comparar la representación textual del esperado con la consulta; comprobar campos faltantes, vocabulario y posibles reglas de dominio. Modificar solo el ranking no puede rescatar un candidato que no se recuperó.

**Pregunta adicional al experto:** este código se repite en 33 etiquetas y describe
una caja cerrada. Confirmar si existe una regla genérica de negocio que explique su
uso en consultas diferentes. No añadirlo como fallback ni corregir la etiqueta por suposición.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0086 — validation — REMOLQUE

**Consulta original:** TOLVA

- Año recibido: 2024.
- Marca recibida: DALTO.
- Submarca recibida: vacía.
- Tipo recibido: TOLVA.
- Top-3 devuelto, en orden: `K000DZ|Z0005P|L0008A`.
- Etapa del fallo: Recuperación: el código esperado no entró en los 50 candidatos.
- Posición de recuperación del esperado: fuera de los 50.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 5626.

**Respuesta esperada según la etiqueta: `Z0000M`**

- Variante 1: RM CAJA CERRADA 2 EJES 40
  Fabricante: SEMIRREMOLQUES; submodelo: CAJA SECA; tipo: SEMIREMOLQUE; segmento: SEMIREMOLQUE.

Años registrados por código: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.

**Primera respuesta devuelta: `K000DZ`**

- Variante 1: RM TOLVA PRESURIZADA 28MTS^3 2EJES
  Fabricante: SEMIRREMOLQUES; submodelo: TOLVA (ALIMENTOS, QUIMICOS); tipo: SEMIREMOLQUE; segmento: SEMIREMOLQUE.

Años registrados por código: 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2024.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.2844096958637238, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Comparar la representación textual del esperado con la consulta; comprobar campos faltantes, vocabulario y posibles reglas de dominio. Modificar solo el ranking no puede rescatar un candidato que no se recuperó.

**Pregunta adicional al experto:** este código se repite en 33 etiquetas y describe
una caja cerrada. Confirmar si existe una regla genérica de negocio que explique su
uso en consultas diferentes. No añadirlo como fallback ni corregir la etiqueta por suposición.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0094 — validation — PICKUP

**Consulta original:** DODEGE RAM 400

- Año recibido: 2019.
- Marca recibida: DODEGE.
- Submarca recibida: vacía.
- Tipo recibido: PICKUP´S.
- Top-3 devuelto, en orden: `R0002P|S0008D|U0004P`.
- Etapa del fallo: Ranking: el esperado fue recuperado, pero quedó fuera de los tres primeros.
- Posición de recuperación del esperado: 10.0.
- Conflictos detectados en top-1: vehicle_type.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 8787.

**Respuesta esperada según la etiqueta: `O0005H`**

- Variante 1: DODGE RAM 2500 R/T 5.7L 4X4 AUT CA
  Fabricante: CHRYSLER; submodelo: RAM 2500; tipo: PICK UP; segmento: PICK UP.

Años registrados por código: 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020.

**Primera respuesta devuelta: `R0002P`**

- Variante 1: EQ ISUZU ELF 400 CHASIS CABINA "F"
  Fabricante: ISUZU; submodelo: ELF 400; tipo: CAMION; segmento: CAMION DE 2.2 HASTA 4.5 TONELADAS.

Años registrados por código: 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2022, 2025, 2026.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.19616316854953766, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Inspeccionar las señales del esperado frente a las alternativas superiores; comprobar si similitud, año o metadatos favorecieron una opción incompatible. No asumir que aumentar el número de candidatos corrige este ordenamiento.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0095 — validation — OTHER

**Consulta original:** 35451

- Año recibido: 2024.
- Marca recibida: DODGE.
- Submarca recibida: DURANGO.
- Tipo recibido: vacío.
- Top-3 devuelto, en orden: `T000CA|C0006Z|M0005H`.
- Etapa del fallo: Ranking: el esperado sí está en el top-3, pero otra alternativa quedó primera.
- Posición de recuperación del esperado: 7.0.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 10157.

**Respuesta esperada según la etiqueta: `C0006Z`**

- Variante 1: DURANGO RT 5.7L V8 AUT 5P ABS CA CE PIEL CD CQ CB
  Fabricante: CHRYSLER; submodelo: DURANGO; tipo: AUTO; segmento: SUV.

Años registrados por código: 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024.

**Primera respuesta devuelta: `T000CA`**

- Variante 1: DURANGO GT PLUS V6 3.6L 5 PTS AUT
  Fabricante: CHRYSLER; submodelo: DURANGO; tipo: AUTO; segmento: SUV.

Años registrados por código: 2022, 2023, 2024, 2025.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.02, "tfidf": 0.38974422812461856, "vehicle_type": 0.0, "year": 0.12}`

**Investigación propuesta:** Comparar atributos que distinguen las opciones y comprobar si aparecen en la entrada. Si faltan motor, versión, capacidad o tracción, pedir esa información y mantener revisión.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0115 — validation — REMOLQUE

**Consulta original:** FERBEL

- Año recibido: 2019.
- Marca recibida: FERBEL.
- Submarca recibida: vacía.
- Tipo recibido: REMOLQUE.
- Top-3 devuelto, en orden: `T0002L|J0008Z|G000AP`.
- Etapa del fallo: Recuperación: el código esperado no entró en los 50 candidatos.
- Posición de recuperación del esperado: fuera de los 50.
- Conflictos detectados en top-1: vehicle_type.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 9805.

**Respuesta esperada según la etiqueta: `Z0000M`**

- Variante 1: RM CAJA CERRADA 2 EJES 40
  Fabricante: SEMIRREMOLQUES; submodelo: CAJA SECA; tipo: SEMIREMOLQUE; segmento: SEMIREMOLQUE.

Años registrados por código: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.

**Primera respuesta devuelta: `T0002L`**

- Variante 1: SANTA FE GLS 2.0T 5 PUERTAS AUTOMATICA
  Fabricante: HYUNDAI; submodelo: SANTA FE; tipo: AUTO; segmento: SUV.

Años registrados por código: 2019.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.04275, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.01953243277966976, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Comparar la representación textual del esperado con la consulta; comprobar campos faltantes, vocabulario y posibles reglas de dominio. Modificar solo el ranking no puede rescatar un candidato que no se recuperó.

**Pregunta adicional al experto:** este código se repite en 33 etiquetas y describe
una caja cerrada. Confirmar si existe una regla genérica de negocio que explique su
uso en consultas diferentes. No añadirlo como fallback ni corregir la etiqueta por suposición.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0130 — validation — CAMION

**Consulta original:** VOLTEO

- Año recibido: 1992.
- Marca recibida: FORD.
- Submarca recibida: VOLTEO.
- Tipo recibido: VOLTEO.
- Top-3 devuelto, en orden: `R0002M|U0001V|Y0004T`.
- Etapa del fallo: Recuperación: el código esperado no entró en los 50 candidatos.
- Posición de recuperación del esperado: fuera de los 50.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 8784.

**Respuesta esperada según la etiqueta: `Z0000M`**

- Variante 1: RM CAJA CERRADA 2 EJES 40
  Fabricante: SEMIRREMOLQUES; submodelo: CAJA SECA; tipo: SEMIREMOLQUE; segmento: SEMIREMOLQUE.

Años registrados por código: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.

**Primera respuesta devuelta: `R0002M`**

- Variante 1: FORD F-600 VOLTEO HASTA 12 TON.
  Fabricante: FORD; submodelo: F-600 VOLTEO; tipo: CAMION; segmento: CAMION DE 9.5 HASTA 12.5 TONELADAS.

Años registrados por código: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.0855, "manufacturer": 0.02, "submodel": 0.0, "tfidf": 0.4996009111404419, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Comparar la representación textual del esperado con la consulta; comprobar campos faltantes, vocabulario y posibles reglas de dominio. Modificar solo el ranking no puede rescatar un candidato que no se recuperó.

**Pregunta adicional al experto:** este código se repite en 33 etiquetas y describe
una caja cerrada. Confirmar si existe una regla genérica de negocio que explique su
uso en consultas diferentes. No añadirlo como fallback ni corregir la etiqueta por suposición.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0131 — validation — CAMION

**Consulta original:** VOLTEO

- Año recibido: 1992.
- Marca recibida: FORD.
- Submarca recibida: VOLTEO.
- Tipo recibido: vacío.
- Top-3 devuelto, en orden: `R0002M|U0001V|Y0004T`.
- Etapa del fallo: Recuperación: el código esperado no entró en los 50 candidatos.
- Posición de recuperación del esperado: fuera de los 50.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 8784.

**Respuesta esperada según la etiqueta: `Z0000M`**

- Variante 1: RM CAJA CERRADA 2 EJES 40
  Fabricante: SEMIRREMOLQUES; submodelo: CAJA SECA; tipo: SEMIREMOLQUE; segmento: SEMIREMOLQUE.

Años registrados por código: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.

**Primera respuesta devuelta: `R0002M`**

- Variante 1: FORD F-600 VOLTEO HASTA 12 TON.
  Fabricante: FORD; submodelo: F-600 VOLTEO; tipo: CAMION; segmento: CAMION DE 9.5 HASTA 12.5 TONELADAS.

Años registrados por código: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.0855, "manufacturer": 0.02, "submodel": 0.0, "tfidf": 0.4996009111404419, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Comparar la representación textual del esperado con la consulta; comprobar campos faltantes, vocabulario y posibles reglas de dominio. Modificar solo el ranking no puede rescatar un candidato que no se recuperó.

**Pregunta adicional al experto:** este código se repite en 33 etiquetas y describe
una caja cerrada. Confirmar si existe una regla genérica de negocio que explique su
uso en consultas diferentes. No añadirlo como fallback ni corregir la etiqueta por suposición.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0132 — validation — OTHER

**Consulta original:** F150

- Año recibido: 2013.
- Marca recibida: FORD  (ROJA).
- Submarca recibida: F150.
- Tipo recibido: REGULAR CA XL.
- Top-3 devuelto, en orden: `Q0008J|T0001Y|E00096`.
- Etapa del fallo: Ranking: el esperado sí está en el top-3, pero otra alternativa quedó primera.
- Posición de recuperación del esperado: 9.0.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 8490.

**Respuesta esperada según la etiqueta: `T0001Y`**

- Variante 1: FORD F-150 XL CABINA REGULAR 4X2 V8 5.0L AUT
  Fabricante: FORD; submodelo: F-150 PICK UP; tipo: PICK UP; segmento: PICK UP.

Años registrados por código: 2013, 2014, 2016, 2017.

**Primera respuesta devuelta: `Q0008J`**

- Variante 1: FORD F-150 XL CABINA REGULAR 4X4 V8 5.0L AUT
  Fabricante: FORD; submodelo: F-150 PICK UP; tipo: PICK UP; segmento: PICK UP.

Años registrados por código: 2013, 2014, 2015, 2016, 2017.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.0855, "manufacturer": 0.02, "submodel": 0.0, "tfidf": 0.08016005605459213, "vehicle_type": 0.0, "year": 0.12}`

**Investigación propuesta:** Comparar atributos que distinguen las opciones y comprobar si aparecen en la entrada. Si faltan motor, versión, capacidad o tracción, pedir esa información y mantener revisión.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0162 — validation — CAMION

**Consulta original:** CHASIS CABINA

- Año recibido: 2024.
- Marca recibida: HINO.
- Submarca recibida: vacía.
- Tipo recibido: vacío.
- Top-3 devuelto, en orden: `D0006W|B000D5|N0004N`.
- Etapa del fallo: Ranking: el esperado fue recuperado, pero quedó fuera de los tres primeros.
- Posición de recuperación del esperado: 21.0.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 1781.

**Respuesta esperada según la etiqueta: `M0001V`**

- Variante 1: HINO 300 514 CHASIS CABINA 4.0L 3.48M L4 136HP DIS STD D/T
  Fabricante: HINO; submodelo: 300 CHASIS; tipo: CAMION; segmento: CAMION DE 4.5 HASTA 6.5 TONELADAS.
- Variante 2: HINO 300 514 CHASIS CABINA 4.0L 3.48M L4 136HP DIS STD D/T
  Fabricante: HINO; submodelo: 300 CHASIS; tipo: PICK UP; segmento: PICK UP 3.5TOM.

Años registrados por código: 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024.

**Primera respuesta devuelta: `D0006W`**

- Variante 1: HINO SERIE 500 2628 6X2 CHASIS CABINA
  Fabricante: HINO; submodelo: 500; tipo: CAMION; segmento: CAMION DE 9.5 HASTA 12.5 TONELADAS.

Años registrados por código: 2022, 2023, 2024.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.0855, "manufacturer": 0.02, "submodel": 0.0, "tfidf": 0.45343301296234134, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Inspeccionar las señales del esperado frente a las alternativas superiores; comprobar si similitud, año o metadatos favorecieron una opción incompatible. No asumir que aumentar el número de candidatos corrige este ordenamiento.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0186 — validation — OTHER

**Consulta original:** CISTERNA CHASSIS CABINA  MOD 4400 250 4X2

- Año recibido: 2003.
- Marca recibida: INTERNACIONAL.
- Submarca recibida: vacía.
- Tipo recibido: vacío.
- Top-3 devuelto, en orden: `B0003G|H00002|U000DT`.
- Etapa del fallo: Ranking: el esperado fue recuperado, pero quedó fuera de los tres primeros.
- Posición de recuperación del esperado: 28.0.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 636.

**Respuesta esperada según la etiqueta: `X0001T`**

- Variante 1: INTERNACIONAL 4300 CHASIS CABINA MODULAR N G 4 X 2 210HP 15.8 TON
  Fabricante: INTERNATIONAL; submodelo: 4300 MAS DE 14 TON; tipo: CAMION; segmento: CAMION HASTA 14 TONELADAS.

Años registrados por código: 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016.

**Primera respuesta devuelta: `B0003G`**

- Variante 1: INTERNACIONAL 4400 CHASIS CABINA 6 X 2 250HP 23.5 TON
  Fabricante: INTERNATIONAL; submodelo: 4400; tipo: CAMION; segmento: CAMION HASTA 14 TONELADAS.

Años registrados por código: 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.07223140495867768, "manufacturer": 0.02, "submodel": 0.0, "tfidf": 0.329634690284729, "vehicle_type": 0.0, "year": 0.12}`

**Investigación propuesta:** Inspeccionar las señales del esperado frente a las alternativas superiores; comprobar si similitud, año o metadatos favorecieron una opción incompatible. No asumir que aumentar el número de candidatos corrige este ordenamiento.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0204 — validation — CAMION

**Consulta original:** JAC FRISON T8 L4 STD

- Año recibido: 2024.
- Marca recibida: JAC.
- Submarca recibida: vacía.
- Tipo recibido: CAMIONES (HASTA 1.5 TONS.).
- Top-3 devuelto, en orden: `B000CS|J0005B|N000CN`.
- Etapa del fallo: Ranking: el esperado sí está en el top-3, pero otra alternativa quedó primera.
- Posición de recuperación del esperado: 4.0.
- Conflictos detectados en top-1: vehicle_type.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 974.

**Respuesta esperada según la etiqueta: `J0005B`**

- Variante 1: T8 FRISON L4 2.0L 139 CP 4 PUERTAS STD BA AA 4X4
  Fabricante: JAC; submodelo: T8; tipo: PICK UP; segmento: PICK UP.

Años registrados por código: 2022, 2023, 2024, 2025, 2026.

**Primera respuesta devuelta: `B000CS`**

- Variante 1: T8 FRISON L4 2.0T 190 CP 4 PUERTAS STD  BA AA
  Fabricante: JAC; submodelo: T8; tipo: PICK UP; segmento: PICK UP.

Años registrados por código: 2024, 2025.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.0855, "manufacturer": 0.02, "submodel": 0.0, "tfidf": 0.5242019712924958, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Comparar atributos que distinguen las opciones y comprobar si aparecen en la entrada. Si faltan motor, versión, capacidad o tracción, pedir esa información y mantener revisión.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0206 — validation — PICKUP

**Consulta original:** PICK UP JACK FRISON T6

- Año recibido: 2024.
- Marca recibida: JACK.
- Submarca recibida: vacía.
- Tipo recibido: vacío.
- Top-3 devuelto, en orden: `N000CN|Z0008D|G000CP`.
- Etapa del fallo: Ranking: el esperado sí está en el top-3, pero otra alternativa quedó primera.
- Posición de recuperación del esperado: 3.0.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 7106.

**Respuesta esperada según la etiqueta: `Z0008D`**

- Variante 1: T6 FLEX FRISON L4 2.0T 190 CP 4 PUERTAS STD  BA AA
  Fabricante: JAC; submodelo: T6; tipo: PICK UP; segmento: PICK UP.

Años registrados por código: 2024, 2025.

**Primera respuesta devuelta: `N000CN`**

- Variante 1: T6 FRISON L4 2.0T 190 CP 4 PUERTAS STD  BA AA
  Fabricante: JAC; submodelo: T6; tipo: PICK UP; segmento: PICK UP.

Años registrados por código: 2020, 2021, 2022, 2023, 2024.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.38269154727458954, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Comparar atributos que distinguen las opciones y comprobar si aparecen en la entrada. Si faltan motor, versión, capacidad o tracción, pedir esa información y mantener revisión.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0221 — validation — TRACTO

**Consulta original:** T800

- Año recibido: 2017.
- Marca recibida: KENWORTH.
- Submarca recibida: vacía.
- Tipo recibido: TRACTO.
- Top-3 devuelto, en orden: `X0003K|F0000H|Z0003D`.
- Etapa del fallo: Ranking: el esperado sí está en el top-3, pero otra alternativa quedó primera.
- Posición de recuperación del esperado: 2.0.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 11891.

**Respuesta esperada según la etiqueta: `F0000H`**

- Variante 1: TR KENWORTH T 800 B 42"
  Fabricante: KENWORTH; submodelo: T800; tipo: TRACTO CAMION; segmento: TRACTOCAMION.

Años registrados por código: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023.

**Primera respuesta devuelta: `X0003K`**

- Variante 1: TR KENWORTH T-800 B 42
  Fabricante: KENWORTH; submodelo: T800; tipo: TRACTO CAMION; segmento: TRACTOCAMION.

Años registrados por código: 2017.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.0855, "manufacturer": 0.02, "submodel": 0.0, "tfidf": 0.4618758022785187, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Comparar atributos que distinguen las opciones y comprobar si aparecen en la entrada. Si faltan motor, versión, capacidad o tracción, pedir esa información y mantener revisión.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0315 — validation — REMOLQUE

**Consulta original:** REMOLQUE

- Año recibido: 2021.
- Marca recibida: REMOLQUES.
- Submarca recibida: REMOLQUE.
- Tipo recibido: vacío.
- Top-3 devuelto, en orden: `Q00046|O0008Q|P0008I`.
- Etapa del fallo: Ranking: el esperado fue recuperado, pero quedó fuera de los tres primeros.
- Posición de recuperación del esperado: 43.0.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 8332.

**Respuesta esperada según la etiqueta: `Z0000M`**

- Variante 1: RM CAJA CERRADA 2 EJES 40
  Fabricante: SEMIRREMOLQUES; submodelo: CAJA SECA; tipo: SEMIREMOLQUE; segmento: SEMIREMOLQUE.

Años registrados por código: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.

**Primera respuesta devuelta: `Q00046`**

- Variante 1: SEMIREMOLQUE TANQUE ELIPTICO
  Fabricante: SEMIRREMOLQUES; submodelo: TANQUE; tipo: SEMIREMOLQUE; segmento: SEMIREMOLQUE.

Años registrados por código: 2014, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.06333333333333334, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.14798598736524582, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Inspeccionar las señales del esperado frente a las alternativas superiores; comprobar si similitud, año o metadatos favorecieron una opción incompatible. No asumir que aumentar el número de candidatos corrige este ordenamiento.

**Pregunta adicional al experto:** este código se repite en 33 etiquetas y describe
una caja cerrada. Confirmar si existe una regla genérica de negocio que explique su
uso en consultas diferentes. No añadirlo como fallback ni corregir la etiqueta por suposición.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0323 — validation — REMOLQUE

**Consulta original:** PLATAFORMA TANDEM 2 EJES

- Año recibido: 2016.
- Marca recibida: RM SEMIREMOLQUE.
- Submarca recibida: vacía.
- Tipo recibido: CHASIS.
- Top-3 devuelto, en orden: `S0008A|U0002I|T00076`.
- Etapa del fallo: Ranking: el esperado sí está en el top-3, pero otra alternativa quedó primera.
- Posición de recuperación del esperado: 5.0.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 9501.

**Respuesta esperada según la etiqueta: `T00076`**

- Variante 1: RM PLATAFORMA PLANA 2 EJES 48
  Fabricante: SEMIRREMOLQUES; submodelo: PLATAFORMA ALTA; tipo: SEMIREMOLQUE; segmento: SEMIREMOLQUE.

Años registrados por código: 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016.

**Primera respuesta devuelta: `S0008A`**

- Variante 1: RM PLATAFORMA 2 EJES 40
  Fabricante: SEMIRREMOLQUES; submodelo: PLATAFORMA ALTA; tipo: SEMIREMOLQUE; segmento: SEMIREMOLQUE.

Años registrados por código: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.0755421686746988, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.3930980354547501, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Comparar atributos que distinguen las opciones y comprobar si aparecen en la entrada. Si faltan motor, versión, capacidad o tracción, pedir esa información y mantener revisión.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0349 — validation — AUTO

**Consulta original:** AUTOMOVIL YARIS CORE H/B MT AC

- Año recibido: 2014.
- Marca recibida: TOYOTA YARIS.
- Submarca recibida: vacía.
- Tipo recibido: vacío.
- Top-3 devuelto, en orden: `D0009T|L0004M|Y0004U`.
- Etapa del fallo: Ranking: el esperado sí está en el top-3, pero otra alternativa quedó primera.
- Posición de recuperación del esperado: 3.0.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 1886.

**Respuesta esperada según la etiqueta: `Y0004U`**

- Variante 1: YARIS CORE HB 1.5L 106HP L4 STD 5P CA SE CD CB
  Fabricante: TOYOTA; submodelo: YARIS; tipo: AUTO; segmento: SUBCOMPACTO.

Años registrados por código: 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2022.

**Primera respuesta devuelta: `D0009T`**

- Variante 1: YARIS CORE 1.5L L4 AUT 4P D/T CA CE TELA CD SQ CB
  Fabricante: TOYOTA; submodelo: YARIS; tipo: AUTO; segmento: SUBCOMPACTO.

Años registrados por código: 2014.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.059814814814814814, "manufacturer": 0.02, "submodel": 0.0, "tfidf": 0.5168550252914429, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Comparar atributos que distinguen las opciones y comprobar si aparecen en la entrada. Si faltan motor, versión, capacidad o tracción, pedir esa información y mantener revisión.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0351 — validation — AUTO

**Consulta original:** AUTOMOVIL YARIS CORE H/B MT A/A

- Año recibido: 2014.
- Marca recibida: TOYOYA YARIS.
- Submarca recibida: vacía.
- Tipo recibido: vacío.
- Top-3 devuelto, en orden: `D0009T|L0004M|Y0004U`.
- Etapa del fallo: Ranking: el esperado sí está en el top-3, pero otra alternativa quedó primera.
- Posición de recuperación del esperado: 3.0.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 1886.

**Respuesta esperada según la etiqueta: `Y0004U`**

- Variante 1: YARIS CORE HB 1.5L 106HP L4 STD 5P CA SE CD CB
  Fabricante: TOYOTA; submodelo: YARIS; tipo: AUTO; segmento: SUBCOMPACTO.

Años registrados por código: 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2022.

**Primera respuesta devuelta: `D0009T`**

- Variante 1: YARIS CORE 1.5L L4 AUT 4P D/T CA CE TELA CD SQ CB
  Fabricante: TOYOTA; submodelo: YARIS; tipo: AUTO; segmento: SUBCOMPACTO.

Años registrados por código: 2014.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.05915094339622641, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.4379332780838013, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Comparar atributos que distinguen las opciones y comprobar si aparecen en la entrada. Si faltan motor, versión, capacidad o tracción, pedir esa información y mantener revisión.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0360 — validation — PICKUP

**Consulta original:** V.W. SAVEIRO  ROJO

- Año recibido: 2012.
- Marca recibida: V.
- Submarca recibida: vacía.
- Tipo recibido: PICKUP´S.
- Top-3 devuelto, en orden: `M000DT|R0004R|B000B1`.
- Etapa del fallo: Ranking: el esperado sí está en el top-3, pero otra alternativa quedó primera.
- Posición de recuperación del esperado: 8.0.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 6640.

**Respuesta esperada según la etiqueta: `B000B1`**

- Variante 1: VOLKSWAGEN SAVEIRO STARTLINE 1.6L STD CA DH
  Fabricante: VOLKSWAGEN; submodelo: SAVEIRO; tipo: PICK UP; segmento: PICK UP.

Años registrados por código: 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018.

**Primera respuesta devuelta: `M000DT`**

- Variante 1: VOLKSWAGEN SAVEIRO STARTLINE 1.6L STD
  Fabricante: VOLKSWAGEN; submodelo: SAVEIRO; tipo: PICK UP; segmento: PICK UP.

Años registrados por código: 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.41259557604789737, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Comparar atributos que distinguen las opciones y comprobar si aparecen en la entrada. Si faltan motor, versión, capacidad o tracción, pedir esa información y mantener revisión.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0383 — validation — OTHER

**Consulta original:** CARRO UTILITARIO

- Año recibido: 2023.
- Marca recibida: VW VIRTUS COMFORTLINE.
- Submarca recibida: vacía.
- Tipo recibido: vacío.
- Top-3 devuelto, en orden: `R000CA|Q000C7|U0006C`.
- Etapa del fallo: Ranking: el esperado sí está en el top-3, pero otra alternativa quedó primera.
- Posición de recuperación del esperado: 2.0.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 9137.

**Respuesta esperada según la etiqueta: `Q000C7`**

- Variante 1: VIRTUS COMFORTLINE, L4, 1.6L, 110 CP, 4 PUERTAS, STD
  Fabricante: VOLKSWAGEN; submodelo: VIRTUS; tipo: AUTO; segmento: COMPACTO.

Años registrados por código: 2020, 2021, 2022, 2023, 2024, 2025.

**Primera respuesta devuelta: `R000CA`**

- Variante 1: VIRTUS COMFORTLINE, L4, 1.6L, 110 CP, 4 PUERTAS, AUT
  Fabricante: VOLKSWAGEN; submodelo: VIRTUS; tipo: AUTO; segmento: COMPACTO.

Años registrados por código: 2020, 2021, 2022, 2023, 2024, 2025.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.4543520987033844, "vehicle_type": 0.0, "year": 0.12}`

**Investigación propuesta:** Comparar atributos que distinguen las opciones y comprobar si aparecen en la entrada. Si faltan motor, versión, capacidad o tracción, pedir esa información y mantener revisión.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0008 — development — OTHER

**Consulta original:** HINO 816 LONG SERIE 300

- Año recibido: 2019.
- Marca recibida: vacía.
- Submarca recibida: vacía.
- Tipo recibido: vacío.
- Top-3 devuelto, en orden: `N00083|W0008K|I000AJ`.
- Etapa del fallo: Ranking: el esperado sí está en el top-3, pero otra alternativa quedó primera.
- Posición de recuperación del esperado: 9.0.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 6942.

**Respuesta esperada según la etiqueta: `I000AJ`**

- Variante 1: 300 816 LARGO, 4.0T, 2 PUERTAS, MANUAL, HIBRIDO
  Fabricante: HINO; submodelo: 300 CHASIS; tipo: CAMION; segmento: CAMION DE 4.5 HASTA 6.5 TONELADAS.

Años registrados por código: 2019.

**Primera respuesta devuelta: `N00083`**

- Variante 1: HINO 300 816 SUPER LARGO 4.0T 2P STD
  Fabricante: HINO; submodelo: 300 CHASIS; tipo: CAMION; segmento: CAMION DE 4.5 HASTA 6.5 TONELADAS.

Años registrados por código: 2018, 2019, 2022, 2023, 2024, 2025.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.35409375429153445, "vehicle_type": 0.0, "year": 0.12}`

**Investigación propuesta:** Comparar atributos que distinguen las opciones y comprobar si aparecen en la entrada. Si faltan motor, versión, capacidad o tracción, pedir esa información y mantener revisión.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0012 — development — OTHER

**Consulta original:** NISSAN NP300 ESTACAS PAQ SEG DH AC STD

- Año recibido: 2018.
- Marca recibida: vacía.
- Submarca recibida: vacía.
- Tipo recibido: vacío.
- Top-3 devuelto, en orden: `P000AO|V00023|P000AN`.
- Etapa del fallo: Ranking: el esperado sí está en el top-3, pero otra alternativa quedó primera.
- Posición de recuperación del esperado: 4.0.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 8059.

**Respuesta esperada según la etiqueta: `V00023`**

- Variante 1: PICK UP 2.5L 2 PUERTAS MANUAL DH AA PAQ SEG
  Fabricante: NISSAN; submodelo: ESTACAS; tipo: PICK UP; segmento: PICK UP.
- Variante 2: NP300 PICK UP 2.5L 2 PUERTAS MANUAL DH AA PAQ SEG
  Fabricante: NISSAN; submodelo: ESTACAS; tipo: PICK UP; segmento: PICK UP.

Años registrados por código: 2017, 2018, 2019, 2020.

**Primera respuesta devuelta: `P000AO`**

- Variante 1: NP300 ESTACAS 2.4L 2 PUERTAS MANUAL DH PAQ SEG
  Fabricante: NISSAN; submodelo: PICK UP; tipo: PICK UP; segmento: PICK UP.

Años registrados por código: 2015, 2017, 2018.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.5382496654987335, "vehicle_type": 0.0, "year": 0.12}`

**Investigación propuesta:** Comparar atributos que distinguen las opciones y comprobar si aparecen en la entrada. Si faltan motor, versión, capacidad o tracción, pedir esa información y mantener revisión.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0014 — development — REMOLQUE

**Consulta original:** PLATAFORMA 2 EJES

- Año recibido: 2006.
- Marca recibida: vacía.
- Submarca recibida: vacía.
- Tipo recibido: vacío.
- Top-3 devuelto, en orden: `S0008A|U0007I|D0006V`.
- Etapa del fallo: Recuperación: el código esperado no entró en los 50 candidatos.
- Posición de recuperación del esperado: fuera de los 50.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 9501.

**Respuesta esperada según la etiqueta: `Z0000M`**

- Variante 1: RM CAJA CERRADA 2 EJES 40
  Fabricante: SEMIRREMOLQUES; submodelo: CAJA SECA; tipo: SEMIREMOLQUE; segmento: SEMIREMOLQUE.

Años registrados por código: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.

**Primera respuesta devuelta: `S0008A`**

- Variante 1: RM PLATAFORMA 2 EJES 40
  Fabricante: SEMIRREMOLQUES; submodelo: PLATAFORMA ALTA; tipo: SEMIREMOLQUE; segmento: SEMIREMOLQUE.

Años registrados por código: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.09000000000000001, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.599103569984436, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Comparar la representación textual del esperado con la consulta; comprobar campos faltantes, vocabulario y posibles reglas de dominio. Modificar solo el ranking no puede rescatar un candidato que no se recuperó.

**Pregunta adicional al experto:** este código se repite en 33 etiquetas y describe
una caja cerrada. Confirmar si existe una regla genérica de negocio que explique su
uso en consultas diferentes. No añadirlo como fallback ni corregir la etiqueta por suposición.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0015 — development — REMOLQUE

**Consulta original:** PLATAFORMA 2 EJES

- Año recibido: 2004.
- Marca recibida: vacía.
- Submarca recibida: vacía.
- Tipo recibido: vacío.
- Top-3 devuelto, en orden: `S0008A|U0007I|D0006V`.
- Etapa del fallo: Recuperación: el código esperado no entró en los 50 candidatos.
- Posición de recuperación del esperado: fuera de los 50.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 9501.

**Respuesta esperada según la etiqueta: `Z0000M`**

- Variante 1: RM CAJA CERRADA 2 EJES 40
  Fabricante: SEMIRREMOLQUES; submodelo: CAJA SECA; tipo: SEMIREMOLQUE; segmento: SEMIREMOLQUE.

Años registrados por código: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.

**Primera respuesta devuelta: `S0008A`**

- Variante 1: RM PLATAFORMA 2 EJES 40
  Fabricante: SEMIRREMOLQUES; submodelo: PLATAFORMA ALTA; tipo: SEMIREMOLQUE; segmento: SEMIREMOLQUE.

Años registrados por código: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.09000000000000001, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.599103569984436, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Comparar la representación textual del esperado con la consulta; comprobar campos faltantes, vocabulario y posibles reglas de dominio. Modificar solo el ranking no puede rescatar un candidato que no se recuperó.

**Pregunta adicional al experto:** este código se repite en 33 etiquetas y describe
una caja cerrada. Confirmar si existe una regla genérica de negocio que explique su
uso en consultas diferentes. No añadirlo como fallback ni corregir la etiqueta por suposición.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0018 — development — REMOLQUE

**Consulta original:** REMOLQUES

- Año recibido: 2025.
- Marca recibida: vacía.
- Submarca recibida: vacía.
- Tipo recibido: vacío.
- Top-3 devuelto, en orden: `G000CT|D0004U|U0001V`.
- Etapa del fallo: Ranking: el esperado fue recuperado, pero quedó fuera de los tres primeros.
- Posición de recuperación del esperado: 26.0.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 3535.

**Respuesta esperada según la etiqueta: `Z0000M`**

- Variante 1: RM CAJA CERRADA 2 EJES 40
  Fabricante: SEMIRREMOLQUES; submodelo: CAJA SECA; tipo: SEMIREMOLQUE; segmento: SEMIREMOLQUE.

Años registrados por código: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.

**Primera respuesta devuelta: `G000CT`**

- Variante 1: RM JAULA 2 EJES 35
  Fabricante: SEMIRREMOLQUES; submodelo: JAULA; tipo: SEMIREMOLQUE; segmento: SEMIREMOLQUE.

Años registrados por código: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2018, 2019, 2023, 2025.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.09000000000000001, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.11544596403837204, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Inspeccionar las señales del esperado frente a las alternativas superiores; comprobar si similitud, año o metadatos favorecieron una opción incompatible. No asumir que aumentar el número de candidatos corrige este ordenamiento.

**Pregunta adicional al experto:** este código se repite en 33 etiquetas y describe
una caja cerrada. Confirmar si existe una regla genérica de negocio que explique su
uso en consultas diferentes. No añadirlo como fallback ni corregir la etiqueta por suposición.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0019 — development — REMOLQUE

**Consulta original:** RM SEMIREMOLQUE

- Año recibido: 2019.
- Marca recibida: vacía.
- Submarca recibida: vacía.
- Tipo recibido: CHASIS.
- Top-3 devuelto, en orden: `Q00046|G000CT|Z0000M`.
- Etapa del fallo: Ranking: el esperado sí está en el top-3, pero otra alternativa quedó primera.
- Posición de recuperación del esperado: 10.0.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 8332.

**Respuesta esperada según la etiqueta: `Z0000M`**

- Variante 1: RM CAJA CERRADA 2 EJES 40
  Fabricante: SEMIRREMOLQUES; submodelo: CAJA SECA; tipo: SEMIREMOLQUE; segmento: SEMIREMOLQUE.

Años registrados por código: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.

**Primera respuesta devuelta: `Q00046`**

- Variante 1: SEMIREMOLQUE TANQUE ELIPTICO
  Fabricante: SEMIRREMOLQUES; submodelo: TANQUE; tipo: SEMIREMOLQUE; segmento: SEMIREMOLQUE.

Años registrados por código: 2014, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.40149444937705997, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Comparar atributos que distinguen las opciones y comprobar si aparecen en la entrada. Si faltan motor, versión, capacidad o tracción, pedir esa información y mantener revisión.

**Pregunta adicional al experto:** este código se repite en 33 etiquetas y describe
una caja cerrada. Confirmar si existe una regla genérica de negocio que explique su
uso en consultas diferentes. No añadirlo como fallback ni corregir la etiqueta por suposición.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0047 — development — AUTO

**Consulta original:** ESCALADE ESV PAQ B 2021

- Año recibido: 2021.
- Marca recibida: CADILLAC.
- Submarca recibida: ESCALADE ESV PAQ B.
- Tipo recibido: AUTO.
- Top-3 devuelto, en orden: `I000A6|E0002F|S00067`.
- Etapa del fallo: Ranking: el esperado sí está en el top-3, pero otra alternativa quedó primera.
- Posición de recuperación del esperado: 7.0.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 4464.

**Respuesta esperada según la etiqueta: `E0002F`**

- Variante 1: ESCALADE ESV PREMIUM LUXURY V8 6.2L 5 PTS AUT
  Fabricante: CADILLAC; submodelo: ESCALADE; tipo: AUTO; segmento: SUV LUJO.

Años registrados por código: 2021, 2022, 2023, 2025, 2026.

**Primera respuesta devuelta: `I000A6`**

- Variante 1: ESCALADE ESV PREMIUM V8 6.2L AUT 5P ABS CA CE PIEL CQ CB
  Fabricante: CADILLAC; submodelo: ESCALADE; tipo: AUTO; segmento: SUV LUJO.
- Variante 2: ESCALADE ESV PREMIUM 6.2L 5 PUERTAS AUTOMATICA PAQ E
  Fabricante: CADILLAC; submodelo: ESCALADE; tipo: AUTO; segmento: SUV LUJO.

Años registrados por código: 2015, 2016, 2020, 2021.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.08333333333333333, "manufacturer": 0.02, "submodel": 0.02, "tfidf": 0.5294214963912964, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Comparar atributos que distinguen las opciones y comprobar si aparecen en la entrada. Si faltan motor, versión, capacidad o tracción, pedir esa información y mantener revisión.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0053 — development — REMOLQUE

**Consulta original:** TOLVA

- Año recibido: 2019.
- Marca recibida: CARMEX.
- Submarca recibida: vacía.
- Tipo recibido: TOLVA.
- Top-3 devuelto, en orden: `Z0005P|Z0003K|R0002X`.
- Etapa del fallo: Recuperación: el código esperado no entró en los 50 candidatos.
- Posición de recuperación del esperado: fuera de los 50.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 12996.

**Respuesta esperada según la etiqueta: `Z0000M`**

- Variante 1: RM CAJA CERRADA 2 EJES 40
  Fabricante: SEMIRREMOLQUES; submodelo: CAJA SECA; tipo: SEMIREMOLQUE; segmento: SEMIREMOLQUE.

Años registrados por código: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.

**Primera respuesta devuelta: `Z0005P`**

- Variante 1: TOLVA CEMENTERA.
  Fabricante: SEMIRREMOLQUES; submodelo: TOLVA CEMENTERA; tipo: SEMIREMOLQUE; segmento: SEMIREMOLQUE.

Años registrados por código: 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.2525744497776032, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Comparar la representación textual del esperado con la consulta; comprobar campos faltantes, vocabulario y posibles reglas de dominio. Modificar solo el ranking no puede rescatar un candidato que no se recuperó.

**Pregunta adicional al experto:** este código se repite en 33 etiquetas y describe
una caja cerrada. Confirmar si existe una regla genérica de negocio que explique su
uso en consultas diferentes. No añadirlo como fallback ni corregir la etiqueta por suposición.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0054 — development — REMOLQUE

**Consulta original:** PLATAFORMA

- Año recibido: 2008.
- Marca recibida: CATAMEX.
- Submarca recibida: PLATAFORMA.
- Tipo recibido: vacío.
- Top-3 devuelto, en orden: `L0001A|D0006V|E0001Q`.
- Etapa del fallo: Recuperación: el código esperado no entró en los 50 candidatos.
- Posición de recuperación del esperado: fuera de los 50.
- Conflictos detectados en top-1: vehicle_type.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 5675.

**Respuesta esperada según la etiqueta: `Z0000M`**

- Variante 1: RM CAJA CERRADA 2 EJES 40
  Fabricante: SEMIRREMOLQUES; submodelo: CAJA SECA; tipo: SEMIREMOLQUE; segmento: SEMIREMOLQUE.

Años registrados por código: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.

**Primera respuesta devuelta: `L0001A`**

- Variante 1: CAMION INTERNACIONAL PLATAFORMA .
  Fabricante: INTERNATIONAL; submodelo: PLATAFORMA; tipo: CAMION; segmento: CAMION DE 9.5 HASTA 12.5 TONELADAS.

Años registrados por código: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.02, "tfidf": 0.4611872792243958, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Comparar la representación textual del esperado con la consulta; comprobar campos faltantes, vocabulario y posibles reglas de dominio. Modificar solo el ranking no puede rescatar un candidato que no se recuperó.

**Pregunta adicional al experto:** este código se repite en 33 etiquetas y describe
una caja cerrada. Confirmar si existe una regla genérica de negocio que explique su
uso en consultas diferentes. No añadirlo como fallback ni corregir la etiqueta por suposición.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0055 — development — AUTO

**Consulta original:** ALSVIN TM

- Año recibido: 2024.
- Marca recibida: CHANGAN.
- Submarca recibida: vacía.
- Tipo recibido: AUTOS.
- Top-3 devuelto, en orden: `P0007H|P00056|Y00051`.
- Etapa del fallo: Ranking: el esperado sí está en el top-3, pero otra alternativa quedó primera.
- Posición de recuperación del esperado: 2.0.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 7942.

**Respuesta esperada según la etiqueta: `P00056`**

- Variante 1: CHANGAN ALSVIN BASE L4 4 PTS STD
  Fabricante: CHANGAN; submodelo: ALSVIN; tipo: AUTO; segmento: SEDAN.

Años registrados por código: 2022, 2023, 2024, 2025, 2026.

**Primera respuesta devuelta: `P0007H`**

- Variante 1: CHANGAN ALSVIN BASE L4 4 PTS AUT
  Fabricante: CHANGAN; submodelo: ALSVIN; tipo: AUTO; segmento: SEDAN.

Años registrados por código: 2022, 2023, 2024, 2025, 2026.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.0855, "manufacturer": 0.02, "submodel": 0.0, "tfidf": 0.5840484380722046, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Comparar atributos que distinguen las opciones y comprobar si aparecen en la entrada. Si faltan motor, versión, capacidad o tracción, pedir esa información y mantener revisión.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0068 — development — OTHER

**Consulta original:** TIGGO 8 PRO PREMIUM E HEV L4 HDS AUT 5 ABS CA CE PIEL SM CQ C

- Año recibido: 2025.
- Marca recibida: CHIREY.
- Submarca recibida: vacía.
- Tipo recibido: vacío.
- Top-3 devuelto, en orden: `C000C5|S0002Y|S0004C`.
- Etapa del fallo: Ranking: el esperado sí está en el top-3, pero otra alternativa quedó primera.
- Posición de recuperación del esperado: 2.0.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 1461.

**Respuesta esperada según la etiqueta: `S0002Y`**

- Variante 1: CHIREY TIGGO 8 PRO E+ PREMIUM
  Fabricante: CHIREY; submodelo: TIGGO 8; tipo: AUTO; segmento: SUV.

Años registrados por código: 2025.

**Primera respuesta devuelta: `C000C5`**

- Variante 1: CHIREY TIGGO 8 PRO PREMIUM L4 1.6T 5 PTS AUT PIEL
  Fabricante: CHIREY; submodelo: TIGGO 8; tipo: AUTO; segmento: SUV.

Años registrados por código: 2024, 2025.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.08539325842696631, "manufacturer": 0.02, "submodel": 0.0, "tfidf": 0.605037260055542, "vehicle_type": 0.0, "year": 0.12}`

**Investigación propuesta:** Comparar atributos que distinguen las opciones y comprobar si aparecen en la entrada. Si faltan motor, versión, capacidad o tracción, pedir esa información y mantener revisión.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0074 — development — OTHER

**Consulta original:** JEEP WRANGLER SAHARA

- Año recibido: 2015.
- Marca recibida: CHRYSLER.
- Submarca recibida: JEEP WRANGLER SAHARA.
- Tipo recibido: vacío.
- Top-3 devuelto, en orden: `I0007V|G00001|M0004C`.
- Etapa del fallo: Ranking: el esperado sí está en el top-3, pero otra alternativa quedó primera.
- Posición de recuperación del esperado: 17.0.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 4380.

**Respuesta esperada según la etiqueta: `G00001`**

- Variante 1: WRANGLER UNLIMITED SAHARA 3.8L 205HP 4X4 V6 AUT 4P CA CE
  Fabricante: CHRYSLER; submodelo: JEEP WRANGLER; tipo: AUTO; segmento: SUV.

Años registrados por código: 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016.

**Primera respuesta devuelta: `I0007V`**

- Variante 1: WRANGLER SAHARA TOLDO DURO 4X4 V6 AUT 2P CA CE PIEL CD
  Fabricante: CHRYSLER; submodelo: JEEP WRANGLER; tipo: AUTO; segmento: SUV.

Años registrados por código: 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.0855, "manufacturer": 0.02, "submodel": 0.02, "tfidf": 0.577604752779007, "vehicle_type": 0.0, "year": 0.12}`

**Investigación propuesta:** Comparar atributos que distinguen las opciones y comprobar si aparecen en la entrada. Si faltan motor, versión, capacidad o tracción, pedir esa información y mantener revisión.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0082 — development — REMOLQUE

**Consulta original:** TOLVA

- Año recibido: 2023.
- Marca recibida: DALTO.
- Submarca recibida: vacía.
- Tipo recibido: TOLVA.
- Top-3 devuelto, en orden: `J0007M|Z0005P|L0008A`.
- Etapa del fallo: Recuperación: el código esperado no entró en los 50 candidatos.
- Posición de recuperación del esperado: fuera de los 50.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 4883.

**Respuesta esperada según la etiqueta: `Z0000M`**

- Variante 1: RM CAJA CERRADA 2 EJES 40
  Fabricante: SEMIRREMOLQUES; submodelo: CAJA SECA; tipo: SEMIREMOLQUE; segmento: SEMIREMOLQUE.

Años registrados por código: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.

**Primera respuesta devuelta: `J0007M`**

- Variante 1: RM TOLVA GRANELERA 2 EJES NAC
  Fabricante: SEMIRREMOLQUES; submodelo: TOLVA GRANELERA; tipo: SEMIREMOLQUE; segmento: SEMIREMOLQUE.

Años registrados por código: 2020, 2021, 2022, 2023.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.3192595839500427, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Comparar la representación textual del esperado con la consulta; comprobar campos faltantes, vocabulario y posibles reglas de dominio. Modificar solo el ranking no puede rescatar un candidato que no se recuperó.

**Pregunta adicional al experto:** este código se repite en 33 etiquetas y describe
una caja cerrada. Confirmar si existe una regla genérica de negocio que explique su
uso en consultas diferentes. No añadirlo como fallback ni corregir la etiqueta por suposición.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0083 — development — REMOLQUE

**Consulta original:** TOLVA

- Año recibido: 2020.
- Marca recibida: DALTO.
- Submarca recibida: vacía.
- Tipo recibido: TOLVA.
- Top-3 devuelto, en orden: `Z0005P|J0007M|R0002X`.
- Etapa del fallo: Recuperación: el código esperado no entró en los 50 candidatos.
- Posición de recuperación del esperado: fuera de los 50.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 12996.

**Respuesta esperada según la etiqueta: `Z0000M`**

- Variante 1: RM CAJA CERRADA 2 EJES 40
  Fabricante: SEMIRREMOLQUES; submodelo: CAJA SECA; tipo: SEMIREMOLQUE; segmento: SEMIREMOLQUE.

Años registrados por código: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.

**Primera respuesta devuelta: `Z0005P`**

- Variante 1: TOLVA CEMENTERA.
  Fabricante: SEMIRREMOLQUES; submodelo: TOLVA CEMENTERA; tipo: SEMIREMOLQUE; segmento: SEMIREMOLQUE.

Años registrados por código: 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.40361698865890505, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Comparar la representación textual del esperado con la consulta; comprobar campos faltantes, vocabulario y posibles reglas de dominio. Modificar solo el ranking no puede rescatar un candidato que no se recuperó.

**Pregunta adicional al experto:** este código se repite en 33 etiquetas y describe
una caja cerrada. Confirmar si existe una regla genérica de negocio que explique su
uso en consultas diferentes. No añadirlo como fallback ni corregir la etiqueta por suposición.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0084 — development — REMOLQUE

**Consulta original:** TOLVA

- Año recibido: 2021.
- Marca recibida: DALTO.
- Submarca recibida: vacía.
- Tipo recibido: TOLVA.
- Top-3 devuelto, en orden: `J0007M|R0002X|K000DZ`.
- Etapa del fallo: Recuperación: el código esperado no entró en los 50 candidatos.
- Posición de recuperación del esperado: fuera de los 50.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 4883.

**Respuesta esperada según la etiqueta: `Z0000M`**

- Variante 1: RM CAJA CERRADA 2 EJES 40
  Fabricante: SEMIRREMOLQUES; submodelo: CAJA SECA; tipo: SEMIREMOLQUE; segmento: SEMIREMOLQUE.

Años registrados por código: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.

**Primera respuesta devuelta: `J0007M`**

- Variante 1: RM TOLVA GRANELERA 2 EJES NAC
  Fabricante: SEMIRREMOLQUES; submodelo: TOLVA GRANELERA; tipo: SEMIREMOLQUE; segmento: SEMIREMOLQUE.

Años registrados por código: 2020, 2021, 2022, 2023.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.3192595839500427, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Comparar la representación textual del esperado con la consulta; comprobar campos faltantes, vocabulario y posibles reglas de dominio. Modificar solo el ranking no puede rescatar un candidato que no se recuperó.

**Pregunta adicional al experto:** este código se repite en 33 etiquetas y describe
una caja cerrada. Confirmar si existe una regla genérica de negocio que explique su
uso en consultas diferentes. No añadirlo como fallback ni corregir la etiqueta por suposición.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0089 — development — REMOLQUE

**Consulta original:** PLATAFORMA

- Año recibido: 2003.
- Marca recibida: DEL NORTE.
- Submarca recibida: PLATAFORMA.
- Tipo recibido: vacío.
- Top-3 devuelto, en orden: `L0001A|D0006V|P000C6`.
- Etapa del fallo: Recuperación: el código esperado no entró en los 50 candidatos.
- Posición de recuperación del esperado: fuera de los 50.
- Conflictos detectados en top-1: vehicle_type.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 5675.

**Respuesta esperada según la etiqueta: `Z0000M`**

- Variante 1: RM CAJA CERRADA 2 EJES 40
  Fabricante: SEMIRREMOLQUES; submodelo: CAJA SECA; tipo: SEMIREMOLQUE; segmento: SEMIREMOLQUE.

Años registrados por código: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.

**Primera respuesta devuelta: `L0001A`**

- Variante 1: CAMION INTERNACIONAL PLATAFORMA .
  Fabricante: INTERNATIONAL; submodelo: PLATAFORMA; tipo: CAMION; segmento: CAMION DE 9.5 HASTA 12.5 TONELADAS.

Años registrados por código: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.02, "tfidf": 0.40458899438381196, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Comparar la representación textual del esperado con la consulta; comprobar campos faltantes, vocabulario y posibles reglas de dominio. Modificar solo el ranking no puede rescatar un candidato que no se recuperó.

**Pregunta adicional al experto:** este código se repite en 33 etiquetas y describe
una caja cerrada. Confirmar si existe una regla genérica de negocio que explique su
uso en consultas diferentes. No añadirlo como fallback ni corregir la etiqueta por suposición.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0093 — development — CAMION

**Consulta original:** VOLTEO

- Año recibido: 1994.
- Marca recibida: DINA.
- Submarca recibida: vacía.
- Tipo recibido: VOLTEO.
- Top-3 devuelto, en orden: `W000CD|B0001Z|Y000DW`.
- Etapa del fallo: Recuperación: el código esperado no entró en los 50 candidatos.
- Posición de recuperación del esperado: fuera de los 50.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 11700.

**Respuesta esperada según la etiqueta: `Z0000M`**

- Variante 1: RM CAJA CERRADA 2 EJES 40
  Fabricante: SEMIRREMOLQUES; submodelo: CAJA SECA; tipo: SEMIREMOLQUE; segmento: SEMIREMOLQUE.

Años registrados por código: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.

**Primera respuesta devuelta: `W000CD`**

- Variante 1: DINA VOLTEO DE 14 TON.
  Fabricante: DINA; submodelo: 661-K VOLTEO; tipo: CAMION; segmento: CAMION DE 12.5 HASTA 14 TONELADAS.

Años registrados por código: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.09000000000000001, "manufacturer": 0.02, "submodel": 0.0, "tfidf": 0.6013042151927949, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Comparar la representación textual del esperado con la consulta; comprobar campos faltantes, vocabulario y posibles reglas de dominio. Modificar solo el ranking no puede rescatar un candidato que no se recuperó.

**Pregunta adicional al experto:** este código se repite en 33 etiquetas y describe
una caja cerrada. Confirmar si existe una regla genérica de negocio que explique su
uso en consultas diferentes. No añadirlo como fallback ni corregir la etiqueta por suposición.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0100 — development — CAMION

**Consulta original:** CHASIS CABINA

- Año recibido: 2009.
- Marca recibida: DODGE H100.
- Submarca recibida: CHASIS CABINA.
- Tipo recibido: vacío.
- Top-3 devuelto, en orden: `H0002P|U00085|K0009D`.
- Etapa del fallo: Ranking: el esperado sí está en el top-3, pero otra alternativa quedó primera.
- Posición de recuperación del esperado: 2.0.
- Conflictos detectados en top-1: submodel|vehicle_type.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 3681.

**Respuesta esperada según la etiqueta: `U00085`**

- Variante 1: DODGE H 100 CHASIS CABINA DH L4 CA
  Fabricante: CHRYSLER; submodelo: H100 ESTACAS; tipo: PICK UP; segmento: PICK UP.

Años registrados por código: 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014.

**Primera respuesta devuelta: `H0002P`**

- Variante 1: H100 CHASIS CABINA DIESEL STD., 02 OCUP.
  Fabricante: CHRYSLER; submodelo: H100 ESTACAS; tipo: PICK UP; segmento: PICK UP.

Años registrados por código: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 2006, 2007, 2008, 2009.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": -0.05, "tfidf": 0.5092259645462036, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Comparar atributos que distinguen las opciones y comprobar si aparecen en la entrada. Si faltan motor, versión, capacidad o tracción, pedir esa información y mantener revisión.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0104 — development — REMOLQUE

**Consulta original:** EL AGUILA *

- Año recibido: 2023.
- Marca recibida: EL AGUILA.
- Submarca recibida: vacía.
- Tipo recibido: SEMIREMOLQUE.
- Top-3 devuelto, en orden: `X0001I|W0005C|X00036`.
- Etapa del fallo: Recuperación: el código esperado no entró en los 50 candidatos.
- Posición de recuperación del esperado: fuera de los 50.
- Conflictos detectados en top-1: vehicle_type|year.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 11816.

**Respuesta esperada según la etiqueta: `Z0000M`**

- Variante 1: RM CAJA CERRADA 2 EJES 40
  Fabricante: SEMIRREMOLQUES; submodelo: CAJA SECA; tipo: SEMIREMOLQUE; segmento: SEMIREMOLQUE.

Años registrados por código: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.

**Primera respuesta devuelta: `X0001I`**

- Variante 1: EL NUEVO JETTA GL AUT., 05 OCUP.
  Fabricante: VOLKSWAGEN; submodelo: JETTA A3; tipo: AUTO; segmento: COMPACTO.

Años registrados por código: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.16423431336879732, "vehicle_type": 0, "year": -0.2}`

**Investigación propuesta:** Comparar la representación textual del esperado con la consulta; comprobar campos faltantes, vocabulario y posibles reglas de dominio. Modificar solo el ranking no puede rescatar un candidato que no se recuperó.

**Pregunta adicional al experto:** este código se repite en 33 etiquetas y describe
una caja cerrada. Confirmar si existe una regla genérica de negocio que explique su
uso en consultas diferentes. No añadirlo como fallback ni corregir la etiqueta por suposición.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0111 — development — OTHER

**Consulta original:** ESTACAS DH NP300 ESTACAS STD AA 158HP 2.5L 4CIL 2P 3OCUP 2019

- Año recibido: 2019.
- Marca recibida: ESTACAS DH NP300 ESTACAS STD AA 158HP 2.5L 4CIL 2P 3OCUP.
- Submarca recibida: vacía.
- Tipo recibido: vacío.
- Top-3 devuelto, en orden: `V00023|N0006O|W0009H`.
- Etapa del fallo: Ranking: el esperado fue recuperado, pero quedó fuera de los tres primeros.
- Posición de recuperación del esperado: 22.0.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 10813.

**Respuesta esperada según la etiqueta: `H000BN`**

- Variante 1: NP300 CHASIS CABINA 2.5L 2 PUERTAS MANUAL DH AA PAQ SEG
  Fabricante: NISSAN; submodelo: CHASIS CABINA; tipo: PICK UP; segmento: PICK UP.

Años registrados por código: 2017, 2018, 2019, 2020.

**Primera respuesta devuelta: `V00023`**

- Variante 1: PICK UP 2.5L 2 PUERTAS MANUAL DH AA PAQ SEG
  Fabricante: NISSAN; submodelo: ESTACAS; tipo: PICK UP; segmento: PICK UP.
- Variante 2: NP300 PICK UP 2.5L 2 PUERTAS MANUAL DH AA PAQ SEG
  Fabricante: NISSAN; submodelo: ESTACAS; tipo: PICK UP; segmento: PICK UP.

Años registrados por código: 2017, 2018, 2019, 2020.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.30323477983474734, "vehicle_type": 0.0, "year": 0.12}`

**Investigación propuesta:** Inspeccionar las señales del esperado frente a las alternativas superiores; comprobar si similitud, año o metadatos favorecieron una opción incompatible. No asumir que aumentar el número de candidatos corrige este ordenamiento.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0123 — development — CAMION

**Consulta original:** FOIRD XL REG CHASIS F550

- Año recibido: 2024.
- Marca recibida: FOIRD.
- Submarca recibida: vacía.
- Tipo recibido: CAMIONES.
- Top-3 devuelto, en orden: `C000BM|N00001|R00091`.
- Etapa del fallo: Recuperación: el código esperado no entró en los 50 candidatos.
- Posición de recuperación del esperado: fuera de los 50.
- Conflictos detectados en top-1: vehicle_type.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 1441.

**Respuesta esperada según la etiqueta: `Q00084`**

- Variante 1: F-550 KTP XL CH 2P V8 6.7L TDI AUT 2 OCUP
  Fabricante: FORD; submodelo: F-550; tipo: PICK UP; segmento: PICK UP.

Años registrados por código: 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024.

**Primera respuesta devuelta: `C000BM`**

- Variante 1: F-150 XL REG CAB 3.5L 2 PUERTAS AUTOMATICA 4X2
  Fabricante: FORD; submodelo: F-150 PICK UP; tipo: PICK UP; segmento: PICK UP.

Años registrados por código: 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.30231362879276275, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Comparar la representación textual del esperado con la consulta; comprobar campos faltantes, vocabulario y posibles reglas de dominio. Modificar solo el ranking no puede rescatar un candidato que no se recuperó.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0127 — development — OTHER

**Consulta original:** F450

- Año recibido: 2023.
- Marca recibida: FORD.
- Submarca recibida: F450.
- Tipo recibido: vacío.
- Top-3 devuelto, en orden: `H0004G|V000AP|U0009M`.
- Etapa del fallo: Recuperación: el código esperado no entró en los 50 candidatos.
- Posición de recuperación del esperado: fuera de los 50.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 3745.

**Respuesta esperada según la etiqueta: `U00024`**

- Variante 1: F-450 XL KTP 6.7L 2 PUERTAS AUTOMATICA DIESEL
  Fabricante: FORD; submodelo: F-450; tipo: PICK UP; segmento: PICK UP.

Años registrados por código: 2001, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024.

**Primera respuesta devuelta: `H0004G`**

- Variante 1: FORD F-150 XL CREW CAB V6 3.3L 4 PTS AUT
  Fabricante: FORD; submodelo: F-150 PICK UP; tipo: PICK UP; segmento: PICK UP.

Años registrados por código: 2022, 2023.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.0855, "manufacturer": 0.02, "submodel": 0.0, "tfidf": 0.1829436331987381, "vehicle_type": 0.0, "year": 0.12}`

**Investigación propuesta:** Comparar la representación textual del esperado con la consulta; comprobar campos faltantes, vocabulario y posibles reglas de dominio. Modificar solo el ranking no puede rescatar un candidato que no se recuperó.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0134 — development — OTHER

**Consulta original:** FREIGHTLINER DETROIT DIESEL DD13 CASCADIA CAS

- Año recibido: 2025.
- Marca recibida: FREIGHTLINER.
- Submarca recibida: CASCADIA 125.
- Tipo recibido: -.
- Top-3 devuelto, en orden: `U0008Z|N0001W|H0001S`.
- Etapa del fallo: Ranking: el esperado sí está en el top-3, pero otra alternativa quedó primera.
- Posición de recuperación del esperado: 15.0.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 10549.

**Respuesta esperada según la etiqueta: `N0001W`**

- Variante 1: FREIGHTLINER NEW CASCADIA  EURO V DD13 470HP FULLER 18VEL
  Fabricante: FREIGHTLINER; submodelo: CASCADIA; tipo: TRACTO CAMION; segmento: TRACTOCAMION.

Años registrados por código: 2020, 2021, 2022, 2023, 2024, 2025, 2026.

**Primera respuesta devuelta: `U0008Z`**

- Variante 1: FREIGHTLINER CASCADIA 116 DD13 470HP
  Fabricante: FREIGHTLINER; submodelo: CASCADIA; tipo: TRACTO CAMION; segmento: TRACTOCAMION.

Años registrados por código: 2024, 2025.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.07967741935483871, "manufacturer": 0.02, "submodel": 0.02, "tfidf": 0.5389693021774292, "vehicle_type": 0.0, "year": 0.12}`

**Investigación propuesta:** Comparar atributos que distinguen las opciones y comprobar si aparecen en la entrada. Si faltan motor, versión, capacidad o tracción, pedir esa información y mantener revisión.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0137 — development — CAMION

**Consulta original:** VOLTEO

- Año recibido: 2010.
- Marca recibida: FREIGHTLINER.
- Submarca recibida: vacía.
- Tipo recibido: VOLTEO.
- Top-3 devuelto, en orden: `G0004P|B00045|Y0000B`.
- Etapa del fallo: Recuperación: el código esperado no entró en los 50 candidatos.
- Posición de recuperación del esperado: fuera de los 50.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 3241.

**Respuesta esperada según la etiqueta: `Z0000M`**

- Variante 1: RM CAJA CERRADA 2 EJES 40
  Fabricante: SEMIRREMOLQUES; submodelo: CAJA SECA; tipo: SEMIREMOLQUE; segmento: SEMIREMOLQUE.

Años registrados por código: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.

**Primera respuesta devuelta: `G0004P`**

- Variante 1: FREIGHTLINER M2 33K VOLTEO 190HP
  Fabricante: FREIGHTLINER; submodelo: M2 33K; tipo: CAMION; segmento: CAMION HASTA 14 TONELADAS.

Años registrados por código: 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.0855, "manufacturer": 0.02, "submodel": 0.0, "tfidf": 0.4302010595798493, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Comparar la representación textual del esperado con la consulta; comprobar campos faltantes, vocabulario y posibles reglas de dominio. Modificar solo el ranking no puede rescatar un candidato que no se recuperó.

**Pregunta adicional al experto:** este código se repite en 33 etiquetas y describe
una caja cerrada. Confirmar si existe una regla genérica de negocio que explique su
uso en consultas diferentes. No añadirlo como fallback ni corregir la etiqueta por suposición.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0144 — development — OTHER

**Consulta original:** CHEVROLET SILVERADO 1500 CAB. REG. D STD

- Año recibido: 2012.
- Marca recibida: GENERAL MOTORS.
- Submarca recibida: vacía.
- Tipo recibido: vacío.
- Top-3 devuelto, en orden: `R000AP|W0008P|L0008K`.
- Etapa del fallo: Ranking: el esperado sí está en el top-3, pero otra alternativa quedó primera.
- Posición de recuperación del esperado: 11.0.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 9079.

**Respuesta esperada según la etiqueta: `W0008P`**

- Variante 1: CHEVROLET SILVERADO 1500 CABINA REGULAR 4.3L 195HP V6 STD CA BA
  Fabricante: GENERAL MOTORS; submodelo: SILVERADO 1500; tipo: PICK UP; segmento: PICK UP.

Años registrados por código: 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016.

**Primera respuesta devuelta: `R000AP`**

- Variante 1: CHEVROLET C-1500 PICK UP SILVERADO STD V6
  Fabricante: GENERAL MOTORS; submodelo: SILVERADO 1500; tipo: PICK UP; segmento: PICK UP.

Años registrados por código: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.08510416666666666, "manufacturer": 0.02, "submodel": 0.0, "tfidf": 0.47731465101242065, "vehicle_type": 0.0, "year": 0.12}`

**Investigación propuesta:** Comparar atributos que distinguen las opciones y comprobar si aparecen en la entrada. Si faltan motor, versión, capacidad o tracción, pedir esa información y mantener revisión.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0151 — development — CAMION

**Consulta original:** GIANT MOTORS JAC FRISON T6 2.0L 4CL 190 HP 213 BLP 6 VEL  CHASIS CABINA  X200

- Año recibido: 2024.
- Marca recibida: GIANT MOTORS.
- Submarca recibida: vacía.
- Tipo recibido: PICKUP.
- Top-3 devuelto, en orden: `N000CN|Z0008D|H0006S`.
- Etapa del fallo: Ranking: el esperado sí está en el top-3, pero otra alternativa quedó primera.
- Posición de recuperación del esperado: 12.0.
- Conflictos detectados en top-1: manufacturer.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 7106.

**Respuesta esperada según la etiqueta: `Z0008D`**

- Variante 1: T6 FLEX FRISON L4 2.0T 190 CP 4 PUERTAS STD  BA AA
  Fabricante: JAC; submodelo: T6; tipo: PICK UP; segmento: PICK UP.

Años registrados por código: 2024, 2025.

**Primera respuesta devuelta: `N000CN`**

- Variante 1: T6 FRISON L4 2.0T 190 CP 4 PUERTAS STD  BA AA
  Fabricante: JAC; submodelo: T6; tipo: PICK UP; segmento: PICK UP.

Años registrados por código: 2020, 2021, 2022, 2023, 2024.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.0855, "manufacturer": -0.1, "submodel": 0.0, "tfidf": 0.2693126142024994, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Comparar atributos que distinguen las opciones y comprobar si aparecen en la entrada. Si faltan motor, versión, capacidad o tracción, pedir esa información y mantener revisión.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0163 — development — CAMION

**Consulta original:** HINO 1018 G EURO

- Año recibido: 2024.
- Marca recibida: HINO.
- Submarca recibida: vacía.
- Tipo recibido: CAMIONES.
- Top-3 devuelto, en orden: `B000D5|N0004N|K0004M`.
- Etapa del fallo: Ranking: el esperado sí está en el top-3, pero otra alternativa quedó primera.
- Posición de recuperación del esperado: 2.0.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 987.

**Respuesta esperada según la etiqueta: `N0004N`**

- Variante 1: EQ HINO MOTORS 1018G CHASIS CABINA
  Fabricante: HINO; submodelo: 1018; tipo: CAMION; segmento: CAMION DE 6.5 HASTA 7.5 TONELADAS.

Años registrados por código: 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2022, 2023, 2024, 2025.

**Primera respuesta devuelta: `B000D5`**

- Variante 1: EQ HINO MOTORS 1018J CHASIS CABINA
  Fabricante: HINO; submodelo: 1018; tipo: CAMION; segmento: CAMION DE 6.5 HASTA 7.5 TONELADAS.

Años registrados por código: 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.0855, "manufacturer": 0.02, "submodel": 0.0, "tfidf": 0.503111493587494, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Comparar atributos que distinguen las opciones y comprobar si aparecen en la entrada. Si faltan motor, versión, capacidad o tracción, pedir esa información y mantener revisión.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0175 — development — AUTO

**Consulta original:** HYUNDAI GRANDi10

- Año recibido: 2022.
- Marca recibida: HYUNDAI.
- Submarca recibida: vacía.
- Tipo recibido: AUTO.
- Top-3 devuelto, en orden: `J000B7|Q000B9|R0005L`.
- Etapa del fallo: Ranking: el esperado fue recuperado, pero quedó fuera de los tres primeros.
- Posición de recuperación del esperado: 43.0.
- Conflictos detectados en top-1: vehicle_type.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 5015.

**Respuesta esperada según la etiqueta: `L000BP`**

- Variante 1: GRAND i10 GL MID 1.25L L4 AUT 4P TELA
  Fabricante: HYUNDAI; submodelo: Grand i; tipo: AUTO; segmento: SUBCOMPACTO.

Años registrados por código: 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026.

**Primera respuesta devuelta: `J000B7`**

- Variante 1: HYUNDAI EX8 CHASIS CABINA 4X2
  Fabricante: HYUNDAI; submodelo: HD72; tipo: CAMION; segmento: CAMION DE 4.5 HASTA 6.5 TONELADAS.

Años registrados por código: 2022, 2023.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.0855, "manufacturer": 0.02, "submodel": 0.0, "tfidf": 0.39230584502220156, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Inspeccionar las señales del esperado frente a las alternativas superiores; comprobar si similitud, año o metadatos favorecieron una opción incompatible. No asumir que aumentar el número de candidatos corrige este ordenamiento.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0180 — development — AUTO

**Consulta original:** QX56 TA AWD V8 5PTAS

- Año recibido: 2012.
- Marca recibida: INFINITI.
- Submarca recibida: vacía.
- Tipo recibido: AUTOS.
- Top-3 devuelto, en orden: `K000B7|G0003R|F0003D`.
- Etapa del fallo: Ranking: el esperado sí está en el top-3, pero otra alternativa quedó primera.
- Posición de recuperación del esperado: 2.0.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 5525.

**Respuesta esperada según la etiqueta: `G0003R`**

- Variante 1: QX 56 AWD 5.6L V8 7SPEED AUT., 08 OCUP.
  Fabricante: INFINITI; submodelo: QX56; tipo: AUTO; segmento: LUJO.

Años registrados por código: 2012, 2013, 2014.

**Primera respuesta devuelta: `K000B7`**

- Variante 1: INFINITI QX56 5.6L AWD V8 AUT CA CE PIEL CQ CB
  Fabricante: INFINITI; submodelo: QX56; tipo: AUTO; segmento: LUJO.

Años registrados por código: 2006, 2012, 2013, 2014.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.0855, "manufacturer": 0.02, "submodel": 0.0, "tfidf": 0.5324179530143738, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Comparar atributos que distinguen las opciones y comprobar si aparecen en la entrada. Si faltan motor, versión, capacidad o tracción, pedir esa información y mantener revisión.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0188 — development — CAMION

**Consulta original:** VOLTEO

- Año recibido: 2008.
- Marca recibida: INTERNACIONAL.
- Submarca recibida: vacía.
- Tipo recibido: VOLTEO.
- Top-3 devuelto, en orden: `E000BZ|F0002G|L0001A`.
- Etapa del fallo: Recuperación: el código esperado no entró en los 50 candidatos.
- Posición de recuperación del esperado: fuera de los 50.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 2477.

**Respuesta esperada según la etiqueta: `Z0000M`**

- Variante 1: RM CAJA CERRADA 2 EJES 40
  Fabricante: SEMIRREMOLQUES; submodelo: CAJA SECA; tipo: SEMIREMOLQUE; segmento: SEMIREMOLQUE.

Años registrados por código: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.

**Primera respuesta devuelta: `E000BZ`**

- Variante 1: INTERNACIONAL 4300 4X2 VOLTEO 195HP 15 TON
  Fabricante: INTERNATIONAL; submodelo: 4300 MAS DE 14 TON; tipo: CAMION; segmento: CAMION HASTA 14 TONELADAS.

Años registrados por código: 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.0855, "manufacturer": 0.02, "submodel": 0.0, "tfidf": 0.3676578998565674, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Comparar la representación textual del esperado con la consulta; comprobar campos faltantes, vocabulario y posibles reglas de dominio. Modificar solo el ranking no puede rescatar un candidato que no se recuperó.

**Pregunta adicional al experto:** este código se repite en 33 etiquetas y describe
una caja cerrada. Confirmar si existe una regla genérica de negocio que explique su
uso en consultas diferentes. No añadirlo como fallback ni corregir la etiqueta por suposición.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0195 — development — CAMION

**Consulta original:** VOLTEO 4300

- Año recibido: 2002.
- Marca recibida: INTERNATIONAL.
- Submarca recibida: vacía.
- Tipo recibido: vacío.
- Top-3 devuelto, en orden: `E000BZ|Y000DN|A000B2`.
- Etapa del fallo: Recuperación: el código esperado no entró en los 50 candidatos.
- Posición de recuperación del esperado: fuera de los 50.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 2477.

**Respuesta esperada según la etiqueta: `Z0000M`**

- Variante 1: RM CAJA CERRADA 2 EJES 40
  Fabricante: SEMIRREMOLQUES; submodelo: CAJA SECA; tipo: SEMIREMOLQUE; segmento: SEMIREMOLQUE.

Años registrados por código: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.

**Primera respuesta devuelta: `E000BZ`**

- Variante 1: INTERNACIONAL 4300 4X2 VOLTEO 195HP 15 TON
  Fabricante: INTERNATIONAL; submodelo: 4300 MAS DE 14 TON; tipo: CAMION; segmento: CAMION HASTA 14 TONELADAS.

Años registrados por código: 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.0855, "manufacturer": 0.02, "submodel": 0.0, "tfidf": 0.474579656124115, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Comparar la representación textual del esperado con la consulta; comprobar campos faltantes, vocabulario y posibles reglas de dominio. Modificar solo el ranking no puede rescatar un candidato que no se recuperó.

**Pregunta adicional al experto:** este código se repite en 33 etiquetas y describe
una caja cerrada. Confirmar si existe una regla genérica de negocio que explique su
uso en consultas diferentes. No añadirlo como fallback ni corregir la etiqueta por suposición.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0200 — development — CAMION

**Consulta original:** ISUZU ELF600 CHASIS CABINA

- Año recibido: 2018.
- Marca recibida: ISUZU.
- Submarca recibida: vacía.
- Tipo recibido: CAMIONES.
- Top-3 devuelto, en orden: `S00079|P0002U|K000CV`.
- Etapa del fallo: Ranking: el esperado sí está en el top-3, pero otra alternativa quedó primera.
- Posición de recuperación del esperado: 4.0.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 9464.

**Respuesta esperada según la etiqueta: `P0002U`**

- Variante 1: EQ ISUZU ELF 600 CHASIS CABINA "H"
  Fabricante: ISUZU; submodelo: ELF 600; tipo: CAMION; segmento: CAMION DE 4.5 HASTA 6.5 TONELADAS.

Años registrados por código: 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018.

**Primera respuesta devuelta: `S00079`**

- Variante 1: EQ ISUZU ELF 600 CHASIS CABINA "M"
  Fabricante: ISUZU; submodelo: ELF 600; tipo: CAMION; segmento: CAMION DE 4.5 HASTA 6.5 TONELADAS.

Años registrados por código: 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2024, 2025, 2026.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.08022222222222222, "manufacturer": 0.02, "submodel": 0.0, "tfidf": 0.4903830707073212, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Comparar atributos que distinguen las opciones y comprobar si aparecen en la entrada. Si faltan motor, versión, capacidad o tracción, pedir esa información y mantener revisión.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0205 — development — OTHER

**Consulta original:** SUNRAY PASS SMART

- Año recibido: 2025.
- Marca recibida: JAC.
- Submarca recibida: SUNRAY PASS SMART.
- Tipo recibido: vacío.
- Top-3 devuelto, en orden: `C000BV|E0001N|B000BM`.
- Etapa del fallo: Ranking: el esperado sí está en el top-3, pero otra alternativa quedó primera.
- Posición de recuperación del esperado: 5.0.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: sí.
- Registro del catálogo usado por el top-1: 1451.

**Respuesta esperada según la etiqueta: `E0001N`**

- Variante 1: SUNRAY PASAJE L4 2.8T 150 CP 5 PTS STD
  Fabricante: JAC; submodelo: SUNRAY; tipo: AUTO; segmento: SUV.

Años registrados por código: 2018, 2022, 2023, 2024, 2025, 2026.

**Primera respuesta devuelta: `C000BV`**

- Variante 1: SUNRAY CARGO L4 2.8T 150 CP 5 PTS STD
  Fabricante: JAC; submodelo: HFC; tipo: PICK UP; segmento: VAN CARGA 3.5TON.
- Variante 2: SUNRAY CARGO L4 2.8T 150 CP 5 PTS STD
  Fabricante: JAC; submodelo: SUNRAY; tipo: PICK UP; segmento: VAN CARGA 3.5TON.

Años registrados por código: 2021, 2022, 2023, 2024, 2025, 2026, 2027.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.061290322580645165, "manufacturer": 0.02, "submodel": 0.02, "tfidf": 0.42449820041656494, "vehicle_type": 0.0, "year": 0.12}`

**Investigación propuesta:** Comparar atributos que distinguen las opciones y comprobar si aparecen en la entrada. Si faltan motor, versión, capacidad o tracción, pedir esa información y mantener revisión.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0210 — development — OTHER

**Consulta original:** SAHARA

- Año recibido: 2020.
- Marca recibida: JEEP UNLIMITED.
- Submarca recibida: SAHARA.
- Tipo recibido: vacío.
- Top-3 devuelto, en orden: `X000A6|U0008O|B00015`.
- Etapa del fallo: Ranking: el esperado fue recuperado, pero quedó fuera de los tres primeros.
- Posición de recuperación del esperado: 35.0.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 12134.

**Respuesta esperada según la etiqueta: `K0004F`**

- Variante 1: WRANGLER JL UNLIMITED RUBICON 3.6L 5 PUERTAS AUTOMATICA
  Fabricante: CHRYSLER; submodelo: JEEP WRANGLER; tipo: AUTO; segmento: SUV.

Años registrados por código: 2018, 2019, 2020.

**Primera respuesta devuelta: `X000A6`**

- Variante 1: WRANGLER UNLIMITED SAHARA L4 2.0L 270 CP 5 PUERTAS AUT MILD HYBRID
  Fabricante: CHRYSLER; submodelo: JEEP WRANGLER; tipo: AUTO; segmento: SUV.
- Variante 2: WRANGLER UNLIMITED SAHARA L4 2.0L 270 CP 5P AUT MILD HYBRID
  Fabricante: CHRYSLER; submodelo: JEEP WRANGLER; tipo: AUTO; segmento: SUV.

Años registrados por código: 2020, 2021.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.41441068053245544, "vehicle_type": 0.0, "year": 0.12}`

**Investigación propuesta:** Inspeccionar las señales del esperado frente a las alternativas superiores; comprobar si similitud, año o metadatos favorecieron una opción incompatible. No asumir que aumentar el número de candidatos corrige este ordenamiento.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0211 — development — OTHER

**Consulta original:** JETTA

- Año recibido: 2024.
- Marca recibida: JETTA.
- Submarca recibida: vacía.
- Tipo recibido: vacío.
- Top-3 devuelto, en orden: `M0006V|I000D3|K000AO`.
- Etapa del fallo: Recuperación: el código esperado no entró en los 50 candidatos.
- Posición de recuperación del esperado: fuera de los 50.
- Conflictos detectados en top-1: year.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 6390.

**Respuesta esperada según la etiqueta: `S0003P`**

- Variante 1: JETTA A7 COMFORTLINE 1.4T 4 PUERTAS AUTOMATICA
  Fabricante: VOLKSWAGEN; submodelo: JETTA A7; tipo: AUTO; segmento: COMPACTO.

Años registrados por código: 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026.

**Primera respuesta devuelta: `M0006V`**

- Variante 1: JETTA GL AUT.
  Fabricante: VOLKSWAGEN; submodelo: JETTA A2; tipo: AUTO; segmento: COMPACTO.

Años registrados por código: 1989, 1990, 1991, 1992.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.47157740592956543, "vehicle_type": 0.0, "year": -0.2}`

**Investigación propuesta:** Comparar la representación textual del esperado con la consulta; comprobar campos faltantes, vocabulario y posibles reglas de dominio. Modificar solo el ranking no puede rescatar un candidato que no se recuperó.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0216 — development — CAMION

**Consulta original:** T-880 DORMITORIO 52 PULG

- Año recibido: 2019.
- Marca recibida: KENWORTH.
- Submarca recibida: vacía.
- Tipo recibido: CAMION.
- Top-3 devuelto, en orden: `T0003N|G0008A|T0008K`.
- Etapa del fallo: Ranking: el esperado sí está en el top-3, pero otra alternativa quedó primera.
- Posición de recuperación del esperado: 2.0.
- Conflictos detectados en top-1: vehicle_type.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 9844.

**Respuesta esperada según la etiqueta: `G0008A`**

- Variante 1: TR KENWORTH T-880 PACCAR MX 13 500HP DORM 52 18V
  Fabricante: KENWORTH; submodelo: T800; tipo: TRACTO CAMION; segmento: TRACTOCAMION.

Años registrados por código: 2015, 2016, 2017, 2018, 2019, 2020.

**Primera respuesta devuelta: `T0003N`**

- Variante 1: KENWORTH T 880 52 in CUMMINS ISX 450 HP
  Fabricante: KENWORTH; submodelo: T680; tipo: TRACTO CAMION; segmento: TRACTOCAMION.

Años registrados por código: 2015, 2016, 2017, 2018, 2019, 2020, 2021.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.0855, "manufacturer": 0.02, "submodel": 0.0, "tfidf": 0.45688576698303224, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Comparar atributos que distinguen las opciones y comprobar si aparecen en la entrada. Si faltan motor, versión, capacidad o tracción, pedir esa información y mantener revisión.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0226 — development — AUTO

**Consulta original:** RIO SEDAN SD LX

- Año recibido: 2020.
- Marca recibida: KIA.
- Submarca recibida: RIO SEDAN SD LX.
- Tipo recibido: vacío.
- Top-3 devuelto, en orden: `D0003G|I00058|S0002L`.
- Etapa del fallo: Ranking: el esperado sí está en el top-3, pero otra alternativa quedó primera.
- Posición de recuperación del esperado: 3.0.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 1656.

**Respuesta esperada según la etiqueta: `S0002L`**

- Variante 1: RIO LX 1.6L 4 PUERTAS MANUAL
  Fabricante: KIA; submodelo: RIO; tipo: AUTO; segmento: COMPACTO.

Años registrados por código: 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023.

**Primera respuesta devuelta: `D0003G`**

- Variante 1: RIO LX 1.6L 4P AUT
  Fabricante: KIA; submodelo: RIO; tipo: AUTO; segmento: COMPACTO.

Años registrados por código: 2018, 2019, 2020, 2021, 2022, 2023.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.06551724137931034, "manufacturer": 0.02, "submodel": 0.02, "tfidf": 0.515907508134842, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Comparar atributos que distinguen las opciones y comprobar si aparecen en la entrada. Si faltan motor, versión, capacidad o tracción, pedir esa información y mantener revisión.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0237 — development — AUTO

**Consulta original:** LX700h LUXURY

- Año recibido: 2026.
- Marca recibida: LEXUS.
- Submarca recibida: vacía.
- Tipo recibido: AUTOS.
- Top-3 devuelto, en orden: `J000BA|H0006M|R000BM`.
- Etapa del fallo: Ranking: el esperado sí está en el top-3, pero otra alternativa quedó primera.
- Posición de recuperación del esperado: 3.0.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 5018.

**Respuesta esperada según la etiqueta: `H0006M`**

- Variante 1: LEXUS LX 700H LUXURY, V6, 3.5T, 457 CP, 5 PUERTAS, AUT, BA, AA, QC, HEV
  Fabricante: LEXUS; submodelo: LEXUS; tipo: AUTO; segmento: LUJO.

Años registrados por código: 2025, 2026.

**Primera respuesta devuelta: `J000BA`**

- Variante 1: LEXUS NX 350H LUXURY L4 2.5L 5 PTS AUT BA AA HEV
  Fabricante: LEXUS; submodelo: LEXUS; tipo: AUTO; segmento: LUJO.

Años registrados por código: 2023, 2025, 2026.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.0855, "manufacturer": 0.02, "submodel": 0.0, "tfidf": 0.4618657171726227, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Comparar atributos que distinguen las opciones y comprobar si aparecen en la entrada. Si faltan motor, versión, capacidad o tracción, pedir esa información y mantener revisión.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0242 — development — OTHER

**Consulta original:** CARRO ESCALA 106 PIES

- Año recibido: 1985.
- Marca recibida: LTI.
- Submarca recibida: vacía.
- Tipo recibido: vacío.
- Top-3 devuelto, en orden: `I00003|R00092|B0008E`.
- Etapa del fallo: Ranking: el esperado sí está en el top-3, pero otra alternativa quedó primera.
- Posición de recuperación del esperado: 7.0.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 4094.

**Respuesta esperada según la etiqueta: `B0008E`**

- Variante 1: EQ FREIGHTLINER FL-106 52K 6X4 CHASIS CABINA
  Fabricante: FREIGHTLINER; submodelo: FL-106; tipo: CAMION; segmento: CAMION HASTA 14 TONELADAS.

Años registrados por código: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004.

**Primera respuesta devuelta: `I00003`**

- Variante 1: DODGE D-600 CARRO TANQUE
  Fabricante: CHRYSLER; submodelo: D-600 TANQUE; tipo: CAMION; segmento: CAMION DE 9.5 HASTA 12.5 TONELADAS.

Años registrados por código: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.1618940055370331, "vehicle_type": 0.0, "year": 0.12}`

**Investigación propuesta:** Comparar atributos que distinguen las opciones y comprobar si aparecen en la entrada. Si faltan motor, versión, capacidad o tracción, pedir esa información y mantener revisión.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0243 — development — OTHER

**Consulta original:** MARCH ACTIVE HB STD AA CD BA 106HP ABS 1.6L 4CIL 5P 5OCUP 2020

- Año recibido: 2020.
- Marca recibida: MARCH ACTIVE HB STD AA CD BA 106HP ABS 1.6L 4CIL 5P 5OCUP.
- Submarca recibida: vacía.
- Tipo recibido: vacío.
- Top-3 devuelto, en orden: `Z0006S|Z0003Z|T00051`.
- Etapa del fallo: Ranking: el esperado sí está en el top-3, pero otra alternativa quedó primera.
- Posición de recuperación del esperado: 4.0.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 13036.

**Respuesta esperada según la etiqueta: `Z0003Z`**

- Variante 1: NISSAN MARCH ACTIVE, 1.6L, 5 PUERTAS, MANUAL, AC, ABS
  Fabricante: NISSAN; submodelo: MARCH; tipo: AUTO; segmento: SUBCOMPACTO.

Años registrados por código: 2016, 2017, 2018, 2019, 2020.

**Primera respuesta devuelta: `Z0006S`**

- Variante 1: MARCH ACTIVE 1.6L 5 PUERTAS MANUAL AC
  Fabricante: NISSAN; submodelo: MARCH; tipo: AUTO; segmento: SUBCOMPACTO.

Años registrados por código: 2015, 2016, 2017, 2018, 2019, 2020.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.3857463151216507, "vehicle_type": 0.0, "year": 0.12}`

**Investigación propuesta:** Comparar atributos que distinguen las opciones y comprobar si aparecen en la entrada. Si faltan motor, versión, capacidad o tracción, pedir esa información y mantener revisión.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0247 — development — AUTO

**Consulta original:** MAZDA 3I SPORT L4 2.5 SEDAN AUT

- Año recibido: 2021.
- Marca recibida: MAZDA.
- Submarca recibida: vacía.
- Tipo recibido: AUTOMOVIL.
- Top-3 devuelto, en orden: `J0006X|J000BG|K0002W`.
- Etapa del fallo: Ranking: el esperado fue recuperado, pero quedó fuera de los tres primeros.
- Posición de recuperación del esperado: 47.0.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 4858.

**Respuesta esperada según la etiqueta: `A00091`**

- Variante 1: 3 I SPORT 2.5L 4 PUERTAS AUTOMATICA
  Fabricante: MAZDA; submodelo: 3; tipo: AUTO; segmento: COMPACTO.

Años registrados por código: 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026.

**Primera respuesta devuelta: `J0006X`**

- Variante 1: MAZDA CX-5 I SPORT 2.0L L4 AUT 5P ABS CA CE TELA CD CB
  Fabricante: MAZDA; submodelo: CX5; tipo: AUTO; segmento: SUV.

Años registrados por código: 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.0855, "manufacturer": 0.02, "submodel": 0.0, "tfidf": 0.3158358782529831, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Inspeccionar las señales del esperado frente a las alternativas superiores; comprobar si similitud, año o metadatos favorecieron una opción incompatible. No asumir que aumentar el número de candidatos corrige este ordenamiento.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0248 — development — AUTO

**Consulta original:** MAZDA 3i AUT 4 PTAS C/A.AC

- Año recibido: 2010.
- Marca recibida: MAZDA.
- Submarca recibida: vacía.
- Tipo recibido: AUTOMOVIL.
- Top-3 devuelto, en orden: `W0004G|W000AJ|E0000K`.
- Etapa del fallo: Recuperación: el código esperado no entró en los 50 candidatos.
- Posición de recuperación del esperado: fuera de los 50.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 11410.

**Respuesta esperada según la etiqueta: `Z00061`**

- Variante 1: 3 SEDAN SPORT 4P AUT., 05 OCUP
  Fabricante: MAZDA; submodelo: 3; tipo: AUTO; segmento: COMPACTO.

Años registrados por código: 2010, 2011, 2012, 2013, 2014, 2015.

**Primera respuesta devuelta: `W0004G`**

- Variante 1: MAZDA 3 I 2.0L L4 AUT 4P D/V CA SE TELA CD SQ CB
  Fabricante: MAZDA; submodelo: 3; tipo: AUTO; segmento: COMPACTO.

Años registrados por código: 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.0855, "manufacturer": 0.02, "submodel": 0.0, "tfidf": 0.302870911359787, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Comparar la representación textual del esperado con la consulta; comprobar campos faltantes, vocabulario y posibles reglas de dominio. Modificar solo el ranking no puede rescatar un candidato que no se recuperó.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0250 — development — AUTO

**Consulta original:** CLASE C 300 SPORT AUT

- Año recibido: 2020.
- Marca recibida: MBENZ.
- Submarca recibida: vacía.
- Tipo recibido: AUTOMOVIL.
- Top-3 devuelto, en orden: `P0002D|J000BQ|Z000DY`.
- Etapa del fallo: Ranking: el esperado fue recuperado, pero quedó fuera de los tres primeros.
- Posición de recuperación del esperado: 24.0.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 7752.

**Respuesta esperada según la etiqueta: `G00080`**

- Variante 1: CGI SPORT 2.0T 4 PUERTAS AUTOMATICA
  Fabricante: MERCEDES BENZ; submodelo: CLASE C; tipo: AUTO; segmento: LUJO.

Años registrados por código: 2020.

**Primera respuesta devuelta: `P0002D`**

- Variante 1: CLASE C 300 CGI COUPE 2.0T 2 PUERTAS AUTOMATICA
  Fabricante: MERCEDES BENZ; submodelo: CLASE C; tipo: AUTO; segmento: LUJO.

Años registrados por código: 2019, 2020, 2021.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.36737685799598696, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Inspeccionar las señales del esperado frente a las alternativas superiores; comprobar si similitud, año o metadatos favorecieron una opción incompatible. No asumir que aumentar el número de candidatos corrige este ordenamiento.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0264 — development — OTHER

**Consulta original:** COOPER S HOT CHILI

- Año recibido: 2007.
- Marca recibida: MINI.
- Submarca recibida: COOPER S HOT CHILI.
- Tipo recibido: vacío.
- Top-3 devuelto, en orden: `Q0004F|K00011|Z000DZ`.
- Etapa del fallo: Ranking: el esperado sí está en el top-3, pero otra alternativa quedó primera.
- Posición de recuperación del esperado: 10.0.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 8341.

**Respuesta esperada según la etiqueta: `Z000DZ`**

- Variante 1: MINI COOPER S HOT CHILI 1.6L 163HP L4 STD 2P PIEL CA CE
  Fabricante: BMW; submodelo: MINI COOPER; tipo: AUTO; segmento: LUJO.

Años registrados por código: 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014.

**Primera respuesta devuelta: `Q0004F`**

- Variante 1: MINI COOPER S HOT CHILI L4 AUT 2P CA CE PIEL CD CQ CB
  Fabricante: BMW; submodelo: MINI COOPER; tipo: AUTO; segmento: LUJO.

Años registrados por código: 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.6758727908134461, "vehicle_type": 0.0, "year": 0.12}`

**Investigación propuesta:** Comparar atributos que distinguen las opciones y comprobar si aparecen en la entrada. Si faltan motor, versión, capacidad o tracción, pedir esa información y mantener revisión.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0267 — development — REMOLQUE

**Consulta original:** TOLVA

- Año recibido: 2016.
- Marca recibida: MIRELES.
- Submarca recibida: vacía.
- Tipo recibido: TOLVA.
- Top-3 devuelto, en orden: `Z0005P|L0008A|U0007D`.
- Etapa del fallo: Recuperación: el código esperado no entró en los 50 candidatos.
- Posición de recuperación del esperado: fuera de los 50.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 12996.

**Respuesta esperada según la etiqueta: `Z0000M`**

- Variante 1: RM CAJA CERRADA 2 EJES 40
  Fabricante: SEMIRREMOLQUES; submodelo: CAJA SECA; tipo: SEMIREMOLQUE; segmento: SEMIREMOLQUE.

Años registrados por código: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.

**Primera respuesta devuelta: `Z0005P`**

- Variante 1: TOLVA CEMENTERA.
  Fabricante: SEMIRREMOLQUES; submodelo: TOLVA CEMENTERA; tipo: SEMIREMOLQUE; segmento: SEMIREMOLQUE.

Años registrados por código: 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.39190560579299927, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Comparar la representación textual del esperado con la consulta; comprobar campos faltantes, vocabulario y posibles reglas de dominio. Modificar solo el ranking no puede rescatar un candidato que no se recuperó.

**Pregunta adicional al experto:** este código se repite en 33 etiquetas y describe
una caja cerrada. Confirmar si existe una regla genérica de negocio que explique su
uso en consultas diferentes. No añadirlo como fallback ni corregir la etiqueta por suposición.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0268 — development — CAMION

**Consulta original:** HILUX DOBLE CABINA BASE STD 4P 4CIL

- Año recibido: 2023.
- Marca recibida: MITSUBICHI.
- Submarca recibida: vacía.
- Tipo recibido: CAMION.
- Top-3 devuelto, en orden: `Z0004B|F0008T|Z000BV`.
- Etapa del fallo: Ranking: el esperado sí está en el top-3, pero otra alternativa quedó primera.
- Posición de recuperación del esperado: 7.0.
- Conflictos detectados en top-1: manufacturer|vehicle_type.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 12946.

**Respuesta esperada según la etiqueta: `Z000BV`**

- Variante 1: HILUX CABINA DOBLE 2.7L L4 STD 4P CA CE CB
  Fabricante: TOYOTA; submodelo: HILUX PICK UP; tipo: PICK UP; segmento: PICK UP.

Años registrados por código: 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024.

**Primera respuesta devuelta: `Z0004B`**

- Variante 1: HILUX DOBLE CABINA DIESEL 2.8L 4P STD
  Fabricante: TOYOTA; submodelo: HILUX PICK UP; tipo: PICK UP; segmento: PICK UP.

Años registrados por código: 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.06690140845070423, "manufacturer": -0.1, "submodel": 0.0, "tfidf": 0.3762846350669861, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Comparar atributos que distinguen las opciones y comprobar si aparecen en la entrada. Si faltan motor, versión, capacidad o tracción, pedir esa información y mantener revisión.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0269 — development — CAMION

**Consulta original:** L200 GLX DIESEL STD 4P 4CIL 2.4L 4WD

- Año recibido: 2023.
- Marca recibida: MITSUBICHI.
- Submarca recibida: vacía.
- Tipo recibido: CAMION.
- Top-3 devuelto, en orden: `T0001C|L0006M|S0002A`.
- Etapa del fallo: Ranking: el esperado sí está en el top-3, pero otra alternativa quedó primera.
- Posición de recuperación del esperado: 6.0.
- Conflictos detectados en top-1: vehicle_type.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 9760.

**Respuesta esperada según la etiqueta: `S0002A`**

- Variante 1: MITSUBISHI L200 GLX L4 178 CP DSL 4 PTS STD
  Fabricante: MITSUBISHI; submodelo: L200; tipo: PICK UP; segmento: PICK UP LUJO.

Años registrados por código: 2022, 2023, 2024, 2025.

**Primera respuesta devuelta: `T0001C`**

- Variante 1: MITSUBISHI L200 GLX L4 126 CP 4 PTS STD
  Fabricante: MITSUBISHI; submodelo: L200; tipo: PICK UP; segmento: PICK UP LUJO.

Años registrados por código: 2022, 2023, 2024, 2025, 2026.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.06627906976744186, "manufacturer": 0.02, "submodel": 0.0, "tfidf": 0.336882421374321, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Comparar atributos que distinguen las opciones y comprobar si aparecen en la entrada. Si faltan motor, versión, capacidad o tracción, pedir esa información y mantener revisión.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0270 — development — CAMION

**Consulta original:** L200 GLX DIESEL STD 4P 4CIL 2.4L 4WD

- Año recibido: 2024.
- Marca recibida: MITSUBICHI.
- Submarca recibida: vacía.
- Tipo recibido: CAMION.
- Top-3 devuelto, en orden: `T0001C|L0006M|S0002A`.
- Etapa del fallo: Ranking: el esperado sí está en el top-3, pero otra alternativa quedó primera.
- Posición de recuperación del esperado: 6.0.
- Conflictos detectados en top-1: vehicle_type.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 9760.

**Respuesta esperada según la etiqueta: `S0002A`**

- Variante 1: MITSUBISHI L200 GLX L4 178 CP DSL 4 PTS STD
  Fabricante: MITSUBISHI; submodelo: L200; tipo: PICK UP; segmento: PICK UP LUJO.

Años registrados por código: 2022, 2023, 2024, 2025.

**Primera respuesta devuelta: `T0001C`**

- Variante 1: MITSUBISHI L200 GLX L4 126 CP 4 PTS STD
  Fabricante: MITSUBISHI; submodelo: L200; tipo: PICK UP; segmento: PICK UP LUJO.

Años registrados por código: 2022, 2023, 2024, 2025, 2026.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.06627906976744186, "manufacturer": 0.02, "submodel": 0.0, "tfidf": 0.336882421374321, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Comparar atributos que distinguen las opciones y comprobar si aparecen en la entrada. Si faltan motor, versión, capacidad o tracción, pedir esa información y mantener revisión.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0273 — development — AUTO

**Consulta original:** MITSUBISHI MIRAGE GLX L3 1.2 AUT

- Año recibido: 2017.
- Marca recibida: MITSUBISHI.
- Submarca recibida: vacía.
- Tipo recibido: AUTOMOVIL.
- Top-3 devuelto, en orden: `W000DT|V00022|F000BX`.
- Etapa del fallo: Ranking: el esperado sí está en el top-3, pero otra alternativa quedó primera.
- Posición de recuperación del esperado: 4.0.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 11753.

**Respuesta esperada según la etiqueta: `V00022`**

- Variante 1: MIRAGE GLX 1.2L 5 PUERTAS CVT
  Fabricante: MITSUBISHI; submodelo: MIRAGE; tipo: AUTO; segmento: SUBCOMPACTO.
- Variante 2: MIRAGE GLX 1.2L L3 AUT CVT 5P CA CE CB
  Fabricante: MITSUBISHI; submodelo: MIRAGE; tipo: AUTO; segmento: SUBCOMPACTO.

Años registrados por código: 2015, 2016, 2017, 2018, 2019, 2020.

**Primera respuesta devuelta: `W000DT`**

- Variante 1: MIRAGE GLX 1.2L 5 PUERTAS MANUAL
  Fabricante: MITSUBISHI; submodelo: MIRAGE; tipo: AUTO; segmento: SUBCOMPACTO.
- Variante 2: MIRAGE GLX 1.2L L3 STD 5P CA CE CB
  Fabricante: MITSUBISHI; submodelo: MIRAGE; tipo: AUTO; segmento: SUBCOMPACTO.

Años registrados por código: 2015, 2016, 2017, 2018, 2019, 2020.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.08142857142857142, "manufacturer": 0.02, "submodel": 0.0, "tfidf": 0.5564435184001922, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Comparar atributos que distinguen las opciones y comprobar si aparecen en la entrada. Si faltan motor, versión, capacidad o tracción, pedir esa información y mantener revisión.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0274 — development — PICKUP

**Consulta original:** PICK UP L200 GLX DOBLE CAB 4WD L4 TDI STD 4 ABS CA CE TELA SM

- Año recibido: 2023.
- Marca recibida: MITSUBISHI.
- Submarca recibida: PICK UP L200 GLX DOBLE CAB 4WD STD.
- Tipo recibido: vacío.
- Top-3 devuelto, en orden: `T0001C|S0002A|L0006M`.
- Etapa del fallo: Ranking: el esperado sí está en el top-3, pero otra alternativa quedó primera.
- Posición de recuperación del esperado: 3.0.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 9760.

**Respuesta esperada según la etiqueta: `S0002A`**

- Variante 1: MITSUBISHI L200 GLX L4 178 CP DSL 4 PTS STD
  Fabricante: MITSUBISHI; submodelo: L200; tipo: PICK UP; segmento: PICK UP LUJO.

Años registrados por código: 2022, 2023, 2024, 2025.

**Primera respuesta devuelta: `T0001C`**

- Variante 1: MITSUBISHI L200 GLX L4 126 CP 4 PTS STD
  Fabricante: MITSUBISHI; submodelo: L200; tipo: PICK UP; segmento: PICK UP LUJO.

Años registrados por código: 2022, 2023, 2024, 2025, 2026.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.0855, "manufacturer": 0.02, "submodel": 0.02, "tfidf": 0.3924002319574356, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Comparar atributos que distinguen las opciones y comprobar si aparecen en la entrada. Si faltan motor, versión, capacidad o tracción, pedir esa información y mantener revisión.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0277 — development — CAMION

**Consulta original:** INTERNATIONAL 4700 COMPACTADOR INTERNACIONAL

- Año recibido: 2002.
- Marca recibida: NAV INT CORP.
- Submarca recibida: COMPACTADOR INTERNACIONAL.
- Tipo recibido: CAMION.
- Top-3 devuelto, en orden: `P0006M|K000A4|P0005X`.
- Etapa del fallo: Ranking: el esperado sí está en el top-3, pero otra alternativa quedó primera.
- Posición de recuperación del esperado: 2.0.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 7911.

**Respuesta esperada según la etiqueta: `K000A4`**

- Variante 1: INTERNACIONAL 4700 CHASIS CABINA 4 X 2 NAVISTAR DT 466 E 190HP 15.4 TON
  Fabricante: INTERNATIONAL; submodelo: 4700 MAS DE 14 TON; tipo: CAMION; segmento: CAMION HASTA 14 TONELADAS.

Años registrados por código: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2014.

**Primera respuesta devuelta: `P0006M`**

- Variante 1: INTERNACIONAL 4700 CHASIS CABINA 4 X 2 DT 466 E 175HP 15.4 TON
  Fabricante: INTERNATIONAL; submodelo: 4700 MAS DE 14 TON; tipo: CAMION; segmento: CAMION HASTA 14 TONELADAS.

Años registrados por código: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.06831460674157303, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.3265778303146362, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Comparar atributos que distinguen las opciones y comprobar si aparecen en la entrada. Si faltan motor, versión, capacidad o tracción, pedir esa información y mantener revisión.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0290 — development — OTHER

**Consulta original:** COCHE GRIS OXFORD SEDAM ADVANCE MT

- Año recibido: 2013.
- Marca recibida: NISSAN SEDAN.
- Submarca recibida: vacía.
- Tipo recibido: vacío.
- Top-3 devuelto, en orden: `Z000AH|Q0007J|V0001D`.
- Etapa del fallo: Ranking: el esperado sí está en el top-3, pero otra alternativa quedó primera.
- Posición de recuperación del esperado: 4.0.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 13171.

**Respuesta esperada según la etiqueta: `Q0007J`**

- Variante 1: SENTRA ADVANCE 1.8L L4 STD 4P CA CE TELA CD CB
  Fabricante: NISSAN; submodelo: SENTRA; tipo: AUTO; segmento: COMPACTO.

Años registrados por código: 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023.

**Primera respuesta devuelta: `Z000AH`**

- Variante 1: MARCH ADVANCE L4 STD 5P CA CE TELA CD CB
  Fabricante: NISSAN; submodelo: MARCH; tipo: AUTO; segmento: SUBCOMPACTO.

Años registrados por código: 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.05659574468085107, "manufacturer": 0.02, "submodel": 0.0, "tfidf": 0.16150036454200745, "vehicle_type": 0.0, "year": 0.12}`

**Investigación propuesta:** Comparar atributos que distinguen las opciones y comprobar si aparecen en la entrada. Si faltan motor, versión, capacidad o tracción, pedir esa información y mantener revisión.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0295 — development — PICKUP

**Consulta original:** PEUGEOT PARTNER MAXI PACK STD DIESEL

- Año recibido: 2025.
- Marca recibida: PEUGEOT.
- Submarca recibida: vacía.
- Tipo recibido: PICKUP CARGA.
- Top-3 devuelto, en orden: `U0005Y|B000AH|E0006Y`.
- Etapa del fallo: Ranking: el esperado sí está en el top-3, pero otra alternativa quedó primera.
- Posición de recuperación del esperado: 3.0.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 10439.

**Respuesta esperada según la etiqueta: `B000AH`**

- Variante 1: PARTNER MAXI PACK L4 1.6T 90 CP 5 PUERTAS STD BA AA FL DIESEL
  Fabricante: PEUGEOT; submodelo: PARTNER MAXI; tipo: PICK UP; segmento: VAN CARGA.

Años registrados por código: 2025.

**Primera respuesta devuelta: `U0005Y`**

- Variante 1: PARTNER MAXI PACK 1.6T 5 PUERTAS MANUAL
  Fabricante: PEUGEOT; submodelo: PARTNER MAXI; tipo: PICK UP; segmento: VAN CARGA.

Años registrados por código: 2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.0778688524590164, "manufacturer": 0.02, "submodel": 0.0, "tfidf": 0.629653126001358, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Comparar atributos que distinguen las opciones y comprobar si aparecen en la entrada. Si faltan motor, versión, capacidad o tracción, pedir esa información y mantener revisión.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0316 — development — REMOLQUE

**Consulta original:** REMOLQUE

- Año recibido: 1991.
- Marca recibida: REMOLQUES.
- Submarca recibida: REMOLQUE.
- Tipo recibido: vacío.
- Top-3 devuelto, en orden: `G00060|E0009F|H000D3`.
- Etapa del fallo: Ranking: el esperado fue recuperado, pero quedó fuera de los tres primeros.
- Posición de recuperación del esperado: 43.0.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 3288.

**Respuesta esperada según la etiqueta: `Z0000M`**

- Variante 1: RM CAJA CERRADA 2 EJES 40
  Fabricante: SEMIRREMOLQUES; submodelo: CAJA SECA; tipo: SEMIREMOLQUE; segmento: SEMIREMOLQUE.

Años registrados por código: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.

**Primera respuesta devuelta: `G00060`**

- Variante 1: REMOLQUE TIPO TANQUE 30000 LTS.
  Fabricante: SEMIRREMOLQUES; submodelo: TANQUE; tipo: SEMIREMOLQUE; segmento: SEMIREMOLQUE.

Años registrados por código: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.35425066351890566, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Inspeccionar las señales del esperado frente a las alternativas superiores; comprobar si similitud, año o metadatos favorecieron una opción incompatible. No asumir que aumentar el número de candidatos corrige este ordenamiento.

**Pregunta adicional al experto:** este código se repite en 33 etiquetas y describe
una caja cerrada. Confirmar si existe una regla genérica de negocio que explique su
uso en consultas diferentes. No añadirlo como fallback ni corregir la etiqueta por suposición.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0318 — development — PICKUP

**Consulta original:** RENAULT RENAULT KANGOO EXPRESS CON AA CD BA STD VAN 4 CIL 4P

- Año recibido: 2015.
- Marca recibida: RENAULT.
- Submarca recibida: vacía.
- Tipo recibido: PICKUP CARGA.
- Top-3 devuelto, en orden: `U0007N|M0001Y|Z000DX`.
- Etapa del fallo: Ranking: el esperado sí está en el top-3, pero otra alternativa quedó primera.
- Posición de recuperación del esperado: 4.0.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 10500.

**Respuesta esperada según la etiqueta: `M0001Y`**

- Variante 1: KANGOO EXPRESS 1.6L C/A AC STD., 02 OCUP.
  Fabricante: RENAULT; submodelo: KANGOO VAN; tipo: PICK UP; segmento: VAN CARGA.

Años registrados por código: 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015.

**Primera respuesta devuelta: `U0007N`**

- Variante 1: RENAULT KANGOO EXPRESS. L4 D/H C/B
  Fabricante: RENAULT; submodelo: KANGOO VAN; tipo: PICK UP; segmento: VAN CARGA.

Años registrados por código: 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2017.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.07841269841269843, "manufacturer": 0.02, "submodel": 0.0, "tfidf": 0.5286436557769776, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Comparar atributos que distinguen las opciones y comprobar si aparecen en la entrada. Si faltan motor, versión, capacidad o tracción, pedir esa información y mantener revisión.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0324 — development — REMOLQUE

**Consulta original:** REMOLQUE

- Año recibido: 2000.
- Marca recibida: S/M.
- Submarca recibida: REMOLQUE.
- Tipo recibido: vacío.
- Top-3 devuelto, en orden: `G00060|E0009F|H000D3`.
- Etapa del fallo: Ranking: el esperado fue recuperado, pero quedó fuera de los tres primeros.
- Posición de recuperación del esperado: 50.0.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 3288.

**Respuesta esperada según la etiqueta: `Z0000M`**

- Variante 1: RM CAJA CERRADA 2 EJES 40
  Fabricante: SEMIRREMOLQUES; submodelo: CAJA SECA; tipo: SEMIREMOLQUE; segmento: SEMIREMOLQUE.

Años registrados por código: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.

**Primera respuesta devuelta: `G00060`**

- Variante 1: REMOLQUE TIPO TANQUE 30000 LTS.
  Fabricante: SEMIRREMOLQUES; submodelo: TANQUE; tipo: SEMIREMOLQUE; segmento: SEMIREMOLQUE.

Años registrados por código: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.3303191900253296, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Inspeccionar las señales del esperado frente a las alternativas superiores; comprobar si similitud, año o metadatos favorecieron una opción incompatible. No asumir que aumentar el número de candidatos corrige este ordenamiento.

**Pregunta adicional al experto:** este código se repite en 33 etiquetas y describe
una caja cerrada. Confirmar si existe una regla genérica de negocio que explique su
uso en consultas diferentes. No añadirlo como fallback ni corregir la etiqueta por suposición.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0340 — development — AUTO

**Consulta original:** SUZUKI SWIFT SPORT GLE 1.4 AUT

- Año recibido: 2022.
- Marca recibida: SUZUKI.
- Submarca recibida: vacía.
- Tipo recibido: AUTOMOVIL.
- Top-3 devuelto, en orden: `H0000H|M0000Q|T00074`.
- Etapa del fallo: Ranking: el esperado fue recuperado, pero quedó fuera de los tres primeros.
- Posición de recuperación del esperado: 13.0.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 3600.

**Respuesta esperada según la etiqueta: `S0001Y`**

- Variante 1: SWIFT GLE SPORT BOOSTERJET L4 1.4L 5 PTS AUT
  Fabricante: SUZUKI; submodelo: SWIFT; tipo: AUTO; segmento: SUBCOMPACTO.

Años registrados por código: 2022.

**Primera respuesta devuelta: `H0000H`**

- Variante 1: SUZUKI SWIFT GLE L4 1.2L 5 PTS AUT
  Fabricante: SUZUKI; submodelo: SWIFT; tipo: AUTO; segmento: SUBCOMPACTO.

Años registrados por código: 2022.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.08015625, "manufacturer": 0.02, "submodel": 0.0, "tfidf": 0.564158570766449, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Inspeccionar las señales del esperado frente a las alternativas superiores; comprobar si similitud, año o metadatos favorecieron una opción incompatible. No asumir que aumentar el número de candidatos corrige este ordenamiento.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0341 — development — AUTO

**Consulta original:** SWIFT HB GLS 5P L4 1.2T ABS BA AC R16 STD.

- Año recibido: 2021.
- Marca recibida: SUZUKI.
- Submarca recibida: vacía.
- Tipo recibido: AUTOMOVIL.
- Top-3 devuelto, en orden: `G000A3|T00074|F0004U`.
- Etapa del fallo: Ranking: el esperado sí está en el top-3, pero otra alternativa quedó primera.
- Posición de recuperación del esperado: 4.0.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 3436.

**Respuesta esperada según la etiqueta: `F0004U`**

- Variante 1: SWIFT GLS 1.2L 5 PUERTAS MANUAL
  Fabricante: SUZUKI; submodelo: SWIFT; tipo: AUTO; segmento: SUBCOMPACTO.

Años registrados por código: 2018, 2019, 2020, 2021, 2022, 2023, 2024.

**Primera respuesta devuelta: `G000A3`**

- Variante 1: ERTIGA GLS 5P L4 1.5T ABS BA AC STD 07 OCUP
  Fabricante: SUZUKI; submodelo: ERTIGA; tipo: AUTO; segmento: VAN/MINIVAN.

Años registrados por código: 2019, 2020, 2021, 2022, 2023, 2024.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.07307692307692307, "manufacturer": 0.02, "submodel": 0.0, "tfidf": 0.3261412471532822, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Comparar atributos que distinguen las opciones y comprobar si aparecen en la entrada. Si faltan motor, versión, capacidad o tracción, pedir esa información y mantener revisión.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0350 — development — PICKUP

**Consulta original:** HILUX DOBLE CABINA

- Año recibido: 2024.
- Marca recibida: TOYOYA.
- Submarca recibida: vacía.
- Tipo recibido: vacío.
- Top-3 devuelto, en orden: `F0008T|Z0004B|H000C0`.
- Etapa del fallo: Ranking: el esperado fue recuperado, pero quedó fuera de los tres primeros.
- Posición de recuperación del esperado: 7.0.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 2876.

**Respuesta esperada según la etiqueta: `Z000BV`**

- Variante 1: HILUX CABINA DOBLE 2.7L L4 STD 4P CA CE CB
  Fabricante: TOYOTA; submodelo: HILUX PICK UP; tipo: PICK UP; segmento: PICK UP.

Años registrados por código: 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024.

**Primera respuesta devuelta: `F0008T`**

- Variante 1: HILUX DOBLE CABINA DIESEL 2.8L 4P AUT
  Fabricante: TOYOTA; submodelo: HILUX PICK UP; tipo: PICK UP; segmento: PICK UP.

Años registrados por código: 2018, 2019, 2020, 2021, 2022, 2023, 2024.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.5719518899917603, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Inspeccionar las señales del esperado frente a las alternativas superiores; comprobar si similitud, año o metadatos favorecieron una opción incompatible. No asumir que aumentar el número de candidatos corrige este ordenamiento.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0352 — development — TRACTO

**Consulta original:** TR CAMION LEGALIZADO TIPO TRACTOCAMION. STD

- Año recibido: 2010.
- Marca recibida: TRACTO.
- Submarca recibida: vacía.
- Tipo recibido: TRACTO.
- Top-3 devuelto, en orden: `O0003Q|C000DF|E0006A`.
- Etapa del fallo: Recuperación: el código esperado no entró en los 50 candidatos.
- Posición de recuperación del esperado: fuera de los 50.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 7290.

**Respuesta esperada según la etiqueta: `E0005R`**

- Variante 1: TR MAN TGS 39S 41.440 8X4
  Fabricante: MAN; submodelo: TGS TRACTOCAMION; tipo: TRACTO CAMION; segmento: TRACTOCAMION.

Años registrados por código: 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016.

**Primera respuesta devuelta: `O0003Q`**

- Variante 1: TRACTOCAMION MACK
  Fabricante: MACK; submodelo: MACK TRACTOCAMION; tipo: TRACTO CAMION; segmento: TRACTOCAMION.

Años registrados por código: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.07862068965517242, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.24313146471977234, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Comparar la representación textual del esperado con la consulta; comprobar campos faltantes, vocabulario y posibles reglas de dominio. Modificar solo el ranking no puede rescatar un candidato que no se recuperó.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0354 — development — TRACTO

**Consulta original:** KENWORTH T 680

- Año recibido: 2025.
- Marca recibida: TRACTO CAMION.
- Submarca recibida: vacía.
- Tipo recibido: TRACTO.
- Top-3 devuelto, en orden: `Y000AG|J0004N|K0009L`.
- Etapa del fallo: Ranking: el esperado sí está en el top-3, pero otra alternativa quedó primera.
- Posición de recuperación del esperado: 33.0.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 12659.

**Respuesta esperada según la etiqueta: `K0009L`**

- Variante 1: KENWORTH T680 TRACTOCAMION KENWORTH NUEVA GENERACION
  Fabricante: KENWORTH; submodelo: T680; tipo: TRACTO CAMION; segmento: TRACTOCAMION.

Años registrados por código: 2025.

**Primera respuesta devuelta: `Y000AG`**

- Variante 1: TRACTOCAMION KENWORTH T 680 52 in CUMMINS ISX 450 HP
  Fabricante: KENWORTH; submodelo: T680; tipo: TRACTO CAMION; segmento: TRACTOCAMION.

Años registrados por código: 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.08666666666666667, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.4228265404701233, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Comparar atributos que distinguen las opciones y comprobar si aparecen en la entrada. Si faltan motor, versión, capacidad o tracción, pedir esa información y mantener revisión.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0355 — development — TRACTO

**Consulta original:** TR CAMION LEGALIZADO TIPO TRACTOCAMION. STD.

- Año recibido: 2010.
- Marca recibida: TRACTO CAMION.
- Submarca recibida: vacía.
- Tipo recibido: TRACTO.
- Top-3 devuelto, en orden: `O0003Q|C000DF|E0006A`.
- Etapa del fallo: Ranking: el esperado fue recuperado, pero quedó fuera de los tres primeros.
- Posición de recuperación del esperado: 50.0.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 7290.

**Respuesta esperada según la etiqueta: `T0004H`**

- Variante 1: TR MAN TGA 26.430
  Fabricante: MAN; submodelo: TGA TRACTOCAMION; tipo: TRACTO CAMION; segmento: TRACTOCAMION.

Años registrados por código: 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016.

**Primera respuesta devuelta: `O0003Q`**

- Variante 1: TRACTOCAMION MACK
  Fabricante: MACK; submodelo: MACK TRACTOCAMION; tipo: TRACTO CAMION; segmento: TRACTOCAMION.

Años registrados por código: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.07862068965517242, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.23458364009857177, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Inspeccionar las señales del esperado frente a las alternativas superiores; comprobar si similitud, año o metadatos favorecieron una opción incompatible. No asumir que aumentar el número de candidatos corrige este ordenamiento.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0358 — development — REMOLQUE

**Consulta original:** TOLVA

- Año recibido: 2018.
- Marca recibida: TYRSOL.
- Submarca recibida: vacía.
- Tipo recibido: TOLVA.
- Top-3 devuelto, en orden: `Z0005P|Z0003K|R0002X`.
- Etapa del fallo: Recuperación: el código esperado no entró en los 50 candidatos.
- Posición de recuperación del esperado: fuera de los 50.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 12996.

**Respuesta esperada según la etiqueta: `Z0000M`**

- Variante 1: RM CAJA CERRADA 2 EJES 40
  Fabricante: SEMIRREMOLQUES; submodelo: CAJA SECA; tipo: SEMIREMOLQUE; segmento: SEMIREMOLQUE.

Años registrados por código: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.

**Primera respuesta devuelta: `Z0005P`**

- Variante 1: TOLVA CEMENTERA.
  Fabricante: SEMIRREMOLQUES; submodelo: TOLVA CEMENTERA; tipo: SEMIREMOLQUE; segmento: SEMIREMOLQUE.

Años registrados por código: 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.40210620760917665, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Comparar la representación textual del esperado con la consulta; comprobar campos faltantes, vocabulario y posibles reglas de dominio. Modificar solo el ranking no puede rescatar un candidato que no se recuperó.

**Pregunta adicional al experto:** este código se repite en 33 etiquetas y describe
una caja cerrada. Confirmar si existe una regla genérica de negocio que explique su
uso en consultas diferentes. No añadirlo como fallback ni corregir la etiqueta por suposición.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0359 — development — REMOLQUE

**Consulta original:** TOLVA

- Año recibido: 2017.
- Marca recibida: TYRSOL.
- Submarca recibida: vacía.
- Tipo recibido: TOLVA.
- Top-3 devuelto, en orden: `Z0005P|Y0001Z|Z0003K`.
- Etapa del fallo: Recuperación: el código esperado no entró en los 50 candidatos.
- Posición de recuperación del esperado: fuera de los 50.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 12996.

**Respuesta esperada según la etiqueta: `Z0000M`**

- Variante 1: RM CAJA CERRADA 2 EJES 40
  Fabricante: SEMIRREMOLQUES; submodelo: CAJA SECA; tipo: SEMIREMOLQUE; segmento: SEMIREMOLQUE.

Años registrados por código: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.

**Primera respuesta devuelta: `Z0005P`**

- Variante 1: TOLVA CEMENTERA.
  Fabricante: SEMIRREMOLQUES; submodelo: TOLVA CEMENTERA; tipo: SEMIREMOLQUE; segmento: SEMIREMOLQUE.

Años registrados por código: 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.40210620760917665, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Comparar la representación textual del esperado con la consulta; comprobar campos faltantes, vocabulario y posibles reglas de dominio. Modificar solo el ranking no puede rescatar un candidato que no se recuperó.

**Pregunta adicional al experto:** este código se repite en 33 etiquetas y describe
una caja cerrada. Confirmar si existe una regla genérica de negocio que explique su
uso en consultas diferentes. No añadirlo como fallback ni corregir la etiqueta por suposición.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0361 — development — OTHER

**Consulta original:** VENTURE EXT

- Año recibido: 1998.
- Marca recibida: VENTURE.
- Submarca recibida: VENTURE EXT.
- Tipo recibido: vacío.
- Top-3 devuelto, en orden: `M0000S|U0001I|J00063`.
- Etapa del fallo: Ranking: el esperado sí está en el top-3, pero otra alternativa quedó primera.
- Posición de recuperación del esperado: 2.0.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 6168.

**Respuesta esperada según la etiqueta: `U0001I`**

- Variante 1: VENTURE VAN LT V6 AUT 5P CA CE PIEL CD CB
  Fabricante: GENERAL MOTORS; submodelo: VENTURE; tipo: AUTO; segmento: VAN/MINIVAN.

Años registrados por código: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003.

**Primera respuesta devuelta: `M0000S`**

- Variante 1: VENTURE LS V6 AUT 5P ABS CA CE TELA CD SQ CB
  Fabricante: GENERAL MOTORS; submodelo: VENTURE; tipo: AUTO; segmento: VAN/MINIVAN.

Años registrados por código: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.02, "tfidf": 0.5289071023464204, "vehicle_type": 0.0, "year": 0.12}`

**Investigación propuesta:** Comparar atributos que distinguen las opciones y comprobar si aparecen en la entrada. Si faltan motor, versión, capacidad o tracción, pedir esa información y mantener revisión.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0369 — development — REMOLQUE

**Consulta original:** TOLVA

- Año recibido: 2015.
- Marca recibida: VISUSA.
- Submarca recibida: vacía.
- Tipo recibido: TOLVA.
- Top-3 devuelto, en orden: `Z0005P|L0008A|U0007D`.
- Etapa del fallo: Recuperación: el código esperado no entró en los 50 candidatos.
- Posición de recuperación del esperado: fuera de los 50.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 12996.

**Respuesta esperada según la etiqueta: `Z0000M`**

- Variante 1: RM CAJA CERRADA 2 EJES 40
  Fabricante: SEMIRREMOLQUES; submodelo: CAJA SECA; tipo: SEMIREMOLQUE; segmento: SEMIREMOLQUE.

Años registrados por código: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.

**Primera respuesta devuelta: `Z0005P`**

- Variante 1: TOLVA CEMENTERA.
  Fabricante: SEMIRREMOLQUES; submodelo: TOLVA CEMENTERA; tipo: SEMIREMOLQUE; segmento: SEMIREMOLQUE.

Años registrados por código: 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.3996225893497467, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Comparar la representación textual del esperado con la consulta; comprobar campos faltantes, vocabulario y posibles reglas de dominio. Modificar solo el ranking no puede rescatar un candidato que no se recuperó.

**Pregunta adicional al experto:** este código se repite en 33 etiquetas y describe
una caja cerrada. Confirmar si existe una regla genérica de negocio que explique su
uso en consultas diferentes. No añadirlo como fallback ni corregir la etiqueta por suposición.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.

### q0370 — development — REMOLQUE

**Consulta original:** TOLVA

- Año recibido: 2013.
- Marca recibida: VISUSA.
- Submarca recibida: vacía.
- Tipo recibido: TOLVA.
- Top-3 devuelto, en orden: `Z0005P|L0008A|U0007D`.
- Etapa del fallo: Recuperación: el código esperado no entró en los 50 candidatos.
- Posición de recuperación del esperado: fuera de los 50.
- Conflictos detectados en top-1: ninguno reconocido; esto no garantiza compatibilidad.
- Catálogo ambiguo para top-1: no según fabricante/submodelo/tipo.
- Registro del catálogo usado por el top-1: 12996.

**Respuesta esperada según la etiqueta: `Z0000M`**

- Variante 1: RM CAJA CERRADA 2 EJES 40
  Fabricante: SEMIRREMOLQUES; submodelo: CAJA SECA; tipo: SEMIREMOLQUE; segmento: SEMIREMOLQUE.

Años registrados por código: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.

**Primera respuesta devuelta: `Z0005P`**

- Variante 1: TOLVA CEMENTERA.
  Fabricante: SEMIRREMOLQUES; submodelo: TOLVA CEMENTERA; tipo: SEMIREMOLQUE; segmento: SEMIREMOLQUE.

Años registrados por código: 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020.

**Contribuciones al score del top-1:**

`{"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.3996225893497467, "vehicle_type": 0, "year": 0.12}`

**Investigación propuesta:** Comparar la representación textual del esperado con la consulta; comprobar campos faltantes, vocabulario y posibles reglas de dominio. Modificar solo el ranking no puede rescatar un candidato que no se recuperó.

**Pregunta adicional al experto:** este código se repite en 33 etiquetas y describe
una caja cerrada. Confirmar si existe una regla genérica de negocio que explique su
uso en consultas diferentes. No añadirlo como fallback ni corregir la etiqueta por suposición.

**Seguimiento:** pendiente de revisión al cierre. Anotar aquí la causa confirmada,
acción decidida y resultado de cualquier experimento futuro, sin borrar el diagnóstico original.
