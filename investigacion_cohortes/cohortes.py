"""Rama 2: ¿el porcentaje sin indicador de fin baja si se da más tiempo a las obras?
Cohortes por año de adjudicación (2021, 2022, 2023) con los criterios del estudio, sobre el estado
final de cada expediente en el corpus 2021–oct. 2026 (escanear.py con los 15 ZIP).
Uso: python -X utf8 -I cohortes.py"""
import csv
import os
from collections import Counter

AQUI = os.path.dirname(os.path.abspath(__file__))
CORTE = "2026-10-29"
obras = [r for r in csv.DictReader(open(os.path.join(AQUI, "obras_estado_final.csv"), encoding="utf-8"))
         if r["estado"] in ("ADJ", "RES") and int(r["n_resultados_adjudicados"] or 0) > 0]


def p(r):
    try:
        return float(r["presupuesto_sin_iva"])
    except ValueError:
        return None


def ccn(r): return r["anuncio_finalizacion"] == "True"
def fin_def(r): return ccn(r) or r["doc_resolucion"] == "True" or r["doc_fin_ordinario"] == "True"


def fila(nombre, sel):
    venc = [r for r in sel if r["fin_teorico"] and r["fin_teorico"] < CORTE]
    sin = [r for r in venc if not fin_def(r)]
    anios = Counter(r["fin_teorico"][:4] for r in venc)
    mediana_fin = sorted(r["fin_teorico"] for r in venc)[len(venc) // 2] if venc else "—"
    print(f"{nombre}: seleccionados {len(sel)}; fin teórico vencido {len(venc)} (mediana del fin teórico {mediana_fin}); "
          f"sin indicador de fin definitivo {len(sin)} = {100 * len(sin) / len(venc):.1f} %; con DOC_CCN {sum(map(ccn, venc))}; "
          f"con documento de resolución {sum(r['doc_resolucion'] == 'True' for r in venc)}; "
          f"con documento de fin ordinario {sum(r['doc_fin_ordinario'] == 'True' for r in venc)}")
    return venc


print("== Criterios del estudio: obras de 1 a 10 M€ (presupuesto base sin IVA)")
for anio in ("2021", "2022", "2023"):
    fila(f"adjudicadas en {anio}", [r for r in obras if r["fecha_adjudicacion"][:4] == anio and p(r) is not None and 1e6 <= p(r) <= 1e7])

print("\n== Todas las obras, cualquier importe")
for anio in ("2021", "2022", "2023"):
    fila(f"adjudicadas en {anio}", [r for r in obras if r["fecha_adjudicacion"][:4] == anio])

print("\n== Por antigüedad del fin teórico (todas las obras adjudicadas en 2021–2023)")
base = [r for r in obras if "2021" <= r["fecha_adjudicacion"][:4] <= "2023" and r["fin_teorico"] and r["fin_teorico"] < CORTE]
for anio in ("2021", "2022", "2023", "2024", "2025", "2026"):
    v = [r for r in base if r["fin_teorico"][:4] == anio]
    if v:
        print(f"fin teórico en {anio}: {len(v)} obras; sin indicador {100 * sum(not fin_def(r) for r in v) / len(v):.1f} %")
