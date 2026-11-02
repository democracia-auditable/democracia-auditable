# Democracia Auditable — Segunda revisión adversarial de la fase 0 (v2.1)

**Fecha:** 30 de octubre de 2026  
**Material recibido:** `para_chatgpt_fase0_v2.zip`, preparado por Claude.  
**Objeto:** revisión del programa `medir_ejecucion.py`, método, resultados, dos fichas de revisión manual y contraste con el Registro de Contratos, en el marco del §8.6 de *Democracia Auditable* v0.4.1.

## Dictamen ejecutivo

**El trabajo ha mejorado sustancialmente y el resultado nominal es internamente coherente, pero no considero cerrado ni validado independientemente el estudio.** En la población que declara el informe, el programa marca **1.579 de 1.594 expedientes (99,1 %) sin nombres o etiquetas coincidentes con su clasificador de documentos de finalización**. Es un resultado **de detección automática**, no una estimación validada del porcentaje de expedientes que carecen de información de cierre.

He **ejecutado las 17 pruebas unitarias** (17/17 satisfactorias), **ejecutado el ejemplo real de 497 entradas** (497 entradas y cinco expedientes seleccionados), **verificado el SHA-256 del programa** frente al manifiesto y **recontado la tabla de 1.652 expedientes aportada**. He construido tres contrapruebas sintéticas que demuestran nuevas debilidades concretas. **No he repetido el procesamiento de los 13 ZIP originales** (más de 7 GB, no incluidos en el paquete), no he podido verificar sus hashes y tampoco he auditado por segunda vez los documentos de los expedientes de la muestra manual.

La norma del artículo 346 de la LCSP está contrastada directamente en el BOE; las distinciones `ANULADA`/`CERRADA` y la función de `updated` están contrastadas en la especificación oficial PLACSP v1.10. He confirmado la existencia de un conjunto de datos y una API públicos del Registro vasco, **pero no he conseguido descargar y recontar su XLSX**; los números concretos que atribuye Claude a esa hoja siguen pendientes de comprobación independiente.

## Respuestas a las diez preguntas

### 1. Diez objeciones anteriores: situación individual

| N.º anterior | Estado | Comprobación o reserva |
|---|---|---|
| 1. `ANULADA` frente a `CERRADA` | **Mitigado; no verificado sobre el corpus** | El código `medir_ejecucion.py:357–360, 459–480` conserva el tipo, excluye `ANULADA` y mantiene `CERRADA`; la prueba sintética pasa. El manifiesto informa 27.075 `CERRADA` en todos los datos pero 0 entre los seleccionados: sin los ZIP no puedo validar esa distribución. La especificación confirma que cerrar/archivar no es anular. |
| 2. Expediente frente a contrato | **Resuelto como problema de rotulación; limitación analítica abierta** | El texto distingue expedientes, lotes y contratos y cuenta 297/1.652 expedientes con más de un resultado adjudicado. El subgrupo de un resultado reduce la mezcla, pero no convierte el análisis en uno por contrato. |
| 3. Sobreinterpretación de nombres | **Mitigado** | `METODO.md` usa «no se identificó» y descarta inferir incumplimientos. Precisión técnica pendiente: el clasificador lee **`FileName` y `DocumentTypeCode@name`**, no solamente nombres de adjuntos (`medir_ejecucion.py:298–309`). |
| 4. Plazos multilote | **Mitigado, no resuelto** | «Fin teórico estimado» y sensibilidad con un resultado. `extraer():252–294` todavía puede mezclar el inicio previsto del expediente con la duración final de una modificación de un lote. |
| 5. Empates de `updated` | **Parcialmente corregido; nuevo fallo demostrado** | Se preservan nombres de documentos de ambas entradas, evitando el falso negativo anterior, pero se conserva la selección estructurada de la **última leída**. Dos entradas con idéntica fecha y presupuestos distintos cambian el denominador cuando se invierte el orden de lectura. Ver contraprueba A. |
| 6. Semántica de documentos | **Mitigado, no resuelto** | Excluye algunos falsos positivos y añade extinción contractual. La validación encuentra 3 falsos positivos entre nueve candidatos del clasificador v2; la v2.1 introduce nuevos candidatos todavía no revisados. |
| 7. Muestra manual insuficiente | **Mitigado, todavía insuficiente** | Hay una segunda muestra estratificada, pero solo 21 elementos del estrato negativo y los nueve positivos del **clasificador anterior**. No permite acotar estrechamente las omisiones del v2.1. |
| 8. Exclusiones y acuerdos marco | **Exclusiones parcialmente resueltas; alcance abierto** | Hay tabla por código. La exclusión de acuerdos marco y contratos basados no desaparece. Además la tabla mezcla posibles expedientes multilote con un resultado adjudicado y otro desierto; conviene evitar que se interprete como razón exclusiva de exclusión. |
| 9. Comparación por administración | **Resuelto como cautela editorial, no como clasificación estadística** | La tabla figura como «exploratoria, no comparable», pero sigue siendo muy fácil reutilizarla fuera de contexto: sugiero retirarla del documento de difusión o mantenerla solo en el anexo técnico. |
| 10. Manifiesto y huellas | **Resuelto en el diseño; verificación parcial** | El SHA-256 del script coincide con el manifiesto (`c00bc89...3788c2`). Hay hashes de los 13 ZIP y versión de Python. No pude verificar los ZIP originales por no incluirse en el paquete; queda pendiente comprobar que sean descargables e idénticos. |

