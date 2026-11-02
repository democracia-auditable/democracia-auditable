# Rama 3: un registro de contratos que publica el fin

**1 de noviembre de 2026. Exploratorio, sin revisión.** Complementa la rama 4 (`investigacion_juridica`). Según ella, la ley obliga a comunicar el importe final y la extinción a los registros de contratos (art. 346.3 LCSP), y el art. 346.5 prevé el acceso público a esos datos, pero no se encontró una descarga abierta del Registro estatal.

**Pregunta:** ¿existe algún registro de contratos que publique en abierto el fin de cada contrato? Si existe, ¿qué publica y con qué cobertura en obras?

**Fuente:** el Registro de Contratos del Sector Público de Euskadi (REVASCON) y la API de contrataciones públicas de Euskadi, ambos en Open Data Euskadi (licencia CC BY). Se describe **una fuente de datos y su mecanismo**, no se evalúa a ningún órgano. Las cifras de este registro **no son comparables** con las del estudio de la PLACSP como medida de cumplimiento: miden otro canal (un registro, no un perfil de contratante), otros órganos y otros años.

## Respuesta corta

1. **Sí existe.** REVASCON publica para cada contrato su estado («Ejecución» o «Finalización»). En el campo «Finalización contrato» da la **fecha de finalización, el importe de finalización y una observación** (por ejemplo, que se liquida el expediente y se cancela la garantía), y además tiene un campo «Resolución contrato». Desde 2020, los ficheros por entidad añaden «Fecha fin contrato», «Datos Finalizacion» y «Datos resolución por finalización anómala o anticipada». Es un ejemplo práctico de lo que permitiría el art. 346.5 a escala estatal.
2. **Cobertura en obras.** En las obras no menores (adjudicación de al menos 50.000 € sin IVA) de los años 2014 a 2017 con el plazo teórico vencido antes del 31/12/2019, el registro abierto recoge el fin o la resolución en el **37–47 %**. Es mucho más que el 1–3 % de indicios de fin en la sindicación de la PLACSP, pero sigue siendo **menos de la mitad**. En el tramo de 1 a 10 M€, con muy pocos casos, la proporción es menor: del 0 al 21 %.
3. **La plataforma de contratación vasca** (otra fuente, vía API) marca como «Finalizado» el 5–16 % de las obras de 1 a 10 M€ adjudicadas en 2019–2023. Sumando el estado «Histórico», cuyo significado no se ha comprobado, llega al 16–23 %.
4. **Las cohortes recientes no se pueden medir con los datos abiertos:** los ficheros por entidad se congelan poco después de terminar el año. Por ejemplo, el de 2022 de una entidad se actualizó por última vez el 12/04/2023.

**Lectura.** Publicar el fin en un registro abierto es **técnicamente viable y ya se hace** en al menos un registro autonómico, con campos estructurados de fecha e importe final. Incluso así, una parte grande de las obras no tiene el fin registrado. Que exista el canal no garantiza que se use, y eso refuerza el papel del protocolo: **preguntar caso a caso y registrar la respuesta** cuando el dato falta.

## Detalle

### 1. Campos de fin en REVASCON

Ejemplo literal de un registro del fichero de 2019, sin datos del adjudicatario:

> `Finalización contrato`: «Fecha finalización: 11/04/2019, Importe de finalización: 48.380, Observaciones castellano: SE LIQUIDA EL EXPTE. Y SE CANCELA LA GARANTÍA»

| Fichero | Contenido | Campos de fin |
|---|---|---|
| Histórico CSV 2011–2018 (`contratos_euskadi_csv.zip`, archivos de septiembre de 2018) | Un fichero por año del contrato; estado a esa fecha; sin contratos menores | Estado contrato, Finalización contrato, Resolución contrato |
| «Registro … del 2019» (XLSX, actualizado el 25/03/2020) | Contratos con alguna inscripción o actualización en 2019, de cualquier año, menores incluidos | Ídem |
| Ficheros por entidad y año, 2020–2026 (p. ej. `doc_contratos_poder16135_2022.xlsx`) | Contratos del año de una entidad; instantánea poco posterior al cierre del año | Estado contrato, Fecha fin plazo, Fecha fin contrato, Datos Finalizacion, Datos resolución por finalización anómala o anticipada |

### 2. Cobertura del fin en obras (2014–2017)

`analizar_revascon.py` une el histórico (estado en septiembre de 2018) y el fichero de 2019 por «Código identificador del contrato». Un contrato cuenta con fin registrado si algún registro tiene estado «Finalización» o datos en «Finalización contrato» o «Resolución contrato». Fin teórico = fecha de formalización (o de adjudicación) + plazo de ejecución en meses.

| Año del contrato | Obras ≥ 50.000 € | Fin teórico vencido antes del 31/12/2019 | Con fin o resolución registrados |
|---|---:|---:|---:|
| 2014 | 79 | 78 | 31 (39,7 %) |
| 2015 | 86 | 85 | 32 (37,6 %) |
| 2016 | 134 | 127 | 59 (46,5 %) |
| 2017 | 156 | 146 | 54 (37,0 %) |

Obras de 1 a 10 M€ (licitación sin IVA): 3 de 14 en 2014, 3 de 17 en 2015, 2 de 21 en 2016 y 0 de 17 en 2017.

