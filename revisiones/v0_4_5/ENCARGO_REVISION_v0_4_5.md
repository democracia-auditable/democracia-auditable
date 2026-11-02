# Encargo de revisión adversarial: «Democracia Auditable» v0.4.5

**Para:** ChatGPT
**Fecha:** 2 de noviembre de 2026
**Qué se pide:** intentar **romper** lo que cambia en la v0.4.5, no aprobarlo. Ya revisaste la v0.4.4. Es la última revisión antes de distribuir el documento y publicar el repositorio. El objetivo es dejarlo todo pulido y cerrado, así que interesan también los problemas menores.

## Qué ha cambiado desde tu última revisión

1. **Respuesta a tu revisión de la v0.4.4.** Tu informe y la respuesta punto por punto están en `revision_anterior/`. Comprueba que cada corrección está bien hecha y que no ha introducido errores nuevos.
2. **Novena investigación** (§9.0 ter, punto 9; `investigaciones/9_terminacion/`). Es una señal de «terminación licitada de nuevo»: el mismo órgano licita después la terminación de una obra, lo que sugiere que el primer contrato no la terminó.
   - La regla se diseñó revisando a mano obras sin final publicado y se congeló con huella antes de validarla.
   - Se validó de forma preregistrada con obras de final conocido: marca el 3,7 % de los contratos resueltos frente al 0,4 % de los terminados con normalidad.
   - Es muy específica y poco sensible: capta en torno al 4 % de las resoluciones.
3. **Órganos de garantía autonómicos** (§9.0 ter, punto 5; `investigaciones/5_consejo/COMPLEMENTO_AUTONOMICO.md`). Recibirían el 58 % de las reclamaciones del protocolo. En dos de ellos, revisados de forma sistemática, ningún caso sobre el fin de obras públicas se desestimó, y al menos uno admite reclamar contra el silencio sin plazo preclusivo.
4. **Protocolo** (Anexo D; `protocolo_obras/`).
   - Prioridad opcional por la señal (`--prioridad terminacion`), ahora también en el ciclo mensual.
   - Regla del plazo para reclamar matizada según el órgano.
   - Guía de la señal (`SENAL_TERMINACION.md`).
5. **Interfaz gráfica** (`fase0_placsp/interfaz.py`, capturas en `capturas/`). Una pestaña nueva hace todo el protocolo sin terminal. Además:
   - el informe legible del estudio (`informe_legible.py`) fallaba con los resultados de la v2.4 y se ha corregido;
   - el README del estudio todavía daba el 98,7 % como cifra vigente y se ha corregido.

Registro de cambios: Anexo A.9, filas 84 a 88.

## Material adjunto

| Carpeta | Contenido |
|---|---|
| `documento/` | v0.4.5 en Markdown y PDF |
| `revision_anterior/` | Tu revisión de la v0.4.4 y la respuesta punto por punto |
| `fase0_placsp/` | Método, README, programa v2.4 y pruebas, informe legible, interfaz gráfica, y resumen, informe y manifiesto de la v2.4 |
| `investigaciones/` | Un informe por investigación, con sus programas y, en las tres preregistradas, el preregistro y su huella |
| `protocolo_obras/` | Reglas, guía, guía de la señal, plantillas, herramientas y pruebas |
| `capturas/` | La interfaz gráfica: pestaña del estudio y pestaña del protocolo |

**Lo que no se adjunta:**
- los datos de la PLACSP;
- los ficheros intermedios con enlaces, títulos o datos de órganos y adjudicatarios;
- la lista de obras marcadas por la señal, que no se publica nunca.

Si necesitas una cifra concreta, pídela y se calculará.

## Preguntas concretas

1. **Tu revisión anterior.** ¿Queda alguno de tus puntos mal resuelto, resuelto solo en parte o contradicho en otro sitio del documento?
2. **La señal de terminación** (`INFORME_TERMINACION.md`, `PREREGISTRO.md`, `validar_e4t.py`, `senal_terminacion.py`, `SENAL_TERMINACION.md`).
   - **Fuga entre diseño y validación:** la regla se ajustó mirando obras sin final publicado y se validó con obras de final conocido. ¿Son poblaciones bastante separadas? ¿Pudo el diseño inflar la validación?
   - **Grupos:** el grupo R (resueltos) y el grupo N (terminación ordinaria) se definen por lo que se publica. ¿Hay sesgo de espectro, es decir, quien publica la resolución es distinto de quien no la publica? ¿Cambia la lectura del cociente de 10,2?
   - **Estadística:** con 10 y 2 casos marcados, ¿son correctos el IC95 logarítmico (`cociente`) y la prueba exacta de Fisher bilateral (`fisher_bilateral`)? ¿Las tablas por tramo de importe, que no estaban como principal en el preregistro, se presentan de forma que no parezcan confirmatorias?
   - **Formulación:** ¿«capta en torno al 4 % de las resoluciones» es una descripción correcta de 10 de 273? ¿Queda claro en todos los sitios que una obra no marcada no dice nada?
   - **Uso:** ¿la lectura «posible terminación anticipada no reflejada en la plataforma, no contrato fracasado» está mantenida en el documento, la guía, la interfaz y las columnas del lote?
3. **Órganos autonómicos.** ¿Alguna afirmación del documento o del protocolo va más allá del complemento? Solo dos citas se verificaron de forma independiente. ¿Está bien dicho que el plazo para reclamar «varía según el órgano»?
4. **Protocolo.**
   - **Prioridad por la señal:** ¿puede funcionar en la práctica como una forma de señalar a un órgano? Ten en cuenta que la columna del lote nombra la licitación que la provoca.
   - **Tope:** la interfaz deja cambiar el tope por órgano y mes en «Opciones avanzadas», con un aviso. ¿Basta, o debería ser fijo?
   - **Reclamaciones:** ¿siguen sirviendo la regla del mes prudencial, la plantilla de reclamación y la asignación del órgano de garantía, que sigue siendo una sugerencia sin verificar?
5. **Interfaz y facilidad de uso** (`interfaz.py`, capturas, `GUIA.md`).
   - ¿Hay algo que pueda llevar a una organización a enviar sin revisar, a publicar el borrador sin revisarlo o a creer que la herramienta presenta las solicitudes?
   - ¿Hay textos confusos o que contradigan la guía?
   - ¿Falta alguna función de la línea de comandos que una organización necesite?
6. **Código.** Busca errores sobre todo en:
   - `interfaz.py`: órdenes que lanza, cancelación, validación de entradas, rutas y apertura de ficheros;
   - `ciclo_mensual.py`: `--prioridad`;
   - `informe_legible.py`: categorías de las notas de modificación y comprobación contra `resumen.json`;
   - `senal_terminacion.py` y `validar_e4t.py`: ¿son equivalentes a la regla congelada `regla_e4t_v2.py`?;
   - `seleccionar_obras.py`: prioridad y columna de la señal.
7. **Cifras.** ¿Queda algún 98,7 % que se lea como cifra vigente? ¿Coinciden todas las cifras de la §9.0 ter con sus informes?
8. **Reglas del proyecto.** ¿Hay algo en el documento, los informes, la guía, la interfaz o las capturas que nombre, compare o permita señalar a un órgano o a una persona?

## Formato de respuesta

Para cada problema:
- **a)** dónde está;
- **b)** qué falla;
- **c)** gravedad: bloqueante, importante o menor;
- **d)** corrección propuesta.

Al final, un veredicto: si la v0.4.5 y el repositorio pueden distribuirse como documento de trabajo, y con qué cambios.
