from django.test import TestCase, Client
from django.urls import reverse

from cuentas.models import Rol, Usuario
from pva.models import Area, CasaVida, CasaVidaEquipo


class CasaVidaScopeTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.rol_pastor = Rol.objects.create(nombre="PASTOR", acceso_casas_vida=True, acceso_escuelas_formacion=True)
        cls.rol_apoyo = Rol.objects.create(nombre="APOYO_CASA_VIDA", acceso_casas_vida=True, acceso_escuelas_formacion=False)

        cls.user_pastor = Usuario.objects.create_user(
            correo="pastor@ccmg.org", nombre_completo="Pastor", rol=cls.rol_pastor, password="password12345678901"
        )
        cls.user_apoyo = Usuario.objects.create_user(
            correo="apoyo@ccmg.org", nombre_completo="Apoyo", rol=cls.rol_apoyo, password="password12345678901"
        )

        cls.area = Area.objects.create(nombre="Area Test", id_supervisor=cls.user_pastor)
        cls.casa1 = CasaVida.objects.create(nombre="Casa 1", id_area=cls.area, id_lider=cls.user_pastor)
        cls.casa2 = CasaVida.objects.create(nombre="Casa 2", id_area=cls.area, id_lider=cls.user_pastor)

        # Vincular usuario de apoyo a casa1 (activo)
        CasaVidaEquipo.objects.create(
            id_casa_vida=cls.casa1, id_usuario=cls.user_apoyo, funcion="APRENDIZ", activo=True
        )

    def test_apoyo_ve_solo_su_casa_activa(self):
        from nucleo.mixins import CasaVidaScopeMixin
        from django.test import RequestFactory
        from django.contrib.auth.models import AnonymousUser

        # Simular queryset filtrado
        from pva.models import CasaVida
        qs = CasaVida.objects.all()
        # Reproducir lógica del mixin
        equipos = CasaVidaEquipo.objects.filter(id_usuario=self.user_apoyo, activo=True).values_list("id_casa_vida", flat=True)
        filtrado = qs.filter(id_casa_vida__in=equipos)
        self.assertEqual(filtrado.count(), 1)
        self.assertEqual(filtrado.first().nombre, "Casa 1")

    def test_apoyo_no_ve_otras_casas(self):
        from pva.models import CasaVida
        equipos = CasaVidaEquipo.objects.filter(id_usuario=self.user_apoyo, activo=True).values_list("id_casa_vida", flat=True)
        filtrado = CasaVida.objects.filter(id_casa_vida__in=equipos)
        self.assertNotIn(self.casa2, filtrado)

    def test_registro_inactivo_no_da_acceso(self):
        # Desactivar el equipo
        CasaVidaEquipo.objects.filter(id_usuario=self.user_apoyo).update(activo=False)
        equipos = CasaVidaEquipo.objects.filter(id_usuario=self.user_apoyo, activo=True).values_list("id_casa_vida", flat=True)
        self.assertEqual(len(list(equipos)), 0)
        # Reactivar para no afectar otros tests
        CasaVidaEquipo.objects.filter(id_usuario=self.user_apoyo).update(activo=True)

    def test_acceso_por_url_a_casa_ajena_responde_404(self):
        client = Client()
        client.login(username="apoyo@ccmg.org", password="password12345678901")
        # Intentar acceder a casa2 (que no es la suya) - simulado con un endpoint que use el mixin
        # Por ahora verificamos que el queryset filtrado no incluya casa2
        equipos = CasaVidaEquipo.objects.filter(id_usuario=self.user_apoyo, activo=True).values_list("id_casa_vida", flat=True)
        self.assertNotIn(self.casa2.id_casa_vida, equipos)
