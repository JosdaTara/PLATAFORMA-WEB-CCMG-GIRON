"""Alcance de la información del módulo Casas de Vida según el rol (RN03, RN04, RN05, RN18).

Toda consulta de Casas de Vida, participantes o asistencia debe pasar por estas
funciones para que cada rol vea únicamente lo que le corresponde.
"""
from nucleo.utils import ROLES_APOYO, ROLES_LIDER, ROLES_PASTOR, ROLES_SUPERVISOR

from .models import ACTIVO, Actividad, CasaVida, CasaVidaEquipo, Participante


def rol_de(user):
    return getattr(getattr(user, "rol", None), "nombre", None)


def es_pastor(user):
    return rol_de(user) == ROLES_PASTOR


def casas_visibles(user):
    """Casas de Vida que el usuario puede consultar."""
    rol = rol_de(user)
    qs = CasaVida.objects.select_related("id_area", "id_lider", "id_supervisor")
    if rol == ROLES_PASTOR:
        return qs
    if rol == ROLES_SUPERVISOR:
        # Fuente de verdad: area.id_supervisor (un Supervisor tiene una sola Área).
        return qs.filter(id_area__id_supervisor=user)
    if rol == ROLES_LIDER:
        return qs.filter(id_lider=user)
    if rol == ROLES_APOYO:
        casas = CasaVidaEquipo.objects.filter(id_usuario=user, activo=True).values("id_casa_vida")
        return qs.filter(id_casa_vida__in=casas)
    return qs.none()


def casa_para_reportar(user):
    """Casa de Vida activa en la que el Líder o el usuario de apoyo registra asistencia (RF09)."""
    if rol_de(user) not in (ROLES_LIDER, ROLES_APOYO):
        return None
    return casas_visibles(user).filter(estado=ACTIVO).first()


def participantes_visibles(user):
    """Participantes que el usuario puede consultar (RF06).

    El Pastor ve todos, incluidos los inactivos y los que aún no tienen Casa de Vida.
    Los demás roles ven solo los participantes activos con membresía activa en sus casas.
    """
    if es_pastor(user):
        return Participante.objects.all()
    return Participante.objects.filter(
        estado=ACTIVO,
        casavidamiembro__estado=ACTIVO,
        casavidamiembro__id_casa_vida__in=casas_visibles(user),
    ).distinct()


def actividades_visibles(user):
    """Actividades de Casas de Vida con su asistencia, según el alcance del usuario (RF10)."""
    return Actividad.objects.filter(
        tipo_modulo=Actividad.TIPO_CASA_VIDA,
        id_casa_vida__in=casas_visibles(user),
    ).select_related("id_casa_vida", "id_responsable")
