# Investigación exploratoria — Visibilidad de la ejecución de obras públicas en la sindicación de la PLACSP (programa v2.4)

**Pregunta:** ¿qué consta de la **ejecución** de las obras públicas (modificaciones, incidencias, recepción, liquidación, extinción) en la sindicación de datos abiertos de la Plataforma de Contratación del Sector Público?

**Relación con «Democracia Auditable» (v0.4.8, §8.6, §9.0 bis y §9.0 ter):** es la medición que pide la §8.6 («la cobertura real se mide en la fase 0 antes de afirmar nada»). El objetivo es **poner a prueba** esa hipótesis, no confirmarla.

**Estado (01/11/2026):** investigación **exploratoria** reproducible, programa v2.4. Corrige los errores señalados en cuatro rondas de revisión adversarial con ChatGPT (no son revisiones independientes: es siempre el mismo sistema), en una revisión de código con Gemini y en las revisiones manuales del autor. La v2.4 lee además el texto de las modificaciones publicadas, donde algunos órganos comunican la liquidación o la certificación final (ver «Hallazgo de la v2.4»). Leídos 2023, 2024, 2025 y enero–octubre de 2026 (corte de datos: 29/10/2026). **Pendiente:** nueva revisión independiente y una muestra amplia del estrato negativo.

## Qué mide la cifra, y qué no

Las cifras miden **la ausencia de coincidencias detectadas por el clasificador en este canal**. Es decir: ni un anuncio estructurado de finalización, ni un nombre de archivo o etiqueta documental, ni un texto de modificación que coincida con los patrones de fin. **No** miden la inexistencia de documentación de finalización, ni que la obra no haya terminado, ni que nadie incumpla una obligación.

## Resultado principal (corte 29/10/2026)

La unidad es el **expediente** (licitación), que puede contener varios lotes y contratos. Se seleccionan 1.651 expedientes de obras con la primera adjudicación en 2023 y un presupuesto base sin IVA de 1 a 10 M€. De ellos, 1.593 tienen un fin teórico estimado anterior al corte.

| Conjunto | Fin teórico anterior al corte | Sin evidencia de fin **definitivo** | Sin **ninguna** evidencia de fin |
|---|---:|---:|---:|
| **Principal** | 1.593 | **1.549 (97,2 %)** | 1.547 (97,1 %) |
| Un solo resultado adjudicado | 1.311 | 1.273 (97,1 %) | 1.272 (97,0 %) |
| Sin versiones empatadas | 1.573 | 1.529 (97,2 %) | 1.527 (97,1 %) |
| **Cotas por empates** (cualquier versión empatada) | 1.573–1.594 | 97,2 % en ambos extremos (1.529/1.573 – 1.550/1.594) | — |

- **Evidencia de fin definitivo:** el anuncio estructurado de finalización (`DOC_CCN`), un documento candidato de recepción definitiva, liquidación, certificación final, fin de obra o resolución del contrato, o (desde la v2.4) el texto de una modificación publicada que comunique la liquidación, la certificación final o la recepción de la obra.
- **Parcial o de avance:** recepción parcial, certificación de avance o resolución en trámite.

**Formulación propuesta:** «En la sindicación de los perfiles alojados en la PLACSP, consultada hasta el 29/10/2026, no se detectó ningún anuncio de finalización ni ningún nombre de archivo, etiqueta documental o texto de modificación coincidente con recepción, liquidación, certificación final, fin de obra o resolución del contrato en 1.549 de 1.593 expedientes de obras adjudicados en 2023 cuyo fin teórico estimado era anterior a esa fecha. La cifra mide coincidencias detectadas; no acredita que los documentos no existan, que la obra no haya concluido ni que no haya información en otros registros».

## Hallazgo de la v2.2: existe un anuncio estructurado de finalización, y en la población estudiada apenas aparece

Durante la revisión manual apareció en la web un **«Anuncio de finalización de contrato»**. En la sindicación es el tipo de anuncio `DOC_CCN` de la lista `TenderingNoticeTypeCode` 2.11. **No figura** en la especificación de sindicación v1.10 (17/09/2024) en la que se basaba el programa.

