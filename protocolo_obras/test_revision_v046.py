"""Pruebas de las correcciones de la revisión adversarial de la v0.4.6 (un caso por hallazgo; ver
revisiones/v0_4_6/respuesta_revision_v0_4_6.md). Se ejecutan con: python -I -X utf8 test_revision_v046.py
(desde esta carpeta)."""
import os
import re
import sys
import unittest
from datetime import date

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import registro as rg  # noqa: E402
import regimenes as rgm  # noqa: E402


HOY = date(2026, 11, 2)   # fecha de corte de en_plazo (desde la v0.4.8)


def fila(**kw):
    r = {c: "" for c in rg.CAMPOS}
    r.update(id_obra="1", fecha_envio="2026-01-12", regimen="Estado|estatal")
    r.update(kw)
    return r


class ConFestivosLimpios(unittest.TestCase):
    def tearDown(self):
        rg.FESTIVOS_ADICIONALES.clear()
        rg.FESTIVOS_POR_AMBITO.clear()


class V01Ampliaciones(ConFestivosLimpios):
    def test_euskadi_amplia_quince_dias_habiles(self):
        # Recepción 12/01/2026: el mes vence el 12/02; quince días hábiles más llevan al 05/03/2026.
        r = fila(regimen="País Vasco|autonómico")
        self.assertEqual(rg.limite(r), date(2026, 2, 12))
        self.assertEqual(rg.limite({**r, "fecha_ampliacion": "2026-02-01"}), date(2026, 3, 5))

    def test_euskadi_con_festivo_de_su_comunidad(self):
        rg.cargar_festivos(["2026-03-02 País Vasco"])
        r = fila(regimen="País Vasco|local", fecha_ampliacion="2026-02-01")
        self.assertEqual(rg.limite(r), date(2026, 3, 6))

    def test_resto_de_ampliaciones_por_igual_periodo(self):
        self.assertEqual(rg.limite(fila(fecha_ampliacion="2026-02-01")), date(2026, 3, 12))
        # Extremadura: 30 + 30 días hábiles, igual que antes.
        self.assertEqual(rgm.regimen("Extremadura|local")["ampliacion"], (30, "dias_habiles"))

    def test_cataluna_prorroga_de_medio_plazo_no_se_automatiza(self):
        r = fila(regimen="Cataluña|local", fecha_ampliacion="2026-02-01")
        self.assertIsNone(rg.limite(r))
        self.assertEqual(rg.limite({**r, "fecha_ampliacion": ""}), date(2026, 2, 12))
        tarea = rg.pendientes([r], date(2026, 6, 1))[0][2]
        self.assertIn("sin cómputo automático", tarea)
        self.assertIn("mitad del inicial", tarea)

    def test_galicia_sin_ampliacion_en_su_ley(self):
        self.assertIsNone(rg.limite(fila(regimen="Galicia|autonómico", fecha_ampliacion="2026-02-01")))

    def test_cada_ampliacion_y_cada_plazo_de_garante_citan_fuente(self):
        for k, r in rgm.TABLA.items():
            if r["ampliacion"] is not None or r["verificado"]:
                self.assertTrue(r["fuente_ampliacion"], k)
            if r["garante"] is not None:
                self.assertTrue(r["fuente_garante"], k)


class V02PlazoDelGarante(ConFestivosLimpios):
    def test_gaip_dos_meses(self):
        tarea = rg.pendientes([fila(regimen="Cataluña|autonómico", fecha_respuesta="2026-02-01",
                                    resultado="denegada_limite", fecha_reclamacion="2026-02-20")], date(2026, 3, 1))
        self.assertEqual(tarea[0][0], date(2026, 4, 20))
        self.assertIn("2 meses", tarea[0][2])
        self.assertIn("mediación", tarea[0][2])

    def test_consejo_estatal_tres_meses(self):
        tarea = rg.pendientes([fila(fecha_respuesta="2026-02-01", resultado="denegada_limite",
                                    fecha_reclamacion="2026-02-20")], date(2026, 3, 1))
        self.assertEqual(tarea[0][0], date(2026, 5, 20))

    def test_garante_sin_plazo_localizado_es_seguimiento_manual(self):
        tarea = rg.pendientes([fila(regimen="Comunidad de Madrid|autonómico", fecha_respuesta="2026-02-01",
                                    resultado="denegada_limite", fecha_reclamacion="2026-02-20")], date(2026, 3, 1))
        self.assertIn("seguimiento manual", tarea[0][2])


