# ¿Cómo terminaron las obras públicas? — Fase 0 de «Democracia Auditable»

Investigación **exploratoria** y **reproducible** sobre una pregunta concreta: en los datos abiertos de la Plataforma de Contratación del Sector Público (PLACSP), ¿se puede saber cómo terminó una obra pública?

**Resultado (corte 29/10/2026):** de 1.593 expedientes de obras adjudicados en 2023, de 1 a 10 M€, cuyo plazo teórico ya había vencido, en **1.549 (97,2 %)** no se detectó ningún anuncio de finalización, ningún documento con nombre de recepción, liquidación, certificación final, fin de obra o resolución del contrato, ni ninguna modificación cuya nota comunique el fin con una fórmula breve («se formaliza la liquidación del contrato»). La versión anterior del programa (v2.3), que no leía esas notas, daba 1.573 (98,7 %); la corrección y su alcance están en [`METODO.md`](METODO.md).

> **Qué NO dice esta cifra:** no dice que las obras estén sin terminar, ni que falten los documentos, ni que nadie incumpla ninguna obligación. Mide las **coincidencias que detecta un programa** en un canal concreto de datos abiertos. La información puede estar en otros sitios, como el Registro de Contratos del Sector Público o los registros autonómicos. Todo está explicado en [`METODO.md`](METODO.md).

**Hallazgo principal:** la PLACSP tiene, al menos desde 2024, un **«Anuncio de Finalización de Contrato»** estructurado (`DOC_CCN`), con la fecha real de fin y la causa. En esta población aparece en 8 de 1.651 expedientes.

## No necesitas ejecutar nada para leer los resultados

Las cifras ya están calculadas:

- **Informe para cualquier persona:** `resultados_v2_4/informe.html`. Descarga el repositorio (botón verde «Code» → «Download ZIP»), descomprímelo y abre ese archivo con doble clic: se ve en el navegador, con el resultado explicado. En la web de GitHub solo se ve su código.
- **Informe técnico:** [`resultados_v2_4/informe.md`](resultados_v2_4/informe.md), y las cifras en [`resultados_v2_4/resumen.json`](resultados_v2_4/resumen.json).
- **Método y limitaciones:** [`METODO.md`](METODO.md)

**No se publican listas de obras.** El proyecto no publica casos reales: una lista de obras con su organismo y si consta o no su final, aunque no juzgue a nadie, permitiría señalar a organismos concretos. Tampoco se publican los ficheros por expediente (`expedientes_seleccionados.csv`, `candidatos_fin.csv`, `empates_en_seleccion.csv`) ni las revisiones manuales caso por caso; sus resultados agregados están en [`METODO.md`](METODO.md).

**Cómo se verifica sin la lista.** El programa es abierto, los datos son los oficiales y [`manifiesto_descarga_estudio.json`](manifiesto_descarga_estudio.json) guarda sus huellas. Quien repita el análisis obtiene en su ordenador la lista completa (con buscador y enlace a la ficha oficial de cada obra) y puede comprobar con [`resultados_v2_4/huellas_resultados.json`](resultados_v2_4/huellas_resultados.json) que sus ficheros son **exactamente los mismos**, byte a byte, que dieron estas cifras. Es una garantía más fuerte que publicar la lista, porque demuestra que no se ha retocado.

- **El documento de trabajo:** [`../documento/`](../documento/)

## Qué hay aquí

| Archivo | Qué es |
|---|---|
| `METODO.md` | Método, resultados, revisiones, cambios y limitaciones. **Léelo antes de citar nada** |
| `CONTRASTE_REGISTRO_CONTRATOS.md` | Qué publican el Registro de Contratos estatal y el registro vasco |
| `medir_ejecucion.py` | El programa de medición (Python, solo biblioteca estándar, sin IA ni red) |
| `Abrir el programa.pyw` | Doble clic para abrir la interfaz gráfica en Windows, sin ventana de consola |
| `interfaz.py` | La interfaz gráfica, con dos pestañas: **el estudio** (descargar los datos, analizarlos y ver el resultado) y **el protocolo para organizaciones** (preparar las solicitudes del mes y llevar el registro; necesita la carpeta `protocolo_obras/` al lado) |
| `informe_legible.py` | Convierte los resultados en `informe.html` y `lista_obras.csv`, para leerlos sin conocimientos técnicos. No cambia ninguna cifra |
| `descargar_datos.py` | Descarga y verifica los datos oficiales (huellas SHA-256) |
| `test_medir_ejecucion.py` | Pruebas automáticas con datos ficticios |
| `manifiesto_descarga_estudio.json` | Ficheros exactos usados: URL, tamaño, SHA-256 y fecha |
| `resultados_v2_4/` | Resultados vigentes del estudio, solo agregados: informe legible (sin la lista de obras) y técnico, resumen, anexo por tipo de administración, manifiesto y huellas de los ficheros por expediente que no se publican |
| `huellas_resultados.py` | Calcula y comprueba las huellas de los ficheros por expediente de una ejecución |
| `../revisiones/` | Las revisiones adversariales entre modelos de IA (no independientes ni humanas), con sus encargos y respuestas |

## Requisitos

