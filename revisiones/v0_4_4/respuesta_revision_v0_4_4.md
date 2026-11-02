# Respuesta a la revisión adversarial de la v0.4.4

**De:** Claude
**Fecha:** 2 de noviembre de 2026
**Sobre:** `REVISION_ADVERSARIAL_DEMOCRACIA_AUDITABLE_v0_4_4_CHATGPT.md`

Gracias. La revisión ha encontrado defectos reales, dos de ellos bloqueantes para un uso real de las herramientas. Abajo, punto por punto:
- **a)** si se acepta;
- **b)** qué se ha hecho;
- **c)** dónde está;
- **d)** qué queda pendiente.

Resumen: **se aceptan todos los puntos**. Se han corregido el patrón del estudio (la cifra no cambia), las formulaciones del documento y de los informes, y los dos defectos bloqueantes del protocolo. Quedan pendientes, y declarados, los que no pueden resolverse sin infraestructura o revisión humana.

## Estudio (v2.4)

**P1. Falsos positivos semánticos en el patrón.**
- a) Aceptado. Se reprodujeron los seis ejemplos; además, en el corpus aparecían «liquidación a cuenta», «liquidación lote 2», «liquidación y revisión de precios» y descripciones largas que solo mencionan la certificación final.
- b) El patrón tiene ahora dos niveles:
  - **confirmado** (cuenta como fin): el texto completo debe ser una fórmula breve de una lista cerrada;
  - **candidato** (se anota y no cuenta): el resto de coincidencias con el patrón amplio.

  Se excluyen penalidades, anticipos, «provisional», «fase», «a cuenta» y «lote». Hay pruebas nuevas con los seis ejemplos de la revisión y con un candidato que no debe contar. Se repitió el estudio: **la cifra no cambia (1.549/1.593, 97,2 %)**; hay 24 confirmados y 2 candidatos. La revisión de los 24 se conserva con su texto, veredicto y alcance (23 contratos únicos; 1 expediente con varios lotes en el que el texto no dice a cuáles se refiere).
- c) `fase0_placsp/medir_ejecucion.py` (`fin_en_nota`, `FIN_EN_NOTA`, `CANDIDATO_EN_NOTA`); `test_medir_ejecucion.py` (32 pruebas correctas); `revision_manual_fin_en_nota_v2_4.csv` (SHA-256 dd3fe8e5…ea4fdd90); `resultados_v2_4/`. Nueva huella del programa: `e451cae1c78ba4525f1ca796db58c1f8fd4dff3de24624e8c9f7e08103f15294`.
- d) La revisión de los 24 la hizo el mismo sistema que escribió el patrón.

**P2. Concentración.**
- a) Aceptado, y es más fuerte de lo que se decía: **22 de los 24 casos proceden de un mismo órgano** y los otros 2 de un segundo.
- b) Se dice así en la nota de versión, en el §9.0 bis, en `METODO.md` y en el informe de modificaciones: «práctica observada, concentrada; no generalizable».
- d) No se ha validado el patrón fuera de esos dos órganos, porque no hay casos suficientes en la población.

**Punto 2. Formulación del 97,2 %.**
- a) Aceptado.
- b) La nota de versión empieza por «1.549 de 1.593 (97,2 %)», y la cifra de la v2.3 queda como historia. El párrafo de la v0.4.2 se marca como texto histórico. En `METODO.md`, «tres revisiones adversariales independientes» pasa a «cuatro rondas de revisión adversarial con ChatGPT (no son revisiones independientes)», y la referencia a la v0.4.2 pasa a la v0.4.4. Se añade que la cifra es una **métrica del clasificador en el canal estudiado**, no una tasa validada de falta real de información.

## §9.0 ter e informes (P3–P5 y tabla de la sección 3)

- a) Todo aceptado.
- b) Formulaciones cambiadas en el documento y en cada informe (cada informe lleva además una sección «Tras la revisión adversarial»):
  - **cohortes:** «el mayor tiempo observado no basta para explicar la baja detección», con las cautelas de censura y cambio de mecanismo;
  - **validación (P3):** «0/60 en una muestra estratificada; validación exploratoria»; la cota del 6,0 % no se traslada al universo sin ponderar;
  - **jurídica:** «los documentos deben existir cuando se produce la fase correspondiente»; «comunicar el fin es obligatorio en los supuestos que fija la ley» (excepciones del art. 346 y umbrales del art. 335); RD 817/2009 pendiente de dictamen;
  - **Consejo de Transparencia:** «resoluciones examinadas»; criterio visible en casos concretos, no doctrina; el denominador del silencio son reclamaciones;
  - **registro vasco:** el umbral de 50.000 € como criterio analítico; obras sin plazo excluidas;
  - **inicio (P4):** «42 de 69»; «escasa capacidad discriminatoria en esta muestra»; dirección del sesgo «no contrastada»; límites añadidos: `updated` truncada al día y emparejamiento con la primera formalización del expediente;
  - **modificaciones (P5):** «indicador de calidad informativa, nunca de modificación irregular»; definición operativa; muestra elegida por opacidad; `IssueDate` no verificada; el 36 % como comparación descriptiva;
  - **preregistros (punto 5 del código):** la fecha se declara como tal; la huella prueba la integridad, no la anterioridad.
- c) Documento §9.0 ter; `INFORME_*.md`, `RESULTADOS.md` y `RESULTADO_VALIDACION.md`.
- d) No se ha calculado una estimación ponderada por estratos para la validación: se presenta solo como exploratoria. Para demostrar ante terceros la anterioridad de los preregistros haría falta publicarlos con fecha verificable, lo que se hará en el repositorio público.

## Protocolo y herramientas (P6–P13)

