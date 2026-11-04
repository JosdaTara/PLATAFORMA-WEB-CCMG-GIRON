"""Correos de la cuenta con la identidad de la iglesia (RF25).

Cada correo sale en dos versiones, HTML y texto plano, para los clientes que no muestran HTML.
El logo va incrustado en el mensaje (Content-ID), así se ve aunque el servidor de la plataforma
no sea accesible desde internet.
"""
import logging
from email.mime.image import MIMEImage

from django.conf import settings
from django.contrib.staticfiles import finders
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone

logger = logging.getLogger(__name__)

LOGO_CID = "logo-ccmg"


def _logo():
    ruta = finders.find("img/logo-blanco.png")
    if not ruta:
        return None
    with open(ruta, "rb") as archivo:
        imagen = MIMEImage(archivo.read(), "png")
    imagen.add_header("Content-ID", f"<{LOGO_CID}>")
    imagen.add_header("Content-Disposition", "inline", filename="logo-ccmg.png")
    return imagen


def enviar(asunto, plantilla, contexto, destinatario):
    """Envía `plantilla`.txt y `plantilla`.html a `destinatario`. Devuelve True si se envió."""
    contexto = {**contexto, "anio": timezone.localdate().year, "logo_cid": LOGO_CID}
    mensaje = EmailMultiAlternatives(
        asunto, render_to_string(f"{plantilla}.txt", contexto), settings.DEFAULT_FROM_EMAIL, [destinatario]
    )
    mensaje.attach_alternative(render_to_string(f"{plantilla}.html", contexto), "text/html")
    logo = _logo()
    if logo:
        mensaje.mixed_subtype = "related"
        mensaje.attach(logo)
    try:
        mensaje.send()
    except Exception:  # SMTP caído o credenciales erradas: se registra sin revelar nada al visitante
        logger.exception("No se pudo enviar el correo «%s» a %s", asunto, destinatario)
        return False
    return True


def url_absoluta(request_o_contexto, ruta):
    """Arma la URL completa con el protocolo y dominio por los que llegó la solicitud."""
    if isinstance(request_o_contexto, dict):
        return f"{request_o_contexto['protocol']}://{request_o_contexto['domain']}{ruta}"
    return request_o_contexto.build_absolute_uri(ruta)


def enviar_recuperacion(contexto_django):
    """Correo con el enlace para crear una contraseña nueva (contexto de PasswordResetForm)."""
    usuario = contexto_django["user"]
    ruta = reverse(
        "cuentas:password_reset_confirm",
        kwargs={"uidb64": contexto_django["uid"], "token": contexto_django["token"]},
    )
    return enviar(
        "Restablece tu contraseña · CCMG Girón",
        "cuentas/correos/recuperar",
        {
            "nombre": usuario.nombre_completo,
            "correo": usuario.correo,
            "enlace": url_absoluta(contexto_django, ruta),
            "minutos": settings.PASSWORD_RESET_TIMEOUT // 60,
            "login": url_absoluta(contexto_django, reverse("cuentas:login")),
        },
        usuario.correo,
    )


def enviar_aviso_cambio(request, usuario):
    """Aviso de seguridad: la contraseña de la cuenta acaba de cambiar."""
    return enviar(
        "Tu contraseña fue cambiada · CCMG Girón",
        "cuentas/correos/contrasena_cambiada",
        {
            "nombre": usuario.nombre_completo,
            "correo": usuario.correo,
            "fecha": timezone.localtime(),
            "login": url_absoluta(request, reverse("cuentas:login")),
            "recuperar": url_absoluta(request, reverse("cuentas:password_reset")),
        },
        usuario.correo,
    )
