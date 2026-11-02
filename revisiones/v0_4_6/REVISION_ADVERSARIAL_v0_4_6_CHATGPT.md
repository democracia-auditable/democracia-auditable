# Revisión adversarial de «Democracia Auditable» v0.4.6

**Fecha:** 2 de noviembre de 2026  
**Objeto:** `para_chatgpt_v046.zip`, el repositorio completo remitido para revisión, no un repositorio remoto ni los datos originales de PLACSP.  
**Dictamen abreviado:** las correcciones de la v0.4.5 están **mayoritariamente incorporadas** y el paquete ya pasa sus cinco baterías de pruebas. **Puede presentarse como borrador crítico de investigación después de las correcciones editoriales señaladas; no debe presentarse como motor de plazos jurídicos listo para uso.** La revisión normativa ha encontrado defectos materiales nuevos que las pruebas no cubren.

## 1. Alcance y pruebas independientes

Extraído el ZIP desde una copia limpia y ejecutadas **exactamente las cinco órdenes del README**, desde la raíz y con Python aislado donde lo establece el proyecto:

| Orden | Resultado |
|---|---|
| `python -X utf8 -m unittest discover -s fase0_placsp -p "test_*.py"` | **32/32, OK** |
| `python -X utf8 investigacion_doc_ccn/test_escanear.py` | **7/7, OK** |
| `python -I -X utf8 protocolo_obras/test_protocolo.py` | **48/48, OK** |
| `python -I -X utf8 protocolo_obras/test_revision_v045.py` | **26/26, OK** (33,9 s) |
| `python -I -X utf8 investigacion_terminacion/test_equivalencia.py` | **1/1, OK** |

**Total: 114 pruebas superadas, ninguna saltada.** Hay archivos `descargar_datos.py` y `escanear.py` que faltaban en el anterior ZIP. El checksum SHA-256 de `medir_ejecucion.py` coincide con el registrado en `resultados_v2_4/manifiesto.json` (`e451cae1…e08103f15294`). Los archivos de resultados agregados, el informe HTML y las huellas de tres archivos por expediente están presentes. He examinado el texto y la portada/última página del PDF de 48 páginas; no he hecho una inspección visual de sus 48 páginas.

**Límites de esta revisión:** no se han descargado los gigabytes de archivos originales ni se han reproducido los recuentos de 1.593, 1.549, 78 y 66 órganos desde el corpus; tampoco se ha probado la GUI manualmente en Windows/macOS, ni se ha hecho una auditoría jurídica humana. Las huellas *facilitan* una réplica externa, pero no la sustituyen.

## 2. Hallazgos pendientes o nuevos

### V01 — Ampliación incorrecta de quince días en Euskadi

- **a) Dónde:** `protocolo_obras/regimenes.py`, filas `País Vasco|autonómico` y `País Vasco|local`, comentario «se amplía por un período igual al inicial»; `protocolo_obras/registro.py:121–130`.
- **b) Qué falla:** el artículo 37.2 de la Ley 3/2026 prevé **ampliar un mes por otros quince días**, no por un mes adicional. `limite()` duplica indiscriminadamente la unidad y el número del plazo inicial. **Prueba concreta:** con recepción 12/01/2026 y ampliación anotada, el programa da **12/03/2026**, en lugar de computar el mes inicial hasta 12/02 y sumar los quince días que correspondan (sin festivos adicionales, quince días hábiles llevan a **05/03/2026**). La discrepancia afecta al momento del silencio y al aviso de reclamación.
- **c) Gravedad:** **bloqueante para activar calendarios de solicitudes reales; importante para un borrador de transferencia**.
- **d) Corrección:** introducir `ampliacion` como magnitud y unidad independiente por régimen; Euskadi `15 días`, demás conforme a su artículo. Probar 15 días hábiles, festivos y casos con el último día inhábil. Mientras tanto, desactivar el cómputo ampliado de Euskadi.

**Fuente:** BOE, Ley 3/2026, art. 37.2: https://www.boe.es/buscar/act.php?id=BOE-A-2026-11851

### V02 — Las reclamaciones ante la GAIP no tienen siempre tres meses de tramitación

