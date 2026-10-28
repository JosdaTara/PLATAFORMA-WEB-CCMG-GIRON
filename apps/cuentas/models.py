from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils import timezone

from nucleo.models import TimeStampedModel


class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True, db_column="id_rol")
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    acceso_casas_vida = models.BooleanField(blank=True, null=True)
    acceso_escuelas_formacion = models.BooleanField(blank=True, null=True)
    creado_en = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "rol"

    def __str__(self):
        return self.nombre


class UsuarioManager(models.Manager):
    def create_user(self, correo, password=None, **extra_fields):
        if not correo:
            raise ValueError("El correo es obligatorio.")
        correo = correo.strip().lower()
        user = self.model(correo=correo, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, correo, password=None, **extra_fields):
        extra_fields.setdefault("activo", True)
        return self.create_user(correo, password, **extra_fields)


class Usuario(AbstractBaseUser):
    id_usuario = models.AutoField(primary_key=True, db_column="id_usuario")
    nombre_completo = models.CharField(max_length=150)
    correo = models.CharField(max_length=150, unique=True)
    username = models.CharField(max_length=50, unique=True, blank=True, null=True)
    password = models.CharField(max_length=255, db_column="password_hash")
    rol = models.ForeignKey(Rol, models.DO_NOTHING, db_column="id_rol")
    activo = models.BooleanField(default=True)
    intentos_fallidos = models.IntegerField(default=0)
    bloqueado_hasta = models.DateTimeField(blank=True, null=True)
    creado_en = models.DateTimeField(blank=True, null=True)
    actualizado_en = models.DateTimeField(blank=True, null=True)
    creado_por = models.ForeignKey(
        "self",
        models.DO_NOTHING,
        db_column="creado_por",
        blank=True,
        null=True,
        related_name="+",
    )
    modificado_por = models.ForeignKey(
        "self",
        models.DO_NOTHING,
        db_column="modificado_por",
        blank=True,
        null=True,
        related_name="+",
    )
    last_login = models.DateTimeField(blank=True, null=True, db_column="ultimo_acceso")

    USERNAME_FIELD = "correo"
    REQUIRED_FIELDS = []

    objects = UsuarioManager()

    class Meta:
        managed = False
        db_table = "usuario"

    @property
    def is_active(self):
        return bool(self.activo)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return self.correo
