"""Crea la cuenta de Super Administrador (desarrollador) o promueve una cuenta existente.

    python manage.py crear_superadmin                      # pide correo, nombre y contraseña
    python manage.py crear_superadmin --promover correo    # convierte una cuenta existente
"""
from django.core.management.base import CommandError

from cuentas.models import Rol, Usuario
from nucleo.utils import ROLES_SUPERADMIN

from .crear_pastor import Command as CrearPastor


class Command(CrearPastor):
    help = "Crea una cuenta de Super Administrador o promueve una existente con --promover. La contraseña se pide por terminal."
    ROL = ROLES_SUPERADMIN
    ETIQUETA = "Super Administrador"

    def add_arguments(self, parser):
        parser.add_argument("--promover", metavar="CORREO", help="Correo de una cuenta existente que pasará a ser Super Administrador.")

    def handle(self, *args, **options):
        correo = options.get("promover")
        if not correo:
            return super().handle(*args, **options)
        try:
            rol = Rol.objects.get(nombre=self.ROL)
        except Rol.DoesNotExist:
            raise CommandError(f"No existe el rol {self.ROL} en la tabla rol. Ejecute datos_iniciales.sql.")
        user = Usuario.objects.filter(correo__iexact=correo.strip()).first()
        if user is None:
            raise CommandError(f"No hay ninguna cuenta con el correo {correo}.")
        anterior = user.rol.etiqueta
        user.rol = rol
        user.activo = True
        user.save(update_fields=["rol", "activo"])
        self.stdout.write(self.style.SUCCESS(f"{user.correo} pasó de {anterior} a Super Administrador."))
