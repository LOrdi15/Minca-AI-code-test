# Detailed failure register

All 91 frozen top-1 failures are retained. Source vehicle descriptions remain verbatim.
29 retrieval misses, 17 recovered outside top-3, 45 expected codes in top-3 but not first.
These are evidence and investigation hypotheses, not corrected labels. All production decisions are review.
The six simulated false accepts are recorded separately in evaluation/confidence_audit and evaluation/final.

## q0005 — validation — CAMION

Source description: FORD F 700 GASOLINA 28000 LBS CHASIS CABIN
Year: 2000; manufacturer: (missing); submodel: (missing); type: CAMIONES (HASTA 7.5 TONS.).
Expected: U0003D; returned: P00000; ordered top-3: P00000|U0003D|B00052.
Expected retrieval rank: 2.0. Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.08539325842696631, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.7094414949417115, "vehicle_type": 0, "year": 0.12}

Expected catalog code: U0003D; explicit years: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000.
- Variant row 10346: FORD; F-700; CAMION; EQ FORD F-700 GASOLINA 28,000 LBS CHASIS CABINA
Returned catalog code: P00000; explicit years: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000.
- Variant row 7667: FORD; F-700; CAMION; EQ FORD F-700 GASOLINA 30,000 LBS CHASIS CABINA

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0016 — validation — REMOLQUE

Source description: PLATAFORMA 2 EJES REVUELTA
Year: 2006; manufacturer: (missing); submodel: (missing); type: (missing).
Expected: Z0000M; returned: S0008A; ordered top-3: S0008A|U0007I|D0006V.
Expected retrieval rank: 43.0. Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.5317389249801636, "vehicle_type": 0, "year": 0.12}

Expected catalog code: Z0000M; explicit years: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.
- Variant row 12812: SEMIRREMOLQUES; CAJA SECA; SEMIREMOLQUE; RM CAJA CERRADA 2 EJES 40
Returned catalog code: S0008A; explicit years: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.
- Variant row 9501: SEMIRREMOLQUES; PLATAFORMA ALTA; SEMIREMOLQUE; RM PLATAFORMA 2 EJES 40

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0024 — validation — REMOLQUE

Source description: TANQUE A.INOX ANILLADO 2 EJES 31,000 LTS MEDIA. AUT.
Year: 2023; manufacturer: -; submodel: (missing); type: REMOLQUE.
Expected: Q00046; returned: U0003Y; ordered top-3: U0003Y|W0008B|Z0005M.
Expected retrieval rank: (not retrieved). Recognized conflicts: year.
Score contributions: {"fuzzy": 0.08444444444444445, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.76396404504776, "vehicle_type": 0, "year": -0.2}

Expected catalog code: Q00046; explicit years: 2014, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024.
- Variant row 8332: SEMIRREMOLQUES; TANQUE; SEMIREMOLQUE; SEMIREMOLQUE TANQUE ELIPTICO
Returned catalog code: U0003Y; explicit years: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022.
- Variant row 10367: SEMIRREMOLQUES; TANQUE; SEMIREMOLQUE; RM TANQUE A.INOX ANILLADO 2 EJES 31,000 LTS

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0035 — validation — AUTO

Source description: AUDI S3 SEDAN
Year: 2016; manufacturer: AUDI; submodel: (missing); type: AUTOS.
Expected: Q0004P; returned: R00034; ordered top-3: R00034|Q0004P|J000B5.
Expected retrieval rank: 4.0. Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.0855, "manufacturer": 0.02, "submodel": 0.0, "tfidf": 0.3962739586830139, "vehicle_type": 0, "year": 0.12}

Expected catalog code: Q0004P; explicit years: 2016, 2017, 2018, 2019.
- Variant row 8351: AUDI; A3; AUTO; AUDI A3 S3, 2.0T, 4 PUERTAS, S TRONIC
Returned catalog code: R00034; explicit years: 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2018.
- Variant row 8802: AUDI; S3; AUTO; S3 2.0L STRONIC QUATTRO L4 FSI AUT 3P CA CE PIEL CQ CB

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0050 — validation — REMOLQUE

Source description: CAJA REFRIGERADA
Year: 2015; manufacturer: CAJA; submodel: (missing); type: REMOLQUES.
Expected: Z0000M; returned: W0008G; ordered top-3: W0008G|I00083|M0009R.
Expected retrieval rank: 34.0. Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.09000000000000001, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.5754315733909607, "vehicle_type": 0, "year": 0.12}

Expected catalog code: Z0000M; explicit years: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.
- Variant row 12812: SEMIRREMOLQUES; CAJA SECA; SEMIREMOLQUE; RM CAJA CERRADA 2 EJES 40
Returned catalog code: W0008G; explicit years: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020.
- Variant row 11556: SEMIRREMOLQUES; CAJA REFRIGERADA; SEMIREMOLQUE; CAJA REFRIGERADORA CON EQUIPO

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0085 — validation — REMOLQUE

Source description: TOLVA
Year: 2022; manufacturer: DALTO; submodel: (missing); type: TOLVA.
Expected: Z0000M; returned: J0007M; ordered top-3: J0007M|Q0001C|Z0005P.
Expected retrieval rank: (not retrieved). Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.3192595839500427, "vehicle_type": 0, "year": 0.12}

Expected catalog code: Z0000M; explicit years: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.
- Variant row 12812: SEMIRREMOLQUES; CAJA SECA; SEMIREMOLQUE; RM CAJA CERRADA 2 EJES 40
Returned catalog code: J0007M; explicit years: 2020, 2021, 2022, 2023.
- Variant row 4883: SEMIRREMOLQUES; TOLVA GRANELERA; SEMIREMOLQUE; RM TOLVA GRANELERA 2 EJES NAC

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0086 — validation — REMOLQUE

Source description: TOLVA
Year: 2024; manufacturer: DALTO; submodel: (missing); type: TOLVA.
Expected: Z0000M; returned: K000DZ; ordered top-3: K000DZ|Z0005P|L0008A.
Expected retrieval rank: (not retrieved). Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.2844096958637238, "vehicle_type": 0, "year": 0.12}

Expected catalog code: Z0000M; explicit years: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.
- Variant row 12812: SEMIRREMOLQUES; CAJA SECA; SEMIREMOLQUE; RM CAJA CERRADA 2 EJES 40
Returned catalog code: K000DZ; explicit years: 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2024.
- Variant row 5626: SEMIRREMOLQUES; TOLVA (ALIMENTOS, QUIMICOS); SEMIREMOLQUE; RM TOLVA PRESURIZADA 28MTS^3 2EJES

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0094 — validation — PICKUP

Source description: DODEGE RAM 400
Year: 2019; manufacturer: DODEGE; submodel: (missing); type: PICKUP´S.
Expected: O0005H; returned: R0002P; ordered top-3: R0002P|S0008D|U0004P.
Expected retrieval rank: 10.0. Recognized conflicts: vehicle_type.
Score contributions: {"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.19616316854953766, "vehicle_type": 0, "year": 0.12}

Expected catalog code: O0005H; explicit years: 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020.
- Variant row 7353: CHRYSLER; RAM 2500; PICK UP; DODGE RAM 2500 R/T 5.7L 4X4 AUT CA
Returned catalog code: R0002P; explicit years: 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2022, 2025, 2026.
- Variant row 8787: ISUZU; ELF 400; CAMION; EQ ISUZU ELF 400 CHASIS CABINA "F"

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0095 — validation — OTHER

Source description: 35451
Year: 2024; manufacturer: DODGE; submodel: DURANGO; type: (missing).
Expected: C0006Z; returned: T000CA; ordered top-3: T000CA|C0006Z|M0005H.
Expected retrieval rank: 7.0. Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.02, "tfidf": 0.38974422812461856, "vehicle_type": 0.0, "year": 0.12}

Expected catalog code: C0006Z; explicit years: 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024.
- Variant row 1274: CHRYSLER; DURANGO; AUTO; DURANGO RT 5.7L V8 AUT 5P ABS CA CE PIEL CD CQ CB
Returned catalog code: T000CA; explicit years: 2022, 2023, 2024, 2025.
- Variant row 10157: CHRYSLER; DURANGO; AUTO; DURANGO GT PLUS V6 3.6L 5 PTS AUT

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0115 — validation — REMOLQUE

Source description: FERBEL
Year: 2019; manufacturer: FERBEL; submodel: (missing); type: REMOLQUE.
Expected: Z0000M; returned: T0002L; ordered top-3: T0002L|J0008Z|G000AP.
Expected retrieval rank: (not retrieved). Recognized conflicts: vehicle_type.
Score contributions: {"fuzzy": 0.04275, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.01953243277966976, "vehicle_type": 0, "year": 0.12}

Expected catalog code: Z0000M; explicit years: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.
- Variant row 12812: SEMIRREMOLQUES; CAJA SECA; SEMIREMOLQUE; RM CAJA CERRADA 2 EJES 40
Returned catalog code: T0002L; explicit years: 2019.
- Variant row 9805: HYUNDAI; SANTA FE; AUTO; SANTA FE GLS 2.0T 5 PUERTAS AUTOMATICA

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0130 — validation — CAMION

Source description: VOLTEO
Year: 1992; manufacturer: FORD; submodel: VOLTEO; type: VOLTEO.
Expected: Z0000M; returned: R0002M; ordered top-3: R0002M|U0001V|Y0004T.
Expected retrieval rank: (not retrieved). Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.0855, "manufacturer": 0.02, "submodel": 0.0, "tfidf": 0.4996009111404419, "vehicle_type": 0, "year": 0.12}

Expected catalog code: Z0000M; explicit years: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.
- Variant row 12812: SEMIRREMOLQUES; CAJA SECA; SEMIREMOLQUE; RM CAJA CERRADA 2 EJES 40
Returned catalog code: R0002M; explicit years: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003.
- Variant row 8784: FORD; F-600 VOLTEO; CAMION; FORD F-600 VOLTEO HASTA 12 TON.

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0131 — validation — CAMION

Source description: VOLTEO
Year: 1992; manufacturer: FORD; submodel: VOLTEO; type: (missing).
Expected: Z0000M; returned: R0002M; ordered top-3: R0002M|U0001V|Y0004T.
Expected retrieval rank: (not retrieved). Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.0855, "manufacturer": 0.02, "submodel": 0.0, "tfidf": 0.4996009111404419, "vehicle_type": 0, "year": 0.12}

