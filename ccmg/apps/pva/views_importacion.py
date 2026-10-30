"""Importación de datos existentes, solo para el Pastor (RF26, HU-42).

Flujo: subir archivo -> vista previa con errores -> confirmar -> resumen. Mientras tanto,
las filas leídas se guardan en la sesión; nada se escribe en la base hasta la confirmación.
"""
from django import forms
from django.contrib import messages
from django.http import Http404, HttpResponse
from django.shortcuts import redirect
from django.views.generic import FormView, TemplateView, View

from nucleo.mixins import PastorRequiredMixin

from . import importacion
from .views import PastorCasasMixin

CLAVE_SESION = "importacion_pva"


class SubirArchivoForm(forms.Form):
    tipo = forms.ChoiceField(
        label="¿Qué va a importar?",
        choices=[("casas", "Casas de Vida"), ("participantes", "Participantes")],
        widget=forms.RadioSelect,
        initial="participantes",
    )
    archivo = forms.FileField(
        label="Archivo CSV o Excel (.xlsx)",
        widget=forms.ClearableFileInput(attrs={"accept": ".csv,.xlsx", "class": "form-control"}),
    )


def _con_valores(tipo, resultados):
    """Agrega a cada fila sus valores en el orden de las columnas de la plantilla."""
    claves = [c[0] for c in importacion.COLUMNAS[tipo]]
    return [{**r, "valores": [r["datos"].get(clave, "") for clave in claves]} for r in resultados]


def _importacion(request):
    datos = request.session.get(CLAVE_SESION)
    if not datos:
        raise Http404
    return datos


class ImportarView(PastorCasasMixin, FormView):
    template_name = "pva/importar.html"
    form_class = SubirArchivoForm
    seccion = "importar"

    def get_initial(self):
        tipo = self.request.GET.get("tipo")
        return {"tipo": tipo} if tipo in importacion.COLUMNAS else {}

    def form_valid(self, form):
        tipo, archivo = form.cleaned_data["tipo"], form.cleaned_data["archivo"]
        try:
            filas = importacion.leer_archivo(tipo, archivo)
        except importacion.ErrorArchivo as e:
            form.add_error("archivo", str(e))
            return self.form_invalid(form)
        self.request.session[CLAVE_SESION] = {
            "tipo": tipo,
            "archivo": archivo.name,
            "filas": filas,
            "resultados": importacion.validar(tipo, filas),
            "confirmada": False,
        }
        return redirect("pva:importar_vista_previa")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["columnas"] = importacion.COLUMNAS
        return ctx


class VistaPreviaView(PastorCasasMixin, TemplateView):
    """Muestra cada fila con su estado antes de guardar (HU-42, criterio 2)."""

    template_name = "pva/importar_vista_previa.html"
    seccion = "importar"

    def get(self, request, *args, **kwargs):
        if _importacion(request).get("confirmada"):
            return redirect("pva:importar_resultado")
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        datos = _importacion(self.request)
        ctx.update(
            tipo=datos["tipo"],
            titulo_tipo=importacion.TITULOS[datos["tipo"]],
            archivo=datos["archivo"],
            resultados=_con_valores(datos["tipo"], datos["resultados"]),
            conteo=importacion.contar(datos["resultados"]),
            columnas=importacion.COLUMNAS[datos["tipo"]],
        )
        return ctx

    def post(self, request, *args, **kwargs):
        datos = _importacion(request)
        if datos.get("confirmada"):
            return redirect("pva:importar_resultado")
        resultados = importacion.importar(datos["tipo"], datos["filas"], request)
        datos.update(resultados=resultados, confirmada=True)
        request.session[CLAVE_SESION] = datos
        conteo = importacion.contar(resultados)
        messages.success(request, f"Importación completada: {conteo['validas']} registros importados.")
        return redirect("pva:importar_resultado")


class ResultadoView(PastorCasasMixin, TemplateView):
    """Resumen de importados, omitidos y con error (salida de RF26)."""

    template_name = "pva/importar_resultado.html"
    seccion = "importar"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        datos = _importacion(self.request)
        if not datos.get("confirmada"):
            raise Http404
        ctx.update(
            tipo=datos["tipo"],
            titulo_tipo=importacion.TITULOS[datos["tipo"]],
            archivo=datos["archivo"],
            conteo=importacion.contar(datos["resultados"]),
            problemas=_con_valores(datos["tipo"], [r for r in datos["resultados"] if r["estado"] != importacion.VALIDA]),
            columnas=importacion.COLUMNAS[datos["tipo"]],
        )
        return ctx


class DetalleErroresView(PastorRequiredMixin, View):
    def get(self, request):
        datos = _importacion(request)
        respuesta = HttpResponse(importacion.detalle_csv(datos["tipo"], datos["resultados"]), content_type="text/csv; charset=utf-8")
        respuesta["Content-Disposition"] = f'attachment; filename="detalle_importacion_{datos["tipo"]}.csv"'
        return respuesta


class PlantillaView(PastorRequiredMixin, View):
    def get(self, request, tipo):
        if tipo not in importacion.COLUMNAS:
            raise Http404
        respuesta = HttpResponse(
            importacion.plantilla_xlsx(tipo),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        respuesta["Content-Disposition"] = f'attachment; filename="plantilla_{tipo}.xlsx"'
        return respuesta
