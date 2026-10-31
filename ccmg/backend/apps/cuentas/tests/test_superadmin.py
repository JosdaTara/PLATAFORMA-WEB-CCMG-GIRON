"""Rol Super Administrador: hereda todo lo del Pastor, queda oculto para él y ve la bitácora."""
import io

from django.core.management import call_command
from django.core.management.base import CommandError
from django.urls import reverse

from cuentas.models import Usuario
from nucleo.models import Auditoria
from pva.tests.test_casas_vida import CLAVE, BaseCasasVida


class SuperAdminHeredaPastorTests(BaseCasasVida):
    def test_accede_a_todo_lo_del_pastor(self):
        self.entrar(self.superadmin)
        rutas = [
            reverse("cuentas:selector_modulo"), reverse("cuentas:usuarios_list"), reverse("pva:panel"),
            reverse("pva:casas"), reverse("pva:areas"), reverse("pva:importar"), reverse("pva:participantes"),
            reverse("pva:reporte_generar"), reverse("formacion:panel"), reverse("formacion:procesos"),
            reverse("ofrendas:index"),
        ]
        for ruta in rutas:
            self.assertEqual(self.client.get(ruta).status_code, 200, ruta)
        self.assertEqual(len(self.client.get(reverse("pva:casas")).context["casas"]), 2)

    def test_panel_por_rol_lo_lleva_al_selector(self):
        self.entrar(self.superadmin)
        self.assertRedirects(self.client.get(reverse("cuentas:panel_por_rol")), reverse("cuentas:selector_modulo"))

    def test_se_muestra_como_super_administrador(self):
        self.entrar(self.superadmin)
        self.assertContains(self.client.get(reverse("cuentas:selector_modulo")), "Super Administrador")
        resp = self.client.get(reverse("pva:casas"))
        self.assertEqual(resp.context["rol_nombre"], "Super Administrador")
        sesion = self.client.get(reverse("pva:panel")).context["sesion_js"]
        self.assertEqual((sesion["rol"], sesion["rolNombre"], sesion["superadmin"]), ("pastor", "Super Administrador", True))


class ProteccionSuperAdminTests(BaseCasasVida):
    def test_pastor_no_lo_ve_ni_lo_modifica(self):
        self.entrar(self.pastor)
        usuarios = self.client.get(reverse("cuentas:usuarios_list")).context["usuarios"]
        self.assertNotIn(self.superadmin, usuarios)
        for nombre in ("cuentas:usuarios_editar", "cuentas:usuarios_desactivar", "cuentas:usuarios_reactivar"):
            metodo = self.client.get if nombre == "cuentas:usuarios_editar" else self.client.post
            self.assertEqual(metodo(reverse(nombre, args=[self.superadmin.pk])).status_code, 404, nombre)
        self.superadmin.refresh_from_db()
        self.assertTrue(self.superadmin.activo)

    def test_pastor_no_puede_asignar_el_rol(self):
        self.entrar(self.pastor)
        form = self.client.get(reverse("cuentas:usuarios_crear")).context["form"]
        self.assertNotIn("SUPERADMIN", [r.nombre for r in form.fields["rol"].queryset])
        resp = self.client.post(
            reverse("cuentas:usuarios_crear"),
            {"nombre_completo": "Intruso", "correo": "intruso@ccmg.org", "username": "", "rol": self.rol["SUPERADMIN"].pk},
        )
        self.assertIn("rol", resp.context["form"].errors)
        self.assertFalse(Usuario.objects.filter(correo="intruso@ccmg.org").exists())

    def test_superadmin_ve_y_asigna_el_rol(self):
        self.entrar(self.superadmin)
        self.assertIn(self.superadmin, self.client.get(reverse("cuentas:usuarios_list")).context["usuarios"])
        self.client.post(
            reverse("cuentas:usuarios_crear"),
            {"nombre_completo": "Otro Dev", "correo": "dev2@ccmg.org", "username": "", "rol": self.rol["SUPERADMIN"].pk},
        )
        self.assertEqual(Usuario.objects.get(correo="dev2@ccmg.org").rol.nombre, "SUPERADMIN")

    def test_no_queda_sin_super_administrador(self):
        otro = Usuario.objects.create_user(correo="dev2@ccmg.org", nombre_completo="Dev 2", rol=self.rol["SUPERADMIN"], password=CLAVE)
        self.entrar(otro)
        self.client.post(reverse("cuentas:usuarios_desactivar", args=[self.superadmin.pk]))
        self.superadmin.refresh_from_db()
        self.assertFalse(self.superadmin.activo)  # había otro activo
        self.client.post(reverse("cuentas:usuarios_desactivar", args=[otro.pk]))
        otro.refresh_from_db()
        self.assertTrue(otro.activo)  # no se desactiva a sí mismo


