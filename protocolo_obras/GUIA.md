# Guía de uso: preguntar por el fin de las obras públicas

Esta guía es para quien vaya a aplicar el protocolo en una organización sin necesidad de saber programar. La justificación de cada regla está en `PROTOCOLO_OBRAS.md`.

**Antes de empezar, tres avisos:**
- **Las solicitudes las presenta la organización**, identificándose, por la sede electrónica de cada órgano. Las herramientas solo preparan el trabajo: **no envían nada**.
- **Es un diseño sin probar.** Conviene empezar con un piloto pequeño, por ejemplo 20–30 solicitudes, y publicar cómo sale.
- **Antes de usarlo a gran escala, consultad a un jurista**, sobre todo sobre el riesgo de que muchas solicitudes se consideren abusivas.

## Qué se necesita

- Un ordenador con **Python 3.11 o posterior** (python.org, instalación por defecto).
- Unos **15 GB libres** para los datos de la Plataforma de Contratación (la primera vez se descargan varios años).
- Una conexión estable. La primera descarga puede tardar horas; las siguientes, minutos.
- La carpeta del proyecto completa: `protocolo_obras/` necesita también `fase0_placsp/` e `investigacion_doc_ccn/`, que están a su lado.

## Sin terminal: la ventana del programa

Lo que explica esta guía se puede preparar desde una ventana, sin escribir órdenes. La ventana prepara borradores de solicitud, el registro y avisos de plazo provisionales; **la verificación (plazos, órgano de garantía, que la obra no tenga ya su final publicado) y la presentación de cada solicitud las hace siempre una persona**. En la carpeta `fase0_placsp`, haced doble clic en **`Abrir el programa.pyw`** (en macOS o Linux: `python interfaz.py`) y abrid la pestaña **«Preguntar por obras»**. Está organizada en los mismos pasos que esta guía:
1. **Preparar las solicitudes del mes:** el código de la organización, de dónde salen los datos (descargarlos o usar los que ya tenéis), qué obras van primero si hay que aplazar y un botón para el ciclo completo.
2. **Presentar y anotar:** botones para abrir lo que toca hacer, las solicitudes, el registro, los pendientes y la plantilla de reclamación.
3. **Seguimiento:** comprobar el registro, ver qué vence (con vuestro fichero de festivos, si lo indicáis), el resumen de resultados y el borrador para publicar.

Las opciones que no conviene tocar sin haberlo decidido antes (carpeta de trabajo, importe mínimo, tope por órgano, tamaño de la muestra) están plegadas en «Opciones avanzadas». El tope solo se puede bajar. Si canceláis el ciclo, al volver a pulsar se reanuda sin rehacer lo ya preparado. La ventana ejecuta por debajo las mismas órdenes que se explican a continuación, así que el resultado es idéntico.

## Una vez al mes: una sola orden

Abrid una terminal en la carpeta `protocolo_obras` y escribid, cambiando `NUESTRA_ORG` por un código breve de vuestra organización (no el nombre de una persona):

```
python -I -X utf8 ciclo_mensual.py --organizacion NUESTRA_ORG
```

Hace todo esto solo:
1. Descarga los datos nuevos de la Plataforma de Contratación.
2. Busca las obras de 1 M€ o más cuyo plazo terminó hace más de cuatro meses y que no han publicado su fin.
3. Prepara una solicitud ya redactada para cada obra nueva, con un máximo de 4 por órgano al mes sumando todos los lotes del mes. Nunca prepara dos veces la misma obra, y no deja rehacer un lote ya preparado.
4. La primera vez, sortea además una muestra fija de 200 obras antiguas, que se irá completando mes a mes.
5. Añade todo al registro y os dice qué tenéis pendiente.

Si el tope obliga a aplazar obras, por defecto van primero las más antiguas. Para dar prioridad a las que tienen señal de posible terminación anticipada, añadid `--prioridad terminacion` (qué es la señal y sus límites: `SENAL_TERMINACION.md`). Si ya tenéis los datos descargados, `--sin-descarga --datos "RUTA/*.zip"` los usa sin conectarse.

Al terminar tendréis en la carpeta:

