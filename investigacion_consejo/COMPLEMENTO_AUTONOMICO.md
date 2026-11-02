> Complemento de `INFORME_CONSEJO.md` (ámbito autonómico). La búsqueda la hizo el 01–02/11/2026 la sesión de la consulta privada, a petición del usuario. Se revisó el 02/11/2026 tras la revisión adversarial de la v0.4.5 (recuento estricto, formulación del 58 % y plazos según la ley de cada comunidad) y otra vez tras la de la v0.4.6 (ampliaciones, plazo de cada órgano de garantía y sin la lista de casos), y tras la de la v0.4.7 (solo llevan número las resoluciones citadas como precedente). **Reproducible:** `filtrar_autonomicos.py` aplica los mismos términos y da las mismas 22 candidatas; los datos de entrada se descargan de los portales de datos abiertos de cada órgano (ver el propio programa) y, como los resúmenes nombran administraciones, ni los datos ni las candidatas se publican. Dos citas verificadas por la sesión principal en el texto de la resolución: CTPD de Madrid 007/2026 y GAIP 1308/2026 (copias en `fuentes/autonomicos/`, no publicadas). La clasificación de cada caso la hizo un solo lector a partir de los resúmenes, sin revisión independiente. **No se nombran las administraciones reclamadas.** Una resolución se cita por su número público solo cuando se usa como **precedente de un criterio** y se dice cuál (apartado 2 y la frase útil), como en la rama 5; las que solo ilustran un resultado se describen sin número. **No se publican las listas sistemáticas de casos clasificados ni casos seleccionados para el protocolo**, porque cada número lleva a una ficha oficial con la administración y la obra: la lista se obtiene en local con `filtrar_autonomicos.py`. Lectura de un no jurista.

# Órganos de garantía autonómicos y documentos del fin de obra

**Por qué.** `INFORME_CONSEJO.md` solo revisó el ámbito estatal. En el escenario de `volumen.py`, el **58 % de las solicitudes potenciales del protocolo** (1.065 de 1.839 al año) corresponde a administraciones autonómicas o locales cuyo órgano de garantía podría ser autonómico, **si se llegara a reclamar y se confirmara la competencia**. No es una proporción de reclamaciones: no se sabe cuántas solicitudes acabarían en reclamación.

## 1. Búsqueda sistemática en datos abiertos (términos fijados antes de descargar)

Términos en castellano y catalán: acta de recepción/recepció, recepción de (la) obra, certificación/certificació final, liquidación/liquidació del contrato, final de obra, replanteo/replanteig.

Clasificación estricta (revisada): **documentación del fin o de la ejecución de una obra pública contratada por la Administración**. Se separan las urbanizaciones (a menudo promovidas por particulares y recibidas por el ayuntamiento), los suministros y los casos dudosos.

| | Andalucía (CTPDA) | Cataluña (GAIP) |
|---|---|---|
| Resoluciones en el conjunto | 6.641 (2016–2026) | 13.762 |
| Campos en los que se busca | «Resumen» (recortado) e «Indicador» | información reclamada, palabras clave y resumen |
| Candidatas | 5 | 16 distintas |
| **Obra pública, en sentido estricto** | **2** | **7** |
| — estimadas | 1 | 3 |
| — estimadas en parte | 1 | 1 |
| — información entregada solo tras la reclamación (pérdida de objeto) | — | 3 |
| — desestimadas o inadmitidas | **0** | **0** |
| Tiempo de resolución (estrictas) | no consta | mediana de 50 días (20–87) |
| Solicitantes (estrictas) | no consta | 4 cargos electos, 2 particulares, 1 empresa |
| Aparte: urbanizaciones | 1 (estimada) | 2 (estimadas) |
| Aparte: otros | 1 dudosa (certificación final de un edificio; información concedida durante la tramitación) | 1 suministro (pérdida de objeto) y 1 desistimiento |

La lista de los casos clasificados (número de cada resolución y su clase) no se publica: quien repita la búsqueda con `filtrar_autonomicos.py` obtiene las mismas 22 candidatas y puede clasificarlas con el criterio estricto de este apartado para contrastar la tabla.

Frase útil: GAIP 1308/2026 (una urbanización) dice que la documentación de recepción «presenta un interès públic evident» porque permite conocer si las obras se ajustaban a las condiciones exigibles y qué deficiencias se detectaron. GAIP 0741/2026 (no es de obras) dice, de paso, que la liquidación, los plazos finales de ejecución y las modificaciones son de interés público.

**Lectura admisible:** entre los muy pocos asuntos pertinentes clasificados (9 en unas 20.400 resoluciones), **ninguna desestimación de fondo ni inadmisión**. No se puede decir que «todos fueran favorables» en general: son pocos casos, la mayoría de solicitantes catalanes son cargos electos (con un derecho de acceso reforzado) y la clasificación no tiene revisión independiente.

