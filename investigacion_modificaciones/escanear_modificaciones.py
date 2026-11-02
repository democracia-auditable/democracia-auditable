"""Modificaciones de contrato en el estado final de cada obra (PREREGISTRO.md).
Escribe modificaciones.csv (una fila por ContractModification) y obras_modificadas.csv (una por obra).
Contienen texto libre (Note) y enlaces: uso local, no publicar (ver .gitignore).
Uso: python -I -X utf8 escanear_modificaciones.py [--datos "patrón1;patrón2"]"""
import argparse
import csv
import glob
import os
import re
import sys
import xml.etree.ElementTree as ET
import zipfile
from concurrent.futures import ProcessPoolExecutor

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "investigacion_doc_ccn"))
sys.path.insert(0, os.path.join(AQUI, "..", "fase0_placsp"))
import escanear as es  # noqa: E402
import medir_ejecucion as me  # noqa: E402

DATOS = os.pathsep.join(os.path.join(AQUI, "..", "datos", d, "*.zip")
                        for d in ("placsp_anteriores", "placsp_2023", "placsp_posteriores"))
TEXTO_PLAZO = re.compile(r"ampliaci\w*\s+(de|del)\s+plazo|prorroga|plazo de ejecucion|nuevo plazo")
TEXTO_DINERO = re.compile(r"euros|€|\d+[.,]\d{2}\s*(eur|€)|incremento|presupuesto")
MIN_TEXTO = 40


def modificaciones(entry):
    cfs = me.child(entry, "ContractFolderStatus")
    out = []
    for m in me.children(cfs, "ContractModification") if cfs is not None else []:
        nota = " ".join(me.text(me.child(m, "Note")).split())
        cmlmt = me.child(m, "ContractModificationLegalMonetaryTotal")
        importe = me.a_float(me.text(me.child(cmlmt, "TaxExclusiveAmount"))) if cmlmt is not None else None
        plazo = me.child(m, "ContractModificationDurationMeasure") is not None or me.child(m, "FinalDurationMeasure") is not None
        n = me.normalizar(nota)
        con_importe = importe is not None and importe != 0
        out.append({
            "num_modificacion": me.text(me.child(m, "ID")), "contrato_id": me.text(me.child(m, "ContractID")),
            "longitud_nota": len(nota), "sin_justificacion": len(n) < MIN_TEXTO,
            "importe": "" if importe is None else importe, "con_importe": con_importe, "con_plazo": plazo,
            "sin_estructura": not con_importe and not plazo,
            "texto_plazo_sin_campo": bool(TEXTO_PLAZO.search(n)) and not plazo,
            "texto_dinero_sin_importe": bool(TEXTO_DINERO.search(n)) and not con_importe,
            "nota": nota[:600],
        })
    for x in out:
        x["opaca"] = x["sin_estructura"] and x["sin_justificacion"]
    return out


def anuncios_mod(entry):
    cfs = me.child(entry, "ContractFolderStatus")
    fechas = []
    for v in me.children(cfs, "ValidNoticeInfo") if cfs is not None else []:
        if me.text(me.child(v, "NoticeTypeCode")) == "DOC_MOD":
            for el in v.iter():
                if me.local(el.tag) == "IssueDate" and el.text:
                    fechas.append(el.text[:10])
    return fechas


def procesar(args):
    ruta, nombre = args
    versiones, borrados = [], []
    with zipfile.ZipFile(ruta) as z, z.open(nombre) as f:
        for _e, el in ET.iterparse(f, events=("end",)):
            if el.tag == me.ATOM + "entry":
                ident, act, d = es.extraer_cualquier_tipo(el)
                if d is not None and d.get("tipo_contrato") == "3" and d["n_modificaciones"] > 0:
                    d = {**d, "_mods": modificaciones(el), "_doc_mod": anuncios_mod(el),
                         "documentos_ejecucion": {k: True for k, v in d["documentos_ejecucion"].items() if v}}
                elif d is not None and d.get("tipo_contrato") == "3":
                    d = {"_sin_mod": True, "id": ident}   # obra sin modificaciones: basta con saber que existe
                else:
                    d = None
                versiones.append((ident, act, d))
                el.clear()
            elif el.tag == me.TOMBSTONE:
                c = el.find(me.TOMBSTONE_NS + "comment")
                tipo = (c.get("type", "") if c is not None else "") or "SIN_TIPO"
                borrados.append((el.get("ref", ""), el.get("when", ""), tipo.upper()))
                el.clear()
    return versiones, borrados


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--datos", default=DATOS)
    a = ap.parse_args()
    zips = sorted(z for p in a.datos.split(os.pathsep) for z in glob.glob(p))
    trabajos = [(r, n) for r in zips for n in sorted(zipfile.ZipFile(r).namelist()) if n.endswith(".atom")]
    print(len(zips), "ZIP,", len(trabajos), "ficheros ATOM", flush=True)
    with ProcessPoolExecutor() as ex:
        ultima, borrados = es.acumular(ex.map(procesar, trabajos, chunksize=4))
    estados, excluidos = estados_finales(ultima, borrados)
    mods, obras = [], []
    for e in estados:
        if e.get("_sin_mod"):
            continue
        docs = e["documentos_ejecucion"]
        base = {"id": e["id"], "enlace": e["enlace"], "organo_id": e["organo_id"], "estado": e["estado"],
                "n_resultados_adjudicados": e["n_resultados_adjudicados"], "presupuesto_sin_iva": e["presupuesto_sin_iva"]}
        obras.append({**base, "n_modificaciones": len(e["_mods"]), "n_doc_mod": len(e["_doc_mod"]),
                      "primer_doc_mod": min(e["_doc_mod"]) if e["_doc_mod"] else "",
                      "doc_modificacion": bool(docs.get("documento_modificacion")),
                      "n_opacas": sum(m["opaca"] for m in e["_mods"])})
        for m in e["_mods"]:
            mods.append({**base, **m})
    for nombre, filas in (("modificaciones.csv", mods), ("obras_modificadas.csv", obras)):
        with open(os.path.join(AQUI, nombre), "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(filas[0].keys()))
            w.writeheader()
            w.writerows(filas)
    print(f"obras en estado final: {len(estados)} (excluidas por borrado: {excluidos}); con modificaciones: {len(obras)}; "
          f"modificaciones: {len(mods)}")


def estados_finales(ultima, borrados):
    """escanear.estados_finales() espera versiones completas; aquí las obras sin modificaciones llevan un
    marcador reducido. Misma política: última `updated`, borrados ANULADA/SIN_TIPO posteriores excluidos y,
    en empates, elegir_principal() entre las versiones completas (o el marcador si no hay ninguna)."""
    estados, excluidos = [], 0
    for ident, (t, versiones) in ultima.items():
        validas = [v for v in versiones if v is not None]
        if not validas:
            continue
        if ident in borrados and borrados[ident][0] >= t and borrados[ident][1] in ("ANULADA", "SIN_TIPO"):
            excluidos += 1
            continue
        completas = [v for v in validas if not v.get("_sin_mod")]
        principal = dict(me.elegir_principal(completas)) if completas else dict(validas[0])
        principal["id"] = ident
        estados.append(principal)
    return estados, excluidos


if __name__ == "__main__":
    main()
