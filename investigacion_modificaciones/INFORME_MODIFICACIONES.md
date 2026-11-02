# Qué dicen (y qué no) los anuncios de modificación

**1 de noviembre de 2026. Exploratorio, sin revisión.** Preregistrado (`PREREGISTRO.md`, SHA-256 50bb51c149c7bf8b2e638d753f564a4baed6b1626bdd20e04f4420d024865a43, fijado a las 21:21 UTC antes de medir). Los hallazgos posteriores al preregistro se señalan como tales.

**Origen.** Una consulta privada del usuario dio lugar a un indicador de triaje que incluía una señal de «modificación opaca» (A3). Esta rama la examina con rigor y la ancla en una obligación legal. El art. 207.3 LCSP exige publicar toda modificación en un plazo de 5 días desde su aprobación, «acompañada de las alegaciones del contratista y de todos los informes». A diferencia del fin de la obra, **esto sí es obligatorio**.

## Respuesta corta

1. **Las modificaciones «opacas» son pocas y están concentradas:** las que no traen importe, plazo ni texto son el 2,1 % (1 M€ o más: 2,2 %). Los 10 órganos con más reúnen el 56–63 %. **Como detector de obras problemáticas, A3 no sirve:** mide sobre todo la costumbre de publicación de unos pocos órganos.
2. **Muchas «modificaciones» no lo son.** En la revisión manual, buena parte de las opacas eran **suspensiones temporales totales, reanudaciones, liquidaciones, recepciones parciales o ampliaciones de plazo** publicadas con el formulario de modificación. Algunos órganos usan ese anuncio para comunicar el estado de la obra.
3. **Corrección para el estudio principal** (hallazgo posterior al preregistro):
   - Hay obras que comunican su **fin** en el texto de una modificación: «se formaliza la liquidación del contrato», «certificación final de obra». El clasificador del estudio no lo ve, porque solo mira los nombres de los documentos.
   - En la cohorte del documento (2023, de 1 a 10 M€), contando ese campo, la proporción sin indicador de fin pasa del **98,7 % al 97,2 %** (1.549 de 1.593; los 24 casos se revisaron a mano). En 2021 pasa de 97,9 % a 96,9 %, y en 2022 de 96,9 % a 95,9 %.
   - La conclusión no cambia, pero **la cifra debe corregirse o acompañarse de esta salvedad**.
4. **Documentación del art. 207.3:**
   - solo el **13–16 %** de las obras modificadas tiene algún documento cuyo nombre corresponda a una modificación;
   - en la revisión de 30 obras, solo 3 mostraban en su página un documento claramente de la modificación, y **en ninguna se vieron las alegaciones del contratista ni los informes previos**;
   - además, el XML del anuncio de modificación **no tiene ningún campo para adjuntarlos**: el formato de la plataforma no está pensado para llevarlos.

   Esto **no prueba un incumplimiento**: los documentos pueden publicarse con nombres genéricos, en otra sección o en otro canal. Pero es una **pregunta concreta y legalmente fundada** para el protocolo.
5. **Plazo de 5 días:** la sindicación no tiene la fecha de aprobación. El XML de cada anuncio sí trae una fecha de la modificación (`ContractModification/IssueDate`). En la muestra (66 modificaciones), el anuncio se publicó una mediana de **3 días** después, y en el **36 %** pasaron más de 5 días naturales (los plazos por días de la LCSP son naturales salvo que se diga lo contrario, DA 12.ª). **Con cautela:** la muestra está sesgada hacia las opacas y no se ha confirmado que esa fecha sea la de aprobación.
6. **Una señal de estado que nadie estaba leyendo:** 200 obras comunican una **suspensión** en el texto de sus modificaciones, sobre todo un órgano (el 73 %). Es justo el tipo de dato («esta obra está parada») que no aparece en ningún otro sitio.

## Detalle (medidas preregistradas)

