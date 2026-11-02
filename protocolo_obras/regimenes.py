"""Régimen jurídico de cada solicitud: plazo para resolver, ampliación, plazo para reclamar contra el silencio y plazo
del órgano de garantía para resolver la reclamación.

Lectura de un NO JURISTA de los textos consolidados del BOE (API de datos abiertos, consultados el 02/11/2026; los
fragmentos están en fuentes/regimenes/, con el artículo de ámbito subjetivo cuando decide si la ley alcanza a las
entidades locales). No sustituye al asesoramiento jurídico: cada fecha que se calcule con esta tabla es una ayuda
PROVISIONAL que hay que comprobar antes de reclamar (fecha real de recepción, calendario del lugar, suspensiones,
notificación de la ampliación).

El régimen depende de quién resuelve (Administración del Estado, autonómica o local) y de la comunidad autónoma
del órgano, no del órgano de garantía: una comunidad con convenio con el Consejo de Transparencia y Buen Gobierno
(Extremadura, por ejemplo) mantiene el plazo para resolver de su propia ley.

Reglas generales:
- Ley 19/2013 (LTAIBG), art. 20.1: un mes desde la recepción por el órgano competente, ampliable por otro mes.
- LTAIBG, art. 24.2: reclamación en un mes desde el día siguiente a la notificación o a los efectos del silencio.
- LTAIBG, art. 24.4: el Consejo de Transparencia y Buen Gobierno resuelve la reclamación en tres meses.
- Ley 39/2015, art. 30.2: los plazos en días que no digan otra cosa son hábiles ("veinte días" = veinte hábiles).
Las leyes autonómicas que fijan otro plazo se aplican a los sujetos de su ámbito. Cuando una ley autonómica no
incluye a las entidades locales en su ámbito, o no fija plazo propio, rige la LTAIBG (básica).

Campos de cada régimen:
- plazo: (n, "meses" | "dias_habiles"), o None si no está verificado.
- ampliacion: lo que añade una ampliación notificada a tiempo, (n, unidad); None si la ley la prevé de una forma
  que no se automatiza (Cataluña: "hasta la mitad del plazo inicial") o si no consta: con una ampliación anotada,
  entonces no se calcula ninguna fecha.
- reclamar: "un_mes" | "sin_plazo" (contra el silencio).
- garante: plazo del órgano de garantía para resolver la reclamación, (n, unidad), o None si no se ha localizado en
  el texto: entonces el seguimiento es manual.
Si el régimen no está verificado (tipo de entidad sin ámbito claro, comunidad desconocida o aplicación dudosa),
las herramientas NO calculan fechas: avisan de que hay que verificar el régimen a mano.
"""

LTAIBG_RESOLVER = "Ley 19/2013, art. 20.1 (BOE-A-2013-12887)"
LTAIBG_RECLAMAR = "Ley 19/2013, art. 24.2 (BOE-A-2013-12887)"
LTAIBG_GARANTE = "Ley 19/2013, art. 24.4 (BOE-A-2013-12887)"
ESTATAL = {"1", "6", "9"}               # ContractingAuthorityCode-2.10
AUTONOMICO = {"2", "7", "10"}
LOCAL = {"3", "8", "11"}

UN_MES = (1, "meses")
TRES_MESES = (3, "meses")


def _r(plazo, fuente, ampliacion=UN_MES, fuente_ampliacion=LTAIBG_RESOLVER, reclamar="un_mes",
       fuente_reclamar=LTAIBG_RECLAMAR, garante=None, fuente_garante="", verificado=True, nota=""):
    return {"plazo": plazo, "fuente": fuente, "ampliacion": ampliacion, "fuente_ampliacion": fuente_ampliacion,
            "reclamar": reclamar, "fuente_reclamar": fuente_reclamar, "garante": garante,
            "fuente_garante": fuente_garante, "verificado": verificado, "nota": nota}


GENERAL = _r(UN_MES, LTAIBG_RESOLVER, garante=TRES_MESES, fuente_garante=LTAIBG_GARANTE)

