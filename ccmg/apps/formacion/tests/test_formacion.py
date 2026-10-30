"""Pruebas del módulo Escuelas de Formación: RF18–RF22, RN12, RN13, RN24 y HU-25 a HU-36."""
import datetime

from django.urls import reverse

from cuentas.models import Usuario
from formacion.models import InscripcionFormacion, ProcesoFormacion
from nucleo.models import Auditoria
from pva.models import ACTIVO, INACTIVO, Actividad, Asistencia, Participante, Seguimiento
from pva.tests.test_casas_vida import CLAVE, BaseCasasVida

HOY = datetime.date.today()


class BaseFormacion(BaseCasasVida):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.coord2 = Usuario.objects.create_user(
            correo="coord2@ccmg.org", nombre_completo="Coord2", rol=cls.rol["COORDINADOR_FORMACION"], password=CLAVE
        )
        cls.pasos = ProcesoFormacion.objects.create(nombre="Pasos de Vida 2026", tipo_proceso="PASOS_VIDA", id_coordinador=cls.coord)
        cls.misiones = ProcesoFormacion.objects.create(nombre="Misiones 2026", tipo_proceso="MISIONES", id_coordinador=cls.coord2)
        InscripcionFormacion.objects.create(id_participante=cls.ana, id_proceso_formacion=cls.pasos)
        InscripcionFormacion.objects.create(id_participante=cls.beto, id_proceso_formacion=cls.pasos)
        InscripcionFormacion.objects.create(id_participante=cls.carla, id_proceso_formacion=cls.misiones)

    def datos_persona(self, **extra):
        d = {
            "nombres_apellidos": "Elena Mora", "documento_identidad": "5001", "fecha_nacimiento": "1995-03-03",
            "telefono": "3015550000", "direccion": "Calle 7", "autorizacion_datos": "on", "proceso": self.pasos.pk,
        }
        d.update(extra)
        return d


class ProcesosTests(BaseFormacion):
    """RF18, RN12, RN13, RN24."""

    def test_coordinador_crea_proceso_propio(self):
        self.entrar(self.coord)
        resp = self.client.post(reverse("formacion:proceso_crear"), {"nombre": "Escuela Vida 1", "tipo_proceso": "ESCUELAS_VIDA"})
        p = ProcesoFormacion.objects.get(nombre="Escuela Vida 1")
        self.assertRedirects(resp, reverse("formacion:proceso_detalle", args=[p.pk]))
        self.assertEqual(p.id_coordinador, self.coord)
        self.assertTrue(Auditoria.objects.filter(entidad="proceso_formacion", id_entidad=p.pk).exists())

    def test_pastor_asigna_coordinador(self):
        self.entrar(self.pastor)
        self.client.post(
            reverse("formacion:proceso_crear"),
            {"nombre": "Liderazgo 1", "tipo_proceso": "MODULOS_LIDERAZGO", "id_coordinador": self.coord2.pk},
        )
        self.assertEqual(ProcesoFormacion.objects.get(nombre="Liderazgo 1").id_coordinador, self.coord2)

    def test_coordinador_ve_solo_sus_procesos(self):
        self.entrar(self.coord)
        resp = self.client.get(reverse("formacion:procesos"))
        self.assertEqual([p.pk for p in resp.context["procesos"]], [self.pasos.pk])
        self.assertEqual(self.client.get(reverse("formacion:proceso_detalle", args=[self.misiones.pk])).status_code, 404)
        self.entrar(self.pastor)
        self.assertEqual(len(self.client.get(reverse("formacion:procesos")).context["procesos"]), 2)

    def test_filtro_por_escuela(self):
        self.entrar(self.pastor)
        resp = self.client.get(reverse("formacion:procesos"), {"tipo": "MISIONES"})
        self.assertEqual([p.pk for p in resp.context["procesos"]], [self.misiones.pk])

    def test_solo_el_pastor_desactiva_procesos(self):
        self.entrar(self.coord)
        self.assertEqual(self.client.post(reverse("formacion:proceso_estado", args=[self.pasos.pk, "desactivar"])).status_code, 403)
        self.entrar(self.pastor)
        self.client.post(reverse("formacion:proceso_estado", args=[self.pasos.pk, "desactivar"]))
        self.pasos.refresh_from_db()
        self.assertEqual(self.pasos.estado, INACTIVO)

    def test_roles_de_casas_no_acceden(self):
        for user in (self.supervisor, self.lider, self.apoyo):
            self.entrar(user)
            self.assertEqual(self.client.get(reverse("formacion:procesos")).status_code, 403)
            self.assertEqual(self.client.get(reverse("formacion:panel")).status_code, 403)


