import datetime

from django import forms

from cuentas.models import Usuario
from nucleo.utils import ROLES_COORD, ROLES_PASTOR
from pva.forms import EstiloBootstrapMixin, ParticipanteForm, UsuarioChoiceField
from pva.models import ACTIVO, Actividad, Participante, Seguimiento

from .alcance import TIPO_MODULO, procesos_visibles
from .models import InscripcionFormacion, ProcesoFormacion


def procesos_activos(user):
    return procesos_visibles(user).filter(estado=ACTIVO).order_by("tipo_proceso", "nombre")


class ProcesoChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.get_tipo_proceso_display()} · {obj.nombre}"


class ProcesoForm(EstiloBootstrapMixin, forms.ModelForm):
    """Proceso de formación (RF18, RN12). El Pastor asigna el coordinador; el Coordinador crea los suyos."""

    id_coordinador = UsuarioChoiceField(queryset=Usuario.objects.none(), label="Coordinador")

    class Meta:
        model = ProcesoFormacion
        fields = ["nombre", "tipo_proceso", "id_coordinador", "descripcion"]
        labels = {"nombre": "Nombre del proceso", "tipo_proceso": "Escuela", "descripcion": "Descripción"}
        help_texts = {"nombre": "Por ejemplo: Escuela Vida Nivel 1 – 2026."}
        widgets = {"descripcion": forms.Textarea(attrs={"rows": 3})}

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None and getattr(user.rol, "nombre", None) != ROLES_PASTOR:
            del self.fields["id_coordinador"]
        else:
            self.fields["id_coordinador"].queryset = Usuario.objects.filter(
                rol__nombre__in=[ROLES_COORD, ROLES_PASTOR], activo=True
            ).order_by("rol__nombre", "nombre_completo")

    def clean_nombre(self):
        nombre = " ".join(self.cleaned_data["nombre"].split())
        qs = ProcesoFormacion.objects.filter(nombre__iexact=nombre)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Ya existe un proceso con ese nombre.")
        return nombre


