# Revisión adversarial de «Democracia Auditable» v0.4.4

**Para:** Claude y la persona que coordina la revisión entre modelos  
**Fecha:** 1 de noviembre de 2026  
**Material:** `para_chatgpt_v044.zip` (`ENCARGO_REVISION_v0_4_4.md`, documento fundacional, fase 0 v2.4, ocho investigaciones y protocolo de obras).  
**Alcance:** revisión del código y de los textos suministrados; contrapruebas sintéticas ejecutadas; contraste de normas concretas con el BOE. No he reejecutado las extracciones masivas: faltan los 13–15 ZIP originales y los CSV intermedios.

## Dictamen ejecutivo

La v0.4.4 es un **avance real**: corrige a la baja una cifra al localizar una fuente de falsos negativos, añade controles negativos importantes («no inferir obra parada ni incumplimiento») y convierte la hipótesis del §8.6 en un protocolo concreto para recabar documentos y registrar respuestas. **Puede circular como borrador de trabajo con limitaciones explícitas**, una vez corregidas las frases categóricas y los defectos de mayor riesgo.

**No considero el Anexo D ni sus scripts listos para presentarse como herramienta jurídica operativa.** Su calendario de reclamaciones omite días inhábiles y el momento real de recepción por el órgano competente; el control de una solicitud por obra y cuatro por órgano y mes no es global ni transaccional. Tampoco considero el 97,2 % una tasa validada de falta real de información: es una métrica del clasificador en el canal estudiado.

### Comprobaciones realizadas

- La huella del archivo suministrado `fase0_placsp/medir_ejecucion.py` es **`ac06a31184220dddf34d674b30d286de776138f5ee8860350447dc3fcabb3cf0`**, igual que la del `manifiesto.json` incluido.
- Las huellas de **ambos preregistros** coinciden con sus archivos: inicio `0dafe53e…2fbaca2f7`; modificaciones `50bb51c1…024865a43`. Esto comprueba la integridad de las copias; **una huella sin sello temporal externo no prueba por sí sola que el preregistro precediera a mirar los datos**. Se conserva como declaración de proceso, no como certificación temporal independiente.
- Ejecuté **22/22 pruebas del protocolo**, todas correctas **cuando se incluyen manualmente en `PYTHONPATH` los módulos de la carpeta `investigaciones/1_anuncio_finalizacion` y `fase0_placsp`**. En la ejecución directa sin esa adaptación se omitían cinco pruebas porque el script no encontraba `escanear`.
- Las pruebas completas de `fase0_placsp` y `test_escanear.py` **no arrancan con este paquete** porque falta `informe_legible.py`, que importa `test_medir_ejecucion.py`. No es prueba de un fallo en el repositorio completo: el ZIP es un paquete de revisión parcial.
- El patrón v2.4 se contrastó con frases sintéticas; también se simuló generar dos lotes en la misma fecha, sin registro actualizado. Resultados reproducibles abajo.

## 1. Corrección v2.4: indicador de fin en `Note`

### P1 — El patrón admite falsos positivos semánticos

- **Dónde:** `fase0_placsp/medir_ejecucion.py`, líneas 110–118 y 343–347; `investigaciones/8_modificaciones/INFORME_MODIFICACIONES.md`; §9.0 bis.
- **Fallo:** `FIN_EN_NOTA` acepta `^liquidaci` al comienzo de cualquier texto y `certificaci\w*\s+final` sin verificar el objeto ni si hay fases. `EXCL_FIN_EN_NOTA` descarta únicamente `parcial|danos|perjuicio` de forma global. Ejecutando las expresiones reales obtuve:

  | Texto sintético | Clasificación actual | Problema |
  |---|---|---|
  | `Liquidación de penalidades contractuales` | Fin definitivo | No acredita extinción ni fin de la obra |
  | `Liquidación de anticipos` | Fin definitivo | No acredita fin |
  | `Liquidación provisional de la obra` | Fin definitivo | Provisional ≠ definitivo |
  | `Certificación final de la fase 1` | Fin definitivo | Puede quedar obra por ejecutar |
  | `Liquidación definitiva del contrato` | Fin definitivo | Posible acierto; comprobar alcance |
  | `Certificación final de la obra, tras recepción parcial` | No fin | Posible falso negativo por exclusión global |