- En la sindicación (ATOM) solo trae el **tipo y la fecha** del anuncio.
- El documento enlazado desde la web (`ContractCompletionNotice`, CODICE 2.8) contiene la **fecha real de fin** (`ActualDurationPeriod/EndDate`), la **causa de extinción** (`TerminationReasonCode`) y el anexo (acta de recepción, orden de resolución…).
- **Uso:** 8 de los 1.651 expedientes seleccionados (0,5 %). En todas las obras de los datos, expedientes con este anuncio por año del anuncio: **88 en 2024, 198 en 2025 y 293 en 2026** (hasta octubre).

**Esto corrige una afirmación anterior del estudio.** No es cierto que el canal «no tenga sitio» para el final del contrato. Lo tiene desde 2024, como mínimo, pero se usa en una proporción muy pequeña de los expedientes. En la población seleccionada solo 8 de 1.651 expedientes lo tienen. Los recuentos globales por año son numeradores sin denominador comparable: muestran que el tipo de anuncio se usa, **no una tasa de uso ni de cumplimiento en toda España**. Tampoco se ha establecido si publicarlo es obligatorio. Para la §8.6, la conclusión pasa de «falta el campo» a «el campo existe; en esta población apenas aparece».

## Hallazgo de la v2.4: el fin también se comunica en el texto de las modificaciones

Algunos órganos publican la liquidación o la certificación final como si fueran una «modificación del contrato», con un texto como «Se formaliza la liquidación del contrato». Ese texto está en el campo `Note` de `ContractModification`, que la especificación de la sindicación (v1.3, 2020) no documenta y que la v2.3 no leía. La v2.4 lo lee en dos niveles: **confirmado** (cuenta como fin) solo si el texto completo es una fórmula breve de una lista cerrada («se formaliza la liquidación del contrato», «certificación final de obra»…), y **candidato** (se anota en `fin_en_nota_candidato`, no cuenta) si solo coincide un patrón amplio. Se excluyen recepciones parciales, liquidaciones de daños, penalidades o anticipos, liquidaciones provisionales o a cuenta, fases y lotes. En la población, **24 expedientes** sin otro indicio de fin tienen un texto confirmado y 2 un candidato; se revisaron a mano los 24 y todos son fines comunicados (`revision_manual_fin_en_nota_v2_4.csv`; uno es un expediente con varios lotes y el texto no dice a cuáles se refiere). La cifra principal pasa de 1.573 (98,7 %) a **1.549 (97,2 %)**. Es una práctica observada y concentrada: **22 de los 24 casos proceden de un mismo órgano** y los otros 2 de un segundo, y en todo el corpus un órgano reúne el 63 % de estos textos. No puede generalizarse a otros órganos. La validación manual anterior (0 falsos negativos en 60 obras de 2021–2024) no lo detectó porque revisó los documentos de cada obra, no este campo.

**Anulaciones (v2.3):** la lista 2.11 incluye también `ANUL_CCN` («Anulación de Anuncio de Finalización de Contrato»). El programa solo cuenta un anuncio como vigente si hay más anuncios que anulaciones. En todo el corpus procesado hay **0 expedientes de obras con alguna anulación**, así que el resultado no cambia.

## Revisión manual

| Revisión | Qué se revisó | Resultado |
|---|---|---|
| Muestra 1 (v1; `revision_manual_muestra_30.csv`) | 30 aleatorios | Modificaciones 30/30; ningún fin; detectó un expediente desierto (corregido) |
| Muestra 2 (v2; `revision_manual_muestra_2.csv`) | Los 9 candidatos de fin de la v2 y 21 aleatorios | Precisión 6/9; 1 falso negativo en 21 aleatorios: una resolución del contrato (corregido) |
| **Candidatos v2.2** (`revision_manual_candidatos_v2_2.csv`) | **Los 22 expedientes con alguna evidencia de fin** (censo) | **En los 20 clasificados como fin definitivo, la revisión del autor encontró evidencia contractual pertinente de finalización** (en un caso, solo de algunos lotes); los 2 clasificados como parciales no la acreditan. No es una precisión estadística validada de forma independiente |

**Entre los 20 expedientes con candidato definitivo reconocido por la revisión del autor:** 13 resoluciones del contrato (por incumplimiento, insolvencia, demora, desistimiento, mutuo acuerdo o extinción de la empresa contratista) y 7 terminaciones normales (actas de recepción, liquidaciones, certificaciones finales). Describe solo esos 20 casos detectados: **no** implica que las resoluciones predominen entre todas las obras ni que haya una tasa institucional elevada de resoluciones. Una hipótesis que habría que comprobar es que las resoluciones se publican más porque tienen un trámite formal más visible.

