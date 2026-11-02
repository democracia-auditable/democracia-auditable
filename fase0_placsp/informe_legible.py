#!/usr/bin/env python3
"""Convierte una carpeta de resultados de `medir_ejecucion.py` en material para leer sin conocimientos
técnicos:

  informe.html     página que se abre en el navegador: el resultado explicado en lenguaje llano,
                   qué significa y qué no, y la lista de obras con buscador, filtros y enlace a la
                   ficha oficial de cada una.
  lista_obras.csv  la misma lista, preparada para abrirla con doble clic en Excel o LibreOffice en
                   español (punto y coma, coma decimal, fechas dd/mm/aaaa, columnas con nombres claros).

No vuelve a analizar los datos ni cambia ninguna cifra: solo lee `resumen.json` y
`expedientes_seleccionados.csv` y aplica las mismas definiciones que `medir_ejecucion.py`
(las importa de él). Si los recuentos no cuadran con `resumen.json`, se detiene con un error.

Con --publico escribe solo informe.html, SIN la lista de obras ni lista_obras.csv: es la versión que se publica.
El proyecto no publica listas de obras con su órgano; quien quiera la lista la regenera en su ordenador repitiendo
el análisis, y puede comprobar con huellas_resultados.json que obtiene exactamente los mismos ficheros.

Uso:
    python informe_legible.py resultados_v2_4            (con la lista: uso local)
    python informe_legible.py resultados_v2_4 --publico  (sin la lista: para publicar)
"""
from __future__ import annotations

import csv
import html
import json
import os
import re
import sys
from datetime import date

from medir_ejecucion import (ANIO_ADJUDICACION, DOCS_FIN_DEFINITIVO, DOCS_FIN_PARCIAL, PRESUPUESTO_MAX,
                             PRESUPUESTO_MIN, VERSION)

# Nombre llano de cada categoría de documento candidato.
NOMBRES_DOCUMENTO = {
    "recepcion_definitiva": "Acta de recepción de la obra",
    "liquidacion": "Liquidación del contrato",
    "certificacion_final": "Certificación final de obra",
    "final_obra": "Documento de fin de obra",
    "resolucion_contrato": "Resolución (extinción anticipada) del contrato",
    "recepcion_parcial": "Recepción parcial",
    "certificacion_avance": "Certificación de avance",
    "resolucion_en_tramite": "Resolución del contrato en trámite",
    "devolucion_garantia": "Devolución de garantía",
    "documento_modificacion": "Modificación del contrato",
    "documento_prorroga": "Prórroga",
    "ampliacion_plazo": "Ampliación de plazo",
    "suspension": "Suspensión",
    "cesion_contrato": "Cesión del contrato",
    "fin_en_nota_modificacion": "Fin indicado en la nota de una modificación",
    "fin_en_nota_candidato": "Posible fin en la nota de una modificación (sin confirmar; no cuenta como final)",
}

# Situación de cada obra según lo encontrado. Clave: (texto, explicación, color).
SITUACIONES = {
    "aviso": ("Aviso oficial de finalización",
              "La administración publicó el «Anuncio de Finalización de Contrato», con la fecha real de fin.",
              "#1b7f4b"),
    "documento": ("Documento de final",
                  "Hay un documento cuyo nombre indica el final (recepción, liquidación, certificación final, "
                  "fin de obra o resolución del contrato), o una modificación cuya nota dice con una fórmula breve "
                  "que la obra terminó («se formaliza la liquidación del contrato»). Se detecta por el nombre o "
                  "por esa nota, no por el contenido de los documentos.",
                  "#2f6db5"),
    "parcial": ("Solo señales parciales",
                "Solo hay documentos de avance o de final parcial (por ejemplo, una recepción parcial).",
                "#b7791f"),
    "nada": ("Ninguna señal de final",
             "El programa no encontró ningún aviso ni documento que indique cómo terminó.",
             "#8a94a3"),
}
PLAZOS = {
    "vencido": "Ya debería haber terminado",
    "en_plazo": "Todavía en plazo",
    "sin_datos": "Sin datos de plazo",
}


def es_num(n: float, dec: int = 0) -> str:
    """Número con formato español: 1.573 · 98,7."""
    s = f"{n:,.{dec}f}"
    return s.replace(",", "\x00").replace(".", ",").replace("\x00", ".")


def es_pct(n: int, d: int) -> str:
    return f"{es_num(100 * n / d, 1)} %" if d else "—"


def es_fecha(s: str) -> str:
    return f"{s[8:10]}/{s[5:7]}/{s[:4]}" if len(s) >= 10 else ""


