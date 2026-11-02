# La «terminación licitada de nuevo»: una coincidencia documental asociada a contratos resueltos

**1–2 de noviembre de 2026. Exploratorio. Revisado el 02/11/2026 tras la revisión adversarial de la v0.4.5** (ver «Revisión adversarial» al final). Comparación preregistrada (`PREREGISTRO.md`, SHA-256 e1d02c20d9c594bd22b59c7a977d352271a0737a89588cf85d4276128078ade5, fijado a las 22:30 UTC del 1 de noviembre antes de aplicar la regla a ninguna obra con final conocido; fecha declarada). Sin revisión independiente.

**Origen.** La señal y la regla (E4t v2) se diseñaron en una consulta privada a partir de la revisión manual de obras. Esta carpeta solo **valida** la regla, sin cambiarla. Ni la consulta privada ni sus casos forman parte del estudio. El código de la regla y del extractor se copió sin cambios de lógica (`regla_e4t_v2.py`, SHA-256 6ea9d8cf36ea727a348918a995c25eaaed1e74a7ee2e849a1e0ef381ff1152e5, idéntica a la congelada).

## Qué detecta

Una obra A, formalizada y con el plazo teórico vencido, para la que **el mismo órgano licita después** una obra B cuyo título casi repite el de A y habla de **terminación, finalización, conclusión, resto de obras u obras pendientes**. Es una **coincidencia documental compatible con que el primer contrato no terminara la obra**, que requiere comprobación: también es compatible con una recepción parcial, un alcance complementario, otra financiación o fases mal descritas en los títulos. No acredita que el contrato se resolviera, ni ningún incumplimiento.

## Respuesta corta

1. **Asociación observada.** Marcó **10 de 273 expedientes con indicios documentales de resolución (3,7 %)**, frente a **2 de 558 con indicios de terminación ordinaria (0,4 %)**.
   - **Cociente: 10,2** (IC95 2,3–46,3; Fisher exacta bilateral p = 0,0004). El intervalo es muy ancho.
   - **Se alcanzaron las tres condiciones preregistradas** (cociente de al menos 3, límite inferior mayor que 1, al menos 5 marcadas en R).
   - **No es una validación confirmatoria independiente:** la regla se diseñó viendo obras de los tramos de 200.000 € a 1 M€ y de 1 M€ o más, que forman parte de la tabla principal. La separación entre obras con y sin final conocido evita usar las etiquetas R/N en el diseño, pero no el ajuste al vocabulario, los órganos y el estilo de los títulos. **En el único tramo ajeno al diseño (50.000–200.000 €)**, 3 de 103 frente a 0 de 193: prometedor, pero el intervalo (0,7–250) incluye 1 y **no cumple por sí solo el criterio preregistrado**. Lectura adecuada: *asociación preregistrada en un corpus parcialmente expuesto al diseño*.
   - **Esas proporciones no son trasladables** a obras sin final publicado. El 83 % de R entre las 12 marcadas depende de la proporción artificial entre los grupos (273 frente a 558): no es la probabilidad de que una obra marcada se haya resuelto.
2. **Poco sensible.** Marca a una pequeña parte de los expedientes del grupo R observado, que a su vez es solo la parte de las resoluciones que se publica de forma reconocible. **Una marca obliga a verificar; su ausencia no informa sobre el estado de la obra.** No sirve para estimar cuántas obras fracasan.
3. **Entre las obras sin final publicado** (2019–2023, 50.000 € o más), la regla marca **78 de 44.178 (0,18 %)**, de **66 órganos** (por identificador; 69 nombres distintos), con un máximo de 3 por órgano. Con la definición de «sin final» del estudio vigente (v2.4) el universo es de 44.290 y las marcadas son las mismas 78.
4. **En una muestra de 20 de esas 78, la página web de la obra no muestra ningún documento de resolución:** solo licitación, adjudicación y formalización (y, en tres casos, algún anuncio de modificación). Que no conste en la web no significa que no conste en otros canales.

