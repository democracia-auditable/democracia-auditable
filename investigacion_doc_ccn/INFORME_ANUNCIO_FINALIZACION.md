# El Anuncio de Finalización de Contrato de la PLACSP: presencia, uso y contenido

**Estudio exploratorio. Versión 2, 1 de noviembre de 2026.** Complementa la fase 0 de «Democracia Auditable» (§8.6 y §9.0 bis). Datos abiertos oficiales y programas sin IA. La versión 1 pasó una ronda de revisión adversarial con ChatGPT. Esta versión incorpora sus correcciones (§7) y **no ha sido revisada todavía**.

**Qué no es este estudio:** no evalúa a ningún órgano de contratación ni compara administraciones, y no nombra a nadie. No prueba incumplimientos. Describe la presencia y el contenido de un mecanismo de publicación **en la sindicación de los perfiles del contratante alojados en la PLACSP**.

---

## Resumen

1. Desde mayo de 2024 la PLACSP dispone de un **Anuncio de Finalización de Contrato** (`DOC_CCN`): un documento estructurado (XML, CODICE 2.8) con la fecha real de inicio y fin de cada contrato, la causa de extinción si la hay, un importe pagado y documentos anexos.
2. **Sus campos de detalle no están en la sindicación ATOM examinada.** Los ficheros de datos abiertos solo indican que el anuncio existe y su fecha. Para leer el contenido hay que localizar la página web de cada expediente y seguir el enlace al XML. Es posible automatizarlo (este estudio lo hizo con 579 obras), pero son más pasos y el proceso es más frágil. La especificación de sindicación v1.10 (17/09/2024) no documenta el anuncio.
3. **Su presencia es muy baja.** Entre las obras observables en el corpus 2023–octubre de 2026 con fin teórico estimado en 2024, lo tiene el **0,69 %**; en 2025, el **0,48 %**. En la cohorte adjudicada desde 2023, que el corpus observa desde su adjudicación, las proporciones son casi iguales: 0,67 % y 0,47 %. De los 4.370 órganos con obras de fin teórico en 2024–2025, **198** lo han usado alguna vez en obras.
4. **El clasificador del estudio no encuentra coincidencias en el 98,4–99,4 % de esas obras** (sin `DOC_CCN` vigente y sin nombres o etiquetas de documentos de recepción, liquidación, certificación final, fin de obra o resolución en los campos examinados). Es el mismo orden que el 98,7 % del estudio, ahora para obras de cualquier importe. **No es una prevalencia de información inexistente:** el clasificador solo se validó a mano en la población del estudio, y no examina el contenido de los adjuntos ni otros canales. *(Cifras con la v2.3 del clasificador. La v2.4 lee además el fin comunicado en la nota de las modificaciones y, en la cohorte del estudio, baja del 98,7 % al 97,2 %; véase `investigacion_modificaciones/INFORME_MODIFICACIONES.md`.)*
5. En las 577 obras con anuncio, **633 contratos**:
   - **181 (28,6 %) llevan un código de causa de resolución** y 452 no lo llevan. Por los documentos anexos, al menos 20 de estos últimos también parecen resoluciones, así que la proporción con indicios de resolución está entre el **29 % y el 32 %**. Es una proporción **entre quienes publican**, no una tasa de resolución de las obras.
   - **Duración real frente a la prevista de cada contrato** (inicial o tras su última modificación, todo del mismo XML): mediana de **+12 días**, cuartiles de −6 a +112; el 61 % dura más de lo previsto y el 15 %, más de 180 días de más. Es una **diferencia entre fechas declaradas**, no un incumplimiento de plazo demostrado.
   - **Del fin real al anuncio:** mediana de 354 días en conjunto, pero muy influida por publicaciones retrospectivas de contratos antiguos. En los contratos adjudicados desde 2023 la mediana es de **64 días**.
6. **El importe pagado no permite medir sobrecostes sin conciliarlo con otras fuentes.** En los contratos sin código de causa suele coincidir con el adjudicado **con IVA** (mediana pagado / adjudicado con IVA = 1,00). En los resueltos vale 0 en el 57 % de los casos, lo que puede ser real (contratos rotos antes de cualquier pago).
7. **Antecedente:** la OIReScon (Informe Anual de Supervisión 2024, módulo XI, pp. 73–74) ya describe cómo siete plataformas autonómicas informan, o no, de la finalización y el coste final. Este estudio no descubre el tema: **cuantifica de forma reproducible la presencia y el contenido de `DOC_CCN` en la plataforma estatal**, que ese módulo no trata.
8. **Recomendaciones para la §8.6** (§5): incluir el contenido del anuncio en la sindicación y documentarlo; estudiar su uso sistemático; y dar criterios de cumplimentación del importe pagado.

