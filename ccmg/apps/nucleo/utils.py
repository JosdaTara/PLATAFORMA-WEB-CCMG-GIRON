"""Constantes y helpers para roles y módulos (ERS)."""
ROLES_PASTOR = "PASTOR"
ROLES_SUPERVISOR = "SUPERVISOR_AREA"
ROLES_LIDER = "LIDER_CASA_VIDA"
ROLES_APOYO = "APOYO_CASA_VIDA"
ROLES_COORD = "COORDINADOR_FORMACION"
# Desarrollador de la plataforma: tiene todo lo del Pastor, más la bitácora de auditoría
# y la gestión de otros Super Administradores. El Pastor no lo ve ni lo modifica.
ROLES_SUPERADMIN = "SUPERADMIN"

MODULO_CASAS_VIDA = "CASAS_VIDA"
MODULO_ESCUELAS_FORMACION = "ESCUELAS_FORMACION"
MODULO_AMBOS = "AMBOS"

# Nombre visible de cada rol en la interfaz.
ROLES_ETIQUETA = {
    ROLES_SUPERADMIN: "Super Administrador",
    ROLES_PASTOR: "Pastor",
    ROLES_SUPERVISOR: "Supervisor de Área",
    ROLES_LIDER: "Líder de Casa de Vida",
    ROLES_APOYO: "Apoyo de Casa de Vida",
    ROLES_COORD: "Coordinador de Formación",
}

# Códigos de rol que entiende el JavaScript del panel (auth.js / ROLES_INFO).
ROLES_JS = {
    ROLES_SUPERADMIN: "pastor",  # en los menús JS se comporta como el Pastor
    ROLES_PASTOR: "pastor",
    ROLES_SUPERVISOR: "supervisor",
    ROLES_LIDER: "lider",
    ROLES_APOYO: "apoyo",
    ROLES_COORD: "coord",
}


def rol_real(user):
    return getattr(getattr(user, "rol", None), "nombre", None)


def rol_efectivo(user):
    """Rol con el que se evalúan permisos y alcance: el Super Administrador cuenta como Pastor."""
    rol = rol_real(user)
    return ROLES_PASTOR if rol == ROLES_SUPERADMIN else rol


def es_superadmin(user):
    return getattr(user, "is_authenticated", False) and rol_real(user) == ROLES_SUPERADMIN


def sesion_js(user):
    """Datos de sesión que el JavaScript necesita para pintar el panel.

    La fuente de verdad sigue siendo la sesión de Django: esto solo se usa
    para mostrar nombre/rol y filtrar el menú, nunca para autorizar.
    """
    if not getattr(user, "is_authenticated", False):
        return None
    from django.urls import reverse

    from nucleo.permissions import puede_gestionar_ofrendas

    rol = getattr(user, "rol", None)
    return {
        "nombre": getattr(user, "nombre_completo", None) or getattr(user, "correo", ""),
        "rol": ROLES_JS.get(getattr(rol, "nombre", None), ""),
        "rolNombre": ROLES_ETIQUETA.get(getattr(rol, "nombre", None), ""),
        "superadmin": es_superadmin(user),
        "auditoria": reverse("cuentas:auditoria") if es_superadmin(user) else None,
        # Enlace al módulo de ofrendas si el usuario está autorizado (RN14).
        "ofrendas": reverse("ofrendas:index") if puede_gestionar_ofrendas(user) else None,
    }



def registrar_auditoria(request, accion, obj):
    """Deja constancia de quién creó, modificó o desactivó un registro (RNF18)."""
    from nucleo.models import Auditoria

    user = getattr(request, "user", None)
    Auditoria.objects.create(
        id_usuario=user if getattr(user, "is_authenticated", False) else None,
        accion=accion,
        entidad=obj._meta.db_table,
        id_entidad=obj.pk,
        ip=(request.META.get("REMOTE_ADDR") or "")[:45] or None,
    )
