# ¿Se puede saber si una obra llegó a empezar?

**1 de noviembre de 2026. Exploratorio, sin revisión.** Análisis preregistrado: las definiciones, la medida principal y los umbrales de interpretación se fijaron antes de ejecutar nada (`PREREGISTRO.md`, SHA-256 0dafe53e104d952e3a8c386cf87988135212aaf540bbb661b401f6c2fbaca2f7, en `PREREGISTRO.sha256`).

**Pregunta.** La ejecución de una obra empieza con el acta de comprobación del replanteo, que debe firmarse como tarde un mes después de la formalización, salvo casos excepcionales justificados (art. 237 LCSP). Ese acta no tiene obligación de publicarse. ¿Permite la sindicación abierta de la PLACSP saber si una obra adjudicada llegó a ejecutarse?

## Respuesta corta

**No, con fiabilidad suficiente.**

1. **Lo que se ve:** entre las obras de 1 a 10 M€ con el plazo vencido y sin fin publicado, el **36 %** muestra algún indicio de ejecución (sobre todo modificaciones publicadas) y el **64 %** no tiene **ningún rastro** después de la formalización.
2. **Lo que vale ese «sin rastro»:** en las obras que **con seguridad se ejecutaron**, porque publicaron su anuncio de finalización, el **61 %** de las de 1 M€ o más (IC95: 48–72 %) tampoco tenía ningún indicio antes de ese anuncio. Contando todos los importes, el 82 % (IC95: 79–86 %). Según la regla preregistrada, por encima del 50 % estar «sin rastro» **apenas informa**.
3. **La comparación decisiva:** la proporción «sin rastro» en la población (61–64 %) es prácticamente la que se observa en obras que sí se ejecutaron (61 %). Es decir, la cifra observada es compatible con que **todas** las obras hubieran empezado. Con estos datos no se puede afirmar que haya un número relevante de obras sin empezar, ni identificar cuáles son.
4. **Lo que sí informa es la presencia de un indicio:** una modificación, suspensión o ampliación de plazo publicada indica que el contrato está en marcha. La ausencia no indica lo contrario.

**Consecuencia.** El dato de inicio solo puede obtenerse **preguntando**. El protocolo de obras ya lo pide (el replanteo, si no existe el acta de recepción), y su registro incluye ahora el campo `fecha_replanteo`.

## Detalle

### 1. Niveles en el estado final

`escanear_versiones.py` (15 ZIP, 2021–octubre de 2026; 613.497 versiones de expedientes de obras; 156.277 obras en estado final, con la política de versiones del estudio). El indicador de fin coincide obra a obra con el del estudio: 0 discrepancias. Población: obras ADJ o RES con un resultado adjudicado y fin teórico estimado anterior al 29/10/2026.

| Tramo | Obras | A. Con fin | B. Sin fin, con indicio | C. Sin fin ni indicio | C entre las sin fin |
|---|---:|---:|---:|---:|---:|
| 1–10 M€ | 8.850 | 2,0 % | 35,6 % | 62,5 % | 63,7 % |
| 1 M€ o más | 9.711 | 1,9 % | 38,0 % | 60,1 % | 61,2 % |
| Todas | 111.186 | 1,1 % | 13,6 % | 85,2 % | 86,2 % |

**Qué indicios tienen las obras B de 1 a 10 M€:**
- modificación estructurada: 2.603;
- documento de modificación, prórroga, ampliación de plazo o suspensión: 994;
- acta de comprobación del replanteo: 122;
- documento de fin parcial: 6.

La modificación estructurada y el anuncio de modificación coinciden en 12.771 de 12.783 obras, así que son en la práctica **la misma señal**.

**Proporción C entre las obras de 1 a 10 M€ sin fin, por año de fin teórico:** 42,6 % (2019), 44,4 % (2020), 50,8 % (2021), 63,1 % (2022), 63,3 % (2023), 63,1 % (2024), 64,7 % (2025) y 69,1 % (2026). Las obras con el fin teórico más reciente han tenido menos tiempo para acumular modificaciones. Unas pocas obras tienen años de fin teórico imposibles (0021, 0204…), por errores en las fechas de origen.

### 2. Calibración con obras de final conocido

Son las obras con `DOC_CCN` vigente. La versión observada es la última con `updated` anterior a la fecha del primer anuncio de finalización: lo que habría visto un observador justo antes del anuncio.

| Grupo | Con DOC_CCN | Sin versión anterior en el corpus | Observadas | Sin ningún indicio antes del anuncio |
|---|---:|---:|---:|---:|
| Todos los importes | 579 | 141 | 438 | 361 = **82,4 %** (IC95 78,5–85,9 %) |
| 1 M€ o más | 76 | 7 | 69 | 42 = **60,9 %** (IC95 48,4–72,4 %) |

Como referencia: si se mirara el **estado final**, que incluye lo subido al cerrar el expediente, la proporción con indicio sería del 16,9 % (todos los importes) y del 39,5 % (1 M€ o más). Mirar el estado final habría sobrestimado lo que se sabe durante la obra.

