import getpass

from django.core.management.base import BaseCommand
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from cuentas.models import Rol, Usuario


class Command(BaseCommand):
    help = "Crea la primera cuenta con rol Pastor. Pide la contraseña por terminal."

    def handle(self, *args, **options):
        self.stdout.write("=== Crear cuenta Pastor ===")

        correo = input("Correo: ").strip().lower()
        if not correo:
            self.stderr.write("El correo es obligatorio.")
            return

        username = input("Username (opcional, Enter para omitir): ").strip()
        if not username:
            username = None
        else:
            username = username.strip()

        nombre = input("Nombre completo: ").strip()
        if not nombre:
            self.stderr.write("El nombre completo es obligatorio.")
            return

        password = getpass.getpass("Contraseña: ")
        password2 = getpass.getpass("Confirmar contraseña: ")
        if password != password2:
            self.stderr.write("Las contraseñas no coinciden.")
            return

        # Validar con reglas de RNF19
        try:
            validate_password(password)
        except ValidationError as e:
            for msg in e.messages:
                self.stderr.write(f"- {msg}")
            return

        # Buscar rol PASTOR
        try:
            rol_pastor = Rol.objects.get(nombre="PASTOR")
        except Rol.DoesNotExist:
            self.stderr.write("No existe el rol PASTOR en la tabla rol. Verifica la base de datos.")
            return

        if Usuario.objects.filter(correo=correo).exists():
            self.stderr.write("Ya existe un usuario con ese correo.")
            return

        if username and Usuario.objects.filter(username__iexact=username).exists():
            self.stderr.write("Ya existe un usuario con ese username.")
            return

        user = Usuario.objects.create_user(
            correo=correo,
            username=username,
            nombre_completo=nombre,
            rol=rol_pastor,
            activo=True,
            password=password,
        )

        self.stdout.write(self.style.SUCCESS(f"Cuenta Pastor creada: {user.correo} (id={user.id_usuario})"))
