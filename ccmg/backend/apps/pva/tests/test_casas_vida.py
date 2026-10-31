"""Pruebas del módulo Casas de Vida: RF05–RF10, RF28 y reglas RN03–RN09, RN20, RN23, RN24."""
import datetime

from django.test import TestCase
from django.urls import reverse

from cuentas.models import Rol, Usuario
from nucleo.models import Auditoria
from pva.models import (
    ACTIVO,
    INACTIVO,
    Actividad,
    Area,
    Asistencia,
    CasaVida,
    CasaVidaEquipo,
    CasaVidaMiembro,
    Participante,
)

CLAVE = "password12345678901"


class BaseCasasVida(TestCase):
    @classmethod
    def setUpTestData(cls):
        roles = {
            "SUPERADMIN": (True, True),
            "PASTOR": (True, True),
            "SUPERVISOR_AREA": (True, False),
            "LIDER_CASA_VIDA": (True, False),
            "APOYO_CASA_VIDA": (True, False),
            "COORDINADOR_FORMACION": (False, True),
        }
        cls.rol = {
            n: Rol.objects.create(nombre=n, acceso_casas_vida=c, acceso_escuelas_formacion=e)
            for n, (c, e) in roles.items()
        }

        def usuario(correo, rol):
            return Usuario.objects.create_user(
                correo=correo, nombre_completo=correo.split("@")[0].title(), rol=cls.rol[rol], password=CLAVE
            )

        cls.superadmin = usuario("superadmin@ccmg.org", "SUPERADMIN")
        cls.pastor = usuario("pastor@ccmg.org", "PASTOR")
        cls.supervisor = usuario("supervisor@ccmg.org", "SUPERVISOR_AREA")
        cls.supervisor2 = usuario("supervisor2@ccmg.org", "SUPERVISOR_AREA")
        cls.lider = usuario("lider@ccmg.org", "LIDER_CASA_VIDA")
        cls.lider2 = usuario("lider2@ccmg.org", "LIDER_CASA_VIDA")
        cls.apoyo = usuario("apoyo@ccmg.org", "APOYO_CASA_VIDA")
        cls.coord = usuario("coord@ccmg.org", "COORDINADOR_FORMACION")

        cls.area = Area.objects.create(nombre="Norte", id_supervisor=cls.supervisor)
        cls.area2 = Area.objects.create(nombre="Sur", id_supervisor=cls.supervisor2)
        cls.casa = CasaVida.objects.create(
            nombre="Casa Norte", id_area=cls.area, id_lider=cls.lider, id_supervisor=cls.supervisor
        )
        cls.casa2 = CasaVida.objects.create(
            nombre="Casa Sur", id_area=cls.area2, id_lider=cls.lider2, id_supervisor=cls.supervisor2
        )
        CasaVidaEquipo.objects.create(id_casa_vida=cls.casa, id_usuario=cls.apoyo, funcion="ANFITRION")

        cls.ana = cls.participante("Ana Pérez", "1001", cls.casa)
        cls.beto = cls.participante("Beto Gómez", "1002", cls.casa)
        cls.carla = cls.participante("Carla Ruiz", "2001", cls.casa2)

    @staticmethod
    def participante(nombre, documento, casa):
        p = Participante.objects.create(
            nombres_apellidos=nombre,
            documento_identidad=documento,
            fecha_nacimiento=datetime.date(1990, 1, 1),
            telefono="3001234567",
            direccion="Calle 1",
            autorizacion_datos=True,
        )
        CasaVidaMiembro.objects.create(id_casa_vida=casa, id_participante=p)
        return p

    def entrar(self, user):
        self.assertTrue(self.client.login(username=user.correo, password=CLAVE))

    def datos_participante(self, **extra):
        datos = {
            "nombres_apellidos": "Diana  López",
            "documento_identidad": "3001",
            "fecha_nacimiento": "2000-05-10",
            "telefono": "3109876543",
            "direccion": "Carrera 5",
            "autorizacion_datos": "on",
            "casa_vida": self.casa.pk,
        }
        datos.update(extra)
        return datos