---

## 1. Qué es el anuncio

- **Código:** `DOC_CCN` en la lista `TenderingNoticeTypeCode` 2.11. La misma lista prevé su anulación (`ANUL_CCN`).
- **Uso observado:** 2 casos sueltos en 2023 y uso continuado desde mayo de 2024.
- **Documento oficial** (`ContractCompletionNotice`, CODICE 2.8). Para cada contrato (`TenderResult/Contract`, con identificador propio) incluye:
  - `ActualDurationPeriod`: fechas reales de inicio y fin;
  - `ContractTermination`: fecha y, en las resoluciones, la causa (`TerminationReasonCode`) y una explicación;
  - `AggregatedAmount`: `PaidAmount`, a veces con `PaidAmountDescription`, y penalidades;
  - las modificaciones del contrato (`ContractModification`, vinculadas por `ContractID`) con su duración e importe finales;
  - los documentos anexos (`MinutesDocumentReference`), como el acta de recepción o el acuerdo de resolución.

  También incluye datos de contacto de los adjudicatarios. **Este estudio no los extrae ni los publica.**
- **En la sindicación** (ficheros ATOM) solo aparecen el tipo, el medio y la fecha del anuncio, sin enlace al documento. Un expediente con varios lotes puede tener un solo anuncio en la sindicación y uno por lote en la web (comprobado en 2 casos).

## 2. Método

| Paso | Qué se hace | Programa |
|---|---|---|
| 1 | Un **único** recorrido de los 13 ZIP de la PLACSP (2023 a octubre de 2026, los mismos del estudio). Fija el **estado final de cada expediente** con la misma política que el estudio (`medir_ejecucion.py` v2.3): última `updated`; empates resueltos con la regla determinista del estudio; exclusión de los borrados `ANULADA` o sin tipo posteriores a la última versión. De ese estado salen **a la vez** el denominador (todas las obras) y la lista de expedientes con `DOC_CCN` vigente | `escanear.py` (7 pruebas en `test_escanear.py`) |
| 2 | Descarga, desde la web de la PLACSP, del XML de cada anuncio de las obras con `DOC_CCN` vigente, a una petición cada 1,5 s | `descargar_ccn.py` |
| 3 | Lectura de los XML: una fila por contrato, con su identificador, lote, fechas, modificaciones, causa, importes y anexos; manifiesto con la huella SHA-256 de cada XML | `leer_xml.py` |
| 4 | Análisis con sensibilidades | `analizar_v2.py` |

**Comprobaciones de coherencia:**
- La selección corregida da **las mismas 579 obras** con anuncio que la versión 1 y 2.582 expedientes de cualquier tipo (uno menos que en la versión 1).
- Ningún empate de versiones discrepa sobre la presencia del anuncio.
- Sobre el mismo estado final, la población del estudio se reconstruye con las mismas cifras: **1.651 expedientes, 8 con anuncio**.

**Unidades:** la proporción se calcula por **expediente** y el contenido, por **contrato**. Las 639 filas leídas incluyen 6 repeticiones exactas del mismo contrato en dos anuncios (se conserva la más reciente), así que quedan **633 contratos**. En 2 claves (expediente, contrato, lote) siguen apareciendo dos filas con datos distintos y se conservan las dos.

**Universo de la proporción:** obras (código 3) en estado ADJ o RES, con al menos un resultado de adjudicación, **presentes en el corpus 2023–2026**, con fin teórico estimado anterior al corte (29/10/2026): 89.030 obras en total.

## 3. Resultados

### 3.1 Expedientes con anuncio (todos los tipos)

| | Expedientes |
|---|---:|
| Con `DOC_CCN` en su estado final | 2.582 |
| — servicios | 1.092 |
| — suministros | 766 |
| — **obras** | **579** |
| — otros tipos | 145 |
| Con alguna anulación (`ANUL_CCN`) | **0** |

Por mes de primer anuncio: de unos 50 al mes a finales de 2024 a entre 80 y 220 al mes en 2026. Lo han usado 517 órganos; 295 en un solo expediente y uno solo en el 22 %.

### 3.2 Proporción con anuncio en obras

