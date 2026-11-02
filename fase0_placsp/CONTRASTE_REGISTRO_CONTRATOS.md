# Contraste con el Registro de Contratos del Sector Público

**Fecha:** 30/10/2026 · **Pregunta:** ¿se publican en otro sitio, contrato a contrato, los datos de ejecución que no constan en la sindicación de la PLACSP?

## 1. Qué dice la ley

Art. 346 LCSP. Texto consultado en una reproducción secundaria (papelea.com); la revisión independiente de ChatGPT lo contrastó en el BOE.

- **346.3:** los órganos de contratación comunican al Registro los datos básicos de cada contrato y, «en su caso, las modificaciones, prórrogas, variaciones de plazos o de precio», **el importe final y la extinción**. El contenido, el formato y el plazo se fijan por reglamento.
- **346.5:** el Registro facilitará el acceso público a los datos no confidenciales, conforme a la ley de transparencia. No incluye los datos que ya se hayan publicado en internet por otra vía.
- **346.6:** las administraciones con un registro propio pueden sustituir la comunicación por un intercambio entre registros.

**Conclusión:** la ley obliga a **comunicar** los datos de ejecución. El acceso público es una obligación de «facilitar», sin un formato ni una forma de publicación concretos.

## 2. Qué publica el Registro estatal

Página del Ministerio de Hacienda sobre el Registro de Contratos del Sector Público (consultada el 30/10/2026).

- **Solo hay estadísticas agregadas**, por año (2013–2024) y por tipo de entidad (Estado, comunidades autónomas, entidades locales, universidades, mutuas). Son ficheros TXT separados por tabuladores y hojas Excel.
- He descargado dos ficheros de 2023 para comprobarlo. Contienen el **número de contratos y su importe por procedimiento de adjudicación** (abierto, simplificado, negociado, directo…) y por ministerio o por tipo de entidad local. Ejemplo: «AYUNTAMIENTOS — Abierto — 6.421.776.918 €».
- **No hay ficheros contrato a contrato**, ni campos de importe final, modificaciones, prórrogas o extinción.
- No he encontrado en las páginas oficiales consultadas ningún servicio de consulta pública de contratos individuales del Registro estatal. **Eso no prueba que no exista**; puede haber vías de acceso a petición, por la Ley 19/2013, que no se anuncian en la web.

## 3. Un registro autonómico que sí lo publica: País Vasco

El Registro de Contratos de la Comunidad Autónoma del País Vasco (un registro análogo de los del art. 346.6) publica en datos.gob.es y en opendata.euskadi.eus un fichero por entidad y año, con licencia CC BY 4.0.

He descargado el del **Gobierno Vasco de 2023** (actualizado el 03/05/2024): `doc_contratos_poder16135_2023.xlsx`, con **2.368 contratos, de ellos 431 de obras**. Tiene una fila por contrato y **63 columnas**, entre ellas:

`Estado contrato` · `Fecha fin plazo` · `Fecha fin contrato` · `Prórrogas` · `Modificaciones del Plazo` · `Modificaciones del Objeto` · `Modificación del adjudicatario` · `Incidencias contractuales` · `Datos resolución por finalización anticipada` · `Datos Finalizacion` · `Garantía` · campos de nulidad · `Continuidad del contrato`

En las 431 obras:

| Campo | Rellenos |
|---|---:|
| Estado del contrato | 431 (249 «Ejecución», 182 «Finalizado») |
| Fecha de fin del contrato | 412 |
| **Datos de finalización** (fecha e **importe de finalización**) | **182**: todos los marcados «Finalizado» |
| Incidencias contractuales | 6 |
| Prórrogas, modificaciones de plazo y de objeto | 0 |

Ejemplo literal de «Datos Finalizacion»: «Fecha finalización: 23/07/2023 00:00:00, Importe Finalización: 18.081».

**Lo que esto demuestra:** publicar contrato a contrato el estado, la fecha de finalización y el importe final **es técnicamente posible y alguien ya lo hace**, en formato abierto. Es exactamente lo que propone la §8.6.

**Lo que no demuestra:**
- que los campos vacíos (prórrogas, modificaciones) signifiquen que no las hubo, o que se omitan;
- que el «importe de finalización» sea el importe de la liquidación. No lo he comprobado contra ningún expediente;
- nada sobre otras comunidades autónomas.

