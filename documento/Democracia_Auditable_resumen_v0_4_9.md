# Democracia Auditable

**Aplicar ingeniería de seguridad a la supervisión democrática**  
*Propuesta de un protocolo abierto para reconstruir decisiones públicas, verificar advertencias y documentar las respuestas institucionales.*

**Documento de presentación para evaluación independiente · Basado en la v0.4.9 · 2 de noviembre de 2026**

> Los seres humanos somos imperfectos. Las instituciones deben estar diseñadas para que nuestros errores —y nuestros posibles abusos— no se conviertan en catástrofes, y para que las advertencias fundadas no puedan ignorarse sin dejar rastro.

## El problema que se quiere abordar

Una democracia dispone de elecciones, parlamentos, tribunales, órganos de control y derechos de acceso a la información. Pero, ante una decisión pública concreta, puede ser difícil reconstruir **qué información existía, quién detectó un problema, a quién se comunicó, qué respuesta recibió y qué ocurrió después**. La propuesta no presupone que las instituciones incumplan sus obligaciones: plantea un método para comprobar cómo funcionan sus mecanismos de detección, respuesta y corrección.

## Qué se propone

**Un protocolo de supervisión distribuida y verificable**, inspirado en la ingeniería de sistemas críticos: trazabilidad, controles independientes, defensa en profundidad, registro de errores y aprendizaje de incidentes. Su resultado buscado es un expediente reconstruible por terceros, no una sentencia automática ni una nueva autoridad. Una organización identificable tendría que asumir la responsabilidad jurídica y editorial de cualquier implantación real.

## Cómo funcionaría el protocolo

**1. Reunir evidencias.** Localizar fuentes públicas, conservar origen, fecha, versión y huella documental; distinguir hechos que constan, información no localizada e interpretaciones.

**2. Contrastar y verificar.** Comparar documentos y métodos independientes, registrar discrepancias y someter a revisión humana lo relevante. Separar calidad de la evidencia, impacto potencial y urgencia; nunca convertir esos ejes en una puntuación de personas o instituciones.

**3. Utilizar el cauce correspondiente.** Cuando falte documentación o exista una advertencia fundada, determinar primero qué procedimiento legal procede. Registrar destinatario, fecha de recepción, fundamento, plazo verificado y, cuando corresponda, reclamación o traslado al órgano competente.

**4. Dejar una memoria comprobable.** Registrar respuestas, inadmisiones motivadas, rectificaciones y **ausencia de respuesta localizada a una fecha determinada**, sin confundir silencio con culpabilidad. Cuando sea legal y prudente publicarlo, permitir reutilizar una pregunta ya formulada y su resultado.

**5. Auditar el propio control.** Publicar métodos, errores, limitaciones, resultados negativos y correcciones; facilitar la contradicción y la evaluación externa. Si una herramienta —incluida la IA— no aporta valor frente a una alternativa más sencilla, se descarta.

---

## Qué se pretende conseguir con su implantación

**Que las advertencias fundadas no se pierdan en el procedimiento.** Poder reconstruir qué se comunicó, por qué vía y qué actuación consta, sin atribuir intenciones ni exigir que toda advertencia sea aceptada.

**Que la respuesta institucional sea medible.** Contar solicitudes admisibles, respuestas motivadas y plazos legalmente aplicables; distinguir una carencia documental, un error del propio protocolo y un incumplimiento realmente acreditado.

**Que el conocimiento sea acumulativo.** Evitar preguntas innecesariamente repetidas y hacer más accesibles documentos, respuestas y rectificaciones, respetando las restricciones legales y de privacidad.

**Que el control sirva también a quien es controlado.** Detectar dónde faltan datos, dónde se concentran cargas de trabajo y qué información convendría publicar de oficio. El objetivo es corregir fallos de funcionamiento, no elaborar clasificaciones partidistas.

## Una primera aplicación: el final de las obras públicas

Para poner a prueba la idea se ha comenzado por la contratación de obras. Un análisis automatizado, **sin inteligencia artificial** (con reglas fijas), examinó datos abiertos de la Plataforma de Contratación del Sector Público. Entre **1.593 expedientes** de obras adjudicadas en 2023, con presupuesto base sin IVA de 1 a 10 millones de euros y finalización teórica anterior al corte, **en 1.549 (97,2 %) el programa no identificó indicadores de finalización o extinción en los campos examinados**.

Esta cifra **no demuestra que las obras no acabaran, que falten documentos por otras vías o que exista incumplimiento legal**. Señala una dificultad de localización en un canal concreto y justifica contrastar la información mediante un piloto. El anexo operativo del proyecto propone reglas de selección, solicitudes limitadas, registro de respuestas y seguimiento de plazos, siempre con verificación humana.

## Salvaguardas y límites

El protocolo **no sustituye** a jueces, interventores, parlamentos ni autoridades competentes; no decide políticas, no imputa delitos ni puntúa personas. No activa sanciones ni vetos automáticos y no es un canal de emergencias. Exige privacidad, derecho de réplica, rectificación visible, control editorial independiente y evaluación del daño que pudiera causar la propia supervisión. La IA es opcional y debe demostrar ventajas frente a métodos manuales o deterministas.

## Estado actual y puesta a disposición

Existe un **borrador metodológico**, un estudio reproducible y herramientas para preparar un piloto sobre obras públicas. **No se ha realizado ningún piloto con solicitudes reales ni existe validación jurídica, estadística o institucional por especialistas humanos.** Las revisiones hasta ahora han sido efectuadas con modelos de IA, por lo que sus conclusiones necesitan comprobación independiente.

Este trabajo se pone a disposición de cualquiera que lo encuentre útil, como una **propuesta abierta, no como un protocolo cerrado que deba adoptarse íntegramente**. Quien lo lea puede examinarlo críticamente, cuestionar sus hipótesis, aprovechar únicamente los principios, procedimientos o herramientas que considere útiles, adaptarlos a sus propias iniciativas o descartar la propuesta.

Quien considere que el protocolo, o una parte de él, merece ponerse a prueba podrá hacerlo bajo su propia responsabilidad y con la revisión técnica y jurídica correspondiente. Un piloto pequeño permitiría medir resultados, costes y posibles efectos no deseados.

**No se solicita adhesión, financiación ni compromiso de continuidad.** El propósito es compartir el trabajo realizado para que cualquiera valore libremente si contiene algo que le resulte útil. El proyecto no tiene entidad promotora operativa; los textos originales se ofrecen bajo CC0 y el código bajo MIT-0.

**Repositorio y documentación completa:** https://github.com/democracia-auditable/democracia-auditable  
**Para profundizar:** documento principal, §§ 1–3, 5–7 y 9–10; estudio § 9.0 bis; piloto de obras, anexo D.
