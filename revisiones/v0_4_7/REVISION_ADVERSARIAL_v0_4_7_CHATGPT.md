# Revisión adversarial de «Democracia Auditable» v0.4.7

**Fecha:** 2 de noviembre de 2026  
**Objeto:** `para_chatgpt_v047.zip`, descomprimido en una carpeta nueva.  
**Encargo:** verificar las correcciones de v0.4.6, comprobar regresiones y pronunciarse sobre la distribución del repositorio como **borrador crítico**, no como herramienta jurídica terminada.

## Dictamen ejecutivo

**Las correcciones de v0.4.6 están incorporadas en lo esencial.** Las seis órdenes del README pasan: **140/140 pruebas, cero errores y cero omisiones**. La v0.4.7 introduce una separación apropiada entre el vencimiento calculado —un aviso provisional— y la `fecha_limite_verificada` anotada por una persona, que ahora gobierna la calificación estadística. Se han corregido los plazos de ampliación de Euskadi y de resolución de la GAIP, se prevén festivos por territorio y se ha delimitado la política de publicación de expedientes.

**Pero no recomiendo congelar todavía el código sin reparar cinco incidencias importantes y comprobables** (N01–N05). Se refieren al registro y su validación, no al estudio de contratación. Una de ellas hace fallar el propio validador ante una fecha inválida; otras generan calificaciones o rechazos incorrectos en situaciones posibles. Hay dos mejoras de trazabilidad y coherencia de menor prioridad (N05–N07).

**Veredicto:** el documento y el repositorio **sí son distribuibles como borrador crítico después de reparar N01–N05**, con la advertencia destacada de que no existe validación jurídica humana ni ensayo real. No es necesario seguir ampliando la investigación ni rehacer el documento de 49 páginas. El protocolo **no debe utilizarse para calcular plazos de reclamaciones reales sin una verificación jurídica independiente expediente por expediente**.

## 1. Pruebas realizadas

Ejecutadas las seis órdenes literalmente indicadas en la raíz del README:

| Orden | Pruebas | Resultado |
|---|---:|---|
| `python -X utf8 -m unittest discover -s fase0_placsp -p "test_*.py"` | 32 | OK |
| `python -X utf8 investigacion_doc_ccn/test_escanear.py` | 7 | OK |
| `python -I -X utf8 protocolo_obras/test_protocolo.py` | 48 | OK |
| `python -I -X utf8 protocolo_obras/test_revision_v045.py` | 26 | OK |
| `python -I -X utf8 protocolo_obras/test_revision_v046.py` | 26 | OK |
| `python -I -X utf8 investigacion_terminacion/test_equivalencia.py` | 1 | OK |
| **TOTAL** | **140** | **Sin errores ni omisiones** |

En el entorno de ejecución se utilizó Python 3.13. Se inspeccionó la estructura del ZIP, el texto Markdown del documento y se extrajo texto del PDF, de **49 páginas**. Se visualizaron la portada y la página final; **no se ha inspeccionado visualmente cada página**. El PDF se titula v0.4.7 y contiene las secciones revisadas. Las cifras del estudio principal no se han recalculado porque no vienen los datos brutos de la PLACSP. No se ha ejecutado la GUI manualmente en Windows/macOS ni se han presentado solicitudes reales.

## 2. Hallazgos nuevos o pendientes

### N01 — Error de fecha que bloquea `validar` en Cataluña y Galicia

