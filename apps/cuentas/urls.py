from django.urls import path
from . import views

app_name = "cuentas"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("panel/", views.panel_por_rol, name="panel_por_rol"),
    path("selector-modulo/", views.selector_modulo, name="selector_modulo"),
]
