# APLICAR LA INGENIERÍA DE SEGURIDAD A LA DEMOCRACIA

## Democracia Auditable: propuesta de un protocolo abierto de supervisión distribuida y verificable del poder público, asistido por inteligencia artificial

**Documento de trabajo — versión 0.4.9 (borrador crítico de distribución, pendiente de revisión humana) | 2 de noviembre de 2026**
**Estado:** borrador fundacional. Ha completado varias rondas de revisión adversarial entre modelos de IA; las tres últimas, sobre la v0.4.5, la v0.4.6 y la v0.4.7, revisaron también el código y el protocolo, y sus correcciones están en esta versión (Anexos A.10 a A.12). **No ha sido revisado todavía por juristas, estadísticos, auditores ni ingenieros humanos**; esa es la siguiente etapa, y ninguna afirmación jurídica de este texto debe usarse sin ella. Que dos modelos hayan contrastado una referencia no certifica su exactitud ni su idoneidad.
**Historial:** v0.1 preparada con ChatGPT; v0.2 revisada por Claude; v0.3 revisada por ChatGPT; v0.4 consolidada por Claude; v0.4.1 con la fe de erratas de la revisión final de ChatGPT, aplicada por Claude; v0.4.2 incorpora el primer resultado empírico de la fase 0 (§9.0 bis), cuyo estudio pasó tres rondas de revisión adversarial con ChatGPT; v0.4.3 añade §3 bis (para qué serviría) y las correcciones de precisión de una nueva revisión de ChatGPT, aplicadas por Claude; v0.4.4 corrige la cifra principal de la fase 0 (98,7 % → 97,2 %), añade las investigaciones complementarias (§9.0 ter) y el diseño de un protocolo de preguntas sobre obras (Anexo D), redactados por Claude y revisados por ChatGPT en una ronda adversarial cuyas correcciones incorpora; v0.4.5 añade una novena investigación (una coincidencia documental asociada a contratos resueltos) y su uso como criterio de prioridad del protocolo; v0.4.6 incorpora la revisión adversarial de ChatGPT de la v0.4.5: rebaja la calificación de la novena investigación, corrige los plazos del protocolo según la ley de cada comunidad, retira del repositorio las listas de obras con su órgano y corrige fallos de las herramientas; v0.4.7 incorpora la revisión adversarial de ChatGPT de la v0.4.6: corrige las ampliaciones y el plazo de los órganos de garantía, deja de calificar respuestas con fechas no verificadas y delimita qué resoluciones se citan; v0.4.8 corrige la validación del registro de protocolo tras la revisión de la v0.4.7; v0.4.9 recoge que el Proyecto de Ley Orgánica de Integridad Pública decayó al disolverse las Cortes. Los documentos de cada ronda se conservan junto a este texto.
**Origen y licencia:** documento de bases **anónimo y sin propietario**, redactado y revisado con modelos de IA a instancias de un particular que actúa solo como intermediario, no reclama autoría ni reconocimiento y no participará en ningún desarrollo posterior. Sin adscripción partidista ni organización promotora. **Intención de dedicación al dominio público (CC0 1.0)** respecto de todo contenido original sobre el que pudiera existir derecho de autor; no se conceden derechos sobre material de terceros citado. Este documento **no publica expedientes ni acusaciones**: quien en el futuro publique auditorías de casos reales siguiendo este protocolo asume la responsabilidad editorial y jurídica con su propia identidad.
**Ámbito inicial:** España, con principios potencialmente adaptables a otras democracias constitucionales.

> **Los seres humanos somos imperfectos. Las instituciones deben estar diseñadas para que nuestros errores —y nuestros posibles abusos— no se conviertan en catástrofes, y para que las advertencias fundadas no puedan ignorarse sin dejar rastro.**

---

## Nota sobre esta versión

**v0.4.9 (02/11/2026).** Corrección editorial de publicación (cambios en el Anexo A.13):
- El **Proyecto de Ley Orgánica de Integridad Pública** (121/000111), que la §8.1 presentaba en tramitación y la §8.6 como posible vía de enmienda, **decayó** al disolverse las Cortes por el Real Decreto 806/2026, de 5 de octubre, publicado y en vigor el 6 de octubre de 2026. Ahora se cita como antecedente, no como vía disponible.
- Se corrigen un enlace interno y dos menciones a un expediente concreto en la documentación del estudio.

**No cambian el método, el código, las cifras ni las limitaciones del estudio.** Sigue siendo un borrador crítico pendiente de revisión por especialistas humanos.

**v0.4.8 (02/11/2026).** Incorpora la revisión adversarial de ChatGPT de la v0.4.7 (respuesta en `revisiones/v0_4_7/respuesta_revision_v0_4_7.md`; cambios en el Anexo A.12). Son correcciones del registro del protocolo y dos detalles editoriales; **las cifras del estudio no cambian**:
- La comprobación del registro ya no se interrumpe con una fecha de ampliación mal escrita, rechaza una ampliación anterior a la recepción por el órgano y una fecha límite verificada anterior a esa recepción.
- Distingue **errores** (cronología imposible) de **avisos** (una ampliación posterior al vencimiento provisional puede ser válida si hubo una suspensión).
- Un silencio no se califica «fuera de plazo» hasta que vence la fecha verificada.
- Avisa de festivos cuyo ámbito no coincide con ninguna fila.
- Rutas internas corregidas; en el complemento autonómico, solo llevan número las resoluciones citadas como precedente.

Se añade un **documento de presentación breve**, de tres páginas, (`documento/Democracia_Auditable_resumen_v0_4_9.pdf`), que remite a este.

**v0.4.7 (02/11/2026).** Incorpora la revisión adversarial de ChatGPT de la v0.4.6, verificada punto por punto contra el código y el BOE (respuesta en `revisiones/v0_4_6/respuesta_revision_v0_4_6.md`; cambios en el Anexo A.11). Afecta solo al protocolo del Anexo D y a su documentación; **las cifras del estudio no cambian**:
- **Ampliaciones según la ley:** quince días en el País Vasco (no otro mes) y hasta la mitad del plazo en Cataluña (error que la revisión no vio y apareció al comprobar las demás leyes). Una ampliación solo cuenta si se notificó antes del vencimiento ordinario y de la respuesta.
- **Plazo de los órganos de garantía según la ley:** dos meses en Cataluña, con la mediación suspendiendo el plazo; donde no se ha localizado en un texto, seguimiento manual.
- **Ninguna respuesta se califica «en plazo» con una fecha calculada:** solo con la fecha límite que una persona verifica (recepción real, calendario del lugar, suspensiones y ampliación). Los festivos se pueden indicar por comunidad o por órgano.
- **Fuentes corregidas** en Castilla y León y en Castilla-La Mancha, y Galicia local pasa a la ley estatal (la gallega no incluye a las entidades locales). El plazo numérico no cambia.
- **Citas de resoluciones:** se citan las públicas como precedentes de un criterio jurídico; la lista de casos autonómicos clasificados ya no se publica.

El Anexo D sigue siendo un diseño para un piloto, **no apto para solicitudes reales sin revisión jurídica**.

**v0.4.6 (02/11/2026).** Incorpora la revisión adversarial de ChatGPT de la v0.4.5, verificada punto por punto contra el código, los datos y el BOE (respuesta en `revisiones/v0_4_5/respuesta_revision_v0_4_5.md`; cambios en el Anexo A.10):
- **La novena investigación se rebaja:** es una *asociación preregistrada en un corpus parcialmente expuesto al diseño*, no una validación confirmatoria. Se describe como coincidencia documental que obliga a verificar, sin trasladar sus proporciones a otras obras. Al recalcular apareció un error: son 66 órganos, no 69.
- **Los plazos del protocolo dependen de la ley aplicable:** el plazo para resolver es de 20 días hábiles en la Administración de Madrid, de Murcia y en la Junta de Andalucía, y de 30 en Extremadura; en tres comunidades se puede reclamar contra el silencio sin plazo. Las herramientas ya no calculan fechas sin un régimen verificado.
- **El repositorio deja de publicar listas de obras con su órgano.** Se publican cifras agregadas y las huellas de los ficheros por expediente, para comprobar una repetición del análisis sin publicar la lista.
- **Fallos de las herramientas corregidos:** la muestra fija, la validación del registro, el tope (ya no admite «sin tope»), un ciclo que daba por bueno un registro con errores, la reanudación tras cancelar, los festivos y la exportación (sin identificadores por defecto).
- **Lo de los órganos autonómicos se precisa:** el 58 % son solicitudes potenciales, no reclamaciones, y el recuento estricto es de 2 y 7 casos, sin desestimaciones de fondo.

El Anexo D sigue siendo un diseño para un piloto, **no apto para solicitudes reales sin revisión jurídica**.

**v0.4.5 (02/11/2026).** *(Formulación de la novena investigación corregida en la v0.4.6.)* Añade una novena investigación a la §9.0 ter: una señal que marca obras para las que el mismo órgano licitó después la «terminación» de la misma obra, lo que sugiere que el primer contrato no la terminó. En una validación preregistrada con obras de final conocido, marca el 3,7 % de los contratos resueltos frente al 0,4 % de los terminados con normalidad. Es **muy específica y poco sensible**: solo capta en torno al 4 % de las resoluciones, de modo que una obra no marcada no dice nada. El Anexo D la incorpora como criterio de prioridad opcional, con su descripción exacta y un procedimiento para refinarla. Añade también, en la §9.0 ter, lo que resuelven los órganos de garantía autonómicos. Estas adiciones **no han pasado todavía revisión adversarial** (Anexo A.9).

**v0.4.4 (02/11/2026).** Tres cambios:

- **Corrige la cifra principal de la fase 0: 1.549 de 1.593 expedientes (97,2 %)** sin indicadores de finalización o extinción detectados por el programa. Algunos órganos comunican la liquidación o la certificación final en el texto de un anuncio de modificación, un campo que la versión anterior del programa no leía (daba 1.573, 98,7 %). Los 24 casos se revisaron a mano; 22 proceden de un mismo órgano. La conclusión no cambia, y la cifra sigue siendo una métrica del clasificador en este canal, no una tasa validada de falta real de información (§9.0 bis).
- **Añade ocho investigaciones complementarias** (§9.0 ter): el anuncio de finalización por dentro, las cohortes de 2021 y 2022, la validación del clasificador, el marco jurídico, las resoluciones del Consejo de Transparencia, un registro autonómico que publica el fin, la imposibilidad de saber si una obra empezó y la publicación de las modificaciones. Dos de ellas se preregistraron.
- **Añade el diseño de un protocolo de preguntas sobre el fin de las obras** (Anexo D): reglas, volumen medido, a quién se reclama, riesgos y herramientas. Es un diseño para un piloto, **no una herramienta jurídica operativa**: no se ha enviado ninguna solicitud ni lo ha revisado un jurista.

La ronda de revisión adversarial con ChatGPT (02/11/2026) llevó a endurecer el patrón de la corrección (sin cambio en la cifra), a matizar varias formulaciones de la §9.0 ter y a corregir dos defectos de las herramientas del Anexo D antes de cualquier uso real: el cómputo de plazos y el control de duplicados (Anexo A.8).

**v0.4.3 (01/11/2026).** Añade la **§3 bis** («Para qué serviría, si funciona»): qué ganaría cada tipo de usuario, con qué condición y con qué riesgo. Incorpora además las correcciones de precisión de una revisión de ChatGPT: formulación del 98,7 % (qué mide y qué no), tipología de los casos con fin acreditado, alcance real de las revisiones, plazo legal de acceso a la información, datos verificables del repositorio y coherencia de versiones (Anexo A.7). Las cifras no cambian.

**v0.4.2 (30/10/2026; texto histórico, cifras superadas por la v0.4.4).** No reescribe el documento: añade el **primer resultado de la fase 0** (§9.0 bis). Se midió, con un programa abierto y los datos abiertos oficiales, qué consta de la ejecución de 1.651 expedientes de obras adjudicados en 2023. Hay tres consecuencias para la §8.6:

- En 1.573 de los 1.593 expedientes cuyo **fin teórico estimado** era anterior al 29/10/2026 (98,7 %), el programa no identificó **indicadores de finalización o extinción** en los campos examinados de la sindicación de la PLACSP. No permite concluir que las obras no hayan terminado, que no exista documentación por otras vías ni que se haya incumplido la ley (§9.0 bis).
- La PLACSP **ya dispone** de un «Anuncio de Finalización de Contrato» estructurado, que en esa población aparece en 8 de 1.651 expedientes.
- Al menos un registro autonómico (el vasco) publica, contrato a contrato, el estado, la fecha y el importe de finalización.

Es una medición exploratoria. No prueba incumplimientos ni que falten documentos. El texto que sigue a este párrafo es el de la v0.4.1, con los cambios puntuales del Anexo A.6.

**v0.4.1.**
La v0.4 consolida las tres rondas anteriores y añade cinco cosas:

1. **Un cauce legal que ya existe y nadie había usado:** el **derecho de petición** (art. 29 de la Constitución; Ley Orgánica 4/2001). Una petición admitida, dirigida a la autoridad competente y sin procedimiento específico aplicable, obliga a esa autoridad a contestar motivadamente en tres meses, con tutela judicial reforzada si no lo hace. No es un cauce universal ni sustituye al acceso a la información (§6.3), pero el «deber de respuesta» que las versiones anteriores proponían legislar ya existe para ese supuesto. Lo que falta es usarlo bien, publicar las respuestas y medir su cumplimiento (§6.3, §8.2).
2. **Una apuesta explícita y falsable** sobre dónde está el fallo (§1), en lugar de una afirmación sin pruebas (v0.2) o de ninguna apuesta (v0.3).
3. **Un prototipo mínimo sin IA que arranca en una semana** (§9.0; las tasas de respuesta llegan al vencer los plazos legales), y una **propuesta normativa concreta** sobre publicación de datos de ejecución contractual (§8.6), cuyo encaje en la ley que se tramita ahora es una oportunidad a verificar, no una vía confirmada.
4. **Parámetros provisionales con números** (Anexo C), marcados como sustituibles en el preregistro. Un documento sin números no puede ser refutado ni adoptado.
5. **Una tabla de referencias con estado de verificación por revisor** (quién comprobó qué, cuándo y contra qué fuente), en lugar de jerarquías de «verificadas» y «heredadas».

Se mantienen de la v0.3: los ejes C/I/U, la entidad editora identificable, las tres pruebas separadas, la línea base sin IA y la regla de retirada de la IA si no supera esa línea base. La v0.4.1 corrige, tras la revisión final: el alcance del derecho de petición (no es un cauce universal; §6.3), el alcance de la transición del art. 50 del Reglamento de IA (§8.5), la descripción de lo que ya se publica y lo que ya se comunica al Registro de Contratos (§8.6), el calendario real del prototipo (§9.0), el desdoblamiento de la apuesta en dos hipótesis medibles (§1) y el tratamiento de las urgencias (§6.4). El registro completo de cambios está en el Anexo A.

### Nota para las organizaciones destinatarias

Este texto se distribuye como **punto de partida**, no como proyecto en marcha. Detrás no hay equipo, financiación, marca ni persona que vaya a reclamar nada. Quien lo reciba puede adoptarlo entero, tomar una sola idea o refutarlo públicamente; las tres cosas cumplen su propósito. Conviene saber tres cosas antes de leerlo:

- **Ha sido redactado por modelos de IA** (ChatGPT y Claude, en rondas sucesivas de crítica mutua) a partir de las indicaciones de un particular que actúa como intermediario, sin reclamar autoría ni responsabilidad futura. No ha intervenido ningún jurista. Los modelos comparten datos de entrenamiento y sesgos; que coincidan no prueba nada. Ninguna afirmación jurídica debe aceptarse sin revisión por juristas.
- **Las referencias se han contrastado con fuentes primarias** (BOE, EUR-Lex, BOCG, páginas oficiales) por al menos uno de los dos modelos, y la tabla final dice cuál y cuándo. Una fuente acredita que una norma existe, no que el proyecto funcione.
- **No hay continuidad garantizada:** no existe equipo, entidad responsable ni financiación, y los modelos de IA no conservan memoria ni seguirán el proyecto. Todo lo que el documento sabe está en el documento.

Si solo pueden leer una parte, lean **§3 bis** (para qué serviría y a quién), **§9.0** (qué se puede empezar en una semana) y **§8.6** (qué cambio legal pequeño tendría más efecto, si la fase 0 confirma la laguna).

---

## Resumen ejecutivo

La democracia dispone de instituciones para elegir, sustituir y controlar a quienes gobiernan. La supervisión concreta de contratos, riesgos técnicos y obligaciones públicas puede estar fragmentada, llegar tarde o ser difícil de reconstruir para la ciudadanía. No sabemos todavía si la causa dominante es falta de información, de detección, de respuesta o de consecuencias: averiguarlo es la fase 0 de este proyecto, y el documento apuesta —de forma explícita y refutable— por que el fallo más frecuente es que las advertencias fundadas no obtienen respuesta documentada.

Proponemos aplicar principios de ingeniería de seguridad: **defensa en profundidad, independencia medida, análisis de fallo de causa común, trazabilidad, fallo seguro y aprendizaje de incidentes**. La inteligencia artificial puede ayudar a extraer y relacionar documentación, pero **no certifica hechos, no evalúa personas y no decide**; y si no demuestra valor frente a métodos sencillos, se retira.

El resultado buscado es un **protocolo abierto de reconstrucción verificable de decisiones públicas**: cada afirmación anclada a su documento; cada comunicación a una administración registrada con su cauce, plazo legal, respuesta o silencio; cada error del propio sistema publicado y analizado. Buena parte de esto puede hacerse hoy con datos abiertos, con el derecho de acceso a la información y con el derecho de petición. La propuesta normativa que se deriva es pequeña: publicar por contrato y en formato reutilizable los datos de **ejecución** que las administraciones ya recogen, y publicar las respuestas a las peticiones y solicitudes en materia de contratación.

Lo que se ganaría, si funciona, es sencillo de enunciar: **una pregunta a la Administración se haría una vez y su resultado, respuesta o silencio, quedaría a disposición de cualquiera.** Lo aprovecharían la ciudadanía y los periodistas, las organizaciones cívicas, la oposición, quien gobierna, el personal técnico de las administraciones y los propios órganos de control, cada uno con sus condiciones y sus riesgos (§3 bis). No se ha medido todavía; es lo que la fase 0 y el piloto deben comprobar.

**Pregunta fundacional:** ¿qué combinación de controles independientes permite detectar y contener errores y abusos del poder sin crear un nuevo poder arbitrario o tecnocrático, y sin que el propio control se convierta en ruido, burocracia o arma partidista?

---

## 1. El problema que pretendemos investigar

Los responsables públicos deciden con información incompleta, presión de tiempo, incentivos dispares y límites presupuestarios. Pueden equivocarse, desatender advertencias o actuar deshonestamente. La cuestión de diseño no es suponer que todos son iguales, sino **no depender de que ninguno sea infalible**.

Distinguimos **seis fallos observables**, cuya prevalencia no conocemos:

