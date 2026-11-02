"""Protocolo de obras: registro de resultados de las solicitudes.

Órdenes:
  crear      Crea registro.csv vacío con las columnas (o añade las filas de un lote: --lote lote_AAAA-MM-DD/lote.csv).
  validar    Comprueba columnas, valores permitidos y orden de fechas.
  pendientes Lista lo que toca hacer a una fecha: solicitudes vencidas sin respuesta (y hasta cuándo reclamar),
             reclamaciones sin resolver fuera de plazo y resoluciones estimatorias sin cumplimiento anotado.
  resumen    Cifras agregadas (sin órganos ni personas).
  exportar   Borrador público sin datos del solicitante. Por defecto, SIN identificadores de obra ni de órgano
             (id, enlace, expediente, órgano, garante); con --con-identificadores los incluye, tras decidirlo y revisarlo.

Plazos: dependen del régimen de cada solicitud (columna «regimen»: comunidad y ámbito; ver regimenes.py, con la cita
del BOE de cada fila). Con carácter general (Ley 19/2013), resolver en un mes desde la recepción POR EL ÓRGANO
COMPETENTE, ampliable un mes con notificación (art. 20.1); el silencio es desestimatorio (art. 20.4); reclamación en un
mes desde el silencio (art. 24.2); el Consejo de Transparencia resuelve en tres meses (art. 24.4). Las leyes
autonómicas cambian el plazo (20 o 30 días hábiles), la ampliación (quince días en Euskadi, media prórroga en
Cataluña), el plazo para reclamar contra el silencio (sin plazo en algunas) y el del órgano de garantía (dos meses
en Cataluña). Si el régimen no está verificado, NO se calcula ninguna fecha. Cómputo (Ley 39/2015, art. 30): por
meses, de fecha a fecha; por días, hábiles; si el último día es inhábil, el siguiente hábil. Se tienen en cuenta
sábados, domingos y festivos nacionales (Viernes Santo incluido); los autonómicos y locales se añaden con --festivos,
para todas las filas, para una comunidad o para un órgano (ver cargar_festivos).

Dos fechas distintas:
- fecha límite PROVISIONAL: la calcula el programa. Sirve para avisar, nunca para calificar.
- fecha_limite_verificada: la anota una persona después de comprobar la recepción real por el órgano, el
  calendario del lugar, las suspensiones (alegaciones de terceros, subsanación) y la ampliación. Solo con ella se
  califica una respuesta de «en plazo» o «fuera de plazo» y entra en las cifras de plazos.
fecha_ampliacion es la fecha en que se NOTIFICÓ la ampliación a quien pregunta; solo cuenta si es anterior al
vencimiento ordinario y a la respuesta.
Uso: python -I -X utf8 registro.py ORDEN [--registro registro.csv] [--fecha AAAA-MM-DD] [--festivos festivos.txt]
"""
import argparse
import csv
import os
import sys
from collections import Counter
from datetime import date, timedelta

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import regimenes as rgm  # noqa: E402

CAMPOS = ["id_obra", "enlace", "expediente", "organo_id", "ambito", "garante", "regimen", "origen", "organizacion",
          "fecha_envio", "fecha_recepcion_organo", "ref_solicitud", "fecha_ampliacion", "fecha_limite_verificada",
          "fecha_respuesta", "resultado", "documentos",
          "fecha_replanteo", "fecha_recepcion_obra", "fecha_reclamacion", "ref_reclamacion", "resultado_reclamacion",
          "fecha_resolucion_reclamacion", "cumplimiento", "notas"]
FECHAS = ["fecha_envio", "fecha_recepcion_organo", "fecha_ampliacion", "fecha_limite_verificada", "fecha_respuesta",
          "fecha_replanteo", "fecha_recepcion_obra", "fecha_reclamacion", "fecha_resolucion_reclamacion"]
