"""Pruebas con datos sintéticos (ningún dato real). Ejecutar: python -m unittest -v"""
import csv
import json
import os
import tempfile
import unittest
import zipfile

import informe_legible
import medir_ejecucion as m

NS = ('xmlns="http://www.w3.org/2005/Atom" '
      'xmlns:at="http://purl.org/atompub/tombstones/1.0" '
      'xmlns:cbc="urn:dgpe:names:draft:codice:schema:xsd:CommonBasicComponents-2" '
      'xmlns:cac="urn:dgpe:names:draft:codice:schema:xsd:CommonAggregateComponents-2" '
      'xmlns:cbc-place-ext="urn:dgpe:names:draft:codice-place-ext:schema:xsd:CommonBasicComponents-2" '
      'xmlns:cac-place-ext="urn:dgpe:names:draft:codice-place-ext:schema:xsd:CommonAggregateComponents-2"')


def entrada(ident, actualizado, tipo="3", estado="RES", adj="2023-05-10", presupuesto="2000000",
            modificaciones=0, ficheros=(), aviso_mod=False, duracion=None, duracion_final_mod=None,
            resultado="9", etiquetas=(), aviso_fin=None, anulaciones_fin=(), avisos_fin_extra=(), notas_mod=()):
    final = (f'<cbc:FinalDurationMeasure unitCode="DAY">{duracion_final_mod}</cbc:FinalDurationMeasure>'
             if duracion_final_mod else "")
    mods = "".join(f"<cac:ContractModification><cbc:ID>{i + 1}</cbc:ID>{final}</cac:ContractModification>"
                   for i in range(modificaciones))
    # Modificaciones con texto libre (cbc:Note), como las que comunican una liquidación (v2.4).
    mods += "".join(f"<cac:ContractModification><cbc:ID>{modificaciones + i + 1}</cbc:ID><cbc:Note>{n}</cbc:Note>"
                    "</cac:ContractModification>" for i, n in enumerate(notas_mod))
    periodo = (f'<cac:PlannedPeriod><cbc:DurationMeasure unitCode="MON">{duracion}</cbc:DurationMeasure>'
               "</cac:PlannedPeriod>") if duracion else ""
    docs = "".join(
        "<cac-place-ext:GeneralDocument><cac-place-ext:GeneralDocumentDocumentReference><cac:Attachment>"
        f"<cac:ExternalReference><cbc:FileName>{f}</cbc:FileName></cac:ExternalReference>"
        "</cac:Attachment></cac-place-ext:GeneralDocumentDocumentReference></cac-place-ext:GeneralDocument>"
        for f in ficheros)
    # Etiqueta de tipo documental sin nombre de archivo (contraprueba C de la revisión adversarial).
    etq = "".join(
        "<cac-place-ext:ValidNoticeInfo><cac-place-ext:AdditionalPublicationStatus>"
        "<cac-place-ext:AdditionalPublicationDocumentReference>"
        f'<cbc:DocumentTypeCode name="{e}">X</cbc:DocumentTypeCode>'
        "</cac-place-ext:AdditionalPublicationDocumentReference></cac-place-ext:AdditionalPublicationStatus>"
        "</cac-place-ext:ValidNoticeInfo>" for e in etiquetas)
    aviso = ("<cac-place-ext:ValidNoticeInfo><cbc-place-ext:NoticeTypeCode>DOC_MOD</cbc-place-ext:NoticeTypeCode>"
             "</cac-place-ext:ValidNoticeInfo>") if aviso_mod else ""
    def notice(codigo, fecha):   # como en los datos reales: tipo de anuncio y fecha
        return ("<cac-place-ext:ValidNoticeInfo>"
                f"<cbc-place-ext:NoticeTypeCode>{codigo}</cbc-place-ext:NoticeTypeCode>"
                "<cac-place-ext:AdditionalPublicationStatus><cac-place-ext:AdditionalPublicationDocumentReference>"
                f"<cbc:IssueDate>{fecha}</cbc:IssueDate></cac-place-ext:AdditionalPublicationDocumentReference>"
                "</cac-place-ext:AdditionalPublicationStatus></cac-place-ext:ValidNoticeInfo>")
    if aviso_fin:   # Anuncio de Finalización de Contrato (DOC_CCN)
        aviso += notice("DOC_CCN", aviso_fin)
    aviso += "".join(notice("DOC_CCN", f) for f in avisos_fin_extra)
    aviso += "".join(notice("ANUL_CCN", f) for f in anulaciones_fin)   # anulación (ANUL_CCN)
    return f"""<entry><id>{ident}</id><link href="https://example.invalid/{ident}"/>
<updated>{actualizado}</updated>
<cac-place-ext:ContractFolderStatus>
 <cbc:ContractFolderID>EXP-FICTICIO-{ident}</cbc:ContractFolderID>
 <cbc-place-ext:ContractFolderStatusCode>{estado}</cbc-place-ext:ContractFolderStatusCode>
 <cac-place-ext:LocatedContractingParty><cbc:ContractingPartyTypeCode>3</cbc:ContractingPartyTypeCode>
  <cac:Party><cac:PartyIdentification><cbc:ID>L000FICT</cbc:ID></cac:PartyIdentification>
  <cac:PartyName><cbc:Name>Ayuntamiento Ficticio de Ejemplo</cbc:Name></cac:PartyName></cac:Party>
 </cac-place-ext:LocatedContractingParty>
 <cac:ProcurementProject><cbc:TypeCode>{tipo}</cbc:TypeCode>
  <cac:BudgetAmount><cbc:TaxExclusiveAmount>{presupuesto}</cbc:TaxExclusiveAmount></cac:BudgetAmount>
  {periodo}
 </cac:ProcurementProject>
 <cac:TenderResult><cbc:ResultCode>{resultado}</cbc:ResultCode><cbc:AwardDate>{adj}</cbc:AwardDate>
  <cac:Contract><cbc:IssueDate>{adj}</cbc:IssueDate></cac:Contract>
  <cac:WinningParty><cac:PartyName><cbc:Name>PERSONA FICTICIA NO EXTRAER</cbc:Name></cac:PartyName></cac:WinningParty>
  <cac:AwardedTenderedProject><cac:LegalMonetaryTotal><cbc:TaxExclusiveAmount>1500000</cbc:TaxExclusiveAmount>
  </cac:LegalMonetaryTotal></cac:AwardedTenderedProject>
 </cac:TenderResult>
 {mods}{docs}{etq}{aviso}
</cac-place-ext:ContractFolderStatus></entry>"""


