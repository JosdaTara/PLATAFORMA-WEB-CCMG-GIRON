import datetime

from django.db import models

# Valores del tipo enum estado_general de PostgreSQL (RN24: baja lógica).
ACTIVO = "ACTIVO"
INACTIVO = "INACTIVO"
ESTADOS = [(ACTIVO, "Activo"), (INACTIVO, "Inactivo")]

FUNCIONES_APOYO = [("APRENDIZ", "Aprendiz"), ("ANFITRION", "Anfitrión"), ("MAESTRO_NINOS", "Maestro de Niños")]


class CasaVidaEquipo(models.Model):
    id_casa_vida_equipo = models.AutoField(primary_key=True, db_column="id_casa_vida_equipo")
    id_casa_vida = models.ForeignKey("CasaVida", models.DO_NOTHING, db_column="id_casa_vida")
    id_usuario = models.ForeignKey("cuentas.Usuario", models.DO_NOTHING, db_column="id_usuario")
    funcion = models.CharField(max_length=20, choices=FUNCIONES_APOYO)
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
    estado = models.CharField(max_length=10, choices=ESTADOS, default=ACTIVO)
    creado_en = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    actualizado_en = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "casa_vida"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre

    @property
    def activa(self):
        return self.estado != INACTIVO


class Area(models.Model):
    id_area = models.AutoField(primary_key=True, db_column="id_area")
    nombre = models.CharField(max_length=100)
    id_supervisor = models.ForeignKey("cuentas.Usuario", models.DO_NOTHING, db_column="id_supervisor", blank=True, null=True)
    estado = models.CharField(max_length=10, choices=ESTADOS, default=ACTIVO)
    creado_en = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "area"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre

    @property
    def activa(self):
        return self.estado != INACTIVO


