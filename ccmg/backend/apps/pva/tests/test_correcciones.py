"""Correcciones de las pruebas de usuarios: límites numéricos y de fechas, carácter nulo, búsqueda sin tildes,
reporte semanal en paralelo, autorización obligatoria, duplicados, aviso de privacidad y casas sin reporte."""
import datetime
from unittest import mock

from django.test import SimpleTestCase
from django.urls import reverse

from nucleo.busqueda import normalizar
from pva import periodos
from pva.forms import ParticipanteForm, ReporteAsistenciaForm
from pva.models import CasaVida, Participante, Reporte, Seguimiento

from .test_casas_vida import BaseCasasVida

HOY = datetime.date.today()
NUL = chr(0)


class LimitesNumericosYFechasTests(BaseCasasVida):
    def enviar(self, **extra):
        self.entrar(self.lider)
        return self.client.post(reverse("pva:asistencia_registrar"), self.datos_asistencia(**extra))

    def test_conteo_enorme_no_da_error_500(self):
        for valor in ("2147483648", "99999999999999999999", "100001"):
            resp = self.enviar(asistentes=valor)
            self.assertEqual(resp.status_code, 200, valor)
            self.assertIn("asistentes", resp.context["form"].errors)
            self.assertIn("no puede superar", resp.context["form"].errors["asistentes"][0])
        self.assertFalse(Reporte.objects.exists())

    def test_conteo_en_el_limite_se_acepta(self):
        self.assertEqual(self.enviar(asistentes="100000").status_code, 302)

    def test_ofrenda_enorme_rechazada(self):
        resp = self.enviar(ofrenda="1000000000")
        self.assertIn("ofrenda", resp.context["form"].errors)
        self.assertIn("no puede superar", resp.context["form"].errors["ofrenda"][0])

    def test_fecha_del_reporte_en_1800_rechazada_y_input_con_min(self):
        resp = self.enviar(fecha=datetime.date(1800, 1, 1))
        self.assertIn("anterior al 01/01/2020", resp.context["form"].errors["fecha"][0])
        form = self.client.get(reverse("pva:asistencia_registrar")).context["form"]
        self.assertEqual(form.fields["fecha"].widget.attrs["min"], "2020-01-01")

    def test_fecha_de_nacimiento_antes_de_1900_rechazada(self):
        form = ParticipanteForm(self.datos_participante(fecha_nacimiento="1850-01-01"))
        self.assertFalse(form.is_valid())
        self.assertIn("anterior al 01/01/1900", form.errors["fecha_nacimiento"][0])
        self.assertEqual(form.fields["fecha_nacimiento"].widget.attrs["min"], "1900-01-01")

    def test_seguimiento_con_fecha_absurda_rechazado(self):
        self.entrar(self.pastor)
        resp = self.client.post(
            reverse("pva:seguimiento_crear"),
            {"id_participante": self.ana.pk, "fecha": "1800-01-01", "tipo": "VISITA", "estado": "ABIERTO", "observacion": "x"},
        )
        self.assertContains(resp, "anterior al 01/01/2020")
        self.assertFalse(Seguimiento.objects.exists())


class CaracterNuloTests(BaseCasasVida):
    def test_busquedas_con_nulo_no_dan_500(self):
        self.entrar(self.pastor)
        for nombre in ("pva:participantes", "pva:seguimientos", "pva:participantes_autocompletar",
                       "formacion:participantes", "formacion:seguimientos", "formacion:participantes_autocompletar",
                       "ofrendas:index"):
            resp = self.client.get(reverse(nombre), {"q": f"an{NUL}a"})
            self.assertEqual(resp.status_code, 200, nombre)

    def test_el_nulo_se_quita_de_la_busqueda(self):
        self.entrar(self.pastor)
        resp = self.client.get(reverse("pva:participantes"), {"q": f"Ana{NUL}"})
        self.assertEqual([p.nombres_apellidos for p in resp.context["participantes"]], ["Ana Pérez"])

    def test_post_con_nulo_se_rechaza_con_400(self):
        self.entrar(self.lider)
        resp = self.client.post(reverse("cuentas:perfil"), {"nombre": f"Mar{NUL}ía"})
        self.assertEqual(resp.status_code, 400)
        self.assertIn("error", resp.json())
        self.lider.refresh_from_db()
        self.assertNotIn(NUL, self.lider.nombre_completo)

    def test_formulario_con_nulo_se_rechaza_con_400(self):
        self.entrar(self.lider)
        resp = self.client.post(
            reverse("pva:participante_crear"),
            {"nombres_apellidos": f"Zoe{NUL}", "telefono": "3001112233", "autorizacion_datos": "on"},
        )
        self.assertEqual(resp.status_code, 400)


