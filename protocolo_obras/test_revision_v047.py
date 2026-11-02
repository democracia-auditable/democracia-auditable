"""Pruebas de las correcciones de la revisión adversarial de la v0.4.7 (un caso por hallazgo; ver
revisiones/v0_4_7/respuesta_revision_v0_4_7.md). Se ejecutan con: python -I -X utf8 test_revision_v047.py
(desde esta carpeta)."""
import csv
import os
import re
import subprocess
import sys
import tempfile
import unittest
from datetime import date

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import registro as rg  # noqa: E402

PY = [sys.executable, "-I", "-X", "utf8"]
HOY = date(2026, 11, 2)


def fila(**kw):
    r = {c: "" for c in rg.CAMPOS}
    r.update(id_obra="1", fecha_envio="2026-01-12", regimen="Estado|estatal")
    r.update(kw)
    return r


class N01FechaDeAmpliacionMalEscrita(unittest.TestCase):
    def test_validar_no_se_rompe_en_cataluna_ni_galicia(self):
        for reg in ("Galicia|autonómico", "Cataluña|local", "Cataluña|autonómico", "Estado|estatal"):
            r = fila(regimen=reg, fecha_ampliacion="2026-02-XX")
            errores = rg.validar([r])
            self.assertTrue(any("fecha_ampliacion no es una fecha" in e for e in errores), reg)
            self.assertIsNone(rg.limite(r), reg)
            self.assertIn("mal escrita", rg.pendientes([r], HOY)[0][2])


class N02AmpliacionAntesDeLaRecepcion(unittest.TestCase):
    def test_es_error_y_no_se_calcula(self):
        r = fila(fecha_recepcion_organo="2026-02-20", fecha_ampliacion="2026-01-20")
        self.assertTrue(any("antes de la recepción por el órgano" in e for e in rg.validar([r])))
        self.assertIsNone(rg.limite(r))


class N03AmpliacionTrasElVencimientoProvisional(unittest.TestCase):
    def test_es_aviso_no_error(self):
        # Pudo haber una suspensión en febrero: no es un error indiscutible.
        r = fila(fecha_ampliacion="2026-02-20")
        self.assertEqual(rg.validar([r]), [])
        self.assertTrue(any("aparentemente tardía" in a for a in rg.avisos([r])))
        self.assertIsNone(rg.limite(r))                        # sin fecha provisional
        self.assertIn("comprobar si hubo suspensión", rg.pendientes([r], HOY)[0][2])

    def test_con_fecha_verificada_no_hay_aviso_y_se_usa(self):
        r = fila(fecha_ampliacion="2026-02-20", fecha_limite_verificada="2026-04-30")
        self.assertEqual(rg.validar([r]), [])
        self.assertEqual(rg.avisos([r]), [])
        self.assertEqual(rg.pendientes([r], date(2026, 3, 1))[0][0], date(2026, 4, 30))

    def test_despues_de_la_respuesta_sigue_siendo_error(self):
        r = fila(fecha_respuesta="2026-02-01", resultado="concedida", fecha_ampliacion="2026-02-05")
        self.assertTrue(any("después de la respuesta" in e for e in rg.validar([r])))


class N04SilencioAntesDelVencimiento(unittest.TestCase):
    def setUp(self):
        self.r = fila(fecha_envio="2026-10-12", fecha_limite_verificada="2026-12-14", resultado="silencio")

    def test_en_plazo_no_califica_antes_de_vencer(self):
        self.assertEqual(rg.en_plazo(self.r, HOY), "")
        self.assertEqual(rg.en_plazo(self.r, date(2026, 12, 15)), "no")

    def test_validar_con_fecha_de_corte_lo_rechaza(self):
        self.assertTrue(any("antes de que venza" in e for e in rg.validar([self.r], HOY)))
        self.assertEqual(rg.validar([self.r], date(2026, 12, 15)), [])

    def test_exportar_validar_pendientes_y_resumen_coinciden(self):
        with tempfile.TemporaryDirectory() as d:
            reg, pub = os.path.join(d, "registro.csv"), os.path.join(d, "pub.csv")
            rg.escribir(reg, [{**self.r, "resultado": ""}])
            comun = ["--registro", reg, "--fecha", HOY.isoformat()]
            subprocess.run(PY + [os.path.join(AQUI, "registro.py"), "exportar", *comun, "--salida", pub],
                           check=True, capture_output=True)
            with open(pub, encoding="utf-8") as fh:
                self.assertEqual(next(csv.DictReader(fh))["en_plazo"], "")
            pend = subprocess.run(PY + [os.path.join(AQUI, "registro.py"), "pendientes", *comun],
                                  capture_output=True, text=True, encoding="utf-8").stdout
            self.assertIn("esperar respuesta hasta el 2026-12-14", pend)
            self.assertIn("con fecha límite verificada y el plazo ya vencido o respondidas: 0",
                          rg.resumen([self.r], HOY))


