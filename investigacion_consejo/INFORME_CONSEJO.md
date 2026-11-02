# Rama 5: ¿qué pasa cuando se pide el fin de una obra por la vía de acceso?

**1 de noviembre de 2026. Exploratorio. Lectura de resoluciones por un no jurista; no lo ha revisado ningún jurista.** Complementa la rama 4 (`investigacion_juridica/INFORME_JURIDICO.md`), según la cual publicar el fin de un contrato no es obligatorio, pero el acta de recepción y la certificación final existen por ley y son información pública.

**Preguntas:**
1. Cuando alguien pide documentos de la ejecución o del fin de una obra, ¿los reconoce el Consejo de Transparencia y Buen Gobierno (CTBG)?
2. ¿Con qué frecuencia la Administración no contesta, cuánto tarda el Consejo y se cumplen sus resoluciones?

**Ámbito:** solo resoluciones de **ámbito estatal**, es decir, frente a la Administración General del Estado y el sector público estatal. Las comunidades autónomas y los ayuntamientos tienen sus propios órganos de garantía, que no se han revisado. **No se nombra ni se compara a ningún organismo**; las resoluciones se citan por su número, que es público, como precedentes de un criterio jurídico, no como lista de casos.

## Respuesta corta

1. **Cuando el documento existe y se pide al organismo que lo tiene, el Consejo reconoce el acceso**, y en los casos revisados la Administración cumplió. El Consejo ha dicho que el acta de recepción tiene «carácter eminentemente público» (R CTBG 2024-0107) y que la ciudadanía puede controlar la contratación «en cualquiera de sus fases», también en la ejecución (R/0526/2020).
2. **Las negativas revisadas tienen motivos identificables:** el documento no existía o lo tenía otro organismo; se pidió antes de que existiera; hubo un error de trámite; o se consideró **abuso de derecho** por pedir de forma repetida y sistemática documentos parciales de una misma obra. En este último caso el Consejo señaló que se habría obtenido lo mismo pidiendo **una vez** la certificación final (R/0863/2021, que cita R/0271/2021 y R/0342/2021).
3. **El silencio es la primera causa de reclamación.** Entre 2019 y 2026, el 34–46 % de las reclamaciones de ámbito estatal resueltas cada año se presentaron por falta de respuesta. En 2021–2026, entre un 29 % y un 39 % de ellas terminaron en «estimatoria por motivos formales»: la Administración entregó la información, pero solo después de que se reclamara ante el Consejo.
4. **El Consejo tarda más de lo que marca la ley.** El plazo legal es de tres meses, y la mediana fue de 4 a 7 meses en 2021–2024 y de 3 meses en 2025. Según el propio Consejo, a 30/09/2026 constaban como **cumplidas el 86–88 %** de sus resoluciones estimatorias de 2023–2025.

**Lectura para el protocolo.** La vía funciona para este tipo de documento, pero es lenta y se activa caso a caso. Una solicitud de acceso, si sale bien, beneficia solo a quien la presenta, salvo que la respuesta se haga pública. Lo que el Consejo penaliza, pedir de forma masiva y repetitiva, es justo lo que el protocolo evitaría: **una pregunta por obra, sobre el documento final, una sola vez, con la respuesta o el silencio a disposición de todos.**

## 1. Resoluciones sobre la ejecución o el fin de contratos

**Cómo se seleccionaron:**
- El Consejo publica un Excel con todas sus resoluciones de ámbito estatal (`ResolucionesAE.xlsx`, actualizado el 09/10/2026): 11.199 resoluciones de 2015 a 2026, con el asunto en una línea, materias y palabras clave.
- `analizar_excel.py` marca 1.226 resoluciones sobre contratos y, de ellas, 29 cuyo asunto menciona la ejecución o el fin: recepción, certificación, liquidación, modificado, sobrecoste, prórroga, facturas, finalización, etc. La lista está en `ejecucion_candidatas.csv`.
- Se descartaron a mano las 16 que solo pedían facturas o datos de servicios sin relación con el fin, y se añadió R/0526/2020, que trata de actas de recepción aunque su asunto no lo diga.
- De las 14 resultantes no se pudieron leer tres: R CTBG 2025-0591 no figura en el índice de PDF de la web, y R/0046/2016 y R/0434/2016 son PDF escaneados sin texto. Quedan **11 leídas**.