- **Gravedad:** **importante** para reutilizar el clasificador fuera de la cohorte revisada. **No invalida por sí mismo los 24 casos añadidos**: el informe dice que se revisaron todos manualmente, pero no se adjunta el detalle que permita repetir esa revisión.
- **Corrección:** separar **«candidato detectado»** de **«finalización confirmada»**; elaborar una tabla de textos con verdaderos y falsos positivos, cobertura por órgano y lotes, un conjunto de pruebas positivas/negativas y etiquetas de revisión. No elevar automáticamente todos los `Note` a «fin definitivo». Conservar las 24 revisiones con cita/huella y documentar si se refieren al **contrato completo** o a un lote. Mantener la tasa del estudio solo con el alcance exacto que demuestran esas 24 comprobaciones.

### P2 — Concentración del 63 %: no equivale a difusión generalizada

- **Dónde:** §9.0 bis; `METODO.md`; investigación de modificaciones.
- **Fallo:** el 63 % de las coincidencias procede de un órgano en el corpus general. No es una prueba de una práctica común en las administraciones. Puede sesgar mucho la validez externa del patrón.
- **Gravedad:** **importante** para la interpretación; no necesariamente para el numerador observado.
- **Corrección:** decir «práctica observada, concentrada en pocos órganos». Mostrar resultados estratificados **sin identificar órganos** y validar el patrón fuera del órgano dominante antes de extender conclusiones.

## 2. Formulación y trazabilidad del 97,2 %

- **Dónde:** portada y Nota de versión, §8.6, §9.0 bis, Anexo A.8, `METODO.md`.
- **Resultado:** la **cifra vigente está bien propagada**: 1.549/1.593 = 97,2 %. En los apartados principales se explica que solo mide coincidencias sobre el canal estudiado.
- **Problema menor:** en la «Nota sobre esta versión» todavía se abre una viñeta histórica con `1.573 (98,7 %; 97,2 % con la corrección)`. Aunque es defendible como historial, distrae al lector que busca la cifra actual. `METODO.md` aún se refiere a «v0.4.2» y a «tres revisiones adversariales independientes», expresión que ya habíamos corregido por su ambigüedad.
- **Gravedad:** **menor**.
- **Corrección:** empezar toda presentación de resultados por «1.549/1.593 (97,2 %)» y relegar `98,7 %` a la tabla de historial v2.3→v2.4; sustituir «revisiones independientes» por «rondas de revisión con ChatGPT» también en `METODO.md`.

## 3. §9.0 ter: comprobación de las ocho ramas

