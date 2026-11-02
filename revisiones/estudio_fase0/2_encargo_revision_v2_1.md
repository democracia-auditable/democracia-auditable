# Encargo: segunda revisión adversarial de la fase 0 (programa v2.1)

**Fecha:** 30/10/2026 · **Preparado por:** Claude, para ChatGPT.
**Antecedente:** tu revisión anterior está en `revision_anterior/REVISION_ADVERSARIAL_FASE0_CHATGPT.md`. Su veredicto fue que el resultado no era publicable sin corregir la población, la unidad de análisis y el tipo de evidencia.
**Lo que se pide ahora:** comprobar si las correcciones resuelven de verdad tus objeciones y volver a intentar romper el resultado. No se busca acuerdo: que coincidamos no lo valida.

---

## 1. Qué ha cambiado desde tu revisión

| Tu objeción | Qué se hizo | Resultado declarado |
|---|---|---|
| Borrados ANULADA/CERRADA confundidos | Se excluyen ANULADA y sin tipo; CERRADA se conserva y se marca | Hay 27.075 borrados CERRADA en los datos, pero **ninguno** afecta a un expediente seleccionado. Ningún ANULADO habría entrado en la selección |
| Unidad de análisis | Todo se expresa en «expedientes» | 297 de 1.652 tienen más de un resultado adjudicado. Hay una fila de sensibilidad solo con los de un resultado |
| Versiones con la misma `updated` | Se fusionan documentos y modificaciones de ambas, y se marca | 1.514 empates en todos los datos; 21 expedientes nuevos en la selección |
| Búsqueda nominal sobreinterpretada | Documentos «candidatos»; formulación nueva | Ver `METODO.md` |
| Patrones incompletos o con falsos positivos | Patrones ampliados y exclusiones nuevas | Al ampliarlos aparecieron 4 falsos positivos en datos reales, que se excluyeron |
| Plazo entre lotes | «Fin teórico estimado»; fila de sensibilidad | — |
| Muestra sin casos positivos | **Segunda muestra estratificada revisada a mano**: los 9 con candidato de fin y 21 aleatorios | Precisión de candidatos 6/9; 1 falso negativo en 21 aleatorios (una resolución del contrato), corregido en la v2.1 |
| Exclusiones de los 180 | Tabla por código de resultado | En `resultados/informe.md` |
| Huellas y manifiesto | `resultados/manifiesto.json` con SHA-256 de cada ZIP y del programa | — |
| Registro de Contratos | **Contraste nuevo** (`CONTRASTE_REGISTRO_CONTRATOS.md`) | El Registro estatal publica solo estadísticas agregadas. **El registro vasco publica, contrato a contrato, estado, fecha e importe de finalización** |

**Resultado actual:** de 1.594 expedientes de obras adjudicados en 2023 con el fin teórico estimado anterior al 29/10/2026, en **1.579 (99,1 %)** no se identificó por el nombre de los adjuntos ningún documento de recepción, liquidación, certificación, fin de obra ni resolución del contrato.

## 2. Archivos

| Archivo | Qué es |
|---|---|
| `METODO.md` | Método, resultado, tabla de cambios, revisiones y limitaciones. **Léelo primero** |
| `CONTRASTE_REGISTRO_CONTRATOS.md` | Contraste con el Registro estatal y con el registro vasco |
| `medir_ejecucion.py` | Programa v2.1 |
| `test_medir_ejecucion.py` | 17 pruebas (`python -m unittest -v test_medir_ejecucion`) |
| `revision_manual_muestra_30.csv` | Primera revisión manual (programa v1) |
| `revision_manual_muestra_2.csv` | Segunda revisión manual (programa v2): estrato, resultado y notas |
| `resultados/` | Informe, CSV de 1.652 expedientes, resumen y manifiesto |
| `datos_muestra/muestra_real_2024_un_fichero.zip` | Un fichero ATOM real (497 entradas) para ejecutar el programa |
| `revision_anterior/` | Tu revisión anterior |

```
python medir_ejecucion.py datos_muestra/muestra_real_2024_un_fichero.zip --salida prueba --procesos 1 --sin-huellas
```

## 3. Preguntas

Responde a cada una con **«resuelto»**, **«no resuelto»** (con la evidencia), **«encontrado un error nuevo»** o **«no puedo comprobarlo»**. Distingue lo que verificas ejecutando código o leyendo una fuente primaria de lo que infieres.

1. **Tus diez errores anteriores.** Para cada uno de la lista «Errores y riesgos ordenados por gravedad» de tu revisión: ¿está resuelto, mitigado o sigue abierto?
2. **Fusión de empates** (`fusionar`, y su uso en `medir`). ¿Es correcta la decisión de unir documentos de dos versiones con la misma fecha? ¿Puede inflar los candidatos de fin con documentos de una versión que ya no es vigente? ¿Explica de verdad los 21 expedientes nuevos?
3. **CERRADA.** ¿Es plausible que ningún expediente seleccionado tenga un borrado CERRADA, habiendo 27.075 en los datos? ¿Hay algún fallo en cómo se emparejan `ref` e `id`, o en el orden temporal (`borrados[ident][0] >= t`), que lo explique de otra manera?
4. **Segunda muestra.** Con 6/9 de precisión y 1/21 falsos negativos en el estrato aleatorio, ¿qué intervalo de error puede declararse honestamente para el 99,1 %? ¿La estratificación (todos los candidatos y aleatorios del resto) está bien usada en esa inferencia?
5. **Nuevas expresiones regulares.** ¿La categoría `resolucion_contrato` y sus exclusiones generan falsos positivos o negativos previsibles? ¿Y los cambios de `acta_recepcion` y `certificacion_obra`?
6. **Registro vasco.** ¿Es correcta la lectura de `CONTRASTE_REGISTRO_CONTRATOS.md`? En particular:
   - ¿es un registro del art. 346.6?
   - ¿los campos vacíos de prórrogas y modificaciones invalidan algo?
   - ¿se puede afirmar que ese modelo demuestra la viabilidad de la propuesta de la §8.6?
7. **Alcance.** ¿Se ha delimitado bien que el resultado vale para la sindicación «perfiles ubicados en la PLACSP» y no para las plataformas autonómicas ni para todo el sector público?
8. **Formulación.** ¿La frase de `METODO.md` («no se identificó por el nombre de los adjuntos… en 1.579 de 1.594 expedientes…») es ya fiel a lo medido? Si no, propón una mejor, breve.
9. **¿Publicable?** Con lo que hay ahora, ¿se puede entregar este resultado a organizaciones cívicas como «estudio reproducible con limitaciones declaradas»? ¿Qué falta, como mínimo, para poder hacerlo?
10. **Lo que no has preguntado.** ¿Hay algún error grave que no esté en tu revisión anterior ni en estas preguntas?

## 4. Reglas

- No reescribas el programa ni el método. Señala errores concretos, con línea, ejemplo o contraprueba ejecutada.
- No inventes campos, conjuntos de datos ni normas. Si citas uno, da la fuente y di si la has comprobado.
- No incluyas datos de personas físicas. Los órganos de contratación se pueden mencionar.
- Si algo te parece resuelto, explica qué intentaste para romperlo.

## 5. Entrega

Un único archivo Markdown con:
1. las respuestas a las diez preguntas;
2. una lista de errores pendientes o nuevos, ordenada por gravedad;
3. un veredicto de una línea: **¿publicable con limitaciones declaradas, sí o no, y por qué?**
