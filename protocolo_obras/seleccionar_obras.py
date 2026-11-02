"""Protocolo de obras: selección de las obras sobre las que toca preguntar y preparación de las solicitudes.

Dos órdenes:

  escanear    Recorre los ZIP de la PLACSP una vez y escribe obras_protocolo.csv: el estado final de cada
              obra con la MISMA política de versiones que el estudio (investigacion_doc_ccn/escanear.py y
              fase0_placsp/medir_ejecucion.py v2.3), más el título, el código postal del órgano y, a partir
              de él, la comunidad autónoma y el órgano ante el que se reclamaría (art. 24 y DA 4.ª LTAIBG).

  seleccionar Para una fecha dada, elige las obras cuya fecha de pregunta (fin teórico + margen) ya ha
              llegado, sin indicador de fin definitivo y que no figuran en el registro de resultados;
              aplica un tope de solicitudes por órgano y lote, y escribe la carpeta lote_AAAA-MM-DD/ con
              lote.csv y una solicitud ya redactada por obra (plantillas/solicitud_obra.txt).

Uso:
  python -I -X utf8 seleccionar_obras.py escanear [--datos "patrón1;patrón2"] [--salida obras_protocolo.csv]
  python -I -X utf8 seleccionar_obras.py seleccionar [--fecha 2026-11-01] [--margen 120] [--min 1000000]
         [--max 0] [--tope 4] [--registro registro.csv] [--obras obras_protocolo.csv]

No extrae datos personales: ni contactos de los órganos ni adjudicatarios.
El título y el código postal se guardan APARTE de la versión, así que no intervienen en el desempate de versiones con
la misma `updated` (elegir_principal): la elección de versión es la misma que en el estudio.
«Obra» significa aquí EXPEDIENTE de la PLACSP, que puede contener varios contratos o lotes.
"""
import argparse
import csv
import glob
import hashlib
import json
import os
import random
import sys
import xml.etree.ElementTree as ET
import zipfile
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from datetime import date, timedelta

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)   # con -I no se añade la carpeta del script
sys.path.insert(0, os.path.join(AQUI, "..", "investigacion_doc_ccn"))
sys.path.insert(0, os.path.join(AQUI, "..", "fase0_placsp"))
import escanear as es  # noqa: E402
import medir_ejecucion as me  # noqa: E402
import senal_terminacion as st  # noqa: E402
import regimenes as rgm  # noqa: E402

DATOS = os.pathsep.join(os.path.join(AQUI, "..", "datos", d, "*.zip")
                        for d in ("placsp_anteriores", "placsp_2023", "placsp_posteriores"))
PLANTILLA = os.path.join(AQUI, "plantillas", "solicitud_obra.txt")

# Provincia (dos primeras cifras del código postal) -> comunidad o ciudad autónoma.
PROVINCIAS = {
    "04": "Andalucía", "11": "Andalucía", "14": "Andalucía", "18": "Andalucía", "21": "Andalucía",
    "23": "Andalucía", "29": "Andalucía", "41": "Andalucía", "22": "Aragón", "44": "Aragón", "50": "Aragón",
    "33": "Principado de Asturias", "07": "Illes Balears", "35": "Canarias", "38": "Canarias",
    "39": "Cantabria", "02": "Castilla-La Mancha", "13": "Castilla-La Mancha", "16": "Castilla-La Mancha",
    "19": "Castilla-La Mancha", "45": "Castilla-La Mancha", "05": "Castilla y León", "09": "Castilla y León",
    "24": "Castilla y León", "34": "Castilla y León", "37": "Castilla y León", "40": "Castilla y León",
    "42": "Castilla y León", "47": "Castilla y León", "49": "Castilla y León", "08": "Cataluña",
    "17": "Cataluña", "25": "Cataluña", "43": "Cataluña", "03": "Comunitat Valenciana",
    "12": "Comunitat Valenciana", "46": "Comunitat Valenciana", "06": "Extremadura", "10": "Extremadura",
    "15": "Galicia", "27": "Galicia", "32": "Galicia", "36": "Galicia", "28": "Comunidad de Madrid",
    "30": "Región de Murcia", "31": "Comunidad Foral de Navarra", "01": "País Vasco", "20": "País Vasco",
    "48": "País Vasco", "26": "La Rioja", "51": "Ceuta", "52": "Melilla",
}
# Convenios vigentes por los que resuelve el Consejo de Transparencia y Buen Gobierno
# (fuentes/ctbg_convenios_ccaa_20261101.txt). Revisar antes de cada uso.
CONVENIO_CTBG = {"Principado de Asturias", "Cantabria", "Extremadura", "Illes Balears", "La Rioja", "Ceuta", "Melilla"}
ESTATAL = {"1", "6", "9"}                      # ContractingAuthorityCode-2.10
AUTONOMICO_LOCAL = {"2", "3", "7", "8", "10", "11"}
CAMPOS = ["id", "enlace", "expediente", "titulo", "organo", "organo_id", "tipo_administracion", "cp_organo",
          "ccaa_organo", "ambito", "garante", "estado", "presupuesto_sin_iva", "fecha_adjudicacion", "fecha_inicio",
          "primer_anuncio", "fin_teorico", "n_modificaciones", "fin_definitivo", "actualizado"]


