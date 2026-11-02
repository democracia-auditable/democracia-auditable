# Rama 2: ¿basta el tiempo para explicar la baja detección?

**1 de noviembre de 2026. Exploratorio, sin revisión.** Complementa la fase 0 de «Democracia Auditable» (§9.0 bis). Las cifras se calcularon con la v2.3 del clasificador; con la v2.4 bajan en torno a un punto (ver la nota posterior, al final).

**Pregunta:** si al 98,7 % del estudio solo le faltara tiempo, las obras adjudicadas antes, con el plazo teórico vencido hace años, deberían mostrar muchas más señales de fin.

**Método:**
- `escanear.py` (de `investigacion_doc_ccn`), con la misma política de versiones que el estudio, sobre **15 ZIP de la PLACSP**: los anuales de 2021 y 2022 (descargados el 01/11/2026) más los 13 del estudio.
- Mismos criterios que el estudio: obras en estado ADJ o RES, con resultado de adjudicación y presupuesto base sin IVA entre 1 y 10 M€.
- Mismo indicador: «sin indicador de fin definitivo» quiere decir sin `DOC_CCN` vigente y sin nombres o etiquetas de documentos de recepción definitiva, liquidación, certificación final, fin de obra o resolución del contrato.
- Programa del análisis: `cohortes.py`.

**Control:** con los 15 ZIP, la cohorte de 2023 reproduce exactamente el estudio: 1.651 / 1.593 / 1.573 (98,7 %).

## Resultado

**Criterios del estudio (1–10 M€):**

| Adjudicadas en | Seleccionadas | Fin teórico vencido | Mediana del fin teórico | Sin indicador de fin definitivo |
|---|---:|---:|---|---:|
| 2021 | 1.408 | 1.377 | agosto de 2022 | **97,9 %** |
| 2022 | 1.768 | 1.699 | agosto de 2023 | **96,9 %** |
| 2023 | 1.651 | 1.593 | agosto de 2024 | **98,7 %** |

**Todas las obras, cualquier importe:** 99,3 % (2021), 98,7 % (2022) y 98,9 % (2023).

**Por antigüedad del fin teórico** (todas las obras adjudicadas en 2021–2023):

| Fin teórico en | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---:|---:|---:|---:|---:|---:|
| Sin indicador | 99,5 % | 99,0 % | 98,8 % | 98,7 % | 98,3 % | 98,4 % |

**Lectura:** con dos o tres años más de margen, la proporción sin indicador apenas baja: de 98,7 % a 97–98 % en el tramo de 1–10 M€. Y las obras cuyo plazo venció hace más tiempo no tienen más indicadores, sino algo menos. **En estos datos, el mayor tiempo observado no basta para explicar la baja detección de indicadores de fin.**

## Límites

- `DOC_CCN` existe solo desde 2024. Las obras que terminaron antes no podían publicarlo en su momento, aunque algunas lo hicieron después; para ellas solo cuentan los documentos con nombre de fin.
- El clasificador por nombre solo se validó a mano en la cohorte de 2023 de 1–10 M€. No se ha comprobado que funcione igual en 2021–2022 ni en otros importes.
- El fin teórico es una estimación. Se mide la sindicación de los perfiles alojados en la PLACSP, no otros canales.
- La cifra no prueba que la información no exista ni que se haya incumplido nada.

## Nota posterior (01/11/2026, programa v2.4)

Contando también el fin comunicado en el texto de las modificaciones (v2.4 del programa), las proporciones sin indicador de fin definitivo en el tramo de 1 a 10 M€ bajan aproximadamente un punto: **96,9 %** (2021), **95,9 %** (2022) y **97,2 %** (2023). Calculado con el mismo patrón sobre `investigacion_modificaciones/modificaciones.csv`; no se ha repetido el escaneo completo de esta rama. La conclusión («no es cuestión de tiempo») no cambia.

## Tras la revisión adversarial (02/11/2026)

- La formulación anterior («no es cuestión de tiempo») era demasiado categórica. El mecanismo disponible cambia con los años (el anuncio de finalización solo existe desde 2024), los datos están censurados y el clasificador no tiene en 2021–2022 una validación equivalente a la de 2023.
