# Fase 0 — Visibilidad de la ejecución de obras públicas en la sindicación de la PLACSP

Programa v2.4 · Generado: 2026-11-01T23:12:10 · Corte de datos: 2026-10-29

> **Lectura obligatoria.** (1) La unidad es el **expediente** (licitación), que puede contener varios lotes y contratos. (2) Los documentos se detectan por **nombres de archivo o etiquetas de tipo documental** de la sindicación, no por su contenido: son *candidatos*. (3) Las cifras miden **la ausencia de coincidencias detectadas por el clasificador** en este canal, NO la inexistencia de documentación de finalización, que la obra no haya terminado ni que nadie incumpla nada; la información puede estar en el Registro de Contratos del Sector Público o en otro sitio. (4) El fin es **teórico estimado**, no la fecha real.

> **«RES» (resuelta)** significa que ha terminado el procedimiento de contratación, no la obra.

## Criterios de selección

- Obras (código 3); estado ADJ, RES
- Primera fecha de adjudicación de un resultado adjudicado (códigos 1, 2, 8, 9) en 2023
- Presupuesto base sin IVA del expediente entre 1,000,000 y 10,000,000 EUR
- Última versión de cada expediente; ante versiones distintas con la misma fecha, regla determinista (más documentos) e incertidumbre informada aparte
- Excluidos los expedientes con borrado ANULADA o sin tipo; los CERRADOS se incluyen y se marcan

## Resultado principal

| Conjunto | Expedientes | Fin teórico anterior al corte | …sin candidato de fin **definitivo** | …sin **ningún** candidato de fin |
|---|---:|---:|---:|---:|
| **Principal** (incluye cerrados) | 1651 | 1593 (96.5 %) | 1549 (97.2 %) | 1547 (97.1 %) |
| Sensibilidad: sin CERRADOS | 1651 | 1593 (96.5 %) | 1549 (97.2 %) | 1547 (97.1 %) |
| Sensibilidad: un solo resultado adjudicado | 1355 | 1311 (96.8 %) | 1273 (97.1 %) | 1272 (97.0 %) |
| Sensibilidad: sin versiones empatadas | 1631 | 1573 (96.4 %) | 1529 (97.2 %) | 1527 (97.1 %) |

Sin datos suficientes para estimar el fin: 20.

**Fin definitivo** = anuncio estructurado de finalización de contrato (DOC_CCN) o documento candidato de recepción definitiva, liquidación, certificación final, fin de obra o resolución del contrato. **Parcial/avance** = recepción parcial, certificación de avance o resolución en trámite.

## Incertidumbre por versiones empatadas

Expedientes con versiones distintas y la misma fecha de actualización en todos los datos: 399. De ellos, 21 serían seleccionables con alguna de sus versiones (detalle en `empates_en_seleccion.csv`).

- Expedientes seleccionados: 1651 (cota mínima 1631, cota máxima 1652)
- Titular (sin candidato de fin definitivo / fin teórico anterior al corte): cota mínima 1529/1573 (97.2 %), cota máxima 1550/1594 (97.2 %)

## Diagnóstico de borrados (`at:deleted-entry`)

| Tipo | `ref` distintos | Con entrada leída | De obras | Borrado posterior a la última versión | …que cumplirían criterios amplios |
|---|---:|---:|---:|---:|---:|
| CERRADA | 27075 | 0 | 0 | 0 | 0 |
| ANULADA | 6870 | 6700 | 966 | 559 | 0 |
| SIN_TIPO | 691 | 21 | 3 | 1 | 0 |

## Datos leídos

- version programa: 2.4
- ficheros leidos: 5190
- entradas leidas: 2557308
- expedientes distintos: 667929
- expedientes de obras ultima version: 114761
- expedientes seleccionados: 1651
- seleccionados cerrados: 0
- seleccionados con varios resultados adjudicados: 296
- fecha de corte datos: 2026-10-29
- años de actualización de las entradas: {'2019': 4542, '2020': 3346, '2021': 4290, '2022': 2200, '2023': 606581, '2024': 632433, '2025': 694148, '2026': 609768}

### Exclusiones por código de resultado

Expedientes que cumplirían los criterios si no se exigiera un resultado adjudicado con fecha en el año. Un expediente multilote puede combinar códigos; no indican una única causa.

| Códigos de resultado | Expedientes |
|---|---:|
| 3 | 141 |
| 4 | 29 |
| 5 | 7 |
| 3,4 | 3 |
| 3,8,9 | 3 |
| 3,9 | 2 |
| 3,8 | 1 |

## Detalle (n = 1651 expedientes)

| Qué consta | Expedientes | % |
|---|---:|---:|
| Formalización publicada (al menos un resultado) | 1601 | 97.0 % |
| Alguna modificación en datos estructurados | 534 | 32.3 % |
| Anuncio de modificación (DOC_MOD) | 534 | 32.3 % |
| **Anuncio de finalización de contrato (DOC_CCN, estructurado)** | 8 | 0.5 % |
| Candidato de fin definitivo por documento, sin DOC_CCN | 36 | 2.2 % |
| Prórroga prevista (texto en pliegos) | 252 | 15.3 % |
| Candidato: recepcion_definitiva | 2 | 0.1 % |
| Candidato: liquidacion | 5 | 0.3 % |
| Candidato: certificacion_final | 3 | 0.2 % |
| Candidato: final_obra | 0 | 0.0 % |
| Candidato: resolucion_contrato | 8 | 0.5 % |
| Candidato: recepcion_parcial | 1 | 0.1 % |
| Candidato: certificacion_avance | 1 | 0.1 % |
| Candidato: resolucion_en_tramite | 1 | 0.1 % |
| Candidato: devolucion_garantia | 0 | 0.0 % |
| Candidato: documento_modificacion | 109 | 6.6 % |
| Candidato: documento_prorroga | 9 | 0.5 % |
| Candidato: ampliacion_plazo | 74 | 4.5 % |
| Candidato: suspension | 31 | 1.9 % |
| Candidato: cesion_contrato | 11 | 0.7 % |
| Candidato: fin_en_nota_modificacion | 24 | 1.5 % |
| Candidato: fin_en_nota_candidato | 2 | 0.1 % |
| Algún candidato de incidencias durante la obra | 192 | 11.6 % |
| Algún candidato de fin definitivo | 44 | 2.7 % |
| Algún candidato de fin (definitivo o parcial/avance) | 46 | 2.8 % |

## Robustez por tramo de importe (añadido a posteriori; expedientes de obras adjudicados en 2023, sin filtro de importe)

| Tramo | n | Alguna modificación | Algún candidato de fin definitivo | Fin teórico anterior al corte | …y sin candidato de fin definitivo |
|---|---:|---:|---:|---:|---:|
| 1–10 M€ | 1651 | 32.3 % | 2.7 % | 96.5 % | 97.2 % |
| < 1 M€ | 18090 | 8.7 % | 1.1 % | 99.3 % | 98.9 % |
| > 10 M€ | 221 | 54.3 % | 1.4 % | 82.8 % | 98.4 % |

La tabla por tipo de administración está en `anexo_por_tipo_administracion.md`.
