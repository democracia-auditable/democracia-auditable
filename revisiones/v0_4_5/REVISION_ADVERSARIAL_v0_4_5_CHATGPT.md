# Revisión adversarial de «Democracia Auditable» v0.4.5

**Fecha:** 2 de noviembre de 2026  
**Objeto:** el ZIP `para_chatgpt_v045.zip`, no un repositorio remoto ni un corpus de datos no adjunto.  
**Dictamen:** **NO APTO todavía para distribución como herramienta operativa; SÍ como borrador de trabajo, después de rectificar las afirmaciones centrales y de indicar expresamente que la parte ejecutable no está validada ni lista para presentar solicitudes.**

## 1. Alcance y evidencia reproducible

Revisé el encargo y el documento v0.4.5, la respuesta y la revisión de v0.4.4, la novena investigación y sus scripts, el complemento autonómico, la guía y el código del estudio y del protocolo, los manifiestos y resultados agregados disponibles y las capturas. Contrasté por separado los números estadísticos y la normativa madrileña. No pude repetir el cálculo con los 15 ZIP de PLACSP, revisar los 24 expedientes de notas de modificación, examinar las listas reales de obras marcadas ni comprobar sistemáticamente los ~20.400 pronunciamientos autonómicos: esos insumos no forman parte del paquete.

Comprobaciones ejecutadas en la carpeta raíz descomprimida:

```sh
python -m unittest discover -s fase0_placsp -p 'test_*.py' -q
# Ran 32 tests — OK

python -m unittest discover -s protocolo_obras -p 'test_*.py' -q
# Ran 47 tests — FAILED (errors=3, skipped=11)
# ModuleNotFoundError: No module named 'descargar_datos'
```

La causa de los 11 saltos es que no se puede importar la dependencia usada por la selección. **No equivalen a 11 pruebas satisfactorias.** También se comprobó que los scripts compilan sintácticamente, lo que no equivale a pruebas de ejecución con datos reales. Para la tabla 2×2 central, verificación independiente con Fisher exacto bilateral: RR = 10,219780; IC95% log-Wald = [2,254736, 46,322005]; p = 0,000434290. Las huellas SHA-256 de `PREREGISTRO.md` y `regla_e4t_v2.py` coinciden con las declaradas. Eso verifica la integridad de **las copias presentes**, no prueba la anterioridad del registro ante un tercero.

## 2. Hallazgos críticos y correcciones

Se especifica en todos los hallazgos **a) dónde, b) fallo, c) gravedad, d) solución**. «Bloqueante» significa bloquear la difusión como software/protocolo utilizable, o una afirmación que sustenta directamente la interpretación de los resultados. No significa bloquear toda discusión académica del borrador.

### B01 — Distribución incompleta y pruebas falsamente tranquilizadoras

- **a) Dónde:** `fase0_placsp/README.md`; `protocolo_obras/ciclo_mensual.py` (importación inicial); `protocolo_obras/test_protocolo.py`; archivos del ZIP.
- **b) Qué falla:** se promete `descargar_datos.py`, pero no está en el paquete. `ciclo_mensual` lo importa incluso al usar `--sin-descarga`; por ello fallan tres pruebas antes de iniciar su lógica. Otras once se saltan al no ser importable el módulo de escaneo que esperan. La opción de la GUI para «pasar las pruebas» no certifica el conjunto cuando están omitidas. Falta también `manifiesto_descarga_estudio.json` anunciado por el README.
- **c) Gravedad:** **bloqueante**.
- **d) Corrección:** generar un ZIP de publicación desde una copia limpia con todos los módulos, datos auxiliares de distribución y rutas coherentes; instalar o colocar las dependencias comunes con una estructura autocontenida. En CI: hacer fallar la comprobación si existe **cualquier** error, omisión no intencional o importación rota; probar también `--sin-descarga`, interfaz y ciclo mensual desde otra carpeta.

### B02 — La validación de la señal no es un holdout plenamente independiente del diseño

- **a) Dónde:** `investigaciones/9_terminacion/PREREGISTRO.md`, `INFORME_TERMINACION.md`, sección §9.0 ter (punto 9) del documento.
- **b) Qué falla:** el propio preregistro reconoce que la regla se diseñó viendo obras de 200.000 € a 1 M€ y de 1 M€ o más; ambos tramos integran la tabla principal de ≥50.000 €. La separación por **etiqueta final conocido/desconocido** protege contra una fuga directa de etiquetas R/N, pero no elimina el sobreajuste a vocabulario, órganos, expedientes, años y estilo de publicación del universo explorado. Solo el tramo de 50.000–200.000 € es ajeno a esos tramos de diseño; allí son 3/103 frente a 0/193 y el IC logarítmico corregido es aprox. 0,7–250: **no cumple por sí solo el criterio de límite inferior >1**. El p de Fisher ≈0,041 para ese tramo no revierte esa incertidumbre, ni convierte una comparación estratificada secundaria en prueba confirmatoria. La frase «solo la tabla principal tiene valor confirmatorio» confunde preregistro con independencia efectiva.
- **c) Gravedad:** **bloqueante para la afirmación de “validación confirmatoria”**; importante para el uso estrictamente exploratorio.
- **d) Corrección:** renombrar «evidencia preregistrada de asociación en corpus parcialmente expuesto al diseño»; mantener los datos numéricos y las condiciones preregistradas alcanzadas **sin** llamar a la regla una «señal validada de resolución» con validez general. Planificar una validación verdaderamente externa con nuevo periodo, nuevos órganos y tramos no utilizados, fijados de antemano; registrar el protocolo en un tercero antes de analizar los casos.

