# Encargo de revisión adversarial: «Democracia Auditable» v0.4.4

**Para:** ChatGPT
**Fecha:** 2 de noviembre de 2026
**Qué se pide:** intentar **romper** lo que cambia en la v0.4.4, no aprobarlo. Ya revisaste la v0.4.3 y el estudio del anuncio de finalización. Esta es la revisión final antes de distribuir el documento.

## Qué ha cambiado desde tu última revisión

1. **La cifra principal de la fase 0 baja del 98,7 % al 97,2 %.** Algunos órganos comunican la liquidación o la certificación final en el texto (`cbc:Note`) de un anuncio de modificación. El programa no leía ese campo y ahora sí (versión 2.4). Son 24 expedientes, revisados a mano.
2. **Nueva §9.0 ter:** resume ocho investigaciones complementarias, dos de ellas preregistradas.
3. **Nuevo Anexo D:** diseño de un protocolo de preguntas sobre el fin de las obras, con herramientas.

## Material adjunto

| Carpeta | Contenido |
|---|---|
| `documento/` | v0.4.4 en Markdown y PDF. El registro de cambios está en el Anexo A.8 |
| `fase0_placsp/` | `METODO.md`, `medir_ejecucion.py` v2.4, sus pruebas y el resumen, el informe y el manifiesto de la v2.4 |
| `investigaciones/` | Un informe por investigación, con sus programas y, en las preregistradas, el preregistro y su huella |
| `protocolo_obras/` | Ficha del protocolo, plantillas, herramientas y pruebas |

No se adjuntan los datos de la PLACSP ni los ficheros intermedios con enlaces, textos o datos de órganos y adjudicatarios. Si necesitas una cifra concreta, pídela y se calculará.

## Preguntas concretas

1. **La corrección v2.4** (`medir_ejecucion.py`: `FIN_EN_NOTA`, `EXCL_FIN_EN_NOTA`; `INFORME_MODIFICACIONES.md`).
   - ¿Es legítimo contar como fin una liquidación comunicada en el texto de una modificación?
   - ¿El patrón deja fuera formulaciones habituales o puede meter falsos positivos? Por ejemplo, «liquidación» a secas, o una certificación final de una fase.
   - El 63 % de esos textos procede de un solo órgano: ¿cambia la lectura de la cifra?
2. **Formulación del 97,2 %.** ¿Está bien trazada la corrección en la nota de versión, el §8.6, el §9.0 bis y el Anexo A.8? ¿Queda algún 98,7 % que pueda confundir?
3. **§9.0 ter, punto por punto.** ¿Hay alguna afirmación que vaya más allá de su informe? En particular:
   - **Jurídica:** que publicar el fin no es obligatorio; la vigencia del RD 817/2009 tras la LCSP de 2017; la asimetría con el art. 207.3; que la cifra «no mide un incumplimiento».
   - **Consejo de Transparencia:** que las cifras de silencio se refieren a reclamaciones, no a solicitudes; la lectura de «estimatoria por motivos formales»; si once resoluciones bastan para hablar de un criterio.
4. **Investigación del inicio** (preregistrada, `INFORME_INICIO.md`).
   - ¿Es válida la calibración con la última versión anterior al anuncio de finalización?
   - ¿Está bien razonado el sentido del sesgo (quien publica su fin puede publicar más)?
   - ¿Se puede concluir que la ausencia de rastro «no distingue» una obra terminada de una sin empezar?
5. **Investigación de las modificaciones** (preregistrada).
   - La definición de «opaca».
   - El uso del nombre de los documentos como aproximación a los informes del art. 207.3.
   - El tratamiento de las ampliaciones de plazo (art. 203.1).
   - Qué significa la fecha `ContractModification/IssueDate` del XML del anuncio.
6. **Registro vasco.** ¿Se justifica descartar 2018 por sesgo de selección? ¿Es correcto el filtro de 50.000 € como aproximación a los contratos menores?
7. **Protocolo (Anexo D y `protocolo_obras/`).**
   - **Riesgo de abuso de derecho:** ¿bastan la regla de una sola pregunta por obra, el tope de 4 por órgano y mes y la finalidad declarada en la solicitud?
   - **Plazos:** el margen de 120 días; la recomendación de reclamar en un mes ante el silencio; el cómputo de «un mes» en `registro.py` (`mas_meses`).
   - **La plantilla:** ¿alguna frase invita a inadmitir (reelaboración, información auxiliar)?
   - **Órganos de garantía:** ¿la asignación por tipo de entidad y provincia tiene errores?
   - **La muestra de 200:** ¿es razonable para estimar lo acumulado?
8. **Código.** Busca errores sobre todo en:
   - `medir_ejecucion.py` (el cambio de la v2.4);
   - `seleccionar_obras.py` (reutiliza la política de versiones del estudio; el sorteo y la lista fija de la muestra);
   - `registro.py` (validación y plazos);
   - `escanear_versiones.py` y `analizar_inicio.py` (versión anterior al anuncio; intervalo de Clopper-Pearson).
9. **Reglas del proyecto.** ¿Hay algo en el documento o en los informes que nombre, compare o permita señalar a un órgano o a una persona?

## Formato de respuesta

Para cada problema:
- **a)** dónde está;
- **b)** qué falla;
- **c)** gravedad: bloqueante, importante o menor;
- **d)** corrección propuesta.

Al final, un veredicto: si la v0.4.4 puede distribuirse como documento de trabajo, y con qué cambios.
