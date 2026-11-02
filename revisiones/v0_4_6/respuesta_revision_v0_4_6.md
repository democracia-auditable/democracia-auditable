# Respuesta a la revisión adversarial de la v0.4.6

**Fecha:** 2 de noviembre de 2026
**Revisión:** `REVISION_ADVERSARIAL_v0_4_6_CHATGPT.md` (ChatGPT, sobre `para_chatgpt_v046.zip`).
**Método:** cada hallazgo se comprobó en el código y en los textos consolidados del BOE, guardados en `protocolo_obras/fuentes/regimenes/`, y se reprodujo cuando era posible. Después se corrigió, con una prueba por hallazgo en `protocolo_obras/test_revision_v046.py`. Además, se revisaron **todas** las filas de la tabla de regímenes, no solo las señaladas, y eso sacó dos errores más.
**Resultado:** se aceptan los ocho hallazgos. En V08 se adopta una de las dos opciones que proponía la revisión. Las correcciones están en la **v0.4.7** (Anexo A.11). Ninguna cambia las cifras del estudio.

## Hallazgos

### V01: la ampliación de Euskadi es de quince días. Aceptado

**Comprobación.** El art. 37.2 de la Ley 3/2026 dice «por otros quince días más». El programa doblaba el plazo y daba el 12/03/2026 en el caso de la revisión.

**Corrección:**
- Cada régimen lleva ahora su propia ampliación, con unidad y fuente (`ampliacion` y `fuente_ampliacion` en `regimenes.py`).
- En Euskadi son 15 días hábiles: los «días» sin más son hábiles por el art. 30.2 de la Ley 39/2015.
- Si la unidad de la ampliación no es la del plazo, la ampliación se cuenta desde el final del plazo ordinario. En el caso de la revisión da el 05/03/2026, como ella calculó.

**Pruebas:** el caso de la revisión, el mismo caso con un festivo de la comunidad, y el resto de ampliaciones.

### V01 bis: dos errores más, encontrados al revisar todas las filas. Corregidos

- **Cataluña.** El art. 33.2 de la Ley 19/2014 permite una prórroga «hasta un plazo igual a la mitad del inicial», no otro mes. La revisión no lo señaló. Medio mes no tiene un cómputo inequívoco, así que, con una ampliación anotada, el programa no calcula la fecha y pide verificarla a mano.
- **Galicia.**
  - **Ampliación:** el art. 27.4 de la Ley 1/2016 fija un mes «como más tarde» y no menciona ampliación. Con una ampliación anotada, tampoco se calcula la fecha.
  - **Entidades locales:** el art. 3.1 no incluye a las entidades locales, así que para ellas pasa a regir la ley estatal. El plazo numérico no cambia.

### V02: la GAIP resuelve en dos meses. Aceptado

**Comprobación.** El art. 42.9 de la Ley 19/2014 fija dos meses desde la presentación, y la Comisión puede ampliarlo quince días. El art. 42.4 dice que la mediación suspende el plazo. El programa aplicaba tres meses a todas las reclamaciones.

**Corrección.** Cada régimen lleva ahora el plazo de su órgano de garantía (`garante` y `fuente_garante`):
- **tres meses** donde la ley revisada lo dice: Estado, Aragón, Cantabria, Castilla-La Mancha, Castilla y León (por remisión al art. 24 de la ley estatal), Comunitat Valenciana, Navarra y Euskadi;
- **dos meses en Cataluña**, con la advertencia de la mediación y la ampliación;
- **seguimiento manual** donde el texto guardado no lo fija: Andalucía, Extremadura, Galicia, Madrid, Murcia, Canarias, Asturias, La Rioja, Baleares, Ceuta y Melilla. Para Andalucía y Extremadura, la remisión a la legislación básica no se ha dado por suficiente.

El aviso habla ahora de «plazo orientativo» y pide comprobar si hubo mediación, suspensión o ampliación.

**Pruebas:**
- **Cataluña:** el 20/02 da el 20/04 («2 meses», con mediación).
- **Estado:** el 20/02 da el 20/05.
- **Madrid:** seguimiento manual.