- **a) Dónde:** `protocolo_obras/registro.py`, `validar` (aprox. líneas 255–275), `problema_ampliacion` (169–176), `limite` (197–209) y `limite_para_avisos` (213–216).
- **b) Qué falla:** si `fecha_ampliacion` contiene una cadena que no es fecha y `regimen` es `Galicia|autonómico` o `Cataluña|local`/`Cataluña|autonómico`, `validar()` identifica internamente la fecha mala, **pero se interrumpe con `TypeError` antes de devolver el informe de errores**. `problema_ampliacion()` da cadena vacía cuando `fs()` devuelve `None`; acto seguido `limite()` intenta desestructurar `reg["ampliacion"]`, que es `None`. **Reproducción:** registro con `fecha_envio=2026-01-12`, `regimen=Galicia|autonómico`, `fecha_ampliacion=2026-02-XX` → `TypeError: cannot unpack non-iterable NoneType object` dentro de `validar`. Esta regresión contradice la mejora de validación robusta de la v0.4.6.
- **c) Gravedad:** **importante** para el repositorio distribuido; debe corregirse antes de la versión de entrega.
- **d) Corrección:** si `fecha_ampliacion` es no vacía pero `fs(...)` da `None`, no intentar calcular el vencimiento; devolver `None` y dejar que `validar` informe el error de formato. Antes de desestructurar, exigir `reg["ampliacion"] is not None`. Añadir dos pruebas específicas de `validar`: Cataluña y Galicia con fecha inválida, sin excepción.

### N02 — Ampliación anterior a la recepción: se acepta

- **a) Dónde:** `protocolo_obras/registro.py`, `validar` (alrededor de 265–272) y `ampliacion_fuera_de_tiempo` (179–192).
- **b) Qué falla:** se comprueba que la notificación de ampliación sea posterior al **envío**, pero no posterior a la **recepción por el órgano competente**, aunque esa fecha sí esté registrada. **Reproducción:** envío 12/01/2026, recepción 20/02/2026, `fecha_ampliacion=20/01/2026`. `validar([fila])` devuelve `[]`; `limite()` calcula 20/04/2026 como si la ampliación hubiera sido válida. Es una incoherencia cronológica verificable del registro.
- **c) Gravedad:** **importante** para el cómputo provisional y el control de calidad.
- **d) Corrección:** rechazar, o al menos marcar para revisión obligatoria, `fecha_ampliacion < fecha_recepcion_organo` cuando consten ambas, con prueba de regresión. Comprobar asimismo que se registra la fecha **de notificación**, no solo la de resolución.

### N03 — Una suspensión puede convertir en falso error una ampliación válida

- **a) Dónde:** `protocolo_obras/registro.py`, `ampliacion_fuera_de_tiempo` (179–192), `limite_ordinario` (160–166) y `validar` (271–272).
- **b) Qué falla:** la regla rechaza siempre una ampliación notificada después del vencimiento **provisional**. Pero ese vencimiento no incorpora las suspensiones expresamente reconocidas por las leyes (por ejemplo, audiencia de terceros). Si el plazo ordinario real se suspende y continúa después, una notificación posterior al vencimiento provisional **puede no ser tardía**. **Reproducción:** recepción 12/01/2026, vencimiento provisional 12/02/2026, suspensión documentada durante febrero, notificación 20/02/2026 y vencimiento final verificado posteriormente. `validar` emite «ampliación ... después del vencimiento ordinario» y `limite` devuelve `None`, aunque la fecha ordinaria efectiva necesita comprobación. La presencia de una `fecha_limite_verificada` no elimina este rechazo.
- **c) Gravedad:** **importante** si el registro va a manejar expedientes con suspensiones; no significa que toda ampliación tras el 12/02 sea jurídicamente válida.
- **d) Corrección:** no convertir la comparación con un plazo **provisional** en un error legal definitivo. Introducir opcionalmente `fecha_limite_ordinaria_verificada`, o emitir una alerta «ampliación aparentemente tardía; comprobar suspensiones» y bloquear solo tras contrastar la fecha ordinaria efectiva. Diferenciar claramente error cronológico incontrovertible de advertencia jurídica condicionada.

### N04 — Se exporta «fuera de plazo» antes de vencer una solicitud marcada como silencio

