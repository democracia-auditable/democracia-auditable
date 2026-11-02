"""Pruebas del protocolo de obras: python -I -X utf8 -m unittest test_protocolo (desde esta carpeta)."""
import csv
import os
import sys
import tempfile
import unittest
from datetime import date

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import registro as rg  # noqa: E402

import seleccionar_obras as so  # noqa: E402   necesita fase0_placsp e investigacion_doc_ccn al lado; si faltan, debe fallar


HOY = date(2026, 11, 2)   # fecha de corte de en_plazo (desde la v0.4.8)


def fila(**kw):
    r = {c: "" for c in rg.CAMPOS}
    r.update(id_obra="1", fecha_envio="2026-01-31", regimen="Estado|estatal")
    r.update(kw)
    return r


class Plazos(unittest.TestCase):
    def test_mes_de_fecha_a_fecha(self):
        self.assertEqual(rg.mas_meses(date(2026, 3, 15)), date(2026, 4, 15))

    def test_dia_inexistente_va_al_ultimo_del_mes(self):
        self.assertEqual(rg.mas_meses(date(2026, 1, 31)), date(2026, 2, 28))
        self.assertEqual(rg.mas_meses(date(2028, 1, 31)), date(2028, 2, 29))

    def test_cambio_de_año(self):
        self.assertEqual(rg.mas_meses(date(2026, 12, 10)), date(2027, 1, 10))

    def test_limite_con_y_sin_ampliacion(self):
        # 28/02/2026 es sábado: el vencimiento pasa al lunes 2 de marzo (art. 30.5 Ley 39/2015).
        self.assertEqual(rg.limite(fila()), date(2026, 3, 2))
        self.assertEqual(rg.limite(fila(fecha_ampliacion="2026-02-10")), date(2026, 3, 31))

    def test_festivos_nacionales_y_viernes_santo(self):
        self.assertEqual(rg.habil(date(2026, 12, 8)), date(2026, 12, 9))
        self.assertEqual(rg.habil(date(2026, 4, 3)), date(2026, 4, 6))   # Viernes Santo y fin de semana
        self.assertEqual(rg.pascua(2027), date(2027, 3, 28))

    def test_base_es_la_recepcion_por_el_organo_si_consta(self):
        self.assertEqual(rg.limite(fila(fecha_recepcion_organo="2026-02-10")), date(2026, 3, 10))

    def test_festivos_adicionales(self):
        rg.FESTIVOS_ADICIONALES.add(date(2026, 3, 2))
        try:
            self.assertEqual(rg.limite(fila()), date(2026, 3, 3))
        finally:
            rg.FESTIVOS_ADICIONALES.clear()


class Validacion(unittest.TestCase):
    def test_registro_correcto(self):
        self.assertEqual(rg.validar([fila(fecha_respuesta="2026-02-20", resultado="concedida",
                                          documentos="acta_recepcion;certificacion_final")]), [])

    def test_obra_repetida(self):
        self.assertTrue(any("repetido" in e for e in rg.validar([fila(), fila()])))

    def test_silencio_con_respuesta_en_plazo(self):
        self.assertTrue(any("silencio" in e for e in rg.validar([fila(fecha_respuesta="2026-02-10", resultado="silencio")])))

    def test_valor_no_permitido_y_documento_desconocido(self):
        errores = rg.validar([fila(fecha_respuesta="2026-02-10", resultado="vale", documentos="acta")])
        self.assertTrue(any("resultado no permitido" in e for e in errores))
        self.assertTrue(any("documento no reconocido" in e for e in errores))

    def test_fecha_mal_escrita(self):
        self.assertTrue(any("no es una fecha" in e for e in rg.validar([fila(fecha_respuesta="20/02/2026")])))

    def test_replanteo_posterior_a_la_recepcion(self):
        errores = rg.validar([fila(fecha_replanteo="2025-06-01", fecha_recepcion_obra="2025-01-01")])
        self.assertTrue(any("replanteo" in e for e in errores))
        self.assertEqual(rg.validar([fila(fecha_replanteo="2024-02-01", fecha_recepcion_obra="2025-01-01")]), [])

    def test_cumplimiento_sin_estimatoria(self):
        self.assertTrue(any("cumplimiento" in e for e in rg.validar([fila(cumplimiento="cumplida")])))