### 2. Empates: ¿es correcta la fusión? ¿Explica los 21 casos?

**Encontrado un error nuevo: la fusión NO es una regla canónica y depende del orden de los ficheros.** `fusionar()` (`:377–394`) toma **todos los campos principales de `b`**, une documentos de `a` y `b`, y usa máximos u operaciones OR en algunos resúmenes. Esto preserva evidencias históricas, pero **no reconstruye necesariamente la última versión vigente**: una corrección puede retirar un documento erróneo y la unión volver a introducirlo. También puede fabricar un expediente compuesto que nunca existió como una sola versión.

**Contraprueba A (ejecutada, datos ficticios):** mismo ID, misma fecha `updated` y misma fecha de adjudicación, pero versión A con presupuesto de 2 M€ y versión B con 12 M€. Con nombres de archivo que fuerzan el orden A→B, `expedientes_seleccionados = 0`; invirtiéndolo B→A, `expedientes_seleccionados = 1`. Código implicado: `:454–455`, `:377–394`, `:397–404`. Es un defecto de estabilidad del denominador, no solo de los documentos.

**Contraprueba B (ejecutada, datos ficticios):** A contiene `Acta de recepción definitiva.pdf`; B, con igual `updated`, la ha eliminado. La versión B se lee después. `fusionar()` mantiene el acta de A y marca al expediente como candidato de fin: potencial **falso positivo** si B era la corrección válida.

El CSV aportado contiene **exactamente 21 expedientes seleccionados con `empate_distinto=True`** y ninguno de esos 21 tiene candidatos de fin; esto hace plausible, pero **no demuestra causalmente**, la afirmación de que todos los 21 nuevos proceden de los empates. Para demostrarlo hay que comparar ambos criterios **sobre los mismos ZIP originales** y registrar los IDs añadidos, retirados y reclasificados. Propuesta: definir un criterio estable por archivo/orden de generación, marcar los conflictos de campos de selección, informar una **sensibilidad con todas las alternativas** y utilizar la unión de documentos como *detección histórica*, no como prueba de la versión vigente.

### 3. `CERRADA`: ¿es plausible que haya 27.075 y ninguna seleccionada?

**No puedo comprobarlo** sin el corpus original. La lógica `borrados[ident][0] >= t` (`:459–472`) tiene sentido si `ref` coincide exactamente con el ID del `entry` y se quiere aplicar solo una eliminación posterior a la última versión. La especificación exige que `ref` señale el ID borrado. Las pruebas con IDs sintéticos coincidentes pasan.

