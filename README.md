# Democracia Auditable

**Un protocolo abierto para reconstruir qué se sabía de una decisión pública, qué se advirtió y qué se respondió.** Su primera aplicación es reproducible y no usa inteligencia artificial: comprueba qué dicen los datos abiertos de la Plataforma de Contratación del Sector Público (PLACSP) sobre cómo terminan las obras públicas, e incluye herramientas para preguntarlo cuando no consta.

> **Este material se publica deliberadamente como borrador incompleto, para facilitar su revisión crítica independiente.** Las críticas, refutaciones y versiones mejoradas son el uso esperado, no un problema.

**Estado: borrador crítico.**
- Elaborado y revisado con modelos de IA, en rondas de revisión adversarial cruzada entre Claude y ChatGPT.
- **No lo ha revisado ningún jurista, estadístico ni auditor humano.**
- El protocolo de preguntas sobre obras es un diseño para un piloto: **no es apto para presentar solicitudes reales sin una revisión jurídica previa**.

## Úsalo como quieras

No es un paquete que haya que adoptar entero. Puedes leerlo, trocearlo, quedarte con una idea, un programa o una plantilla, adaptarlo a lo que ya haces o descartarlo. Código bajo **MIT-0** y textos bajo **CC0 1.0**: no hace falta pedir permiso ni citar a nadie.

## Leer sin ejecutar nada

| Si quieres… | Abre |
|---|---|
| Hacerte una idea en pocas páginas | [`documento/Democracia_Auditable_resumen_v0_4_9.pdf`](documento/Democracia_Auditable_resumen_v0_4_9.pdf) |
| Leer la propuesta completa | [`documento/Democracia_Auditable_v0_4_9.pdf`](documento/Democracia_Auditable_v0_4_9.pdf) |
| Ver el resultado del estudio explicado | `fase0_placsp/resultados_v2_4/informe.html` (descarga el repositorio y ábrelo con doble clic; en GitHub solo se ve el código) |
| Ver el informe técnico y las cifras | [`fase0_placsp/resultados_v2_4/informe.md`](fase0_placsp/resultados_v2_4/informe.md) y [`resumen.json`](fase0_placsp/resultados_v2_4/resumen.json) |
| Entender cómo se midió y sus límites | [`fase0_placsp/METODO.md`](fase0_placsp/METODO.md) |
| Leer cada investigación complementaria | el informe `.md` de cada carpeta `investigacion_*` (tabla de abajo) |
| Ver cómo se aplicaría el protocolo | [`protocolo_obras/GUIA.md`](protocolo_obras/GUIA.md) (uso) y [`protocolo_obras/PROTOCOLO_OBRAS.md`](protocolo_obras/PROTOCOLO_OBRAS.md) (reglas) |
| Ver qué se discutió en cada revisión | [`revisiones/`](revisiones/) |

## El resultado principal

De 1.593 expedientes de obras adjudicados en 2023, de 1 a 10 M€ (presupuesto base sin IVA) y con el plazo teórico vencido el 29/10/2026, en **1.549 (97,2 %)** el programa no detectó en los datos abiertos ningún indicador de finalización o extinción: ni anuncio de finalización, ni documento de recepción, liquidación, certificación final, fin de obra o resolución, ni una modificación que comunique el fin.

**Qué no dice:** no dice que las obras estén sin terminar, ni que falten los documentos, ni que nadie incumpla ninguna obligación, porque publicar el fin no es obligatorio en ese canal. Mide lo que detecta un programa en un canal concreto. Todo está en [`fase0_placsp/METODO.md`](fase0_placsp/METODO.md).

## Mapa: qué hay y qué se puede usar por separado

**Los textos se entienden solos.** El documento, los informes, la guía, las plantillas y la tabla de plazos se pueden leer y reutilizar sin nada más.

**El código comparte dos piezas:**
- `fase0_placsp/medir_ejecucion.py`, que lee los datos de la PLACSP;
- el escáner de `investigacion_doc_ccn/`, que busca los anuncios de finalización.

Para ejecutar una carpeta, descarga el repositorio entero y no muevas las carpetas, porque los programas se buscan entre sí por su posición.