class Pendientes(unittest.TestCase):
    def test_silencio_propone_reclamar_en_un_mes(self):
        tareas = rg.pendientes([fila()], date(2026, 3, 5))
        self.assertEqual(tareas[0][0], date(2026, 4, 2))
        self.assertIn("provisional", tareas[0][2] + "provisional")
        self.assertIn("reclamar", tareas[0][2])

    def test_dentro_de_plazo_espera(self):
        self.assertIn("esperar", rg.pendientes([fila()], date(2026, 2, 10))[0][2])

    def test_estimatoria_sin_cumplimiento(self):
        r = fila(fecha_reclamacion="2026-03-01", fecha_resolucion_reclamacion="2026-05-01", resultado_reclamacion="estimatoria")
        self.assertTrue(any("comprobar" in t[2] for t in rg.pendientes([r], date(2026, 6, 15))))


class Descartadas(unittest.TestCase):
    def test_descartada_sale_de_pendientes(self):
        self.assertEqual(rg.pendientes([fila(fecha_envio="", resultado="descartada")], date(2026, 3, 1)), [])

    def test_descartada_valida_solo_sin_fechas(self):
        self.assertEqual(rg.validar([fila(fecha_envio="", resultado="descartada")]), [])
        self.assertTrue(any("descartada" in e for e in rg.validar([fila(resultado="descartada")])))


class CicloMensual(unittest.TestCase):
    def setUp(self):
        import ciclo_mensual
        self.cm = ciclo_mensual

    def test_ficheros_necesarios(self):
        f = self.cm.ficheros_necesarios(date(2026, 3, 15), 2024)
        self.assertEqual([p for p, _ in f], ["2024", "2025", "202601", "202602", "202603"])
        self.assertEqual([p for p, siempre in f if siempre], ["202603"])   # el mes en curso se vuelve a bajar

    def test_enero(self):
        f = self.cm.ficheros_necesarios(date(2027, 1, 5), 2026)
        self.assertEqual(f, [("2026", False), ("202701", True)])

    @unittest.skipIf(so is None, "faltan fase0_placsp o investigacion_doc_ccn")
    def test_prioridad_llega_al_lote(self):
        """--prioridad del ciclo se aplica al lote del mes (sin descarga, reutilizando un escaneo mínimo)."""
        import subprocess
        for prioridad, esperada in (("antiguedad", ["vieja"]), ("terminacion", ["marcada"])):
            with tempfile.TemporaryDirectory() as d:
                with open(os.path.join(d, "obras_protocolo.csv"), "w", newline="", encoding="utf-8") as fh:
                    w = csv.DictWriter(fh, fieldnames=so.CAMPOS)
                    w.writeheader()
                    comun = {**{c: "" for c in so.CAMPOS}, "estado": "ADJ", "fecha_adjudicacion": "2023-01-01",
                             "fecha_inicio": "2023-02-01", "presupuesto_sin_iva": "1500000", "fin_definitivo": "False",
                             "organo_id": "O1", "primer_anuncio": "2022-12-01"}
                    w.writerow({**comun, "id": "vieja", "titulo": "Asfaltado de caminos rurales del norte", "fin_teorico": "2025-08-10"})
                    w.writerow({**comun, "id": "marcada", "titulo": "Construcción del pabellón polideportivo municipal Valdeverde",
                                "fin_teorico": "2025-08-20"})
                    w.writerow({**comun, "id": "b", "estado": "PUB", "titulo": "Terminación del pabellón polideportivo municipal Valdeverde",
                                "fecha_adjudicacion": "", "fin_teorico": "", "primer_anuncio": "2025-06-01"})
                open(os.path.join(d, "vacio.zip"), "w").close()   # solo tiene que existir: el escaneo se reutiliza
                r = subprocess.run([sys.executable, "-I", "-X", "utf8", os.path.join(AQUI, "ciclo_mensual.py"),
                                    "--organizacion", "PRUEBA", "--fecha", "2026-01-01", "--trabajo", d, "--sin-descarga",
                                    "--datos", os.path.join(d, "*.zip"), "--reutilizar-escaneo", "--tope", "1",
                                    "--muestra", "0", "--prioridad", prioridad], capture_output=True, text=True, encoding="utf-8")
                self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
                with open(os.path.join(d, "lote_2026-01-01_flujo", "lote.csv"), encoding="utf-8") as fh:
                    self.assertEqual([f["id"] for f in csv.DictReader(fh)], esperada)


