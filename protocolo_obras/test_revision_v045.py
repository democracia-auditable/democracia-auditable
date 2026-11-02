"""Pruebas de las correcciones de la revisión adversarial de la v0.4.5 (un caso por hallazgo; ver
revisiones/v0_4_5/respuesta_revision_v0_4_5.md). Se ejecutan junto con test_protocolo.py:
python -I -X utf8 test_revision_v045.py (desde esta carpeta)."""
import csv
import json
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import date

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import registro as rg  # noqa: E402
import regimenes as rgm  # noqa: E402
import seleccionar_obras as so  # noqa: E402   (sin try: el repositorio se distribuye completo; si falta, debe fallar)

PY = [sys.executable, "-I", "-X", "utf8"]


def fila(**kw):
    r = {c: "" for c in rg.CAMPOS}
    r.update(id_obra="1", fecha_envio="2026-01-30", regimen="Estado|estatal")
    r.update(kw)
    return r


def escribir_obras(d, filas):
    with open(os.path.join(d, "obras.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=so.CAMPOS)
        w.writeheader()
        for i, extra in enumerate(filas):
            w.writerow({**{c: "" for c in so.CAMPOS}, "id": f"o{i:02d}", "estado": "ADJ", "fecha_adjudicacion": "2024-01-01",
                        "fin_teorico": "2025-01-01", "presupuesto_sin_iva": "1500000", "fin_definitivo": "False",
                        "organo_id": f"org{i}", "tipo_administracion": "3", "ccaa_organo": "Galicia", **extra})


def seleccionar(d, *args):
    sys.argv = ["seleccionar_obras.py", "seleccionar", "--obras", os.path.join(d, "obras.csv"), "--carpeta", d,
                "--registro", os.path.join(d, "reg.csv"), *args]
    so.main()


class B03Regimenes(unittest.TestCase):
    """Plazos por régimen jurídico, con la cita del BOE de cada fila."""

    def test_clave(self):
        self.assertEqual(rgm.clave("1", "Galicia"), "Estado|estatal")
        self.assertEqual(rgm.clave("2", "Comunidad de Madrid"), "Comunidad de Madrid|autonómico")
        self.assertEqual(rgm.clave("8", "Extremadura"), "Extremadura|local")
        self.assertEqual(rgm.clave("4", "Galicia"), "")     # tipo sin ámbito claro
        self.assertEqual(rgm.clave("3", ""), "")            # comunidad desconocida

    def test_todas_las_comunidades_tienen_regimen(self):
        for ccaa in set(so.PROVINCIAS.values()):
            for tipo in ("2", "3"):
                self.assertIsNot(rgm.regimen(rgm.clave(tipo, ccaa)), rgm.SIN_VERIFICAR, ccaa)

    def test_cada_fila_cita_su_fuente(self):
        for k, r in rgm.TABLA.items():
            self.assertTrue(r["fuente"], k)
            self.assertTrue(r["fuente_reclamar"], k)

    def test_madrid_veinte_dias_habiles(self):
        # Recepción el viernes 30/01/2026: 20 días hábiles terminan el viernes 27/02/2026.
        self.assertEqual(rg.limite(fila(regimen="Comunidad de Madrid|autonómico")), date(2026, 2, 27))
        # Régimen general: un mes, de fecha a fecha (28/02/2026, sábado) → primer día hábil, lunes 02/03/2026.
        self.assertEqual(rg.limite(fila(regimen="Estado|estatal")), date(2026, 3, 2))

    def test_extremadura_treinta_dias_habiles_tambien_en_lo_local(self):
        self.assertEqual(rg.limite(fila(regimen="Extremadura|local")), date(2026, 3, 13))
        # Con ampliación, 60 días hábiles; el Viernes Santo (03/04/2026) es inhábil → lunes 27/04/2026.
        self.assertEqual(rg.limite(fila(regimen="Extremadura|local", fecha_ampliacion="2026-02-10")), date(2026, 4, 27))

    def test_sin_verificar_no_calcula_fechas(self):
        r = fila(regimen="Comunidad de Madrid|local")
        self.assertIsNone(rg.limite(r))
        self.assertEqual(rg.en_plazo({**r, "resultado": "silencio"}, date(2026, 11, 2)), "")
        tareas = rg.pendientes([r], date(2026, 6, 1))
        self.assertIn("no se calcula ninguna fecha", tareas[0][2])
        self.assertIsNone(rg.limite(fila(regimen="")))

    def test_silencio_sin_plazo_segun_la_ley(self):
        tareas = rg.pendientes([fila(regimen="Cantabria|local")], date(2026, 3, 10))
        self.assertIn("no está sujeta a plazo", tareas[0][2])

    def test_regimen_desconocido_es_error_de_validacion(self):
        self.assertTrue(any("regimen desconocido" in e for e in rg.validar([fila(regimen="Atlántida|local")])))

    def test_resumen_excluye_lo_no_verificado_de_las_cifras_de_plazo(self):
        # Desde la v0.4.7 las cifras de plazo solo usan fecha_limite_verificada; una fila con régimen sin verificar
        # no puede tenerla calculada y queda fuera, como antes.
        texto = rg.resumen([fila(regimen="Comunidad de Madrid|local", id_obra="a"),
                            fila(id_obra="b", fecha_limite_verificada="2026-03-02")], date(2026, 6, 1))
        self.assertIn("sin fecha límite verificada (excluidas de las cifras de plazo): 1", texto)

    def test_el_lote_lleva_el_regimen(self):
        with tempfile.TemporaryDirectory() as d:
            escribir_obras(d, [{"tipo_administracion": "2", "ccaa_organo": "Comunidad de Madrid"}])
            seleccionar(d, "--fecha", "2026-01-01")
            with open(os.path.join(d, "lote_2026-01-01", "lote.csv"), encoding="utf-8") as fh:
                self.assertEqual(next(csv.DictReader(fh))["regimen"], "Comunidad de Madrid|autonómico")


class B04MuestraPersistente(unittest.TestCase):
    def test_muestra_mayor_que_las_candidatas_se_guarda_entera(self):
        with tempfile.TemporaryDirectory() as d:
            escribir_obras(d, [{}, {}])
            seleccionar(d, "--fecha", "2026-01-01", "--muestra", "200", "--nombre", "m")
            with open(os.path.join(d, "lote_2026-01-01_m", "muestra.csv"), encoding="utf-8") as fh:
                self.assertEqual(len(list(csv.DictReader(fh))), 2)
            with open(os.path.join(d, "lote_2026-01-01_m", "marco_muestra.json"), encoding="utf-8") as fh:
                marco = json.load(fh)
            self.assertEqual((marco["n_pedida"], marco["n_marco"], marco["n_muestra"]), (200, 2, 2))

    def test_muestra_sin_candidatas_tambien_se_guarda(self):
        with tempfile.TemporaryDirectory() as d:
            escribir_obras(d, [{"fin_definitivo": "True"}])
            seleccionar(d, "--fecha", "2026-01-01", "--muestra", "5", "--nombre", "m")
            self.assertTrue(os.path.exists(os.path.join(d, "lote_2026-01-01_m", "muestra.csv")))


class I27SorteoIndependienteDeLaPrioridad(unittest.TestCase):
    def test_misma_muestra_con_cualquier_prioridad(self):
        muestras = []
        for prioridad in ("antiguedad", "terminacion"):
            with tempfile.TemporaryDirectory() as d:
                escribir_obras(d, [{"fin_teorico": f"2025-0{1 + i % 9}-01"} for i in range(30)])
                seleccionar(d, "--fecha", "2026-01-01", "--muestra", "7", "--prioridad", prioridad, "--nombre", "m")
                with open(os.path.join(d, "lote_2026-01-01_m", "muestra.csv"), encoding="utf-8") as fh:
                    muestras.append({r["id"] for r in csv.DictReader(fh)})
        self.assertEqual(muestras[0], muestras[1])


class B05ValidacionNoSeRompe(unittest.TestCase):
    def test_fechas_mal_escritas_en_cualquier_campo(self):
        for campo in ("fecha_recepcion_organo", "fecha_replanteo", "fecha_recepcion_obra", "fecha_envio"):
            errores = rg.validar([fila(**{campo: "NO_FECHA"})])
            self.assertTrue(any(campo in e for e in errores), campo)

    def test_pendientes_y_resumen_toleran_fechas_mal_escritas(self):
        r = fila(fecha_recepcion_organo="NO_FECHA")
        rg.pendientes([r], date(2026, 6, 1))
        rg.resumen([r], date(2026, 6, 1))


class B06Tope(unittest.TestCase):
    def test_tope_cero_no_existe(self):
        with tempfile.TemporaryDirectory() as d:
            escribir_obras(d, [{}])
            with self.assertRaises(SystemExit):
                seleccionar(d, "--fecha", "2026-01-01", "--tope", "0")

    def test_tope_mayor_que_cuatro_exige_justificacion(self):
        with tempfile.TemporaryDirectory() as d:
            escribir_obras(d, [{}])
            with self.assertRaises(SystemExit):
                seleccionar(d, "--fecha", "2026-01-01", "--tope", "6")
            seleccionar(d, "--fecha", "2026-01-01", "--tope", "6", "--justificacion-tope", "piloto acordado con el órgano")
            with open(os.path.join(d, "lote_2026-01-01", "parametros.json"), encoding="utf-8") as fh:
                self.assertEqual(json.load(fh)["justificacion_tope"], "piloto acordado con el órgano")


class B06OrigenDeCadaSolicitud(unittest.TestCase):
    """Sin reserva aleatoria en el flujo: el registro distingue muestra y flujo, y el resumen avisa de qué permite estimar."""

    def test_origen_se_anota_y_se_resume(self):
        with tempfile.TemporaryDirectory() as d:
            reg = os.path.join(d, "registro.csv")
            for nombre, ident in (("lote_2026-01-01_muestra", "m1"), ("lote_2026-01-01_flujo", "f1")):
                os.makedirs(os.path.join(d, nombre))
                with open(os.path.join(d, nombre, "lote.csv"), "w", newline="", encoding="utf-8") as fh:
                    w = csv.DictWriter(fh, fieldnames=["id", "enlace", "expediente", "organo_id", "ambito", "garante", "regimen"])
                    w.writeheader()
                    w.writerow({"id": ident, "enlace": "", "expediente": "", "organo_id": "O", "ambito": "estatal",
                                "garante": "", "regimen": "Estado|estatal"})
                sys.argv = ["registro.py", "crear", "--registro", reg, "--lote", os.path.join(d, nombre, "lote.csv")]
                rg.main()
            filas = {r["id_obra"]: r for r in rg.leer(reg)}
            self.assertEqual((filas["m1"]["origen"], filas["f1"]["origen"]), ("muestra", "flujo"))
            for r in filas.values():
                r["fecha_envio"] = "2026-01-30"
            self.assertIn("Solo la muestra fija aleatoria permite estimar", rg.resumen(list(filas.values()), date(2026, 6, 1)))


class CicloMensualRobusto(unittest.TestCase):
    """B09 (no da por bueno un registro con errores), B10 (reanudación), I22 (festivos) y dos ciclos seguidos."""

    def _ciclo(self, d, fecha, *extra):
        open(os.path.join(d, "vacio.zip"), "a").close()
        return subprocess.run(PY + [os.path.join(AQUI, "ciclo_mensual.py"), "--organizacion", "PRUEBA", "--fecha", fecha,
                                    "--trabajo", d, "--sin-descarga", "--datos", os.path.join(d, "*.zip"),
                                    "--reutilizar-escaneo", *extra], capture_output=True, text=True, encoding="utf-8")

    def _escaneo(self, d, n):
        escribir_obras(d, [{"fin_teorico": "2025-08-15"} for _ in range(n)])
        os.replace(os.path.join(d, "obras.csv"), os.path.join(d, "obras_protocolo.csv"))

    def test_dos_ciclos_seguidos_con_muestra_pequena(self):
        with tempfile.TemporaryDirectory() as d:
            self._escaneo(d, 3)
            r1 = self._ciclo(d, "2026-01-01", "--muestra", "200")
            self.assertEqual(r1.returncode, 0, r1.stdout + r1.stderr)
            r2 = self._ciclo(d, "2026-02-01", "--muestra", "200")
            self.assertEqual(r2.returncode, 0, r2.stdout + r2.stderr)

    def test_registro_con_errores_detiene_el_ciclo_sin_avanzarlo(self):
        with tempfile.TemporaryDirectory() as d:
            self._escaneo(d, 2)
            rg.escribir(os.path.join(d, "registro.csv"), [fila(fecha_envio="31/01/2026")])
            r = self._ciclo(d, "2026-01-01", "--muestra", "0")
            self.assertNotEqual(r.returncode, 0)
            self.assertIn("errores", r.stdout + r.stderr)
            self.assertFalse(os.path.exists(os.path.join(d, "ciclo_estado.json")))
            self.assertFalse(any(n.startswith("lote_") for n in os.listdir(d)))

    def test_reanuda_tras_una_interrupcion(self):
        with tempfile.TemporaryDirectory() as d:
            self._escaneo(d, 3)
            sys.argv = ["seleccionar_obras.py", "seleccionar", "--obras", os.path.join(d, "obras_protocolo.csv"),
                        "--carpeta", d, "--registro", os.path.join(d, "registro.csv"), "--fecha", "2026-01-01",
                        "--desde", "2025-12-01", "--nombre", "flujo"]
            so.main()                      # el lote de flujo quedó preparado y el ciclo se cortó
            r = self._ciclo(d, "2026-01-01", "--muestra", "0")
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertIn("se reutiliza", r.stdout)
            self.assertEqual(len(rg.leer(os.path.join(d, "registro.csv"))), 3)

    def test_festivos_llegan_a_los_pendientes(self):
        with tempfile.TemporaryDirectory() as d:
            self._escaneo(d, 1)
            with open(os.path.join(d, "festivos.txt"), "w", encoding="utf-8") as fh:
                fh.write("2026-03-19\n")
            r = self._ciclo(d, "2026-01-01", "--muestra", "0", "--festivos", os.path.join(d, "festivos.txt"))
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            with open(os.path.join(d, "resumen_ciclo_2026-01-01.md"), encoding="utf-8") as fh:
                self.assertIn("festivos.txt", fh.read())


class B11Privacidad(unittest.TestCase):
    def test_exportar_sin_identificadores_por_defecto(self):
        with tempfile.TemporaryDirectory() as d:
            reg, sal = os.path.join(d, "registro.csv"), os.path.join(d, "pub.csv")
            rg.escribir(reg, [fila(enlace="https://x", expediente="E1", organo_id="O1", garante="G")])
            sys.argv = ["registro.py", "exportar", "--registro", reg, "--salida", sal]
            rg.main()
            with open(sal, encoding="utf-8") as fh:
                cabecera = next(csv.reader(fh))
            for c in rg.IDENTIFICADORES:
                self.assertNotIn(c, cabecera)
            sys.argv += ["--con-identificadores"]
            rg.main()
            with open(sal, encoding="utf-8") as fh:
                self.assertIn("enlace", next(csv.reader(fh)))

    def test_gitignore_cubre_las_salidas_con_datos_reales(self):
        with open(os.path.join(AQUI, ".gitignore"), encoding="utf-8") as fh:
            patrones = {l.strip() for l in fh if l.strip() and not l.startswith("#")}
        for p in ("obras_protocolo.csv", "lote_*/", "registro.csv", "pendientes_*.csv", "resumen_ciclo_*.md",
                  "registro_publico*.csv", "ciclo_estado.json", "datos/", ".seleccion.lock"):
            self.assertIn(p, patrones)


class Interfaz(unittest.TestCase):
    def setUp(self):
        try:
            sys.path.insert(0, os.path.join(AQUI, "..", "fase0_placsp"))
            import interfaz
        except ImportError as e:   # solo si falta tkinter (algunas distribuciones de Linux)
            self.skipTest(str(e))
        self.i = interfaz

    def test_tope_solo_de_uno_a_cuatro(self):
        with self.assertRaises(ValueError):
            self.i.orden_ciclo("ORG1", "T", tope="0")
        with self.assertRaises(ValueError):
            self.i.orden_ciclo("ORG1", "T", tope="5")

    def test_festivos_llegan_al_ciclo(self):
        cmd = self.i.orden_ciclo("ORG1", "T", festivos="f.txt")
        self.assertEqual(cmd[cmd.index("--festivos") + 1], "f.txt")


if __name__ == "__main__":
    unittest.main()
