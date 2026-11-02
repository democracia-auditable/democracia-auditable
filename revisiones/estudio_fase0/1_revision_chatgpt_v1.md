# Democracia Auditable — Revisión adversarial de la fase 0

**Revisor:** ChatGPT (GPT-6) · **Fecha:** 30/10/2026  
**Objeto:** paquete `para_chatgpt_fase0.zip` preparado por Claude.  
**Veredicto:** **hay errores y limitaciones materiales que deben corregirse antes de difundir las cifras como hallazgo definitivo.** No se ha falsado la hipótesis general de escasa información sobre la finalización de obras en el *feed* reutilizable de la PLACSP. Sí se ha comprobado que el programa no cuenta contratos individuales sino expedientes/licitaciones y que mezcla archivos anulados y cerrados; el 99,4 % es un resultado del clasificador aplicado a una población que necesita validación, no un censo confirmado de obras sin información final.

## Qué he comprobado personalmente

- He leído `METODO.md`, el informe, el CSV de 1.631 filas, la muestra manual de 30 expedientes y el código.
- He **ejecutado las 11 pruebas** (`python -m unittest -v test_medir_ejecucion`): **11/11 pasan**.
- He **ejecutado el programa contra el ZIP real incluido**: 497 `entry`, 112 entradas de obras, **5 expedientes seleccionados**. Confirma su ejecución en la muestra, no reproduce las 1.631 filas porque no se proporcionaron los ~6 GB de fuentes completos.
- He **creado una contraprueba con dos versiones de la misma entrada y el mismo `updated`**: la última incorpora `Acta de recepción definitiva.pdf`, pero el programa conserva la primera, dando **0 documentos de recepción**. Es un falso negativo reproducible.
- He contado **300 de 1.631 filas (18,4 %) con varios `TenderResult`** en el CSV; 32 contienen además algún resultado no adjudicado. Esto no equivale a 300 expedientes con contratos múltiples confirmados; sí demuestra que la unidad de análisis requiere aclaración.
- He inspeccionado la **especificación oficial de sindicación de la PLACSP, v1.10 de 17/09/2024**, especialmente apartados 3.1.2, 3.3.1–3.3.2, 3.4.2–3.4.3, 4.35.7–4.35.8, 4.38 y 4.42, y el **artículo 346 LCSP** en el BOE.
- **No** he descargado ni reproducido el corpus completo 2023–2026 ni he reabierto uno por uno los 30 expedientes en la web. Sus cifras agregadas y su inspección manual son resultados **declarados por Claude**, no independientemente replicados.

## Respuestas a las diez preguntas

### 1. Código — **ENCONTRADO UN ERROR**

**(a) Deduplicación por `atom:id` y `updated`:** el principio de tomar la entrada con mayor fecha es correcto y está en el apartado 3.3.2 de la especificación oficial. Sin embargo, el apartado 3.3.1 advierte expresamente de que correcciones excepcionales **no cambian `entry/updated`**. En `medir_ejecucion.py:369–372`, la condición `t > ultima[ident][0]` descarta toda versión posterior con fecha empatada. **Contraprueba ejecutada:** dos archivos ATOM consecutivos con mismo ID y misma fecha; el segundo contiene un acta de recepción, y el CSV final deja `acta_recepcion` vacío. No sé cuántos empates de este tipo hay en el corpus completo. La solución es detectar y reportar versiones empatadas pero distintas, conservar el criterio de procedencia y, cuando sea posible, contrastar con la versión vigente de la PLACSP; sustituir `>` por `>=` sin más no resuelve siempre el orden de los ficheros.

**(b) Tombstones:** el programa identifica el formato (`:320–322`) y hace una exclusión temporal coherente (`:382–385`), **pero ignora el subelemento `at:comment@type`**. Desde julio de 2022 los borrados pueden ser `ANULADA` (expediente inválido) o `CERRADA` (cerrado/archivado, deja de estar accesible), distinción explícita en la especificación, apartado 3.1.2, pp. 18–19. **Excluir automáticamente ambos es una decisión de selección sesgada potencialmente importante**, precisamente en un estudio de finalización de contratos. Hay que conservar ambos tipos, contar cuántos serían candidatos y hacer un análisis de sensibilidad con `CERRADA` incluido como «histórico no accesible», sin confundir cierre del *feed* con recepción material de la obra. El ZIP reducido solo contiene ejemplos `ANULADA`; no prueba qué ocurrió con los 3.312 tombstones del corpus original.

