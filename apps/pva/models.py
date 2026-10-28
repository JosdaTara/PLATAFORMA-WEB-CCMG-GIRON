from django.db import models


class CasaVidaEquipo(models.Model):
    id_casa_vida_equipo = models.AutoField(primary_key=True, db_column="id_casa_vida_equipo")
    id_casa_vida = models.ForeignKey("CasaVida", models.DO_NOTHING, db_column="id_casa_vida")
    id_usuario = models.ForeignKey("cuentas.Usuario", models.DO_NOTHING, db_column="id_usuario")
    funcion = models.CharField(max_length=20)
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "casa_vida_equipo"

    def __str__(self):
        return f"{self.id_usuario} - {self.id_casa_vida} ({self.funcion})"


class CasaVida(models.Model):
    id_casa_vida = models.AutoField(primary_key=True, db_column="id_casa_vida")
    nombre = models.CharField(max_length=100)
    id_area = models.ForeignKey("Area", models.DO_NOTHING, db_column="id_area", blank=True, null=True)
    id_lider = models.ForeignKey("cuentas.Usuario", models.DO_NOTHING, db_column="id_lider", blank=True, null=True)
    id_supervisor = models.ForeignKey("cuentas.Usuario", models.DO_NOTHING, db_column="id_supervisor", blank=True, null=True, related_name="casavida_supervisor_set")
    direccion = models.TextField(blank=True, null=True)
    estado = models.TextField(blank=True, null=True)
    creado_en = models.DateTimeField(blank=True, null=True)
    actualizado_en = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "casa_vida"

    def __str__(self):
        return self.nombre


class Area(models.Model):
    id_area = models.AutoField(primary_key=True, db_column="id_area")
    nombre = models.CharField(max_length=100)
    id_supervisor = models.ForeignKey("cuentas.Usuario", models.DO_NOTHING, db_column="id_supervisor", blank=True, null=True)
    estado = models.TextField(blank=True, null=True)
    creado_en = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "area"

    def __str__(self):
        return self.nombre