### B03 — El calendario automático puede inducir a reclamaciones fuera de plazo

- **a) Dónde:** `protocolo_obras/registro.py` (`limite`, `pendientes`, `en_plazo`, `resumen`), `GUIA.md` (regla del mes), Anexo D y mensajes de la interfaz.
- **b) Qué falla:** el algoritmo aplica a todo caso **un mes desde la recepción, o dos con ampliación**, antes de calcular reclamaciones. No es universal. El art. 42 de la Ley madrileña 10/2019 prevé 20 días ampliables otros 20, y el portal oficial de la Comunidad lo confirma. La sede del Ayuntamiento aclara el cómputo hábil en su procedimiento. Además, el plazo para **reclamar** no debe confundirse con el plazo para **resolver la solicitud**; el art. 48 madrileño formula un mes desde el acto o el efecto del silencio, mientras que los criterios administrativos sobre silencio exigen verificar cada caso. La aplicación actual produce fechas concretas y porcentajes de «en plazo» a partir de un modelo jurídico que no cubre su población.
- **c) Gravedad:** **bloqueante para uso jurídico real**.
- **d) Corrección:** perfiles jurídicos documentados por administración, procedimiento, fecha y norma; origen del plazo y suspensiones/ampliaciones justificadas; fecha de entrada acreditada; calendarios locales/autonómicos. Para perfiles no verificados: no emitir fechas «reclamar antes de», ni métricas jurídicas de cumplimiento; mostrar «verificación jurídica pendiente». Revisión por un profesional antes de habilitar el botón de pendientes.

### B04 — Falla la persistencia de la muestra en el primer ciclo

- **a) Dónde:** `protocolo_obras/seleccionar_obras.py`, rama `elif a.muestra and a.muestra < len(candidatas)`; `ciclo_mensual.py`, variable `muestra`.
- **b) Qué falla:** el ciclo pide por defecto 200 obras. Si existen 200 o menos elegibles, `seleccionar_obras` no sortea ni escribe `muestra.csv`; sin embargo `ciclo_mensual` guarda **siempre** su ruta para el próximo mes y lo intentará abrir con `--lista`. Se reprodujo con dos filas sintéticas elegibles: sale `lote.csv` pero no `muestra.csv`. El segundo ciclo fallará por archivo inexistente. También dificulta interpretar cero elegibles y contabilizar el marco real.
- **c) Gravedad:** **bloqueante**.
- **d) Corrección:** ante `--muestra=N>0`, seleccionar y congelar **min(N, número elegible)** incluso cuando es cero; producir `muestra.csv` y `seguimiento_muestra.csv` consistentes y guardar su ruta en estado solo después de verificar la escritura. Probar N=0, N=1, N=candidatas, N>candidatas y dos ciclos consecutivos.

### B05 — El registro puede romperse justo cuando debería detectar entradas inválidas

- **a) Dónde:** `protocolo_obras/registro.py:121–172`, especialmente lecturas de `fecha_recepcion_organo`, `fecha_replanteo` y `fecha_recepcion_obra` fuera del bloque `try`.
- **b) Qué falla:** la primera pasada añade un error legible de fecha incorrecta, pero el código vuelve a convertir algunos campos sin protección y provoca `ValueError`. Confirmado con `NO_FECHA` en una fila sintética. El botón «Comprobar registro» puede mostrar una excepción en vez del reporte de validación.
- **c) Gravedad:** **bloqueante**.
- **d) Corrección:** parsear una sola vez todas las fechas de cada fila, guardar `None` si el valor es inválido y acumular todos los mensajes de error sin abortar. Hacer que la GUI muestre la lista y no ejecute `pendientes`, `resumen` ni exportación hasta validar.

### B06 — El tope de cuatro se desactiva con 0 y no hay fracción aleatoria en el flujo

- **a) Dónde:** `interfaz.py` («Opciones avanzadas»), `seleccionar_obras.py:276` y argumentos `--tope 0`, Anexo D y `PROTOCOLO_OBRAS.md`.
- **b) Qué falla:** el máximo de cuatro solicitudes por órgano y mes se presenta como salvaguarda, pero el operador puede poner **cero**, que significa «sin tope» en la lógica (`if a.tope ...`). Basta una entrada de GUI válida sintácticamente para anularlo. Además, el flujo mensual ordena todas las candidatas por señal si se activa la prioridad: **no reserva una submuestra aleatoria del flujo**, aunque el plan de medición declara que la reserva protege contra sesgo. La muestra inicial separada de 200 expedientes **no** sustituye una fracción aleatoria dentro de cada flujo.
- **c) Gravedad:** **bloqueante para despliegue masivo**; **importante** para la inferencia estadística.
- **d) Corrección:** tope de cuatro inmutable en el modo piloto recomendado, con autorización y justificación registrada para excepciones, nunca `0` como atajo casual. Implementar asignación aleatoria en una fracción preregistrada de cada lote, guardar probabilidades de inclusión y registrar el orden; de lo contrario quitar la afirmación de que ese control existe y no inferir proporciones poblacionales de lotes priorizados.

### B07 — El paquete de la novena investigación no permite repetir su propia validación

