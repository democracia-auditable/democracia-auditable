"""Muestra estratificada de obras SIN indicador de fin definitivo y con fin teórico vencido.
Estratos: año de adjudicación (2021–2024) × tramo de importe (<1, 1–10, >10 M€); 5 por estrato.
Semilla publicada: 20261101. Uso: python -X utf8 -I sortear.py"""
import csv, os, random
AQUI = os.path.dirname(os.path.abspath(__file__))
CORTE, SEMILLA, N = "2026-10-29", 20261101, 5
obras = [r for r in csv.DictReader(open(os.path.join(AQUI, "..", "obras_estado_final.csv"), encoding="utf-8"))
         if r["estado"] in ("ADJ", "RES") and int(r["n_resultados_adjudicados"] or 0) > 0
         and r["fin_teorico"] and r["fin_teorico"] < CORTE
         and r["anuncio_finalizacion"] != "True" and r["doc_resolucion"] != "True" and r["doc_fin_ordinario"] != "True"]
def tramo(r):
    try: p = float(r["presupuesto_sin_iva"])
    except ValueError: return None
    return "<1 M€" if p < 1e6 else ("1–10 M€" if p <= 1e7 else ">10 M€")
rng = random.Random(SEMILLA)
muestra = []
for anio in ("2021", "2022", "2023", "2024"):
    for t in ("<1 M€", "1–10 M€", ">10 M€"):
        pob = sorted((r for r in obras if r["fecha_adjudicacion"][:4] == anio and tramo(r) == t), key=lambda r: r["id"])
        for r in rng.sample(pob, min(N, len(pob))):
            muestra.append({"estrato": f"{anio} {t}", "poblacion_estrato": len(pob), "id": r["id"], "enlace": r["enlace"],
                            "fecha_adjudicacion": r["fecha_adjudicacion"], "presupuesto_sin_iva": r["presupuesto_sin_iva"],
                            "fin_teorico": r["fin_teorico"]})
        print(anio, t, "población", len(pob))
with open(os.path.join(AQUI, "muestra.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(muestra[0])); w.writeheader(); w.writerows(muestra)
print("muestra:", len(muestra))
