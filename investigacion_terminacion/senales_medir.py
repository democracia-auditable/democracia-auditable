"""Consulta privada (NO forma parte del estudio): señales EXPLÍCITAS de problema y silencio
relativo al órgano, sobre obras.jsonl (salida de senales_extraer.py).

CRITERIOS DECLARADOS ANTES DE MEDIR (01/11/2026)
Base: obras ADJ/RES formalizadas, 1.ª adjudicación 2019–2023, presupuesto >= 1 M€, fin teórico < corte.
«Sin fin»: sin DOC_CCN vigente, sin documento candidato de fin definitivo (medir_ejecucion v2.3) y sin
  nota de modificación que hable de liquidación, recepción o finalización (hallazgo de la sesión principal).
Señales (texto normalizado de las notas cbc:Note de modificaciones + nombres de documentos):
  E1 suspensión: «suspensi», salvo contexto de licitación (oferta, licitación, procedimiento, apertura...).
  E2 resolución del contrato (acordada o en trámite): «resolución del contrato», «resolver el contrato»,
     «extinción del contrato», salvo contexto de adjudicación/licitación/clasificación.
  E3 ampliaciones repetidas: >= 2 modificaciones con plazo estructurado o con texto de ampliación/prórroga.
  E4 nueva licitación de la misma obra: otra obra (cualquier estado) del mismo órgano, con primer anuncio
     posterior a la formalización de la primera, similitud de título (Jaccard de palabras significativas)
     >= 0,6 y sin indicar una fase o lote distinto. E4t: además el título nuevo habla de terminación,
     finalización o resto de obras.
  R silencio relativo al órgano: obra sin fin cuyo órgano (>= 10 obras en la base, excluida ella)
     muestra fin en >= 50 % de sus obras.
"""
import json
import os
import re
import sys
import unicodedata
from collections import Counter, defaultdict

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fase0_placsp"))   # copia publicada: ruta local sustituida
import medir_ejecucion as m  # noqa: E402

AQUI = os.path.dirname(os.path.abspath(__file__))
CPV_SEGURIDAD = ("45234115", "45221", "45246", "45247", "452151", "45343")


def norm(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"[_\-]+", " ", s)


CTX_LICIT = re.compile(r"ofert|licitac|procedimiento|plazo de present|apertura|pliego|mesa")
SUSP = re.compile(r"suspensi")
RESOL = re.compile(r"resoluci\w*\s+(del?\s+)?(contrato|contracte)|resolver\s+el\s+contrato|extinci\w*\s+del\s+contrato")
CTX_RESOL = re.compile(r"adjudicac|licitac|clasificac")
AMPL = re.compile(r"ampliac\w*\s+(del?\s+)?(plazo|termini)|prorrog")
FIN_NOTA = re.compile(r"liquidaci|recepci|finalizaci\w*\s+de\s+(la|las)\s+obra|acta\s+de\s+recepcion")
TERMIN = re.compile(r"terminaci|finalizaci|conclusi|resto\s+de\s+(las\s+)?obras|obras\s+pendientes|completar\s+las\s+obras")
FASE = re.compile(r"\b(fase|lote|etapa|tramo)\s+([0-9ivx]+)\b")
VACIAS = set("""obras obra proyecto ejecucion construccion contrato contratacion para del las los una con por
 sus que como sobre desde hasta entre calle calles avenida plaza municipal termino municipio ayuntamiento
 mejora mejoras reforma adecuacion""".split())


def palabras(t):
    return {w for w in re.findall(r"[a-z0-9]{4,}", norm(t)) if w not in VACIAS}


def textos(c):
    return [norm(x["nota"]) for x in c["mods"] if x["nota"]] + [norm(d) for d in c["docs"]]