- **a) Dónde:** `investigaciones/9_terminacion/validar_e4t.py:19–21,100`, `regla_e4t_v2.py`, `senales_medir.py`, `INFORME_TERMINACION.md` (reproducción).
- **b) Qué falla:** importa `medir_ejecucion` por una ruta privada fija de Windows y busca `protocolo_obras` como carpeta hermana inmediata, cuando en el ZIP queda **dos niveles por encima**. También pretende leer `../investigacion_doc_ccn/contratos_ccn.csv`, inexistente en esta estructura, y faltan los datos originales. Una ejecución real falla primero en las importaciones. Usar `python -I` en la receta acentúa la dependencia de rutas correctas. Se contrastaron los fragmentos estáticos de los emparejamientos y no se advirtió una divergencia obvia, pero **no está acreditada equivalencia funcional de extremo a extremo**.
- **c) Gravedad:** **bloqueante para declarar la validación reproducible desde el paquete**.
- **d) Corrección:** convertir utilidades compartidas en módulos importables sin rutas absolutas; usar `pathlib` sobre la raíz del proyecto, documentar insumos opcionales privados y añadir un fixture sintético en el repositorio. Test de regresión que compare `marcada(..., regla original)` con `Indice.terminacion(...)` para un conjunto con todos los bordes: fase, números, títulos, fechas, rareza y empates.

### B08 — Datos y salidas anunciadas no acompañan a los resultados entregados

- **a) Dónde:** `fase0_placsp/README.md`, `fase0_placsp/resultados_v2_4/`, `interfaz.py:_ver_estudio`.
- **b) Qué falla:** el README anuncia `informe.html`, `lista_obras.csv`, `expedientes_seleccionados.csv`, auditorías y revisiones manuales. `resultados_v2_4/` contiene solo `informe.md`, `resumen.json` y `manifiesto.json`. `_ver_estudio()` intenta generar HTML sobre un CSV de expedientes **que no está**; intercepta la excepción y dice vagamente que faltan resultados. Tampoco puede comprobarse la nueva clasificación de las 1.651 filas del informe con este ZIP.
- **c) Gravedad:** **bloqueante para la promesa de «abrir el resultado» y replicabilidad entregada**, no para la lectura del agregado documental.
- **d) Corrección:** separar una distribución ligera explícitamente marcada «solo informe agregado» de otra distribución funcional, o incluir los archivos públicos de resultados y ejecutar una prueba real de abrir HTML/lista. No mostrar botones a archivos omitidos. Conservar internamente, pero no publicar sin revisión editorial, los CSV identificativos.

### B09 — El ciclo puede declarar éxito con registros inválidos

- **a) Dónde:** `ciclo_mensual.py`, `ejecutar(... "validar", codigos_validos=(0, 1))`, escritura de `resumen_ciclo_*.md` y `ciclo_estado.json`.
- **b) Qué falla:** el código 1 representa errores del registro, pero el ciclo lo tolera como éxito y avanza el estado mensual. Después puede usar esos datos erróneos en pendientes y estadísticas, o dar por preparado un trabajo que requiere intervención.
- **c) Gravedad:** **bloqueante**.
- **d) Corrección:** ante errores, **no** seguir ni adelantar `ultimo_ciclo`; conservar borrador transaccional y presentar un reporte legible de errores para su reparación y posterior reanudación.

### B10 — La cancelación no tiene una reanudación segura

- **a) Dónde:** `interfaz.py` (cancelar/subprocesos y mensaje final), `ciclo_mensual.py` y `seleccionar_obras.py` (negativa a sobrescribir lote).
- **b) Qué falla:** cancelar después de crear el lote `flujo` pero antes del `muestra` deja una carpeta de salida; volver a pulsar el ciclo el mismo día falla porque la selección rechaza un lote existente. La interfaz sugiere que se puede empezar de nuevo cuando se quiera, pero no ofrece `--forzar`, limpieza controlada ni reanudar. La solución ad hoc de borrar carpetas amenaza el control de duplicados.
- **c) Gravedad:** **importante** (bloqueante para despliegue desatendido).
- **d) Corrección:** fases idempotentes, escritura en directorio temporal y confirmación/commit al finalizar, persistencia de etapa y botón «Reanudar ciclo» que conserve registro, marco de muestra y lote preparado. Probar interrupción en cada fase.

### B11 — Riesgo de generar y divulgar acusaciones indirectas con nombres

- **a) Dónde:** `seleccionar_obras.py` columna `senal_terminacion`, `interfaz.py` (priorizar la señal), `informe_legible.py`/README (lista de obras, organismo y enlaces), `registro.py:exportar` y ruta de trabajo por defecto del protocolo.
- **b) Qué falla:** el `lote.csv` guarda órgano, obra, enlace y **título de la nueva licitación** que activó la señal. Eso permite identificar a los órganos por una presunta terminación problemática incluso sin una clasificación textual «fracasó». La opción de prioridad aumenta la concentración de esos nombres en los primeros lotes. En el estudio, la lista pública anunciada es nominativa y buscable. El paquete no incluye `.gitignore`, y el protocolo usa por defecto su propia carpeta fuente para guardar registros y lotes: un posterior `git add .` puede filtrar esos ficheros a un repositorio. La regla del proyecto «no nombrar ni permitir señalar» no queda asegurada solo con decir «no se publicará la lista».
- **c) Gravedad:** **bloqueante para publicación o uso con datos reales sin barreras de privacidad**.
- **d) Corrección:** carpeta externa privada por defecto, permisos y `.gitignore` probado, separación de producto interno y público, aprobación editorial obligatoria con control de nombres, no exportar campo `senal_terminacion` ni título B por defecto; borrador público con agregados y supresión de identificadores/URL salvo justificación explícita. Documentar qué casos de expedientes individuales pueden publicarse y con qué contexto, sin convertir una señal de título en atribución de incumplimiento.