`escanear_modificaciones.py` (15 ZIP; estado final con la política de versiones del estudio): 12.783 obras con modificaciones y 19.554 modificaciones. Población: obras adjudicadas, ADJ o RES.

| Medida | Cualquier importe | 1 M€ o más |
|---|---:|---:|
| Modificaciones / obras | 19.547 / 12.779 | 6.457 / 3.639 |
| Con texto (`Note`) | 58,4 % | 62,2 % |
| Sin justificación textual (<40 caracteres o sin texto) | 65,5 % | 57,6 % |
| Con importe distinto de 0 / con plazo | 50,3 % / 71,8 % | 62,1 % / 67,1 % |
| Sin contenido estructurado (ni importe ni plazo) | 5,7 % | 5,5 % |
| **Opacas** (sin estructura ni texto) | **2,1 %** (IC95 1,9–2,3) | **2,2 %** (1,8–2,6) |
| Obras con al menos una opaca | 2,9 % (2,6–3,2) | 3,5 % (2,9–4,2) |
| Texto con plazo y sin campo de plazo / con dinero y sin importe | 1,0 % / 2,0 % | 1,3 % / 1,8 % |
| **Obras con algún documento de modificación** (por nombre) | **13,3 %** (12,7–13,9) | **15,8 %** (14,6–17,0) |
| Obras modificadas sin anuncio DOC_MOD | 0,1 % | 0,0 % |
| Concentración de las opacas: los 10 órganos con más / el primero | 55,6 % / 26,6 % | 63,1 % / 27,7 % |

**Opacas por año del primer anuncio:** entre el 1,3 % y el 3,5 %, sin tendencia clara.

**El campo `Note`:** la especificación oficial de la sindicación (v1.3, 05/08/2020, apdo. 4.38) no lo recoge, pero aparece en los datos actuales. Eso explica que la revisión previa creyera que el texto explicativo solo estaba en la web.

## Revisión manual (30 obras, semilla 20261102)

- **Muestra:** obras de 1 M€ o más con alguna modificación opaca; se descargaron sus 30 páginas web y los XML de sus 75 anuncios de modificación.
- **Errores:** 5 XML no se pudieron leer (formato no válido); se excluyen.

**Qué eran las 31 modificaciones opacas leídas en el XML.** La categoría más frecuente es «SUSPENSION – SUSPENSION TEMP. TOTAL». Le siguen modificaciones sin texto y con importe 0, a menudo posteriores a otra con importe, y textos como «Liquidación», «Recepciones parciales», «Modificado precio 0,00 €», «Ampliación de plazo», «Circunstancias sobrevenidas» o «Modificado 1».

**Días entre la fecha de la modificación y la del anuncio** (66 modificaciones con ambas fechas): mediana de 3; 24 de 66 por encima de 5; ningún caso negativo. Hay casos aislados de varios cientos de días.

**Documentos en la página:**
- La búsqueda por palabras clave encontró sobre todo informes y resoluciones de la **licitación**, no de la modificación.
- Documentos claramente de la modificación: 3 de 30 obras (un contrato modificado, un proyecto modificado, notas informativas de ampliación de plazo).
- Alegaciones del contratista o informes previos a la modificación: ninguno identificado.

## Qué cambia y qué no

- **Para el documento (estudio, §9.0 bis):**
  - corregir o matizar el 98,7 %: con el texto de las modificaciones, el **97,2 %**;
  - añadir el límite: el clasificador no lee el texto de las modificaciones, donde unos pocos órganos comunican liquidaciones y certificaciones finales;
  - la validación manual (0/60) no lo detectó porque revisó documentos, no este campo.

  **Decisión pendiente** para la revisión final: corregir el programa del estudio (y la cifra) o mantenerlo y añadir la salvedad.