**(c) Navegación CODICE:** no he encontrado una equivocación general en el uso de hijos directos. La especificación confirma que `TenderResult`, `ContractModification` y `ProcurementProject` son rutas directas bajo `ContractFolderStatus`; descender indiscriminadamente sería peligroso. **Sí hay una limitación específica**: el escáner de documentos `:265–270` busca todo `FileName` y casi ignora el `DocumentTypeCode` codificado (solo usa el atributo `name` si existe), y tampoco relaciona adjuntos con su contexto o lote. Debe analizar la referencia estructurada `GeneralDocument` y su código cuando sea relevante.

**(d) `fin_previsto`:** hay una inferencia cuestionable en `:255–260`: usa `PlannedPeriod.StartDate` o el mínimo de fechas de inicio, formalización o adjudicación **de todos los resultados**, y la `FinalDurationMeasure` de la modificación con número más alto **de toda la licitación** (`:247–254`). En varios lotes puede combinar el inicio del lote A con la duración del lote B; además, una modificación no equivale a todas las ampliaciones o suspensiones, y el inicio de la obra puede diferir de la fecha formal. El plazo estimado no debe presentarse como fecha real de vencimiento o de finalización. En un expediente multicontrato requiere cálculo por `ContractID`.

### 2. ¿La entrada es foto completa o cambio parcial? — **NO ENCONTRADO** (para la objeción central)

La especificación oficial, §3.3.2, dice que la versión más actual engloba los datos actualizados del expediente y relaciona sus anuncios; §3.4.2 describe añadir una entrada nueva con información del expediente. Por tanto, el supuesto de **foto completa** está apoyado expresamente. Si fuera un mero *delta*, sustituir la versión anterior perdería adjudicaciones, modificaciones y documentos, y el resultado sería inválido. El problema real que sí aparece es la posibilidad de dos fotos distintas con **idéntico `updated`**; no desacredita el modelo de foto completa.

### 3. Selección y lotes — **ENCONTRADO UN ERROR**

El filtro posterior de códigos de adjudicación corrige razonablemente el caso desierto descubierto en revisión. Pero `Contrato.id` es `atom:id` del **expediente**, y el programa crea **una fila por licitación** (`extraer` y `medir`), no una por contrato. La propia especificación, §4.35.7, establece que una licitación puede generar varios contratos. **Comprobación propia:** 300/1.631 filas contienen varios resultados `TenderResult`, y 32 incluyen algún resultado no adjudicado junto a otros. El mínimo de fechas de resultados adjudicados puede mezclar adjudicaciones de años diferentes; el presupuesto utilizado es el del **proyecto/lici­tación completa**, no necesariamente el de cada lote. Las modificaciones también se mezclan a nivel expediente. Hay que elegir y explicitar «licitaciones/expedientes con al menos una adjudicación de 2023» o desagregar por contrato/lote y recalcular importes, plazos, resultados y fuentes. Los acuerdos marco y contratos basados pueden requerir filtros por sistema de contratación; sin corpus completo **no puedo cuantificar** su presencia ni exclusión.

### 4. ¿Existen datos sobre finalización que no se estén mirando? — **ENCONTRADO UN ERROR DE ALCANCE; NO PUEDO COMPROBAR UNA REFUTACIÓN NUMÉRICA**

- La sindicación de PLACSP contiene **modificaciones** con `FinalLegalMonetaryTotal` y `FinalDurationMeasure` (§4.38), pero son importes y duraciones **después de una modificación**, no necesariamente el coste real final de ejecución ni un acta de recepción.
- En «otros documentos publicados» (§4.42) hay referencias y `DocumentTypeCode`; el programa solo detecta nombres mediante expresiones regulares, por lo que puede omitir **documentos existentes con nombres opacos** (y clasificar erróneamente otros). No hay prueba de que los nombres libres agoten los documentos relevantes.
- El **art. 346.3 LCSP**, contrastado en el BOE, exige comunicar al Registro de Contratos del Sector Público modificaciones, prórrogas, cambios de plazo/precio, **importe final y extinción**. Los apartados 5 y 6 prevén acceso público bajo condiciones y comunicación entre registros. El portal oficial ofrece también **estadísticas agregadas en CSV/XLS/PDF**, pero **no he encontrado en las páginas oficiales revisadas un volcado público individual de ese Registro** que permita unir automáticamente sus importes finales a las 1.631 filas. Su existencia administrativa no refuta el porcentaje restringido al feed de PLACSP, pero **sí impide generalizarlo a toda la información pública española sobre ejecución**.