No hay contradicción matemática en que una categoría muy frecuente en el total esté ausente en una subpoblación estrecha; podría concentrarse en otros años, tipos o estados. Pero antes de afirmarlo como hallazgo conviene publicar un **diagnóstico de emparejamiento**: cuántos `ref` de `CERRADA` coinciden con un `entry` leído, cuántos con obras, cuántos con obras adjudicadas en 2023, y cuántos tienen borrado posterior. Esto distinguirá una explicación de cobertura de una posible divergencia de identificadores o temporalidad. Un borrado `CERRADA` indica cierre/archivo en la PLACSP, **no** recepción o fin material de la obra.

### 4. Segunda muestra: precisión, falsos negativos y «99,1 %»

**Mitigado, no resuelto estadísticamente.** La muestra v2 incluye **los nueve positivos automáticos** (censo del estrato positivo antiguo) y **21 aleatorios del resto**, excluyendo previamente los revisados en v1. Según sus fichas, **6/9** positivos nominales representan documentación de fin y **1/21** negativos ocultaba un acuerdo de resolución contractual.

- Para la tasa de omisiones observada en ese estrato negativo **1/21 = 4,76 %**, el intervalo exacto binomial **bilateral del 95 % es aproximadamente 0,12 %–23,82 %**. Supone clasificación manual correcta y muestreo aleatorio representativo; no constituye garantía ni intervalo de error del 99,1 %.
- Si se retira ese caso porque la v2.1 ya lo detecta, quedan **0 omisiones observadas entre esos 20 expedientes**, pero **no es una muestra nueva independiente** del estrato negativo de v2.1. Como orientación sobre la incertidumbre de una hipotética muestra de 20 negativos sin hallazgos, el límite superior exacto bilateral al 95 % sería aproximadamente **16,8 %**, no cero.
- **Cambio de población de interés:** se sortearon expedientes entre los **1.652 seleccionados**, pero el titular usa los **1.594 con fin teórico anterior al corte**. La validación no se diseñó específicamente sobre este último subconjunto.
- Tras incorporar `resolucion_contrato`, el v2.1 tiene **15 expedientes positivos nominales** entre los 1.594, no nueve. **Los siete nuevos casos de esta categoría no se han sometido íntegramente a la misma revisión documentada**: una de esas siete resoluciones se descubrió en la muestra; quedan otras por comprobar.

Por tanto **el 99,1 % es un recuento exhaustivo de etiquetas producidas por el programa sobre el CSV**, no la proporción real estimada de expedientes sin documentación de fin. Para estimar esta última se necesitan muestras *revisadas sobre los propios documentos*, por estratos del clasificador definitivo y de la población con fin teórico anterior al corte, con intervalos adecuados a la estratificación y al cambio de reglas.

### 5. Expresiones regulares nuevas

**Encontrados errores residuales previsibles; no he comprobado su tasa real sobre el corpus completo.**

- `resolucion_contrato` (`:94–95`): registra algunos títulos adecuados como «Acuerdo de resolución del contrato», pero la exclusión `aprobac|inici|expediente|licitac` puede producir falsos negativos en «**Aprobación de la resolución del contrato**» (decisión posiblemente definitiva). Y «Resolución del contrato: propuesta de acuerdo» puede producir falso positivo si nunca se adoptó. No basta el nombre para afirmar extinción.
- `acta_recepcion` (`:79–83`): `recep` detecta **recepciones parciales**, que el propio muestreo muestra que no acreditan recepción final. El patrón `acta de conformidad` también puede referirse a un trámite distinto.
- `certificacion_obra` (`:86–91`): admite «certificación mensual» y certificaciones numeradas, que prueban avance, **no necesariamente la terminación**; excluir cualquier nombre con `pleno` o `mesa` puede ocultar una certificación final válida anexada a una resolución de pleno.
- `final_obra` (`:92`) y `liquidacion` (`:84–85`): mantienen títulos ambiguos. Por ejemplo, una «certificación final de obra» puede aparecer bajo una etiqueta estructurada distinta o un nombre genérico imposible de reconocer.
- **Contraprueba C (ejecutada):** creé un `entry` sin ningún `FileName`, pero con `<DocumentTypeCode name="Acta de recepción de obra">`. `extraer()` clasificó `acta_recepcion`. Esto prueba que la fórmula «por el **nombre de los adjuntos**» es literalmente demasiado estrecha: también se usan **etiquetas de tipo documental** (si aparecen en las entradas reales).