def feed(*cuerpos):
    return f'<?xml version="1.0" encoding="UTF-8"?><feed {NS}>' + "".join(cuerpos) + "</feed>"


FECHA_EMPATE = "2023-06-01T10:00:00+02:00"

FEED_A = feed(
    entrada("1", "2023-03-01T10:00:00+01:00"),                       # versión antigua de 1
    entrada("2", FECHA_EMPATE, modificaciones=2, aviso_mod=True,
            ficheros=["Acta_recepcion_obras.pdf", "Liquidación del contrato.pdf"]),
    entrada("3", FECHA_EMPATE, tipo="2"),                            # servicios: fuera
    entrada("4", FECHA_EMPATE, adj="2022-12-30"),                    # adjudicada en 2022: fuera
    entrada("5", FECHA_EMPATE, presupuesto="500000"),                # importe: fuera
    entrada("6", FECHA_EMPATE,
            ficheros=["Plazo de recepción de ofertas.pdf", "Certificado acuerdo de pleno.pdf",
                      "Liquidación ICIO.pdf", "Devolución garantías provisionales.pdf",
                      "Modificación fecha apertura sobre C.pdf"]),
    entrada("7", FECHA_EMPATE),                                      # será eliminada
    entrada("8", FECHA_EMPATE, duracion="6"),                        # fin = 2023-05-10 + 183 días
    entrada("9", FECHA_EMPATE, duracion="6", modificaciones=1, duracion_final_mod="1000",
            ficheros=["Decreto Ampliación plazo segundo.pdf", "Decreto Suspensión Temporal Parcial.pdf",
                      "Acuerdo JG cesión.pdf"]),
    entrada("10", FECHA_EMPATE, resultado="7"),                      # desierta: fuera
    entrada("11", FECHA_EMPATE,                                      # incidencias de licitación, no de obra
            ficheros=["Acuerdo de ampliación del plazo de presentación de ofertas.pdf"]),
    entrada("12", FECHA_EMPATE),                                     # será CERRADA: se conserva
    entrada("13", FECHA_EMPATE),                                     # será ANULADA: fuera
    entrada("14", FECHA_EMPATE),                                     # empate de fecha (ver FEED_B)
    # Contraprueba A: misma fecha, presupuestos distintos (2 M€ aquí, 12 M€ en FEED_B).
    entrada("15", FECHA_EMPATE, presupuesto="2000000"),
    # Contraprueba C: solo una etiqueta de tipo documental, sin nombre de archivo.
    entrada("16", FECHA_EMPATE, etiquetas=["Acta de recepción de obra"]),
    # Anuncio estructurado de finalización (DOC_CCN), sin ningún documento con nombre de fin.
    entrada("17", FECHA_EMPATE, duracion="1", aviso_fin="2023-06-20"),
    # Contraprueba de la revisión adversarial 3: anuncio de finalización anulado después.
    entrada("18", FECHA_EMPATE, duracion="1", aviso_fin="2023-06-20", anulaciones_fin=["2023-06-25"]),
    # Anuncio, anulación y nuevo anuncio: vuelve a haber uno vigente.
    entrada("19", FECHA_EMPATE, duracion="1", aviso_fin="2023-06-20", anulaciones_fin=["2023-06-25"],
            avisos_fin_extra=["2023-07-01"]),
)
FEED_B = feed(
    '<at:deleted-entry ref="7" when="2023-10-01T00:00:00+02:00"/>',
    '<at:deleted-entry ref="12" when="2023-10-01T00:00:00+02:00"><at:comment type="CERRADA"/></at:deleted-entry>',
    '<at:deleted-entry ref="13" when="2023-10-01T00:00:00+02:00"><at:comment type="ANULADA"/></at:deleted-entry>',
    entrada("1", "2023-09-01T10:00:00+02:00", ficheros=["Certificación nº 3 de obra.pdf"]),
    # Misma fecha que en FEED_A, con un acta añadida (corrección sin cambiar `updated`, §3.3.1).
    entrada("14", FECHA_EMPATE, ficheros=["Acta de recepción definitiva.pdf"]),
    entrada("15", FECHA_EMPATE, presupuesto="12000000"),
)


