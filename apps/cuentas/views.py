from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.urls import reverse
from django.utils import timezone

from .forms import LoginForm
from .models import Usuario


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
    return render(request, "cuentas/login.html", {"form": form, "error": error})


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
    return redirect("cuentas:login")


@login_required
def selector_modulo(request):
    return render(request, "cuentas/selector_modulo.html", {"user": request.user})


def panel_casas_view(request):
    return render(request, "pva/panel.html", {"user": request.user})


def panel_escuelas_view(request):
    return render(request, "formacion/panel.html", {"user": request.user})
