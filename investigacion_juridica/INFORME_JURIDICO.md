# Rama 4: ¿es obligatorio publicar el fin de un contrato de obras?

**1 de noviembre de 2026. Exploratorio. Lectura de normas por un no jurista; no lo ha revisado ningún jurista.** Complementa la fase 0 de «Democracia Auditable» (§9.0 bis), la investigación del anuncio de finalización (`investigacion_doc_ccn`) y la rama 2 (`investigacion_cohortes`).

**Pregunta:** el estudio encuentra que en el 97–99 % de las obras con plazo teórico vencido no consta en la PLACSP ningún indicio de fin. ¿Falta algo que la ley obliga a publicar, o la ley no lo exige?

**Fuentes:** texto consolidado del BOE, descargado el 01/11/2026 con la API de datos abiertos (`https://www.boe.es/datosabiertos/api/legislacion-consolidada/id/<norma>/texto/bloque/<bloque>`; se toma la última versión de cada bloque), y documentación técnica oficial de la PLACSP. Copias y huellas en `fuentes/` (tabla al final).

## Respuesta corta

1. **Publicar el fin no es obligatorio** con carácter general en el perfil de contratante. Ni la LCSP (art. 63.3) ni la Ley 19/2013 (art. 8.1.a) lo incluyen entre la información mínima. La propia PLACSP califica su anuncio de finalización de **«carácter voluntario»**, y el formulario europeo equivalente (eForms E5) también es voluntario.
2. **Comunicar el fin sí es obligatorio, pero a otros destinatarios.** El órgano de contratación debe comunicar al **Registro de Contratos del Sector Público** el importe final y la extinción (art. 346.3 LCSP) y, en los contratos de obras de más de 600.000 €, también al **Tribunal de Cuentas** u órgano autonómico de fiscalización, incluida la «extinción normal o anormal» (art. 335).
3. **El fin queda documentado por obligación legal:** el acta de recepción (art. 243.2) y la certificación final, que debe aprobarse en tres meses (art. 243.1). Esos documentos «obran en poder» de la Administración y son, por tanto, **información pública** a efectos del derecho de acceso (Ley 19/2013, art. 13).

**Consecuencia para el estudio:** la cifra del estudio (97,2 % tras la corrección de la v2.4; 98,7 % cuando se escribió este informe) **no mide un incumplimiento** de una obligación de publicar, y no debe presentarse así. Mide una **brecha entre lo que la Administración está obligada a saber, y a comunicar a otros órganos, y lo que publica en abierto**. Es lo que el documento ya dice con prudencia (§9.0 bis) y lo que justifica el protocolo: si la información existe pero no se publica, la vía es preguntarla y dejar constancia de la respuesta.

## Detalle

### 1. Lo que debe publicarse en el perfil de contratante

**LCSP, art. 63.3** (sin modificaciones desde 2018). Información mínima de cada contrato: memoria, pliegos, objeto, duración, presupuesto, importe de adjudicación, anuncios de información previa, de licitación, de adjudicación y de formalización, **anuncios de modificación**, licitadores, actas, resolución de adjudicación, y además la decisión de no adjudicar, el desistimiento, la declaración de desierto y los recursos. **No menciona la recepción, la liquidación, la certificación final, la resolución del contrato ni su extinción.** El art. 63.2 permite publicar «cualesquiera datos y documentos», pero no lo exige.

**LCSP, art. 154.** Anuncio de formalización: obligatorio, en el perfil en 15 días y en el DOUE si es armonizado.

**LCSP, art. 207.3.** Toda modificación, armonizada o no, debe publicarse en el perfil **en 5 días**, con las alegaciones del contratista y los informes.

**Ley 19/2013, art. 8.1.a** (versión vigente desde el 29/07/2022). Publicidad activa de todos los contratos: objeto, duración, importes, procedimiento, licitadores, adjudicatario, **modificaciones**, desistimiento y renuncia. **Tampoco incluye la ejecución ni el fin.**

> **Asimetría:** la ley obliga a publicar en 5 días que un contrato se ha modificado, pero no obliga a publicar cuándo ni cómo terminó.