def limpiar_documento(etiqueta: str) -> str:
    """Quita la procedencia técnica «⟨archivo·Sección⟩» del nombre del documento."""
    return re.sub(r"\s*⟨[^⟩]*⟩\s*$", "", etiqueta).strip()


def leer(carpeta: str) -> tuple[dict, list[dict]]:
    with open(os.path.join(carpeta, "resumen.json"), encoding="utf-8") as f:
        resumen = json.load(f)
    with open(os.path.join(carpeta, "expedientes_seleccionados.csv"), encoding="utf-8-sig", newline="") as f:
        filas = list(csv.DictReader(f, delimiter=";"))
    return resumen, filas


def por_documento(documentos: dict) -> list[tuple[str, str]]:
    """Agrupa por documento: un mismo archivo puede encajar en varias categorías."""
    agrupado: dict[str, list[str]] = {}
    for cat, ds in documentos.items():
        for d in ds:
            agrupado.setdefault(d, []).append(NOMBRES_DOCUMENTO[cat])
    return [(" / ".join(cats), d) for d, cats in agrupado.items()]


def clasificar(fila: dict, corte: date) -> dict:
    documentos = {cat: [limpiar_documento(d) for d in fila.get(cat, "").split(" | ") if d.strip()]
                  for cat in NOMBRES_DOCUMENTO}
    documentos = {cat: ds for cat, ds in documentos.items() if ds}
    if fila["anuncio_finalizacion"] == "True":
        situacion = "aviso"
    elif DOCS_FIN_DEFINITIVO & documentos.keys():
        situacion = "documento"
    elif DOCS_FIN_PARCIAL & documentos.keys():
        situacion = "parcial"
    else:
        situacion = "nada"
    fin = fila["fin_teorico"][:10]
    plazo = "sin_datos" if not fin else ("vencido" if date.fromisoformat(fin) < corte else "en_plazo")

    def num(s):
        try:
            return float(s)
        except ValueError:
            return None
    return {
        "organo": fila["organo"], "expediente": fila["expediente"], "enlace": fila["enlace"],
        "presupuesto": num(fila["presupuesto_sin_iva"]), "adjudicado": num(fila["importe_adjudicado_sin_iva"]),
        "fecha_adjudicacion": fila["fecha_adjudicacion"][:10], "fin_teorico": fin,
        "fecha_aviso": fila["fecha_anuncio_finalizacion"][:10],
        "situacion": situacion, "plazo": plazo, "documentos": documentos, "por_documento": por_documento(documentos),
        "un_resultado": fila["n_resultados_adjudicados"] == "1",
        "sin_empate": fila["n_versiones_empatadas"] in ("", "1"),
    }


def cifras(obras: list[dict]) -> dict:
    venc = [o for o in obras if o["plazo"] == "vencido"]
    sin_def = [o for o in venc if o["situacion"] in ("parcial", "nada")]
    return {"total": len(obras), "vencidas": len(venc), "sin_fin": len(sin_def),
            "sin_nada": sum(o["situacion"] == "nada" for o in venc)}


def comprobar(resumen: dict, c: dict) -> None:
    esperado = {"total": resumen["expedientes_seleccionados"], "vencidas": resumen["fin_teorico_anterior_al_corte"],
                "sin_fin": resumen["vencidos_sin_candidato_fin_definitivo"],
                "sin_nada": resumen["vencidos_sin_ningun_candidato_fin"]}
    if esperado != c:
        raise SystemExit(f"Los recuentos no cuadran con resumen.json: {c} frente a {esperado}")


def escribir_csv(ruta: str, obras: list[dict]) -> None:
    def dec(x):
        return "" if x is None else f"{x:.2f}".replace(".", ",")
    with open(ruta, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["Organismo", "Expediente", "Presupuesto sin IVA (€)", "Importe adjudicado sin IVA (€)",
                    "Fecha de adjudicación", "Debería haber terminado (estimación)", "Plazo",
                    "Qué se ha encontrado", "Fecha del aviso de finalización", "Documentos encontrados",
                    "Ficha oficial"])
        for o in obras:
            docs = " | ".join(f"{cats}: {d}" for cats, d in o["por_documento"])
            w.writerow([o["organo"], o["expediente"], dec(o["presupuesto"]), dec(o["adjudicado"]),
                        es_fecha(o["fecha_adjudicacion"]), es_fecha(o["fin_teorico"]), PLAZOS[o["plazo"]],
                        SITUACIONES[o["situacion"]][0], es_fecha(o["fecha_aviso"]), docs, o["enlace"]])


