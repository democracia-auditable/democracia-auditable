"""Consulta privada (NO forma parte del estudio): regla E4t v2, CONGELADA el 01/11/2026 antes de
ver el conjunto de prueba (obras de 50.000 € a < 200.000 €, 1.ª adjudicación 2019–2023).

v1 (e4t_prueba_2024.py) más dos correcciones, motivadas por los errores vistos en 0,2–1 M€:
  C1 oficios: se descarta el par si alguno de los títulos describe una parte dentro de otra obra
     («en/para la(s) obra(s) de ...»).
  C2 obras hermanas: (a) si los dos títulos tienen números (sin contar años 1990–2039) y no comparten
     ninguno, se descarta; (b) palabras raras = las que aparecen en <= 100 títulos de todo el corpus de
     obras; si el título A tiene alguna, su Jaccard con las raras de B debe ser >= 0,5.
Todo lo demás, igual que v1. No se modifica tras ver el conjunto de prueba.
Uso: python e4t_v2.py PRESUPUESTO_MIN PRESUPUESTO_MAX [AÑO_DESDE AÑO_HASTA]
"""
import json
import os
import re
import sys
from collections import Counter

sys.dont_write_bytecode = True
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(1, os.path.join(AQUI, "..", "fase0_placsp"))   # copia publicada: ruta local sustituida
import medir_ejecucion as m  # noqa: E402
from senales_medir import norm, palabras, FASE, TERMIN, FIN_NOTA  # noqa: E402

AM = re.compile(r"acuerdos?\s+marco")
PARTE = re.compile(r"\b(en|para)\s+(la|las)\s+obras?\s+de\b")
NUM = re.compile(r"\b\d+\b")
RARA_DF = 100


def numeros(t):
    return {x for x in NUM.findall(t) if not (len(x) == 4 and 1990 <= int(x) <= 2039)}


def main():
    pmin, pmax = float(sys.argv[1]), float(sys.argv[2])
    a0, a1 = (sys.argv[3], sys.argv[4]) if len(sys.argv) > 4 else ("2019", "2023")
    obras = [json.loads(l) for l in open(os.path.join(AQUI, "obras.jsonl"), encoding="utf-8")]
    corte = m.fecha_dia(obras[0]["corte"])
    org = lambda c: c["organo_id"] or c["organo"]
    df = Counter(w for c in obras for w in palabras(c["titulo"]))
    raras = lambda p: {w for w in p if df[w] <= RARA_DF}
    por_org = {}
    for c in obras:
        if c["primer_anuncio"]:
            por_org.setdefault(org(c), []).append((c["id"], c["primer_anuncio"], palabras(c["titulo"]), norm(c["titulo"])))
    base, marcadas = [], []
    for c in obras:
        p, fin = c["presupuesto_sin_iva"], m.fecha_dia(c["fin_teorico"])
        if not (c["estado"] in m.ESTADOS_ADMITIDOS and c["formalizado"] and a0 <= c["fecha_adjudicacion"][:4] <= a1
                and p is not None and pmin <= p < pmax and fin and fin < corte):
            continue
        if c["anuncio_finalizacion"] or (m.DOCS_FIN_DEFINITIVO & set(c["cats"])) or any(FIN_NOTA.search(norm(x["nota"])) for x in c["mods"]):
            continue
        base.append(c)
        ta = norm(c["titulo"])
        if AM.search(ta) or PARTE.search(ta):
            continue
        pa, fa, na, ra = palabras(c["titulo"]), set(FASE.findall(ta)), numeros(ta), None
        ra = raras(pa)
        desde = c["fecha_inicio"] or c["fecha_adjudicacion"]
        for ident, f, pb, tb in por_org.get(org(c), []):
            if ident == c["id"] or f <= desde or not pa or not pb or AM.search(tb) or PARTE.search(tb) or not TERMIN.search(tb):
                continue
            if len(pa & pb) / len(pa | pb) < 0.6:
                continue
            fb = set(FASE.findall(tb))
            if fa != fb and (fa or fb):
                continue
            nb = numeros(tb)
            if na and nb and not (na & nb):
                continue
            rb = raras(pb)
            if ra and len(ra & rb) / len(ra | rb) < 0.5:
                continue
            marcadas.append((c, tb, f))
            break
    print(f"v2 presupuesto [{pmin:.0f}, {pmax:.0f}) años {a0}-{a1}: base sin fin {len(base)}; marcadas {len(marcadas)} "
          f"({100 * len(marcadas) / max(len(base), 1):.2f} %); órganos {len({c['organo'] for c, _, _ in marcadas})}; "
          f"máx. de un órgano {max(Counter(c['organo'] for c, _, _ in marcadas).values(), default=0)}")
    for c, tb, f in marcadas:
        print(f"- [{c['fecha_inicio']} -> {f}] {c['titulo'][:120]}\n   => {tb[:120]}\n   {c['enlace']}")


if __name__ == "__main__":
    main()
