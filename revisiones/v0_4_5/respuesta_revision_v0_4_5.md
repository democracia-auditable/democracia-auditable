# Respuesta a la revisión adversarial de la v0.4.5

**2 de noviembre de 2026.** Revisión: `REVISION_ADVERSARIAL_v0_4_5_CHATGPT.md` (ChatGPT, sobre `para_chatgpt_v045.zip`). Cada punto se comprobó contra el código, los datos o el BOE **antes** de aceptarlo; los fallos de código se reprodujeron y cada uno tiene ahora una prueba en `protocolo_obras/test_revision_v045.py`. Resultado: v0.4.6 (cambios en su Anexo A.10).

Leyenda: **Aceptado** (se corrige tal cual), **Aceptado con matiz** (se corrige, con una diferencia que se explica), **Ya estaba** (el defecto no existe en el proyecto, solo en el paquete).

## Hallazgos bloqueantes

| Nº | Hallazgo | Comprobación | Decisión y corrección |
|---|---|---|---|
| B01 | Paquete incompleto; 3 pruebas fallan y 11 se saltan | El paquete solo llevaba una selección de ficheros (faltaban `descargar_datos.py` y el escáner). Pero el fondo es justo: `ciclo_mensual.py` importaba la descarga aunque no se usara, y las pruebas se saltaban en silencio si faltaba un módulo | **Aceptado con matiz.** Importación diferida; las pruebas ya no se saltan (fallan si falta un módulo); el repositorio se regenera desde una copia limpia y se prueba allí entero |
| B02 | La validación de la señal no es independiente del diseño | Cierto: la regla se diseñó viendo los tramos de 0,2–1 M€ y de 1 M€ o más, que forman la tabla principal. Recalculado el único tramo independiente: 3/103 frente a 0/193, IC 0,7–250 | **Aceptado.** «Asociación preregistrada en un corpus parcialmente expuesto al diseño»; se planifica una validación externa |
| B03 | Los plazos automáticos pueden llevar a reclamar fuera de plazo | **Confirmado en el BOE**, y es más amplio de lo que decía la revisión: 20 días (hábiles) en la Administración de Madrid (art. 42) y de Murcia (art. 26), 20 días hábiles en la Junta de Andalucía (art. 32), **30 días hábiles en Extremadura** (art. 23, también para sus entidades locales); reclamación contra el silencio sin plazo en Cantabria (art. 18), Navarra (art. 45) y el País Vasco (Ley 3/2026, art. 40) | **Aceptado.** `regimenes.py`: tabla por comunidad y ámbito con la cita del BOE de cada fila (fragmentos en `fuentes/regimenes/`). Sin régimen verificado no se calcula ninguna fecha (p. ej., el plazo de 20 días en las entidades locales de Madrid es dudoso). Las cifras «en plazo» solo cuentan regímenes verificados |
| B04 | La muestra no se guarda si hay 200 candidatas o menos | Reproducido | **Aceptado.** Se sortea `min(N, candidatas)` y se guarda siempre, con `marco_muestra.json`; el ciclo solo guarda la ruta si el fichero existe. Probado con dos ciclos seguidos |
| B05 | La validación del registro se rompe con una fecha mal escrita | Reproducido (`fecha_recepcion_organo`, `fecha_replanteo`, `fecha_recepcion_obra`) | **Aceptado.** Cada fecha se lee una vez y sin excepción; la interfaz valida antes de calcular pendientes, resumen o exportación |
| B06 | El tope se anula con 0; no hay reserva aleatoria en el flujo | Ambos ciertos. La «reserva aleatoria» del Anexo D.4 nunca se implementó | **Aceptado.** El tope solo admite de 1 a 4; más, con una justificación escrita en el lote; la interfaz solo deja bajarlo. Se retira la frase de la reserva: las proporciones se estiman solo con la muestra fija, y el registro anota el `origen` (muestra o flujo) |
| B07 | La validación de la señal no se puede repetir desde el paquete | Las copias congeladas tienen una ruta absoluta (no se pueden tocar sin romper su huella) | **Aceptado.** `ejecutar_regla_congelada.py` y `validar_e4t.py` anteponen las rutas relativas; `extraer_obras.py` usa rutas relativas; `test_equivalencia.py` comprueba con casos sintéticos de cada condición que la señal del protocolo marca lo mismo que la regla congelada |
| B08 | Faltan los ficheros de resultados anunciados | En el proyecto existían; no iban en el paquete | **Aceptado con matiz**, y resuelto de otro modo por decisión del proyecto: el repositorio deja de publicar las listas por expediente (ver B11). Se publican los agregados, un informe legible sin la lista (`informe_legible.py --publico`) y las huellas de los ficheros por expediente (`huellas_resultados.py`), verificadas con una repetición completa del análisis que dio ficheros idénticos byte a byte |
| B09 | El ciclo da por bueno un registro con errores | Reproducido | **Aceptado.** Valida antes de empezar y después de añadir los lotes; con errores se detiene sin avanzar el mes |
| B10 | Cancelar deja un estado que impide reanudar | Reproducido (lote ya creado; cerrojo colgado tras matar el proceso) | **Aceptado.** El ciclo reutiliza los lotes ya preparados ese día; el cerrojo de un proceso muerto se retira solo; la interfaz lo explica |
| B11 | Riesgo de señalar órganos con nombre | El `.gitignore` ya excluía los lotes y el registro (no iba en el paquete). Pero la tensión que señala la revisión en el estudio (lista pública de 1.651 obras con su órgano) era real | **Aceptado.** Se retiran del repositorio todas las listas nominativas del estudio; la exportación del registro va sin identificadores por defecto; prueba que comprueba el `.gitignore`. Se mantiene la carpeta de trabajo por defecto dentro del protocolo, protegida por `.gitignore` probado |
| B12 | Reserva arbitraria de datos auxiliares en empates | Cierto en el código (`next(iter(...))`) | **Aceptado.** Sin coincidencia exacta, los campos auxiliares quedan vacíos (comunidad desconocida, régimen sin verificar) y se informa de cuántas son |