| Fichero | Para qué sirve |
|---|---|
| `resumen_ciclo_AAAA-MM-DD.md` | Qué ha preparado y qué hay que hacer ahora |
| `lote_AAAA-MM-DD_flujo/solicitudes/` y `lote_AAAA-MM-DD_muestra/solicitudes/` | Una solicitud por obra, lista para copiar |
| `lote_…/lote.csv` | La lista de obras del lote: órgano, enlace a la Plataforma, a quién reclamar y, en `senal_terminacion`, si el mismo órgano licitó después la terminación de esa obra (posible contrato resuelto que no consta; ver `SENAL_TERMINACION.md`) |
| `pendientes_AAAA-MM-DD.csv` | Lo que vence y cuándo; se abre con cualquier hoja de cálculo |
| `registro.csv` | El registro de todas las preguntas; aquí se anota cada paso |

## Qué hacer con cada solicitud

1. **Abrid la solicitud** (`solicitudes/0001.txt`…) y completad el lugar, la fecha y la identificación del solicitante.
2. **Buscad la sede electrónica del órgano** (columna `organo` de `lote.csv`) y presentad la solicitud como «solicitud de acceso a información pública». Guardad el justificante.
3. **Anotad en `registro.csv`**, en la fila de esa obra (columna `id_obra`), la `fecha_envio` en formato AAAA-MM-DD y la `ref_solicitud`. Si el órgano os comunica cuándo recibió la solicitud el órgano competente, anotadla en `fecha_recepcion_organo`: el plazo se cuenta desde ahí. Si os notifican una **ampliación**, anotad en `fecha_ampliacion` la fecha en que os la **notificaron** (no la de la resolución que la acuerda): solo cuenta si llegó antes de que venciera el plazo ordinario y antes de la respuesta; si no, la validación lo señala. El registro se puede abrir con una hoja de cálculo; guardadlo como CSV en UTF-8.

## Cuando llegue la respuesta

Anotad en `registro.csv`:
- `fecha_respuesta`;
- `resultado`: `concedida`, `concedida_parcial`, `inexistente` (si dicen que el documento no existe), `remitida` (si la pasan a otro órgano), `inadmitida_18.1.x` o `denegada_limite`;
- `documentos`, separados por `;`: `acta_recepcion`, `certificacion_final`, `replanteo`, `suspension`, `ampliacion_plazo`, `resolucion_contrato`, `otro`;
- `fecha_replanteo` y `fecha_recepcion_obra`, si los documentos las indican.

**No publiquéis los documentos recibidos sin antes tachar los nombres de las personas** que aparezcan (técnicos, representantes de empresas).

## Si no contestan

- **Plazo de respuesta:** depende de la ley que se aplica a quien resuelve (columna `regimen` del registro). En general, un mes desde que la solicitud llega al órgano competente, ampliable otro mes con notificación; pero es de **20 días hábiles** (ampliables otros 20) en la Administración de la Comunidad de Madrid, en la de la Región de Murcia y en la Junta de Andalucía, y de **30 días hábiles** (ampliables otros 30) en Extremadura, también en sus ayuntamientos. La ampliación es de **quince días** en el País Vasco y de **hasta la mitad del plazo** en Cataluña; en Cataluña y Galicia, con una ampliación anotada, las herramientas no calculan la fecha. Si el último día es inhábil, el siguiente hábil.
- **Festivos:** las herramientas cuentan sábados, domingos y festivos nacionales. Para los demás, preparad un fichero con una fecha por línea y usad `--festivos festivos.txt` (en el ciclo mensual y en `registro.py pendientes`) o el campo «Festivos propios» de la ventana. Si preguntáis a órganos de sitios distintos, indicad a quién vale cada festivo: `2026-03-19 Comunitat Valenciana` (las filas de esa comunidad, escrita como en la columna `regimen`) o `2026-05-15 organo:ID` (las filas de ese órgano, para los festivos locales). Una fecha sola vale para todas las filas.
- **Fecha provisional y fecha verificada:** la fecha que calculan las herramientas es **provisional**: no conoce la recepción real si no la anotáis, ni el calendario completo del lugar, ni las **suspensiones** (por ejemplo, cuando el órgano pide alegaciones a la empresa, que suspende el plazo), ni si la ampliación es válida. **Si el régimen no está verificado, no se calcula ninguna fecha.** Antes de reclamar, una persona comprueba el vencimiento y lo anota en `fecha_limite_verificada`. Desde ese momento los avisos usan esa fecha, y **solo las filas con fecha verificada cuentan para decir si se respondió en plazo** (`en_plazo` y las cifras del resumen). Un silencio solo cuenta como «fuera de plazo» cuando esa fecha ya ha pasado (la fecha de corte es la de `--fecha`, hoy por defecto), y anotar `silencio` antes de que venza es un error.
- **Errores y avisos al comprobar el registro:** un **error** es algo imposible (una ampliación notificada antes de que el órgano recibiera la solicitud o después de responder, una fecha verificada anterior a la recepción, una fecha mal escrita) y hay que corregirlo. Un **AVISO** señala algo que puede estar bien: por ejemplo, una ampliación posterior al vencimiento provisional, que es válida si hubo una suspensión; desaparece al anotar `fecha_limite_verificada`. También avisa si una línea del fichero de festivos no coincide con ninguna fila (una comunidad sin tilde, un órgano que no está en el registro).
- **Si vence sin respuesta:** el fichero de pendientes os dirá «reclamar antes del …». Ese plazo es un criterio prudencial (un mes), no una fecha garantizada: en algunas comunidades (Cantabria, Navarra, País Vasco) la ley no pone plazo para reclamar contra el silencio, y en Cataluña cabe mediación; el fichero lo indica. Después, el fichero de pendientes muestra un plazo **orientativo** para que el órgano de garantía resuelva: tres meses en general y **dos en Cataluña** (la mediación lo suspende); donde la tabla no lo tiene localizado, pide seguimiento manual. Usad `plantillas/reclamacion_silencio.txt` y presentadla ante el órgano de garantía de la columna `garante`:
  - el Consejo de Transparencia y Buen Gobierno para la Administración del Estado y, por convenio, para algunas comunidades;
  - en las demás comunidades, su órgano propio.

  Comprobad antes que esa asignación sigue vigente.
