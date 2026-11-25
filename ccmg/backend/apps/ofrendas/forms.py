import datetime
from decimal import Decimal

from django import forms

from nucleo.utils import FECHA_MINIMA_REGISTRO, MAX_VALOR_COP
from pva.forms import EstiloBootstrapMixin, validar_fecha_registro
from pva.models import ACTIVO, CasaVida

from .models import Ofrenda


class OfrendaForm(EstiloBootstrapMixin, forms.ModelForm):
    """Fecha, valor y concepto son obligatorios; el valor debe ser mayor que cero (HU-08)."""

    id_casa_vida = forms.ModelChoiceField(
        queryset=CasaVida.objects.none(), required=False, label="Casa de Vida", empty_label="General (sin Casa de Vida)"
    )

    class Meta:
        model = Ofrenda
        fields = ["fecha", "concepto", "valor", "id_casa_vida", "observacion"]
        labels = {"valor": "Valor (COP)", "observacion": "Observaciones"}
        widgets = {
            "fecha": forms.DateInput(attrs={"type": "date", "min": FECHA_MINIMA_REGISTRO.isoformat()}, format="%Y-%m-%d"),
            "valor": forms.NumberInput(attrs={"min": "1", "max": str(MAX_VALOR_COP), "step": "1"}),
            "observacion": forms.Textarea(attrs={"rows": 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        casas = CasaVida.objects.filter(estado=ACTIVO)
        if self.instance.pk and self.instance.id_casa_vida_id:
            casas = CasaVida.objects.filter(pk=self.instance.id_casa_vida_id) | casas
        self.fields["id_casa_vida"].queryset = casas.order_by("nombre")

    def clean_fecha(self):
        fecha = self.cleaned_data["fecha"]
        if fecha > datetime.date.today():
            raise forms.ValidationError("La fecha de la ofrenda no puede ser futura.")
        return validar_fecha_registro(fecha, "la fecha de la ofrenda")

    def clean_concepto(self):
        return " ".join(self.cleaned_data["concepto"].split())

    def clean_valor(self):
        valor = self.cleaned_data["valor"]
        if valor is None or valor <= Decimal("0"):
            raise forms.ValidationError("El valor debe ser mayor que cero.")
        if valor > MAX_VALOR_COP:
            raise forms.ValidationError(f"El valor no puede superar {MAX_VALOR_COP:,} pesos.".replace(",", "."))
        return valor


class FiltroOfrendasForm(EstiloBootstrapMixin, forms.Form):
    """Consulta por rango de fechas y Casa de Vida (HU-08, criterio 3)."""

    desde = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"))
    hasta = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"))
    casa = forms.ModelChoiceField(queryset=CasaVida.objects.all(), required=False, empty_label="Todas")
    q = forms.CharField(required=False, label="Concepto")

    def clean(self):
        datos = super().clean()
        if datos.get("desde") and datos.get("hasta") and datos["desde"] > datos["hasta"]:
            raise forms.ValidationError("La fecha inicial no puede ser posterior a la final.")
        return datos
