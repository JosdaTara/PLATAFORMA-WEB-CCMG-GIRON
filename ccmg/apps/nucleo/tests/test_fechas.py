"""Las fechas no se desplazan al volver a guardar un registro (columnas timestamptz con USE_TZ)."""
import datetime

from django.test import TestCase
from django.utils import timezone

from cuentas.models import Rol, Usuario
from pva.models import Area, Participante


class FechasSinDesplazamientoTests(TestCase):
    def assertNoSeDesplaza(self, obj, campo):
        obj.refresh_from_db()
        original = getattr(obj, campo)
        self.assertIsNotNone(original)
        self.assertTrue(timezone.is_aware(original))
        obj.save()
        obj.refresh_from_db()
        self.assertEqual(getattr(obj, campo), original)

    def test_participante(self):
        p = Participante.objects.create(
            nombres_apellidos="Ana", documento_identidad="1", fecha_nacimiento=datetime.date(1990, 1, 1)
        )
        self.assertNoSeDesplaza(p, "creado_en")

    def test_area(self):
        self.assertNoSeDesplaza(Area.objects.create(nombre="Norte"), "creado_en")

    def test_usuario(self):
        rol = Rol.objects.create(nombre="PASTOR", acceso_casas_vida=True, acceso_escuelas_formacion=True)
        u = Usuario.objects.create_user(
            correo="p@ccmg.org", nombre_completo="P", rol=rol, password="password12345678901",
            creado_en=timezone.now(), bloqueado_hasta=timezone.now() + datetime.timedelta(minutes=15),
        )
        self.assertNoSeDesplaza(u, "creado_en")
        self.assertNoSeDesplaza(u, "bloqueado_hasta")
