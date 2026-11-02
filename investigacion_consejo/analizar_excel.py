"""Rama 5: resoluciones del Consejo de Transparencia y Buen Gobierno (ámbito estatal).
Lee fuentes/excel/ResolucionesAE.xlsx (una hoja por año de resolución, columnas distintas según el año),
armoniza las columnas y escribe resoluciones.csv. Después resume, sin nombrar organismos:
  1. reclamaciones por silencio y su desenlace, por año;
  2. resoluciones sobre contratos;
  3. resoluciones sobre la ejecución o el fin de contratos (lista para revisión manual).
Uso: uv run --with openpyxl python -I -X utf8 analizar_excel.py"""
import csv
import os
import re
import unicodedata
from collections import Counter

import openpyxl

AQUI = os.path.dirname(os.path.abspath(__file__))
EXCEL = os.path.join(AQUI, "fuentes", "excel", "ResolucionesAE.xlsx")

# Columnas de cada hoja → campo armonizado (se toma la primera que exista).
EQUIV = {
    "resolucion": ["Resolución"],
    "motivo": ["Motivo de la reclamación", "Motivo denegación / reclamación", "Primer motivo denegación / reclamación"],
    "motivo2": ["Segundo motivo denegación/reclamación", "Otros motivos"],
    "sentido": ["Sentido de la resolución", "Sentido"],
    "asunto": ["Asunto"],
    "descriptores": ["Descriptores materia 1", "Descriptores materia 2", "Descriptores materia 3", "Descriptores"],
    "criterio": ["Criterio CTBG 1", "Criterio CTBG 2", "Criterio del Consejo. 1er nivel", "Criterio del Consejo. 2º nivel", "Otros criterios"],
    "palabras": ["Palabras clave"],
    "mes_entrada": ["Mes de entrada"],
    "anio_entrada": ["Año de entrada de la reclamación", "Año de entrada (reclamación)"],
    "mes_resolucion": ["Mes de resolución"],
    "organismo": ["Ministerio/organismo", "Ministerio / Organismo"],
}
UNIR = {"descriptores", "criterio", "motivo2"}   # campos que concatenan varias columnas

# Ejecución o fin del contrato. Se busca en asunto + descriptores + palabras clave (sin tildes, minúsculas).
EJECUCION = [r"\brecepcion", r"certificacion(es)? final", r"certificaciones? de obra", r"\bliquidacion",
             r"\bejecucion del contrato", r"ejecucion de (la|las) obra", r"\bmodificad", r"modificacion(es)? del contrato",
             r"\bsobrecoste", r"\bpenalidad", r"\bresolucion del contrato", r"\bfinalizacion", r"\bfin de (la )?obra",
             r"\bprorroga", r"\bdemora", r"\bfacturas?\b", r"\bcertificaciones\b", r"\bacta de comprobacion",
             r"\bgarantia definitiva", r"\bdireccion de obra", r"\bincumplimiento del contrat"]
CONTRATO = [r"\bcontrat", r"\blicitacion", r"\badjudicacion", r"\bobras?\b", r"\bpliego", r"\bexpediente de contratacion"]


def norm(s):
    s = unicodedata.normalize("NFD", str(s or "")).encode("ascii", "ignore").decode()
    return " ".join(s.lower().split())


def sentido_norm(s):
    s = norm(s)
    if s.startswith("desestim"):   # antes que «estim», que está contenido en «desestimatoria»
        return "desestimatoria"
    if "formal" in s:
        return "estimatoria por motivos formales"
    if "parcial" in s and "estim" in s:
        return "estimatoria parcial"
    if "estim" in s:
        return "estimatoria"
    if "desestim" in s:
        return "desestimatoria"
    if "inadmi" in s:
        return "inadmitida"
    if "archiv" in s or "desist" in s or "perdida" in s or "carencia" in s:
        return "archivo / pérdida de objeto"
    return "otro" if s else "sin dato"