**Incertidumbre del estrato negativo (los 1.573 de la v2.3; 1.549 en la v2.4):** la única estimación es la de la muestra 2: 1 omisión en 21 aleatorios, un 4,8 %, con un intervalo exacto al 95 % de ≈ 0,1 %–23,8 %. Esa omisión ya la detecta la v2.2, pero no hay una muestra nueva e independiente del estrato negativo de la v2.2. Además, la muestra se sorteó entre los 1.652 seleccionados de la v2 y no específicamente entre los que tienen el fin vencido. **Pendiente:** una muestra amplia y aleatoria de los 1.573.

## Criterios y cambios

**Declarados antes de ver resultados:** obras (código 3) · estado ADJ o RES · primera fecha de adjudicación en 2023 · presupuesto base sin IVA del expediente entre 1 y 10 M€ · última versión de cada expediente.

| Versión | Cambio | Motivo | Efecto |
|---|---|---|---|
| v1 | Solo resultados con código de adjudicación (1, 2, 8, 9) | Revisión manual: expediente desierto | 1.811 → 1.631 |
| v1 | Categorías de incidencias (ampliación de plazo, suspensión, cesión) | Revisión manual | No cambia el fin |
| v2 | Borrados: se excluyen ANULADA y sin tipo; CERRADA se conserva | Revisión adversarial 1; especificación §3.1.2 | Ninguno en la selección (ver diagnóstico) |
| v2 | Patrones ampliados y exclusiones | Revisiones adversariales 1 (ChatGPT y Gemini); datos reales | — |
| v2.1 | Categoría de resolución del contrato | Muestra 2 | 99,4 % → 99,1 % |
| **v2.2** | **Empates de `updated`: sin fusionar; regla determinista (más documentos) y cotas mínima y máxima** | Revisión adversarial 2: la selección dependía del orden de lectura | Cotas 98,7 %–98,7 % |
| **v2.2** | **Procedencia de cada coincidencia** (archivo o etiqueta, y sección) | Revisión adversarial 2 | Ver `candidatos_fin.csv` |
| **v2.2** | **Categorías separadas:** fin definitivo frente a parcial o avance | Revisión adversarial 2; muestras | — |
| **v2.2** | **Anuncio estructurado de finalización `DOC_CCN`** | Revisión manual de candidatos | 8 expedientes; 99,1 % → **98,7 %** |
| v2.2 | Diagnóstico de borrados; anexo aparte por tipo de administración; script de descarga | Revisión adversarial 2 | — |
| v2.3 | Anulaciones del anuncio de finalización (`ANUL_CCN`); redacción más prudente sobre `DOC_CCN`, la revisión y el art. 346 | Revisión adversarial 3 | Ninguno: 0 anulaciones en el corpus |
| **v2.4** | **Fin comunicado en el texto (`Note`) de una modificación** (categoría `fin_en_nota_modificacion`) | Investigación de las modificaciones (01/11/2026); 24 casos revisados a mano | **98,7 % → 97,2 %** |

## Diagnóstico de borrados

| Tipo | `ref` distintos | Coinciden con una entrada leída | De obras | Borrado posterior a la última versión |
|---|---:|---:|---:|---:|
| CERRADA | 27.075 | **0** | 0 | 0 |
| ANULADA | 6.870 | 6.700 | 966 | 559 |
| Sin tipo | 691 | 21 | 3 | 1 |

**Los CERRADA no coinciden con ninguna entrada del corpus procesado**; todo indica que no es un fallo de emparejamiento, aunque no se han inspeccionado los 27.075 uno a uno. El formato de los identificadores es idéntico (`…/licitacionesPerfilContratante/N`). Los números de los cerrados van de 0,73 a 5,9 millones (mediana 1,6 millones), y el 90 % de las entradas leídas está por encima de 11,9 millones. Son archivados de expedientes antiguos que no aparecen en los ficheros de 2023 en adelante. Ningún ANULADO cumpliría los criterios.

## Empates

Hay 399 expedientes con versiones distintas y la misma `updated` máxima en todos los datos (la especificación §3.3.1 admite correcciones sin cambiar la fecha). 21 serían seleccionables con alguna de sus versiones. Ya no se fusionan: se elige una versión con una regla determinista, que no depende del orden de lectura, y se informan las cotas (`empates_en_seleccion.csv`). El titular es 97,2 % en ambos extremos (v2.4; 98,7 % en la v2.3).

## Fuentes

