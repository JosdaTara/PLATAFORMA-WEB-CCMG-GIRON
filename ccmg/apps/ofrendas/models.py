import datetime

from django.db import models


class Ofrenda(models.Model):
    """Ofrenda recibida en las actividades del PVA (RF17)."""

    id_ofrenda = models.AutoField(primary_key=True, db_column="id_ofrenda")
    fecha = models.DateField(default=datetime.date.today)
    concepto = models.CharField(max_length=150)
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    id_casa_vida = models.ForeignKey(
        "pva.CasaVida", models.DO_NOTHING, db_column="id_casa_vida", blank=True, null=True
    )
    id_usuario_registro = models.ForeignKey(
        "cuentas.Usuario", models.DO_NOTHING, db_column="id_usuario_registro", blank=True, null=True, related_name="ofrendas_registradas"
    )
    modificado_por = models.ForeignKey(
        "cuentas.Usuario", models.DO_NOTHING, db_column="modificado_por", blank=True, null=True, related_name="+"
    )
    observacion = models.TextField(blank=True, null=True)
    creado_en = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    actualizado_en = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "ofrenda"
        ordering = ["-fecha", "-id_ofrenda"]

    def __str__(self):
        return f"{self.concepto} ({self.fecha:%d/%m/%Y})"