Expected catalog code: Z0000M; explicit years: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.
- Variant row 12812: SEMIRREMOLQUES; CAJA SECA; SEMIREMOLQUE; RM CAJA CERRADA 2 EJES 40
Returned catalog code: R0002M; explicit years: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003.
- Variant row 8784: FORD; F-600 VOLTEO; CAMION; FORD F-600 VOLTEO HASTA 12 TON.

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0132 — validation — OTHER

Source description: F150
Year: 2013; manufacturer: FORD  (ROJA); submodel: F150; type: REGULAR CA XL.
Expected: T0001Y; returned: Q0008J; ordered top-3: Q0008J|T0001Y|E00096.
Expected retrieval rank: 9.0. Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.0855, "manufacturer": 0.02, "submodel": 0.0, "tfidf": 0.08016005605459213, "vehicle_type": 0.0, "year": 0.12}

Expected catalog code: T0001Y; explicit years: 2013, 2014, 2016, 2017.
- Variant row 9782: FORD; F-150 PICK UP; PICK UP; FORD F-150 XL CABINA REGULAR 4X2 V8 5.0L AUT
Returned catalog code: Q0008J; explicit years: 2013, 2014, 2015, 2016, 2017.
- Variant row 8490: FORD; F-150 PICK UP; PICK UP; FORD F-150 XL CABINA REGULAR 4X4 V8 5.0L AUT

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0162 — validation — CAMION

Source description: CHASIS CABINA
Year: 2024; manufacturer: HINO; submodel: (missing); type: (missing).
Expected: M0001V; returned: D0006W; ordered top-3: D0006W|B000D5|N0004N.
Expected retrieval rank: 21.0. Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.0855, "manufacturer": 0.02, "submodel": 0.0, "tfidf": 0.45343301296234134, "vehicle_type": 0, "year": 0.12}

Expected catalog code: M0001V; explicit years: 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024.
- Variant row 6207: HINO; 300 CHASIS; CAMION; HINO 300 514 CHASIS CABINA 4.0L 3.48M L4 136HP DIS STD D/T
- Variant row 6208: HINO; 300 CHASIS; PICK UP; HINO 300 514 CHASIS CABINA 4.0L 3.48M L4 136HP DIS STD D/T
Returned catalog code: D0006W; explicit years: 2022, 2023, 2024.
- Variant row 1781: HINO; 500; CAMION; HINO SERIE 500 2628 6X2 CHASIS CABINA

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0186 — validation — OTHER

Source description: CISTERNA CHASSIS CABINA  MOD 4400 250 4X2
Year: 2003; manufacturer: INTERNACIONAL; submodel: (missing); type: (missing).
Expected: X0001T; returned: B0003G; ordered top-3: B0003G|H00002|U000DT.
Expected retrieval rank: 28.0. Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.07223140495867768, "manufacturer": 0.02, "submodel": 0.0, "tfidf": 0.329634690284729, "vehicle_type": 0.0, "year": 0.12}

Expected catalog code: X0001T; explicit years: 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016.
- Variant row 11827: INTERNATIONAL; 4300 MAS DE 14 TON; CAMION; INTERNACIONAL 4300 CHASIS CABINA MODULAR N G 4 X 2 210HP 15.8 TON
Returned catalog code: B0003G; explicit years: 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016.
- Variant row 636: INTERNATIONAL; 4400; CAMION; INTERNACIONAL 4400 CHASIS CABINA 6 X 2 250HP 23.5 TON

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0204 — validation — CAMION

Source description: JAC FRISON T8 L4 STD
Year: 2024; manufacturer: JAC; submodel: (missing); type: CAMIONES (HASTA 1.5 TONS.).
Expected: J0005B; returned: B000CS; ordered top-3: B000CS|J0005B|N000CN.
Expected retrieval rank: 4.0. Recognized conflicts: vehicle_type.
Score contributions: {"fuzzy": 0.0855, "manufacturer": 0.02, "submodel": 0.0, "tfidf": 0.5242019712924958, "vehicle_type": 0, "year": 0.12}

Expected catalog code: J0005B; explicit years: 2022, 2023, 2024, 2025, 2026.
- Variant row 4798: JAC; T8; PICK UP; T8 FRISON L4 2.0L 139 CP 4 PUERTAS STD BA AA 4X4
Returned catalog code: B000CS; explicit years: 2024, 2025.
- Variant row 974: JAC; T8; PICK UP; T8 FRISON L4 2.0T 190 CP 4 PUERTAS STD  BA AA

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0206 — validation — PICKUP

Source description: PICK UP JACK FRISON T6
Year: 2024; manufacturer: JACK; submodel: (missing); type: (missing).
Expected: Z0008D; returned: N000CN; ordered top-3: N000CN|Z0008D|G000CP.
Expected retrieval rank: 3.0. Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.38269154727458954, "vehicle_type": 0, "year": 0.12}

Expected catalog code: Z0008D; explicit years: 2024, 2025.
- Variant row 13094: JAC; T6; PICK UP; T6 FLEX FRISON L4 2.0T 190 CP 4 PUERTAS STD  BA AA
Returned catalog code: N000CN; explicit years: 2020, 2021, 2022, 2023, 2024.
- Variant row 7106: JAC; T6; PICK UP; T6 FRISON L4 2.0T 190 CP 4 PUERTAS STD  BA AA

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0221 — validation — TRACTO

Source description: T800
Year: 2017; manufacturer: KENWORTH; submodel: (missing); type: TRACTO.
Expected: F0000H; returned: X0003K; ordered top-3: X0003K|F0000H|Z0003D.
Expected retrieval rank: 2.0. Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.0855, "manufacturer": 0.02, "submodel": 0.0, "tfidf": 0.4618758022785187, "vehicle_type": 0, "year": 0.12}

Expected catalog code: F0000H; explicit years: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023.
- Variant row 2571: KENWORTH; T800; TRACTO CAMION; TR KENWORTH T 800 B 42"
Returned catalog code: X0003K; explicit years: 2017.
- Variant row 11891: KENWORTH; T800; TRACTO CAMION; TR KENWORTH T-800 B 42

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0315 — validation — REMOLQUE

Source description: REMOLQUE
Year: 2021; manufacturer: REMOLQUES; submodel: REMOLQUE; type: (missing).
Expected: Z0000M; returned: Q00046; ordered top-3: Q00046|O0008Q|P0008I.
Expected retrieval rank: 43.0. Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.06333333333333334, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.14798598736524582, "vehicle_type": 0, "year": 0.12}

Expected catalog code: Z0000M; explicit years: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.
- Variant row 12812: SEMIRREMOLQUES; CAJA SECA; SEMIREMOLQUE; RM CAJA CERRADA 2 EJES 40
Returned catalog code: Q00046; explicit years: 2014, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024.
- Variant row 8332: SEMIRREMOLQUES; TANQUE; SEMIREMOLQUE; SEMIREMOLQUE TANQUE ELIPTICO

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0323 — validation — REMOLQUE

Source description: PLATAFORMA TANDEM 2 EJES
Year: 2016; manufacturer: RM SEMIREMOLQUE; submodel: (missing); type: CHASIS.
Expected: T00076; returned: S0008A; ordered top-3: S0008A|U0002I|T00076.
Expected retrieval rank: 5.0. Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.0755421686746988, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.3930980354547501, "vehicle_type": 0, "year": 0.12}

Expected catalog code: T00076; explicit years: 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016.
- Variant row 9972: SEMIRREMOLQUES; PLATAFORMA ALTA; SEMIREMOLQUE; RM PLATAFORMA PLANA 2 EJES 48
Returned catalog code: S0008A; explicit years: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.
- Variant row 9501: SEMIRREMOLQUES; PLATAFORMA ALTA; SEMIREMOLQUE; RM PLATAFORMA 2 EJES 40

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0349 — validation — AUTO

Source description: AUTOMOVIL YARIS CORE H/B MT AC
Year: 2014; manufacturer: TOYOTA YARIS; submodel: (missing); type: (missing).
Expected: Y0004U; returned: D0009T; ordered top-3: D0009T|L0004M|Y0004U.
Expected retrieval rank: 3.0. Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.059814814814814814, "manufacturer": 0.02, "submodel": 0.0, "tfidf": 0.5168550252914429, "vehicle_type": 0, "year": 0.12}

Expected catalog code: Y0004U; explicit years: 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2022.
- Variant row 12453: TOYOTA; YARIS; AUTO; YARIS CORE HB 1.5L 106HP L4 STD 5P CA SE CD CB
Returned catalog code: D0009T; explicit years: 2014.
- Variant row 1886: TOYOTA; YARIS; AUTO; YARIS CORE 1.5L L4 AUT 4P D/T CA CE TELA CD SQ CB

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0351 — validation — AUTO

Source description: AUTOMOVIL YARIS CORE H/B MT A/A
Year: 2014; manufacturer: TOYOYA YARIS; submodel: (missing); type: (missing).
Expected: Y0004U; returned: D0009T; ordered top-3: D0009T|L0004M|Y0004U.
Expected retrieval rank: 3.0. Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.05915094339622641, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.4379332780838013, "vehicle_type": 0, "year": 0.12}

Expected catalog code: Y0004U; explicit years: 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2022.
- Variant row 12453: TOYOTA; YARIS; AUTO; YARIS CORE HB 1.5L 106HP L4 STD 5P CA SE CD CB
Returned catalog code: D0009T; explicit years: 2014.
- Variant row 1886: TOYOTA; YARIS; AUTO; YARIS CORE 1.5L L4 AUT 4P D/T CA CE TELA CD SQ CB

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0360 — validation — PICKUP

Source description: V.W. SAVEIRO  ROJO
Year: 2012; manufacturer: V; submodel: (missing); type: PICKUP´S.
Expected: B000B1; returned: M000DT; ordered top-3: M000DT|R0004R|B000B1.
Expected retrieval rank: 8.0. Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.41259557604789737, "vehicle_type": 0, "year": 0.12}

Expected catalog code: B000B1; explicit years: 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018.
- Variant row 911: VOLKSWAGEN; SAVEIRO; PICK UP; VOLKSWAGEN SAVEIRO STARTLINE 1.6L STD CA DH
Returned catalog code: M000DT; explicit years: 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018.
- Variant row 6640: VOLKSWAGEN; SAVEIRO; PICK UP; VOLKSWAGEN SAVEIRO STARTLINE 1.6L STD

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0383 — validation — OTHER