| Carpeta | Qué es | Para ejecutarla necesita |
|---|---|---|
| `documento/` | El documento de trabajo (v0.4.9) y su presentación breve, en Markdown y PDF | — |
| `fase0_placsp/` | **El estudio:** descarga y verificación de los datos, el programa de medición (v2.4), la interfaz gráfica, el método, los resultados agregados y las huellas | Nada más (es la base del resto) |
| `investigacion_doc_ccn/` | El anuncio de finalización de contrato por dentro | `fase0_placsp/` |
| `investigacion_cohortes/` | ¿Es cuestión de tiempo? Cohortes de 2021 y 2022, y validación del clasificador con 60 obras | `investigacion_doc_ccn/` (que genera sus datos) y `fase0_placsp/` |
| `investigacion_juridica/` | Marco jurídico, con los artículos descargados del BOE | — (solo texto) |
| `investigacion_consejo/` | Qué resuelven el Consejo de Transparencia y dos órganos autonómicos cuando se pide el fin de una obra | — (datos de cada órgano) |
| `investigacion_registro_vasco/` | Un registro autonómico que sí publica el fin | — (datos de Euskadi) |
| `investigacion_inicio/` | ¿Se puede saber si una obra empezó? (preregistrada) | `fase0_placsp/`, `investigacion_doc_ccn/` |
| `investigacion_modificaciones/` | Qué traen los anuncios de modificación (preregistrada) | `fase0_placsp/`, `investigacion_doc_ccn/`, `investigacion_inicio/` |
| `investigacion_terminacion/` | La coincidencia «terminación licitada de nuevo» (comparación preregistrada) | `fase0_placsp/`, `investigacion_doc_ccn/`, `protocolo_obras/` |
| `protocolo_obras/` | **El protocolo de preguntas sobre el fin de las obras:** reglas, guía, plantillas, plazos por régimen jurídico (con la cita del BOE), herramientas y pruebas | Para elegir obras: `fase0_placsp/` e `investigacion_doc_ccn/`. El registro (`registro.py`), la tabla de plazos (`regimenes.py`) y las plantillas funcionan solos |
| `revisiones/` | Encargos, revisiones adversariales y respuestas punto por punto | — |

## Ejecutarlo

Requiere **Python 3.11 o posterior**. Usa solo la biblioteca estándar: no hay que instalar nada más. La interfaz usa tkinter, que viene incluido en Windows y macOS.

**Con ventanas, sin programar.** En Windows, doble clic en `fase0_placsp/Abrir el programa.pyw`; en macOS o Linux, `python fase0_placsp/interfaz.py`. La ventana tiene dos pestañas:
- **El estudio:** descargar los datos, analizarlos y ver el resultado.
- **El protocolo:** preparar las solicitudes del mes y llevar el registro.

[`fase0_placsp/README.md`](fase0_placsp/README.md) explica paso a paso cómo instalar Python.

**Por la línea de órdenes.** Para repetir el estudio, desde `fase0_placsp/`:

```bash
python descargar_datos.py reproducir --manifiesto manifiesto_descarga_estudio.json --destino datos
python medir_ejecucion.py datos/*.zip --salida resultados
python informe_legible.py resultados
```

La descarga son 13 ficheros, unos 7,6 GB, y tarda varias horas; el análisis, unos minutos. Para el protocolo, [`protocolo_obras/GUIA.md`](protocolo_obras/GUIA.md) explica el ciclo mensual (`ciclo_mensual.py`) y el registro (`registro.py`).

## No se publican listas de obras

El proyecto **no publica listas de casos del estudio**. No publica:
- listas de obras con su órgano;
- las revisiones manuales caso por caso;
- las obras marcadas por ninguna señal;
- la lista de resoluciones autonómicas clasificadas;
- resultados individuales del protocolo.

Una lista así, aunque no juzgue a nadie, permitiría señalar a organismos concretos. **Sí se citan resoluciones públicas de los órganos de garantía como precedentes de un criterio jurídico**, por su número, como se cita cualquier doctrina publicada.

**Cómo se verifica sin la lista.**
- El programa es abierto, los datos son los oficiales y `fase0_placsp/manifiesto_descarga_estudio.json` guarda sus huellas.
- Quien repita el análisis obtiene la lista completa en su ordenador.
- Con `fase0_placsp/resultados_v2_4/huellas_resultados.json` puede comprobar que sus ficheros por expediente son idénticos, byte a byte, a los que dieron las cifras publicadas. Tras los tres pasos anteriores:

```bash
python huellas_resultados.py comprobar resultados_v2_4 resultados
```

## Comprobar que todo funciona

Desde la raíz del repositorio:

```bash
python -X utf8 -m unittest discover -s fase0_placsp -p "test_*.py"
python -X utf8 investigacion_doc_ccn/test_escanear.py
python -I -X utf8 protocolo_obras/test_protocolo.py
python -I -X utf8 protocolo_obras/test_revision_v045.py
python -I -X utf8 protocolo_obras/test_revision_v046.py
python -I -X utf8 protocolo_obras/test_revision_v047.py
python -I -X utf8 investigacion_terminacion/test_equivalencia.py
```

Deben pasar todas (32, 7, 48, 26, 26, 14 y 1). Ninguna se salta si el repositorio está completo. Usan datos ficticios: comprueban que los programas hacen lo que dicen, no que las cifras del estudio sean exactas.

## Mantenimiento y licencia

Este material se entrega **tal cual y sin mantenimiento**: quien lo publicó no va a responder incidencias ni a actualizarlo. Si te resulta útil, **haz una copia y conviértete en su responsable**. La especificación de la PLACSP cambia, así que conviene revisar los programas antes de usarlos con datos nuevos.

Código bajo **MIT-0** y documentos bajo **CC0 1.0** (ver `LICENSE` y `LICENSE-CC0-1.0.txt`). Los datos de origen tienen sus propias condiciones de reutilización.
