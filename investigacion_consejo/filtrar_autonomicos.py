"""Complemento autonómico de la rama 5 (COMPLEMENTO_AUTONOMICO.md): filtra las resoluciones de dos órganos de
garantía autonómicos con los términos fijados antes de descargar los datos.

Datos de entrada (descarga manual en datos_autonomicos/, que no se publica):
  - andalucia_2t.csv: resoluciones de reclamaciones de derecho de acceso del Consejo de Transparencia y Protección de
    Datos de Andalucía (portal de datos abiertos de la Junta de Andalucía, organización CTPDA). Campos usados:
    «Resumen», «Indicador», «Fecha», «Sentido», «Url».
  - gaip.csv: resoluciones de la Comissió de Garantia del Dret d'Accés a la Informació Pública (conjunto de la GAIP en
    analisi.transparenciacatalunya.cat). Campos usados: «Informació reclamada», «Paraules clau», «Resum»,
    «Resolució», «Data de resolució», «Sentit de la resolució», «Condició reclamant», «Temps trigat en resoldre», «URL».
Salida: candidatas_autonomicas.jsonl (uso local: los resúmenes nombran administraciones; no se publica). La
clasificación de cada candidata se hizo después a mano (ver el complemento).

Copia del filtro usado el 01/11/2026 en la sesión que hizo la búsqueda, con las rutas adaptadas a esta carpeta.
Uso: python -I -X utf8 filtrar_autonomicos.py
"""
import csv
import io
import json
import os
import re
import unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(AQUI, "datos_autonomicos")
csv.field_size_limit(10**8)

TERM = re.compile(r"acta\w*\s+de\s+recep|recepcio\w*\s+de\s+(la\s+|l'|les\s+|las\s+)?obr|recepcio\w*\s+d'obr"
                  r"|certificaci\w*\s+final|liquidaci\w*\s+del?\s+contra|final\s+d[e']\s*obra|replante|replanteig")


def norm(s):
    return unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()


def arregla(s):
    """Algunos campos del fichero andaluz vienen con la codificación cambiada (UTF-8 leído como cp1252)."""
    try:
        return s.encode("cp1252").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return s


def main():
    out = {}
    raw = open(os.path.join(D, "andalucia_2t.csv"), encoding="utf-8").read()
    filas = list(csv.reader(io.StringIO(raw)))
    cab = [arregla(x) for x in filas[0]]
    A = [dict(zip(cab, [arregla(v) for v in f])) for f in filas[1:] if f]
    candA = [r for r in A if TERM.search(norm(r.get("Resumen", "") + " " + r.get("Indicador", "")))]
    out["andalucia"] = {"total": len(A), "anios": f"{min(r['Fecha'][-4:] for r in A)}-{max(r['Fecha'][-4:] for r in A)}",
                        "candidatas": len(candA)}
    G = list(csv.DictReader(open(os.path.join(D, "gaip.csv"), encoding="utf-8")))
    candG = [r for r in G if TERM.search(norm(" ".join(r.get(k, "") for k in ("Informació reclamada", "Paraules clau", "Resum"))))]
    out["gaip"] = {"total": len(G), "candidatas": len(candG)}
    print(json.dumps(out, ensure_ascii=False))
    with open(os.path.join(AQUI, "candidatas_autonomicas.jsonl"), "w", encoding="utf-8") as f:
        for r in candA:
            f.write(json.dumps({"fuente": "andalucia", "num": r.get(cab[0]), "fecha": r["Fecha"], "sentido": r["Sentido"],
                                "indicador": r["Indicador"][:300], "resumen": r["Resumen"][:900], "url": r["Url"]}, ensure_ascii=False) + "\n")
        for r in candG:
            f.write(json.dumps({"fuente": "gaip", "num": r["Resolució"], "fecha": r["Data de resolució"], "sentido": r["Sentit de la resolució"],
                                "reclamante": r["Condició reclamant"], "dias": r["Temps trigat en resoldre"],
                                "info": r["Informació reclamada"][:400], "claves": r["Paraules clau"][:300],
                                "resumen": r["Resum"][:900], "url": r["URL"]}, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
