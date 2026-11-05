import datetime

from django import forms

from cuentas.models import Usuario
from nucleo.utils import ROLES_LIDER, ROLES_SUPERVISOR

from . import periodos
from .models import ACTIVO, Actividad, Area, CasaVida, Participante, Reporte, Seguimiento


def _usuarios_con_rol(rol):
    return Usuario.objects.filter(rol__nombre=rol, activo=True).order_by("nombre_completo")


class UsuarioChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.nombre_completo


class EstiloBootstrapMixin:
    """Asigna las clases de Bootstrap a los widgets y marca los campos con error."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.fields.values():
            w = campo.widget
            if isinstance(w, forms.CheckboxInput):
                clase = "form-check-input"
            elif isinstance(w, forms.Select):
                clase = "form-select"
            else:
                clase = "form-control"
            w.attrs["class"] = clase

    def is_valid(self):
        valido = super().is_valid()
        for nombre in self.errors:
            if nombre in self.fields:
                self.fields[nombre].widget.attrs["class"] += " is-invalid"
        return valido


class AreaForm(EstiloBootstrapMixin, forms.ModelForm):
    id_supervisor = UsuarioChoiceField(
        queryset=Usuario.objects.none(), required=False, label="Supervisor de Área"
    )

    class Meta:
        model = Area
        fields = ["nombre", "id_supervisor"]
        labels = {"nombre": "Nombre del Área"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["id_supervisor"].queryset = _usuarios_con_rol(ROLES_SUPERVISOR)

    def clean_nombre(self):
        nombre = " ".join(self.cleaned_data["nombre"].split())
        qs = Area.objects.filter(nombre__iexact=nombre)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Ya existe un Área con ese nombre.")
        return nombre

    def clean_id_supervisor(self):
        supervisor = self.cleaned_data.get("id_supervisor")
        if supervisor:
            otra = Area.objects.filter(id_supervisor=supervisor)
            if self.instance.pk:
                otra = otra.exclude(pk=self.instance.pk)
            otra = otra.first()
            if otra:
                raise forms.ValidationError(f"Este Supervisor ya está asignado al Área «{otra}».")
        return supervisor


class CasaVidaForm(EstiloBootstrapMixin, forms.ModelForm):
    id_area = forms.ModelChoiceField(queryset=Area.objects.none(), label="Área")
    id_lider = UsuarioChoiceField(
        queryset=Usuario.objects.none(), required=False, label="Líder de Casa de Vida"
    )

    class Meta:
        model = CasaVida
        fields = ["nombre", "id_area", "id_lider", "direccion"]
        labels = {"nombre": "Nombre de la Casa de Vida", "direccion": "Dirección"}
        widgets = {"direccion": forms.TextInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        areas = Area.objects.filter(estado=ACTIVO)
        if self.instance.pk and self.instance.id_area_id:
            # Conservar el Área actual aunque esté inactiva.
            areas = Area.objects.filter(pk=self.instance.id_area_id) | areas
        self.fields["id_area"].queryset = areas
        self.fields["id_lider"].queryset = _usuarios_con_rol(ROLES_LIDER)

    def clean_nombre(self):
        return " ".join(self.cleaned_data["nombre"].split())

    def clean_id_lider(self):
        lider = self.cleaned_data.get("id_lider")
        if lider:
            otra = CasaVida.objects.filter(id_lider=lider, estado=ACTIVO)
            if self.instance.pk:
                otra = otra.exclude(pk=self.instance.pk)
            otra = otra.first()
            if otra:
                raise forms.ValidationError(f"Este Líder ya está asignado a la Casa de Vida «{otra}».")
        return lider

class ParticipanteForm(EstiloBootstrapMixin, forms.ModelForm):
    """Datos mínimos del participante (RN09) y autorización de datos (RN23)."""

    casa_vida = forms.ModelChoiceField(queryset=CasaVida.objects.none(), label="Casa de Vida")

    class Meta:
        model = Participante
        fields = [
            "nombres_apellidos",
            "documento_identidad",
            "fecha_nacimiento",
            "telefono",
            "direccion",
            "autorizacion_datos",
        ]
        labels = {
            "nombres_apellidos": "Nombres y apellidos",
            "documento_identidad": "Documento de identidad",
            "fecha_nacimiento": "Fecha de nacimiento",
            "telefono": "Teléfono de contacto",
            "direccion": "Dirección",
            "autorizacion_datos": "Autoriza el tratamiento de sus datos personales (Ley 1581 de 2012)",
        }
        help_texts = {
            "autorizacion_datos": "Si es menor de edad, la autorización la otorga su representante legal.",
        }
        widgets = {
            "fecha_nacimiento": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "direccion": forms.TextInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in ("fecha_nacimiento", "telefono", "direccion"):
            self.fields[campo].required = True
        self.fields["autorizacion_datos"].required = True
        self.fields["autorizacion_datos"].error_messages["required"] = (
            "Sin la autorización de tratamiento de datos no se puede registrar al participante."
        )
        casas = CasaVida.objects.filter(estado=ACTIVO)
        membresia = self.instance.membresia_activa if self.instance.pk else None
        if membresia:
            casas = CasaVida.objects.filter(pk=membresia.id_casa_vida_id) | casas
            self.initial.setdefault("casa_vida", membresia.id_casa_vida_id)
        self.fields["casa_vida"].queryset = casas

    def clean_nombres_apellidos(self):
        return " ".join(self.cleaned_data["nombres_apellidos"].split())

    def clean_documento_identidad(self):
        documento = self.cleaned_data["documento_identidad"].strip()
        qs = Participante.objects.filter(documento_identidad__iexact=documento)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Ya existe un participante con ese documento de identidad.")
        return documento

    def clean_fecha_nacimiento(self):
        fecha = self.cleaned_data.get("fecha_nacimiento")
        if fecha and fecha > datetime.date.today():
            raise forms.ValidationError("La fecha de nacimiento no puede ser futura.")
        return fecha

    def clean_telefono(self):
        telefono = self.cleaned_data["telefono"].strip()
        digitos = telefono.replace(" ", "").replace("+", "").replace("-", "")
        if not digitos.isdigit() or not 7 <= len(digitos) <= 15:
            raise forms.ValidationError("Ingrese un teléfono válido (solo números, de 7 a 15 dígitos).")
        return telefono


class RegistroAsistenciaForm(EstiloBootstrapMixin, forms.Form):
    """Datos de la actividad; la asistencia de cada participante llega como casillas 'presente_<id>'."""

    titulo = forms.CharField(max_length=150, label="Actividad", initial="Reunión semanal")
    fecha = forms.DateField(
        label="Fecha", widget=forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d")
    )
    descripcion = forms.CharField(
        label="Observaciones", required=False, widget=forms.Textarea(attrs={"rows": 2})
    )

    def __init__(self, *args, casa=None, **kwargs):
        self.casa = casa
        super().__init__(*args, **kwargs)
        self.fields["fecha"].initial = datetime.date.today

    def clean_titulo(self):
        return " ".join(self.cleaned_data["titulo"].split())

    def clean_fecha(self):
        fecha = self.cleaned_data["fecha"]
        if fecha > datetime.date.today():
            raise forms.ValidationError("No se puede registrar asistencia de una fecha futura.")
        if self.casa and Reporte.objects.filter(
            tipo_reporte=Reporte.CASA_VIDA, id_casa_vida=self.casa, periodo=periodos.semana(fecha).etiqueta
        ).exists():
            raise forms.ValidationError(
                "El reporte de esa semana ya fue enviado al Supervisor; no se puede agregar asistencia."
            )
        return fecha

    def clean(self):
        datos = super().clean()
        titulo, fecha = datos.get("titulo"), datos.get("fecha")
        if self.casa and titulo and fecha:
            # Si otro integrante del equipo ya la registró, se muestra como registrada (RN06).
            ya = (
                Actividad.objects.filter(id_casa_vida=self.casa, fecha=fecha, titulo__iexact=titulo)
                .select_related("id_responsable")
                .first()
            )
            if ya:
                quien = ya.id_responsable.nombre_completo if ya.id_responsable else "otro integrante"
                raise forms.ValidationError(
                    f"La asistencia de «{titulo}» del {fecha:%d/%m/%Y} ya fue registrada por {quien}."
                )
        return datos


class SeguimientoForm(EstiloBootstrapMixin, forms.ModelForm):
    """Registro de seguimiento por el Pastor (RF11, RN10)."""

    class Meta:
        model = Seguimiento
        fields = ["id_participante", "fecha", "tipo", "estado", "observacion"]
        labels = {"id_participante": "Participante", "observacion": "Observaciones"}
        widgets = {
            "fecha": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "observacion": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        participantes = Participante.objects.filter(estado=ACTIVO)
        if self.instance.pk:
            participantes = Participante.objects.filter(pk=self.instance.id_participante_id) | participantes
        self.fields["id_participante"].queryset = participantes.order_by("nombres_apellidos")

    def clean_fecha(self):
        fecha = self.cleaned_data["fecha"]
        if fecha > datetime.date.today():
            raise forms.ValidationError("La fecha del seguimiento no puede ser futura.")
        return fecha

    def clean_observacion(self):
        return self.cleaned_data["observacion"].strip()


class EnviarReporteCasaForm(EstiloBootstrapMixin, forms.Form):
    """Reporte semanal de la Casa de Vida al Supervisor de Área (RF14, CU02)."""

    semana = forms.ChoiceField(label="Semana")
    observaciones = forms.CharField(
        label="Observaciones para el Supervisor", required=False, widget=forms.Textarea(attrs={"rows": 3})
    )

    def __init__(self, *args, casa=None, **kwargs):
        self.casa = casa
        super().__init__(*args, **kwargs)
        self.fields["semana"].choices = [(p.inicio.isoformat(), p.nombre) for p in periodos.semanas_recientes(8)]

    def clean_semana(self):
        periodo = periodos.semana(datetime.date.fromisoformat(self.cleaned_data["semana"]))
        ya = (
            Reporte.objects.filter(tipo_reporte=Reporte.CASA_VIDA, id_casa_vida=self.casa, periodo=periodo.etiqueta)
            .select_related("id_usuario_envia")
            .first()
        )
        if ya:
            raise forms.ValidationError(
                f"El reporte de esta semana ya fue enviado por {ya.id_usuario_envia.nombre_completo}."
            )
        if not Actividad.objects.filter(id_casa_vida=self.casa, fecha__range=(periodo.inicio, periodo.fin)).exists():
            raise forms.ValidationError("No hay asistencia registrada en esta semana. Regístrela antes de enviar el reporte.")
        return periodo


class EnviarReporteGeneralForm(EstiloBootstrapMixin, forms.Form):
    """Reporte general mensual del Supervisor al Pastor (RF13, CU03)."""

    mes = forms.ChoiceField(label="Mes")
    observaciones = forms.CharField(
        label="Observaciones generales", required=False, widget=forms.Textarea(attrs={"rows": 3})
    )

    def __init__(self, *args, area=None, **kwargs):
        self.area = area
        super().__init__(*args, **kwargs)
        self.fields["mes"].choices = [(p.inicio.isoformat(), p.nombre) for p in periodos.meses_recientes(6)]

    def clean_mes(self):
        periodo = periodos.mes(datetime.date.fromisoformat(self.cleaned_data["mes"]))
        if Reporte.objects.filter(tipo_reporte=Reporte.GENERAL_AREA, id_area=self.area, periodo=periodo.etiqueta).exists():
            raise forms.ValidationError("El reporte general de este mes ya fue enviado al Pastor.")
        if not reportes_casa_pendientes(self.area, periodo).exists():
            raise forms.ValidationError("No hay reportes de las Casas de Vida en este mes; no se puede enviar un reporte vacío.")
        return periodo


def reportes_casa_pendientes(area, periodo):
    """Reportes semanales del Área que empiezan en el mes y aún no van en un reporte general."""
    return Reporte.objects.filter(
        tipo_reporte=Reporte.CASA_VIDA,
        id_casa_vida__id_area=area,
        fecha_inicio__range=(periodo.inicio, periodo.fin),
        id_reporte_general__isnull=True,
    ).select_related("id_casa_vida", "id_usuario_envia")


class GenerarReporteForm(EstiloBootstrapMixin, forms.Form):
    """Parámetros del reporte consolidado del Pastor (RF16, CU04)."""

    tipo = forms.ChoiceField(
        label="Periodo", choices=[("semanal", "Semanal"), ("mensual", "Mensual"), ("anual", "Anual")], initial="mensual"
    )
    fecha = forms.DateField(
        label="Fecha de referencia", widget=forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        help_text="Se toma la semana, el mes o el año que contiene esta fecha.",
    )
    area = forms.ModelChoiceField(queryset=Area.objects.all(), required=False, empty_label="Todas", label="Área")
    casa = forms.ModelChoiceField(queryset=CasaVida.objects.all(), required=False, empty_label="Todas", label="Casa de Vida")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["fecha"].initial = datetime.date.today

    @property
    def periodo(self):
        return periodos.POR_TIPO[self.cleaned_data["tipo"]](self.cleaned_data["fecha"])