- **Anotad** `fecha_reclamacion`, `ref_reclamacion` y, cuando llegue, `resultado_reclamacion` y `fecha_resolucion_reclamacion`.
- **Si os dan la razón pero no os entregan la información,** comunicadlo al órgano de garantía y anotad `cumplimiento` = `no_consta`.

## Reglas que no hay que saltarse

- **Una sola solicitud por obra, nunca repetida.** Preguntar varias veces por la misma obra se ha considerado abusivo.
- **No adelantar preguntas.** La herramienta espera a que hayan pasado cuatro meses desde el fin previsto. Es un umbral práctico, no un plazo legal: muchas obras se reciben más tarde, y «aún no se ha recibido» es una respuesta legítima.
- **No señalar a nadie.** Se publican hechos (respuesta o silencio, documentos, fechas), no juicios sobre personas u órganos.
- **Coordinarse con otras organizaciones** que apliquen el protocolo, compartiendo el registro o al menos la lista de obras ya preguntadas, para no duplicar preguntas.

## Publicar los resultados

```
python -I -X utf8 registro.py exportar
python -I -X utf8 registro.py resumen
```

`exportar` crea `registro_publico_BORRADOR.csv`, sin datos del solicitante ni notas internas y, por defecto, **sin identificadores de obra ni de órgano** (enlace, expediente, órgano, garante). Incluirlos (`registro.py exportar --con-identificadores`) es una decisión editorial que tomáis aparte: permite comprobar cada caso, pero también señalar a órganos concretos. **Es un borrador:** antes de publicar cualquier versión, revisad caso por caso que los enlaces y las fechas no permitan identificar a personas en los documentos enlazados, y que ninguna fila parezca un juicio sobre un órgano o una persona. El resto de ficheros (lotes, registro, pendientes) contienen datos de trabajo y no se publican.

## Comprobaciones útiles

```
python -I -X utf8 registro.py validar      # detecta fechas mal escritas, valores no permitidos o preguntas repetidas
python -I -X utf8 registro.py pendientes   # vuelve a calcular lo que vence
python -I -X utf8 test_protocolo.py        # comprueba que las herramientas funcionan (deben pasar todas las pruebas)
```

## Problemas frecuentes

- **«No hay ficheros de datos»:** la descarga falló. Repetid la orden; continúa donde se quedó.
- **La columna `garante` es solo una sugerencia** («sugerido, sin verificar»): se deduce del tipo de entidad y de la provincia del órgano. Verificadla siempre antes de reclamar; si dice «comprobar», buscadlo a mano.
- **La obra ya está terminada y publicada:** si al abrir el enlace veis el acta de recepción, no enviéis la solicitud. Poned `resultado` = `descartada`, anotad en `notas` que ya constaba y dejad `fecha_envio` vacía. Así deja de aparecer en los pendientes.