| Resolución | Qué se pedía (genérico) | Sentido | Motivo principal | Cumplimiento (seguimiento del CTBG, 30/09/2026) |
|---|---|---|---|---|
| R CTBG 2024-0107 | Acta de recepción de una obra e informes de comprobación | Estimatoria | El acta tiene «carácter eminentemente público» (art. 243.2 LCSP); un expediente abierto no impide el acceso a documentos terminados | Cumplida |
| R CTBG 2024-0792 | Fecha de recepción, fecha de aprobación de la liquidación y valoración final de un contrato | Estimatoria por motivos formales | La información se completó ya iniciada la reclamación, fuera de plazo | — (formal) |
| R/0609/2021 | Fecha de recepción de un suministro y motivo del retraso | Estimatoria | Información pública; no se invocó ningún límite | Cumplida |
| R/0548/2017 | Fechas de finalización de concesiones | Estimatoria | Información pública | Cumplida |
| R/0392/2016 | Copias de las certificaciones de dos obras | Estimatoria | No basta con ofrecer consulta presencial en una oficina lejana | Cumplida |
| R/0526/2020 | Actas de recepción, presupuestos y facturas de un contrato de servicios | Estimatoria parcial | Las actas se entregaron durante la reclamación; control ciudadano «en cualquiera de sus fases» | Cumplida |
| R CTBG 2025-1472 | Documentación del cumplimiento de la LCSP y liquidación de una obra | Estimatoria (retroacción) | La liquidación la tenía otra entidad: el organismo debía remitirle la solicitud (art. 19.1 LTAIBG) | Cumplida |
| R/0148/2019 | Certificaciones y facturas de una obra | Desestimatoria | Se entregó todo lo existente a la fecha de la solicitud; lo posterior no era exigible | — |
| R/0863/2021 | Carátulas de certificaciones mensuales (con fecha de terminación) de varias obras | Desestimatoria | Abuso de derecho (art. 18.1.e): solicitudes repetidas sobre la misma obra desde 2018 | — |
| R/0198/2021 | Certificaciones completas de cuatro obras | Inadmitida | Se reclamó contra el acuerdo de ampliación de plazo, que no es recurrible | — |
| R/0003/2021 | Un proyecto modificado | Desestimatoria | El documento no consta en poder del organismo | — |

**Citas literales:**
- R CTBG 2024-0107, FJ 5: «el carácter eminentemente público de la información solicitada en la medida en que se trata de un documento emitido por la Administración como constatación de la correcta realización de las obras contratadas».
- R/0526/2020: «desde la entrada en vigor de la LTAIBG, la ciudadanía puede efectuar ese control sobre la contratación del sector público, en cualquiera de sus fases». La misma resolución constata que las actas de recepción, presupuestos y facturas «no son objeto de publicación, por no exigirlo así» la Ley 19/2013 ni la LCSP. Coincide con la rama 4.
- R/0863/2021, que reproduce R/0271/2021 y R/0342/2021: el reclamante «habría obtenido la misma información si llegado el momento hubiera pedido la certificación final de las obras, en lugar de ejercer el derecho de acceso de manera reiterada y sistemática sobre certificaciones parciales».

**Plazos de un caso:** en R CTBG 2024-0107, la solicitud es de abril de 2023, la respuesta del organismo de junio (el plazo legal es de un mes), la reclamación de julio y la resolución del Consejo de enero de 2024. Pasaron **unos nueve meses** desde la pregunta hasta la orden de entregar el acta.

## 2. Silencio, tardanza y cumplimiento

**Reclamaciones por silencio** (`analizar_excel.py`, sección 1). Año de resolución; porcentajes sobre las resoluciones de ese año y, en las dos últimas columnas, sobre las de silencio:

| Año | Resoluciones | Por silencio | Estimatoria por motivos formales | Estimatoria (total o parcial) |
|---|---:|---:|---:|---:|
| 2019 | 903 | 39,5 % | 21,8 % | 27,7 % |
| 2020 | 893 | 45,9 % | 16,3 % | 33,7 % |
| 2021 | 910 | 41,5 % | 29,9 % | 24,1 % |
| 2022 | 996 | 33,7 % | 32,7 % | 38,1 % |
| 2023 | 1.151 | 33,8 % | 39,3 % | 27,0 % |
| 2024 | 1.530 | 42,2 % | 35,3 % | 36,2 % |
| 2025 | 1.565 | 45,6 % | 37,1 % | 35,4 % |
| 2026 (hasta sept.) | 1.028 | 40,0 % | 29,4 % | 36,3 % |

«Estimatoria por motivos formales» es la que se dicta cuando la información se entrega durante la reclamación. En palabras de R CTBG 2024-0792, se da «al no haberse respetado el derecho del solicitante a acceder a la información completa en el plazo máximo legalmente establecido, habiendo sido necesaria la interposición de una reclamación».

**En contratos** (1.226 resoluciones de 2015–2026), el 35,9 % de las reclamaciones fueron por silencio, frente al 37,9 % del total, y el 20,1 % acabaron en estimatoria por motivos formales, frente al 17,8 % del total.

**Tiempo de resolución del Consejo** (sección 3, aproximado por meses naturales entre la entrada y la resolución; el plazo legal es de tres meses, art. 24.4 LTAIBG): la mediana fue de 2–3 meses en 2015–2020, 4 en 2021, 6 en 2022, 7 en 2023, 4 en 2024, 3 en 2025 y 4 en 2026. La proporción con una diferencia de cuatro o más meses fue del 63 % (2021), 93 % (2022), 93 % (2023), 78 % (2024), 46 % (2025) y 63 % (2026).

**Cumplimiento** (página oficial del Consejo, estado a 30/09/2026 de las resoluciones dictadas hasta el 30/06/2026; `fuentes/cumplimiento_pagina_20261101.txt` y `Seguimiento_AGE.xlsx`). «Cumplida» significa que el destinatario ha comunicado al Consejo que la cumplió, no que el Consejo lo haya verificado.

| Año | Cumplida | No consta cumplimiento | Contencioso |
|---|---:|---:|---:|
| 2022 | 83,5 % | 10,1 % | 6,4 % |
| 2023 | 87,1 % | 6,8 % | 6,1 % |
| 2024 | 87,8 % | 7,7 % | 4,5 % |
| 2025 | 86,2 % | 10,4 % | 3,4 % |

**Volumen** (boletín estadístico del Portal de la Transparencia de la AGE, enero de 2026, datos acumulados desde diciembre de 2014): 96.029 solicitudes de acceso, de las que el 62,3 % de las finalizadas terminó en concesión y el 21,6 % en inadmisión; 9.382 reclamaciones de ámbito estatal finalizadas por el Consejo hasta el 30/06/2025, aproximadamente una por cada diez solicitudes; y 1.616 expedientes (1,68 %) «en silencio administrativo» en el momento del recuento. El boletín no informa de cuántas solicitudes se contestaron en plazo.

## Qué cambia y qué no

- **Para el documento:** respalda con resoluciones concretas que la información que el estudio no encuentra publicada **puede obtenerse** por la vía de acceso, y que el Consejo la considera pública. También documenta el coste de esa vía: retrasos, reclamaciones necesarias para obtener respuesta y meses de espera.
- **Para el diseño del protocolo** (pendiente de valorar en la revisión final):
  - preguntar por el **documento final** (acta de recepción, certificación final o liquidación) y no por documentos parciales periódicos;
  - **una sola pregunta por obra** y no repetirla, porque la repetición sistemática se ha considerado abusiva;
  - dirigirla al órgano de contratación y, si no tiene el documento, esperar a que la remita a quien lo tenga (art. 19.1);
  - preguntar solo cuando el fin teórico ya ha vencido, porque lo que no existía en la fecha de la solicitud no es exigible;
  - y **registrar el resultado**: respuesta, silencio, reclamación y cumplimiento.
