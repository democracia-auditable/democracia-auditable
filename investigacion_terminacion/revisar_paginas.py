"""Comprobación en la web de una muestra de obras SIN final publicado que la regla E4t v2 marca:
¿consta la resolución del primer contrato en su página de la PLACSP, con un nombre que el clasificador no
reconoce, o no consta en ningún sitio? Muestra de 20 (semilla 20261102) de revision_manual/marcadas_sinfin.txt.
Uso local (las páginas contienen nombres de órganos y empresas): python -I -X utf8 revisar_paginas.py"""
import hashlib
import html
import http.cookiejar
import json
import os
import random
import re
import time
import unicodedata
import urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(AQUI, "revision_manual")
RESOL = re.compile(r"resoluci\w*\s+(del?\s+)?(contrato|contracte)|resolver\s+el\s+contrato|rescisi|desistimiento|"
                   r"mutuo\s+acuerdo|incumplimiento|extinci\w*\s+del\s+contrato|penalidad|incautaci|garant\w*.*(incaut|perd)")
LICIT = re.compile(r"ofert|licitac|licitador|adjudicac|clasificac|mesa")


def norm(s): return unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()


def main():
    with open(os.path.join(R, "marcadas_sinfin.txt"), encoding="utf-8") as f:
        enlaces = [l.strip() for l in f if l.strip().startswith("https://")]
    muestra = random.Random(20261102).sample(enlaces, min(20, len(enlaces)))
    op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
    op.addheaders = [("User-Agent", "Mozilla/5.0 (estudio de datos abiertos; descarga pausada)")]
    os.makedirs(os.path.join(R, "paginas"), exist_ok=True)
    salida = []
    for i, url in enumerate(muestra, 1):
        time.sleep(1.5)
        res = {"n": i, "enlace": url}
        try:
            datos = op.open(url, timeout=90).read()
            clave = hashlib.sha1(url.encode()).hexdigest()[:16]
            with open(os.path.join(R, "paginas", clave + ".html"), "wb") as f:
                f.write(datos)
            t = datos.decode("utf-8", "replace")
            filas = []
            for mm in re.finditer(r"<tr.*?</tr>", t, re.S):
                txt = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", mm.group(0)))).strip()
                if re.search(r"\d{2}/\d{2}/\d{4}", txt) and len(txt) < 400:
                    filas.append(txt)
            res["filas"] = list(dict.fromkeys(filas))
            res["indicios_resolucion"] = [x for x in res["filas"] if RESOL.search(norm(x)) and not LICIT.search(norm(x))]
            res["sha256"] = hashlib.sha256(datos).hexdigest()
        except Exception as e:  # noqa: BLE001
            res["error"] = repr(e)[:200]
        salida.append(res)
        print(i, "error" if "error" in res else f"{len(res['filas'])} filas; indicios de resolución: {len(res['indicios_resolucion'])}")
    with open(os.path.join(R, "revision_paginas.json"), "w", encoding="utf-8") as f:
        json.dump(salida, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
