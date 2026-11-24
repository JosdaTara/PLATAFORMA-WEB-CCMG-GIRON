"""«Mi perfil»: guardar el nombre completo y enlazar al cambio de contraseña."""
from django.test import Client, TestCase
from django.urls import reverse

from cuentas.models import Rol, Usuario
from nucleo.models import Auditoria
from nucleo.utils import sesion_js

CLAVE = "password12345678901"


class PerfilTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        rol = Rol.objects.create(nombre="LIDER_CASA_VIDA", acceso_casas_vida=True)
        cls.user = Usuario.objects.create_user(
            correo="lider@ccmg.org", nombre_completo="María Líder", rol=rol, password=CLAVE, activo=True
        )
        cls.otro = Usuario.objects.create_user(
            correo="otro@ccmg.org", nombre_completo="Otra Persona", rol=rol, password=CLAVE, activo=True
        )

    def setUp(self):
        self.client = Client()
        self.client.force_login(self.user)
        self.url = reverse("cuentas:perfil")

    def test_guarda_el_nombre_en_la_base_de_datos(self):
        resp = self.client.post(self.url, {"nombre": "  María   José  Líder "})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {"nombre": "María José Líder"})
        self.user.refresh_from_db()
        self.assertEqual(self.user.nombre_completo, "María José Líder")

    def test_solo_cambia_la_cuenta_propia(self):
        self.client.post(self.url, {"nombre": "Nuevo Nombre", "id": self.otro.pk})
        self.otro.refresh_from_db()
        self.assertEqual(self.otro.nombre_completo, "Otra Persona")

    def test_deja_constancia_en_la_auditoria(self):
        self.client.post(self.url, {"nombre": "María José Líder"})
        self.assertTrue(Auditoria.objects.filter(accion="ACTUALIZAR_PERFIL").exists())

    def test_sin_cambios_no_audita(self):
        self.client.post(self.url, {"nombre": "María Líder"})
        self.assertFalse(Auditoria.objects.filter(accion="ACTUALIZAR_PERFIL").exists())

    def test_rechaza_nombre_vacio(self):
        resp = self.client.post(self.url, {"nombre": "   "})
        self.assertEqual(resp.status_code, 400)
        self.assertIn("error", resp.json())
        self.user.refresh_from_db()
        self.assertEqual(self.user.nombre_completo, "María Líder")

    def test_rechaza_nombre_demasiado_largo(self):
        resp = self.client.post(self.url, {"nombre": "a" * 151})
        self.assertEqual(resp.status_code, 400)

    def test_solo_acepta_post(self):
        self.assertEqual(self.client.get(self.url).status_code, 405)

    def test_requiere_sesion(self):
        resp = Client().post(self.url, {"nombre": "Intruso"})
        self.assertEqual(resp.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.nombre_completo, "María Líder")

    def test_exige_csrf(self):
        cliente = Client(enforce_csrf_checks=True)
        cliente.force_login(self.user)
        self.assertEqual(cliente.post(self.url, {"nombre": "Sin token"}).status_code, 403)

    def test_la_sesion_del_panel_trae_los_enlaces(self):
        datos = sesion_js(self.user)
        self.assertEqual(datos["urlPerfil"], self.url)
        self.assertEqual(datos["urlCambiarPassword"], reverse("cuentas:cambiar_password"))
