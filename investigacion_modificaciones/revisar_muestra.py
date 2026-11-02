"""Revisión de la muestra (PREREGISTRO.md, «Revisión manual»), con dos añadidos posteriores al preregistro:
el XML de cada anuncio de modificación (fecha de la modificación frente a la del anuncio, texto, importe y plazo)
y la búsqueda en la página de documentos sobre la modificación. No extrae datos de adjudicatarios.
Uso local: python -I -X utf8 revisar_muestra.py   (1 petición cada 1,5 s; reanudable)"""
import html
import http.cookiejar
import json
import os
import re
import time
import unicodedata
import urllib.request
import xml.etree.ElementTree as ET

AQUI = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(AQUI, "revision_manual")
op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
op.addheaders = [("User-Agent", "Mozilla/5.0 (estudio de datos abiertos; descarga pausada)")]
DOC_MOD = re.compile(r"modific|informe|alegac|aprobaci|resoluci|suspensi|ampliac|prorrog|precios contradictorios")


def local(t): return t.rsplit("}", 1)[-1]


def norm(s): return unicodedata.normalize("NFD", s or "").encode("ascii", "ignore").decode().lower()


def hijo(el, n):
    return next((c for c in el if local(c.tag) == n), None) if el is not None else None


def txt(el): return (el.text or "").strip() if el is not None else ""


def leer_xml(datos):
    raiz = ET.fromstring(datos)
    out = {"raiz": local(raiz.tag), "fecha_anuncio": txt(hijo(raiz, "IssueDate"))[:10], "modificaciones": []}
    for m in (c for c in raiz if local(c.tag) == "ContractModification"):
        cm = hijo(m, "ContractModificationLegalMonetaryTotal")
        out["modificaciones"].append({
            "num": txt(hijo(m, "ID")), "fecha_modificacion": txt(hijo(m, "IssueDate"))[:10],
            "nota": " ".join(txt(hijo(m, "Note")).split())[:300],
            "importe": txt(hijo(cm, "TaxExclusiveAmount")),
            "plazo": txt(hijo(m, "ContractModificationDurationMeasure")) or txt(hijo(m, "FinalDurationMeasure")),
        })
    return out


def main():
    salida = os.path.join(R, "revision.jsonl")
    hechos = set()
    if os.path.exists(salida):
        with open(salida, encoding="utf-8") as fh:
            hechos = {json.loads(l)["id"] for l in fh}
    with open(os.path.join(R, "paginas_extraidas.jsonl"), encoding="utf-8") as fh:
        paginas = [json.loads(l) for l in fh]
    with open(salida, "a", encoding="utf-8") as log:
        for p in paginas:
            if p["id"] in hechos or "fichero" not in p:
                continue
            with open(os.path.join(R, "paginas", p["fichero"]), encoding="utf-8", errors="replace") as fh:
                t = fh.read()
            res = {"id": p["id"], "anuncios": [], "documentos_modificacion": []}
            for m in re.finditer(r"<tr.*?</tr>", t, re.S):
                fila = m.group(0)
                texto = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", fila))).strip()
                if "Modificaci" in fila and ("Modificación de Contrato" in texto):
                    enlaces = [html.unescape(u) for u in re.findall(r'href="([^"]+)"', fila) if "GetDocument" in u]
                    tipos = re.findall(r'alt="([^"]+)"', fila)
                    xml = next((u for u, a in zip(enlaces, tipos) if "xml" in a.lower()), None)
                    a = {"fila": texto[:120], "rectificacion": texto.find("Rectificaci") >= 0}
                    if xml:
                        time.sleep(1.5)
                        try:
                            a.update(leer_xml(op.open(xml, timeout=90).read()))
                        except Exception as e:  # noqa: BLE001
                            a["error"] = repr(e)[:200]
                    res["anuncios"].append(a)
                elif re.search(r"\d{2}/\d{2}/\d{4}", texto) and DOC_MOD.search(norm(texto)) and "Modificación de Contrato" not in texto:
                    res["documentos_modificacion"].append(texto[:160])
            log.write(json.dumps(res, ensure_ascii=False) + "\n")
            log.flush()
    print("hecho")


if __name__ == "__main__":
    main()