1. **Información:** documentos no públicos, incompletos, incompatibles o incorrectos.
2. **Detección:** el indicio existía y nadie lo identificó a tiempo.
3. **Transmisión:** el hallazgo se detectó pero no llegó al órgano competente, o no quedó rastro.
4. **Respuesta:** ante una advertencia recibida no hay respuesta suficiente, en los casos en que la ley exige darla.
5. **Corrección:** hubo respuesta, pero la medida fue insuficiente, tardía o no se ejecutó.
6. **Responsabilidad y aprendizaje:** no se revisaron decisiones ni se incorporaron lecciones.

No toda advertencia merece actuación; no todo silencio viola un deber; no toda actuación ineficaz es ilícita. Existen deberes jurídicos distintos de resolver o responder en ámbitos delimitados: procedimientos administrativos (Ley 39/2015, art. 21), solicitudes de acceso a información (Ley 19/2013, art. 20), recomendaciones del Defensor del Pueblo (LO 3/1981, art. 30) y **peticiones ciudadanas** (LO 4/2001, art. 11). La fase 0 mapeará qué obligación corresponde a cada tipo de comunicación y si se cumplió.

### Apuesta explícita (falsable)

La apuesta se formula en dos hipótesis separadas, porque no pueden medirse con la misma muestra:

- **H0a (respuesta).** En una cohorte de comunicaciones fundadas, **admisibles y correctamente encauzadas**, con seguimiento completo hasta el vencimiento del plazo legal, apostamos a que la mayoría **no obtiene respuesta motivada en plazo**.
- **H0b (detección).** En una muestra independiente de contratos **auditada exhaustivamente** por humanos, apostamos a que la mayoría de las discrepancias documentales relevantes que encuentre esa auditoría **no habían sido señaladas por nadie** en fuentes públicas.

Ninguna de las dos permite por sí sola afirmar qué fallo «domina»: el denominador de lo que nadie detectó es invisible por diseño, y una muestra seleccionada por discrepancias ya detectadas no sirve para medir detección. La fase 0 solo podrá comparar ambas si define de antemano poblaciones de inferencia y reglas de muestreo distintas para cada una. **Si H0a resulta falsa** (las comunicaciones se responden), el proyecto se reorienta hacia la publicidad de datos (§8.6) o hacia las consecuencias; **si H0b resulta falsa** (lo relevante ya está señalado), la capa de detección sobra y queda solo la de seguimiento. Esta apuesta no es una conclusión: es lo que convierte la fase 0 en un experimento y no en un informe.

**Hipótesis comprobable:** un protocolo abierto de reconstrucción de expedientes podría acelerar el hallazgo de inconsistencias, hacer visible la cadena de avisos y respuestas, y mejorar la rendición de cuentas. Ni su utilidad ni su efecto causal están probados. Debe medirse contra alternativas más sencillas.

---

## 2. Inspiración: tolerancia a fallos, no fe tecnológica

El antecedente conceptual es la ingeniería de sistemas críticos: redundancia con análisis de causa común, separación de funciones, diagnósticos independientes, límites de operación segura, registro e investigación de incidentes, y la idea —desarrollada en el análisis de seguridad de sistemas sociotécnicos (Leveson, 2011)— de que la seguridad es un problema de **estructura de control**: no basta con componentes fiables; hace falta que cada nivel (operador, gestor, regulador, legislador) reciba la información que necesita y tenga capacidad real de actuar. También aprendemos de los **accidentes normales** (Perrow, 1984): añadir capas de supervisión a un sistema complejo y fuertemente acoplado puede crear nuevos modos de fallo. Un sistema de supervisión mal diseñado es un riesgo más.

De los protocolos abiertos tomamos tres ideas y rechazamos una:

- **Tomamos:** reglas públicas y auditables; verificación independiente sin pedir permiso; ausencia de llave maestra.
- **Rechazamos:** la pretensión de «confianza cero». La validez de una transacción en Bitcoin es mecánicamente decidible dentro de un mundo cerrado, y su seguridad es económica; nada de eso sirve para verificar hechos del mundo real. Evaluar si una obra pública es segura o si un contrato se ejecutó bien exige inspección, juicio y, a menudo, datos que no existen. Y nadie paga nativamente la verificación. La analogía es **parcial**: útil para la gobernanza del protocolo (registro de solo adición, copias firmadas en entidades distintas, gestión distribuida de cambios), inútil para la epistemología de los hechos. No se propone cadena de bloques ni token; antes de añadirlos habría que justificar qué ataque concreto resuelven mejor que sistemas convencionales.

### Principios de diseño

1. **Sin punto único de fallo.** Ninguna persona, modelo, proveedor u organismo controla a la vez datos, criterios, resolución de alertas y apelación.
2. **Defensa en profundidad con análisis de causa común.** Varias capas detectan, verifican y corrigen; la independencia entre ellas se **mide**, no se presume.
3. **Verificabilidad anclada.** Una afirmación publicada como hecho enlaza a un documento identificado (huella criptográfica, página, cita). Lo que no puede anclarse no se publica como hecho.
4. **Los modelos de IA no certifican.** Extraen, comparan, redactan y proponen. Una comprobación determinista o una verificación humana pueden establecer **qué consta** en la fuente; ninguna certifica por sí sola que el mundo corresponda a lo escrito.
5. **Fallo seguro.** En incertidumbre, el sistema se abstiene de imputar, y la abstención se registra.
6. **Actos, no personas.** El objeto del sistema son expedientes, contratos, decisiones y entidades. No se perfila, puntúa ni evalúa a personas físicas.
7. **Derechos y recursos.** Notificación previa a los afectados, contradicción, rectificación visible, privacidad, proporcionalidad y control judicial.
8. **Control del controlador.** El sistema publica sus errores, sus financiadores, sus métricas y sus post-mortems, y acepta auditorías externas que no elige.
9. **Reproducibilidad proporcional.** Se conservan evidencias y decisiones para reproducir la comprobación documental. La reejecución exacta del cálculo requiere código, datos autorizados, modelos, dependencias y entorno; si un proveedor desaparece, se declara la limitación.
10. **Prescindibilidad de la tecnología.** Si la IA no supera a la alternativa determinista y manual en exactitud, coste y seguridad, se retira, y el protocolo conserva su razón de ser.

---

## 3. Alcance: qué pretendemos y qué no

**Pretendemos:**
- Producir expedientes verificables sobre actuaciones públicas documentadas.
- Registrar comunicaciones a administraciones (peticiones, solicitudes de acceso, remisiones a órganos de control) con su cauce, plazo legal, respuesta o silencio.
- Medir y publicar la capacidad de respuesta institucional.
- Servir de control externo y reproducible de los organismos de supervisión, incluidos los sistemas de analítica de datos que use el propio Estado.
- Proponer, solo con evidencia, reformas acotadas: publicidad estructurada de la ejecución contractual y de las respuestas a peticiones y solicitudes.

**No pretendemos:**
- Sustituir a jueces, interventores, auditores, parlamentos o electores.
- Crear una potestad de bloqueo, suspensión o veto vinculada a alertas algorítmicas.
- Evaluar, puntuar o predecir la conducta de personas físicas.
- Publicar acusaciones. Publicamos discrepancias documentales y preguntas, con su grado de soporte.
- Evaluar causalmente los efectos de políticas públicas con modelos de lenguaje.
- Medir «daño evitado». No tenemos contrafactual; quien lo afirme estará extrapolando.

---

## 3 bis. Para qué serviría, si funciona

Las secciones 4 a 9 explican cómo funcionaría el protocolo y qué límites tiene. Esta explica antes qué ganaría cada cual si llegara a funcionar. Son **usos posibles, no resultados demostrados**: dependen de que el registro exista, se mantenga y aplique las mismas reglas a todos (§7), y ninguno se ha medido todavía (§9.5).

### Qué cambia: una pregunta se hace una vez

Hoy, quien quiere saber si una obra pública terminó, cuándo y por cuánto tiene que abrir el expediente en la Plataforma de Contratación del Sector Público y revisar sus documentos uno a uno. En la primera medición (§9.0 bis), un programa que buscaba indicadores de finalización en los datos abiertos de esa plataforma no los encontró en la gran mayoría de las obras con el plazo teórico vencido. Si no encuentra el dato en las fuentes públicas consultadas, puede necesitar una solicitud de acceso a la información pública, que exige identificarse, y esperar su resolución dentro del plazo legal (con carácter general, un mes, ampliable en los supuestos previstos). Si otra persona hizo antes la misma pregunta, no lo sabe; si la respuesta no llegó, ese silencio no queda en ningún sitio público.

Con el protocolo, ese expediente tendría una ficha pública con lo que consta, lo que falta, quién preguntó por lo que falta, por qué cauce, con qué plazo legal, y la respuesta recibida o su ausencia a fecha de consulta (§5.5, §6.2). **La pregunta se hace una vez y su resultado, respuesta o silencio, queda disponible para cualquiera.** Lo que hoy está disperso se vuelve consultable, y lo que hoy es una anécdota («a mí no me contestaron») se convierte en un dato que se puede sumar y comparar («de N comunicaciones admisibles sobre contratación, X recibieron respuesta motivada en plazo»).

### Quién podría usarlo y para qué

| Quién | Qué podría hacer que hoy le cuesta mucho o no puede | Condición | Riesgo |
|---|---|---|---|
| **Ciudadanía y periodistas** | Consultar en un solo lugar el estado documentado de un contrato y el historial de lo preguntado sobre él; reutilizar preguntas ya hechas en lugar de repetirlas | Que las fichas estén al día y digan su fecha de consulta | Leer «no consta» como «no existe» o «no se hizo» (§6.2) |
| **Organizaciones cívicas** | Decidir con criterios escritos qué seguir, escalar por los cauces existentes cuando vence un plazo (§6.3) y dejar constancia de todo el proceso | Actuar como entidad editora identificable (§5.4) y sostener el esfuerzo | Agotamiento del voluntariado; sesgo hacia los casos mediáticos |
| **Oposición y grupos parlamentarios** | Basar preguntas y mociones de control en hechos registrados y verificables | Que el registro aplique las mismas reglas gobierne quien gobierne | Uso selectivo: citar solo lo que conviene (§11.8) |
| **Quien gobierna** | Ver qué contratos acumulan retrasos o resoluciones (rupturas anticipadas del contrato) y qué servicios no responden en plazo; acreditar mejoras con datos que no ha elaborado él mismo | Aceptar ser medido con las mismas reglas que los demás | Presentar como éxito de gestión lo que solo es una mejora de la medición |
| **Personal técnico de las administraciones** | Mostrar con datos cuándo un retraso se debe a falta de medios (volumen de peticiones frente a personal disponible) y no a desidia | Que el registro distinga capacidad de voluntad | Que la cifra se use contra el servicio en lugar de para dotarlo |
| **Órganos de control y fiscalización** | Disponer de un indicador externo y reproducible de cobertura y de respuesta que complemente los suyos, sin depender del órgano controlado | Que el método sea abierto y replicable por terceros (§10, fase 4) | Duplicar lo que ya hacen; debe comprobarse antes (§8.1) |

Ninguno de estos usos exige potestades nuevas: todos se apoyan en datos abiertos, en el derecho de acceso a la información y en el derecho de petición, que ya existen (§6.3, §10).

### Por qué también es útil a quien es medido

«No damos abasto» es hoy una explicación que nadie puede comprobar. Con un registro así pasa a ser una hipótesis medible: si los retrasos se concentran donde el volumen de peticiones es mayor, el remedio no es reprochar sino dotar medios o **publicar de oficio** lo que se pregunta una y otra vez, lo que además reduce el número de peticiones. El protocolo trata «responden, pero tarde por falta de medios» como un resultado útil, no como un fracaso: es una de las formas en que la apuesta H0a puede resultar falsa (§1).

### Lo que no conseguiría

- **No dice quién tiene razón.** Registra hechos («enviada», «plazo vencido», «respuesta recibida»), no culpas (§6.1 bis, §6.2).
- **No sustituye** a jueces, interventores, auditores ni autoridades; hace visible si los cauces que ya existen funcionan (§3).
- **No prueba** que una falta de respuesta causara un daño concreto, ni mide «daño evitado» (§3).
- **Solo contiene lo que alguien haya preguntado o publicado.** Amplía mucho lo visible, pero no lo cubre todo.
- **No sirve para emergencias.** Un riesgo grave e inminente va directamente a la autoridad competente, sin esperar plazos (§6.4).

---

## 4. Modelo de amenazas

Un sistema que fiscaliza al poder debe partir de que será atacado, capturado o instrumentalizado. Los adversarios no son solo quienes quieren silenciarlo; son también quienes quieren usarlo.

| Adversario | Capacidades | Ataque probable | Contramedida | Riesgo residual |
|---|---|---|---|---|
| Gobierno o administración auditada | Controla publicación de datos, nombramientos, subvenciones, acceso | Degradar o retrasar datos; no responder; financiar para condicionar; deslegitimar | Medir y publicar cobertura y respuesta; usar cauces con deber legal de respuesta (petición, acceso); carta de financiación; multiplicidad de fuentes | Alto mientras el incumplimiento de plazos no tenga consecuencia práctica |
| Oposición política y actores partidistas | Amplificación; presión sobre la agenda | Seleccionar casos; presentar discrepancias de bajo soporte como pruebas; forzar publicaciones prematuras | Universo y muestra preregistrados y ciegos al signo político; grados de soporte visibles; embargo hasta contradicción; prohibición de rankings | Medio-alto |
| Adjudicatarios y grupos de interés | Recursos legales y económicos; conocimiento del sector | Demandas por honor; cumplir sobre el papel; infiltración | Canon de veracidad y diligencia; reglas públicas con conjuntos de prueba reservados bajo custodia externa; incompatibilidades | Medio |
| Medios y redes sociales | Amplificación sin matices | Convertir una discrepancia C1 en acusación; ignorar rectificaciones | Cada cita lleva su grado; rectificaciones con la misma visibilidad; sin nombres de personas físicas | Alto: no controlable |
| Proveedores de modelos de IA | Capacidades, precios, versiones | Cambios silenciosos; retirada de modelos; condiciones de uso | Pesos abiertos cuando sea posible; versiones congeladas; marcado de no reproducibilidad; métodos no generativos como respaldo | Medio |
| Atacantes técnicos | Inyección de instrucciones en documentos, envenenamiento, intrusión | Documentos con instrucciones ocultas; PDF falsificados; feeds manipulados; documentos oficiales pero materialmente engañosos | Toda fuente es no confiable; aislamiento y permisos mínimos; verificación de origen y huellas; corroboración con fuentes independientes; prohibición de lenguaje acusatorio en salidas automáticas | Medio |
| Los propios operadores | Acceso privilegiado; incentivo reputacional | Alterar expedientes, borrar discrepancias, seleccionar casos, filtrar borradores | Registro de solo adición con firmas; llaves múltiples; separación de roles; auditoría externa no elegida; control de accesos y auditoría de lecturas; post-mortems | Medio: la captura más difícil de ver desde dentro |
| Dinámica del propio sistema | — | Fatiga por alarmas; administración defensiva; falsos positivos acumulados; irrelevancia | Umbrales estrictos; métrica negativa de carga inducida; criterio de parada; publicación de resultados negativos | Alto en los primeros años |

El modelo se revisa en cada versión y se somete a un equipo rojo con presupuesto propio antes de cualquier publicación de expedientes.

---

## 5. Arquitectura funcional

Se describe un **pipeline de evidencia** en el que los modelos generativos ocupan un lugar acotado y prescindible.

### 5.1 Capa A — Fuentes y cadena de custodia

Conectores que recopilan exclusivamente datos obtenidos de modo legítimo: boletines oficiales, perfiles de contratante y sindicación de la Plataforma de Contratación del Sector Público, presupuestos y liquidaciones, informes de fiscalización publicados, respuestas a peticiones y solicitudes de acceso, datos abiertos. Cada documento conserva procedencia, fecha de obtención, versión, huella criptográfica y transformaciones. Se distinguen siempre el **original**, la **extracción estructurada** y el **resumen generado**.

Una huella criptográfica prueba que el archivo no ha cambiado respecto de otra copia, **no** que su contenido, su emisor o su interpretación sean correctos. No se asume que «dato oficial» equivale a «dato correcto». El sistema mide y publica **cobertura** (qué debería constar y no consta) y **contradicciones** entre fuentes. No se recopilan datos personales innecesarios; los nombres de personas físicas presentes en documentos públicos no se extraen a campos estructurados.

### 5.2 Capa B — Extracción determinista y asistida

- **Reglas deterministas** sobre datos estructurados (XML/ATOM/JSON): fechas, importes, plazos, porcentajes de modificación, presencia o ausencia de documentos legalmente exigibles.
- **Extracción asistida por modelos** sobre documentos no estructurados: los modelos proponen valores con anclaje (documento, página, fragmento) y confianza; una muestra se valida por humanos de forma continua; la tasa de error por tipo de campo se publica.
- **Fallo de causa común:** al menos dos métodos de naturaleza distinta (un modelo generativo y un extractor determinista o clásico, o dos modelos de pesos abiertos de linajes distintos), midiendo la correlación de sus errores sobre el conjunto de referencia. Una segunda lectura del mismo texto mal extraído no es independencia: el segundo método debe partir de otra representación o fuente. Un desacuerdo no se resuelve por mayoría: se marca y va a validación humana.

### 5.3 Capa C — Funciones analíticas separadas

Roles que pueden desempeñar personas, reglas o modelos, siempre con anclaje:

- **Documental:** concordancia entre documentos, hitos, importes, plazos.
- **Económico-presupuestaria:** compromisos, pagos, costes, con supuestos explícitos.
- **Técnico-sectorial:** requisitos normativos y señales de riesgo; **requiere expertos humanos acreditados por sector**; los modelos solo preparan material.
- **Jurídica:** obligaciones aplicables y cauces disponibles; nunca imputación.
- **Contradictora:** intenta refutar, busca documentos omitidos, propone explicaciones alternativas; incluye revisión humana obligatoria, porque un modelo contradictor es vulnerable a los mismos documentos manipulados que los demás.

Los roles no votan. Aportan argumentos, referencias y límites de confianza. Las discrepancias se publican.

### 5.4 Capa D — Graduación y verificación humana

Un comité editor, perteneciente a una entidad identificable, asigna por separado **calidad del soporte, impacto y urgencia** (§6) y decide la divulgación conforme a reglas escritas. Las firmas humanas delimitan **responsabilidad editorial, no prueba de verdad**. Los ítems urgentes siguen un cauce propio (§6.4).

### 5.5 Capa E — Registro público, comunicaciones y recurso

Cada expediente contiene: afirmaciones con sus tres ejes, discrepancias, réplicas, decisiones del comité, comunicaciones enviadas (a quién, cuándo, por qué cauce, con qué plazo legal), respuestas localizadas o su ausencia **a fecha de consulta**, rectificaciones y revisiones. El registro de auditoría es **de solo adición**; una publicación puede retirarse del acceso público para prevenir daño o cumplir la ley, y la retirada y sus motivos se documentan. No se garantiza inmutabilidad absoluta. Las publicaciones protegen datos personales, secretos legalmente protegidos y seguridad operativa. Toda persona u organismo afectado dispone de cauce de rectificación con la misma prominencia que la publicación original.

### 5.6 Capa F — Análisis de incidentes del propio sistema

Todo falso positivo publicado, toda rectificación material y todo fallo de seguridad activa una revisión; se publica un post-mortem cuando no divulgue datos protegidos ni facilite ataques: qué falló, por qué, qué cambia. Esta capa distingue un sistema de supervisión de una máquina de opinión.