**Formulación correcta:** «coincidencia documental compatible con una terminación posterior que requiere comprobación». No «contrato fracasado» ni «resuelto»: la resolución puede constar en otros canales (Registro de Contratos, boletines, el propio órgano) o no haber existido, y en cada caso hay que preguntarlo sin presuponer la respuesta.

## Detalle

### Validación con obras de final conocido (preregistrada)

`validar_e4t.py` sobre `obras.jsonl` (`extraer_obras.py`, 15 ZIP, 156.277 obras):
- **población:** estados admitidos, formalizadas, primera adjudicación en 2019–2023, 50.000 € o más, fin teórico anterior al 29/10/2026;
- **grupo R** (grupo documental operativo, no veredicto jurídico): documento de resolución del contrato localizado por el clasificador, o anuncio de finalización con código de causa;
- **grupo N** (ídem): documento de recepción, liquidación, certificación final o fin de obra, texto de modificación confirmado, o anuncio de finalización sin causa, y no está en R. Una liquidación también existe cuando se resuelve un contrato, y un anuncio sin causa no demuestra que el contrato acabara con normalidad.

| Tramo | R marcadas | N marcadas | Cociente R/N (IC95) | Fisher p |
|---|---:|---:|---|---:|
| **50.000 € o más (principal)** | **10/273 (3,66 %)** | **2/558 (0,36 %)** | **10,2 (2,3–46,3)** | **0,0004** |
| 1 M€ o más | 5/76 (6,58 %) | 1/132 (0,76 %) | 8,7 (1,0–73,0) | 0,025 |
| 200.000 €–1 M€ | 2/94 (2,13 %) | 1/233 (0,43 %) | 5,0 (0,5–54,0) | 0,2 |
| 50.000–200.000 € | 3/103 (2,91 %) | 0/193 | 13,1 (0,7–250) | 0,041 |

**Tablas por tramo: descriptivas y muy imprecisas** (5/1, 2/1 y 3/0 casos). En el último tramo se usa la corrección de 0,5 de Haldane: el intervalo logarítmico incluye 1 mientras la prueba exacta da p < 0,05; no es un error de cálculo, sino el reflejo de una incertidumbre extrema. Ninguna tabla por tramo es confirmatoria, y la principal tampoco es independiente del diseño (ver arriba).

**Las dos marcas del grupo N** tienen también títulos de «terminación» de la misma obra. Podrían ser contratos resueltos cuya resolución el clasificador no reconoce (una liquidación existe también cuando se resuelve un contrato), pero no se ha comprobado y cuentan como falsas alarmas.

### Muestra de obras sin final (comprobación en la web)

`revisar_paginas.py`: 20 de las 78 obras marcadas sin final publicado, sorteadas con semilla 20261102; páginas descargadas una por una (1,5 s entre peticiones).
- **Documentos de resolución, desistimiento, mutuo acuerdo, rescisión, incautación de garantía o penalidades:** **0 de 20**, ni con otro nombre.
- **Qué hay:** documentos de licitación, adjudicación y formalización en todas, y anuncios de modificación en 3. Ninguna muestra documentos de la ejecución ni de su final.

## Qué cambia

- **Para el estudio:** es la única coincidencia de las probadas que se asoció a las resoluciones en la comparación preregistrada; las demás (ausencia de rastro, retraso, ampliaciones repetidas, silencio relativo al órgano) no discriminaban. Ilustra la brecha que mide el estudio, pero no demuestra resoluciones concretas. **Incorporada a la v0.4.5 como novena investigación** de la §9.0 ter (solo cifras agregadas), revisada en la ronda adversarial de la v0.4.5 y **pendiente de una validación externa** (otro periodo, otros órganos, tramos no usados en el diseño, fijados antes en un registro con fecha verificable).
- **Para el protocolo:** puede ser un **criterio de prioridad declarado**. La plantilla pide el estado del contrato y, **si existen**, el acta de recepción o el acuerdo de resolución, sin presuponer cuál.
- **Lo que no cambia:** la lista de obras **no se publica**, porque señalaría posibles fracasos con nombre. Cada organización puede generarla para sus propias preguntas.