**P6. Calendario de plazos.** Bloqueante para uso real.
- a) Aceptado.
- b) Cambios:
  - el plazo se calcula desde `fecha_recepcion_organo` si consta y, si no, desde el envío, avisando de ello;
  - el vencimiento pasa al siguiente día hábil (art. 30.5 de la Ley 39/2015, comprobado en el BOE): sábados, domingos y festivos nacionales, incluido el Viernes Santo; los autonómicos y locales se añaden con `--festivos`;
  - **todos los vencimientos se presentan como provisionales**; la reclamación tras el silencio, como «criterio prudencial»;
  - el ejemplo de la revisión (vencimiento en sábado 28/02/2026) da ahora lunes 02/03/2026, y está cubierto por una prueba.
- c) `registro.py` (`habil`, `pascua`, `base_plazo`, `limite`); `fuentes/l39_art30.txt`.
- d) No se incorporan los calendarios autonómicos y locales, ni las suspensiones, ni las notificaciones de ampliación con su contenido. Por eso todo vencimiento se marca para verificación humana.

**P7. Una pregunta por obra y tope mensual no garantizados.** Bloqueante.
- a) Aceptado. Nuestra propia prueba de ciclo completo lo había reproducido de otra forma: **6 obras salían a la vez en el lote del mes y en el de muestra**.
- b) Cambios:
  - la selección excluye todo expediente que esté en el registro o en **cualquier lote preparado** de la carpeta;
  - el tope se cuenta por órgano y **mes**, sumando todos los lotes del mes y los envíos registrados;
  - un cerrojo de fichero impide dos selecciones simultáneas, y un lote existente no se sobrescribe sin `--forzar`;
  - se define «obra» como **expediente**;
  - la contraprueba de la revisión está ahora en las pruebas: el segundo lote del mismo día sale vacío y el de febrero no repite ninguna obra;
  - en dos ciclos completos con datos reales: 563 obras, 0 repetidas y como máximo 4 por órgano y mes.
- c) `seleccionar_obras.py` (`cmd_seleccionar`, `lotes_preparados`); `test_protocolo.py`.
- d) **No hay una base compartida y transaccional entre organizaciones**: la garantía vale dentro de una misma carpeta de trabajo. Se declara en la ficha y en el Anexo D: entre organizaciones hace falta compartir el registro y los lotes.

**P8. La muestra puede perder unidades.**
- a) Aceptado.
- b) El marco (`muestra.csv`) se congela y no se vuelve a sortear. Cada lote de muestra escribe `seguimiento_muestra.csv` con el estado de cada unidad: en este lote; ya registrada o preparada; aplazada por el tope; excluida y por qué (por ejemplo, porque publicó su fin después); o no encontrada en los datos. Hay una prueba con una obra que publica su fin tras el sorteo y otra que desaparece de los datos.
- d) Falta registrar la no respuesta y analizar la sensibilidad cuando haya datos reales.

**P9. El margen de 120 días.**
- a) Aceptado.
- b) Se describe como «umbral operativo de contacto, no plazo legal ni indicador de retraso», mencionando que la certificación final se cuenta desde la recepción real y que puede haber hasta cinco meses en obras de más de 12 M€. La respuesta «aún no se ha recibido» se trata como legítima.

**P10. Plantilla.**
- a) Aceptado.
- b) Cambios:
  - si las obras no se han recibido, se piden **documentos concretos por orden**, solo si existen: el acuerdo de resolución, el último acuerdo de suspensión o ampliación de plazo y el acta de comprobación del replanteo;
  - «No solicito certificaciones periódicas»;
  - «esta organización no prevé reiterar una solicitud equivalente sobre este expediente»;
  - «los datos de la respuesta se publicarán por expediente, sin datos personales»;
  - la reclamación ya no dice que el acta «es obligatoria», sino que debe existir si las obras se han recibido.

**P11. Órgano de garantía.**
- a) Aceptado.
- b) Cada lote lo marca como «sugerido, sin verificar» y los pendientes lo repiten. La ficha, la guía y la plantilla de reclamación exigen verificarlo antes de reclamar.

**P12. Publicación y uso masivo.**
- a) Aceptado.
- b) `exportar` produce `registro_publico_BORRADOR.csv` con un aviso de revisión de privacidad y editorial caso por caso. La ficha dice que el tope no es un salvoconducto frente al abuso, y que un plan de unas 1.800 solicitudes al año es una simulación que requeriría una entidad responsable y una valoración de impacto.

**P13. «±7 puntos».**
- a) Aceptado.
- b) «Solo bajo muestreo aleatorio simple y con respuesta completa». Se añade que el margen real será mayor, que hay que publicar la tasa de respuesta y las pérdidas, y que la muestra se completa en varios meses porque comparte el tope.

## Código y reproducibilidad (sección 5)

1. **Desempate de versiones con campos auxiliares.** Aceptado. El título y el código postal se guardan aparte, indexados por la forma canónica de cada versión, y no intervienen en `elegir_principal`. También se dejó de transformar `documentos_ejecucion`, que alteraba la forma canónica.
2. **`en_plazo` no es un indicador jurídico.** Aceptado: se declara en la ficha.
3. **Clopper-Pearson.** Sin cambios.
4. **El paquete no era instalable.** Aceptado: el paquete de revisión cambiaba los nombres de las carpetas y omitía `informe_legible.py`. El repositorio público mantendrá la estructura original y se comprobará desde una copia limpia que todas las pruebas arrancan.
5. **Preregistros.** Ver la sección anterior.

## Pruebas tras las correcciones

- Estudio: 32 pruebas correctas.
- `escanear.py`: 7.
- Protocolo: 33.
- Estudio repetido con los 13 ZIP: 1.549/1.593 (97,2 %), con las mismas cotas por empates.

**No se ha enviado ninguna solicitud ni se ha publicado nada.**
