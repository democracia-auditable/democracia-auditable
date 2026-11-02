# Protocolo de preguntas sobre el fin de las obras públicas

**Versión 0.4, 2 de noviembre de 2026. Diseño para un piloto, no herramienta jurídica operativa.** No lo ha revisado ningún jurista ni se ha probado con solicitudes reales. La v0.4 incorpora la revisión adversarial de la v0.4.6 del documento (`respuesta_revision_v0_4_6.md`): ampliación y plazo del órgano de garantía según la ley, ampliaciones solo si se notificaron a tiempo, festivos por comunidad u órgano y calificación «en plazo» solo con la fecha límite verificada por una persona; y, tras la revisión de la v0.4.7, la validación del registro distingue errores de avisos, rechaza ampliaciones y fechas verificadas anteriores a la recepción, no califica un silencio «fuera de plazo» antes del vencimiento verificado y avisa de festivos sin fila (`test_revision_v047.py`). La v0.3 incorporó la de la v0.4.5 (plazos según la ley aplicable, tope, muestra persistente, registro robusto, reanudación y exportación sin identificadores), y la v0.2, la de la v0.4.4 (plazos con días inhábiles, control de duplicados y tope mensual, seguimiento de la muestra, plantilla más precisa y exportación como borrador). Las respuestas están en `revisiones/`. Herramientas: código MIT-0; texto CC0.

**Antes de usarlo con solicitudes reales:**
- supervisión jurídica de la organización que lo adopte, sobre todo del riesgo de abuso de derecho y del cómputo de plazos;
- un piloto pequeño (20–30 solicitudes) con su resultado publicado.

## Para qué sirve

El estudio de fase 0 encontró que en el 97,2 % de las obras de su población con el plazo previsto vencido no consta en la sindicación de la Plataforma de Contratación del Sector Público (PLACSP) ningún indicador de fin detectado por el programa. Las investigaciones posteriores aclararon por qué y qué se puede hacer:

- **Publicar el fin no es obligatorio con carácter general,** pero el acta de recepción y la certificación final **deben existir cuando la obra se ha recibido** (LCSP, art. 243) y son **información pública** (Ley 19/2013, art. 13). Ver `investigacion_juridica/INFORME_JURIDICO.md`.
- **En las resoluciones examinadas, el Consejo de Transparencia reconoce el acceso** a esos documentos y la Administración cumplió, aunque con retrasos frecuentes. En dos órganos autonómicos revisados de forma sistemática, ninguno de los pocos casos sobre documentación del fin de obras públicas se desestimó. También ha considerado abusivo pedir de forma repetida documentos parciales de una misma obra. Ver `investigacion_consejo/INFORME_CONSEJO.md`.
- **Un registro abierto puede publicar el fin,** pero incluso así falta en más de la mitad de las obras. Ver `investigacion_registro_vasco/INFORME_REGISTRO_VASCO.md`.

El protocolo convierte esto en un procedimiento: **una pregunta por expediente, sobre los documentos finales, cuando razonablemente deberían existir, con la respuesta o el silencio registrados para que nadie tenga que volver a preguntar.**

## Las reglas

