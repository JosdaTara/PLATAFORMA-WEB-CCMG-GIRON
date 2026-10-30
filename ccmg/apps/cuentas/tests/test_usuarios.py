from django.test import TestCase, Client
from django.urls import reverse
from django.core.exceptions import PermissionDenied

from cuentas.models import Rol, Usuario
from pva.models import Area, CasaVida, CasaVidaEquipo


class UsuarioGestionTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.rol_pastor = Rol.objects.create(
            nombre="PASTOR", acceso_casas_vida=True, acceso_escuelas_formacion=True
        )
        cls.rol_supervisor = Rol.objects.create(
            nombre="SUPERVISOR_AREA", acceso_casas_vida=True, acceso_escuelas_formacion=False
        )
        cls.rol_lider = Rol.objects.create(
            nombre="LIDER_CASA_VIDA", acceso_casas_vida=True, acceso_escuelas_formacion=False
        )
        cls.rol_apoyo = Rol.objects.create(
            nombre="APOYO_CASA_VIDA", acceso_casas_vida=True, acceso_escuelas_formacion=False
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
        cls.area1 = Area.objects.create(nombre="Area 1", id_supervisor=None)
        cls.area2 = Area.objects.create(nombre="Area 2", id_supervisor=None)
        cls.casa1 = CasaVida.objects.create(nombre="Casa 1", id_area=cls.area1, id_lider=None)
        cls.casa2 = CasaVida.objects.create(nombre="Casa 2", id_area=cls.area2, id_lider=None)

    def test_list_requires_pastor(self):
        c = Client()
        c.login(username="lider@ccmg.org", password="password12345678901")
        resp = c.get(reverse("cuentas:usuarios_list"))
        self.assertIn(resp.status_code, [403, 302])

    def test_create_requires_pastor(self):
        c = Client()
        c.login(username="lider@ccmg.org", password="password12345678901")
        resp = c.get(reverse("cuentas:usuarios_crear"))
        self.assertIn(resp.status_code, [403, 302])

    def test_cannot_deactivate_self(self):
        c = Client()
        c.login(username="pastor@ccmg.org", password="password12345678901")
        resp = c.post(reverse("cuentas:usuarios_desactivar", args=[self.pastor.pk]))
        self.pastor.refresh_from_db()
        self.assertTrue(self.pastor.activo)
        self.assertIn(resp.status_code, [302])

    def test_cannot_deactivate_last_pastor(self):
        c = Client()
        c.login(username="pastor@ccmg.org", password="password12345678901")
        otro = Usuario.objects.create_user(
            correo="pastor2@ccmg.org", nombre_completo="P2", rol=self.rol_pastor, password="password12345678901", activo=True
        )
        c.post(reverse("cuentas:usuarios_desactivar", args=[otro.pk]))
        otro.refresh_from_db()
        self.assertFalse(otro.activo)
        # ahora solo queda pastor, no puede desactivarlo
        resp = c.post(reverse("cuentas:usuarios_desactivar", args=[self.pastor.pk]))
        self.pastor.refresh_from_db()
        self.assertTrue(self.pastor.activo)

    def test_soft_delete(self):
        c = Client()
        c.login(username="pastor@ccmg.org", password="password12345678901")
        u = Usuario.objects.create_user(
            correo="x@ccmg.org", nombre_completo="X", rol=self.rol_lider, password="password12345678901", activo=True
        )
        self.casa1.id_lider = u
        self.casa1.save()
        c.post(reverse("cuentas:usuarios_desactivar", args=[u.pk]))
        u.refresh_from_db()
        self.casa1.refresh_from_db()
        self.assertFalse(u.activo)
        self.assertIsNone(self.casa1.id_lider_id)

    def test_reactivate_respects_apoyo_unique(self):
        c = Client()
        c.login(username="pastor@ccmg.org", password="password12345678901")
        u = Usuario.objects.create_user(
            correo="apoyo@ccmg.org", nombre_completo="A", rol=self.rol_apoyo, password="password12345678901", activo=True
        )
        CasaVidaEquipo.objects.create(id_casa_vida=self.casa1, id_usuario=u, funcion="APRENDIZ", activo=True)
        c.post(reverse("cuentas:usuarios_desactivar", args=[u.pk]))
        u.refresh_from_db()
        self.assertFalse(u.activo)
        c.post(reverse("cuentas:usuarios_reactivar", args=[u.pk]))
        u.refresh_from_db()
        self.assertTrue(u.activo)

    def test_supervisor_one_area_block(self):
        c = Client()
        c.login(username="pastor@ccmg.org", password="password12345678901")
        sup = Usuario.objects.create_user(
            correo="sup@ccmg.org", nombre_completo="Sup", rol=self.rol_supervisor, password="password12345678901", activo=True
        )
        self.area1.id_supervisor = sup
        self.area1.save()
        # intentar asignar segunda área
        resp = c.post(reverse("cuentas:usuarios_editar", args=[sup.pk]), {
            "nombre_completo": sup.nombre_completo,
            "correo": sup.correo,
            "username": sup.username or "",
            "rol": self.rol_supervisor.pk,
            "area": self.area2.pk,
            "casa_vida": "",
            "funcion_apoyo": "",
        })
        self.area2.refresh_from_db()
        self.assertNotEqual(self.area2.id_supervisor_id, sup.pk)

    def test_supervisor_without_area_allowed(self):
        c = Client()
        c.login(username="pastor@ccmg.org", password="password12345678901")
        sup = Usuario.objects.create_user(
            correo="sup2@ccmg.org", nombre_completo="Sup2", rol=self.rol_supervisor, password="password12345678901", activo=True
        )
        resp = c.get(reverse("cuentas:usuarios_editar", args=[sup.pk]))
        self.assertEqual(resp.status_code, 200)