### B12 — Selección auxiliar en empates puede asignar título ajeno

- **a) Dónde:** `seleccionar_obras.py:133–154` (`resultados`, `auxiliares`, empates canónicos).
- **b) Qué falla:** si el resultado de `me.canonica(original)` no coincide con ninguna versión indexada, el código cae en `next(iter(opciones.values()), {})`: elige **arbitrariamente la primera versión disponible**, pese a que otra ha sido seleccionada como principal. Así podría asignar título, primer anuncio o comunidad erróneos al contrato. Es un comportamiento de reserva constatable en el código; no se ha demostrado su frecuencia con el corpus ausente.
- **c) Gravedad:** **importante**.
- **d) Corrección:** no usar fallback arbitrario; buscar y verificar la misma versión por un identificador estable, fallar con diagnóstico de discrepancia o dejar campos auxiliares vacíos, y cubrir empates sin clave coincidente con un test.

## 3. Señal de «terminación licitada de nuevo»: interpretación y cifras

### I13 — Sesgo de espectro y grupos operativos no equivalentes a verdades jurídicas

- **a) Dónde:** `PREREGISTRO.md`, `validar_e4t.py:99–115`, `INFORME_TERMINACION.md`, §9.0 ter.
- **b) Qué falla:** R significa «indicio documental de resolución localizado por el clasificador o CCN con causa» y N «otro indicio de fin y ninguna de esas marcas de resolución». No son auditorías exhaustivas con veredicto jurídico independiente; una liquidación puede acompañar una resolución y un anuncio sin código de causa no demuestra que el contrato acabara normalmente. La elección por publicación documental filtra a órganos con prácticas distintas y la correlación por órgano puede reducir el tamaño muestral efectivo. Por ello el RR de 10,2 es una **asociación observada condicionada a esos grupos publicados**, no una razón poblacional universal ni especificidad/precisión transferible a las 44.178 obras sin fin.
- **c) Gravedad:** **importante**.
- **d) Corrección:** denominar R y N «grupos documentales operativos», revisar manual y ciegamente los doce positivos y una muestra representativa de negativos, estratificar por órgano y año, validar por órgano no utilizado en desarrollo; no decir que 83% es la probabilidad de resolución de cualquier obra marcada.

### I14 — «Capta un 4 %» y «muy fiable» son expresiones que necesitan población

- **a) Dónde:** `INFORME_TERMINACION.md` (resumen), §9.0 ter, `interfaz.py` alrededor de la prioridad, `seleccionar_obras.py` (texto impreso), `SENAL_TERMINACION.md`.
- **b) Qué falla:** 10/273 = **3,66 % de los expedientes del grupo R observado**, no «en torno al 4 % de todas las resoluciones», porque muchas carecen de documentación para clasificarlas. «Muy fiable cuando aparece», «es muy específica», «primera señal positiva validada» y «sirve para señalar casos con bastante fiabilidad» se leen como probabilidad de acierto fuera del corpus de comparación. El 83 % de R entre los doce marcados depende además de la composición artificial R/N (273/558); no es valor predictivo positivo universal. «Una obra no marcada no dice nada» está bien expresado en varias piezas y debe mantenerse en **todas**.
- **c) Gravedad:** **importante**.
- **d) Corrección:** sustituir por: «Marcó 10 de 273 expedientes con indicios documentales de resolución (3,7 %), frente a 2 de 558 con indicios de terminación ordinaria (0,4 %). La magnitud y precisión no son trasladables a expedientes sin final publicado. **Una marca obliga a verificar; su ausencia no informa sobre el estado de la obra.**» Cambiar el tooltip de la GUI, las cabeceras y los mensajes de CLI.

### I15 — Confusión entre señal de documentación y prueba de fracaso

- **a) Dónde:** §9.0 ter («Si hizo falta otro contrato para terminar la obra, el primero no la terminó»), `INFORME_TERMINACION.md` y uso de prioridad en GUI/CSV.
- **b) Qué falla:** dos títulos similares y una nueva licitación son compatibles con recepción parcial, alcance complementario, financiación distinta, fases descritas de forma imperfecta y títulos poco específicos. Que B se licite después no acredita per se que A se resolvió, ni que se incumplió la ley, ni que falta un documento obligado. Se atenúa en la sección de límites, pero la formulación categórica reaparece antes.
- **c) Gravedad:** **importante**.
- **d) Corrección:** hablar consistentemente de «coincidencia documental compatible con una terminación ulterior que requiere comprobación»; solicitar estado, acuerdo y documentación concreta «si existen», sin presuponer el resultado; prohibir salidas de apariencia sancionadora.

### I16 — Contradicciones internas de la novena investigación y su alcance

- **a) Dónde:** `documento/Democracia_Auditable_v0_4_5.md` inicio del §9.0 ter (afirma que nueve pasaron revisión adversarial), junto al nuevo punto 9 «sin revisión adversarial»; `INFORME_TERMINACION.md` («Pendiente de decidir si entra... sería la novena»).
- **b) Qué falla:** contradicciones textuales: a fecha del ZIP la novena se acababa de añadir y no había sido revisada; su informe dice a la vez que aún podría incorporarse.
- **c) Gravedad:** **menor**.
- **d) Corrección:** «Ocho investigaciones pasaron rondas adversariales; la novena se somete a la presente» y «incorporada a la v0.4.5, pendiente de replicación independiente».

