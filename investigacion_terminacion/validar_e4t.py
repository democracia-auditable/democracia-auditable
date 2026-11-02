"""Validación preregistrada (PREREGISTRO.md) de la regla E4t v2 con obras de final conocido.
Aplica a las obras CON final conocido la misma búsqueda de una nueva licitación de «terminación» que la regla
(regla_e4t_v2.py, sin cambios de lógica) y compara contratos resueltos (R) con terminaciones ordinarias (N).
Lee obras.jsonl (extraer_obras.py) y ../investigacion_doc_ccn/contratos_ccn.csv.
Escribe marcadas_validacion.csv (uso local: títulos y enlaces; no publicar).
Uso: python -I -X utf8 validar_e4t.py [--regla original|modulo]
Por defecto usa protocolo_obras/senal_terminacion.py, de modo que al refinar la señal basta con cambiar ese módulo
y volver a ejecutar esta validación; «original» usa la copia congelada de la regla (regla_e4t_v2.py)."""
import csv
import json
import os
import sys
from collections import Counter
from math import exp, lgamma, log, sqrt

sys.dont_write_bytecode = True
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
# regla_e4t_v2.py y senales_medir.py son copias congeladas (con huella); las originales llevan la ruta absoluta del equipo
# donde se escribieron (en la copia publicada, sustituida). Se antepone aquí la ruta relativa de fase0_placsp para que
# funcionen en cualquier copia del proyecto.
sys.path.insert(0, os.path.join(AQUI, "..", "fase0_placsp"))
import regla_e4t_v2 as r  # noqa: E402   (importa medir_ejecucion y senales_medir)
sys.path.insert(0, os.path.join(AQUI, "..", "protocolo_obras"))
import senal_terminacion as st  # noqa: E402   (misma lógica que la regla; es el módulo que se refina)

m = r.m
DOCS_ORDINARIOS = {"recepcion_definitiva", "liquidacion", "certificacion_final", "final_obra", m.CATEGORIA_NOTA}


def cargar():
    with open(os.path.join(AQUI, "obras.jsonl"), encoding="utf-8") as f:
        return [json.loads(l) for l in f]


def preparar(obras):
    """Índices que usa la regla: frecuencia de palabras en todo el corpus y licitaciones por órgano."""
    org = lambda c: c["organo_id"] or c["organo"]  # noqa: E731
    df = Counter(w for c in obras for w in r.palabras(c["titulo"]))
    por_org = {}
    for c in obras:
        if c["primer_anuncio"]:
            por_org.setdefault(org(c), []).append((c["id"], c["primer_anuncio"], r.palabras(c["titulo"]), r.norm(c["titulo"])))
    return org, df, por_org


def marcada(c, org, df, por_org):
    """Emparejamiento de regla_e4t_v2.main() para una obra A, sin cambios. Devuelve el título de B o None."""
    raras = lambda p: {w for w in p if df[w] <= r.RARA_DF}  # noqa: E731
    ta = r.norm(c["titulo"])
    if r.AM.search(ta) or r.PARTE.search(ta):
        return None
    pa, fa, na = r.palabras(c["titulo"]), set(r.FASE.findall(ta)), r.numeros(ta)
    ra = raras(pa)
    desde = c["fecha_inicio"] or c["fecha_adjudicacion"]
    for ident, f, pb, tb in por_org.get(org(c), []):
        if ident == c["id"] or f <= desde or not pa or not pb or r.AM.search(tb) or r.PARTE.search(tb) or not r.TERMIN.search(tb):
            continue
        if len(pa & pb) / len(pa | pb) < 0.6:
            continue
        fb = set(r.FASE.findall(tb))
        if fa != fb and (fa or fb):
            continue
        nb = r.numeros(tb)
        if na and nb and not (na & nb):
            continue
        rb = raras(pb)
        if ra and len(ra & rb) / len(ra | rb) < 0.5:
            continue
        return tb
    return None


def fisher_bilateral(a, b, c, d):
    """Prueba exacta de Fisher (bilateral) para la tabla [[a, b], [c, d]]."""
    n1, n2, k, n = a + b, c + d, a + c, a + b + c + d
    lp = lambda x: (lgamma(n1 + 1) - lgamma(x + 1) - lgamma(n1 - x + 1) + lgamma(n2 + 1) - lgamma(k - x + 1)  # noqa: E731
                    - lgamma(n2 - k + x + 1) - lgamma(n + 1) + lgamma(k + 1) + lgamma(n - k + 1))
    obs = lp(a)
    return min(1.0, sum(exp(lp(x)) for x in range(max(0, k - n2), min(k, n1) + 1) if lp(x) <= obs + 1e-9))