### 2. El anuncio de finalización de la PLACSP

Descripción funcional de los servicios de la PLACSP para órganos de contratación, **v3.9 (26/06/2024)**, apartado 5.12, p. 78, versión en la que se añadió el anuncio:

> «Es un Anuncio de carácter voluntario.» El anuncio no se envía al BOE ni, «por el momento», al DOUE. Está disponible en todos los procedimientos y en los contratos menores, y cada anuncio se refiere a un único contrato: en las licitaciones con lotes, a un único lote o adjudicatario.

La **v3.10 (18/12/2025)**, la más reciente encontrada, mantiene el mismo texto (p. 81). Las versiones 3.11 y 4.0 a 4.5 no existen en la ruta oficial (HTTP 404, 01/11/2026).

Esto explica dos resultados de la rama 1. Primero, que el anuncio aparezca en una minoría de expedientes. Segundo, la discrepancia entre la sindicación y la web en los expedientes con varios lotes: el diseño prevé un anuncio por lote.

### 3. El nivel europeo

Documentación de eForms (TED, versión actual): el «Contract completion notice», subtipo **E5**, se describe como «Voluntary». La Directiva 2014/24/UE no impone un anuncio de finalización; esta revisión no ha analizado su texto artículo por artículo.

### 4. Lo que debe comunicarse a otros órganos

**LCSP, art. 346.3:** los poderes adjudicadores comunicarán al Registro, «en su caso, las modificaciones, prórrogas, variaciones de plazos o de precio, importe final y extinción». El contenido, el formato y el plazo «se establecerán reglamentariamente».

**RD 817/2009, art. 31 y anexo I** (BOE-A-2009-8053; sin modificaciones en esos bloques). Dictado para la ley anterior; se aplica aquí en lo que no se oponga a la LCSP de 2017, porque no se ha encontrado norma posterior que lo sustituya (**punto que debe confirmar un jurista**):
- Datos de fin que se exigen (anexo I, III): «Importe final del contrato por todos los conceptos», «Causa de resolución (en su caso)» y «Fecha de resolución (en su caso)». **Para un contrato que termina con normalidad no se pide ninguna fecha de fin o de recepción.**
- Plazo (art. 31.2): antes de que termine el primer trimestre del año siguiente; para el importe final y la extinción, la fecha de referencia es la de la extinción.

**LCSP, art. 346.5:** el Registro «facilitará el acceso público a los datos que no tengan el carácter de confidenciales y que no hayan sido previamente publicados de modo telemático y a través de Internet», con los límites de protección de datos. **No se ha encontrado un servicio público de descarga de los datos de fin del Registro estatal**; algunas administraciones publican los de sus registros propios.

**LCSP, art. 335.1–2:** remisión al Tribunal de Cuentas u órgano autonómico de fiscalización de los contratos de obras de más de 600.000 € y comunicación de «el importe final, la nulidad y la extinción normal o anormal». Esas comunicaciones no son públicas.

### 5. Lo que debe existir en el expediente

- **Art. 210.2:** «un acto formal y positivo de recepción o conformidad dentro del mes siguiente» a la entrega.
- **Art. 243.1–2 (obras):** acta de recepción; certificación final aprobada en tres meses desde la recepción, ampliables a cinco en obras de más de 12 M€ con liquidación compleja; plazo de garantía de al menos un año.
- **Ley 19/2013, art. 13:** es información pública todo contenido o documento que obre en poder de la Administración y se haya elaborado en ejercicio de sus funciones. **Art. 20.1:** plazo máximo de un mes para resolver una solicitud de acceso.

## Qué cambia y qué no

- **Para el estudio:** confirma la redacción actual. No hay que hablar de incumplimiento, y la cifra describe una práctica de publicación sobre un mecanismo voluntario y documentos de publicación no obligatoria.
- **Para la propuesta:** precisa la recomendación del Anexo A.6, filas 39 y 51 (publicar por contrato lo ya comunicado al Registro). Esa publicación ya está prevista en el art. 346.5 para los datos no publicados, pero lo que el reglamento obliga a comunicar del fin es poco: el importe final y, si hubo resolución, su causa y su fecha. Una obligación de publicar la **fecha de recepción** requeriría un cambio normativo o de práctica, aunque el dato ya existe en el expediente (art. 243).
- **Para el protocolo:** es su caso de uso más claro. Un dato que la ley obliga a producir (el acta de recepción) y a comunicar (el importe final y la extinción), pero no a publicar, se puede pedir por la vía de acceso, con plazo de un mes, y la respuesta o el silencio quedarían registrados una sola vez para todos.