---

## 6. Evidencia, impacto, urgencia y respuesta

### 6.1 Tres ejes independientes, sin puntuación total

| Eje | Categorías | Qué significa |
|---|---|---|
| **C — Calidad del soporte** | C0 sin soporte suficiente · C1 observación anclada · C2 discrepancia reproducible entre fuentes o con la norma · C3 hallazgo corroborado por fuentes independientes o revisión experta | Soporte **de la proposición concreta**; nunca certeza de irregularidad ni de causalidad |
| **I — Impacto potencial** | I0 administrativo menor · I1 económico u operativo limitado · I2 material relevante · I3 posible amenaza grave a derechos, seguridad o fondos | Severidad potencial, no infracción demostrada |
| **U — Urgencia** | U0 rutinario · U1 plazo identificable · U2 verificación acelerada · U3 posible riesgo grave e inminente | Tiempo disponible para actuar; puede ser alto aunque C sea bajo |

Ejemplos: una fecha de adjudicación confirmada es C3-I0-U0; una comunicación inicial sobre un peligro inminente puede ser C1-I3-U3, y exige **derivación urgente para comprobarla**, no darla por cierta ni hacerla viral. Los tres ejes no se suman ni producen rankings de organismos, personas o partidos.

### 6.1 bis Reglas mínimas de publicación

| Situación | Qué puede publicarse | Requisitos | Qué no puede afirmarse |
|---|---|---|---|
| C0 | Solo estado de cobertura («no consta X») | Ninguno adicional | Nada sobre la entidad |
| C1, cualquier I | La observación con su anclaje | Validación por regla o humano | Que exista irregularidad |
| C2, I0–I1 | La discrepancia, ambas fuentes, explicaciones alternativas | Dos firmas; notificación con plazo de réplica (por defecto 15 días hábiles, ampliable); réplica publicada íntegra | Que exista infracción |
| C2–C3, I2–I3 | Lo anterior más contexto normativo | Lo anterior más revisión experta y jurídica; remisión al órgano competente **antes** de publicar | Culpabilidad, intencionalidad, responsabilidad personal |
| Cualquier C, U3 | Nada hasta que la autoridad haya podido actuar | Cauce de urgencia (§6.4) | — |
| Personas físicas | Nunca en campos estructurados ni resúmenes | — | — |

«Hecho comprobado» se predica solo de **lo comprobado** («el contrato consta fechado el X»), nunca de una conclusión global.

### 6.2 Estados de una comunicación

No se usará la etiqueta «advertencia ignorada». Se publican estados verificables: «enviada por [cauce] el [fecha], plazo legal [n] según [norma]», «acuse recibido», «respuesta recibida el [fecha]» (con el texto, si es publicable), «inadmitida con motivación», «sin respuesta localizada a fecha X», «plazo legal vencido según [fundamento]». La falta de respuesta pública no implica que la entidad no haya actuado por canales reservados, y así se dice.

### 6.3 De la comunicación a la actuación: cauces que ya existen

**Nivel A — Evidencia pública.** Expediente verificable, sin efectos jurídicos.

**Nivel B — Cauces con deber legal de respuesta.** Toda comunicación se **clasifica por finalidad antes de elegir el cauce**; no se presume que cualquier discrepancia C2+ sea una petición admisible.

- **(a) Solicitud documental** —obtener un documento que debería existir y no consta—: **acceso a la información pública** (Ley 19/2013) o el procedimiento específico que corresponda. Plazo de un mes con carácter general, ampliable (algunas leyes autonómicas fijan otros: Anexo D.1); reclamación ante el órgano de garantía competente (el Consejo de Transparencia o el autonómico).
- **(b) Comunicación de riesgo o de indicios de infracción**: el **canal sectorial legalmente competente**, con su régimen propio y, cuando proceda, el de urgencia (§6.4): OIReScon, IGAE y órganos de control interno, órganos de control externo, CNMC (indicios de colusión; arts. 132.3 y 150.1 LCSP), Autoridad Independiente de Protección del Informante en los supuestos de la Ley 2/2023, Defensor del Pueblo (cuyas recomendaciones obligan a responder en un mes, LO 3/1981, art. 30), Fiscalía.
- **(c) Petición de actuación general** dentro de las competencias del destinatario, **solo cuando no exista un cauce específico aplicable**: **derecho de petición** (art. 29 CE; LO 4/2001). La autoridad debe **contestar y notificar en tres meses** (art. 11.1), recogiendo los términos en que la petición se ha tomado en consideración **y los motivos** (art. 11.3); la inadmisión debe ser motivada y notificarse en 45 días hábiles (art. 9); la omisión de respuesta o una respuesta sin los requisitos mínimos es impugnable por el **procedimiento de protección de derechos fundamentales** (art. 12). La petición no da derecho a obtener lo pedido; es inadmisible cuando su objeto tenga un procedimiento específico o esté sometido a un procedimiento en curso (arts. 3 y 8); exige peticionario identificado, por lo que la firma la entidad editora. No debe forzarse este cauce para generar una tasa artificial de inadmisiones.

El registro anota, para cada comunicación, la finalidad, el cauce elegido y por qué, de modo que la **admisibilidad y la elección correcta del cauce** se midan antes que la calidad de las respuestas; de lo contrario el indicador principal sería un artefacto del protocolo.

**Nivel C — Medidas por autoridad competente.** Jueces, reguladores y autoridades administrativas adoptan, motivan y revisan medidas cautelares **conforme a su legislación**. No hay veto automatizado ni potestad nueva.

Ninguna salida del sistema produce efectos jurídicos por sí misma. Quien decide sigue siendo quien la ley dice que decide; el objetivo es que decida **informado, en plazo y dejando constancia**, y que el incumplimiento de un deber de respuesta ya existente sea visible y, cuando proceda, impugnable.

### 6.4 Cauce de urgencia (I3/U3)

El protocolo **no es un sistema de alerta de emergencias** y no debe presentarse como tal. Si pese a ello un ítem queda marcado I3/U3 por una regla, un modelo o un revisor, **sale del pipeline de inmediato** y se escala sin demora a una persona de guardia identificada, que decide si remitirlo por los **canales de urgencia que la autoridad sectorial competente ya tiene** y deja constancia de fecha, canal y acuse. El plazo de 24 horas del Anexo C es el máximo para **documentar y revisar el encaminamiento**, no un tiempo de reacción admisible ante un riesgo para personas: la reacción es inmediata o el protocolo no debe recibir ese tipo de señales. Quien opere el protocolo debe garantizar disponibilidad organizativa y probar el circuito antes de usarlo. Nada se publica hasta que la autoridad haya podido actuar; la publicación posterior describe el proceso, no el contenido sensible. El algoritmo puede **avisar a una persona**; nunca envía nada por sí mismo ni formula acusaciones. Una filtración se trata como incidente de seguridad.

### 6.5 Control de daños del propio sistema

Retirada temporal motivada de publicaciones materialmente erróneas; registro de la actuación; derecho de impugnación; notificación a terceros receptores cuando sea practicable; plan de incidentes; evaluación del daño causado. Prohibida la generación automática de acusaciones de delito o de calificaciones de probidad de personas.

---

## 7. Gobernanza, responsabilidad y financiación

### 7.1 Separar iniciador, editor, analista, verificador y auditor

Este documento puede difundirse sin revelar a quien impulsó su redacción, igual que un estándar técnico no responde de los productos que lo implementan. **Una plataforma que publique expedientes reales no puede descansar en una autoría anónima**: necesita una entidad responsable con personalidad jurídica, contacto de rectificación, cobertura de responsabilidad, política de seguridad y órgano de revisión independiente. Esa entidad será la organización que adopte el protocolo; quien inició el borrador no la dirige ni figura en ella.

Modelo institucional deseable: **red federada** con roles incompatibles cuando proceda (custodios de datos, extractores, verificadores, comité de publicación, consejo de control independiente). Las decisiones editoriales requieren varias personas responsables, pero las firmas **no certifican infalibilidad**. Protocolo y criterios abiertos; evidencias con datos protegidos en repositorios de acceso limitado con registro de accesos. **La reproducibilidad pública no justifica difundir datos sensibles.**

**Separación de poderes interna:** nadie puede seleccionar la muestra, aprobar un caso, redactar su publicación, tramitar el recurso y juzgar su propia actuación sin control de otro rol. Las objeciones de revisores minoritarios quedan documentadas y, cuando sea posible, se publican como votos particulares.

### 7.2 Prevención de captura y participación simétrica

- Publicar el **universo de expedientes elegibles**, exclusiones, criterios y semilla reproducible antes de conocer hallazgos.
- Prohibir investigaciones a petición de partidos; reglas editoriales iguales para todos los expedientes; ventanas de embargo iguales.
- No construir rankings de partidos o autoridades a partir de muestras no representativas, ni afirmaciones agregadas sobre «quién es más corrupto»: el piloto no tiene diseño causal para ello.
- Publicar también expedientes sin incidencias, abstenciones, falsos positivos y limitaciones de cobertura.
- Separar publicación, comunicación social y actuaciones jurídicas; evitar uso selectivo en campañas electorales.
- Trazabilidad de quién propuso cada expediente y quién lo autorizó.
- Auditoría externa no designada por el equipo operativo.

### 7.3 Carta de financiación provisional

Donaciones pequeñas (volatilidad, campañas coordinadas), fundaciones (agenda del donante), universidades (dependencia de convocatorias), fondos públicos competitivos (condicionamiento, cofinanciación), convenios con administraciones (captura, autocensura), servicios a terceros (cliente convertido en prioridad), aportaciones técnicas en especie (dependencia de proveedor): cada fuente tiene su riesgo y ninguna es inocua. Reglas: publicar importes y financiadores dentro de los límites de protección de donantes; cuentas auditables; reserva de operación; ningún financiador por encima de un porcentaje máximo (parámetro provisional en el Anexo C); prohibición de fondos de entidades con contratos en la muestra y de partidos; quien tenga contratos en la muestra o participe en partidos no controla casos ni resultados; incompatibilidad de verificadores con cargos públicos electos o de confianza durante y hasta dos años después.

### 7.4 Coste y salida ordenada

Antes de constituir una institución permanente, demostrar valor frente a la alternativa sin IA. Medir coste total y carga sobre entidades auditadas. Prever insolvencia, traslado de custodia, revocación de claves, informe final y preservación legal de rectificaciones. **La propia organización debe poder desaparecer sin destruir evidencias.**

---

## 8. Encaje jurídico preliminar: España y Unión Europea

**Esta sección distingue texto legal comprobado, antecedentes y propuestas. Requiere revisión de juristas antes de presentarse como dictamen.** El estado de verificación de cada fuente está en la tabla final.

### 8.1 Instituciones existentes y principio de no duplicación

España dispone de órganos cuya función se solapa con partes de esta propuesta, y el proyecto no pretende sustituirlos sino hacerlos verificables desde fuera:

- **Contratación:** la Oficina Independiente de Regulación y Supervisión de la Contratación (OIReScon, art. 332 LCSP) publica un Informe Anual de Supervisión con módulos específicos sobre prácticas colusorias y sobre prevención de la corrupción, y explota datos de la PLACSP. La IGAE y los órganos de control externo (Tribunal de Cuentas y órganos autonómicos) ejercen el control económico-financiero. Los tribunales administrativos de recursos contractuales resuelven el recurso especial.
- **Competencia:** la CNMC recibe los indicios de colusión que los órganos de contratación deben comunicar (art. 132.3 LCSP) y su Unidad de Inteligencia Económica **ya opera** una herramienta propia de aprendizaje automático, **BRAVA** (*Bid Rigging Algorithm for Vigilance in Antitrust*), que analiza su base de datos de licitaciones para detectar indicios de colusión y que, según su memoria de 2025, se ha usado en expedientes que acabaron en sanción; está desarrollando un sistema de razonamiento complementario (ATENEA). Es el ejemplo español más claro de analítica algorítmica **dentro** de un supervisor, y por tanto de lo que este protocolo debería poder auditar desde fuera.
- **Evaluación:** Ley 27/2022 y Agencia Estatal de Evaluación de Políticas Públicas (Estatuto por Real Decreto 65/2026, publicado el 4 de febrero de 2026; constituida en abril de 2026); AIReF; Tribunal de Cuentas.
- **Informantes:** Ley 2/2023 y Autoridad Independiente de Protección del Informante, en funcionamiento desde el 1 de septiembre de 2025.
- **Analítica de riesgos del propio Estado:** MINERVA (AEAT; análisis sistemático de conflicto de interés en fondos del Plan de Recuperación, Orden HFP/55/2023) y Arachne (Comisión Europea).
- **Transparencia:** Ley 19/2013 y Consejo de Transparencia y Buen Gobierno; Defensor del Pueblo.
- **Detección de riesgos con datos abiertos, fuera del Estado:** existen herramientas públicas de «banderas rojas» sobre contratación que incluyen España: opentender (Government Transparency Institute), Integrity Watch de Transparencia Internacional UE y exploradores de la PLACSP como Gobierto Contratación. Ya hay **monitorización ciudadana** de contratos concretos (iMonitor). **Este documento no propone construir otra herramienta de detección**: su sitio es la ejecución, la respuesta y la publicidad de lo que ocurre después de la adjudicación. Referencias facilitadas en una ronda de trabajo anterior; su estado actual debe verificarse.
- **Antecedente legislativo decaído:** el **Proyecto de Ley Orgánica de Integridad Pública** (expediente 121/000111) se publicó en el BOCG el 11 de septiembre de 2026 y se tramitó por **procedimiento de urgencia** en la Comisión de Hacienda y Función Pública. Preveía una Agencia Independiente de Integridad Pública que integraría la Oficina de Conflictos de Intereses, la AIPI y el Servicio Nacional de Coordinación Antifraude, con cruces de registros para detectar riesgos. **No llegó a aprobarse:** el Real Decreto 806/2026, de 5 de octubre (publicado y en vigor el 6 de octubre de 2026), disolvió el Congreso y el Senado, y la iniciativa decayó con el fin de la legislatura. La ficha del Congreso puede seguir mostrando la última fase, «Enmiendas»; esa etiqueta histórica **no significa que el plazo siga abierto**. Es un antecedente documental: cualquier reforma requeriría una nueva iniciativa.

**Alcance real, resultados y capacidad de respuesta de cada órgano: pendientes de evaluación empírica en la fase 0.** No afirmamos que no funcionen. Afirmamos que su funcionamiento debe poder verificarse desde fuera, y que si el Estado va a supervisar con analítica de datos, alguien externo debe poder auditar esa analítica.

### 8.2 Deberes de respuesta que ya existen

| Cauce | Norma | Quién puede usarlo | Deber | Plazo | Si no responden |
|---|---|---|---|---|---|
| Procedimiento administrativo | Ley 39/2015, art. 21 | Interesados | Resolver expresamente | El del procedimiento | Silencio con efectos; recurso |
| Acceso a información pública | Ley 19/2013, art. 20 | Cualquier persona | Resolver la solicitud | 1 mes, ampliable | Reclamación ante Consejo de Transparencia; contencioso |
| **Derecho de petición** | **Art. 29 CE; LO 4/2001, arts. 9, 11, 12** | **Cualquier persona física o jurídica** | **Contestar motivadamente; inadmitir motivadamente** | **3 meses (contestación); 45 días hábiles (inadmisión)** | **Procedimiento de protección de derechos fundamentales** |
| Recomendaciones del Defensor del Pueblo | LO 3/1981, art. 30 | Solo el Defensor | Responder por escrito | 1 mes | Inclusión en informe a las Cortes |
| Informantes | Ley 2/2023 | Informantes en los supuestos legales | Tramitación y protección | Los de la ley | Autoridad Independiente de Protección del Informante |

**Conclusión:** no hace falta legislar un deber genérico de respuesta. Hace falta **elegir bien el cauce** para cada comunicación (§6.3), **usar** los deberes existentes, **publicar** las respuestas y **medir** el cumplimiento. El derecho de petición es el cauce residual, no el universal: cubre las peticiones de actuación general que no tienen procedimiento propio; el acceso documental va por la Ley 19/2013 y los indicios de infracción por el canal sectorial. La propuesta normativa derivada (§8.6) es la publicidad de las respuestas, no la creación del deber. Se retira la idea de «entidades acreditadas» con deber de respuesta reforzado: duplicaría la ley y crearía un privilegio capturable.

### 8.3 Recursos y legitimación

El art. 48 LCSP vincula el recurso especial a derechos o intereses legítimos afectados (con mención expresa de sindicatos y organizaciones empresariales en determinados supuestos); el art. 19 LJCA exige interés legítimo o habilitación legal. **Una red que se proclama vigilante no queda legitimada automáticamente.** No se conoce una laguna justiciable documentada que justifique una acción pública general en contratación. Prioridad: acceso a datos, derecho de petición, colaboración con legitimados y comunicación de indicios a los órganos competentes. La ampliación de legitimación queda como pregunta abierta (§11).

### 8.4 Privacidad, honor y transparencia algorítmica

- **Honor e información** (arts. 18 y 20 CE; LO 1/1982): la doctrina constitucional exige veracidad como diligencia en la comprobación, no infalibilidad. Los grados de soporte, la notificación previa y la rectificación visible son la forma operativa de esa diligencia; no la sustituyen. Las personas jurídicas también tienen protección del honor.
- **Protección de datos** (RGPD; LO 3/2018): minimización, finalidad, evaluación de impacto. Los documentos públicos contienen datos personales; un autónomo adjudicatario es persona física. Regla del piloto: la ficha pública dice «adjudicatario: persona física; identidad en la fuente oficial [enlace]»; no se almacenan nombres ni NIF de personas físicas en campos estructurados públicos ni se usan como clave de agregación; cualquier cruce necesario se hace bajo acceso restringido, con registro y resultado agregado. Esto **reduce** la exposición pero **no elimina el tratamiento**: la ingesta de documentos, los identificadores enlazados y los conjuntos restringidos pueden permitir reidentificación. La base jurídica (no se da por válido el interés legítimo de forma automática) y la necesidad de una evaluación de impacto deben determinarlas especialistas según el tratamiento concreto.
- **Acceso al código de algoritmos públicos:** la Sentencia del Tribunal Supremo (Sala Tercera, Sección Tercera) de 11 de septiembre de 2025, recurso 7878/2024, reconoció a la Fundación Civio el derecho de acceso al código fuente de la aplicación BOSCO (bono social eléctrico) al amparo de la legislación de transparencia. Existencia, fecha y sentido del fallo están confirmados por reseñas jurídicas independientes; el texto íntegro queda pendiente de cotejo antes de afirmar su alcance general. Es un precedente favorable a la auditoría externa de sistemas automatizados públicos y una exigencia que este proyecto se aplica a sí mismo: código, reglas, conjuntos de referencia y versiones de modelos, públicos.
- Como paralelo no vinculante, el Algorithmic Transparency Recording Standard británico exige fichas públicas de determinados sistemas algorítmicos del sector público.

### 8.5 Reglamento de IA de la UE

