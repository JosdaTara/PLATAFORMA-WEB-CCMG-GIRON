"""Pruebas de seguimiento y reportes: RF11, RF13–RF16, RN06, RN07, RN10, RN19."""
import datetime

from django.urls import reverse

from nucleo.models import Auditoria
from pva import periodos
from pva.models import Actividad, Asistencia, CasaVidaMiembro, Reporte, Seguimiento

from .test_casas_vida import BaseCasasVida

HOY = datetime.date.today()
SEMANA = periodos.semana(HOY)
SEMANA_PASADA = periodos.semana(HOY - datetime.timedelta(weeks=1))


class PeriodosTests(BaseCasasVida):
    def test_semana_mes_anio(self):
        p = periodos.semana(datetime.date(2026, 10, 30))
        self.assertEqual((p.etiqueta, p.inicio, p.fin), ("2026-S44", datetime.date(2026, 10, 26), datetime.date(2026, 11, 1)))
        m = periodos.mes(datetime.date(2026, 2, 10))
        self.assertEqual((m.etiqueta, m.inicio, m.fin), ("2026-02", datetime.date(2026, 2, 1), datetime.date(2026, 2, 28)))
        self.assertEqual(periodos.anio(datetime.date(2026, 5, 1)).etiqueta, "2026")

    def test_lunes_transcurridos(self):
        octubre = periodos.mes(datetime.date(2026, 10, 1))
        self.assertEqual(periodos.lunes_transcurridos(octubre, hoy=datetime.date(2026, 10, 31)), 4)
        self.assertEqual(periodos.lunes_transcurridos(octubre, hoy=datetime.date(2026, 10, 4)), 0)


class SeguimientoTests(BaseCasasVida):
    """RF11: el Pastor registra; Supervisor y Líder consultan su alcance; el apoyo no accede."""

    def crear(self, participante, **extra):
        datos = dict(id_participante=participante, id_usuario=self.pastor, observacion="Visita", tipo_modulo="CASA_VIDA")
        datos.update(extra)
        return Seguimiento.objects.create(**datos)

    def test_pastor_registra_seguimiento(self):
        self.entrar(self.pastor)
        resp = self.client.post(
            reverse("pva:seguimiento_crear"),
            {"id_participante": self.ana.pk, "fecha": HOY.isoformat(), "tipo": "LLAMADA", "estado": "ABIERTO", "observacion": " Llamada de bienvenida "},
        )
        self.assertRedirects(resp, reverse("pva:participante_detalle", args=[self.ana.pk]))
        s = Seguimiento.objects.get()
        self.assertEqual((s.id_usuario, s.observacion, s.tipo), (self.pastor, "Llamada de bienvenida", "LLAMADA"))
        self.assertTrue(Auditoria.objects.filter(entidad="seguimiento", id_entidad=s.pk).exists())

    def test_fecha_futura_rechazada(self):
        self.entrar(self.pastor)
        resp = self.client.post(
            reverse("pva:seguimiento_crear"),
            {"id_participante": self.ana.pk, "fecha": (HOY + datetime.timedelta(days=2)).isoformat(), "tipo": "VISITA", "estado": "ABIERTO", "observacion": "x"},
        )
        self.assertContains(resp, "no puede ser futura")

    def test_pastor_actualiza_estado(self):
        s = self.crear(self.ana)
        self.entrar(self.pastor)
        self.client.post(
            reverse("pva:seguimiento_editar", args=[s.pk]),
            {"id_participante": self.ana.pk, "fecha": HOY.isoformat(), "tipo": "VISITA", "estado": "CERRADO", "observacion": "Resuelto"},
        )
        s.refresh_from_db()
        self.assertEqual((s.estado, s.id_usuario), ("CERRADO", self.pastor))

    def test_alcance_de_consulta(self):
        self.crear(self.ana)
        self.crear(self.carla)
        for user, esperado in ((self.pastor, 2), (self.supervisor, 1), (self.lider, 1), (self.lider2, 1)):
            self.entrar(user)
            resp = self.client.get(reverse("pva:seguimientos"))
            self.assertEqual(len(resp.context["seguimientos"]), esperado, user.correo)

    def test_solo_el_pastor_registra(self):
        for user in (self.supervisor, self.lider):
            self.entrar(user)
            self.assertEqual(self.client.get(reverse("pva:seguimiento_crear")).status_code, 403)

    def test_apoyo_no_consulta_seguimiento(self):
        self.entrar(self.apoyo)
        self.assertEqual(self.client.get(reverse("pva:seguimientos")).status_code, 403)


