"""Coincidencia «terminación licitada de nuevo»: indicio documental que obliga a verificar el final de una obra.

QUÉ HACE
  Marca una obra A cuando el MISMO órgano de contratación licita, después de que A empezara, otra obra B cuyo
  título casi repite el de A y habla de terminarla («terminación», «finalización», «conclusión», «resto de
  obras», «obras pendientes», «completar las obras»). Es compatible con que el primer contrato no terminara la
  obra (resolución, abandono…), pero también con recepciones parciales, alcances complementarios u otras fases:
  no prueba nada por sí sola.

  Es la regla E4t v2, congelada el 01/11/2026 (SHA-256 del original 6ea9d8cf36ea727a348918a995c25eaaed1e74a7ee2e849a1e0ef381ff1152e5,
  en investigacion_terminacion/regla_e4t_v2.py). Este módulo reproduce su lógica sin cambios, separada en
  funciones; investigacion_terminacion/test_equivalencia.py y test_protocolo.py comprueban que da el mismo resultado.

CONDICIONES (todas):
  1. B es del mismo órgano (identificador, o nombre si no hay identificador).
  2. El primer anuncio de B es posterior al inicio de A (o a su adjudicación, si no hay inicio).
  3. Ni A ni B son acuerdos marco ni describen una parte dentro de otra obra («en/para la(s) obra(s) de»).
  4. El título de B contiene vocabulario de terminación (TERMIN).
  5. Parecido de títulos: índice de Jaccard de «palabras significativas» >= UMBRAL_JACCARD (0,6). Palabras
     significativas: de 4 o más letras o cifras, sin tildes, excluidas las de VACIAS.
  6. Misma fase, lote, etapa o tramo (o ninguno en ambos).
  7. Si los dos títulos tienen números (sin contar años 1990–2039), comparten al menos uno.
  8. Si A tiene «palabras raras» (las que aparecen en <= RARA_DF títulos de todo el corpus de obras), el Jaccard
     de sus palabras raras con las de B es >= UMBRAL_RARAS (0,5).

QUÉ SE SABE DE ELLA (investigacion_terminacion/INFORME_TERMINACION.md; comparación preregistrada)
  - Marcó 10 de 273 expedientes con indicios documentales de resolución (3,7 %) frente a 2 de 558 con indicios de
    terminación ordinaria (0,4 %); cociente 10,2 (IC95 2,3–46,3). Corpus parcialmente expuesto al diseño: no es una
    validación independiente, y esas cifras no son trasladables a obras sin final publicado.
  - Una marca obliga a verificar; su ausencia no informa sobre el estado de la obra (sensibilidad muy baja).
  - Avisa con retraso (la nueva licitación llega 1–3 años después) y depende del vocabulario de los títulos.
  - Una obra marcada es una coincidencia documental que requiere comprobación, no un fracaso ni una resolución probados.
  - La lista de obras marcadas no debe publicarse: permitiría señalar a órganos por un indicio sin comprobar.

PARA REFINARLA: ver protocolo_obras/SENAL_TERMINACION.md (parámetros, fallos conocidos y cómo validar cambios).
"""
import re
import unicodedata
from collections import Counter

UMBRAL_JACCARD = 0.6
UMBRAL_RARAS = 0.5
RARA_DF = 100

TERMIN = re.compile(r"terminaci|finalizaci|conclusi|resto\s+de\s+(las\s+)?obras|obras\s+pendientes|completar\s+las\s+obras")
FASE = re.compile(r"\b(fase|lote|etapa|tramo)\s+([0-9ivx]+)\b")
AM = re.compile(r"acuerdos?\s+marco")
PARTE = re.compile(r"\b(en|para)\s+(la|las)\s+obras?\s+de\b")
NUM = re.compile(r"\b\d+\b")
VACIAS = set("""obras obra proyecto ejecucion construccion contrato contratacion para del las los una con por
 sus que como sobre desde hasta entre calle calles avenida plaza municipal termino municipio ayuntamiento
 mejora mejoras reforma adecuacion""".split())


def norm(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"[_\-]+", " ", s)


def palabras(t):
    return {w for w in re.findall(r"[a-z0-9]{4,}", norm(t)) if w not in VACIAS}


def numeros(t):
    return {x for x in NUM.findall(t) if not (len(x) == 4 and 1990 <= int(x) <= 2039)}


def jaccard(a, b):
    return len(a & b) / len(a | b) if a | b else 0.0


class Indice:
    """Índices sobre TODAS las obras del corpus: frecuencia de palabras y licitaciones por órgano.

    Cada obra es un dict con: id, titulo, organo_id, organo, primer_anuncio (AAAA-MM-DD), fecha_inicio,
    fecha_adjudicacion."""

    def __init__(self, obras):
        self.df = Counter(w for c in obras for w in palabras(c["titulo"]))
        self.por_org = {}
        for c in obras:
            if c.get("primer_anuncio"):
                self.por_org.setdefault(self.organo(c), []).append(
                    (c["id"], c["primer_anuncio"], palabras(c["titulo"]), norm(c["titulo"])))

    @staticmethod
    def organo(c):
        return c.get("organo_id") or c.get("organo") or ""

    def raras(self, p):
        return {w for w in p if self.df[w] <= RARA_DF}

    def terminacion(self, c):
        """Título normalizado de la licitación B que marca la obra A = c, o None si no la hay."""
        ta = norm(c["titulo"])
        if AM.search(ta) or PARTE.search(ta):
            return None
        pa, fa, na = palabras(c["titulo"]), set(FASE.findall(ta)), numeros(ta)
        ra = self.raras(pa)
        desde = c.get("fecha_inicio") or c.get("fecha_adjudicacion") or ""
        for ident, f, pb, tb in self.por_org.get(self.organo(c), []):
            if ident == c["id"] or f <= desde or not pa or not pb or AM.search(tb) or PARTE.search(tb) or not TERMIN.search(tb):
                continue
            if jaccard(pa, pb) < UMBRAL_JACCARD:
                continue
            fb = set(FASE.findall(tb))
            if fa != fb and (fa or fb):
                continue
            nb = numeros(tb)
            if na and nb and not (na & nb):
                continue
            rb = self.raras(pb)
            if ra and jaccard(ra, rb) < UMBRAL_RARAS:
                continue
            return tb
        return None