- El **Reglamento (UE) 2026/1744**, de 8 de julio de 2026 (DOUE de 24 de julio de 2026, «Digital Omnibus on AI»), modificó el Reglamento (UE) 2024/1689. Las obligaciones para sistemas de alto riesgo del **anexo III** se aplican desde el **2 de diciembre de 2027**; las del **anexo I**, desde el **2 de agosto de 2028**. El capítulo IV, incluido el **art. 50**, es aplicable en general desde el **2 de agosto de 2026**. La única transición que introduce el Reglamento 2026/1744 en este punto (nuevo art. 111.4) afecta **solo a la obligación del art. 50.2** —marcado legible por máquina de contenido sintético— de determinados proveedores de sistemas introducidos en el mercado antes del 2 de agosto de 2026, que disponen hasta el 2 de diciembre de 2026. **No aplaza el art. 50.4**, que obliga a quien despliegue el sistema a declarar el texto generado o manipulado por IA publicado sobre asuntos de interés público, sin perjuicio de sus excepciones (revisión humana con responsabilidad editorial real). El protocolo declara siempre el uso de IA como salvaguarda adicional.
- **Art. 5.1.d** (aplicable desde febrero de 2025): prohíbe evaluar o predecir el riesgo de que una **persona física** cometa un delito basándose únicamente en perfilado o rasgos personales. No es una prohibición general de analítica sobre entidades o actos; el principio «actos, no personas» mantiene al proyecto fuera de ese supuesto, lo que no lo exime de las demás normas.
- **Art. 50.4:** quien publique texto generado por IA para informar al público sobre asuntos de interés público debe indicarlo, salvo revisión humana con responsabilidad editorial real. El proyecto **declarará siempre** qué fragmentos fueron generados, sin presumir la exención.
- **Arts. 14 y 27** (supervisión humana; evaluación de impacto sobre derechos fundamentales): el piloto cívico informativo no parece encajar en el anexo III, pero adopta voluntariamente ambos requisitos. Cualquier uso institucional futuro exige análisis caso por caso.

### 8.6 Posibles reformas, solo con evidencia de fase 0 y piloto

| Posible reforma | Qué existe ya | Qué faltaría | Instrumento | Prioridad |
|---|---|---|---|---|
| **Publicidad por contrato de los datos de ejecución** | El art. 63.3 LCSP obliga a publicar en el perfil de contratante, entre otros, objeto, duración, presupuesto e importe de adjudicación, formalización y **anuncios de modificación con su justificación**, y el art. 63.1 exige ya **formatos abiertos y reutilizables** para esa información; la Ley 19/2013 (art. 8.1.a) añade modificaciones, desistimientos y renuncias; el **art. 346.3 LCSP** obliga a comunicar al Registro de Contratos del Sector Público, con excepciones, modificaciones, **prórrogas, variaciones de plazo o precio, importe final y extinción**, y el **art. 346.5** prevé acceso público a los datos no confidenciales no publicados previamente | Publicación **sistemática, interoperable y vinculada al identificador de cada expediente** de los datos de ejecución que ya deben comunicarse al Registro conforme al art. 346; y estudio separado, jurídico y de costes, de la publicación de certificaciones (art. 240 para obras), pagos y documentos de recepción o conformidad (art. 210) según el tipo contractual, salvaguardando la información protegida. La reforma puede implicar obligaciones adicionales de estandarización, conexión y publicación; no presupone ausencia total de acceso público hoy. **La cobertura real se mide en la fase 0 antes de afirmar nada.** Primera medición (§9.0 bis, 30/10/2026; corregida el 01/11/2026): en 1.549 de 1.593 expedientes de obras adjudicados en 2023 (1–10 M€) con fin teórico estimado anterior al corte (97,2 %), el programa no identificó indicadores de finalización o extinción en los campos examinados de la sindicación de la PLACSP; no prueba que no exista la información por otras vías. Ya existen un **Anuncio de Finalización de Contrato** estructurado en la PLACSP (`DOC_CCN`), que se usa muy poco en esa población, y un registro autonómico (el vasco) que publica la finalización contrato a contrato, aunque con cobertura incompleta. Publicar el fin no figura entre lo que el art. 63.3 obliga a publicar (§9.0 ter). Si la revisión humana lo confirma, la reforma podría consistir más en **usar sistemáticamente cauces que ya existen** que en crear otros nuevos; es una propuesta a estudiar, no una conclusión jurídica | Eventual reforma de la LCSP (arts. 63 y 346) o de la Ley 19/2013, mediante una **nueva iniciativa legislativa**. El Proyecto 121/000111 **decayó al disolverse las Cortes en octubre de 2026** y no es una vía de enmienda disponible. El alcance y los costes deben contrastarse con especialistas antes de redactar un texto | **Máxima**: es la medida con mejor relación coste-beneficio del documento, si la fase 0 confirma la laguna |
| **Publicidad de respuestas a peticiones y solicitudes en materia de contratación** | Deberes de respuesta vigentes (§8.2) | Publicación de las contestaciones (anonimizadas si procede) en el perfil de contratante o portal de transparencia; identificador y acuse interoperables | Ley ordinaria o reglamento | Alta |
| **Auditabilidad externa de los sistemas de analítica de riesgo usados por administraciones** | Precedente BOSCO; art. 41 Ley 40/2015 para actuación automatizada | Obligación de publicar reglas, métricas de error y permitir auditoría de los sistemas de supervisión algorítmica (incluidos los de organismos que puedan crearse en reformas futuras) | Ley ordinaria | Media |
| Ampliación de legitimación para recurrir | Arts. 48 LCSP y 19 LJCA | Laguna no documentada | — | Solo como pregunta (§11) |
| Deber de respuesta a «entidades acreditadas» | **Ya cubierto** por LO 4/2001 | — | — | **Retirada** |
| Potestad cautelar nueva vinculada a alertas | Potestades existentes | — | — | **Descartada** |

La arquitectura no presupone reformar la Constitución. No hay propuesta de suspensión automatizada de decisiones gubernamentales o parlamentarias.

### 8.7 Referencias internacionales

La OCDE (2025) documenta más de 200 casos de uso de IA en funciones centrales del Estado y advierte de datos sesgados, opacidad, errores y confianza excesiva en la automatización. El Tribunal de Cuentas de la Unión y la Contraloría General de Brasil usan desde hace años la herramienta **Alice** para analizar diariamente pliegos y licitaciones y generar alertas para auditores: un precedente de analítica **dentro** de un órgano de control, útil para aprender de sus métricas y falsos positivos.

---

## 9. Plan experimental: comprobar primero si hace falta la IA

El primer producto no son acusaciones ni bloqueos, sino expedientes de contratos públicos con fuentes trazables y un protocolo de medición. Antes de analizar casos se publican el preregistro y un análisis jurídico de las fuentes y sus condiciones de reutilización.

### 9.0 Prototipo mínimo sin IA (arranque en una semana; seguimiento hasta el vencimiento de plazos)

**Semana de arranque (una persona, una hoja de cálculo):**

1. Descargar la sindicación ATOM de licitaciones de la PLACSP para **un sector y un año**.
2. Elegir **30 contratos** por criterios publicados de antemano (tipo, importe, fecha, territorio, tamaño y nivel de la administración) y sorteo con semilla publicada. Si se quiere comparar después administraciones gobernadas por distintas formaciones, la clasificación política se documenta aparte y solo se usa para control de sesgos, nunca como criterio de selección ni de culpabilidad.
3. Para cada contrato, una fila: enlace al expediente; importe de adjudicación; modificaciones publicadas (sí/no, importe, justificación); prórrogas; ¿consta acta de recepción?; ¿consta importe final?; ¿consta algún pago o certificación?; ¿consta en el acceso público del Registro de Contratos?; fecha de la última publicación. Sin nombres de personas físicas.
4. Clasificar cada carencia por finalidad (§6.3) y enviar **tres solicitudes de acceso** (Ley 19/2013) para documentos que deberían existir y, **solo si hay objeto admisible sin procedimiento específico**, hasta tres **peticiones** (LO 4/2001) de actuación general, registrando fecha, cauce, motivo de la elección y plazo legal.
5. Publicar al final de la semana: porcentaje de campos de ejecución que constan; comunicaciones **enviadas, acuses recibidos y plazos pendientes**; coste en horas. **No se publican tasas de cumplimiento**: los plazos no han vencido.

**Seguimiento (uno a tres meses después):** al vencer cada plazo legal, registrar admisión o inadmisión y su motivo, respuesta y su contenido, o ausencia de respuesta localizada; publicar entonces la tasa y el tiempo de respuesta, separando «cauce correctamente elegido» de «inadmitida por cauce inadecuado» (este segundo dato mide al protocolo, no a la administración).

Sin modelos, sin código, sin acusaciones. Responde a la única pregunta que importa antes que todas las demás: **¿los datos de ejecución están o no están, y responden o no responden?** Es también lo que debería ponerse delante de un administrativista y de la OIReScon para obtener una primera revisión humana honesta.

### 9.0 bis Primer resultado de la fase 0 (30/10/2026; cifra corregida el 01/11/2026)

La primera parte del prototipo de §9.0, comprobar si los datos de ejecución constan, se ha hecho con más alcance que el previsto. En lugar de una hoja de cálculo con 30 contratos, un programa abierto (Python, sin IA) leyó **todos** los datos abiertos de la PLACSP de 2023 a octubre de 2026: 2,56 millones de registros y 667.929 expedientes. **No se ha hecho la segunda parte**: las solicitudes de acceso y las peticiones exigen identificarse y quedan para quien adopte el protocolo.

- **Población:** 1.651 expedientes de obras con la primera adjudicación en 2023 y un presupuesto base sin IVA de 1 a 10 M€, en la sindicación «perfiles del contratante alojados en la PLACSP».
- **Resultado:** de los 1.593 con **fin teórico estimado** anterior al corte (29/10/2026), en **1.549 (97,2 %)** el programa no identificó **indicadores de finalización o extinción** en los campos examinados de la sindicación: ningún anuncio de finalización (`DOC_CCN`) vigente, ningún nombre de archivo o etiqueta documental de recepción, liquidación, certificación final, fin de obra o resolución del contrato, y ningún texto de modificación que comunique la liquidación, la certificación final o la recepción. El método inspecciona **códigos, nombres de archivo y etiquetas**, no el contenido de los adjuntos, y el fin teórico es una estimación hecha con las fechas y duraciones publicadas (incluidas las modificaciones de plazo que constan), no la fecha contractual real. La cifra **no permite concluir** que las obras no hayan terminado, que no exista documentación por otras vías ni que se haya incumplido la ley.
- **Corrección (01/11/2026):** la versión 2.3 del programa daba 1.573 (98,7 %). Algunos órganos publican la liquidación o la certificación final como si fuera una «modificación del contrato» («se formaliza la liquidación del contrato»), en un campo de texto que la especificación de la sindicación no documenta y que el programa no leía. La versión 2.4 lo lee en dos niveles: solo cuenta como fin un texto que sea, completo, una fórmula breve de una lista cerrada («se formaliza la liquidación del contrato», «certificación final de obra»…); los textos que solo coinciden con un patrón amplio se anotan como candidatos y **no cuentan** (2 en la población). Los 24 expedientes nuevos se revisaron a mano y todos son fines comunicados (uno es un expediente con varios lotes y el texto no dice a cuáles se refiere); la revisión caso por caso se conserva, pero desde la v0.4.6 no se publica porque nombra órganos. Es una **práctica observada, concentrada en pocos órganos**: 22 de los 24 casos proceden de un mismo órgano y los otros 2 de un segundo, así que no puede generalizarse a otros. La revisión manual previa no lo detectó porque revisaba documentos, no ese campo.
- **Hallazgo:** la PLACSP tiene un **Anuncio de Finalización de Contrato** (`DOC_CCN`, lista de códigos 2.11). Su documento contiene la fecha real de fin y la causa de extinción. No figura en la especificación de sindicación de 2024 y aparece en 8 de los 1.651 expedientes. La misma lista prevé su anulación (`ANUL_CCN`); el programa no cuenta un anuncio anulado, y en todo el corpus procesado no hay ninguna anulación, de modo que los 8 casos no están afectados.
- **Contraste:** el Registro de Contratos del Sector Público publica solo estadísticas agregadas. El registro de contratos vasco publica, contrato a contrato, el estado, la fecha y el importe de finalización.
- **Revisión realizada:** tres rondas sucesivas de revisión adversarial con ChatGPT sobre el programa (las objeciones de la tercera se corrigieron en la versión 2.3; ver `METODO.md`), más la ronda de la v0.4.4, que endureció el patrón de la versión 2.4, una revisión de código con Gemini sobre la primera versión (su texto no se conservó; el repositorio resume qué detectó) y comprobaciones manuales de expedientes en la web oficial. **No constituyen una auditoría humana independiente ni una validación jurídica o estadística.**
- **Qué había en los 20 casos con indicador de fin definitivo de la versión 2.3** (a los que la 2.4 suma los 24 de la corrección, todos liquidaciones o certificaciones finales): la comprobación manual confirmó en los 20 la **extinción** del contrato, pero de dos tipos distintos. **7 terminaciones ordinarias**, cada una acreditada por su propio documento (acta de recepción, liquidación, certificación o certificado final de obra; uno, por un `DOC_CCN` con el acta de recepción como anexo). **13 resoluciones**, es decir, rupturas anticipadas del contrato (incumplimiento, demora, insolvencia o extinción del contratista, desistimiento o mutuo acuerdo); en una de ellas la resolución solo afecta a dos lotes del expediente. Una resolución acredita que el contrato se extinguió, **no que la obra se recibiera ni se ejecutara satisfactoriamente**. La cifra principal mide indicadores de finalización **o extinción**, no «obra terminada correctamente».

**Repositorio sin listas de obras (v0.4.6):** el repositorio publica las cifras agregadas y las **huellas SHA-256 de los ficheros por expediente**, no la lista de obras con su órgano. Quien repita el análisis con los datos del manifiesto obtiene la lista en su ordenador y puede comprobar que sus ficheros son idénticos a los del estudio (se comprobó con una repetición completa el 02/11/2026).

**Límites:** la cifra es una **métrica del clasificador en el canal estudiado**, no una tasa validada de falta real de información. Mide coincidencias que detecta un programa en un canal de datos, no la inexistencia de documentos, ni que las obras no hayan terminado, ni incumplimientos. Los casos sin indicador se muestrearon a mano con 21 expedientes de la población y con 60 de otros años e importes (0 omisiones de documentos; §9.0 ter), pero esas muestras no detectaron los fines comunicados en el texto de las modificaciones, así que **no bastan para descartar otras fuentes de falsos negativos**, y no lo ha revisado ningún jurista ni estadístico.

**Reproducción:** el método (`METODO.md`), el programa, los resultados agregados, las huellas de los ficheros por expediente y las revisiones están en el repositorio público https://github.com/democracia-auditable/democracia-auditable (código MIT-0, documentos CC0); los resultados agregados de la clasificación manual están en `METODO.md`, sin la lista de casos. Los ficheros de datos de la PLACSP **no se redistribuyen**: el script `descargar_datos.py` los descarga de la fuente oficial y comprueba su huella SHA-256 contra `manifiesto_descarga_estudio.json`. El programa que produjo las cifras es la versión 2.4 de `medir_ejecucion.py`, con huella SHA-256 `e451cae1c78ba4525f1ca796db58c1f8fd4dff3de24624e8c9f7e08103f15294`, que consta también en el manifiesto de resultados. La versión 2.3 (`b393a0d682f28acfb586a9ccc14c55f7fcf7e99db53591fe34432ff0328de202`) y sus resultados se conservan para comparar. Si la fuente actualiza sus ficheros, la descarga no coincidirá con las huellas: entonces se estará **repitiendo** la medición con datos nuevos, no reproduciendo la original.

### 9.0 ter Investigaciones complementarias (1 de noviembre de 2026)

Después del primer resultado se hicieron nueve investigaciones con el mismo método: datos y textos oficiales, programas abiertos sin IA y límites declarados. **Ninguna nombra ni compara órganos, y ninguna ha pasado revisión humana independiente.** Las ocho primeras pasaron una ronda de revisión adversarial con ChatGPT con la v0.4.4, y la novena, con la v0.4.5; las dos rondas no son independientes entre sí (mismo revisor). Las tres marcadas como *preregistradas* fijaron por escrito sus definiciones y umbrales, con huella SHA-256 y hora, antes de medir. La fecha es **declarada**: la huella prueba la integridad del texto, no su anterioridad ante terceros. Cada una tiene su informe, sus programas y sus fuentes en el repositorio.

1. **El anuncio de finalización por dentro** (`investigacion_doc_ccn/`).
    - **Presencia:** se usa desde mayo de 2024, pero lo tiene solo el 0,69 % de las obras con fin teórico en 2024 y el 0,48 % de las de 2025; lo han usado 198 de 4.370 órganos.
    - **Contenido:** en los 633 contratos con anuncio, entre el 29 % y el 32 % muestran indicios de resolución. Es una proporción **entre quienes publican**, no una tasa de resolución de las obras. La duración real supera a la prevista en una mediana de 12 días.
    - **Acceso:** el contenido del anuncio no está en la sindicación; hay que seguir el enlace de cada expediente.
2. **El mayor tiempo observado no basta para explicar la baja detección** (`investigacion_cohortes/RESULTADOS.md`). En las obras adjudicadas en 2021 y 2022, con dos o tres años más de margen, la proporción sin indicador apenas baja: alrededor del 96–97 % con la corrección de la v0.4.4. Las obras cuyo plazo venció hace más tiempo no tienen más indicadores. Con cautelas: el anuncio de finalización solo existe desde 2024, los datos están censurados y el clasificador no se validó igual en esos años.
3. **Validación del clasificador fuera de 2023** (`investigacion_cohortes/validacion/`).
    - **Resultado:** en una muestra **estratificada** de 60 obras sin indicador (12 estratos de año e importe, 5 por estrato, semilla publicada), la página web no mostraba ningún documento de fin que el programa hubiera pasado por alto: 0/60. Es una **validación exploratoria**: la cota binomial del 6,0 % supone una muestra homogénea, que la estratificación no garantiza, y no se traslada sin ponderar al conjunto de las obras.
    - **Límite:** esa revisión miró documentos, no el texto de las modificaciones, donde después apareció la omisión que corrige la v0.4.4. La hizo el mismo sistema que escribió el clasificador.
4. **Marco jurídico** (`investigacion_juridica/`; lectura de normas sin revisión jurídica).
    - **Publicar el fin no es obligatorio con carácter general:** no figura en el art. 63.3 LCSP ni en el art. 8.1.a de la Ley 19/2013, y la documentación técnica de la PLACSP califica su anuncio de finalización de «carácter voluntario».
    - **Comunicarlo sí es obligatorio en los supuestos que fija la ley,** pero a otros órganos: al Registro de Contratos, con excepciones (art. 346.3 LCSP; el RD 817/2009, art. 31 y anexo I, solo exige el importe final y, si hubo resolución, su causa y fecha; su encaje completo tras la LCSP de 2017 está pendiente de dictamen jurídico), y al Tribunal de Cuentas para los contratos que superan ciertos umbrales (art. 335).
    - **Los documentos deben existir cuando se produce la fase correspondiente:** si la obra se ha recibido, el acta de recepción y, después, la certificación final (art. 243). Cuando existen, son información pública (Ley 19/2013, art. 13).
    - **Asimetría:** una modificación debe publicarse en 5 días (art. 207.3); el fin, no.
    - **Consecuencia:** la cifra de la §9.0 bis **no mide un incumplimiento**, sino la distancia entre lo que la Administración debe saber y comunicar y lo que publica.