class Interfaz(unittest.TestCase):
    """La pestaña del protocolo de la interfaz gráfica (fase0_placsp/interfaz.py) construye la misma orden."""
    def setUp(self):
        try:
            sys.path.insert(0, os.path.join(AQUI, "..", "fase0_placsp"))
            import interfaz
        except ImportError as e:   # sin tkinter (algunas distribuciones de Linux) o sin la carpeta
            self.skipTest(str(e))
        self.i = interfaz

    def test_orden_con_datos_propios(self):
        cmd = self.i.orden_ciclo("ORG1", "T", "terminacion", ["a.zip", "b.zip"], "2000000", "3", "100", True)
        self.assertEqual(os.path.basename(cmd[cmd.index("-X") + 2]), "ciclo_mensual.py")
        for opcion, valor in (("--organizacion", "ORG1"), ("--trabajo", "T"), ("--prioridad", "terminacion"),
                              ("--min", "2000000"), ("--tope", "3"), ("--muestra", "100"),
                              ("--datos", os.pathsep.join(["a.zip", "b.zip"]))):
            self.assertEqual(cmd[cmd.index(opcion) + 1], valor)
        self.assertIn("--sin-descarga", cmd)
        self.assertIn("--reutilizar-escaneo", cmd)

    def test_orden_con_descarga(self):
        cmd = self.i.orden_ciclo("ORG1", "T")
        self.assertNotIn("--sin-descarga", cmd)
        self.assertEqual(cmd[cmd.index("--prioridad") + 1], "antiguedad")

    def test_codigo_de_organizacion(self):
        self.assertTrue(self.i.CODIGO_ORG.fullmatch("ORG_1"))
        for malo in ("", "A", "Nombre Apellido", "x" * 21):
            self.assertFalse(self.i.CODIGO_ORG.fullmatch(malo))

    def test_prioridades_validas(self):
        import ciclo_mensual
        self.assertEqual(set(self.i.PRIORIDADES.values()), {"antiguedad", "terminacion"})


class Exportacion(unittest.TestCase):
    def test_no_exporta_campos_privados(self):
        for privado in ("organizacion", "ref_solicitud", "ref_reclamacion", "notas"):
            self.assertNotIn(privado, rg.PUBLICOS)

    def test_en_plazo(self):
        # Solo se califica con la fecha límite verificada a mano (revisión de la v0.4.6, V05 y V07).
        v = {"fecha_limite_verificada": "2026-03-02"}
        self.assertEqual(rg.en_plazo(fila(fecha_respuesta="2026-02-28", resultado="concedida", **v), HOY), "sí")
        self.assertEqual(rg.en_plazo(fila(fecha_respuesta="2026-03-03", resultado="concedida", **v), HOY), "no")
        self.assertEqual(rg.en_plazo(fila(resultado="silencio", **v), HOY), "no")
        self.assertEqual(rg.en_plazo(fila(fecha_respuesta="2026-02-28", resultado="concedida"), HOY), "")

    def test_crear_desde_lote_no_duplica(self):
        with tempfile.TemporaryDirectory() as d:
            lote, reg = os.path.join(d, "lote.csv"), os.path.join(d, "registro.csv")
            with open(lote, "w", newline="", encoding="utf-8") as fh:
                w = csv.DictWriter(fh, fieldnames=["id", "enlace", "expediente", "organo_id", "ambito", "garante"])
                w.writeheader()
                w.writerow({"id": "A", "enlace": "x", "expediente": "1", "organo_id": "O", "ambito": "estatal", "garante": "g"})
            for _ in range(2):
                sys.argv = ["registro.py", "crear", "--registro", reg, "--lote", lote]
                rg.main()
            self.assertEqual(len(rg.leer(reg)), 1)


import senal_terminacion as st  # noqa: E402