class GestionPastorTests(BaseCasasVida):
    """RF05, RF07, RN20: el Pastor registra y actualiza; queda auditoría (RNF18)."""

    def setUp(self):
        self.entrar(self.pastor)

    def test_pastor_crea_area(self):
        resp = self.client.post(reverse("pva:area_crear"), {"nombre": "Centro"})
        self.assertRedirects(resp, reverse("pva:areas"))
        self.assertTrue(Area.objects.filter(nombre="Centro", estado=ACTIVO).exists())

    def test_supervisor_no_puede_tener_dos_areas(self):
        resp = self.client.post(reverse("pva:area_crear"), {"nombre": "Centro", "id_supervisor": self.supervisor.pk})
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "ya está asignado al Área")
        self.assertFalse(Area.objects.filter(nombre="Centro").exists())

    def test_casa_hereda_supervisor_del_area(self):
        resp = self.client.post(
            reverse("pva:casa_crear"),
            {"nombre": "Casa Nueva", "id_area": self.area.pk, "direccion": "Calle 9"},
        )
        casa = CasaVida.objects.get(nombre="Casa Nueva")
        self.assertRedirects(resp, reverse("pva:casa_detalle", args=[casa.pk]))
        self.assertEqual(casa.id_supervisor, self.supervisor)
        self.assertTrue(Auditoria.objects.filter(entidad="casa_vida", id_entidad=casa.pk, accion="CREAR").exists())

    def test_cambiar_supervisor_del_area_actualiza_sus_casas(self):
        nuevo = Usuario.objects.create_user(
            correo="sup3@ccmg.org", nombre_completo="Sup 3", rol=self.rol["SUPERVISOR_AREA"], password=CLAVE
        )
        self.client.post(reverse("pva:area_editar", args=[self.area.pk]), {"nombre": "Norte", "id_supervisor": nuevo.pk})
        self.casa.refresh_from_db()
        self.assertEqual(self.casa.id_supervisor, nuevo)

    def test_lider_no_puede_liderar_dos_casas_activas(self):
        resp = self.client.post(
            reverse("pva:casa_crear"), {"nombre": "Otra", "id_area": self.area.pk, "id_lider": self.lider.pk}
        )
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "ya está asignado a la Casa de Vida")

    def test_pastor_registra_participante_con_casa(self):
        resp = self.client.post(reverse("pva:participante_crear"), self.datos_participante())
        p = Participante.objects.get(documento_identidad="3001")
        self.assertRedirects(resp, reverse("pva:participante_detalle", args=[p.pk]))
        self.assertEqual(p.nombres_apellidos, "Diana López")
        self.assertEqual(p.membresia_activa.id_casa_vida, self.casa)
        self.assertTrue(Auditoria.objects.filter(entidad="participante", id_entidad=p.pk).exists())

    def test_sin_autorizacion_de_datos_no_se_guarda(self):
        datos = self.datos_participante()
        del datos["autorizacion_datos"]
        resp = self.client.post(reverse("pva:participante_crear"), datos)
        self.assertContains(resp, "Sin la autorización de tratamiento de datos")
        self.assertFalse(Participante.objects.filter(documento_identidad="3001").exists())

    def test_documento_duplicado(self):
        resp = self.client.post(reverse("pva:participante_crear"), self.datos_participante(documento_identidad="1001"))
        self.assertContains(resp, "Ya existe un participante con ese documento")

    def test_datos_minimos_obligatorios(self):
        resp = self.client.post(
            reverse("pva:participante_crear"), self.datos_participante(telefono="", direccion="", fecha_nacimiento="")
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context["form"].errors), 3)

    def test_cambio_de_casa_conserva_historial(self):
        datos = self.datos_participante(
            nombres_apellidos=self.ana.nombres_apellidos, documento_identidad="1001", casa_vida=self.casa2.pk
        )
        self.client.post(reverse("pva:participante_editar", args=[self.ana.pk]), datos)
        membresias = dict(CasaVidaMiembro.objects.filter(id_participante=self.ana).values_list("id_casa_vida", "estado"))
        self.assertEqual(membresias, {self.casa.pk: INACTIVO, self.casa2.pk: ACTIVO})

    def test_desactivar_y_reactivar_participante(self):
        self.client.post(reverse("pva:participante_estado", args=[self.ana.pk, "desactivar"]))
        self.ana.refresh_from_db()
        self.assertEqual(self.ana.estado, INACTIVO)
        self.client.post(reverse("pva:participante_estado", args=[self.ana.pk, "activar"]))
        self.ana.refresh_from_db()
        self.assertEqual(self.ana.estado, ACTIVO)

    def test_no_se_desactiva_area_con_casas_activas(self):
        self.client.post(reverse("pva:area_estado", args=[self.area.pk, "desactivar"]))
        self.area.refresh_from_db()
        self.assertEqual(self.area.estado, ACTIVO)

    def test_accion_de_estado_desconocida(self):
        resp = self.client.post(reverse("pva:casa_estado", args=[self.casa.pk, "borrar"]))
        self.assertEqual(resp.status_code, 404)

    def test_pastor_ve_todo(self):
        resp = self.client.get(reverse("pva:participantes"))
        self.assertEqual(len(resp.context["participantes"]), 3)
        resp = self.client.get(reverse("pva:casas"))
        self.assertEqual(len(resp.context["casas"]), 2)


