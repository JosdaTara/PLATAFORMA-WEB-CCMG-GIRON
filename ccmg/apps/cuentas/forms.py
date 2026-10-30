from django import forms
from django.contrib.auth.forms import PasswordResetForm as DjangoPasswordResetForm

from .models import Usuario, Rol
from pva.models import Area, CasaVida


class LoginForm(forms.Form):
    usuario = forms.CharField(label="Usuario o correo")
    clave = forms.CharField(label="Contraseña", widget=forms.PasswordInput)


class CcmgPasswordResetForm(DjangoPasswordResetForm):
    """PasswordResetForm adaptado a nuestro modelo (campo 'activo' en vez de 'is_active')."""

    def get_users(self, email):
        email_field_name = Usuario.EMAIL_FIELD
        active_users = Usuario._default_manager.filter(
            **{f"{email_field_name}__iexact": email, "activo": True}
        )
        return (
            u for u in active_users
            if u.has_usable_password()
            and getattr(u, "email", None)
        )


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ["nombre_completo", "correo", "username", "rol", "responsable_ofrendas"]
        labels = {"responsable_ofrendas": "Autorizado como responsable de ofrendas"}
        help_texts = {
            "responsable_ofrendas": "Puede registrar y consultar ofrendas (RN14). El Pastor siempre tiene este acceso.",
        }

    def clean_correo(self):
        correo = self.cleaned_data.get("correo", "")
        correo = correo.strip().lower()
        qs = Usuario.objects.filter(correo__iexact=correo)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Ya existe un usuario con ese correo.")
        return correo

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not username:
            return None
        username = username.strip()
        qs = Usuario.objects.filter(username__iexact=username)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Ya existe un usuario con ese nombre de usuario.")
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        if user.correo:
            user.correo = user.correo.strip().lower()
        if user.username:
            user.username = user.username.strip()
        if commit:
            user.save()
        return user


class UsuarioAsignacionForm(forms.Form):
    area = forms.ModelChoiceField(queryset=Area.objects.all(), required=False)
    casa_vida = forms.ModelChoiceField(queryset=CasaVida.objects.all(), required=False)
    funcion_apoyo = forms.ChoiceField(
        choices=[("", "---------"), ("APRENDIZ", "Aprendiz"), ("ANFITRION", "Anfitrión"), ("MAESTRO_NINOS", "Maestro de Niños")],
        required=False,
    )