class ParticipantesFormacionTests(BaseFormacion):
    """RF05/RF06 para el Coordinador, HU-25 criterios 1–3."""

    def test_registra_participante_nuevo_inscrito(self):
        self.entrar(self.coord)
        resp = self.client.post(reverse("formacion:participante_crear"), self.datos_persona())
        p = Participante.objects.get(documento_identidad="5001")
        self.assertRedirects(resp, reverse("formacion:participante_detalle", args=[p.pk]))
        self.assertTrue(InscripcionFormacion.objects.filter(id_participante=p, id_proceso_formacion=self.pasos, estado=ACTIVO).exists())
        self.assertIsNone(p.membresia_activa)

    def test_exige_datos_y_autorizacion(self):
        self.entrar(self.coord)
        datos = self.datos_persona(telefono="")
        del datos["autorizacion_datos"]
        resp = self.client.post(reverse("formacion:participante_crear"), datos)
        self.assertEqual(set(resp.context["form"].errors), {"telefono", "autorizacion_datos"})

    def test_documento_existente_sugiere_inscribir(self):
        self.entrar(self.coord)
        resp = self.client.post(reverse("formacion:participante_crear"), self.datos_persona(documento_identidad="2001"))
        self.assertIn("Inscribir participante existente", resp.context["form"].errors["documento_identidad"][0])

    def test_no_inscribe_en_proceso_ajeno(self):
        self.entrar(self.coord)
        resp = self.client.post(reverse("formacion:participante_crear"), self.datos_persona(proceso=self.misiones.pk))
        self.assertIn("proceso", resp.context["form"].errors)

    def test_inscribir_existente(self):
        self.entrar(self.coord)
        resp = self.client.post(reverse("formacion:inscribir"), {"documento_identidad": "2001", "proceso": self.pasos.pk})
        self.assertRedirects(resp, reverse("formacion:proceso_detalle", args=[self.pasos.pk]))
        self.assertTrue(InscripcionFormacion.objects.filter(id_participante=self.carla, id_proceso_formacion=self.pasos).exists())
        resp = self.client.post(reverse("formacion:inscribir"), {"documento_identidad": "2001", "proceso": self.pasos.pk})
        self.assertIn("ya está inscrito", resp.context["form"].non_field_errors()[0])

    def test_coordinador_ve_y_edita_solo_sus_participantes(self):
        self.entrar(self.coord)
        resp = self.client.get(reverse("formacion:participantes"))
        self.assertEqual({p.pk for p in resp.context["participantes"]}, {self.ana.pk, self.beto.pk})
        self.assertEqual(self.client.get(reverse("formacion:participante_detalle", args=[self.carla.pk])).status_code, 404)
        self.assertEqual(self.client.get(reverse("formacion:participante_editar", args=[self.carla.pk])).status_code, 404)
        datos = self.datos_persona(nombres_apellidos="Ana Pérez Ruiz", documento_identidad="1001")
        del datos["proceso"]
        self.client.post(reverse("formacion:participante_editar", args=[self.ana.pk]), datos)
        self.ana.refresh_from_db()
        self.assertEqual(self.ana.nombres_apellidos, "Ana Pérez Ruiz")

    def test_retirar_y_reincorporar_inscripcion(self):
        insc = InscripcionFormacion.objects.get(id_participante=self.ana, id_proceso_formacion=self.pasos)
        self.entrar(self.coord)
        self.client.post(reverse("formacion:inscripcion_estado", args=[insc.pk, "desactivar"]))
        insc.refresh_from_db()
        self.assertEqual(insc.estado, INACTIVO)
        self.client.post(reverse("formacion:inscripcion_estado", args=[insc.pk, "activar"]))
        insc.refresh_from_db()
        self.assertEqual(insc.estado, ACTIVO)
        otra = InscripcionFormacion.objects.get(id_participante=self.carla)
        self.assertEqual(self.client.post(reverse("formacion:inscripcion_estado", args=[otra.pk, "desactivar"])).status_code, 404)