- **a) Dónde:** `protocolo_obras/registro.py:226–231`, `pendientes`: `mas_meses(rec, 3)` para cualquier reclamación.
- **b) Qué falla:** el artículo 42.9 de la Ley catalana 19/2014 establece **dos meses** para resolver, con posibilidades de suspensión o ampliación (la mediación modifica el cálculo). La sede catalana explica dos meses ordinarios y hasta tres en el caso descrito de mediación. El programa anuncia sin distinguir «plazo de tres meses», incluso sin mediación. **Prueba:** reclamación el 20/02/2026, Cataluña autonómica, salida «tres meses 20/05/2026» aunque el plazo ordinario inicial es 20/04/2026, sujeto a los ajustes jurídicos aplicables.
- **c) Gravedad:** **importante** (y bloqueante para interpretar el aviso como vencimiento legal).
- **d) Corrección:** tabla separada de plazo de resolución del **órgano de garantía**, no reutilizar el régimen de acceso; registrar mediación, suspensión y ampliación. Si no se conocen, mostrar «seguimiento manual, plazo por verificar» en vez de una fecha jurídica automática.

**Fuentes:** BOE, Ley 19/2014, art. 42.9: https://www.boe.es/buscar/act.php?id=BOE-A-2015-470 ; trámite oficial: https://tramits.gencat.cat/es/tramits/tramits-temes/Reclamacio-davant-la-Comissio-de-Garantia-del-Dret-dAcces-a-la-Informacio-Publica-GAIP

### V03 — Una ampliación retroactiva o posterior a la respuesta se admite como válida

- **a) Dónde:** `protocolo_obras/registro.py:150–202`, función `validar`, y `registro.py:121–130`.
- **b) Qué falla:** `validar()` solo comprueba que `fecha_ampliacion` no sea anterior a `fecha_envio`; no exige que la notificación de ampliación sea **anterior al vencimiento ordinario** ni a `fecha_respuesta`. Una fecha arbitraria posterior activa el doble de plazo. **Reproducido:** recepción estatal el 12/01/2026, respuesta el 01/03/2026 y ampliación anotada el **01/04/2026**: `validar()` devuelve `[]` y `en_plazo()` devuelve **«sí»**. Sin esa ampliación, el límite ordinario sería 12/02 y la respuesta quedaría fuera.
- **c) Gravedad:** **importante** (métricas y avisos potencialmente erróneos).
- **d) Corrección:** validar `fecha_ampliacion <= limite_sin_ampliacion` y `fecha_ampliacion <= fecha_respuesta` cuando proceda; exigir constancia de notificación y distinguir fecha de resolución de fecha de notificación. Si faltan esos datos, no considerar confirmada la ampliación.

### V04 — El calendario de festivos se aplica globalmente, no por lugar o expediente

- **a) Dónde:** `protocolo_obras/registro.py:91–113` (`FESTIVOS_ADICIONALES` global) y `protocolo_obras/ciclo_mensual.py:196–221` (`--festivos` único para todo el ciclo).
- **b) Qué falla:** en un lote que incluye órganos de diferentes comunidades o municipios, un único conjunto de festivos hace **inhábil para todos** un día que puede ser festivo solo en un municipio o comunidad. Si se omite el fichero, tampoco se incorporan varios festivos autonómicos/locales. El resumen lo advierte, pero las columnas `en_plazo` siguen calculándose y agregándose.
- **c) Gravedad:** **importante** para una herramienta multiadministración.
- **d) Corrección:** aplicar calendario por expediente u órgano (municipio, comunidad y calendario nacional), con trazabilidad de los festivos considerados; **sin calendario completo, no calificar la respuesta de «en plazo»**. Probar dos expedientes idénticos de territorios diferentes el mismo día festivo solo en uno.

### V05 — No se reflejan suspensiones del procedimiento ni incidencias que cambian el vencimiento