class V03AmpliacionFueraDeTiempo(ConFestivosLimpios):
    def test_ampliacion_despues_del_vencimiento(self):
        # El caso de la revisión: recepción 12/01, respuesta 01/03, ampliación anotada 01/04.
        r = fila(fecha_respuesta="2026-03-01", resultado="concedida", fecha_ampliacion="2026-04-01")
        self.assertTrue(any("después de la respuesta" in e for e in rg.validar([r])))
        self.assertTrue(any("vencimiento ordinario provisional" in a for a in rg.avisos([r])))
        self.assertIsNone(rg.limite(r))
        self.assertEqual(rg.en_plazo(r, HOY), "")

    def test_ampliacion_despues_de_la_respuesta(self):
        r = fila(fecha_respuesta="2026-02-01", resultado="concedida", fecha_ampliacion="2026-02-05")
        self.assertTrue(any("después de la respuesta" in e for e in rg.validar([r])))

    def test_ampliacion_a_tiempo_es_valida(self):
        r = fila(fecha_respuesta="2026-03-01", resultado="concedida", fecha_ampliacion="2026-02-05")
        self.assertEqual(rg.validar([r]), [])
        self.assertEqual(rg.limite(r), date(2026, 3, 12))


class V04FestivosPorTerritorio(ConFestivosLimpios):
    def test_festivo_de_una_comunidad_no_afecta_a_otra(self):
        rg.cargar_festivos(["# festivos de prueba", "2026-02-16 Región de Murcia"])
        madrid = fila(regimen="Comunidad de Madrid|autonómico", fecha_envio="2026-01-30")
        murcia = fila(regimen="Región de Murcia|autonómico", fecha_envio="2026-01-30")
        self.assertEqual(rg.limite(madrid), date(2026, 2, 27))
        self.assertEqual(rg.limite(murcia), date(2026, 3, 2))

    def test_festivo_de_un_organo(self):
        rg.cargar_festivos(["2026-02-12 organo:L01"])
        self.assertEqual(rg.limite(fila(organo_id="L01")), date(2026, 2, 13))
        self.assertEqual(rg.limite(fila(organo_id="L02")), date(2026, 2, 12))

    def test_linea_sin_ambito_vale_para_todas(self):
        rg.cargar_festivos(["2026-02-12"])
        self.assertEqual(rg.limite(fila(organo_id="L02")), date(2026, 2, 13))


class V05V07SoloSeCalificaConFechaVerificada(ConFestivosLimpios):
    def test_sin_fecha_verificada_no_se_califica(self):
        r = fila(fecha_respuesta="2026-03-20", resultado="concedida")
        self.assertIsNotNone(rg.limite(r))          # hay vencimiento provisional para avisar
        self.assertEqual(rg.en_plazo(r, HOY), "")         # pero no se califica

    def test_con_fecha_verificada_si(self):
        # Una suspensión por alegaciones de terceros llevó el vencimiento al 31/03: la persona lo anota.
        r = fila(fecha_respuesta="2026-03-20", resultado="concedida", fecha_limite_verificada="2026-03-31")
        self.assertEqual(rg.en_plazo(r, HOY), "sí")
        self.assertEqual(rg.en_plazo({**r, "fecha_respuesta": "2026-04-02"}, HOY), "no")

    def test_resumen_solo_cuenta_las_verificadas(self):
        filas = [fila(id_obra="a", fecha_respuesta="2026-03-20", resultado="concedida"),
                 fila(id_obra="b", fecha_respuesta="2026-03-20", resultado="concedida", fecha_limite_verificada="2026-03-31")]
        texto = rg.resumen(filas, date(2026, 6, 1))
        self.assertIn("con fecha límite verificada y el plazo ya vencido o respondidas: 1", texto)
        self.assertIn("sin fecha límite verificada (excluidas de las cifras de plazo): 1", texto)
        self.assertIn("respondidas en plazo: 1 (100.0 %)", texto)

    def test_los_avisos_usan_la_fecha_verificada_si_existe(self):
        tarea = rg.pendientes([fila(fecha_limite_verificada="2026-03-31")], date(2026, 3, 1))[0]
        self.assertEqual(tarea[0], date(2026, 3, 31))
        self.assertIn("vencimiento verificado", tarea[2])
        tarea = rg.pendientes([fila()], date(2026, 2, 1))[0]
        self.assertIn("vencimiento provisional", tarea[2])
        self.assertIn("suspensiones", tarea[2])

    def test_fecha_verificada_mal_escrita_o_anterior_al_envio(self):
        self.assertTrue(any("fecha_limite_verificada" in e for e in rg.validar([fila(fecha_limite_verificada="31/03/2026")])))
        self.assertTrue(any("no posterior al envío" in e for e in rg.validar([fila(fecha_limite_verificada="2026-01-01")])))


