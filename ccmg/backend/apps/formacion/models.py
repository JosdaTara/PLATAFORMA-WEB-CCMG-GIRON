import datetime

from django.db import models

from pva.models import ACTIVO, ESTADOS, INACTIVO


class ProcesoFormacion(models.Model):
    """Proceso de las Escuelas de Formación (RF18–RF22, RN12): una cohorte de un tipo concreto."""

    PASOS_VIDA = "PASOS_VIDA"
    ESCUELAS_VIDA = "ESCUELAS_VIDA"
    MODULOS_LIDERAZGO = "MODULOS_LIDERAZGO"
    MISIONES = "MISIONES"
    TIPOS = [
        (PASOS_VIDA, "Pasos de Vida"),
        (ESCUELAS_VIDA, "Escuelas Vida"),
        (MODULOS_LIDERAZGO, "Módulos de Liderazgo"),
        (MISIONES, "Misiones"),
    ]

    id_proceso_formacion = models.AutoField(primary_key=True, db_column="id_proceso_formacion")
    nombre = models.CharField(max_length=150)
    tipo_proceso = models.CharField(max_length=20, choices=TIPOS)
    id_coordinador = models.ForeignKey("cuentas.Usuario", models.DO_NOTHING, db_column="id_coordinador", related_name="procesos_coordinados")
    descripcion = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=10, choices=ESTADOS, default=ACTIVO)
    creado_en = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    actualizado_en = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "proceso_formacion"
        ordering = ["tipo_proceso", "nombre"]

    def __str__(self):
        return self.nombre

    @property
    def activo(self):
        return self.estado != INACTIVO


class InscripcionFormacion(models.Model):
    """Vínculo de un participante con un proceso de formación (HU-25, criterio 3)."""

    id_inscripcion = models.AutoField(primary_key=True, db_column="id_inscripcion")
    id_participante = models.ForeignKey("pva.Participante", models.DO_NOTHING, db_column="id_participante")
    id_proceso_formacion = models.ForeignKey(ProcesoFormacion, models.DO_NOTHING, db_column="id_proceso_formacion")
    fecha_inscripcion = models.DateField(default=datetime.date.today, blank=True, null=True)
    estado = models.CharField(max_length=10, choices=ESTADOS, default=ACTIVO)

    class Meta:
        managed = False
        db_table = "inscripcion_formacion"
        unique_together = [("id_participante", "id_proceso_formacion")]

    def __str__(self):
        return f"{self.id_participante} en {self.id_proceso_formacion}"