def barra(c_sit: dict, total: int) -> str:
    """Barra apilada con la situación de las obras que ya deberían haber terminado."""
    partes, leyenda = [], []
    for clave in ("aviso", "documento", "parcial", "nada"):
        n = c_sit.get(clave, 0)
        texto, _, color = SITUACIONES[clave]
        ancho = max(100 * n / total, 0.6 if n else 0)
        partes.append(f'<span style="width:{ancho:.2f}%;background:{color}" title="{texto}: {es_num(n)}"></span>')
        leyenda.append(f'<li><i style="background:{color}"></i>{texto}: <b>{es_num(n)}</b></li>')
    return f'<div class="barra" role="img" aria-label="Reparto de las obras">{"".join(partes)}</div>' \
           f'<ul class="leyenda">{"".join(leyenda)}</ul>'


SECCION_PUBLICA = """<section id="lista">
<h2>La lista de obras</h2>
<p>Esta versión <b>no incluye la lista de obras</b> con su organismo. El proyecto no publica listas de casos reales:
una lista así, aunque no juzgue a nadie, permitiría señalar a organismos concretos.</p>
<p>La lista se puede regenerar en cualquier ordenador: el programa es abierto, los datos son los oficiales y el
manifiesto guarda sus huellas. Al repetir el análisis se obtiene la lista completa, con buscador y enlace a la ficha
oficial de cada obra, y con <b>huellas_resultados.json</b> se puede comprobar que los ficheros obtenidos son
exactamente los mismos que dieron estas cifras.</p>
</section>
"""
ARCHIVOS_PUBLICOS = """<section id="archivos">
<h2>Archivos de este análisis</h2>
<ul class="limpia">
<li><b>informe.html</b>: esta página.</li>
<li><b>informe.md</b>: el informe técnico completo, con todas las cifras y diagnósticos.</li>
<li><b>resumen.json</b>: las cifras en formato para programas.</li>
<li><b>manifiesto.json</b>: huellas de los datos oficiales y del programa usados.</li>
<li><b>huellas_resultados.json</b>: huellas de los ficheros por expediente que no se publican, para comprobar una repetición.</li>
</ul>
</section>"""


def escribir_html(ruta: str, resumen: dict, obras: list[dict], c: dict, metodo_relativo: str | None,
                  publico: bool = False) -> None:
    e = html.escape
    corte = resumen["fecha_de_corte_datos"]
    venc = [o for o in obras if o["plazo"] == "vencido"]
    por_sit = {k: sum(o["situacion"] == k for o in venc) for k in SITUACIONES}
    con_fin = c["vencidas"] - c["sin_fin"]
    en_plazo = sum(o["plazo"] == "en_plazo" for o in obras)
    sin_datos = sum(o["plazo"] == "sin_datos" for o in obras)
    avisos = sum(o["situacion"] == "aviso" for o in obras)

    def sensibilidad(nombre, filtro):
        sub = [o for o in obras if filtro(o)]
        cc = cifras(sub)
        return f"<tr><td>{nombre}</td><td>{es_num(cc['total'])}</td><td><b>{es_pct(cc['sin_fin'], cc['vencidas'])}</b></td></tr>"
    filas_sens = "".join([
        sensibilidad("Todas las obras seleccionadas (cifra principal)", lambda o: True),
        sensibilidad("Solo obras con un único contrato adjudicado", lambda o: o["un_resultado"]),
        sensibilidad("Sin las obras con versiones dudosas en los datos", lambda o: o["sin_empate"]),
    ])
    emp = resumen.get("empates", {})
    cotas = ""
    if emp:
        def solo_pct(t):
            m = re.search(r"\(([\d.]+) %\)", t)
            return f"{es_num(float(m.group(1)), 1)} %" if m else t
        cotas = (f"<p>Además, {es_num(emp['expedientes_empatados_relevantes'])} obras tienen en los datos dos versiones "
                 f"distintas con la misma fecha y no se puede saber cuál es la buena. Probando todas las combinaciones, "
                 f"la cifra queda entre <b>{solo_pct(emp['titular_cota_minima'])}</b> y "
                 f"<b>{solo_pct(emp['titular_cota_maxima'])}</b>.</p>")
    por_anio = resumen.get("obras_con_anuncio_finalizacion_por_anio_del_anuncio", {})
    anios = ", ".join(f"{es_num(n)} en {a}" for a, n in sorted(por_anio.items()))
    metodo = (f'<a href="{e(metodo_relativo)}">METODO.md</a>' if metodo_relativo
              else "<code>METODO.md</code> (en la carpeta del programa)")

    datos_js = json.dumps([
        [o["organo"], o["expediente"], o["enlace"], o["presupuesto"], o["fecha_adjudicacion"], o["fin_teorico"],
         o["plazo"], o["situacion"], o["fecha_aviso"],
         [list(x) for x in o["por_documento"]]]
        for o in obras], ensure_ascii=False).replace("</", "<\\/")
    sit_js = json.dumps({k: [v[0], v[2]] for k, v in SITUACIONES.items()}, ensure_ascii=False)
    plazos_js = json.dumps(PLAZOS, ensure_ascii=False)
    opciones_sit = "".join(f'<option value="{k}">{e(v[0])}</option>' for k, v in SITUACIONES.items())
    opciones_plazo = "".join(f'<option value="{k}"{" selected" if k == "vencido" else ""}>{e(v)}</option>'
                             for k, v in PLAZOS.items())
    explicacion_sit = "".join(f'<li><span class="chip" style="--c:{v[2]}">{e(v[0])}</span> {e(v[1])}</li>'
                              for v in SITUACIONES.values())

    pagina = f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>¿Cómo terminaron las obras públicas?</title>