1. **Qué obras.** Expedientes de obras de la PLACSP adjudicados, con presupuesto base de **1 M€ o más** sin IVA (configurable), sin anuncio de finalización ni otro indicador de fin (incluido el texto de sus modificaciones). «Obra» significa aquí **expediente**, que puede contener varios contratos o lotes.
2. **Cuándo.** A partir de **120 días después del fin teórico estimado**. Es un **umbral operativo de contacto, no un plazo legal ni un indicador de retraso**. Se eligió así porque la recepción se hace dentro del mes siguiente a la terminación (art. 210.2 LCSP) y la certificación final debe aprobarse en los tres meses siguientes a la recepción (art. 243.1; hasta cinco en algunas obras de más de 12 M€). Pero la recepción real puede ser muy posterior al fin estimado, así que una respuesta de «la obra aún no se ha recibido» es legítima.
3. **Qué se pide.** Copia del **acta de recepción** y de la **certificación final**, si existen. Si las obras no se han recibido, que se indique y se aporten, solo si existen y por este orden: el acuerdo de resolución, el último acuerdo de suspensión o de ampliación de plazo y el acta de comprobación del replanteo. Nunca certificaciones periódicas. Se piden documentos existentes, no información elaborada (art. 18.1.c).
4. **A quién.** Al órgano de contratación que figura en la PLACSP. Si no tiene los documentos, debe remitir la solicitud a quien los tenga (art. 19.1; R CTBG 2025-1472).
5. **Una sola vez.** Una solicitud por expediente, nunca repetida. El Consejo ha desestimado por abuso series de solicitudes sobre la misma obra y ha señalado que se habría obtenido lo mismo pidiendo una vez la certificación final (R/0863/2021). Las herramientas excluyen todo expediente que ya figure en el registro **o en cualquier lote preparado**.
6. **Tope por órgano.** Como máximo **4 solicitudes por órgano y mes, contando todos los lotes del mes y los envíos registrados**. No existe la opción «sin tope»: las herramientas solo admiten de 1 a 4, y un tope mayor exige una justificación que queda escrita en el lote (`parametros.json`); la interfaz solo permite bajarlo. Un cerrojo impide dos selecciones a la vez (si quedó de una ejecución interrumpida, se retira solo), y un lote preparado no se puede sobrescribir. El tope reduce la carga, pero **no es una garantía frente a la inadmisión por abuso**.
7. **Silencio.** El plazo para resolver **depende de la ley aplicable** a quien resuelve, y se cuenta **desde que la solicitud llega al órgano competente**. Con carácter general es de un mes, ampliable a dos con notificación (Ley 19/2013, art. 20.1), pero hay leyes autonómicas con otros plazos: **20 días hábiles** en la Administración de la Comunidad de Madrid, en la de la Región de Murcia y en la Junta de Andalucía, y **30 días hábiles** en Extremadura, también para sus entidades locales. La ampliación también cambia: **quince días** en el País Vasco y **hasta la mitad del plazo inicial** en Cataluña; la ley gallega no la menciona. Solo cuenta una ampliación notificada antes del vencimiento ordinario y de la respuesta. El plazo para reclamar contra el silencio es, en general, de un mes (art. 24.2), pero en Cantabria, Navarra y el País Vasco la ley dice que no está sujeto a plazo, en Cataluña cabe mediación, y en Madrid su órgano de garantía aplica un criterio de no preclusión aunque la ley diga un mes. La tabla con la cita del BOE de cada régimen está en `regimenes.py` (fragmentos en `fuentes/regimenes/`); el régimen de cada obra se anota en la columna `regimen`. Las herramientas calculan vencimientos **provisionales** (días inhábiles: sábados, domingos y festivos nacionales; los autonómicos y locales se añaden con `--festivos`, para todas las filas, para una comunidad o para un órgano; si no se ha anotado la recepción por el órgano, desde la fecha de envío) y **no calculan ninguna fecha cuando el régimen no está verificado** (tipo de entidad sin ámbito claro, comunidad desconocida o aplicación dudosa, como el plazo de 20 días en las entidades locales de Madrid) ni cuando la ampliación no se puede calcular con seguridad. No conocen las suspensiones (alegaciones de terceros, subsanación). Por eso el vencimiento que se usa para calificar una respuesta es el que una persona **verifica y anota** en `fecha_limite_verificada`; el calculado solo sirve para avisar. El plazo del órgano de garantía para resolver también depende de la ley (tres meses en general, **dos en Cataluña**, con suspensión por mediación) y se muestra como orientativo. Si vence sin respuesta, se reclama **dentro del mes siguiente**: es un **criterio prudencial**, válido en todos los regímenes revisados porque ninguno da menos de un mes para reclamar. **Es una lectura de un no jurista: cada vencimiento, régimen y órgano de garantía se verifican a mano antes de reclamar.**
8. **Registro.** Cada paso se anota en `registro.csv`: envío, recepción por el órgano, ampliación, respuesta, documentos, fechas de replanteo y recepción, reclamación, resolución y cumplimiento. Una obra que no se pregunta porque su fin ya era público se marca como `descartada`.
9. **Publicación.** `registro.py exportar` produce un **borrador** sin datos del solicitante ni notas internas y, por defecto, **sin identificadores de obra ni de órgano** (enlace, expediente, órgano, garante); incluirlos (`--con-identificadores`) es una decisión editorial expresa. Antes de publicar cualquier versión hace falta una revisión de privacidad caso por caso, porque los enlaces y las fechas pueden permitir identificar a personas en los documentos enlazados, y una revisión editorial que evite cualquier apariencia de juicio sobre un órgano o una persona. Los lotes (con la columna de la coincidencia de terminación) son ficheros de trabajo privados. Los documentos recibidos solo se publican tras disociar los datos personales; los originales se custodian de forma privada.