class SenalTerminacion(unittest.TestCase):
    """Cada condición de la regla E4t v2 (senal_terminacion.py), con datos inventados."""
    A = {"id": "A", "titulo": "Construcción del pabellón polideportivo municipal Valdeverde", "organo_id": "O1",
         "primer_anuncio": "2020-01-10", "fecha_inicio": "2020-06-01", "fecha_adjudicacion": "2020-05-01"}

    def b(self, **kw):
        base = {"id": "B", "titulo": "Obras de terminación del pabellón polideportivo municipal Valdeverde", "organo_id": "O1",
                "primer_anuncio": "2022-03-01", "fecha_inicio": "", "fecha_adjudicacion": ""}
        base.update(kw)
        return base

    def marca(self, a=None, b=None):
        a = a or self.A
        return st.Indice([a, b or self.b()]).terminacion(a)

    def test_positivo(self):
        self.assertTrue(self.marca())

    def test_otro_organo(self):
        self.assertIsNone(self.marca(b=self.b(organo_id="O2")))

    def test_licitacion_anterior_al_inicio(self):
        self.assertIsNone(self.marca(b=self.b(primer_anuncio="2020-03-01")))

    def test_sin_vocabulario_de_terminacion(self):
        self.assertIsNone(self.marca(b=self.b(titulo="Mejora del pabellón polideportivo municipal Valdeverde")))

    def test_titulo_poco_parecido(self):
        self.assertIsNone(self.marca(b=self.b(titulo="Terminación de la piscina cubierta de Valdeverde")))

    def test_otra_fase(self):
        a = dict(self.A, titulo="Construcción del pabellón polideportivo municipal Valdeverde fase 1")
        self.assertIsNone(self.marca(a, self.b(titulo="Terminación del pabellón polideportivo municipal Valdeverde fase 2")))

    def test_numeros_distintos(self):
        a = dict(self.A, titulo="Rehabilitación de 12 viviendas sociales del barrio Valdeverde")
        self.assertIsNone(self.marca(a, self.b(titulo="Terminación de rehabilitación de 30 viviendas sociales del barrio Valdeverde")))

    def test_acuerdo_marco_y_parte_de_otra_obra(self):
        self.assertIsNone(self.marca(b=self.b(titulo="Acuerdo marco de terminación del pabellón polideportivo municipal Valdeverde")))
        self.assertIsNone(self.marca(b=self.b(titulo="Instalaciones de terminación para la obra de pabellón polideportivo municipal Valdeverde")))


