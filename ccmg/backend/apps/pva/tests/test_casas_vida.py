"""Pruebas del módulo Casas de Vida: RF05–RF10, RF28 y reglas RN03–RN09, RN20, RN23, RN24."""
import datetime

from django.test import TestCase
from django.urls import reverse

from cuentas.models import Rol, Usuario
from nucleo.models import Auditoria
from ofrendas.models import Ofrenda
from pva import periodos
from pva.models import (
    ACTIVO,
    INACTIVO,
    Area,
    CasaVida,
    CasaVidaEquipo,
    CasaVidaMiembro,
    Participante,
    Reporte,
    ReporteAsistencia,
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
            nombre="Casa Norte", id_area=cls.area, id_lider=cls.lider
        )
        cls.casa2 = CasaVida.objects.create(
            nombre="Casa Sur", id_area=cls.area2, id_lider=cls.lider2
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

    def reporte_asistencia(self, casa, fecha, envia, **valores):
        """Reporte semanal de una Casa de Vida con los totales de su reunión."""
        semana = periodos.semana(fecha)
        reporte = Reporte.objects.create(
            tipo_modulo="CASA_VIDA", tipo_reporte="CASA_VIDA", id_usuario_envia=envia, id_usuario_destino=casa.supervisor,
            id_casa_vida=casa, id_area=casa.id_area, periodo=semana.etiqueta, fecha_inicio=semana.inicio, fecha_fin=semana.fin,
        )
        ReporteAsistencia.objects.create(id_reporte=reporte, fecha=fecha, id_lider=casa.id_lider, **valores)
        return reporte

    def datos_asistencia(self, fecha=None, **extra):
        """Formulario del reporte de asistencia con el formato de la iglesia."""
        datos = {c: "0" for c, _ in ReporteAsistencia.INDICADORES + ReporteAsistencia.ESCUELAS + ReporteAsistencia.CULTOS}
        del datos["sabado"]
        datos.update(
            fecha=(fecha or datetime.date.today()).isoformat(), asistentes="14", ninos="4", nuevos="2",
            conversiones="1", pasos_vida="2", ciclo_conexion="1", dominical="12", ofrenda="185000", observaciones="",
        )
        datos.update(extra)
        return datos

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
        self.assertEqual(casa.supervisor, self.supervisor)
        self.assertTrue(Auditoria.objects.filter(entidad="casa_vida", id_entidad=casa.pk, accion="CREAR").exists())

    def test_cambiar_supervisor_del_area_actualiza_sus_casas(self):
        nuevo = Usuario.objects.create_user(
            correo="sup3@ccmg.org", nombre_completo="Sup 3", rol=self.rol["SUPERVISOR_AREA"], password=CLAVE
        )
        self.client.post(reverse("pva:area_editar", args=[self.area.pk]), {"nombre": "Norte", "id_supervisor": nuevo.pk})
        self.casa.refresh_from_db()
        self.assertEqual(self.casa.supervisor, nuevo)

    def test_lider_no_puede_liderar_dos_casas_activas(self):
        resp = self.client.post(
            reverse("pva:casa_crear"), {"nombre": "Otra", "id_area": self.area.pk, "id_lider": self.lider.pk}
        )
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "ya está asignado a la Casa de Vida")

    def test_pastor_no_registra_personas_nuevas(self):
        """En la Casa de Vida no se lleva una lista fija: el Pastor no registra participantes."""
        self.assertEqual(self.client.get(reverse("pva:participante_crear")).status_code, 403)

    def test_pastor_corrige_los_datos_de_una_persona(self):
        resp = self.client.post(
            reverse("pva:participante_editar", args=[self.ana.pk]),
            {"nombres_apellidos": "Ana María  Pérez", "telefono": "3119998877", "autorizacion_datos": "on"},
        )
        self.assertRedirects(resp, reverse("pva:participante_detalle", args=[self.ana.pk]))
        self.ana.refresh_from_db()
        self.assertEqual((self.ana.nombres_apellidos, self.ana.telefono), ("Ana María Pérez", "3119998877"))
        self.assertEqual(self.ana.documento_identidad, "1001")  # los demás datos no se pierden

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

    def test_busqueda_por_nombre_o_telefono(self):
        Participante.objects.filter(pk=self.carla.pk).update(telefono="3155550000")
        self.entrar(self.pastor)
        resp = self.client.get(reverse("pva:participantes"), {"q": "315555"})
        self.assertEqual([p.pk for p in resp.context["participantes"]], [self.carla.pk])
        resp = self.client.get(reverse("pva:participantes"), {"q": "beto"})
        self.assertEqual([p.pk for p in resp.context["participantes"]], [self.beto.pk])

    def test_supervisor_no_ve_participantes_de_otra_area_aunque_filtre(self):
        self.entrar(self.supervisor)
        resp = self.client.get(reverse("pva:participantes"), {"casa": self.casa2.pk})
        self.assertEqual(len(resp.context["participantes"]), 0)