Source description: CARRO UTILITARIO
Year: 2023; manufacturer: VW VIRTUS COMFORTLINE; submodel: (missing); type: (missing).
Expected: Q000C7; returned: R000CA; ordered top-3: R000CA|Q000C7|U0006C.
Expected retrieval rank: 2.0. Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.4543520987033844, "vehicle_type": 0.0, "year": 0.12}

Expected catalog code: Q000C7; explicit years: 2020, 2021, 2022, 2023, 2024, 2025.
- Variant row 8623: VOLKSWAGEN; VIRTUS; AUTO; VIRTUS COMFORTLINE, L4, 1.6L, 110 CP, 4 PUERTAS, STD
Returned catalog code: R000CA; explicit years: 2020, 2021, 2022, 2023, 2024, 2025.
- Variant row 9137: VOLKSWAGEN; VIRTUS; AUTO; VIRTUS COMFORTLINE, L4, 1.6L, 110 CP, 4 PUERTAS, AUT

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0008 — development — OTHER

Source description: HINO 816 LONG SERIE 300
Year: 2019; manufacturer: (missing); submodel: (missing); type: (missing).
Expected: I000AJ; returned: N00083; ordered top-3: N00083|W0008K|I000AJ.
Expected retrieval rank: 9.0. Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.35409375429153445, "vehicle_type": 0.0, "year": 0.12}

Expected catalog code: I000AJ; explicit years: 2019.
- Variant row 4477: HINO; 300 CHASIS; CAMION; 300 816 LARGO, 4.0T, 2 PUERTAS, MANUAL, HIBRIDO
Returned catalog code: N00083; explicit years: 2018, 2019, 2022, 2023, 2024, 2025.
- Variant row 6942: HINO; 300 CHASIS; CAMION; HINO 300 816 SUPER LARGO 4.0T 2P STD

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0012 — development — OTHER

Source description: NISSAN NP300 ESTACAS PAQ SEG DH AC STD
Year: 2018; manufacturer: (missing); submodel: (missing); type: (missing).
Expected: V00023; returned: P000AO; ordered top-3: P000AO|V00023|P000AN.
Expected retrieval rank: 4.0. Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.5382496654987335, "vehicle_type": 0.0, "year": 0.12}

Expected catalog code: V00023; explicit years: 2017, 2018, 2019, 2020.
- Variant row 10812: NISSAN; ESTACAS; PICK UP; PICK UP 2.5L 2 PUERTAS MANUAL DH AA PAQ SEG
- Variant row 10813: NISSAN; ESTACAS; PICK UP; NP300 PICK UP 2.5L 2 PUERTAS MANUAL DH AA PAQ SEG
Returned catalog code: P000AO; explicit years: 2015, 2017, 2018.
- Variant row 8059: NISSAN; PICK UP; PICK UP; NP300 ESTACAS 2.4L 2 PUERTAS MANUAL DH PAQ SEG

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0014 — development — REMOLQUE

Source description: PLATAFORMA 2 EJES
Year: 2006; manufacturer: (missing); submodel: (missing); type: (missing).
Expected: Z0000M; returned: S0008A; ordered top-3: S0008A|U0007I|D0006V.
Expected retrieval rank: (not retrieved). Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.09000000000000001, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.599103569984436, "vehicle_type": 0, "year": 0.12}

Expected catalog code: Z0000M; explicit years: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.
- Variant row 12812: SEMIRREMOLQUES; CAJA SECA; SEMIREMOLQUE; RM CAJA CERRADA 2 EJES 40
Returned catalog code: S0008A; explicit years: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.
- Variant row 9501: SEMIRREMOLQUES; PLATAFORMA ALTA; SEMIREMOLQUE; RM PLATAFORMA 2 EJES 40

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0015 — development — REMOLQUE

Source description: PLATAFORMA 2 EJES
Year: 2004; manufacturer: (missing); submodel: (missing); type: (missing).
Expected: Z0000M; returned: S0008A; ordered top-3: S0008A|U0007I|D0006V.
Expected retrieval rank: (not retrieved). Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.09000000000000001, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.599103569984436, "vehicle_type": 0, "year": 0.12}

Expected catalog code: Z0000M; explicit years: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.
- Variant row 12812: SEMIRREMOLQUES; CAJA SECA; SEMIREMOLQUE; RM CAJA CERRADA 2 EJES 40
Returned catalog code: S0008A; explicit years: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.
- Variant row 9501: SEMIRREMOLQUES; PLATAFORMA ALTA; SEMIREMOLQUE; RM PLATAFORMA 2 EJES 40

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0018 — development — REMOLQUE

Source description: REMOLQUES
Year: 2025; manufacturer: (missing); submodel: (missing); type: (missing).
Expected: Z0000M; returned: G000CT; ordered top-3: G000CT|D0004U|U0001V.
Expected retrieval rank: 26.0. Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.09000000000000001, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.11544596403837204, "vehicle_type": 0, "year": 0.12}

Expected catalog code: Z0000M; explicit years: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.
- Variant row 12812: SEMIRREMOLQUES; CAJA SECA; SEMIREMOLQUE; RM CAJA CERRADA 2 EJES 40
Returned catalog code: G000CT; explicit years: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2018, 2019, 2023, 2025.
- Variant row 3535: SEMIRREMOLQUES; JAULA; SEMIREMOLQUE; RM JAULA 2 EJES 35

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0019 — development — REMOLQUE

Source description: RM SEMIREMOLQUE
Year: 2019; manufacturer: (missing); submodel: (missing); type: CHASIS.
Expected: Z0000M; returned: Q00046; ordered top-3: Q00046|G000CT|Z0000M.
Expected retrieval rank: 10.0. Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.40149444937705997, "vehicle_type": 0, "year": 0.12}

Expected catalog code: Z0000M; explicit years: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.
- Variant row 12812: SEMIRREMOLQUES; CAJA SECA; SEMIREMOLQUE; RM CAJA CERRADA 2 EJES 40
Returned catalog code: Q00046; explicit years: 2014, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024.
- Variant row 8332: SEMIRREMOLQUES; TANQUE; SEMIREMOLQUE; SEMIREMOLQUE TANQUE ELIPTICO

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0047 — development — AUTO

Source description: ESCALADE ESV PAQ B 2021
Year: 2021; manufacturer: CADILLAC; submodel: ESCALADE ESV PAQ B; type: AUTO.
Expected: E0002F; returned: I000A6; ordered top-3: I000A6|E0002F|S00067.
Expected retrieval rank: 7.0. Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.08333333333333333, "manufacturer": 0.02, "submodel": 0.02, "tfidf": 0.5294214963912964, "vehicle_type": 0, "year": 0.12}

Expected catalog code: E0002F; explicit years: 2021, 2022, 2023, 2025, 2026.
- Variant row 2128: CADILLAC; ESCALADE; AUTO; ESCALADE ESV PREMIUM LUXURY V8 6.2L 5 PTS AUT
Returned catalog code: I000A6; explicit years: 2015, 2016, 2020, 2021.
- Variant row 4463: CADILLAC; ESCALADE; AUTO; ESCALADE ESV PREMIUM V8 6.2L AUT 5P ABS CA CE PIEL CQ CB
- Variant row 4464: CADILLAC; ESCALADE; AUTO; ESCALADE ESV PREMIUM 6.2L 5 PUERTAS AUTOMATICA PAQ E

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0053 — development — REMOLQUE

Source description: TOLVA
Year: 2019; manufacturer: CARMEX; submodel: (missing); type: TOLVA.
Expected: Z0000M; returned: Z0005P; ordered top-3: Z0005P|Z0003K|R0002X.
Expected retrieval rank: (not retrieved). Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.2525744497776032, "vehicle_type": 0, "year": 0.12}

Expected catalog code: Z0000M; explicit years: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.
- Variant row 12812: SEMIRREMOLQUES; CAJA SECA; SEMIREMOLQUE; RM CAJA CERRADA 2 EJES 40
Returned catalog code: Z0005P; explicit years: 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020.
- Variant row 12996: SEMIRREMOLQUES; TOLVA CEMENTERA; SEMIREMOLQUE; TOLVA CEMENTERA.

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0054 — development — REMOLQUE

Source description: PLATAFORMA
Year: 2008; manufacturer: CATAMEX; submodel: PLATAFORMA; type: (missing).
Expected: Z0000M; returned: L0001A; ordered top-3: L0001A|D0006V|E0001Q.
Expected retrieval rank: (not retrieved). Recognized conflicts: vehicle_type.
Score contributions: {"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.02, "tfidf": 0.4611872792243958, "vehicle_type": 0, "year": 0.12}

Expected catalog code: Z0000M; explicit years: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.
- Variant row 12812: SEMIRREMOLQUES; CAJA SECA; SEMIREMOLQUE; RM CAJA CERRADA 2 EJES 40
Returned catalog code: L0001A; explicit years: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008.
- Variant row 5675: INTERNATIONAL; PLATAFORMA; CAMION; CAMION INTERNACIONAL PLATAFORMA .

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0055 — development — AUTO

Source description: ALSVIN TM
Year: 2024; manufacturer: CHANGAN; submodel: (missing); type: AUTOS.
Expected: P00056; returned: P0007H; ordered top-3: P0007H|P00056|Y00051.
Expected retrieval rank: 2.0. Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.0855, "manufacturer": 0.02, "submodel": 0.0, "tfidf": 0.5840484380722046, "vehicle_type": 0, "year": 0.12}

Expected catalog code: P00056; explicit years: 2022, 2023, 2024, 2025, 2026.
- Variant row 7859: CHANGAN; ALSVIN; AUTO; CHANGAN ALSVIN BASE L4 4 PTS STD
Returned catalog code: P0007H; explicit years: 2022, 2023, 2024, 2025, 2026.
- Variant row 7942: CHANGAN; ALSVIN; AUTO; CHANGAN ALSVIN BASE L4 4 PTS AUT

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0068 — development — OTHER

Source description: TIGGO 8 PRO PREMIUM E HEV L4 HDS AUT 5 ABS CA CE PIEL SM CQ C
Year: 2025; manufacturer: CHIREY; submodel: (missing); type: (missing).
Expected: S0002Y; returned: C000C5; ordered top-3: C000C5|S0002Y|S0004C.
Expected retrieval rank: 2.0. Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.08539325842696631, "manufacturer": 0.02, "submodel": 0.0, "tfidf": 0.605037260055542, "vehicle_type": 0.0, "year": 0.12}

