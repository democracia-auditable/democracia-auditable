"""La señal del protocolo (protocolo_obras/senal_terminacion.py) marca exactamente lo mismo que el emparejamiento
de la regla congelada (validar_e4t.marcada, copia literal del bucle de regla_e4t_v2.py), en obras sintéticas que
cubren cada condición: vocabulario de terminación, fecha posterior al inicio, acuerdo marco, «parte de», parecido de
títulos, fases, números y palabras raras. Uso: python -I -X utf8 test_equivalencia.py (desde esta carpeta)."""
import os
import sys
import unittest

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import validar_e4t as v  # noqa: E402

st = v.st


def obra(ident, titulo, organo="O1", inicio="2021-03-01", anuncio="2020-12-01"):
    return {"id": ident, "titulo": titulo, "organo_id": organo, "organo": organo, "fecha_inicio": inicio,
            "fecha_adjudicacion": "2021-01-15", "primer_anuncio": anuncio}


A = "Construcción del pabellón polideportivo municipal de Valdeverde"
CASOS = [
    obra("a_ok", A),
    obra("b_ok", "Terminación del pabellón polideportivo municipal de Valdeverde", anuncio="2023-05-01"),
    obra("a_antes", "Reforma integral del mercado de abastos de Pinarejo"),
    obra("b_antes", "Terminación de la reforma integral del mercado de abastos de Pinarejo", anuncio="2020-06-01"),
    obra("a_otro_organo", "Urbanización del sector industrial Los Llanos de Sotoalto"),
    obra("b_otro_organo", "Finalización de la urbanización del sector industrial Los Llanos de Sotoalto", organo="O2",
         anuncio="2023-01-01"),
    obra("a_fase", "Rehabilitación del puente romano de Ribalta fase 1"),
    obra("b_fase", "Terminación de la rehabilitación del puente romano de Ribalta fase 2", anuncio="2023-01-01"),
    obra("a_num", "Ampliación del colegio público número 3 de Torremar"),
    obra("b_num", "Terminación de la ampliación del colegio público número 5 de Torremar", anuncio="2023-01-01"),
    obra("a_am", "Acuerdo marco de pavimentación de calles de Encinar"),
    obra("b_am", "Terminación del acuerdo marco de pavimentación de calles de Encinar", anuncio="2023-01-01"),
    obra("a_parte", "Depósito de agua potable de Monteviejo"),
    obra("b_parte", "Terminación de las obras para la obra de depósito de agua potable de Monteviejo", anuncio="2023-01-01"),
    obra("a_poco", "Nuevo centro de salud con aparcamiento subterráneo en Almendral"),
    obra("b_poco", "Terminación de la pista de atletismo de Almendral", anuncio="2023-01-01"),
    obra("a_resto", "Saneamiento y depuración del núcleo de Castroval"),
    obra("b_resto", "Resto de obras del saneamiento y depuración del núcleo de Castroval", anuncio="2024-02-01"),
    obra("a_sin_termin", "Pavimentación de la travesía de Robledillo"),
    obra("b_sin_termin", "Mejora de la pavimentación de la travesía de Robledillo", anuncio="2023-01-01"),
]


class Equivalencia(unittest.TestCase):
    def test_mismas_marcas_que_la_regla_congelada(self):
        org, df, por_org = v.preparar(CASOS)
        indice = st.Indice(CASOS)
        congelada = {c["id"]: v.marcada(c, org, df, por_org) for c in CASOS}
        modulo = {c["id"]: indice.terminacion(c) for c in CASOS}
        self.assertEqual({k: bool(x) for k, x in congelada.items()}, {k: bool(x) for k, x in modulo.items()})
        self.assertTrue(congelada["a_ok"] and congelada["a_resto"])            # los casos positivos se marcan
        for negativo in ("a_antes", "a_otro_organo", "a_fase", "a_num", "a_am", "a_parte", "a_poco", "a_sin_termin"):
            self.assertFalse(congelada[negativo], negativo)


if __name__ == "__main__":
    unittest.main()