VALORES = {
    "resultado": {"", "concedida", "concedida_parcial", "inexistente", "remitida", "inadmitida_18.1.a",
                  "inadmitida_18.1.b", "inadmitida_18.1.c", "inadmitida_18.1.d", "inadmitida_18.1.e",
                  "denegada_limite", "desistimiento", "silencio",
                  "descartada"},   # no se envió: la información ya era pública (anotar el motivo en «notas»)
    "resultado_reclamacion": {"", "estimatoria", "estimatoria_parcial", "estimatoria_formal", "desestimatoria",
                              "inadmitida", "archivo", "desistimiento"},
    "cumplimiento": {"", "cumplida", "no_consta", "contencioso", "no_aplica"},
    "ambito": {"", "estatal", "autonómico o local", "otro"},
}
DOCUMENTOS = {"acta_recepcion", "certificacion_final", "replanteo", "suspension", "ampliacion_plazo",
              "resolucion_contrato", "otro"}
IDENTIFICADORES = ["id_obra", "enlace", "expediente", "organo_id", "garante"]
PUBLICOS = ["id_obra", "enlace", "expediente", "organo_id", "ambito", "garante", "fecha_envio", "fecha_recepcion_organo",
            "fecha_limite_provisional", "fecha_limite_verificada", "fecha_respuesta", "en_plazo", "resultado", "documentos", "fecha_replanteo", "fecha_recepcion_obra", "fecha_reclamacion",
            "resultado_reclamacion", "fecha_resolucion_reclamacion", "cumplimiento"]


def mas_meses(d, n=1):
    """Cómputo de plazos por meses: de fecha a fecha; si el día no existe en el mes final, el último día."""
    y, m = divmod(d.month - 1 + n, 12)
    y, m = d.year + y, m + 1
    ultimo = (date(y + (m == 12), m % 12 + 1, 1) - timedelta(days=1)).day
    return date(y, m, min(d.day, ultimo))


def f(s):
    return date.fromisoformat(s) if s else None


def fs(s):
    """Como f(), pero devuelve None si la fecha está mal escrita (la validación ya informa del error)."""
    try:
        return f(s)
    except ValueError:
        return None


def pascua(anio):
    """Domingo de Pascua (algoritmo gregoriano anónimo)."""
    a, b, c = anio % 19, anio // 100, anio % 100
    d, e = b // 4, b % 4
    g = (8 * b + 13) // 25
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 19 * l) // 433
    mes = (h + l - 7 * m + 90) // 25
    return date(anio, mes, (h + l - 7 * m + 33 * mes + 19) % 32)


FESTIVOS_ADICIONALES = set()   # festivos para TODAS las filas (solo si todos los órganos comparten calendario)
FESTIVOS_POR_AMBITO = {}       # "ccaa:<comunidad>" u "organo:<id>" -> festivos de ese territorio u órgano


def cargar_festivos(lineas):
    """Una fecha por línea: «AAAA-MM-DD» (todas las filas), «AAAA-MM-DD País Vasco» (las filas de esa comunidad,
    escrita como en la columna «regimen») o «AAAA-MM-DD organo:ID» (las filas de ese órgano, para los locales).
    Las líneas que empiezan por # son comentarios."""
    for l in lineas:
        l = l.strip()
        if not l or l.startswith("#"):
            continue
        fecha, _, ambito = l.partition(" ")
        d, ambito = date.fromisoformat(fecha), ambito.strip()
        if not ambito:
            FESTIVOS_ADICIONALES.add(d)
        else:
            FESTIVOS_POR_AMBITO.setdefault(ambito if ambito.startswith("organo:") else "ccaa:" + ambito, set()).add(d)


def festivos_de(r):
    """Festivos adicionales que valen para una fila: los generales, los de su comunidad y los de su órgano."""
    ccaa = (r.get("regimen") or "").split("|")[0]
    return (FESTIVOS_ADICIONALES | FESTIVOS_POR_AMBITO.get("ccaa:" + ccaa, set())
            | FESTIVOS_POR_AMBITO.get("organo:" + (r.get("organo_id") or ""), set()))


def inhabil(d, extra=frozenset()):
    nacionales = {(1, 1), (1, 6), (5, 1), (8, 15), (10, 12), (11, 1), (12, 6), (12, 8), (12, 25)}
    return (d.weekday() >= 5 or (d.month, d.day) in nacionales or d == pascua(d.year) - timedelta(days=2)
            or d in FESTIVOS_ADICIONALES or d in extra)


def habil(d, extra=frozenset()):
    """Art. 30.5 Ley 39/2015: si el último día del plazo es inhábil, se prorroga al primer día hábil siguiente."""
    while inhabil(d, extra):
        d += timedelta(days=1)
    return d