class ReporteCasaTests(BaseCasasVida):
    """RF14, RN06, CU02."""

    def asistencia(self, casa, fecha, presentes):
        act = Actividad.objects.create(id_casa_vida=casa, titulo="Reunión", fecha=fecha, id_responsable=self.lider)
        for p in Participante_de(casa):
            Asistencia.objects.create(id_actividad=act, id_participante=p, presente=p in presentes)
        return act

    def enviar(self, user, semana=SEMANA, obs="Todo bien"):
        self.entrar(user)
        return self.client.post(reverse("pva:reporte_enviar_casa"), {"semana": semana.inicio.isoformat(), "observaciones": obs})

    def test_apoyo_envia_reporte_al_supervisor(self):
        self.asistencia(self.casa, SEMANA.inicio, [self.ana])
        resp = self.enviar(self.apoyo)
        r = Reporte.objects.get()
        self.assertRedirects(resp, reverse("pva:reporte_detalle", args=[r.pk]))
        self.assertEqual(
            (r.tipo_reporte, r.id_casa_vida, r.id_area, r.id_usuario_envia, r.id_usuario_destino, r.periodo),
            ("CASA_VIDA", self.casa, self.area, self.apoyo, self.supervisor, SEMANA.etiqueta),
        )

    def test_se_muestra_enviado_al_resto_del_equipo(self):
        self.asistencia(self.casa, SEMANA.inicio, [self.ana])
        self.enviar(self.apoyo)
        resp = self.enviar(self.lider)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context["ya_enviado"].id_usuario_envia, self.apoyo)
        self.assertIn("ya fue enviado por Apoyo", resp.context["form"].errors["semana"][0])
        self.assertEqual(Reporte.objects.count(), 1)
        resp = self.client.get(reverse("pva:reportes"))
        self.assertEqual(resp.context["reporte_semana"].id_usuario_envia, self.apoyo)

    def test_no_se_envia_semana_sin_asistencia(self):
        resp = self.enviar(self.lider)
        self.assertContains(resp, "No hay asistencia registrada en esta semana")
        self.assertFalse(Reporte.objects.exists())

    def test_semana_reportada_bloquea_nueva_asistencia(self):
        self.asistencia(self.casa, SEMANA.inicio, [self.ana])
        self.enviar(self.lider)
        resp = self.client.post(
            reverse("pva:asistencia_registrar"),
            {"titulo": "Otra reunión", "fecha": SEMANA.inicio.isoformat(), f"presente_{self.ana.pk}": "1"},
        )
        self.assertContains(resp, "ya fue enviado al Supervisor")
        self.assertEqual(Actividad.objects.count(), 1)

    def test_pastor_y_supervisor_no_envian_reporte_de_casa(self):
        for user in (self.pastor, self.supervisor):
            self.entrar(user)
            self.assertEqual(self.client.get(reverse("pva:reporte_enviar_casa")).status_code, 403)

    def test_consulta_de_reportes_por_alcance(self):
        self.asistencia(self.casa, SEMANA.inicio, [self.ana])
        self.asistencia(self.casa2, SEMANA.inicio, [self.carla])
        self.enviar(self.lider)
        self.enviar(self.lider2)
        otro = Reporte.objects.get(id_casa_vida=self.casa2)
        self.entrar(self.supervisor)
        resp = self.client.get(reverse("pva:reportes"))
        self.assertEqual([r.id_casa_vida for r in resp.context["reportes_casa"]], [self.casa])
        self.assertEqual(self.client.get(reverse("pva:reporte_detalle", args=[otro.pk])).status_code, 404)
        self.entrar(self.pastor)
        self.assertEqual(self.client.get(reverse("pva:reporte_detalle", args=[otro.pk])).status_code, 200)


def Participante_de(casa):
    return [m.id_participante for m in CasaVidaMiembro.objects.filter(id_casa_vida=casa).select_related("id_participante")]