## Señal de terminación (I13–I18)

| Nº | Decisión |
|---|---|
| I13 | **Aceptado.** R y N se describen como grupos documentales operativos; se añade el sesgo de espectro y la dependencia entre obras de un mismo órgano; el 83 % ya no se presenta como probabilidad |
| I14 | **Aceptado.** Se usa la formulación propuesta en el informe, la guía, el documento, la interfaz y los mensajes del programa |
| I15 | **Aceptado.** «Coincidencia documental compatible con una terminación posterior que requiere comprobación». La plantilla ya pedía la resolución solo «si se ha resuelto» |
| I16 | **Aceptado.** El documento aclara qué ronda revisó cada investigación; el informe ya no dice «pendiente de decidir» |
| I17 | **Aceptado, y recalculado.** Con la definición de «sin final» del estudio v2.4, el universo es de 44.290 y las marcadas son las mismas 78. Al recalcular apareció un error que la revisión no vio: son **66 órganos** por identificador, no 69 (el informe contó nombres) |
| I18 | **Aceptado.** Tablas por tramo declaradas descriptivas, con la explicación de la discrepancia entre el intervalo corregido y la prueba exacta |

## Órganos autonómicos y reclamaciones (I19–I21)

| Nº | Decisión |
|---|---|
| I19 | **Aceptado.** «58 % de las solicitudes potenciales», no de las reclamaciones |
| I20 | **Aceptado.** Recuento estricto con el desenlace de cada caso: 2 (Andalucía) y 7 (Cataluña) de obra pública; aparte, urbanizaciones, un suministro, un desistimiento y un caso dudoso. Ninguna desestimación de fondo ni inadmisión. El filtro se incorpora al proyecto (`filtrar_autonomicos.py`) y reproduce las 22 candidatas |
| I21 | **Aceptado.** «Depende de la ley aplicable y de la doctrina del órgano»; en Madrid se distingue la ley (un mes, art. 48) del criterio de no preclusión |

## Facilidad de uso y consistencia (I22–I28)

| Nº | Decisión |
|---|---|
| I22 | **Aceptado.** `--festivos` en el ciclo mensual y desde la interfaz; el resumen indica el calendario usado |
| I23 | **Aceptado.** El informe legible define el fin teórico como el estudio: incluye la última modificación de plazo publicada |
| I24 | **Aceptado.** La rama 2 avisa arriba de que sus cifras son de la v2.3 |
| I25 | **Aceptado.** Esta respuesta distingue lo comprobado con código, con pruebas sintéticas y con el corpus real |
| I26 | **Aceptado.** La interfaz y la guía dicen «prepara borradores, registro y avisos provisionales; la verificación y la presentación son humanas»; aviso visible de que no es apta para solicitudes reales sin revisión jurídica |
| I27 | **Aceptado.** El marco se ordena por identificador antes de sortear; la muestra es la misma con cualquier prioridad (prueba) |
| I28 | **Aceptado con matiz.** Las cifras de plazo excluyen los regímenes sin verificar y el resumen separa muestra y flujo. No se añaden campos `verificado_por` ni `norma_aplicada` por fila: la norma está en la tabla de regímenes, y la verificación humana es una regla del protocolo |

## Respuesta a la revisión anterior (P1–P13)

Se acepta la tabla de la revisión. Las regresiones que señala (P6, P7, P8, P11, P12, P13) quedan cubiertas por B03, B04, B06, B11 e I27.

## Qué se ha comprobado y cómo

| Tipo | Qué |
|---|---|
| Código y pruebas sintéticas | Todos los fallos de código: reproducidos antes de corregir; 26 pruebas nuevas, una por hallazgo, y prueba de equivalencia de la señal |
| Corpus real | Repetición completa del estudio v2.4 (ficheros idénticos byte a byte); recálculo de las 78 marcadas con la definición v2.4; filtro autonómico (mismas 22 candidatas) |
| Textos oficiales | Plazos de las 17 leyes (16 autonómicas y la estatal) en la API de legislación consolidada del BOE |
| Sin comprobar | La lectura jurídica sigue siendo de un no jurista; la clasificación de los casos autonómicos es de un solo lector; la equivalencia de la señal se comprobó con casos sintéticos y con el recuento real (78), no fila a fila en todo el corpus |
