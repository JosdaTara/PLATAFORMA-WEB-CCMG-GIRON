from django.test import TestCase, Client
from django.urls import reverse

from cuentas.models import Rol, Usuario


class TemplateRenderTests(TestCase):
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

    def test_index_renders(self):
        client = Client()
        resp = client.get(reverse("publico:index"))
        self.assertEqual(resp.status_code, 200)

    def test_login_renders(self):
        client = Client()
        resp = client.get(reverse("cuentas:login"))
        self.assertEqual(resp.status_code, 200)

    def test_password_reset_renders(self):
        client = Client()
        resp = client.get(reverse("cuentas:password_reset"))
        self.assertEqual(resp.status_code, 200)

    def test_selector_modulo_requires_login(self):
        client = Client()
        resp = client.get(reverse("cuentas:selector_modulo"))
        self.assertEqual(resp.status_code, 302)

    def test_panel_requires_login(self):
        client = Client()
        resp = client.get(reverse("cuentas:panel_por_rol"))
        self.assertEqual(resp.status_code, 302)

    def test_panel_casas_requires_login(self):
        client = Client()
        resp = client.get(reverse("pva:panel"))
        self.assertEqual(resp.status_code, 302)

    def test_panel_escuelas_requires_login(self):
        client = Client()
        resp = client.get(reverse("formacion:panel"))
        self.assertEqual(resp.status_code, 302)

    def test_login_authenticated_renders(self):
        client = Client()
        client.login(username="pastor@ccmg.org", password="password12345678901")
        resp = client.get(reverse("cuentas:login"))
        self.assertEqual(resp.status_code, 302)  # redirige si ya autenticado

    def test_pastor_puede_entrar_a_los_dos_modulos(self):
        """El panel recibe la sesión desde Django (no depende de sessionStorage)."""
        client = Client()
        client.login(username="pastor@ccmg.org", password="password12345678901")
        rutas = [
            reverse("cuentas:selector_modulo"),
            reverse("pva:panel"),
            reverse("formacion:panel"),
        ]
        for ruta in rutas:
            with self.subTest(ruta=ruta):
                resp = client.get(ruta)
                self.assertEqual(resp.status_code, 200)
                self.assertContains(resp, 'id="ccmg-sesion"')
                self.assertContains(resp, '"rol": "pastor"')

    def test_lider_no_puede_entrar_a_selector_ni_a_escuelas(self):
        rol = Rol.objects.create(
            nombre="LIDER_CASA_VIDA",
            acceso_casas_vida=True,
            acceso_escuelas_formacion=False,
        )
        Usuario.objects.create_user(
            correo="lider@ccmg.org",
            nombre_completo="Líder Test",
            rol=rol,
            password="password12345678901",
            activo=True,
        )
        client = Client()
        client.login(username="lider@ccmg.org", password="password12345678901")

        self.assertEqual(
            client.get(reverse("cuentas:selector_modulo")).status_code, 403
        )
        self.assertEqual(
            client.get(reverse("formacion:panel")).status_code, 403
        )

        resp = client.get(reverse("pva:panel"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, '"rol": "lider"')