5. **Qué ocurre cuando se pregunta** (`investigacion_consejo/`; 11.199 resoluciones estatales del Consejo de Transparencia y su seguimiento de cumplimiento).
    - **Acceso reconocido en las resoluciones examinadas:** el Consejo ha reconocido el «carácter eminentemente público» del acta de recepción (R CTBG 2024-0107, cumplida) y el control ciudadano de la contratación «en cualquiera de sus fases» (R/0526/2020). Once resoluciones muestran un criterio visible en casos concretos, no una doctrina general ni una garantía de acceso.
    - **Por qué se deniega:** porque el documento no existe o lo tiene otro órgano, porque se pidió antes de que existiera, por errores de trámite o por **abuso de derecho** al pedir repetidamente documentos parciales de una misma obra (R/0863/2021, que cita R/0271/2021 y R/0342/2021).
    - **Silencio:** está detrás del 34–46 % de las **reclamaciones** de cada año (el denominador son reclamaciones, no solicitudes; no permite estimar cuántas solicitudes quedan sin respuesta). En 2021–2026, entre el 29 % y el 39 % de esas reclamaciones por silencio solo obtuvieron la información durante el procedimiento ante el Consejo.
    - **Tiempos y cumplimiento:** el Consejo resolvió con una mediana de 4 a 7 meses en 2021–2024 (plazo legal: tres meses). El 86–88 % de sus resoluciones estimatorias de 2023–2025 consta como cumplido.
    - **Órganos autonómicos** (añadido en la v0.4.5; revisado en la v0.4.6). En el escenario del protocolo, el 58 % de las **solicitudes potenciales** corresponde a administraciones cuyo órgano de garantía podría ser autonómico, si se llegara a reclamar; no es una proporción de reclamaciones. En dos órganos revisados de forma sistemática (unas 20.400 resoluciones), los asuntos sobre documentación del fin o la ejecución de obras públicas, en sentido estricto, son muy pocos (2 y 7) y **ninguno tuvo una desestimación de fondo ni una inadmisión**; en uno, 3 de los 7 terminaron porque la información se entregó tras reclamar. Cautelas: pocos casos, clasificación de un solo lector, muchos solicitantes con un derecho de acceso reforzado (cargos electos) y solo dos de unos diez órganos (`investigacion_consejo/COMPLEMENTO_AUTONOMICO.md`, reproducible con `filtrar_autonomicos.py`).
    - **Los plazos dependen de la ley aplicable** (revisado en el BOE en la v0.4.6 y la v0.4.7; `protocolo_obras/regimenes.py`): para resolver, un mes en la mayoría de los regímenes, **20 días hábiles** en la Administración de Madrid y de Murcia y en la Junta de Andalucía, y **30 días hábiles** en Extremadura; la ampliación es por un período igual en la mayoría, de **quince días** en el País Vasco y de **hasta la mitad del plazo** en Cataluña; para reclamar contra el silencio, un mes en la mayoría y **sin plazo según la ley** en Cantabria, Navarra y el País Vasco; el órgano de garantía resuelve en tres meses en general y en **dos en Cataluña**. En Madrid, la ley dice un mes y su órgano de garantía aplica un criterio de no preclusión. Es una lectura de un no jurista.
6. **Un registro que publica el fin** (`investigacion_registro_vasco/`).
    - **Qué publica:** el registro de contratos vasco da en abierto, por contrato, el estado, la fecha y el importe de finalización, y la resolución si la hubo.
    - **Cobertura:** aun así, en las obras de al menos 50.000 € de 2014–2017 con el plazo vencido, el fin consta solo en el 37–47 %. El umbral de 50.000 € es un criterio analítico para aproximar los contratos no menores, no una identificación jurídica, y quedan fuera muchas obras sin plazo estimable.
    - **Lectura:** el canal existe, pero no garantiza el dato. No es comparable con la PLACSP como medida de cumplimiento.
7. **¿Se puede saber si una obra empezó?** (`investigacion_inicio/`; *preregistrada*). No con fiabilidad.
    - **Lo que se ve:** el 64 % de las obras de 1 a 10 M€ sin fin no muestra ningún rastro publicado después de la formalización.
    - **Lo que vale:** en las obras que con seguridad se ejecutaron, porque publicaron su anuncio de finalización, 42 de 69 de 1 M€ o más (61 %; IC95 48–72 %) tampoco tenían rastro antes del anuncio. La ausencia de rastro tiene, por tanto, **escasa capacidad para distinguir** una obra terminada sin publicarlo de una que no empezó, al menos en esta muestra. No es una muestra aleatoria de todas las obras ejecutadas, y la dirección del posible sesgo (quien publica su fin puede publicar más) no está contrastada.
    - **Inicio real:** la ejecución empieza con el acta de comprobación del replanteo (art. 237), que no se publica. El dato solo se obtiene preguntando.
8. **Qué traen los anuncios de modificación** (`investigacion_modificaciones/`; *preregistrada*).
    - **Modificaciones «opacas»** (sin importe, sin plazo y sin un texto de al menos 40 caracteres; definición operativa, no jurídica): son el 2,1 % y se concentran en pocos órganos. Es un **indicador de calidad informativa**, nunca de modificación irregular. Muchas son en realidad suspensiones, reanudaciones, liquidaciones o recepciones parciales publicadas con el formulario de modificación. De ahí sale la corrección de la v0.4.4.
    - **Documentación del art. 207.3** (alegaciones del contratista e informes): solo el 13–16 % de las obras modificadas tiene algún documento cuyo nombre corresponda a una modificación, y el XML del anuncio de modificación no tiene campo para adjuntarlos. Esto **no prueba un incumplimiento**: los documentos pueden publicarse con otros nombres o en otro canal.
    - **Plazo de 5 días:** en una muestra pequeña y elegida por opacidad, el anuncio se publicó una mediana de 3 días después de la fecha que trae el XML del anuncio, cuyo significado (aprobación, efectos o registro) no está verificado. Es una comparación descriptiva, no una tasa de incumplimiento.

9. **Una coincidencia documental asociada a contratos resueltos: la «terminación licitada de nuevo»** (`investigacion_terminacion/`; *comparación preregistrada*; añadida en la v0.4.5 y revisada en la v0.4.6).
    - **Qué hace:** marca una obra cuando el mismo órgano licita después otra cuyo título casi repite el suyo y habla de terminarla («terminación», «finalización», «resto de obras», «obras pendientes»…). Es **compatible** con que el primer contrato no terminara la obra, pero también con una recepción parcial, un alcance complementario u otras fases: **obliga a verificar, no prueba nada**. Las condiciones exactas (parecido de títulos, fases, números, palabras raras) están en `protocolo_obras/SENAL_TERMINACION.md`. La regla se diseñó en una revisión manual de obras y se congeló con huella antes de probarla.
    - **Comparación con obras de final conocido** (50.000 € o más, adjudicadas en 2019–2023): marcó **10 de 273 expedientes con indicios documentales de resolución (3,7 %)**, frente a **2 de 558 con indicios de terminación ordinaria (0,4 %)**. Cociente 10,2 (IC95 2,3–46,3, muy ancho); Fisher p = 0,0004. Se alcanzaron las condiciones preregistradas.
    - **Grado de evidencia:** *asociación preregistrada en un corpus parcialmente expuesto al diseño*, **no una validación confirmatoria**: la regla se diseñó viendo dos de los tres tramos de importe que forman la tabla principal. En el único tramo ajeno al diseño (50.000–200.000 €), 3 de 103 frente a 0 de 193: prometedor, pero no concluyente (IC 0,7–250). Los grupos se forman por lo que se publica (posible sesgo de espectro) y las proporciones **no son trasladables** a obras sin final publicado. Falta una validación externa con otro periodo, otros órganos y un registro previo con fecha verificable.
    - **Uso:** una marca obliga a verificar; **su ausencia no informa sobre el estado de la obra** (marca a muy pocos de los resueltos). Avisa con uno a tres años de retraso y depende del vocabulario de los títulos.
    - **Entre las obras sin final publicado**, marca 78 de 44.178 (0,18 %), de 66 órganos y con un máximo de 3 por órgano (con la definición de «sin final» del estudio v2.4, 78 de 44.290). En una muestra de 20, la página web de la plataforma no mostraba ningún documento de resolución; puede constar en otros canales.
    - **Lectura:** «coincidencia documental compatible con una terminación posterior que requiere comprobación», no contrato fracasado ni resuelto. **La lista de obras no se publica.**

**Qué se deduce para el protocolo.** La información que falta en los datos abiertos **debe existir cuando la obra se ha recibido y puede pedirse**. En las resoluciones examinadas, el Consejo de Transparencia la considera pública, pero obtenerla es lento y depende de que cada persona pregunte y reclame. Es exactamente el problema que el protocolo quiere resolver: **una pregunta por obra, sobre el documento final, una sola vez, con la respuesta o el silencio a la vista de todos.** El Anexo D concreta ese diseño para las obras públicas.

### 9.1 Tres pruebas separadas

**Prueba A — Mapa institucional y de datos (sin IA).** Un sector y tipo contractual; qué campos de licitación, adjudicación, ejecución y pago deberían constar por ley, cuáles son accesibles y cuáles solo mediante solicitud; plazos reales. No se etiqueta como incumplimiento una ausencia hasta verificar la obligación legal y su plazo.

**Prueba B — Benchmark técnico independiente.** Conjunto de referencia de al menos **300 documentos/contratos** heterogéneos (propuesta inicial; tamaño definitivo por cálculo de potencia a partir de un estudio preliminar), con **2.000–3.000 instancias de campo**, estratificado por administración, fecha, PDF nativo/escaneado, complejidad y tipo de campo. Anotación ciega por dos humanos y arbitraje de un tercero; se publica el acuerdo interanotador y **se conservan las divergencias como dato**. Tres métodos comparados: manual; reglas y parseo estructurado; reglas más extracción asistida por IA. Se audita el 100 % de los desacuerdos entre métodos y una muestra de los acuerdos (los acuerdos erróneos son el caso peligroso). Precisión siempre desagregada por tipo de documento.

**Prueba C — Operación.** **20–40 contratos** como ensayo de flujo de trabajo, no como muestra para inferir tasas raras. Universo y muestreo preregistrados, exclusión de financiadores y miembros, simetría entre entidades de distinto signo. Se miden tiempos, respuestas, costes y errores; se publican los casos sin hallazgos.

### 9.2 Hipótesis falsables

- **H1.** Frente a la línea base determinista/manual, la IA reduce el trabajo humano total manteniendo o mejorando la exactitud por campo y sin aumentar los daños por alertas falsas.
- **H2.** La segunda lectura reduce de forma medible los errores conjuntos, no solo produce desacuerdos aparentes.
- **H3.** El expediente completo mejora la capacidad de auditar la procedencia de cada afirmación respecto a la práctica manual.
- **H4.** La red puede medir y publicar con precisión plazos y tasas de respuesta **legalmente aplicables**, sin etiquetar silencios indebidamente.
- **H5.** El valor de los datos estructurados puede aislarse del valor de los modelos generativos.
- **H0a y H0b (apuesta de §1).** Respuesta a comunicaciones admisibles y bien encauzadas, en una cohorte observada hasta el vencimiento de plazos; detección de discrepancias relevantes, en una muestra independiente auditada exhaustivamente. Poblaciones y muestreos distintos, definidos en el preregistro.

Si H1 falla, la IA **no se despliega** para esa función. Si H0a falla, el proyecto se reorienta a §8.6; si H0b falla, la capa de detección sobra y queda la de seguimiento.

### 9.3 Datos, extracción y contraste

Fuentes: sindicación ATOM y datos abiertos de la PLACSP (histórico desde 2012), perfiles de contratante, boletines, documentos de ejecución públicos, informes de órganos fiscalizadores, respuestas a peticiones y solicitudes. El estándar **OCDS** puede orientar un esquema interoperable de contratos, modificaciones, transacciones e hitos, sin atribuir a España una adopción que no se ha comprobado.

Extracción prioritaria: XML/ATOM/JSON y sus esquemas; validación de fechas e importes; identificación de contrato y versiones; cruce determinista de eventos. Para PDF: texto digital con anclaje; OCR solo si es indispensable y con control humano; los modelos **proponen** campos y nunca los convierten por sí solos en hechos. Cada fila extraída contiene afirmación, documento, página o fragmento, fecha de descarga, huella, transformación, método, versión, discrepancia y revisión humana.

### 9.4 Evaluación estadística

Por tipo de campo y estrato: aciertos, falsos positivos, faltas de cobertura, coste por expediente, fallos de anclaje y errores graves. Para dos extractores A y B: p(A erra), p(B erra), p(ambos), P(B erra | A erra) y cociente entre error conjunto observado y esperado bajo independencia. Intervalos de confianza por **bootstrap agrupado por contrato**; pruebas pareadas cuando corresponda. Sin coeficiente de correlación universal; sin umbrales definitivos antes del preregistro. Los umbrales **provisionales** del Anexo C existen para que el preregistro tenga algo que sustituir.

### 9.5 Retrospectiva y medición de impacto

Un conjunto aparte de contratos previamente fiscalizados (informes de órganos de control, resoluciones de tribunales de recursos contractuales, sanciones firmes de la CNMC) permite medir cuántos hallazgos **documentales** históricos detecta el sistema, sin llamar negativos verdaderos a expedientes nunca inspeccionados. Se separan «hallazgo detectado», «riesgo corregido» y «daño evitado»: el tercero no se mide.

**Resultado primario del piloto:** proporción de discrepancias comunicadas que obtienen respuesta motivada en el plazo legal aplicable, y proporción de las que se corrigen o explican satisfactoriamente. **Secundarios:** tiempo hasta respuesta; tasa de rectificación propia; coste por expediente; carga inducida (diarios de trabajo, tiempos observables, duplicaciones, entrevistas), reconociendo expresamente los problemas de causalidad.

**Señal de alarma sobre el propio sistema:** si la mayoría de las discrepancias C2 se resuelven con «el documento existía y no estaba publicado», el sistema está midiendo publicidad, no gestión, y debe decirlo o detenerse.

### 9.6 Protocolo de publicación y derechos

- No se publican imputaciones, puntuaciones personales ni predicciones de delito.
- Todo material con posible impacto reputacional pasa control experto, jurídico y editorial; dos firmas delimitan responsabilidad, no certifican verdad.
- Réplica efectiva de las entidades afectadas (15 días hábiles por defecto), salvo remisión urgente y reservada a la autoridad competente.
- Correcciones prominentes; publicación de métodos, financiación, universo de muestra y resultados negativos.
- Protección de informantes y datos personales; licencias de documentos fuente examinadas por separado.
- Equipo rojo externo que ensaya inyección de instrucciones, falsificación, manipulación de contexto, filtraciones, reidentificación, sesgos de selección y captura, con contención y retirada temporal motivada.

### 9.7 Criterios de parada y replanteamiento

**Parada inmediata del caso** ante publicación materialmente falsa sin respaldo, exposición indebida de datos personales, filtración de informante o fallo de seguridad grave. **Suspensión del piloto** ante daño reputacional reiterado, falsos positivos graves, ausencia de responsables legales o incapacidad de financiar reparación. **Retirada de la IA** si no supera a la alternativa determinista/manual con beneficio neto demostrado (Anexo C). **Replanteamiento** si la fase 0 muestra que ya existe una solución eficaz que basta con financiar o conectar, o si la apuesta de §1 resulta falsa.

### 9.8 Entregables

1. Prototipo de una semana (§9.0). 2. Mapa legal y operativo de un sector. 3. Esquema de datos y fuentes. 4. Benchmark anotado y política de acceso. 5. Informe de comparación con/sin IA. 6. Prototipo reproducible, si procede. 7. Informe de riesgos y post-mortems. 8. Costes y réplicas de entidades. 9. Resultados desfavorables, publicados con el mismo formato que los favorables. Los recursos y plazos se presupuestan tras la fase 0.

---

## 10. Hoja de ruta que no exige crear un partido ni recibir potestades

**Fase 0 — Diagnóstico contrastable (puerta de salida).** Prototipo de una semana; mapa de competencias, cauces, deberes de respuesta, datos disponibles y lagunas. Si el fallo principal es la no aplicación de deberes existentes, priorizar su uso y publicidad sobre software nuevo. Revisión externa del mapa antes de avanzar.

**Fase 1 — Prueba determinista.** Expediente verificable usando solo registros, parseo y revisión humana; medir coste y utilidad.

**Fase 2 — Ensayo IA contra línea base.** Preregistro, benchmark, estadística, equipo rojo, evaluación RGPD y de licencias; retirar los modelos que no aporten valor.

**Fase 3 — Auditoría pública responsable.** Una entidad editora identificable decide si los resultados permiten publicar casos. Hasta entonces, el proyecto circula solo como metodología.

**Fase 4 — Adopción voluntaria y comparación institucional.** Ofrecer métodos y conjuntos de referencia a universidades, órganos de fiscalización y organizaciones cívicas; proponer auditorías cruzadas de los sistemas de analítica del Estado conforme al precedente BOSCO. La replicación por un equipo independiente vale más que el número de modelos de IA conformes.

**Fase 5 — Política pública basada en evidencia.** Las reformas de §8.6 por orden de prioridad.

**Fase 6 — Evaluación continuada y caducidad.** Auditoría externa, límites de financiación, métricas de daño y procedimiento para retirar lo que no funcione.

### Dos cosas distintas que este documento no debe confundir

1. **La propuesta operativa inicial** (§§5–9): auditoría documental de contratos, trazabilidad, seguimiento de comunicaciones, contraste con una línea base sin IA y control editorial. Es limitada, comprobable y útil por sí misma.
2. **El programa de investigación institucional de largo alcance** que inspiró el proyecto: estudiar, sector por sector, si existen fallos de transmisión, supervisión y actuación ante riesgos de alto impacto que exijan reformas de las potestades de las autoridades competentes; y, como línea futura, la evaluación a largo plazo de políticas públicas con estadística, economía causal y especialistas (los modelos de lenguaje pueden ayudar a recopilar evidencia; **no certifican efectos causales**).

El éxito de la primera **no demuestra** nada sobre la segunda, y la segunda **no es una funcionalidad futura garantizada** de la primera. Tampoco se elimina del marco por temor a una lectura hostil: no incluye veto autónomo de IA y no presupone que las soluciones sean legislativas. Quien adopte la propuesta operativa puede ignorar el programa; quien quiera el programa necesitará mucho más que este documento.

---

## 11. Preguntas pendientes antes de pedir cambios legales