Expected catalog code: S0002Y; explicit years: 2025.
- Variant row 9307: CHIREY; TIGGO 8; AUTO; CHIREY TIGGO 8 PRO E+ PREMIUM
Returned catalog code: C000C5; explicit years: 2024, 2025.
- Variant row 1461: CHIREY; TIGGO 8; AUTO; CHIREY TIGGO 8 PRO PREMIUM L4 1.6T 5 PTS AUT PIEL

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0074 — development — OTHER

Source description: JEEP WRANGLER SAHARA
Year: 2015; manufacturer: CHRYSLER; submodel: JEEP WRANGLER SAHARA; type: (missing).
Expected: G00001; returned: I0007V; ordered top-3: I0007V|G00001|M0004C.
Expected retrieval rank: 17.0. Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.0855, "manufacturer": 0.02, "submodel": 0.02, "tfidf": 0.577604752779007, "vehicle_type": 0.0, "year": 0.12}

Expected catalog code: G00001; explicit years: 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016.
- Variant row 3070: CHRYSLER; JEEP WRANGLER; AUTO; WRANGLER UNLIMITED SAHARA 3.8L 205HP 4X4 V6 AUT 4P CA CE
Returned catalog code: I0007V; explicit years: 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018.
- Variant row 4380: CHRYSLER; JEEP WRANGLER; AUTO; WRANGLER SAHARA TOLDO DURO 4X4 V6 AUT 2P CA CE PIEL CD

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0082 — development — REMOLQUE

Source description: TOLVA
Year: 2023; manufacturer: DALTO; submodel: (missing); type: TOLVA.
Expected: Z0000M; returned: J0007M; ordered top-3: J0007M|Z0005P|L0008A.
Expected retrieval rank: (not retrieved). Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.3192595839500427, "vehicle_type": 0, "year": 0.12}

Expected catalog code: Z0000M; explicit years: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.
- Variant row 12812: SEMIRREMOLQUES; CAJA SECA; SEMIREMOLQUE; RM CAJA CERRADA 2 EJES 40
Returned catalog code: J0007M; explicit years: 2020, 2021, 2022, 2023.
- Variant row 4883: SEMIRREMOLQUES; TOLVA GRANELERA; SEMIREMOLQUE; RM TOLVA GRANELERA 2 EJES NAC

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0083 — development — REMOLQUE

Source description: TOLVA
Year: 2020; manufacturer: DALTO; submodel: (missing); type: TOLVA.
Expected: Z0000M; returned: Z0005P; ordered top-3: Z0005P|J0007M|R0002X.
Expected retrieval rank: (not retrieved). Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.40361698865890505, "vehicle_type": 0, "year": 0.12}

Expected catalog code: Z0000M; explicit years: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.
- Variant row 12812: SEMIRREMOLQUES; CAJA SECA; SEMIREMOLQUE; RM CAJA CERRADA 2 EJES 40
Returned catalog code: Z0005P; explicit years: 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020.
- Variant row 12996: SEMIRREMOLQUES; TOLVA CEMENTERA; SEMIREMOLQUE; TOLVA CEMENTERA.

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0084 — development — REMOLQUE

Source description: TOLVA
Year: 2021; manufacturer: DALTO; submodel: (missing); type: TOLVA.
Expected: Z0000M; returned: J0007M; ordered top-3: J0007M|R0002X|K000DZ.
Expected retrieval rank: (not retrieved). Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.3192595839500427, "vehicle_type": 0, "year": 0.12}

Expected catalog code: Z0000M; explicit years: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.
- Variant row 12812: SEMIRREMOLQUES; CAJA SECA; SEMIREMOLQUE; RM CAJA CERRADA 2 EJES 40
Returned catalog code: J0007M; explicit years: 2020, 2021, 2022, 2023.
- Variant row 4883: SEMIRREMOLQUES; TOLVA GRANELERA; SEMIREMOLQUE; RM TOLVA GRANELERA 2 EJES NAC

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0089 — development — REMOLQUE

Source description: PLATAFORMA
Year: 2003; manufacturer: DEL NORTE; submodel: PLATAFORMA; type: (missing).
Expected: Z0000M; returned: L0001A; ordered top-3: L0001A|D0006V|P000C6.
Expected retrieval rank: (not retrieved). Recognized conflicts: vehicle_type.
Score contributions: {"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.02, "tfidf": 0.40458899438381196, "vehicle_type": 0, "year": 0.12}

Expected catalog code: Z0000M; explicit years: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.
- Variant row 12812: SEMIRREMOLQUES; CAJA SECA; SEMIREMOLQUE; RM CAJA CERRADA 2 EJES 40
Returned catalog code: L0001A; explicit years: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008.
- Variant row 5675: INTERNATIONAL; PLATAFORMA; CAMION; CAMION INTERNACIONAL PLATAFORMA .

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0093 — development — CAMION

Source description: VOLTEO
Year: 1994; manufacturer: DINA; submodel: (missing); type: VOLTEO.
Expected: Z0000M; returned: W000CD; ordered top-3: W000CD|B0001Z|Y000DW.
Expected retrieval rank: (not retrieved). Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.09000000000000001, "manufacturer": 0.02, "submodel": 0.0, "tfidf": 0.6013042151927949, "vehicle_type": 0, "year": 0.12}

Expected catalog code: Z0000M; explicit years: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.
- Variant row 12812: SEMIRREMOLQUES; CAJA SECA; SEMIREMOLQUE; RM CAJA CERRADA 2 EJES 40
Returned catalog code: W000CD; explicit years: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004.
- Variant row 11700: DINA; 661-K VOLTEO; CAMION; DINA VOLTEO DE 14 TON.

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0100 — development — CAMION

Source description: CHASIS CABINA
Year: 2009; manufacturer: DODGE H100; submodel: CHASIS CABINA; type: (missing).
Expected: U00085; returned: H0002P; ordered top-3: H0002P|U00085|K0009D.
Expected retrieval rank: 2.0. Recognized conflicts: submodel|vehicle_type.
Score contributions: {"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": -0.05, "tfidf": 0.5092259645462036, "vehicle_type": 0, "year": 0.12}

Expected catalog code: U00085; explicit years: 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014.
- Variant row 10519: CHRYSLER; H100 ESTACAS; PICK UP; DODGE H 100 CHASIS CABINA DH L4 CA
Returned catalog code: H0002P; explicit years: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 2006, 2007, 2008, 2009.
- Variant row 3681: CHRYSLER; H100 ESTACAS; PICK UP; H100 CHASIS CABINA DIESEL STD., 02 OCUP.

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0104 — development — REMOLQUE

Source description: EL AGUILA *
Year: 2023; manufacturer: EL AGUILA; submodel: (missing); type: SEMIREMOLQUE.
Expected: Z0000M; returned: X0001I; ordered top-3: X0001I|W0005C|X00036.
Expected retrieval rank: (not retrieved). Recognized conflicts: vehicle_type|year.
Score contributions: {"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.16423431336879732, "vehicle_type": 0, "year": -0.2}

Expected catalog code: Z0000M; explicit years: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.
- Variant row 12812: SEMIRREMOLQUES; CAJA SECA; SEMIREMOLQUE; RM CAJA CERRADA 2 EJES 40
Returned catalog code: X0001I; explicit years: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998.
- Variant row 11816: VOLKSWAGEN; JETTA A3; AUTO; EL NUEVO JETTA GL AUT., 05 OCUP.

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0111 — development — OTHER

Source description: ESTACAS DH NP300 ESTACAS STD AA 158HP 2.5L 4CIL 2P 3OCUP 2019
Year: 2019; manufacturer: ESTACAS DH NP300 ESTACAS STD AA 158HP 2.5L 4CIL 2P 3OCUP; submodel: (missing); type: (missing).
Expected: H000BN; returned: V00023; ordered top-3: V00023|N0006O|W0009H.
Expected retrieval rank: 22.0. Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.30323477983474734, "vehicle_type": 0.0, "year": 0.12}

Expected catalog code: H000BN; explicit years: 2017, 2018, 2019, 2020.
- Variant row 4004: NISSAN; CHASIS CABINA; PICK UP; NP300 CHASIS CABINA 2.5L 2 PUERTAS MANUAL DH AA PAQ SEG
Returned catalog code: V00023; explicit years: 2017, 2018, 2019, 2020.
- Variant row 10812: NISSAN; ESTACAS; PICK UP; PICK UP 2.5L 2 PUERTAS MANUAL DH AA PAQ SEG
- Variant row 10813: NISSAN; ESTACAS; PICK UP; NP300 PICK UP 2.5L 2 PUERTAS MANUAL DH AA PAQ SEG

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0123 — development — CAMION

Source description: FOIRD XL REG CHASIS F550
Year: 2024; manufacturer: FOIRD; submodel: (missing); type: CAMIONES.
Expected: Q00084; returned: C000BM; ordered top-3: C000BM|N00001|R00091.
Expected retrieval rank: (not retrieved). Recognized conflicts: vehicle_type.
Score contributions: {"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.30231362879276275, "vehicle_type": 0, "year": 0.12}

Expected catalog code: Q00084; explicit years: 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024.
- Variant row 8475: FORD; F-550; PICK UP; F-550 KTP XL CH 2P V8 6.7L TDI AUT 2 OCUP
Returned catalog code: C000BM; explicit years: 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024.
- Variant row 1441: FORD; F-150 PICK UP; PICK UP; F-150 XL REG CAB 3.5L 2 PUERTAS AUTOMATICA 4X2

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0127 — development — OTHER

Source description: F450
Year: 2023; manufacturer: FORD; submodel: F450; type: (missing).
Expected: U00024; returned: H0004G; ordered top-3: H0004G|V000AP|U0009M.
Expected retrieval rank: (not retrieved). Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.0855, "manufacturer": 0.02, "submodel": 0.0, "tfidf": 0.1829436331987381, "vehicle_type": 0.0, "year": 0.12}

Expected catalog code: U00024; explicit years: 2001, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024.
- Variant row 10301: FORD; F-450; PICK UP; F-450 XL KTP 6.7L 2 PUERTAS AUTOMATICA DIESEL
Returned catalog code: H0004G; explicit years: 2022, 2023.
- Variant row 3745: FORD; F-150 PICK UP; PICK UP; FORD F-150 XL CREW CAB V6 3.3L 4 PTS AUT

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0134 — development — OTHER

Source description: FREIGHTLINER DETROIT DIESEL DD13 CASCADIA CAS
Year: 2025; manufacturer: FREIGHTLINER; submodel: CASCADIA 125; type: -.
Expected: N0001W; returned: U0008Z; ordered top-3: U0008Z|N0001W|H0001S.
Expected retrieval rank: 15.0. Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.07967741935483871, "manufacturer": 0.02, "submodel": 0.02, "tfidf": 0.5389693021774292, "vehicle_type": 0.0, "year": 0.12}

