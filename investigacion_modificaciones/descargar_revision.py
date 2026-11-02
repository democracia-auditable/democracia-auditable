"""Descarga la página web de cada obra de muestra_revision.csv y extrae las filas con fecha (anuncios y documentos)
y los enlaces a documentos. Uso local: las páginas contienen nombres de órganos y empresas (no publicar).
Uso: python -I -X utf8 descargar_revision.py   (1 petición cada 1,5 s; reanudable)"""
import csv
import hashlib
import html
import http.cookiejar
import json
import os
import re
import time
import urllib.request
from datetime import datetime, timezone

AQUI = os.path.dirname(os.path.abspath(__file__))
CARPETA = os.path.join(AQUI, "revision_manual")
os.makedirs(os.path.join(CARPETA, "paginas"), exist_ok=True)
op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
op.addheaders = [("User-Agent", "Mozilla/5.0 (estudio de datos abiertos; descarga pausada)")]
salida = os.path.join(CARPETA, "paginas_extraidas.jsonl")
hechos = set()
if os.path.exists(salida):
    with open(salida, encoding="utf-8") as fh:
        hechos = {json.loads(l)["id"] for l in fh}
with open(os.path.join(AQUI, "muestra_revision.csv"), encoding="utf-8") as fh:
    muestra = list(csv.DictReader(fh))
with open(salida, "a", encoding="utf-8") as log:
    for r in muestra:
        if r["id"] in hechos:
            continue
        time.sleep(1.5)
        res = {"id": r["id"], "fecha_hora_utc": datetime.now(timezone.utc).isoformat(timespec="seconds")}
        try:
            with op.open(r["enlace"], timeout=90) as resp:
                res["http"] = resp.status
                datos = resp.read()
            clave = hashlib.sha1(r["id"].encode()).hexdigest()[:16]
            with open(os.path.join(CARPETA, "paginas", clave + ".html"), "wb") as f:
                f.write(datos)
            res.update(fichero=clave + ".html", sha256=hashlib.sha256(datos).hexdigest())
            t = datos.decode("utf-8", "replace")
            filas = []
            for m in re.finditer(r"<tr.*?</tr>", t, re.S):
                txt = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", m.group(0)))).strip()
                if re.search(r"\d{2}/\d{2}/\d{4}", txt) and len(txt) < 400:
                    filas.append(txt)
            res["filas"] = list(dict.fromkeys(filas))
        except Exception as e:  # noqa: BLE001
            res["error"] = repr(e)[:300]
        log.write(json.dumps(res, ensure_ascii=False) + "\n")
        log.flush()
print("hecho")