- **a) Dónde:** `protocolo_obras/registro.py` (`CAMPOS`, `limite`, `pendientes`), guía del protocolo.
- **b) Qué falla:** se contempla la ampliación, pero no el intervalo de suspensión por audiencia a terceros, subsanación u otras causas. La Ley 19/2013 y leyes como Galicia 1/2016 (art. 27.2) y Euskadi 3/2026 prevén suspensiones. Por tanto el «silencio desde...» y el cálculo de `en_plazo` podrían ser anticipados aunque el régimen esté marcado `verificado`.
- **c) Gravedad:** **importante** en funcionamiento real; **riesgo ya parcialmente mitigado** porque la documentación marca las fechas como provisionales.
- **d) Corrección:** registrar eventos de suspensión con fecha de inicio/fin y evidencia, o renunciar al cálculo jurídico automático cuando su existencia no se haya descartado; recalcular los indicadores solo tras verificación humana.

**Fuente:** BOE, Galicia, art. 27.2: https://www.boe.es/buscar/act.php?id=BOE-A-2016-3190

### V06 — Referencias normativas erróneas para dos regímenes marcados como «verificados»

- **a) Dónde:** `protocolo_obras/regimenes.py:64–66` (**Castilla y León**), `:60–63` (**Castilla-La Mancha local**); `fuentes/regimenes/castilla_leon.txt` y `castilla_la_mancha.txt`.
- **b) Qué falla:** se cita el **artículo 9 de la Ley 3/2015 de Castilla y León** como fuente del mes para resolver, pero trata de **reutilización**. El plazo de un mes para el acceso deriva de la legislación básica, no de ese artículo. En **Castilla-La Mancha local**, el artículo 33.1 de la Ley 4/2016 establece el plazo específicamente para los sujetos del **artículo 4.1.a** (Junta y entidades dependientes), mientras que el art. 4.2 remite a las entidades locales a la legislación básica y a las previsiones expresamente aplicables. Los **plazos numéricos de un mes pueden seguir siendo correctos**, pero las justificaciones citadas no prueban ese régimen.
- **c) Gravedad:** **importante para trazabilidad jurídica**; no equivale a demostrar que el plazo numérico de un mes sea falso.
- **d) Corrección:** cambiar las fuentes de esos regímenes a Ley 19/2013, art. 20.1, y añadir la referencia autonómica solo para competencia o reclamación cuando proceda. Revisar de forma cruzada **todas** las filas con el ámbito personal de la norma, no limitar las pruebas a que `fuente` sea una cadena no vacía.

**Fuentes:** Castilla y León https://www.boe.es/buscar/act.php?id=BOE-A-2015-3281 ; Castilla-La Mancha https://www.boe.es/buscar/act.php?id=BOE-A-2017-1373

### V07 — Las métricas de «en plazo» usan fechas de recepción no siempre comprobadas

- **a) Dónde:** `protocolo_obras/registro.py:116–118`, `:247–285`; `protocolo_obras/GUIA.md`.
- **b) Qué falla:** `base_plazo()` utiliza `fecha_envio` cuando falta `fecha_recepcion_organo`. La herramienta lo advierte al generar tareas, pero `en_plazo()` puede devolver `sí`/`no` y `resumen()` sumar los porcentajes como si la fecha de partida fuera cierta. Un régimen «verificado» no demuestra una recepción verificada. Tampoco es obligatorio registrar evidencia de esa fecha.
- **c) Gravedad:** **importante** para métricas y comparaciones; no invalida las cifras agregadas del estudio principal.
- **d) Corrección:** separar fecha provisional de vencimiento legal confirmado; no computar «en plazo» en el denominador hasta verificar recepción, calendario, incidencias y ampliaciones; añadir una etiqueta clara `provisional/confirmado`.

### V08 — Las citas de resoluciones permiten identificar administraciones, aunque no se publiquen las listas de obras del estudio