# (comunidad, "autonómico" | "local") -> régimen.
TABLA = {
    ("Estado", "estatal"): GENERAL,
    ("Andalucía", "autonómico"): _r((20, "dias_habiles"), "Ley 1/2014 de Andalucía, art. 32 (BOE-A-2014-7534): 20 días "
                                    "hábiles en la Junta y sus entidades instrumentales",
                                    ampliacion=(20, "dias_habiles"), fuente_ampliacion="Ley 1/2014 de Andalucía, art. 32: "
                                    "«prorrogables por igual período»",
                                    fuente_reclamar="Ley 1/2014 de Andalucía, art. 33 (remite a la legislación básica); " + LTAIBG_RECLAMAR),
    ("Andalucía", "local"): _r(UN_MES, LTAIBG_RESOLVER + "; el art. 32 de la Ley 1/2014 limita los 20 días hábiles a la Junta",
                               fuente_reclamar="Ley 1/2014 de Andalucía, art. 33; " + LTAIBG_RECLAMAR),
    ("Aragón", "autonómico"): _r(UN_MES, "Ley 8/2015 de Aragón, art. 31 (BOE-A-2015-5332)",
                                 fuente_ampliacion="Ley 8/2015 de Aragón, art. 31: «por otro mes»",
                                 fuente_reclamar="Ley 8/2015 de Aragón, art. 36", garante=TRES_MESES,
                                 fuente_garante="Ley 8/2015 de Aragón, art. 36.4"),
    ("Aragón", "local"): _r(UN_MES, "Ley 8/2015 de Aragón, art. 31 (art. 4.1.c incluye la Administración local)",
                            fuente_ampliacion="Ley 8/2015 de Aragón, art. 31: «por otro mes»",
                            fuente_reclamar="Ley 8/2015 de Aragón, art. 36", garante=TRES_MESES,
                            fuente_garante="Ley 8/2015 de Aragón, art. 36.4"),
    ("Canarias", "autonómico"): _r(UN_MES, "Ley 12/2014 de Canarias, art. 46 (BOE-A-2015-1114)",
                                   fuente_ampliacion="Ley 12/2014 de Canarias, art. 46: «por otro mes»",
                                   fuente_reclamar="Ley 12/2014 de Canarias, art. 53"),
    ("Canarias", "local"): _r(UN_MES, "Ley 12/2014 de Canarias, art. 46 (art. 2 incluye cabildos y ayuntamientos)",
                              fuente_ampliacion="Ley 12/2014 de Canarias, art. 46: «por otro mes»",
                              fuente_reclamar="Ley 12/2014 de Canarias, art. 53"),
    ("Cantabria", "autonómico"): _r(UN_MES, "Ley 1/2018 de Cantabria, art. 13 (BOE-A-2018-5393)",
                                    fuente_ampliacion="Ley 1/2018 de Cantabria, art. 13: «por otro mes»", reclamar="sin_plazo",
                                    fuente_reclamar="Ley 1/2018 de Cantabria, art. 18: contra el silencio, «no estará sujeta a plazo»",
                                    garante=TRES_MESES, fuente_garante="Ley 1/2018 de Cantabria, art. 18.4"),
    ("Cantabria", "local"): _r(UN_MES, "Ley 1/2018 de Cantabria, art. 13 (art. 4.2 incluye la Administración local)",
                               fuente_ampliacion="Ley 1/2018 de Cantabria, art. 13: «por otro mes»", reclamar="sin_plazo",
                               fuente_reclamar="Ley 1/2018 de Cantabria, art. 18", garante=TRES_MESES,
                               fuente_garante="Ley 1/2018 de Cantabria, art. 18.4"),
    # El art. 33.1 de la Ley 4/2016 fija el mes solo para los sujetos de su art. 4.1.a (la Junta y sus entidades de
    # derecho público); el art. 4.2 remite a las entidades locales a la legislación básica. El plazo numérico es el
    # mismo (un mes), pero la fuente que lo prueba para los demás sujetos es la LTAIBG.
    ("Castilla-La Mancha", "autonómico"): _r(UN_MES, "Ley 4/2016 de Castilla-La Mancha, art. 33.1 (BOE-A-2017-1373), para "
                                             "los sujetos de su art. 4.1.a; para el resto, " + LTAIBG_RESOLVER,
                                             fuente_reclamar="Ley 4/2016 de Castilla-La Mancha, art. 64.2", garante=TRES_MESES,
                                             fuente_garante="Ley 4/2016 de Castilla-La Mancha, art. 64.4"),
    ("Castilla-La Mancha", "local"): _r(UN_MES, LTAIBG_RESOLVER + "; el art. 4.2 de la Ley 4/2016 de Castilla-La Mancha "
                                        "remite a las entidades locales a la legislación básica",
                                        fuente_reclamar=LTAIBG_RECLAMAR + " (un mes también en el art. 64.2 de la Ley 4/2016)",
                                        garante=TRES_MESES, fuente_garante=LTAIBG_GARANTE + " (tres meses también en el "
                                                                                            "art. 64.4 de la Ley 4/2016)"),
    # La Ley 3/2015 de Castilla y León no fija plazo propio para resolver el acceso (su art. 9 trata de la
    # reutilización): rige la LTAIBG. La reclamación ante la Comisión de Transparencia se ajusta al art. 24 LTAIBG.
    ("Castilla y León", "autonómico"): _r(UN_MES, LTAIBG_RESOLVER + "; la Ley 3/2015 de Castilla y León (BOE-A-2015-3281) no "
                                          "fija plazo propio para el acceso",
                                          fuente_reclamar="Ley 3/2015 de Castilla y León, art. 8.2 (remite al art. 24 de la "
                                                          "Ley 19/2013); " + LTAIBG_RECLAMAR,
                                          garante=TRES_MESES, fuente_garante="Ley 3/2015 de Castilla y León, art. 8.2; " + LTAIBG_GARANTE),
    ("Castilla y León", "local"): _r(UN_MES, LTAIBG_RESOLVER,
                                     fuente_reclamar="Ley 3/2015 de Castilla y León, art. 8 (incluye las entidades locales); "
                                                     + LTAIBG_RECLAMAR,
                                     garante=TRES_MESES, fuente_garante="Ley 3/2015 de Castilla y León, art. 8.2; " + LTAIBG_GARANTE),
    # Cataluña: prórroga "hasta un plazo igual a la mitad del inicial" (no se automatiza) y la GAIP resuelve en DOS
    # meses (art. 42.9), con la mediación suspendiendo el plazo (art. 42.4) y una ampliación posible de quince días.
    ("Cataluña", "autonómico"): _r(UN_MES, "Ley 19/2014 de Cataluña, art. 33.1 (BOE-A-2015-470)", ampliacion=None,
                                   fuente_ampliacion="Ley 19/2014 de Cataluña, art. 33.2: prórroga «hasta un plazo igual a "
                                                     "la mitad del inicial»; su cómputo no se automatiza",
                                   fuente_reclamar="Ley 19/2014 de Cataluña, art. 42.1: un mes desde que finaliza el plazo "
                                                   "para resolver",
                                   garante=(2, "meses"), fuente_garante="Ley 19/2014 de Cataluña, art. 42.9: dos meses desde "
                                   "la presentación; la mediación suspende el plazo (art. 42.4) y la Comisión puede ampliarlo "
                                   "hasta quince días (art. 42.9)"),
    ("Cataluña", "local"): _r(UN_MES, "Ley 19/2014 de Cataluña, art. 33.1 (art. 3.1.a incluye la Administración local)",
                              ampliacion=None, fuente_ampliacion="Ley 19/2014 de Cataluña, art. 33.2: prórroga «hasta un "
                                                                 "plazo igual a la mitad del inicial»; su cómputo no se automatiza",
                              fuente_reclamar="Ley 19/2014 de Cataluña, art. 42.1",
                              garante=(2, "meses"), fuente_garante="Ley 19/2014 de Cataluña, art. 42.9: dos meses; la "
                              "mediación suspende el plazo (art. 42.4) y la Comisión puede ampliarlo hasta quince días"),
    ("Comunitat Valenciana", "autonómico"): _r(UN_MES, "Ley 1/2022 de la Comunitat Valenciana, art. 34 (BOE-A-2022-8187): "
                                               "desde la entrada en el registro del órgano competente",
                                               fuente_ampliacion="Ley 1/2022 de la Comunitat Valenciana, art. 34: «por un "
                                                                 "mes más», mediante resolución motivada notificada",
                                               fuente_reclamar="Ley 1/2022 de la Comunitat Valenciana, art. 38",
                                               garante=TRES_MESES, fuente_garante="Ley 1/2022 de la Comunitat Valenciana, "
                                                                                  "art. 38: tres meses desde la recepción"),
    ("Comunitat Valenciana", "local"): _r(UN_MES, "Ley 1/2022 de la Comunitat Valenciana, art. 34 (art. 3.1.d incluye la "
                                          "Administración local)",
                                          fuente_ampliacion="Ley 1/2022 de la Comunitat Valenciana, art. 34: «por un mes más»",
                                          fuente_reclamar="Ley 1/2022 de la Comunitat Valenciana, art. 38",
                                          garante=TRES_MESES, fuente_garante="Ley 1/2022 de la Comunitat Valenciana, art. 38"),
    ("Extremadura", "autonómico"): _r((30, "dias_habiles"), "Ley 4/2013 de Extremadura, art. 23 (BOE-A-2013-6050): 30 días "
                                      "hábiles", ampliacion=(30, "dias_habiles"),
                                      fuente_ampliacion="Ley 4/2013 de Extremadura, art. 23: «por otros treinta días más»",
                                      fuente_reclamar="Ley 4/2013 de Extremadura, art. 25 (remite a la legislación básica); "
                                                      + LTAIBG_RECLAMAR),
    ("Extremadura", "local"): _r((30, "dias_habiles"), "Ley 4/2013 de Extremadura, art. 23 (art. 2.c incluye la Administración local)",
                                 ampliacion=(30, "dias_habiles"),
                                 fuente_ampliacion="Ley 4/2013 de Extremadura, art. 23: «por otros treinta días más»",
                                 fuente_reclamar="Ley 4/2013 de Extremadura, art. 25; " + LTAIBG_RECLAMAR),
    # Galicia: el art. 27.4 fija un mes «como más tarde» y no menciona ampliación (el art. 27.1 remite la tramitación a
    # la normativa básica): con una ampliación anotada no se calcula fecha. El art. 3.1 no incluye a las entidades
    # locales: para ellas rige la LTAIBG. El art. 27.2 prevé la suspensión por alegaciones de terceros.
    ("Galicia", "autonómico"): _r(UN_MES, "Ley 1/2016 de Galicia, art. 27.4 (BOE-A-2016-3190)", ampliacion=None,
                                  fuente_ampliacion="Ley 1/2016 de Galicia, art. 27: no menciona ampliación; si el órgano "
                                                    "la notifica, verificar a mano",
                                  nota="no se localizó en la ley gallega una regla propia sobre el plazo de reclamación"),
    ("Galicia", "local"): _r(UN_MES, LTAIBG_RESOLVER + "; el art. 3.1 de la Ley 1/2016 de Galicia no incluye a las "
                                                       "entidades locales"),
    ("Comunidad de Madrid", "autonómico"): _r((20, "dias_habiles"), "Ley 10/2019 de la Comunidad de Madrid, art. 42 "
                                              "(BOE-A-2019-10102): veinte días (hábiles: Ley 39/2015, art. 30.2)",
                                              ampliacion=(20, "dias_habiles"),
                                              fuente_ampliacion="Ley 10/2019 de la Comunidad de Madrid, art. 42: «por otros "
                                                                "veinte días más»",
                                              fuente_reclamar="Ley 10/2019 de la Comunidad de Madrid, art. 48 (un mes); el Consejo de "
                                                              "Transparencia y Participación aplica un criterio de no preclusión "
                                                              "contra el silencio (criterio de 09/10/2025)"),
    ("Comunidad de Madrid", "local"): _r((20, "dias_habiles"), "Ley 10/2019 de la Comunidad de Madrid, art. 42 y disposición "
                                         "adicional octava: se aplica a las entidades locales «en todo aquello que no afecte a la "
                                         "autonomía local»", ampliacion=(20, "dias_habiles"),
                                         fuente_ampliacion="Ley 10/2019, art. 42", fuente_reclamar="Ley 10/2019, art. 48",
                                         verificado=False,
                                         nota="aplicación del plazo de 20 días a las entidades locales dudosa: verificar con el órgano"),
    ("Región de Murcia", "autonómico"): _r((20, "dias_habiles"), "Ley 12/2014 de la Región de Murcia, art. 26 (BOE-A-2015-184): "
                                           "veinte días (hábiles: Ley 39/2015, art. 30.2)", ampliacion=(20, "dias_habiles"),
                                           fuente_ampliacion="Ley 12/2014 de la Región de Murcia, art. 26: «ampliable a otros "
                                                             "veinte días»",
                                           nota="no se localizó en la ley murciana una regla propia sobre el plazo de reclamación"),
    ("Región de Murcia", "local"): _r(UN_MES, LTAIBG_RESOLVER + "; el art. 5 de la Ley 12/2014 no incluye a las entidades locales"),
    ("Comunidad Foral de Navarra", "autonómico"): _r(UN_MES, "Ley Foral 5/2018, art. 41 (BOE-A-2018-7642): desde la entrada en "
                                                     "el registro del órgano competente",
                                                     fuente_ampliacion="Ley Foral 5/2018, art. 41: «por otro mes más»",
                                                     reclamar="sin_plazo",
                                                     fuente_reclamar="Ley Foral 5/2018, art. 45: contra el silencio, «en "
                                                                     "cualquier momento»",
                                                     garante=TRES_MESES, fuente_garante="Ley Foral 5/2018, art. 45.5"),
    ("Comunidad Foral de Navarra", "local"): _r(UN_MES, "Ley Foral 5/2018, art. 41 (art. 2.1.c incluye las entidades locales)",
                                                fuente_ampliacion="Ley Foral 5/2018, art. 41: «por otro mes más»",
                                                reclamar="sin_plazo", fuente_reclamar="Ley Foral 5/2018, art. 45",
                                                garante=TRES_MESES, fuente_garante="Ley Foral 5/2018, art. 45.5"),
    # Euskadi: la ampliación es de QUINCE DÍAS (art. 37.2), no de otro mes; «días» sin más son hábiles (Ley 39/2015,
    # art. 30.2).
    ("País Vasco", "autonómico"): _r(UN_MES, "Ley 3/2026 de Transparencia de Euskadi, art. 37.1 (BOE-A-2026-11851)",
                                     ampliacion=(15, "dias_habiles"),
                                     fuente_ampliacion="Ley 3/2026 de Euskadi, art. 37.2: «por otros quince días más» "
                                                       "(hábiles: Ley 39/2015, art. 30.2)",
                                     reclamar="sin_plazo", fuente_reclamar="Ley 3/2026 de Euskadi, art. 40.2.a: contra el "
                                                                           "silencio, «en cualquier momento»",
                                     garante=TRES_MESES, fuente_garante="Ley 3/2026 de Euskadi, art. 40.2.c",
                                     nota="ley de mayo de 2026: para solicitudes anteriores a su entrada en vigor, verificar"),
    ("País Vasco", "local"): _r(UN_MES, "Ley 3/2026 de Transparencia de Euskadi, art. 37.1 (art. 8.1.b incluye las entidades "
                                        "locales)", ampliacion=(15, "dias_habiles"),
                                fuente_ampliacion="Ley 3/2026 de Euskadi, art. 37.2: «por otros quince días más»",
                                reclamar="sin_plazo", fuente_reclamar="Ley 3/2026 de Euskadi, art. 40.2.a",
                                garante=TRES_MESES, fuente_garante="Ley 3/2026 de Euskadi, art. 40.2.c",
                                nota="ley de mayo de 2026: para solicitudes anteriores a su entrada en vigor, verificar"),
}
# Sin plazo propio en su ley autonómica, o sin ley propia localizada: rige la LTAIBG para resolver y ampliar. El
# plazo del órgano que resuelve la reclamación no se ha localizado en un texto: seguimiento manual.
for _c, _n in (("Principado de Asturias", "Ley 8/2018 de Asturias (BOE-A-2018-14293) no fija plazo propio"),
               ("La Rioja", "Ley 3/2014 de La Rioja (BOE-A-2014-9898) no fija plazo propio para el acceso"),
               ("Illes Balears", "no se localizó ley autonómica de transparencia con plazo propio"),
               ("Ceuta", "ciudad autónoma: legislación básica"), ("Melilla", "ciudad autónoma: legislación básica")):
    for _a in ("autonómico", "local"):
        TABLA[(_c, _a)] = _r(UN_MES, LTAIBG_RESOLVER, nota=_n)

