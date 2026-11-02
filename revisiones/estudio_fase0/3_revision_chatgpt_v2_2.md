# Democracia Auditable — Tercera revisión adversarial, fase 0 v2.2

**Fecha:** 30 de octubre de 2026  
**Destinatario:** Claude, para nueva iteración técnica.  
**Pregunta:** ¿puede publicarse la investigación como exploratoria y reproducible, sin presentar su indicador como prueba de ausencia real de documentación ni de incumplimiento?

## Dictamen ejecutivo

**Avance sustancial y resultado internamente consistente, pero NO publicaría aún el informe v2.2 como versión estable: he reproducido un defecto específico sobre anulaciones del anuncio `DOC_CCN`, documentado oficialmente, que debe corregirse o acotarse en los casos reales.** Después de verificar los ocho anuncios de la selección, añadir una prueba y ajustar dos frases causales, **sí considero defendible publicar una investigación exploratoria**, sin exigir ahora una tercera muestra manual grande ni una verificación material de todo el estrato negativo. La muestra insuficiente seguirá siendo una limitación explícita y sustantiva.

He ejecutado las **21 pruebas (21/21 correctas)**; procesado la muestra real incluida (**497 entradas, 112 expedientes de obras, cinco seleccionados**); comprobado la huella SHA-256 de `medir_ejecucion.py` (**`0ac0b37d4a13614aa20760b91dfcb09e73fcd0b1ff193d114795ddef5cd14e9b`**, idéntica al manifiesto); recontado el CSV y las hojas de revisión del paquete; y construido una contraprueba XML sintética nueva. **No he descargado ni ejecutado los 13 ZIP originales (7,59 GB), de modo que no puedo certificar de manera independiente el origen ni la integridad de los resultados completos, solo su coherencia con los archivos que envía Claude.** Tampoco he contrastado individualmente los documentos originales de los 22 casos contra la web oficial, ni recontado el Excel vasco.

La lista oficial CODICE 2.11 confirma **ambos** códigos: `DOC_CCN` = «Anuncio de Finalización de Contrato» y `ANUL_CCN` = «Anulación de Anuncio de Finalización de Contrato». Referencia primaria: https://contrataciondelestado.es/codice/cl/2.11/TenderingNoticeTypeCode-2.11.gc (filas del XML correspondientes a los dos códigos). La descripción del anuncio aparece asimismo en la documentación oficial de servicios web, versión 1.14, de 18/12/2025: https://contrataciondelestado.es/b2b/DGPE_PLACE_WS_OC_Estructura%20Datos%20XML%20EVL%20v1.14.pdf. No se ha verificado de forma independiente aquí el contenido de cada `ContractCompletionNotice` enlazado.

## 1. Los ocho problemas pendientes de la revisión anterior

| Tema | Estado v2.2 | Comprobación y reserva |
|---|---|---|
| 1. Empates `updated`, no determinismo y mezcla de versiones | **RESUELTO para el defecto original** | `medir_ejecucion.py:392–401`, `:461–508`, `:563–619`; las pruebas invirtiendo el orden pasan. Ya no fusiona dos documentos incompatibles. La elección «más documentos» sigue siendo convencional, no una prueba de vigencia. |
| 2. Validación del clasificador y falsos negativos | **PARCIALMENTE RESUELTO** | 22 candidatos en `revision_manual_candidatos_v2_2.csv`, 20 marcados como finales y dos parciales. Entre los no candidatos persiste muestreo pequeño y no estratificado específicamente según el denominador actual; no puede estimarse su sensibilidad. |
| 3. Denominadores de muestra frente al titular | **ACLARADO, NO RESUELTO INFERENCIALMENTE** | El informe especifica 1.651 seleccionados y 1.593 con fin teórico vencido; la muestra antigua no fue sorteada exclusivamente del segundo conjunto. |
| 4. Fin teórico y multilote | **LIMITACIÓN BIEN DECLARADA** | `extraer():283–296` aún puede combinar duración y fechas pertenecientes a lotes distintos. El subgrupo con un resultado reduce pero no elimina todas las dificultades. |
| 5. Origen y fase de las coincidencias | **RESUELTO COMO TRAZABILIDAD BÁSICA** | `extraer():307–322` y CSV guardan nombre de archivo / etiqueta documental y sección superior. No indican necesariamente el documento fuente exacto ni fecha contractual del contenido; siguen siendo *candidatos*. |
| 6. `CERRADA` y borrados | **MEJORADO Y PLAUSIBLE; NO VERIFICADO SOBRE LOS 13 ZIP** | `diagnosticar_borrados():622–639` publica 27.075 refs `CERRADA`, cero coincidencias con entradas. La explicación de identificadores antiguos es plausible, pero la ausencia de coincidencia por cadenas exactas no demuestra por sí sola que nunca exista variante de identificador o fuente histórica. |
| 7. Registro vasco | **LIMITACIÓN ABIERTA** | El estudio da nombres, fuente y cifras concretas, pero no adjunta XLSX ni he podido verificarlas con una extracción independiente. Deben etiquetarse como resultados del autor. |
| 8. Comparación de administraciones, descargas y publicación | **MEJORADO** | Tabla de administraciones relegada al anexo; `descargar_datos.py` diferencia `reproducir` y `actualizar`; hashes históricos publicados. Todavía no verificados por otro ejecutor frente a los 13 ZIP oficiales. |

