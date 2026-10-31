"""Seguimiento de participantes (RF11, RN10)."""
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, ListView, UpdateView

from nucleo.utils import ROLES_LIDER, ROLES_PASTOR, ROLES_SUPERVISOR, registrar_auditoria

from .alcance import rol_de, seguimientos_visibles
from .forms import SeguimientoForm
from .models import Actividad, Participante, Seguimiento
from .views import PanelCasasMixin, PastorCasasMixin


class SeguimientoListView(PanelCasasMixin, ListView):
    """Pastor, Supervisor de Área y Líder consultan el seguimiento de su alcance."""

    template_name = "pva/seguimientos_lista.html"
    context_object_name = "seguimientos"
    paginate_by = 25
    seccion = "seguimiento"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and rol_de(request.user) not in (ROLES_PASTOR, ROLES_SUPERVISOR, ROLES_LIDER):
            raise PermissionDenied("Tu rol no consulta el seguimiento de participantes.")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = seguimientos_visibles(self.request.user)
        g = self.request.GET
        q = g.get("q", "").strip()
        if q:
            qs = qs.filter(Q(id_participante__nombres_apellidos__icontains=q) | Q(observacion__icontains=q))
        if g.get("estado") in dict(Seguimiento.ESTADOS):
            qs = qs.filter(estado=g["estado"])
        if g.get("tipo") in dict(Seguimiento.TIPOS):
            qs = qs.filter(tipo=g["tipo"])
        participante = g.get("participante")
        if participante and participante.isdigit():
            qs = qs.filter(id_participante=participante)
        return qs.order_by("-fecha", "-id_seguimiento")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["filtros"] = self.request.GET
        ctx["estados"] = Seguimiento.ESTADOS
        ctx["tipos"] = Seguimiento.TIPOS
        params = self.request.GET.copy()
        params.pop("page", None)
        ctx["query_sin_pagina"] = params.urlencode()
        return ctx


class SeguimientoFormMixin(PastorCasasMixin):
    model = Seguimiento
    form_class = SeguimientoForm
    template_name = "pva/formulario.html"
    seccion = "seguimiento"

    def get_success_url(self):
        return reverse("pva:participante_detalle", args=[self.object.id_participante_id])

    def form_valid(self, form):
        with transaction.atomic():
            seguimiento = form.save(commit=False)
            if not seguimiento.pk:
                seguimiento.id_usuario = self.request.user
                seguimiento.tipo_modulo = Actividad.TIPO_CASA_VIDA
            seguimiento.save()
            registrar_auditoria(self.request, self.accion, seguimiento)
        self.object = seguimiento
        messages.success(self.request, self.mensaje)
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(titulo=self.titulo, volver=reverse("pva:seguimientos"))
        return ctx


class SeguimientoCreateView(SeguimientoFormMixin, CreateView):
    titulo = "Nuevo seguimiento"
    accion = "CREAR"
    mensaje = "Seguimiento registrado correctamente."

    def get_initial(self):
        inicial = super().get_initial()
        participante = self.request.GET.get("participante")
        if participante and participante.isdigit() and Participante.objects.filter(pk=participante).exists():
            inicial["id_participante"] = participante
        return inicial


class SeguimientoUpdateView(SeguimientoFormMixin, UpdateView):
    titulo = "Editar seguimiento"
    accion = "ACTUALIZAR"
    mensaje = "Seguimiento actualizado correctamente."

    def get_queryset(self):
        return Seguimiento.objects.filter(tipo_modulo=Actividad.TIPO_CASA_VIDA)