### V03: ampliaciones retroactivas o posteriores a la respuesta. Aceptado

**Comprobación.** Se reprodujo el caso de la revisión:
- recepción el 12/01;
- respuesta el 01/03;
- ampliación anotada el 01/04.

`validar()` no daba errores y `en_plazo()` respondía «sí».

**Corrección:**
- Una ampliación solo cuenta si se notificó **antes del vencimiento ordinario** y **antes de la respuesta** (`ampliacion_fuera_de_tiempo`). Si no, la validación da un error y no se calcula ninguna fecha.
- La guía y el programa dicen ahora que `fecha_ampliacion` es la fecha en que se **notificó** la ampliación, no la de la resolución que la acuerda.
- No se añade un campo para la prueba de la notificación: el registro ya admite notas y el justificante lo guarda la organización.

**Pruebas:** ampliación después del vencimiento, ampliación después de la respuesta y ampliación a tiempo.

### V04: un calendario único para órganos de sitios distintos. Aceptado

**Corrección.** El fichero de festivos admite tres formas, una por línea:

| Línea | Vale para |
|---|---|
| `AAAA-MM-DD` | todas las filas |
| `AAAA-MM-DD Comunidad` | las filas de esa comunidad, escrita como en la columna `regimen` |
| `AAAA-MM-DD organo:ID` | las filas de ese órgano, para los festivos locales |

La guía explica que una fecha sola vale para todas las filas. Además, según V07, ninguna respuesta se califica con un calendario sin verificar.

**Pruebas:** dos filas de comunidades distintas con un festivo que solo vale en una; un festivo de un órgano; y una fecha sin ámbito.

### V05 y V07: suspensiones y recepción sin verificar en las cifras. Aceptado

**Por qué se resuelven juntos.** Calcular cada suspensión en el programa exigiría conocer cada trámite de alegaciones o de subsanación, y lo habitual es que la organización no lo sepa hasta que el órgano lo comunica. En vez de añadir campos de suspensión, se separan las dos fechas que la revisión pedía distinguir:
- **la fecha calculada** sigue existiendo, pero solo como **aviso provisional**. En el borrador exportado aparece como `fecha_limite_provisional`;
- **una persona verifica** la recepción real, el calendario del lugar, las suspensiones y la ampliación, y **anota `fecha_limite_verificada`**.

**Qué cambia en el programa:**
- Solo con la fecha verificada se calcula `en_plazo`, y solo esas filas entran en las cifras de plazos del resumen. El resumen dice cuántas filas quedan fuera.
- Los avisos usan la fecha verificada cuando existe y lo indican.
- Los avisos provisionales recuerdan comprobar el calendario, las suspensiones y la ampliación.

**Pruebas:**
- sin fecha verificada, la respuesta no se califica;
- con fecha verificada, se califica «sí» o «no»;
- el resumen solo cuenta las filas verificadas;
- los avisos usan la fecha verificada;
- la validación rechaza una fecha verificada mal escrita o anterior al envío.

**Efecto en las pruebas anteriores.** Este cambio afecta a dos pruebas de rondas anteriores. Se reescribieron para la regla nueva, y queda anotado en su código:
- `test_en_plazo` en `test_protocolo.py`;
- la del resumen en `test_revision_v045.py`.

### V06: fuentes de Castilla y León y de Castilla-La Mancha. Aceptado

**Comprobación.**
- **Castilla y León:** el art. 9 de la Ley 3/2015 trata de la reutilización.
- **Castilla-La Mancha:** el art. 33.1 de la Ley 4/2016 vale solo para los sujetos de su art. 4.1.a, y el art. 4.2 remite a las entidades locales a la legislación básica. Ambos textos se añadieron a los fragmentos guardados.