## Cuántas preguntas serían

`volumen.py`, sobre el estado final de las obras del corpus 2021–octubre de 2026. Obras sin indicador de fin definitivo cuya fecha de pregunta (fin teórico + 120 días) cae en 2025:

| Tramo (presupuesto sin IVA) | Preguntas al año | Órganos | Por órgano: mediana / p90 / máximo | Órganos con más de 12 al año |
|---|---:|---:|---|---:|
| Menos de 1 M€ | 18.092 | 3.361 | 2 / 8 / 2.412 | 194 |
| 1–10 M€ | 1.653 | 567 | 1 / 5 / 76 | 16 |
| Más de 10 M€ | 186 | 79 | 1 / 4 / 39 | 3 |
| **1 M€ o más** | **1.839** | 591 | 1 / 5 / 115 | 19 |

- **Ritmo:** el tramo de 1 a 10 M€ supone unas 140 preguntas al mes, bastante uniformes a lo largo del año.
- **A quién se reclamaría** (1 M€ o más, 2025): 1.065 casos ante órganos autonómicos o locales, 651 ante el Consejo estatal y 123 sin ámbito claro.
- **Efecto del tope** (1 a 10 M€, 2025): con 1 solicitud por órgano y mes quedarían sin enviar a final de año el 21 %; con 2, el 12 %; con 4, el 3 % (5 órganos afectados); con 8, ninguna.

**Lectura.** Para la gran mayoría de los órganos serían una o dos preguntas al año. La carga se concentra en una veintena de órganos con mucho volumen, y el tope la reparte a lo largo de los meses. Un plan a esta escala necesitaría una entidad responsable y una valoración de su impacto administrativo: **es una simulación, no un piloto avalado**.

## Herramientas

| Fichero | Qué hace |
|---|---|
| `ciclo_mensual.py` | El ciclo de cada mes en una orden: descarga, escaneo, lotes (flujo y muestra), registro, pendientes y resumen. Ver `GUIA.md` |
| `seleccionar_obras.py escanear` | Lee los ZIP con la misma política de versiones que el estudio; el título y el código postal no intervienen en el desempate de versiones |
| `seleccionar_obras.py seleccionar` | Elige las obras a las que toca preguntar; excluye las ya registradas o preparadas; aplica el tope mensual; escribe el lote, una solicitud por obra y, en las muestras, `seguimiento_muestra.csv` |
| `registro.py` | `crear`, `validar`, `pendientes` (vencimientos provisionales con días inhábiles), `resumen` y `exportar` (borrador) |
| `plantillas/` | Solicitud y reclamación por silencio |
| `senal_terminacion.py` | Coincidencia «terminación licitada de nuevo»: una marca obliga a verificar, su ausencia no informa. Asociación preregistrada en un corpus parcialmente expuesto al diseño, no una validación: marcó el 3,7 % de los expedientes del grupo documental R estudiado (10 de 273, con indicios documentales de resolución) frente al 0,4 % del grupo N; esa proporción no se extrapola a todas las resoluciones. Ver `SENAL_TERMINACION.md` |
| `volumen.py` | Volumen y efecto del tope |
| `../fase0_placsp/interfaz.py` | Interfaz gráfica: la pestaña «Preguntar por obras» prepara borradores, registro y avisos provisionales sin terminal (en Windows, doble clic en `Abrir el programa.pyw`); la verificación y la presentación son humanas |
| `regimenes.py` | Plazo para resolver y para reclamar contra el silencio por régimen (comunidad y ámbito), con la cita del BOE de cada fila; sin régimen verificado no se calcula ninguna fecha |
| `test_revision_v045.py` | Pruebas de las correcciones de la revisión adversarial de la v0.4.5 (una por hallazgo) |
| `test_protocolo.py` | 48 pruebas (incluida una por cada condición de la señal de terminación, la prioridad en el ciclo mensual y la orden que construye la interfaz): plazos e inhábiles, validación, pendientes, exportación, descartadas, órgano de garantía, plantilla, tope mensual entre lotes, cerrojo, lotes no sobrescribibles, muestra fija y su seguimiento, y ciclo mensual |

