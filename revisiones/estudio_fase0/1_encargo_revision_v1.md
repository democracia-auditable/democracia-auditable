# Encargo: revisión adversarial de la fase 0 de «Democracia Auditable»

**Fecha:** 30/10/2026 · **Preparado por:** Claude, para revisión independiente por ChatGPT.
**Lo que se pide:** intentar **romper** este trabajo. No se busca aprobación ni acuerdo entre modelos; que coincidamos no prueba nada.

---

## 1. Contexto en cinco líneas

El documento «Democracia Auditable» v0.4.1 apuesta (§8.6, §9.0) a que los datos de **ejecución** de los contratos públicos (modificaciones, recepción, liquidación, importe final) no son accesibles para la ciudadanía contrato a contrato, aunque se comuniquen al Registro de Contratos del Sector Público.

Para comprobarlo, Claude ha escrito un programa (Python, solo biblioteca estándar, sin IA) que lee los datos abiertos de la Plataforma de Contratación del Sector Público (PLACSP) de 2023 a octubre de 2026 y mide, para las obras adjudicadas en 2023, qué consta de su ejecución.

El objetivo final es entregar a organizaciones cívicas **el documento, este resultado y el programa**, como un método probado en un sector que otros puedan aplicar a otros.

## 2. Resultado que debes intentar refutar

De **1.631 contratos de obras** adjudicados en 2023, con un presupuesto base sin IVA de entre 1 y 10 millones de euros:

- el **96,4 %** tiene ya vencido su plazo previsto (estimado);
- y de esos, en el **99,4 %** no consta en los datos abiertos de la PLACSP **ningún documento de recepción, liquidación, certificación ni fin de obra**.

Formulación que se propone publicar: *«de estos contratos no consta en los datos abiertos de la PLACSP cómo terminaron»*. No se afirma retraso, abandono ni incumplimiento.

## 3. Archivos

| Archivo | Qué es |
|---|---|
| `METODO.md` | Fuente, criterios, revisión manual, correcciones y limitaciones. **Léelo primero.** |
| `medir_ejecucion.py` | El programa |
| `test_medir_ejecucion.py` | 11 pruebas con datos ficticios (`python -m unittest -v test_medir_ejecucion`) |
| `resultados/informe.md` | Informe generado con todos los datos |
| `resultados/contratos_seleccionados.csv` | Una fila por contrato (1.631), separador `;` |
| `resultados/resumen.json` | Cifras de lectura de datos |
| `revision_manual_muestra_30.csv` | Comparación manual de 30 contratos con la web de la PLACSP |
| `datos_muestra/muestra_real_2024_un_fichero.zip` | **Un** fichero ATOM real (497 entradas) para que puedas ejecutar el programa. Los datos completos ocupan unos 6 GB comprimidos y no se adjuntan. |

Para ejecutarlo con la muestra:

```
python medir_ejecucion.py datos_muestra/muestra_real_2024_un_fichero.zip --salida prueba --procesos 1
```

Salen 5 contratos seleccionados. Con un solo fichero, el resultado **no** es representativo; sirve para comprobar el código.

## 4. Preguntas concretas

Responde a cada una con **«encontrado un error»** (con la evidencia), **«no encontrado»** o **«no puedo comprobarlo»**. Marca qué has verificado tú (ejecutando código o leyendo una fuente primaria) y qué es inferencia.

1. **Código.** ¿Hay errores en `medir_ejecucion.py`? En especial:
   - (a) la deduplicación por `atom:id` quedándose con la versión de `updated` más reciente;
   - (b) el tratamiento de las entradas eliminadas (`at:deleted-entry`);
   - (c) la navegación por la estructura CODICE, que lee hijos directos y no descendientes;
   - (d) el cálculo de `fin_previsto`.
2. **Supuesto de foto completa.** El programa supone que cada entrada ATOM es la foto completa de la licitación y no un cambio parcial. Si eso fuera falso, ¿qué se rompería? ¿Hay algo en la especificación de sindicación de la PLACSP (versión del 17/09/2024) que lo contradiga?
3. **Selección.** ¿Es correcto exigir un código de resultado de adjudicación (TenderResultCode 1, 2, 8 o 9) y la primera fecha de adjudicación en 2023? ¿Se cuelan o se pierden contratos por lotes, por acuerdos marco o por contratos basados?
4. **Dónde podrían estar los documentos de fin.** ¿Hay algún campo o elemento de la sindicación, o algún otro conjunto de datos abiertos oficial (por ejemplo, del Registro de Contratos del Sector Público), donde la recepción, la liquidación o el importe final **sí** consten y el programa no los esté mirando? Si existe, el resultado principal es falso.
5. **Detección por nombre de archivo.** ¿Qué patrones de nombre de documentos de fin de obra pueden escaparse a las expresiones regulares de `CATEGORIAS_DOCUMENTO`? Propón casos concretos.
6. **Inferencia a partir de la muestra.** Con 0 discrepancias en 30 contratos sobre documentos de fin, ¿es correcto decir que, como mucho, se escaparían documentos en un 10 % aproximado de los contratos (regla del tres)? ¿Invalida algo que la muestra se sortease antes de corregir la población?
7. **Correcciones a posteriori.** Dos correcciones se hicieron después de ver los datos: excluir desiertas y añadir categorías de incidencias. ¿Están bien declaradas? ¿Cambian lo que puede afirmarse?
8. **Interpretación.** ¿La frase «no consta en los datos abiertos de la PLACSP cómo terminaron» es fiel a los datos, o sugiere más de lo que se ha medido? Propón una redacción mejor si la tienes.
9. **Tipos de administración.** `METODO.md` desaconseja comparar administraciones porque conviven dos versiones de la lista de códigos (1.04 y 2.10). ¿Estás de acuerdo, o hay una forma correcta de hacer esa comparación?
10. **Relación con el documento.** ¿Este resultado apoya la apuesta de la §8.6 de la v0.4.1, o solo demuestra algo más pequeño? ¿Qué no puede concluirse de él?

## 5. Reglas

- **No reescribas** el programa ni el método enteros. Señala errores concretos, con línea o con un ejemplo.
- No inventes campos de la especificación ni conjuntos de datos: si citas uno, da la fuente y di si la has comprobado.
- No incluyas nombres ni datos de personas. Los órganos de contratación son entidades públicas y se pueden mencionar.
- Si todo te parece correcto, dilo y explica **qué intentaste** para romperlo y no pudiste.

## 6. Entrega

Un único archivo Markdown con:
1. las respuestas a las diez preguntas, en orden;
2. una lista de errores encontrados, ordenada por gravedad;
3. lo que, en tu opinión, **no debería afirmarse** al entregar este resultado.