Expected catalog code: N0001W; explicit years: 2020, 2021, 2022, 2023, 2024, 2025, 2026.
- Variant row 6716: FREIGHTLINER; CASCADIA; TRACTO CAMION; FREIGHTLINER NEW CASCADIA  EURO V DD13 470HP FULLER 18VEL
Returned catalog code: U0008Z; explicit years: 2024, 2025.
- Variant row 10549: FREIGHTLINER; CASCADIA; TRACTO CAMION; FREIGHTLINER CASCADIA 116 DD13 470HP

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0137 — development — CAMION

Source description: VOLTEO
Year: 2010; manufacturer: FREIGHTLINER; submodel: (missing); type: VOLTEO.
Expected: Z0000M; returned: G0004P; ordered top-3: G0004P|B00045|Y0000B.
Expected retrieval rank: (not retrieved). Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.0855, "manufacturer": 0.02, "submodel": 0.0, "tfidf": 0.4302010595798493, "vehicle_type": 0, "year": 0.12}

Expected catalog code: Z0000M; explicit years: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.
- Variant row 12812: SEMIRREMOLQUES; CAJA SECA; SEMIREMOLQUE; RM CAJA CERRADA 2 EJES 40
Returned catalog code: G0004P; explicit years: 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014.
- Variant row 3241: FREIGHTLINER; M2 33K; CAMION; FREIGHTLINER M2 33K VOLTEO 190HP

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0144 — development — OTHER

Source description: CHEVROLET SILVERADO 1500 CAB. REG. D STD
Year: 2012; manufacturer: GENERAL MOTORS; submodel: (missing); type: (missing).
Expected: W0008P; returned: R000AP; ordered top-3: R000AP|W0008P|L0008K.
Expected retrieval rank: 11.0. Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.08510416666666666, "manufacturer": 0.02, "submodel": 0.0, "tfidf": 0.47731465101242065, "vehicle_type": 0.0, "year": 0.12}

Expected catalog code: W0008P; explicit years: 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016.
- Variant row 11565: GENERAL MOTORS; SILVERADO 1500; PICK UP; CHEVROLET SILVERADO 1500 CABINA REGULAR 4.3L 195HP V6 STD CA BA
Returned catalog code: R000AP; explicit years: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014.
- Variant row 9079: GENERAL MOTORS; SILVERADO 1500; PICK UP; CHEVROLET C-1500 PICK UP SILVERADO STD V6

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0151 — development — CAMION

Source description: GIANT MOTORS JAC FRISON T6 2.0L 4CL 190 HP 213 BLP 6 VEL  CHASIS CABINA  X200
Year: 2024; manufacturer: GIANT MOTORS; submodel: (missing); type: PICKUP.
Expected: Z0008D; returned: N000CN; ordered top-3: N000CN|Z0008D|H0006S.
Expected retrieval rank: 12.0. Recognized conflicts: manufacturer.
Score contributions: {"fuzzy": 0.0855, "manufacturer": -0.1, "submodel": 0.0, "tfidf": 0.2693126142024994, "vehicle_type": 0, "year": 0.12}

Expected catalog code: Z0008D; explicit years: 2024, 2025.
- Variant row 13094: JAC; T6; PICK UP; T6 FLEX FRISON L4 2.0T 190 CP 4 PUERTAS STD  BA AA
Returned catalog code: N000CN; explicit years: 2020, 2021, 2022, 2023, 2024.
- Variant row 7106: JAC; T6; PICK UP; T6 FRISON L4 2.0T 190 CP 4 PUERTAS STD  BA AA

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0163 — development — CAMION

Source description: HINO 1018 G EURO
Year: 2024; manufacturer: HINO; submodel: (missing); type: CAMIONES.
Expected: N0004N; returned: B000D5; ordered top-3: B000D5|N0004N|K0004M.
Expected retrieval rank: 2.0. Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.0855, "manufacturer": 0.02, "submodel": 0.0, "tfidf": 0.503111493587494, "vehicle_type": 0, "year": 0.12}

Expected catalog code: N0004N; explicit years: 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2022, 2023, 2024, 2025.
- Variant row 6817: HINO; 1018; CAMION; EQ HINO MOTORS 1018G CHASIS CABINA
Returned catalog code: B000D5; explicit years: 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.
- Variant row 987: HINO; 1018; CAMION; EQ HINO MOTORS 1018J CHASIS CABINA

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0175 — development — AUTO

Source description: HYUNDAI GRANDi10
Year: 2022; manufacturer: HYUNDAI; submodel: (missing); type: AUTO.
Expected: L000BP; returned: J000B7; ordered top-3: J000B7|Q000B9|R0005L.
Expected retrieval rank: 43.0. Recognized conflicts: vehicle_type.
Score contributions: {"fuzzy": 0.0855, "manufacturer": 0.02, "submodel": 0.0, "tfidf": 0.39230584502220156, "vehicle_type": 0, "year": 0.12}

Expected catalog code: L000BP; explicit years: 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026.
- Variant row 6055: HYUNDAI; Grand i; AUTO; GRAND i10 GL MID 1.25L L4 AUT 4P TELA
Returned catalog code: J000B7; explicit years: 2022, 2023.
- Variant row 5015: HYUNDAI; HD72; CAMION; HYUNDAI EX8 CHASIS CABINA 4X2

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0180 — development — AUTO

Source description: QX56 TA AWD V8 5PTAS
Year: 2012; manufacturer: INFINITI; submodel: (missing); type: AUTOS.
Expected: G0003R; returned: K000B7; ordered top-3: K000B7|G0003R|F0003D.
Expected retrieval rank: 2.0. Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.0855, "manufacturer": 0.02, "submodel": 0.0, "tfidf": 0.5324179530143738, "vehicle_type": 0, "year": 0.12}

Expected catalog code: G0003R; explicit years: 2012, 2013, 2014.
- Variant row 3207: INFINITI; QX56; AUTO; QX 56 AWD 5.6L V8 7SPEED AUT., 08 OCUP.
Returned catalog code: K000B7; explicit years: 2006, 2012, 2013, 2014.
- Variant row 5525: INFINITI; QX56; AUTO; INFINITI QX56 5.6L AWD V8 AUT CA CE PIEL CQ CB

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0188 — development — CAMION

Source description: VOLTEO
Year: 2008; manufacturer: INTERNACIONAL; submodel: (missing); type: VOLTEO.
Expected: Z0000M; returned: E000BZ; ordered top-3: E000BZ|F0002G|L0001A.
Expected retrieval rank: (not retrieved). Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.0855, "manufacturer": 0.02, "submodel": 0.0, "tfidf": 0.3676578998565674, "vehicle_type": 0, "year": 0.12}

Expected catalog code: Z0000M; explicit years: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.
- Variant row 12812: SEMIRREMOLQUES; CAJA SECA; SEMIREMOLQUE; RM CAJA CERRADA 2 EJES 40
Returned catalog code: E000BZ; explicit years: 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016.
- Variant row 2477: INTERNATIONAL; 4300 MAS DE 14 TON; CAMION; INTERNACIONAL 4300 4X2 VOLTEO 195HP 15 TON

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0195 — development — CAMION

Source description: VOLTEO 4300
Year: 2002; manufacturer: INTERNATIONAL; submodel: (missing); type: (missing).
Expected: Z0000M; returned: E000BZ; ordered top-3: E000BZ|Y000DN|A000B2.
Expected retrieval rank: (not retrieved). Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.0855, "manufacturer": 0.02, "submodel": 0.0, "tfidf": 0.474579656124115, "vehicle_type": 0, "year": 0.12}

Expected catalog code: Z0000M; explicit years: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.
- Variant row 12812: SEMIRREMOLQUES; CAJA SECA; SEMIREMOLQUE; RM CAJA CERRADA 2 EJES 40
Returned catalog code: E000BZ; explicit years: 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016.
- Variant row 2477: INTERNATIONAL; 4300 MAS DE 14 TON; CAMION; INTERNACIONAL 4300 4X2 VOLTEO 195HP 15 TON

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0200 — development — CAMION

Source description: ISUZU ELF600 CHASIS CABINA
Year: 2018; manufacturer: ISUZU; submodel: (missing); type: CAMIONES.
Expected: P0002U; returned: S00079; ordered top-3: S00079|P0002U|K000CV.
Expected retrieval rank: 4.0. Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.08022222222222222, "manufacturer": 0.02, "submodel": 0.0, "tfidf": 0.4903830707073212, "vehicle_type": 0, "year": 0.12}

Expected catalog code: P0002U; explicit years: 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018.
- Variant row 7770: ISUZU; ELF 600; CAMION; EQ ISUZU ELF 600 CHASIS CABINA "H"
Returned catalog code: S00079; explicit years: 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2024, 2025, 2026.
- Variant row 9464: ISUZU; ELF 600; CAMION; EQ ISUZU ELF 600 CHASIS CABINA "M"

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0205 — development — OTHER

Source description: SUNRAY PASS SMART
Year: 2025; manufacturer: JAC; submodel: SUNRAY PASS SMART; type: (missing).
Expected: E0001N; returned: C000BV; ordered top-3: C000BV|E0001N|B000BM.
Expected retrieval rank: 5.0. Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.061290322580645165, "manufacturer": 0.02, "submodel": 0.02, "tfidf": 0.42449820041656494, "vehicle_type": 0.0, "year": 0.12}

Expected catalog code: E0001N; explicit years: 2018, 2022, 2023, 2024, 2025, 2026.
- Variant row 2100: JAC; SUNRAY; AUTO; SUNRAY PASAJE L4 2.8T 150 CP 5 PTS STD
Returned catalog code: C000BV; explicit years: 2021, 2022, 2023, 2024, 2025, 2026, 2027.
- Variant row 1450: JAC; HFC; PICK UP; SUNRAY CARGO L4 2.8T 150 CP 5 PTS STD
- Variant row 1451: JAC; SUNRAY; PICK UP; SUNRAY CARGO L4 2.8T 150 CP 5 PTS STD

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0210 — development — OTHER

Source description: SAHARA
Year: 2020; manufacturer: JEEP UNLIMITED; submodel: SAHARA; type: (missing).
Expected: K0004F; returned: X000A6; ordered top-3: X000A6|U0008O|B00015.
Expected retrieval rank: 35.0. Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.41441068053245544, "vehicle_type": 0.0, "year": 0.12}