### I17 — El marco de 78/44.178 y la versión de «fin publicado» requieren comprobación

- **a) Dónde:** `investigaciones/9_terminacion/regla_e4t_v2.py`, `senales_medir.py`, `extraer_obras.py`, `fase0_placsp/medir_ejecucion.py`, el informe de la novena y el estudio v2.4.
- **b) Qué falla:** la selección original de «sin fin» aplica en `senales_medir.py` categorías/expresiones distintas de las de los *confirmados* por notas de modificación de `medir_ejecucion.py` v2.4; el extractor de la novena tiene además una política de desempate de versiones que su propio informe declara distinta. No se adjunta `obras.jsonl`, por lo que no se puede establecer que los 78 se calcularon bajo exactamente la misma definición de ausencia de fin del estudio vigente. El 0,18% sí es la división redondeada de los dos números anunciados, no un cotejo del universo.
- **c) Gravedad:** **importante**.
- **d) Corrección:** ejecutar ambos clasificadores sobre el mismo archivo y fecha de corte; exportar **solo agregados** de la tabla de coincidencias y discrepancias, explicar cada regla diferente y recalcular el total de la novena tras unificar la definición.

### I18 — Intervalos estratificados inestables: no atribuirles confirmación

- **a) Dónde:** tabla por importe de `INFORME_TERMINACION.md`, `validar_e4t.py` (`cociente`).
- **b) Qué falla:** los RR por tramos se apoyan en 5/1, 2/1 y 3/0 casos. En el último se usa corrección de continuidad Haldane 0,5: RR≈13,1; IC≈0,7–250, con p exacta ≈0,041. Es posible que el IC logarítmico corregido cruce 1 mientras la prueba exacta marque p<0,05: no es un fallo aritmético, sino métodos e incertidumbre extremos en muestras dispersas. El estudio tiene un contraste central, pero la generalización no es confirmatoria por diseño y los estratos siguen siendo secundarios.
- **c) Gravedad:** **importante**.
- **d) Corrección:** etiquetar todas las tablas por tramo «descriptivas y muy imprecisas»; mantener el RR/IC/p tal cual, explicar corrección y discrepancia entre métodos; considerar intervalos exactos o modelos ajustados en una réplica con más casos, sin reinterpretar post hoc los umbrales del preregistro.

## 4. Órganos autonómicos y reclamaciones

### I19 — El «58 % de las reclamaciones» tiene denominador incorrecto

- **a) Dónde:** `COMPLEMENTO_AUTONOMICO.md` introducción, §9.0 ter, `volumen.py`.
- **b) Qué falla:** 1.065/1.839≈57,9 % se refiere a **solicitudes proyectadas por ámbito** que podrían terminar, si se reclamasen, ante un garante autonómico. No equivale a la proporción de **reclamaciones efectivamente presentadas**: faltan las tasas de respuesta, el no recurso, competencia y exclusiones por jurisdicción.
- **c) Gravedad:** **importante**.
- **d) Corrección:** «El 58 % de las solicitudes potenciales del escenario correspondería a administraciones cuyo garante podría ser autonómico, si se diera una reclamación y se confirmara la competencia». No denominar el 1.839 «reclamaciones».

### I20 — «Ningún caso desestimado» no es «todos favorables»

- **a) Dónde:** `COMPLEMENTO_AUTONOMICO.md` tabla y conclusión; §9.0 ter.
- **b) Qué falla:** entre los 11 supuestos tipo (a) de GAIP se incluye expresamente **un suministro** (0478/2025) y **un desistimiento** (2199/2025). Un desistimiento no es una estimación del fondo; el suministro no es fin de obra. Se suman urbanizaciones posiblemente promovidas privadamente y casos de cargos electos con regímenes jurídicos distintos. Además, el reporte dice que solo dos citas fueron comprobadas de manera independiente y los ficheros del filtro no se distribuyen. No se puede concluir que «todos los precedentes relevantes sobre obra pública son favorables» con ese universo tal como está codificado.
- **c) Gravedad:** **importante**.
- **d) Corrección:** reclasificar el denominador en casos estrictos de obra pública, distinguir estimación, estimación parcial, satisfacción extraprocesal, desistimiento e inadmisión; publicar una metodología reproducible **sin administraciones individualizadas** y señalar «ninguna desestimación de fondo entre los pocos asuntos pertinentes clasificados» solo después de verificar la lista.

### I21 — El plazo de reclamación debe describirse por régimen jurídico, no por «órgano»

- **a) Dónde:** Anexo D, `GUIA.md`, `COMPLEMENTO_AUTONOMICO.md`, `registro.py`.
- **b) Qué falla:** «varía según el órgano» puede sugerir discrecionalidad del órgano administrativo cuando depende de la ley aplicable, tipo de recurso, efecto de silencio y criterios interpretativos del garante. El complemento cita una resolución de Madrid contra el silencio sin plazo preclusivo, mientras el art. 48 de su ley formula un mes desde el efecto del silencio; esa coexistencia requiere distinguir **texto legal y criterio interpretativo actualizado**, no una regla automática. No se ha hecho auditoría jurídica de la docena de regímenes aplicables.
- **c) Gravedad:** **importante**.
- **d) Corrección:** «Los plazos y la posibilidad de reclamar frente al silencio dependen de la normativa aplicable y de la doctrina del órgano competente; verificación individual previa a cada recurso». Citar el artículo, criterio y fecha; no informar una fecha preclusiva automatizada cuando hay criterios de no preclusión o un régimen no confirmado.