## Límites

- **Números pequeños:** 10 y 2 casos marcados; el intervalo del cociente va de 2,3 a 46.
- **Sensibilidad muy baja** (10 de 273 en el grupo R observado): no detecta obras paradas sin nueva licitación ni resoluciones sin un segundo contrato con título reconocible, y depende del vocabulario del título.
- **Avisa con retraso:** la nueva licitación aparece entre uno y tres años después.
- **Validez externa y sesgo de espectro:** las obras con final conocido publican más que las demás, y los grupos se forman por lo que se publica. La comparación dice que la coincidencia se asocia a las resoluciones **entre obras que publican su final**; además, varias obras de un mismo órgano no son casos independientes.
- **Diseño y revisión:** la regla se diseñó viendo obras de 0,2–1 M€ y de 1 M€ o más, y la precisión de los títulos la revisó el mismo sistema que la escribió. La validación R frente a N no se usó para diseñarla.
- **Política de versiones:** el extractor elige la última versión de cada expediente con un desempate por número de documentos, no con la regla exacta del estudio. Puede diferir en casos raros de versiones empatadas.
- **Datos reales:** `obras.jsonl`, `marcadas_validacion.csv` y `revision_manual/` contienen títulos y enlaces de obras reales: uso local, excluidos en `.gitignore`.

## Reproducción

```
python -I -X utf8 extraer_obras.py           # obras.jsonl desde los 15 ZIP (minutos)
python -I -X utf8 validar_e4t.py             # validación preregistrada
python -I -X utf8 ejecutar_regla_congelada.py 50000 1e13 2019 2023 > revision_manual/marcadas_sinfin.txt
python -I -X utf8 test_equivalencia.py       # la señal del protocolo marca lo mismo que la regla congelada
python -I -X utf8 revisar_paginas.py         # muestra de 20 en la web (1 petición/1,5 s)
```

`regla_e4t_v2.py` y `senales_medir.py` son copias congeladas, y sus huellas están en el preregistro. Las originales llevan, en una línea cada una, la ruta absoluta del equipo donde se escribieron. **En las copias de este repositorio esa línea se sustituyó por una ruta relativa equivalente, para no publicar rutas del equipo; el resto es idéntico.** Por eso sus huellas no son las del preregistro (6ea9d8cf… y 2afa0bfb…), sino 670b5e6de851d4d62cb32e5baf0d30477caf11ebb46f5fdda5a9785680d2fd8a (`regla_e4t_v2.py`) y f5c06ea03804f5b3ce4d909e91564e9833bbd715a1e43ce5b2aff4371b9dc60a (`senales_medir.py`). Quien tenga las originales puede comprobar que solo difieren en esa línea; quien no, no puede recomprobar las huellas del preregistro a partir de estas copias. Se ejecutan con `ejecutar_regla_congelada.py` o a través de `validar_e4t.py`, que anteponen las rutas relativas del proyecto. La validación necesita además `../investigacion_doc_ccn/contratos_ccn.csv` (lo genera `investigacion_doc_ccn/escanear.py`) y los datos de la PLACSP; ninguno se publica.

## Revisión adversarial (v0.4.5, 02/11/2026)

ChatGPT revisó esta investigación. Cambios: se deja de llamar «validación confirmatoria» a la comparación (la regla se diseñó viendo dos de los tres tramos de la tabla principal); los grupos R y N se describen como grupos documentales operativos; se quitan «muy fiable», «muy específica» y «en torno al 4 % de las resoluciones»; se distingue coincidencia documental de prueba de resolución; las tablas por tramo se declaran descriptivas. Al recalcular para responder a la revisión aparecieron dos correcciones: las 78 marcadas son de **66 órganos** por identificador (el informe contó 69 nombres), y con la definición de «sin final» del estudio v2.4 el universo es de 44.290 (las marcadas no cambian). Se añadieron `ejecutar_regla_congelada.py` y `test_equivalencia.py`.