def main():
    obras = [json.loads(l) for l in open(os.path.join(AQUI, "obras.jsonl"), encoding="utf-8")]
    corte = m.fecha_dia(obras[0]["corte"])
    org = lambda c: c["organo_id"] or c["organo"]

    base = []
    for c in obras:
        p, fin = c["presupuesto_sin_iva"], m.fecha_dia(c["fin_teorico"])
        if (c["estado"] in m.ESTADOS_ADMITIDOS and c["formalizado"] and "2019" <= c["fecha_adjudicacion"][:4] <= "2023"
                and p is not None and p >= 1_000_000 and fin and fin < corte):
            T = textos(c)
            c["fin"] = bool(c["anuncio_finalizacion"] or (m.DOCS_FIN_DEFINITIVO & set(c["cats"]))
                            or any(FIN_NOTA.search(norm(x["nota"])) for x in c["mods"]))
            c["E1"] = any(SUSP.search(t) and not CTX_LICIT.search(t) for t in T)
            c["E2"] = any(RESOL.search(t) and not CTX_RESOL.search(t) for t in T)
            c["E3"] = sum(1 for x in c["mods"] if x["plazo"] or AMPL.search(norm(x["nota"]))) >= 2
            c["B1"] = any(cpv.startswith(CPV_SEGURIDAD) for cpv in c["cpvs"])
            c["B2"] = (c["importe_adjudicado_sin_iva"] or p) >= 10_000_000
            c["pal"] = palabras(c["titulo"])
            base.append(c)

    # E4: nuevas licitaciones del mismo órgano con título casi igual.
    por_org = defaultdict(list)
    for c in obras:
        if c["primer_anuncio"]:
            por_org[org(c)].append((c["id"], c["primer_anuncio"], palabras(c["titulo"]), norm(c["titulo"])))
    for c in base:
        c["E4"] = c["E4t"] = False
        c["E4_ej"] = ""
        desde = c["fecha_inicio"] or c["fecha_adjudicacion"]
        fases_a = set(FASE.findall(norm(c["titulo"])))
        for ident, f, pal, tit in por_org[org(c)]:
            if ident == c["id"] or f <= desde or not c["pal"] or not pal:
                continue
            j = len(c["pal"] & pal) / len(c["pal"] | pal)
            if j < 0.6:
                continue
            fases_b = set(FASE.findall(tit))
            if fases_a != fases_b and (fases_a or fases_b):
                continue
            c["E4"] = True
            c["E4_ej"] = tit[:160]
            if TERMIN.search(tit):
                c["E4t"] = True
                break

    # R: silencio relativo al órgano (tasa de fin del órgano, excluida la propia obra).
    tot, fins = Counter(), Counter()
    for c in base:
        tot[org(c)] += 1
        fins[org(c)] += c["fin"]
    for c in base:
        o = org(c)
        n_otros = tot[o] - 1
        tasa = (fins[o] - c["fin"]) / n_otros if n_otros else 0
        c["R"] = (not c["fin"]) and n_otros >= 10 and tasa >= 0.5

    sinfin = [c for c in base if not c["fin"]]
    N = len(sinfin)
    print(f"corte {corte}; base {len(base)}; sin fin {N} ({100 * N / len(base):.1f} %)")

    def informe(nombre, g):
        orgs = Counter(c["organo"] for c in g)
        top = orgs.most_common(10)
        t1 = top[0][1] if top else 0
        t10 = sum(v for _, v in top)
        print(f"{nombre}: {len(g)} ({100 * len(g) / max(N, 1):.2f} % de sin fin) | órganos {len(orgs)} | "
              f"máx. uno {t1} ({100 * t1 / max(len(g), 1):.0f} %) | 10 primeros {100 * t10 / max(len(g), 1):.0f} % | "
              f"B1 {sum(c['B1'] for c in g)} | B2 {sum(c['B2'] for c in g)}")

    for s in ("E1", "E2", "E3", "E4", "E4t", "R"):
        informe(s, [c for c in sinfin if c[s]])
    alguna = [c for c in sinfin if c["E1"] or c["E2"] or c["E4t"]]
    informe("E1|E2|E4t (explícitas fuertes)", alguna)
    informe("explícitas fuertes y (B1|B2)", [c for c in alguna if c["B1"] or c["B2"]])
    informe("R y (B1|B2)", [c for c in sinfin if c["R"] and (c["B1"] or c["B2"])])
    # En las obras CON fin, ¿cuántas tuvieron también señales? (para comparar tasas)
    confin = [c for c in base if c["fin"]]
    for s in ("E1", "E2", "E3", "E4"):
        k = sum(c[s] for c in confin)
        print(f"  con fin, {s}: {k} de {len(confin)} ({100 * k / max(len(confin), 1):.1f} %)")

    campos = ["id", "enlace", "organo", "titulo", "fecha_adjudicacion", "presupuesto_sin_iva", "fin_teorico",
              "E1", "E2", "E3", "E4", "E4t", "E4_ej", "R", "B1", "B2"]
    with open(os.path.join(AQUI, "senales_sinfin.jsonl"), "w", encoding="utf-8") as f:
        for c in sinfin:
            if c["E1"] or c["E2"] or c["E3"] or c["E4"] or c["R"]:
                f.write(json.dumps({k: c[k] for k in campos} | {"notas": [x["nota"][:300] for x in c["mods"] if x["nota"]]},
                                   ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
