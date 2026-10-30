from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, CreateView, UpdateView, View
from django.contrib import messages
from django.db import transaction
import secrets
import string

from nucleo.mixins import PastorRequiredMixin
from nucleo.permissions import pastor_required
from nucleo.utils import sesion_js

from .forms import LoginForm, UsuarioForm, UsuarioAsignacionForm
from .models import Usuario, Rol
from pva.models import Area, CasaVida, CasaVidaEquipo


class CambiarPasswordView(PasswordChangeView):
    template_name = "cuentas/cambiar_password.html"
    success_url = reverse_lazy("cuentas:panel_por_rol")

    def form_valid(self, form):
        response = super().form_valid(form)
        update_session_auth_hash(self.request, form.user)
        if getattr(self.request.user, "debe_cambiar_password", False):
            self.request.user.debe_cambiar_password = False
            self.request.user.save(update_fields=["debe_cambiar_password"])
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
                return redirect("cuentas:panel_por_rol")
            error = "Usuario o contraseña incorrectos."
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form, "error": error})


def logout_view(request):
    logout(request)
    return redirect("cuentas:login")


@login_required
def panel_por_rol(request):
    user = request.user
    rol = getattr(user, "rol", None)
    codigo = getattr(rol, "nombre", None)
    if codigo == "PASTOR":
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
        "selector-modulo.html",
        {"user": request.user, "sesion_js": sesion_js(request.user)},
    )


def panel_casas_view(request):
    return render(request, "panel.html", {"user": request.user})


def panel_escuelas_view(request):
    return render(request, "panel.html", {"user": request.user})


class UsuarioListView(PastorRequiredMixin, ListView):
    model = Usuario
    template_name = "usuarios/lista.html"
    context_object_name = "usuarios"

    def get_queryset(self):
        return Usuario.objects.all().select_related("rol")


class UsuarioCreateView(PastorRequiredMixin, CreateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = "usuarios/formulario.html"
    success_url = reverse_lazy("cuentas:usuarios_list")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["form_asig"] = UsuarioAsignacionForm(self.request.POST or None)
        ctx["titulo"] = "Crear usuario"
        ctx["password_generada"] = self.request.session.pop("password_generada", None)
        return ctx

    def post(self, request, *args, **kwargs):
        form = UsuarioForm(request.POST)
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
                    messages.success(request, "Usuario creado correctamente.")
                    return redirect(self.success_url)
            except Exception as e:
                # transaction.atomic will rollback
                pass

        return self.render_to_response(self.get_context_data(form=form))


class UsuarioUpdateView(PastorRequiredMixin, UpdateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = "usuarios/formulario.html"
    success_url = reverse_lazy("cuentas:usuarios_list")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["form_asig"] = UsuarioAsignacionForm(self.request.POST or None)
        ctx["titulo"] = "Editar usuario"
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = UsuarioForm(request.POST, instance=self.object)
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

                    messages.success(request, "Usuario actualizado correctamente.")
                    return redirect(self.success_url)
            except Exception:
                pass

        return self.render_to_response(self.get_context_data(form=form))


class UsuarioDesactivarView(PastorRequiredMixin, View):
    def post(self, request, pk):
        user = get_object_or_404(Usuario, pk=pk)
        if user == request.user:
            messages.error(request, "No puedes desactivarte a ti mismo.")
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
        messages.success(request, "Usuario desactivado correctamente.")
        return redirect("cuentas:usuarios_list")


class UsuarioReactivarView(PastorRequiredMixin, View):
    def post(self, request, pk):
        user = get_object_or_404(Usuario, pk=pk)
        user.activo = True
        user.modificado_por = request.user
        user.save(update_fields=["activo", "modificado_por"])
        messages.success(request, "Usuario reactivado correctamente.")
        return redirect("cuentas:usuarios_list")