class PersonasNuevasTests(BaseCasasVida):
    """RF05, RN09: el Líder o su equipo toman nombre y teléfono de quien llega por primera vez."""

    def registrar(self, user, **extra):
        self.entrar(user)
        datos = {"nombres_apellidos": "  Diana   López ", "telefono": "310 987 6543", "autorizacion_datos": "on"}
        datos.update(extra)
        return self.client.post(reverse("pva:participante_crear"), datos)

    def test_lider_registra_persona_nueva_con_nombre_y_telefono(self):
        resp = self.registrar(self.lider)
        self.assertRedirects(resp, reverse("pva:participantes"))
        p = Participante.objects.get(nombres_apellidos="Diana López")
        self.assertIsNone(p.documento_identidad)
        self.assertEqual(p.telefono, "310 987 6543")
        membresia = p.membresia_activa
        self.assertEqual((membresia.id_casa_vida, membresia.fecha_ingreso), (self.casa, datetime.date.today()))
        self.assertTrue(Auditoria.objects.filter(entidad="participante", id_entidad=p.pk, accion="CREAR").exists())

    def test_apoyo_tambien_registra(self):
        self.registrar(self.apoyo, nombres_apellidos="Elena Mora")
        self.assertEqual(Participante.objects.get(nombres_apellidos="Elena Mora").membresia_activa.id_casa_vida, self.casa)

    def test_varias_personas_sin_documento(self):
        """El documento es opcional: dos personas nuevas sin documento no chocan con la restricción única."""
        self.registrar(self.lider, nombres_apellidos="Persona Uno")
        self.registrar(self.lider, nombres_apellidos="Persona Dos")
        self.assertEqual(Participante.objects.filter(documento_identidad__isnull=True).count(), 2)

    def test_sin_autorizacion_no_se_registra(self):
        """RN23: la autorización de datos es obligatoria también en el formulario corto de persona nueva."""
        datos = {"nombres_apellidos": "Fabio Ríos", "telefono": "3001112233"}
        self.entrar(self.lider)
        resp = self.client.post(reverse("pva:participante_crear"), datos)
        self.assertEqual(resp.status_code, 200)
        self.assertIn("autorizacion_datos", resp.context["form"].errors)
        self.assertFalse(Participante.objects.filter(nombres_apellidos="Fabio Ríos").exists())

    def test_nombre_y_telefono_obligatorios(self):
        resp = self.registrar(self.lider, nombres_apellidos="", telefono="")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(set(resp.context["form"].errors), {"nombres_apellidos", "telefono"})
        resp = self.registrar(self.lider, telefono="abc")
        self.assertIn("teléfono válido", resp.context["form"].errors["telefono"][0])

    def test_supervisor_y_pastor_solo_consultan(self):
        for user in (self.supervisor, self.pastor):
            self.entrar(user)
            self.assertEqual(self.client.get(reverse("pva:participante_crear")).status_code, 403)
            self.assertEqual(self.client.get(reverse("pva:participantes")).status_code, 200)

    def test_el_equipo_corrige_solo_los_de_su_casa(self):
        self.entrar(self.lider)
        self.assertEqual(self.client.get(reverse("pva:participante_editar", args=[self.ana.pk])).status_code, 200)
        self.entrar(self.lider2)
        self.assertEqual(self.client.get(reverse("pva:participante_editar", args=[self.ana.pk])).status_code, 404)
        self.entrar(self.supervisor)
        self.assertEqual(self.client.get(reverse("pva:participante_editar", args=[self.ana.pk])).status_code, 403)