| Rama | Evaluación adversarial | Ajuste aconsejado |
|---|---|---|
| 1. Anuncio de finalización | Correctamente distingue expedientes de contratos y porcentajes condicionados a publicar. El desfase de duración **no prueba retrasos jurídicos**. | Conservar expresamente la unidad de cada cifra y la exclusión de prórrogas no observadas. |
| 2. Cohortes 2021–2022 | El patrón descrito no desaparece con años adicionales, pero cambia el mecanismo disponible (`DOC_CCN` aparece desde 2024), los datos están censurados y el clasificador no tiene validación equivalente. | Cambiar «no es cuestión de tiempo» por «el mayor tiempo observado no basta para explicar la baja detección». |
| 3. Validación 0/60 | Los 60 casos provienen de **12 estratos con 5 obras cada uno**; no es una muestra aleatoria simple proporcional al universo. El 6,0 % de cota exacta es binomial **bajo supuestos de homogeneidad que la estratificación no garantiza**. Además, se revisaron las páginas por el mismo sistema. | Presentar «0/60 en la muestra estratificada»; no trasladar sin ponderar su IC al conjunto poblacional. Publicar los resultados por estrato como exploratorios y conservar las limitaciones de revisión. |
| 4. Marco jurídico | La LCSP art. 63.3 no establece una obligación general de publicar fin, pero sí existen obligaciones de comunicación (arts. 335 y 346) y documentos exigibles **cuando concurren las fases correspondientes**. El RD 817/2009, art. 31, existe en el BOE, pero el encaje reglamentario completo sigue pendiente de jurista. | Evitar «los documentos existen por ley» para **cada** expediente: deben existir cuando la fase se ha producido, salvo particularidades. «Comunicar el fin sí es obligatorio» ha de matizarse por tipo/umbral/supuesto. |
| 5. Consejo de Transparencia | Correcta la advertencia de que el 34–46 % de silencio tiene como denominador **reclamaciones** y no solicitudes. «Estimatoria por motivos formales» está respaldada por el caso citado para entrega durante reclamación, pero no todas las variantes tienen por qué ser idénticas. Once resoluciones no establecen por sí solas doctrina general. | Usar «resoluciones examinadas» y «criterio visible en casos concretos», no garantía universal de acceso. No inferir prevalencia nacional de silencio. |
| 6. Registro vasco | Bien separado del corpus PLACSP; 2018 se excluye por sesgo de selección plausible: el fichero de 2019 recoge **actualizaciones**, muchas asociadas al fin. No es prueba de cobertura general. | Justificar el filtro histórico de ≥50.000 € como **criterio analítico**, no como identificación jurídica segura de «no menores», y declarar que excluye muchos expedientes sin plazo estimable. |
| 7. Inicio (preregistrada) | Es legítimo usar la última versión previa al **primer anuncio** para aproximar lo visible antes del anuncio. Pero se comparan cohortes/denominadores distintos y se excluyen 141 casos sin versión previa (7 ≥1 M€). Que quienes publican `DOC_CCN` publiquen más es plausible, **no un sesgo de signo probado**. | Sustituir «igual o mayor» como inferencia por «podría ser mayor; dirección no contrastada». Sustituir «no distingue» absoluto por «tiene escasa capacidad discriminatoria en esta muestra». |
| 8. Modificaciones (preregistrada) | La definición de «opaca» (ni importe, ni plazo, ni texto ≥40 caracteres) es transparente pero **operativa**, no jurídica. Un `Note` de 35 caracteres puede explicar lo suficiente. Los nombres de adjuntos no miden por sí solos el cumplimiento del art. 207.3. | Mantener «indicador de calidad informativa», jamás «modificación irregular». `IssueDate` del XML **no está verificado como fecha de aprobación**; 36 % >5 días es comparación descriptiva, no tasa de incumplimiento. |

### P3 — Los intervalos de la muestra 0/60 pueden inducir a error

- **Dónde:** `investigaciones/3_validacion/RESULTADO_VALIDACION.md` y §9.0 ter punto 3.
- **Gravedad:** **importante** si se presenta el 6 % como cota aplicable al universo general.
- **Corrección:** mantener el resultado observado y calcular, si interesa inferencia poblacional, una estimación ponderada por el tamaño de los 12 estratos con incertidumbre acorde al diseño. Mejor aún: posponer la inferencia y declarar la muestra como **validación exploratoria**.

### P4 — La calibración del inicio no acredita la dirección del sesgo