def mas_habiles(d, n, extra=frozenset()):
    """n días hábiles contados desde el día siguiente a d (Ley 39/2015, art. 30.2 y 30.3)."""
    while n > 0:
        d += timedelta(days=1)
        if not inhabil(d, extra):
            n -= 1
    return d


def base_plazo(r):
    """Recepción por el órgano competente si se conoce; si no, el envío (plazo provisional)."""
    return fs(r["fecha_recepcion_organo"]) or fs(r["fecha_envio"])


def _sumar(d, plazo, extra):
    n, unidad = plazo
    return mas_meses(d, n) if unidad == "meses" else mas_habiles(d, n, extra)


def limite_ordinario(r):
    """Vencimiento sin ampliación (provisional). None si no hay base o el régimen no está verificado."""
    b = base_plazo(r)
    reg = rgm.regimen(r.get("regimen", ""))
    if not b or not reg["verificado"] or reg["plazo"] is None:
        return None
    return habil(_sumar(b, reg["plazo"], festivos_de(r)), festivos_de(r))


def problema_ampliacion(r):
    """Motivo por el que una ampliación anotada no puede contarse; vacío si puede contarse (o no hay ampliación)."""
    if not r["fecha_ampliacion"]:
        return ""
    if not fs(r["fecha_ampliacion"]):
        return "fecha_ampliacion mal escrita"
    reg = rgm.regimen(r.get("regimen", ""))
    if reg["verificado"] and reg["plazo"] is not None and reg["ampliacion"] is None:
        return f"ampliación sin cómputo automático ({reg['fuente_ampliacion']})"
    return ampliacion_imposible(r) or ampliacion_aparentemente_tardia(r)


def ampliacion_imposible(r):
    """Errores de cronología indiscutibles: una ampliación no se notifica antes de que el órgano competente reciba la
    solicitud ni después de haber respondido."""
    a = fs(r["fecha_ampliacion"])
    if not a:
        return ""
    rco, resp = fs(r["fecha_recepcion_organo"]), fs(r["fecha_respuesta"])
    if rco and a < rco:
        return f"ampliación notificada el {a}, antes de la recepción por el órgano ({rco})"
    if resp and a > resp:
        return f"ampliación notificada el {a}, después de la respuesta ({resp})"
    return ""


def ampliacion_aparentemente_tardia(r):
    """Aviso, no error: una ampliación posterior al vencimiento ordinario PROVISIONAL puede ser válida si hubo una
    suspensión (alegaciones de terceros, subsanación) que el programa no conoce."""
    a = fs(r["fecha_ampliacion"])
    lim = limite_ordinario(r) if a else None
    if lim and a > lim:
        return (f"ampliación notificada el {a}, después del vencimiento ordinario provisional ({lim}): aparentemente "
                "tardía; comprobar si hubo suspensión y anotar fecha_limite_verificada")
    return ""


def limite(r):
    """Fecha límite de resolución PROVISIONAL según el régimen de la fila y, si consta, la ampliación notificada a
    tiempo. None (no se calcula ninguna fecha) si no hay base, si el régimen no está verificado o si la ampliación
    no puede contarse. Si plazo y ampliación van en la misma unidad, se suman desde la base (un mes + un mes = dos
    meses de fecha a fecha); si no, la ampliación se cuenta desde el final del plazo ordinario (Euskadi: un mes y
    luego quince días hábiles)."""
    b = base_plazo(r)
    reg = rgm.regimen(r.get("regimen", ""))
    if not b or not reg["verificado"] or reg["plazo"] is None:
        return None
    if not r["fecha_ampliacion"]:
        return limite_ordinario(r)
    if problema_ampliacion(r):
        return None
    extra = festivos_de(r)
    (n, u), (m, v) = reg["plazo"], reg["ampliacion"]
    fin = _sumar(b, (n + m, u), extra) if u == v else _sumar(habil(_sumar(b, (n, u), extra), extra), (m, v), extra)
    return habil(fin, extra)


def limite_para_avisos(r):
    """(fecha, verificada): la fecha límite verificada a mano si está anotada; si no, la provisional."""
    v = fs(r["fecha_limite_verificada"])
    return (v, True) if v else (limite(r), False)


def leer(ruta):
    with open(ruta, encoding="utf-8") as fh:
        filas = list(csv.DictReader(fh))
    for r in filas:
        for c in CAMPOS:
            r.setdefault(c, "")
            r[c] = (r[c] or "").strip()
    return filas