def garante(tipo, ccaa):
    """Órgano ante el que se reclamaría frente al silencio o la denegación (orientativo)."""
    if tipo in ESTATAL:
        return "estatal", "Consejo de Transparencia y Buen Gobierno"
    if tipo in AUTONOMICO_LOCAL:
        if not ccaa:
            return "autonómico o local", "comprobar (comunidad desconocida)"
        if ccaa in CONVENIO_CTBG:
            return "autonómico o local", "Consejo de Transparencia y Buen Gobierno (por convenio)"
        return "autonómico o local", f"órgano de garantía de {ccaa}"
    return "otro", "comprobar (tipo de entidad sin ámbito claro)"


def extras(entry):
    cfs = me.child(entry, "ContractFolderStatus")
    proy = me.child(cfs, "ProcurementProject")
    party = me.child(me.child(cfs, "LocatedContractingParty"), "Party")
    cp = me.text(me.child(me.child(party, "PostalAddress"), "PostalZone")) if party is not None else ""
    # Fecha del primer anuncio publicado (la usa la señal de terminación para ordenar licitaciones en el tiempo).
    fechas = sorted(me.text(d) for v in me.children(cfs, "ValidNoticeInfo")
                    for d in v.iter() if me.local(d.tag) == "IssueDate" and me.text(d))
    return {"titulo": " ".join(me.text(me.child(proy, "Name")).split())[:400], "cp_organo": cp,
            "primer_anuncio": fechas[0][:10] if fechas else ""}


def procesar(args):
    """Como escanear.procesar(), pero solo conserva obras. El título y el código postal del órgano se devuelven
    aparte (clave: identificador y forma canónica de la versión) para no alterar el desempate de versiones."""
    ruta, nombre = args
    versiones, borrados, aux = [], [], []
    with zipfile.ZipFile(ruta) as z, z.open(nombre) as f:
        for _e, el in ET.iterparse(f, events=("end",)):
            if el.tag == me.ATOM + "entry":
                ident, act, d = es.extraer_cualquier_tipo(el)
                if d is not None and d.get("tipo_contrato") == "3":
                    aux.append((ident, me.canonica(d), extras(el)))
                else:
                    d = None   # se conserva la versión (para la política de versiones) sin su contenido
                versiones.append((ident, act, d))
                el.clear()
            elif el.tag == me.TOMBSTONE:
                c = el.find(me.TOMBSTONE_NS + "comment")
                tipo = (c.get("type", "") if c is not None else "") or "SIN_TIPO"
                borrados.append((el.get("ref", ""), el.get("when", ""), tipo.upper()))
                el.clear()
    return versiones, borrados, aux


def fila_obra(e):
    docs = e["documentos_ejecucion"]
    fin = bool(e["anuncio_finalizacion"]) or any(docs.get(c) for c in (
        "resolucion_contrato", "recepcion_definitiva", "liquidacion", "certificacion_final", "final_obra", me.CATEGORIA_NOTA))
    ccaa = PROVINCIAS.get((e.get("cp_organo") or "")[:2], "")
    ambito, gar = garante(e["tipo_administracion"], ccaa)
    f = {k: e.get(k, "") for k in CAMPOS}
    f.update(ccaa_organo=ccaa, ambito=ambito, garante=gar, fin_definitivo=fin)
    return f


