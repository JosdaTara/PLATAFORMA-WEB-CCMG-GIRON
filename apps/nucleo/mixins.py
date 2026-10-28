"""Mixins de permisos para vistas basadas en clases (RF04, RN01, RN03, RN04, RN05, RN20)."""
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse


class RoleRequiredMixin(LoginRequiredMixin):
    allowed_roles = []

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        rol = getattr(getattr(request.user, "rol", None), "nombre", None)
        if rol not in self.allowed_roles:
            raise PermissionDenied("No tienes permiso para acceder a esta vista.")
        return super().dispatch(request, *args, **kwargs)


class PastorRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        rol = getattr(getattr(request.user, "rol", None), "nombre", None)
        if rol != "PASTOR":
            raise PermissionDenied("Solo el Pastor puede realizar esta acción.")
        return super().dispatch(request, *args, **kwargs)


class ModuleRequiredMixin(LoginRequiredMixin):
    required_module = None  # 'CASAS_VIDA' o 'ESCUELAS_FORMACION'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        rol = getattr(request.user, "rol", None)
        if self.required_module == "CASAS_VIDA" and not getattr(rol, "acceso_casas_vida", False):
            raise PermissionDenied("No tienes acceso al módulo Casas de Vida.")
        if self.required_module == "ESCUELAS_FORMACION" and not getattr(rol, "acceso_escuelas_formacion", False):
            raise PermissionDenied("No tienes acceso al módulo Escuelas de Formación.")
        return super().dispatch(request, *args, **kwargs)


class CasaVidaScopeMixin:
    """Filtra queryset por Casa de Vida asignada al usuario.

    Fuente de verdad para Supervisor: area.id_supervisor.
    Para Líder: casa_vida.id_lider.
    Para apoyo: pendiente de tabla casa_vida_equipo (ver SQL propuesto).
    """

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        rol = getattr(user, "rol", None)
        codigo = getattr(rol, "nombre", None) if rol else None

        if codigo == "PASTOR":
            return qs

        if codigo == "SUPERVISOR_AREA":
            # área del supervisor (fuente de verdad: area.id_supervisor)
            from pva.models import Area  # se importa aquí para evitar circular
            areas = Area.objects.filter(id_supervisor=user)
            return qs.filter(id_area__in=areas)

        if codigo == "LIDER_CASA_VIDA":
            from pva.models import CasaVida
            casas = CasaVida.objects.filter(id_lider=user)
            return qs.filter(id_casa_vida__in=casas)

        # APOYO_CASA_VIDA: pendiente de tabla casa_vida_equipo
        return qs.none()
