from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .forms import CcmgPasswordResetForm, CcmgSetPasswordForm

app_name = "cuentas"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("panel/", views.panel_por_rol, name="panel_por_rol"),
    path("selector-modulo/", views.selector_modulo, name="selector_modulo"),
    path("cambiar-password/", views.CambiarPasswordView.as_view(), name="cambiar_password"),
    path(
        "recuperar/",
        auth_views.PasswordResetView.as_view(
            template_name="cuentas/password_reset_form.html",
            form_class=CcmgPasswordResetForm,
            email_template_name="cuentas/password_reset_email.html",
            subject_template_name="cuentas/password_reset_subject.txt",
            success_url="/cuentas/recuperar/enviado/",
        ),
        name="password_reset",
    ),
    path(
        "recuperar/enviado/",
        auth_views.PasswordResetDoneView.as_view(template_name="cuentas/password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "recuperar/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="cuentas/password_reset_confirm.html", form_class=CcmgSetPasswordForm
        ),
        name="password_reset_confirm",
    ),
    path(
        "recuperar/completado/",
        auth_views.PasswordResetCompleteView.as_view(template_name="cuentas/password_reset_complete.html"),
        name="password_reset_complete",
    ),
    path("usuarios/", views.UsuarioListView.as_view(), name="usuarios_list"),
    path("usuarios/crear/", views.UsuarioCreateView.as_view(), name="usuarios_crear"),
    path("usuarios/<int:pk>/editar/", views.UsuarioUpdateView.as_view(), name="usuarios_editar"),
    path("usuarios/<int:pk>/desactivar/", views.UsuarioDesactivarView.as_view(), name="usuarios_desactivar"),
    path("usuarios/<int:pk>/reactivar/", views.UsuarioReactivarView.as_view(), name="usuarios_reactivar"),
]