<style>
:root {{ --fondo:#f6f7f9; --papel:#fff; --texto:#1d2733; --suave:#5a6676; --borde:#d9dee5; --acento:#16324f; --aviso:#fff6e0; --aviso-borde:#e2b04a; }}
@media (prefers-color-scheme: dark) {{
  :root {{ --fondo:#14181d; --papel:#1c2128; --texto:#e6e9ee; --suave:#a3adba; --borde:#323a45; --acento:#9cc3ec; --aviso:#2e2716; --aviso-borde:#8a6a22; }}
}}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--fondo); color:var(--texto); font:17px/1.55 "Segoe UI", system-ui, -apple-system, Roboto, Arial, sans-serif; }}
main {{ max-width:1000px; margin:0 auto; padding:24px 16px 60px; }}
h1 {{ font-size:2rem; line-height:1.2; margin:.2em 0 .1em; color:var(--acento); }}
h2 {{ font-size:1.35rem; margin:0 0 .6em; color:var(--acento); }}
.sub {{ color:var(--suave); margin:0 0 18px; }}
section {{ background:var(--papel); border:1px solid var(--borde); border-radius:12px; padding:22px 24px; margin:16px 0; }}
nav.saltos {{ display:flex; flex-wrap:wrap; gap:8px; margin:10px 0 0; }}
nav.saltos a {{ font-size:.92rem; padding:4px 12px; border:1px solid var(--borde); border-radius:999px; text-decoration:none; color:var(--texto); background:var(--papel); }}
.cifra {{ font-size:4.2rem; font-weight:700; line-height:1; color:var(--acento); margin:4px 0 8px; }}
.frase {{ font-size:1.25rem; margin:0 0 14px; }}
.barra {{ display:flex; height:28px; border-radius:6px; overflow:hidden; border:1px solid var(--borde); margin:14px 0 8px; }}
.barra span {{ display:block; height:100%; }}
.leyenda {{ list-style:none; padding:0; margin:0; display:flex; flex-wrap:wrap; gap:6px 20px; font-size:.95rem; }}
.leyenda i, .chip::before {{ display:inline-block; width:12px; height:12px; border-radius:3px; margin-right:6px; vertical-align:-1px; }}
.chip {{ white-space:nowrap; font-weight:600; }}
.chip::before {{ content:""; background:var(--c); }}
.aviso {{ background:var(--aviso); border:1px solid var(--aviso-borde); border-radius:10px; padding:14px 18px; }}
.dos {{ display:grid; grid-template-columns:1fr 1fr; gap:18px; }}
.dos h3 {{ margin:.2em 0 .4em; font-size:1.05rem; }}
ul.limpia {{ padding-left:1.2em; margin:.3em 0; }}
ul.limpia li {{ margin:.25em 0; }}
table {{ border-collapse:collapse; width:100%; }}
th, td {{ text-align:left; padding:8px 10px; border-bottom:1px solid var(--borde); vertical-align:top; }}
th {{ font-size:.85rem; text-transform:uppercase; letter-spacing:.03em; color:var(--suave); }}
td.num {{ text-align:right; white-space:nowrap; }}
.controles {{ display:flex; flex-wrap:wrap; gap:10px; margin:0 0 12px; align-items:center; }}
.controles input, .controles select {{ font:inherit; font-size:1rem; padding:7px 10px; border:1px solid var(--borde); border-radius:8px; background:var(--papel); color:var(--texto); }}
.controles input {{ flex:1 1 260px; }}
#contador {{ color:var(--suave); font-size:.95rem; margin:0 0 8px; }}
#tabla th[data-orden] {{ cursor:pointer; }}
#tabla th[data-orden]::after {{ content:"\\00a0↕"; opacity:.4; }}
#tabla .organo {{ font-size:.95rem; }}
#tabla .exp {{ color:var(--suave); font-size:.85rem; }}
#tabla .docs {{ font-size:.85rem; color:var(--suave); margin:.3em 0 0; padding-left:1.1em; }}
#tabla a {{ white-space:nowrap; }}
.tabla-caja {{ overflow-x:auto; }}
#mas {{ margin:12px 0 0; font:inherit; padding:8px 16px; border-radius:8px; border:1px solid var(--borde); background:var(--papel); color:var(--texto); cursor:pointer; }}
a {{ color:#1f5a96; }}
@media (prefers-color-scheme: dark) {{ a {{ color:#8fbdf0; }} }}
dl dt {{ font-weight:700; margin-top:.7em; }}
dl dd {{ margin:.1em 0 0 0; color:var(--suave); }}
ol li {{ margin:.35em 0; }}
footer {{ color:var(--suave); font-size:.85rem; text-align:center; margin-top:28px; }}
@media (max-width:700px) {{
  #tabla thead {{ display:none; }}
  #tabla tr {{ display:block; border-bottom:1px solid var(--borde); padding:10px 0; }}
  #tabla td {{ display:block; border:0; padding:2px 0; text-align:left; }}
  #tabla td.num::before {{ content:"Presupuesto: "; color:var(--suave); }}
  #tabla td.fin::before {{ content:"Fin previsto: "; color:var(--suave); }}
}}
@media (max-width:700px) {{ .dos {{ grid-template-columns:1fr; }} .cifra {{ font-size:3.2rem; }} section {{ padding:18px 16px; }} body {{ font-size:16px; }} }}
@media print {{ .controles, #mas, nav.saltos {{ display:none; }} body {{ background:#fff; }} section {{ break-inside:avoid; }} }}
</style>
</head>
<body>
<main>
<h1>¿Cómo terminaron las obras públicas?</h1>
<p class="sub">Lo que se puede saber, y lo que no, con los datos abiertos de la Plataforma de Contratación del Sector Público.
Datos hasta el {es_fecha(corte)}.</p>
<nav class="saltos" aria-label="Apartados">
<a href="#resultado">Resultado</a><a href="#significa">Qué significa</a><a href="#obras">Qué obras</a>
<a href="#hallazgo">Hallazgo</a><a href="#solidez">¿Es fiable?</a><a href="#lista">Lista de obras</a>
<a href="#comprobar">Compruébalo tú</a><a href="#palabras">Palabras</a><a href="#archivos">Archivos</a>
</nav>

<section id="resultado">
<h2>El resultado</h2>
<div class="cifra">{es_pct(c['sin_fin'], c['vencidas'])}</div>
<p class="frase">De las <b>{es_num(c['vencidas'])}</b> obras públicas que, según su plazo, ya deberían haber terminado,
en <b>{es_num(c['sin_fin'])}</b> no aparece en los datos públicos ninguna señal de cómo terminaron.
Solo en <b>{es_num(con_fin)}</b> hay un aviso o un documento de final.</p>
{barra(por_sit, c['vencidas'])}
</section>

<section id="significa">
<h2>Qué significa, y qué no</h2>
<div class="dos">
<div><h3>Sí significa</h3>
<ul class="limpia">
<li>Que, mirando solo estos datos abiertos, <b>casi nunca se puede saber cómo acabó una obra</b>: si se terminó, cuándo, cuánto costó al final o si se canceló.</li>
<li>Que la información del final, si existe, <b>no se está publicando en este canal</b> de forma que se pueda encontrar.</li>
</ul></div>
<div><h3>No significa</h3>
<ul class="limpia">
<li>Que las obras estén sin terminar.</li>
<li>Que falten los documentos: pueden estar en otro sitio, como el Registro de Contratos del Sector Público o los registros autonómicos.</li>
<li>Que alguien incumpla ninguna obligación.</li>
</ul></div>
</div>
<p class="aviso">El programa busca <b>avisos, nombres de documentos y notas de las modificaciones</b>; no lee el contenido de los documentos. Es una medición exploratoria
que no ha revisado ningún jurista ni estadístico. Antes de citar la cifra, lee {metodo}.</p>
</section>

<section id="obras">
<h2>Qué obras se han mirado</h2>
<ul class="limpia">
<li>Contratos de <b>obras</b> publicados en la Plataforma de Contratación del Sector Público.</li>
<li>Adjudicados por primera vez en <b>{ANIO_ADJUDICACION}</b>.</li>
<li>Con un presupuesto de entre <b>{es_num(PRESUPUESTO_MIN / 1e6)} y {es_num(PRESUPUESTO_MAX / 1e6)} millones de euros</b> sin IVA: ni obras pequeñas ni grandes infraestructuras.</li>
</ul>
<p>Son <b>{es_num(c['total'])}</b> obras. De ellas, <b>{es_num(c['vencidas'])}</b> ya deberían haber terminado según el plazo
que figura en el contrato, {es_num(en_plazo)} siguen en plazo y en {es_num(sin_datos)} faltan datos para calcularlo.
El plazo es una <b>estimación</b> (inicio más duración prevista, o la de la última modificación publicada): las ampliaciones no publicadas pueden alargarlo.</p>
</section>

<section id="hallazgo">
<h2>El hallazgo: el aviso de finalización ya existe, pero casi no se usa</h2>
<p>La plataforma permite publicar un <b>«Anuncio de Finalización de Contrato»</b>, con la fecha real en que terminó y el motivo.
Es justo la información que falta. Entre estas {es_num(c['total'])} obras, solo aparece en <b>{es_num(avisos)}</b>.</p>
{f"<p>En toda la plataforma, contando todas las obras, se publicaron {anios}.</p>" if anios else ""}
<p>Es decir: no haría falta inventar nada nuevo para saber cómo terminan las obras, sino usar lo que ya existe.</p>
</section>

<section id="solidez">
<h2>¿Es fiable la cifra?</h2>
<p>Se ha repetido el cálculo quitando los casos que podían dar problemas. La cifra apenas cambia:</p>
<div class="tabla-caja"><table>
<thead><tr><th>Cálculo</th><th>Obras</th><th>Sin señal de final</th></tr></thead>
<tbody>{filas_sens}</tbody>
</table></div>
{cotas}
<p>También se revisaron a mano muestras de obras, ficha por ficha, para ver si el programa se dejaba casos. El detalle está en {metodo}.</p>
</section>

<section id="lista">
<h2>Lista de obras</h2>
<p>Cada obra tiene un enlace a su <b>ficha oficial</b>, donde se pueden ver todos sus documentos. Qué quiere decir cada color:</p>
<ul class="limpia">{explicacion_sit}</ul>
<div class="controles">
<input id="buscar" type="search" placeholder="Buscar organismo o expediente (por ejemplo, Ayuntamiento de…)" aria-label="Buscar">
<select id="f-plazo" aria-label="Plazo"><option value="">Todos los plazos</option>{opciones_plazo}</select>
<select id="f-sit" aria-label="Qué se ha encontrado"><option value="">Todo lo encontrado</option>{opciones_sit}</select>
</div>
<p id="contador"></p>
<div class="tabla-caja"><table id="tabla">
<thead><tr><th data-orden="0">Organismo y expediente</th><th data-orden="3">Presupuesto</th>
<th data-orden="5">Debería haber terminado</th><th data-orden="7">Qué se ha encontrado</th><th>Ficha</th></tr></thead>
<tbody></tbody>
</table></div>
<button id="mas" type="button">Ver más obras</button>
<p>La misma lista se puede abrir con Excel: <a href="lista_obras.csv">lista_obras.csv</a>.</p>
</section>

<section id="comprobar">
<h2>Cómo comprobar una obra tú mismo</h2>
<ol>
<li>En la lista de arriba, pulsa <b>«Ver ficha»</b> en la obra que te interese. Se abre su página en la web oficial de la Plataforma de Contratación.</li>
<li>Busca el apartado de <b>documentos</b> y los <b>anuncios publicados</b> (adjudicación, formalización, modificaciones…).</li>
<li>Mira si hay algo que indique el final: un <b>anuncio de finalización</b>, un <b>acta de recepción</b>, una <b>liquidación</b>, una <b>certificación final</b>, una <b>resolución del contrato</b> o una <b>modificación</b> cuyo texto diga que la obra terminó.</li>
<li>Si encuentras algo que el programa no detectó, es justo el tipo de error que conviene conocer: anótalo.</li>
</ol>
<p>Si la obra no aparece en la Plataforma, puede consultarse al organismo o en el portal de transparencia correspondiente.</p>
</section>

<section id="palabras">
<h2>Palabras que aparecen</h2>
<dl>
<dt>Plataforma de Contratación del Sector Público (PLACSP)</dt><dd>La web del Ministerio de Hacienda donde las administraciones publican sus contratos. Publica sus datos en abierto para descargarlos.</dd>
<dt>Expediente</dt><dd>Cada contratación, con su número. Una obra puede dividirse en varios lotes y contratos dentro del mismo expediente.</dd>
<dt>Adjudicación</dt><dd>Cuando la administración decide qué empresa hará la obra.</dd>
<dt>Presupuesto sin IVA</dt><dd>Lo que la administración preveía gastar, antes de impuestos, al sacar la obra a concurso.</dd>
<dt>Debería haber terminado</dt><dd>Fecha estimada: inicio de la obra más la duración prevista en el contrato o, si se publicó una modificación que cambia el plazo, la duración de la última publicada. No incluye las ampliaciones que no se publicaron.</dd>
<dt>Acta de recepción</dt><dd>Documento en el que la administración da por recibida la obra terminada.</dd>
<dt>Liquidación</dt><dd>Cuenta final de lo que costó la obra.</dd>
<dt>Certificación final</dt><dd>Medición y valoración de todo lo construido al acabar.</dd>
<dt>Resolución del contrato</dt><dd>Cuando el contrato se termina antes de tiempo, por ejemplo por incumplimiento.</dd>
<dt>Nota de una modificación</dt><dd>Texto breve que acompaña al anuncio de una modificación del contrato. Algunos organismos lo usan para comunicar el final («se formaliza la liquidación del contrato»); el programa solo lo cuenta si es una de esas fórmulas.</dd>
<dt>Anuncio de Finalización de Contrato</dt><dd>Aviso estructurado de la Plataforma con la fecha real de fin y la causa.</dd>
</dl>
</section>

<section id="archivos">
<h2>Archivos de este análisis</h2>
<ul class="limpia">
<li><b>informe.html</b>: esta página.</li>
<li><b>lista_obras.csv</b>: la lista de obras para Excel o LibreOffice.</li>
<li><b>informe.md</b>: el informe técnico completo, con todas las cifras y diagnósticos.</li>
<li><b>expedientes_seleccionados.csv</b> y <b>candidatos_fin.csv</b>: los datos técnicos completos, columna a columna.</li>
<li><b>manifiesto.json</b>: huellas de los ficheros y del programa, para comprobar que nadie los ha cambiado.</li>
</ul>
</section>

<footer>Programa v{e(VERSION)} · Sin inteligencia artificial: solo reglas fijas sobre los datos oficiales ·
Datos: Ministerio de Hacienda, Plataforma de Contratación del Sector Público</footer>
</main>
<script>
const OBRAS = {datos_js};
const SIT = {sit_js};
const PLAZOS = {plazos_js};
const PASO = 100;
let visibles = PASO, orden = null, asc = true;
const cuerpo = document.querySelector("#tabla tbody");
const fmtEur = new Intl.NumberFormat("es-ES", {{style:"currency", currency:"EUR", maximumFractionDigits:0}});
const fmtNum = {{format: n => String(n).replace(/\\B(?=(\\d{{3}})+(?!\\d))/g, ".")}};   // 1.593 (Intl no agrupa 4 cifras)
const fecha = s => s ? s.slice(8,10) + "/" + s.slice(5,7) + "/" + s.slice(0,4) : "—";
const esc = s => String(s).replace(/[&<>"]/g, c => ({{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}}[c]));
const sinTildes = s => s.normalize("NFD").replace(/[\\u0300-\\u036f]/g, "").toLowerCase();
function filtradas() {{
  const q = sinTildes(document.getElementById("buscar").value.trim());
  const fp = document.getElementById("f-plazo").value, fs = document.getElementById("f-sit").value;
  let r = OBRAS.filter(o => (!fp || o[6] === fp) && (!fs || o[7] === fs) &&
    (!q || sinTildes(o[0] + " " + o[1]).includes(q)));
  if (orden !== null) r = r.slice().sort((a, b) => {{
    const x = a[orden] ?? "", y = b[orden] ?? "";
    return (x < y ? -1 : x > y ? 1 : 0) * (asc ? 1 : -1);
  }});
  return r;
}}
function pintar() {{
  const r = filtradas();
  document.getElementById("contador").textContent =
    fmtNum.format(r.length) + (r.length === 1 ? " obra" : " obras") + " con estos filtros";
  cuerpo.innerHTML = r.slice(0, visibles).map(o => {{
    const [texto, color] = SIT[o[7]];
    const aviso = o[8] ? " (" + fecha(o[8]) + ")" : "";
    const docs = o[9].length ? '<ul class="docs">' + o[9].map(d => "<li>" + esc(d[0]) + ": " + esc(d[1]) + "</li>").join("") + "</ul>" : "";
    return "<tr><td><div class=organo>" + esc(o[0]) + "</div><div class=exp>Expediente " + esc(o[1]) + "</div></td>" +
      "<td class=num>" + (o[3] == null ? "—" : fmtEur.format(o[3])) + "</td>" +
      "<td class=fin>" + fecha(o[5]) + "<div class=exp>" + esc(PLAZOS[o[6]]) + "</div></td>" +
      '<td><span class=chip style="--c:' + color + '">' + esc(texto) + aviso + "</span>" + docs + "</td>" +
      '<td><a href="' + esc(o[2]) + '" target="_blank" rel="noopener">Ver ficha</a></td></tr>';
  }}).join("") || '<tr><td colspan="5">Ninguna obra coincide con la búsqueda. Prueba con menos palabras o quita los filtros.</td></tr>';
  document.getElementById("mas").style.display = r.length > visibles ? "" : "none";
}}
document.getElementById("buscar").addEventListener("input", () => {{ visibles = PASO; pintar(); }});
document.getElementById("f-plazo").addEventListener("change", () => {{ visibles = PASO; pintar(); }});
document.getElementById("f-sit").addEventListener("change", () => {{ visibles = PASO; pintar(); }});
document.getElementById("mas").addEventListener("click", () => {{ visibles += PASO; pintar(); }});
document.querySelectorAll("#tabla th[data-orden]").forEach(th => th.addEventListener("click", () => {{
  const k = Number(th.dataset.orden);
  asc = orden === k ? !asc : true; orden = k; pintar();
}}));
pintar();
</script>
</body>
</html>
"""
    if publico:
        # Sin la lista de obras: fuera la sección de la lista, la de comprobar una obra, los datos y el programa que los pinta.
        pagina, n = re.subn(r'<section id="lista">.*?</section>\s*<section id="comprobar">.*?</section>\s*',
                            SECCION_PUBLICA + "\n", pagina, flags=re.S)
        pagina, m = re.subn(r'<section id="archivos">.*?</section>', ARCHIVOS_PUBLICOS, pagina, flags=re.S)
        pagina, k = re.subn(r"<script>.*?</script>\s*", "", pagina, flags=re.S)
        pagina = pagina.replace('<a href="#lista">Lista de obras</a>', '<a href="#lista">La lista de obras</a>')
        pagina = pagina.replace('\n<a href="#comprobar">Compruébalo tú</a>', "\n")
        assert (n, m, k) == (1, 1, 1), "no se pudo quitar la lista del informe público"
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(pagina)


def generar(carpeta: str, carpeta_programa: str | None = None, publico: bool = False) -> dict:
    """Escribe informe.html y lista_obras.csv en `carpeta` (con publico=True, solo informe.html, sin la lista).
    Devuelve las cifras principales."""
    resumen, filas = leer(carpeta)
    corte = date.fromisoformat(resumen["fecha_de_corte_datos"])
    obras = sorted((clasificar(f, corte) for f in filas), key=lambda o: (o["organo"], o["expediente"]))
    c = cifras(obras)
    comprobar(resumen, c)
    carpeta_programa = carpeta_programa or os.path.dirname(os.path.abspath(__file__))
    metodo = os.path.join(carpeta_programa, "METODO.md")
    relativo = None
    if os.path.exists(metodo):
        try:
            rel = os.path.relpath(metodo, os.path.abspath(carpeta))
        except ValueError:                                 # otra unidad de disco en Windows
            rel = ""
        if rel and not rel.startswith(".." + os.sep + ".."):   # solo si la carpeta está junto al programa
            relativo = rel.replace(os.sep, "/")
    if not publico:
        escribir_csv(os.path.join(carpeta, "lista_obras.csv"), obras)
    escribir_html(os.path.join(carpeta, "informe.html"), resumen, obras, c, relativo, publico)
    return {**c, "porcentaje": es_pct(c["sin_fin"], c["vencidas"]), "corte": es_fecha(resumen["fecha_de_corte_datos"])}


def main() -> None:
    args = [a for a in sys.argv[1:] if a != "--publico"]
    publico = "--publico" in sys.argv[1:]
    if len(args) != 1:
        raise SystemExit(__doc__)
    r = generar(args[0], publico=publico)
    escritos = "informe.html (público, sin la lista de obras)" if publico else "informe.html y lista_obras.csv"
    print(f"{escritos} escritos en {args[0]}: {r['sin_fin']} de {r['vencidas']} ({r['porcentaje']}) sin señal de final.")


if __name__ == "__main__":
    main()
