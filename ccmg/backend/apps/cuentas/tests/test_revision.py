"""Regresiones encontradas al recorrer la plataforma en el navegador con cada rol."""
import re

from django.conf import settings
from django.urls import reverse

from cuentas.models import Usuario
from pva.tests.test_casas_vida import BaseCasasVida


class RevisionNavegadorTests(BaseCasasVida):
    def test_funciones_js_que_usan_los_paneles_estan_definidas(self):
        """panel-comun.js y los paneles llaman a funciones de auth.js; si faltan, el inicio queda en blanco."""
        js = settings.FRONTEND_DIR / "static" / "js"
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

    def crear(self, clave1="ClaveInicial-Giron-2026", clave2=None, debe_cambiar=True, follow=False):
        datos = {"nombre_completo": "Nueva Persona", "correo": "nueva@ccmg.org", "username": "",
                 "rol": self.rol["COORDINADOR_FORMACION"].pk, "clave1": clave1, "clave2": clave1 if clave2 is None else clave2}
        if debe_cambiar:
            datos["debe_cambiar"] = "on"
        return self.client.post(reverse("cuentas:usuarios_crear"), datos, follow=follow)

    def test_quien_crea_la_cuenta_asigna_la_contrasena(self):
        for creador in (self.pastor, self.superadmin):
            Usuario.objects.filter(correo="nueva@ccmg.org").delete()
            self.entrar(creador)
            self.assertContains(self.client.get(reverse("cuentas:usuarios_crear")), "Generar una contraseña segura")
            resp = self.crear(follow=True)
            self.assertEqual(resp.request["PATH_INFO"], reverse("cuentas:usuarios_list"))
            nueva = Usuario.objects.get(correo="nueva@ccmg.org")
            self.assertTrue(nueva.check_password("ClaveInicial-Giron-2026"))
            self.assertTrue(nueva.debe_cambiar_password)
            self.assertNotContains(resp, "ClaveInicial-Giron-2026")  # la contraseña nunca se vuelve a mostrar
        self.client.logout()
        self.assertTrue(self.client.login(username="nueva@ccmg.org", password="ClaveInicial-Giron-2026"))

    def test_sin_pedir_cambio_al_primer_ingreso(self):
        self.entrar(self.pastor)
        self.crear(debe_cambiar=False)
        self.assertFalse(Usuario.objects.get(correo="nueva@ccmg.org").debe_cambiar_password)

    def test_contrasenas_distintas_o_debiles_se_rechazan(self):
        self.entrar(self.pastor)
        for clave1, clave2, campo in (
            ("ClaveInicial-Giron-2026", "OtraClaveDistinta-2026", "clave2"),
            ("corta", "corta", "clave1"),
            ("", "", "clave1"),
        ):
            resp = self.crear(clave1, clave2)
            self.assertEqual(resp.status_code, 200)
            self.assertIn(campo, resp.context["form"].errors)
            self.assertFalse(Usuario.objects.filter(correo="nueva@ccmg.org").exists())

    def test_editar_no_pide_contrasena(self):
        self.entrar(self.pastor)
        form = self.client.get(reverse("cuentas:usuarios_editar", args=[self.lider.pk])).context["form"]
        self.assertNotIn("clave1", form.fields)

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