class CreacionDeAdministradoresTests(BaseCasasVida):
    """Solo el Super Administrador crea y gestiona Administradores (rol PASTOR); el Pastor gestiona los niveles inferiores."""

    def datos(self, usuario, rol):
        return {"nombre_completo": usuario.nombre_completo, "correo": usuario.correo,
                "username": usuario.username or "", "rol": self.rol[rol].pk}

    def test_pastor_no_puede_crear_administradores(self):
        self.entrar(self.pastor)
        form = self.client.get(reverse("cuentas:usuarios_crear")).context["form"]
        self.assertNotIn("PASTOR", [r.nombre for r in form.fields["rol"].queryset])
        resp = self.client.post(
            reverse("cuentas:usuarios_crear"),
            {"nombre_completo": "Otro Pastor", "correo": "pastor2@ccmg.org", "username": "", "rol": self.rol["PASTOR"].pk},
        )
        self.assertIn("rol", resp.context["form"].errors)
        self.assertFalse(Usuario.objects.filter(correo="pastor2@ccmg.org").exists())

    def test_pastor_no_puede_ascender_a_administrador(self):
        self.entrar(self.pastor)
        resp = self.client.post(reverse("cuentas:usuarios_editar", args=[self.coord.pk]), self.datos(self.coord, "PASTOR"))
        self.assertIn("rol", resp.context["form"].errors)
        self.coord.refresh_from_db()
        self.assertEqual(self.coord.rol.nombre, "COORDINADOR_FORMACION")

    def test_pastor_sigue_creando_los_niveles_inferiores(self):
        self.entrar(self.pastor)
        self.client.post(
            reverse("cuentas:usuarios_crear"),
            {"nombre_completo": "Nuevo Coord", "correo": "coord2@ccmg.org", "username": "",
             "rol": self.rol["COORDINADOR_FORMACION"].pk},
        )
        self.assertEqual(Usuario.objects.get(correo="coord2@ccmg.org").rol.nombre, "COORDINADOR_FORMACION")

    def test_pastor_conserva_su_rol_al_editar_sus_datos(self):
        self.entrar(self.pastor)
        datos = self.datos(self.pastor, "PASTOR") | {"nombre_completo": "Pastor Principal"}
        self.assertRedirects(self.client.post(reverse("cuentas:usuarios_editar", args=[self.pastor.pk]), datos),
                             reverse("cuentas:usuarios_list"))
        self.pastor.refresh_from_db()
        self.assertEqual((self.pastor.nombre_completo, self.pastor.rol.nombre), ("Pastor Principal", "PASTOR"))

    def test_pastor_no_puede_cambiarse_el_rol(self):
        self.entrar(self.pastor)
        resp = self.client.post(reverse("cuentas:usuarios_editar", args=[self.pastor.pk]),
                                self.datos(self.pastor, "COORDINADOR_FORMACION"))
        self.assertIn("rol", resp.context["form"].errors)
        self.pastor.refresh_from_db()
        self.assertEqual(self.pastor.rol.nombre, "PASTOR")

    def test_pastor_no_gestiona_a_otros_administradores(self):
        otro = Usuario.objects.create_user(correo="pastor2@ccmg.org", nombre_completo="Pastor 2",
                                           rol=self.rol["PASTOR"], password=CLAVE)
        self.entrar(self.pastor)
        usuarios = self.client.get(reverse("cuentas:usuarios_list")).context["usuarios"]
        self.assertNotIn(otro, usuarios)
        self.assertIn(self.pastor, usuarios)
        self.assertEqual(self.client.get(reverse("cuentas:usuarios_editar", args=[otro.pk])).status_code, 404)
        self.assertEqual(self.client.post(reverse("cuentas:usuarios_editar", args=[otro.pk]),
                                          self.datos(otro, "PASTOR")).status_code, 404)
        self.assertEqual(self.client.post(reverse("cuentas:usuarios_desactivar", args=[otro.pk])).status_code, 404)
        self.assertEqual(self.client.post(reverse("cuentas:usuarios_reactivar", args=[otro.pk])).status_code, 404)
        otro.refresh_from_db()
        self.assertTrue(otro.activo)

    def test_superadmin_gestiona_a_los_administradores(self):
        otro = Usuario.objects.create_user(correo="pastor2@ccmg.org", nombre_completo="Pastor 2",
                                           rol=self.rol["PASTOR"], password=CLAVE)
        self.entrar(self.superadmin)
        self.assertIn(otro, self.client.get(reverse("cuentas:usuarios_list")).context["usuarios"])
        self.client.post(reverse("cuentas:usuarios_editar", args=[otro.pk]),
                         self.datos(otro, "PASTOR") | {"nombre_completo": "Pastor Dos"})
        self.client.post(reverse("cuentas:usuarios_desactivar", args=[otro.pk]))
        otro.refresh_from_db()
        self.assertEqual((otro.nombre_completo, otro.activo), ("Pastor Dos", False))

    def test_superadmin_crea_administradores(self):
        self.entrar(self.superadmin)
        form = self.client.get(reverse("cuentas:usuarios_crear")).context["form"]
        self.assertIn("PASTOR", [r.nombre for r in form.fields["rol"].queryset])
        self.client.post(
            reverse("cuentas:usuarios_crear"),
            {"nombre_completo": "Otro Pastor", "correo": "pastor2@ccmg.org", "username": "", "rol": self.rol["PASTOR"].pk},
        )
        self.assertEqual(Usuario.objects.get(correo="pastor2@ccmg.org").rol.nombre, "PASTOR")


