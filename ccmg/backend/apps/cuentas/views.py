import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView, PasswordResetConfirmView
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, CreateView, UpdateView, View
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
import secrets
import string

from nucleo import exportar
from nucleo.exportar import ExportableMixin
from nucleo.mixins import PastorRequiredMixin, SuperAdminRequiredMixin
from nucleo.models import Auditoria
from nucleo.permissions import pastor_required
from nucleo.utils import ROLES_PASTOR, ROLES_SUPERADMIN, es_superadmin, registrar_auditoria, rol_efectivo, sesion_js

from .correos import enviar_aviso_cambio
from .forms import CcmgPasswordChangeForm, CcmgSetPasswordForm, LoginForm, UsuarioForm, UsuarioAsignacionForm
from .models import Usuario, Rol
from pva.models import Area, CasaVida, CasaVidaEquipo


class CambiarPasswordView(PasswordChangeView):
    template_name = "cuentas/cambiar_password.html"
    form_class = CcmgPasswordChangeForm
    success_url = reverse_lazy("cuentas:panel_por_rol")

    def form_valid(self, form):
        response = super().form_valid(form)
        update_session_auth_hash(self.request, form.user)
        if getattr(self.request.user, "debe_cambiar_password", False):
            self.request.user.debe_cambiar_password = False
            self.request.user.save(update_fields=["debe_cambiar_password"])
        registrar_auditoria(self.request, "CAMBIAR_CONTRASENA", form.user)
        enviar_aviso_cambio(self.request, form.user)
        return response


class RestablecerPasswordView(PasswordResetConfirmView):
    """Página a la que lleva el enlace del correo: crea la contraseña nueva y avisa por correo."""
    template_name = "cuentas/password_reset_confirm.html"
    form_class = CcmgSetPasswordForm
    success_url = reverse_lazy("cuentas:password_reset_complete")  # Django lo busca sin el espacio «cuentas:»

    def form_valid(self, form):
        response = super().form_valid(form)
        # Quien restablece no ha iniciado sesión: la bitácora se atribuye al dueño de la cuenta.
        Auditoria.objects.create(
            id_usuario=form.user, accion="RESTABLECER_CONTRASENA", entidad=form.user._meta.db_table,
            id_entidad=form.user.pk, ip=(self.request.META.get("REMOTE_ADDR") or "")[:45] or None,
        )
        if getattr(form.user, "debe_cambiar_password", False):
            form.user.debe_cambiar_password = False
            form.user.save(update_fields=["debe_cambiar_password"])
        enviar_aviso_cambio(self.request, form.user)
        return response


def login_view(request):
    if request.user.is_authenticated:
        return redirect("cuentas:panel_por_rol")
    error = None
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            u = form.cleaned_data["usuario"]
            c = form.cleaned_data["clave"]
            from django.contrib.auth import authenticate

            user = authenticate(request, username=u, password=c)
            if user is not None:
                login(request, user)
                registrar_auditoria(request, "INICIAR_SESION", user)
                return redirect("cuentas:panel_por_rol")
            error = "Usuario o contraseña incorrectos."
    else:
        form = LoginForm()
    return render(request, "cuentas/login.html", {"form": form, "error": error})


def logout_view(request):
    logout(request)
    return redirect("cuentas:login")


@login_required
def panel_por_rol(request):
    user = request.user
    rol = getattr(user, "rol", None)
    if rol_efectivo(user) == "PASTOR":
        return redirect("cuentas:selector_modulo")
    if getattr(rol, "acceso_casas_vida", False):
        return redirect("pva:panel")
    if getattr(rol, "acceso_escuelas_formacion", False):
        return redirect("formacion:panel")
    return redirect("publico:index")


@pastor_required
def selector_modulo(request):
    return render(
        request,
        "cuentas/selector_modulo.html",
        {"user": request.user, "sesion_js": sesion_js(request.user)},
    )