Expected catalog code: K0004F; explicit years: 2018, 2019, 2020.
- Variant row 5278: CHRYSLER; JEEP WRANGLER; AUTO; WRANGLER JL UNLIMITED RUBICON 3.6L 5 PUERTAS AUTOMATICA
Returned catalog code: X000A6; explicit years: 2020, 2021.
- Variant row 12134: CHRYSLER; JEEP WRANGLER; AUTO; WRANGLER UNLIMITED SAHARA L4 2.0L 270 CP 5 PUERTAS AUT MILD HYBRID
- Variant row 12135: CHRYSLER; JEEP WRANGLER; AUTO; WRANGLER UNLIMITED SAHARA L4 2.0L 270 CP 5P AUT MILD HYBRID

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0211 — development — OTHER

Source description: JETTA
Year: 2024; manufacturer: JETTA; submodel: (missing); type: (missing).
Expected: S0003P; returned: M0006V; ordered top-3: M0006V|I000D3|K000AO.
Expected retrieval rank: (not retrieved). Recognized conflicts: year.
Score contributions: {"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.47157740592956543, "vehicle_type": 0.0, "year": -0.2}

Expected catalog code: S0003P; explicit years: 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026.
- Variant row 9335: VOLKSWAGEN; JETTA A7; AUTO; JETTA A7 COMFORTLINE 1.4T 4 PUERTAS AUTOMATICA
Returned catalog code: M0006V; explicit years: 1989, 1990, 1991, 1992.
- Variant row 6390: VOLKSWAGEN; JETTA A2; AUTO; JETTA GL AUT.

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0216 — development — CAMION

Source description: T-880 DORMITORIO 52 PULG
Year: 2019; manufacturer: KENWORTH; submodel: (missing); type: CAMION.
Expected: G0008A; returned: T0003N; ordered top-3: T0003N|G0008A|T0008K.
Expected retrieval rank: 2.0. Recognized conflicts: vehicle_type.
Score contributions: {"fuzzy": 0.0855, "manufacturer": 0.02, "submodel": 0.0, "tfidf": 0.45688576698303224, "vehicle_type": 0, "year": 0.12}

Expected catalog code: G0008A; explicit years: 2015, 2016, 2017, 2018, 2019, 2020.
- Variant row 3370: KENWORTH; T800; TRACTO CAMION; TR KENWORTH T-880 PACCAR MX 13 500HP DORM 52 18V
Returned catalog code: T0003N; explicit years: 2015, 2016, 2017, 2018, 2019, 2020, 2021.
- Variant row 9844: KENWORTH; T680; TRACTO CAMION; KENWORTH T 880 52 in CUMMINS ISX 450 HP

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0226 — development — AUTO

Source description: RIO SEDAN SD LX
Year: 2020; manufacturer: KIA; submodel: RIO SEDAN SD LX; type: (missing).
Expected: S0002L; returned: D0003G; ordered top-3: D0003G|I00058|S0002L.
Expected retrieval rank: 3.0. Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.06551724137931034, "manufacturer": 0.02, "submodel": 0.02, "tfidf": 0.515907508134842, "vehicle_type": 0, "year": 0.12}

Expected catalog code: S0002L; explicit years: 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023.
- Variant row 9294: KIA; RIO; AUTO; RIO LX 1.6L 4 PUERTAS MANUAL
Returned catalog code: D0003G; explicit years: 2018, 2019, 2020, 2021, 2022, 2023.
- Variant row 1656: KIA; RIO; AUTO; RIO LX 1.6L 4P AUT

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0237 — development — AUTO

Source description: LX700h LUXURY
Year: 2026; manufacturer: LEXUS; submodel: (missing); type: AUTOS.
Expected: H0006M; returned: J000BA; ordered top-3: J000BA|H0006M|R000BM.
Expected retrieval rank: 3.0. Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.0855, "manufacturer": 0.02, "submodel": 0.0, "tfidf": 0.4618657171726227, "vehicle_type": 0, "year": 0.12}

Expected catalog code: H0006M; explicit years: 2025, 2026.
- Variant row 3823: LEXUS; LEXUS; AUTO; LEXUS LX 700H LUXURY, V6, 3.5T, 457 CP, 5 PUERTAS, AUT, BA, AA, QC, HEV
Returned catalog code: J000BA; explicit years: 2023, 2025, 2026.
- Variant row 5018: LEXUS; LEXUS; AUTO; LEXUS NX 350H LUXURY L4 2.5L 5 PTS AUT BA AA HEV

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0242 — development — OTHER

Source description: CARRO ESCALA 106 PIES
Year: 1985; manufacturer: LTI; submodel: (missing); type: (missing).
Expected: B0008E; returned: I00003; ordered top-3: I00003|R00092|B0008E.
Expected retrieval rank: 7.0. Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.1618940055370331, "vehicle_type": 0.0, "year": 0.12}

Expected catalog code: B0008E; explicit years: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004.
- Variant row 816: FREIGHTLINER; FL-106; CAMION; EQ FREIGHTLINER FL-106 52K 6X4 CHASIS CABINA
Returned catalog code: I00003; explicit years: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003.
- Variant row 4094: CHRYSLER; D-600 TANQUE; CAMION; DODGE D-600 CARRO TANQUE

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0243 — development — OTHER

Source description: MARCH ACTIVE HB STD AA CD BA 106HP ABS 1.6L 4CIL 5P 5OCUP 2020
Year: 2020; manufacturer: MARCH ACTIVE HB STD AA CD BA 106HP ABS 1.6L 4CIL 5P 5OCUP; submodel: (missing); type: (missing).
Expected: Z0003Z; returned: Z0006S; ordered top-3: Z0006S|Z0003Z|T00051.
Expected retrieval rank: 4.0. Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.3857463151216507, "vehicle_type": 0.0, "year": 0.12}

Expected catalog code: Z0003Z; explicit years: 2016, 2017, 2018, 2019, 2020.
- Variant row 12934: NISSAN; MARCH; AUTO; NISSAN MARCH ACTIVE, 1.6L, 5 PUERTAS, MANUAL, AC, ABS
Returned catalog code: Z0006S; explicit years: 2015, 2016, 2017, 2018, 2019, 2020.
- Variant row 13036: NISSAN; MARCH; AUTO; MARCH ACTIVE 1.6L 5 PUERTAS MANUAL AC

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0247 — development — AUTO

Source description: MAZDA 3I SPORT L4 2.5 SEDAN AUT
Year: 2021; manufacturer: MAZDA; submodel: (missing); type: AUTOMOVIL.
Expected: A00091; returned: J0006X; ordered top-3: J0006X|J000BG|K0002W.
Expected retrieval rank: 47.0. Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.0855, "manufacturer": 0.02, "submodel": 0.0, "tfidf": 0.3158358782529831, "vehicle_type": 0, "year": 0.12}

Expected catalog code: A00091; explicit years: 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026.
- Variant row 329: MAZDA; 3; AUTO; 3 I SPORT 2.5L 4 PUERTAS AUTOMATICA
Returned catalog code: J0006X; explicit years: 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024.
- Variant row 4858: MAZDA; CX5; AUTO; MAZDA CX-5 I SPORT 2.0L L4 AUT 5P ABS CA CE TELA CD CB

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0248 — development — AUTO

Source description: MAZDA 3i AUT 4 PTAS C/A.AC
Year: 2010; manufacturer: MAZDA; submodel: (missing); type: AUTOMOVIL.
Expected: Z00061; returned: W0004G; ordered top-3: W0004G|W000AJ|E0000K.
Expected retrieval rank: (not retrieved). Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.0855, "manufacturer": 0.02, "submodel": 0.0, "tfidf": 0.302870911359787, "vehicle_type": 0, "year": 0.12}

Expected catalog code: Z00061; explicit years: 2010, 2011, 2012, 2013, 2014, 2015.
- Variant row 13009: MAZDA; 3; AUTO; 3 SEDAN SPORT 4P AUT., 05 OCUP
Returned catalog code: W0004G; explicit years: 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018.
- Variant row 11410: MAZDA; 3; AUTO; MAZDA 3 I 2.0L L4 AUT 4P D/V CA SE TELA CD SQ CB

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0250 — development — AUTO

Source description: CLASE C 300 SPORT AUT
Year: 2020; manufacturer: MBENZ; submodel: (missing); type: AUTOMOVIL.
Expected: G00080; returned: P0002D; ordered top-3: P0002D|J000BQ|Z000DY.
Expected retrieval rank: 24.0. Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.36737685799598696, "vehicle_type": 0, "year": 0.12}

Expected catalog code: G00080; explicit years: 2020.
- Variant row 3360: MERCEDES BENZ; CLASE C; AUTO; CGI SPORT 2.0T 4 PUERTAS AUTOMATICA
Returned catalog code: P0002D; explicit years: 2019, 2020, 2021.
- Variant row 7752: MERCEDES BENZ; CLASE C; AUTO; CLASE C 300 CGI COUPE 2.0T 2 PUERTAS AUTOMATICA

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0264 — development — OTHER

Source description: COOPER S HOT CHILI
Year: 2007; manufacturer: MINI; submodel: COOPER S HOT CHILI; type: (missing).
Expected: Z000DZ; returned: Q0004F; ordered top-3: Q0004F|K00011|Z000DZ.
Expected retrieval rank: 10.0. Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.6758727908134461, "vehicle_type": 0.0, "year": 0.12}

Expected catalog code: Z000DZ; explicit years: 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014.
- Variant row 13298: BMW; MINI COOPER; AUTO; MINI COOPER S HOT CHILI 1.6L 163HP L4 STD 2P PIEL CA CE
Returned catalog code: Q0004F; explicit years: 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017.
- Variant row 8341: BMW; MINI COOPER; AUTO; MINI COOPER S HOT CHILI L4 AUT 2P CA CE PIEL CD CQ CB

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0267 — development — REMOLQUE

Source description: TOLVA
Year: 2016; manufacturer: MIRELES; submodel: (missing); type: TOLVA.
Expected: Z0000M; returned: Z0005P; ordered top-3: Z0005P|L0008A|U0007D.
Expected retrieval rank: (not retrieved). Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.39190560579299927, "vehicle_type": 0, "year": 0.12}