class Participante(models.Model):
    id_participante = models.AutoField(primary_key=True, db_column="id_participante")
    nombres_apellidos = models.CharField(max_length=150)
    documento_identidad = models.CharField(max_length=50, unique=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    autorizacion_datos = models.BooleanField(default=False)
    estado = models.CharField(max_length=10, choices=ESTADOS, default=ACTIVO)
    creado_en = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    actualizado_en = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "participante"
        ordering = ["nombres_apellidos"]

    def __str__(self):
        return self.nombres_apellidos

    @property
    def activo(self):
        return self.estado != INACTIVO

    @property
    def membresia_activa(self):
        """Casa de Vida actual del participante (una sola membresía activa)."""
        return (
            self.casavidamiembro_set.filter(estado=ACTIVO)
            .select_related("id_casa_vida")
            .first()
        )


class CasaVidaMiembro(models.Model):
    id_casa_vida_miembro = models.AutoField(primary_key=True, db_column="id_casa_vida_miembro")
    id_casa_vida = models.ForeignKey(CasaVida, models.DO_NOTHING, db_column="id_casa_vida")
    id_participante = models.ForeignKey(Participante, models.DO_NOTHING, db_column="id_participante")
    fecha_ingreso = models.DateField(default=datetime.date.today, blank=True, null=True)
    estado = models.CharField(max_length=10, choices=ESTADOS, default=ACTIVO)

    class Meta:
        managed = False
        db_table = "casa_vida_miembro"
        unique_together = [("id_casa_vida", "id_participante")]

    def __str__(self):
        return f"{self.id_participante} en {self.id_casa_vida}"


class Actividad(models.Model):
    """Actividad de una Casa de Vida (tipo_modulo CASA_VIDA) o de un proceso de formación."""

    TIPO_CASA_VIDA = "CASA_VIDA"
    TIPO_ESCUELAS = "ESCUELAS_FORMACION"

    id_actividad = models.AutoField(primary_key=True, db_column="id_actividad")
    tipo_modulo = models.CharField(max_length=20, default=TIPO_CASA_VIDA)
    id_casa_vida = models.ForeignKey(CasaVida, models.DO_NOTHING, db_column="id_casa_vida", blank=True, null=True)
    id_proceso_formacion = models.IntegerField(db_column="id_proceso_formacion", blank=True, null=True)
    titulo = models.CharField(max_length=150)
    fecha = models.DateField()
    hora = models.TimeField(blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    id_responsable = models.ForeignKey("cuentas.Usuario", models.DO_NOTHING, db_column="id_responsable", blank=True, null=True)
    creado_en = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "actividad"
        ordering = ["-fecha", "-id_actividad"]

    def __str__(self):
        return f"{self.titulo} ({self.fecha})"


class Asistencia(models.Model):
    id_asistencia = models.AutoField(primary_key=True, db_column="id_asistencia")
    id_actividad = models.ForeignKey(Actividad, models.DO_NOTHING, db_column="id_actividad")
    id_participante = models.ForeignKey(Participante, models.DO_NOTHING, db_column="id_participante")
    presente = models.BooleanField(default=False)
    observacion = models.CharField(max_length=255, blank=True, null=True)
    registrado_por = models.ForeignKey("cuentas.Usuario", models.DO_NOTHING, db_column="registrado_por", blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "asistencia"
        unique_together = [("id_actividad", "id_participante")]

    def __str__(self):
        return f"{self.id_participante} - {self.id_actividad}"


class Seguimiento(models.Model):
    """Seguimiento pastoral de un participante (RF11, RN10)."""

    TIPOS = [("VISITA", "Visita"), ("LLAMADA", "Llamada"), ("CONSEJERIA", "Consejería"), ("OTRO", "Otro")]
    ESTADOS = [("ABIERTO", "Abierto"), ("EN_PROCESO", "En proceso"), ("CERRADO", "Cerrado")]

    id_seguimiento = models.AutoField(primary_key=True, db_column="id_seguimiento")
    id_participante = models.ForeignKey(Participante, models.DO_NOTHING, db_column="id_participante")
    id_usuario = models.ForeignKey("cuentas.Usuario", models.DO_NOTHING, db_column="id_usuario")
    fecha = models.DateField(default=datetime.date.today)
    tipo = models.CharField(max_length=20, choices=TIPOS, default="VISITA")
    observacion = models.TextField()
    estado = models.CharField(max_length=15, choices=ESTADOS, default="ABIERTO")
    tipo_modulo = models.CharField(max_length=20, default=Actividad.TIPO_CASA_VIDA)
    creado_en = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    actualizado_en = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "seguimiento"
        ordering = ["-fecha", "-id_seguimiento"]

    def __str__(self):
        return f"Seguimiento de {self.id_participante} ({self.fecha})"


class Reporte(models.Model):
    """Reporte semanal de una Casa de Vida (RF14) o general mensual de un Área (RF13)."""

    CASA_VIDA = "CASA_VIDA"
    GENERAL_AREA = "GENERAL_AREA"

    id_reporte = models.AutoField(primary_key=True, db_column="id_reporte")
    tipo_modulo = models.CharField(max_length=20, default=Actividad.TIPO_CASA_VIDA)
    tipo_reporte = models.CharField(max_length=20, default=CASA_VIDA)
    id_usuario_envia = models.ForeignKey("cuentas.Usuario", models.DO_NOTHING, db_column="id_usuario_envia", related_name="reportes_enviados")
    id_usuario_destino = models.ForeignKey("cuentas.Usuario", models.DO_NOTHING, db_column="id_usuario_destino", blank=True, null=True, related_name="reportes_recibidos")
    id_casa_vida = models.ForeignKey(CasaVida, models.DO_NOTHING, db_column="id_casa_vida", blank=True, null=True)
    id_area = models.ForeignKey(Area, models.DO_NOTHING, db_column="id_area", blank=True, null=True)
    id_reporte_general = models.ForeignKey("self", models.DO_NOTHING, db_column="id_reporte_general", blank=True, null=True, related_name="reportes_casa")
    periodo = models.CharField(max_length=20)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    ruta_archivo = models.CharField(max_length=255, blank=True, null=True)
    enviado_en = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "reporte"
        ordering = ["-fecha_inicio", "-id_reporte"]

    def __str__(self):
        if self.tipo_reporte == self.GENERAL_AREA:
            return f"Reporte general {self.id_area} · {self.periodo}"
        return f"Reporte {self.id_casa_vida} · {self.periodo}"

    @property
    def es_general(self):
        return self.tipo_reporte == self.GENERAL_AREA
