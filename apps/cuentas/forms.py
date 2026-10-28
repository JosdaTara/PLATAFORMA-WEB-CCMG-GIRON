from django import forms


class LoginForm(forms.Form):
    usuario = forms.CharField(label="Usuario o correo")
    clave = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