## 2. Empates

**RESUELTO en la contraprueba A.** El código conserva cada versión empatada completa y elige mediante una regla estable, por lo que invertir el orden de lectura no cambia la selección. El CSV de empates contiene **21 expedientes** relevantes: en todos se ve `0/0,1/1` para las dos alternativas. Los extremos declarados del titular, **1.553/1.573** y **1.574/1.594**, se redondean ambos a **98,7 %**. La cota de expedientes seleccionados es **1.631–1.652** y la elección principal produce 1.651.

**Reserva:** `elegir_principal():396–401` escoge la versión con más documentos; esto no es necesariamente la última corrección publicada. Está bien como convención de trabajo **si** no se presenta como «versión verdaderamente vigente» y si se conservan/explican las alternativas. Para que los resultados no dependan del contenido no probatorio, consideraría el dato principal una selección convencional sometida a sensibilidad; para v2.2 la sensibilidad presentada es suficiente en el sentido limitado que declara.

## 3. `DOC_CCN`: código oficial y nueva contraprueba

**CONFIRMADO** por la lista CODICE 2.11: `DOC_CCN` identifica «Anuncio de Finalización de Contrato». Su detección en `ValidNoticeInfo` (`:298–305`, `:343–344`) es una mejora real frente a v2.1. Un anuncio válido es evidencia documental pertinente de **la finalización declarada de al menos el contrato/lote al que se refiera**, aunque no acredite que todos los lotes del expediente hayan terminado. La fecha y causa reales requieren consultar el anuncio enlazado; la sindicación por sí sola no las acredita.

**ERROR NUEVO — posible anuncio anulado:** la misma lista oficial CODICE contiene `ANUL_CCN` («Anulación de Anuncio de Finalización de Contrato»), que el programa no evalúa. La variable `anuncio_finalizacion` es simplemente `"DOC_CCN" in avisos` (`:298–305`, `:343`); por tanto, si un expediente tiene un `DOC_CCN` y posteriormente un `ANUL_CCN`, el programa puede contarlo como evidencia vigente de fin. Una anotación de cancelación en el propio anuncio también podría requerir tratamiento.

**Contraprueba ejecutada:** construí un `ContractFolderStatus` ficticio con `ValidNoticeInfo` de tipo `DOC_CCN` y, a continuación, `ValidNoticeInfo` de tipo `ANUL_CCN`. `extraer()` devuelve `anuncio_finalizacion=True` y `sin_fin_definitivo()` devuelve `False`; es decir, lo clasifica como finalizado aun existiendo anulación. No afirmo que ninguno de los **ocho** expedientes reales tenga tal anulación: **esa frecuencia no está comprobada**. Antes de publicar, inspeccionar los ocho casos reales y añadir test con anulación; establecer semántica correcta considerando la identidad y el orden de los anuncios, no un simple veto global a cualquier `ANUL_CCN` (puede haber anuncios sucesivos o lotes distintos).

## 4. Cambio de la conclusión sobre la PLACSP

**CORRECCIÓN CONCEPTUAL MUY IMPORTANTE, BIEN INCORPORADA EN GENERAL.** El formato **sí prevé** finalización estructurada (`DOC_CCN`). Se puede afirmar que **en la población seleccionada** se detectaron solo ocho expedientes con ese anuncio en su sindicación; no que el canal carezca de soporte, que su uso sea universalmente escaso en toda España, ni que exista deber jurídico general de utilizar específicamente `DOC_CCN` cada vez que finaliza una obra.

**AJUSTE EDITORIAL NECESARIO:** en `CONTRASTE_REGISTRO_CONTRATOS.md`, apartado 3 bis, y apartado 4, fórmulas como «lo que falta es que se use de forma sistemática» o «lo que el art. 346.3 obliga a comunicar al Registro se publique por esta vía» deberían presentarse como **propuesta a estudiar**, no conclusión jurídico-empírica ni equivalencia de obligaciones. El artículo 346 LCSP exige comunicar ciertos datos al Registro «en su caso», pero el canal, la temporalidad y la publicidad accesible se rigen por otras reglas. Fuente primaria: https://www.boe.es/buscar/act.php?id=BOE-A-2017-12902 (art. 346).

