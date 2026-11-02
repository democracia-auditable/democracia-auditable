# Encargo de revisión adversarial: «Democracia Auditable» v0.4.6 (comprobación de correcciones)

**Para:** ChatGPT
**Fecha:** 2 de noviembre de 2026
**Qué se pide:** comprobar que las correcciones de tu revisión de la v0.4.5 están **bien hechas** y no han introducido errores nuevos. Esta vez el paquete es **el repositorio completo tal como se publicaría** (`democracia-auditable/`), no una selección: debe funcionar entero desde una copia limpia.

## Qué ha cambiado

La respuesta punto por punto a tu revisión está en `democracia-auditable/revisiones/v0_4_5/respuesta_revision_v0_4_5.md`, y el registro de cambios del documento, en el Anexo A.10 de la v0.4.6. Lo principal:
1. **Plazos por régimen jurídico** (`protocolo_obras/regimenes.py`, fragmentos del BOE en `protocolo_obras/fuentes/regimenes/`). Ya no se calcula ninguna fecha sin un régimen verificado.
2. **Fallos de las herramientas corregidos**, cada uno con una prueba en `protocolo_obras/test_revision_v045.py`: muestra, sorteo, validación, tope, ciclo, reanudación, festivos, exportación y origen de cada solicitud.
3. **La novena investigación, recalificada** como asociación preregistrada en un corpus parcialmente expuesto al diseño. Además, 66 órganos (no 69) y `test_equivalencia.py`.
4. **Órganos autonómicos:** recuento estricto y filtro reproducible.
5. **El repositorio ya no publica listas de obras con su órgano:** cifras agregadas, informe legible sin la lista y `huellas_resultados.json`, que se comprobó con una repetición completa del análisis.

## Qué comprobar

1. **Pruebas:** ejecuta las cinco órdenes del `README.md` de la raíz. Deben pasar todas y ninguna debe saltarse.
2. **Tabla de regímenes:**
   - ¿Cada fila de `regimenes.py` coincide con el fragmento del BOE que cita?
   - ¿Hay algún régimen mal clasificado como verificado?
   - ¿Falta alguna comunidad o algún caso dudoso?
   - ¿Es correcta la regla de que «veinte días» sin más son hábiles (Ley 39/2015, art. 30.2)?
3. **Cómputo:** ¿son correctos `mas_habiles`, `limite` y los mensajes de `pendientes` para cada tipo de régimen (meses, días hábiles, reclamación sin plazo, sin verificar)?
4. **Cada punto de la respuesta:** ¿está resuelto de verdad en el código o el texto, o solo en la respuesta?
5. **Privacidad:** ¿queda en el repositorio algo que nombre o permita señalar a un órgano o a una persona? Por ejemplo, ficheros de datos, enlaces a expedientes concretos o ejemplos reales.
6. **Coherencia:** ¿coinciden las cifras y las formulaciones entre el documento, los informes, la guía, la interfaz y los READMEs? ¿Queda algún «validada», «muy fiable», «4 %», «58 % de las reclamaciones» o «todos favorables» fuera de su contexto histórico?
7. **Cualquier error nuevo** introducido por las correcciones.

No se adjuntan los datos de la PLACSP. Si necesitas una cifra del corpus, pídela y se calculará.

## Formato de respuesta

Para cada problema:
- **a)** dónde está;
- **b)** qué falla;
- **c)** gravedad: bloqueante, importante o menor;
- **d)** corrección propuesta.

Al final, un veredicto: si la v0.4.6 y el repositorio pueden distribuirse como borrador crítico, y con qué cambios.