## 5. Facilidad de uso, metodología y consistencia editorial

### I22 — El calendario generado ignora festivos que el usuario sí facilita en GUI

- **a) Dónde:** `ciclo_mensual.py` (`pendientes`), `interfaz.py` (archivo de festivos para consulta puntual), `GUIA.md`.
- **b) Qué falla:** el archivo de festivos adicionales se utiliza al consultar pendientes desde la interfaz, pero el ciclo mensual escribe `pendientes_<fecha>.csv` **sin** `--festivos`, y el resumen puede señalar una fecha distinta de la que se ve en el botón interactivo.
- **c) Gravedad:** **importante**.
- **d) Corrección:** almacenar calendario jurídico/local de trabajo, transmitirlo a todos los cálculos, mostrar la versión/calendario usado en el resumen y bloquear el calendario si falta un calendario exigible.

### I23 — `informe_legible.py` mejora la clasificación, pero contiene una definición de fecha inconsistente

- **a) Dónde:** `fase0_placsp/informe_legible.py:112` y categorías `fin_en_nota_modificacion` / `fin_en_nota_candidato`; texto HTML de «Debería haber terminado» alrededor de la línea 407; documento §9.0 bis.
- **b) Qué falla:** las dos nuevas categorías están definidas y no se ha hallado en la inspección estática la regresión denunciada de contar un candidato como confirmado. Pero el texto HTML dice que la fecha estimada «No incluye prórrogas posteriores» mientras la metodología principal contempla modificaciones de plazo recogidas. Falta el CSV para comprobar los 1.651 resultados reales y la conciliación fila a fila con `resumen.json`.
- **c) Gravedad:** **menor** en texto; **importante** en la promesa de verificación no reproducible.
- **d) Corrección:** fijar una única definición exacta de «fin teórico» alineada con la función y documentar cuándo se incorporan ampliaciones; test automático por categoría contra `resumen.json` y un fixture de modificación confirmada versus candidata, más un smoke test del HTML.

### I24 — 98,7 % sobrevive como cifra histórica potencialmente equívoca

- **a) Dónde:** `investigaciones/2_cohortes/RESULTADOS.md` (tabla antigua v2.3), referencias históricas en documento y ejemplos aislados.
- **b) Qué falla:** el README ya presenta correctamente **1.549/1.593 = 97,2 %** como versión actual; el 98,7 % queda generalmente contextualizado como anterior. No obstante, la tabla con encabezado v2.3 en `RESULTADOS.md` mantiene 98,7 % destacado y puede circular recortada como vigente. No se encontró una sustitución completa que falsee la cifra vigente.
- **c) Gravedad:** **menor**.
- **d) Corrección:** rotular la tabla «Resultado histórico v2.3 — sustituido por v2.4 (97,2 %)» **encima** de los porcentajes; mantener el 98,7% solo como historial con versión, fecha y denominador.

### I25 — La reproducibilidad de P1–P5 de la revisión anterior es solo parcial en este ZIP

- **a) Dónde:** `revision_anterior/respuesta_revision_v0_4_4.md`, archivos prometidos de revisión manual y series históricas.
- **b) Qué falla:** se verifican estáticamente la separación «confirmado/candidato», la precisión editorial de 97,2 %, las cautelas sobre concentración de 22/24 en un solo órgano, los informes jurídicos y el tamaño del muestreo exploratorio. Sin embargo los CSV de revisión de los 24 y varias salidas citadas no están: **no puede confirmarse** que todos los supuestos reales hayan quedado bien clasificados o que las 2 candidatas estén separadas en los 1.651 registros. No se debe presentar «aceptado y corregido» como «replicado independientemente».
- **c) Gravedad:** **importante** para el reclamo de réplica; **menor** para borrador.
- **d) Corrección:** separar en una tabla «corrección de código observada / prueba sintética pasada / prueba corpus real pendiente», incluir datos públicos revisables anonimizados o un hash con protocolo de auditoría privada y ejecutar la repetición ante revisor externo.

### I26 — Errores de rutas/documentación y falsas garantías de facilidad

- **a) Dónde:** referencias en los informes a `investigacion_consejo/`, `investigacion_doc_ccn/`, `fuentes/autonomicos/`, `fuentes/l39_art30.txt`; `README.md` y la propia GUI.
- **b) Qué falla:** varias rutas corresponden al árbol original de trabajo, no al ZIP entregado, y otras apuntan a archivos deliberadamente omitidos. La guía de la GUI dice que «hace todo el protocolo» aunque no presenta solicitudes ni verifica que el garante y plazos sean correctos; el contenido interior sí aclara que no envía, pero un usuario inexperto puede interpretar «herramientas funcionan» cuando 11 pruebas se omiten y los datos de ejemplos faltan.
- **c) Gravedad:** **importante**.
- **d) Corrección:** normalizar rutas relativas al paquete distribuidor, listar claramente los ficheros omitidos por privacidad y reemplazar «hace todo» por «prepara borradores, registro y avisos provisionales; requiere verificación y presentación humana»; no anunciar funcionalidad sin un test real en Windows/macOS/Linux.

### I27 — La muestra «reproducible» cambia de composición si cambia la prioridad