@unittest.skipIf(so is None, "seleccionar_obras no se puede importar aquí")
class Seleccion(unittest.TestCase):
    def test_garante(self):
        self.assertEqual(so.garante("1", "")[1], "Consejo de Transparencia y Buen Gobierno")
        self.assertIn("por convenio", so.garante("3", "Cantabria")[1])
        self.assertEqual(so.garante("3", "Galicia")[1], "órgano de garantía de Galicia")
        self.assertIn("comprobar", so.garante("3", "")[1])
        self.assertIn("comprobar", so.garante("4", "Galicia")[1])

    def test_todas_las_provincias(self):
        self.assertEqual(len(so.PROVINCIAS), 52)

    def _seleccionar(self, d, *args):
        sys.argv = ["seleccionar_obras.py", "seleccionar", "--obras", os.path.join(d, "obras.csv"),
                    "--carpeta", d, "--registro", os.path.join(d, "reg.csv"), *args]
        so.main()

    def test_muestra_fija_se_completa_sin_repetir(self):
        with tempfile.TemporaryDirectory() as d:
            with open(os.path.join(d, "obras.csv"), "w", newline="", encoding="utf-8") as fh:
                w = csv.DictWriter(fh, fieldnames=so.CAMPOS)
                w.writeheader()
                for i in range(40):   # 40 obras de 2 M€ vencidas; la mitad del mismo órgano
                    w.writerow({**{c: "" for c in so.CAMPOS}, "id": f"o{i}", "estado": "RES", "fecha_adjudicacion": "2024-01-01",
                                "fin_teorico": "2025-01-01", "presupuesto_sin_iva": "2000000", "fin_definitivo": "False",
                                "organo_id": "MISMO" if i % 2 else f"org{i}", "titulo": f"Obra {i}", "expediente": str(i)})
            self._seleccionar(d, "--fecha", "2026-01-01", "--muestra", "10", "--nombre", "m")
            lote1 = os.path.join(d, "lote_2026-01-01_m")
            with open(os.path.join(lote1, "muestra.csv"), encoding="utf-8") as fh:
                muestra = {r["id"] for r in csv.DictReader(fh)}
            sys.argv = ["registro.py", "crear", "--registro", os.path.join(d, "reg.csv"), "--lote", os.path.join(lote1, "lote.csv")]
            rg.main()
            vistas = {r["id_obra"] for r in rg.leer(os.path.join(d, "reg.csv"))}
            for mes in ("2026-02-01", "2026-03-01", "2026-04-01"):
                self._seleccionar(d, "--fecha", mes, "--lista", os.path.join(lote1, "muestra.csv"), "--nombre", "m")
                with open(os.path.join(d, f"lote_{mes}_m", "lote.csv"), encoding="utf-8") as fh:
                    nuevas = {r["id"] for r in csv.DictReader(fh)}
                self.assertFalse(nuevas & vistas, "una obra se preguntó dos veces")
                sys.argv = ["registro.py", "crear", "--registro", os.path.join(d, "reg.csv"),
                            "--lote", os.path.join(d, f"lote_{mes}_m", "lote.csv")]
                rg.main()
                vistas |= nuevas
            self.assertEqual(len(muestra), 10)
            self.assertEqual(vistas, muestra)

    def test_tope_por_organo(self):
        with tempfile.TemporaryDirectory() as d:
            with open(os.path.join(d, "obras.csv"), "w", newline="", encoding="utf-8") as fh:
                w = csv.DictWriter(fh, fieldnames=so.CAMPOS)
                w.writeheader()
                for i in range(10):
                    w.writerow({**{c: "" for c in so.CAMPOS}, "id": f"o{i}", "estado": "ADJ", "fecha_adjudicacion": "2024-01-01",
                                "fin_teorico": "2025-01-01", "presupuesto_sin_iva": "1500000", "fin_definitivo": "False",
                                "organo_id": "MISMO"})
            self._seleccionar(d, "--fecha", "2026-01-01", "--tope", "3")
            with open(os.path.join(d, "lote_2026-01-01", "lote.csv"), encoding="utf-8") as fh:
                self.assertEqual(len(list(csv.DictReader(fh))), 3)

    def _obras(self, d, n, organo="MISMO", fin=False):
        with open(os.path.join(d, "obras.csv"), "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=so.CAMPOS)
            w.writeheader()
            for i in range(n):
                w.writerow({**{c: "" for c in so.CAMPOS}, "id": f"o{i}", "estado": "ADJ", "fecha_adjudicacion": "2024-01-01",
                            "fin_teorico": "2025-01-01", "presupuesto_sin_iva": "1500000",
                            "fin_definitivo": str(fin and i == 0), "organo_id": organo})

    def _lote(self, d, nombre):
        with open(os.path.join(d, nombre, "lote.csv"), encoding="utf-8") as fh:
            return [r["id"] for r in csv.DictReader(fh)]

    def test_dos_lotes_el_mismo_dia_no_repiten_ni_superan_el_tope(self):
        # Reproduce la contraprueba de la revisión adversarial (P7): dos ejecuciones el mismo día sin registrar.
        with tempfile.TemporaryDirectory() as d:
            self._obras(d, 10)
            self._seleccionar(d, "--fecha", "2026-01-01", "--nombre", "run1")
            self._seleccionar(d, "--fecha", "2026-01-01", "--nombre", "run2")
            r1, r2 = self._lote(d, "lote_2026-01-01_run1"), self._lote(d, "lote_2026-01-01_run2")
            self.assertEqual(len(r1), 4)
            self.assertEqual(r2, [])                 # el órgano ya tiene sus 4 de enero
            self._seleccionar(d, "--fecha", "2026-02-01", "--nombre", "feb")
            r3 = self._lote(d, "lote_2026-02-01_feb")
            self.assertEqual(len(r3), 4)
            self.assertFalse(set(r1) & set(r3))      # febrero: otras 4, sin repetir

    def test_no_sobrescribe_un_lote(self):
        with tempfile.TemporaryDirectory() as d:
            self._obras(d, 2)
            self._seleccionar(d, "--fecha", "2026-01-01")
            with self.assertRaises(SystemExit):
                self._seleccionar(d, "--fecha", "2026-01-01")

    def test_cerrojo_impide_dos_selecciones_a_la_vez(self):
        with tempfile.TemporaryDirectory() as d:
            self._obras(d, 2)
            with open(os.path.join(d, ".seleccion.lock"), "w") as fh:
                fh.write(str(os.getpid()))   # un proceso vivo: esta misma prueba
            with self.assertRaises(SystemExit):
                self._seleccionar(d, "--fecha", "2026-01-01")

    def test_cerrojo_de_seleccion_interrumpida_se_retira(self):
        import subprocess
        with tempfile.TemporaryDirectory() as d:
            self._obras(d, 2)
            p = subprocess.Popen([sys.executable, "-c", "pass"])
            p.wait()                          # proceso ya terminado, como tras cancelar
            with open(os.path.join(d, ".seleccion.lock"), "w") as fh:
                fh.write(str(p.pid))
            self._seleccionar(d, "--fecha", "2026-01-01")
            self.assertTrue(os.path.exists(os.path.join(d, "lote_2026-01-01", "lote.csv")))

    def test_seguimiento_registra_la_obra_que_publica_su_fin_despues(self):
        with tempfile.TemporaryDirectory() as d:
            self._obras(d, 6, organo="")
            with open(os.path.join(d, "marco.csv"), "w", encoding="utf-8") as fh:
                fh.write("id\n" + "\n".join(f"o{i}" for i in range(6)) + "\no_desaparecida\n")
            self._obras(d, 6, organo="", fin=True)   # o0 publica su fin después del sorteo
            self._seleccionar(d, "--fecha", "2026-01-01", "--lista", os.path.join(d, "marco.csv"), "--tope", "10",
                              "--justificacion-tope", "prueba con un solo órgano")
            with open(os.path.join(d, "lote_2026-01-01", "seguimiento_muestra.csv"), encoding="utf-8") as fh:
                estado = {r["id"]: r["estado"] for r in csv.DictReader(fh)}
            self.assertEqual(len(estado), 7)          # el denominador no cambia
            self.assertEqual(estado["o0"], "excluida: ya consta un indicador de fin")
            self.assertEqual(estado["o_desaparecida"], "no encontrada en los datos")
            self.assertEqual(estado["o1"], "en este lote")

    def test_prioridad_terminacion(self):
        with tempfile.TemporaryDirectory() as d:
            with open(os.path.join(d, "obras.csv"), "w", newline="", encoding="utf-8") as fh:
                w = csv.DictWriter(fh, fieldnames=so.CAMPOS)
                w.writeheader()
                comun = {**{c: "" for c in so.CAMPOS}, "estado": "ADJ", "fecha_adjudicacion": "2023-01-01", "fecha_inicio": "2023-02-01",
                         "presupuesto_sin_iva": "1500000", "fin_definitivo": "False", "organo_id": "O1", "primer_anuncio": "2022-12-01"}
                w.writerow({**comun, "id": "vieja", "titulo": "Asfaltado de caminos rurales del norte", "fin_teorico": "2024-01-01"})
                w.writerow({**comun, "id": "marcada", "titulo": "Construcción del pabellón polideportivo municipal Valdeverde",
                            "fin_teorico": "2025-01-01"})
                w.writerow({**comun, "id": "b", "estado": "PUB", "titulo": "Terminación del pabellón polideportivo municipal Valdeverde",
                            "fecha_adjudicacion": "", "fin_teorico": "", "primer_anuncio": "2025-06-01"})
            self._seleccionar(d, "--fecha", "2026-01-01", "--tope", "1", "--nombre", "antig")
            self.assertEqual(self._lote(d, "lote_2026-01-01_antig"), ["vieja"])
            os.remove(os.path.join(d, "lote_2026-01-01_antig", "lote.csv"))
            self._seleccionar(d, "--fecha", "2026-01-01", "--tope", "1", "--nombre", "term", "--prioridad", "terminacion")
            with open(os.path.join(d, "lote_2026-01-01_term", "lote.csv"), encoding="utf-8") as fh:
                filas = list(csv.DictReader(fh))
            self.assertEqual([f["id"] for f in filas], ["marcada"])
            self.assertIn("terminacion", filas[0]["senal_terminacion"])

    def test_plantilla_se_rellena(self):
        with open(so.PLANTILLA, encoding="utf-8") as fh:
            texto = fh.read().format(organo="O", expediente="E", titulo="T", enlace="L")
        self.assertIn("«T»", texto)
        self.assertNotIn("{", texto)


if __name__ == "__main__":
    unittest.main()
