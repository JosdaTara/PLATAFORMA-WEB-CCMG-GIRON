from django.contrib.auth.backends import BaseBackend
from django.utils import timezone
from .models import Usuario


class CcmgAuthBackend(BaseBackend):
    """Autenticación por username O correo (RF01, RNF20)."""

    def authenticate(self, request, username=None, password=None, **kwargs):
        if not username or not password:
            return None

        # Normalizar: correo siempre en minúsculas
        ident = username.strip()
        if "@" in ident:
            ident = ident.lower()

        # Buscar por correo o username
        user = None
        try:
            if "@" in username.strip():
                user = Usuario.objects.get(correo__iexact=ident)
            else:
                user = Usuario.objects.get(username__iexact=ident)
        except Usuario.DoesNotExist:
            return None

        # Cuenta desactivada (RN24)
        if not user.activo:
            return None

        # Bloqueo (RNF20)
        if user.bloqueado_hasta and timezone.now() < user.bloqueado_hasta:
            return None

        if user.check_password(password):
            # Resetear intentos y bloqueo
            user.intentos_fallidos = 0
            user.bloqueado_hasta = None
            user.last_login = timezone.now()
            user.save(update_fields=["intentos_fallidos", "bloqueado_hasta", "last_login"])
            return user
        else:
            user.intentos_fallidos = (user.intentos_fallidos or 0) + 1
            if user.intentos_fallidos >= 5:
                user.bloqueado_hasta = timezone.now() + timezone.timedelta(minutes=15)
            user.save(update_fields=["intentos_fallidos", "bloqueado_hasta"])
            return None

    def get_user(self, user_id):
        try:
            return Usuario.objects.get(pk=user_id)
        except Usuario.DoesNotExist:
            return None