Recomiendo separar categorías de **recepción definitiva**, **recepción parcial**, **certificaciones de avance**, **certificación final**, **liquidación**, **extinción por resolución**; mantener el indicador combinado como heurística exploratoria y precisar el origen exacto de cada coincidencia (`FileName` o nombre de tipo).

### 6. Registro vasco: artículo 346.6, campos vacíos y viabilidad

**Parcialmente resuelto; conteos concretos no comprobados.** El **artículo 346.6 LCSP** prevé que las administraciones con registros propios análogos puedan intercambiar comunicaciones con el Registro estatal: existe base jurídica para considerar el registro autonómico como modalidad comparable, pero **no he verificado el acuerdo técnico de intercambio concreto**. <https://www.boe.es/buscar/act.php?id=BOE-A-2017-12902>

He comprobado en fuentes oficiales la existencia del dataset *Registro de contratos de Gobierno Vasco del 2023*, su **licencia CC BY 4.0** y sus dos distribuciones (API y XLSX). El portal de Euskadi también ofrece un buscador del Registro de Contratos. <https://datos.gob.es/es/catalogo/a16003011-registro-de-contratos-de-gobierno-vasco-del-2023> · <https://opendata.euskadi.eus/catalogo/-/registro-contratos-gobierno-vasco-del-2023/>.

No he podido descargar ahora el XLSX y, por tanto, **no puedo corroborar autónomamente los 2.368 contratos, 431 de obras, 182 finalizados ni el contenido exacto de las 63 columnas** citados por Claude. Su descripción es contrastable y creíble, pero aún no es una verificación independiente de esas cifras.

Que los campos de prórrogas o modificaciones estén vacíos **no invalida** la presencia de campos de estado/finalización; sí impide deducir que no hubo incidencias y exige verificar cómo se alimentan esos campos. Que una administración publique un registro individual de contratos **apoya la viabilidad técnica** de publicar parte de los datos propuestos en §8.6; **no acredita por sí solo** que los campos reflejen recepción efectiva, pagos, liquidación auditada, equivalencia semántica entre sistemas o cobertura estatal. Distinguir «registro de datos de fin» de «acta firmada de recepción».

El BOE obliga a comunicar al Registro los datos de **importe final y extinción, en su caso**, y dispone acceso público a datos no confidenciales en las condiciones indicadas; **no exige literalmente que todo ese registro se ofrezca en un único CSV público individualizado**. Por otro lado, el portal ministerial que he revisado enlaza **estadísticas agregadas**; no prueba la inexistencia de cualquier servicio de acceso individual. <https://www.hacienda.gob.es/es-es/areas%20tematicas/contratacion/junta%20consultiva%20de%20contratacion%20administrativa/paginas/registro%20publico%20de%20contratos.aspx>.

### 7. Alcance de la población

**Resuelto en la formulación con una precisión importante.** El estudio analiza el conjunto **«Licitaciones publicadas en los perfiles del contratante ubicados en la PLACSP (excluyendo contratos menores)»**. No representa todas las obras españolas ni los registros autonómicos. El hecho de que la ley prevea agregación de anuncios autonómicos en la PLACSP **no convierte automáticamente esos anuncios en el corpus «perfiles ubicados»**; son conjuntos distintos. <https://www.boe.es/buscar/act.php?id=BOE-A-2017-12902> (art. 347).