- **a) Dónde:** `investigacion_consejo/COMPLEMENTO_AUTONOMICO.md`, apartado 1 (números de resoluciones concretas), apartado 2; y el README de raíz, «No se publican casos reales».
- **b) Qué falla:** se publican identificadores exactos de resoluciones (`GAIP 0387/2021`, etc.), que conducen a fichas oficiales con el órgano y contrato/obra. La ficha de la primera puede localizarse directamente en el portal GAIP. Por ello, **«no se publican casos reales» es demasiado absoluto**. No he encontrado listas nominativas de las **78 obras marcadas por la señal** ni listas de expedientes seleccionados en el ZIP: ese riesgo sí está sustancialmente corregido. Citar jurisprudencia administrativa pública no es, por sí mismo, una vulneración de privacidad: el problema es la inconsistencia con la política de no identificación expresada de manera general.
- **c) Gravedad:** **menor editorial**, o **importante** si la regla del proyecto prohíbe toda identificación indirecta de un organismo.
- **d) Corrección:** delimitar la norma: «no publicamos listas de obras/órganos seleccionados, ni resultados individuales del protocolo; sí citamos resoluciones públicas como fuentes jurídicas», o bien anonimizar las referencias de casos si se desea una prohibición total (a costa de reducir verificabilidad). Mantener revisión de datos personales para cualquier enlace.

**Ejemplo de fuente pública rastreable:** https://www.gaip.cat/es/detall/normativa/2021-0387

### V09 — Los ensayos no prueban la parte dependiente de documentos reales ni la interfaz gráfica en plataformas objetivo

- **a) Dónde:** `investigacion_terminacion/test_equivalencia.py`, `protocolo_obras/test_revision_v045.py`, README.
- **b) Qué falla:** no es un fallo del código demostrado: las pruebas de equivalencia son **sintéticas** y la GUI se prueba indirectamente (funciones), no con interacciones reales en los sistemas declarados. Las huellas del corpus no se han comprobado sin los datos originales.
- **c) Gravedad:** **menor como limitación declarada**; importante si se anunciara «validación de extremo a extremo» de la aplicación o del estudio empírico.
- **d) Corrección:** mantener esta limitación visible, proponer prueba manual en Windows y un pequeño piloto supervisado. No retrasar la distribución del borrador solo por no disponer de este pilotaje.

## 3. Comprobación de los hallazgos de v0.4.5

| Hallazgo anterior | Estado de v0.4.6 |
|---|---|
| B01, paquete incompleto/pruebas omitidas | **Resuelto** en el ZIP; 114 pruebas sin omisiones |
| B02, validación no independiente | **Corregido editorialmente**; asociación preregistrada parcialmente expuesta; validación externa pendiente |
| B03, plazos autonómicos | **Mejorado, no cerrado**; se detectan V01–V07 |
| B04, persistencia de muestra pequeña o vacía | **Resuelto** por código y pruebas |
| B05, fechas inválidas que rompían validación | **Resuelto** para los campos comprobados |
| B06, tope cero y «reserva aleatoria» inexistente | **Resuelto**; el flujo distingue muestra/selección priorizada |
| B07, réplica de la regla congelada | **Mejorado** con rutas relativas y prueba de equivalencia sintética; falta contraste fila a fila real |
| B08, ficheros de salida anunciados ausentes | **Resuelto por rediseño**: agregados+HTML+huellas sin listas nominativas |
| B09, ciclo exitoso con registro inválido | **Resuelto** y probado |
| B10, reanudación tras interrupción | **Resuelto** en los casos sintéticos ensayados |
| B11, publicación accidental de listas con órgano | **Mejorado** con exclusiones, exportación prudente y eliminación de listas; matiz V08 |
| B12, datos auxiliares arbitrarios por empate | **Resuelto** según código |
| I13–I18, alcance de la señal | **Mejor formulado**: grupos operativos, sesgo, 78/44.290 y 66 órganos; no reproducido con el corpus |
| I19–I21, reclamaciones autonómicas | **Mejor formulado**: 58 % de solicitudes potenciales; 2 y 7 casos; sin extrapolación |
| I22–I23, festivos y definición de fin teórico | **Mejorado**; calendario aún global (V04) |
| I24–I26, histórica 98,7 %, reproducibilidad y facilidad de uso | **Corregido o advertido** en fuentes relevantes; revisiones históricas conservan expresiones antiguas contextualizadas |
| I27, muestra cambia con prioridad | **Resuelto** por orden estable antes de sortear y prueba |
| I28, calidad jurídica y doble cómputo | **Parcial**: separa origen y régimen verificado; la confirmación de fechas/calendario sigue pendiente (V04, V05, V07) |

## 4. Consistencia, ley y privacidad: respuesta a preguntas del encargo

