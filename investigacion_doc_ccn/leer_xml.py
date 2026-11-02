"""Lee los XML ContractCompletionNotice descargados: una fila por contrato (TenderResult/Contract).
Sustituye a leer_ccn.py (revisión adversarial de ChatGPT, puntos D, E, G y J).

Uso: python -I leer_xml.py [--xml xml_anuncios] [--obras obras_estado_final.csv] [--salida contratos_ccn.csv]
Escribe también manifiesto_xml.csv (huella, tamaño y validez de cada XML).
No extrae datos de los adjudicatarios (WinningParty).
"""
import argparse
import csv
import hashlib
import json
import os
import xml.etree.ElementTree as ET
from datetime import date

DIAS_POR_UNIDAD = {"DAY": 1.0, "WEE": 7.0, "MON": 30.44, "ANN": 365.25}   # como medir_ejecucion.py


def local(t): return t.rsplit("}", 1)[-1]
def hijos(el, n): return [c for c in el if local(c.tag) == n] if el is not None else []
def hijo(el, n):
    for c in (el if el is not None else []):
        if local(c.tag) == n:
            return c
def txt(el): return (el.text or "").strip() if el is not None else ""
def ruta(el, *ns):
    for n in ns:
        el = hijo(el, n)
    return el
def dia(s):
    try:
        return date.fromisoformat(s[:10])   # día tal como figura en la fuente; se ignora el desfase horario
    except ValueError:
        return None
def num(s):
    try:
        return float(s)
    except ValueError:
        return None
def dias(el):
    v, f = num(txt(el)), DIAS_POR_UNIDAD.get(el.get("unitCode", "")) if el is not None else None
    return round(v * f) if v is not None and f else None


def duracion_prevista(raiz):
    pp = ruta(raiz, "ProcurementProject", "PlannedPeriod")
    d = dias(hijo(pp, "DurationMeasure"))
    if d is None and dia(txt(hijo(pp, "StartDate"))) and dia(txt(hijo(pp, "EndDate"))):
        d = (dia(txt(hijo(pp, "EndDate"))) - dia(txt(hijo(pp, "StartDate")))).days
    return d


