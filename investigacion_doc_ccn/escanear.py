"""Estado final de cada expediente del corpus, con la MISMA política de versiones que el estudio
(medir_ejecucion.py v2.3): última `updated`, versiones empatadas resueltas con elegir_principal(),
borrados ANULADA o sin tipo posteriores o iguales a la última versión excluidos. De este único
recorrido salen el denominador (todas las obras) y la lista de expedientes con DOC_CCN vigente,
así que ambos usan el mismo estado de cada expediente.

Uso: python escanear.py [--datos "RUTA/*/licitacionesPerfilesContratanteCompleto3_*.zip"] [--salida .]
Salidas: obras_estado_final.csv (obras, código 3) y ccn_todos_tipos.csv (cualquier tipo con DOC_CCN).
"""
import argparse
import csv
import glob
import os
import sys
import xml.etree.ElementTree as ET
import zipfile
from concurrent.futures import ProcessPoolExecutor

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "fase0_placsp"))
import medir_ejecucion as me  # noqa: E402

CAMPOS_OBRA = ["id", "enlace", "actualizado", "estado", "organo_id", "tipo_administracion",
               "presupuesto_sin_iva", "fecha_adjudicacion", "n_resultados_adjudicados", "fecha_inicio",
               "duracion_final_dias", "fin_teorico", "anuncio_finalizacion", "n_anuncios_finalizacion",
               "n_anulaciones_finalizacion", "fecha_anuncio_finalizacion", "n_modificaciones"]
CAMPOS_REDUCIDOS = ["tipo_contrato", "estado", "organo_id", "anuncio_finalizacion", "n_anuncios_finalizacion",
                    "n_anulaciones_finalizacion", "fecha_anuncio_finalizacion", "fecha_adjudicacion",
                    "n_documentos"]


def extraer_cualquier_tipo(entry):
    """extraer() del estudio para cualquier tipo de contrato. Las obras conservan el registro completo
    (para que elegir_principal() decida exactamente igual que el estudio); el resto, uno reducido."""
    cfs = me.child(entry, "ContractFolderStatus")
    proy = me.child(cfs, "ProcurementProject") if cfs is not None else None
    tipo = me.text(me.child(proy, "TypeCode")) if proy is not None else ""
    me.TIPO_CONTRATO = tipo
    ident, act, exp = me.extraer(entry)
    if exp is None:
        return ident, act, None
    d = me.asdict(exp)
    if tipo != "3":
        d = {k: d[k] for k in CAMPOS_REDUCIDOS}
    return ident, act, d


def procesar(args):
    ruta, nombre = args
    versiones, borrados = [], []
    with zipfile.ZipFile(ruta) as z, z.open(nombre) as f:
        for _e, el in ET.iterparse(f, events=("end",)):
            if el.tag == me.ATOM + "entry":
                versiones.append(extraer_cualquier_tipo(el))
                el.clear()
            elif el.tag == me.TOMBSTONE:
                c = el.find(me.TOMBSTONE_NS + "comment")
                tipo = (c.get("type", "") if c is not None else "") or "SIN_TIPO"
                borrados.append((el.get("ref", ""), el.get("when", ""), tipo.upper()))
                el.clear()
    return versiones, borrados


def acumular(resultados):
    """Igual que medir(): id -> (fecha máxima, versiones distintas con esa fecha) y último borrado."""
    ultima, borrados = {}, {}
    for versiones, bs in resultados:
        for ident, actualizado, c in versiones:
            t = me.fecha(actualizado)
            previa = ultima.get(ident)
            if previa is None or t > previa[0]:
                ultima[ident] = (t, [c])
            elif t == previa[0] and c not in previa[1]:
                previa[1].append(c)
        for ref, when, tipo in bs:
            t = me.fecha(when)
            if ref not in borrados or t > borrados[ref][0]:
                borrados[ref] = (t, tipo)
    return ultima, borrados


def estados_finales(ultima, borrados):
    """Devuelve (estados, excluidos). Cada estado lleva la versión principal y, si hubo empate,
    si las versiones empatadas discrepan sobre el anuncio de finalización (para dar cotas)."""
    estados, excluidos = [], 0
    for ident, (t, versiones) in ultima.items():
        validas = [v for v in versiones if v is not None]
        if not validas:
            continue
        if ident in borrados and borrados[ident][0] >= t and borrados[ident][1] in ("ANULADA", "SIN_TIPO"):
            excluidos += 1
            continue
        principal = dict(me.elegir_principal(validas))
        principal["id"] = ident
        principal["n_versiones_empatadas"] = len(versiones)
        principal["ccn_discrepa_en_empate"] = len({bool(v["anuncio_finalizacion"]) for v in validas}) > 1
        estados.append(principal)
    return estados, excluidos


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--datos", default=os.path.join(AQUI, "..", "datos", "placsp_2023", "*.zip") + os.pathsep +
                    os.path.join(AQUI, "..", "datos", "placsp_posteriores", "*.zip"),
                    help="patrones glob de los ZIP, separados por el separador de rutas del sistema")
    ap.add_argument("--salida", default=AQUI)
    a = ap.parse_args()
    zips = sorted(z for patron in a.datos.split(os.pathsep) for z in glob.glob(patron))
    trabajos = [(r, n) for r in zips for n in sorted(zipfile.ZipFile(r).namelist()) if n.endswith(".atom")]
    print(len(zips), "ZIP,", len(trabajos), "ficheros ATOM", flush=True)
    with ProcessPoolExecutor() as ex:
        ultima, borrados = acumular(ex.map(procesar, trabajos, chunksize=4))
    estados, excluidos = estados_finales(ultima, borrados)

    obras = [e for e in estados if e.get("tipo_contrato") == "3"]
    with open(os.path.join(a.salida, "obras_estado_final.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS_OBRA + ["doc_resolucion", "doc_fin_ordinario",
                                                        "n_versiones_empatadas", "ccn_discrepa_en_empate"])
        w.writeheader()
        for e in obras:
            docs = e["documentos_ejecucion"]
            fila = {k: e[k] for k in CAMPOS_OBRA}
            fila["doc_resolucion"] = bool(docs.get("resolucion_contrato"))
            fila["doc_fin_ordinario"] = any(docs.get(c) for c in ("recepcion_definitiva", "liquidacion",
                                                                  "certificacion_final", "final_obra",
                                                                  me.CATEGORIA_NOTA))
            fila["n_versiones_empatadas"] = e["n_versiones_empatadas"]
            fila["ccn_discrepa_en_empate"] = e["ccn_discrepa_en_empate"]
            w.writerow(fila)
    ccn = [e for e in estados if e["n_anuncios_finalizacion"] or e["n_anulaciones_finalizacion"]]
    with open(os.path.join(a.salida, "ccn_todos_tipos.csv"), "w", newline="", encoding="utf-8") as f:
        campos = ["id"] + CAMPOS_REDUCIDOS + ["n_versiones_empatadas", "ccn_discrepa_en_empate"]
        w = csv.DictWriter(f, fieldnames=campos, extrasaction="ignore")
        w.writeheader()
        w.writerows(ccn)
    print(f"expedientes: {len(estados)} (excluidos por borrado: {excluidos}); obras: {len(obras)}; "
          f"con DOC_CCN o ANUL_CCN en su estado final: {len(ccn)}, de ellos obras: "
          f"{sum(e.get('tipo_contrato') == '3' for e in ccn)}; empates que discrepan sobre DOC_CCN: "
          f"{sum(e['ccn_discrepa_en_empate'] for e in estados)}")


if __name__ == "__main__":
    main()