**Corrección.**
- **Castilla y León:** en lo autonómico y en lo local, cita la ley estatal (art. 20.1); para la reclamación, el art. 8.2, que remite al art. 24 de la ley estatal.
- **Castilla-La Mancha, autonómico:** cita el art. 33.1 para los sujetos del art. 4.1.a y la ley estatal para el resto.
- **Castilla-La Mancha, local:** cita la ley estatal.

**Revisión cruzada del ámbito personal de todas las filas.** Se descargó del BOE el artículo de ámbito de las leyes cuyos fragmentos no lo tenían: Galicia, Navarra, Valencia, Euskadi y Cataluña.
- **Galicia:** su ley no incluye a las entidades locales (ver V01 bis).
- **Las demás:** sí las incluyen. Cada fila local con ley propia cita ahora el artículo que las incluye.

**Pruebas:**
- ninguna de las dos fuentes corregidas cita el artículo erróneo;
- toda fila local con ley autonómica cita su artículo de ámbito;
- las citas de ámbito y de ampliación están, literalmente, en los fragmentos guardados.

Esto último es la prueba de *aplicación* que pedía la revisión, en vez de comprobar solo que la cadena no está vacía.

### V08: citas de resoluciones. Aceptado, con la opción más prudente para la lista de casos

La revisión acierta en que «no se publican casos reales» era una frase demasiado absoluta. Se delimita la regla así:
- **Se mantienen las resoluciones públicas citadas como precedente de un criterio jurídico:** las del Consejo de Transparencia en la rama 5 y la frase útil de la GAIP. Citar doctrina administrativa publicada es necesario para que el argumento jurídico se pueda verificar.
- **Se retira la lista de casos autonómicos clasificados:** los números de cada resolución estimada, en pérdida de objeto, de urbanización, etc. Esa lista es un dato del estudio y cada número lleva a una ficha con la administración y la obra.

**Cómo se comprueba sin la lista.** `filtrar_autonomicos.py` reproduce las 22 candidatas en local. El complemento autonómico, el informe del Consejo y el README de la raíz explican la regla.

**Prueba:** el complemento no contiene la lista ni sus números.

### V09: limitaciones de las pruebas. Aceptado como limitación

Se mantiene declarada:
- las pruebas usan datos ficticios;
- la interfaz no se ha probado a mano en todas las plataformas;
- las huellas no se han comprobado sin los datos.

`PROTOCOLO_OBRAS.md` y el Anexo D.6 dicen ahora expresamente que las pruebas no sustituyen a un piloto supervisado.

## Respuestas a las preguntas del encargo

- **Tabla normativa:** corregida en ampliaciones, fuentes y ámbito. Sigue siendo la lectura de un no jurista.
- **Cómputo:** `limite`, `pendientes` y las métricas se corrigieron en los casos V01–V07, con pruebas.
- **Privacidad:** ver V08.
- **Cifras históricas:** la revisión no encontró expresiones antiguas fuera de contexto. La recomendación de destacar la corrección en el bloque histórico de la v0.4.5 ya está cubierta: ese bloque lleva el aviso «Formulación de la novena investigación corregida en la v0.4.6».

## Lo que no se ha hecho, y por qué

- **No se calculan suspensiones** (V05): se sustituye por la fecha verificada a mano, ver arriba.
- **No hay plazo del órgano de garantía donde el texto guardado no lo fija:** seguimiento manual. Es preferible a una fecha que podría ser errónea.
- **No hay un campo de prueba de la notificación de la ampliación** (V03): bastan la nota y el justificante.
- **No hay revisión jurídica humana.** Sigue siendo el límite principal, y el veredicto de la revisión lo mantiene: el protocolo no es apto para solicitudes reales sin ella.

## Estado tras la respuesta

Pruebas, todas correctas y ninguna saltada:

| Batería | Pruebas |
|---|---|
| fase0 | 32 |
| escáner | 7 |
| protocolo | 48 |
| revisión de la v0.4.5 | 26 |
| revisión de la v0.4.6 | 26 |
| equivalencia | 1 |
| **Total** | **140** |

Documento: **v0.4.7**, de 49 páginas. Repositorio regenerado con la lista blanca.