def crear_zip(ruta, primero, segundo):
    with zipfile.ZipFile(ruta, "w") as z:
        z.writestr("a.atom", primero)
        z.writestr("b.atom", segundo)


class Pruebas(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.zip = os.path.join(self.dir, "ficticio.zip")
        crear_zip(self.zip, FEED_A, FEED_B)
        self.salida = os.path.join(self.dir, "res")
        self.resumen = m.medir([self.zip], self.salida, None, 1)
        self.filas = self.leer(self.salida)

    @staticmethod
    def leer(salida):
        with open(os.path.join(salida, "expedientes_seleccionados.csv"), encoding="utf-8-sig") as f:
            return {r["id"]: r for r in csv.DictReader(f, delimiter=";")}

    def test_seleccion_aplica_criterios(self):
        # Fuera: 3 servicios, 4 de 2022, 5 importe, 7 borrada sin tipo, 10 desierta, 13 anulada.
        # 15: empate 2 M€ / 12 M€; la regla determinista elige una de las dos (ver test de empates).
        ids = sorted((i for i in self.filas if i != "15"), key=int)
        self.assertEqual(ids, ["1", "2", "6", "8", "9", "11", "12", "14", "16", "17", "18", "19"])

    def test_anulacion_del_anuncio_de_finalizacion(self):
        self.assertEqual(self.filas["18"]["anuncio_finalizacion"], "False")     # anulado: no cuenta
        self.assertEqual(self.filas["18"]["n_anulaciones_finalizacion"], "1")
        self.assertEqual(self.filas["19"]["anuncio_finalizacion"], "True")      # republicado: cuenta
        self.assertEqual(self.resumen["obras_con_anulacion_de_anuncio_finalizacion"], 2)

    def test_anuncio_de_finalizacion_cuenta_como_fin_definitivo(self):
        f = self.filas["17"]
        self.assertEqual(f["anuncio_finalizacion"], "True")
        self.assertEqual(f["fecha_anuncio_finalizacion"], "2023-06-20")
        self.assertFalse(m.sin_fin_definitivo({"anuncio_finalizacion": True, "documentos_ejecucion": {}}))
        self.assertEqual(self.resumen["seleccionados_con_anuncio_finalizacion"], 2)   # 17 y 19
        # Corte = 2023-09-01; 17, 18 y 19 vencen el 2023-06-10. 17 y 19 tienen un DOC_CCN vigente;
        # 18 lo tiene anulado, así que cuenta como «sin fin definitivo».
        self.assertEqual(self.resumen["fin_teorico_anterior_al_corte"], 3)
        self.assertEqual(self.resumen["vencidos_sin_candidato_fin_definitivo"], 1)

    def test_borrado_cerrada_se_conserva_y_anulada_no(self):
        self.assertEqual(self.filas["12"]["borrado_tipo"], "CERRADA")
        self.assertNotIn("13", self.filas)
        self.assertEqual(self.resumen["expedientes_de_obras_excluidos_por_borrado"], {"SIN_TIPO": 1, "ANULADA": 1})
        self.assertEqual(self.resumen["seleccionados_cerrados"], 1)

    def test_diagnostico_de_borrados(self):
        d = self.resumen["diagnostico_borrados"]
        for tipo in ("CERRADA", "ANULADA", "SIN_TIPO"):
            self.assertEqual(d[tipo]["refs_distintos"], 1)
            self.assertEqual(d[tipo]["de_obras_con_borrado_posterior_a_su_ultima_version"], 1)

    def test_empate_no_fusiona_y_es_determinista(self):
        f = self.filas["14"]
        self.assertEqual(f["n_versiones_empatadas"], "2")
        # La versión principal es la de más documentos (la que tiene el acta), sin mezclar campos.
        self.assertTrue(f["recepcion_definitiva"])

    def test_contraprueba_A_orden_de_lectura_no_cambia_el_resultado(self):
        zip_inv = os.path.join(self.dir, "invertido.zip")
        crear_zip(zip_inv, FEED_B, FEED_A)   # el mismo par de versiones, leído en orden inverso
        salida_inv = os.path.join(self.dir, "res_inv")
        r_inv = m.medir([zip_inv], salida_inv, None, 1, huellas=False)
        self.assertEqual(sorted(self.leer(salida_inv)), sorted(self.filas))
        self.assertEqual(r_inv["empates"], self.resumen["empates"])

    def test_contraprueba_A_cotas(self):
        e = self.resumen["empates"]
        # 15 es seleccionable con una versión (2 M€) y no con la otra (12 M€); 14 con ambas.
        self.assertEqual(e["expedientes_empatados_relevantes"], 2)
        self.assertEqual(e["seleccionados_cota_maxima"] - e["seleccionados_cota_minima"], 1)
        n = self.resumen["expedientes_seleccionados"]
        self.assertTrue(e["seleccionados_cota_minima"] <= n <= e["seleccionados_cota_maxima"])

    def test_contraprueba_C_etiqueta_documental_con_procedencia(self):
        f = self.filas["16"]
        self.assertIn("⟨etiqueta·ValidNoticeInfo⟩", f["recepcion_definitiva"])
        self.assertIn("⟨archivo·GeneralDocument⟩", self.filas["2"]["recepcion_definitiva"])

    def test_categorias_de_fin(self):
        c = m.clasificar_documento
        self.assertEqual(c("Recepción parcial") & m.DOCS_FIN_DEFINITIVO, set())
        self.assertIn("recepcion_parcial", c("Recepción parcial"))
        self.assertIn("certificacion_avance", c("Certificación nº 3 de obra.pdf"))
        self.assertNotIn("certificacion_final", c("Certificación nº 3 de obra.pdf"))
        self.assertTrue({"certificacion_final", "liquidacion"} <= c("Aprobación incidencia 1 (certificación final y liquidación)."))
        self.assertNotIn("certificacion_avance", c("Aprobación incidencia 1 (certificación final y liquidación)."))
        self.assertIn("certificacion_final", c("CFO.pdf"))
        self.assertIn("certificacion_final", c("Medición general.pdf"))
        self.assertIn("resolucion_contrato", c("Acuerdo de Resolución del contrato"))
        self.assertIn("resolucion_contrato", c("Aprobación de la resolución del contrato"))
        self.assertNotIn("resolucion_contrato", c("Inicio expediente de resolución del contrato"))
        self.assertIn("resolucion_en_tramite", c("Inicio expediente de resolución del contrato"))
        self.assertIn("resolucion_en_tramite", c("Resolución del contrato: propuesta de acuerdo"))
        self.assertNotIn("resolucion_contrato", c("Resolución de adjudicación del contrato"))

    def test_patrones_de_revisiones_anteriores(self):
        c = m.clasificar_documento
        self.assertIn("recepcion_definitiva", c("Acta de conformidad.pdf"))
        self.assertIn("recepcion_definitiva", c("Acta de entrega del edificio.pdf"))
        self.assertFalse(c("Acta de comprobación del replanteo.pdf") & (m.DOCS_FIN_DEFINITIVO | m.DOCS_FIN_PARCIAL))
        self.assertIn("certificacion_avance", c("Cert. economica parcial n 1 de obra.pdf"))
        self.assertIn("certificacion_avance", c("Certificación 15ª.pdf"))
        self.assertNotIn("liquidacion", c("Liquidación de penalidades.pdf"))
        self.assertNotIn("documento_modificacion", c("Ordenanza ICIO MODIFICACION 2016.pdf"))
        self.assertFalse(c("Cert 2 -CON7 -23 ADJUDICACION firmado.pdf") & m.DOCS_FIN_PARCIAL)
        self.assertFalse(c("Cert. eficiencia energética + informe acta replanteo") & m.DOCS_FIN_PARCIAL)
        self.assertFalse(c("Cert. MRR") & m.DOCS_FIN_PARCIAL)
        self.assertFalse(c("Acta de conformidad documentación adjudicación") & m.DOCS_FIN_DEFINITIVO)
        self.assertFalse(c("04 ACTA 19 12  2023 RECEP JUST BT EXPTE 120 2023 BIS") & m.DOCS_FIN_DEFINITIVO)
        self.assertIn("ampliacion_plazo", c("RESOLUCIO URG AMPLIACIO TERMINI EXP 5-23"))
        self.assertIn("liquidacion", c("PROP I RES LIQUIDACIÓ OBRES TERMINUS EXP 5/23"))

    def test_incidencias_durante_la_obra(self):
        f = self.filas["9"]
        self.assertTrue(f["ampliacion_plazo"])
        self.assertTrue(f["suspension"])
        self.assertTrue(f["cesion_contrato"])
        self.assertEqual(self.filas["11"]["ampliacion_plazo"], "")   # plazo de ofertas, no de obra

    def test_fin_teorico(self):
        self.assertEqual(self.filas["8"]["fin_teorico"], "2023-11-09")    # 6 × 30,44 días ≈ 183
        self.assertEqual(self.filas["9"]["fin_teorico"], "2026-02-03")    # 1000 días tras la modificación
        self.assertEqual(self.filas["1"]["fin_teorico"], "")              # sin duración: no se estima

    def test_informe_y_anexo(self):
        with open(os.path.join(self.salida, "informe.md"), encoding="utf-8") as f:
            informe = f.read()
        self.assertIn("| **Principal** (incluye cerrados) |", informe)
        self.assertIn("ausencia de coincidencias detectadas por el clasificador", informe)
        self.assertNotIn("NO COMPARABLE", informe)                  # la tabla va al anexo
        with open(os.path.join(self.salida, "anexo_por_tipo_administracion.md"), encoding="utf-8") as f:
            self.assertIn("NO COMPARABLE", f.read())

    def test_usa_ultima_version(self):
        self.assertEqual(self.filas["1"]["actualizado"], "2023-09-01T10:00:00+02:00")
        self.assertIn("Certificación", self.filas["1"]["certificacion_avance"])

    def test_borrado_sin_tipo_elimina(self):
        self.assertNotIn("7", self.filas)

    def test_modificaciones_y_documentos(self):
        f = self.filas["2"]
        self.assertEqual(f["n_modificaciones"], "2")
        self.assertEqual(f["anuncio_modificacion"], "True")
        self.assertTrue(f["recepcion_definitiva"])
        self.assertTrue(f["liquidacion"])

    def test_falsos_positivos_conocidos_excluidos(self):
        f = self.filas["6"]
        for cat in ("recepcion_definitiva", "certificacion_avance", "liquidacion", "devolucion_garantia",
                    "documento_modificacion"):
            self.assertEqual(f[cat], "", cat)

    def test_no_extrae_adjudicatario(self):
        for nombre in os.listdir(self.salida):
            with open(os.path.join(self.salida, nombre), encoding="utf-8-sig") as f:
                self.assertNotIn("PERSONA FICTICIA", f.read(), nombre)

    def test_exclusiones_por_codigo(self):
        self.assertEqual(self.resumen["excluidos_por_codigo_de_resultado"], {"7": 1})

    def test_manifiesto(self):
        with open(os.path.join(self.salida, "manifiesto.json"), encoding="utf-8") as f:
            man = json.load(f)
        self.assertEqual(len(man["ficheros"][0]["sha256"]), 64)
        self.assertEqual(len(man["programa"]["sha256"]), 64)

    def test_candidatos_fin(self):
        with open(os.path.join(self.salida, "candidatos_fin.csv"), encoding="utf-8-sig") as f:
            ids = {r["id"] for r in csv.DictReader(f, delimiter=";")}
        self.assertTrue({"1", "2", "14", "16"} <= ids)
        self.assertNotIn("8", ids)

    def test_informe_legible_cuadra_con_el_resumen(self):
        r = informe_legible.generar(self.salida)    # se detiene si los recuentos no cuadran
        self.assertEqual(r["sin_fin"], self.resumen["vencidos_sin_candidato_fin_definitivo"])
        with open(os.path.join(self.salida, "lista_obras.csv"), encoding="utf-8-sig") as f:
            filas = list(csv.DictReader(f, delimiter=";"))
        self.assertEqual(len(filas), self.resumen["expedientes_seleccionados"])
        self.assertTrue(all("." not in x["Presupuesto sin IVA (€)"] for x in filas))   # coma decimal
        with open(os.path.join(self.salida, "informe.html"), encoding="utf-8") as f:
            pagina = f.read()
        self.assertIn(r["porcentaje"], pagina)
        self.assertNotIn("PERSONA FICTICIA", pagina)
        self.assertNotIn("⟨", pagina)                 # sin la procedencia técnica de los documentos


class PruebasAnuncioFinalizacion(unittest.TestCase):
    """Vigencia de DOC_CCN frente a ANUL_CCN en una sola entrada (revisión de la v0.4.3)."""

    @staticmethod
    def expediente(**kw):
        raiz = m.ET.fromstring(feed(entrada("1", FECHA_EMPATE, duracion="1", **kw)))
        return m.extraer(raiz.find(m.ATOM + "entry"))[2]

    def test_anulado_no_cuenta(self):
        e = self.expediente(aviso_fin="2023-06-20", anulaciones_fin=["2023-06-25"])
        self.assertFalse(e.anuncio_finalizacion)
        self.assertTrue(m.sin_fin_definitivo({"anuncio_finalizacion": e.anuncio_finalizacion,
                                              "documentos_ejecucion": e.documentos_ejecucion}))

    def test_anulacion_sin_anuncio_no_crea_fin(self):
        e = self.expediente(anulaciones_fin=["2023-06-25"])
        self.assertFalse(e.anuncio_finalizacion)
        self.assertEqual((e.n_anuncios_finalizacion, e.n_anulaciones_finalizacion), (0, 1))

    def test_varios_lotes_una_anulacion_sigue_vigente(self):
        # Límite conocido: la sindicación no dice a qué lote se refiere cada anuncio o anulación.
        # Con dos anuncios y una anulación se da por vigente uno, sin saber cuál.
        e = self.expediente(aviso_fin="2023-06-20", avisos_fin_extra=["2023-06-21"],
                            anulaciones_fin=["2023-06-25"])
        self.assertTrue(e.anuncio_finalizacion)
        self.assertEqual((e.n_anuncios_finalizacion, e.n_anulaciones_finalizacion), (2, 1))


if __name__ == "__main__":
    unittest.main()


class PruebasFinEnNotaModificacion(unittest.TestCase):
    """v2.4: fin comunicado en el texto de una modificación publicada."""

    def expediente(self, **kw):
        raiz = m.ET.fromstring(feed(entrada("1", FECHA_EMPATE, duracion="1", **kw)))
        return m.extraer(next(iter(raiz)))[2]

    def fin(self, *notas):
        e = self.expediente(notas_mod=notas)
        return not m.sin_fin_definitivo({"anuncio_finalizacion": e.anuncio_finalizacion,
                                         "documentos_ejecucion": e.documentos_ejecucion})

    def test_liquidacion_y_certificacion_final_cuentan(self):
        self.assertTrue(self.fin("Se formaliza la liquidación del contrato"))
        self.assertTrue(self.fin("CERTIFICACIÓN FINAL DE OBRA"))
        self.assertTrue(self.fin("Liquidación"))

    def test_falsos_positivos_de_la_revision_adversarial(self):
        for t in ("Liquidación de penalidades contractuales", "Liquidación de anticipos", "Liquidación provisional de la obra",
                  "Certificación final de la fase 1", "Liquidación lote 2", "Certificación final y liquidación a cuenta"):
            self.assertFalse(self.fin(t), t)

    def test_candidato_se_anota_pero_no_cuenta(self):
        e = self.expediente(notas_mod=["Reajuste de anualidades para el pago de la certificación final de obra"])
        self.assertIn(m.CATEGORIA_NOTA_CANDIDATO, e.documentos_ejecucion)
        self.assertTrue(m.sin_fin_definitivo({"anuncio_finalizacion": e.anuncio_finalizacion,
                                              "documentos_ejecucion": e.documentos_ejecucion}))

    def test_textos_que_no_son_fin(self):
        self.assertFalse(self.fin("Recepciones Parciales"))
        self.assertFalse(self.fin("Liquidación de daños y perjuicios"))
        self.assertFalse(self.fin("El acto objeto de la presente publicación pone fin a la vía administrativa"))
        self.assertFalse(self.fin("SUSPENSION - SUSPENSION TEMP. TOTAL", "Ampliación de plazo"))

    def test_procedencia_y_cuenta_como_modificacion(self):
        e = self.expediente(notas_mod=["Se formaliza la liquidación del contrato"])
        self.assertEqual(e.n_modificaciones, 1)
        self.assertIn("⟨nota·modificación 1⟩", e.documentos_ejecucion[m.CATEGORIA_NOTA][0])

    def test_sin_texto_no_cambia_nada(self):
        e = self.expediente(modificaciones=2)
        self.assertNotIn(m.CATEGORIA_NOTA, e.documentos_ejecucion)