Además, los recuentos globales de **88, 198 y 293** anuncios por año son numeradores sin denominador comparable de contratos finalizados: muestran presencia del tipo documental, no una tasa global de uso o cumplimiento. El subgrupo 2023 y la tabla 1–10 M€ sí ofrecen una descripción circunscrita.

## 5. Revisión manual de los 22 candidatos

**RESUELTO EL CENSO DEL ESTRATO POSITIVO, NO LA SENSIBILIDAD.** El CSV registra 22 casos positivos según el detector amplio: 20 definitivos y dos parciales. En los 20 definitivos, las notas del autor consideran reconocible alguna finalización: 19 «fin acreditado» y **uno** «fin acreditado (parcial del expediente)». En este sentido es aceptable mencionar **20/20 positivos con alguna evidencia contractual pertinente revisados por el autor**, **no** «20/20 de precisión estadística validada de forma independiente» ni «20 expedientes con todas sus obras terminadas».

Entre 1.573 negativos del titular, el programa puede omitir documentación cuyo nombre no revele su contenido o esté publicada en otra fuente. La muestra previa tiene solo **21 casos aleatorios** y se diseñó para un denominador diferente; una sensibilidad poblacional precisa sigue sin estimarse. Eso no impide publicar una **medición nominal exploratoria**, pero sí llamar a 98,7 % «ausencia verificada de documentación» o «tasa de incumplimiento».

## 6. `CERRADA`

**PLAUSIBLE, NO COMPROBADO INDEPENDIENTEMENTE.** En la salida entregada, de 27.075 referencias `CERRADA` ninguna coincide con los 667.929 identificadores de entrada leídos en los 13 ZIP. La explicación de referencias antiguas (0,73–5,9 millones frente a identificadores generalmente más recientes) resulta razonable y coherente con el ámbito temporal. El código realiza emparejamiento exacto `ref`→`id` y hay coincidencias con `ANULADA`, lo que proporciona una comprobación indirecta útil. No obstante, no he inspeccionado los 27.075 eventos contra la fuente; conviene afirmar «no coincide en el corpus procesado», no «se ha probado que el formato excluye toda posibilidad de relación».

## 7. Reproducibilidad

**MUY MEJORADA, PERO VERIFICACIÓN INDEPENDIENTE PENDIENTE.** `descargar_datos.py` incluye URL, SHA-256, tamaño y fecha, y distingue datos históricos de descarga actualizada. La huella del programa en `resultados/manifiesto.json` coincide exactamente con el archivo suministrado. Hay 13 ZIP por **7.590.646.494 bytes** en total (aproximadamente **7,59 GB decimales**, antes de descomprimir). Las pruebas sintéticas pasan y la muestra real incluida se procesa.

**Lo comprobado:** estructura y comandos, hash del código, tests y muestra, consistencia de las salidas CSV/JSON. **No comprobado:** que los 13 ZIP del servidor sigan siendo byte a byte idénticos, que produzcan efectivamente los 2.557.308 registros reportados, y que el XLSX vasco reproduzca los recuentos; no hay copias archivadas en el paquete.

**Detalles menores para publicar en GitHub:** falta un `LICENSE` explícito que permita copiar y adaptar el software conforme al deseo de dominio público del autor (por ejemplo, **CC0-1.0**, con asesoramiento sobre jurisdicciones y sin asumir que borrar el copyright del README basta); una guía mínima `README.md` de entrada con Python, memoria/disco recomendados y coste de descargar 7,59 GB; comprobar `bytes` además de `sha256` en el modo reproducción sería redundante desde el punto de vista criptográfico, pero útil para diagnosticar errores de descarga. Conservar las fuentes por nombre y SHA y no afirmar reproducibilidad eterna si el servidor oficial regenera los ZIP.

## 8. Trece resoluciones frente a siete terminaciones normales

**ACEPTABLE SOLO COMO DESCRIPCIÓN DE LOS 20 CASOS DETECTADOS Y REVISADOS.** No implica que las resoluciones predominen entre todas las obras ni que exista una tasa institucional elevada de resolución de contratos. En expedientes con varios lotes, alguna finalización puede no cubrir el conjunto. Recomiendo presentarlo como «entre los 20 expedientes con candidato definitivo reconocido por la revisión del autor, 13 contienen resolución/extinción y siete terminación ordinaria», con esa nota.

## 9. ¿Publicable como investigación exploratoria reproducible?

**NO TODAVÍA COMO INFORME V2.2 ESTABLE TAL CUAL**, por un número reducido de pendientes concretos, no por exigir una investigación nueva desproporcionada:

1. **Comprobar los ocho `DOC_CCN` del grupo, detectar posibles `ANUL_CCN`/anulaciones e introducir una prueba para la semántica de anulación**, conservando la diferencia entre anuncios sobre contratos o lotes concretos. Si no se demuestra impacto, decirlo explícitamente.
2. **Eliminar las dos sobreafirmaciones de `CONTRASTE_REGISTRO_CONTRATOS.md`** sobre que «falta usarlo sistemáticamente» como conclusión probada y sobre la equivalencia automática entre art. 346 y publicación de `DOC_CCN`.
3. **Preparar el paquete mínimo de liberación** (licencia abierta explícita + `README` con ejecución y límites). Esto es necesario si el objetivo es que terceros puedan reutilizar libremente el programa, aunque no impide que circulen borradores técnicos.

**NO exigiría ahora una tercera muestra grande.** Sí exigiría que se declarase expresamente la incertidumbre de los falsos negativos y que el hallazgo principal fuera una medición de coincidencias detectadas en **un conjunto de datos y una población delimitados**. Tras los tres ajustes, **SÍ consideraría publicable el estudio como *exploratorio reproducible* para organizaciones, con reservas y sin afirmar un incumplimiento ni un porcentaje real de ausencias de documentos**.

## 10. Nuevos errores o amenazas metodológicas no preguntadas

### A. Error demostrable: falta de manejo de `ANUL_CCN` (importancia media; efecto real desconocido)

Véase §3. Referencia: `medir_ejecucion.py:298–305`, `:343–344`; tipo y anulación confirmados en la lista oficial CODICE 2.11. La prueba mínima deberá incluir un expediente con anuncio de finalización y anulación posterior, y otro con anuncio válido posterior a la anulación, más un caso multilote si el esquema permite identificar contrato/lote.

### B. Diferencia entre ausencia de anuncio y ausencia de obligación (importancia editorial alta)

Ni `DOC_CCN` ni art. 346 permiten pasar de «no detectado en sindicación» a «obligación incumplida». El denominador relevante para medir obligación de publicar (si existiera y fuera del mismo ámbito) no sería necesariamente «fin teórico estimado anterior al corte». Debe figurar el carácter **exploratorio** desde el título y no solo en las notas de lectura.

### C. Calidad del corte y población (limitación ya asumida, importante)

`medir_ejecucion.py:512` usa la fecha máxima `updated` del corpus como corte. Es válido como parámetro de cálculo, pero no representa necesariamente una verificación de disponibilidad homogénea ni de cada fuente a esa fecha; además el fin teórico no incorpora todas las suspensiones/ampliaciones posibles (`:283–296`). La explicación actual lo reconoce razonablemente; evitar usar «vencido» como si indicara mora real.

### D. Etiquetas documentales en todo el expediente y lote afectado (limitación estructural)

La exploración de `FileName` y `DocumentTypeCode@name` recorre todas las secciones, no solo ejecución (`:307–322`). El estudio identifica coincidencias nominales, con posibles falsos positivos o referencias a un solo lote. La procedencia por sección permite investigarlo, pero no equivale a una revisión semántica del contenido.

### E. Sin licencia explícita todavía (importancia práctica para el objetivo del usuario)

El paquete es auditable como código entregado, pero no **formalmente liberado** para cualquier uso y modificación hasta adjuntar licencia que otorgue esos permisos. Dado que el propósito es la cesión pública sin seguimiento del autor, esto forma parte del entregable final.

## Veredicto de una línea

**NO aún como informe exploratorio estable v2.2: falta descartar/anotar la posible anulación de `DOC_CCN` y corregir dos afirmaciones excesivas; después SÍ será publicable como medición nominal exploratoria y reproducible, con la incertidumbre del estrato negativo declarada y sin inferir incumplimientos.**

---

**Fuentes primarias verificadas para esta ronda**

- PLACSP — CODICE `TenderingNoticeTypeCode-2.11.gc`: https://contrataciondelestado.es/codice/cl/2.11/TenderingNoticeTypeCode-2.11.gc (`DOC_CCN`, `ANUL_CCN`).
- Ministerio de Hacienda — conjuntos de datos de licitaciones alojadas y agregadas diferenciados: https://www.hacienda.gob.es/es-ES/GobiernoAbierto/Datos%20Abiertos/paginas/licitaciones_plataforma_contratacion.aspx.
- BOE — Ley 9/2017, artículo 346: https://www.boe.es/buscar/act.php?id=BOE-A-2017-12902.
- PLACSP — documentación de servicios web, versión 1.14: https://contrataciondelestado.es/b2b/DGPE_PLACE_WS_OC_Estructura%20Datos%20XML%20EVL%20v1.14.pdf.

**Integridad de la revisión:** no se ha modificado el código de Claude, no se han extraído ni divulgado datos de personas físicas y todas las contrapruebas nuevas utilizan XML ficticio.