- Conjunto «Licitaciones publicadas en los perfiles del contratante ubicados en la PLACSP (excluyendo contratos menores)», Ministerio de Hacienda, datos abiertos. ZIP anuales 2023–2025 y mensuales 202601–202610, descargados el 30/10/2026.
- «Formato de sindicación y reutilización de datos sobre las publicaciones en la PLACSP», v1.10, 17/09/2024. **No documenta** `DOC_CCN`.
- Lista de códigos `TenderingNoticeTypeCode` 2.11: `DOC_CCN` = «Anuncio de Finalización de Contrato».
- Contraste con el Registro de Contratos y con el registro vasco: `CONTRASTE_REGISTRO_CONTRATOS.md`.

## Limitaciones

1. **Clasificador nominal:** los documentos se detectan por nombre o etiqueta, no por contenido; desde la v2.4 también se lee el texto de las modificaciones, pero no el de los documentos. El estrato negativo solo se ha muestreado con 21 casos.
2. **`DOC_CCN`:** la sindicación no trae la fecha real ni la causa, solo el tipo y la fecha del anuncio. El detalle exige descargar el documento enlazado. Tampoco dice a qué lote se refiere cada anuncio o anulación: con varios anuncios y una anulación se da por vigente uno sin saber cuál (prueba `test_varios_lotes_una_anulacion_sigue_vigente`, añadida el 01/11/2026 junto con otras dos sobre anulaciones). Además, la sindicación puede registrar **un solo** anuncio donde la web muestra uno por lote (comprobado en dos de los 8 expedientes), así que el número de anuncios por expediente no es fiable; lo que usa el programa es si hay alguno vigente.
3. **Fin teórico estimado:** inicio (o formalización, o adjudicación) + duración prevista o final tras modificaciones. No incluye suspensiones ni ampliaciones no publicadas, y en expedientes multilote puede mezclar lotes. En el caso comprobado, el error fue de unas dos semanas.
4. **Expedientes, no contratos:** 296 de 1.651 tienen varios resultados adjudicados. Un expediente puede tener acreditado el fin de uno de sus lotes y no el de los demás.
5. **Alcance:** solo perfiles alojados en la PLACSP; ni plataformas autonómicas, ni contratos menores, ni acuerdos marco analizados por separado. No extrapolar a otros años, tipos o importes.
6. **No implica incumplimiento:** la información puede estar en el Registro de Contratos (art. 346 LCSP), en registros autonómicos o en el perfil fuera de la sindicación.
7. Las comparaciones por tipo de administración están en un **anexo** y no son comparables (conviven las listas de códigos 1.04 y 2.10).
8. No se extraen datos de adjudicatarios.

## Reproducir

**Reproducir el estudio** (mismos ficheros y mismos resultados):

```bash
python descargar_datos.py reproducir --manifiesto manifiesto_descarga_estudio.json --destino datos
```
```bash
python -m unittest -v test_medir_ejecucion
```
```bash
python medir_ejecucion.py datos/licitacionesPerfilesContratanteCompleto3_2023.zip datos/licitacionesPerfilesContratanteCompleto3_2024.zip datos/licitacionesPerfilesContratanteCompleto3_2025.zip datos/licitacionesPerfilesContratanteCompleto3_2026??.zip --salida resultados_v2_4
```

Si `descargar_datos.py` informa de huellas distintas, Hacienda ha regenerado los ficheros: se **repetirá** el estudio con otros datos, no se reproducirá.

**Repetir con datos actuales:** `python descargar_datos.py actualizar --anuales … --mensuales … --destino datos_nuevos`, que genera un manifiesto nuevo.

Las huellas del programa y de los datos de esta ejecución están en `resultados_v2_4/manifiesto.json` (programa v2.4, SHA-256 e451cae1c78ba4525f1ca796db58c1f8fd4dff3de24624e8c9f7e08103f15294, con el patrón endurecido tras la revisión adversarial del 02/11/2026; la v2.3, con SHA-256 b393a0d6…, y sus resultados se conservan fuera del repositorio, para comparar), y las fuentes con fechas en `manifiesto_descarga_estudio.json`. Las huellas de los ficheros por expediente de esta ejecución están en `resultados_v2_4/huellas_resultados.json`; el 02/11/2026 se repitió el análisis completo y `huellas_resultados.py comprobar` dio idénticos los tres ficheros (`expedientes_seleccionados.csv`, `candidatos_fin.csv` y `empates_en_seleccion.csv`).
