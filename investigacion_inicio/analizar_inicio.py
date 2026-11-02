"""Análisis preregistrado (PREREGISTRO.md): niveles A/B/C, calibración con obras de final conocido e inicio real.
Lee estado_final.csv y versiones_obras.csv (escanear_versiones.py) y ../investigacion_doc_ccn/contratos_ccn.csv.
Uso: python -I -X utf8 analizar_inicio.py"""
import csv
import os
from collections import Counter, defaultdict
from datetime import date
from math import exp, lgamma, log

AQUI = os.path.dirname(os.path.abspath(__file__))
CORTE = "2026-10-29"
MARCAS = ["mod_estructurada", "anuncio_modificacion", "doc_durante", "doc_fin_parcial", "replanteo"]


def leer(nombre):
    with open(os.path.join(AQUI, nombre), encoding="utf-8") as f:
        return list(csv.DictReader(f))


def si(v): return v == "True"


def num(s):
    try:
        return float(s)
    except (TypeError, ValueError):
        return None


def binom_cdf(k, n, p):
    if p <= 0:
        return 1.0
    if p >= 1:
        return 1.0 if k >= n else 0.0
    return sum(exp(lgamma(n + 1) - lgamma(i + 1) - lgamma(n - i + 1) + i * log(p) + (n - i) * log(1 - p))
               for i in range(k + 1))


def clopper_pearson(k, n, alfa=0.05):
    def biseccion(f):
        lo, hi = 0.0, 1.0
        for _ in range(60):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if f(mid) else (lo, mid)
        return (lo + hi) / 2
    inf = 0.0 if k == 0 else biseccion(lambda p: 1 - binom_cdf(k - 1, n, p) < alfa / 2)
    sup = 1.0 if k == n else biseccion(lambda p: binom_cdf(k, n, p) > alfa / 2)
    return inf, sup


def pct(a, b): return f"{100 * a / b:.1f} %" if b else "—"


def cuartiles(xs):
    xs = sorted(xs)
    q = lambda f: xs[min(len(xs) - 1, int(f * len(xs)))]  # noqa: E731
    return q(0.25), q(0.5), q(0.75)


def main():
    final = leer("estado_final.csv")
    pob = [r for r in final if r["estado"] in ("ADJ", "RES") and int(r["n_resultados_adjudicados"] or 0) > 0
           and r["fin_teorico"] and r["fin_teorico"] < CORTE]
    print(f"Obras en estado final: {len(final)}; población (adjudicadas, fin teórico vencido): {len(pob)}\n")

    print("== 1. Niveles: A con fin; B sin fin con indicio de ejecución; C sin fin ni indicio")
    for nombre, cond in (("1–10 M€", lambda p: p is not None and 1e6 <= p <= 1e7),
                         ("1 M€ o más", lambda p: p is not None and p >= 1e6),
                         ("todas", lambda p: True)):
        sel = [r for r in pob if cond(num(r["presupuesto_sin_iva"]))]
        c = Counter(r["nivel"] for r in sel)
        sin_fin = c["B"] + c["C"]
        print(f"{nombre}: {len(sel)} obras; A {c['A']} ({pct(c['A'], len(sel))}); B {c['B']} ({pct(c['B'], len(sel))}); "
              f"C {c['C']} ({pct(c['C'], len(sel))}); entre las que no tienen fin: B {pct(c['B'], sin_fin)}, C {pct(c['C'], sin_fin)}")
        if nombre == "1–10 M€":
            print("  qué indicio tienen las B: " + "; ".join(
                f"{m} {sum(si(r[m]) for r in sel if r['nivel'] == 'B')}" for m in MARCAS))
            por_anio = defaultdict(Counter)
            for r in sel:
                por_anio[r["fin_teorico"][:4]][r["nivel"]] += 1
            print("  C entre las sin fin, por año de fin teórico: " + "; ".join(
                f"{a} {pct(v['C'], v['B'] + v['C'])} (n={v['B'] + v['C']})" for a, v in sorted(por_anio.items())))

    print("\n== 2. Calibración: obras con DOC_CCN vigente; versión observada = última anterior al primer DOC_CCN")
    versiones = defaultdict(list)
    for v in leer("versiones_obras.csv"):
        versiones[v["id"]].append(v)
    ccn = [r for r in final if si(r["ccn"]) and r["fecha_anuncio_finalizacion"]]
    for nombre, cond in (("todas", lambda p: True), ("1 M€ o más", lambda p: p is not None and p >= 1e6)):
        sel = [r for r in ccn if cond(num(r["presupuesto_sin_iva"]))]
        observadas, sin_previa = [], 0
        for r in sel:
            previas = [v for v in versiones[r["id"]] if v["updated"][:10] < r["fecha_anuncio_finalizacion"]]
            if not previas:
                sin_previa += 1
                continue
            observadas.append(max(previas, key=lambda v: v["updated"]))
        n = len(observadas)
        k = sum(not si(v["indicio"]) for v in observadas)
        inf, sup = clopper_pearson(k, n) if n else (0, 0)
        print(f"{nombre}: {len(sel)} obras con DOC_CCN; sin versión anterior en el corpus {sin_previa}; observadas {n}")
        print(f"  SIN indicio antes del anuncio (quedarían en C): {k} = {pct(k, n)} (IC95 {100 * inf:.1f}–{100 * sup:.1f} %)")
        print("  indicios presentes: " + "; ".join(f"{m} {sum(si(v[m]) for v in observadas)}" for m in MARCAS))
        print(f"  ya con algún fin por documento antes del anuncio: {sum(si(v['fin']) for v in observadas)}")
        if n:
            print(f"  con indicio en su ESTADO FINAL (referencia, incluye lo subido al cerrar): "
                  f"{pct(sum(si(r['indicio']) for r in sel), len(sel))}")

    print("\n== 3. Inicio real (XML ContractCompletionNotice) frente a la formalización del expediente")
    formal = {r["id"]: r["formalizacion"] for r in final}
    vistos, difs, sin_dato = set(), [], 0
    with open(os.path.join(AQUI, "..", "investigacion_doc_ccn", "contratos_ccn.csv"), encoding="utf-8") as f:
        for c in csv.DictReader(f):
            clave = (c["id"], c["contrato_id"], c["inicio_real"], c["fin_real"])
            if clave in vistos:
                continue
            vistos.add(clave)
            fz = formal.get(c["id"], "")
            if not c["inicio_real"] or not fz:
                sin_dato += 1
                continue
            difs.append((date.fromisoformat(c["inicio_real"]) - date.fromisoformat(fz)).days)
    if difs:
        q1, med, q3 = cuartiles(difs)
        print(f"contratos con inicio real y formalización: {len(difs)} (sin alguno de los dos: {sin_dato})")
        print(f"  días de la formalización al inicio real: mediana {med}, cuartiles {q1} a {q3}")
        print(f"  más de 31 días: {sum(d > 31 for d in difs)} ({pct(sum(d > 31 for d in difs), len(difs))}); "
              f"más de 90: {pct(sum(d > 90 for d in difs), len(difs))}; más de 180: {pct(sum(d > 180 for d in difs), len(difs))}; "
              f"negativos (inicio antes de la formalización): {pct(sum(d < 0 for d in difs), len(difs))}")


if __name__ == "__main__":
    main()