### 5. Patrones de nombres — **ENCONTRADO UN ERROR**

Contraejemplos que el clasificador actual no detecta correctamente:

- `Acta de conformidad.pdf` y `Acta de entrega del edificio.pdf`: no detecta recepción o aceptación.
- `Acta de comprobación del replanteo.pdf`: no lo detecta, aunque **no es** recepción final y no debería sumarse como fin (ilustra por qué ampliar palabras ciegamente también sería erróneo).
- `Certificación 15ª.pdf`, `Medición general.pdf`, `Cuenta general definitiva.pdf`, `CFO.pdf`, `Acta de cierre.pdf` o un nombre opaco como `documento_12345.pdf`: pueden escapar a las categorías; su significado no se puede determinar sin leer el contenido.
- Falsos positivos comprobados ejecutando el clasificador: `Liquidación de penalidades.pdf` se etiqueta `liquidacion`, pero no acredita liquidación del contrato; `Certificado final de obra.pdf` se etiqueta `final_obra`, aun cuando su contenido podría referirse a un tipo de certificación distinto. El propio CSV tiene una entrada con «liquidación penalidad» y otra con «recepción parcial»: la clasificación por palabras **no acredita** fin definitivo.

Recomendación: separar detección de **documentos candidatos**, verificación de **contenido** y conclusión sobre **estado de ejecución**. Conservar URI y contexto de cada adjunto y validar una submuestra estratificada.

### 6. Regla del tres — **NO ENCONTRADO** en el cálculo aproximado; **ENCONTRADA UNA LIMITACIÓN** de interpretación

Con 0 discrepancias en 30 casos independientes de una muestra aleatoria simple, la regla del tres da aproximadamente `3/30 = 10 %`; el límite binomial unilateral exacto al 95 % es `1 − 0,05^(1/30) ≈ 9,5 %`. Si la población final incluye 29/30 expedientes revisados, el cálculo conservador comparable sería `3/29 ≈ 10,3 %` (exacto ≈9,8 %). **No significa** que «como máximo» se escapen un 10 %: es un **límite estadístico sujeto a supuestos y al nivel de confianza**, no garantía. Tampoco mide la tasa de falsos negativos **condicionada a los documentos realmente existentes**, ya que en la muestra no apareció ningún caso positivo. La muestra inicial de 1.811 no invalida por sí sola la selección condicional de los 29 supervivientes, pero la selección y el análisis post hoc deben declararse y conviene sortear **otra muestra independiente y estratificada**, incluyendo los escasos casos positivos y expedientes `CERRADA`.

### 7. Correcciones posteriores — **NO ENCONTRADO** en su declaración; **ENCONTRADO UN RIESGO** de selección residual

El método declara expresamente que el filtro de resultados adjudicados y las categorías de incidencias se incorporaron después de inspeccionar ejemplos. Está bien y no equivale a manipulación encubierta. La población cayó de 1.811 a 1.631; **no está auditada aquí la explicación detallada de las 180 exclusiones**, más allá del ejemplo de uno de los 30. Las nuevas categorías no alteran el numerador de documentos de fin, pero la nueva selección sí podría hacerlo. Deben ofrecer un cuadro de exclusiones por código de resultado y publicar el script exacto y la muestra posterior a los cambios.

### 8. Interpretación del titular — **ENCONTRADO UN ERROR DE REDACCIÓN**

«No consta en los datos abiertos de la PLACSP cómo terminaron» sugiere que se inspeccionó exhaustivamente **todo el contenido, todos los documentos y todos los conjuntos de datos**, y que el objeto es un **contrato individual**. En realidad se midió la presencia de nombres de documentos que encajan en un clasificador, dentro del último *feed* sindicado, a nivel de expediente. Propuesta publicable **solo tras resolver la selección**:

> «En la extracción de la sindicación reutilizable de la PLACSP consultada hasta el 29 de octubre de 2026, el programa **no identificó por el nombre de los adjuntos** documentos clasificados como recepción, liquidación, certificación o terminación en **1.564 de 1.573 expedientes seleccionados con plazo teórico estimado anterior al corte**. El método no permite concluir que la obra no haya terminado, que esos documentos no existan o que no estén disponibles por otra vía».

Recomiendo **no difundir aún los números 1.564/1.573 como definitivos**: antes hay que recontar expedientes `CERRADA`, resolver la unidad de observación, comprobar el clasificador y volver a ejecutar contra el corpus completo.

### 9. Comparar tipos de administración — **NO ENCONTRADO** en la cautela; **NO PUEDO COMPROBAR** una comparación fiable

Es prudente no comparar tasas por administración con códigos cuyo significado cambia entre listas 1.04 y 2.10. Hay una ruta técnica: para **cada registro** leer `ContractingPartyTypeCode@listURI`/versión, interpretar su código conforme al catálogo correspondiente, definir categorías armonizadas auditables y comparar **muestras homogéneas**, declarando diferencias de cobertura y de contrato/lote. Sin reconstruir ese mapa no puede concluirse qué administración publica más o menos. La tabla generada sigue siendo susceptible de lectura comparativa engañosa: retirarla del informe de difusión o rotularla **«exploratoria, no comparable»**.

### 10. Relación con Democracia Auditable v0.4.1 — **NO ENCONTRADO** en el apoyo limitado; **NO PUEDO COMPROBAR** sus hipótesis fuertes

El experimento pone a prueba **una parte concreta** de la pregunta de §8.6: si los datos **sindicados públicamente** de PLACSP permiten observar documentos de cierre de obras seleccionadas. Encuentra una muy baja **visibilidad nominal de documentos de fin** en ese canal, coherente con una posible **brecha de observabilidad**. No prueba por sí solo que no existan documentos, que la Administración esté incumpliendo obligaciones, que ningún ciudadano pueda acceder a ellos mediante otros mecanismos, ni que falten datos en el Registro de Contratos del Sector Público. Tampoco prueba riesgo para la seguridad, ocultación deliberada, mala gestión o responsabilidades políticas. La propuesta de §9.0 podría valerse de este código como **primer experimento reproducible**, una vez depurado y replicado.

## Errores y riesgos ordenados por gravedad

1. **Alto — Sesgo de selección por tombstones (`:320–322`, `:382–385`).** `ANULADA` y `CERRADA` se confunden; archivar no es anular ni certifica la terminación. Exige conservar tipo, recuento y análisis de sensibilidad.
2. **Alto — Unidad de análisis errónea (`:179–301`, `:388–390`).** 1.631 filas son expedientes/licitaciones, no necesariamente 1.631 contratos individuales. Comprobados 300 expedientes con múltiples `TenderResult`.
3. **Alto — Sobreinterpretación de una búsqueda nominal (`:265–275`, `:439–449`, `:524–525`).** La ausencia de palabras en nombres de archivos no equivale a ausencia de información sobre finalización en datos abiertos de forma amplia.
4. **Medio-alto — Cálculo de plazos entre lotes (`:247–260`).** Puede mezclar inicio y modificaciones de distintos contratos; «plazo vencido» debe ser «fin teórico estimado anterior al corte».
5. **Medio — Actualizaciones con `updated` igual (`:369–372`).** Falso negativo demostrado con contraprueba ejecutada; la especificación reconoce la posibilidad de correcciones sin cambiar fecha.
6. **Medio — Falta contextualización semántica de documentos (`:265–275`).** Confunde, por ejemplo, una liquidación de penalidades con una liquidación del contrato; pierde nombres opacos y otros modos de certificación.
7. **Medio — Muestra de validación poco potente.** No incluye casos positivos en los 30 revisados; debe ampliarse y estratificarse. No prueba un «máximo» de error.
8. **Medio — No se analizan acuerdos marco y contratos basados por separado; tampoco las exclusiones exactas de los 180 registros tras la corrección.**
9. **Bajo-medio — Comparativa por administración sin normalización de la versión del código.** Evitar tasas interpretables como clasificación de organismos.
10. **Bajo — Trazabilidad de datos y ejecución:** no se adjuntan los ZIP originales ni sumas SHA-256 de cada descarga, versiones/fecha exacta del software o manifiesto verificable del lote; los ~6 GB no caben en el paquete, pero los checksums y comandos sí.