La muestra se restringe además a obras del código seleccionado, primera adjudicación identificada en 2023, presupuesto base del expediente de 1–10 M€, estados `ADJ`/`RES` y fin teórico estimable anterior al 29/10/2026. No extrapolar a otros años, tipos o importes sin análisis explícito.

### 8. Frase publicable más precisa

**Mitigado, con corrección necesaria.** Propongo:

> «En los datos ATOM sindicados de los **perfiles alojados en la PLACSP**, analizados hasta el 29 de octubre de 2026, el clasificador automático **no encontró títulos de archivo ni etiquetas documentales que coincidieran con sus patrones de recepción, liquidación, certificación, terminación de obra o resolución contractual** en **1.579 de 1.594 expedientes de obras de la muestra definida**, cuyo fin teórico estimado era anterior al corte. **La cifra mide coincidencias nominales; no acredita que los documentos no existan, que la obra no esté concluida ni que no haya información en otros registros**».

Para la comunicación no técnica, abreviaría «nombres o etiquetas de documentos sindicados» y enlazaría la definición del clasificador. **No** llamaría a esos 1.579 expedientes «sin documentación de cierre» ni al 99,1 % «proporción de contratos con falta de transparencia».

### 9. ¿Publicable como estudio reproducible con límites declarados?

**No todavía como investigación empírica cerrada con cifra validada; sí compartible como borrador exploratorio reproducible para revisión técnica.** El script, el CSV, el manifiesto, la documentación y los tests permiten auditar mucho más que la primera versión. Pero, para una entrega pública con conclusiones consolidadas, considero mínimo:

1. **Resolver o acotar la inestabilidad de empates**, publicar resultados de sensibilidad y conservar las versiones discrepantes sin confundir la unión histórica con estado vigente.
2. **Revisar el clasificador definitivo v2.1**, especialmente los siete casos de resolución y un muestreo nuevo del gran estrato sin candidato; limitar el titular a lo que se ha comprobado en archivos y etiquetas.
3. **Ejecutar de nuevo los 13 ZIP**, comparar su SHA-256 con el manifiesto y suministrar instrucciones reproducibles, totales intermedios y listado de cambios respecto a la v2.1.
4. **Delimitar con mayor rigor el fin teórico**, separando expedientes multilote y documentando cuánto cambia la muestra ante fechas alternativas de inicio, suspensiones y modificaciones.
5. **Contrastar directamente un subconjunto de expedientes** con otras fuentes de ejecución (registro autonómico, portal institucional o acceso formal), distinguiendo fuente y significado de cada variable.

Estas condiciones no impiden **enviar el código y el borrador** a organizaciones para que lo critiquen; impiden describir el 99,1 % como un hecho externo ya independientemente establecido.

### 10. Lo que no se había preguntado: nuevos riesgos

**Encontrados errores nuevos:**

**A. La pertenencia a la población depende del orden de lectura cuando hay empate de fecha.** Es el contrajemplo de la pregunta 2, demostrado ejecutando el código. No basta con afirmar que «se fusionan» las versiones: no se fusionan los campos que determinan la selección.

**B. La extracción mezcla nombres de archivos y nombres de tipos documentales sin guardar procedencia ni ubicación.** `cfs.iter()` (`:298–309`) visita **todos** los `FileName` y nombres `DocumentTypeCode@name`, incluidos documentos de licitación, y registra solo un texto clasificado. La salida no permite saber si una coincidencia pertenece a un trámite inicial, a una modificación o a la etapa de ejecución. La segunda revisión manual ya encontró casos falsos positivos precisamente por esa mezcla. Esto dificulta construir un indicador realmente específico de finalización.

**C. El titular y el muestreo están definidos sobre denominadores distintos.** La muestra se sortea entre 1.652 y la proporción destacada usa 1.594. La validación debe corresponder a la variable y población cuya inferencia se publica.