1. ¿Qué fallos concretos están documentados, y de los seis tipos de §1, cuál predomina y con qué evidencia?
2. ¿Qué proporción de los datos de ejecución contractual que la LCSP obliga a recoger es realmente accesible por contrato, y qué cuesta publicarla? *(Primera respuesta parcial, limitada a la sindicación de la PLACSP y a obras de 2023: §9.0 bis.)*
3. ¿Qué tasa de cumplimiento tienen hoy los plazos de la LO 4/2001 y de la Ley 19/2013 en materia de contratación? ¿Alguien la mide?
4. ¿Qué tasa de error tiene la extracción asistida sobre documentación administrativa española, por tipo de documento y de campo?
5. ¿Son independientes los errores de métodos y modelos distintos? ¿Cuánto?
6. ¿Quién fija los umbrales de soporte y de publicación, quién puede cambiarlos y con qué procedimiento auditable?
7. ¿Qué riesgo legal y reputacional genera un registro público de comunicaciones y respuestas sobre entidades concretas, y qué seguro o fondo de reparación lo cubre?
8. ¿Cómo detectar el uso partidista selectivo, incluidas filtraciones de borradores?
9. ¿Existe alguna laguna justiciable que justifique ampliar la legitimación para recurrir en contratación? ¿Qué perjudicados no obtienen tutela hoy?
10. ¿Existe algún caso documentado en que una autoridad sectorial careciera de la potestad cautelar necesaria ante un riesgo grave? Solo si lo hay cabría estudiar una reforma sectorial específica, con resolución humana y control judicial; el veto algorítmico queda excluido en todo caso.
11. ¿Qué evidencia demostraría efectos netos sobre decisiones reales y no solo más expedientes?
12. ¿Puede una iniciativa no institucional sostenerse sin donante dominante ni voluntariado agotado?
13. ¿Qué aprender de OIReScon, CNMC, MINERVA, Arachne y Alice para no duplicar?
14. ¿Qué partes del proyecto deben abandonarse si el prototipo de una semana muestra que los datos de ejecución sencillamente no existen en fuentes públicas?

---

## 12. Invitación abierta

Este texto **no pide confianza ni obediencia a sus autores ni a sus modelos de IA**. Propone una hipótesis institucional sometida a refutación: que controles diseñados con principios de ingeniería de seguridad —y con IA solo cuando añada valor probado— pueden mejorar la trazabilidad, las respuestas y las consecuencias de los fallos públicos sin crear un nuevo poder arbitrario.

Se invita a juristas, ingenieros, estadísticos, administraciones, periodistas, organizaciones cívicas y expertos en contratación a corregir el mapa legal, refutar las métricas, proponer alternativas más baratas y medir el daño que el propio sistema pueda causar. La primera respuesta válida puede ser **«no hace falta IA»**, **«el problema no está donde se ha supuesto»** o **«esto ya lo hace alguien; financiadlo»**.

**Éxito:** menos puntos únicos de fallo; hechos más verificables; respuesta institucional medida y publicada; errores propios descubiertos y corregidos antes; y todo ello **sin** debilitar la soberanía popular, la independencia judicial ni los derechos fundamentales.

---

## Referencias y estado de verificación

**Leyenda.** C = verificado por Claude el 30-10-2026; G = verificado por ChatGPT el 30-10-2026; P = contra fuente primaria (BOE, EUR-Lex, BOCG, web oficial del organismo); S = contra fuentes secundarias independientes; — = no verificado por ese revisor. Ninguna verificación por modelos sustituye la revisión humana.

| Nº | Referencia | Enlace | C | G |
|---|---|---|---|---|
| 1 | Ley 27/2022, de institucionalización de la evaluación de políticas públicas en la AGE (BOE-A-2022-21677) | https://www.boe.es/buscar/act.php?id=BOE-A-2022-21677 | P | — |
| 2 | Real Decreto 65/2026, de 3 de febrero, Estatuto de la Agencia Estatal de Evaluación de Políticas Públicas (BOE 04-02-2026, BOE-A-2026-2553) | https://www.boe.es/eli/es/rd/2026/02/03/65/con | P | P |
| 3 | Ley 9/2017, de Contratos del Sector Público (arts. 44, 48, 63, 132.3, 150.1, 210, 240, 332, 346) | https://www.boe.es/buscar/act.php?id=BOE-A-2017-12902 | S | P (arts. 44, 48, 49, 63, 210, 240, 346) |
| 4 | Ley 19/2013, de transparencia (arts. 8, 14, 15, 20) | https://www.boe.es/buscar/act.php?id=BOE-A-2013-12887 | S | P (art. 20) |
| 5 | Ley 39/2015 (arts. 21, 56) | https://www.boe.es/buscar/act.php?id=BOE-A-2015-10565 | S | P (art. 21) |
| 6 | Ley Orgánica 4/2001, reguladora del Derecho de Petición (arts. 1–4, 8, 9, 11, 12) | https://www.boe.es/buscar/act.php?id=BOE-A-2001-21090 | S (dos fuentes institucionales) | P |
| 7 | Ley Orgánica 3/1981, del Defensor del Pueblo (art. 30) | https://www.boe.es/buscar/act.php?id=BOE-A-1981-10325 | — | P |
| 8 | Ley 29/1998, LJCA (arts. 19, 129–136) | https://www.boe.es/buscar/act.php?id=BOE-A-1998-16718 | S | P (art. 19) |
| 9 | Ley 2/2023, protección de informantes | https://www.boe.es/buscar/act.php?id=BOE-A-2023-4513 | S | P |
| 10 | Orden PJC/908/2025, puesta en funcionamiento de la AIPI el 01-09-2025 (BOE-A-2025-16764) | https://www.boe.es/boe/dias/2025/08/12/pdfs/BOE-A-2025-16764.pdf | P | — |
| 11 | Orden HFP/55/2023, análisis sistemático de conflicto de interés en el PRTR (MINERVA) (BOE-A-2023-2074) | https://www.boe.es/buscar/act.php?id=BOE-A-2023-2074 | P | — |
| 12 | OIReScon, Informe Anual de Supervisión 2025 (módulos III y IV) y Plan Plurianual 2025-2030 | https://www.hacienda.gob.es/es-ES/Oirescon/Paginas/ias.aspx | P | — |
| 13 | CNMC, informe sobre el Anteproyecto de LO de Integridad Pública (IPN/CNMC/011/26); Unidad de Inteligencia Económica y herramienta BRAVA (memorias 2024 y 2025) | https://cnmc.es/prensa/informe-APLO-integridad-20260423 ; https://www.cnmc.es/vigilamos-la-competencia/unidad-de-inteligencia-economica ; https://cnmc.es/sites/default/files/editor_contenidos/CNMC/Memorias/Executive_memory_2025_CNMC.pdf | P | P (UIE y BRAVA) |
| 14 | Proyecto de Ley Orgánica de Integridad Pública, expediente 121/000111; BOCG Serie A núm. 112-1, 11-09-2026 (urgencia; enmiendas hasta 21-09-2026, ampliaciones hasta 07-10-2026). **Decaído** al disolverse las Cortes: Real Decreto 806/2026, de 5 de octubre, BOE núm. 248, de 06-10-2026 (BOE-A-2026-20742). La ficha del Congreso conserva la fase «Enmiendas» como dato histórico | https://www.boe.es/diario_boe/txt.php?id=BOE-A-2026-20742 ; https://www.congreso.es/public_oficiales/L15/CONG/BOCG/A/BOCG-15-A-112-1.PDF ; ficha: https://www.congreso.es/es/busqueda-de-iniciativas?_iniciativas_id=121%2F000111&_iniciativas_legislatura=XV&_iniciativas_mode=mostrarDetalle&p_p_id=iniciativas&p_p_lifecycle=0&p_p_mode=view&p_p_state=normal | P (BOCG) | P (ficha) |
| 15 | Ministerio de Hacienda, nota de prensa 28-07-2026 (aprobación en segunda vuelta del Proyecto) | https://www.hacienda.gob.es/ca-es/prensa/noticias/paginas/2026/20260728-np-cm-proyecto-ley-integridad-publica.aspx | P | — |
| 16 | STS, Sala 3.ª, Sección 3.ª, 11-09-2025, rec. 7878/2024 (acceso al código fuente de BOSCO; Fundación Civio) | CENDOJ; reseña: https://www.civil-mercantil.com/node/19859 | S (dos reseñas jurídicas independientes) | — (texto íntegro pendiente) |
| 17 | Reglamento (UE) 2024/1689 (Reglamento de IA), arts. 5, 14, 27, 50, 113 y anexos I/III; versión consolidada 27-07-2026 | https://eur-lex.europa.eu/eli/reg/2024/1689/2026-07-27/eng ; arts. 14 y 27: https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-14 , .../article-27 | P (arts. 14, 27 vía Service Desk) | P |
| 18 | Reglamento (UE) 2026/1744, de 8 de julio de 2026 (Digital Omnibus on AI), DOUE L 24-07-2026; arts. 111.4 y 113 modificados | https://eur-lex.europa.eu/eli/reg/2026/1744/oj/eng ; versión en el BOE: https://www.boe.es/buscar/doc.php?id=DOUE-L-2026-81147 | P | P |
| 19 | Art. 50 del Reglamento de IA aplicable desde 02-08-2026; transición del art. 111.4 (hasta 02-12-2026) limitada al art. 50.2 para determinados proveedores | https://eur-lex.europa.eu/legal-content/ES/TXT/?uri=CELEX:02024R1689-20260727 | S | P |
| 20 | OCDE (2025), *Governing with Artificial Intelligence: The State of Play and Way Forward in Core Government Functions* | https://doi.org/10.1787/795de142-en | P | — |
| 21 | TCU/CGU (Brasil), sistema Alice | https://portal.tcu.gov.br/imprensa/noticias/tcu-ministerio-da-infraestrutura-e-dnit-firmam-acordo-para-aperfeicoar-fiscalizacao-e-prevenir-fraudes-em-licitacoes | P | — |
| 22 | Ministerio de Hacienda, datos abiertos de licitaciones de la PLACSP (sindicación ATOM, desde 2012) | https://www.hacienda.gob.es/es-ES/GobiernoAbierto/Datos%20Abiertos/Paginas/licitaciones_plataforma_contratacion.aspx | P | P |
| 23 | Open Contracting Data Standard v1.1 | https://standard.open-contracting.org/latest/en/schema/reference/ | — | P |
| 24 | NIST (2024), AI RMF: Generative AI Profile | https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence | — | P |
| 25 | Gobierno del Reino Unido, Algorithmic Transparency Recording Standard | https://www.gov.uk/government/publications/guidance-for-organisations-using-the-algorithmic-transparency-recording-standard/algorithmic-transparency-recording-standard-guidance-for-public-sector-bodies | — | P |
| 26 | AIReF, misión; Tribunal de Cuentas, Estrategia 2024-2027 | https://www.airef.es/es/mision/ ; https://www.tcu.es/es/institucion/estrategia/ | S | — |
| 27 | PLACSP, «Formato de sindicación y reutilización de datos», v1.10, 17-09-2024 | https://contrataciondelsectorpublico.gob.es/datosabiertos/especificacion-sindicacion.pdf | P | P |
| 28 | CODICE, lista TenderingNoticeTypeCode 2.11 (`DOC_CCN` «Anuncio de Finalización de Contrato»; `ANUL_CCN`) | https://contrataciondelestado.es/codice/cl/2.11/TenderingNoticeTypeCode-2.11.gc | P | P |
| 29 | Ministerio de Hacienda, datos abiertos de licitaciones alojadas en la PLACSP (ZIP 2023–2026 usados en §9.0 bis) | https://www.hacienda.gob.es/es-es/gobiernoabierto/datos%20abiertos/paginas/licitacionescontratante.aspx | P | — |
| 30 | Ministerio de Hacienda, Registro de Contratos del Sector Público (estadísticas agregadas) | https://www.hacienda.gob.es/es-es/areas%20tematicas/contratacion/junta%20consultiva%20de%20contratacion%20administrativa/paginas/registro%20publico%20de%20contratos.aspx | P | P |
| 31 | Registro de contratos del Gobierno Vasco 2023 (datos.gob.es; XLSX descargado y analizado) | https://datos.gob.es/es/catalogo/a16003011-registro-de-contratos-de-gobierno-vasco-del-2023 | P | P (ficha; XLSX no recontado) |
| 32 | opentender (GTI); Integrity Watch (TI UE); Gobierto Contratación; iMonitor | — | — (no verificado en esta ronda) | — |

**Obras citadas sin enlace:** Leveson, N. (2011), *Engineering a Safer World*; Perrow, C. (1984), *Normal Accidents*; Power, M. (1997), *The Audit Society*; Rosanvallon, P. (2006), *La contre-démocratie*.

**Normas citadas sin verificación específica en esta ronda:** Constitución Española (arts. 9.3, 18, 20, 29, 97, 103, 105, 106, 117, 136); Ley 40/2015 (arts. 41, 109–110); LO 1/1982; LO 3/2018.

---

## ANEXO A · Protocolo de revisión y registro de cambios

### A.1 Protocolo

Cada revisión debe devolver: errores fácticos o jurídicos con referencias; supuestos no probados y riesgos omitidos; posibles abusos del propio sistema; puntos poco realistas; propuestas clasificadas en imprescindibles, recomendables y opcionales; texto alternativo sin eliminar desacuerdos; preguntas abiertas que requieran especialistas humanos. Una revisión de otro modelo no prueba validez. **La ronda de revisión del texto entre modelos se dio por concluida con la v0.4.1; las rondas posteriores (Anexos A.7 a A.12) revisaron las adiciones empíricas, el protocolo y el código. El siguiente revisor debe ser humano**, en este orden sugerido: jurista de contratación pública y derecho administrativo; después estadístico o ingeniero de seguridad; después especialista en protección de datos. Se les pide en particular que comprueben si la reforma de datos de ejecución añade algo sustantivo a lo que ya se publica y si existen lagunas justiciables relevantes.

### A.2 Registro de cambios v0.1 → v0.2 (Claude)

| Nº | Sección v0.1 | Hallazgo | Cambio en v0.2 | Severidad |
|---|---|---|---|---|
| 1 | §4 Nivel 3 | «Bloqueo reglado» redundante o ilegítimo; no ataca el fallo de respuesta | Grados de evidencia, registro de advertencias, deber de respuesta y legitimación | Imprescindible |
| 2 | §2, §3.2, §5 | Redundancia entre modelos presumida | Análisis de causa común; independencia medida | Imprescindible |
| 3 | Todo | Sin modelo de amenazas | §4 nuevo | Imprescindible |
| 4 | §6 | Sin modelo de financiación | Carta de financiación | Imprescindible |
| 5 | §9 | Mapa institucional incompleto | OIReScon, IGAE, CNMC, AIPI, MINERVA, LO Integridad Pública, STS BOSCO | Imprescindible |
| 6 | §9 | Reglamento de IA sin arts. 5.1.d, 50.4 ni calendario | §8.3 | Recomendable |
| 7 | §3.2 | «Agentes» decisorios | Roles sin capacidad de certificar | Recomendable |
| 8 | §3.3 | Hecho/indicio/hipótesis sin reglas | Esquema E0–E4 | Recomendable |
| 9 | §7 | Piloto sin preregistro, referencia, equipo rojo ni métricas negativas | §9 reescrito | Imprescindible |
| 10 | §1 | Problema solo como fallo de información | Tres tipos de fallo | Recomendable |
| 11 | §8 | Sin fase de diagnóstico | Fase 0 | Recomendable |
| 12 | §11 | «Nadie pueda silenciar las advertencias» sin mecanismo | Registro de advertencias | Opcional |
| 13 | Encargo | «Evaluar políticas a largo plazo» con IA | Excluido del alcance | Recomendable |
| 14 | — | Sin análisis de incidentes propios | Capa F | Recomendable |
| 15 | — | Sin reproducibilidad | Principio 9 | Recomendable |
| 16 | — | Sin regla sobre personas físicas | Principio 6 | Imprescindible |

### A.3 Registro de cambios v0.2 → v0.3 (ChatGPT)

| Nº | Sección v0.2 | Hallazgo | Cambio v0.3 | Severidad |
|---|---|---|---|---|
| 17 | §8.3, ref. [7] | Omnibus tratado como no verificado | Reglamento (UE) 2026/1744 y calendario | Imprescindible |
| 18 | §6 | E0–E4 confunde soporte con gravedad | Ejes C/I/U | Imprescindible |
| 19 | §1 | Dominancia del fallo de respuesta sin medición | Seis fallos; fase 0 empírica | Imprescindible |
| 20 | §9 | 20–40 contratos insuficientes para tasas raras | Benchmark separado | Imprescindible |
| 21 | §9 | No se aislaba el valor de la IA | Línea base sin IA | Imprescindible |
| 22 | §6/§8 | Eliminación demasiado concluyente de potestad sectorial | Nivel D condicionado a laguna documentada | Recomendable |
| 23 | §6 | «Advertencias ignoradas» imputa | Estados observables | Imprescindible |
| 24 | Encabezado | Anonimato confundido con ausencia de editor | Entidad editora identificable | Imprescindible |
| 25 | §2/§5 | Hash confundible con verdad | Integridad ≠ exactitud | Recomendable |
| 26 | §8.4 | Legitimación y acreditación prematuras | Limitadas | Imprescindible |
| 27 | §9 | Tasas de extracción, detección y efectos mezcladas | Tres pruebas | Imprescindible |
| 28 | §7/§9 | Barreras insuficientes al uso partidista | Universo, embargo, resultados negativos | Recomendable |
| 29 | §10 | Evaluación de políticas excluida | Línea futura | Recomendable |
| 30 | Autoría | CC0 y verificación demasiado categóricas | Licencia intencional; bibliografía separada | Imprescindible |
| 31 | §9.9 | Costes sin base | Condicionados a fase 0 | Recomendable |
| 32 | §5–§7 | Control de daños insuficiente | Incidentes, retirada, datos sensibles | Imprescindible |

### A.4 Registro de cambios v0.3 → v0.4 (Claude)

| Nº | Sección v0.3 | Hallazgo | Cambio v0.4 | Severidad | Estado |
|---|---|---|---|---|---|
| 33 | §6.3, §8.2 | Omitido el derecho de petición (LO 4/2001): el deber de respuesta ya existe | Cauce ordinario de comunicación; §8.2 reescrita; propuesta de «entidades acreditadas» retirada | Imprescindible | Cotejar texto legal en BOE |
| 34 | §1 | Ninguna apuesta falsable | Apuesta explícita H0 con condición de refutación | Imprescindible | Abierta a evidencia |
| 35 | §9 | Sin parámetros numéricos | Anexo C de parámetros provisionales | Imprescindible | Sustituir en preregistro |
| 36 | §6 | C/I/U sin reglas de publicación | §6.1 bis matriz; plazo de réplica por defecto | Imprescindible | — |
| 37 | §6.3 Nivel D | Reforma cautelar sectorial dentro de la arquitectura invita a lectura hostil | Movida a §11, pregunta 10; contenido intacto | Recomendable | — |
| 38 | §9 | Sin acción inmediata posible | §9.0 prototipo de una semana sin IA | Imprescindible | — |
| 39 | §8.6 | Reformas sin concreción legal | Enmienda concreta: publicar por contrato lo comunicado al Registro (art. 346) + pagos + recepción | Imprescindible | Cotejar arts. 63.3 y 346 |
| 40 | Referencias | Fuentes verificadas rebajadas a «heredadas» | Tabla con estado de verificación por revisor | Recomendable | — |
| 41 | §8.4 | BOSCO como «pendiente de cotejo» | Verificada en fuentes secundarias independientes; texto íntegro pendiente | Opcional | — |
| 42 | §8.1 | «En fase de enmiendas» | Urgencia; plazo inicial 21-09-2026; estado a comprobar | Recomendable | — |
| 43 | §8.5 | Art. 50 sin fecha | No aplazado; marcado hasta 02-12-2026 (fuentes secundarias) | Recomendable | Cotejar transitorias |
| 44 | §8.4 | Datos de autónomos sin regla operativa | Regla de la ficha pública y cruces restringidos | Recomendable | Validar RGPD |
| 45 | §6.4 | Urgencia sin procedimiento | Guardia humana, canales de emergencia existentes, sin envío automático | Recomendable | — |
| 46 | §9.5 | Sin resultado primario | Resultado primario de proceso; «daño evitado» excluido | Imprescindible | — |
| 47 | §9.1 | Gold standard sin tratamiento de acuerdos erróneos | Auditoría del 100 % de desacuerdos y muestra de acuerdos | Recomendable | — |
| 48 | §9.5 | Sin señal de alarma sobre medir publicidad y no gestión | Añadida | Recomendable | — |