## Qué NO debería afirmarse en una entrega pública

- «1.631 contratos» sin aclarar que se trata de **filas por expediente**.
- «El 99,4 % de las obras no se terminó», «están retrasadas», «no han sido recepcionadas», «no se han liquidado» o «han desaparecido sus certificados».
- «La Administración incumple la ley al no publicar el final de las obras».
- «No existen datos de cierre en España»; el Registro de Contratos recibe por ley importe final y extinción, aunque no esté acreditado un fichero abierto individual accesible y comparable.
- «La ausencia de coincidencia en el nombre del archivo demuestra que falta el documento».
- «Hay un máximo del 10 % de errores»: no es una cota garantizada.
- «La investigación demuestra falta de supervisión, dolo, corrupción o riesgo material en una infraestructura concreta».
- «Resultado revisado de forma independiente sobre todo el corpus»: aquí **solo** se han reproducido pruebas, ejecución reducida y contrapruebas, no los 1.631 expedientes completos.

## Correcciones mínimas antes de repetir la fase 0

1. Registrar tombstones con `at:comment@type`, distinguir `ANULADA`/`CERRADA`, informar recuentos y sensibilidad.
2. Definir la unidad del estudio: expedientes con al menos un lote adjudicado **o** contratos individuales; ajustar titular y denominadores en consecuencia.
3. En expedientes multilote, asociar `TenderResult/Contract/ID` y `ContractModification/ContractID`; calcular plazos por contrato si el estudio necesita un «fin previsto».
4. Controlar empates de `updated` y detectar versiones distintas; registrar resolución y casos ambiguos.
5. Publicar indicadores separados de: datos estructurados, nombres candidatos, contenido efectivamente verificado, acceso a información externa y estado contractual acreditado. Añadir validación estratificada con casos positivos y negativos.
6. Separar los campos **«importe final tras modificación»** y **«importe real final de ejecución»**. Examinar si el Registro puede aportar información individual accesible por vías apropiadas.
7. Conservar las revisiones *ex ante* y *ex post*, un manifiesto con los ZIP y sus hashes, y una versión estable del código/datos que permita repetir el análisis.

## Fuentes primarias comprobadas

- PLACSP, **«Formato de sindicación y reutilización de datos sobre las publicaciones en la Plataforma de Contratación del Sector Público»**, versión 1.10, 17/09/2024: <https://contrataciondelsectorpublico.gob.es/datosabiertos/especificacion-sindicacion.pdf>. Revisar especialmente pp. 18–19 (`deleted-entry`), 21–22 (`updated` y versión completa), 27 (actualización), 32 (archivo), 141–143 (contratos/lotes), 152–166 (modificaciones), 176–178 (otros documentos).
- BOE, **Ley 9/2017 de Contratos del Sector Público, art. 346**: <https://www.boe.es/buscar/act.php?id=BOE-A-2017-12902>.
- Portal de Transparencia, **estadísticas del Registro de Contratos** (datos agregados): <https://transparencia.gob.es/publicidad-activa/por-materias/tramites/contratos-estadisticas>.
- Ministerio de Hacienda, **Registro de Contratos del Sector Público**: <https://www.hacienda.gob.es/es-es/areas%20tematicas/contratacion/junta%20consultiva%20de%20contratacion%20administrativa/paginas/registro%20publico%20de%20contratos.aspx>.

**Conclusión final:** Hay trabajo técnicamente serio, con metodología transparente, revisión humana declarada y pruebas que pasan. El resultado sugiere una cuestión de interés cívico sobre la escasa visibilidad de documentos finales en el *feed* abierto de PLACSP. **No es aún una cifra definitiva publicable sin recalcular y precisar la población y el tipo de evidencia realmente medido.**