class V06FuentesYAmbito(unittest.TestCase):
    def test_castilla_y_leon_cita_la_ley_estatal_no_la_reutilizacion(self):
        for a in ("autonómico", "local"):
            f = rgm.regimen(f"Castilla y León|{a}")["fuente"]
            self.assertIn(rgm.LTAIBG_RESOLVER, f)
            self.assertNotIn("art. 9", f)

    def test_castilla_la_mancha_local_cita_la_ley_estatal(self):
        f = rgm.regimen("Castilla-La Mancha|local")["fuente"]
        self.assertTrue(f.startswith(rgm.LTAIBG_RESOLVER), f)
        self.assertIn("4.1.a", rgm.regimen("Castilla-La Mancha|autonómico")["fuente"])

    def test_galicia_local_cita_la_ley_estatal(self):
        self.assertTrue(rgm.regimen("Galicia|local")["fuente"].startswith(rgm.LTAIBG_RESOLVER))

    def test_cada_regimen_local_con_ley_propia_cita_el_articulo_de_ambito(self):
        # Si la fuente del plazo de un régimen local es una ley autonómica, debe decir qué artículo incluye a los locales.
        for (ccaa, ambito), r in rgm.TABLA.items():
            if ambito == "local" and r["verificado"] and not r["fuente"].startswith(rgm.LTAIBG_RESOLVER):
                self.assertRegex(r["fuente"], r"art\. [\d.]+[a-z.]* incluye|art\. \d+ incluye", (ccaa, ambito))

    def test_las_citas_de_ambito_estan_en_los_fragmentos(self):
        fuentes = os.path.join(AQUI, "fuentes", "regimenes")
        for fichero, texto in (("galicia.txt", "Artículo 3. Ámbito subjetivo"), ("navarra.txt", "entidades locales de Navarra"),
                               ("valenciana.txt", "administración local de la Comunitat Valenciana"),
                               ("euskadi.txt", "entidades locales de la Comunidad Autónoma del País Vasco"),
                               ("cataluna.txt", "Administración local en Cataluña"),
                               ("castilla_la_mancha.txt", "estarán sujetos a la legislación básica"),
                               ("euskadi.txt", "por otros quince días más"), ("cataluna.txt", "la mitad del inicial"),
                               ("cataluna.txt", "dos meses desde la presentación de la reclamación")):
            with open(os.path.join(fuentes, fichero), encoding="utf-8") as fh:
                self.assertIn(texto, fh.read(), fichero)


class V08CitasDeResoluciones(unittest.TestCase):
    def test_el_complemento_no_publica_la_lista_de_casos(self):
        ruta = os.path.join(AQUI, "..", "investigacion_consejo", "COMPLEMENTO_AUTONOMICO.md")
        with open(ruta, encoding="utf-8") as fh:
            texto = fh.read()
        self.assertNotIn("Casos estrictos:", texto)
        for numero in ("0387/2021", "51/2024", "778/2023", "1070/2026", "0893/2025"):
            self.assertNotIn(numero, texto)
        self.assertIn("precedente de un criterio", texto)


if __name__ == "__main__":
    unittest.main(verbosity=2)