def escribir(ruta, filas, campos=CAMPOS):
    with open(ruta, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=campos, extrasaction="ignore")
        w.writeheader()
        w.writerows(filas)


def validar(filas, hoy=None):
    """Errores del registro: lo que es imposible o está mal escrito. Con «hoy», también un silencio anotado antes del
    vencimiento verificado. Los avisos condicionados (dependen de algo que el programa no conoce) van en avisos()."""
    errores = []
    vistos = Counter(r["id_obra"] for r in filas)
    for i, r in enumerate(filas, 2):   # línea del CSV (1 = cabecera)
        def err(msg): errores.append(f"línea {i} ({r['id_obra'] or 'sin id'}): {msg}")
        if not r["id_obra"]:
            err("falta id_obra")
        elif vistos[r["id_obra"]] > 1:
            err("id_obra repetido: el protocolo pregunta una sola vez por obra")
        for c in FECHAS:
            try:
                f(r[c])
            except ValueError:
                err(f"{c} no es una fecha AAAA-MM-DD: {r[c]!r}")
        for c, vals in VALORES.items():
            if r[c] not in vals:
                err(f"{c} no permitido: {r[c]!r}")
        for d in filter(None, r["documentos"].split(";")):
            if d.strip() not in DOCUMENTOS:
                err(f"documento no reconocido: {d!r}")
        if r.get("regimen") and rgm.regimen(r["regimen"]) is rgm.SIN_VERIFICAR:
            err(f"regimen desconocido: {r['regimen']!r} (formato «comunidad|ámbito», ver regimenes.py; vacío si no se sabe)")
        # Cada fecha se lee una sola vez; las mal escritas quedan como None y ya se han informado arriba.
        e, a, resp, rec, res, rco, rep, recep, ver = (fs(r[c]) for c in (
            "fecha_envio", "fecha_ampliacion", "fecha_respuesta", "fecha_reclamacion", "fecha_resolucion_reclamacion",
            "fecha_recepcion_organo", "fecha_replanteo", "fecha_recepcion_obra", "fecha_limite_verificada"))
        if (a or resp or rec or ver) and not e:
            err("hay fechas posteriores sin fecha_envio")
        if e and rco and rco < e:
            err("fecha_recepcion_organo anterior al envío")
        if e and a and a < e:
            err("fecha_ampliacion anterior al envío")
        if e and ver and ver <= e:
            err("fecha_limite_verificada no posterior al envío")
        if rco and ver and ver <= rco:
            err("fecha_limite_verificada no posterior a la recepción por el órgano: el cómputo empieza ahí")
        if e and a and ampliacion_imposible(r):
            err(ampliacion_imposible(r))
        if hoy and r["resultado"] == "silencio" and not resp and ver and hoy <= ver:
            err(f"resultado «silencio» anotado antes de que venza la fecha_limite_verificada ({ver})")
        if e and resp and resp < e:
            err("fecha_respuesta anterior al envío")
        lim, _ = limite_para_avisos(r)
        if r["resultado"] == "silencio" and resp and e and lim and resp <= lim:
            err("resultado «silencio» con respuesta dentro de plazo")
        if r["resultado"] == "descartada" and (e or resp or rec):
            err("«descartada» es para obras no preguntadas: no lleva fechas de envío, respuesta ni reclamación")
        if r["resultado"] and r["resultado"] not in ("silencio", "descartada") and not resp:
            err("resultado anotado sin fecha_respuesta")
        if rec and e and rec < e:
            err("fecha_reclamacion anterior al envío")
        if rep and recep and recep < rep:
            err("fecha_recepcion_obra anterior a fecha_replanteo")
        if r["resultado_reclamacion"] and not res:
            err("resultado_reclamacion sin fecha_resolucion_reclamacion")
        if res and not rec:
            err("fecha_resolucion_reclamacion sin fecha_reclamacion")
        if r["cumplimiento"] and r["cumplimiento"] != "no_aplica" and not r["resultado_reclamacion"].startswith("estimatoria"):
            err("cumplimiento anotado sin resolución estimatoria")
    return errores


