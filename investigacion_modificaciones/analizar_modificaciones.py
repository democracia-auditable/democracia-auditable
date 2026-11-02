"""Análisis preregistrado de las modificaciones (PREREGISTRO.md). Lee modificaciones.csv y obras_modificadas.csv.
Escribe muestra_revision.csv (30 obras con alguna modificación opaca; semilla 20261102) para la revisión manual.
Uso: python -I -X utf8 analizar_modificaciones.py"""
import csv
import os
import random
import sys
from collections import Counter

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "investigacion_inicio"))
from analizar_inicio import clopper_pearson  # noqa: E402


def leer(n):
    with open(os.path.join(AQUI, n), encoding="utf-8") as f:
        return list(csv.DictReader(f))


def si(v): return v == "True"


def num(s):
    try:
        return float(s)
    except (TypeError, ValueError):
        return None


def pct(a, b): return f"{100 * a / b:.1f} %" if b else "—"


def ic(k, n):
    i, s = clopper_pearson(k, n)
    return f"IC95 {100 * i:.1f}–{100 * s:.1f} %"


def adjudicada(r): return r["estado"] in ("ADJ", "RES") and int(r["n_resultados_adjudicados"] or 0) > 0


def informe(nombre, mods, obras):
    n, no = len(mods), len(obras)
    print(f"\n### {nombre}: {n} modificaciones en {no} obras")
    c = lambda k: sum(si(m[k]) for m in mods)  # noqa: E731
    print(f"1. Texto: con nota {pct(sum(int(m['longitud_nota']) > 0 for m in mods), n)}; "
          f"sin justificación textual (<40 caracteres o sin nota) {c('sin_justificacion')} ({pct(c('sin_justificacion'), n)})")
    longs = sorted(int(m["longitud_nota"]) for m in mods)
    print(f"   longitud de la nota: mediana {longs[n // 2]}, p25 {longs[n // 4]}, p75 {longs[3 * n // 4]}")
    print(f"2. Con importe distinto de 0: {pct(c('con_importe'), n)}; con plazo: {pct(c('con_plazo'), n)}")
    print(f"3. Sin contenido estructurado (ni importe ni plazo): {c('sin_estructura')} ({pct(c('sin_estructura'), n)})")
    k = c("opaca")
    print(f"4. OPACAS (sin estructura y sin justificación textual): {k} ({pct(k, n)}; {ic(k, n)})")
    ko = sum(int(o["n_opacas"]) > 0 for o in obras)
    print(f"   obras con al menos una opaca: {ko} ({pct(ko, no)}; {ic(ko, no)})")
    print(f"5. Texto con plazo y sin campo de plazo: {c('texto_plazo_sin_campo')} ({pct(c('texto_plazo_sin_campo'), n)}); "
          f"texto con dinero y sin importe: {c('texto_dinero_sin_importe')} ({pct(c('texto_dinero_sin_importe'), n)})")
    con_texto = [m for m in mods if not si(m["sin_justificacion"])]
    print(f"   entre las que tienen texto ({len(con_texto)}): plazo sin campo {pct(sum(si(m['texto_plazo_sin_campo']) for m in con_texto), len(con_texto))}, "
          f"dinero sin importe {pct(sum(si(m['texto_dinero_sin_importe']) for m in con_texto), len(con_texto))}")
    kd = sum(si(o["doc_modificacion"]) for o in obras)
    print(f"6. Obras modificadas con algún documento de modificación (por nombre): {kd} ({pct(kd, no)}; {ic(kd, no)}); "
          f"entre las que tienen alguna opaca: {pct(sum(si(o['doc_modificacion']) for o in obras if int(o['n_opacas'])), ko)}")
    sin_anuncio = sum(int(o["n_doc_mod"]) == 0 for o in obras)
    print(f"7. Obras modificadas sin anuncio DOC_MOD: {sin_anuncio} ({pct(sin_anuncio, no)}); "
          f"anuncios por obra frente a modificaciones: menos anuncios {pct(sum(int(o['n_doc_mod']) < int(o['n_modificaciones']) for o in obras), no)}, "
          f"igual {pct(sum(int(o['n_doc_mod']) == int(o['n_modificaciones']) for o in obras), no)}, "
          f"más {pct(sum(int(o['n_doc_mod']) > int(o['n_modificaciones']) for o in obras), no)}")
    anios = Counter(o["primer_doc_mod"][:4] for o in obras if o["primer_doc_mod"])
    por_anio = {}
    for o in obras:
        a = o["primer_doc_mod"][:4]
        if a:
            por_anio.setdefault(a, [0, 0])
            por_anio[a][0] += int(o["n_modificaciones"])
            por_anio[a][1] += int(o["n_opacas"])
    print("   opacas por año del primer anuncio: " + "; ".join(
        f"{a} {pct(v[1], v[0])} (n={v[0]})" for a, v in sorted(por_anio.items()) if anios[a] >= 20))
    org = Counter(m["organo_id"] for m in mods if si(m["opaca"]))
    top = sum(v for _, v in org.most_common(10))
    print(f"   concentración: {len(org)} órganos con alguna opaca; los 10 con más reúnen {pct(top, k)}; "
          f"el primero {pct(org.most_common(1)[0][1] if org else 0, k)}")


def main():
    mods = [m for m in leer("modificaciones.csv") if adjudicada(m)]
    obras = [o for o in leer("obras_modificadas.csv") if adjudicada(o)]
    informe("Obras adjudicadas, cualquier importe", mods, obras)
    grandes = lambda r: (num(r["presupuesto_sin_iva"]) or 0) >= 1e6  # noqa: E731
    informe("1 M€ o más", [m for m in mods if grandes(m)], [o for o in obras if grandes(o)])

    con_opaca = sorted(o["id"] for o in obras if int(o["n_opacas"]) > 0 and grandes(o))
    muestra = set(random.Random(20261102).sample(con_opaca, min(30, len(con_opaca))))
    filas = [o for o in obras if o["id"] in muestra]
    with open(os.path.join(AQUI, "muestra_revision.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["id", "enlace", "n_modificaciones", "n_opacas", "doc_modificacion"], extrasaction="ignore")
        w.writeheader()
        w.writerows(filas)
    print(f"\nMuestra para revisión manual: {len(filas)} obras de 1 M€ o más con alguna opaca -> muestra_revision.csv")


if __name__ == "__main__":
    main()