class BusquedaSinTildesTests(BaseCasasVida):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.lucia = cls.participante("Lucía Gómez", "3001", cls.casa)
        cls.ana_maria = cls.participante("Ana María Pérez", "3002", cls.casa)

    def buscar(self, q, url="pva:participantes"):
        self.entrar(self.pastor)
        return [p.nombres_apellidos for p in self.client.get(reverse(url), {"q": q}).context["participantes"]]

    def test_ignora_tildes_y_mayusculas(self):
        self.assertEqual(self.buscar("lucia"), ["Lucía Gómez"])
        self.assertEqual(self.buscar("lúcía"), ["Lucía Gómez"])
        self.assertEqual(sorted(self.buscar("GOMEZ")), ["Beto Gómez", "Lucía Gómez"])

    def test_varias_palabras_deben_aparecer_todas(self):
        self.assertEqual(sorted(self.buscar("ana perez")), ["Ana María Pérez", "Ana Pérez"])
        self.assertEqual(self.buscar("ana gomez"), [])
        self.assertEqual(self.buscar("perez  maria"), ["Ana María Pérez"])

    def test_autocompletar_ignora_tildes(self):
        self.entrar(self.pastor)
        resp = self.client.get(reverse("pva:participantes_autocompletar"), {"q": "lucia"})
        self.assertEqual([r["nombre"] for r in resp.json()["resultados"]], ["Lucía Gómez"])

    def test_busqueda_en_formacion(self):
        from formacion.models import InscripcionFormacion, ProcesoFormacion

        proceso = ProcesoFormacion.objects.create(nombre="Pasos", tipo_proceso="PASOS_VIDA", id_coordinador=self.coord)
        InscripcionFormacion.objects.create(id_participante=self.lucia, id_proceso_formacion=proceso)
        self.entrar(self.pastor)
        resp = self.client.get(reverse("formacion:participantes"), {"q": "lucia gomez"})
        self.assertEqual([p.nombres_apellidos for p in resp.context["participantes"]], ["Lucía Gómez"])


class NormalizarTests(SimpleTestCase):
    def test_normalizar(self):
        self.assertEqual(normalizar("  ÁNA   María  Pérez "), "ana maria perez")
        self.assertEqual(normalizar("Muñoz"), "munoz")
        self.assertEqual(normalizar(f"a{NUL}b"), "ab")


class ReporteEnParaleloTests(BaseCasasVida):
    def test_integrity_error_se_muestra_como_ya_enviado(self):
        """Si otro integrante envía justo después de validar, el índice único choca: sin 500, sale «ya enviado»."""
        self.reporte_asistencia(self.casa, HOY, self.apoyo)
        self.entrar(self.lider)
        original = ReporteAsistenciaForm.reporte_de_la_semana
        llamadas = []

        def simulado(form, semana):
            # La validación (primera llamada) todavía no ve el reporte del otro integrante.
            llamadas.append(1)
            return None if len(llamadas) == 1 else original(form, semana)

        with mock.patch.object(ReporteAsistenciaForm, "reporte_de_la_semana", simulado):
            resp = self.client.post(reverse("pva:asistencia_registrar"), self.datos_asistencia())
        self.assertEqual(resp.status_code, 200)
        self.assertIn("ya fue enviado por Apoyo", resp.context["form"].errors["fecha"][0])
        self.assertEqual(Reporte.objects.count(), 1)


class AutorizacionObligatoriaTests(BaseCasasVida):
    def test_persona_nueva_exige_autorizacion(self):
        self.entrar(self.lider)
        resp = self.client.post(reverse("pva:participante_crear"), {"nombres_apellidos": "Fabio Ríos", "telefono": "3001112233"})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            resp.context["form"].errors["autorizacion_datos"],
            ["Sin la autorización de tratamiento de datos no se puede registrar al participante."],
        )
        self.assertFalse(Participante.objects.filter(nombres_apellidos="Fabio Ríos").exists())

    def test_formulario_enlaza_la_politica_de_privacidad(self):
        self.entrar(self.lider)
        self.assertContains(self.client.get(reverse("pva:participante_crear")), reverse("publico:privacidad"))