def avisos(filas):
    """Avisos que no impiden validar: dependen de algo que el programa no conoce (suspensiones) y desaparecen cuando
    una persona anota la fecha_limite_verificada."""
    salida = []
    for i, r in enumerate(filas, 2):
        if r["fecha_envio"] and not r["fecha_limite_verificada"] and ampliacion_aparentemente_tardia(r):
            salida.append(f"línea {i} ({r['id_obra']}): {ampliacion_aparentemente_tardia(r)}")
    return salida


def avisos_festivos(filas):
    """Ámbitos del fichero de festivos que no coinciden con ninguna fila (una comunidad mal escrita, un órgano que no
    está en el registro): sus festivos no se aplican a nadie."""
    comunidades = {(r.get("regimen") or "").split("|")[0] for r in filas}
    organos = {r.get("organo_id") or "" for r in filas}
    conocidas = {c for c, _ in rgm.TABLA}
    salida = []
    for ambito in sorted(FESTIVOS_POR_AMBITO):
        tipo, _, nombre = ambito.partition(":")
        if tipo == "ccaa" and nombre not in conocidas:
            salida.append(f"festivos para «{nombre}»: no es una comunidad de regimenes.py (¿falta una tilde?); no se aplican")
        elif (tipo == "ccaa" and nombre not in comunidades) or (tipo == "organo" and nombre not in organos):
            salida.append(f"festivos para «{ambito}»: ninguna fila del registro coincide; no se aplican")
    return salida


def pendientes(filas, hoy):
    tareas = []
    for r in filas:
        if r["resultado"] == "descartada":
            continue
        e, (lim, verificada) = fs(r["fecha_envio"]), limite_para_avisos(r)
        reg = rgm.regimen(r.get("regimen", ""))
        if not e:
            tareas.append((hoy, r["id_obra"], "preparada sin enviar"))
            continue
        if not r["fecha_respuesta"] and not r["fecha_reclamacion"]:
            if lim is None:
                motivo = problema_ampliacion(r) or rgm.describir(r.get("regimen", ""))
                tareas.append((hoy, r["id_obra"], f"sin respuesta anotada; {motivo}: no se calcula ninguna fecha "
                                                  "(anotad fecha_limite_verificada tras comprobarla)"))
                continue
            if verificada:
                prov = ""
            else:
                prov = (" (calculado desde el envío: anotar la recepción por el órgano)" if not r["fecha_recepcion_organo"]
                        else "") + "; comprobar calendario del lugar, suspensiones y ampliación antes de reclamar"
            tipo = "vencimiento verificado" if verificada else "vencimiento provisional"
            if hoy <= lim:
                tareas.append((lim, r["id_obra"], f"esperar respuesta hasta el {lim}, {tipo}{prov}"))
            else:
                garante = f"«{r['garante'] or 'órgano de garantía'}» (sugerido, sin verificar)"
                hasta = habil(mas_meses(lim, 1), festivos_de(r))
                if reg["reclamar"] == "sin_plazo":
                    tareas.append((hasta, r["id_obra"], f"silencio desde el {lim + timedelta(days=1)}: según {reg['fuente_reclamar']}, "
                                                        f"la reclamación contra el silencio no está sujeta a plazo; el protocolo "
                                                        f"recomienda presentarla ante {garante} antes del {hasta}{prov}"))
                else:
                    aviso = "" if hoy <= hasta else " (plazo prudente vencido: consultar al órgano de garantía)"
                    tareas.append((hasta, r["id_obra"], f"silencio desde el {lim + timedelta(days=1)}: reclamar ante {garante} "
                                                        f"antes del {hasta}{aviso} ({reg['fuente_reclamar']}); verificar plazo, "
                                                        f"calendario, régimen y garante{prov}"))
        rec, res = fs(r["fecha_reclamacion"]), fs(r["fecha_resolucion_reclamacion"])
        if rec and not res:
            if reg["verificado"] and reg["garante"]:
                plazo = habil(_sumar(rec, reg["garante"], festivos_de(r)), festivos_de(r))
                estado = ("esperar resolución" if hoy <= plazo
                          else "plazo orientativo vencido: comprobar si hubo mediación, suspensión o ampliación; anotar y seguir esperando")
                tareas.append((plazo, r["id_obra"], f"reclamación del {rec}: {estado} (plazo orientativo de "
                                                    f"{rgm.texto_plazo(reg['garante'])}, {plazo}; {reg['fuente_garante']})"))
            else:
                tareas.append((hoy, r["id_obra"], f"reclamación del {rec}: plazo de resolución del órgano de garantía "
                                                  "por verificar (no localizado en la tabla de regímenes): seguimiento manual"))
        if res and r["resultado_reclamacion"] in ("estimatoria", "estimatoria_parcial") and not r["cumplimiento"]:
            revisar = res + timedelta(days=30)   # las resoluciones suelen dar 10 días hábiles; se deja margen
            tareas.append((revisar, r["id_obra"], f"comprobar desde el {revisar} si se recibió la información; "
                                                  "si no, comunicarlo al órgano de garantía y anotar «no_consta»"))
    return sorted(tareas)


