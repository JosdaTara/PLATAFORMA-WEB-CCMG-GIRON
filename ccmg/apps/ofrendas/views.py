"""Gestión de ofrendas: solo el Pastor o el responsable que él autorice (RF17, RN14)."""
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import Count, Sum
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from nucleo import exportar
from nucleo.permissions import puede_gestionar_ofrendas
from nucleo.utils import registrar_auditoria, rol_real
from pva.alcance import es_pastor, rol_de
from pva.views import ROLES_NOMBRE, menu_casas

from .forms import FiltroOfrendasForm, OfrendaForm
from .models import Ofrenda


class OfrendasMixin(LoginRequiredMixin):
    """Acceso al módulo de ofrendas y barra lateral según el módulo del usuario."""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and not puede_gestionar_ofrendas(request.user):
            raise PermissionDenied("Solo el Pastor o el responsable de ofrendas acceden a este módulo.")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        if getattr(user.rol, "acceso_casas_vida", False):
            ctx["menu"] = menu_casas(user, "ofrendas")
        else:
            # Responsable de ofrendas fuera del módulo Casas de Vida (p. ej. Coordinador de Formación).
            ctx["menu"] = [
                {"id": "ofrendas", "t": "Ofrendas", "icono": "cash-coin", "url": reverse("ofrendas:index"), "activo": True},
                {"id": "panel", "t": "Mi panel", "icono": "arrow-left", "url": reverse("cuentas:panel_por_rol"), "activo": False},
            ]
        ctx["rol_nombre"] = ROLES_NOMBRE.get(rol_real(user), "Responsable de ofrendas")
        ctx["es_pastor"] = es_pastor(user)
        return ctx


class OfrendaListView(exportar.ExportableMixin, OfrendasMixin, ListView):
    template_name = "ofrendas/lista.html"
    context_object_name = "ofrendas"
    paginate_by = 25

    def get_queryset(self):
        qs = Ofrenda.objects.select_related("id_casa_vida", "id_usuario_registro")
        self.filtro = FiltroOfrendasForm(self.request.GET or None)
        if self.filtro.is_bound and self.filtro.is_valid():
            d = self.filtro.cleaned_data
            if d["desde"]:
                qs = qs.filter(fecha__gte=d["desde"])
            if d["hasta"]:
                qs = qs.filter(fecha__lte=d["hasta"])
            if d["casa"]:
                qs = qs.filter(id_casa_vida=d["casa"])
            if d["q"]:
                qs = qs.filter(concepto__icontains=d["q"].strip())
        return qs.order_by("-fecha", "-id_ofrenda")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        totales = self.object_list.aggregate(total=Sum("valor"), cantidad=Count("id_ofrenda"))
        ctx["total"] = totales["total"] or 0
        ctx["cantidad"] = totales["cantidad"]
        ctx["filtro"] = self.filtro
        params = self.request.GET.copy()
        params.pop("page", None)
        ctx["query_sin_pagina"] = params.urlencode()
        return ctx

    def documento_exportable(self, ctx):
        d = self.filtro.cleaned_data if self.filtro.is_bound and self.filtro.is_valid() else {}
        desde, hasta = d.get("desde"), d.get("hasta")
        if desde or hasta:
            periodo = f"{desde:%d/%m/%Y}" if desde else "Desde el inicio"
            periodo += f" al {hasta:%d/%m/%Y}" if hasta else " a la fecha"
        else:
            periodo = "Todas las fechas"
        ofrendas = self.object_list  # todas las filas filtradas, no solo la página visible
        return exportar.Documento(
            titulo="Ofrendas",
            periodo=periodo,
            datos=[("Casa de Vida", d.get("casa") or "Todas"), ("Concepto", d.get("q") or "Todos"),
                   ("Registros", ctx["cantidad"])],
            tablas=[exportar.Tabla(
                "Ofrendas registradas",
                [("Fecha", exportar.FECHA), ("Concepto", exportar.TEXTO), ("Casa de Vida", exportar.TEXTO),
                 ("Valor", exportar.PESOS), ("Registró", exportar.TEXTO), ("Observaciones", exportar.TEXTO)],
                [[o.fecha, o.concepto, o.id_casa_vida.nombre if o.id_casa_vida_id else "General", o.valor,
                  o.id_usuario_registro.nombre_completo if o.id_usuario_registro_id else "", o.observacion or ""]
                 for o in ofrendas],
                total=["Total", "", "", ctx["total"], "", ""],
            )],
            nombre_archivo="ofrendas",
        )


class OfrendaFormMixin(OfrendasMixin):
    model = Ofrenda
    form_class = OfrendaForm
    template_name = "ofrendas/formulario.html"
    success_url = reverse_lazy("ofrendas:index")

    def form_valid(self, form):
        with transaction.atomic():
            ofrenda = form.save(commit=False)
            if ofrenda.pk:
                ofrenda.modificado_por = self.request.user
            else:
                ofrenda.id_usuario_registro = self.request.user
            ofrenda.save()
            registrar_auditoria(self.request, self.accion, ofrenda)
        messages.success(self.request, self.mensaje)
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(titulo=self.titulo, volver=self.success_url)
        return ctx


class OfrendaCreateView(OfrendaFormMixin, CreateView):
    titulo = "Registrar ofrenda"
    accion = "CREAR"
    mensaje = "Ofrenda registrada correctamente."


class OfrendaUpdateView(OfrendaFormMixin, UpdateView):
    titulo = "Editar ofrenda"
    accion = "ACTUALIZAR"
    mensaje = "Ofrenda actualizada correctamente."
