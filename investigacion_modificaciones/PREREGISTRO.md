# Preregistro: ¿cuánta información trae cada modificación publicada?

**Escrito el 1 de noviembre de 2026, antes de medir.** Las definiciones no se cambiarán a la vista de los resultados. Las correcciones posteriores se anotarán al final con su motivo.

## Marco legal (`fuentes/`)

- **LCSP art. 207.3:** toda modificación debe publicarse en el perfil de contratante en un plazo de 5 días desde su aprobación, «acompañada de las alegaciones del contratista y de todos los informes» previos.
- **Art. 203.3:** las modificaciones deben publicarse conforme a los arts. 207 y 63.
- **Art. 203.1:** separa de la potestad de modificación, entre otros supuestos, la **ampliación del plazo de ejecución**, que tiene su propio régimen. Una modificación publicada que solo amplía el plazo **puede no ser una modificación** en sentido legal; no se le aplicará la lectura del art. 207.3 sin más.
- **Guía técnica de la PLACSP (v3.10, apdo. 5.11):** dice que el órgano «puede publicar» el anuncio de modificación. Es una guía de uso de la plataforma, no una norma.
- **Especificación de la sindicación (v1.3, 05/08/2020, apdo. 4.38):** no recoge el campo `cbc:Note` dentro de `ContractModification`, aunque aparece en los datos actuales.

## Unidad y población

- **Unidad:** cada `ContractModification` del **estado final** de cada obra (política de versiones del estudio).
- **Población:** obras (tipo 3) en estado ADJ o RES con al menos un resultado adjudicado. Se informa también del tramo de 1 M€ o más.

## Medidas

1. **Texto:** si `Note` existe y no está vacío; su longitud. Se considera **sin justificación textual** si, una vez normalizado, tiene menos de 40 caracteres o falta.
2. **Contenido estructurado:**
   - **importe** presente y distinto de 0 (`ContractModificationLegalMonetaryTotal/TaxExclusiveAmount`);
   - **plazo** presente: `ContractModificationDurationMeasure` o `FinalDurationMeasure`.
3. **Sin contenido estructurado:** sin importe distinto de 0 y sin plazo.
4. **Opaca:** sin contenido estructurado **y** sin justificación textual.
5. **Incoherencia texto–campos**, con texto normalizado:
   - el texto menciona un plazo (`ampliaci\w*\s+(de|del)\s+plazo|prorroga|plazo de ejecucion|nuevo plazo`) y no hay campo de plazo;
   - el texto menciona dinero (`euros|€|\d+[.,]\d{2}\s*(eur|€)|incremento|presupuesto`) y el importe es 0 o falta.
6. **Documentación en el expediente:** la obra tiene al menos un documento de la categoría `documento_modificacion` del clasificador del estudio (por nombre). Es una aproximación a los informes y alegaciones del art. 207.3: **no permite** atribuir un documento a una modificación concreta ni conocer su contenido.
7. **Anuncio:** la obra tiene un anuncio `DOC_MOD`. Se dan el número de anuncios frente al número de modificaciones y la distribución por año de publicación del primer anuncio.

**No medible:** el plazo de 5 días, porque la fecha de aprobación no está en la sindicación.

**Agregación:** proporciones por modificación y por obra, con intervalo exacto de Clopper-Pearson al 95 % en las medidas principales (4 y 6). Concentración: proporción de las modificaciones opacas que reúnen los 10 órganos con más opacas (sin nombrarlos).

## Revisión manual

- **Muestra:** 30 obras con alguna modificación opaca (semilla 20261102), revisadas en la página web de la PLACSP.
- **Qué se anota:** si el anuncio de modificación de la web muestra motivo, importe o plazo, y si hay documentos adjuntos (informes, alegaciones, resolución de aprobación).
- **Para qué:** estimar cuánto de lo «opaco» en la sindicación sí está en la web.

## Lo que no se afirmará

- Una modificación opaca en los datos **no prueba un incumplimiento** del art. 207.3: la información puede estar en documentos adjuntos o en la web, o la «modificación» puede ser una ampliación de plazo con otro régimen.
- No se nombrarán órganos ni obras.