class SoloLecturaTests(BaseCasasVida):
    """RN20: solo el Pastor modifica; los demás roles consultan sin editar."""

    def test_roles_no_pastor_no_pueden_modificar(self):
        rutas_get = [
            reverse("pva:areas"),
            reverse("pva:area_crear"),
            reverse("pva:casa_crear"),
            reverse("pva:casa_editar", args=[self.casa.pk]),
            reverse("pva:participante_crear"),
            reverse("pva:participante_editar", args=[self.ana.pk]),
        ]
        for user in (self.supervisor, self.lider, self.apoyo):
            self.entrar(user)
            for ruta in rutas_get:
                self.assertEqual(self.client.get(ruta).status_code, 403, (user.correo, ruta))
            resp = self.client.post(reverse("pva:casa_estado", args=[self.casa.pk, "desactivar"]))
            self.assertEqual(resp.status_code, 403)
        self.casa.refresh_from_db()
        self.assertEqual(self.casa.estado, ACTIVO)

    def test_lista_no_muestra_acciones_de_edicion(self):
        self.entrar(self.lider)
        resp = self.client.get(reverse("pva:casas"))
        self.assertContains(resp, "Solo lectura")
        self.assertNotContains(resp, reverse("pva:casa_editar", args=[self.casa.pk]))

    def test_coordinador_no_accede_al_modulo(self):
        self.entrar(self.coord)
        self.assertEqual(self.client.get(reverse("pva:participantes")).status_code, 403)

    def test_anonimo_va_al_login(self):
        resp = self.client.get(reverse("pva:casas"))
        self.assertEqual(resp.status_code, 302)
        self.assertIn(reverse("cuentas:login"), resp["Location"])


class AlcanceTests(BaseCasasVida):
    """RF06, RF08, RN03–RN05: cada rol ve solo lo de su Área o su Casa de Vida."""

    def test_supervisor_ve_solo_casas_de_su_area(self):
        self.entrar(self.supervisor)
        resp = self.client.get(reverse("pva:casas"))
        self.assertEqual([c.nombre for c in resp.context["casas"]], ["Casa Norte"])
        self.assertEqual(self.client.get(reverse("pva:casa_detalle", args=[self.casa.pk])).status_code, 200)
        self.assertEqual(self.client.get(reverse("pva:casa_detalle", args=[self.casa2.pk])).status_code, 404)

    def test_lider_ve_solo_participantes_de_su_casa(self):
        self.entrar(self.lider)
        resp = self.client.get(reverse("pva:participantes"))
        self.assertEqual({p.pk for p in resp.context["participantes"]}, {self.ana.pk, self.beto.pk})
        self.assertEqual(self.client.get(reverse("pva:participante_detalle", args=[self.carla.pk])).status_code, 404)

    def test_apoyo_ve_su_casa(self):
        self.entrar(self.apoyo)
        resp = self.client.get(reverse("pva:casas"))
        self.assertEqual([c.pk for c in resp.context["casas"]], [self.casa.pk])

    def test_participante_inactivo_no_lo_ve_el_lider(self):
        Participante.objects.filter(pk=self.beto.pk).update(estado=INACTIVO)
        self.entrar(self.lider)
        resp = self.client.get(reverse("pva:participantes"))
        self.assertEqual([p.pk for p in resp.context["participantes"]], [self.ana.pk])

    def test_busqueda_por_documento(self):
        self.entrar(self.pastor)
        resp = self.client.get(reverse("pva:participantes"), {"q": "200"})
        self.assertEqual([p.pk for p in resp.context["participantes"]], [self.carla.pk])

    def test_supervisor_no_ve_participantes_de_otra_area_aunque_filtre(self):
        self.entrar(self.supervisor)
        resp = self.client.get(reverse("pva:participantes"), {"casa": self.casa2.pk})
        self.assertEqual(len(resp.context["participantes"]), 0)