class ActividadesFormacionTests(BaseFormacion):
    """HU-26 criterios 1–3."""

    def registrar(self, presentes, proceso=None, **extra):
        datos = {"titulo": "Clase 1", "fecha": HOY.isoformat(), "descripcion": "Intro"}
        datos.update(extra)
        for p in presentes:
            datos[f"presente_{p.pk}"] = "1"
        return self.client.post(reverse("formacion:actividad_registrar", args=[(proceso or self.pasos).pk]), datos)

    def test_registra_actividad_y_asistencia(self):
        self.entrar(self.coord)
        resp = self.registrar([self.ana])
        act = Actividad.objects.get()
        self.assertRedirects(resp, reverse("formacion:actividad_detalle", args=[act.pk]))
        self.assertEqual((act.tipo_modulo, act.id_proceso_formacion, act.id_casa_vida), ("ESCUELAS_FORMACION", self.pasos, None))
        self.assertEqual(dict(Asistencia.objects.values_list("id_participante", "presente")), {self.ana.pk: True, self.beto.pk: False})

    def test_no_registra_asistencia_de_no_inscritos(self):
        self.entrar(self.coord)
        self.registrar([self.ana, self.carla])
        self.assertFalse(Asistencia.objects.filter(id_participante=self.carla).exists())

    def test_retirados_no_aparecen(self):
        InscripcionFormacion.objects.filter(id_participante=self.beto).update(estado=INACTIVO)
        self.entrar(self.coord)
        self.registrar([self.ana])
        self.assertEqual(list(Asistencia.objects.values_list("id_participante", flat=True)), [self.ana.pk])

    def test_actividad_duplicada_y_fecha_futura(self):
        self.entrar(self.coord)
        self.registrar([self.ana])
        resp = self.registrar([self.ana])
        self.assertIn("ya está registrada", resp.context["form"].non_field_errors()[0])
        resp = self.registrar([self.ana], titulo="Clase 2", fecha=(HOY + datetime.timedelta(days=1)).isoformat())
        self.assertIn("fecha", resp.context["form"].errors)
        self.assertEqual(Actividad.objects.count(), 1)

    def test_no_registra_en_proceso_ajeno_o_inactivo(self):
        self.entrar(self.coord)
        self.assertEqual(self.client.get(reverse("formacion:actividad_registrar", args=[self.misiones.pk])).status_code, 404)
        ProcesoFormacion.objects.filter(pk=self.pasos.pk).update(estado=INACTIVO)
        self.assertEqual(self.client.get(reverse("formacion:actividad_registrar", args=[self.pasos.pk])).status_code, 404)

    def test_las_actividades_de_formacion_no_salen_en_casas_de_vida(self):
        self.entrar(self.coord)
        self.registrar([self.ana])
        self.entrar(self.pastor)
        self.assertEqual(len(self.client.get(reverse("pva:asistencia")).context["actividades"]), 0)
        self.assertEqual(len(self.client.get(reverse("formacion:actividades")).context["actividades"]), 1)


