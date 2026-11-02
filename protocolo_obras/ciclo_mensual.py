"""Protocolo de obras: el ciclo de cada mes en una sola orden.

  1. Descarga los ficheros de la PLACSP que falten (anuales de los años cerrados; mensuales del año en curso;
     el del mes en curso se vuelve a descargar siempre, porque crece) y anota sus huellas.
  2. Escanea los datos con la política de versiones del estudio (seleccionar_obras.py escanear).
  3. Prepara el lote del mes: las obras cuya fecha de pregunta ha llegado desde el último ciclo. La primera vez,
     además, sortea la muestra fija de 200 obras acumuladas; los meses siguientes la completa con la lista guardada.
  4. Añade las obras de los lotes al registro (como «preparadas sin enviar»), lo valida y escribe los pendientes
     en pendientes_AAAA-MM-DD.csv (se abre con cualquier hoja de cálculo).
  5. Escribe resumen_ciclo_AAAA-MM-DD.md con lo que hay que hacer y guarda la fecha del ciclo en ciclo_estado.json.

Es reanudable: si se interrumpe (o se cancela desde la interfaz), al volver a lanzarlo el mismo día reutiliza los
lotes ya preparados y no los rehace. Si el registro tiene errores, se detiene antes de preparar nada y no da el ciclo
por hecho hasta que se corrijan.

Todo se escribe en la carpeta de trabajo (--trabajo; por defecto, esta). Las salidas contienen datos reales de
órganos y obras: no se publican (ver .gitignore). Nada se envía a ningún sitio: las solicitudes las presenta
la organización por la sede electrónica de cada órgano.

Uso:
  python -I -X utf8 ciclo_mensual.py --organizacion ORG1
  python -I -X utf8 ciclo_mensual.py --organizacion ORG1 --sin-descarga --datos "RUTA/*.zip"   (sin red)
Opciones: --fecha AAAA-MM-DD (por defecto, hoy) · --desde-anio 2021 · --min 1000000 · --tope 4 · --muestra 200
          · --prioridad antiguedad|terminacion (qué obras van primero si el tope obliga a aplazar; ver SENAL_TERMINACION.md)
          · --festivos festivos.txt (festivos autonómicos y locales: «AAAA-MM-DD», «AAAA-MM-DD Comunidad» u
            «AAAA-MM-DD organo:ID», uno por línea; ver registro.cargar_festivos)
"""
import argparse
import csv
import glob
import json
import os
import subprocess
import sys
import urllib.error
from datetime import date, timedelta

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "fase0_placsp"))

PY = [sys.executable, "-I", "-X", "utf8"]


def ficheros_necesarios(hoy, desde_anio):
    """(periodo, siempre): anuales de los años cerrados y mensuales del año en curso hasta el mes actual.
    `siempre` indica que hay que volver a descargarlo aunque exista (el del mes en curso)."""
    necesarios = [(str(a), False) for a in range(desde_anio, hoy.year)]
    necesarios += [(f"{hoy.year}{m:02d}", m == hoy.month) for m in range(1, hoy.month + 1)]
    return necesarios


def descargar(carpeta, hoy, desde_anio, registro_descargas):
    import descargar_datos as dd   # solo hace falta si se descarga (con --sin-descarga no se importa)
    os.makedirs(carpeta, exist_ok=True)
    for periodo, siempre in ficheros_necesarios(hoy, desde_anio):
        nombre = f"{dd.PREFIJO}{periodo}.zip"
        ruta = os.path.join(carpeta, nombre)
        if os.path.exists(ruta) and not siempre:
            continue
        try:
            print(f"Descargando {nombre} …", flush=True)
            meta = dd.descargar(dd.BASE + nombre, ruta)
        except urllib.error.HTTPError as e:
            if len(periodo) == 4 and e.code == 404:
                # El anual de un año recién cerrado puede no estar publicado todavía: se usan sus mensuales.
                print(f"  {nombre} no está publicado; se usan los mensuales de {periodo}")
                for m in range(1, 13):
                    nm = f"{dd.PREFIJO}{periodo}{m:02d}.zip"
                    rm = os.path.join(carpeta, nm)
                    if not os.path.exists(rm):
                        registro_descargas.append({"nombre": nm, **dd.descargar(dd.BASE + nm, rm), "sha256": dd.sha256(rm)})
                continue
            if e.code == 404 and siempre:
                print(f"  {nombre} todavía no existe (mes recién empezado)")
                continue
            raise
        registro_descargas.append({"nombre": nombre, **meta, "sha256": dd.sha256(ruta)})