- **a) Dónde:** `protocolo_obras/registro.py`, `en_plazo` (348–356), `validar` (273–280) y `exportar` (447–452).
- **b) Qué falla:** `en_plazo` devuelve `"no"` ante cualquier `resultado="silencio"` con `fecha_limite_verificada`, sin consultar la fecha actual; `validar` no rechaza un silencio anotado **antes** del vencimiento si no hay fecha de respuesta. **Reproducción:** envío 12/10/2026, `fecha_limite_verificada=14/12/2026`, `resultado=silencio`, consulta/exportación el 02/11/2026. El registro se considera válido y `en_plazo()` devuelve `"no"`, aunque el vencimiento todavía es futuro. `pendientes`, por separado, muestra correctamente «esperar respuesta hasta ...». `resumen` evita en general contabilizar esa fila antes de vencer, pero la **exportación no**.
- **c) Gravedad:** **importante** porque afecta a la calificación pública de cumplimiento; arreglo localizado.
- **d) Corrección:** validar coherencia entre silencio y fecha actual de corte, o definir `en_plazo(r, fecha_corte)` y evitar `"no"` hasta el vencimiento verificado. Una alternativa aún más simple es no exportar un juicio automático de incumplimiento por «silencio» sin un corte temporal verificable. Añadir prueba que cruce `validar`, `pendientes`, `resumen` y `exportar`.

### N05 — Fecha límite «verificada» anterior a la recepción del órgano

- **a) Dónde:** `protocolo_obras/registro.py`, `validar` (aprox. 266–270) y `en_plazo` (348–356).
- **b) Qué falla:** la comprobación solo exige que la `fecha_limite_verificada` sea posterior al envío. **Reproducción:** envío 12/01/2026; recepción 20/02/2026; límite supuestamente verificado 30/01/2026; respuesta 22/02/2026. `validar` devuelve `[]`, y `en_plazo` produce `"no"`. No se debe aceptar como verificada una fecha límite anterior al inicio conocido del cómputo.
- **c) Gravedad:** **importante** para la integridad de las métricas, aunque está acotado a un dato inconsistente.
- **d) Corrección:** exigir `fecha_limite_verificada > fecha_recepcion_organo` cuando ambas existan; probar el caso. Mantener la verificación humana de suspensiones y festivos.

### N06 — Festivos territoriales con ámbito mal escrito pasan inadvertidos

- **a) Dónde:** `protocolo_obras/registro.py`, `cargar_festivos` (105–118) y `festivos_de` (121–125); formato descrito en `GUIA.md`.
- **b) Qué falla:** el fichero admite cualquier cadena después de la fecha como ámbito. Por ejemplo, `2026-03-02 Pais Vasco` —sin tilde— queda registrado, pero no coincide con `regimen="País Vasco|local"`; el festivo no se aplica y no hay advertencia. No equivale a un cálculo jurídicamente confirmado, puesto que el sistema lo llama provisional, pero degrada su fiabilidad.
- **c) Gravedad:** **menor** para un borrador; importante para operar calendarios reales.
- **d) Corrección:** validar que cada comunidad nombrada esté en la tabla o imprimir una advertencia sobre ámbitos de festivo sin coincidencia con las filas del registro. La revisión manual sigue siendo obligatoria.

### N07 — Referencias internas erróneas y política de precedentes demasiado categórica

