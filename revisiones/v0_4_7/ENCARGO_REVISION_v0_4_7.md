# Encargo de revisión adversarial: «Democracia Auditable» v0.4.7 (comprobación de correcciones)

**Para:** ChatGPT
**Fecha:** 2 de noviembre de 2026
**Qué se pide:** comprobar que las correcciones de tu revisión de la v0.4.6 están **bien hechas** y que no han introducido errores nuevos. El paquete vuelve a ser **el repositorio completo tal como se publicaría** (`democracia-auditable/`).

## Qué ha cambiado

La respuesta punto por punto está en `democracia-auditable/revisiones/v0_4_6/respuesta_revision_v0_4_6.md`, y el registro de cambios del documento, en el Anexo A.11 de la v0.4.7. Los cambios afectan solo al protocolo del Anexo D y a su documentación: **las cifras del estudio no cambian**.

1. **Ampliación por régimen** (`protocolo_obras/regimenes.py`, campos `ampliacion` y `fuente_ampliacion`):
   - **País Vasco:** quince días hábiles.
   - **Cataluña:** hasta la mitad del plazo inicial; no se calcula.
   - **Galicia:** su ley no menciona la ampliación; tampoco se calcula.
   - Lo de Cataluña y Galicia no lo señalaba tu revisión: apareció al comprobar todas las filas.
2. **Plazo del órgano de garantía por régimen** (campos `garante` y `fuente_garante`):
   - dos meses en Cataluña, con la mediación suspendiendo el plazo;
   - seguimiento manual donde el texto guardado no lo fija.
3. **Ampliaciones fuera de tiempo:** una ampliación solo cuenta si se notificó antes del vencimiento ordinario y antes de la respuesta.
4. **Festivos por territorio:** cada línea del fichero de festivos puede valer para todas las filas, para una comunidad («AAAA-MM-DD Comunidad») o para un órgano («AAAA-MM-DD organo:ID»).
5. **Calificación solo con fecha verificada:**
   - la fecha calculada es un aviso provisional;
   - `en_plazo` y las cifras de plazos solo usan `fecha_limite_verificada`, que anota una persona tras comprobar la recepción, el calendario, las suspensiones y la ampliación.

   Esta es la solución elegida para V05 y V07, en lugar de calcular las suspensiones.
6. **Fuentes y ámbito:**
   - Castilla y León y Castilla-La Mancha (local) citan ahora la ley estatal.
   - Galicia local pasa a regirse por la ley estatal.
   - Cada fila local con ley propia cita el artículo que incluye a las entidades locales. Esos artículos se añadieron a `fuentes/regimenes/`.
7. **Citas de resoluciones:**
   - se citan las públicas como precedente de un criterio jurídico;
   - la lista de casos autonómicos clasificados ya no se publica (`investigacion_consejo/COMPLEMENTO_AUTONOMICO.md`, README de la raíz).
8. **Pruebas:** hay 26 nuevas en `protocolo_obras/test_revision_v046.py`. Se reescribieron dos pruebas antiguas por el cambio de regla de «en plazo»; está anotado en su código.

## Qué comprobar

1. **Pruebas:** ejecuta las seis órdenes del `README.md` de la raíz. Deben pasar todas (140) y ninguna debe saltarse.
2. **Tabla de regímenes:**
   - ¿Coincide cada `ampliacion` y cada `garante` con el fragmento del BOE que cita?
   - ¿Queda alguna fila con un ámbito personal mal atribuido?
   - ¿Es razonable no automatizar la prórroga catalana ni la gallega?
3. **Cómputo:**
   - ¿Es correcta la regla de encadenar plazo y ampliación cuando sus unidades difieren (un mes y después quince días hábiles, contados desde el final del plazo ordinario ya ajustado a día hábil)?
   - ¿Y la de sumarlos desde la base cuando la unidad es la misma?
4. **Fecha verificada:**
   - ¿Resuelve de verdad V04, V05 y V07, o solo traslada el problema a la persona que verifica?
   - ¿Queda algún sitio (interfaz, ciclo, exportación, resumen, guía) que siga calificando con la fecha provisional?
5. **Cada punto de la respuesta:** ¿está resuelto en el código o en el texto, o solo en la respuesta?
6. **V08:** ¿es coherente la regla delimitada (precedentes sí, listas de casos no) en todo el repositorio y en el documento?
7. **Coherencia:** ¿coinciden versiones, números de pruebas y formulaciones en el documento, los READMEs, `PROTOCOLO_OBRAS.md`, `GUIA.md` y la interfaz?
8. **Cualquier error nuevo** introducido por las correcciones.

No se adjuntan los datos de la PLACSP. Si necesitas una cifra del corpus, pídela y se calculará.

## Sobre el documento breve que propusiste

Dijiste que convendría un documento breve, aparte del de 49 páginas. Para redactarlo después de esta ronda, concreta:
- **a quién va dirigido:** organizaciones que adopten el protocolo, periodistas, juristas que lo revisen, o un público general;
- **qué extensión tendría;**
- **qué apartados llevaría;**
- **qué debe quedar fuera** para que no se lea como algo más de lo que es: un borrador, sin revisión jurídica, con el protocolo en fase de diseño.

## Formato de respuesta

Para cada problema:
- **a)** dónde está;
- **b)** qué falla;
- **c)** gravedad: bloqueante, importante o menor;
- **d)** corrección propuesta.

Al final:
- un veredicto: si la v0.4.7 y el repositorio pueden distribuirse como borrador crítico, y con qué cambios;
- tu propuesta concreta para el documento breve.