class AsistenciaTests(BaseCasasVida):
    """RF09, RF10, RN06, RN08."""

    def registrar(self, user, presentes, titulo="Reunión semanal", fecha=None):
        self.entrar(user)
        datos = {"titulo": titulo, "fecha": (fecha or datetime.date.today()).isoformat(), "descripcion": ""}
        for p in presentes:
            datos[f"presente_{p.pk}"] = "1"
        return self.client.post(reverse("pva:asistencia_registrar"), datos)

    def test_apoyo_registra_asistencia_de_su_casa(self):
        resp = self.registrar(self.apoyo, [self.ana])
        actividad = Actividad.objects.get()
        self.assertRedirects(resp, reverse("pva:asistencia_detalle", args=[actividad.pk]))
        self.assertEqual(actividad.id_casa_vida, self.casa)
        self.assertEqual(actividad.id_responsable, self.apoyo)
        registros = dict(Asistencia.objects.values_list("id_participante", "presente"))
        self.assertEqual(registros, {self.ana.pk: True, self.beto.pk: False})

    def test_registro_duplicado_aparece_como_enviado(self):
        self.registrar(self.lider, [self.ana])
        resp = self.registrar(self.apoyo, [self.beto])
        self.assertContains(resp, "ya fue registrada por Lider")
        self.assertEqual(Actividad.objects.count(), 1)

    def test_no_se_registra_fecha_futura(self):
        resp = self.registrar(self.lider, [self.ana], fecha=datetime.date.today() + datetime.timedelta(days=1))
        self.assertContains(resp, "fecha futura")
        self.assertFalse(Actividad.objects.exists())

    def test_pastor_y_supervisor_no_registran(self):
        for user in (self.pastor, self.supervisor):
            self.entrar(user)
            self.assertEqual(self.client.get(reverse("pva:asistencia_registrar")).status_code, 403)

    def test_participante_de_otra_casa_no_se_registra(self):
        self.registrar(self.lider, [self.ana, self.carla])
        self.assertFalse(Asistencia.objects.filter(id_participante=self.carla).exists())

    def test_consulta_segun_alcance(self):
        self.registrar(self.lider, [self.ana])
        self.registrar(self.lider2, [self.carla])
        esperado = {self.supervisor: 1, self.supervisor2: 1, self.apoyo: 1, self.pastor: 2}
        for user, total in esperado.items():
            self.entrar(user)
            resp = self.client.get(reverse("pva:asistencia"))
            self.assertEqual(len(resp.context["actividades"]), total, user.correo)
        otra = Actividad.objects.get(id_casa_vida=self.casa2)
        self.entrar(self.supervisor)
        self.assertEqual(self.client.get(reverse("pva:asistencia_detalle", args=[otra.pk])).status_code, 404)

    def test_panel_muestra_resumen_real(self):
        self.registrar(self.lider, [self.ana])
        self.entrar(self.supervisor)
        resp = self.client.get(reverse("pva:panel"))
        resumen = resp.context["resumen_pva"]
        self.assertEqual(resumen["participantes"], 2)
        self.assertEqual(resumen["asistenciaPromedio"], 50)
