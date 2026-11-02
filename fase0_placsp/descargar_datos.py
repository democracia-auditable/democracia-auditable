#!/usr/bin/env python3
"""Descarga y verifica los ZIP oficiales de la sindicación de la PLACSP usados por la fase 0.

Dos modos, que NO son lo mismo:

  reproducir  Descarga (si faltan) los ficheros del manifiesto del estudio y comprueba que su
              SHA-256 coincide. Si coincide, `medir_ejecucion.py` debe dar exactamente los mismos
              resultados. Si no coincide, el fichero oficial ha cambiado desde el estudio (Hacienda
              regenera los paquetes; los mensuales del año en curso cambian cada mes): ya no es una
              reproducción, sino una repetición con datos distintos.

  actualizar  Descarga los ficheros indicados tal como están hoy y escribe un manifiesto NUEVO
              (URL, fecha y hora de descarga, Last-Modified del servidor, bytes, SHA-256). Sirve para
              repetir el estudio con datos posteriores; los resultados pueden diferir.

Solo biblioteca estándar. Ejemplos:
    python descargar_datos.py reproducir --manifiesto manifiesto_descarga_estudio.json --destino datos
    python descargar_datos.py actualizar --anuales 2023 2024 2025 --mensuales 202601 202602 --destino datos_nuevos
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone

BASE = "https://contrataciondelsectorpublico.gob.es/sindicacion/sindicacion_643/"
PREFIJO = "licitacionesPerfilesContratanteCompleto3_"
CONJUNTO = ("Licitaciones publicadas en los perfiles del contratante ubicados en la Plataforma de "
            "Contratación del Sector Público (excluyendo contratos menores) — Ministerio de Hacienda, datos abiertos")


def sha256(ruta: str) -> str:
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def descargar(url: str, destino: str) -> dict:
    """Descarga a un fichero temporal y lo renombra al terminar. El servidor es lento (≈0,5–3 MB/s)."""
    tmp = destino + ".part"
    peticion = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (fase0-democracia-auditable)"})
    with urllib.request.urlopen(peticion, timeout=120) as r, open(tmp, "wb") as f:
        last_modified = r.headers.get("Last-Modified", "")
        total = 0
        for bloque in iter(lambda: r.read(1 << 20), b""):
            f.write(bloque)
            total += len(bloque)
            if total % (100 << 20) < (1 << 20):
                print(f"    {os.path.basename(destino)}: {total >> 20} MB", file=sys.stderr, flush=True)
    os.replace(tmp, destino)
    return {"last_modified_servidor": last_modified,
            "descargado_utc": datetime.now(timezone.utc).isoformat(timespec="seconds")}


def reproducir(manifiesto: str, destino: str) -> int:
    with open(manifiesto, encoding="utf-8") as f:
        man = json.load(f)
    os.makedirs(destino, exist_ok=True)
    fallos = 0
    for fic in man["ficheros"]:
        ruta = os.path.join(destino, fic["nombre"])
        if not os.path.exists(ruta):
            print(f"Descargando {fic['nombre']} …", file=sys.stderr)
            descargar(fic["url"], ruta)
        h = sha256(ruta)
        ok = h == fic["sha256"]
        fallos += not ok
        print(f"{'OK   ' if ok else 'DISTINTO'} {fic['nombre']}  {os.path.getsize(ruta)} bytes  {h}")
    if fallos:
        print(f"\n{fallos} fichero(s) no coinciden con el estudio. Con ellos se REPITE el estudio con datos "
              "distintos; no se reproduce. Ver la explicación al inicio de este script.")
    else:
        print("\nTodos los ficheros coinciden: `medir_ejecucion.py` debe reproducir los resultados del estudio.")
    return 1 if fallos else 0


def actualizar(anuales: list[str], mensuales: list[str], destino: str) -> int:
    os.makedirs(destino, exist_ok=True)
    ficheros = []
    for periodo in anuales + mensuales:
        nombre = f"{PREFIJO}{periodo}.zip"
        url = BASE + nombre
        ruta = os.path.join(destino, nombre)
        print(f"Descargando {nombre} …", file=sys.stderr)
        meta = descargar(url, ruta)
        ficheros.append({"nombre": nombre, "url": url, "bytes": os.path.getsize(ruta), "sha256": sha256(ruta), **meta})
    man = {"conjunto": CONJUNTO, "pagina_oficial":
           "https://www.hacienda.gob.es/es-es/gobiernoabierto/datos%20abiertos/paginas/licitacionescontratante.aspx",
           "especificacion": "https://contrataciondelsectorpublico.gob.es/datosabiertos/especificacion-sindicacion.pdf",
           "modo": "actualizar", "ficheros": ficheros}
    ruta_man = os.path.join(destino, "manifiesto_descarga.json")
    with open(ruta_man, "w", encoding="utf-8") as f:
        json.dump(man, f, ensure_ascii=False, indent=2)
    print(f"Manifiesto nuevo: {ruta_man}")
    return 0


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="modo", required=True)
    r = sub.add_parser("reproducir")
    r.add_argument("--manifiesto", default="manifiesto_descarga_estudio.json")
    r.add_argument("--destino", default="datos")
    a = sub.add_parser("actualizar")
    a.add_argument("--anuales", nargs="*", default=[])
    a.add_argument("--mensuales", nargs="*", default=[])
    a.add_argument("--destino", default="datos_nuevos")
    args = ap.parse_args()
    if args.modo == "reproducir":
        sys.exit(reproducir(args.manifiesto, args.destino))
    sys.exit(actualizar(args.anuales, args.mensuales, args.destino))


if __name__ == "__main__":
    main()
