"""Protocolo de obras: ¿cuántas preguntas habría que hacer al año y cómo se repartirían entre órganos?
Lee el estado final de las obras del corpus 2021–oct. 2026 (investigacion_cohortes/obras_estado_final.csv,
generado por investigacion_doc_ccn/escanear.py con los 15 ZIP) y cuenta las obras que, sin indicador de fin
definitivo, alcanzan su fecha de pregunta (fin teórico + MARGEN_DIAS) en cada año. No nombra órganos:
solo distribuciones.
Uso: python -I -X utf8 volumen.py [--obras ruta.csv] [--margen 120]"""
import argparse
import csv
import os
from collections import Counter, defaultdict
from datetime import date, timedelta

AQUI = os.path.dirname(os.path.abspath(__file__))
OBRAS = os.path.join(AQUI, "..", "investigacion_cohortes", "obras_estado_final.csv")
CORTE = date(2026, 10, 29)   # fecha de los datos más recientes del corpus

# A quién se reclama (art. 24 y DA 4.ª LTAIBG), según ContractingPartyTypeCode (ContractingAuthorityCode-2.10).
AMBITO = {"1": "estatal", "6": "estatal", "9": "estatal",
          "2": "autonómico o local", "3": "autonómico o local", "7": "autonómico o local",
          "8": "autonómico o local", "10": "autonómico o local", "11": "autonómico o local"}
TRAMOS = [("menos de 1 M€", 0, 1e6), ("1–10 M€", 1e6, 1e7 + 0.01), ("más de 10 M€", 1e7 + 0.01, float("inf"))]


def num(s):
    try:
        return float(s)
    except (TypeError, ValueError):
        return None


def fin_definitivo(r):
    return r["anuncio_finalizacion"] == "True" or r["doc_resolucion"] == "True" or r["doc_fin_ordinario"] == "True"


def pct(a, b): return f"{100 * a / b:.1f} %" if b else "—"


def cuantil(xs, q):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(q * len(xs)))] if xs else 0


def describir(nombre, sel):
    por_organo = Counter(r["organo_id"] or "(sin id)" for r in sel)
    n = len(sel)
    cuentas = sorted(por_organo.values(), reverse=True)
    top10 = sum(cuentas[:10])
    print(f"  {nombre}: {n} preguntas; {len(por_organo)} órganos; por órgano: mediana {cuantil(cuentas, 0.5)}, "
          f"p90 {cuantil(cuentas, 0.9)}, máximo {cuentas[0] if cuentas else 0} ({pct(cuentas[0] if cuentas else 0, n)} del total); "
          f"los 10 con más reúnen {pct(top10, n)}; órganos con más de 12 al año: {sum(c > 12 for c in cuentas)}, "
          f"con más de 52: {sum(c > 52 for c in cuentas)}")
    return cuentas


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--obras", default=OBRAS)
    ap.add_argument("--margen", type=int, default=120)
    a = ap.parse_args()
    obras = [r for r in csv.DictReader(open(a.obras, encoding="utf-8"))
             if r["estado"] in ("ADJ", "RES") and int(r["n_resultados_adjudicados"] or 0) > 0 and r["fin_teorico"]]
    for r in obras:
        r["_pregunta"] = date.fromisoformat(r["fin_teorico"]) + timedelta(days=a.margen)
        r["_p"] = num(r["presupuesto_sin_iva"])
    print(f"Obras adjudicadas con fin teórico estimable: {len(obras)}; margen tras el fin teórico: {a.margen} días\n")

    for anio in (2024, 2025):
        cand = [r for r in obras if r["_pregunta"].year == anio and r["_pregunta"] <= CORTE]
        sin = [r for r in cand if not fin_definitivo(r)]
        print(f"== Fecha de pregunta en {anio}: {len(cand)} obras; sin indicador de fin definitivo {len(sin)} ({pct(len(sin), len(cand))})")
        for nombre, lo, hi in TRAMOS:
            describir(nombre, [r for r in sin if r["_p"] is not None and lo <= r["_p"] < hi])
        describir("1 M€ o más", [r for r in sin if r["_p"] is not None and r["_p"] >= 1e6])
        amb = Counter(AMBITO.get(r["tipo_administracion"], "otro o sin código") for r in sin if r["_p"] is not None and r["_p"] >= 1e6)
        print("  1 M€ o más por ámbito de reclamación: " + "; ".join(f"{k} {v}" for k, v in amb.most_common()))
        meses = Counter(r["_pregunta"].month for r in sin if r["_p"] is not None and 1e6 <= r["_p"] <= 1e7)
        print("  1–10 M€ por mes de pregunta: " + " ".join(f"{m}:{meses[m]}" for m in range(1, 13)) + "\n")

    # Efecto de un tope por órgano y mes (para el tramo 1–10 M€ de 2025).
    sel = [r for r in obras if r["_pregunta"].year == 2025 and not fin_definitivo(r) and r["_p"] is not None and 1e6 <= r["_p"] <= 1e7]
    print("== Tope de preguntas por órgano y mes (1–10 M€, 2025): preguntas aplazadas al mes siguiente o más")
    for tope in (1, 2, 4, 8):
        cola = defaultdict(int)   # órgano -> preguntas pendientes que pasan al mes siguiente
        for mes in range(1, 13):
            llegan = Counter(r["organo_id"] for r in sel if r["_pregunta"].month == mes)
            for org in set(llegan) | set(cola):
                cola[org] = max(0, llegan[org] + cola[org] - tope)
        pendientes = sum(cola.values())
        print(f"  tope {tope}/mes: quedan {pendientes} sin enviar a final de año ({pct(pendientes, len(sel))}); "
              f"órganos afectados: {sum(v > 0 for v in cola.values())}")


if __name__ == "__main__":
    main()
