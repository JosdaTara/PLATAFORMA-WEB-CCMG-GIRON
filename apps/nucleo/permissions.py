"""Capa central de permisos por rol y módulo (RF04, RN01, RN03, RN04, RN05, RN20)."""
from functools import wraps
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse


def _rol_codigo(request):
    user = getattr(request, "user", None)
    if not user or not user.is_authenticated:
        return None
    rol = getattr(user, "rol", None)
    if rol is None:
        return None
    return getattr(rol, "nombre", None)


def _acceso_casas_vida(request):
    user = getattr(request, "user", None)
    if not user or not user.is_authenticated:
        return False
    rol = getattr(user, "rol", None)
    return bool(rol and getattr(rol, "acceso_casas_vida", False))


def _acceso_escuelas(request):
    user = getattr(request, "user", None)
    if not user or not user.is_authenticated:
        return False
    rol = getattr(user, "rol", None)
    return bool(rol and getattr(rol, "acceso_escuelas_formacion", False))


def es_pastor(request):
    return _rol_codigo(request) == "PASTOR"


def role_required(*roles):
    """Decorador para vistas funcionales: exige rol exacto."""
    def decorator(view):
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect(reverse("cuentas:login"))
            if _rol_codigo(request) not in roles:
                raise PermissionDenied("No tienes permiso para esta acción.")
            return view(request, *args, **kwargs)
        return wrapper
    return decorator


def module_required(modulo):
    """modulo: 'CASAS_VIDA' o 'ESCUELAS_FORMACION'."""
    def decorator(view):
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect(reverse("cuentas:login"))
            if modulo == "CASAS_VIDA" and not _acceso_casas_vida(request):
                raise PermissionDenied("No tienes acceso al módulo Casas de Vida.")
            if modulo == "ESCUELAS_FORMACION" and not _acceso_escuelas(request):
                raise PermissionDenied("No tienes acceso al módulo Escuelas de Formación.")
            return view(request, *args, **kwargs)
        return wrapper
    return decorator


def pastor_required(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse("cuentas:login"))
        if not es_pastor(request):
            raise PermissionDenied("Solo el Pastor puede realizar esta acción.")
        return view(request, *args, **kwargs)
    return wrapper
