"""Alcance de la información del módulo Casas de Vida según el rol (RN03, RN04, RN05, RN18).

Toda consulta de Casas de Vida, participantes o asistencia debe pasar por estas
funciones para que cada rol vea únicamente lo que le corresponde.
"""
from nucleo.utils import ROLES_APOYO, ROLES_LIDER, ROLES_PASTOR, ROLES_SUPERVISOR, rol_efectivo

from .models import ACTIVO, Actividad, Area, CasaVida, CasaVidaEquipo, Participante, Reporte, Seguimiento


def rol_de(user):
    """Rol efectivo: el Super Administrador ve y gestiona lo mismo que el Pastor."""
    return rol_efectivo(user)


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


def area_del_supervisor(user):
    if rol_de(user) != ROLES_SUPERVISOR:
        return None
    return Area.objects.filter(id_supervisor=user).first()


def seguimientos_visibles(user):
    """Seguimiento: lo registra el Pastor; el Supervisor y el Líder solo lo consultan (RF11)."""
    if rol_de(user) not in (ROLES_PASTOR, ROLES_SUPERVISOR, ROLES_LIDER):
        return Seguimiento.objects.none()
    return Seguimiento.objects.filter(
        tipo_modulo=Actividad.TIPO_CASA_VIDA,
        id_participante__in=participantes_visibles(user),
    ).select_related("id_participante", "id_usuario")


def reportes_casa_visibles(user):
    """Reportes semanales de las Casas de Vida al alcance del usuario (RF15)."""
    return Reporte.objects.filter(
        tipo_reporte=Reporte.CASA_VIDA,
        id_casa_vida__in=casas_visibles(user),
    ).select_related("id_casa_vida", "id_usuario_envia", "id_reporte_general")


def reportes_generales_visibles(user):
    """Reportes generales: el Pastor los recibe todos; el Supervisor ve los suyos (RF15)."""
    qs = Reporte.objects.filter(tipo_reporte=Reporte.GENERAL_AREA).select_related("id_area", "id_usuario_envia")
    rol = rol_de(user)
    if rol == ROLES_PASTOR:
        return qs
    if rol == ROLES_SUPERVISOR:
        return qs.filter(id_area__id_supervisor=user)
    return qs.none()