class AsistenciaTests(BaseCasasVida):
    """RF09, RF10, RF14, RN06, RN08: reporte de asistencia por totales de la reunión."""

    def llenar(self, user, **extra):
        self.entrar(user)
        return self.client.post(reverse("pva:asistencia_registrar"), self.datos_asistencia(**extra))

    def test_apoyo_llena_el_reporte_y_queda_enviado_al_supervisor(self):
        resp = self.llenar(self.apoyo)
        reporte = Reporte.objects.get()
        self.assertRedirects(resp, reverse("pva:reporte_detalle", args=[reporte.pk]))
        self.assertEqual(
            (reporte.id_casa_vida, reporte.id_usuario_envia, reporte.id_usuario_destino, reporte.periodo),
            (self.casa, self.apoyo, self.supervisor, periodos.semana(datetime.date.today()).etiqueta),
        )
        a = reporte.asistencia
        self.assertEqual((a.fecha, a.id_lider, a.asistentes, a.ninos, a.nuevos, a.dominical), (datetime.date.today(), self.lider, 14, 4, 2, 12))
        self.assertEqual(a.total_discipulos_escuelas, 3)
        self.assertIsNone(a.sabado)
        self.assertTrue(Auditoria.objects.filter(accion="ENVIAR_REPORTE", id_entidad=reporte.pk).exists())

    def test_la_ofrenda_va_al_modulo_de_ofrendas(self):
        self.llenar(self.lider)
        a = ReporteAsistencia.objects.get()
        ofrenda = Ofrenda.objects.get()
        self.assertEqual(a.id_ofrenda, ofrenda)
        self.assertEqual((ofrenda.valor, ofrenda.id_casa_vida, ofrenda.fecha), (185000, self.casa, a.fecha))

    def test_ofrenda_en_cero_no_crea_registro(self):
        self.llenar(self.lider, ofrenda="0")
        self.assertIsNone(ReporteAsistencia.objects.get().id_ofrenda)
        self.assertFalse(Ofrenda.objects.exists())

    def test_sabado_solo_en_areas_r21_y_zonar21(self):
        self.entrar(self.lider)
        self.assertNotIn("sabado", self.client.get(reverse("pva:asistencia_registrar")).context["form"].fields)
        for nombre in ("ZONAR21", "ZONR21", "R21"):
            Area.objects.filter(pk=self.area.pk).update(nombre=nombre)
            self.assertIn("sabado", self.client.get(reverse("pva:asistencia_registrar")).context["form"].fields, nombre)
        self.llenar(self.lider, sabado="9")
        self.assertEqual(ReporteAsistencia.objects.get().sabado, 9)

    def test_semana_ya_reportada_aparece_como_enviada(self):
        self.llenar(self.lider)
        resp = self.llenar(self.apoyo)
        self.assertEqual(resp.status_code, 200)
        self.assertIn("ya fue enviado por Lider", resp.context["form"].errors["fecha"][0])
        self.assertEqual(resp.context["ya_enviado"].id_usuario_envia, self.lider)
        self.assertEqual(Reporte.objects.count(), 1)

    def test_no_se_reporta_fecha_futura_ni_valores_negativos(self):
        resp = self.llenar(self.lider, fecha=datetime.date.today() + datetime.timedelta(days=1))
        self.assertContains(resp, "fecha futura")
        resp = self.llenar(self.lider, asistentes="-3")
        self.assertIn("asistentes", resp.context["form"].errors)
        self.assertFalse(Reporte.objects.exists())

    def test_sin_supervisor_no_se_envia(self):
        Area.objects.filter(pk=self.area.pk).update(id_supervisor=None)
        resp = self.llenar(self.lider)
        self.assertContains(resp, "no tiene Supervisor de Área")
        self.assertFalse(Reporte.objects.exists())

    def test_pastor_y_supervisor_no_llenan_el_reporte(self):
        for user in (self.pastor, self.supervisor):
            self.entrar(user)
            self.assertEqual(self.client.get(reverse("pva:asistencia_registrar")).status_code, 403)

    def test_consulta_segun_alcance(self):
        self.reporte_asistencia(self.casa, datetime.date.today(), self.lider, asistentes=10)
        otro = self.reporte_asistencia(self.casa2, datetime.date.today(), self.lider2, asistentes=8)
        esperado = {self.supervisor: 1, self.supervisor2: 1, self.apoyo: 1, self.pastor: 2}
        for user, total in esperado.items():
            self.entrar(user)
            resp = self.client.get(reverse("pva:asistencia"))
            self.assertEqual(len(resp.context["asistencias"]), total, user.correo)
        self.entrar(self.supervisor)
        self.assertEqual(self.client.get(reverse("pva:reporte_detalle", args=[otro.pk])).status_code, 404)
        self.assertRedirects(
            self.client.get(reverse("pva:asistencia_detalle", args=[otro.pk])),
            reverse("pva:reporte_detalle", args=[otro.pk]), target_status_code=404,
        )

    def test_panel_muestra_resumen_real(self):
        self.reporte_asistencia(self.casa, datetime.date.today(), self.lider, asistentes=14)
        self.reporte_asistencia(self.casa, datetime.date.today() - datetime.timedelta(weeks=1), self.lider, asistentes=10)
        self.entrar(self.supervisor)
        resumen = self.client.get(reverse("pva:panel")).context["resumen_pva"]
        self.assertEqual(resumen["participantes"], 2)
        self.assertEqual(resumen["asistenciaPromedio"], 12)
