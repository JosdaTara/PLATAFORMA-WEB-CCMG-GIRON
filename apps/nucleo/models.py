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
