# Preregistro: ¿la señal «terminación licitada de nuevo» distingue contratos resueltos?

**Escrito el 1 de noviembre de 2026 (hacia las 23:30, hora peninsular), antes de aplicar la regla a ninguna obra con final conocido.** Las definiciones no se cambiarán a la vista de los resultados; cualquier corrección se anotará al final con su motivo.

## Qué se valida

La regla **E4t v2**, diseñada en una consulta privada y congelada antes de probarla (`regla_e4t_v2.py`, SHA-256 6ea9d8cf36ea727a348918a995c25eaaed1e74a7ee2e849a1e0ef381ff1152e5; copia sin cambios de lógica). Marca una obra A cuando el **mismo órgano** licita después una obra B cuyo título se parece al de A (Jaccard de palabras significativas de al menos 0,6, misma fase o lote, números compatibles, palabras raras compatibles) y habla de **terminación, finalización, conclusión, resto de obras, obras pendientes o completar las obras**. La idea es que, si hizo falta otro contrato para terminar la obra, el primero no la terminó.

La revisión previa midió si el título de B se refiere a terminar A, no si A fracasó. Esta validación mide lo segundo con obras **cuyo final se conoce**.

## Datos

`extraer_obras.py` (copia del extractor de la consulta privada), con los 15 ZIP de 2021 a octubre de 2026 → `obras.jsonl`. Se usa la **misma búsqueda de B** que la regla (`regla_e4t_v2.py`, función de emparejamiento reproducida sin cambios), pero aplicada a obras **con** final conocido en lugar de a las que no lo tienen.

**Población:** obras en los estados admitidos por el estudio, formalizadas, con la primera adjudicación en 2019–2023, presupuesto base sin IVA de **50.000 € o más** y fin teórico anterior al corte.

**Grupos de final conocido** (excluyentes):
- **R, contrato resuelto:** la obra tiene un documento candidato de resolución del contrato (`resolucion_contrato` del clasificador del estudio), o su anuncio de finalización (`investigacion_doc_ccn/contratos_ccn.csv`) trae un código de causa de resolución en algún contrato del expediente.
- **N, terminación ordinaria:** no está en R y tiene un documento de recepción definitiva, liquidación, certificación final o fin de obra, un texto de modificación confirmado como liquidación o certificación final, o un anuncio de finalización sin código de causa.

## Medidas

- **Principal:** proporción de obras marcadas por la regla en R y en N, y su **cociente (R/N)** con intervalo de confianza al 95 % (método logarítmico; con corrección de 0,5 si alguna celda es 0). Prueba exacta de Fisher bilateral.
- **Secundarias:** lo mismo para los tramos de 1 M€ o más y de 50.000–200.000 €; y, entre las obras marcadas con final conocido, qué proporción está en R.

## Cómo se interpretará

- **Validada como indicador de resolución:** cociente de al menos 3 **y** límite inferior del IC95 mayor que 1.
- **No validada:** el IC95 incluye 1.
- **Indicio parcial:** cualquier otro caso.
- **Si hay menos de 5 obras marcadas en R,** el resultado se declarará **no concluyente** por falta de casos, cualquiera que sea el cociente.

## Sesgos que se declaran de antemano

- **Quien publica el final puede publicar más.** Las obras con final conocido pueden no representar a las que no lo tienen: la validación dice si la señal distingue resoluciones **entre obras que publican su final**.
- **El grupo N incluye terminaciones en las que una segunda licitación completa un alcance previsto** (fases no numeradas, obras complementarias). Esos casos cuentan como falsas alarmas: es justo lo que se quiere medir.
- **La revisión de la consulta privada vio obras de 0,2–1 M€ y de 1 M€ o más al diseñar la regla.** En esos tramos la tasa no es independiente del diseño, pero el grupo de comparación (R frente a N) no se usó para diseñarla.

## Lo que no se afirmará

- Ninguna obra concreta se presentará como fracasada.
- No se publicará la lista de obras marcadas.
- No se nombrarán órganos.
