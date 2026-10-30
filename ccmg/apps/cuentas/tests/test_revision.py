"""Regresiones encontradas al recorrer la plataforma en el navegador con cada rol."""
import re

from django.conf import settings
from django.urls import reverse

from pva.tests.test_casas_vida import BaseCasasVida


class RevisionNavegadorTests(BaseCasasVida):
    def test_funciones_js_que_usan_los_paneles_estan_definidas(self):
        """panel-comun.js y los paneles llaman a funciones de auth.js; si faltan, el inicio queda en blanco."""
        js = settings.BASE_DIR / "static" / "js"
        auth = (js / "cuentas" / "auth.js").read_text(encoding="utf-8")
        definidas = set(re.findall(r"function (\w+)\s*\(", auth)) | set(re.findall(r"const (\w+)\s*=", auth))
        for nombre in ("requiereSesion", "sesionActual", "ROLES_INFO", "cerrarSesion"):
            self.assertIn(nombre, definidas)

    def test_pastor_tiene_enlace_a_gestion_de_usuarios(self):
        self.entrar(self.pastor)
        self.assertContains(self.client.get(reverse("cuentas:selector_modulo")), reverse("cuentas:usuarios_list"))
        for ruta in (reverse("pva:casas"), reverse("formacion:procesos")):
            menu = self.client.get(ruta).context["menu"]
            self.assertIn("usuarios", [m["id"] for m in menu], ruta)
        self.entrar(self.supervisor)
        self.assertNotIn("usuarios", [m["id"] for m in self.client.get(reverse("pva:casas")).context["menu"]])

    def test_contrasena_temporal_visible_tras_crear(self):
        self.entrar(self.pastor)
        resp = self.client.post(
            reverse("cuentas:usuarios_crear"),
            {"nombre_completo": "Nueva Persona", "correo": "nueva@ccmg.org", "username": "", "rol": self.rol["COORDINADOR_FORMACION"].pk},
            follow=True,
        )
        self.assertEqual(resp.request["PATH_INFO"], reverse("cuentas:usuarios_list"))
        self.assertTrue(resp.context["password_generada"])
        self.assertContains(resp, "Contraseña temporal de nueva@ccmg.org")
        # Se muestra una sola vez.
        self.assertIsNone(self.client.get(reverse("cuentas:usuarios_list")).context["password_generada"])

    def test_editar_usuario_precarga_su_asignacion(self):
        self.entrar(self.pastor)
        asig = self.client.get(reverse("cuentas:usuarios_editar", args=[self.lider.pk])).context["form_asig"]
        self.assertEqual(asig.initial["casa_vida"], self.casa.pk)
        asig = self.client.get(reverse("cuentas:usuarios_editar", args=[self.apoyo.pk])).context["form_asig"]
        self.assertEqual((asig.initial["casa_vida"], asig.initial["funcion_apoyo"]), (self.casa.pk, "ANFITRION"))
        asig = self.client.get(reverse("cuentas:usuarios_editar", args=[self.supervisor.pk])).context["form_asig"]
        self.assertEqual(asig.initial["area"], self.area.pk)

    def test_roles_con_nombre_legible(self):
        self.entrar(self.pastor)
        resp = self.client.get(reverse("cuentas:usuarios_list"))
        self.assertContains(resp, "Supervisor de Área")
        self.assertNotContains(resp, "SUPERVISOR_AREA")

    def test_pagina_403_propia(self):
        self.entrar(self.lider)
        resp = self.client.get(reverse("pva:areas"))
        self.assertEqual(resp.status_code, 403)
        self.assertContains(resp, "No tienes permiso para ver esta página", status_code=403)
        self.assertContains(resp, reverse("cuentas:panel_por_rol"), status_code=403)