def cmd_escanear(a):
    zips = sorted(z for patron in a.datos.split(os.pathsep) for z in glob.glob(patron))
    trabajos = [(r, n) for r in zips for n in sorted(zipfile.ZipFile(r).namelist()) if n.endswith(".atom")]
    print(len(zips), "ZIP,", len(trabajos), "ficheros ATOM", flush=True)
    auxiliares = {}

    def resultados():
        with ProcessPoolExecutor() as ex:
            for versiones, borrados, aux in ex.map(procesar, trabajos, chunksize=4):
                for ident, canon, adicional in aux:
                    auxiliares.setdefault(ident, {})[canon] = adicional
                yield versiones, borrados

    ultima, borrados = es.acumular(resultados())
    estados, excluidos = es.estados_finales(ultima, borrados)
    sin_aux = 0
    for e in estados:
        # Forma canónica de la versión elegida tal como salió de extraer(): sin lo que añade estados_finales().
        original = {k: v for k, v in e.items() if k != "ccn_discrepa_en_empate"}
        original["n_versiones_empatadas"] = 1
        aux = auxiliares.get(e["id"], {}).get(me.canonica(original))
        if aux is None:
            # No se toma el título ni el código postal de otra versión: se dejan vacíos (la obra queda con la
            # comunidad «desconocida» y el régimen sin verificar) y se informa de cuántas son.
            sin_aux += 1
            aux = {"titulo": "", "cp_organo": "", "primer_anuncio": ""}
        e.update(aux)
    with open(a.salida, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS)
        w.writeheader()
        for e in estados:
            w.writerow(fila_obra(e))
    print(f"obras: {len(estados)} (excluidas por borrado: {excluidos}; sin título ni código postal de la versión elegida: "
          f"{sin_aux}) -> {a.salida}")


def leer_registro(ruta):
    if not ruta or not os.path.exists(ruta):
        return []
    with open(ruta, encoding="utf-8") as fh:
        return [r for r in csv.DictReader(fh) if r.get("id_obra")]


def lotes_preparados(carpeta):
    """(carpeta del lote, fecha del lote, filas) de cada lote_*/lote.csv ya preparado."""
    out = []
    for ruta in glob.glob(os.path.join(carpeta, "lote_*", "lote.csv")):
        d = os.path.dirname(ruta)
        with open(ruta, encoding="utf-8") as fh:
            out.append((os.path.abspath(d), os.path.basename(d)[5:15], list(csv.DictReader(fh))))
    return out


def num(s):
    try:
        return float(s)
    except (TypeError, ValueError):
        return None


def proceso_vivo(pid):
    """¿Sigue en marcha el proceso? (en Windows no se usa os.kill, que lo terminaría)."""
    if pid <= 0:
        return False
    if sys.platform.startswith("win"):
        import ctypes
        h = ctypes.windll.kernel32.OpenProcess(0x1000, False, pid)   # PROCESS_QUERY_LIMITED_INFORMATION
        if not h:
            return False
        codigo = ctypes.c_ulong()
        ctypes.windll.kernel32.GetExitCodeProcess(h, ctypes.byref(codigo))
        ctypes.windll.kernel32.CloseHandle(h)
        return codigo.value == 259   # STILL_ACTIVE
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def cmd_seleccionar(a):
    os.makedirs(a.carpeta, exist_ok=True)
    cerrojo = os.path.join(a.carpeta, ".seleccion.lock")
    if os.path.exists(cerrojo):
        try:
            with open(cerrojo, encoding="utf-8") as fh:
                pid = int(fh.read().strip() or 0)
        except (OSError, ValueError):
            pid = 0
        if not proceso_vivo(pid):
            print(f"Cerrojo de una selección interrumpida (proceso {pid}, ya terminado): se retira.")
            os.remove(cerrojo)
    try:
        with open(cerrojo, "x", encoding="utf-8") as fh:
            fh.write(str(os.getpid()))
    except FileExistsError:
        raise SystemExit(f"Hay otra selección en curso: {cerrojo}.")
    try:
        _seleccionar(a)
    finally:
        os.remove(cerrojo)


TOPE_MAXIMO = 4   # salvaguarda frente al riesgo de abuso (PROTOCOLO_OBRAS.md, regla 3)


