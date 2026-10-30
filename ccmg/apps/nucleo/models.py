from django.db import models


class TimeStampedModel(models.Model):
    """Modelo abstracto de auditoría (RNF18)."""
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteModel(models.Model):
    """Baja lógica (RN24, RF28)."""
    activo = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Auditoria(models.Model):
    """Registro de acciones sobre la información (RNF18)."""
    id_auditoria = models.AutoField(primary_key=True, db_column="id_auditoria")
    id_usuario = models.ForeignKey("cuentas.Usuario", models.DO_NOTHING, db_column="id_usuario", blank=True, null=True)
    accion = models.CharField(max_length=100)
    entidad = models.CharField(max_length=50)
    id_entidad = models.IntegerField(blank=True, null=True)
    ip = models.CharField(max_length=45, blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "auditoria"
        ordering = ["-fecha"]