**Proporción dentro de las obras observables en el corpus 2023–2026, con fin teórico estimado anterior al corte:**

| Año del fin teórico | Obras observables | Con `DOC_CCN` | % | Sin coincidencia del clasificador | Cohorte adjudicada desde 2023: obras | % con `DOC_CCN` | Sin coincidencia |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2023 | 15.596 | 71 | 0,46 % | 98,4 % | 11.995 | 0,32 % | 99,1 % |
| 2024 | 18.356 | 126 | 0,69 % | 98,8 % | 17.788 | 0,67 % | 98,8 % |
| 2025 | 20.640 | 99 | 0,48 % | 99,0 % | 20.438 | 0,47 % | 99,0 % |
| 2026 (hasta el corte) | 18.778 | 54 | 0,29 % | 99,4 % | 18.668 | 0,28 % | 99,4 % |

Cómo leer la tabla:
- **Truncamiento por la izquierda.** El corpus solo contiene expedientes con alguna publicación desde 2023. Una obra adjudicada antes que no se haya actualizado desde entonces no está, y publicar un anuncio es precisamente una actualización. Eso puede **inflar** la proporción en las cohortes antiguas. La cohorte adjudicada desde 2023, observada desde su adjudicación, no tiene ese sesgo. Para 2024–2026 da prácticamente lo mismo (el 97–99 % de esas obras se adjudicó desde 2023); para 2023 la proporción baja de 0,46 % a 0,32 %.
- **Censura reciente.** En 2026, muchas obras no han tenido tiempo de publicar el anuncio.
- **El fin teórico es una estimación** con las fechas y duraciones publicadas, no la fecha contractual real.
- **«Sin coincidencia del clasificador»** significa que no hay `DOC_CCN` vigente ni coincidencias en los códigos, nombres y etiquetas de documentos de la sindicación examinada. El clasificador se validó a mano solo en la población del estudio (obras de 1–10 M€ adjudicadas en 2023), con 21 casos negativos. **Su validez en otros importes y años está pendiente**, y la cifra no demuestra que la información no exista.

**Por importe** (fin teórico 2024–2025): menos de 1 M€, 0,56 %; de 1 a 10 M€, 0,72 %; más de 10 M€, 0,90 %.

**Por órgano:** de los 4.370 órganos con obras de fin teórico en 2024–2025, 198 (4,5 %) han usado el anuncio en obras. De los 210 que lo han usado en obras, 143 lo hicieron en un solo expediente, y **uno concentra 145 de los 577 expedientes** con XML leído. En ese órgano, 162 de sus 164 contratos se adjudicaron antes de 2023 y no llevan código de causa: parece una publicación retrospectiva de contratos antiguos.

### 3.3 Cómo terminaron los contratos anunciados (633 contratos)

| Indicador en el XML | Contratos | Anexo de recepción, liquidación o certificación | Anexo de resolución |
|---|---:|---:|---:|
| Con código de causa de resolución | 181 (28,6 %) | 15 | 117 |
| `ContractTermination` sin código | 11 | 4 | 5 |
| Sin `ContractTermination` | 441 | 89 | 15 |

Lo que permite y lo que no permite decir:
- **Que falte el código de causa no prueba un cumplimiento satisfactorio.** En la mayoría de los casos con anexo, el anexo es de recepción, liquidación o certificación. Pero 20 contratos sin código tienen un anexo de resolución, y el 69 % de los que no tienen `ContractTermination` no tienen anexo.
- La proporción con **indicios de resolución** está entre el 28,6 % (solo código) y el 32 % (código o anexo de resolución).
- Es una proporción **condicional a haber publicado el anuncio**, no una tasa de resolución de las obras.

**Causas de resolución consignadas** (181): mutuo acuerdo, incumplimiento de la obligación principal, demora del contratista, imposibilidad de ejecutar en los términos pactados, desistimiento, demora en la comprobación del replanteo y suspensiones de más de 4 u 8 meses, por este orden de frecuencia.

### 3.4 Duración real frente a prevista

Medida dentro del **mismo documento oficial y para cada contrato**: duración real (de `ActualDurationPeriod/StartDate` a `EndDate`) menos duración prevista (la del proyecto o, si existe, la final de la última modificación de **ese** contrato).