def _seleccionar(a):
    if a.tope < 1:
        raise SystemExit("El tope por órgano y mes tiene que ser 1 o más: no existe la opción «sin tope».")
    if a.tope > TOPE_MAXIMO and not a.justificacion_tope.strip():
        raise SystemExit(f"Un tope mayor que {TOPE_MAXIMO} exige --justificacion-tope «motivo»; queda escrito en el lote.")
    hoy = date.fromisoformat(a.fecha)
    mes = hoy.isoformat()[:7]
    carpeta = os.path.abspath(os.path.join(a.carpeta, f"lote_{hoy.isoformat()}" + (f"_{a.nombre}" if a.nombre else "")))
    if os.path.exists(carpeta) and not a.forzar:
        raise SystemExit(f"Ya existe {carpeta}: no se sobrescribe un lote preparado (use --forzar si se descartó).")
    registro = leer_registro(a.registro)
    otros = [x for x in lotes_preparados(a.carpeta) if x[0] != carpeta]
    # Una obra no se prepara dos veces: ni si está en el registro ni si ya figura en otro lote preparado.
    ya = {r["id_obra"] for r in registro} | {f["id"] for _, _, filas in otros for f in filas}
    # Tope por órgano y MES: lo ya preparado este mes en otros lotes y lo enviado este mes según el registro.
    por_organo, ids_del_mes = Counter(), set()
    for _, fecha, filas in otros:
        if fecha[:7] == mes:
            for f in filas:
                por_organo[f["organo_id"] or f["organo"]] += 1
                ids_del_mes.add(f["id"])
    for r in registro:
        if (r.get("fecha_envio") or "")[:7] == mes and r["id_obra"] not in ids_del_mes:
            por_organo[r.get("organo_id", "")] += 1
    ya_del_mes = sum(por_organo.values())
    with open(PLANTILLA, encoding="utf-8") as fh:
        plantilla = fh.read()
    with open(a.obras, encoding="utf-8") as fh:
        obras = list(csv.DictReader(fh))
    candidatas, motivos, motivo_de = [], Counter(), {}
    for r in obras:
        p = num(r["presupuesto_sin_iva"])
        motivo = ""
        if r["estado"] not in ("ADJ", "RES") or not r["fecha_adjudicacion"]:
            motivo = "no adjudicada o sin resultado"
        elif not r["fin_teorico"]:
            motivo = "sin fin teórico estimable"
        elif r["fin_definitivo"] == "True":
            motivo = "ya consta un indicador de fin"
        elif p is None or p < a.min or (a.max and p > a.max):
            motivo = "fuera del tramo de importe"
        elif date.fromisoformat(r["fin_teorico"]) + timedelta(days=a.margen) > hoy:
            motivo = "aún no toca preguntar"
        elif a.desde and date.fromisoformat(r["fin_teorico"]) + timedelta(days=a.margen) < date.fromisoformat(a.desde):
            motivo = "fecha de pregunta anterior a --desde"
        if motivo:
            motivos[motivo] += 1
            motivo_de[r["id"]] = motivo
        else:
            r["fecha_pregunta"] = (date.fromisoformat(r["fin_teorico"]) + timedelta(days=a.margen)).isoformat()
            candidatas.append(r)
    # Señal «terminación licitada de nuevo» (senal_terminacion.py): se calcula para todas las candidatas y se anota
    # en el lote. Con --prioridad terminacion, las marcadas van primero; por defecto, el orden es la antigüedad.
    indice = st.Indice(obras)
    for r in candidatas:
        r["senal_terminacion"] = indice.terminacion(r) or ""
        r["regimen"] = rgm.clave(r.get("tipo_administracion", ""), r.get("ccaa_organo", ""))
    # Primero las que llevan más tiempo esperando; a igualdad, las de mayor importe.
    orden = lambda r: (r["fecha_pregunta"], -(num(r["presupuesto_sin_iva"]) or 0))  # noqa: E731
    if a.prioridad == "terminacion":
        base_orden = orden
        orden = lambda r: (not r["senal_terminacion"], *base_orden(r))  # noqa: E731
    candidatas.sort(key=lambda r: (orden(r), r["id"]))
    muestra, marco = None, None
    if a.lista:
        # Una lista fija (p. ej. la muestra.csv de un lote anterior): solo esas obras.
        with open(a.lista, encoding="utf-8") as fh:
            marco = [r["id"] for r in csv.DictReader(fh)]
        fijas = set(marco)
        motivos["fuera de la lista fija"] = sum(r["id"] not in fijas for r in candidatas)
        candidatas = [r for r in candidatas if r["id"] in fijas]
    elif a.muestra:
        # Muestra aleatoria simple y reproducible: el marco se ordena por id ANTES de sortear (así no depende de la
        # prioridad elegida) y se sortea ANTES de quitar las obras ya registradas. Si hay N o menos candidatas, la
        # muestra son todas. Se guarda siempre en muestra.csv (aunque esté vacía), con el marco y sus parámetros en
        # marco_muestra.json: los meses siguientes se completa con --lista, sin volver a sortear.
        marco_ids = sorted(r["id"] for r in candidatas)
        por_id = {r["id"]: r for r in candidatas}
        sorteadas = random.Random(a.semilla).sample(marco_ids, min(a.muestra, len(marco_ids)))
        candidatas = sorted((por_id[i] for i in sorteadas), key=lambda r: (orden(r), r["id"]))
        muestra = list(candidatas)
        marco = [r["id"] for r in muestra]
        marco_muestra = {"fecha": hoy.isoformat(), "semilla": a.semilla, "n_pedida": a.muestra, "n_marco": len(marco_ids),
                         "n_muestra": len(marco), "parametros": {"min": a.min, "max": a.max, "margen": a.margen},
                         "sha256_marco": hashlib.sha256("\n".join(marco_ids).encode()).hexdigest()}
    motivos["ya en el registro o en otro lote preparado"] = sum(r["id"] in ya for r in candidatas)
    candidatas = [r for r in candidatas if r["id"] not in ya]
    lote, aplazadas = [], set()
    for r in candidatas:
        clave = r["organo_id"] or r["organo"]
        if a.tope and por_organo[clave] >= a.tope:
            aplazadas.add(r["id"])
            continue
        por_organo[clave] += 1
        lote.append(r)

    os.makedirs(os.path.join(carpeta, "solicitudes"), exist_ok=True)
    campos = ["n", "id", "enlace", "expediente", "titulo", "organo", "organo_id", "ccaa_organo", "ambito", "garante",
              "garante_estado", "regimen", "presupuesto_sin_iva", "fecha_adjudicacion", "fin_teorico", "fecha_pregunta",
              "senal_terminacion", "fichero_solicitud"]
    with open(os.path.join(carpeta, "parametros.json"), "w", encoding="utf-8") as f:
        json.dump({"fecha": hoy.isoformat(), "tope": a.tope, "justificacion_tope": a.justificacion_tope, "min": a.min,
                   "max": a.max, "margen": a.margen, "prioridad": a.prioridad, "muestra": a.muestra, "semilla": a.semilla,
                   "lista": os.path.basename(a.lista) if a.lista else "", "desde": a.desde}, f, ensure_ascii=False, indent=2)
    if marco is not None:
        # Seguimiento del marco muestral congelado: el denominador no cambia sin constancia (pérdidas y exclusiones).
        en_lote = {r["id"] for r in lote}
        with open(os.path.join(carpeta, "seguimiento_muestra.csv"), "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["id", "estado"])
            for i in marco:
                estado = ("en este lote" if i in en_lote else "ya en el registro o en otro lote" if i in ya
                          else "aplazada por el tope" if i in aplazadas
                          else f"excluida: {motivo_de[i]}" if i in motivo_de else "no encontrada en los datos")
                w.writerow([i, estado])
    if muestra is not None:
        with open(os.path.join(carpeta, "muestra.csv"), "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["id", "enlace", "fecha_pregunta", "presupuesto_sin_iva"], extrasaction="ignore")
            w.writeheader()
            w.writerows(muestra)
        with open(os.path.join(carpeta, "marco_muestra.json"), "w", encoding="utf-8") as f:
            json.dump(marco_muestra, f, ensure_ascii=False, indent=2)
        print(f"Muestra completa ({len(muestra)} de {marco_muestra['n_marco']} candidatas, semilla {a.semilla}) guardada en "
              "muestra.csv; complétela los meses siguientes con --lista")
    with open(os.path.join(carpeta, "lote.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campos, extrasaction="ignore")
        w.writeheader()
        for i, r in enumerate(lote, 1):
            nombre = f"{i:04d}.txt"
            r.update(n=i, fichero_solicitud=nombre, garante_estado="sugerido, sin verificar")
            w.writerow(r)
            texto = plantilla.format(organo=r["organo"] or "[órgano de contratación]", expediente=r["expediente"] or "[sin número]",
                                     titulo=r["titulo"] or "[sin título]", enlace=r["enlace"] or "[sin enlace]")
            with open(os.path.join(carpeta, "solicitudes", nombre), "w", encoding="utf-8") as fh:
                fh.write(texto)
    print(f"Fecha {hoy}; margen {a.margen} días; importe {a.min:,.0f}–{a.max or '∞'} €; tope por órgano y mes {a.tope}"
          + (f" (justificación: {a.justificacion_tope})" if a.justificacion_tope else ""))
    for k, v in motivos.most_common():
        print(f"  descartadas: {k}: {v}")
    print(f"Candidatas: {len(candidatas)}; en el lote: {len(lote)}; aplazadas por el tope: {len(aplazadas)}; "
          f"órganos distintos: {len({r['organo_id'] or r['organo'] for r in lote})}; "
          f"ya preparadas o enviadas este mes antes de este lote: {ya_del_mes}")
    print("Por órgano de garantía: " + "; ".join(f"{k}: {v}" for k, v in Counter(r["garante"] for r in lote).most_common()))
    print(f"Con coincidencia «terminación licitada de nuevo» (senal_terminacion.py; una marca obliga a verificar, su "
          f"ausencia no informa): "
          f"{sum(bool(r['senal_terminacion']) for r in lote)} en el lote, {sum(bool(r['senal_terminacion']) for r in candidatas)} "
          f"entre las candidatas; prioridad: {a.prioridad}")
    print(f"Carpeta: {carpeta}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="orden", required=True)
    e = sub.add_parser("escanear")
    e.add_argument("--datos", default=DATOS, help="patrones glob de los ZIP, separados por el separador de rutas del sistema")
    e.add_argument("--salida", default=os.path.join(AQUI, "obras_protocolo.csv"))
    s = sub.add_parser("seleccionar")
    s.add_argument("--obras", default=os.path.join(AQUI, "obras_protocolo.csv"))
    s.add_argument("--registro", default=os.path.join(AQUI, "registro.csv"))
    s.add_argument("--fecha", default=date.today().isoformat())
    s.add_argument("--margen", type=int, default=120, help="días tras el fin teórico (recepción + certificación final)")
    s.add_argument("--min", type=float, default=1_000_000, help="presupuesto base sin IVA mínimo")
    s.add_argument("--max", type=float, default=0, help="presupuesto base sin IVA máximo (0 = sin máximo)")
    s.add_argument("--tope", type=int, default=4, help="solicitudes como máximo por órgano y MES, sumando los lotes del mes "
                   "en --carpeta y los envíos del mes en el registro (de 1 a 4; más, solo con --justificacion-tope)")
    s.add_argument("--justificacion-tope", default="", help="motivo de un tope mayor que 4; queda escrito en parametros.json")
    s.add_argument("--forzar", action="store_true", help="rehacer un lote que ya existe (si se descartó sin enviar)")
    s.add_argument("--prioridad", choices=["antiguedad", "terminacion"], default="antiguedad",
                   help="orden cuando el tope obliga a aplazar: antigüedad (por defecto) o primero las obras con señal de "
                        "posible terminación anticipada (ver SENAL_TERMINACION.md)")
    s.add_argument("--desde", default="", help="solo obras cuya fecha de pregunta es igual o posterior (flujo reciente)")
    s.add_argument("--muestra", type=int, default=0, help="muestra aleatoria de N candidatas (0 = todas)")
    s.add_argument("--semilla", type=int, default=20261101, help="semilla de la muestra, para poder repetirla")
    s.add_argument("--lista", default="", help="CSV con columna id: limita la selección a esas obras (p. ej. muestra.csv)")
    s.add_argument("--nombre", default="", help="sufijo de la carpeta del lote (p. ej. «muestra»)")
    s.add_argument("--carpeta", default=AQUI)
    a = ap.parse_args()
    cmd_escanear(a) if a.orden == "escanear" else cmd_seleccionar(a)


if __name__ == "__main__":
    main()
