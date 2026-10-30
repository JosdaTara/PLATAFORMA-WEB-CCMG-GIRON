"""Pruebas de exportación a PDF y Excel: RF27 y HU-43 (criterios 1–3)."""
import datetime
import io
from decimal import Decimal

from django.urls import reverse
from openpyxl import load_workbook

from formacion.models import InscripcionFormacion, ProcesoFormacion
from ofrendas.models import Ofrenda
from pva import periodos
from pva.models import Actividad, Asistencia, Reporte
from pva.tests.test_casas_vida import BaseCasasVida

HOY = datetime.date.today()
SEMANA = periodos.semana(HOY)


def celdas(resp):
    """Todo el texto de la primera hoja del Excel exportado."""
    hoja = load_workbook(io.BytesIO(resp.content)).worksheets[0]
    return " | ".join(str(c) for fila in hoja.iter_rows(values_only=True) for c in fila if c is not None)


class ExportarTests(BaseCasasVida):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        act = Actividad.objects.create(id_casa_vida=cls.casa, titulo="Reunión", fecha=SEMANA.inicio, id_responsable=cls.lider)
        Asistencia.objects.create(id_actividad=act, id_participante=cls.ana, presente=True)
        Asistencia.objects.create(id_actividad=act, id_participante=cls.beto, presente=False)
        cls.reporte_casa = Reporte.objects.create(
            tipo_modulo="CASA_VIDA", tipo_reporte="CASA_VIDA", id_usuario_envia=cls.lider, id_usuario_destino=cls.supervisor,
            id_casa_vida=cls.casa, id_area=cls.area, periodo=SEMANA.etiqueta, fecha_inicio=SEMANA.inicio, fecha_fin=SEMANA.fin,
            observaciones="Semana tranquila",
        )
        mes = periodos.mes(SEMANA.inicio)
        cls.reporte_general = Reporte.objects.create(
            tipo_modulo="CASA_VIDA", tipo_reporte="GENERAL_AREA", id_usuario_envia=cls.supervisor, id_area=cls.area,
            periodo=mes.etiqueta, fecha_inicio=mes.inicio, fecha_fin=mes.fin,
        )
        Reporte.objects.filter(pk=cls.reporte_casa.pk).update(id_reporte_general=cls.reporte_general)

    def exportar(self, url, formato, **params):
        return self.client.get(url, {**params, "formato": formato})

    def assertArchivo(self, resp, formato):
        self.assertEqual(resp.status_code, 200)
        self.assertIn("attachment;", resp["Content-Disposition"])
        self.assertIn(f".{formato}\"", resp["Content-Disposition"])
        if formato == "pdf":
            self.assertEqual(resp["Content-Type"], "application/pdf")
            self.assertTrue(resp.content.startswith(b"%PDF"))
        else:
            self.assertIn("spreadsheetml", resp["Content-Type"])

    def test_reporte_semanal_en_ambos_formatos(self):
        self.entrar(self.lider)
        url = reverse("pva:reporte_detalle", args=[self.reporte_casa.pk])
        for formato in ("pdf", "xlsx"):
            self.assertArchivo(self.exportar(url, formato), formato)
        texto = celdas(self.exportar(url, "xlsx"))
        self.assertIn("Reporte semanal · Casa Norte", texto)
        self.assertIn(f"{SEMANA.inicio:%d/%m/%Y} al {SEMANA.fin:%d/%m/%Y}", texto)  # criterio 3: periodo
        self.assertIn("Generado", texto)  # criterio 3: fecha de generación
        self.assertIn(f"{datetime.date.today():%d/%m/%Y}", texto)
        self.assertIn("Semana tranquila", texto)
        self.assertIn("Ley 1581", texto)

    def test_reporte_general(self):
        self.entrar(self.pastor)
        url = reverse("pva:reporte_detalle", args=[self.reporte_general.pk])
        self.assertArchivo(self.exportar(url, "pdf"), "pdf")
        texto = celdas(self.exportar(url, "xlsx"))
        self.assertIn("Reporte general · Área Norte", texto)
        self.assertIn("Casa Norte", texto)

    def test_solo_exporta_lo_que_el_rol_puede_ver(self):
        self.entrar(self.supervisor2)
        for formato in ("pdf", "xlsx"):
            self.assertEqual(self.exportar(reverse("pva:reporte_detalle", args=[self.reporte_casa.pk]), formato).status_code, 404)
            self.assertEqual(self.exportar(reverse("pva:reporte_generar"), formato, tipo="mensual", fecha=HOY.isoformat()).status_code, 403)
        self.entrar(self.lider2)
        self.assertEqual(self.exportar(reverse("pva:reporte_detalle", args=[self.reporte_general.pk]), "pdf").status_code, 404)

    def test_reporte_consolidado_del_pastor(self):
        self.entrar(self.pastor)
        url = reverse("pva:reporte_generar")
        self.assertArchivo(self.exportar(url, "pdf", tipo="mensual", fecha=SEMANA.inicio.isoformat()), "pdf")
        resp = self.exportar(url, "xlsx", tipo="mensual", fecha=SEMANA.inicio.isoformat(), area=self.area.pk)
        self.assertArchivo(resp, "xlsx")
        texto = celdas(resp)
        self.assertIn(periodos.mes(SEMANA.inicio).nombre, texto)
        self.assertIn("Casa Norte", texto)
        self.assertNotIn("Casa Sur", texto)  # respeta el filtro de Área
        self.assertEqual(self.exportar(url, "pdf").status_code, 404)  # sin parámetros no hay reporte

    def test_reporte_de_formacion(self):
        proceso = ProcesoFormacion.objects.create(nombre="Misiones 2026", tipo_proceso="MISIONES", id_coordinador=self.coord)
        otro = ProcesoFormacion.objects.create(nombre="Ajeno", tipo_proceso="PASOS_VIDA", id_coordinador=self.pastor)
        InscripcionFormacion.objects.create(id_participante=self.ana, id_proceso_formacion=proceso)
        self.entrar(self.coord)
        url = reverse("formacion:reportes")
        self.assertArchivo(self.exportar(url, "pdf", tipo="anual", fecha=HOY.isoformat()), "pdf")
        texto = celdas(self.exportar(url, "xlsx", tipo="anual", fecha=HOY.isoformat()))
        self.assertIn("Misiones 2026", texto)
        self.assertNotIn(otro.nombre, texto)

    def test_ofrendas(self):
        Ofrenda.objects.create(fecha=datetime.date(2026, 1, 5), concepto="Diezmo enero", valor=Decimal("120000"), id_usuario_registro=self.pastor)
        Ofrenda.objects.create(fecha=datetime.date(2026, 3, 5), concepto="Fuera de rango", valor=Decimal("1000"), id_usuario_registro=self.pastor)
        self.entrar(self.pastor)
        url = reverse("ofrendas:index")
        self.assertArchivo(self.exportar(url, "pdf", desde="2026-01-01", hasta="2026-01-31"), "pdf")
        resp = self.exportar(url, "xlsx", desde="2026-01-01", hasta="2026-01-31")
        texto = celdas(resp)
        self.assertIn("01/01/2026 al 31/01/2026", texto)
        self.assertIn("Diezmo enero", texto)
        self.assertNotIn("Fuera de rango", texto)
        hoja = load_workbook(io.BytesIO(resp.content)).worksheets[0]
        valores = [c.value for fila in hoja.iter_rows() for c in fila if c.number_format == '"$"#,##0' and c.value]
        self.assertIn(120000, valores)  # el valor queda como número en Excel
        self.entrar(self.lider)
        self.assertEqual(self.exportar(url, "xlsx").status_code, 403)

    def test_formato_desconocido_muestra_la_pagina(self):
        self.entrar(self.lider)
        resp = self.client.get(reverse("pva:reporte_detalle", args=[self.reporte_casa.pk]), {"formato": "docx"})
        self.assertEqual(resp["Content-Type"], "text/html; charset=utf-8")
        self.assertContains(resp, "formato=pdf")