**Por qué no se usan otros años:**
- **2011–2013:** pocas obras y proporciones dispares, del 0 al 37 %. El registro abierto parece haber tenido entonces una cobertura parcial.
- **2018:** sale un 78,9 %, pero está **sesgado**. El histórico casi no tiene contratos de 2018, y los que aparecen en el fichero de 2019 están ahí precisamente porque cambiaron de estado ese año, muchas veces por terminar.
- **2019 en adelante:** no hay datos posteriores con los que ver su fin.

### 3. Plataforma de contratación (API)

`estados_api.py` pide a `https://api.euskadi.eus/procurements/contracts` el total de contratos de obras (tipo 1) por año de adjudicación y estado del procedimiento, para el tramo de 1 a 10 M€ según el filtro `contract-budget` de la API (consulta del 01/11/2026; las URL están en `estados_api.csv`).

| Adjudicadas en | Obras | Finalizado | Histórico | En ejecución o modificación |
|---|---:|---:|---:|---:|
| 2019 | 86 | 4 | 10 | 72 |
| 2020 | 66 | 6 | 5 | 51 |
| 2021 | 114 | 12 | 8 | 69 |
| 2022 | 140 | 16 | 10 | 105 |
| 2023 | 171 | 27 | 13 | 125 |
| 2024 | 182 | 8 | 10 | 154 |

La API también publica una «contractEndDate» por contrato, pero en el ejemplo revisado no coincide con la duración en meses. No se ha comprobado si es la fecha prevista o la real, así que no se usa.

## Qué cambia y qué no

- **Para el documento:** da un **ejemplo existente** para la recomendación de publicar por contrato lo comunicado al Registro (Anexo A.6, filas 39 y 51). Los campos estructurados de fecha e importe final ya existen en un registro público abierto; lo que falta a escala estatal es abrirlos.
- **Matiz importante:** aun con el canal abierto, menos de la mitad de las obras de 2014–2017 tienen el fin registrado dos o más años después de su plazo teórico. La publicación en registro **no sustituye** a la pregunta caso a caso; la complementa.
- **Lo que no se ha podido hacer:** cruzar estos contratos con la PLACSP. Las entidades de este registro publican en su propia plataforma, que llega a la PLACSP por agregación, en ficheros distintos de los perfiles alojados que usa el estudio. Además, los periodos con datos abiertos (hasta 2019 en el registro, desde 2019 en la API) apenas se solapan.

## Límites

- **Filtro de 50.000 €:** el histórico no marca ninguna obra como menor, pero tiene muchas obras de poco importe. Por eso se usa ese umbral como frontera aproximada de los contratos menores de obras (régimen anterior a 2018).
- **Obras sin plazo:** en 2016 y 2017 muchas obras no tienen plazo de ejecución utilizable (168 y 281 sin fin teórico) y quedan fuera del denominador, lo que puede sesgar el porcentaje.
- **Fichero de 2019:** sus cifras se leen con columnas armonizadas; los importes de ese fichero no se usan para seleccionar.
- **Interpretación de la API:** no se ha documentado qué significa el estado «Histórico», ni a qué importe se aplica exactamente el filtro `contract-budget`.
- **Número de casos:** el tramo de 1 a 10 M€ tiene muy pocos casos (14–21 por año) y no permite una estimación precisa.
- **Lo que se mide:** si el fin consta en los datos abiertos, no si la obra terminó ni si se comunicó por otra vía.
- **Datos personales:** los ficheros de origen contienen la razón social de los adjudicatarios, en algunos casos personas físicas. Los scripts no la extraen, y **los ficheros de origen no deben subirse a ningún repositorio**: se descargan de Open Data Euskadi.

## Reproducción

```
uv run --with openpyxl python -I -X utf8 analizar_revascon.py   # obras_revascon.csv y tablas
python -I -X utf8 estados_api.py                                 # estados_api.csv (≈170 consultas, 0,5 s entre ellas)
```

| Fichero (descargado el 01/11/2026) | Origen | Bytes | SHA-256 |
|---|---|---:|---|
| `fuentes/historico_csv.zip` | https://opendata.euskadi.eus/contenidos/ds_contrataciones/contratos_euskadi/es_contracc/adjuntos/contratos_euskadi_csv.zip | 3280694 | 3f89278afb5938550c0293196b4bfe8a29517f272bfe3d592ab591a9d96a1b46 |
| `fuentes/revascon_2019.xlsx` | https://opendata.euskadi.eus/contenidos/ds_contrataciones/contratos_euskadi_2019/es_contracc/adjuntos/Registro_de_contratos_del_Sector_Publico_de_Euskadi_del_2019.xlsx | 14477423 | 007d309e5b427beec96ba8b4dc19a1b0fa5eb525fca09a310ae1164d606e28a6 |
| `fuentes/gv_2022.xlsx` | https://opendata.euskadi.eus/contenidos/ds_contrataciones/contratos_poder16135_2022/es_contracc/adjuntos/doc_contratos_poder16135_2022.xlsx | 1548735 | 420c7789881941503838e8a62a525a6ef0cd58791f2b766eabbbe5c7eaaf0077 |

## Tras la revisión adversarial (02/11/2026)

- **El umbral de 50.000 € es un criterio analítico** para aproximar los contratos no menores de obras, no una identificación jurídica segura. Además, excluye muchas obras sin plazo estimable (168 en 2016 y 281 en 2017).
- **Descartar 2018** se justifica por un sesgo de selección plausible (el fichero de 2019 recoge actualizaciones, muchas asociadas al fin), no por una prueba de cobertura general.
