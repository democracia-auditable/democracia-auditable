"""Consulta privada (NO forma parte del estudio): extrae de los 15 ZIP la última versión de cada
expediente de obras con los campos necesarios para medir señales explícitas de problema
(textos cbc:Note de las modificaciones, documentos, anuncios) y nuevas licitaciones.

Reutiliza fase0_placsp/medir_ejecucion.py en solo lectura. Escribe obras.jsonl en esta carpeta (uso local: contiene títulos y enlaces; no publicar).
Copia sin cambios de lógica del extractor de la sesión de la consulta privada (01/11/2026), usada aquí para validar la regla E4t v2.
"""
import glob
import json
import os
import sys
import zipfile
from concurrent.futures import ProcessPoolExecutor
import xml.etree.ElementTree as ET

sys.dont_write_bytecode = True
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "fase0_placsp"))
import medir_ejecucion as m  # noqa: E402

RAIZ = os.path.join(AQUI, "..", "datos")


def extras(entry):
    cfs = m.child(entry, "ContractFolderStatus")
    proyecto = m.child(cfs, "ProcurementProject")
    titulo = m.text(m.child(proyecto, "Name")) if proyecto is not None else ""
    cpvs, prtr = set(), False
    for el in cfs.iter():
        t = m.local(el.tag)
        if t == "ItemClassificationCode" and m.text(el):
            cpvs.add(m.text(el))
        elif t == "FundingProgramCode" and m.text(el) == "PRTR":
            prtr = True
    mods = []
    for mod in m.children(cfs, "ContractModification"):
        tot = m.child(mod, "ContractModificationLegalMonetaryTotal")
        imp = m.a_float(m.text(m.child(tot, "TaxExclusiveAmount"))) if tot is not None else None
        plazo = any(m.child(mod, n) is not None and m.text(m.child(mod, n))
                    for n in ("FinalDurationMeasure", "ContractModificationDurationMeasure"))
        nota = " ".join(m.text(n) for n in mod.iter() if m.local(n.tag) == "Note" and m.text(n))
        mods.append({"importe": imp, "plazo": plazo, "nota": nota[:600]})
    fechas = sorted(m.text(d) for v in m.children(cfs, "ValidNoticeInfo")
                    for d in v.iter() if m.local(d.tag) == "IssueDate" and m.text(d))
    avisos = sorted({m.text(m.child(v, "NoticeTypeCode")) for v in m.children(cfs, "ValidNoticeInfo")})
    docs = sorted({m.text(d) for d in cfs.iter() if m.local(d.tag) == "FileName" and m.text(d)}
                  | {d.get("name") for d in cfs.iter() if m.local(d.tag) == "DocumentTypeCode" and d.get("name")})
    return {"titulo": titulo[:300], "cpvs": sorted(cpvs), "prtr": prtr, "mods": mods,
            "primer_anuncio": fechas[0][:10] if fechas else "", "avisos": avisos, "docs": docs[:80]}


def procesar(args):
    ruta, nombre = args
    ultima, borrados, maxupd = {}, {}, ""
    with zipfile.ZipFile(ruta) as z, z.open(nombre) as f:
        for _ev, el in ET.iterparse(f, events=("end",)):
            if el.tag == m.ATOM + "entry":
                ident, upd, exp = m.extraer(el)
                maxupd = max(maxupd, upd)
                if exp is not None:
                    d = {k: v for k, v in vars(exp).items() if k != "documentos_ejecucion"}
                    d["cats"] = sorted(exp.documentos_ejecucion)
                    d.update(extras(el))
                else:
                    d = None
                p = ultima.get(ident)
                if p is None or m.fecha(upd) > m.fecha(p[0]) or (
                        m.fecha(upd) == m.fecha(p[0]) and d and (p[1] is None or d["n_documentos"] > p[1]["n_documentos"])):
                    ultima[ident] = (upd, d)
                el.clear()
            elif el.tag == m.TOMBSTONE:
                com = el.find(m.TOMBSTONE_NS + "comment")
                tipo = ((com.get("type", "") if com is not None else "") or "SIN_TIPO").upper()
                ref, when = el.get("ref", ""), el.get("when", "")
                if ref not in borrados or m.fecha(when) > m.fecha(borrados[ref][0]):
                    borrados[ref] = (when, tipo)
                el.clear()
    return ultima, borrados, maxupd


def main():
    zips = sorted(glob.glob(os.path.join(RAIZ, "*", "*.zip")))
    tareas = []
    for r in zips:
        with zipfile.ZipFile(r) as z:
            tareas += [(r, n) for n in sorted(z.namelist()) if n.endswith(".atom")]
    print(len(zips), "ZIP,", len(tareas), "ficheros", flush=True)
    ultima, borrados, maxupd = {}, {}, ""
    with ProcessPoolExecutor(max_workers=6) as ex:
        for i, (u, b, mu) in enumerate(ex.map(procesar, tareas, chunksize=4), 1):
            maxupd = max(maxupd, mu)
            for k, (upd, d) in u.items():
                p = ultima.get(k)
                if p is None or m.fecha(upd) > m.fecha(p[0]) or (
                        m.fecha(upd) == m.fecha(p[0]) and d and (p[1] is None or d["n_documentos"] > p[1]["n_documentos"])):
                    ultima[k] = (upd, d)
            for k, (when, tipo) in b.items():
                if k not in borrados or m.fecha(when) > m.fecha(borrados[k][0]):
                    borrados[k] = (when, tipo)
            if i % 500 == 0:
                print(f"  {i}/{len(tareas)}", flush=True)
    n = 0
    with open(os.path.join(AQUI, "obras.jsonl"), "w", encoding="utf-8") as f:
        for k, (upd, d) in ultima.items():
            if d is None:
                continue
            if k in borrados and m.fecha(borrados[k][0]) >= m.fecha(upd) and borrados[k][1] in ("ANULADA", "SIN_TIPO"):
                continue
            d["corte"] = m.fecha(maxupd).date().isoformat()
            f.write(json.dumps(d, ensure_ascii=False) + "\n")
            n += 1
    print("obras escritas:", n, "corte:", m.fecha(maxupd).date())


if __name__ == "__main__":
    main()
