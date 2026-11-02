"""Descarga el XML (ContractCompletionNotice) de cada anuncio de finalización desde la web de la PLACSP.
Reanudable; 1 petición cada 1,5 s. Los expedientes cuya última pasada terminó en error se reintentan.

Uso: python -I descargar_ccn.py [--entrada obras_estado_final.csv] [--carpeta xml_anuncios]
La entrada es cualquier CSV con columnas `id`, `enlace` y `anuncio_finalizacion`; solo se procesan
los expedientes con anuncio vigente. Registro: <carpeta>/_registro.jsonl, una línea por pasada, con la
URL, el código HTTP, la fecha y hora (UTC), el tamaño y la huella SHA-256 de cada documento.
"""
import argparse
import csv
import hashlib
import html
import json
import os
import re
import time
import urllib.request
import http.cookiejar
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

PAUSA = 1.5
cj = http.cookiejar.CookieJar()
op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
op.addheaders = [("User-Agent", "Mozilla/5.0 (estudio de datos abiertos; descarga pausada)")]


def pedir(url):
    ultimo = None
    for intento in range(3):
        try:
            time.sleep(PAUSA)
            with op.open(url, timeout=90) as r:
                return r.status, r.read()
        except Exception as e:
            ultimo = e
            time.sleep(10 * (intento + 1))
    raise ultimo


def es_ccn(datos):
    try:
        return ET.fromstring(datos).tag.rsplit("}", 1)[-1] == "ContractCompletionNotice"
    except ET.ParseError:
        return False


def main():
    aqui = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser()
    ap.add_argument("--entrada", default=os.path.join(aqui, "obras_estado_final.csv"))
    ap.add_argument("--carpeta", default=os.path.join(aqui, "xml_anuncios"))
    a = ap.parse_args()
    os.makedirs(a.carpeta, exist_ok=True)
    registro = os.path.join(a.carpeta, "_registro.jsonl")
    ultimo = {}
    if os.path.exists(registro):
        for linea in open(registro, encoding="utf-8"):
            d = json.loads(linea)
            ultimo[d["id"]] = d
    hechos = {i for i, d in ultimo.items() if "error" not in d}
    filas = [r for r in csv.DictReader(open(a.entrada, encoding="utf-8")) if r["anuncio_finalizacion"] == "True"]
    print(len(filas), "expedientes;", len(hechos), "ya hechos", flush=True)
    with open(registro, "a", encoding="utf-8") as log:
        for i, r in enumerate(filas, 1):
            if r["id"] in hechos:
                continue
            clave = hashlib.sha1(r["id"].encode()).hexdigest()[:16]
            res = {"id": r["id"], "clave": clave, "pagina": r["enlace"],
                   "fecha_hora_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"), "anuncios": []}
            try:
                estado, pagina = pedir(r["enlace"])
                res["http_pagina"] = estado
                for m in re.finditer(r"<tr.*?</tr>", pagina.decode("utf-8", "replace"), re.S):
                    fila = m.group(0)
                    texto = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", fila))).strip()
                    if not re.search(r"finalizaci[oó]n de contrato", texto, re.I):
                        continue
                    anuncio = {"texto": texto[:200], "fichero": ""}
                    # Se prueba cada enlace de la fila hasta encontrar el XML ContractCompletionNotice.
                    for enlace in [html.unescape(h) for h in re.findall(r'href="([^"]*GetDocumentByIdServlet[^"]*)"', fila)]:
                        estado, datos = pedir(enlace)
                        if es_ccn(datos):
                            nombre = f"{clave}_{len(res['anuncios'])}.xml"
                            with open(os.path.join(a.carpeta, nombre), "wb") as f:
                                f.write(datos)
                            anuncio.update(fichero=nombre, url=enlace, http=estado, bytes=len(datos),
                                           sha256=hashlib.sha256(datos).hexdigest())
                            break
                    else:
                        anuncio["error"] = "ningún enlace de la fila es un ContractCompletionNotice"
                    res["anuncios"].append(anuncio)
                if not res["anuncios"]:
                    res["aviso"] = "la página no muestra ningún anuncio de finalización"
            except Exception as e:
                res["error"] = repr(e)[:300]
            log.write(json.dumps(res, ensure_ascii=False) + "\n")
            log.flush()
            if i % 25 == 0:
                print(f"{i}/{len(filas)}", flush=True)
    print("fin", flush=True)


if __name__ == "__main__":
    main()
