#!/usr/bin/env python3
"""Fase 0 de «Democracia Auditable» (§8.6/§9.0): ¿qué consta de la EJECUCIÓN de
las obras públicas en la sindicación de datos abiertos de la Plataforma de
Contratación del Sector Público (PLACSP)?

Lee uno o varios ZIP de la sindicación «licitacionesPerfilesContratante» sin
descomprimirlos, se queda con la última versión de cada EXPEDIENTE (licitación;
puede contener varios lotes y contratos), aplica los criterios de selección
declarados abajo y mide si constan modificaciones y documentos CANDIDATOS a ser
de ejecución, detectados por NOMBRES DE ARCHIVO o ETIQUETAS DE TIPO DOCUMENTAL
(no por su contenido).

Solo biblioteca estándar de Python (3.11+). No usa IA ni red.
No extrae datos de adjudicatarios (pueden ser personas físicas).

Versión 2.4 (01/11/2026): lee también el texto (`Note`) de cada modificación, donde algunos órganos
comunican la liquidación o la certificación final (investigacion_modificaciones/INFORME_MODIFICACIONES.md).
Versión 2.3 (30/10/2026): anulaciones del anuncio de finalización (ANUL_CCN).
Versión 2.2: empates de `updated` tratados como incertidumbre
(sin fusionar; cotas mínima y máxima), procedencia de cada coincidencia,
categorías de fin separadas (definitivo / parcial o de avance), diagnóstico de
borrados y anexo aparte por tipo de administración.

Uso:
    python medir_ejecucion.py DATOS.zip [OTRO.zip ...] --salida resultados
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import platform
import re
import sys
import unicodedata
import zipfile
from collections import Counter, defaultdict
from concurrent.futures import ProcessPoolExecutor
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta, timezone
import xml.etree.ElementTree as ET

VERSION = "2.4"

# ---------------------------------------------------------------------------
# CRITERIOS DECLARADOS ANTES DE VER LOS RESULTADOS (no modificar sin dejar
# constancia en METODO.md y en el informe).
# ---------------------------------------------------------------------------
TIPO_CONTRATO = "3"                    # 3 = Obras (SyndicationContractCode-2.04)
ESTADOS_ADMITIDOS = {"ADJ", "RES"}     # adjudicada o resuelta (formalizada)
ANIO_ADJUDICACION = 2023               # año de la PRIMERA fecha de adjudicación
PRESUPUESTO_MIN = 1_000_000.0          # presupuesto base de licitación sin IVA del expediente, EUR
PRESUPUESTO_MAX = 10_000_000.0

TIPOS_ADMINISTRACION = {               # ContractingAuthorityCode-2.10 (la 1.04 solo tenía 1–5)
    "1": "Autoridad estatal",
    "2": "Autoridad regional",
    "3": "Autoridad local",
    "4": "Organismo de Derecho público",
    "5": "Otras Entidades del Sector Público",
    "6": "Organismo de Derecho público bajo control estatal",
    "7": "Organismo de Derecho público bajo control regional",
    "8": "Organismo de Derecho público bajo control local",
    "9": "Empresa pública bajo control estatal",
    "10": "Empresa pública bajo control regional",
    "11": "Empresa pública bajo control local",
    "12": "Entidad con derechos especiales o exclusivos",
}

# Categorías de documentos CANDIDATOS, buscadas en nombres de archivo (FileName) y en etiquetas
# de tipo documental (DocumentTypeCode@name), con texto normalizado (minúsculas, sin tildes).
# Son heurísticas: una coincidencia no acredita el contenido y una ausencia no acredita que el
# documento falte. Cada entrada: (patrón, exclusión o None).
_EXCL_RECEPCION = (r"ofert|solicit|propos|plica|participac|licitador|replanteo|adjudicac|documentacion"
                   r"|\bjust|baja\s+temer|\bbt\b")   # «recep just bt»: justificación de baja temeraria
_PATRON_RECEPCION = r"recep|acta\s+de\s+(conformidad|entrega)|entrega\s+de(l|\s+la)?\s+(obra|edificio|instalac)"
_EXCL_CERTIFICADO = r"adjudicac|eficiencia|energetic|\bmrr\b|replanteo|acuerdo|pleno|mesa"
CATEGORIAS_DOCUMENTO = {
    # --- Fin definitivo de la obra o del contrato ---
    "recepcion_definitiva": (re.compile(_PATRON_RECEPCION), re.compile(_EXCL_RECEPCION + r"|parcial")),
    "liquidacion": (re.compile(r"liquidac"), re.compile(r"icio|tasa|impuesto|tribut|penalidad|penalizac|sancion")),
    "certificacion_final": (re.compile(r"certificaci\w*\s+final|certificado\s+final|\bcfo\b|medicion\s+general"),
                            re.compile(_EXCL_CERTIFICADO)),
    "final_obra": (re.compile(r"(fin|final|terminacion)\s+de\s+(las?\s+)?obras?"), None),
    # Extinción anticipada (art. 211 LCSP). Excluye trámites iniciales o propuestas.
    "resolucion_contrato": (re.compile(r"resoluci\w*\s+(del?\s+)?(contrato|contracte)|extinci\w*\s+del\s+contrato"),
                            re.compile(r"adjudicac|clasificac|licitac|\binici|propuesta")),
    # --- Fin parcial, avance o trámite no concluido (no cuentan como fin definitivo) ---
    "recepcion_parcial": (re.compile(r"recep\w*\s+parcial|parcial\w*.*recep"), re.compile(_EXCL_RECEPCION)),
    "certificacion_avance": (re.compile(
        r"certificaci(on|ones)\s*(de\s*)?(la\s*)?(obra|mensual|ordinaria|parcial|economica|n[o.º]?\s*\d|\d)"
        r"|certif\.?\s*(de\s*)?obra|\bcert\.?\s*(n[o.º]?\.?\s*)?\d|\bcert\.\s"),
        re.compile(_EXCL_CERTIFICADO + r"|final")),
    "resolucion_en_tramite": (re.compile(r"(\binici\w*|propuesta)\b.*resoluci\w*\s+(del?\s+)?(contrato|contracte)"
                                         r"|resoluci\w*\s+(del?\s+)?(contrato|contracte).*(\binici|propuesta)"), None),
    "devolucion_garantia": (re.compile(r"devoluci\w*.*garant|cancelaci\w*.*garant|garant\w*.*devol"),
                            re.compile(r"provisional")),
    # --- Incidencias durante la obra ---
    "documento_modificacion": (re.compile(r"modific"),
                               re.compile(r"apertura|oferta|presentacion|pliego|pptp|pcap|solvencia|"
                                          r"clasificacion|anuncio|licitacion|fecha|ordenanza")),
    "documento_prorroga": (re.compile(r"prorrog"), None),
    "ampliacion_plazo": (re.compile(r"ampliac\w*\s+(del?\s+)?(plazo|termini)"),   # «termini»: catalán
                         re.compile(r"ofert|presentac|licitac|solicitud|proposic")),
    "suspension": (re.compile(r"suspensi"), re.compile(r"ofert|licitac|procedimiento|plazo de present")),
    "cesion_contrato": (re.compile(r"\bcesion\b"), None),
}
# Fin comunicado en el texto (`Note`) de una modificación publicada (v2.4, endurecido tras la revisión adversarial).
# Dos niveles: «confirmado» solo si el texto COMPLETO es una fórmula breve de una lista cerrada (es el que cuenta como fin;
# los 24 casos de la cohorte de 2023 se revisaron a mano: revision_manual_fin_en_nota_v2_4.csv); «candidato» si coincide
# un patrón amplio (se anota para revisión y no cuenta como fin).
FIN_EN_NOTA = re.compile(r"(se (formaliza|procede a|firma) )?(la )?liquidacion( final)?( del contrato| de (la )?obra)?"
                         r"|(pago )?certificacion final( de (la )?obra| del contrato| obra)?"
                         r"|certificacion final y liquidacion( de (la )?obra)?")
CANDIDATO_EN_NOTA = re.compile(r"liquidaci|certificaci\w*\s+final|acta\s+de\s+recepci|recepci\w*\s+(de\s+(la|las)\s+obras?|definitiva)")
EXCL_FIN_EN_NOTA = re.compile(r"parcial|danos|perjuicio|penalidad|anticipo|provisional|fase|a cuenta|lote")


def fin_en_nota(nota: str) -> str:
    """'confirmado', 'candidato' o '' según el texto de una modificación."""
    n = re.sub(r"\s+", " ", normalizar(nota)).strip().rstrip(".").strip()
    if not n or EXCL_FIN_EN_NOTA.search(n):
        return ""
    if FIN_EN_NOTA.fullmatch(n):
        return "confirmado"
    return "candidato" if CANDIDATO_EN_NOTA.search(n) else ""


CATEGORIA_NOTA = "fin_en_nota_modificacion"
CATEGORIA_NOTA_CANDIDATO = "fin_en_nota_candidato"   # no cuenta como fin
CATEGORIAS_SALIDA = list(CATEGORIAS_DOCUMENTO) + [CATEGORIA_NOTA, CATEGORIA_NOTA_CANDIDATO]   # columnas y filas de los informes
DOCS_FIN_DEFINITIVO = {"recepcion_definitiva", "liquidacion", "certificacion_final", "final_obra", "resolucion_contrato",
                       CATEGORIA_NOTA}
DOCS_FIN_PARCIAL = {"recepcion_parcial", "certificacion_avance", "resolucion_en_tramite"}
DOCS_DURANTE = {"documento_modificacion", "documento_prorroga", "ampliacion_plazo", "suspension", "cesion_contrato"}

# Códigos de resultado que significan adjudicación (TenderResultCode 2.02/2.09). Se excluyen
# desierto (3, 6, 7), desistimiento (4), renuncia (5) y «mejor valorado» (10).
RESULTADOS_ADJUDICADOS = {"1", "2", "8", "9"}

ATOM = "{http://www.w3.org/2005/Atom}"
TOMBSTONE_NS = "{http://purl.org/atompub/tombstones/1.0}"
TOMBSTONE = TOMBSTONE_NS + "deleted-entry"


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def children(el, name):
    return [c for c in el if local(c.tag) == name]


def child(el, name):
    for c in el:
        if local(c.tag) == name:
            return c
    return None


def text(el) -> str:
    return (el.text or "").strip() if el is not None else ""


def normalizar(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[_\-]+", " ", s.lower())


def a_float(s: str) -> float | None:
    try:
        return float(s)
    except (TypeError, ValueError):
        return None


def clasificar_documento(nombre: str) -> set[str]:
    n = normalizar(nombre)
    encontradas = set()
    for categoria, (patron, exclusion) in CATEGORIAS_DOCUMENTO.items():
        if patron.search(n) and not (exclusion and exclusion.search(n)):
            encontradas.add(categoria)
    return encontradas


@dataclass
class Expediente:
    id: str
    enlace: str
    expediente: str
    organo: str
    organo_id: str
    tipo_administracion: str
    estado: str
    actualizado: str
    tipo_contrato: str
    presupuesto_sin_iva: float | None
    fecha_adjudicacion: str          # la primera fecha de un resultado adjudicado
    fecha_adjudicacion_cualquiera: str   # la primera fecha de cualquier resultado (para la tabla de exclusiones)
    importe_adjudicado_sin_iva: float | None
    formalizado: bool
    duracion_prevista: str
    prorroga_prevista_texto: bool
    n_modificaciones: int
    anuncio_modificacion: bool
    n_documentos: int
    anuncio_finalizacion: bool = False         # anuncio estructurado DOC_CCN vigente (no anulado)
    fecha_anuncio_finalizacion: str = ""
    n_anuncios_finalizacion: int = 0           # DOC_CCN publicados
    n_anulaciones_finalizacion: int = 0        # ANUL_CCN publicados
    n_resultados: int = 0
    n_resultados_adjudicados: int = 0
    codigos_resultado: str = ""      # TenderResultCode de cada resultado (lotes), separados por comas
    fecha_inicio: str = ""           # inicio de ejecución; si falta, formalización; si falta, adjudicación
    duracion_final_dias: float | None = None   # tras la última modificación publicada, si la hay
    fin_teorico: str = ""            # estimado; en expedientes con varios resultados puede mezclar lotes
    borrado_tipo: str = ""           # "", CERRADA, ANULADA o SIN_TIPO (at:deleted-entry posterior)
    n_versiones_empatadas: int = 1   # versiones distintas con la misma `updated` máxima
    # categoría -> lista de «nombre ⟨origen·sección⟩»; origen = archivo (FileName) o etiqueta (DocumentTypeCode@name)
    documentos_ejecucion: dict[str, list[str]] = field(default_factory=dict)


DIAS_POR_UNIDAD = {"DAY": 1.0, "WEE": 7.0, "MON": 30.44, "ANN": 365.25}
DURACION_MAX_DIAS = 50 * 365.25   # duraciones mayores se tratan como error de datos: plazo no estimable


def a_dias(el) -> float | None:
    v = a_float(text(el)) if el is not None else None
    factor = DIAS_POR_UNIDAD.get(el.get("unitCode", "")) if el is not None else None
    return v * factor if v is not None and factor else None


def fecha_dia(s: str):
    try:
        return datetime.strptime(s[:10], "%Y-%m-%d").date()
    except ValueError:
        return None


def extraer(entry) -> tuple[str, str, Expediente | None]:
    """Devuelve (id, fecha_actualización, expediente|None). None si no es de obras."""
    ident = text(child(entry, "id"))
    actualizado = text(child(entry, "updated"))
    cfs = child(entry, "ContractFolderStatus")
    if cfs is None:
        return ident, actualizado, None
    proyecto = child(cfs, "ProcurementProject")
    tipo = text(child(proyecto, "TypeCode")) if proyecto is not None else ""
    if tipo != TIPO_CONTRATO:
        return ident, actualizado, None

    enlace_el = child(entry, "link")
    parte = child(cfs, "LocatedContractingParty")
    party = child(parte, "Party") if parte is not None else None
    nombre_organo = ""
    organo_id = ""
    if party is not None:
        pn = child(party, "PartyName")
        nombre_organo = text(child(pn, "Name")) if pn is not None else ""
        pid = child(party, "PartyIdentification")
        organo_id = text(child(pid, "ID")) if pid is not None else ""

    presupuesto = None
    duracion = ""
    duracion_dias = None
    periodo_inicio = periodo_fin = ""
    prorroga_texto = False
    if proyecto is not None:
        ba = child(proyecto, "BudgetAmount")
        presupuesto = a_float(text(child(ba, "TaxExclusiveAmount"))) if ba is not None else None
        pp = child(proyecto, "PlannedPeriod")
        if pp is not None:
            dm = child(pp, "DurationMeasure")
            if dm is not None:
                duracion = f"{text(dm)} {dm.get('unitCode', '')}".strip()
                duracion_dias = a_dias(dm)
            periodo_inicio = text(child(pp, "StartDate"))
            periodo_fin = text(child(pp, "EndDate"))
        ext = child(proyecto, "ContractExtension")
        prorroga_texto = ext is not None and any(text(d) for d in ext.iter())

    fechas_adj = []
    fechas_cualquiera = []
    inicios = []
    formalizaciones = []
    importe_adj = 0.0
    hay_importe = False
    formalizado = False
    codigos_resultado = []
    for tr in children(cfs, "TenderResult"):
        codigo = text(child(tr, "ResultCode"))
        codigos_resultado.append(codigo)
        f = text(child(tr, "AwardDate"))
        if f:
            fechas_cualquiera.append(f)
            if codigo in RESULTADOS_ADJUDICADOS:
                fechas_adj.append(f)
        if text(child(tr, "StartDate")):
            inicios.append(text(child(tr, "StartDate")))
        atp = child(tr, "AwardedTenderedProject")
        lmt = child(atp, "LegalMonetaryTotal") if atp is not None else None
        v = a_float(text(child(lmt, "TaxExclusiveAmount"))) if lmt is not None else None
        if v is not None:
            importe_adj += v
            hay_importe = True
        c = child(tr, "Contract")
        if c is not None and text(child(c, "IssueDate")):
            formalizado = True
            formalizaciones.append(text(child(c, "IssueDate")))

    # Duración tras la última modificación publicada (la de número más alto).
    modificaciones = children(cfs, "ContractModification")
    duracion_final = duracion_dias
    for mod in sorted(modificaciones, key=lambda x: a_float(text(child(x, "ID"))) or 0):
        d = a_dias(child(mod, "FinalDurationMeasure"))
        if d is not None:
            duracion_final = d

    inicio = periodo_inicio or min(inicios or formalizaciones or fechas_adj or [""])
    fin = ""
    if periodo_fin and not modificaciones:
        fin = periodo_fin[:10]
    elif fecha_dia(inicio) and duracion_final is not None and 0 < duracion_final <= DURACION_MAX_DIAS:
        fin = (fecha_dia(inicio) + timedelta(days=round(duracion_final))).isoformat()

    avisos = {text(child(v, "NoticeTypeCode")) for v in children(cfs, "ValidNoticeInfo")}
    # Anuncio de Finalización de Contrato (DOC_CCN, TenderingNoticeTypeCode 2.11). No figura en la
    # especificación de sindicación v1.10 (17/09/2024); se descubrió en la revisión manual v2.2. La
    # sindicación solo trae el tipo y la fecha; el detalle (fecha real de fin, causa de extinción)
    # está en el documento ContractCompletionNotice enlazado desde la web.
    # La lista 2.11 incluye también ANUL_CCN (anulación de un anuncio de finalización). Se considera
    # vigente si hay más anuncios que anulaciones (una anulación retira un anuncio; uno publicado
    # después vuelve a contar). La sindicación no indica a qué contrato o lote se refiere cada uno.
    def fechas_aviso(codigo):
        return sorted(
            text(d) for v in children(cfs, "ValidNoticeInfo") if text(child(v, "NoticeTypeCode")) == codigo
            for d in v.iter() if local(d.tag) == "IssueDate" and text(d))
    n_ccn = sum(text(child(v, "NoticeTypeCode")) == "DOC_CCN" for v in children(cfs, "ValidNoticeInfo"))
    n_anul_ccn = sum(text(child(v, "NoticeTypeCode")) == "ANUL_CCN" for v in children(cfs, "ValidNoticeInfo"))
    fechas_ccn = fechas_aviso("DOC_CCN")

    # Documentos con su procedencia: origen (archivo/etiqueta) y sección de primer nivel del expediente.
    documentos = []
    for seccion in cfs:
        nombre_seccion = local(seccion.tag)
        for d in seccion.iter():
            l = local(d.tag)
            if l == "FileName" and text(d):
                documentos.append((text(d), "archivo", nombre_seccion))
            elif l == "DocumentTypeCode" and d.get("name"):
                documentos.append((d.get("name"), "etiqueta", nombre_seccion))
    docs_ejec: dict[str, list[str]] = defaultdict(list)
    for nombre, origen, seccion in documentos:
        etiqueta = f"{nombre} ⟨{origen}·{seccion}⟩"
        for cat in clasificar_documento(nombre):
            if etiqueta not in docs_ejec[cat]:
                docs_ejec[cat].append(etiqueta)
    for mod in modificaciones:
        nota = " ".join(text(child(mod, "Note")).split())
        nivel = fin_en_nota(nota)
        if nivel:
            cat = CATEGORIA_NOTA if nivel == "confirmado" else CATEGORIA_NOTA_CANDIDATO
            docs_ejec[cat].append(f"{nota[:80]} ⟨nota·modificación {text(child(mod, 'ID'))}⟩")

    exp = Expediente(
        id=ident,
        enlace=enlace_el.get("href", "") if enlace_el is not None else "",
        expediente=text(child(cfs, "ContractFolderID")),
        organo=nombre_organo,
        organo_id=organo_id,
        tipo_administracion=text(child(parte, "ContractingPartyTypeCode")) if parte is not None else "",
        estado=text(child(cfs, "ContractFolderStatusCode")),
        actualizado=actualizado,
        tipo_contrato=tipo,
        presupuesto_sin_iva=presupuesto,
        fecha_adjudicacion=min(fechas_adj) if fechas_adj else "",
        fecha_adjudicacion_cualquiera=min(fechas_cualquiera) if fechas_cualquiera else "",
        importe_adjudicado_sin_iva=importe_adj if hay_importe else None,
        formalizado=formalizado,
        duracion_prevista=duracion,
        prorroga_prevista_texto=prorroga_texto,
        n_modificaciones=len(modificaciones),
        anuncio_modificacion="DOC_MOD" in avisos,
        anuncio_finalizacion=n_ccn > n_anul_ccn,
        n_anuncios_finalizacion=n_ccn,
        n_anulaciones_finalizacion=n_anul_ccn,
        fecha_anuncio_finalizacion=fechas_ccn[0][:10] if fechas_ccn else "",
        n_documentos=len(documentos),
        n_resultados=len(codigos_resultado),
        n_resultados_adjudicados=sum(c in RESULTADOS_ADJUDICADOS for c in codigos_resultado),
        codigos_resultado=",".join(codigos_resultado),
        fecha_inicio=inicio[:10],
        duracion_final_dias=duracion_final,
        fin_teorico=fin,
        documentos_ejecucion=dict(docs_ejec),
    )
    return ident, actualizado, exp


def procesar_fichero(args) -> dict:
    """Trabajo de un proceso: un fichero ATOM dentro de un ZIP."""
    ruta_zip, nombre = args
    versiones = []          # (id, actualizado, expediente_dict|None)
    borrados = []           # (ref, when, tipo)
    entradas = 0
    anios = Counter()
    with zipfile.ZipFile(ruta_zip) as z, z.open(nombre) as f:
        for _ev, el in ET.iterparse(f, events=("end",)):
            if el.tag == ATOM + "entry":
                entradas += 1
                ident, actualizado, exp = extraer(el)
                anios[actualizado[:4]] += 1
                versiones.append((ident, actualizado, asdict(exp) if exp else None))
                el.clear()
            elif el.tag == TOMBSTONE:
                comentario = el.find(TOMBSTONE_NS + "comment")
                tipo = (comentario.get("type", "") if comentario is not None else "") or "SIN_TIPO"
                borrados.append((el.get("ref", ""), el.get("when", ""), tipo.upper()))
                el.clear()
    return {"versiones": versiones, "borrados": borrados, "entradas": entradas, "anios": anios}


FECHA_MIN = datetime.min.replace(tzinfo=timezone.utc)


def fecha(s: str) -> datetime:
    """Fecha con zona horaria; las que no la traen se toman como UTC."""
    try:
        t = datetime.fromisoformat(s)
    except ValueError:
        return FECHA_MIN
    return t if t.tzinfo else t.replace(tzinfo=timezone.utc)


def canonica(c: dict) -> str:
    return json.dumps(c, sort_keys=True, ensure_ascii=False)


def elegir_principal(versiones: list[dict]) -> dict:
    """Ante versiones distintas con la misma `updated` máxima (la especificación admite correcciones
    sin cambiar la fecha, §3.3.1) no se puede saber cuál es la vigente. Regla DETERMINISTA, que no
    depende del orden de lectura: la de más documentos y, a igualdad, la de mayor representación
    canónica. No se combinan campos de versiones distintas; la incertidumbre se informa aparte."""
    return max(versiones, key=lambda v: (v["n_documentos"], canonica(v)))


def seleccionado(c: dict) -> bool:
    p = c["presupuesto_sin_iva"]
    return (
        c["estado"] in ESTADOS_ADMITIDOS
        and c["fecha_adjudicacion"][:4] == str(ANIO_ADJUDICACION)
        and p is not None
        and PRESUPUESTO_MIN <= p <= PRESUPUESTO_MAX
    )


def candidato_amplio(c: dict) -> bool:
    """Como `seleccionado`, pero sin exigir código de resultado de adjudicación."""
    p = c["presupuesto_sin_iva"]
    return (
        c["estado"] in ESTADOS_ADMITIDOS
        and c["fecha_adjudicacion_cualquiera"][:4] == str(ANIO_ADJUDICACION)
        and p is not None
        and PRESUPUESTO_MIN <= p <= PRESUPUESTO_MAX
    )


def plazo_vencido(c: dict, corte) -> bool | None:
    fin = fecha_dia(c["fin_teorico"])
    return None if fin is None else fin < corte


def sin_fin_definitivo(c: dict) -> bool:
    """Sin anuncio estructurado de finalización ni documento candidato de fin definitivo."""
    return not c.get("anuncio_finalizacion") and not (DOCS_FIN_DEFINITIVO & set(c["documentos_ejecucion"]))


def sin_ningun_fin(c: dict) -> bool:
    return sin_fin_definitivo(c) and not (DOCS_FIN_PARCIAL & set(c["documentos_ejecucion"]))


def pct(n: int, d: int) -> str:
    return f"{100 * n / d:.1f} %" if d else "—"


def sha256_fichero(ruta: str) -> str:
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def medir(rutas_zip: list[str], salida: str, max_ficheros: int | None, procesos: int,
          huellas: bool = True) -> dict:
    tareas = []
    for ruta in rutas_zip:
        with zipfile.ZipFile(ruta) as z:
            nombres = sorted(n for n in z.namelist() if n.endswith(".atom"))
        tareas += [(ruta, n) for n in nombres]
    if max_ficheros:
        tareas = tareas[:max_ficheros]

    # id -> (fecha máxima, versiones distintas con esa fecha); la lista puede contener None
    # (la versión no es de obras).
    ultima: dict[str, tuple[datetime, list]] = {}
    borrados: dict[str, tuple[datetime, str]] = {}
    entradas = 0
    anios = Counter()
    with ProcessPoolExecutor(max_workers=procesos) as ex:
        for i, r in enumerate(ex.map(procesar_fichero, tareas, chunksize=4), 1):
            entradas += r["entradas"]
            anios.update(r["anios"])
            for ident, actualizado, c in r["versiones"]:
                t = fecha(actualizado)
                previa = ultima.get(ident)
                if previa is None or t > previa[0]:
                    ultima[ident] = (t, [c])
                elif t == previa[0] and c not in previa[1]:
                    previa[1].append(c)
            for ref, when, tipo in r["borrados"]:
                t = fecha(when)
                if ref not in borrados or t > borrados[ref][0]:
                    borrados[ref] = (t, tipo)
            if i % 50 == 0 or i == len(tareas):
                print(f"  {i}/{len(tareas)} ficheros, {entradas} entradas", file=sys.stderr, flush=True)

    obras = []                       # versión principal de cada expediente de obras no anulado
    alternativas: dict[str, list[dict]] = {}   # id -> todas las versiones de obras empatadas (si >1)
    excluidas_borrado = Counter()
    candidatos_excluidos_borrado = Counter()
    empates_totales = 0
    for ident, (t, versiones) in ultima.items():
        de_obras = [v for v in versiones if v is not None]
        if len(versiones) > 1:
            empates_totales += 1
        if not de_obras:
            continue
        principal = dict(elegir_principal(de_obras))
        principal["n_versiones_empatadas"] = len(versiones)
        tipo_borrado = borrados[ident][1] if ident in borrados and borrados[ident][0] >= t else ""
        principal["borrado_tipo"] = tipo_borrado
        if tipo_borrado in ("ANULADA", "SIN_TIPO"):
            excluidas_borrado[tipo_borrado] += 1
            if any(candidato_amplio(v) for v in de_obras):
                candidatos_excluidos_borrado[tipo_borrado] += 1
            continue
        obras.append(principal)
        if len(versiones) > 1:
            alternativas[ident] = de_obras + ([None] if None in versiones else [])

    seleccion = sorted((c for c in obras if seleccionado(c)), key=lambda c: c["id"])
    obras_anio = [c for c in obras if c["estado"] in ESTADOS_ADMITIDOS
                  and c["fecha_adjudicacion"][:4] == str(ANIO_ADJUDICACION)]
    corte = max((t for t, _ in ultima.values()), default=FECHA_MIN).date()

    exclusiones = Counter()
    for c in obras:
        if candidato_amplio(c) and not seleccionado(c):
            codigos = sorted(set(c["codigos_resultado"].split(","))) if c["codigos_resultado"] else ["(ninguno)"]
            exclusiones[",".join(codigos)] += 1

    empates = analizar_empates(seleccion, obras, alternativas, corte)
    diagnostico = diagnosticar_borrados(ultima, borrados)

    os.makedirs(salida, exist_ok=True)
    escribir_csv(os.path.join(salida, "expedientes_seleccionados.csv"), seleccion)
    escribir_csv(os.path.join(salida, "candidatos_fin.csv"),
                 [c for c in seleccion if not sin_ningun_fin(c)])
    avisos_ccn = Counter(c["fecha_anuncio_finalizacion"][:4] for c in obras if c.get("anuncio_finalizacion"))
    escribir_empates(os.path.join(salida, "empates_en_seleccion.csv"), empates["filas"])

    vencidos = [c for c in seleccion if plazo_vencido(c, corte)]
    resumen = {
        "version_programa": VERSION,
        "ficheros_leidos": len(tareas),
        "zips": [os.path.basename(r) for r in rutas_zip],
        "entradas_leidas": entradas,
        "expedientes_distintos": len(ultima),
        "expedientes_con_versiones_empatadas_en_todos_los_datos": empates_totales,
        "expedientes_de_obras_excluidos_por_borrado": dict(excluidas_borrado),
        "candidatos_excluidos_por_borrado": dict(candidatos_excluidos_borrado),
        "expedientes_de_obras_ultima_version": len(obras),
        "expedientes_seleccionados": len(seleccion),
        "seleccionados_cerrados": sum(c["borrado_tipo"] == "CERRADA" for c in seleccion),
        "seleccionados_con_varios_resultados_adjudicados": sum(c["n_resultados_adjudicados"] > 1 for c in seleccion),
        "fin_teorico_anterior_al_corte": len(vencidos),
        "vencidos_sin_candidato_fin_definitivo": sum(sin_fin_definitivo(c) for c in vencidos),
        "vencidos_sin_ningun_candidato_fin": sum(sin_ningun_fin(c) for c in vencidos),
        "seleccionados_con_anuncio_finalizacion": sum(bool(c.get("anuncio_finalizacion")) for c in seleccion),
        "obras_con_anulacion_de_anuncio_finalizacion": sum(c.get("n_anulaciones_finalizacion", 0) > 0 for c in obras),
        "obras_con_anuncio_finalizacion_por_anio_del_anuncio": dict(sorted(avisos_ccn.items())),
        "empates": {k: v for k, v in empates.items() if k != "filas"},
        "diagnostico_borrados": diagnostico,
        "excluidos_por_codigo_de_resultado": dict(exclusiones.most_common()),
        "fecha_de_corte_datos": corte.isoformat(),
        "anios_de_actualizacion_en_las_entradas": dict(sorted(anios.items())),
    }
    escribir_informe(os.path.join(salida, "informe.md"), seleccion, resumen, obras_anio, corte)
    escribir_anexo_administraciones(os.path.join(salida, "anexo_por_tipo_administracion.md"), seleccion, corte)
    with open(os.path.join(salida, "resumen.json"), "w", encoding="utf-8") as f:
        json.dump(resumen, f, ensure_ascii=False, indent=2)
    escribir_manifiesto(os.path.join(salida, "manifiesto.json"), rutas_zip, huellas)
    return resumen


def opciones_titular(v: dict | None, corte) -> tuple[int, int]:
    """Contribución de una versión al titular: (está en el denominador, está en el numerador).
    Denominador = seleccionado con fin teórico anterior al corte; numerador = además sin candidato
    de fin definitivo."""
    if v is None or not seleccionado(v) or not plazo_vencido(v, corte):
        return (0, 0)
    return (1, 1 if sin_fin_definitivo(v) else 0)


def analizar_empates(seleccion: list[dict], obras: list[dict], alternativas: dict, corte) -> dict:
    """Cotas mínima y máxima del número de seleccionados y de la proporción del titular si, en cada
    expediente con versiones empatadas, se hubiera elegido cualquiera de ellas."""
    principales = {c["id"]: c for c in obras}
    filas = []
    sel_min = sel_max = len(seleccion)
    base_d = base_n = 0
    opciones = []
    for c in seleccion:
        if c["id"] not in alternativas:
            d, n = opciones_titular(c, corte)
            base_d += d
            base_n += n
    for ident, versiones in alternativas.items():
        principal = principales[ident]
        sel = [v is not None and seleccionado(v) for v in versiones]
        if seleccionado(principal) and not all(sel):
            sel_min -= 1
        if not seleccionado(principal) and any(sel):
            sel_max += 1
        ops = {opciones_titular(v, corte) for v in versiones}
        if any(sel):
            opciones.append(ops)
            filas.append({
                "id": ident, "expediente": principal["expediente"], "n_versiones": len(versiones),
                "seleccionado_por_version": ",".join("si" if s else "no" for s in sel),
                "titular_por_version": ",".join(f"{d}/{n}" for d, n in (opciones_titular(v, corte) for v in versiones)),
                "candidato_fin_definitivo_por_version": ",".join(
                    "-" if v is None else ("no" if sin_fin_definitivo(v) else "si") for v in versiones),
                "principal_seleccionado": "si" if seleccionado(principal) else "no",
            })
    # Cota inferior de la proporción: preferir (1,0), luego (0,0), luego (1,1); la superior, al revés.
    d_min, n_min, d_max, n_max = base_d, base_n, base_d, base_n
    for ops in opciones:
        for orden, acum in (([(1, 0), (0, 0), (1, 1)], "min"), ([(1, 1), (0, 0), (1, 0)], "max")):
            elegido = next(o for o in orden if o in ops)
            if acum == "min":
                d_min += elegido[0]; n_min += elegido[1]
            else:
                d_max += elegido[0]; n_max += elegido[1]
    return {
        "expedientes_empatados_relevantes": len(filas),
        "seleccionados_cota_minima": sel_min,
        "seleccionados_cota_maxima": sel_max,
        "titular_cota_minima": f"{n_min}/{d_min} ({pct(n_min, d_min)})",
        "titular_cota_maxima": f"{n_max}/{d_max} ({pct(n_max, d_max)})",
        "filas": filas,
    }


def diagnosticar_borrados(ultima: dict, borrados: dict) -> dict:
    """Recuentos que permiten auditar cómo se emparejan los `ref` de los borrados con los `id`."""
    diag = {}
    for tipo in ("CERRADA", "ANULADA", "SIN_TIPO"):
        refs = [r for r, (_, tp) in borrados.items() if tp == tipo]
        con_entrada = [r for r in refs if r in ultima]
        de_obras = [r for r in con_entrada if any(v is not None for v in ultima[r][1])]
        posteriores = [r for r in de_obras if borrados[r][0] >= ultima[r][0]]
        amplios = [r for r in posteriores
                   if any(v is not None and candidato_amplio(v) for v in ultima[r][1])]
        diag[tipo] = {
            "refs_distintos": len(refs),
            "con_entrada_leida": len(con_entrada),
            "de_obras": len(de_obras),
            "de_obras_con_borrado_posterior_a_su_ultima_version": len(posteriores),
            "de_esos_cumplirian_criterios_sin_exigir_resultado_adjudicado": len(amplios),
        }
    return diag


def escribir_csv(ruta: str, expedientes: list[dict]) -> None:
    columnas = [k for k in Expediente.__dataclass_fields__ if k != "documentos_ejecucion"]
    with open(ruta, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(columnas + CATEGORIAS_SALIDA)
        for c in expedientes:
            fila = [c.get(k, "") for k in columnas]
            fila += [" | ".join(c["documentos_ejecucion"].get(cat, [])) for cat in CATEGORIAS_SALIDA]
            w.writerow(fila)


def escribir_empates(ruta: str, filas: list[dict]) -> None:
    columnas = ["id", "expediente", "n_versiones", "principal_seleccionado", "seleccionado_por_version",
                "titular_por_version", "candidato_fin_definitivo_por_version"]
    with open(ruta, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=columnas, delimiter=";")
        w.writeheader()
        w.writerows(filas)


def escribir_manifiesto(ruta: str, rutas_zip: list[str], huellas: bool) -> None:
    with open(os.path.abspath(__file__), "rb") as f:
        huella_programa = hashlib.sha256(f.read()).hexdigest()
    datos = {
        "generado": datetime.now().isoformat(timespec="seconds"),
        "programa": {"version": VERSION, "sha256": huella_programa},
        "python": platform.python_version(),
        "ficheros": [{"nombre": os.path.basename(r), "bytes": os.path.getsize(r),
                      "sha256": sha256_fichero(r) if huellas else None} for r in rutas_zip],
    }
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)


def tramo(c: dict) -> str:
    p = c["presupuesto_sin_iva"]
    if p is None:
        return "sin presupuesto"
    if p < PRESUPUESTO_MIN:
        return f"< {PRESUPUESTO_MIN / 1e6:g} M€"
    if p <= PRESUPUESTO_MAX:
        return f"{PRESUPUESTO_MIN / 1e6:g}–{PRESUPUESTO_MAX / 1e6:g} M€"
    return f"> {PRESUPUESTO_MAX / 1e6:g} M€"


def bloque_plazo(f, titulo: str, cs: list[dict], corte) -> None:
    venc = [c for c in cs if plazo_vencido(c, corte)]
    sin_def = sum(sin_fin_definitivo(c) for c in venc)
    sin_nada = sum(sin_ningun_fin(c) for c in venc)
    f.write(f"| {titulo} | {len(cs)} | {len(venc)} ({pct(len(venc), len(cs))}) | "
            f"{sin_def} ({pct(sin_def, len(venc))}) | {sin_nada} ({pct(sin_nada, len(venc))}) |\n")


def escribir_informe(ruta: str, sel: list[dict], resumen: dict, obras_anio: list[dict], corte) -> None:
    n = len(sel)

    def cuenta(pred):
        return sum(1 for c in sel if pred(c))

    filas = [
        ("Formalización publicada (al menos un resultado)", cuenta(lambda c: c["formalizado"])),
        ("Alguna modificación en datos estructurados", cuenta(lambda c: c["n_modificaciones"] > 0)),
        ("Anuncio de modificación (DOC_MOD)", cuenta(lambda c: c["anuncio_modificacion"])),
        ("**Anuncio de finalización de contrato (DOC_CCN, estructurado)**", cuenta(lambda c: c["anuncio_finalizacion"])),
        ("Candidato de fin definitivo por documento, sin DOC_CCN",
         cuenta(lambda c: not c["anuncio_finalizacion"] and bool(DOCS_FIN_DEFINITIVO & set(c["documentos_ejecucion"])))),
        ("Prórroga prevista (texto en pliegos)", cuenta(lambda c: c["prorroga_prevista_texto"])),
    ]
    filas += [(f"Candidato: {cat}", cuenta(lambda c, cat=cat: cat in c["documentos_ejecucion"]))
              for cat in CATEGORIAS_SALIDA]
    filas.append(("Algún candidato de incidencias durante la obra",
                  cuenta(lambda c: bool(DOCS_DURANTE & set(c["documentos_ejecucion"])))))
    filas.append(("Algún candidato de fin definitivo", cuenta(lambda c: not sin_fin_definitivo(c))))
    filas.append(("Algún candidato de fin (definitivo o parcial/avance)", cuenta(lambda c: not sin_ningun_fin(c))))

    e = resumen["empates"]
    d = resumen["diagnostico_borrados"]
    with open(ruta, "w", encoding="utf-8") as f:
        f.write("# Fase 0 — Visibilidad de la ejecución de obras públicas en la sindicación de la PLACSP\n\n")
        f.write(f"Programa v{VERSION} · Generado: {datetime.now().isoformat(timespec='seconds')} · "
                f"Corte de datos: {corte.isoformat()}\n\n")
        f.write("> **Lectura obligatoria.** (1) La unidad es el **expediente** (licitación), que puede contener "
                "varios lotes y contratos. (2) Los documentos se detectan por **nombres de archivo o etiquetas de "
                "tipo documental** de la sindicación, no por su contenido: son *candidatos*. (3) Las cifras miden "
                "**la ausencia de coincidencias detectadas por el clasificador** en este canal, NO la inexistencia "
                "de documentación de finalización, que la obra no haya terminado ni que nadie incumpla nada; la "
                "información puede estar en el Registro de Contratos del Sector Público o en otro sitio. (4) El fin "
                "es **teórico estimado**, no la fecha real.\n\n"
                "> **«RES» (resuelta)** significa que ha terminado el procedimiento de contratación, no la obra.\n\n")
        f.write("## Criterios de selección\n\n")
        f.write(f"- Obras (código {TIPO_CONTRATO}); estado {', '.join(sorted(ESTADOS_ADMITIDOS))}\n"
                f"- Primera fecha de adjudicación de un resultado adjudicado (códigos "
                f"{', '.join(sorted(RESULTADOS_ADJUDICADOS))}) en {ANIO_ADJUDICACION}\n"
                f"- Presupuesto base sin IVA del expediente entre {PRESUPUESTO_MIN:,.0f} y {PRESUPUESTO_MAX:,.0f} EUR\n"
                "- Última versión de cada expediente; ante versiones distintas con la misma fecha, regla "
                "determinista (más documentos) e incertidumbre informada aparte\n"
                "- Excluidos los expedientes con borrado ANULADA o sin tipo; los CERRADOS se incluyen y se marcan\n\n")

        f.write("## Resultado principal\n\n| Conjunto | Expedientes | Fin teórico anterior al corte | "
                "…sin candidato de fin **definitivo** | …sin **ningún** candidato de fin |\n|---|---:|---:|---:|---:|\n")
        bloque_plazo(f, "**Principal** (incluye cerrados)", sel, corte)
        bloque_plazo(f, "Sensibilidad: sin CERRADOS", [c for c in sel if c["borrado_tipo"] != "CERRADA"], corte)
        bloque_plazo(f, "Sensibilidad: un solo resultado adjudicado", [c for c in sel if c["n_resultados_adjudicados"] == 1], corte)
        bloque_plazo(f, "Sensibilidad: sin versiones empatadas", [c for c in sel if c["n_versiones_empatadas"] == 1], corte)
        f.write(f"\nSin datos suficientes para estimar el fin: {sum(plazo_vencido(c, corte) is None for c in sel)}.\n\n"
                "**Fin definitivo** = anuncio estructurado de finalización de contrato (DOC_CCN) o documento "
                "candidato de recepción definitiva, liquidación, certificación final, fin de obra o "
                "resolución del contrato. **Parcial/avance** = recepción parcial, certificación de avance o "
                "resolución en trámite.\n\n")

        f.write("## Incertidumbre por versiones empatadas\n\n"
                f"Expedientes con versiones distintas y la misma fecha de actualización en todos los datos: "
                f"{resumen['expedientes_con_versiones_empatadas_en_todos_los_datos']}. De ellos, "
                f"{e['expedientes_empatados_relevantes']} serían seleccionables con alguna de sus versiones "
                "(detalle en `empates_en_seleccion.csv`).\n\n"
                f"- Expedientes seleccionados: {n} (cota mínima {e['seleccionados_cota_minima']}, "
                f"cota máxima {e['seleccionados_cota_maxima']})\n"
                f"- Titular (sin candidato de fin definitivo / fin teórico anterior al corte): cota mínima "
                f"{e['titular_cota_minima']}, cota máxima {e['titular_cota_maxima']}\n\n")

        f.write("## Diagnóstico de borrados (`at:deleted-entry`)\n\n| Tipo | `ref` distintos | Con entrada leída | "
                "De obras | Borrado posterior a la última versión | …que cumplirían criterios amplios |\n"
                "|---|---:|---:|---:|---:|---:|\n")
        for tipo, v in d.items():
            f.write(f"| {tipo} | {v['refs_distintos']} | {v['con_entrada_leida']} | {v['de_obras']} | "
                    f"{v['de_obras_con_borrado_posterior_a_su_ultima_version']} | "
                    f"{v['de_esos_cumplirian_criterios_sin_exigir_resultado_adjudicado']} |\n")

        f.write("\n## Datos leídos\n\n")
        for k in ("version_programa", "ficheros_leidos", "entradas_leidas", "expedientes_distintos",
                  "expedientes_de_obras_ultima_version", "expedientes_seleccionados", "seleccionados_cerrados",
                  "seleccionados_con_varios_resultados_adjudicados", "fecha_de_corte_datos"):
            f.write(f"- {k.replace('_', ' ')}: {resumen[k]}\n")
        f.write(f"- años de actualización de las entradas: {resumen['anios_de_actualizacion_en_las_entradas']}\n\n")
        f.write("### Exclusiones por código de resultado\n\nExpedientes que cumplirían los criterios si no se "
                "exigiera un resultado adjudicado con fecha en el año. Un expediente multilote puede combinar "
                "códigos; no indican una única causa.\n\n| Códigos de resultado | Expedientes |\n|---|---:|\n")
        for k, v in resumen["excluidos_por_codigo_de_resultado"].items():
            f.write(f"| {k} | {v} |\n")
        f.write(f"\n## Detalle (n = {n} expedientes)\n\n| Qué consta | Expedientes | % |\n|---|---:|---:|\n")
        for etiqueta, k in filas:
            f.write(f"| {etiqueta} | {k} | {pct(k, n)} |\n")

        por_tramo = defaultdict(list)
        for c in obras_anio:
            por_tramo[tramo(c)].append(c)
        f.write(f"\n## Robustez por tramo de importe (añadido a posteriori; expedientes de obras adjudicados en "
                f"{ANIO_ADJUDICACION}, sin filtro de importe)\n\n"
                "| Tramo | n | Alguna modificación | Algún candidato de fin definitivo | Fin teórico anterior al corte | "
                "…y sin candidato de fin definitivo |\n|---|---:|---:|---:|---:|---:|\n")
        for t, cs in sorted(por_tramo.items()):
            m = len(cs)
            venc = [c for c in cs if plazo_vencido(c, corte)]
            f.write(f"| {t} | {m} | {pct(sum(c['n_modificaciones'] > 0 for c in cs), m)} | "
                    f"{pct(sum(not sin_fin_definitivo(c) for c in cs), m)} | {pct(len(venc), m)} | "
                    f"{pct(sum(sin_fin_definitivo(c) for c in venc), len(venc))} |\n")
        f.write("\nLa tabla por tipo de administración está en `anexo_por_tipo_administracion.md`.\n")


def escribir_anexo_administraciones(ruta: str, sel: list[dict], corte) -> None:
    por_admin = defaultdict(list)
    for c in sel:
        por_admin[TIPOS_ADMINISTRACION.get(c["tipo_administracion"], "Sin código")].append(c)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write("# Anexo técnico — por tipo de administración\n\n"
                "> **EXPLORATORIA, NO COMPARABLE.** Conviven dos versiones de la lista de códigos de tipo de "
                "administración (1.04 y 2.10) y las entradas recientes usan la 2.10. Las diferencias pueden "
                "deberse a la versión de la lista. **No usar para comparar organismos ni para clasificarlos.**\n\n"
                "| Tipo | n | Alguna modificación | Algún candidato de fin definitivo |\n|---|---:|---:|---:|\n")
        for tipo, cs in sorted(por_admin.items()):
            m = len(cs)
            f.write(f"| {tipo} | {m} | {pct(sum(c['n_modificaciones'] > 0 for c in cs), m)} | "
                    f"{pct(sum(not sin_fin_definitivo(c) for c in cs), m)} |\n")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("zips", nargs="+", help="ZIP(s) de la sindicación de la PLACSP")
    ap.add_argument("--salida", default="resultados")
    ap.add_argument("--max-ficheros", type=int, default=None, help="solo para pruebas")
    ap.add_argument("--procesos", type=int, default=max(1, (os.cpu_count() or 2) - 1))
    ap.add_argument("--sin-huellas", action="store_true", help="no calcular SHA-256 de los ZIP (más rápido)")
    a = ap.parse_args()
    r = medir(a.zips, a.salida, a.max_ficheros, a.procesos, not a.sin_huellas)
    print(json.dumps({k: v for k, v in r.items() if k != "excluidos_por_codigo_de_resultado"},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