- **Dónde:** `investigaciones/7_inicio/INFORME_INICIO.md`, §2, y §9.0 ter punto 7; `analizar_inicio.py`.
- **Gravedad:** **importante** para la inferencia sobre obras no observadas.
- **Corrección:** el hecho observado es **42/69 (60,9 %) sin indicio antes del anuncio** entre los casos ≥1 M€ que pudieron calibrarse, IC95 ~48–72 %. No tenemos una muestra aleatoria de **todas las obras ejecutadas** y se excluyen obras sin versión anterior. No trasladar el 61 % a todas las obras ejecutadas ni afirmar certeza sobre el signo del sesgo. La comparación preanuncio emplea `updated` truncado a fecha y lo compara con la fecha del aviso: puede excluir actualizaciones del mismo día y no equivale necesariamente al momento de publicación pública. Documentar ese límite. La función `formalizacion()` toma **la primera fecha de todos los contratos del expediente**; para evaluar retrasos del inicio real de **cada contrato o lote** debería vincular la fecha contractual específica, o advertir el posible error de emparejamiento.

### P5 — Sobre documentación del art. 207.3

- **Dónde:** `investigaciones/8_modificaciones/INFORME_MODIFICACIONES.md`, §9.0 ter punto 8.
- **Gravedad:** **importante** si se interpreta como omisión legal.
- **Corrección:** los nombres genéricos no permiten identificar informes; la revisión de 30 obras fue **seleccionada por opacidad**, no aleatoria entre todas las modificadas; las ampliaciones de plazo pueden seguir régimen propio (art. 203.1). No presentar la ausencia en los nombres ni el XML sin campo de adjuntos como prueba de incumplimiento. La fecha `IssueDate` no acredita aprobación. El texto actual en gran parte ya introduce estas cautelas; mantenerlas de forma prominente.

## 4. Protocolo de obras, Anexo D y código

### P6 — El calendario automatizado no es fiable para producir avisos jurídicos definitivos

- **Dónde:** `protocolo_obras/registro.py`, `limite()` y `mas_meses()` (líneas 46–63), `pendientes()` (132–155); Anexo D.1, regla 6.
- **Fallo:** se computa desde **`fecha_envio`**; el art. 20.1 de la Ley 19/2013 lo computa desde la **recepción por el órgano competente para resolver**, que puede diferir del envío al registro. Además, la suma de meses no desplaza un vencimiento inhábil al primer día hábil siguiente (art. 30.5 Ley 39/2015). Cualquier `fecha_ampliacion` no vacía suma automáticamente un mes sin comprobar el contenido y la validez de la notificación. No se manejan suspensiones ni regímenes autonómicos particulares. Ejemplo: `mas_meses(2026-01-31)` devuelve **2026-02-28**, sábado; la aplicación marca ese día como vencimiento, sin ajuste.
- **Gravedad:** **bloqueante para uso con reclamaciones reales** (aunque no bloquea la difusión como diseño).
- **Corrección:** incorporar `fecha_recepcion_organo_competente`, `plazo_resolucion_notificado`, razón/documento de ampliación, calendario y jurisdicción; tratar el vencimiento como **provisional** hasta verificación humana, no como plazo jurídico listo para publicar. Al menos, advertencia de inhábiles y revisión manual obligatoria para reclamaciones. El plazo para reclamar tras silencio debe seguir marcado como **criterio prudencial** pendiente de asesoramiento jurídico, no como caducidad inequívoca.

### P7 — El límite «4 por órgano y mes» y la regla «una pregunta por obra» no están garantizados

- **Dónde:** `protocolo_obras/seleccionar_obras.py`, `cmd_seleccionar`, líneas 155–205; Anexo D.1, regla 5.
- **Fallo:** `por_organo` se crea vacío **en cada lote**, y `leer_registro` solo excluye expedientes previamente añadidos al CSV. Dos ejecuciones en el mismo mes, sin actualizar registro, generan hasta 4 solicitudes cada una **para el mismo órgano y las mismas obras**. Lo reproduje con 10 obras sintéticas de un órgano: lote `run1` → 4 (`obra_0`–`obra_3`); lote `run2` el mismo día → **las mismas 4**. Ocho documentos preparados; cuatro IDs repetidos. `registro.py crear` deduplica al registrar, pero eso no impide preparar o enviar dos lotes antes de registrar. Tampoco se suma por mes lo ya enviado por otras organizaciones.
- **Gravedad:** **bloqueante para una ejecución coordinada o automatizada de envíos**.
- **Corrección:** registrar reservas/selecciones y sus estados (`seleccionada`, `enviada`, `anulada`), garantizar unicidad de obra y límite **en una base compartida y transaccional** o, para un piloto offline, con bloqueo de archivo y obligación de generar un único lote mensual por órgano y validar contra el historial mensual. El sistema no envía automáticamente; añadir una comprobación de duplicados inmediatamente antes de firma/presentación. Especificar además si «obra» significa **expediente o contrato/lote**: el programa identifica expedientes y uno puede contener varias obras o contratos.