- **Un riesgo que antes no estaba documentado:** si una sola entidad enviara muchas solicitudes, aunque sean una por obra, podría tratarse como abusiva. Las resoluciones revisadas aprecian el abuso por la repetición sobre **la misma obra**, no por el número de obras distintas, pero este punto **no está resuelto** y requiere criterio jurídico.

## Límites

- **Solo ámbito estatal** y solo resoluciones del Consejo; no se ha consultado jurisprudencia de los tribunales ni las resoluciones de los órganos autonómicos.
- **La selección de casos depende del asunto resumido en el Excel**, que es una línea. Puede haber resoluciones sobre actas de recepción o liquidaciones con asuntos genéricos, como «expediente de contratación», que no se han detectado. No se han descargado ni leído las 1.226 resoluciones sobre contratos.
- **Once resoluciones leídas** no permiten hablar de una doctrina consolidada; sí muestran un criterio repetido.
- **Las cifras de silencio se refieren a reclamaciones, no a solicitudes:** no dicen qué parte de las solicitudes queda sin respuesta, solo qué parte de las reclamaciones se debe al silencio. La mayoría de quienes no reciben respuesta probablemente no reclaman.
- **El tiempo de resolución es aproximado,** calculado por meses naturales, y no descuenta las suspensiones de plazos de 2020.
- **«Cumplida» se basa en la comunicación del propio destinatario.**
- Las hojas del Excel cambian de columnas entre años; la armonización (`analizar_excel.py`, `EQUIV`) puede clasificar mal algún caso límite. En los asuntos del Excel aparecen a veces nombres de empresas o de personas; no se reproducen aquí.

## Reproducción

```
uv run --with openpyxl python -I -X utf8 analizar_excel.py   # resoluciones.csv, ejecucion_candidatas.csv y resumen
python -I -X utf8 indexar_pdf.py                            # indice_pdf.csv (≈140 páginas, 1 petición/s)
uv run --with pypdf python -I -X utf8 pdf_a_txt.py           # texto de los PDF de fuentes/pdf
```

**Fuentes** (descargadas el 01/11/2026 de consejodetransparencia.es y transparencia.gob.es):

| Fichero | Bytes | SHA-256 |
|---|---:|---|
| `fuentes/excel/ResolucionesAE.xlsx` | 2011618 | e85539b5655d1882c28d94e1ebfe2ce23b3bfd47b01d0b4faf58f39b8ca32326 |
| `fuentes/excel/Seguimiento_AGE.xlsx` | 978031 | 69610bab2b41b14e4b1df4ad7d0c6c4aa7c80592df30c7f1ceb24c3bebad250c |
| `fuentes/pdf/portal_boletin_2026_01.pdf` | 4065787 | 5206934f9159d62c0a682cedc54de8924b5bdde1bac8f28e3dad0550af23cf96 |
| `fuentes/pdf/R-2024-0107.pdf` | 210758 | 5d73db46c999fc9e94e13831f8a2de705ac04a5c49c97f7eeb75846a4e10b5e1 |
| `fuentes/pdf/R-2024-0792.pdf` | 202367 | ffaad60a44cc121d0d4866b110565e4e28d527af42c05dffe857dd3805d6609a |
| `fuentes/pdf/R-2025-1472.pdf` | 171990 | 9f1c691f92525e1d80fd61d82fc1c2ec289e5ad39a3fdb7b66487827092b10a4 |
| `fuentes/pdf/R-0609-2021.pdf` | 175990 | 2439e77048c2cb68f9de831674b361533cdfce043183478b4747f68c603f8c94 |
| `fuentes/pdf/R-0548-2017.pdf` | 408770 | a7ee309151d2104c15c795db8c56e260ab1dd2f8d214f62a2ba3cbdd055d1c40 |
| `fuentes/pdf/R-0392-2016.pdf` | 94646 | 73f167bedfe09ea61eee7c424a89df19d9b709f3ed99865221bfe21dad952ae8 |
| `fuentes/pdf/R-0526-2020.pdf` | 238789 | 2f5024a08cff76770b5649632556682b53b9350bf380d74cdd6a40803beeaa9c |
| `fuentes/pdf/R-0148-2019.pdf` | 133271 | cee638583e8789b69b88807ebb7a05086181e88cbc0ef69b792b017b0f3c4e86 |
| `fuentes/pdf/R-0863-2021.pdf` | 209192 | 20da34d877fbf29fd11c931d10bc39f4df837458b66b90468a7b7ab689e39228 |
| `fuentes/pdf/R-0198-2021.pdf` | 201278 | 3ad746cbcd70a166eb0f38d627dc538a1b4f330716265bb7445e7f49c058ec37 |
| `fuentes/pdf/R-0003-2021.pdf` | 224402 | 5085f63fde1c10bd4976a778611312ef7896e23e302a534d201fe9b57c152b11 |
| `fuentes/pdf/R-0046-2016.pdf` (escaneado, sin leer) | 1847299 | 1fea897cfd6a8b6e7b96fda165db65685a1e30134fec5da3c494fdb51e9b2653 |
| `fuentes/pdf/R-0434-2016.pdf` (escaneado, sin leer) | 2981568 | 4d975de71adf9e560b18c4f4fe294633c650760790526b45ad7d6f0bc4e758b6 |