def main():
    ap = argparse.ArgumentParser()
    aqui = os.path.dirname(os.path.abspath(__file__))
    ap.add_argument("--xml", default=os.path.join(aqui, "xml_anuncios"))
    ap.add_argument("--obras", default=os.path.join(aqui, "obras_estado_final.csv"))
    ap.add_argument("--salida", default=os.path.join(aqui, "contratos_ccn.csv"))
    a = ap.parse_args()
    obras = {r["id"]: r for r in csv.DictReader(open(a.obras, encoding="utf-8"))}

    ultimo = {}   # última pasada de cada expediente (las anteriores pudieron terminar en error)
    for linea in open(os.path.join(a.xml, "_registro.jsonl"), encoding="utf-8"):
        reg = json.loads(linea)
        ultimo[reg["id"]] = reg
    manifiesto, filas = [], []
    for reg in ultimo.values():
        e = obras.get(reg["id"], {})
        for anuncio in reg["anuncios"]:
            fichero = anuncio.get("fichero")
            if not fichero:
                manifiesto.append({"id": reg["id"], "fichero": "", "estado": anuncio.get("error", "sin enlace"),
                                   "texto_web": anuncio.get("texto", "")})
                continue
            p = os.path.join(a.xml, fichero)
            datos = open(p, "rb").read()
            m = {"id": reg["id"], "fichero": fichero, "bytes": len(datos),
                 "sha256": hashlib.sha256(datos).hexdigest(), "texto_web": anuncio.get("texto", "")}
            try:
                raiz = ET.fromstring(datos)
            except ET.ParseError as err:
                m["estado"] = f"XML no válido: {err}"
                manifiesto.append(m)
                continue
            m["estado"] = "ok" if local(raiz.tag) == "ContractCompletionNotice" else f"raíz inesperada {local(raiz.tag)}"
            m["anuncio_id"] = txt(hijo(raiz, "ID"))
            manifiesto.append(m)
            fecha_anuncio = txt(hijo(raiz, "IssueDate"))[:10]
            prevista_inicial = duracion_prevista(raiz)
            # Modificaciones por contrato: la de número más alto con duración o importe final.
            mods = {}
            for mod in hijos(raiz, "ContractModification"):
                mods.setdefault(txt(hijo(mod, "ContractID")), []).append(mod)
            for tr in hijos(raiz, "TenderResult"):
                c = hijo(tr, "Contract")
                if c is None:
                    continue
                cid = txt(hijo(c, "ID"))
                propias = sorted(mods.get(cid, []), key=lambda x: num(txt(hijo(x, "ID"))) or 0)
                prevista_final, final_sin, final_con = prevista_inicial, None, None
                for mod in propias:
                    if dias(hijo(mod, "FinalDurationMeasure")) is not None:
                        prevista_final = dias(hijo(mod, "FinalDurationMeasure"))
                    flm = hijo(mod, "FinalLegalMonetaryTotal")
                    if flm is not None:
                        final_sin = num(txt(hijo(flm, "TaxExclusiveAmount")))
                        final_con = num(txt(hijo(flm, "PayableAmount")))
                ini, fin = dia(txt(ruta(c, "ActualDurationPeriod", "StartDate"))), dia(txt(ruta(c, "ActualDurationPeriod", "EndDate")))
                real = (fin - ini).days if ini and fin else None
                ct = hijo(c, "ContractTermination")
                motivo = hijo(ct, "TerminationReasonCode")
                lmt = ruta(tr, "AwardedTenderedProject", "LegalMonetaryTotal")
                agg = hijo(c, "AggregatedAmount")
                ft = dia(e.get("fin_teorico", ""))
                filas.append({
                    "id": reg["id"], "fichero": fichero, "anuncio_id": m["anuncio_id"], "fecha_anuncio": fecha_anuncio,
                    "contrato_id": cid, "lote": txt(ruta(tr, "AwardedTenderedProject", "ProcurementProjectLotID")),
                    "organo_id": e.get("organo_id", ""), "fecha_adjudicacion": e.get("fecha_adjudicacion", ""),
                    "en_estado_final_con_ccn": e.get("anuncio_finalizacion", "") == "True",
                    "inicio_real": ini.isoformat() if ini else "", "fin_real": fin.isoformat() if fin else "",
                    "duracion_real_dias": real if real is not None else "",
                    "duracion_prevista_inicial_dias": prevista_inicial if prevista_inicial is not None else "",
                    "duracion_prevista_final_dias": prevista_final if prevista_final is not None else "",
                    "dif_duracion_dias": real - prevista_final if real is not None and prevista_final is not None else "",
                    "n_modificaciones_contrato": len(propias),
                    "n_suspensiones": len(hijos(c, "SuspensionPeriod")),
                    "prorrogas_numero": txt(ruta(c, "ContractExtension", "NumberNumeric")),
                    "fin_teorico_expediente": e.get("fin_teorico", ""),
                    "dif_fin_teorico_expediente_dias": (fin - ft).days if fin and ft else "",
                    "dias_fin_a_anuncio": (dia(fecha_anuncio) - fin).days if fin and dia(fecha_anuncio) else "",
                    "terminacion_presente": ct is not None,
                    "terminacion_fecha": txt(hijo(ct, "IssueDate"))[:10],
                    "causa_codigo": txt(motivo), "causa": motivo.get("name", "") if motivo is not None else "",
                    "causa_texto": txt(hijo(ct, "TerminationContractDescription"))[:300],
                    "adjudicado_sin_iva": num(txt(hijo(lmt, "TaxExclusiveAmount"))),
                    "adjudicado_con_iva": num(txt(hijo(lmt, "PayableAmount"))),
                    "final_mod_sin_iva": final_sin, "final_mod_con_iva": final_con,
                    "pagado": num(txt(hijo(agg, "PaidAmount"))),
                    "pagado_descripcion": txt(hijo(agg, "PaidAmountDescription"))[:300],
                    "penalidades": num(txt(hijo(agg, "PenaltiesAmount"))),
                    "anexos": " | ".join(txt(hijo(d, "ID")) for d in hijos(raiz, "MinutesDocumentReference")),
                })
    with open(a.salida, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0].keys()))
        w.writeheader()
        w.writerows(filas)
    campos = ["id", "fichero", "estado", "anuncio_id", "bytes", "sha256", "texto_web"]
    with open(os.path.join(os.path.dirname(a.salida), "manifiesto_xml.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campos, extrasaction="ignore")
        w.writeheader()
        w.writerows(manifiesto)
    print(f"{len(filas)} contratos; {len(manifiesto)} anuncios en el manifiesto "
          f"({sum(m['estado'] == 'ok' for m in manifiesto)} XML válidos)")


if __name__ == "__main__":
    main()
