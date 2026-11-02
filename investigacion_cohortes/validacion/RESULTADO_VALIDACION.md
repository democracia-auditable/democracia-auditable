# Validación del clasificador fuera de la población del estudio

**1 de noviembre de 2026. Exploratorio, sin revisión.**

**Pregunta:** el clasificador del estudio busca indicios de fin en los códigos, nombres y etiquetas de los documentos de la sindicación. Solo se había validado a mano en obras de 1 a 10 M€ adjudicadas en 2023, con 21 casos negativos. ¿Pasa por alto, en otros años e importes, documentos de fin que la web de la PLACSP sí muestra?

## Método

- **Población:** obras del corpus 2021–octubre de 2026 (15 ZIP; `escanear.py`) en estado ADJ o RES, con resultado de adjudicación, fin teórico estimado anterior al 29/10/2026 y **sin** indicador de fin definitivo según el clasificador.
- **Muestra estratificada** con semilla publicada **20261101** (`sortear.py`): 4 años de adjudicación (2021–2024) × 3 tramos de presupuesto (<1 M€, 1–10 M€, >10 M€) × 5 obras = **60 obras**. La población de cada estrato va de 124 a 17.770 obras (`muestra.csv`).
- **Descarga** de la página web de cada obra (`descargar_paginas.py`; las 60 respondieron con HTTP 200; se guardan la página y su huella SHA-256) y extracción de todas las filas con fecha: anuncios y documentos.
- **Revisión manual** de esas filas, una a una. Se consideró indicio de fin cualquier anuncio o documento de recepción, liquidación, certificación final, fin de obra, resolución del contrato, anuncio de finalización o devolución de la garantía definitiva. El resultado está en `revision_manual.csv`.

## Resultado

**Falsos negativos: 0 de 60.** Ninguna página muestra un documento o anuncio de fin que el clasificador no detectara.

- Con 0 de 60, la cota superior del intervalo de confianza exacto al 95 % para la proporción de falsos negativos es del **6,0 %** en el conjunto de estratos muestreados. Por estrato (0 de 5) la cota es del 52 %: la muestra no permite afirmar nada estrato a estrato.
- **19 de las 60 obras** muestran documentos de la ejecución: modificaciones, suspensiones, ampliaciones de plazo, precios nuevos o adendas. En ninguna aparece su final. Las otras 41 solo tienen documentos de licitación, adjudicación y formalización.
- Hay casos que el clasificador resolvió bien pese a parecer de fin por el nombre: «Resolución rectificación error», «certificado resolución adjudicación», «Desistimiento licitador», «Anulación Formalización» y «Resolución modificación».

## Lectura

En los años e importes muestreados, el clasificador no pierde indicios de fin visibles en la web de la PLACSP. Junto con la muestra anterior (1 omisión en 21, ya corregida en la versión 2.1 del programa), esto refuerza que el 97–99 % de obras «sin indicador» refleja lo que publica la plataforma, y no un fallo de detección.

## Límites

- **Valida el clasificador frente a lo que muestra la web de la PLACSP, no frente a la realidad.** Un documento que no se subió a la plataforma no aparece ni en la sindicación ni en la web. Tampoco se ha comprobado el Registro de Contratos, otros perfiles ni las plataformas autonómicas.
- **Se revisaron nombres y tipos de documento, no su contenido.** Es la misma limitación que la del clasificador. Un documento con un nombre genérico podría contener información de fin.
- **La muestra es estratificada, no proporcional**, y 60 casos dan una cota del 6 % para el conjunto, no una estimación precisa por estrato.
- **Revisión hecha por el mismo sistema** (Claude) que escribió el clasificador. Una revisión humana independiente de una parte de la muestra la reforzaría.

## Reproducción

```
python -X utf8 -I sortear.py           # requiere ../obras_estado_final.csv (escanear.py con los 15 ZIP)
python -I descargar_paginas.py         # 60 peticiones, 1 cada 1,5 s; páginas en paginas/
```

## Nota posterior (01/11/2026, programa v2.4)

Esta validación revisó los **documentos** de cada obra, no el texto de los anuncios de modificación. Después se descubrió que algunos órganos comunican la liquidación o la certificación final en ese texto (campo `Note` de `ContractModification`), que la v2.3 no leía: en la cohorte del estudio son 24 expedientes, todos fines reales. Es un tipo de falso negativo que esta muestra no podía detectar. La v2.4 del programa lo corrige (98,7 % → 97,2 %); ver `investigacion_modificaciones/INFORME_MODIFICACIONES.md` y `fase0_placsp/METODO.md`.

## Tras la revisión adversarial (02/11/2026)

- **La muestra es estratificada** (12 estratos de año e importe, 5 obras cada uno), no una muestra aleatoria simple proporcional al universo. La cota binomial del 6,0 % supone una muestra homogénea, que la estratificación no garantiza: **no se traslada sin ponderar al conjunto de las obras**. Se presenta como **validación exploratoria**: 0/60 en la muestra estratificada.
- La revisión la hizo el mismo sistema que escribió el clasificador y miró documentos, no el texto de las modificaciones (ver la nota anterior).