class ReporteGeneralTests(ReporteCasaTests.__bases__[0]):
    """RF13, RN07, CU03."""

    def preparar_reportes_casa(self):
        mes = periodos.mes(SEMANA_PASADA.inicio)
        act = Actividad.objects.create(id_casa_vida=self.casa, titulo="Reunión", fecha=SEMANA_PASADA.inicio, id_responsable=self.lider)
        Asistencia.objects.create(id_actividad=act, id_participante=self.ana, presente=True)
        Asistencia.objects.create(id_actividad=act, id_participante=self.beto, presente=False)
        Reporte.objects.create(
            tipo_modulo="CASA_VIDA", tipo_reporte="CASA_VIDA", id_usuario_envia=self.lider, id_usuario_destino=self.supervisor,
            id_casa_vida=self.casa, id_area=self.area, periodo=SEMANA_PASADA.etiqueta,
            fecha_inicio=SEMANA_PASADA.inicio, fecha_fin=SEMANA_PASADA.fin,
        )
        return mes

    def test_supervisor_envia_reporte_general(self):
        mes = self.preparar_reportes_casa()
        self.entrar(self.supervisor)
        resp = self.client.post(reverse("pva:reporte_enviar_general"), {"mes": mes.inicio.isoformat(), "observaciones": "Buen mes"})
        general = Reporte.objects.get(tipo_reporte="GENERAL_AREA")
        self.assertRedirects(resp, reverse("pva:reporte_detalle", args=[general.pk]))
        self.assertEqual((general.id_area, general.periodo, general.id_usuario_envia), (self.area, mes.etiqueta, self.supervisor))
        self.assertEqual(Reporte.objects.get(tipo_reporte="CASA_VIDA").id_reporte_general, general)
        resp = self.client.get(reverse("pva:reporte_detalle", args=[general.pk]))
        self.assertEqual(resp.context["total"]["porcentaje"], 50)

    def test_no_se_envia_reporte_general_vacio(self):
        self.entrar(self.supervisor)
        resp = self.client.post(reverse("pva:reporte_enviar_general"), {"mes": periodos.mes(HOY).inicio.isoformat()})
        self.assertContains(resp, "no se puede enviar un reporte vacío")

    def test_un_reporte_general_por_mes(self):
        mes = self.preparar_reportes_casa()
        self.entrar(self.supervisor)
        self.client.post(reverse("pva:reporte_enviar_general"), {"mes": mes.inicio.isoformat()})
        resp = self.client.post(reverse("pva:reporte_enviar_general"), {"mes": mes.inicio.isoformat()})
        self.assertIn("ya fue enviado al Pastor", resp.context["form"].errors["mes"][0])
        self.assertEqual(Reporte.objects.filter(tipo_reporte="GENERAL_AREA").count(), 1)

    def test_pastor_recibe_y_no_envia(self):
        mes = self.preparar_reportes_casa()
        self.entrar(self.supervisor)
        self.client.post(reverse("pva:reporte_enviar_general"), {"mes": mes.inicio.isoformat()})
        self.entrar(self.pastor)
        self.assertEqual(self.client.get(reverse("pva:reporte_enviar_general")).status_code, 403)
        resp = self.client.get(reverse("pva:reportes"))
        self.assertEqual(len(resp.context["reportes_generales"]), 1)
        self.entrar(self.supervisor2)
        resp = self.client.get(reverse("pva:reportes"))
        self.assertEqual(len(resp.context["reportes_generales"]), 0)


class GenerarReporteTests(BaseCasasVida):
    """RF16, RN19, CU04."""

    def test_pastor_genera_reporte_mensual(self):
        act = Actividad.objects.create(id_casa_vida=self.casa, titulo="Reunión", fecha=HOY, id_responsable=self.lider)
        Asistencia.objects.create(id_actividad=act, id_participante=self.ana, presente=True)
        Asistencia.objects.create(id_actividad=act, id_participante=self.beto, presente=True)
        Seguimiento.objects.create(id_participante=self.ana, id_usuario=self.pastor, observacion="x", tipo_modulo="CASA_VIDA")
        self.entrar(self.pastor)
        resp = self.client.get(reverse("pva:reporte_generar"), {"tipo": "mensual", "fecha": HOY.isoformat()})
        filas = {f["casa"].pk: f for f in resp.context["filas"]}
        self.assertEqual(filas[self.casa.pk]["porcentaje"], 100)
        self.assertEqual(filas[self.casa.pk]["seguimientos"], 1)
        self.assertEqual(filas[self.casa.pk]["participantes"], 2)
        self.assertEqual(filas[self.casa2.pk]["actividades"], 0)
        self.assertEqual(resp.context["total"]["actividades"], 1)

    def test_filtro_por_area(self):
        self.entrar(self.pastor)
        resp = self.client.get(reverse("pva:reporte_generar"), {"tipo": "anual", "fecha": "2020-06-01", "area": self.area2.pk})
        self.assertEqual([f["casa"] for f in resp.context["filas"]], [self.casa2])
        self.assertFalse(resp.context["hay_datos"])
        self.assertContains(resp, "No hay información registrada")

    def test_solo_el_pastor_genera(self):
        for user in (self.supervisor, self.lider, self.apoyo):
            self.entrar(user)
            self.assertEqual(self.client.get(reverse("pva:reporte_generar")).status_code, 403)
