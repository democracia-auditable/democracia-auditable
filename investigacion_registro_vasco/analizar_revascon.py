"""Rama 3: ¿consta el fin de las obras en el Registro de Contratos del Sector Público de Euskadi (REVASCON)?
Fuentes (Open Data Euskadi, CC BY): histórico CSV por año del contrato 2011–2018 (instantánea de septiembre
de 2018) y fichero XLSX «del 2019» (inscripciones y actualizaciones de 2019). Se unen por «Código identificador
del contrato»: un contrato cuenta con fin registrado si algún registro tiene estado «Finalización» o datos en
«Finalización contrato» o «Resolución contrato». Fin teórico = fecha de formalización (o adjudicación) + plazo en meses.
No se extraen ni se escriben adjudicatarios.
Uso: uv run --with openpyxl python -I -X utf8 analizar_revascon.py"""
import csv
import glob
import io
import os
import re
from collections import defaultdict
from datetime import date

import openpyxl

AQUI = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(AQUI, "fuentes")
CORTE = date(2019, 12, 31)   # último dato disponible: fichero de 2019
CAMPOS = ["Estado contrato", "Tipo de contrato", "Año del contrato", "Código identificador del contrato",
          "Importe de licitación sin IVA", "Importe de adjudicación sin IVA", "Plazo de ejecución (meses)",
          "Fecha de adjudicación", "Fecha de formalización", "Finalización contrato", "Resolución contrato", "Contrato menor"]


def limpio(k): return " ".join(str(k or "").split())


def num(s):
    s = str(s or "").strip().replace(".", "").replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None


def fecha(s):
    m = re.match(r"(\d{2})/(\d{2})/(\d{4})", str(s or "").strip())
    if m:
        try:
            return date(int(m[3]), int(m[2]), int(m[1]))
        except ValueError:
            return None


def mas_meses(d, m):
    y, mo = divmod(d.month - 1 + int(round(m)), 12)
    return date(min(d.year + y, 9999), mo + 1, min(d.day, 28))


def normalizar(d, origen):
    d = {limpio(k): ("" if v is None else str(v).strip()) for k, v in d.items() if k}
    r = {c: d.get(c, "") for c in CAMPOS}
    r["origen"] = origen
    return r


def leer_csv(p):
    t = open(p, "rb").read().decode("cp1252")
    lineas = t.splitlines()
    i = next(k for k, l in enumerate(lineas[:20]) if "Estado contrato" in l)
    return [normalizar(d, os.path.basename(p)) for d in csv.DictReader(io.StringIO("\n".join(lineas[i:])), delimiter=";")]


def leer_xlsx(p):
    ws = openpyxl.load_workbook(p, read_only=True).worksheets[0]
    ws.reset_dimensions()
    filas, cab = [], None
    for r in ws.iter_rows(values_only=True):
        if cab is None:
            if r and "Estado contrato" in [limpio(c) for c in r]:
                cab = [limpio(c) for c in r]
            continue
        if any(r):
            filas.append(normalizar(dict(zip(cab, r)), os.path.basename(p)))
    return filas


def main():
    registros = []
    for p in sorted(glob.glob(os.path.join(F, "historico", "*.csv"))):
        registros += leer_csv(p)
    registros += leer_xlsx(os.path.join(F, "revascon_2019.xlsx"))
    por_codigo = defaultdict(list)
    for r in registros:
        if r["Código identificador del contrato"]:
            por_codigo[r["Código identificador del contrato"]].append(r)
    print(f"registros {len(registros)}; contratos distintos {len(por_codigo)}")

    contratos = []
    for cod, rs in por_codigo.items():
        r0 = next((r for r in rs if r["origen"].endswith(".csv")), rs[0])   # datos básicos: histórico si existe
        if r0["Tipo de contrato"] != "Obras":
            continue
        menor = any(r["Contrato menor"].lower().startswith("s") for r in rs)
        lic, adj = num(r0["Importe de licitación sin IVA"]), num(r0["Importe de adjudicación sin IVA"])
        base = fecha(r0["Fecha de formalización"]) or fecha(r0["Fecha de adjudicación"])
        plazo = num(r0["Plazo de ejecución (meses)"])
        fin_teorico = mas_meses(base, plazo) if base and plazo is not None and 0 < plazo < 600 else None
        fin = any(r["Estado contrato"] == "Finalización" or r["Finalización contrato"] for r in rs)
        resol = any(r["Resolución contrato"] for r in rs)
        contratos.append({"codigo": cod, "anio": r0["Año del contrato"][:4], "menor": menor, "licitacion": lic,
                          "adjudicacion": adj, "fin_teorico": fin_teorico, "fin_registrado": fin, "resolucion": resol,
                          "en_2019": any(r["origen"].endswith(".xlsx") for r in rs)})

    def tabla(titulo, cond):
        print(f"\n== {titulo}")
        print("año del contrato | obras | fin teórico vencido antes del 31/12/2019 | con fin o resolución registrados")
        for anio in [str(a) for a in range(2011, 2019)]:
            sel = [c for c in contratos if c["anio"] == anio and cond(c)]
            venc = [c for c in sel if c["fin_teorico"] and c["fin_teorico"] <= CORTE]
            con = [c for c in venc if c["fin_registrado"] or c["resolucion"]]
            if venc:
                print(f"{anio} | {len(sel)} | {len(venc)} | {len(con)} ({100 * len(con) / len(venc):.1f} %)")

    tabla("Obras no menores (adjudicación sin IVA ≥ 50.000 € y no marcadas como menores)",
          lambda c: not c["menor"] and (c["adjudicacion"] or 0) >= 50000)
    tabla("Obras de 1 a 10 M€ (licitación sin IVA)", lambda c: c["licitacion"] and 1e6 <= c["licitacion"] <= 1e7)
    tabla("Obras menores", lambda c: c["menor"])

    with open(os.path.join(AQUI, "obras_revascon.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(contratos[0].keys()))
        w.writeheader()
        w.writerows(contratos)


if __name__ == "__main__":
    main()