| Subconjunto | n | Mediana | Cuartiles | Dura más de lo previsto | Más de 180 días de más |
|---|---:|---:|---:|---:|---:|
| Todos | 633 | +12 días | −6 a +112 | 61 % | 15 % |
| Sin código de causa | 452 | +15 | −2 a +92 | 63 % | 13 % |
| Con código de causa | 181 | +1 | −40 a +154 | 54 % | 20 % |
| Adjudicados desde 2023 | 330 | +6 | −12 a +101 | 57 % | 13 % |
| Sin el órgano con más contratos | 469 | +10 | −8 a +126 | 59 % | 16 % |
| Sin modificaciones ni suspensiones | 564 | +8 | −7 a +92 | 59 % | 13 % |

- **La versión 1 daba +57 días** porque restaba el fin teórico **del expediente** al fin real **del contrato**, con fechas de inicio que a menudo no coinciden. Esa métrica queda retirada.
- **Sigue siendo una diferencia entre fechas declaradas**, no un retraso contractual demostrado. La duración prevista del XML es la del proyecto, sin las prórrogas que no consten como modificación (35 contratos declaran un número de prórrogas) ni las suspensiones (7 contratos).
- En las resoluciones la diferencia es más dispersa porque el contrato se interrumpe.

### 3.5 Del fin real al anuncio

| Subconjunto | n | Mediana | Cuartiles |
|---|---:|---:|---:|
| Todos | 633 | 354 días | 40 – 1.702 |
| Adjudicados desde 2023 | 330 | **64 días** | 11 – 239 |
| Sin el órgano con más contratos | 469 | 134 días | 15 – 538 |
| Anuncios publicados en 2026 | 334 | 1.040 días | 82 – 2.036 |

La mediana global refleja sobre todo **publicaciones retrospectivas**. No describe el plazo habitual de quien publica hoy un anuncio de un contrato reciente (64 días en mediana en la cohorte desde 2023), y de ella no se deduce ningún plazo que deba imponerse.

### 3.6 Importe pagado

| | Sin código de causa (452) | Con código de causa (181) |
|---|---:|---:|
| `PaidAmount` = 0 | 12 (2,7 %) | 103 (56,9 %) |
| = adjudicado sin IVA | 45 | 0 |
| = adjudicado con IVA (`PayableAmount`) | 189 | 4 |
| = importe final tras modificación (sin / con IVA) | 6 / 10 | 0 / 0 |
| Otro valor | 190 | 74 |
| Con `PaidAmountDescription` (mencionan el IVA) | 85 (36) | 56 (11) |

- En los contratos sin código de causa, **el pagado suele coincidir con el adjudicado con IVA**: la mediana pagado / adjudicado con IVA es 1,00, con cuartiles de 1,00 a 1,06. Una parte lo da sin IVA. Los «otros valores» pueden deberse a modificaciones, revisiones de precios, pagos parciales o bases distintas.
- **Los ceros se concentran en las resoluciones** y pueden ser reales: contratos rotos antes de cualquier pago. No hay base para tratarlos como errores.
- **Conclusión:** el campo no permite medir sobrecostes sin conciliar la base fiscal (con o sin IVA), las modificaciones y su significado contable.

## 4. Antecedentes

- **OIReScon, Informe Anual de Supervisión 2024, módulo XI, pp. 73–74**: compara cómo siete plataformas autonómicas (Navarra, País Vasco, La Rioja, Galicia, Cataluña, Madrid y Andalucía) permiten publicar la ejecución y la finalización del contrato y si avisan de su conclusión y coste final. Navarra, por ejemplo, dispone de un anuncio de finalización. El módulo no trata la plataforma estatal en este punto. https://www.hacienda.gob.es/RSC/OIReScon/informe-anual-supervision-2024/ias2024-modulo11.pdf
- **Especificación de sindicación y reutilización de la PLACSP, v1.10 (17/09/2024)**: no documenta `DOC_CCN`. https://contrataciondelsectorpublico.gob.es/datosabiertos/especificacion-sindicacion.pdf
- **Ley 9/2017 (LCSP), art. 346.3 y 346.5**: comunicación al Registro de Contratos del Sector Público de, entre otros datos, el importe final y la extinción, y acceso público a los datos no confidenciales. https://www.boe.es/eli/es/l/2017/11/08/9/con

## 5. Recomendaciones para la §8.6

Son **recomendaciones**, que pueden necesitar desarrollo técnico y una valoración jurídica:

1. **Incluir el contenido del anuncio en la sindicación de datos abiertos** (fechas reales, causa, importe, identificador de contrato y lote) y documentarlo en la especificación. Es la que mejor se apoya en los datos: el formato ya existe y la sindicación no lo transporta.
2. **Estudiar el uso sistemático del anuncio** al terminar los contratos. Si debe ser obligatorio, y en qué plazo, es una cuestión jurídica que este estudio no resuelve.
3. **Dar criterios de cumplimentación del importe pagado** (con o sin IVA, tratamiento de las modificaciones). No se propone prohibir el valor 0, que puede ser correcto.

## 6. Límites

- **Sesgo de selección:** solo se ve a quien publica. Los porcentajes de §3.3 a §3.6 no describen las obras en general.
- **Truncamiento y censura:** ver §3.2.
- **Clasificador por nombre:** sin validación manual fuera de la población del estudio.
- **Duración prevista:** la del proyecto o la de la última modificación publicada, sin prórrogas ni suspensiones no registradas como modificación.
- **Fechas:** se usa el día tal como figura en la fuente, sin ajustar el desfase horario. Ninguna conclusión depende de diferencias de un día.
- **Extracción web:** depende de la estructura de las páginas de la PLACSP. 2 de las 579 obras no mostraban el anuncio en su página al descargarlo (no fue un error HTTP); los 602 XML descargados son válidos.
- **Solo perfiles alojados en la PLACSP**, sin las plataformas autonómicas agregadas.
- **Sin revisión** jurídica ni estadística.

## 7. Correcciones tras la revisión adversarial de ChatGPT (versión 1 → versión 2)

| Punto | Objeción | Qué se ha hecho | Efecto |
|---|---|---|---|
| A | Truncamiento por la izquierda; universo mal titulado | Universo redefinido como «obras observables en el corpus»; cohorte adjudicada desde 2023 | 2024–2026 casi iguales; 2023 baja de 0,46 % a 0,32 % |
| B | El extractor filtraba antes de elegir la última versión, sin borrados ni regla de empates | Recorrido único con la política del estudio; 7 pruebas (anuncio retirado, borrado posterior, empate, independencia del orden…) | Mismas 579 obras; 2.582 frente a 2.583 en todos los tipos; 0 empates discrepantes |
| C | «Sin ningún indicador» fuera de la población validada | Reformulado como «sin coincidencia del clasificador»; validación fuera del estudio declarada pendiente | Redacción |
| D | Retraso calculado con fechas de distinto nivel | Nueva métrica por contrato dentro del mismo XML, con las modificaciones de ese contrato | **+57 días → +12 días** (mediana) |
| E | «Cumplimiento» deducido de la ausencia de código | «Con / sin código de causa», contraste con los anexos | 28,6 % con código; 29–32 % con indicios de resolución |
| F | 29 % frente a 51 % no comparables | Comparación retirada | — |
| G | «Pagado no fiable» demasiado fuerte | Comparación con el adjudicado con IVA (`PayableAmount`); ceros separados por tipo | La mayoría coincide con el adjudicado con IVA; ceros sobre todo en resoluciones |
| H | Mediana de 354 días dominada por publicaciones retrospectivas | Sensibilidad por cohorte y por año del anuncio | 64 días en la cohorte desde 2023 |
| I | «No se puede reutilizar masivamente» demasiado absoluto | «Sus campos no están en la sindicación examinada; recuperarlos exige más pasos» | Redacción |
| J | Rutas fijas, descarga no auditable, sin identificador de contrato | Rutas relativas y argumentos; registro con URL, HTTP, hora y SHA-256; reintento de errores; manifiesto de los 602 XML; `Contract/ID` y lote | — |
| — | Antecedente de la OIReScon | Citado (§4), comprobado en la fuente | Delimita la novedad |

## 8. Reproducción

```
python -m unittest -v test_escanear                 # 7 pruebas
python escanear.py                                   # ~3,5 min; obras_estado_final.csv y ccn_todos_tipos.csv
python -I descargar_ccn.py                           # ~40 min, pausado; xml_anuncios/
python -I -X utf8 leer_xml.py                        # contratos_ccn.csv y manifiesto_xml.csv
python -X utf8 -I analizar_v2.py
```

Los ZIP se obtienen con `descargar_datos.py` del estudio, que comprueba sus huellas. Los XML de la web pueden cambiar o desaparecer: `manifiesto_xml.csv` guarda la huella de los descargados el 01/11/2026. En esa primera descarga no se registraron el código HTTP ni la hora de cada documento; el programa actual sí lo hace. Los XML contienen datos de contacto de los adjudicatarios: **no deben redistribuirse tal cual**.