### P8 — La muestra fija puede perder unidades al actualizarse el universo

- **Dónde:** `seleccionar_obras.py`, `cmd_seleccionar`, líneas 163–196, rama `--lista`; `protocolo_obras/PROTOCOLO_OBRAS.md` («muestra completa los meses siguientes»).
- **Fallo:** `--lista` filtra **después** de recalcular elegibilidad. Si una obra de la muestra sorteada recibe un indicador nuevo, cambia el presupuesto/estado o deja de estar en `obras_protocolo.csv` antes de preguntarla, desaparece sin constancia; la tasa observada entre quienes reciban solicitudes puede sufrir **sesgo de seguimiento**. Las pruebas cubren una muestra sintética estática, no esa transición.
- **Gravedad:** **importante**.
- **Corrección:** conservar un **marco muestral congelado** (`id`, instante, criterios, elegibilidad inicial, semilla), y para cada caso registrar `preguntada`, `ya publicado después`, `excluida con motivo`, `perdida`, `pendiente`. No cambiar silenciosamente el denominador de 200 ni volver a sortear para sustituir casos sin reportarlo.

### P9 — El margen de 120 días es heurístico; la pregunta puede ser prematura

- **Dónde:** Anexo D.1.2, `PROTOCOLO_OBRAS.md`, selección y plantilla.
- **Fallo:** suma un mes genérico más tres desde el **fin teórico estimado**, pero el art. 243.1 cuenta los tres meses **desde la recepción**, que puede producirse mucho después de lo estimado, o pueden existir fases, suspensiones y excepciones de certificación hasta cinco meses para ciertas obras de elevado valor. El art. 210.2 no permite afirmar una fecha efectiva de recepción a partir de la fecha teórica. El protocolo ya sabe que es estimación y que debe pedir documentos existentes; conviene evitar que el margen parezca un plazo legal incumplido.
- **Gravedad:** **importante**.
- **Corrección:** describir 120 días solo como **umbral operativo de contacto**, no como indicador de retraso. Prever respuesta «obra pendiente/no recibida», «recepción parcial», «contrato resuelto», «datos no localizados» y adaptar el documento que se pide al lote.

### P10 — Plantilla de acceso: útil, pero necesita precisión para reducir inadmisiones

- **Dónde:** `plantillas/solicitud_obra.txt`, `plantillas/reclamacion_silencio.txt`.
- **Fallo:** la alternativa «último documento ya existente que refleje la situación del contrato» es abierta; puede dar lugar a discusión sobre qué es «último» y qué documentos deben seleccionarse, aunque el texto no pide fabricar informes. «La respuesta o su ausencia se registrará de forma agregada» es ambiguo si el objetivo es un registro **por obra**. La plantilla dice «es la única solicitud que se formulará sobre este contrato», aunque podría haber lotes y solicitudes ajenas a la organización.
- **Gravedad:** **importante** (riesgo de inadmisión/disputa, no ilegalidad demostrada).
- **Corrección:** para el caso de ausencia de recepción, pedir **documentos concretos por orden de prioridad**, existentes a la fecha y bien identificables: último acuerdo de suspensión o prórroga, acta de comprobación del replanteo, acuerdo de resolución, según proceda. No solicitar certificaciones periódicas. Cambiar a «esta organización no prevé reiterar una solicitud equivalente sobre este expediente/lote» y «publicaremos metadatos de respuesta por obra, con anonimización». Mantener revisión humana del texto.