Las órdenes paso a paso están en `GUIA.md`. Opciones de `seleccionar`:
- `--min` y `--max`: tramo de presupuesto;
- `--margen`: días después del fin teórico (por defecto, 120);
- `--tope`: solicitudes por órgano y mes (por defecto, 4);
- `--desde`: solo el flujo reciente;
- `--muestra N --semilla S` y `--lista muestra.csv`: muestra fija del acumulado;
- `--nombre`: sufijo del lote;
- `--forzar`: rehacer un lote descartado;
- `--prioridad antiguedad|terminacion`: orden cuando el tope obliga a aplazar. Con `terminacion`, primero las obras con la coincidencia «terminación licitada de nuevo» (`SENAL_TERMINACION.md`). Cada lote indica la coincidencia en la columna `senal_terminacion`, sea cual sea la prioridad. La muestra fija se sortea sobre el marco ordenado por identificador, antes de aplicar la prioridad, así que no depende de ella. **El flujo no reserva una parte aleatoria:** si va priorizado, sus cifras describen lo preguntado, no la población; las proporciones de todas las obras se estiman solo con la muestra fija (el registro anota el `origen` de cada solicitud y el resumen los separa).

## A quién se reclama

Según la disposición adicional cuarta de la Ley 19/2013 y los convenios publicados por el Consejo de Transparencia y Buen Gobierno (consultados el 01/11/2026; `fuentes/ctbg_convenios_ccaa_20261101.txt`):

| Órgano requerido | Órgano de garantía |
|---|---|
| Administración General del Estado y sector público estatal | Consejo de Transparencia y Buen Gobierno |
| Asturias, Cantabria, Extremadura, Illes Balears, La Rioja, Ceuta y Melilla, y sus entidades locales | Consejo de Transparencia y Buen Gobierno, por convenio |
| Resto de comunidades autónomas y sus entidades locales | Órgano de garantía propio de cada comunidad |

`seleccionar_obras.py` propone el órgano de garantía a partir del tipo de entidad y de la provincia del código postal del órgano, y lo marca como **«sugerido, sin verificar»**. La ubicación no siempre determina la adscripción: consorcios, entidades mixtas u organismos autónomos pueden requerir análisis propio, y los convenios cambian. **Hay que verificarlo antes de cada reclamación.**

## Cómo coordinarse entre organizaciones

- **Un único registro compartido**, o al menos la carpeta de lotes y la lista de obras ya preguntadas. Las herramientas solo ven los lotes y el registro de su carpeta: sin compartirlos, dos organizaciones podrían preguntar por la misma obra o superar entre ambas el tope de un órgano.
- **Repartir por órganos o por territorios**, no por obras sueltas.
- **Publicar los hechos de cada pregunta**, sin juicios.

## Qué medirá el protocolo y qué no

**Mide:**
- la proporción de preguntas respondidas en plazo, fuera de plazo o no respondidas;
- la proporción de obras con el acta de recepción ya firmada;
- la diferencia entre el fin teórico y la fecha real de recepción;
- el resultado y el cumplimiento de las reclamaciones.

`en_plazo` solo se calcula con la fecha límite verificada a mano (`fecha_limite_verificada`), a una fecha de corte (un silencio no es «fuera de plazo» hasta que esa fecha ha pasado), y las cifras de plazos del resumen solo cuentan esas filas. El CSV no prueba por sí mismo que alguien verificara: para un piloto, conviene guardar en el registro privado la fuente del calendario, el justificante de recepción, las incidencias de suspensión y quién y cuándo verificó. Aun así son indicadores, no determinaciones jurídicas: la verificación la hace la organización, sin revisión jurídica salvo que la busque.

**No mide:** la calidad de la obra, si un retraso está justificado ni la conducta de nadie. Un silencio es un dato sobre la respuesta, no sobre la obra.

## Riesgos y cuestiones abiertas

- **Abuso de derecho (art. 18.1.e).** Las resoluciones examinadas lo aprecian por insistir sobre la misma obra. Que una entidad pregunte por muchas obras distintas no se ha examinado: **requiere criterio jurídico**. Las reglas lo mitigan, pero no son un salvoconducto.
- **Plazos.** Los vencimientos dependen de la fecha real de recepción por el órgano competente, de los calendarios autonómicos y locales, de las notificaciones de ampliación y de posibles suspensiones. Las herramientas no conocen nada de eso si no se anota.
- **Identificación del solicitante.** La solicitud exige identificarse (art. 17.2). Corresponde a cada organización decidir quién firma.
- **Cobertura.** Solo los perfiles alojados en la PLACSP.
- **Inicio de la obra.** Los datos abiertos tienen escasa capacidad para distinguir una obra terminada sin publicarlo de una que no empezó (`investigacion_inicio/INFORME_INICIO.md`). Por eso se pide el replanteo cuando no hay recepción, y **ningún criterio de prioridad debe usar la ausencia de rastro como señal de anomalía**.
- **Fin teórico estimado.** Si una ampliación no se publicó, la pregunta puede llegar antes de tiempo. La plantilla lo prevé.