class AdminUsuariosMixin:
    """Barra lateral y datos comunes de la gestión de usuarios (RF03)."""

    def get_context_data(self, **kwargs):
        from pva.views import ROLES_NOMBRE, menu_casas

        ctx = super().get_context_data(**kwargs)
        ctx["menu"] = menu_casas(self.request.user, getattr(self, "seccion", "usuarios"))
        ctx["rol_nombre"] = ROLES_NOMBRE.get(self.request.user.rol.nombre, "")
        ctx["es_pastor"] = True
        # Para mostrar solo los campos de asignación que aplican al rol elegido.
        ctx["roles_codigos"] = dict(Rol.objects.values_list("id_rol", "nombre"))
        return ctx


def usuarios_gestionables(editor):
    """Usuarios que el editor puede ver y modificar.

    Solo el Super Administrador gestiona a los Super Administradores y a los Administradores (Pastor).
    El Pastor no ve a ninguno de ellos, salvo a sí mismo.
    """
    qs = Usuario.objects.all()
    if not es_superadmin(editor):
        qs = qs.exclude(rol__nombre=ROLES_SUPERADMIN).exclude(
            Q(rol__nombre=ROLES_PASTOR) & ~Q(pk=getattr(editor, "pk", None))
        )
    return qs


def asignacion_actual(user):
    """Valores iniciales del formulario de asignación según lo que el usuario tiene hoy."""
    inicial = {}
    area = Area.objects.filter(id_supervisor=user).first()
    if area:
        inicial["area"] = area.pk
    casa = CasaVida.objects.filter(id_lider=user).order_by("-estado").first()
    if casa:
        inicial["casa_vida"] = casa.pk
    equipo = CasaVidaEquipo.objects.filter(id_usuario=user, activo=True).first()
    if equipo:
        inicial.update(casa_vida=equipo.id_casa_vida_id, funcion_apoyo=equipo.funcion)
    return inicial


class UsuarioListView(AdminUsuariosMixin, PastorRequiredMixin, ListView):
    model = Usuario
    template_name = "cuentas/usuarios/lista.html"
    context_object_name = "usuarios"

    def get_queryset(self):
        return usuarios_gestionables(self.request.user).select_related("rol").order_by("-activo", "rol__id_rol", "nombre_completo")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # La contraseña temporal se muestra una sola vez, justo después de crear el usuario.
        ctx["password_generada"] = self.request.session.pop("password_generada", None)
        ctx["usuario_creado"] = self.request.session.pop("usuario_creado", None)
        return ctx