class AuditoriaTests(BaseCasasVida):
    def test_solo_el_superadmin_ve_la_bitacora(self):
        for user in (self.pastor, self.supervisor, self.lider, self.coord):
            self.entrar(user)
            self.assertEqual(self.client.get(reverse("cuentas:auditoria")).status_code, 403, user.correo)
            self.assertNotIn("auditoria", [m["id"] for m in self.client.get(reverse("pva:casas")).context["menu"]] if user != self.coord else [])
        self.entrar(self.superadmin)
        self.assertEqual(self.client.get(reverse("cuentas:auditoria")).status_code, 200)
        self.assertIn("auditoria", [m["id"] for m in self.client.get(reverse("pva:casas")).context["menu"]])
        self.assertIn("auditoria", [m["id"] for m in self.client.get(reverse("formacion:procesos")).context["menu"]])

    def test_registra_inicio_de_sesion_y_cambios_de_usuarios(self):
        self.client.post(reverse("cuentas:login"), {"usuario": self.pastor.correo, "clave": CLAVE})
        self.assertTrue(Auditoria.objects.filter(accion="INICIAR_SESION", id_usuario=self.pastor).exists())
        self.client.post(
            reverse("cuentas:usuarios_crear"),
            {"nombre_completo": "Nueva", "correo": "nueva@ccmg.org", "username": "", "rol": self.rol["COORDINADOR_FORMACION"].pk},
        )
        nueva = Usuario.objects.get(correo="nueva@ccmg.org")
        self.assertTrue(Auditoria.objects.filter(accion="CREAR", entidad="usuario", id_entidad=nueva.pk).exists())

    def test_filtros_y_exportacion(self):
        Auditoria.objects.create(id_usuario=self.pastor, accion="CREAR", entidad="area", id_entidad=1)
        Auditoria.objects.create(id_usuario=self.lider, accion="REGISTRAR_ASISTENCIA", entidad="actividad", id_entidad=2)
        self.entrar(self.superadmin)
        url = reverse("cuentas:auditoria")
        self.assertEqual(
            [r.accion for r in self.client.get(url, {"usuario": self.lider.pk}).context["registros"]], ["REGISTRAR_ASISTENCIA"]
        )
        self.assertEqual([r.entidad for r in self.client.get(url, {"entidad": "area"}).context["registros"]], ["area"])
        for formato in ("pdf", "xlsx"):
            resp = self.client.get(url, {"formato": formato})
            self.assertEqual(resp.status_code, 200)
            self.assertIn(f".{formato}", resp["Content-Disposition"])


class ComandoSuperAdminTests(BaseCasasVida):
    def test_promover_cuenta_existente(self):
        salida = io.StringIO()
        call_command("crear_superadmin", promover="LIDER@ccmg.org", stdout=salida)
        self.lider.refresh_from_db()
        self.assertEqual(self.lider.rol.nombre, "SUPERADMIN")
        self.assertIn("Super Administrador", salida.getvalue())

    def test_promover_correo_inexistente(self):
        with self.assertRaises(CommandError):
            call_command("crear_superadmin", promover="nadie@ccmg.org")


class CrearUsuarioConErroresTests(BaseCasasVida):
    def test_correo_repetido_muestra_el_error(self):
        """Antes respondía 500 porque la vista no definía self.object."""
        self.entrar(self.pastor)
        resp = self.client.post(
            reverse("cuentas:usuarios_crear"),
            {"nombre_completo": "Repetido", "correo": self.lider.correo, "username": "", "rol": self.rol["LIDER_CASA_VIDA"].pk},
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIn("correo", resp.context["form"].errors)