1. **Cinco órdenes:** pasan todas sin omisiones, como indicado arriba.
2. **Tabla normativa:** los 20 días sin especificar más se cuentan como hábiles por la regla general del **art. 30.2 de la Ley 39/2015** (salvo norma con cómputo distinto). Madrid autonómica, Murcia autonómica y Extremadura son coherentes en ese punto. Se han encontrado errores de **ampliación** y **fuentes**; por tanto, no puede certificarse que cada fila verificada coincida plenamente con la ley. No se identifica una comunidad ausente en las opciones explícitas, pero comunidades/municipios pueden requerir reglas adicionales y la administración efectiva puede diferir de la categoría estadística.
3. **Cómputo:** las pruebas de `mas_habiles` para 20/30 días y fin de mes pasan. `limite()` y `pendientes()` fallan en los casos V01–V05 y las métricas en V07.
4. **Respuesta a v0.4.5:** la mayoría de cambios están implementados, no solamente declarados; algunos han introducido/permitido nuevas inconsistencias normativas.
5. **Privacidad:** no hay listas por expediente ni archivos operativos identificables en el ZIP; se conservan identificadores públicos de resoluciones, que permiten conocer órganos por remisión a la fuente (V08).
6. **Cifras/formulaciones:** el README y las conclusiones principales declaran 97,2 %, 10/273 vs 2/558, 66 órganos, 58 % de solicitudes *potenciales*. Los términos antiguos «muy específica», «4 % de las resoluciones» y «58 % de las reclamaciones» aparecen principalmente en el **historial de versiones** y material de revisión como descripción de lo que se afirmó antes, y se explican como corregidos. Se recomienda destacar visualmente la corrección en el bloque histórico v0.4.5 para lectores que escaneen por palabras.
7. **Errores nuevos:** V01–V04, V06 se han hallado inspeccionando las correcciones; V05, V07 son limitaciones de alcance no resueltas; V08 es una inconsistencia de política editorial.

## 5. Prioridad para preparar una entrega pública

**Corrección mínima inmediata (sin ampliar el alcance del proyecto):**

1. Corregir **Euskadi +15 días** y la fila/función de ampliaciones; añadir prueba concreta.
2. Corregir el mensaje de seguimiento **GAIP 2 meses**, con mediación/suspensiones como supuesto no automatizado; añadir prueba.
3. Rechazar **ampliaciones retroactivas** o posteriores a la respuesta; prueba de regresión.
4. Evitar publicar `en_plazo` como métrica comparable si faltan calendario territorial, recepción verificada o suspensiones; etiquetar la salida como *pendiente de comprobar*.
5. Arreglar las **fuentes Castilla y León / Castilla-La Mancha local**; añadir prueba legal que contraste *aplicación* del artículo, no solo existencia del texto.
6. Precisar que **las resoluciones administrativas públicas se citan como precedentes**, pero no se publican los casos seleccionados ni los órganos marcados por la señal.

## 6. Veredicto

**Investigación y documento:** **SÍ, distribuibles como borrador crítico**, una vez subsanados los detalles editoriales y con la falta de revisión humana claramente expuesta. La cautela estadística es sustancialmente mejor que en v0.4.5, y los resultados principales no se invalidan por los errores del calendario.

**Repositorio íntegro:** **SÍ, distribuible como repositorio de trabajo y evaluación, después de corregir V01–V04 y V06 o desactivar las funciones de plazos jurídicos afectadas**. Las cinco baterías pasando permiten afirmaciones sobre el comportamiento de las pruebas, no sobre corrección legal universal o exactitud del corpus sin datos.

**Protocolo para usarlo con solicitudes y reclamaciones reales:** **NO aún**. Necesita una revisión jurídica humana del régimen, calendario, recepción, suspensión y órgano de garantía de cada expediente. El calendario debe ser una ayuda revisable, no una instrucción de presentar reclamaciones según fechas calculadas automáticamente.

**Recomendación práctica al autor:** no añadir nuevas investigaciones ni alargar innecesariamente el documento; reparar estos defectos delimitados, congelar una versión de transferencia y remitirla a organizaciones para un piloto independiente. La propuesta merece evaluación externa aunque el programa jurídico permanezca claramente marcado como prototipo.
