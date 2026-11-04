"""Recuperación de contraseña (RF25): correo con la identidad de la iglesia, página de cambio y aviso."""
import re
from unittest import mock

from django.core import mail
from django.urls import reverse

from nucleo.models import Auditoria
from pva.tests.test_casas_vida import CLAVE, BaseCasasVida

NUEVA = "NuevaClaveSegura-Giron-2026"


class CorreoDeRecuperacionTests(BaseCasasVida):
    def solicitar(self, correo=None):
        return self.client.post(reverse("cuentas:password_reset"), {"email": correo or self.lider.correo})

    def enlace(self, mensaje):
        return re.search(r"https?://\S+/cuentas/recuperar/[^/\s]+/[^/\s]+/", mensaje.body).group(0)

    def test_correo_con_nombre_correo_y_enlace(self):
        self.assertRedirects(self.solicitar(), reverse("cuentas:password_reset_done"))
        self.assertEqual(len(mail.outbox), 1)
        m = mail.outbox[0]
        self.assertEqual(m.to, [self.lider.correo])
        self.assertIn("Restablece tu contraseña", m.subject)
        self.assertIn("CCMG Girón", m.from_email)
        for texto in (self.lider.nombre_completo, self.lider.correo, self.enlace(m), "60 minutos"):
            self.assertIn(texto, m.body)

    def test_version_html_con_colores_y_logo_incrustado(self):
        self.solicitar()
        m = mail.outbox[0]
        html = dict((tipo, cuerpo) for cuerpo, tipo in m.alternatives)["text/html"]
        for texto in (self.lider.nombre_completo, self.lider.correo, "#00674F", "#CBB279", "cid:logo-ccmg", "Crear nueva contraseña"):
            self.assertIn(texto, html)
        logo = [a for a in m.attachments if not isinstance(a, tuple)]
        self.assertEqual(len(logo), 1)
        self.assertEqual(logo[0]["Content-ID"], "<logo-ccmg>")

    def test_correo_inexistente_no_envia_pero_responde_igual(self):
        self.assertRedirects(self.solicitar("nadie@ccmg.org"), reverse("cuentas:password_reset_done"))
        self.assertEqual(len(mail.outbox), 0)

    def test_falla_del_servidor_de_correo_no_rompe_la_pagina(self):
        with mock.patch("django.core.mail.EmailMultiAlternatives.send", side_effect=OSError("SMTP caído")):
            with self.assertLogs("cuentas.correos", level="ERROR"):
                resp = self.solicitar()
        self.assertRedirects(resp, reverse("cuentas:password_reset_done"))

    def test_pagina_de_cambio_muestra_la_cuenta_y_cambia_la_contrasena(self):
        self.solicitar()
        resp = self.client.get(self.enlace(mail.outbox[0]), follow=True)
        self.assertTrue(resp.context["validlink"])
        self.assertContains(resp, self.lider.nombre_completo)
        self.assertContains(resp, self.lider.correo)

        resp = self.client.post(resp.request["PATH_INFO"], {"new_password1": NUEVA, "new_password2": NUEVA})
        self.assertRedirects(resp, reverse("cuentas:password_reset_complete"))
        self.lider.refresh_from_db()
        self.assertTrue(self.lider.check_password(NUEVA))
        self.assertTrue(
            Auditoria.objects.filter(accion="RESTABLECER_CONTRASENA", id_usuario=self.lider, id_entidad=self.lider.pk).exists()
        )

        aviso = mail.outbox[1]
        self.assertEqual(aviso.to, [self.lider.correo])
        self.assertIn("Tu contraseña fue cambiada", aviso.subject)
        self.assertIn(self.lider.nombre_completo, aviso.body)
        self.assertContains(self.client.get(reverse("cuentas:password_reset_complete")), "Contraseña actualizada")

    def test_el_enlace_sirve_una_sola_vez(self):
        self.solicitar()
        url = self.client.get(self.enlace(mail.outbox[0]), follow=True).request["PATH_INFO"]
        self.client.post(url, {"new_password1": NUEVA, "new_password2": NUEVA})
        resp = self.client.get(self.enlace(mail.outbox[0]), follow=True)
        self.assertFalse(resp.context["validlink"])
        self.assertContains(resp, "Solicitar un enlace nuevo")

    def test_contrasena_corta_se_rechaza(self):
        self.solicitar()
        url = self.client.get(self.enlace(mail.outbox[0]), follow=True).request["PATH_INFO"]
        resp = self.client.post(url, {"new_password1": "corta", "new_password2": "corta"})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.context["form"].errors)
        self.lider.refresh_from_db()
        self.assertTrue(self.lider.check_password(CLAVE))


class AvisoAlCambiarContrasenaTests(BaseCasasVida):
    def test_cambio_desde_la_sesion_avisa_por_correo(self):
        self.entrar(self.lider)
        resp = self.client.post(
            reverse("cuentas:cambiar_password"),
            {"old_password": CLAVE, "new_password1": NUEVA, "new_password2": NUEVA},
        )
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [self.lider.correo])
        self.assertIn("Tu contraseña fue cambiada", mail.outbox[0].subject)
        self.assertTrue(Auditoria.objects.filter(accion="CAMBIAR_CONTRASENA", id_usuario=self.lider).exists())
