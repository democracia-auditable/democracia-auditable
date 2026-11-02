"""Rama 3: cuántas obras figuran como finalizadas en la API de contrataciones públicas de Euskadi.
Para cada año de adjudicación y estado del procedimiento, pide a la API solo el total (totalItems)
de contratos de obras, de cualquier importe y de 1 a 10 M€ (filtro contract-budget de la API).
Escribe estados_api.csv con la fecha y hora de consulta. Una petición cada 0,5 s.
Uso: python -I -X utf8 estados_api.py"""
import csv
import datetime
import json
import os
import time
import urllib.parse
import urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
API = "https://api.euskadi.eus/procurements"


def get(ruta, **q):
    time.sleep(0.5)
    url = f"{API}/{ruta}?" + urllib.parse.urlencode(q)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=60)), url


estados = {e["id"]: e["name"] for e in get("contracting-notices/procedures-status")[0]}
filas = []
for anio in range(2019, 2025):
    for tramo, filtro in (("todas", {}), ("1-10 M€", {"contract-budget.gt": 1000000, "contract-budget.lt": 10000000})):
        base = {"contract-type-id": 1, "award-date.gt": f"{anio - 1}-12-31", "award-date.lt": f"{anio + 1}-01-01",
                "itemsOfPage": 1, **filtro}
        total = get("contracts", **base)[0]["totalItems"]
        for eid, nombre in estados.items():
            d, url = get("contracts", **base, **{"contract-procedure-status-id": eid})
            if d["totalItems"]:
                filas.append({"anio_adjudicacion": anio, "tramo": tramo, "estado_id": eid, "estado": nombre,
                              "n": d["totalItems"], "total": total, "url": url,
                              "consulta_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")})
        print(anio, tramo, total, {f["estado"]: f["n"] for f in filas if f["anio_adjudicacion"] == anio and f["tramo"] == tramo})

with open(os.path.join(AQUI, "estados_api.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(filas[0].keys()))
    w.writeheader()
    w.writerows(filas)