### A.5 Fe de erratas v0.4 → v0.4.1 (revisión final de ChatGPT, aplicada por Claude)

| Nº | Sección v0.4 | Error o imprecisión | Corrección v0.4.1 | Fuente |
|---|---|---|---|---|
| 49 | §6.3, §8.2 | El derecho de petición presentado como cauce ordinario para toda discrepancia C2+ | Clasificación por finalidad: acceso documental (Ley 19/2013), indicios (canal sectorial), actuación general sin cauce específico (LO 4/2001, arts. 3 y 8); se mide la admisibilidad antes que la respuesta | LO 4/2001, BOE-A-2001-21090 |
| 50 | §8.5, ref. 19 | «Plazo de gracia» del art. 50 descrito de forma imprecisa | La transición del art. 111.4 (hasta 02-12-2026) afecta solo al art. 50.2 de ciertos proveedores; el art. 50.4 se aplica desde 02-08-2026 | Reglamento 2026/1744; consolidado 02024R1689-20260727 |
| 51 | §8.6 | «No crea obligaciones nuevas de recogida, solo de publicación» y «el Registro no publica», demasiado categóricos; art. 63.1 ya exige formatos reutilizables; arts. 346.3 y 346.5 | Redacción prudente: publicación sistemática e interoperable de lo ya comunicado al Registro; estudio separado de certificaciones (art. 240), pagos y recepción (art. 210); cobertura medida en fase 0 | LCSP arts. 63, 210, 240, 346 |
| 52 | §8.1, §8.6 | Estado del expediente 121/000111 citado solo por el BOCG inicial; enmienda tratada como vía disponible | Ficha del Congreso: «Enmiendas», ampliaciones hasta 07-10-2026; encaje de la enmienda como oportunidad a verificar | Ficha del Congreso |
| 53 | §9.0 | Una semana no permite medir tasas de respuesta | Semana de arranque (envíos y acuses) separada del seguimiento al vencer los plazos; distinción admitida/inadmitida y motivo | Plazos de Ley 19/2013 y LO 4/2001 |
| 54 | §1, §9.2 | H0 no identificable: compara respuesta y detección con la misma muestra | Desdoblada en H0a (cohorte de comunicaciones) y H0b (muestra independiente auditada), con poblaciones distintas | Análisis metodológico |
| 55 | §6.4, Anexo C | 24 horas presentadas como tiempo de reacción ante riesgo inminente | Escalamiento inmediato por canal sectorial; las 24 horas son plazo de documentación; el protocolo no es un sistema de emergencias | Análisis de seguridad |
| 56 | §8.4 | Regla sobre autónomos daba por válido el interés legítimo | Reducción de exposición ≠ ausencia de tratamiento; base jurídica y evaluación de impacto por especialistas | RGPD |
| 57 | §9.0 | «Administraciones de distinto signo político» como criterio de muestra | Muestra por sector, territorio, tamaño y nivel; clasificación política solo documentada para control de sesgos | Propuesta |
| 58 | §10 | Propuesta operativa y programa de largo alcance sin separar | Sección «Dos cosas distintas» en §10 | Diseño |
| 59 | Nota sobre esta versión, punto 1 | Resumen del derecho de petición más amplio que el cuerpo (reserva de la verificación final de ChatGPT) | Redacción ajustada a admisión, competencia y residualidad | LO 4/2001 |
| 60 | §8.1 | La CNMC «ha anunciado» algoritmos: en realidad opera BRAVA desde hace años y desarrolla ATENEA (hallazgo de la búsqueda de destinatarios) | Añadida descripción de BRAVA como analítica dentro de un supervisor | Memoria CNMC 2024 y 2025; web de la Unidad de Inteligencia Económica |

---

### A.6 Cambios v0.4.1 → v0.4.2 (primer resultado de la fase 0)

| Nº | Sección | Cambio | Motivo | Fuente |
|---|---|---|---|---|
| 61 | Nota sobre esta versión | Párrafo v0.4.2 | Resumir el resultado empírico | §9.0 bis |
| 62 | §8.1 | Herramientas de detección de riesgos fuera del Estado; el documento no propone otra | No duplicar lo existente | Ref. 32 (no verificada en esta ronda) |
| 63 | §8.6 | Primera medición de cobertura; existencia de `DOC_CCN` y del registro vasco; reforma como «uso sistemático de cauces existentes», propuesta a estudiar | Resultado de la fase 0 | Refs. 27–31 |
| 64 | §9.0 bis (nuevo) | Resultado, hallazgo, contraste, validación y límites | Fase 0 ejecutada en parte | Repositorio del estudio |
| 65 | §11.2 | Remisión a la primera respuesta parcial | — | §9.0 bis |

### A.7 Cambios v0.4.2 → v0.4.3 (usos y correcciones de precisión)

| Nº | Sección | Cambio | Motivo | Fuente |
|---|---|---|---|---|
| 66 | §3 bis (nuevo), Resumen ejecutivo, Nota para las organizaciones | Para qué serviría el protocolo y a quién, con condiciones, riesgos y lo que no conseguiría; §3 bis entre las lecturas recomendadas | El documento explicaba el «cómo» y sus límites, pero no qué se ganaría | Propuesta del intermediario; redacción de Claude |
| 67 | Nota sobre esta versión, §3 bis, §8.6, §9.0 bis | Formulación homogénea del 98,7 %: numerador, denominador, corte, canal, «indicadores de finalización o extinción», qué no permite concluir | Evitar que se lea como ausencia de documentos | Revisión de ChatGPT (01/11/2026), punto 1 |
| 68 | §9.0 bis | `ANUL_CCN`: cómo se trata y 0 anulaciones en el corpus; tres pruebas automatizadas nuevas en el programa | Trazar la vigencia de los 8 anuncios | Ídem, punto 2; repositorio |
| 69 | §9.0 bis | «Validación» pasa a «Revisión realizada»: rondas con un mismo sistema, alcance de la revisión de Gemini, sin valor de auditoría | No sugerir revisores independientes | Ídem, punto 3 |
| 70 | §9.0 bis | Desglose de los 20 casos: 7 terminaciones ordinarias con su documento y 13 resoluciones (una parcial por lotes); la cifra mide finalización o extinción | No confundir «contrato extinguido» con «obra recibida» | Ídem, punto 4; `revision_manual_candidatos_v2_2.csv` |
| 71 | §3 bis | Plazo de acceso: máximo legal de un mes, ampliable, no espera mínima | Error de hecho | Ídem, punto 5; Ley 19/2013, art. 20.1 |
| 72 | §9.0 bis | Reproducción: URL del repositorio, licencias, datos no redistribuidos con script y huellas, huella SHA-256 del programa, diferencia entre reproducir y repetir | Que el artefacto sea localizable y verificable | Ídem, punto 6 |
| 73 | Portada, historial, Nota para las organizaciones, cierre | Versión coherente; se retira «sin formación jurídica ni técnica» del intermediario | Coherencia; no presuponer datos personales | Ídem, punto 7 |

### A.8 Cambios v0.4.3 → v0.4.4 (corrección de la cifra, investigaciones complementarias y protocolo de obras)

| Nº | Sección | Cambio | Motivo | Fuente |
|---|---|---|---|---|
| 74 | Nota sobre esta versión, §8.6, §9.0 bis | Cifra principal: 1.573 (98,7 %) → **1.549 (97,2 %)**. El programa (versión 2.4) lee también el texto de las modificaciones, donde algunos órganos comunican la liquidación o la certificación final | Falso negativo sistemático descubierto al investigar las modificaciones; 24 casos revisados a mano | `investigacion_modificaciones/INFORME_MODIFICACIONES.md`; `fase0_placsp/METODO.md` |
| 75 | §9.0 bis | Huella del programa v2.4; se conserva la de la v2.3. Límite de las muestras manuales reformulado | Reproducibilidad; no sobrestimar las validaciones | Ídem |
| 76 | §9.0 ter (nueva) | Resumen de ocho investigaciones complementarias, dos de ellas preregistradas | Responder a las preguntas abiertas por la fase 0 antes de proponer cambios | Informes de cada carpeta del repositorio |
| 77 | §8.6 | Se añade que publicar el fin no figura en el art. 63.3 LCSP y que el registro vasco tiene cobertura incompleta | Precisión jurídica y empírica | `investigacion_juridica/`, `investigacion_registro_vasco/` |
| 78 | Anexo D (nuevo) | Diseño del protocolo de preguntas sobre el fin de las obras: reglas, volumen, órganos de garantía, riesgos y herramientas | Convertir los hallazgos en un procedimiento que una organización pueda adoptar | `protocolo_obras/PROTOCOLO_OBRAS.md`; redacción de Claude |
| 79 | Portada, historial, Anexo B, cierre | Versión coherente y estado de la revisión | Transparencia | — |
| 80 | §9.0 bis | Patrón del fin en el texto en dos niveles (confirmado / candidato); revisión de los 24 casos conservada; concentración (22 de 24 en un órgano); la cifra como métrica del clasificador; huella nueva del programa | Falsos positivos semánticos posibles (P1) y validez externa (P2) | Revisión adversarial de ChatGPT, 02/11/2026; `revision_manual_fin_en_nota_v2_4.csv` |
| 81 | Nota sobre esta versión | La cifra vigente encabeza; la de la v2.3 queda como historia | Claridad (punto 2) | Ídem |
| 82 | §9.0 ter | Formulaciones matizadas: tiempo observado (2), muestra estratificada (3), documentos «cuando se produce la fase» y obligación de comunicar «en los supuestos que fija la ley» (4), «resoluciones examinadas» y denominador de reclamaciones (5), umbral analítico (6), «escasa capacidad discriminatoria» y sesgo no contrastado (7), indicador de calidad informativa y fecha no verificada (8); fecha de preregistro declarada | Evitar formulaciones categóricas (P3–P5) | Ídem |
| 83 | Anexo D | Plazos desde la recepción por el órgano, con días inhábiles y provisionales; tope mensual común a todos los lotes, exclusión de lo ya preparado, cerrojo; seguimiento de la muestra; 120 días como umbral operativo; plantilla con documentos concretos; garante sugerido; exportación como borrador; ±7 condicional | Defectos bloqueantes para uso real (P6, P7) e importantes (P8–P13) | Ídem; `protocolo_obras/` v0.2 |

### A.9 Cambios v0.4.4 → v0.4.5 (señal de posible terminación anticipada; sin revisión adversarial)

| Nº | Sección | Cambio | Motivo | Fuente |
|---|---|---|---|---|
| 84 | §9.0 ter, punto 9 (nuevo) | Señal «terminación licitada de nuevo»: qué hace, validación preregistrada con obras de final conocido (3,7 % frente a 0,4 %; cociente 10,2), sensibilidad de en torno al 4 %, retraso, comprobación de 20 obras en la web | Única señal positiva validada de un problema de ejecución en los datos abiertos | `investigacion_terminacion/INFORME_TERMINACION.md`; la regla procede de una revisión manual de obras ajena al estudio |
| 85 | Anexo D.4 y D.6 | Criterio de prioridad opcional `--prioridad terminacion`, columna de aviso en cada lote y guía para refinar la señal | Dejarla lista para usarla y mejorarla con el mismo método | `protocolo_obras/senal_terminacion.py`, `SENAL_TERMINACION.md` |
| 86 | Portada, historial, Nota, Anexo B, cierre | Versión coherente; se declara que la v0.4.5 no ha pasado revisión adversarial | Transparencia | — |
| 87 | §9.0 ter punto 5; Anexo D.1 regla 6 | Órganos de garantía autonómicos: precedentes favorables en dos órganos revisados de forma sistemática, con cautelas; el plazo para reclamar contra el silencio varía según el órgano | El 58 % de las reclamaciones del protocolo irían a órganos autonómicos | `investigacion_consejo/COMPLEMENTO_AUTONOMICO.md` (búsqueda de la consulta privada; dos citas verificadas) |
| 88 | Anexo D.6 | Interfaz gráfica con pestaña del protocolo; el ciclo mensual acepta la prioridad por la señal; el informe legible del estudio reconoce el fin indicado en notas de modificación (antes fallaba con los resultados v2.4) | Que las organizaciones puedan usar todo sin terminal; coherencia con la v2.4 | `fase0_placsp/interfaz.py`, `informe_legible.py`; `protocolo_obras/ciclo_mensual.py`, `test_protocolo.py` |

### A.10 Cambios v0.4.5 → v0.4.6 (revisión adversarial de ChatGPT de la v0.4.5)

| Nº | Sección | Cambio | Motivo | Fuente |
|---|---|---|---|---|
| 89 | §9.0 ter, punto 9; Nota | «Validación» pasa a «asociación preregistrada en un corpus parcialmente expuesto al diseño»; grupos documentales operativos; fuera «muy fiable», «muy específica» y «4 % de las resoluciones»; coincidencia que obliga a verificar | Revisión: la regla se diseñó viendo dos de los tres tramos de la tabla principal; el único tramo independiente no es concluyente | `investigacion_terminacion/INFORME_TERMINACION.md` |
| 90 | §9.0 ter, punto 9 | 66 órganos (no 69); universo de 44.290 con la definición v2.4 | Recálculo al responder a la revisión: el informe contó nombres en vez de identificadores | Ídem |
| 91 | §9.0 ter, punto 5; Anexo D.1 regla 6 | Plazos según la ley aplicable (20 días hábiles en Madrid, Murcia y la Junta de Andalucía; 30 en Extremadura; reclamación contra el silencio sin plazo en Cantabria, Navarra y el País Vasco) | Revisión: el protocolo aplicaba un mes a todos | Textos consolidados del BOE; `protocolo_obras/regimenes.py` |
| 92 | §9.0 ter, punto 5 | El 58 % son solicitudes potenciales, no reclamaciones; recuento estricto de casos autonómicos (2 y 7), sin desestimaciones de fondo; filtro reproducible | Revisión: denominador mal descrito; los 11 casos incluían un suministro y un desistimiento | `investigacion_consejo/COMPLEMENTO_AUTONOMICO.md` |
| 93 | §9.0 bis; repositorio | Se retiran las listas de obras con su órgano y las revisiones caso por caso; se publican las huellas de los ficheros por expediente, verificadas con una repetición completa | Coherencia con la regla de no señalar órganos | `fase0_placsp/huellas_resultados.py` |
| 94 | Anexo D.1, D.4 y D.6 | Tope sin «sin tope»; muestra persistente y sorteada antes de la prioridad; registro robusto ante fechas mal escritas; ciclo que no avanza con errores y se reanuda; festivos en todo el ciclo; exportación sin identificadores; origen de cada solicitud; se retira la «reserva aleatoria» que no existía | Fallos reproducidos de la revisión | `protocolo_obras/test_revision_v045.py` |
| 95 | Portada, historial, Nota, §9.0 ter, Anexo B, cierre | Versión coherente; se aclara qué ronda revisó cada investigación | Revisión: el texto decía que las nueve habían pasado revisión | — |

### A.11 Cambios v0.4.6 → v0.4.7 (revisión adversarial de ChatGPT de la v0.4.6)

| Nº | Sección | Cambio | Motivo | Fuente |
|---|---|---|---|---|
| 96 | Anexo D.1 regla 6; §9.0 ter, punto 5 | Ampliación por régimen: quince días hábiles en el País Vasco; en Cataluña, hasta la mitad del plazo (sin cómputo automático); sin ampliación en la ley gallega | Revisión (País Vasco); la de Cataluña la encontró la comprobación de las demás leyes | Ley 3/2026 de Euskadi, art. 37.2; Ley 19/2014 de Cataluña, art. 33.2 |
| 97 | Anexo D.1 regla 6; §9.0 ter, punto 5 | Plazo del órgano de garantía por régimen: dos meses en Cataluña, con mediación que suspende; seguimiento manual donde no consta | Revisión: se aplicaban tres meses a todos | Ley 19/2014 de Cataluña, art. 42.9 |
| 98 | Anexo D.1 regla 6 | Una ampliación solo cuenta si se notificó antes del vencimiento ordinario y de la respuesta | Revisión: se aceptaban ampliaciones retroactivas | `protocolo_obras/registro.py` |
| 99 | Anexo D.1 regla 6 | Festivos por comunidad o por órgano | Revisión: un único calendario para órganos de sitios distintos | Ídem |
| 100 | Anexo D.1 regla 6; D.6 | «En plazo» y las cifras de plazos, solo con la fecha límite verificada a mano | Revisión: suspensiones, recepción y calendario no verificados | Ídem |
| 101 | Anexo D.6 (`regimenes.py`) | Fuentes de Castilla y León y de Castilla-La Mancha (ley estatal); Galicia local, ley estatal; artículo de ámbito local citado en cada fila | Revisión (las dos primeras); Galicia, comprobación del ámbito de todas las leyes | Textos consolidados del BOE |
| 102 | §9.0 ter, punto 5 (complemento autonómico) | Se citan resoluciones públicas como precedentes de un criterio; la lista de casos clasificados deja de publicarse | Revisión: la lista permitía identificar administraciones | `investigacion_consejo/COMPLEMENTO_AUTONOMICO.md` |
| 103 | Portada, estado, historial, Nota, Anexo B, Anexo D (versión 0.4), D.6, cierre | Versión coherente y número de pruebas | — | `protocolo_obras/test_revision_v046.py` |

### A.12 Cambios v0.4.7 → v0.4.8 (revisión adversarial de ChatGPT de la v0.4.7)

