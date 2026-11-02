"""Análisis tras la revisión adversarial de ChatGPT. Lee obras_estado_final.csv y contratos_ccn.csv.
Uso: python -X utf8 -I analizar_v2.py"""
import csv
import os
import re
import statistics as st
from collections import Counter, defaultdict

AQUI = os.path.dirname(os.path.abspath(__file__))
CORTE = "2026-10-29"
obras = [r for r in csv.DictReader(open(os.path.join(AQUI, "obras_estado_final.csv"), encoding="utf-8"))
         if r["estado"] in ("ADJ", "RES") and int(r["n_resultados_adjudicados"] or 0) > 0]
crudos = list(csv.DictReader(open(os.path.join(AQUI, "contratos_ccn.csv"), encoding="utf-8")))


def f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def mediana(v):
    return f"{st.median(v):.0f}" if v else "—"


def cuartiles(v):
    if len(v) < 4:
        return "—"
    q = st.quantiles(v, n=4)
    return f"{q[0]:.0f} – {q[2]:.0f}"


# --- Unidad de contrato: (expediente, contrato, lote); repeticiones exactas -> el anuncio más reciente
grupos = defaultdict(list)
for r in crudos:
    grupos[(r["id"], r["contrato_id"], r["lote"], r["fin_real"], r["causa_codigo"])].append(r)
contratos = [max(g, key=lambda r: r["fecha_anuncio"]) for g in grupos.values()]
k = Counter((r["id"], r["contrato_id"], r["lote"]) for r in contratos)
print(f"Filas leídas: {len(crudos)}; tras quitar repeticiones exactas: {len(contratos)}; "
      f"(expediente, contrato, lote) que siguen repetidos con datos distintos: {sum(v > 1 for v in k.values())}")
principal = Counter(r["organo_id"] for r in contratos).most_common(1)[0][0]

print("\n== 1. Proporción con DOC_CCN entre obras observables, por año del fin teórico")
print("año | universo observable | con DOC_CCN | % | sin coincidencia | cohorte adjudicada desde 2023: n, con DOC_CCN, %, sin coincidencia")
def sin_coinc(r):
    return r["anuncio_finalizacion"] != "True" and r["doc_resolucion"] != "True" and r["doc_fin_ordinario"] != "True"
for anio in ("2023", "2024", "2025", "2026"):
    u = [r for r in obras if r["fin_teorico"][:4] == anio and r["fin_teorico"] < CORTE]
    c = [r for r in u if r["fecha_adjudicacion"] >= "2023"]
    pct = lambda a, b: f"{100 * a / b:.2f} %" if b else "—"
    print(f"{anio} | {len(u)} | {sum(r['anuncio_finalizacion'] == 'True' for r in u)} | "
          f"{pct(sum(r['anuncio_finalizacion'] == 'True' for r in u), len(u))} | {pct(sum(map(sin_coinc, u)), len(u))} | "
          f"{len(c)}, {sum(r['anuncio_finalizacion'] == 'True' for r in c)}, "
          f"{pct(sum(r['anuncio_finalizacion'] == 'True' for r in c), len(c))}, {pct(sum(map(sin_coinc, c)), len(c))}")
adj = Counter(r["fecha_adjudicacion"][:4] for r in obras if r["fin_teorico"][:4] in ("2023", "2024", "2025"))
print("año de adjudicación de las obras con fin teórico 2023–2025:", sorted(adj.items())[-8:])

print("\n== 2. Causa de extinción y anexos (unidad: contrato)")
def anexo(r, patron):
    return bool(re.search(patron, r["anexos"], re.I))
PAT_ORD = r"recep|liquid|certific|final de obra|\bcfo\b|conformidad|acta"
PAT_RES = r"resol|desist|rescis|extinc"
for nombre, sub in (("con código de causa", [r for r in contratos if r["causa_codigo"]]),
                    ("ContractTermination sin código", [r for r in contratos if not r["causa_codigo"] and r["terminacion_presente"] == "True"]),
                    ("sin ContractTermination", [r for r in contratos if r["terminacion_presente"] != "True"])):
    con_anexo = [r for r in sub if r["anexos"]]
    print(f"{nombre}: {len(sub)}; con anexo {len(con_anexo)}; anexo de recepción/liquidación/certificación {sum(anexo(r, PAT_ORD) for r in con_anexo)}; "
          f"anexo de resolución {sum(anexo(r, PAT_RES) for r in con_anexo)}")

print("\n== 3. Duración real frente a prevista (mismo XML; prevista = inicial o tras la última modificación del contrato)")
def dif(sub):
    return [int(r["dif_duracion_dias"]) for r in sub if r["dif_duracion_dias"] != ""]