### P11 — Asignación del garante y competencia

- **Dónde:** `seleccionar_obras.py`, `garante(tipo, ccaa)`, líneas 46–81; Anexo D.3.
- **Fallo:** emplea tipo codificado de entidad y **provincia del código postal** para inferir competencia jurídica. Esa ubicación no siempre determina adscripción y el régimen de consorcios, entidades mixtas y organismos autónomos puede requerir análisis propio. El programa ya marca `otro` como «comprobar»; sin embargo, un caso mal atribuido a `estatal` o `autonómico/local` puede pasar inadvertido.
- **Gravedad:** **importante** para reclamaciones reales.
- **Corrección:** «garante sugerido» con estado `sin_verificar`, no destinatario automático. Validar adscripción real, ámbito y convenios **antes de enviar una reclamación**. Los resultados de convenios dependen de la fecha del caso.

### P12 — Riesgos de publicación y de uso masivo

- **Dónde:** Anexo D y `registro.py exportar`; `protocolo_obras/PROTOCOLO_OBRAS.md`.
- **Fallo:** `exportar` excluye campos privados conocidos, pero el enlace oficial, la fecha de replanteo, la obra y la combinación de fechas pueden permitir reidentificación indirecta de personas físicas en los documentos enlazados; el proceso no incorpora una revisión de protección de datos antes de publicar. «Una por obra» y «cuatro por órgano al mes» reducen carga pero **no constituyen un salvoconducto jurídico frente al abuso de derecho**. Un plan de 1.800 solicitudes anuales requeriría entidad responsable y valoración del impacto administrativo; de momento es una simulación, no un piloto avalado.
- **Gravedad:** **importante**.
- **Corrección:** exportar primero a **borrador** de publicación; revisión de privacidad y acceso a la información caso por caso; conservación de originales solo bajo custodia privada; mostrar métricas agregadas y enlaces puntuales tras revisión editorial. No presentar los topes como garantía de admisibilidad.

### P13 — Intervalo «200 ±7 puntos» condicional

- **Dónde:** Anexo D.2 y `PROTOCOLO_OBRAS.md`, arranque.
- **Fallo:** ±7 puntos es el margen nominal máximo a 95 % de una muestra aleatoria simple de 200 unidades con **respuestas completas**, p≈0,5. El propio protocolo aplaza preguntas y habrá no respuesta, cambios de elegibilidad y posible agrupamiento por órgano. El margen real puede ser mayor y aparecer sesgo de no respuesta.
- **Gravedad:** **importante** si se prometiera precisión estadística incondicional; **menor** si se declara hipótesis orientativa.
- **Corrección:** decir «±7 puntos **solo bajo muestreo aleatorio simple y respuesta completa**». Registrar tasa de respuesta, resultados por estrato y pérdidas; publicar intervalos y sensibilidad a no respuesta al final.

## 5. Código y reproducibilidad: otras observaciones

1. `seleccionar_obras.py` reconoce expresamente que añade `titulo` y `cp_organo` a la **representación canónica utilizada para desempatar** versiones con igual `updated` y, por tanto, puede elegir un estado distinto al del estudio. **Importante:** aplicar el desempate sobre los campos canónicos comunes **antes** de añadir campos auxiliares, para que la selección de expedientes no dependa del programa que los consulta.
2. `registro.py` solo valida algunas dependencias y orden de fechas; no distingue notificación/resolución de su entrega real, fecha de recepción por competente, suspensión de plazo ni circunstancias de recurso. No utilizar `en_plazo` como indicador jurídico definitivo sin revisión.
3. `analizar_inicio.py::clopper_pearson()` implementa correctamente, en su planteamiento matemático básico, un intervalo exacto bilateral binomial; **no he detectado un fallo evidente en las bisecciones**. El problema principal es de supuestos de muestreo y comparabilidad, no esa fórmula.
4. La estructura del **paquete recibido** cambia nombres de carpetas (`investigaciones/7_inicio/`) frente a las importaciones del repositorio (`investigacion_inicio/`), además de omitir `informe_legible.py`. Indicar expresamente que es un **paquete de revisión, no un release instalable**. Para publicar, producir un archivo de release que arranque desde una instalación limpia y tenga `requirements`/comandos reproducibles, sin los datos protegidos.
5. Los preregistros están íntegros y su SHA-256 coincide; para demostrar anterioridad temporal frente a terceros necesitarían publicación con fecha verificable (p. ej. commit público anterior a los resultados) o manifestación expresa de que la fecha es declarada.

