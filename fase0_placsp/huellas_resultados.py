"""Huellas de los ficheros por expediente de una ejecución de medir_ejecucion.py, que el proyecto no publica.

El repositorio publica solo cifras agregadas. Para que una repetición del análisis se pueda comprobar sin publicar
la lista de obras, se publican las huellas SHA-256 de esos ficheros: quien repita el análisis con los mismos datos
(manifiesto_descarga_estudio.json) y el mismo programa debe obtener exactamente las mismas.

Uso:
  python huellas_resultados.py escribir resultados_v2_4      -> resultados_v2_4/huellas_resultados.json
  python huellas_resultados.py comprobar resultados_v2_4 MI_CARPETA
      compara los ficheros de MI_CARPETA (una repetición) con las huellas publicadas en resultados_v2_4.
"""
import hashlib
import json
import os
import sys

FICHEROS = ["expedientes_seleccionados.csv", "candidatos_fin.csv", "empates_en_seleccion.csv"]


def sha256(ruta):
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def main():
    if len(sys.argv) < 3 or sys.argv[1] not in ("escribir", "comprobar"):
        raise SystemExit(__doc__)
    carpeta = sys.argv[2]
    ruta = os.path.join(carpeta, "huellas_resultados.json")
    if sys.argv[1] == "escribir":
        with open(os.path.join(carpeta, "resumen.json"), encoding="utf-8") as f:
            version = json.load(f)["version_programa"]
        huellas = {"version_programa": version, "nota": "huellas de ficheros por expediente que no se publican; "
                   "una repetición con los mismos datos y programa debe dar las mismas",
                   "ficheros": {n: sha256(os.path.join(carpeta, n)) for n in FICHEROS}}
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(huellas, f, ensure_ascii=False, indent=2)
        print(f"escrito {ruta}")
        return
    if len(sys.argv) != 4:
        raise SystemExit(__doc__)
    with open(ruta, encoding="utf-8") as f:
        publicadas = json.load(f)["ficheros"]
    iguales = True
    for n, h in publicadas.items():
        propia = os.path.join(sys.argv[3], n)
        obtenida = sha256(propia) if os.path.exists(propia) else "(no existe)"
        ok = obtenida == h
        iguales &= ok
        print(f"{'IGUAL   ' if ok else 'DISTINTO'} {n}")
    print("La repetición coincide exactamente con el estudio." if iguales else
          "La repetición NO coincide: revisa que los datos (manifiesto) y la versión del programa sean los mismos.")
    sys.exit(0 if iguales else 1)


if __name__ == "__main__":
    main()