## 3 bis. Actualización (v2.2): la propia PLACSP tiene un anuncio de finalización

Después de este contraste se descubrió que la PLACSP tiene un **«Anuncio de Finalización de Contrato»** (`DOC_CCN`, `TenderingNoticeTypeCode` 2.11, documento `ContractCompletionNotice` CODICE 2.8). Incluye la fecha real de fin, la causa de extinción y un anexo. Su uso es todavía escaso: 8 de los 1.651 expedientes seleccionados, y 88, 198 y 293 expedientes de obras en 2024, 2025 y 2026. Ver `METODO.md`.

**Propuesta a estudiar** (no conclusión probada): el cauce estatal ya existe (`DOC_CCN`) y el registro vasco muestra campos comparables. Una posible formulación de la §8.6 sería promover el uso sistemático de ese anuncio, o estudiar si lo que el art. 346.3 obliga a comunicar al Registro podría publicarse por esta vía.

Este estudio **no** ha establecido:
- si publicar `DOC_CCN` es obligatorio en algún caso;
- que exista una equivalencia entre la obligación de comunicar al Registro (art. 346.3, «en su caso») y la publicación de ese anuncio. El canal, el plazo y la publicidad de cada obligación se rigen por normas distintas, y eso es una cuestión jurídica.

Los recuentos por año (88, 198 y 293) son **numeradores sin denominador**: muestran que el tipo de anuncio se usa, no una tasa de uso ni de cumplimiento.

## 4. Consecuencias para el estudio

1. **El hallazgo se mantiene, pero hay que acotarlo.** Lo que hemos medido es la sindicación estatal de la PLACSP, de expedientes alojados en ella. Al menos un registro autonómico publica los datos de ejecución que en la PLACSP no constan.
2. **Aporta ejemplos concretos para la propuesta de la §8.6, sin probarla.** Existen dos modelos en funcionamiento: los campos del registro vasco y el anuncio `DOC_CCN` de la PLACSP. Que existan muestra que publicar estos datos es técnicamente viable. No resuelve qué obligación jurídica corresponde a cada órgano ni si basta con publicar por esas vías, que es lo que tendría que estudiar un jurista.
3. **Pregunta abierta para quien continúe:**
   - ¿Qué publican los demás registros autonómicos?
   - ¿Qué responde el Ministerio de Hacienda a una solicitud de acceso (Ley 19/2013) a los datos de ejecución de una muestra de contratos del Registro estatal?

   Lo segundo exige identificarse. Queda para una organización.
4. **Limitación nueva del estudio:** los expedientes de entidades vascas (y de otras plataformas autonómicas) pueden no estar en la sindicación «perfiles ubicados en la PLACSP». El resultado no puede extrapolarse a esos territorios.

## Fuentes consultadas

- Ley 9/2017, art. 346 (reproducción en papelea.com): https://papelea.com/es/leyes/ley-de-contratos-del-sector-publico/libro-cuarto_titulo-ii_capitulo-ii. Texto oficial: https://www.boe.es/buscar/act.php?id=BOE-A-2017-12902
- Ministerio de Hacienda, Registro de Contratos del Sector Público: https://www.hacienda.gob.es/es-es/areas%20tematicas/contratacion/junta%20consultiva%20de%20contratacion%20administrativa/paginas/registro%20publico%20de%20contratos.aspx
- Ficheros agregados descargados: `Contratos2023-EELL-Importes-Porcentajes.txt` y `Contratos2023-Estado-Numero.txt`, en `https://www.hacienda.gob.es/DGPatrimonio/Junta%20Consultiva/Documentos%20txt%20registro%20de%20contratos/2023/`
- datos.gob.es, «Registro de contratos de Gobierno Vasco del 2023»: https://datos.gob.es/en/catalogo/a16003011-registro-de-contratos-de-gobierno-vasco-del-2023
- Fichero descargado: https://opendata.euskadi.eus/contenidos/ds_contrataciones/contratos_poder16135_2023/es_contracc/adjuntos/doc_contratos_poder16135_2023.xlsx
- No disponibles a 30/10/2026 (error 404): una resolución del Consejo de Transparencia (RT 0119/2021) y la «Contratopedia» de Civio, que aparecían en las búsquedas.
