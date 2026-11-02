"""Descarga la página web de cada obra de la muestra y extrae las filas con fecha (anuncios y documentos).
Uso: python -I descargar_paginas.py   (1 petición cada 1,5 s; reanudable)"""
import csv, hashlib, html, json, os, re, time, urllib.request, http.cookiejar
from datetime import datetime, timezone
AQUI = os.path.dirname(os.path.abspath(__file__))
op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
op.addheaders = [("User-Agent", "Mozilla/5.0 (estudio de datos abiertos; descarga pausada)")]
salida = os.path.join(AQUI, "paginas_extraidas.jsonl")
hechos = {json.loads(l)["id"] for l in open(salida, encoding="utf-8")} if os.path.exists(salida) else set()
with open(salida, "a", encoding="utf-8") as log:
    for r in csv.DictReader(open(os.path.join(AQUI, "muestra.csv"), encoding="utf-8")):
        if r["id"] in hechos: continue
        time.sleep(1.5)
        res = {"id": r["id"], "estrato": r["estrato"], "fecha_hora_utc": datetime.now(timezone.utc).isoformat(timespec="seconds")}
        try:
            with op.open(r["enlace"], timeout=90) as resp:
                res["http"] = resp.status; datos = resp.read()
            clave = hashlib.sha1(r["id"].encode()).hexdigest()[:16]
            open(os.path.join(AQUI, "paginas", clave + ".html"), "wb").write(datos)
            res["fichero"] = clave + ".html"; res["sha256"] = hashlib.sha256(datos).hexdigest()
            t = datos.decode("utf-8", "replace")
            filas = []
            for m in re.finditer(r"<tr.*?</tr>", t, re.S):
                txt = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", m.group(0)))).strip()
                if re.search(r"\d{2}/\d{2}/\d{4}", txt) and len(txt) < 400:
                    filas.append(txt)
            res["filas"] = list(dict.fromkeys(filas))
        except Exception as e:
            res["error"] = repr(e)[:300]
        log.write(json.dumps(res, ensure_ascii=False) + "\n"); log.flush()
print("hecho")
