from django.test import TestCase, Client
from django.urls import reverse
import os

from cuentas.models import Rol, Usuario


class BloqueATests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.rol_pastor = Rol.objects.create(
            nombre="PASTOR", acceso_casas_vida=True, acceso_escuelas_formacion=True
        )
        cls.rol_lider = Rol.objects.create(
            nombre="LIDER_CASA_VIDA", acceso_casas_vida=True, acceso_escuelas_formacion=False
        )
        cls.pastor = Usuario.objects.create_user(
            correo="pastor@ccmg.org",
            nombre_completo="Pastor Test",
            rol=cls.rol_pastor,
            password="password12345678901",
            activo=True,
        )
        cls.lider = Usuario.objects.create_user(
            correo="lider@ccmg.org",
            nombre_completo="Lider Test",
            rol=cls.rol_lider,
            password="password12345678901",
            activo=True,
        )

    def test_ofrendas_requires_pastor(self):
        c = Client()
        c.login(username="lider@ccmg.org", password="password12345678901")
        resp = c.get(reverse("ofrendas:index"))
        self.assertIn(resp.status_code, [403, 302])

    def test_ofrendas_pastor_ok(self):
        c = Client()
        c.login(username="pastor@ccmg.org", password="password12345678901")
        resp = c.get(reverse("ofrendas:index"))
        self.assertEqual(resp.status_code, 200)

    def test_no_sessionstorage_in_templates(self):
        base = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "templates")
        if os.path.exists(base):
            for root, dirs, files in os.walk(base):
                for fn in files:
                    if fn.endswith('.html'):
                        p = os.path.join(root, fn)
                        s = open(p, encoding='utf-8').read()
                        self.assertNotIn('sessionStorage', s, f'sessionStorage found in {p}')
        jsbase = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "static", "js")
        if os.path.exists(jsbase):
            for fn in os.listdir(jsbase):
                if fn.endswith('.js'):
                    p = os.path.join(jsbase, fn)
                    s = open(p, encoding='utf-8').read()
                    self.assertNotIn('sessionStorage', s, f'sessionStorage found in {p}')
        self.assertTrue(True)