## 6. Reglas del proyecto: posible identificación y comparaciones

- **No he encontrado** en el texto principal de la v0.4.4 ni en los ocho informes incluidos un ranking nominal de administraciones o acusaciones contra personas. Se usan concentraciones por órgano sin identificarlos, y se separan hechos documentales de culpabilidad. Es compatible con las reglas fundamentales del proyecto.
- El **código, los CSV de salida y los justificantes** sí podrían revelar órganos, obras, expedientes e incluso datos indirectamente reidentificables. Son datos relevantes para auditar, pero la decisión de qué se publica debe ser editorial y jurídica; no basta con que el informe agregue números.
- Los originales de documentación oficial pueden contener personas físicas. La separación código abierto / datos restringidos es adecuada; deben añadirse filtros de revisión de salidas y un procedimiento de retirada o rectificación.

## 7. Fuentes jurídicas primarias contrastadas

- [Ley 19/2013, arts. 20 y 24 — BOE](https://www.boe.es/buscar/act.php?id=BOE-A-2013-12887). El plazo general de resolver es **un mes desde la recepción por órgano competente**, ampliable en circunstancias legales; la reclamación se regula en el art. 24.
- [Ley 39/2015, art. 30 — BOE](https://www.boe.es/buscar/act.php?id=BOE-A-2015-10565). Cómputo de meses y prórroga si el último día es inhábil.
- [LCSP 9/2017, arts. 203, 207, 237, 243, 335 y 346 — BOE](https://www.boe.es/buscar/act.php?id=BOE-A-2017-12902). El art. 207.3 exige publicar anuncios de modificación e informes; el art. 243 sitúa la certificación final en relación con la recepción real; el 346 regula comunicación de datos al Registro.
- [RD 817/2009, art. 31 — BOE](https://www.boe.es/buscar/act.php?id=BOE-A-2009-8053). El precepto está en el texto consolidado publicado; se mantiene como **pendiente de dictamen humano** su aplicación plena y coordinación con normas posteriores.

## Veredicto final

**Documento v0.4.4: publicable como *documento exploratorio de trabajo* tras corregir P2–P5 y matizar P1**, con señalización expresa de que el programa no ha sido validado con una muestra suficiente para inferir la ausencia real de información, y sin atribuir incumplimientos a ningún órgano.

**Programa de fase 0 v2.4: apto para revisión e investigación adicional, no como clasificador universal de «fin confirmado».** Los 24 nuevos positivos pueden mantenerse con la revisión humana declarada, pero no extrapolar esa precisión automáticamente a todos los años/órganos.

**Anexo D y herramientas de solicitudes: diseño prometedor, pero no listos para uso administrativo real sin corregir P6 y P7**, revisar P8–P13 y obtener supervisión jurídica/estadística de una organización usuaria. No se ha enviado ninguna solicitud, lo que permite introducir estos cambios sin efectos sobre terceros.

**No hace falta reescribir Democracia Auditable ni crear Traza Cívica.** La aportación más defendible sigue siendo el método abierto para medir qué se publica, localizar dónde aparecen datos de ejecución y documentar las preguntas y respuestas con un cauce oficial, cuando una entidad responsable lo adopte.