Las resoluciones son documentos públicos y ya anonimizados por el Consejo. Antes de redistribuir copias, conviene comprobar que no contienen datos personales y, en su caso, enlazar a la web del Consejo en lugar de copiarlas.

## Tras la revisión adversarial (02/11/2026)

- **Once resoluciones** muestran un criterio visible en casos concretos, no una doctrina general ni una garantía de acceso. Conviene hablar de «resoluciones examinadas».
- **Las cifras de silencio tienen como denominador las reclamaciones,** no las solicitudes; no permiten inferir cuántas solicitudes quedan sin respuesta en España.
- **«Estimatoria por motivos formales»** está documentada en el caso citado (entrega durante la reclamación), pero no todas sus variantes tienen por qué ser idénticas.

## Ámbito autonómico (añadido el 02/11/2026; revisado tras la revisión adversarial de la v0.4.5)

En el escenario de `protocolo_obras/volumen.py`, el 58 % de las solicitudes potenciales del protocolo (1.065 de 1.839 al año) corresponde a administraciones cuyo órgano de garantía podría ser autonómico, si se llegara a reclamar y se confirmara la competencia; no es una proporción de reclamaciones. Una búsqueda complementaria (`COMPLEMENTO_AUTONOMICO.md`, reproducible con `filtrar_autonomicos.py`), hecha con términos fijados antes de descargar en los datos abiertos de dos órganos autonómicos (6.641 y 13.762 resoluciones), da:
- **Muy pocos asuntos sobre documentación del fin o la ejecución de obras públicas**, en sentido estricto: 2 y 7 (aparte, urbanizaciones, un suministro, un desistimiento y un caso dudoso).
- **Ninguna desestimación de fondo ni inadmisión** entre ellos. En uno de los órganos, 3 de los 7 terminaron por pérdida de objeto: la información se entregó solo tras reclamar. Mediana de 50 días.
- **Lecturas sueltas de otros órganos van en la misma dirección.** Las negativas vistas son por abuso tras accesos ofrecidos y no ejercidos, o por falta de concreción.
- **Los plazos dependen de la ley aplicable.** Para resolver: un mes en la mayoría, 20 días hábiles en Madrid, Murcia y la Junta de Andalucía, 30 días hábiles en Extremadura. Para reclamar contra el silencio: un mes en la mayoría; sin plazo según la ley en Cantabria, Navarra y el País Vasco; en Madrid, un mes según la ley (art. 48) y un criterio de no preclusión de su órgano de garantía (criterio de 09/10/2025, aplicado en la resolución 007/2026; verificado en `fuentes/autonomicos/`, copias no publicadas); Cataluña ofrece mediación. Detalle y citas del BOE: `protocolo_obras/regimenes.py`.

**Cautelas:**
- solo dos de unos diez órganos se revisaron de forma sistemática, y en uno solo se buscó en un resumen recortado;
- muchos solicitantes son cargos electos, con un derecho de acceso reforzado;
- la clasificación de cada caso es de un solo lector, a partir de los resúmenes; es una lectura de un no jurista, y solo dos citas se verificaron en el texto de la resolución.
