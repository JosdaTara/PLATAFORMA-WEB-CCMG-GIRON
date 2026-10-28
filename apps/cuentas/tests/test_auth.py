from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

from cuentas.models import Rol, Usuario


class AuthBackendTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.rol_pastor = Rol.objects.create(
            nombre="PASTOR",
            acceso_casas_vida=True,
            acceso_escuelas_formacion=True,
        )
        cls.rol_supervisor = Rol.objects.create(
            nombre="SUPERVISOR_AREA",
            acceso_casas_vida=True,
            acceso_escuelas_formacion=False,
        )

    def _crear_usuario(self, correo, rol, username=None, activo=True, password="password12345678901"):
        return Usuario.objects.create_user(
            correo=correo,
            username=username,
            nombre_completo="Test User",
            rol=rol,
            activo=activo,
            password=password,
        )

    def test_login_por_correo(self):
        user = self._crear_usuario("test@ccmg.org", self.rol_pastor)
        client = Client()
        resp = client.post(reverse("cuentas:login"), {
            "usuario": "TEST@CCMG.ORG",
            "clave": "password12345678901",
        })
        self.assertEqual(resp.status_code, 302)
        self.assertTrue("_auth_user_id" in client.session)

    def test_login_por_username(self):
        user = self._crear_usuario("u2@ccmg.org", self.rol_pastor, username="juan")
        client = Client()
        resp = client.post(reverse("cuentas:login"), {
            "usuario": "JUAN",
            "clave": "password12345678901",
        })
        self.assertEqual(resp.status_code, 302)

    def test_login_invalido_mensaje_generico(self):
        user = self._crear_usuario("u3@ccmg.org", self.rol_pastor)
        client = Client()
        resp = client.post(reverse("cuentas:login"), {
            "usuario": "noexiste@ccmg.org",
            "clave": "wrongpassword12345",
        })
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Usuario o contraseña incorrectos.")

    def test_cuenta_inactiva_no_login(self):
        user = self._crear_usuario("u4@ccmg.org", self.rol_pastor, activo=False)
        client = Client()
        resp = client.post(reverse("cuentas:login"), {
            "usuario": "u4@ccmg.org",
            "clave": "password12345678901",
        })
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Usuario o contraseña incorrectos.")

    def test_bloqueo_5_intentos(self):
        user = self._crear_usuario("u5@ccmg.org", self.rol_pastor)
        client = Client()
        for i in range(5):
            client.post(reverse("cuentas:login"), {
                "usuario": "u5@ccmg.org",
                "clave": "wrongpassword12345",
            })
        user.refresh_from_db()
        self.assertEqual(user.intentos_fallidos, 5)
        self.assertIsNotNone(user.bloqueado_hasta)
        # Intento 6 debe ser bloqueado
        resp = client.post(reverse("cuentas:login"), {
            "usuario": "u5@ccmg.org",
            "clave": "password12345678901",
        })
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Usuario o contraseña incorrectos.")

    def test_reset_intentos_al_login_ok(self):
        user = self._crear_usuario("u6@ccmg.org", self.rol_pastor)
        user.intentos_fallidos = 3
        user.save()
        client = Client()
        client.post(reverse("cuentas:login"), {
            "usuario": "u6@ccmg.org",
            "clave": "password12345678901",
        })
        user.refresh_from_db()
        self.assertEqual(user.intentos_fallidos, 0)
        self.assertIsNone(user.bloqueado_hasta)
