from django.urls import path, include
from django.shortcuts import redirect


def redirect_to_login(request):
    return redirect("cuentas:login")


def redirect_to_index(request):
    return redirect("publico:index")


def redirect_to_selector(request):
    return redirect("cuentas:selector_modulo")


def redirect_to_panel(request):
    return redirect("cuentas:panel_por_rol")


def redirect_to_panel_casas(request):
    return redirect("pva:panel")


def redirect_to_panel_formacion(request):
    return redirect("formacion:panel")


urlpatterns = [
    path("", include("publico.urls")),
    path("cuentas/", include("cuentas.urls")),
    path("pva/", include("pva.urls")),
    path("formacion/", include("formacion.urls")),
    path("ofrendas/", include("ofrendas.urls")),
    path("cuentas/login.html", redirect_to_login),
    path("cuentas/selector-modulo/login.html", redirect_to_login),
    path("cuentas/selector-modulo/index.html", redirect_to_index),
    path("cuentas/selector-modulo/selector-modulo.html", redirect_to_selector),
    path("cuentas/selector-modulo/panel.html", redirect_to_panel),
    path("cuentas/selector-modulo/panel-casas-vida.html", redirect_to_panel_casas),
    path("cuentas/selector-modulo/panel-escuelas-formacion.html", redirect_to_panel_formacion),
]
