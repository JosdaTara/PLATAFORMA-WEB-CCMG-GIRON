from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

from cuentas.models import Rol, Usuario


class AuthViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.rol_pastor = Rol.objects.create(
            nombre="PASTOR", acceso_casas_vida=True, acceso_escuelas_formacion=True
        )
        cls.user = Usuario.objects.create_user(
            correo="pastor@ccmg.org",
            nombre_completo="Pastor Test",
            rol=cls.rol_pastor,
            password="password12345678901",
            activo=True,
        )
        cls.user_inactive = Usuario.objects.create_user(
            correo="inactive@ccmg.org",
            nombre_completo="Inactive User",
            rol=cls.rol_pastor,
            password="password12345678901",
            activo=False,
        )

    def test_login_correcto_redirige(self):
        client = Client()
        resp = client.post(reverse("cuentas:login"), {
            "usuario": "pastor@ccmg.org",
            "clave": "password12345678901",
        })
        self.assertEqual(resp.status_code, 302)

    def test_login_error_generico(self):
        client = Client()
        resp = client.post(reverse("cuentas:login"), {
            "usuario": "noexiste@ccmg.org",
            "clave": "wrongpassword12345",
        })
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Usuario o contraseña incorrectos.")

    def test_cuenta_inactiva_no_login(self):
        client = Client()
        resp = client.post(reverse("cuentas:login"), {
            "usuario": "inactive@ccmg.org",
            "clave": "password12345678901",
        })
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Usuario o contraseña incorrectos.")

    def test_cuenta_bloqueada_no_login(self):
        self.user.intentos_fallidos = 5
        self.user.bloqueado_hasta = timezone.now() + timedelta(minutes=15)
        self.user.save()
        client = Client()
        resp = client.post(reverse("cuentas:login"), {
            "usuario": "pastor@ccmg.org",
            "clave": "password12345678901",
        })
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Usuario o contraseña incorrectos.")
        # Reset
        self.user.intentos_fallidos = 0
        self.user.bloqueado_hasta = None
        self.user.save()

    def test_logout_post(self):
        client = Client()
        client.login(username="pastor@ccmg.org", password="password12345678901")
        resp = client.post(reverse("cuentas:logout"))
        self.assertEqual(resp.status_code, 302)
        self.assertNotIn("_auth_user_id", client.session)

    def test_ruta_privada_sin_sesion_redirige_login(self):
        client = Client()
        resp = client.get(reverse("cuentas:selector_modulo"))
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/cuentas/login/", resp.url)

    def test_password_reset_correo_existente(self):
        client = Client()
        resp = client.post(reverse("cuentas:password_reset"), {
            "email": "pastor@ccmg.org",
        })
        self.assertEqual(resp.status_code, 302)

    def test_password_reset_correo_inexistente_mismo_mensaje(self):
        client = Client()
        resp = client.post(reverse("cuentas:password_reset"), {
            "email": "noexiste@ccmg.org",
        })
        self.assertEqual(resp.status_code, 302)

    def test_password_reset_ignora_mayusculas(self):
        client = Client()
        resp = client.post(reverse("cuentas:password_reset"), {
            "email": "PASTOR@CCMG.ORG",
        })
        self.assertEqual(resp.status_code, 302)

    def test_enlaces_relativos_del_prototipo_no_dan_404(self):
        """El prototipo antiguo usaba enlaces relativos tipo "login.html".

        Aunque el navegador conserve una página en caché, esas rutas deben
        redirigir a la URL real en lugar de devolver 404.
        """
        client = Client()
        casos = [
            ("/cuentas/selector-modulo/login.html", reverse("cuentas:login")),
            ("/cuentas/login.html", reverse("cuentas:login")),
            ("/cuentas/selector-modulo/index.html", reverse("publico:index")),
            (
                "/cuentas/selector-modulo/selector-modulo.html",
                reverse("cuentas:selector_modulo"),
            ),
            ("/cuentas/selector-modulo/panel.html", reverse("cuentas:panel_por_rol")),
            (
                "/cuentas/selector-modulo/panel-casas-vida.html",
                reverse("pva:panel"),
            ),
            (
                "/cuentas/selector-modulo/panel-escuelas-formacion.html",
                reverse("formacion:panel"),
            ),
        ]
        for ruta, destino in casos:
            with self.subTest(ruta=ruta):
                resp = client.get(ruta)
                self.assertRedirects(
                    resp, destino, fetch_redirect_response=False
                )
