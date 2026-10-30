"""Alcance del módulo Escuelas de Formación (RN13, RN21).

El Pastor ve todos los procesos; el Coordinador de Formación, los procesos que coordina.
"""
from nucleo.utils import ROLES_COORD, ROLES_PASTOR
from pva.alcance import rol_de
from pva.models import Actividad, Participante, Seguimiento

from .models import ProcesoFormacion

TIPO_MODULO = Actividad.TIPO_ESCUELAS


def procesos_visibles(user):
    rol = rol_de(user)
    qs = ProcesoFormacion.objects.select_related("id_coordinador")
    if rol == ROLES_PASTOR:
        return qs
    if rol == ROLES_COORD:
        return qs.filter(id_coordinador=user)
    return qs.none()


def participantes_formacion(user):
    """Personas inscritas (o que estuvieron inscritas) en los procesos al alcance del usuario (RF06)."""
    return Participante.objects.filter(
        inscripcionformacion__id_proceso_formacion__in=procesos_visibles(user)
    ).distinct()


def actividades_formacion(user):
    return Actividad.objects.filter(
        tipo_modulo=TIPO_MODULO, id_proceso_formacion__in=procesos_visibles(user)
    ).select_related("id_proceso_formacion", "id_responsable")


def seguimientos_formacion(user):
    return Seguimiento.objects.filter(
        tipo_modulo=TIPO_MODULO, id_proceso_formacion__in=procesos_visibles(user)
    ).select_related("id_participante", "id_usuario", "id_proceso_formacion")