- **a) Dónde:** `documento/Democracia_Auditable_v0_4_7.md`, apartados iniciales de v0.4.7 y v0.4.6 (aprox. líneas 17 y 26); `investigacion_consejo/COMPLEMENTO_AUTONOMICO.md`, introducción y apartado 2.
- **b) Qué falla:** el documento dice `documento_v0_4_6/respuesta_revision_v0_4_6.md` y `documento_v0_4_5/...`, directorios que **no existen** en el ZIP. Los archivos reales están en `revisiones/v0_4_6/` y `revisiones/v0_4_5/`. Además, el complemento declara que las resoluciones públicas se citan *solo* como precedentes de un criterio, pero su apartado 2 incluye referencias de casos con mero resultado o título (por ejemplo, Canarias R159/2026 y Madrid RDA136/2023). **No reaparece la lista de los casos sistemáticamente clasificados**: V08 está sustancialmente resuelto; el problema es una pequeña tensión entre la regla declarada y estas menciones aisladas.
- **c) Gravedad:** **menor editorial**.
- **d) Corrección:** arreglar las dos rutas y actualizar el PDF correspondiente; formular que «no se publican las listas sistemáticas ni casos seleccionados para el protocolo; se citan algunos precedentes públicos, con justificación de su relevancia» o retirar las menciones que no ilustran ningún criterio.

## 3. Comprobación de las correcciones pedidas en v0.4.6

| Hallazgo previo | Estado en v0.4.7 | Observación |
|---|---|---|
| **V01** Euskadi: ampliación +15 días | **Corregido** | `ampliacion=(15, "dias_habiles")` para autonómico y local; caso 12/01 → 05/03 y festivo territorial cubiertos por pruebas. Concuerda con art. 37.2 de Ley 3/2026. |
| **V01 bis** Cataluña y Galicia: ampliación | **Mitigado prudentemente** | `ampliacion=None` impide automatizar; es coherente con la incertidumbre. No significa que una ampliación gallega sea necesariamente imposible: su art. 27.1 remite la tramitación a la normativa básica. |
| **V02** GAIP dos meses | **Corregido** | `(2, "meses")`; la salida advierte que mediación, informes y ampliaciones pueden alterar el vencimiento. |
| **V03** ampliaciones retroactivas | **Corregido en los ejemplos probados, no en todos los supuestos** | Rechaza ampliaciones realmente extemporáneas, pero hay falsos rechazos con suspensión (N03) y admite ampliación antes de recepción (N02). |
| **V04** festivos por territorio | **Implementado** | Claves por comunidad y `organo:ID`, más los generales. Carece de verificación de grafía (N06); sigue sin calcular calendario oficial completo automáticamente. |
| **V05** suspensiones | **Mitigado, no automatizado** | `fecha_limite_verificada` evita basar la calificación en vencimientos provisionales; el seguimiento de la suspensión se traslada, expresamente, a una persona. N03 muestra la interacción pendiente con la validación. |
| **V06** fuentes y ámbito | **Corregido en las filas objeto de revisión** | Castilla y León y Castilla-La Mancha local citan normativa básica; Galicia local pasa a legislación básica; se citan artículos de ámbito. La remisión gallega a la legislación básica de reclamaciones (art. 28.3) podría documentarse mejor para el seguimiento del garante, aunque conservar un aviso manual es prudente. |
| **V07** fecha y métricas | **Mejora sustancial, con dos huecos** | `en_plazo` y el resumen requieren fecha verificada; hay incoherencias de integridad/tiempo en N04 y N05. |
| **V08** identificación por casos | **Resuelto en su núcleo** | Se retira la lista nominativa de las resoluciones sistemáticamente clasificadas; quedan resoluciones públicas utilizadas como precedentes o ejemplos. Matiz editorial N07. |
| **V09** validación externa | **Declaración correcta de limitaciones** | No hay prueba integral con PLACSP real ni GUI manual en los sistemas objetivo; no sustituye un piloto ni auditoría jurídica. |

### Sobre la tabla normativa y el cómputo