- **Para el protocolo:**
  - leer el texto de las modificaciones antes de preguntar: si dice que la obra se liquidó o se recibió, **no se pregunta** (sería una pregunta inútil y reforzaría el argumento del abuso);
  - las suspensiones comunicadas son un **dato de estado** que conviene mostrar junto a cada obra;
  - una posible segunda pregunta, distinta y legalmente fundada, para obras con modificaciones: las alegaciones del contratista y los informes previos que exige el art. 207.3.
- **Para el triaje de la consulta privada:** A3 no debe usarse como señal de anomalía de la obra. Sí puede usarse, con otro nombre, como **indicador de calidad de la publicación** de las modificaciones, siempre medido de forma agregada y no por órgano.

## Límites

- Los documentos se identifican por **nombre**. Pueden existir informes con nombres genéricos que no se han reconocido.
- La revisión manual es de 30 obras, elegidas entre las que tienen alguna opaca: **no representa** a todas las modificaciones.
- El recuento de «más de 5 días» usa días naturales (DA 12.ª LCSP, `fuentes/lcsp_da12.txt`) pero no aplica la prórroga al primer día hábil cuando el quinto día es inhábil, así que puede contar de más algún caso.
- La fecha `ContractModification/IssueDate` del XML del anuncio no está documentada. Puede ser la de aprobación, la de efectos o la de registro.
- El patrón de fin en el texto se revisó a mano solo en la cohorte de 2023 (24 casos, todos correctos). En el resto del corpus puede haber algún falso positivo o negativo.
- Las suspensiones y los fines en el texto están muy concentrados (un órgano reúne el 63–73 %), así que generalizar a otros órganos no es posible.
- El XML del anuncio contiene datos del adjudicatario; no se extraen ni se conservan fuera de `revision_manual/`, que no debe publicarse (`.gitignore`).

## Reproducción

```
python -I -X utf8 escanear_modificaciones.py   # modificaciones.csv, obras_modificadas.csv (uso local)
python -I -X utf8 analizar_modificaciones.py   # medidas preregistradas y muestra_revision.csv
python -I -X utf8 descargar_revision.py        # páginas web de la muestra (1 petición/1,5 s)
python -I -X utf8 revisar_muestra.py           # XML de los anuncios de modificación de la muestra
```

**Fuentes legales y técnicas** (`fuentes/`): LCSP arts. 203, 205, 207 y 242 (BOE, API de datos abiertos, 01/11/2026); especificación de la sindicación v1.3 (SHA-256 4599df9651dfe5b5b0e87f717bd2b8aa2b20f933d0b105abf20971488ec170b5); guía de servicios web v3.10 (en `investigacion_juridica/fuentes/descargas/`).

## Tras la revisión adversarial (02/11/2026)

- **«Opaca» es una definición operativa, no jurídica:** un texto de menos de 40 caracteres puede explicar lo suficiente. Es un **indicador de calidad informativa**, nunca de «modificación irregular».
- **Los nombres de los adjuntos no miden el cumplimiento del art. 207.3,** la revisión de 30 obras se eligió por opacidad (no es aleatoria entre todas las modificadas) y las ampliaciones de plazo pueden seguir su propio régimen (art. 203.1).
- **La fecha `ContractModification/IssueDate`** no está verificada como fecha de aprobación; el 36 % por encima de 5 días es una comparación descriptiva, no una tasa de incumplimiento.
- **Corrección del estudio:** el programa (v2.4) solo cuenta como fin un texto que sea, completo, una fórmula breve de una lista cerrada; el resto se anota como candidato y no cuenta. La cifra no cambia (1.549, 97,2 %). **22 de los 24 casos proceden de un mismo órgano** y los otros 2 de un segundo: es una práctica observada y concentrada, que no se puede generalizar. La revisión de los 24 está en `fase0_placsp/revision_manual_fin_en_nota_v2_4.csv`.
- **La fecha del preregistro es declarada:** la huella prueba la integridad del texto, no su anterioridad ante terceros.