**D. Las fuentes originales no están adjuntas.** Eso es razonable por volumen, pero los hashes y la tabla no sustituyen la reproducción independiente. Conviene publicar un comando de descarga verificable, la fuente exacta, fecha/hora de captura y tamaños, y documentar qué ocurre si los ZIP oficiales cambian.

## Errores pendientes y nuevos, ordenados por gravedad

1. **Alto — Empates de `updated` no deterministas y selección dependiente del orden** (`:377–404`, `:449–458`). **Contraprueba ejecutada**, población 0 frente a 1 con el mismo par de versiones en orden inverso. La unión de documentos puede conservar evidencias retiradas por corrección.
2. **Alto — Validez de contenido y error de clasificación insuficientemente cuantificados** (`:74–110`, `:298–309`). Tres de nueve candidatos de la v2 eran falsos positivos según la revisión aportada; los siete candidatos nuevos de resolución no están revisados de forma equivalente. El estrato negativo es muy pequeño.
3. **Medio-alto — Muestreo no diseñado exactamente para el denominador del titular** (`:484–499`, `:525–545`, `:606–610`), con cambios post hoc entre v2 y v2.1.
4. **Medio-alto — Plazo teórico débil en contratos multilote y sin comprobación de suspensiones** (`:252–294`). La «vencida» es una estimación orientativa, no evidencia de retraso.
5. **Medio — Falta de procedencia y fase contractual de las coincidencias documentales** (`:298–309`, `:548–556`), incluso el origen `DocumentTypeCode@name` frente a `FileName`.
6. **Medio — Distribución `CERRADA` sin verificación del emparejamiento real y ausencia de casos cerrados en la muestra** (`:459–480`); la lógica sintética funciona, pero los 27.075 casos del informe no se han auditado independientemente.
7. **Medio — Contraste con Registro vasco aún sin validación del XLSX por segundo analista**, ni comprobación de correspondencia con expedientes de la PLACSP.
8. **Bajo — Tabla exploratoria por administración susceptible de reutilización engañosa** (`:679–689`). Mantener solo en anexo con advertencia destacada.

## Veredicto, en una línea

**NO todavía como estudio validado para difusión pública: el 99,1 % es un resultado nominal plausible y reproducible sobre los archivos del autor, pero permanecen una inestabilidad demostrada de selección y una incertidumbre de clasificación que impiden presentarlo como cobertura real verificada; SÍ puede circular como borrador para revisión adversarial.**

## Fuentes primarias consultadas y alcance de la comprobación

- **Especificación PLACSP v1.10, 17/09/2024**, pp. 19, 21–22: tipos de eliminación y finalidad de `updated`; lectura del documento oficial PDF y comprobación visual de esas páginas: <https://contrataciondelsectorpublico.gob.es/datosabiertos/especificacion-sindicacion.pdf>.
- **BOE — Ley 9/2017, arts. 346 y 347**, texto consolidado en línea: <https://www.boe.es/buscar/act.php?id=BOE-A-2017-12902>.
- **Ministerio de Hacienda — Registro de Contratos del Sector Público**, lista pública de estadísticas agregadas 2013–2024 en la página consultada: <https://www.hacienda.gob.es/es-es/areas%20tematicas/contratacion/junta%20consultiva%20de%20contratacion%20administrativa/paginas/registro%20publico%20de%20contratos.aspx>.
- **datos.gob.es — Registro de contratos de Gobierno Vasco del 2023**, ficha de metadatos y distribuciones API/XLSX: <https://datos.gob.es/es/catalogo/a16003011-registro-de-contratos-de-gobierno-vasco-del-2023>.
- **Open Data Euskadi — misma publicación**, ficha y catálogo: <https://opendata.euskadi.eus/catalogo/-/registro-contratos-gobierno-vasco-del-2023/>.

**Nota de integridad:** este informe evalúa y reproduce parcialmente la evidencia facilitada; no modifica ni reemplaza el programa o los resultados originales. Los experimentos A, B y C utilizan exclusivamente entradas XML sintéticas.