- **a) Dónde:** `seleccionar_obras.py:247–271`, sorteo con `random.Random(a.semilla).sample(candidatas, a.muestra)` después de ordenar candidatas por `--prioridad`.
- **b) Qué falla:** una semilla fija solo reproduce el sorteo para el **mismo orden de entrada**; pasar de `antiguedad` a `terminacion` reordena el marco y puede cambiar las obras de la muestra al mantener la misma semilla. Si una entidad compara ambos criterios, la «muestra aleatoria fija» puede dejar de ser la misma; además se sortea después de aplicar los filtros del flujo/fecha según la orden recibida, por lo que debe fijarse el marco explícitamente.
- **c) Gravedad:** **importante**.
- **d) Corrección:** ordenar por `id` estable **antes de sortear**, con independencia de la prioridad, y solo después ordenar los sorteados para preparar lotes; guardar el marco (ids y hash), fecha y parámetros y prohibir cambios retroactivos.

### I28 — Doble contabilidad institucional y métrica del protocolo no auditada

- **a) Dónde:** `ciclo_mensual.py`, `registro.py:en_plazo/resumen`, guía.
- **b) Qué falla:** las cifras «respondidas en plazo» dependen de fechas provisionales y de notas que no codifican suspensiones/pausas, además del problema autonómico ya descrito. Las comparaciones entre órganos o entre meses tendrían denominadores y reglas jurídicamente heterogéneas. Las tareas muestran el `garante` «sugerido, sin verificar», pero nada impide usarlo directamente como destinatario.
- **c) Gravedad:** **importante**.
- **d) Corrección:** desactivar métricas jurídicas comparativas y envío de modelos de reclamación hasta tener recepción, calendario, régimen, garante y documento de ampliación verificados. Guardar `calidad_del_dato`, `norma_aplicada` y `verificado_por`, permitiendo separar «plazo calculado» de «plazo legal confirmado».

## 6. Estado de la respuesta a v0.4.4 (P1–P13)

| Punto de la revisión anterior | Estado de este ZIP | Justificación breve |
|---|---|---|
| P1. Falsos positivos de liquidación | **Parcialmente comprobado** | Patrón de dos niveles y 32 pruebas aprobadas; no se adjunta revisión manual 24/2. |
| P2. Concentración | **Corregido editorialmente** | Se reconoce 22/24 de un órgano y no se generaliza. |
| P3. Muestreo 0/60 | **Corregido en cautelas** | Se declara exploratorio; no se traslada cota sin ponderar. |
| P4. Señal de inicio 42/69 | **Corregido editorialmente; réplica pendiente** | Límite del emparejamiento y día en `updated` explicitados. |
| P5. Modificaciones opacas y art. 207 | **Corregido en alcance** | Se distingue calidad documental de irregularidad. |
| P6. Plazos | **Solo parcialmente resuelto; nuevo bloqueante** | Mejora calendario general y fecha de recepción, pero falta plazo propio de cada régimen. |
| P7. Topes y duplicados | **Parcialmente resuelto; regresión operativa** | Excluye lotes previos, pero tope=0, pruebas omitidas y carpeta local impiden garantía global. |
| P8. Muestra fija/seguimiento | **Regresión bloqueante** | Falla `muestra.csv` cuando N≥elegibles; reproducibilidad cambia según orden. |
| P9. Margen 120 días | **Matizado correctamente en teoría** | La guía aún dice «deberían existir», más categórico que la cautela de fondo. |
| P10. Plantillas | **Bien encaminado** | Petición condicional y sin documentos excesivos; exige revisión de existencia/competencia. |
| P11. Garante | **Parcial** | Indica «sugerido», pero se usa en tareas sin verificación forzosa. |
| P12. Publicación | **Parcial** | Exporta BORRADOR, pero lista del estudio y lote privado nombran órganos y pueden filtrarse. |
| P13. ±7 puntos | **Cautela corregida; diseño pendiente** | Advertencia sobre muestreo simple, pero flujo sin reserva aleatoria y semilla dependiente del orden. |
| Código: desempate de versiones | **Incompleto** | Queda fallback a primera versión auxiliar si no coincide canónica. |
| Código: paquete instalable | **No resuelto en este ZIP** | Imports y archivos faltantes. No se prejuzga un repositorio externo distinto. |

## 7. Conciliación de cifras y qué sí es defendible

| Afirmación | Comprobación | Lectura admisible |
|---|---|---|
| Estudio v2.4: 1.549/1.593 = 97,2 % | División correcta; 98,7 % aparece como histórico | Métrica de detección del clasificador en ese canal, **no tasa real de incumplimiento ni recepción física**. |
| Señal: 10/273 vs 2/558 | 3,663 % vs 0,358 % | Tasas condicionadas a dos grupos documentales publicados. |
| RR 10,2; IC95 2,3–46,3; Fisher p=0,0004 | **Verificado** de forma independiente | Asociación en la población seleccionada. El IC es muy ancho. |
| Entre marcados R: 10/12 = 83 % | Correcta la división | **No** equivale a valor predictivo aplicable a todas las obras. |
| 3/103 vs 0/193 (tramo no usado en diseño) | Fisher ≈0,041; IC RR corregido ≈0,7–250 | Señal prometedora, pero muy imprecisa; no cumple el criterio preregistrado por sí sola. |
| 78/44.178 = 0,18 % | Correcta la división | No auditado contra el corpus; posible definición divergente de «sin final». |
| 69 órganos, máximo 3 | Solo declarado en informe | No comprobable sin la lista excluida por privacidad. Mejor mantener solo agregado con cautela. |
| 0/20 páginas con resolución visible | Solo declarado en informe | Comprobación exploratoria no replicable desde este ZIP; ausencia en web ≠ ausencia en otros canales. |
| 1.065/1.839 = 58 % | División correcta | Proyección de solicitudes por ámbito, **no porcentaje de reclamaciones efectivas**. |
| 3–4 y 11 casos autonómicos | Enumeración interna inconsistente con tipo estricto | Depurar suministro/desistimiento/urbanizaciones y accesos reforzados. |