class SeguimientoFormacionTests(BaseFormacion):
    """RF11 para el Coordinador, HU-36."""

    def test_registra_seguimiento_asociado_al_proceso(self):
        self.entrar(self.coord)
        resp = self.client.post(
            reverse("formacion:seguimiento_crear"),
            {"id_proceso_formacion": self.pasos.pk, "id_participante": self.ana.pk, "fecha": HOY.isoformat(),
             "tipo": "LLAMADA", "estado": "ABIERTO", "observacion": "Avanza bien"},
        )
        self.assertRedirects(resp, reverse("formacion:participante_detalle", args=[self.ana.pk]))
        s = Seguimiento.objects.get()
        self.assertEqual((s.tipo_modulo, s.id_proceso_formacion, s.id_usuario), ("ESCUELAS_FORMACION", self.pasos, self.coord))

    def test_participante_debe_estar_inscrito(self):
        self.entrar(self.pastor)
        resp = self.client.post(
            reverse("formacion:seguimiento_crear"),
            {"id_proceso_formacion": self.pasos.pk, "id_participante": self.carla.pk, "fecha": HOY.isoformat(),
             "tipo": "VISITA", "estado": "ABIERTO", "observacion": "x"},
        )
        self.assertIn("no está inscrito", resp.context["form"].errors["id_participante"][0])

    def test_alcance_y_separacion_de_modulos(self):
        Seguimiento.objects.create(id_participante=self.ana, id_usuario=self.coord, observacion="f", tipo_modulo="ESCUELAS_FORMACION", id_proceso_formacion=self.pasos)
        Seguimiento.objects.create(id_participante=self.carla, id_usuario=self.coord2, observacion="m", tipo_modulo="ESCUELAS_FORMACION", id_proceso_formacion=self.misiones)
        Seguimiento.objects.create(id_participante=self.ana, id_usuario=self.pastor, observacion="c", tipo_modulo="CASA_VIDA")
        self.entrar(self.coord)
        self.assertEqual([s.observacion for s in self.client.get(reverse("formacion:seguimientos")).context["seguimientos"]], ["f"])
        self.entrar(self.lider)
        self.assertEqual([s.observacion for s in self.client.get(reverse("pva:seguimientos")).context["seguimientos"]], ["c"])


class ReportesFormacionTests(BaseFormacion):
    """RF15/RF16 para el Coordinador, HU-27 criterios 1–2."""

    def test_reporte_por_periodo_solo_de_sus_procesos(self):
        act = Actividad.objects.create(tipo_modulo="ESCUELAS_FORMACION", id_proceso_formacion=self.pasos, titulo="Clase", fecha=HOY, id_responsable=self.coord)
        Asistencia.objects.create(id_actividad=act, id_participante=self.ana, presente=True)
        Asistencia.objects.create(id_actividad=act, id_participante=self.beto, presente=False)
        self.entrar(self.coord)
        resp = self.client.get(reverse("formacion:reportes"), {"tipo": "mensual", "fecha": HOY.isoformat()})
        filas = resp.context["filas"]
        self.assertEqual([f["proceso"] for f in filas], [self.pasos])
        self.assertEqual((filas[0]["actividades"], filas[0]["porcentaje"], filas[0]["inscritos"]), (1, 50, 2))

    def test_filtro_por_escuela_y_sin_datos(self):
        self.entrar(self.pastor)
        resp = self.client.get(reverse("formacion:reportes"), {"tipo": "anual", "fecha": "2020-01-01", "tipo_proceso": "MISIONES"})
        self.assertEqual([f["proceso"] for f in resp.context["filas"]], [self.misiones])
        self.assertContains(resp, "No hay información registrada")

    def test_panel_resumen(self):
        self.entrar(self.coord)
        resumen = self.client.get(reverse("formacion:panel")).context["resumen_formacion"]
        self.assertEqual((resumen["procesosActivos"], resumen["inscritos"]), (1, 2))