- La tabla contiene **39 entradas** (`TABLA`), de las cuales **una** está marcada expresamente `verificado=False` (Comunidad de Madrid local). Es una marca de cautela en el programa, **no** una certificación legal de las otras 38.
- Distribución de ampliaciones: 28 de un mes, cuatro de 20 días hábiles, dos de 30, dos de 15 y tres no automatizadas. Para el órgano de garantía: 15 filas con tres meses, dos con dos meses y 22 con seguimiento manual. La opción de no dar fecha cuando no está acreditada es defensible.
- **Cómputo con unidades distintas:** un mes desde recepción y después 15 días hábiles desde el fin ordinario *ajustado a hábil*, es una convención razonable para el aviso provisional, y el caso de Euskadi concuerda con el ejemplo. **Unidades iguales:** sumar desde la base evita errores de redondeo al encadenar meses cortos. Ninguna de las dos reglas sustituye el examen de suspensiones o de la regla específica de cada régimen.
- Las disposiciones del BOE consultadas directamente confirman los puntos principales: Euskadi, Ley 3/2026 arts. 37 y 40; Cataluña, Ley 19/2014 arts. 33 y 42; Galicia, Ley 1/2016 arts. 27 y 28. Se han cotejado los fragmentos incluidos para las filas cambiadas, **sin pretender una certificación jurídica exhaustiva e independiente de las 39 situaciones**.

**Fuentes legales consultables:**

- Euskadi, Ley 3/2026: https://www.boe.es/buscar/act.php?id=BOE-A-2026-11851
- Cataluña, Ley 19/2014: https://www.boe.es/buscar/act.php?id=BOE-A-2015-470
- Galicia, Ley 1/2016: https://www.boe.es/buscar/act.php?id=BOE-A-2016-3190
- Ley estatal 19/2013: https://www.boe.es/buscar/act.php?id=BOE-A-2013-12887
- Ley 39/2015: https://www.boe.es/buscar/act.php?id=BOE-A-2015-10565

**Nota sobre verificación humana:** separar la fecha provisional de la verificada es una decisión arquitectónica correcta, pero el fichero CSV **no prueba por sí mismo** que alguien verificara realmente la notificación, los festivos y las suspensiones. Para un piloto, convendría documentar fuente del calendario, justificante de recepción, incidencias de suspensión, fecha e identidad organizativa del revisor, conservadas en el registro privado. No hace falta automatizarlo todo para distribuir un borrador, pero no debe presentarse como garantía automática.

## 4. Coherencia de paquete, datos y privacidad

- **Versiones y pruebas:** README v0.4.7; documento Markdown y PDF v0.4.7; README anuncia seis órdenes y 140 pruebas, resultado verificado. No se detectó desajuste de recuento en las secciones principales.
- **Archivos:** están incluidos los scripts necesarios para las pruebas, los agregados del estudio, `huellas_resultados.json` y los fragmentos jurídicos. No se han encontrado CSV de casos identificados en el paquete publicado. La reproducción del corpus con los datos oficiales sigue pendiente de un tercero.
- **Citas:** el complemento elimina la lista de 22 candidatas y las listas de casos estrictos, pero conserva lecturas aisladas de resoluciones públicas. Su existencia no equivale a publicar la lista del estudio; conviene precisar el alcance de la regla de no identificación (N07).
- **Avisos y salidas:** `GUIA.md`, `PROTOCOLO_OBRAS.md`, `ciclo_mensual.py` y la interfaz explican la nueva distinción provisional/verificada. `resumen` usa fechas verificadas; `exportar` usa `en_plazo`, cuyo defecto se detalla en N04. Las salidas no incluyen las notas privadas, ni identificadores de obras por defecto.

## 5. Recomendación de cierre y distribución

**Corrección mínima previa a publicar el ZIP de transferencia:**

1. **N01:** impedir el `TypeError` del validador con fechas de ampliación inválidas.
2. **N02 + N03:** distinguir incoherencias de cronología indiscutibles de supuestas ampliaciones extemporáneas cuando puede existir suspensión; evitar falso cómputo.
3. **N04 + N05:** no emitir calificaciones de incumplimiento antes del vencimiento y rechazar límites verificados previos a una recepción conocida.
4. **N07:** arreglar las dos rutas y ajustar la formulación de precedentes; regenerar el PDF.

