"""Índice de los PDF de resoluciones de ámbito estatal publicados en la web del Consejo de Transparencia.
Recorre la página de cada año (2015–2026) y la de cada mes, y escribe indice_pdf.csv (año, página, URL del PDF).
Una petición por segundo. Uso: python -I -X utf8 indexar_pdf.py"""
import csv
import os
import re
import time
import urllib.parse
import urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
BASE = "https://consejodetransparencia.es"
RAIZ = "/reclamaciones/nuestras-resoluciones/resoluciones-ambito-estatal"


def get(ruta):
    time.sleep(1)
    req = urllib.request.Request(BASE + ruta, headers={"User-Agent": "Mozilla/5.0"})
    return urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "replace")


filas = []
for anio in range(2015, 2027):
    html = get(f"{RAIZ}/{anio}")
    meses = sorted(set(re.findall(rf'href="({re.escape(RAIZ)}/{anio}/[^"#?]+)"', html)))
    paginas = meses or [f"{RAIZ}/{anio}"]
    for pag in paginas:
        h = html if pag == f"{RAIZ}/{anio}" else get(pag)
        pdfs = sorted(set(re.findall(r'href="([^"]+\.pdf)"', h, re.I)))
        for p in pdfs:
            filas.append({"anio": anio, "pagina": pag, "url": urllib.parse.urljoin(BASE, p)})
        print(anio, pag.rsplit("/", 1)[-1], len(pdfs))

with open(os.path.join(AQUI, "indice_pdf.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["anio", "pagina", "url"])
    w.writeheader()
    w.writerows(filas)
print("PDF:", len(filas), "únicos:", len({f["url"] for f in filas}))