class UsuarioCreateView(AdminUsuariosMixin, PastorRequiredMixin, CreateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = "cuentas/usuarios/formulario.html"
    success_url = reverse_lazy("cuentas:usuarios_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["editor"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["form_asig"] = UsuarioAsignacionForm(self.request.POST or None)
        ctx["titulo"] = "Crear usuario"
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = None  # CreateView lo necesita para volver a mostrar el formulario con errores
        form = UsuarioForm(request.POST, editor=request.user)
        form_asig = UsuarioAsignacionForm(request.POST)
        if form.is_valid() and form_asig.is_valid():
            try:
                with transaction.atomic():
                    user = form.save(commit=False)
                    user.creado_por = request.user
                    user.activo = True
                    user.debe_cambiar_password = True
                    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
                    pwd = "".join(secrets.choice(alphabet) for _ in range(20))
                    user.set_password(pwd)
                    user.save()

                    rol = user.rol
                    codigo = getattr(rol, "nombre", None)

                    if codigo == "SUPERVISOR_AREA":
                        area = form_asig.cleaned_data.get("area")
                        if not area:
                            messages.error(request, "Debe seleccionar un Área para el Supervisor de Área.")
                            raise Exception("area_required")
                        supervisor_existente = Usuario.objects.filter(rol__nombre="SUPERVISOR_AREA", area_set=area).exclude(pk=user.pk).exists() if False else None
                        # Check: un supervisor solo puede tener UNA área
                        otras_areas = Area.objects.filter(id_supervisor=user).exclude(pk=area.pk)
                        if otras_areas.exists():
                            messages.error(request, "Este Supervisor ya tiene otra Área asignada. Debe reasignarla primero.")
                            raise Exception("supervisor_otras_areas")
                        if area.id_supervisor and area.id_supervisor_id != user.pk:
                            messages.error(request, "El Área ya tiene otro Supervisor. Confirme el reemplazo antes de continuar.")
                            raise Exception("area_tiene_supervisor")
                        area.id_supervisor = user
                        area.save(update_fields=["id_supervisor"])

                    elif codigo == "LIDER_CASA_VIDA":
                        casa = form_asig.cleaned_data.get("casa_vida")
                        if not casa:
                            messages.error(request, "Debe seleccionar una Casa de Vida para el Líder.")
                            raise Exception("casa_required")
                        if casa.id_lider and casa.id_lider_id != user.pk:
                            messages.error(request, "La Casa de Vida ya tiene otro Líder. Confirme el reemplazo antes de continuar.")
                            raise Exception("casa_tiene_lider")
                        casa.id_lider = user
                        casa.save(update_fields=["id_lider"])

                    elif codigo == "APOYO_CASA_VIDA":
                        casa = form_asig.cleaned_data.get("casa_vida")
                        funcion = form_asig.cleaned_data.get("funcion_apoyo")
                        if not casa or not funcion:
                            messages.error(request, "Debe seleccionar Casa de Vida y función para el usuario de apoyo.")
                            raise Exception("apoyo_required")
                        CasaVidaEquipo.objects.filter(id_usuario=user, activo=True).update(activo=False)
                        CasaVidaEquipo.objects.create(id_casa_vida=casa, id_usuario=user, funcion=funcion, activo=True)

                    request.session["password_generada"] = pwd
                    request.session["usuario_creado"] = user.correo
                    registrar_auditoria(request, "CREAR", user)
                    messages.success(request, "Usuario creado correctamente.")
                    return redirect(self.success_url)
            except Exception as e:
                # transaction.atomic will rollback
                pass

        return self.render_to_response(self.get_context_data(form=form))


class UsuarioUpdateView(AdminUsuariosMixin, PastorRequiredMixin, UpdateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = "cuentas/usuarios/formulario.html"
    success_url = reverse_lazy("cuentas:usuarios_list")

    def get_queryset(self):
        return usuarios_gestionables(self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["editor"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["form_asig"] = UsuarioAsignacionForm(self.request.POST or None, initial=asignacion_actual(self.object))
        ctx["titulo"] = "Editar usuario"
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = UsuarioForm(request.POST, instance=self.object, editor=request.user)
        form_asig = UsuarioAsignacionForm(request.POST)
        if form.is_valid() and form_asig.is_valid():
            try:
                with transaction.atomic():
                    old_rol = self.object.rol
                    user = form.save(commit=False)
                    user.modificado_por = request.user
                    user.save()

                    rol = user.rol
                    codigo = getattr(rol, "nombre", None)
                    old_codigo = getattr(old_rol, "nombre", None)

                    # Desactivar asignaciones si cambia de rol
                    if codigo != old_codigo:
                        if old_codigo == "SUPERVISOR_AREA":
                            for a in Area.objects.filter(id_supervisor=user):
                                a.id_supervisor = None
                                a.save(update_fields=["id_supervisor"])
                        elif old_codigo == "LIDER_CASA_VIDA":
                            for c in CasaVida.objects.filter(id_lider=user):
                                c.id_lider = None
                                c.save(update_fields=["id_lider"])
                        elif old_codigo == "APOYO_CASA_VIDA":
                            CasaVidaEquipo.objects.filter(id_usuario=user, activo=True).update(activo=False)

                    if codigo == "SUPERVISOR_AREA":
                        area = form_asig.cleaned_data.get("area")
                        if not area:
                            messages.error(request, "Debe seleccionar un Área para el Supervisor de Área.")
                            raise Exception("area_required")
                        otras_areas = Area.objects.filter(id_supervisor=user).exclude(pk=area.pk)
                        if otras_areas.exists():
                            messages.error(request, "Este Supervisor ya tiene otra Área asignada. Debe reasignarla primero.")
                            raise Exception("supervisor_otras_areas")
                        if area.id_supervisor and area.id_supervisor_id != user.pk:
                            messages.error(request, "El Área ya tiene otro Supervisor. Confirme el reemplazo antes de continuar.")
                            raise Exception("area_tiene_supervisor")
                        area.id_supervisor = user
                        area.save(update_fields=["id_supervisor"])

                    elif codigo == "LIDER_CASA_VIDA":
                        casa = form_asig.cleaned_data.get("casa_vida")
                        if not casa:
                            messages.error(request, "Debe seleccionar una Casa de Vida para el Líder.")
                            raise Exception("casa_required")
                        if casa.id_lider and casa.id_lider_id != user.pk:
                            messages.error(request, "La Casa de Vida ya tiene otro Líder. Confirme el reemplazo antes de continuar.")
                            raise Exception("casa_tiene_lider")
                        casa.id_lider = user
                        casa.save(update_fields=["id_lider"])

                    elif codigo == "APOYO_CASA_VIDA":
                        casa = form_asig.cleaned_data.get("casa_vida")
                        funcion = form_asig.cleaned_data.get("funcion_apoyo")
                        if not casa or not funcion:
                            messages.error(request, "Debe seleccionar Casa de Vida y función para el usuario de apoyo.")
                            raise Exception("apoyo_required")
                        CasaVidaEquipo.objects.filter(id_usuario=user, activo=True).update(activo=False)
                        CasaVidaEquipo.objects.create(id_casa_vida=casa, id_usuario=user, funcion=funcion, activo=True)

                    registrar_auditoria(request, "ACTUALIZAR", user)
                    messages.success(request, "Usuario actualizado correctamente.")
                    return redirect(self.success_url)
            except Exception:
                pass

        return self.render_to_response(self.get_context_data(form=form))


class UsuarioDesactivarView(PastorRequiredMixin, View):
    def post(self, request, pk):
        user = get_object_or_404(usuarios_gestionables(request.user), pk=pk)
        if user == request.user:
            messages.error(request, "No puedes desactivarte a ti mismo.")
            return redirect("cuentas:usuarios_list")
        if getattr(user.rol, "nombre", None) == ROLES_SUPERADMIN:
            if Usuario.objects.filter(rol__nombre=ROLES_SUPERADMIN, activo=True).count() <= 1:
                messages.error(request, "No puedes dejar el sistema sin ningún Super Administrador activo.")
                return redirect("cuentas:usuarios_list")
        if getattr(user.rol, "nombre", None) == "PASTOR":
            activos = Usuario.objects.filter(rol__nombre="PASTOR", activo=True).count()
            if activos <= 1:
                messages.error(request, "No puedes dejar el sistema sin ningún Pastor activo.")
                return redirect("cuentas:usuarios_list")
        user.activo = False
        user.modificado_por = request.user
        user.save(update_fields=["activo", "modificado_por"])
        # Desasignar para evitar referencias a usuario inactivo
        for a in Area.objects.filter(id_supervisor=user):
            a.id_supervisor = None
            a.save(update_fields=["id_supervisor"])
        for c in CasaVida.objects.filter(id_lider=user):
            c.id_lider = None
            c.save(update_fields=["id_lider"])
        CasaVidaEquipo.objects.filter(id_usuario=user, activo=True).update(activo=False)
        # Invalidar sesión activa
        from django.contrib.sessions.models import Session
        from django.utils import timezone
        for s in Session.objects.all():
            data = s.get_decoded()
            if data.get("_auth_user_id") == str(user.pk):
                s.delete()
        registrar_auditoria(request, "DESACTIVAR", user)
        messages.success(request, "Usuario desactivado correctamente.")
        return redirect("cuentas:usuarios_list")


class UsuarioReactivarView(PastorRequiredMixin, View):
    def post(self, request, pk):
        user = get_object_or_404(usuarios_gestionables(request.user), pk=pk)
        user.activo = True
        user.modificado_por = request.user
        user.save(update_fields=["activo", "modificado_por"])
        registrar_auditoria(request, "REACTIVAR", user)
        messages.success(request, "Usuario reactivado correctamente.")
        return redirect("cuentas:usuarios_list")


# ----------------------------------------------------------------- Bitácora de auditoría

ENTIDADES_AUDITORIA = {
    "usuario": "Usuario",
    "area": "Área",
    "casa_vida": "Casa de Vida",
    "participante": "Participante",
    "actividad": "Actividad y asistencia",
    "seguimiento": "Seguimiento",
    "reporte": "Reporte",
    "ofrenda": "Ofrenda",
    "proceso_formacion": "Proceso de formación",
    "inscripcion_formacion": "Inscripción de formación",
}


class AuditoriaListView(AdminUsuariosMixin, SuperAdminRequiredMixin, ExportableMixin, ListView):
    """Quién hizo qué y cuándo en la plataforma (RNF18). Solo para el Super Administrador."""

    template_name = "cuentas/auditoria.html"
    context_object_name = "registros"
    seccion = "auditoria"
    paginate_by = 50

    def get_queryset(self):
        qs = Auditoria.objects.select_related("id_usuario", "id_usuario__rol")
        g = self.request.GET
        if g.get("usuario", "").isdigit():
            qs = qs.filter(id_usuario=g["usuario"])
        if g.get("accion"):
            qs = qs.filter(accion=g["accion"])
        if g.get("entidad"):
            qs = qs.filter(entidad=g["entidad"])
        for campo, lookup in (("desde", "fecha__date__gte"), ("hasta", "fecha__date__lte")):
            try:
                qs = qs.filter(**{lookup: datetime.date.fromisoformat(g.get(campo, ""))})
            except ValueError:
                pass
        return qs.order_by("-fecha", "-id_auditoria")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["usuarios_filtro"] = Usuario.objects.filter(
            pk__in=Auditoria.objects.values("id_usuario")
        ).order_by("nombre_completo")
        ctx["acciones"] = Auditoria.objects.order_by("accion").values_list("accion", flat=True).distinct()
        ctx["entidades"] = ENTIDADES_AUDITORIA
        ctx["filtros"] = self.request.GET
        params = self.request.GET.copy()
        params.pop("page", None)
        params.pop("formato", None)
        ctx["query_sin_pagina"] = params.urlencode()
        return ctx

    def documento_exportable(self, ctx):
        g = self.request.GET
        desde, hasta = g.get("desde") or "el inicio", g.get("hasta") or "hoy"
        return exportar.Documento(
            titulo="Bitácora de auditoría",
            periodo=f"Desde {desde} hasta {hasta}",
            datos=[("Acción", g.get("accion") or "Todas"),
                   ("Entidad", ENTIDADES_AUDITORIA.get(g.get("entidad"), "Todas")),
                   ("Registros", self.object_list.count())],
            tablas=[exportar.Tabla(
                "Registros",
                [("Fecha", exportar.TEXTO), ("Usuario", exportar.TEXTO), ("Acción", exportar.TEXTO),
                 ("Entidad", exportar.TEXTO), ("Id", exportar.ENTERO), ("IP", exportar.TEXTO)],
                [[r.fecha, r.id_usuario.nombre_completo if r.id_usuario_id else "—", r.accion,
                  ENTIDADES_AUDITORIA.get(r.entidad, r.entidad), r.id_entidad, r.ip or ""]
                 for r in self.object_list[:5000]],
            )],
            nombre_archivo="bitacora_auditoria",
        )
