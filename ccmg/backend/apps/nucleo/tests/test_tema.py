"""Modo oscuro en toda la plataforma y recuperación de contraseña (RF25)."""
import os
import re

from django.conf import settings
from django.core import mail
from django.urls import reverse

from pva.tests.test_casas_vida import BaseCasasVida

PLANTILLAS = settings.FRONTEND_DIR / "templates"


def plantillas_con_head():
    for raiz, _, archivos in os.walk(PLANTILLAS):
        if os.path.basename(raiz) == "correos":
            continue  # los correos no son páginas: el cliente de correo no aplica el tema de la plataforma
        for nombre in archivos:
            if nombre.endswith(".html"):
                ruta = os.path.join(raiz, nombre)
                texto = open(ruta, encoding="utf-8").read()
                if "<head>" in texto:
                    yield ruta, texto


class ModoOscuroTests(BaseCasasVida):
    def test_toda_pagina_aplica_el_tema_antes_de_pintar(self):
        rutas = list(plantillas_con_head())
        self.assertGreater(len(rutas), 5)
        for ruta, texto in rutas:
            self.assertIn('{% include "_tema.html" %}', texto, ruta)

    def test_los_botones_de_tema_cargan_theme_js(self):
        for ruta, texto in plantillas_con_head():
            if "data-tema-toggle" in texto:
                self.assertIn("js/comun/theme.js", texto, ruta)

    def test_estilos_definen_el_modo_oscuro(self):
        css = (settings.FRONTEND_DIR / "static" / "css" / "styles.css").read_text(encoding="utf-8")
        self.assertIn('[data-theme="dark"]{', css)
        bloque = css[css.index('[data-theme="dark"]{'):]
        for token in ("--fondo:", "--superficie:", "--texto:", "--titulo:", "--bs-body-bg:"):
            self.assertIn(token, bloque)

    def test_paginas_con_boton_de_tema(self):
        self.assertContains(self.client.get(reverse("publico:index")), "data-tema-toggle")
        self.assertContains(self.client.get(reverse("cuentas:login")), "data-tema-toggle")
        self.entrar(self.lider)
        for ruta in (reverse("pva:panel"), reverse("pva:casas")):
            self.assertContains(self.client.get(ruta), "data-tema-toggle")


class RecuperarContrasenaTests(BaseCasasVida):
    def test_login_enlaza_la_recuperacion(self):
        self.assertContains(self.client.get(reverse("cuentas:login")), reverse("cuentas:password_reset"))

    def test_se_envia_el_correo_con_el_enlace(self):
        resp = self.client.post(reverse("cuentas:password_reset"), {"email": "LIDER@ccmg.org"})
        self.assertRedirects(resp, reverse("cuentas:password_reset_done"))
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["lider@ccmg.org"])
        enlace = re.search(r"https?://\S+/cuentas/recuperar/\S+/\S+/", mail.outbox[0].body).group(0)
        resp = self.client.get(enlace, follow=True)
        self.assertTrue(resp.context["validlink"])

    def test_usuario_inactivo_no_recibe_correo(self):
        self.lider.activo = False
        self.lider.save(update_fields=["activo"])
        self.client.post(reverse("cuentas:password_reset"), {"email": "lider@ccmg.org"})
        self.assertEqual(len(mail.outbox), 0)

    def test_paginas_de_cuenta_con_estilo(self):
        for ruta in (reverse("cuentas:password_reset"), reverse("cuentas:password_reset_done"), reverse("cuentas:password_reset_complete")):
            self.assertContains(self.client.get(ruta), "card-ccmg")
        self.entrar(self.lider)
        resp = self.client.get(reverse("cuentas:cambiar_password"))
        self.assertContains(resp, "card-ccmg")
        self.assertContains(resp, 'class="form-control')