def cociente(a, n_r, c, n_n):
    """Cociente de proporciones R/N con IC95 logarítmico (corrección de 0,5 si hay ceros)."""
    if a == 0 or c == 0:
        a, c, n_r, n_n = a + 0.5, c + 0.5, n_r + 1, n_n + 1
    rr = (a / n_r) / (c / n_n)
    se = sqrt(1 / a - 1 / n_r + 1 / c - 1 / n_n)
    return rr, exp(log(rr) - 1.96 * se), exp(log(rr) + 1.96 * se)


def main():
    obras = cargar()
    org, df, por_org = preparar(obras)
    if "--regla" in sys.argv and sys.argv[sys.argv.index("--regla") + 1] == "original":
        buscar = lambda c: marcada(c, org, df, por_org)  # noqa: E731
        print("Regla: copia congelada regla_e4t_v2.py")
    else:
        indice = st.Indice(obras)
        buscar = indice.terminacion
        print("Regla: protocolo_obras/senal_terminacion.py")
    corte = m.fecha_dia(obras[0]["corte"])
    causa = {}
    with open(os.path.join(AQUI, "..", "investigacion_doc_ccn", "contratos_ccn.csv"), encoding="utf-8") as f:
        for x in csv.DictReader(f):
            causa[x["id"]] = causa.get(x["id"], False) or bool(x["causa_codigo"])
    grupos = {"R": [], "N": []}
    for c in obras:
        p, fin = c["presupuesto_sin_iva"], m.fecha_dia(c["fin_teorico"])
        if not (c["estado"] in m.ESTADOS_ADMITIDOS and c["formalizado"] and "2019" <= c["fecha_adjudicacion"][:4] <= "2023"
                and p is not None and p >= 50_000 and fin and fin < corte):
            continue
        cats = set(c["cats"])
        resuelta = "resolucion_contrato" in cats or causa.get(c["id"], False)
        ordinaria = bool(DOCS_ORDINARIOS & cats) or (c["anuncio_finalizacion"] and c["id"] in causa and not causa[c["id"]])
        if resuelta:
            grupos["R"].append(c)
        elif ordinaria:
            grupos["N"].append(c)
    filas = []
    for g, lista in grupos.items():
        for c in lista:
            tb = buscar(c)
            c["_marca"] = tb
            if tb:
                filas.append({"grupo": g, "id": c["id"], "enlace": c["enlace"], "titulo_a": c["titulo"][:200],
                              "titulo_b": tb[:200], "presupuesto": c["presupuesto_sin_iva"]})

    def tabla(nombre, cond):
        R = [c for c in grupos["R"] if cond(c["presupuesto_sin_iva"])]
        N = [c for c in grupos["N"] if cond(c["presupuesto_sin_iva"])]
        a, cc = sum(bool(c["_marca"]) for c in R), sum(bool(c["_marca"]) for c in N)
        rr, li, ls = cociente(a, len(R), cc, len(N)) if R and N else (float("nan"),) * 3
        pf = fisher_bilateral(a, len(R) - a, cc, len(N) - cc) if R and N else float("nan")
        print(f"{nombre}: R {a}/{len(R)} ({100 * a / max(len(R), 1):.2f} %) | N {cc}/{len(N)} ({100 * cc / max(len(N), 1):.2f} %) | "
              f"cociente R/N {rr:.1f} (IC95 {li:.1f}–{ls:.1f}) | Fisher p = {pf:.2g} | "
              f"entre las marcadas, en R: {a}/{a + cc} ({100 * a / max(a + cc, 1):.0f} %)")
        return a, len(R), cc, len(N), rr, li

    print(f"corte {corte}; obras {len(obras)}; R (resueltas) {len(grupos['R'])}; N (terminación ordinaria) {len(grupos['N'])}\n")
    a, nr, cc, nn, rr, li = tabla("Principal: 50.000 € o más", lambda p: p >= 50_000)
    tabla("1 M€ o más", lambda p: p >= 1_000_000)
    tabla("50.000–200.000 €", lambda p: 50_000 <= p < 200_000)
    tabla("200.000 €–1 M€", lambda p: 200_000 <= p < 1_000_000)
    if a < 5:
        veredicto = "NO CONCLUYENTE (menos de 5 marcadas en R)"
    elif li > 1 and rr >= 3:
        veredicto = "VALIDADA como indicador de resolución"
    elif li <= 1:
        veredicto = "NO VALIDADA (el IC95 incluye 1)"
    else:
        veredicto = "INDICIO PARCIAL"
    print(f"\nVeredicto preregistrado (tabla principal): {veredicto}")
    with open(os.path.join(AQUI, "marcadas_validacion.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["grupo", "id", "enlace", "titulo_a", "titulo_b", "presupuesto"])
        w.writeheader()
        w.writerows(filas)


if __name__ == "__main__":
    main()