**N06** (validar ámbitos de festivos) puede corregirse en la misma pasada si es sencillo, o documentarse como limitación menor. **No pediría nuevas investigaciones, nuevos corpus, otro estudio estadístico ni un rediseño de gobernanza antes de la distribución.** Cada corrección debe tener prueba de regresión específica además de las 140 existentes.

**Uso admisible:** publicar el proyecto como *borrador crítico, revisado por IA, sin validación jurídica humana, a disposición de organizaciones para evaluación/piloto*. **No admisible:** promocionarlo como herramienta operativa que calcula con fiabilidad legal universal el vencimiento de solicitudes y reclamaciones.

## 6. Propuesta concreta de documento breve para organizaciones

**Destinatario principal:** personas responsables de programas de transparencia, control ciudadano y periodismo de datos en **organizaciones cívicas que puedan valorar la adopción de un piloto**. El objetivo no es persuadir a público general ni obtener una revisión jurídica exhaustiva en el primer correo; juristas y periodistas pueden ser revisores secundarios.

**Extensión:** **dos páginas A4**, unas **650–850 palabras**, con un máximo de una tabla pequeña o diagrama sencillo. Título sugerido: **«Democracia Auditable: propuesta abierta para comprobar qué sabemos del fin de las obras públicas»**. El texto debe poder entenderse sin abrir el repositorio.

**Apartados y espacio orientativo:**

1. **Qué problema aborda (120 palabras):** dificultad para encontrar información de finalización de obras en la fuente concreta estudiada; diferencia entre *no detectado en PLACSP* e *incumplimiento o falta de terminación*.
2. **Qué se ha comprobado (150):** muestra de 1.593 expedientes y resultado de 1.549 sin indicador detectable; condiciones metodológicas y limitaciones. Una referencia al estudio completo y al código reproducible.
3. **Qué se ofrece (150):** protocolo para elegir casos, formular una solicitud, registrar respuesta/silencio, custodiar evidencias y publicar agregados; herramientas, licencias y estado de prototipo.
4. **Qué no está demostrado (100):** ninguna evaluación con solicitudes reales; las fechas jurídicas y las métricas deben revisarse; las pruebas sintéticas y las revisiones por IA no constituyen validación experta.
5. **Qué se pide a la entidad (130):** evaluación libre y crítica, posible selección de un piloto pequeño bajo su propia responsabilidad, revisión jurídica y medición de utilidad/costes. No se pide adhesión, financiación ni compromiso inicial.
6. **Dónde comprobarlo (50):** enlaces directos al repositorio, a `README`, metodología, PDF íntegro, código y límites; fecha y versión del material.

**Debe quedar fuera:** 49 páginas de fundamentación, historial de rondas, detalles de nueve investigaciones, todas las tablas legales, resultados individuales, nombres de administraciones o contratistas, sugerencias de corrupción, porcentajes interpretados como incumplimientos y promesas de que la solución ya funciona o de que habrá mantenimiento. Tampoco declarar «validado científicamente» ni «verificado legalmente». **Conservar a la vista** «borrador crítico», «pendiente de revisión jurídica y humana», «sin piloto real», «revisión con IA».

**Entrega recomendada:** correo corto (alrededor de 120–160 palabras), **documento breve como entrada** y enlace al repositorio completo como respaldo. El apartado 3 bis puede proporcionar la idea central y la motivación, pero debe reescribirse como documento autónomo, no extraerse literalmente.

## 7. Resumen final

La v0.4.7 es una mejora real y supera todas sus pruebas. **No hay razón para reiniciar el estudio ni prolongar la fase de investigación.** Quedan unas pocas correcciones verificables en `registro.py` y dos detalles de documentación. Una vez subsanados, el repositorio puede distribuirse de forma responsable como **propuesta abierta para que una organización decida si merece un piloto**. Ni el éxito de sus pruebas ni este informe deben interpretarse como certificación legal o empírica del funcionamiento en casos reales.