SIN_VERIFICAR = _r(None, "", ampliacion=None, fuente_ampliacion="", reclamar="", fuente_reclamar="", verificado=False)


def clave(tipo, ccaa):
    """Clave del régimen («comunidad|ámbito») a partir del tipo de entidad y la comunidad del órgano."""
    if tipo in ESTATAL:
        return "Estado|estatal"
    ambito = "autonómico" if tipo in AUTONOMICO else "local" if tipo in LOCAL else ""
    if not ambito or not ccaa:
        return ""
    return f"{ccaa}|{ambito}"


def regimen(c):
    """Régimen para una clave; SIN_VERIFICAR si la clave está vacía o no es conocida."""
    if not c or "|" not in c:
        return SIN_VERIFICAR
    return TABLA.get(tuple(c.split("|", 1)), SIN_VERIFICAR)


def texto_plazo(p):
    if p is None:
        return "sin automatizar"
    n, unidad = p
    return f"{n} {'mes' if n == 1 else 'meses'}" if unidad == "meses" else f"{n} días hábiles"


def describir(c):
    r = regimen(c)
    if not r["verificado"] or r["plazo"] is None:
        return "régimen sin verificar: comprobad a mano el plazo aplicable" + (f" ({r['nota']})" if r["nota"] else "")
    silencio = "sin plazo según la ley" if r["reclamar"] == "sin_plazo" else "un mes"
    return (f"resolver: {texto_plazo(r['plazo'])} ({r['fuente']}); ampliación: {texto_plazo(r['ampliacion'])} "
            f"({r['fuente_ampliacion']}); reclamar contra el silencio: {silencio} ({r['fuente_reclamar']})")