**Punto positivo:** los cambios de la versión 0.4.4 han avanzado mucho en distinguir «indicador documental» de «ilegalidad», en reconocer el sesgo de concentración y en no ocultar que la revisión manual y los preregistros no son independientes. Los números fundamentales de v2.4 y de la señal nueva, como operaciones, son coherentes. No hay motivos para borrarlos, pero sí para cambiar la interpretación y calificación del grado de evidencia.

## 8. Riesgos de nombrar personas u órganos

1. El **documento público agregado** no contiene aquí una relación de 78 órganos marcados; eso es correcto.
2. Un `lote.csv` de uso operativo incluye organismo, título, enlace y nombre de la licitación que activó la señal; **sí permite señalarlos**. Se debe mantener estrictamente privado, no confiar solo en una nota editorial.
3. La lista legible del **estudio** permite consultar organismos por nombre y expedientes. Aunque no etiquete fracasos, hay tensión con una norma general redactada como «no permitir señalar». Hace falta delimitar si se prohíben solo imputaciones o también cualquier lista de expediente/órgano; si es lo segundo, la lista publicada no es compatible.
4. Los borradores de solicitudes y reclamaciones deben identificarse para su presentación, pero sus campos personales han de seguir fuera de cualquier exportación pública. Un enlace a documentación puede contener firmas/identificaciones: una simple supresión de nombres en CSV no anonimiza todo el expediente.
5. El directorio fuente como carpeta de trabajo y ausencia de `.gitignore` en este ZIP aumentan el riesgo de publicación accidental de registros y lotes. El repositorio real podría contenerlo; **el paquete evaluado no**.

## 9. Plan mínimo de salida y veredicto

**Antes de difundir la v0.4.5 como borrador de investigación:** cambiar las cinco frases centrales (validación «confirmatoria», «muy fiable», «4% de las resoluciones», «58% de reclamaciones», «todos favorables»), corregir la contradicción de las «nueve revisadas», separar historia 98,7% de resultado vigente, declarar que los datos y pruebas no permiten réplica independiente completa y colocar una advertencia visible de que el protocolo jurídico aún no es apto para expedientes reales.

**Antes de publicar el código como repositorio que se pueda ejecutar:** corregir B01, B04, B05, B07, B08, B09 y B10; incorporar tests con dos ciclos y con interrupción; hacer pública la estructura de dependencias, las rutas y las exclusiones de datos privados; generar una copia limpia y **hacer pasar todas las pruebas sin omisiones**. Añadir pruebas de equivalencia de la señal e informe HTML para los datos sintéticos. Documentar los 78/44.178 como resultado agregado no auditado desde este ZIP si no se publica el corpus.

**Antes de realizar solicitudes o presentar reclamaciones:** corregir B03, B06, B11, I21, I22 e I28; verificar por humanos plazos y órgano competente en el régimen concreto, implantar controles de tope y reserva aleatoria; revisar impacto en administraciones y personas, política antiabuso, seguimiento de la muestra y controles de información sensible. La aplicación no debe sugerir que una reclamación se puede presentar automáticamente en función de la fecha calculada.

**Veredicto final:** **Documento v0.4.5: distribuible únicamente como *borrador crítico* tras las correcciones editoriales prioritarias, con los hallazgos no replicados identificados. Paquete de código adjunto: no apto todavía como repositorio instalable ni como herramienta operativa. Protocolo para solicitudes reales: no apto hasta corregir el motor jurídico y reforzar límites, gestión de privacidad y validación humana.** No se ha probado el repositorio público de origen —solo este ZIP— y no se ha enviado ninguna solicitud.

### Referencias jurídicas externas contrastadas

- BOE, Ley 10/2019 de la Comunidad de Madrid, texto consolidado, arts. 42 y 48: <https://www.boe.es/buscar/act.php?id=BOE-A-2019-10102>
- Comunidad de Madrid, sede electrónica, «Acceso a información pública» (20 días, ampliables): <https://sede.comunidad.madrid/comunicaciones-declaraciones/acceso-informacion-publica>
- Ayuntamiento de Madrid, solicitud de acceso (20 días hábiles): <https://sede.madrid.es/portal/site/tramites/menuitem.62876cb64654a55e2dbd7003a8a409a0/?vgnextchannel=23a99c5ffb020310VgnVCM100000171f5a0aRCRD&vgnextfmt=default&vgnextoid=48422ee1f6851510VgnVCM2000000c205a0aRCRD>

---

**Nota metodológica:** Se han contrastado por lectura de código las ramas mencionadas y se han hecho pruebas sintéticas de fallos concretos. Los hallazgos estadísticos y jurídicos son independientes de que se entregue en el futuro un ZIP más completo. Los hallazgos de empaquetado se refieren solamente a la distribución examinada; no implican necesariamente que falten los archivos en otro repositorio o equipo.