class DatosParticipanteForm(ParticipanteForm):
    """Datos personales del participante (RN09, RN23), sin Casa de Vida."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields["casa_vida"]

    def clean_documento_identidad(self):
        try:
            return super().clean_documento_identidad()
        except forms.ValidationError:
            raise forms.ValidationError(
                "Ya existe un participante con ese documento. Use «Inscribir participante existente»."
            )


class NuevoParticipanteFormacionForm(DatosParticipanteForm):
    """Registro de una persona nueva inscrita en un proceso (HU-25, HU-28, HU-31, HU-34)."""

    proceso = ProcesoChoiceField(queryset=ProcesoFormacion.objects.none(), label="Proceso de formación")

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["proceso"].queryset = procesos_activos(user)


class InscribirExistenteForm(EstiloBootstrapMixin, forms.Form):
    """Inscribe a una persona ya registrada (por ejemplo, de una Casa de Vida) sin duplicarla."""

    documento_identidad = forms.CharField(max_length=50, label="Documento de identidad")
    proceso = ProcesoChoiceField(queryset=ProcesoFormacion.objects.none(), label="Proceso de formación")

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["proceso"].queryset = procesos_activos(user)

    def clean(self):
        datos = super().clean()
        documento, proceso = (datos.get("documento_identidad") or "").strip(), datos.get("proceso")
        if not documento or not proceso:
            return datos
        participante = Participante.objects.filter(documento_identidad__iexact=documento).first()
        if participante is None:
            raise forms.ValidationError("No hay ningún participante con ese documento. Regístrelo como participante nuevo.")
        if not participante.activo:
            raise forms.ValidationError("El participante está desactivado; solo el Pastor puede reactivarlo.")
        if InscripcionFormacion.objects.filter(id_participante=participante, id_proceso_formacion=proceso, estado=ACTIVO).exists():
            raise forms.ValidationError(f"{participante} ya está inscrito en {proceso}.")
        datos["participante"] = participante
        return datos


def inscribir(participante, proceso):
    """Crea o reactiva la inscripción; las anteriores se conservan como historial (RN17)."""
    inscripcion, creada = InscripcionFormacion.objects.get_or_create(
        id_participante=participante, id_proceso_formacion=proceso
    )
    if not creada and inscripcion.estado != ACTIVO:
        inscripcion.estado = ACTIVO
        inscripcion.fecha_inscripcion = datetime.date.today()
        inscripcion.save(update_fields=["estado", "fecha_inscripcion"])
    return inscripcion


def inscritos_activos(proceso):
    return Participante.objects.filter(
        estado=ACTIVO,
        inscripcionformacion__id_proceso_formacion=proceso,
        inscripcionformacion__estado=ACTIVO,
    ).order_by("nombres_apellidos")


class ActividadFormacionForm(EstiloBootstrapMixin, forms.Form):
    """Actividad de un proceso con su asistencia (HU-26, HU-29, HU-32, HU-35).

    La asistencia llega como casillas 'presente_<id>' y solo cuenta para los inscritos del proceso.
    """

    titulo = forms.CharField(max_length=150, label="Nombre de la actividad")
    fecha = forms.DateField(label="Fecha", widget=forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"))
    descripcion = forms.CharField(label="Descripción", required=False, widget=forms.Textarea(attrs={"rows": 2}))

    def __init__(self, *args, proceso=None, **kwargs):
        self.proceso = proceso
        super().__init__(*args, **kwargs)
        self.fields["fecha"].initial = datetime.date.today

    def clean_titulo(self):
        return " ".join(self.cleaned_data["titulo"].split())

    def clean_fecha(self):
        fecha = self.cleaned_data["fecha"]
        if fecha > datetime.date.today():
            raise forms.ValidationError("No se puede registrar una actividad con fecha futura.")
        return fecha

    def clean(self):
        datos = super().clean()
        titulo, fecha = datos.get("titulo"), datos.get("fecha")
        if self.proceso and titulo and fecha and Actividad.objects.filter(
            id_proceso_formacion=self.proceso, fecha=fecha, titulo__iexact=titulo
        ).exists():
            raise forms.ValidationError(f"La actividad «{titulo}» del {fecha:%d/%m/%Y} ya está registrada en este proceso.")
        return datos


class SeguimientoFormacionForm(EstiloBootstrapMixin, forms.ModelForm):
    """Seguimiento de un participante dentro de un proceso (RF11, RN10, HU-36)."""

    id_proceso_formacion = ProcesoChoiceField(queryset=ProcesoFormacion.objects.none(), label="Proceso de formación")

    class Meta:
        model = Seguimiento
        fields = ["id_proceso_formacion", "id_participante", "fecha", "tipo", "estado", "observacion"]
        labels = {"id_participante": "Participante", "observacion": "Observaciones"}
        widgets = {
            "fecha": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "observacion": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        procesos = procesos_visibles(user)
        self.fields["id_proceso_formacion"].queryset = procesos.order_by("tipo_proceso", "nombre")
        self.fields["id_participante"].queryset = Participante.objects.filter(
            inscripcionformacion__id_proceso_formacion__in=procesos
        ).distinct().order_by("nombres_apellidos")

    def clean_fecha(self):
        fecha = self.cleaned_data["fecha"]
        if fecha > datetime.date.today():
            raise forms.ValidationError("La fecha del seguimiento no puede ser futura.")
        return fecha

    def clean_observacion(self):
        return self.cleaned_data["observacion"].strip()

    def clean(self):
        datos = super().clean()
        proceso, participante = datos.get("id_proceso_formacion"), datos.get("id_participante")
        if proceso and participante and not InscripcionFormacion.objects.filter(
            id_proceso_formacion=proceso, id_participante=participante
        ).exists():
            self.add_error("id_participante", "El participante no está inscrito en ese proceso.")
        return datos

    def save(self, commit=True):
        seguimiento = super().save(commit=False)
        seguimiento.tipo_modulo = TIPO_MODULO
        if commit:
            seguimiento.save()
        return seguimiento