| Nº | Sección | Cambio | Motivo | Fuente |
|---|---|---|---|---|
| 104 | Anexo D.6 (`registro.py`) | La validación no se interrumpe con una fecha de ampliación mal escrita (Cataluña y Galicia) | Revisión: excepción en `validar` | `protocolo_obras/test_revision_v047.py` |
| 105 | Anexo D.1 regla 6 | Error si la ampliación se notificó antes de la recepción por el órgano; aviso, no error, si es posterior al vencimiento provisional (puede haber suspensión) | Revisión: aceptaba lo primero y rechazaba ampliaciones válidas | Ídem |
| 106 | Anexo D.1 regla 6 | Un silencio solo es «fuera de plazo» cuando vence la fecha verificada; error si se anota antes | Revisión: la exportación lo calificaba antes de vencer | Ídem |
| 107 | Anexo D.1 regla 6 | Error si la fecha límite verificada es anterior a la recepción por el órgano | Revisión | Ídem |
| 108 | Anexo D.6 | Aviso de festivos cuyo ámbito no coincide con ninguna fila | Revisión: una comunidad sin tilde se ignoraba sin avisar | Ídem |
| 109 | Nota, Anexo B; complemento autonómico | Rutas a `revisiones/`; solo llevan número las resoluciones citadas como precedente | Revisión: rutas inexistentes en el repositorio | `investigacion_consejo/COMPLEMENTO_AUTONOMICO.md` |
| 110 | §9.0 bis; repositorio | La reproducción remite al repositorio único (`democracia-auditable`) y ya no dice que publica la clasificación manual de cada caso | Coherencia con la retirada de las listas (v0.4.6) | — |
| 111 | Repositorio | Documento de presentación breve, de tres páginas y con el aspecto del documento completo: el problema, el protocolo en cinco pasos, qué se pretende conseguir, la primera aplicación a obras públicas, salvaguardas y estado | Formato propuesto por la revisión; texto elegido por el autor y contrastado con este documento | `documento/Democracia_Auditable_resumen_v0_4_9.md` |
| 112 | Anexo D.6 (`PROTOCOLO_OBRAS.md`) | La coincidencia de terminación deja de describirse como «validada» que «capta en torno al 4 % de las resoluciones»: marcó el 3,7 % del grupo documental R estudiado (10 de 273), no extrapolable | Detectado por el autor: quedaba una formulación anterior a la v0.4.6 | `protocolo_obras/SENAL_TERMINACION.md` |
| 113 | §9.0 bis, Anexo A.1, A.9 y D (estado); método, informes del Consejo, notas de envío | Rondas de revisión del estudio contadas igual que en el método; la ronda entre modelos «concluida con la v0.4.1» se matiza; filas del A.9 en orden; estado del Anexo D con la revisión de la v0.4.7; referencias a ficheros no publicados marcadas como tales; registro de la comprobación de huellas; asunto a medios acotado a su población | Pasada de coherencia con Fable (modelo de IA de la misma familia que el redactor; no es una revisión independiente) | — |

### A.13 Cambios v0.4.8 → v0.4.9 (corrección editorial de publicación)

| Nº | Sección | Cambio | Motivo | Fuente |
|---|---|---|---|---|
| 114 | §8.1, §8.6, referencia 14, Anexo B | El Proyecto de Ley Orgánica de Integridad Pública pasa de «en tramitación» y posible vía de enmienda a antecedente decaído; la agencia que preveía, de «futura» a organismos de reformas futuras | Revisión editorial de ChatGPT (02/11/2026), comprobada en el BOE: las Cortes se disolvieron el 06/10/2026. Las filas 42 y 52 del Anexo A registran lo que se comprobó entonces y no se reescriben | Real Decreto 806/2026, BOE-A-2026-20742 |
| 115 | Estudio (`fase0_placsp/METODO.md`, `README.md`) | Se quitan dos menciones a un expediente concreto; se corrige el enlace a la licencia | Coherencia con la regla de no destacar casos individuales; enlace roto | — |
| 116 | Portada, historial, Nota, cierre; presentación breve | Versión 0.4.9 | — | — |

## ANEXO B · Estado de la revisión

La ronda de revisión del **texto** entre modelos de IA concluyó con la v0.4.1. La v0.4.2 no es una ronda nueva: añade un resultado empírico cuyo **estudio** pasó tres rondas de revisión adversarial con ChatGPT (ver repositorio). La v0.4.3 añade una sección nueva (§3 bis) y las correcciones de precisión de una revisión de ChatGPT; la §3 bis fue redactada por Claude y revisada en esa misma ronda. La v0.4.4 corrige la cifra de la fase 0 y añade la §9.0 ter y el Anexo D, redactados por Claude y revisados por ChatGPT en una ronda adversarial (02/11/2026). Sus correcciones están aplicadas (Anexo A.8); la respuesta punto por punto se conserva junto a este texto. Las herramientas del Anexo D siguen **sin validación jurídica** y no deben usarse con solicitudes reales sin supervisión. La v0.4.5 añadió el punto 9 de la §9.0 ter y la prioridad por la coincidencia de terminación; la revisión adversarial de ChatGPT de la v0.4.5 (02/11/2026) los revisó junto con las herramientas, y sus correcciones están en la v0.4.6 (Anexo A.10; respuesta punto por punto en `revisiones/v0_4_5/`). Su veredicto: el documento es distribuible como **borrador crítico**, y el protocolo **no es apto para solicitudes reales** hasta una revisión jurídica. La revisión de la v0.4.6 (02/11/2026) comprobó esas correcciones con el repositorio completo (114 pruebas superadas) y encontró defectos nuevos en el cálculo de plazos, corregidos en la v0.4.7 (Anexo A.11; respuesta punto por punto en `revisiones/v0_4_6/`); mantuvo el mismo veredicto. La revisión de la v0.4.7 (140 pruebas superadas) encontró fallos de validación del registro, corregidos en la v0.4.8 (Anexo A.12), y concluyó que no hace falta ampliar la investigación ni rehacer el documento. Las dos partes coinciden en que una nueva reescritura por modelos aportaría coincidencia, no verdad. Los documentos de cada ronda (críticas, respuestas, revisión final) se conservan junto a este texto para que cualquier revisor humano pueda ver qué se discutió, qué se aceptó y qué se rechazó.

**Puntos que los modelos dejan expresamente abiertos para la revisión humana:** si la reforma de datos de ejecución añade algo sustantivo a lo que ya se publica (§8.6); si existen lagunas justiciables que justifiquen ampliar la legitimación (§11.9); la base jurídica del tratamiento de datos de adjudicatarios personas físicas (§8.4); la vía legislativa adecuada para proponer una reforma futura, una vez decaído el expediente 121/000111; y el diseño estadístico de la fase 0 (§1, §9).

---

## ANEXO C · Parámetros provisionales

Todos los valores de esta tabla son **provisionales y arbitrarios**: existen para que el preregistro tenga algo que sustituir, no porque estén justificados. Quien adopte el protocolo debe fijarlos con un estadístico y un jurista y publicar la justificación.

| Parámetro | Valor provisional | Dónde se usa |
|---|---|---|
| Exactitud mínima por campo (extracción asistida vs. validación ciega) | ≥ 95 % global; ≥ 90 % en cada estrato de tipo de documento | §9.1 B, §9.4 |
| Tasa máxima de afirmaciones sin anclaje real | 0 % en publicaciones; ≤ 1 % en extracción interna | §6.1 bis |
| Reducción mínima de tiempo humano para mantener la IA en una función | ≥ 30 % frente a la línea base, con exactitud igual o mejor y sin errores graves nuevos | §9.2 H1, §9.7 |
| Falsas alarmas máximas en el conjunto retrospectivo | ≤ 10 % | §9.5 |
| Hallazgos documentales históricos detectados | ≥ 60 % | §9.5 |
| Plazo de réplica por defecto antes de publicar C2+ | 15 días hábiles, ampliable a petición | §6.1 bis |
| Plazo máximo para documentar y revisar el encaminamiento de un ítem I3/U3 (el escalamiento humano es inmediato) | 24 horas | §6.4 |
| Rectificaciones por error propio que suspenden el piloto | > 2 en fichas C2+ | §9.7 |
| Porcentaje máximo de un solo financiador | 20 % del presupuesto anual | §7.3 |
| Tamaño inicial del benchmark | 300 documentos/contratos; 2.000–3.000 instancias de campo; definitivo por cálculo de potencia | §9.1 B |
| Tamaño del ensayo operativo | 20–40 contratos | §9.1 C |
| Tamaño del prototipo de arranque | 30 contratos, 1 sector, 1 año; 3 solicitudes de acceso + hasta 3 peticiones admisibles; seguimiento de 1 a 3 meses | §9.0 |

---

## ANEXO D · Protocolo de preguntas sobre el fin de las obras (diseño)

**Estado:** diseño de la versión 0.4, del 2 de noviembre de 2026, para un **piloto**, no una herramienta jurídica operativa. **No se ha enviado ninguna solicitud ni lo ha revisado un jurista, y no es apto para solicitudes reales sin esa revisión** (plazos, órgano de garantía y plantillas). La versión 0.4 incorpora la revisión adversarial de la v0.4.6: ampliación y plazo del órgano de garantía según la ley, ampliaciones solo si se notificaron a tiempo, festivos por comunidad u órgano y calificación «en plazo» solo con la fecha límite verificada por una persona; y, tras la revisión de la v0.4.7, una validación del registro que distingue errores de avisos, rechaza ampliaciones y fechas verificadas anteriores a la recepción, no califica un silencio «fuera de plazo» antes del vencimiento verificado y avisa de festivos sin fila. La versión 0.3 incorporó la revisión adversarial de la v0.4.5: plazos según la ley aplicable, tope sin la opción «sin tope», muestra persistente, registro que no se rompe ni avanza con errores, reanudación y exportación sin identificadores por defecto. La versión 0.2 incorporó la revisión de la v0.4.4: plazos con días inhábiles, control de duplicados y tope mensual entre lotes, seguimiento de la muestra, plantilla más precisa y exportación como borrador. El detalle, las plantillas, las herramientas y sus pruebas están en `protocolo_obras/` del repositorio.

**Objetivo.** Aplicar a las obras públicas la idea central del documento: que una pregunta se haga una vez y su resultado quede a disposición de todos. La §9.0 ter muestra que el dato falta en los datos abiertos, que existe por ley y que el Consejo de Transparencia lo considera público.

### D.1 Reglas

1. **Qué obras.** Expedientes de obras adjudicados de **1 M€ o más** (presupuesto base sin IVA), sin anuncio de finalización ni otro indicador de fin en la PLACSP, incluido el texto de sus modificaciones. «Obra» significa aquí expediente, que puede contener varios contratos o lotes.
2. **Cuándo.** A partir de **120 días después del fin teórico estimado**. Es un **umbral operativo de contacto, no un plazo legal ni un indicador de retraso**: la certificación final se cuenta desde la recepción real (art. 243.1), que puede ser muy posterior al fin estimado. «La obra aún no se ha recibido» es una respuesta legítima.
3. **Qué se pide.** Copia del **acta de recepción** y de la **certificación final**, si existen. Si las obras no se han recibido, que se diga así y se entreguen, solo si existen y por este orden: el acuerdo de resolución, el último acuerdo de suspensión o de ampliación de plazo y el acta de comprobación del replanteo. Nunca certificaciones periódicas. Se piden documentos existentes, no información elaborada (art. 18.1.c de la Ley 19/2013).
4. **A quién.** Al órgano de contratación. Si no tiene los documentos, debe remitir la solicitud a quien los tenga (art. 19.1).
5. **Una sola vez y con tope.** Una solicitud por expediente, nunca repetida, y como máximo **4 por órgano y mes**, contando todos los lotes preparados del mes y los envíos registrados. Las herramientas excluyen lo ya registrado o preparado, usan un cerrojo e impiden sobrescribir un lote; no admiten un tope de cero («sin tope»), y uno mayor que 4 exige una justificación escrita en el lote. Entre organizaciones hace falta un registro compartido. El Consejo ha considerado abusivo pedir repetidamente documentos parciales de una misma obra. El tope reduce la carga, pero **no es un salvoconducto frente al abuso de derecho**.
6. **Silencio.** El plazo para resolver **depende de la ley aplicable** y se cuenta desde la recepción por el órgano competente: en general, un mes, ampliable a dos (Ley 19/2013, art. 20.1); 20 días hábiles en la Administración de Madrid y de Murcia y en la Junta de Andalucía; 30 días hábiles en Extremadura. La ampliación depende también de la ley (quince días en el País Vasco, hasta la mitad del plazo en Cataluña) y solo cuenta si se notificó antes del vencimiento ordinario y de la respuesta. Si el último día es inhábil, el siguiente hábil (Ley 39/2015, art. 30.5). Las herramientas anotan el régimen de cada obra (comunidad y ámbito; tabla con la cita del BOE en `protocolo_obras/regimenes.py`), dan vencimientos **provisionales** para avisar (sábados, domingos y festivos nacionales; los autonómicos y locales se añaden para todas las filas, una comunidad o un órgano) y **no calculan ninguna fecha si el régimen no está verificado** o la ampliación no se puede calcular con seguridad. No conocen las suspensiones. Por eso **una respuesta solo se califica «en plazo» o «fuera de plazo» con la fecha límite que una persona verifica y anota** (recepción real, calendario del lugar, suspensiones y ampliación), y solo esas filas entran en las cifras de plazos. Si vence sin respuesta, se reclama **dentro del mes siguiente**, como **criterio prudencial**: ninguno de los regímenes revisados da menos de un mes para reclamar, y en Cantabria, Navarra y el País Vasco la ley no pone plazo contra el silencio. Todo ello es una lectura de un no jurista.
7. **Registro y publicación.** Se registra cada paso (envío, recepción por el órgano, respuesta, documentos, fechas de replanteo y recepción, reclamación, resolución y cumplimiento). La exportación es un **borrador** y, por defecto, **sin identificadores de obra ni de órgano**; incluirlos es una decisión editorial expresa. Antes de publicar cualquier versión hace falta una revisión de privacidad caso por caso, porque enlaces y fechas pueden permitir identificar a personas en los documentos enlazados. Los documentos recibidos solo se publican tras disociar los datos personales.

### D.2 Volumen y arranque

- **Volumen anual** (medido con los datos de 2025): unas **1.840 solicitudes al año** para las obras de 1 M€ o más, repartidas entre unos 590 órganos.
    - La mitad de los órganos recibiría **una al año**, y el 90 %, cinco o menos.
    - Con el tope de 4 al mes, solo el 3 % de las preguntas se retrasaría más allá del año.
    - Incluir las obras de menos de 1 M€ multiplicaría el volumen por diez.
- **Arranque:** al empezar hay unas **8.700 obras acumuladas** sin fin publicado. La propuesta es preguntar cada mes por las nuevas (unas 150–270) y, de las acumuladas, solo por una **muestra aleatoria fija de 200**, que se completa en varios meses porque comparte el tope. **Solo bajo muestreo aleatorio simple y con respuesta completa** daría un margen de unos ±7 puntos; con aplazamientos, falta de respuesta y cambios de elegibilidad será mayor. El marco de la muestra se congela y cada lote registra el estado de cada una de las 200 (preguntada, aplazada, excluida y por qué, o desaparecida), para que el denominador no cambie sin constancia.

### D.3 A quién se reclama

| Órgano requerido | Órgano de garantía |
|---|---|
| Administración General del Estado y sector público estatal | Consejo de Transparencia y Buen Gobierno |
| Asturias, Cantabria, Extremadura, Illes Balears, La Rioja, Ceuta y Melilla, y sus entidades locales | Consejo de Transparencia y Buen Gobierno, por convenio |
| Resto de comunidades autónomas y sus entidades locales | Órgano de garantía propio de cada comunidad |

Situación de los convenios publicada por el Consejo, consultada el 01/11/2026. Las herramientas proponen el órgano de garantía como **«sugerido, sin verificar»** a partir del tipo de entidad y la provincia del órgano; la ubicación no siempre determina la adscripción, así que hay que verificarlo antes de cada reclamación.

### D.4 Prioridad entre obras

Si el tope obliga a aplazar preguntas, el orden por defecto es la **antigüedad**. Pueden declararse otros criterios: importe, materia vinculada a la seguridad de las personas, financiación europea o, desde la v0.4.5, la **señal de posible terminación anticipada** de la §9.0 ter, punto 9 (`--prioridad terminacion`; cada lote indica en una columna qué licitación la provoca). Esta coincidencia obliga a verificar, pero su ausencia no informa de nada y sus proporciones no son trasladables (§9.0 ter, punto 9): adelanta unas pocas preguntas, sin decir nada de las demás obras ni de ningún órgano. Tres condiciones:

1. **Ordenan, no excluyen:** toda obra acaba recibiendo su pregunta.
2. **Se declaran antes de aplicarse.** El flujo mensual no reserva una parte aleatoria: si va priorizado, sus cifras describen lo preguntado, no la población. Las proporciones de todas las obras se estiman solo con la muestra fija aleatoria, que se sortea antes de aplicar ninguna prioridad; el registro anota el origen de cada solicitud y el resumen los separa.
3. **No se usa la ausencia de rastro publicado como señal de anomalía,** porque la §9.0 ter muestra que no distingue una obra terminada de una sin empezar. Tampoco se usa ningún criterio basado en la identidad, el color político o el territorio del órgano.

### D.5 Riesgos abiertos

- **Abuso de derecho.** Las resoluciones revisadas lo aprecian por insistir sobre una misma obra. Que una entidad pregunte por muchas obras distintas no se ha examinado: **requiere criterio jurídico.**
- **Identificación.** La solicitud exige identificarse (art. 17.2). Corresponde a cada organización decidir quién firma, y el registro público no lo recoge.
- **Coordinación.** Sin un registro compartido entre organizaciones podría haber preguntas duplicadas.
- **Cobertura.** Solo los perfiles alojados en la PLACSP; las plataformas autonómicas propias quedan fuera.
- **Fechas estimadas.** Si una ampliación de plazo no se publicó, la pregunta puede llegar antes de tiempo. La plantilla lo prevé.

### D.6 Herramientas

Todo el código está en `protocolo_obras/`, con licencia MIT-0:

- **`seleccionar_obras.py`:** lee los datos de la PLACSP con la misma política de versiones que el estudio, elige las obras de cada mes, aplica el tope y genera una solicitud redactada por obra.
- **`registro.py`:** valida el registro (también ampliaciones fuera de tiempo), avisa de lo que vence (vencimientos provisionales con días inhábiles, o el verificado si se ha anotado), hasta cuándo se puede reclamar y el plazo orientativo del órgano de garantía, resume las cifras (las de plazos, solo con fechas verificadas) y exporta un borrador para publicar.
- **`ciclo_mensual.py` y `GUIA.md`:** el ciclo de cada mes en una orden y una guía para personas no técnicas.
- **Plantillas** de solicitud y de reclamación por silencio.
- **`senal_terminacion.py` y `SENAL_TERMINACION.md`:** la señal de posible terminación anticipada, documentada condición por condición, con lo que se sabe de ella y el procedimiento para refinarla y volver a validarla.
- **`regimenes.py`:** por régimen (comunidad y ámbito), el plazo para resolver, la ampliación, el plazo para reclamar contra el silencio y el del órgano de garantía, con la cita del BOE de cada uno y el artículo que incluye a las entidades locales; sin régimen verificado no se calcula ninguna fecha.
- **Interfaz gráfica** (`fase0_placsp/interfaz.py`; en Windows, doble clic en `Abrir el programa.pyw`), con una pestaña para el estudio y otra para el protocolo. Prepara borradores de solicitud, el registro y avisos de plazo provisionales sin usar la terminal; la verificación y la presentación son humanas. Comprueba el registro antes de calcular nada, permite reanudar un ciclo cancelado y solo deja bajar el tope. No envía nada.
- **114 pruebas automáticas** (48 de las herramientas y 26, 26 y 14 de las correcciones de las revisiones de la v0.4.5, la v0.4.6 y la v0.4.7), más una prueba de equivalencia entre la coincidencia del protocolo y la regla congelada. Usan datos ficticios: no sustituyen a un piloto supervisado.

Las salidas con datos reales de órganos y obras no forman parte del repositorio.

---

*Fin de la v0.4.9. Elaborada y revisada con modelos de IA; no validada por especialistas humanos. Ninguna institución respalda el contenido y no se ha enviado ninguna comunicación en nombre de este proyecto.*