def en_plazo(r, hoy):
    """«sí», «no» o vacío a la fecha de corte «hoy» (un silencio solo es «no» cuando la fecha verificada ya ha
    pasado). Solo con fecha_limite_verificada: el vencimiento calculado es provisional (puede faltar
    la recepción real, el calendario del lugar, una suspensión o la ampliación) y no basta para calificar."""
    lim, resp = fs(r["fecha_limite_verificada"]), fs(r["fecha_respuesta"])
    if not lim:
        return ""
    if resp:
        return "sí" if resp <= lim else "no"
    return "no" if r["resultado"] == "silencio" and hoy > lim else ""


def pct(a, b): return f"{100 * a / b:.1f} %" if b else "—"


def resumen(filas, hoy):
    env = [r for r in filas if r["fecha_envio"]]
    con_plazo = [r for r in env if fs(r["fecha_limite_verificada"])]
    sin_verificar = len(env) - len(con_plazo)
    vencidas = [r for r in con_plazo if r["fecha_respuesta"] or fs(r["fecha_limite_verificada"]) < hoy]
    resp_plazo = sum(en_plazo(r, hoy) == "sí" for r in vencidas)
    resp_tarde = sum(en_plazo(r, hoy) == "no" and r["fecha_respuesta"] != "" for r in vencidas)
    sin_resp = sum(not r["fecha_respuesta"] for r in vencidas)
    docs = Counter(d.strip() for r in env for d in r["documentos"].split(";") if d.strip())
    por_origen = Counter(r.get("origen") or "sin origen" for r in env)
    lineas = [
        f"Fecha del resumen: {hoy}",
        "Origen de las enviadas: " + "; ".join(f"{k} {v}" for k, v in sorted(por_origen.items()))
        + ". Solo la muestra fija aleatoria permite estimar proporciones de todas las obras; el flujo mensual puede ir "
          "priorizado y sus cifras describen lo preguntado, no la población.",
        f"Solicitudes enviadas: {len(env)}; con fecha límite verificada y el plazo ya vencido o respondidas: {len(vencidas)}"
        + (f"; sin fecha límite verificada (excluidas de las cifras de plazo): {sin_verificar}" if sin_verificar else ""),
        f"  respondidas en plazo: {resp_plazo} ({pct(resp_plazo, len(vencidas))})",
        f"  respondidas fuera de plazo: {resp_tarde} ({pct(resp_tarde, len(vencidas))})",
        f"  sin respuesta: {sin_resp} ({pct(sin_resp, len(vencidas))})",
        "  (solo filas con fecha_limite_verificada, anotada a mano tras comprobar recepción, calendario del lugar, "
        "suspensiones y ampliación; sin revisión jurídica salvo que se indique)",
        "Resultado de las respondidas: " + "; ".join(f"{k} {v}" for k, v in Counter(r["resultado"] for r in env if r["resultado"]).most_common()),
        f"Con acta de recepción recibida: {docs['acta_recepcion']} ({pct(docs['acta_recepcion'], len(env))} de las enviadas); "
        f"con certificación final: {docs['certificacion_final']}",
        "Documentos recibidos: " + "; ".join(f"{k} {v}" for k, v in docs.most_common()),
        f"Reclamaciones: {sum(bool(r['fecha_reclamacion']) for r in env)}; resultado: "
        + "; ".join(f"{k} {v}" for k, v in Counter(r["resultado_reclamacion"] for r in env if r["resultado_reclamacion"]).most_common()),
        "Cumplimiento de las estimatorias: " + "; ".join(f"{k} {v}" for k, v in Counter(r["cumplimiento"] for r in env if r["cumplimiento"]).most_common()),
    ]
    rec = [r for r in env if r["fecha_recepcion_obra"] and r["fecha_envio"]]
    if rec:
        lineas.append(f"Obras con fecha de recepción conocida: {len(rec)}")
    return "\n".join(lineas)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("orden", choices=["crear", "validar", "pendientes", "resumen", "exportar"])
    ap.add_argument("--registro", default=os.path.join(AQUI, "registro.csv"))
    ap.add_argument("--fecha", default=date.today().isoformat())
    ap.add_argument("--lote", help="con «crear»: lote.csv cuyas obras se añaden al registro")
    ap.add_argument("--organizacion", default="", help="con «crear --lote»: código (no nombre de persona) de quien envía")
    ap.add_argument("--salida", default=os.path.join(AQUI, "registro_publico_BORRADOR.csv"))
    ap.add_argument("--festivos", help="fichero con festivos autonómicos y locales: «AAAA-MM-DD» (todas las filas), "
                                       "«AAAA-MM-DD Comunidad» u «AAAA-MM-DD organo:ID», uno por línea")
    ap.add_argument("--con-identificadores", action="store_true",
                    help="con «exportar»: incluir id, enlace, expediente, órgano y garante (por defecto se omiten)")
    a = ap.parse_args()
    hoy = date.fromisoformat(a.fecha)
    if a.festivos:
        with open(a.festivos, encoding="utf-8") as fh:
            cargar_festivos(fh)

    if a.orden == "crear":
        filas = leer(a.registro) if os.path.exists(a.registro) else []
        ya = {r["id_obra"] for r in filas}
        if a.lote:
            nuevas = 0
            with open(a.lote, encoding="utf-8") as fh:
                lote = list(csv.DictReader(fh))
            # La muestra fija aleatoria es lo único que permite estimar proporciones; los lotes de flujo pueden ir priorizados.
            origen = "muestra" if "muestra" in os.path.basename(os.path.dirname(os.path.abspath(a.lote))) else "flujo"
            for r in lote:
                if r["id"] in ya:
                    continue
                filas.append({**{c: "" for c in CAMPOS}, "id_obra": r["id"], "enlace": r["enlace"],
                              "expediente": r["expediente"], "organo_id": r["organo_id"], "ambito": r["ambito"],
                              "garante": r["garante"], "regimen": r.get("regimen", ""), "origen": origen,
                              "organizacion": a.organizacion})
                nuevas += 1
            print(f"Añadidas {nuevas} obras del lote; el registro tiene {len(filas)}")
        escribir(a.registro, filas)
        return
    filas = leer(a.registro)
    if a.orden == "validar":
        errores = validar(filas, hoy)
        for aviso in avisos(filas) + avisos_festivos(filas):
            print("AVISO: " + aviso)
        print("\n".join(errores) if errores else f"Registro válido: {len(filas)} filas")
        sys.exit(1 if errores else 0)
    if a.orden == "pendientes":
        for cuando, ident, que in pendientes(filas, hoy):
            print(f"{cuando}  {ident}  {que}")
    elif a.orden == "resumen":
        print(resumen(filas, hoy))
    elif a.orden == "exportar":
        for r in filas:
            lim = limite(r)
            r["fecha_limite_provisional"] = lim.isoformat() if lim else ""
            r["en_plazo"] = en_plazo(r, hoy)   # solo con fecha_limite_verificada y a la fecha de corte --fecha
        campos = PUBLICOS if a.con_identificadores else [c for c in PUBLICOS if c not in IDENTIFICADORES]
        escribir(a.salida, filas, campos)
        if a.con_identificadores:
            print(f"BORRADOR exportado CON identificadores de obra y órgano: {len(filas)} filas -> {a.salida}. Antes de "
                  "publicarlo: decisión editorial expresa, revisión de privacidad caso por caso (los enlaces pueden llevar a "
                  "documentos con nombres y firmas) y comprobar que ninguna fila sugiere un juicio sobre un órgano o una persona.")
        else:
            print(f"BORRADOR exportado sin identificadores de obra ni de órgano: {len(filas)} filas -> {a.salida}. "
                  "Revisadlo antes de publicarlo; para incluir los identificadores hay que pedirlo con --con-identificadores.")


if __name__ == "__main__":
    main()