for nombre, sub in (("todos", contratos),
                    ("sin código de causa", [r for r in contratos if not r["causa_codigo"]]),
                    ("con código de causa", [r for r in contratos if r["causa_codigo"]]),
                    ("adjudicados desde 2023", [r for r in contratos if r["fecha_adjudicacion"] >= "2023"]),
                    ("sin el órgano con más contratos", [r for r in contratos if r["organo_id"] != principal]),
                    ("sin modificaciones ni suspensiones", [r for r in contratos if r["n_modificaciones_contrato"] == "0" and r["n_suspensiones"] == "0"])):
    v = dif(sub)
    print(f"{nombre}: n={len(v)}; mediana {mediana(v)} d; cuartiles {cuartiles(v)}; "
          f">0: {100 * sum(x > 0 for x in v) / len(v):.0f} %; >180: {100 * sum(x > 180 for x in v) / len(v):.0f} %")
v = [int(r["dif_fin_teorico_expediente_dias"]) for r in contratos if r["dif_fin_teorico_expediente_dias"] != ""]
print(f"(métrica anterior, fin real del contrato − fin teórico del expediente: n={len(v)}, mediana {mediana(v)} d)")
sin_prev = sum(1 for r in contratos if r["duracion_prevista_final_dias"] == "")
print(f"contratos sin duración prevista en el XML: {sin_prev}; con prórrogas declaradas (NumberNumeric>0): "
      f"{sum(1 for r in contratos if (f(r['prorrogas_numero']) or 0) > 0)}")

print("\n== 4. Días del fin real al anuncio")
for nombre, sub in (("todos", contratos),
                    ("adjudicados desde 2023", [r for r in contratos if r["fecha_adjudicacion"] >= "2023"]),
                    ("sin el órgano con más contratos", [r for r in contratos if r["organo_id"] != principal]),
                    ("anuncios de 2026", [r for r in contratos if r["fecha_anuncio"] >= "2026"])):
    v = [int(r["dias_fin_a_anuncio"]) for r in sub if r["dias_fin_a_anuncio"] != ""]
    print(f"{nombre}: n={len(v)}; mediana {mediana(v)} d; cuartiles {cuartiles(v)}")

print("\n== 5. Importe pagado")
def casa(p, ref, tol=0.005):
    return p is not None and ref and abs(p / ref - 1) < tol
for nombre, sub in (("sin código de causa", [r for r in contratos if not r["causa_codigo"]]),
                    ("con código de causa", [r for r in contratos if r["causa_codigo"]])):
    cero = [r for r in sub if f(r["pagado"]) == 0]
    pos = [r for r in sub if (f(r["pagado"]) or 0) > 0]
    cuenta = Counter()
    for r in pos:
        p = f(r["pagado"])
        if casa(p, f(r["adjudicado_sin_iva"])): cuenta["= adjudicado sin IVA"] += 1
        elif casa(p, f(r["adjudicado_con_iva"])): cuenta["= adjudicado con IVA (PayableAmount)"] += 1
        elif casa(p, f(r["final_mod_sin_iva"])): cuenta["= final tras modificación sin IVA"] += 1
        elif casa(p, f(r["final_mod_con_iva"])): cuenta["= final tras modificación con IVA"] += 1
        else: cuenta["otro valor"] += 1
    desc = [r for r in sub if r["pagado_descripcion"]]
    print(f"{nombre}: {len(sub)}; pagado 0: {len(cero)} ({100 * len(cero) / len(sub):.1f} %); >0: {len(pos)} -> {dict(cuenta)}; "
          f"con descripción: {len(desc)}, que mencionan IVA: {sum(bool(re.search(r'iva', r['pagado_descripcion'], re.I)) for r in desc)}")
rat = [f(r["pagado"]) / f(r["adjudicado_con_iva"]) for r in contratos if not r["causa_codigo"] and (f(r["pagado"]) or 0) > 0 and f(r["adjudicado_con_iva"])]
print(f"sin código de causa, pagado/adjudicado con IVA: mediana {st.median(rat):.2f}, cuartiles {st.quantiles(rat, n=4)[0]:.2f} – {st.quantiles(rat, n=4)[2]:.2f}")

print("\n== 6. Concentración")
org = Counter(r["organo_id"] for r in contratos)
exp = Counter(r["organo_id"] for r in {r["id"]: r for r in contratos}.values())
print(f"contratos: {len(contratos)}; del órgano con más: {org[principal]}; expedientes: {sum(exp.values())}; del mismo órgano: {exp[principal]}")
t = [r for r in contratos if r["organo_id"] == principal]
print(f"ese órgano: sin código de causa {sum(not r['causa_codigo'] for r in t)} de {len(t)}; adjudicados antes de 2023: "
      f"{sum(r['fecha_adjudicacion'] < '2023' for r in t)}")
