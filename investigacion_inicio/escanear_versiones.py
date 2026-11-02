"""Indicios de ejecución por versión (PREREGISTRO.md). Recorre los ZIP de la PLACSP y escribe:
  versiones_obras.csv  una fila por versión de cada expediente de obras, con sus indicios;
  estado_final.csv     el estado final de cada obra con la política de versiones del estudio y su nivel A/B/C.
Uso: python -I -X utf8 escanear_versiones.py [--datos "patrón1;patrón2"]"""
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
REPLANTEO = re.compile(r"comprobaci\w*\s+(del\s+)?replanteo|acta\s+(de\s+)?replanteo")
MARCAS = ["mod_estructurada", "anuncio_modificacion", "doc_durante", "doc_fin_parcial", "replanteo",
          "fin", "ccn", "indicio"]


def nombres_documentos(entry):
    for el in entry.iter():
        t = me.local(el.tag)
        if t == "FileName" and el.text:
            yield el.text
        elif t == "DocumentTypeCode" and el.get("name"):
            yield el.get("name")


def marcas(d, entry):
    docs = d["documentos_ejecucion"]
    rep = any(REPLANTEO.search(n) and "previo" not in n for n in map(me.normalizar, nombres_documentos(entry)))
    m = {
        "mod_estructurada": d["n_modificaciones"] > 0,
        "anuncio_modificacion": bool(d["anuncio_modificacion"]),
        "doc_durante": any(docs.get(c) for c in me.DOCS_DURANTE),
        "doc_fin_parcial": any(docs.get(c) for c in me.DOCS_FIN_PARCIAL),
        "replanteo": rep,
        "ccn": bool(d["anuncio_finalizacion"]),
    }
    m["fin"] = m["ccn"] or any(docs.get(c) for c in me.DOCS_FIN_DEFINITIVO)
    m["indicio"] = m["mod_estructurada"] or m["anuncio_modificacion"] or m["doc_durante"] or m["doc_fin_parcial"] or rep
    return m


def formalizacion(entry):
    cfs = me.child(entry, "ContractFolderStatus")
    fechas = []
    for tr in me.children(cfs, "TenderResult") if cfs is not None else []:
        c = me.child(tr, "Contract")
        if c is not None and me.text(me.child(c, "IssueDate")):
            fechas.append(me.text(me.child(c, "IssueDate"))[:10])
    return min(fechas) if fechas else ""


def procesar(args):
    ruta, nombre = args
    versiones, borrados, filas = [], [], []
    with zipfile.ZipFile(ruta) as z, z.open(nombre) as f:
        for _e, el in ET.iterparse(f, events=("end",)):
            if el.tag == me.ATOM + "entry":
                ident, act, d = es.extraer_cualquier_tipo(el)
                if d is not None and d.get("tipo_contrato") == "3":
                    m = marcas(d, el)
                    fz = formalizacion(el)
                    filas.append({"id": ident, "updated": act, "fecha_anuncio_finalizacion": d["fecha_anuncio_finalizacion"],
                                  "formalizacion": fz, **m})
                    d = {**d, "_marcas": m, "_formalizacion": fz}
                else:
                    d = None
                versiones.append((ident, act, d))
                el.clear()
            elif el.tag == me.TOMBSTONE:
                c = el.find(me.TOMBSTONE_NS + "comment")
                tipo = (c.get("type", "") if c is not None else "") or "SIN_TIPO"
                borrados.append((el.get("ref", ""), el.get("when", ""), tipo.upper()))
                el.clear()
    return versiones, borrados, filas


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--datos", default=DATOS)
    a = ap.parse_args()
    zips = sorted(z for p in a.datos.split(os.pathsep) for z in glob.glob(p))
    trabajos = [(r, n) for r in zips for n in sorted(zipfile.ZipFile(r).namelist()) if n.endswith(".atom")]
    print(len(zips), "ZIP,", len(trabajos), "ficheros ATOM", flush=True)
    todas = []

    def resultados():
        with ProcessPoolExecutor() as ex:
            for versiones, borrados, filas in ex.map(procesar, trabajos, chunksize=4):
                todas.extend(filas)
                yield versiones, borrados

    ultima, borrados = es.acumular(resultados())
    estados, excluidos = es.estados_finales(ultima, borrados)
    with open(os.path.join(AQUI, "versiones_obras.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["id", "updated", "fecha_anuncio_finalizacion", "formalizacion"] + MARCAS)
        w.writeheader()
        w.writerows(todas)
    campos = ["id", "estado", "n_resultados_adjudicados", "presupuesto_sin_iva", "fecha_adjudicacion", "formalizacion",
              "fin_teorico", "fecha_anuncio_finalizacion", "nivel"] + MARCAS
    with open(os.path.join(AQUI, "estado_final.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        for e in estados:
            m = e["_marcas"]
            nivel = "A" if m["fin"] else "B" if m["indicio"] else "C"
            w.writerow({**{k: e.get(k, "") for k in campos}, **m, "formalizacion": e["_formalizacion"], "nivel": nivel})
    print(f"versiones de obras: {len(todas)}; obras en estado final: {len(estados)} (excluidas por borrado: {excluidos})")


if __name__ == "__main__":
    main()