def leer():
    wb = openpyxl.load_workbook(EXCEL, read_only=True)
    filas = []
    for ws in wb.worksheets:
        it = ws.iter_rows(values_only=True)
        cab = [str(c).strip() if c else "" for c in next(it)]
        for r in it:
            if not any(r):
                continue
            d = dict(zip(cab, r))
            f = {"anio_resolucion": ws.title}
            for campo, cols in EQUIV.items():
                vals = [str(d[c]).strip() for c in cols if c in d and d[c] not in (None, "")]
                f[campo] = " | ".join(vals) if campo in UNIR else (vals[0] if vals else "")
            if not f["resolucion"]:
                continue
            f["sentido_norm"] = sentido_norm(f["sentido"])
            f["silencio"] = "silencio" in norm(f["motivo"])
            texto = norm(" ".join([f["asunto"], f["descriptores"], f["palabras"]]))
            f["contratos"] = any(re.search(p, texto) for p in CONTRATO)
            f["ejecucion"] = f["contratos"] and any(re.search(p, texto) for p in EJECUCION)
            filas.append(f)
    return filas


def pct(a, b): return f"{100 * a / b:.1f} %" if b else "—"


MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]


def mes(s):
    s = norm(s)
    for i, m in enumerate(MESES, 1):
        if s.startswith(m):
            return i


def meses(f):
    """Meses naturales entre entrada y resolución; None si falta algún dato o sale negativo."""
    me, mr = mes(f["mes_entrada"]), mes(f["mes_resolucion"])
    try:
        ae, ar = int(str(f["anio_entrada"])[:4]), int(f["anio_resolucion"])
    except ValueError:
        return None
    if not me or not mr:
        return None
    d = (ar - ae) * 12 + (mr - me)
    return d if 0 <= d <= 60 else None


def main():
    filas = leer()
    campos = ["anio_resolucion", "resolucion", "anio_entrada", "mes_entrada", "mes_resolucion", "motivo", "motivo2",
              "sentido", "sentido_norm", "silencio", "asunto", "descriptores", "criterio", "palabras", "contratos",
              "ejecucion", "organismo"]
    with open(os.path.join(AQUI, "resoluciones.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=campos)
        w.writeheader()
        w.writerows(filas)

    print(f"Resoluciones: {len(filas)}\n")
    print("== 1. Silencio por año de resolución")
    print("año | resoluciones | por silencio | de ellas: estimatoria por motivos formales / estimatoria (total o parcial) / desestimatoria / otras")
    for anio in sorted({f["anio_resolucion"] for f in filas}):
        a = [f for f in filas if f["anio_resolucion"] == anio]
        s = [f for f in a if f["silencio"]]
        c = Counter(f["sentido_norm"] for f in s)
        est = c["estimatoria"] + c["estimatoria parcial"]
        print(f"{anio} | {len(a)} | {len(s)} ({pct(len(s), len(a))}) | {c['estimatoria por motivos formales']} ({pct(c['estimatoria por motivos formales'], len(s))}) / "
              f"{est} ({pct(est, len(s))}) / {c['desestimatoria']} / {len(s) - est - c['estimatoria por motivos formales'] - c['desestimatoria']}")

    print("\n== 2. Contratos")
    con = [f for f in filas if f["contratos"]]
    for etiqueta, sub in (("todas", filas), ("contratos", con), ("ejecución o fin", [f for f in con if f["ejecucion"]])):
        c = Counter(f["sentido_norm"] for f in sub)
        s = sum(f["silencio"] for f in sub)
        print(f"{etiqueta}: {len(sub)}; por silencio {s} ({pct(s, len(sub))}); "
              + "; ".join(f"{k} {v} ({pct(v, len(sub))})" for k, v in c.most_common()))

    print("\n== 3. Meses entre la entrada de la reclamación y la resolución (aproximado, por mes natural)")
    print("año de resolución | con dato | mediana | más de 3 meses (plazo del art. 24.4 LTAIBG)")
    for anio in sorted({f["anio_resolucion"] for f in filas}):
        m = sorted(x for x in (meses(f) for f in filas if f["anio_resolucion"] == anio) if x is not None)
        if m:
            print(f"{anio} | {len(m)} | {m[len(m) // 2]} | {pct(sum(x > 3 for x in m), len(m))}")

    eje = [f for f in con if f["ejecucion"]]
    with open(os.path.join(AQUI, "ejecucion_candidatas.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["anio_resolucion", "resolucion", "motivo", "sentido_norm", "asunto", "descriptores", "palabras"], extrasaction="ignore")
        w.writeheader()
        w.writerows(eje)
    print(f"\nCandidatas sobre ejecución o fin escritas en ejecucion_candidatas.csv: {len(eje)}")


if __name__ == "__main__":
    main()
