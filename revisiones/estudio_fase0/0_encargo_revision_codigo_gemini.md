# Encargo: revisión de código de `medir_ejecucion.py`

**Fecha:** 30/10/2026 · **Preparado por:** Claude, para revisión independiente por Gemini.
**Lo que se pide:** encontrar **errores en el código**. No hace falta opinar sobre el proyecto ni sobre sus conclusiones: de eso se ocupa otra revisión.

---

## 1. Qué hace el programa

`medir_ejecucion.py` (Python 3.11+, solo biblioteca estándar) lee los ZIP de datos abiertos de la Plataforma de Contratación del Sector Público (PLACSP). Contienen ficheros ATOM con entradas en formato CODICE. Para cada licitación se queda con la versión más reciente y selecciona las obras adjudicadas en 2023 con un presupuesto de entre 1 y 10 millones de euros. Después mide, contrato a contrato, si constan modificaciones y documentos de ejecución (recepción, liquidación, ampliaciones de plazo…). Esos documentos se detectan por su nombre de archivo.

El resultado principal: de 1.631 contratos seleccionados, en el 99,4 % de los que tienen el plazo previsto vencido no consta ningún documento de fin de obra. **Si el código tiene un error que infle esa cifra, es lo que más importa encontrar.**

`METODO.md` explica los criterios y limitaciones, por si necesitas contexto.

## 2. Archivos

| Archivo | Qué es |
|---|---|
| `medir_ejecucion.py` | El programa que hay que revisar |
| `test_medir_ejecucion.py` | 11 pruebas con datos ficticios |
| `METODO.md` | Contexto: criterios, revisión manual y limitaciones |
| `datos_muestra/muestra_real_2024_un_fichero.zip` | Un fichero ATOM real de la PLACSP (497 entradas) |

```
python -m unittest -v test_medir_ejecucion
python medir_ejecucion.py datos_muestra/muestra_real_2024_un_fichero.zip --salida prueba --procesos 1
```

Con la muestra salen 5 contratos seleccionados.

## 3. Qué revisar, por orden de importancia

1. **Deduplicación y versiones** (`medir`, `fecha`). Se queda con la entrada de `updated` más reciente por `atom:id`, y descarta las eliminadas por `at:deleted-entry` si la eliminación es igual o posterior. ¿Hay casos en que se quede con una versión equivocada? Piensa en zonas horarias, fechas sin zona, fechas iguales, o un mismo id en varios ZIP.
2. **Extracción CODICE** (`extraer`). Se navega por hijos directos (`child`, `children`) por nombre local, ignorando el espacio de nombres. ¿Puede leer un campo equivocado, o no encontrar uno que sí existe (por ejemplo, en licitaciones con lotes, `ProcurementProjectLot`)?
3. **Selección** (`seleccionado`, `RESULTADOS_ADJUDICADOS`). ¿La lógica de estado, código de resultado, fecha de adjudicación y presupuesto hace lo que dice `METODO.md`?
4. **Detección de documentos** (`CATEGORIAS_DOCUMENTO`, `clasificar_documento`, `normalizar`). ¿Qué nombres reales de documentos de recepción, liquidación o fin de obra **no** detectarían estas expresiones regulares? ¿Qué falsos positivos siguen entrando? Da ejemplos concretos de cadenas.
5. **Fin previsto** (`a_dias`, cálculo de `fin`). ¿Errores con unidades (`DAY`, `MON`, `ANN`), duraciones nulas o negativas, fechas mal formadas, o el orden de las modificaciones?
6. **Informe** (`escribir_informe`). ¿Algún porcentaje se calcula sobre un denominador equivocado?
7. **Pruebas.** ¿Qué casos importantes no cubren las pruebas? Si puedes, escribe pruebas nuevas que fallen y demuestren un error.

## 4. Reglas

- Para cada error: **dónde** (función o línea), **qué entrada lo provoca**, **qué sale mal** y **cuánto puede afectar al resultado principal** (mucho, poco o nada).
- Distingue lo que has **comprobado ejecutando código** de lo que **deduces leyendo**.
- No reescribas el programa entero. Si propones un cambio, que sea pequeño y concreto.
- Si no encuentras errores en un apartado, dilo y explica qué probaste.

## 5. Entrega

Un único archivo Markdown con una lista de errores ordenada por gravedad, las pruebas nuevas que propongas y una valoración final de una frase: **¿puede el código haber inflado el 99,4 %?**
