"""Pruebas de ofrendas: RF17, RN14 y criterios de aceptación de HU-08."""
import datetime
from decimal import Decimal

from django.urls import reverse

from nucleo.models import Auditoria
from nucleo.templatetags.formato import pesos
from ofrendas.models import Ofrenda
from pva.tests.test_casas_vida import CLAVE, BaseCasasVida

HOY = datetime.date.today()


class OfrendasTests(BaseCasasVida):
    def datos(self, **extra):
        d = {"fecha": HOY.isoformat(), "concepto": "Ofrenda  semanal", "valor": "150000", "id_casa_vida": self.casa.pk, "observacion": ""}
        d.update(extra)
        return d

    def ofrenda(self, fecha, valor, casa=None, concepto="Ofrenda"):
        return Ofrenda.objects.create(fecha=fecha, valor=Decimal(valor), id_casa_vida=casa, concepto=concepto, id_usuario_registro=self.pastor)

    def test_pastor_registra_ofrenda(self):
        self.entrar(self.pastor)
        resp = self.client.post(reverse("ofrendas:crear"), self.datos())
        self.assertRedirects(resp, reverse("ofrendas:index"))
        o = Ofrenda.objects.get()
        self.assertEqual((o.concepto, o.valor, o.id_casa_vida, o.id_usuario_registro), ("Ofrenda semanal", Decimal("150000"), self.casa, self.pastor))
        self.assertTrue(Auditoria.objects.filter(entidad="ofrenda", id_entidad=o.pk, accion="CREAR").exists())

    def test_ofrenda_general_sin_casa(self):
        self.entrar(self.pastor)
        self.client.post(reverse("ofrendas:crear"), self.datos(id_casa_vida=""))
        self.assertIsNone(Ofrenda.objects.get().id_casa_vida)

    def test_campos_obligatorios(self):
        self.entrar(self.pastor)
        resp = self.client.post(reverse("ofrendas:crear"), self.datos(fecha="", concepto="", valor=""))
        self.assertEqual(set(resp.context["form"].errors), {"fecha", "concepto", "valor"})
        self.assertFalse(Ofrenda.objects.exists())

    def test_valor_cero_o_negativo_rechazado(self):
        self.entrar(self.pastor)
        for valor in ("0", "-5000"):
            resp = self.client.post(reverse("ofrendas:crear"), self.datos(valor=valor))
            self.assertIn("mayor que cero", resp.context["form"].errors["valor"][0])
        self.assertFalse(Ofrenda.objects.exists())

    def test_fecha_futura_rechazada(self):
        self.entrar(self.pastor)
        resp = self.client.post(reverse("ofrendas:crear"), self.datos(fecha=(HOY + datetime.timedelta(days=1)).isoformat()))
        self.assertIn("fecha", resp.context["form"].errors)

    def test_consulta_por_rango_de_fechas_y_total(self):
        self.ofrenda(datetime.date(2026, 1, 10), "100000", self.casa)
        self.ofrenda(datetime.date(2026, 2, 10), "50000", self.casa2)
        self.ofrenda(datetime.date(2026, 3, 10), "25000")
        self.entrar(self.pastor)
        resp = self.client.get(reverse("ofrendas:index"), {"desde": "2026-02-01", "hasta": "2026-03-31"})
        self.assertEqual(len(resp.context["ofrendas"]), 2)
        self.assertEqual(resp.context["total"], Decimal("75000"))
        self.assertContains(resp, "$75.000")
        resp = self.client.get(reverse("ofrendas:index"), {"casa": self.casa.pk})
        self.assertEqual(resp.context["total"], Decimal("100000"))

    def test_rango_invertido(self):
        self.entrar(self.pastor)
        resp = self.client.get(reverse("ofrendas:index"), {"desde": "2026-03-01", "hasta": "2026-01-01"})
        self.assertContains(resp, "no puede ser posterior")

    def test_edicion_queda_trazada(self):
        o = self.ofrenda(HOY, "10000", self.casa)
        self.entrar(self.pastor)
        self.client.post(reverse("ofrendas:editar", args=[o.pk]), self.datos(valor="12000"))
        o.refresh_from_db()
        self.assertEqual((o.valor, o.modificado_por, o.id_usuario_registro), (Decimal("12000"), self.pastor, self.pastor))

    def test_otros_roles_sin_autorizacion_no_acceden(self):
        for user in (self.supervisor, self.lider, self.apoyo, self.coord):
            self.entrar(user)
            for ruta in (reverse("ofrendas:index"), reverse("ofrendas:crear")):
                self.assertEqual(self.client.get(ruta).status_code, 403, (user.correo, ruta))

    def test_responsable_autorizado_registra_y_consulta(self):
        self.supervisor.responsable_ofrendas = True
        self.supervisor.save(update_fields=["responsable_ofrendas"])
        self.entrar(self.supervisor)
        self.assertEqual(self.client.get(reverse("ofrendas:index")).status_code, 200)
        self.client.post(reverse("ofrendas:crear"), self.datos())
        self.assertEqual(Ofrenda.objects.get().id_usuario_registro, self.supervisor)
        resp = self.client.get(reverse("pva:casas"))
        self.assertIn("ofrendas", [m["id"] for m in resp.context["menu"]])

    def test_responsable_fuera_de_casas_de_vida(self):
        self.coord.responsable_ofrendas = True
        self.coord.save(update_fields=["responsable_ofrendas"])
        self.entrar(self.coord)
        resp = self.client.get(reverse("ofrendas:index"))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual([m["id"] for m in resp.context["menu"]], ["ofrendas", "panel"])

    def test_menu_oculta_ofrendas_sin_autorizacion(self):
        self.entrar(self.lider)
        resp = self.client.get(reverse("pva:casas"))
        self.assertNotIn("ofrendas", [m["id"] for m in resp.context["menu"]])
        self.assertIsNone(self.client.get(reverse("pva:panel")).context["sesion_js"]["ofrendas"])

    def test_pastor_autoriza_responsable_desde_usuarios(self):
        self.entrar(self.pastor)
        self.client.post(
            reverse("cuentas:usuarios_editar", args=[self.coord.pk]),
            {"nombre_completo": "Coord", "correo": self.coord.correo, "username": "", "rol": self.coord.rol_id, "responsable_ofrendas": "on"},
        )
        self.coord.refresh_from_db()
        self.assertTrue(self.coord.responsable_ofrendas)
        self.assertTrue(self.client.login(username=self.coord.correo, password=CLAVE))
        self.assertEqual(self.client.get(reverse("ofrendas:index")).status_code, 200)


class FormatoPesosTests(BaseCasasVida):
    def test_pesos(self):
        self.assertEqual(pesos(Decimal("1234567.50")), "$1.234.568")
        self.assertEqual(pesos(0), "$0")
        self.assertEqual(pesos(None), "$0")