class N05FechaVerificadaAnteriorALaRecepcion(unittest.TestCase):
    def test_es_error(self):
        r = fila(fecha_recepcion_organo="2026-02-20", fecha_limite_verificada="2026-01-30",
                 fecha_respuesta="2026-02-22", resultado="concedida")
        self.assertTrue(any("no posterior a la recepción" in e for e in rg.validar([r])))


class N06FestivosConAmbitoQueNoCoincide(unittest.TestCase):
    def tearDown(self):
        rg.FESTIVOS_ADICIONALES.clear()
        rg.FESTIVOS_POR_AMBITO.clear()

    def test_comunidad_sin_tilde_y_organo_inexistente(self):
        rg.cargar_festivos(["2026-03-02 Pais Vasco", "2026-03-03 Galicia", "2026-03-04 organo:NO", "2026-03-05 País Vasco"])
        avisos = rg.avisos_festivos([fila(regimen="País Vasco|local", organo_id="L1")])
        self.assertTrue(any("«Pais Vasco»" in a and "tilde" in a for a in avisos))
        self.assertTrue(any("ccaa:Galicia" in a for a in avisos))      # existe, pero no hay filas de Galicia
        self.assertTrue(any("organo:NO" in a for a in avisos))
        self.assertFalse(any("País Vasco»" in a for a in avisos))      # el bien escrito no avisa

    def test_validar_por_linea_de_ordenes_muestra_el_aviso(self):
        with tempfile.TemporaryDirectory() as d:
            reg, fest = os.path.join(d, "registro.csv"), os.path.join(d, "festivos.txt")
            rg.escribir(reg, [fila(regimen="País Vasco|local")])
            with open(fest, "w", encoding="utf-8") as fh:
                fh.write("2026-03-02 Pais Vasco\n")
            p = subprocess.run(PY + [os.path.join(AQUI, "registro.py"), "validar", "--registro", reg, "--festivos", fest],
                               capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(p.returncode, 0)
            self.assertIn("AVISO: festivos para «Pais Vasco»", p.stdout)
            self.assertTrue(p.stdout.strip().splitlines()[-1].startswith("Registro válido"))


class N07RutasYPrecedentes(unittest.TestCase):
    RAIZ = os.path.join(AQUI, "..")

    def test_no_quedan_rutas_a_carpetas_que_no_estan_en_el_repositorio(self):
        for ruta in (os.path.join("investigacion_consejo", "COMPLEMENTO_AUTONOMICO.md"),
                     os.path.join("protocolo_obras", "PROTOCOLO_OBRAS.md"),
                     os.path.join("protocolo_obras", "GUIA.md")):
            with open(os.path.join(self.RAIZ, ruta), encoding="utf-8") as fh:
                self.assertIsNone(re.search(r"documento_v0_4_\d/", fh.read()), ruta)

    def test_la_coincidencia_de_terminacion_no_se_describe_como_validada(self):
        with open(os.path.join(self.RAIZ, "protocolo_obras", "PROTOCOLO_OBRAS.md"), encoding="utf-8") as fh:
            texto = fh.read()
        self.assertNotIn("validada;", texto)
        self.assertNotIn("4 % de las resoluciones", texto)
        self.assertIn("3,7 % de los expedientes del grupo documental R", texto)

    def test_el_complemento_solo_cita_numeros_de_precedentes(self):
        with open(os.path.join(self.RAIZ, "investigacion_consejo", "COMPLEMENTO_AUTONOMICO.md"), encoding="utf-8") as fh:
            texto = fh.read()
        for numero in ("R159/2026", "RDA136/2023", "136/2022", "107/2021"):
            self.assertNotIn(numero, texto)


if __name__ == "__main__":
    unittest.main(verbosity=2)
