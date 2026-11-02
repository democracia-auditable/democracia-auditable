# Coincidencia «terminación licitada de nuevo»: qué hace, qué se sabe y cómo refinarla

**Estado (2 de noviembre de 2026, tras la revisión adversarial de la v0.4.5):** asociación con los contratos resueltos observada en una comparación preregistrada, en un corpus **parcialmente expuesto al diseño** de la regla; **sin validación externa**. Sensibilidad muy baja. Código: `senal_terminacion.py`. Informe completo: `investigacion_terminacion/INFORME_TERMINACION.md`.

## Qué hace

Marca una obra A cuando **el mismo órgano licita después otra obra B** cuyo título casi repite el de A y habla de terminarla: «terminación», «finalización», «conclusión», «resto de obras», «obras pendientes» o «completar las obras».

**La idea:** una licitación posterior para «terminar» la misma obra es **compatible** con que el primer contrato no la terminara (resolución, abandono…), pero también con una recepción parcial, un alcance complementario, otra financiación o fases mal descritas en los títulos. Es una coincidencia documental que **obliga a verificar**, no una prueba.

**Condiciones exactas** (todas a la vez):

| Nº | Condición | Parámetro en el código |
|---|---|---|
| 1 | B es del mismo órgano (identificador; si no hay, nombre) | `Indice.organo` |
| 2 | El primer anuncio de B es posterior al inicio de A (o a su adjudicación, si no consta el inicio) | — |
| 3 | Ni A ni B son acuerdos marco ni describen una parte dentro de otra obra («en/para la(s) obra(s) de») | `AM`, `PARTE` |
| 4 | El título de B contiene vocabulario de terminación | `TERMIN` |
| 5 | Parecido de títulos: Jaccard de palabras significativas ≥ 0,6. Son significativas las de 4 o más letras o cifras, sin tildes, excluidas las genéricas | `UMBRAL_JACCARD`, `VACIAS` |
| 6 | Misma fase, lote, etapa o tramo, o ninguno en ambos | `FASE` |
| 7 | Si ambos títulos tienen números (sin contar años 1990–2039), comparten al menos uno | `numeros` |
| 8 | Si A tiene palabras raras (las que aparecen en 100 títulos o menos de todo el corpus), su Jaccard con las raras de B es ≥ 0,5 | `RARA_DF`, `UMBRAL_RARAS` |

## Qué se sabe

**Comparación con obras de final conocido** (preregistrada; 50.000 € o más, adjudicadas en 2019–2023):

| | Indicios documentales de resolución (grupo R) | Indicios de terminación ordinaria (grupo N) |
|---|---:|---:|
| Marcados | 10 de 273 (3,7 %) | 2 de 558 (0,4 %) |

- **Cociente:** 10,2 (IC95 2,3–46,3); Fisher exacta p = 0,0004. Intervalo muy ancho.
- **No es una validación independiente:** la regla se diseñó viendo dos de los tres tramos de importe de la tabla. En el único tramo ajeno al diseño (50.000–200.000 €), 3 de 103 frente a 0 de 193: prometedor, pero no concluyente por sí solo.
- **Las proporciones no son trasladables** a obras sin final publicado, y el 83 % de resueltos entre las 12 marcadas depende de cuántas obras hay en cada grupo: no es la probabilidad de que una obra marcada se haya resuelto.

**Lo más importante: una marca obliga a verificar; su ausencia no informa sobre el estado de la obra.** La regla marca a muy pocos expedientes del grupo R (10 de 273), que a su vez son solo las resoluciones que se publican de forma reconocible: la mayoría de los contratos resueltos no deja una segunda licitación con un título reconocible.