**Sesgo declarado de antemano:** las obras que publican el anuncio de finalización probablemente publican más que las demás. En la población, la proporción de obras ejecutadas que no dejan rastro **podría** ser mayor; la dirección del sesgo es plausible, pero **no está contrastada**.

### 3. Del contrato al inicio real

Fuente: los XML ContractCompletionNotice, campo `ActualDurationPeriod/StartDate`; 629 contratos con inicio real y fecha de formalización.

- **Todos los contratos:** mediana de **21 días** entre la formalización y el inicio real (cuartiles de 0 a 44); el 32,9 % pasa de 31 días, el 10,8 % de 90 y el 3,5 % de 180.
- **En 178 contratos (28 %) el «inicio real» es exactamente la fecha de formalización.** Es probable que en ellos se haya copiado esa fecha en lugar de la del replanteo. Sin esos casos (453 contratos): mediana de **30 días** (cuartiles de 15 a 62); el **45,7 %** pasa de 31 días y el 15,0 % de 90.

**Sesgo de supervivencia:** solo se observan contratos que terminaron. Las obras que nunca arrancan no aparecen, así que estas cifras no dicen cuántas obras no empiezan. El plazo legal del mes admite excepciones justificadas, así que superarlo **no es por sí mismo un incumplimiento**.

## Qué cambia y qué no

- **Para el estudio:** confirma que el 97–99 % sin indicador de fin **no puede leerse** como «obras paradas» ni «obras sin empezar». En los datos abiertos, la ausencia de rastro tiene **escasa capacidad para distinguir**, en esta muestra, una obra que terminó con normalidad de otra que nunca empezó.
- **Para el protocolo:**
  - la pregunta debe pedir el **replanteo** cuando no exista el acta de recepción (la plantilla ya lo hace), y el registro anotar `fecha_replanteo` (añadido);
  - **los criterios de prioridad no deben usar la ausencia de rastro como señal de anomalía**, porque la calibración muestra que falla en la mayoría de las obras que sí se ejecutaron. La presencia de modificaciones o suspensiones sí es informativa, pero de lo contrario: indica que la obra está en marcha.
- **Lo que no se afirma:** que alguna obra concreta no haya empezado; que haya incumplimientos; nada sobre ningún órgano.

## Límites

- Los indicios son **nombres y etiquetas de documentos**, no su contenido.
- El patrón del replanteo excluye «previo». Puede dejar fuera actas con nombres atípicos o incluir alguna que no sea de comprobación.
- La versión «anterior al anuncio» depende de cuándo se descargó cada ZIP. 141 obras no tienen ninguna versión anterior en el corpus y se excluyen; en el tramo de 1 M€ o más son 7.
- El tramo de 1 M€ o más de la calibración tiene solo 69 obras, y su intervalo (48–72 %) roza el umbral del 50 %. Su lectura más prudente es «apenas informa o informa muy poco».
- El inicio real procede de lo que declara el órgano en el anuncio de finalización y, como se ha visto, a menudo es la fecha de formalización.

## Reproducción

```
python -I -X utf8 escanear_versiones.py   # versiones_obras.csv, estado_final.csv (15 ZIP; minutos)
python -I -X utf8 analizar_inicio.py      # resultados de este informe
```

Requiere `fase0_placsp/medir_ejecucion.py` e `investigacion_doc_ccn/escanear.py` (política de versiones del estudio) e `investigacion_doc_ccn/contratos_ccn.csv`.

## Correcciones posteriores al preregistro

- **Error de programación corregido antes de obtener ningún resultado:** la primera ejecución falló porque había resultados sin el bloque `Contract`, y la función de formalización no lo preveía. Se añadió la comprobación; no cambia ninguna definición.
- **Añadido sin cambiar el preregistro:** el recálculo del inicio real sin los contratos cuyo inicio coincide con la formalización (sección 3). Es un análisis adicional, motivado por haber observado esa coincidencia.

## Tras la revisión adversarial (02/11/2026)

- **Lo observado es 42 de 69** obras de 1 M€ o más sin indicio antes del anuncio (61 %; IC95 48–72 %), entre las que pudieron calibrarse. No es una muestra aleatoria de todas las obras ejecutadas, y se excluyen las 141 obras (7 de 1 M€ o más) sin versión anterior en el corpus. El 61 % no se traslada a todas las obras ejecutadas.
- **La comparación «antes del anuncio»** usa la fecha `updated` truncada al día y la compara con la fecha del anuncio: puede excluir actualizaciones del mismo día, y `updated` no equivale necesariamente al momento de la publicación pública.
- **El retraso del inicio real** compara el inicio de cada contrato con la **primera** fecha de formalización del expediente. En expedientes con varios contratos o lotes puede haber error de emparejamiento.
- **La fecha del preregistro es declarada:** la huella SHA-256 prueba la integridad del texto, no que fuera anterior a los datos ante terceros.
