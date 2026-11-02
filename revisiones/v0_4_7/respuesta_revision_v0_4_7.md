# Respuesta a la revisión adversarial de la v0.4.7

**Fecha:** 2 de noviembre de 2026.
**Revisión respondida:** `REVISION_ADVERSARIAL_v0_4_7_CHATGPT.md`, de ChatGPT, sobre `para_chatgpt_v047.zip`.
**Método:** primero se reprodujo cada hallazgo y después se corrigió. Cada corrección tiene su prueba en `protocolo_obras/test_revision_v047.py`, con 14 pruebas.
**Resultado:** se aceptan los siete hallazgos. Las correcciones están en la **v0.4.8** (Anexo A.12). Ninguna cambia las cifras del estudio. Se añade además el documento breve que propuso la revisión.

## Hallazgos

### N01. Una fecha de ampliación mal escrita interrumpía la validación: aceptado

**Comprobación:** reproducido. Con `2026-02-XX` en Galicia o en Cataluña, `validar()` se cortaba con `TypeError`.

**Corrección:**
- `problema_ampliacion()` devuelve ahora «fecha_ampliacion mal escrita».
- `limite()` ya no calcula nada en ese caso.
- `validar()` informa del error de formato.

**Pruebas:** cubren los dos regímenes de Cataluña, Galicia y el régimen estatal.

### N02. Se aceptaba una ampliación anterior a la recepción: aceptado

**Comprobación:** reproducido. El programa calculaba el 20/04 como si la ampliación fuera válida.

**Corrección:** es un error cronológico indiscutible, recogido en `ampliacion_imposible()` junto con la ampliación posterior a la respuesta. No se calcula ninguna fecha.

**Fecha de notificación:** la guía y el programa ya dicen que `fecha_ampliacion` es la fecha en que se notificó la ampliación.

### N03. Una suspensión podía convertir en error una ampliación válida: aceptado

**Comprobación:** reproducido. Además, el rechazo seguía aunque hubiera una fecha verificada.

**Corrección:** se separan **errores** de **avisos**, como proponía la revisión.
- **Ampliación posterior al vencimiento provisional:** es un aviso (`ampliacion_aparentemente_tardia()` y `avisos()`).
  - `validar` lo muestra como «AVISO» y no da el registro por inválido.
  - No se calcula fecha provisional.
  - Los pendientes piden comprobar si hubo suspensión.
  - El aviso desaparece al anotar `fecha_limite_verificada`, que es la que se usa.
- **Ampliación anterior a la recepción o posterior a la respuesta:** sigue siendo un error.
- **Por qué no se añade una `fecha_limite_ordinaria_verificada`:** la fecha verificada final ya resuelve el caso, con un campo menos.

### N04. Se calificaba «fuera de plazo» un silencio antes de que venciera el plazo: aceptado

**Comprobación:** reproducido.

**Corrección:**
- `en_plazo(r, hoy)` recibe ahora una fecha de corte. Un silencio solo es «no» cuando la fecha verificada ya ha pasado.
- La fecha de corte es `--fecha` (hoy, por defecto) en `exportar` y en `resumen`.
- `validar` da error si se anota «silencio» antes de que venza la fecha verificada.

**Prueba:** cruza `exportar`, `pendientes`, `resumen` y `validar` sobre el mismo caso. Tres pruebas antiguas se adaptaron a la nueva firma de la función; está anotado en su código.

### N05. Una fecha verificada anterior a la recepción: aceptado

**Corrección:** error si `fecha_limite_verificada` no es posterior a `fecha_recepcion_organo`.

### N06. Festivos con un ámbito mal escrito: aceptado

**Corrección:** `avisos_festivos()` avisa en dos casos, y `validar` lo muestra como «AVISO»:
- una comunidad que no está en la tabla de regímenes, con la pista «¿falta una tilde?»;
- un ámbito que no coincide con ninguna fila del registro, sea una comunidad o un órgano.

**Interfaz:** ahora pasa el fichero de festivos también al comprobar el registro y al exportar, y muestra los avisos.

### N07. Rutas internas y precedentes: aceptado

**Rutas:**
- **Qué fallaba:** el documento remitía a `documento_v0_4_x/`, carpetas que no existen en el repositorio.
- **Corrección:** ahora remite a `revisiones/v0_4_x/`, en la Nota y en el Anexo B. Lo mismo en el código de las pruebas.

**Precedentes:**
- **Corrección:** en el complemento autonómico, solo llevan número las resoluciones citadas como precedente de un criterio que se explica (la de Madrid sobre la no preclusión, la de la GAIP sobre el abuso de derecho y las dos de la frase útil).
- **Las que solo ilustraban un resultado:** se describen sin número (Castilla y León, Canarias y otra de Madrid).
- **La regla, en el texto:** «no se publican las listas sistemáticas ni casos seleccionados para el protocolo».

## Otra corrección, señalada por el autor durante esta ronda

**Qué decía:** la tabla de herramientas de `PROTOCOLO_OBRAS.md` describía todavía la coincidencia de terminación como «validada» y decía que «capta en torno al 4 % de las resoluciones». Era una frase anterior a la v0.4.6, y ni las dos revisiones ni la respuesta anterior la detectaron.

**Corrección:** dice ahora que es una asociación preregistrada en un corpus parcialmente expuesto al diseño. Marcó el 3,7 % de los expedientes del grupo documental R estudiado (10 de 273), frente al 0,4 % del grupo N, y esa proporción no se extrapola a todas las resoluciones.

**Comprobaciones:**
- Hay una prueba para ello.
- Se buscó la misma formulación en el resto del proyecto. Solo queda en registros históricos que la marcan como corregida.

## Sobre la nota de verificación humana

Se acepta: el CSV no prueba que alguien verificara. `PROTOCOLO_OBRAS.md` recomienda ahora que el piloto guarde en el registro privado:
- la fuente del calendario;
- el justificante de recepción;
- las incidencias de suspensión;
- quién verificó y cuándo.

No se automatiza.

## Documento breve

**Dónde está:** `documento/Democracia_Auditable_resumen_v0_4_8.md` y su PDF de tres páginas, maquetado con el mismo aspecto que el documento completo.

**Qué se tomó de la propuesta de la revisión:** el formato (un documento breve para organizaciones que valoren un piloto), la lista de lo que debe quedar fuera y las etiquetas visibles («borrador», «sin piloto real», «sin validación jurídica ni humana», «revisado con IA»).

**Qué se cambió:** el contenido. La revisión proponía centrarlo en el estudio; el autor eligió un **documento de presentación de la propuesta entera**. Contiene:
- el problema;
- el protocolo en cinco pasos;
- qué se pretende conseguir;
- la medición de obras como primera aplicación;
- salvaguardas y estado.

Se contrastó con este documento y se corrigieron dos precisiones: el estudio no usa ninguna IA, no solo «IA generativa», y el criterio de importe es el presupuesto base **sin IVA**.

**Pendiente:** el correo corto de presentación no se ha redactado; es parte del envío y lo decide el autor.

## Estado

**Pruebas:** todas correctas, ninguna saltada, 154 en total:

| Conjunto | Pruebas |
|---|---|
| fase 0 | 32 |
| escáner | 7 |
| protocolo | 48 |
| revisión v0.4.5 | 26 |
| revisión v0.4.6 | 26 |
| revisión v0.4.7 | 14 |
| equivalencia | 1 |

**Documento:** v0.4.8, de 50 páginas, más la presentación de 3.

**Veredicto de la revisión:** distribuible como borrador crítico después de reparar N01 a N05, que están reparados.
