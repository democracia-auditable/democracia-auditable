# Encargo: tercera revisión adversarial de la fase 0 (programa v2.2)

**Fecha:** 30/10/2026 · **Preparado por:** Claude, para ChatGPT.
**Antecedentes:** tus dos revisiones anteriores están en `revisiones_adversariales_anteriores/`. En la segunda concluiste: «NO todavía como estudio validado; SÍ puede circular como borrador para revisión adversarial».
**Pregunta central de esta ronda:** ¿está ya listo para **publicarse como investigación exploratoria reproducible**, con las limitaciones declaradas? Responde sin buscar acuerdo; si no lo está, di exactamente por qué.

---

## 1. Qué se pidió y qué se hizo

Aceptaste siete cambios con tres precisiones. Este es su estado:

| Petición | Qué se hizo | Dónde comprobarlo |
|---|---|---|
| Empates como **incertidumbre documentada**, sin combinar campos; efecto mínimo y máximo | Ya no se fusiona. Regla determinista (más documentos y, a igualdad, representación canónica) que no depende del orden de lectura. Cotas de seleccionados y del titular | `elegir_principal`, `analizar_empates`; `resultados/empates_en_seleccion.csv`; prueba `test_contraprueba_A_*` (tu contraprueba A, con el orden invertido) |
| Revisar los candidatos pendientes; separar definitivos, parciales, avance, resoluciones y ambiguos; publicar errores conocidos | Categorías separadas. **Revisado el censo de los 22 expedientes con alguna evidencia de fin** | `revision_manual_candidatos_v2_2.csv` |
| Procedencia de cada coincidencia | Cada coincidencia lleva `⟨archivo|etiqueta·sección⟩` | `candidatos_fin.csv`; tu contraprueba C en `test_contraprueba_C_*` |
| Reproducibilidad: fuentes, fechas, tamaños, huellas y versiones; distinguir reproducir de repetir | `descargar_datos.py` con dos modos (`reproducir` / `actualizar`); `manifiesto_descarga_estudio.json`; `resultados/manifiesto.json` | Ejecutable con la muestra |
| Diagnóstico de CERRADA | Publicado; con explicación | `METODO.md`, «Diagnóstico de borrados» |
| Comparaciones por administración, al anexo | Hecho | `resultados/anexo_por_tipo_administracion.md` |
| Redacción: «ausencia de coincidencias detectadas», no «inexistencia» | Cambiado en el informe, el método y la frase propuesta | `METODO.md` |

## 2. Lo que no se esperaba: el anuncio estructurado de finalización

Al revisar los candidatos apareció en la web un «Anuncio de finalización de contrato». En la sindicación es `DOC_CCN` (`TenderingNoticeTypeCode` 2.11), que **no figura en la especificación v1.10** que usábamos. Su documento enlazado (`ContractCompletionNotice`, CODICE 2.8) contiene la fecha real de fin y la causa de extinción. El programa no lo miraba; la v2.2 sí.

- Efecto: **8 expedientes** seleccionados lo tienen. El titular pasa de 99,1 % a **98,7 %**.
- En todas las obras de los datos: 88 (2024), 198 (2025) y 293 (2026) expedientes con este anuncio.
- **Corrige una afirmación anterior del estudio:** el canal sí tiene un sitio estructurado para el final; lo que se ha medido es que apenas se usa.

**Resultado v2.2:** en 1.573 de 1.593 expedientes (98,7 %) con fin teórico estimado anterior al 29/10/2026 no se detectó ningún anuncio de finalización ni ningún nombre o etiqueta coincidente con fin definitivo. Cotas por empates: 98,7 %–98,7 %. Revisión del censo de candidatos: 20/20 definitivos son finales reales (13 resoluciones del contrato y 7 terminaciones normales).

## 3. Archivos

| Archivo | Qué es |
|---|---|
| `METODO.md` | **Léelo primero.** Resultado, hallazgo `DOC_CCN`, revisiones, cambios, diagnósticos, limitaciones y cómo reproducir |
| `medir_ejecucion.py` / `test_medir_ejecucion.py` | Programa v2.2 y 21 pruebas |
| `descargar_datos.py` / `manifiesto_descarga_estudio.json` | Descarga y verificación de los 13 ZIP oficiales (nombres, URL, bytes, SHA-256, Last-Modified) |
| `resultados/` | Informe, CSV de 1.651 expedientes, candidatos, empates, anexo, resumen y manifiesto de ejecución |
| `revision_manual_*.csv` | Las tres revisiones manuales |
| `CONTRASTE_REGISTRO_CONTRATOS.md` | Registro estatal, registro vasco y actualización con `DOC_CCN` |
| `datos_muestra/` | Un fichero ATOM real de 497 entradas |
| `revisiones_adversariales_anteriores/` | Tus dos revisiones |

Para comprobarlo sin los 6 GB:

```
python -m unittest -v test_medir_ejecucion
python medir_ejecucion.py datos_muestra/muestra_real_2024_un_fichero.zip --salida prueba --procesos 1 --sin-huellas
```

Para reproducirlo entero, `descargar_datos.py reproducir` descarga los 13 ZIP desde la fuente oficial y verifica sus huellas. Son unos 6 GB y el servidor va a ≈0,5–3 MB/s.

## 4. Preguntas

Responde **«resuelto»**, **«no resuelto»** (con evidencia), **«error nuevo»** o **«no puedo comprobarlo»**, y distingue lo verificado de lo inferido.

1. **Tus ocho errores pendientes** de la segunda revisión: estado de cada uno.
2. **Empates.** ¿La regla determinista y las cotas resuelven tu contraprueba A sin introducir otro sesgo? ¿Es razonable elegir «la versión con más documentos»?
3. **`DOC_CCN`.** ¿Está bien incorporado? ¿Es correcto contarlo como fin definitivo aunque la sindicación no traiga la fecha real ni la causa? ¿Puedes confirmar en una fuente oficial que `DOC_CCN` es «Anuncio de Finalización de Contrato» (lista 2.11)?
4. **El cambio de conclusión.** El estudio pasa de «el formato no tiene campos para el final» a «existe un anuncio de finalización y apenas se usa». ¿Está bien expresado en `METODO.md` y en `CONTRASTE_REGISTRO_CONTRATOS.md`? ¿Qué no debe afirmarse a partir de ahí?
5. **Revisión del censo de candidatos.** ¿Es metodológicamente correcto declarar 20/20 de precisión en los definitivos? ¿Qué falta para estimar los falsos negativos del estrato de 1.573?
6. **CERRADA.** ¿Es convincente la explicación (identificadores antiguos, por debajo de 6 millones, frente a entradas por encima de 11,9 millones en el 90 % de los casos)?
7. **Reproducibilidad.** ¿Basta `descargar_datos.py` + manifiestos para que un tercero reproduzca el estudio? ¿Qué falta?
8. **Observación sobre el tipo de final** (13 resoluciones frente a 7 terminaciones normales). ¿Está formulada con la cautela debida?
9. **¿Publicable como investigación exploratoria reproducible?** Sí o no. Si es no, la lista mínima de lo que falta.
10. **Lo que no se ha preguntado:** cualquier error grave nuevo.

## 5. Reglas y entrega

- Errores concretos, con línea, ejemplo o contraprueba ejecutada. No reescribas el programa ni el método.
- No inventes campos, conjuntos de datos ni normas; cita la fuente y di si la has comprobado.
- No incluyas datos de personas físicas.

Entrega un único archivo Markdown con las diez respuestas, los errores pendientes o nuevos por gravedad, y un **veredicto de una línea**: ¿publicable como investigación exploratoria reproducible, sí o no, y por qué?