def ejecutar(args, codigos_validos=(0,)):
    print("  $", " ".join(os.path.basename(a) if a.endswith(".py") else a for a in args[len(PY):]), flush=True)
    r = subprocess.run(args, capture_output=True, text=True, encoding="utf-8")
    if r.returncode not in codigos_validos:
        print(r.stdout, r.stderr)
        raise SystemExit(f"Falló: {' '.join(args)}")
    return r


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--organizacion", required=True, help="código de quien envía (no el nombre de una persona)")
    ap.add_argument("--fecha", default=date.today().isoformat())
    ap.add_argument("--trabajo", default=AQUI, help="carpeta donde se escriben datos, lotes y registro")
    ap.add_argument("--datos", default="", help="patrones de ZIP ya descargados (separados por el separador de rutas)")
    ap.add_argument("--sin-descarga", action="store_true")
    ap.add_argument("--reutilizar-escaneo", action="store_true", help="usar obras_protocolo.csv si ya existe")
    ap.add_argument("--desde-anio", type=int, default=2021)
    ap.add_argument("--min", default="1000000")
    ap.add_argument("--tope", default="4")
    ap.add_argument("--justificacion-tope", default="", help="obligatoria si --tope es mayor que 4")
    ap.add_argument("--festivos", default="", help="fichero con festivos autonómicos y locales («AAAA-MM-DD», «AAAA-MM-DD Comunidad» u «AAAA-MM-DD organo:ID»)")
    ap.add_argument("--muestra", type=int, default=200)
    ap.add_argument("--prioridad", choices=["antiguedad", "terminacion"], default="antiguedad",
                    help="orden cuando el tope por órgano obliga a aplazar obras (ver SENAL_TERMINACION.md)")
    a = ap.parse_args()
    hoy = date.fromisoformat(a.fecha)
    t = os.path.abspath(a.trabajo)
    os.makedirs(t, exist_ok=True)
    estado_ruta = os.path.join(t, "ciclo_estado.json")
    estado = {}
    if os.path.exists(estado_ruta):
        with open(estado_ruta, encoding="utf-8") as f:
            estado = json.load(f)

    registro = os.path.join(t, "registro.csv")
    rg = os.path.join(AQUI, "registro.py")

    # 0. El registro tiene que estar bien antes de preparar nada (si no, los pendientes y las cifras serían erróneos).
    if os.path.exists(registro):
        v0 = ejecutar(PY + [rg, "validar", "--registro", registro], codigos_validos=(0, 1))
        if v0.returncode:
            print(v0.stdout)
            raise SystemExit("El registro tiene errores (arriba, línea por línea). Corregidlos y volved a lanzar el ciclo: "
                             "no se ha preparado nada ni se ha dado el mes por hecho.")

    # 1. Datos
    descargas = []
    if a.sin_descarga:
        patrones = a.datos or os.path.join(t, "datos", "*.zip")
    else:
        descargar(os.path.join(t, "datos"), hoy, a.desde_anio, descargas)
        patrones = os.path.join(t, "datos", "*.zip")
    zips = sorted(z for p in patrones.split(os.pathsep) for z in glob.glob(p))
    if not zips:
        raise SystemExit(f"No hay ficheros de datos en {patrones}")
    print(f"1. Datos: {len(zips)} ficheros ({len(descargas)} descargados ahora)")

    # 2. Escaneo
    obras = os.path.join(t, "obras_protocolo.csv")
    if a.reutilizar_escaneo and os.path.exists(obras):
        print("2. Escaneo reutilizado:", obras)
    else:
        ejecutar(PY + [os.path.join(AQUI, "seleccionar_obras.py"), "escanear", "--datos", patrones, "--salida", obras])
        print("2. Escaneo terminado")

    # 3. Lotes: flujo desde el último ciclo y muestra de lo acumulado
    desde = estado.get("ultimo_ciclo") or (hoy - timedelta(days=31)).isoformat()
    comun = ["--obras", obras, "--registro", registro, "--fecha", hoy.isoformat(), "--min", a.min,
             "--tope", a.tope, "--prioridad", a.prioridad, "--carpeta", t]
    if a.justificacion_tope:
        comun += ["--justificacion-tope", a.justificacion_tope]
    sel = os.path.join(AQUI, "seleccionar_obras.py")

    def lote(nombre, extra):
        """Prepara un lote o, si ya se preparó hoy (ciclo interrumpido), lo reutiliza sin rehacerlo."""
        carpeta = os.path.join(t, f"lote_{hoy.isoformat()}_{nombre}")
        if os.path.exists(os.path.join(carpeta, "lote.csv")):
            print(f"   lote {nombre} ya preparado hoy: se reutiliza (ciclo reanudado)")
            return carpeta, ""
        if os.path.exists(carpeta):
            raise SystemExit(f"{carpeta} quedó a medias (sin lote.csv). Revisad su contenido y, si no se ha enviado nada, "
                             "borradla y volved a lanzar el ciclo.")
        return carpeta, ejecutar(PY + [sel, "seleccionar", *comun, *extra, "--nombre", nombre]).stdout

    c_flujo, salida = lote("flujo", ["--desde", desde])
    lotes = [os.path.join(c_flujo, "lote.csv")]
    muestra = estado.get("muestra")
    if not muestra and a.muestra:
        c_m, s_m = lote("muestra", ["--muestra", str(a.muestra)])
        muestra = os.path.join(c_m, "muestra.csv")
        if not os.path.exists(muestra):
            raise SystemExit(f"No se escribió {muestra}: no se guarda una muestra que no existe.")
        lotes.append(os.path.join(c_m, "lote.csv"))
        salida += s_m
    elif muestra:
        if not os.path.exists(muestra):
            raise SystemExit(f"La muestra fija guardada en ciclo_estado.json no existe: {muestra}")
        c_m, s_m = lote("muestra", ["--lista", muestra])
        lotes.append(os.path.join(c_m, "lote.csv"))
        salida += s_m
    print("3. Lotes preparados")
    for linea in salida.splitlines():
        if linea.startswith(("Candidatas", "Carpeta", "Muestra")):
            print("   ", linea)

    # 4. Registro y pendientes
    nuevas = 0
    for lote in lotes:
        if os.path.exists(lote):
            r = ejecutar(PY + [rg, "crear", "--registro", registro, "--lote", lote, "--organizacion", a.organizacion])
            nuevas += int(r.stdout.split()[1]) if r.stdout.startswith("Añadidas") else 0
    v = ejecutar(PY + [rg, "validar", "--registro", registro], codigos_validos=(0, 1))
    if v.returncode:
        print(v.stdout)
        raise SystemExit("El registro tiene errores tras añadir los lotes: corregidlos y volved a lanzar el ciclo (se "
                         "reanudará sin rehacer los lotes). El mes no se da por hecho.")
    festivos = ["--festivos", a.festivos] if a.festivos else []
    p = ejecutar(PY + [rg, "pendientes", "--registro", registro, "--fecha", hoy.isoformat(), *festivos])
    pend_ruta = os.path.join(t, f"pendientes_{hoy.isoformat()}.csv")
    tareas = [l.split("  ", 2) for l in p.stdout.splitlines() if l.strip()]
    with open(pend_ruta, "w", newline="", encoding="utf-8-sig") as f:   # BOM: lo abre bien cualquier hoja de cálculo
        w = csv.writer(f, delimiter=";")
        w.writerow(["fecha", "id_obra", "tarea"])
        w.writerows(tareas)
    sin_enviar = sum("preparada sin enviar" in x[-1] for x in tareas)
    reclamar = sum("reclamar" in x[-1] for x in tareas)
    print(f"4. Registro: {nuevas} obras nuevas; {len(tareas)} tareas pendientes ({sin_enviar} sin enviar, {reclamar} por reclamar)")
    print("   validación:", v.stdout.strip().splitlines()[-1] if v.stdout.strip() else "sin salida")

    # 5. Resumen y estado
    res = os.path.join(t, f"resumen_ciclo_{hoy.isoformat()}.md")
    with open(res, "w", encoding="utf-8") as f:
        f.write(f"# Ciclo del {hoy.isoformat()}\n\n")
        f.write(f"- Datos: {len(zips)} ficheros; descargados en este ciclo: {', '.join(d['nombre'] for d in descargas) or 'ninguno'}\n")
        f.write(f"- Obras nuevas añadidas al registro: {nuevas} (flujo desde {desde}"
                f"{'; muestra fija: ' + os.path.relpath(muestra, t) if muestra else ''})\n")
        f.write(f"- Solicitudes preparadas sin enviar: {sin_enviar}. Están en `lote_{hoy.isoformat()}_*/solicitudes/`.\n")
        f.write(f"- Reclamaciones que toca presentar: {reclamar}.\n")
        f.write(f"- Validación del registro: {v.stdout.strip().splitlines()[-1] if v.stdout.strip() else '—'}\n")
        f.write(f"- Calendario de los vencimientos: sábados, domingos y festivos nacionales"
                f"{'; festivos propios de ' + os.path.basename(a.festivos) if a.festivos else ' (sin festivos autonómicos ni locales: añadidlos con --festivos)'}. "
                "Los plazos dependen del régimen de cada obra (columna «regimen»; ver regimenes.py); si no está verificado, "
                "no se calcula fecha. Las fechas calculadas son PROVISIONALES: «en plazo» y las cifras de plazos solo usan "
                "la columna `fecha_limite_verificada`, que anota una persona tras comprobar recepción, calendario del "
                "lugar, suspensiones y ampliación.\n\n")
        f.write("## Qué hacer ahora\n\n"
                "1. Presentar cada solicitud preparada por la sede electrónica del órgano y anotar en `registro.csv` "
                "`fecha_envio` y `ref_solicitud`.\n"
                "2. Revisar `pendientes_" + hoy.isoformat() + ".csv`: reclamar las que estén en silencio antes de la fecha indicada "
                "(plantilla `plantillas/reclamacion_silencio.txt`).\n"
                "3. Anotar respuestas, documentos recibidos y fechas de replanteo y recepción.\n"
                "4. Para publicar resultados, ejecutar `python -I -X utf8 registro.py exportar`: crea "
                "`registro_publico_BORRADOR.csv`, que hay que revisar caso por caso antes de publicarlo (ver `GUIA.md`).\n")
    estado.update(ultimo_ciclo=hoy.isoformat(), muestra=muestra,
                  historial=estado.get("historial", []) + [{"fecha": hoy.isoformat(), "nuevas": nuevas, "descargas": descargas}])
    with open(estado_ruta, "w", encoding="utf-8") as f:
        json.dump(estado, f, ensure_ascii=False, indent=2)
    print(f"5. Resumen: {res}")


if __name__ == "__main__":
    main()
