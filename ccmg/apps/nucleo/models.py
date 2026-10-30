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


class ConservaCreadoEnModel(models.Model):
    """Evita reescribir creado_en al actualizar.

    Las columnas son timestamp sin zona horaria y USE_TZ está activo: volver a guardar
    el valor leído lo desplazaría por la diferencia con UTC en cada edición.
    """

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self._state.adding and kwargs.get("update_fields") is None:
            kwargs["update_fields"] = [
                f.name for f in self._meta.concrete_fields if not f.primary_key and f.name != "creado_en"
            ]
        super().save(*args, **kwargs)