class DuplicadosTests(BaseCasasVida):
    def registrar(self, **extra):
        self.entrar(self.lider)
        datos = {"nombres_apellidos": "ANA  perez", "telefono": "300 123 4567", "autorizacion_datos": "on"}
        datos.update(extra)
        return self.client.post(reverse("pva:participante_crear"), datos)

    def test_mismo_nombre_normalizado_y_telefono_no_se_duplica(self):
        resp = self.registrar(nombres_apellidos="  ÁNA   Pérez ")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("Ya existe una persona registrada con ese nombre y teléfono.", resp.context["form"].non_field_errors())
        self.assertContains(resp, reverse("pva:participante_detalle", args=[self.ana.pk]))
        self.assertEqual(Participante.objects.filter(nombres_apellidos__icontains="ana").count(), 1)

    def test_guardar_dos_veces_seguidas_crea_una_sola(self):
        datos = {"nombres_apellidos": "Gina Rojas", "telefono": "3205550000"}
        self.assertEqual(self.registrar(**datos).status_code, 302)
        self.assertEqual(self.registrar(**datos).status_code, 200)
        self.assertEqual(Participante.objects.filter(nombres_apellidos="Gina Rojas").count(), 1)

    def test_otro_telefono_si_se_permite(self):
        self.assertEqual(self.registrar(nombres_apellidos="Ana Pérez", telefono="3119990000").status_code, 302)

    def test_persona_inactiva_no_cuenta(self):
        self.ana.estado = "INACTIVO"
        self.ana.save()
        self.assertEqual(self.registrar(nombres_apellidos="Ana Pérez").status_code, 302)

    def test_editar_no_se_confunde_con_duplicado(self):
        self.entrar(self.lider)
        resp = self.client.post(
            reverse("pva:participante_editar", args=[self.ana.pk]),
            {"nombres_apellidos": "Ana Pérez", "telefono": "3001234567", "autorizacion_datos": "on"},
        )
        self.assertEqual(resp.status_code, 302)

    def test_no_enlaza_a_una_persona_que_el_usuario_no_ve(self):
        self.entrar(self.lider2)
        resp = self.client.post(
            reverse("pva:participante_crear"),
            {"nombres_apellidos": "Ana Pérez", "telefono": "3001234567", "autorizacion_datos": "on"},
        )
        self.assertEqual(resp.status_code, 200)
        self.assertNotContains(resp, reverse("pva:participante_detalle", args=[self.ana.pk]))


class PoliticaPrivacidadTests(BaseCasasVida):
    def test_pagina_publica_con_secciones_y_datos_por_confirmar(self):
        resp = self.client.get(reverse("publico:privacidad"))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(reverse("publico:privacidad"), "/privacidad/")
        for texto in ("Ley 1581 de 2012", "Responsable del tratamiento", "representante legal", "[Por confirmar]", "Revocar"):
            self.assertContains(resp, texto)

    def test_enlaces_desde_inicio_y_login(self):
        for nombre in ("publico:index", "cuentas:login"):
            self.assertContains(self.client.get(reverse(nombre)), reverse("publico:privacidad"))


class CasasSinReporteTests(BaseCasasVida):
    def resumen(self, user):
        self.entrar(user)
        return self.client.get(reverse("pva:panel")).context["resumen_pva"]

    def test_pastor_ve_todas_las_casas_activas_sin_reporte(self):
        r = self.resumen(self.pastor)["sinReporte"]
        self.assertEqual([c["casa"] for c in r["casas"]], ["Casa Norte", "Casa Sur"])
        self.assertEqual(r["casas"][0]["lider"], "Lider")
        self.assertEqual(r["semana"], periodos.semana(HOY).nombre)

    def test_supervisor_solo_ve_su_area(self):
        r = self.resumen(self.supervisor)["sinReporte"]
        self.assertEqual([c["casa"] for c in r["casas"]], ["Casa Norte"])

    def test_la_casa_que_ya_envio_no_aparece_y_si_todas_enviaron_queda_vacio(self):
        self.reporte_asistencia(self.casa, HOY, self.lider)
        self.assertEqual([c["casa"] for c in self.resumen(self.pastor)["sinReporte"]["casas"]], ["Casa Sur"])
        self.reporte_asistencia(self.casa2, HOY, self.lider2)
        r = self.resumen(self.pastor)["sinReporte"]
        self.assertEqual((r["casas"], r["totalActivas"]), ([], 2))

    def test_el_reporte_de_otra_semana_no_cuenta_y_las_inactivas_no_aparecen(self):
        self.reporte_asistencia(self.casa, HOY - datetime.timedelta(weeks=1), self.lider)
        CasaVida.objects.filter(pk=self.casa2.pk).update(estado="INACTIVO")
        r = self.resumen(self.pastor)["sinReporte"]
        self.assertEqual([c["casa"] for c in r["casas"]], ["Casa Norte"])

    def test_lider_y_apoyo_no_reciben_el_bloque(self):
        for user in (self.lider, self.apoyo):
            self.assertNotIn("sinReporte", self.resumen(user))
