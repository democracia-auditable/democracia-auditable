# Preregistro: indicios de ejecución en la PLACSP

**Escrito el 1 de noviembre de 2026, antes de ejecutar ninguna medición de esta rama.** Las definiciones no se cambiarán a la vista de los resultados. Si se corrige algo después (por ejemplo, un error de programación), se anotará al final con su motivo.

## Pregunta

¿Permite la sindicación abierta de la PLACSP saber si una obra adjudicada **llegó a ejecutarse**, es decir, si pasó de la formalización a la ejecución? Por ley, la ejecución empieza con el acta de comprobación del replanteo, como tarde un mes después de la formalización (art. 237 LCSP), pero ese acta no tiene obligación de publicarse.

## Definiciones

**Indicio de ejecución** en una versión de un expediente de obras: cualquiera de las señales siguientes.
1. Una modificación estructurada (`ContractModification`; `n_modificaciones > 0`).
2. Un anuncio de modificación (`DOC_MOD`).
3. Un documento de las categorías del clasificador del estudio para el periodo de obra (`DOCS_DURANTE`: modificación, prórroga, ampliación de plazo, suspensión, cesión) o de fin parcial (`DOCS_FIN_PARCIAL`: recepción parcial, certificación de obra o de avance, resolución en trámite).
4. Un documento cuyo nombre o etiqueta, normalizado, cumple `comprobaci\w*\s+(del\s+)?replanteo|acta\s+(de\s+)?replanteo` y no contiene `previo`, porque el replanteo previo es anterior a la licitación (art. 236).

**Fin**: el indicador de fin definitivo del estudio, es decir, `DOC_CCN` vigente o un documento de recepción definitiva, liquidación, certificación final, fin de obra o resolución del contrato.

**Niveles** de cada obra en su estado final (política de versiones del estudio):
- **A. Con fin**;
- **B. Sin fin, con indicio de ejecución**;
- **C. Sin fin y sin indicio**, es decir, sin ningún rastro publicado después de la formalización.

**Población principal**: obras en estado ADJ o RES con un resultado adjudicado y fin teórico estimado anterior al 29/10/2026. Se miden dos tramos: de 1 a 10 M€, el del estudio, y de 1 M€ o más, el del protocolo.

## Calibración

Obras con `DOC_CCN` vigente en su estado final. Como terminaron, se sabe que empezaron.

- **Versión observada**: la última versión del expediente con `updated` **anterior** a la fecha del primer `DOC_CCN` (`fecha_anuncio_finalizacion`). Es lo que habría visto un observador justo antes del anuncio.
- **Medida principal**: la proporción de esas obras **sin ningún indicio de ejecución** en la versión observada. Esa proporción estima con qué frecuencia una obra que sí se ejecutó queda en el nivel C. Se da con su intervalo exacto de Clopper-Pearson al 95 %.
- **Cómo se interpreta**:
  - si esa proporción es **baja (menos del 20 %)**, estar en el nivel C es una señal informativa;
  - si es **alta (más del 50 %)**, estar en C apenas informa;
  - entre ambos valores, informa de forma parcial.
- **Sesgos que se declaran de antemano**:
  - las obras que publican `DOC_CCN` pueden publicar más que las demás, así que la proporción calibrada sería un límite inferior de lo que pasa en la población;
  - una parte de esas obras puede no tener ninguna versión anterior al anuncio dentro del corpus; se cuentan aparte y se excluyen.

## Inicio real

Para las obras cuyo XML ContractCompletionNotice trae `ActualDurationPeriod/StartDate` (`investigacion_doc_ccn/contratos_ccn.csv`, campo `inicio_real`):
- se mide la diferencia en días entre la formalización (la fecha más temprana de `Contract/IssueDate` del expediente) y el inicio real;
- se da la mediana, los cuartiles y la proporción por encima de 31 días.

**Sesgo de supervivencia que se declara de antemano:** solo se observan obras que terminaron; las que nunca arrancan no aparecen.

## Lo que no se afirmará

- El nivel C no significa que la obra no haya empezado.
- Ninguna cifra se presentará como incumplimiento.
- No se nombrarán órganos ni obras.