Expected catalog code: Z0000M; explicit years: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.
- Variant row 12812: SEMIRREMOLQUES; CAJA SECA; SEMIREMOLQUE; RM CAJA CERRADA 2 EJES 40
Returned catalog code: Z0005P; explicit years: 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020.
- Variant row 12996: SEMIRREMOLQUES; TOLVA CEMENTERA; SEMIREMOLQUE; TOLVA CEMENTERA.

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0268 — development — CAMION

Source description: HILUX DOBLE CABINA BASE STD 4P 4CIL
Year: 2023; manufacturer: MITSUBICHI; submodel: (missing); type: CAMION.
Expected: Z000BV; returned: Z0004B; ordered top-3: Z0004B|F0008T|Z000BV.
Expected retrieval rank: 7.0. Recognized conflicts: manufacturer|vehicle_type.
Score contributions: {"fuzzy": 0.06690140845070423, "manufacturer": -0.1, "submodel": 0.0, "tfidf": 0.3762846350669861, "vehicle_type": 0, "year": 0.12}

Expected catalog code: Z000BV; explicit years: 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024.
- Variant row 13221: TOYOTA; HILUX PICK UP; PICK UP; HILUX CABINA DOBLE 2.7L L4 STD 4P CA CE CB
Returned catalog code: Z0004B; explicit years: 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026.
- Variant row 12946: TOYOTA; HILUX PICK UP; PICK UP; HILUX DOBLE CABINA DIESEL 2.8L 4P STD

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0269 — development — CAMION

Source description: L200 GLX DIESEL STD 4P 4CIL 2.4L 4WD
Year: 2023; manufacturer: MITSUBICHI; submodel: (missing); type: CAMION.
Expected: S0002A; returned: T0001C; ordered top-3: T0001C|L0006M|S0002A.
Expected retrieval rank: 6.0. Recognized conflicts: vehicle_type.
Score contributions: {"fuzzy": 0.06627906976744186, "manufacturer": 0.02, "submodel": 0.0, "tfidf": 0.336882421374321, "vehicle_type": 0, "year": 0.12}

Expected catalog code: S0002A; explicit years: 2022, 2023, 2024, 2025.
- Variant row 9283: MITSUBISHI; L200; PICK UP; MITSUBISHI L200 GLX L4 178 CP DSL 4 PTS STD
Returned catalog code: T0001C; explicit years: 2022, 2023, 2024, 2025, 2026.
- Variant row 9760: MITSUBISHI; L200; PICK UP; MITSUBISHI L200 GLX L4 126 CP 4 PTS STD

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0270 — development — CAMION

Source description: L200 GLX DIESEL STD 4P 4CIL 2.4L 4WD
Year: 2024; manufacturer: MITSUBICHI; submodel: (missing); type: CAMION.
Expected: S0002A; returned: T0001C; ordered top-3: T0001C|L0006M|S0002A.
Expected retrieval rank: 6.0. Recognized conflicts: vehicle_type.
Score contributions: {"fuzzy": 0.06627906976744186, "manufacturer": 0.02, "submodel": 0.0, "tfidf": 0.336882421374321, "vehicle_type": 0, "year": 0.12}

Expected catalog code: S0002A; explicit years: 2022, 2023, 2024, 2025.
- Variant row 9283: MITSUBISHI; L200; PICK UP; MITSUBISHI L200 GLX L4 178 CP DSL 4 PTS STD
Returned catalog code: T0001C; explicit years: 2022, 2023, 2024, 2025, 2026.
- Variant row 9760: MITSUBISHI; L200; PICK UP; MITSUBISHI L200 GLX L4 126 CP 4 PTS STD

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0273 — development — AUTO

Source description: MITSUBISHI MIRAGE GLX L3 1.2 AUT
Year: 2017; manufacturer: MITSUBISHI; submodel: (missing); type: AUTOMOVIL.
Expected: V00022; returned: W000DT; ordered top-3: W000DT|V00022|F000BX.
Expected retrieval rank: 4.0. Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.08142857142857142, "manufacturer": 0.02, "submodel": 0.0, "tfidf": 0.5564435184001922, "vehicle_type": 0, "year": 0.12}

Expected catalog code: V00022; explicit years: 2015, 2016, 2017, 2018, 2019, 2020.
- Variant row 10810: MITSUBISHI; MIRAGE; AUTO; MIRAGE GLX 1.2L 5 PUERTAS CVT
- Variant row 10811: MITSUBISHI; MIRAGE; AUTO; MIRAGE GLX 1.2L L3 AUT CVT 5P CA CE CB
Returned catalog code: W000DT; explicit years: 2015, 2016, 2017, 2018, 2019, 2020.
- Variant row 11752: MITSUBISHI; MIRAGE; AUTO; MIRAGE GLX 1.2L 5 PUERTAS MANUAL
- Variant row 11753: MITSUBISHI; MIRAGE; AUTO; MIRAGE GLX 1.2L L3 STD 5P CA CE CB

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0274 — development — PICKUP

Source description: PICK UP L200 GLX DOBLE CAB 4WD L4 TDI STD 4 ABS CA CE TELA SM
Year: 2023; manufacturer: MITSUBISHI; submodel: PICK UP L200 GLX DOBLE CAB 4WD STD; type: (missing).
Expected: S0002A; returned: T0001C; ordered top-3: T0001C|S0002A|L0006M.
Expected retrieval rank: 3.0. Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.0855, "manufacturer": 0.02, "submodel": 0.02, "tfidf": 0.3924002319574356, "vehicle_type": 0, "year": 0.12}

Expected catalog code: S0002A; explicit years: 2022, 2023, 2024, 2025.
- Variant row 9283: MITSUBISHI; L200; PICK UP; MITSUBISHI L200 GLX L4 178 CP DSL 4 PTS STD
Returned catalog code: T0001C; explicit years: 2022, 2023, 2024, 2025, 2026.
- Variant row 9760: MITSUBISHI; L200; PICK UP; MITSUBISHI L200 GLX L4 126 CP 4 PTS STD

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0277 — development — CAMION

Source description: INTERNATIONAL 4700 COMPACTADOR INTERNACIONAL
Year: 2002; manufacturer: NAV INT CORP; submodel: COMPACTADOR INTERNACIONAL; type: CAMION.
Expected: K000A4; returned: P0006M; ordered top-3: P0006M|K000A4|P0005X.
Expected retrieval rank: 2.0. Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.06831460674157303, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.3265778303146362, "vehicle_type": 0, "year": 0.12}

Expected catalog code: K000A4; explicit years: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2014.
- Variant row 5486: INTERNATIONAL; 4700 MAS DE 14 TON; CAMION; INTERNACIONAL 4700 CHASIS CABINA 4 X 2 NAVISTAR DT 466 E 190HP 15.4 TON
Returned catalog code: P0006M; explicit years: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005.
- Variant row 7911: INTERNATIONAL; 4700 MAS DE 14 TON; CAMION; INTERNACIONAL 4700 CHASIS CABINA 4 X 2 DT 466 E 175HP 15.4 TON

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0290 — development — OTHER

Source description: COCHE GRIS OXFORD SEDAM ADVANCE MT
Year: 2013; manufacturer: NISSAN SEDAN; submodel: (missing); type: (missing).
Expected: Q0007J; returned: Z000AH; ordered top-3: Z000AH|Q0007J|V0001D.
Expected retrieval rank: 4.0. Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.05659574468085107, "manufacturer": 0.02, "submodel": 0.0, "tfidf": 0.16150036454200745, "vehicle_type": 0.0, "year": 0.12}

Expected catalog code: Q0007J; explicit years: 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023.
- Variant row 8454: NISSAN; SENTRA; AUTO; SENTRA ADVANCE 1.8L L4 STD 4P CA CE TELA CD CB
Returned catalog code: Z000AH; explicit years: 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026.
- Variant row 13171: NISSAN; MARCH; AUTO; MARCH ADVANCE L4 STD 5P CA CE TELA CD CB

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0295 — development — PICKUP

Source description: PEUGEOT PARTNER MAXI PACK STD DIESEL
Year: 2025; manufacturer: PEUGEOT; submodel: (missing); type: PICKUP CARGA.
Expected: B000AH; returned: U0005Y; ordered top-3: U0005Y|B000AH|E0006Y.
Expected retrieval rank: 3.0. Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.0778688524590164, "manufacturer": 0.02, "submodel": 0.0, "tfidf": 0.629653126001358, "vehicle_type": 0, "year": 0.12}

Expected catalog code: B000AH; explicit years: 2025.
- Variant row 891: PEUGEOT; PARTNER MAXI; PICK UP; PARTNER MAXI PACK L4 1.6T 90 CP 5 PUERTAS STD BA AA FL DIESEL
Returned catalog code: U0005Y; explicit years: 2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027.
- Variant row 10439: PEUGEOT; PARTNER MAXI; PICK UP; PARTNER MAXI PACK 1.6T 5 PUERTAS MANUAL

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0316 — development — REMOLQUE

Source description: REMOLQUE
Year: 1991; manufacturer: REMOLQUES; submodel: REMOLQUE; type: (missing).
Expected: Z0000M; returned: G00060; ordered top-3: G00060|E0009F|H000D3.
Expected retrieval rank: 43.0. Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.35425066351890566, "vehicle_type": 0, "year": 0.12}

Expected catalog code: Z0000M; explicit years: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.
- Variant row 12812: SEMIRREMOLQUES; CAJA SECA; SEMIREMOLQUE; RM CAJA CERRADA 2 EJES 40
Returned catalog code: G00060; explicit years: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016.
- Variant row 3288: SEMIRREMOLQUES; TANQUE; SEMIREMOLQUE; REMOLQUE TIPO TANQUE 30000 LTS.

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0318 — development — PICKUP

Source description: RENAULT RENAULT KANGOO EXPRESS CON AA CD BA STD VAN 4 CIL 4P
Year: 2015; manufacturer: RENAULT; submodel: (missing); type: PICKUP CARGA.
Expected: M0001Y; returned: U0007N; ordered top-3: U0007N|M0001Y|Z000DX.
Expected retrieval rank: 4.0. Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.07841269841269843, "manufacturer": 0.02, "submodel": 0.0, "tfidf": 0.5286436557769776, "vehicle_type": 0, "year": 0.12}

Expected catalog code: M0001Y; explicit years: 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015.
- Variant row 6211: RENAULT; KANGOO VAN; PICK UP; KANGOO EXPRESS 1.6L C/A AC STD., 02 OCUP.
Returned catalog code: U0007N; explicit years: 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2017.
- Variant row 10500: RENAULT; KANGOO VAN; PICK UP; RENAULT KANGOO EXPRESS. L4 D/H C/B

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0324 — development — REMOLQUE