**Otras limitaciones:**
- **Avisa con retraso:** la nueva licitación llega entre uno y tres años después.
- **Depende del vocabulario de los títulos.**
- **Números pequeños:** 10 y 2 marcas en la validación, de ahí la anchura del intervalo.
- **Validez externa y sesgo de espectro:** los grupos se forman por lo que se publica, y las obras que publican su final pueden no representar a las demás. Varias obras de un mismo órgano no son casos independientes.
- **Diseño y revisión:** se diseñó viendo obras de 0,2–1 M€ y de 1 M€ o más, y la precisión de los títulos la revisó el mismo sistema que la escribió.
- **Lo que significa una marca:** una **coincidencia documental que requiere comprobación**, no un fracaso ni una resolución probados. En una muestra de 20 obras marcadas sin final publicado, ninguna página web mostraba la resolución; puede constar en otros canales o no haber existido.

**Uso en el protocolo:**
- La columna `senal_terminacion` de cada lote indica qué licitación la provoca. **El lote es un fichero de trabajo privado** (excluido en `.gitignore`); `registro.py exportar` no incluye esa columna.
- Con `--prioridad terminacion`, las obras marcadas pasan primero cuando el tope obliga a aplazar. La muestra fija se sortea antes y no depende de esta opción.
- La plantilla pide el estado del contrato y, solo si existen, el acta de recepción o el acuerdo de resolución, sin presuponer cuál. **La lista de obras marcadas no se publica**, ni se usa para afirmar nada de un órgano.

## Cómo refinarla

Cualquier cambio (un umbral, una palabra, una condición nueva) cambia la regla. Para que la versión refinada valga, hay que **repetir la validación con el mismo método**, no basta con mirar si «parece mejor».

1. **Antes de tocar nada**, escribir y fijar con huella un preregistro: qué se cambia, por qué y qué resultado se considerará mejor. Plantilla: `investigacion_terminacion/PREREGISTRO.md`.
2. **Diseñar con unas obras y probar con otras.** Separar un tramo, unos años o un conjunto de órganos que no se miren durante el diseño, y que la prueba principal sea **solo** sobre esa parte. La v2 no lo cumplió del todo: se diseñó viendo obras de 0,2–1 M€ y de 1 M€ o más, que también entraron en la tabla principal; solo el tramo de 50.000–200.000 € era ajeno al diseño. Registrar el preregistro en un servicio con fecha verificable antes de analizar.
3. **Validar con obras de final conocido:** ejecutar `investigacion_terminacion/validar_e4t.py` (que usa este módulo; `test_equivalencia.py` comprueba que la versión vigente marca lo mismo que la congelada), y comparar contratos resueltos frente a terminados con normalidad. Mantener los mismos criterios: cociente de al menos 3, límite inferior del IC95 mayor que 1 y al menos 5 casos marcados en el grupo de resueltos.
4. **Medir la sensibilidad** (qué proporción de los resueltos marca) y la proporción de resueltos entre las marcadas. Una versión que capte más resoluciones a costa de muchas falsas alarmas puede no ser mejor: publicar las dos cifras.
5. **Comprobar a mano una muestra** de obras marcadas en su página web, y que la revise alguien distinto de quien escribió la regla.
6. **Actualizar este fichero, `senal_terminacion.py` y sus pruebas,** conservando la versión anterior con su huella.

**Ideas que no se han probado** (cada una exigiría el procedimiento anterior):
- **Ampliar el vocabulario de B:** «reanudación», «continuación», «obras inacabadas», «paralizadas», «nueva adjudicación del resto».
- **Usar también el objeto o el CPV**, no solo el título, para emparejar A y B.
- **Combinarla con los textos de modificación de A** (suspensiones, «resolución» en trámite) para ganar sensibilidad.
- **Buscar B también en otros órganos del mismo grupo de entidades** (por ejemplo, una sociedad pública que licita lo que empezó su administración matriz).
- **Medir el tiempo entre el fin teórico de A y la licitación de B**, para estimar cuánto se tarda en reaccionar.

**Fallos conocidos de la v2** (revisión de títulos de la consulta privada):
- encargos de oficios redactados como «para la obra: …»;
- partes distintas de un mismo edificio que la regla confunde con la misma obra.