## Límites

- **Lectura de un no jurista, sin revisión jurídica.** No se ha consultado jurisprudencia, doctrina ni informes de juntas consultivas.
- **Solo normas estatales.** Las comunidades autónomas con plataforma propia pueden tener normas o prácticas distintas; el informe de la OIReScon de 2024 (módulo XI) señala que Navarra dispone de un anuncio de finalización. Tampoco se han revisado normas sectoriales, como las de fondos europeos, ni los pliegos de cada contrato, que pueden imponer obligaciones adicionales.
- **Vigencia del RD 817/2009** tras la LCSP de 2017: se ha asumido, no verificado con un análisis de derogaciones.
- **Acceso al Registro estatal:** no se ha comprobado qué datos facilita en la práctica. La resolución del Consejo de Transparencia R/0155/2021, que según un buscador trata del Registro, no pudo descargarse (HTTP 404); queda para la rama 5.

## Fuentes (descargadas el 01/11/2026)

| Norma o documento | Bloque o páginas | Versión vigente usada | Fichero |
|---|---|---|---|
| Ley 9/2017 (BOE-A-2017-12902) | arts. 63, 154, 207, 210, 243, 335, 346, 347 | 09/03/2018, salvo arts. 154 y 347: 23/04/2021 | `fuentes/lcsp_art*.xml` / `.txt` |
| Ley 19/2013 (BOE-A-2013-12887) | arts. 8, 13, 14, 20 | art. 8: 29/07/2022; resto: 10/12/2014 | `fuentes/l19_art*.txt` |
| RD 817/2009 (BOE-A-2009-8053) | art. 31, anexo I | 16/06/2009 | `fuentes/rd817_registro.txt`, `fuentes/rd817_anexoI.txt` |
| PLACSP, Descripción funcional WS órganos de contratación v3.9 | apdo. 5.12, p. 78 | 26/06/2024 | `fuentes/descargas/placsp_ws_oc_v3.9.pdf` (SHA-256 e93f42c314f8072856b444dcd16a06540b2ad0ff0913ce63ad2a9f76d2b1254f) |
| Ídem v3.10 | p. 81 | 18/12/2025 | `fuentes/descargas/placsp_ws_oc_v3.10.pdf` (SHA-256 f60c55bf627572bb78a8973c4671ef42bd6a3d8c8817c7e18ac77f5f69fe2b14) |
| TED, eForms «Documents, forms & notices» | tabla 1 | documentación vigente | https://docs.ted.europa.eu/eforms/latest/schema/documents-forms-and-notices.html |

URL de los PDF de la PLACSP: `https://contrataciondelestado.es/b2b/DGPE_PLACE_WS_OC.DescripcionFuncionalv3.9.pdf` y `…v3.10.pdf`.

## Tras la revisión adversarial (02/11/2026)

- **Los documentos deben existir cuando se produce la fase correspondiente,** no en todo expediente: el acta de recepción si la obra se ha recibido y, después, la certificación final (art. 243). Puede haber particularidades (lotes, fases, contratos resueltos).
- **La obligación de comunicar el fin se aplica en los supuestos que fija la ley:** al Registro, con excepciones (art. 346.3); al Tribunal de Cuentas, solo por encima de ciertos umbrales (art. 335). La aplicación plena del RD 817/2009 tras la LCSP de 2017 sigue **pendiente de dictamen jurídico**.
- **Cómputo de plazos:** el art. 20.1 de la Ley 19/2013 cuenta el mes desde la **recepción por el órgano competente**, y si el último día es inhábil se prorroga al siguiente hábil (Ley 39/2015, art. 30.5; texto en `protocolo_obras/fuentes/l39_art30.txt`).