Source description: REMOLQUE
Year: 2000; manufacturer: S/M; submodel: REMOLQUE; type: (missing).
Expected: Z0000M; returned: G00060; ordered top-3: G00060|E0009F|H000D3.
Expected retrieval rank: 50.0. Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.3303191900253296, "vehicle_type": 0, "year": 0.12}

Expected catalog code: Z0000M; explicit years: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.
- Variant row 12812: SEMIRREMOLQUES; CAJA SECA; SEMIREMOLQUE; RM CAJA CERRADA 2 EJES 40
Returned catalog code: G00060; explicit years: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016.
- Variant row 3288: SEMIRREMOLQUES; TANQUE; SEMIREMOLQUE; REMOLQUE TIPO TANQUE 30000 LTS.

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0340 — development — AUTO

Source description: SUZUKI SWIFT SPORT GLE 1.4 AUT
Year: 2022; manufacturer: SUZUKI; submodel: (missing); type: AUTOMOVIL.
Expected: S0001Y; returned: H0000H; ordered top-3: H0000H|M0000Q|T00074.
Expected retrieval rank: 13.0. Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.08015625, "manufacturer": 0.02, "submodel": 0.0, "tfidf": 0.564158570766449, "vehicle_type": 0, "year": 0.12}

Expected catalog code: S0001Y; explicit years: 2022.
- Variant row 9271: SUZUKI; SWIFT; AUTO; SWIFT GLE SPORT BOOSTERJET L4 1.4L 5 PTS AUT
Returned catalog code: H0000H; explicit years: 2022.
- Variant row 3600: SUZUKI; SWIFT; AUTO; SUZUKI SWIFT GLE L4 1.2L 5 PTS AUT

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0341 — development — AUTO

Source description: SWIFT HB GLS 5P L4 1.2T ABS BA AC R16 STD.
Year: 2021; manufacturer: SUZUKI; submodel: (missing); type: AUTOMOVIL.
Expected: F0004U; returned: G000A3; ordered top-3: G000A3|T00074|F0004U.
Expected retrieval rank: 4.0. Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.07307692307692307, "manufacturer": 0.02, "submodel": 0.0, "tfidf": 0.3261412471532822, "vehicle_type": 0, "year": 0.12}

Expected catalog code: F0004U; explicit years: 2018, 2019, 2020, 2021, 2022, 2023, 2024.
- Variant row 2732: SUZUKI; SWIFT; AUTO; SWIFT GLS 1.2L 5 PUERTAS MANUAL
Returned catalog code: G000A3; explicit years: 2019, 2020, 2021, 2022, 2023, 2024.
- Variant row 3436: SUZUKI; ERTIGA; AUTO; ERTIGA GLS 5P L4 1.5T ABS BA AC STD 07 OCUP

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0350 — development — PICKUP

Source description: HILUX DOBLE CABINA
Year: 2024; manufacturer: TOYOYA; submodel: (missing); type: (missing).
Expected: Z000BV; returned: F0008T; ordered top-3: F0008T|Z0004B|H000C0.
Expected retrieval rank: 7.0. Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.5719518899917603, "vehicle_type": 0, "year": 0.12}

Expected catalog code: Z000BV; explicit years: 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024.
- Variant row 13221: TOYOTA; HILUX PICK UP; PICK UP; HILUX CABINA DOBLE 2.7L L4 STD 4P CA CE CB
Returned catalog code: F0008T; explicit years: 2018, 2019, 2020, 2021, 2022, 2023, 2024.
- Variant row 2876: TOYOTA; HILUX PICK UP; PICK UP; HILUX DOBLE CABINA DIESEL 2.8L 4P AUT

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0352 — development — TRACTO

Source description: TR CAMION LEGALIZADO TIPO TRACTOCAMION. STD
Year: 2010; manufacturer: TRACTO; submodel: (missing); type: TRACTO.
Expected: E0005R; returned: O0003Q; ordered top-3: O0003Q|C000DF|E0006A.
Expected retrieval rank: (not retrieved). Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.07862068965517242, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.24313146471977234, "vehicle_type": 0, "year": 0.12}

Expected catalog code: E0005R; explicit years: 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016.
- Variant row 2249: MAN; TGS TRACTOCAMION; TRACTO CAMION; TR MAN TGS 39S 41.440 8X4
Returned catalog code: O0003Q; explicit years: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018.
- Variant row 7290: MACK; MACK TRACTOCAMION; TRACTO CAMION; TRACTOCAMION MACK

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0354 — development — TRACTO

Source description: KENWORTH T 680
Year: 2025; manufacturer: TRACTO CAMION; submodel: (missing); type: TRACTO.
Expected: K0009L; returned: Y000AG; ordered top-3: Y000AG|J0004N|K0009L.
Expected retrieval rank: 33.0. Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.08666666666666667, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.4228265404701233, "vehicle_type": 0, "year": 0.12}

Expected catalog code: K0009L; explicit years: 2025.
- Variant row 5467: KENWORTH; T680; TRACTO CAMION; KENWORTH T680 TRACTOCAMION KENWORTH NUEVA GENERACION
Returned catalog code: Y000AG; explicit years: 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027.
- Variant row 12659: KENWORTH; T680; TRACTO CAMION; TRACTOCAMION KENWORTH T 680 52 in CUMMINS ISX 450 HP

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0355 — development — TRACTO

Source description: TR CAMION LEGALIZADO TIPO TRACTOCAMION. STD.
Year: 2010; manufacturer: TRACTO CAMION; submodel: (missing); type: TRACTO.
Expected: T0004H; returned: O0003Q; ordered top-3: O0003Q|C000DF|E0006A.
Expected retrieval rank: 50.0. Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.07862068965517242, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.23458364009857177, "vehicle_type": 0, "year": 0.12}

Expected catalog code: T0004H; explicit years: 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016.
- Variant row 9874: MAN; TGA TRACTOCAMION; TRACTO CAMION; TR MAN TGA 26.430
Returned catalog code: O0003Q; explicit years: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018.
- Variant row 7290: MACK; MACK TRACTOCAMION; TRACTO CAMION; TRACTOCAMION MACK

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0358 — development — REMOLQUE

Source description: TOLVA
Year: 2018; manufacturer: TYRSOL; submodel: (missing); type: TOLVA.
Expected: Z0000M; returned: Z0005P; ordered top-3: Z0005P|Z0003K|R0002X.
Expected retrieval rank: (not retrieved). Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.40210620760917665, "vehicle_type": 0, "year": 0.12}

Expected catalog code: Z0000M; explicit years: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.
- Variant row 12812: SEMIRREMOLQUES; CAJA SECA; SEMIREMOLQUE; RM CAJA CERRADA 2 EJES 40
Returned catalog code: Z0005P; explicit years: 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020.
- Variant row 12996: SEMIRREMOLQUES; TOLVA CEMENTERA; SEMIREMOLQUE; TOLVA CEMENTERA.

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0359 — development — REMOLQUE

Source description: TOLVA
Year: 2017; manufacturer: TYRSOL; submodel: (missing); type: TOLVA.
Expected: Z0000M; returned: Z0005P; ordered top-3: Z0005P|Y0001Z|Z0003K.
Expected retrieval rank: (not retrieved). Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.40210620760917665, "vehicle_type": 0, "year": 0.12}

Expected catalog code: Z0000M; explicit years: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.
- Variant row 12812: SEMIRREMOLQUES; CAJA SECA; SEMIREMOLQUE; RM CAJA CERRADA 2 EJES 40
Returned catalog code: Z0005P; explicit years: 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020.
- Variant row 12996: SEMIRREMOLQUES; TOLVA CEMENTERA; SEMIREMOLQUE; TOLVA CEMENTERA.

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0361 — development — OTHER

Source description: VENTURE EXT
Year: 1998; manufacturer: VENTURE; submodel: VENTURE EXT; type: (missing).
Expected: U0001I; returned: M0000S; ordered top-3: M0000S|U0001I|J00063.
Expected retrieval rank: 2.0. Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.02, "tfidf": 0.5289071023464204, "vehicle_type": 0.0, "year": 0.12}

Expected catalog code: U0001I; explicit years: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003.
- Variant row 10279: GENERAL MOTORS; VENTURE; AUTO; VENTURE VAN LT V6 AUT 5P CA CE PIEL CD CB
Returned catalog code: M0000S; explicit years: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005.
- Variant row 6168: GENERAL MOTORS; VENTURE; AUTO; VENTURE LS V6 AUT 5P ABS CA CE TELA CD SQ CB

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0369 — development — REMOLQUE

Source description: TOLVA
Year: 2015; manufacturer: VISUSA; submodel: (missing); type: TOLVA.
Expected: Z0000M; returned: Z0005P; ordered top-3: Z0005P|L0008A|U0007D.
Expected retrieval rank: (not retrieved). Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.3996225893497467, "vehicle_type": 0, "year": 0.12}

Expected catalog code: Z0000M; explicit years: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.
- Variant row 12812: SEMIRREMOLQUES; CAJA SECA; SEMIREMOLQUE; RM CAJA CERRADA 2 EJES 40
Returned catalog code: Z0005P; explicit years: 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020.
- Variant row 12996: SEMIRREMOLQUES; TOLVA CEMENTERA; SEMIREMOLQUE; TOLVA CEMENTERA.

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.

## q0370 — development — REMOLQUE

Source description: TOLVA
Year: 2013; manufacturer: VISUSA; submodel: (missing); type: TOLVA.
Expected: Z0000M; returned: Z0005P; ordered top-3: Z0005P|L0008A|U0007D.
Expected retrieval rank: (not retrieved). Recognized conflicts: (none recognized).
Score contributions: {"fuzzy": 0.0855, "manufacturer": 0.0, "submodel": 0.0, "tfidf": 0.3996225893497467, "vehicle_type": 0, "year": 0.12}

Expected catalog code: Z0000M; explicit years: 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.
- Variant row 12812: SEMIRREMOLQUES; CAJA SECA; SEMIREMOLQUE; RM CAJA CERRADA 2 EJES 40
Returned catalog code: Z0005P; explicit years: 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020.
- Variant row 12996: SEMIRREMOLQUES; TOLVA CEMENTERA; SEMIREMOLQUE; TOLVA CEMENTERA.

Investigation: verify domain classification and missing/version-specific attributes before changing labels or adding rules. Inspect retrieval coverage separately from ordering; obtain new validation evidence for any proposed change.
