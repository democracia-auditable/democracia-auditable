"""Pruebas de la selección del estado final (revisión adversarial de ChatGPT, punto B).
Datos sintéticos. Ejecutar: python -m unittest -v test_escanear"""
import os
import sys
import tempfile
import unittest
import zipfile

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "fase0_placsp"))
import escanear  # noqa: E402
from test_medir_ejecucion import entrada, feed  # noqa: E402

T1 = "2024-01-01T10:00:00+01:00"
T2 = "2024-06-01T10:00:00+02:00"


def estados(*feeds):
    d = tempfile.mkdtemp()
    ruta = os.path.join(d, "f.zip")
    with zipfile.ZipFile(ruta, "w") as z:
        for i, cuerpo in enumerate(feeds):
            z.writestr(f"{i}.atom", feed(*cuerpo))
    trabajos = [(ruta, n) for n in sorted(zipfile.ZipFile(ruta).namelist())]
    ultima, borrados = escanear.acumular(map(escanear.procesar, trabajos))
    res, excluidos = escanear.estados_finales(ultima, borrados)
    return {e["id"]: e for e in res}, excluidos


class PruebasSeleccion(unittest.TestCase):
    def test_anuncio_antiguo_retirado_en_version_posterior(self):
        e, _ = estados([entrada("1", T1, aviso_fin="2023-12-20")], [entrada("1", T2)])
        self.assertFalse(e["1"]["anuncio_finalizacion"])

    def test_anuncio_en_version_posterior(self):
        e, _ = estados([entrada("1", T1)], [entrada("1", T2, aviso_fin="2024-05-20")])
        self.assertTrue(e["1"]["anuncio_finalizacion"])

    def test_borrado_anulada_posterior_excluye(self):
        borrado = '<at:deleted-entry ref="1" when="2024-07-01T00:00:00+02:00"><at:comment type="ANULADA"/></at:deleted-entry>'
        e, excl = estados([entrada("1", T1, aviso_fin="2023-12-20")], [borrado])
        self.assertNotIn("1", e)
        self.assertEqual(excl, 1)

    def test_borrado_cerrada_se_conserva(self):
        borrado = '<at:deleted-entry ref="1" when="2024-07-01T00:00:00+02:00"><at:comment type="CERRADA"/></at:deleted-entry>'
        e, _ = estados([entrada("1", T1, aviso_fin="2023-12-20")], [borrado])
        self.assertTrue(e["1"]["anuncio_finalizacion"])

    def test_borrado_anterior_a_la_ultima_version_no_excluye(self):
        borrado = '<at:deleted-entry ref="1" when="2024-03-01T00:00:00+01:00"><at:comment type="ANULADA"/></at:deleted-entry>'
        e, _ = estados([borrado], [entrada("1", T2, aviso_fin="2024-05-20")])
        self.assertIn("1", e)

    def test_empate_con_anuncio_en_una_sola_version(self):
        # Misma `updated`; la versión con anuncio tiene un documento más y gana por la regla del estudio.
        a = entrada("1", T2)
        b = entrada("1", T2, aviso_fin="2024-05-20", ficheros=["Acta de recepción.pdf"])
        e1, _ = estados([a], [b])
        e2, _ = estados([b], [a])
        self.assertTrue(e1["1"]["ccn_discrepa_en_empate"])
        self.assertEqual(e1["1"]["anuncio_finalizacion"], e2["1"]["anuncio_finalizacion"])   # no depende del orden
        self.assertEqual(e1["1"]["n_versiones_empatadas"], 2)

    def test_otros_tipos_se_conservan_reducidos(self):
        e, _ = estados([entrada("1", T1, tipo="2", aviso_fin="2023-12-20")])
        self.assertTrue(e["1"]["anuncio_finalizacion"])
        self.assertEqual(e["1"]["tipo_contrato"], "2")
        self.assertNotIn("documentos_ejecucion", e["1"])


if __name__ == "__main__":
    unittest.main()