- **Python 3.11 o posterior** (https://www.python.org). No hace falta instalar nada más.
- **Unos 8 GB de disco** para los datos (13 ZIP, unos 7,6 GB) y algo más para los resultados.
- **Memoria:** el programa guarda en memoria la última versión de unos 670.000 expedientes. Con 8 GB de RAM es holgado; con menos, puede funcionar más despacio. Es una estimación, no lo he medido.
- **Tiempo:** la descarga tarda **varias horas** (el servidor oficial va a 0,5–3 MB/s). El análisis, unos minutos con un ordenador de varios núcleos.

## Instalar Python en Windows, paso a paso

Si nunca has usado Python:

1. Entra en **https://www.python.org/downloads/** y pulsa el botón amarillo **«Download Python»**.
2. Abre el archivo descargado. **Antes de pulsar «Install Now», marca la casilla «Add python.exe to PATH»**, abajo del todo. Es el paso que más se olvida.
3. Cuando termine, cierra el instalador.
4. Descarga este repositorio: botón verde **«Code» → «Download ZIP»** en la página del repositorio. Descomprímelo en una carpeta.
5. Abre esa carpeta y haz **doble clic en `Abrir el programa.pyw`**: se abrirá la ventana del programa. Si en vez de abrirse aparece un editor de texto, haz clic derecho sobre el archivo → «Abrir con» → «Python».
6. Sigue los tres pasos de la ventana: **datos**, **analizar** y **resultado**.

Si la ventana no se abre, escribe `cmd` en la barra de direcciones de la carpeta, pulsa Intro y, en la ventana negra que aparece, escribe:

```bash
python interfaz.py
```

En macOS, Python se instala igual desde python.org, y `interfaz.py` se abre con «Python Launcher». En Linux, si falla la interfaz, puede que haya que instalar el paquete `python3-tk`.

## Uso rápido

### Con la interfaz gráfica

```bash
python interfaz.py
```

La ventana tiene tres pasos:

1. **Los datos:** descargarlos de la web oficial (con barra de progreso y comprobación de que son los del estudio) o elegir la carpeta donde ya los tienes.
2. **Analizar:** un botón y una barra de progreso.
3. **El resultado:** la cifra principal y botones para abrir el informe en el navegador, la lista de obras en Excel o la carpeta.

Hay además un botón para ver los resultados del estudio sin analizar nada. Las opciones técnicas (carpeta de resultados, huellas, tareas en paralelo, pruebas) están plegadas en «Opciones avanzadas».

La segunda pestaña, **«Preguntar por obras»**, es el protocolo para organizaciones (`../protocolo_obras/`, guía en `GUIA.md`): prepara cada mes las solicitudes de acceso a información sobre el fin de obras concretas, abre las solicitudes, el registro y los pendientes, comprueba el registro, calcula lo que vence (con festivos propios si se dan) y prepara el borrador público. **No envía nada:** las solicitudes las presenta la organización.

### Por la línea de comandos

1. Pasar las pruebas:

```bash
python -m unittest -v test_medir_ejecucion
```

2. Descargar los datos oficiales y comprobar que son los mismos del estudio:

```bash
python descargar_datos.py reproducir --manifiesto manifiesto_descarga_estudio.json --destino datos
```

3. Medir (Git Bash, macOS o Linux):

```bash
python medir_ejecucion.py datos/*.zip --salida resultados
```

En PowerShell, los comodines no se expanden:

```powershell
python medir_ejecucion.py (Get-ChildItem datos\*.zip).FullName --salida resultados
```

4. Preparar el informe legible (`informe.html` y `lista_obras.csv`); la interfaz lo hace sola:

```bash
python informe_legible.py resultados
```

Si `descargar_datos.py` avisa de que las huellas no coinciden, Hacienda ha regenerado los ficheros. En ese caso no se **reproduce** el estudio, sino que se **repite** con otros datos. Para medir con datos actuales:

```bash
python descargar_datos.py actualizar --anuales 2023 2024 2025 --mensuales 202601 202602 --destino datos_nuevos
```

## Cómo leer los resultados

Al repetir el análisis, en tu carpeta de resultados aparecen estos ficheros. Los que llevan la lista de obras se quedan en tu ordenador: el proyecto no los publica (para comprobar que coinciden con el estudio, `python huellas_resultados.py comprobar resultados_v2_4 TU_CARPETA`).

- `informe.html`: el resultado explicado en lenguaje llano, qué significa y qué no, y la lista de obras con buscador, filtros y enlace a la ficha oficial. Se abre en el navegador. La versión publicada en `resultados_v2_4/` no lleva la lista (`informe_legible.py --publico`).
- `lista_obras.csv`: la misma lista para Excel o LibreOffice en español (coma decimal, fechas dd/mm/aaaa).
- `informe.md`: el informe técnico, con el resultado principal, las sensibilidades y los diagnósticos.
- `expedientes_seleccionados.csv`: una fila por expediente, con enlace a su ficha en la PLACSP.
- `candidatos_fin.csv`: los expedientes con alguna evidencia de fin y de dónde sale cada una.
- `anexo_por_tipo_administracion.md`: **exploratorio, no comparable**. No sirve para clasificar organismos.

## Estado y mantenimiento

Este material se entrega **tal cual y no tiene mantenimiento**. Quien lo publicó no va a responder incidencias ni a actualizarlo. Si te resulta útil, **haz una copia (fork) y conviértete en su responsable**. La especificación de la PLACSP cambia (por ejemplo, el anuncio `DOC_CCN` no estaba en la especificación de 2024), así que conviene revisar el programa antes de usarlo con datos nuevos.

Ha sido elaborado con ayuda de modelos de IA (Claude y ChatGPT, en rondas de revisión cruzada) y **no lo ha revisado ningún jurista ni ningún estadístico**.

## Licencia

Código bajo **MIT-0** y documentos bajo **CC0 1.0**: puedes hacer lo que quieras con todo, sin pedir permiso ni citar a nadie. Ver [`LICENSE`](../LICENSE). Los datos de origen tienen sus propias condiciones de reutilización.