## 2. Lecturas sueltas de otros órganos (búsqueda web, sin revisión sistemática)

- CTPD de Madrid 007/2026: las actas de recepción de urbanización son información pública. Aplica un **criterio de no preclusión** de la reclamación contra el silencio (criterio unificado del 09/10/2025), aunque el art. 48 de la Ley 10/2019 de Madrid fija un mes desde los efectos del silencio: hay que distinguir el texto legal del criterio interpretativo. Unos 5 meses.
- Comisión de Transparencia de Castilla y León (una resolución de 2022): recuerda que una resolución anterior dio acceso a la documentación base de un acta de recepción, y se cumplió.
- Comisionado de Canarias (una resolución de 2026): estimatoria sobre el acta de recepción de una infraestructura hidráulica (solo título).
- Consejo de Madrid (una resolución de 2023): estimación parcial; actas de entrega y recepción de urbanización.
- GAIP 435/2025: inadmisión por **abuso de derecho**, aunque la información era pública, porque el acceso se había ofrecido varias veces y no se había ejercido. La ley catalana no recoge el art. 18.1.e; se aplica el principio general, que exige ánimo de perjudicar y ausencia de beneficio para el derecho de acceso.
- Castilla-La Mancha: una reclamación sobre actas de recepción de urbanización, desestimada por falta de concreción (PDF cifrado, no leído).
- Sin caso específico encontrado: Comunitat Valenciana, Galicia, País Vasco, Aragón, Murcia y Navarra.
- Tiempos: Madrid, de 130 reclamaciones resueltas desde diciembre de 2023, 58 fuera de plazo (media de 5 meses); GAIP 2023, 94,5 % en plazo (nota de prensa).

## 3. Plazos: dependen de la ley aplicable, no del órgano

Revisados en los textos consolidados del BOE (`protocolo_obras/regimenes.py`, con la cita de cada fila, y `protocolo_obras/fuentes/regimenes/`):
- **Para resolver la solicitud:** un mes en la mayoría de los regímenes; **20 días hábiles** en la Comunidad de Madrid y la Región de Murcia (Administración autonómica) y en la Junta de Andalucía; **30 días hábiles** en Extremadura, también para sus entidades locales. Para las entidades locales de Madrid, la aplicación del plazo de 20 días es dudosa.
- **Ampliación:** en la mayoría, por un período igual al inicial; en el **País Vasco, quince días** (art. 37.2 de la Ley 3/2026); en **Cataluña, hasta la mitad del plazo inicial** (art. 33.2 de la Ley 19/2014); la ley gallega no la menciona. Donde la ampliación no se puede calcular con seguridad, las herramientas no dan fecha.
- **Para reclamar contra el silencio:** un mes en la mayoría; **sin plazo según la ley** en Cantabria, Navarra y el País Vasco; en Cataluña, un mes desde que vence el plazo para resolver, con mediación posible; en Madrid, un mes según la ley y un criterio de no preclusión del órgano de garantía.
- **Para que el órgano de garantía resuelva:** tres meses en el régimen estatal y en las leyes revisadas que lo fijan; **dos meses en Cataluña** (art. 42.9 de la Ley 19/2014), con la mediación suspendiendo el plazo y una ampliación posible de quince días. Donde no se ha localizado en el texto, el seguimiento es manual.
- **Ámbito:** la ley gallega no incluye a las entidades locales (rige la ley estatal), y la de Castilla-La Mancha fija su plazo solo para la Junta y sus entidades de derecho público. Las suspensiones (alegaciones de terceros, subsanación) cambian el vencimiento y no se calculan: cada fecha es provisional hasta que una persona la verifica.

Cada solicitud exige verificar la normativa aplicable y la doctrina del órgano competente; las herramientas no calculan fechas cuando el régimen no está verificado.

## Lectura para el protocolo

1. Ningún órgano autonómico revisado discute que la documentación de recepción y de fin sea pública. Las negativas vistas son por abuso (repetición tras haber tenido acceso) o por falta de concreción, ambas previstas en las reglas del protocolo.
2. El patrón de entregar solo tras la reclamación también aparece aquí: 3 de los 7 casos estrictos catalanes.
3. Los plazos para resolver y para reclamar dependen de la ley aplicable (apartado 3), y la regla prudencial del protocolo («reclamar en el mes siguiente al silencio») sigue siendo prudente en todos los regímenes revisados, porque ninguno da menos de un mes para reclamar.
4. Muy pocos precedentes; ninguna desestimación de fondo entre los clasificados.
5. Cautelas: solicitantes con derecho reforzado; en Andalucía solo se buscó en un resumen recortado; dos órganos revisados de forma sistemática de unos diez; clasificación de un solo lector.