## Arranque: flujo mensual y obras acumuladas

Al arrancar hay **todas las obras acumuladas** desde 2021 sin fin publicado, no solo las del mes. Con `--fecha 2026-11-01` (1 M€ o más, sin registro previo; cifras de la v0.1, antes del tope mensual común):

| Selección | Candidatas | En el lote (tope 4 por órgano) | Órganos |
|---|---:|---:|---:|
| Todo lo acumulado | 8.666 | 3.100 | 1.298 |
| Flujo del último mes (`--desde 2026-10-01`) | 267 | 211 | 155 |
| Muestra del acumulado (`--muestra 200`, semilla 20261101) | 200 | 186 | 142 |

**Recomendación:**
- **Flujo, completo:** cada mes, las obras cuya fecha de pregunta llegó desde el ciclo anterior.
- **Acumulado, por muestra fija:** 200 obras sorteadas una vez. **Solo bajo muestreo aleatorio simple y con respuesta completa**, el margen de error al 95 % sería de unos ±7 puntos. Con aplazamientos, falta de respuesta, cambios de elegibilidad y agrupamiento por órgano, el margen real será mayor y puede haber sesgo: hay que publicar la tasa de respuesta, las pérdidas y un análisis de sensibilidad.
- **Seguimiento de la muestra:** el marco (`muestra.csv`) se congela y no se vuelve a sortear; `marco_muestra.json` guarda la fecha, la semilla, el tamaño pedido y el obtenido, los parámetros y la huella del marco. Si hay 200 candidatas o menos, la muestra son todas, y se guarda igualmente. Cada lote de muestra deja `seguimiento_muestra.csv` con el estado de cada una de las 200: en este lote; ya preparada o registrada; aplazada por el tope; excluida y por qué (por ejemplo, porque publicó su fin después); o desaparecida de los datos.

## Prueba

- **Escaneo** (15 ZIP de 2021 a octubre de 2026): 156.277 obras, el mismo número que la rama 2, con 0 discrepancias en identificadores, indicador de fin y fin teórico.
- **Ciclo mensual completo** (`ciclo_mensual.py --sin-descarga`, fecha 01/11/2026, carpeta temporal): escaneo, lote de flujo (210), muestra (180), 384 obras en el registro, validación correcta y pendientes. Esta prueba **descubrió que 6 obras salían a la vez en el lote de flujo y en el de muestra**, el mismo fallo que señaló la revisión (P7). Corregido: los lotes se excluyen entre sí y comparten el tope mensual.
- **Segundo ciclo** (fecha 01/12/2026): 563 obras en lotes entre los dos meses, ninguna repetida, y como máximo 4 por órgano y mes. Como la muestra comparte el tope con el lote del mes, **se completa en varios meses**: en diciembre, 49 de las 200 seguían aplazadas por el tope.
- **Pruebas automáticas:** 48 en `test_protocolo.py`, 26 en `test_revision_v045.py` (una por cada hallazgo de la revisión adversarial de la v0.4.5: regímenes y plazos, muestra persistente y sorteo independiente de la prioridad, validación robusta, tope, origen de cada solicitud, ciclo que no avanza con errores y se reanuda, festivos, exportación sin identificadores, `.gitignore`) y 26 en `test_revision_v046.py` (los hallazgos de la de la v0.4.6: ampliaciones por régimen, plazo de cada órgano de garantía, ampliaciones fuera de tiempo, festivos por territorio, calificación solo con fecha verificada, fuentes y ámbito de cada ley y citas de resoluciones) y 14 en `test_revision_v047.py` (los de la v0.4.7: validación sin excepciones, cronología de la ampliación, avisos frente a errores, silencio antes del vencimiento, festivos mal escritos, rutas y descripción de la coincidencia de terminación), todas correctas. Son pruebas con datos ficticios: no sustituyen a un piloto supervisado ni a una revisión jurídica.
- **Datos reales:** los lotes y registros de prueba se generan en carpetas temporales o se borran. `.gitignore` excluye todas las salidas con datos reales.

**No se ha enviado ninguna solicitud.**
