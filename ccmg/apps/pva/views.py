import datetime

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import Count, Prefetch, Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.generic import CreateView, DetailView, FormView, ListView, UpdateView, View

from nucleo.mixins import ModuleRequiredMixin, PastorRequiredMixin
from nucleo.permissions import module_required
from nucleo.utils import (
    ROLES_APOYO,
    ROLES_LIDER,
    ROLES_PASTOR,
    ROLES_SUPERVISOR,
    registrar_auditoria,
    sesion_js,
)

from .alcance import (
    actividades_visibles,
    casa_para_reportar,
    casas_visibles,
    es_pastor,
    participantes_visibles,
    rol_de,
)
from .forms import AreaForm, CasaVidaForm, ParticipanteForm, RegistroAsistenciaForm
from .models import (
    ACTIVO,
    INACTIVO,
    Actividad,
    Area,
    Asistencia,
    CasaVida,
    CasaVidaEquipo,
    CasaVidaMiembro,
    Participante,
)

ROLES_NOMBRE = {
    ROLES_PASTOR: "Pastor",
    ROLES_SUPERVISOR: "Supervisor de Área",
    ROLES_LIDER: "Líder de Casa de Vida",
    ROLES_APOYO: "Usuario de apoyo",
}


def menu_casas(user, seccion):
    """Menú lateral del módulo según el rol. Las secciones aún no migradas viven en el panel JS."""
    rol = rol_de(user)
    panel = reverse("pva:panel")
    todos = [ROLES_PASTOR, ROLES_SUPERVISOR, ROLES_LIDER, ROLES_APOYO]
    items = [
        ("inicio", "Inicio", "speedometer2", panel + "#inicio", todos),
        ("participantes", "Participantes", "people", reverse("pva:participantes"), todos),
        ("casas", "Casas de Vida", "houses", reverse("pva:casas"), todos),
        ("areas", "Áreas", "map", reverse("pva:areas"), [ROLES_PASTOR]),
        ("asistencia", "Asistencia", "check2-square", reverse("pva:asistencia"), todos),
        ("seguimiento", "Seguimiento", "clipboard-check", panel + "#seguimiento", [ROLES_PASTOR, ROLES_SUPERVISOR, ROLES_LIDER]),
        ("ofrendas", "Ofrendas", "cash-coin", panel + "#ofrendas", [ROLES_PASTOR]),
        ("reportes", "Reportes", "file-earmark-text", panel + "#reportes", todos),
        ("perfil", "Mi perfil", "person-circle", panel + "#perfil", todos),
    ]
    return [
        {"id": i, "t": t, "icono": ic, "url": url, "activo": i == seccion}
        for i, t, ic, url, roles in items
        if rol in roles
    ]


class PanelCasasMixin(ModuleRequiredMixin):
    """Vistas del módulo Casas de Vida: exige acceso al módulo y arma el menú lateral."""

    required_module = "CASAS_VIDA"
    seccion = None

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        ctx["menu"] = menu_casas(user, self.seccion)
        ctx["rol_nombre"] = ROLES_NOMBRE.get(rol_de(user), "")
        ctx["es_pastor"] = es_pastor(user)
        return ctx


class PastorCasasMixin(PastorRequiredMixin, PanelCasasMixin):
    """Solo el Pastor crea, modifica, asigna y desactiva (RN20, RN24)."""


class CambiarEstadoView(PastorRequiredMixin, View):
    """Baja lógica y reactivación de registros (RF28, RN24)."""

    model = None
    url_retorno = None
    nombre = ""

    def validar_desactivacion(self, obj):
        return None

    def despues_de_cambiar(self, obj, nuevo_estado):
        pass

    def post(self, request, pk, accion):
        if accion not in ("activar", "desactivar"):
            raise Http404
        obj = get_object_or_404(self.model, pk=pk)
        nuevo = INACTIVO if accion == "desactivar" else ACTIVO
        if nuevo == INACTIVO:
            error = self.validar_desactivacion(obj)
            if error:
                messages.error(request, error)
                return redirect(self.url_retorno)
        with transaction.atomic():
            obj.estado = nuevo
            obj.save(update_fields=["estado"])
            self.despues_de_cambiar(obj, nuevo)
            registrar_auditoria(request, "DESACTIVAR" if nuevo == INACTIVO else "REACTIVAR", obj)
        verbo = "desactivado" if nuevo == INACTIVO else "reactivado"
        messages.success(request, f"{self.nombre} «{obj}» {verbo} correctamente.")
        siguiente = request.POST.get("next", "")
        if not url_has_allowed_host_and_scheme(siguiente, allowed_hosts={request.get_host()}):
            siguiente = self.url_retorno
        return redirect(siguiente)


# ----------------------------------------------------------------- Panel


@module_required("CASAS_VIDA")
def panel_casas(request):
    user = request.user
    casas = casas_visibles(user)
    actividades = actividades_visibles(user).annotate(
        presentes=Count("asistencia", filter=Q(asistencia__presente=True)),
        total=Count("asistencia"),
    ).order_by("-fecha", "-id_actividad")
    total_presentes = sum(a.presentes for a in actividades)
    total_registros = sum(a.total for a in actividades)
    resumen = {
        "participantes": participantes_visibles(user).filter(estado=ACTIVO).count(),
        "casas": casas.count(),
        "casasActivas": casas.filter(estado=ACTIVO).count(),
        "asistenciaPromedio": round(total_presentes * 100 / total_registros) if total_registros else 0,
        "actividades": [
            {"casa": a.id_casa_vida.nombre, "fecha": a.fecha.isoformat(), "tipo": a.titulo, "asistentes": a.presentes}
            for a in actividades[:4]
        ],
    }
    return render(
        request,
        "panel-casas-vida.html",
        {
            "user": user,
            "sesion_js": sesion_js(user),
            "resumen_pva": resumen,
            "urls_pva": {
                "participantes": reverse("pva:participantes"),
                "casas": reverse("pva:casas"),
                "areas": reverse("pva:areas"),
                "asistencia": reverse("pva:asistencia"),
            },
        },
    )


# ----------------------------------------------------------------- Áreas


class AreaListView(PastorCasasMixin, ListView):
    template_name = "pva/areas_lista.html"
    context_object_name = "areas"
    seccion = "areas"

    def get_queryset(self):
        return Area.objects.select_related("id_supervisor").annotate(
            casas_activas=Count("casavida", filter=Q(casavida__estado=ACTIVO))
        ).order_by("nombre")


class AreaFormMixin(PastorCasasMixin):
    model = Area
    form_class = AreaForm
    template_name = "pva/formulario.html"
    success_url = reverse_lazy("pva:areas")
    seccion = "areas"

    def form_valid(self, form):
        with transaction.atomic():
            area = form.save()
            # Las casas del Área heredan su Supervisor (RN03).
            CasaVida.objects.filter(id_area=area).update(id_supervisor=area.id_supervisor)
            registrar_auditoria(self.request, self.accion, area)
        messages.success(self.request, self.mensaje)
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(titulo=self.titulo, volver=self.success_url)
        return ctx


class AreaCreateView(AreaFormMixin, CreateView):
    titulo = "Nueva Área"
    accion = "CREAR"
    mensaje = "Área creada correctamente."


class AreaUpdateView(AreaFormMixin, UpdateView):
    titulo = "Editar Área"
    accion = "ACTUALIZAR"
    mensaje = "Área actualizada correctamente."


class AreaEstadoView(CambiarEstadoView):
    model = Area
    url_retorno = reverse_lazy("pva:areas")
    nombre = "Área"

    def validar_desactivacion(self, area):
        if CasaVida.objects.filter(id_area=area, estado=ACTIVO).exists():
            return "No se puede desactivar un Área con Casas de Vida activas. Reasígnelas o desactívelas primero."
        return None


# ----------------------------------------------------------------- Casas de Vida


class CasaListView(PanelCasasMixin, ListView):
    template_name = "pva/casas_lista.html"
    context_object_name = "casas"
    seccion = "casas"

    def get_queryset(self):
        qs = casas_visibles(self.request.user)
        if not es_pastor(self.request.user):
            qs = qs.filter(estado=ACTIVO)
        area = self.request.GET.get("area")
        if area and area.isdigit():
            qs = qs.filter(id_area=area)
        return qs.annotate(
            miembros=Count(
                "casavidamiembro",
                filter=Q(casavidamiembro__estado=ACTIVO, casavidamiembro__id_participante__estado=ACTIVO),
            )
        ).order_by("nombre")


class CasaDetailView(PanelCasasMixin, DetailView):
    """Consulta de una Casa de Vida: solo lectura para quien no es Pastor (RF08, RN03, RN04)."""

    template_name = "pva/casa_detalle.html"
    context_object_name = "casa"
    seccion = "casas"

    def get_queryset(self):
        qs = casas_visibles(self.request.user)
        if not es_pastor(self.request.user):
            qs = qs.filter(estado=ACTIVO)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        casa = self.object
        ctx["miembros"] = Participante.objects.filter(
            estado=ACTIVO,
            casavidamiembro__id_casa_vida=casa,
            casavidamiembro__estado=ACTIVO,
        )
        ctx["equipo"] = CasaVidaEquipo.objects.filter(id_casa_vida=casa, activo=True).select_related("id_usuario")
        ctx["actividades"] = (
            Actividad.objects.filter(id_casa_vida=casa)
            .annotate(presentes=Count("asistencia", filter=Q(asistencia__presente=True)), total=Count("asistencia"))
            .select_related("id_responsable")
            .order_by("-fecha", "-id_actividad")[:5]
        )
        return ctx


class CasaFormMixin(PastorCasasMixin):
    model = CasaVida
    form_class = CasaVidaForm
    template_name = "pva/formulario.html"
    seccion = "casas"

    def form_valid(self, form):
        with transaction.atomic():
            casa = form.save()
            registrar_auditoria(self.request, self.accion, casa)
        messages.success(self.request, self.mensaje)
        return redirect("pva:casa_detalle", pk=casa.pk)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(titulo=self.titulo, volver=reverse("pva:casas"))
        if not Area.objects.filter(estado=ACTIVO).exists():
            ctx["aviso"] = "Primero registre al menos un Área activa para poder asignar la Casa de Vida."
        return ctx


class CasaCreateView(CasaFormMixin, CreateView):
    titulo = "Nueva Casa de Vida"
    accion = "CREAR"
    mensaje = "Casa de Vida creada correctamente."


class CasaUpdateView(CasaFormMixin, UpdateView):
    titulo = "Editar Casa de Vida"
    accion = "ACTUALIZAR"
    mensaje = "Casa de Vida actualizada correctamente."


class CasaEstadoView(CambiarEstadoView):
    model = CasaVida
    url_retorno = reverse_lazy("pva:casas")
    nombre = "Casa de Vida"


# ----------------------------------------------------------------- Participantes


def _con_casa_actual(qs):
    return qs.prefetch_related(
        Prefetch(
            "casavidamiembro_set",
            queryset=CasaVidaMiembro.objects.filter(estado=ACTIVO).select_related("id_casa_vida"),
            to_attr="membresias",
        )
    )


class ParticipanteListView(PanelCasasMixin, ListView):
    template_name = "pva/participantes_lista.html"
    context_object_name = "participantes"
    paginate_by = 25
    seccion = "participantes"

    def get_queryset(self):
        user = self.request.user
        qs = participantes_visibles(user)
        g = self.request.GET
        q = g.get("q", "").strip()
        if q:
            qs = qs.filter(Q(nombres_apellidos__icontains=q) | Q(documento_identidad__icontains=q))
        casa = g.get("casa")
        if casa and casa.isdigit():
            qs = qs.filter(casavidamiembro__id_casa_vida=casa, casavidamiembro__estado=ACTIVO)
        if es_pastor(user) and g.get("estado") in (ACTIVO, INACTIVO):
            qs = qs.filter(estado=g["estado"])
        return _con_casa_actual(qs.distinct().order_by("nombres_apellidos"))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["casas_filtro"] = casas_visibles(self.request.user)
        ctx["filtros"] = self.request.GET
        params = self.request.GET.copy()
        params.pop("page", None)
        ctx["query_sin_pagina"] = params.urlencode()
        return ctx


class ParticipanteDetailView(PanelCasasMixin, DetailView):
    template_name = "pva/participante_detalle.html"
    context_object_name = "participante"
    seccion = "participantes"

    def get_queryset(self):
        return participantes_visibles(self.request.user)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        p = self.object
        ctx["historial_casas"] = p.casavidamiembro_set.select_related("id_casa_vida").order_by("-fecha_ingreso")
        ctx["asistencias"] = (
            Asistencia.objects.filter(id_participante=p, id_actividad__in=actividades_visibles(self.request.user))
            .select_related("id_actividad", "id_actividad__id_casa_vida")
            .order_by("-id_actividad__fecha")[:10]
        )
        return ctx


def asignar_casa(participante, casa):
    """Deja una sola membresía activa; la anterior se conserva como historial (RN17)."""
    actual = participante.membresia_activa
    if actual and actual.id_casa_vida_id == casa.pk:
        return
    CasaVidaMiembro.objects.filter(id_participante=participante, estado=ACTIVO).update(estado=INACTIVO)
    membresia, creada = CasaVidaMiembro.objects.get_or_create(
        id_casa_vida=casa, id_participante=participante
    )
    if not creada:
        membresia.estado = ACTIVO
        membresia.fecha_ingreso = datetime.date.today()
        membresia.save(update_fields=["estado", "fecha_ingreso"])


class ParticipanteFormMixin(PastorCasasMixin):
    model = Participante
    form_class = ParticipanteForm
    template_name = "pva/formulario.html"
    seccion = "participantes"

    def form_valid(self, form):
        with transaction.atomic():
            participante = form.save()
            asignar_casa(participante, form.cleaned_data["casa_vida"])
            registrar_auditoria(self.request, self.accion, participante)
        messages.success(self.request, self.mensaje)
        return redirect("pva:participante_detalle", pk=participante.pk)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(titulo=self.titulo, volver=reverse("pva:participantes"))
        if not CasaVida.objects.filter(estado=ACTIVO).exists():
            ctx["aviso"] = "Primero registre al menos una Casa de Vida activa para asociar al participante."
        return ctx


class ParticipanteCreateView(ParticipanteFormMixin, CreateView):
    titulo = "Nuevo participante"
    accion = "CREAR"
    mensaje = "Participante registrado correctamente."


class ParticipanteUpdateView(ParticipanteFormMixin, UpdateView):
    titulo = "Editar participante"
    accion = "ACTUALIZAR"
    mensaje = "Participante actualizado correctamente."


class ParticipanteEstadoView(CambiarEstadoView):
    model = Participante
    url_retorno = reverse_lazy("pva:participantes")
    nombre = "Participante"


# ----------------------------------------------------------------- Asistencia


class AsistenciaListView(PanelCasasMixin, ListView):
    """Consulta de asistencia según el alcance del rol (RF10)."""

    template_name = "pva/asistencia_lista.html"
    context_object_name = "actividades"
    paginate_by = 20
    seccion = "asistencia"

    def get_queryset(self):
        qs = actividades_visibles(self.request.user)
        g = self.request.GET
        casa = g.get("casa")
        if casa and casa.isdigit():
            qs = qs.filter(id_casa_vida=casa)
        for campo, lookup in (("desde", "fecha__gte"), ("hasta", "fecha__lte")):
            try:
                qs = qs.filter(**{lookup: datetime.date.fromisoformat(g.get(campo, ""))})
            except ValueError:
                pass
        return qs.annotate(
            presentes=Count("asistencia", filter=Q(asistencia__presente=True)),
            total=Count("asistencia"),
        ).order_by("-fecha", "-id_actividad")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["casas_filtro"] = casas_visibles(self.request.user)
        ctx["filtros"] = self.request.GET
        ctx["casa_reporte"] = casa_para_reportar(self.request.user)
        params = self.request.GET.copy()
        params.pop("page", None)
        ctx["query_sin_pagina"] = params.urlencode()
        return ctx


class AsistenciaDetailView(PanelCasasMixin, DetailView):
    template_name = "pva/asistencia_detalle.html"
    context_object_name = "actividad"
    seccion = "asistencia"

    def get_queryset(self):
        return actividades_visibles(self.request.user)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["asistencias"] = (
            self.object.asistencia_set.select_related("id_participante")
            .order_by("id_participante__nombres_apellidos")
        )
        ctx["presentes"] = sum(1 for a in ctx["asistencias"] if a.presente)
        return ctx


class RegistrarAsistenciaView(PanelCasasMixin, FormView):
    """El Líder y los usuarios de apoyo registran la asistencia de su Casa de Vida (RF09, RN05, RN08)."""

    template_name = "pva/asistencia_registrar.html"
    form_class = RegistroAsistenciaForm
    seccion = "asistencia"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and rol_de(request.user) not in (ROLES_LIDER, ROLES_APOYO):
            raise PermissionDenied("Solo el Líder y los usuarios de apoyo registran asistencia.")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if self.casa is None:
            messages.error(request, "No tienes una Casa de Vida activa asignada para registrar asistencia.")
            return redirect("pva:asistencia")
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.casa is None:
            messages.error(request, "No tienes una Casa de Vida activa asignada para registrar asistencia.")
            return redirect("pva:asistencia")
        return super().post(request, *args, **kwargs)

    @property
    def casa(self):
        if not hasattr(self, "_casa"):
            self._casa = casa_para_reportar(self.request.user)
        return self._casa

    def miembros(self):
        return Participante.objects.filter(
            estado=ACTIVO,
            casavidamiembro__id_casa_vida=self.casa,
            casavidamiembro__estado=ACTIVO,
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["casa"] = self.casa
        return kwargs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["casa"] = self.casa
        ctx["miembros"] = self.miembros()
        marcados = self.request.POST if self.request.method == "POST" else None
        ctx["marcados"] = {
            p.pk for p in ctx["miembros"] if marcados is None or marcados.get(f"presente_{p.pk}")
        }
        return ctx

    def form_valid(self, form):
        miembros = list(self.miembros())
        if not miembros:
            form.add_error(None, "La Casa de Vida no tiene participantes activos para registrar asistencia.")
            return self.form_invalid(form)
        user = self.request.user
        with transaction.atomic():
            actividad = Actividad.objects.create(
                tipo_modulo=Actividad.TIPO_CASA_VIDA,
                id_casa_vida=self.casa,
                titulo=form.cleaned_data["titulo"],
                fecha=form.cleaned_data["fecha"],
                descripcion=form.cleaned_data["descripcion"] or None,
                id_responsable=user,
            )
            Asistencia.objects.bulk_create(
                Asistencia(
                    id_actividad=actividad,
                    id_participante=p,
                    presente=bool(self.request.POST.get(f"presente_{p.pk}")),
                    registrado_por=user,
                )
                for p in miembros
            )
            registrar_auditoria(self.request, "REGISTRAR_ASISTENCIA", actividad)
        presentes = sum(1 for p in miembros if self.request.POST.get(f"presente_{p.pk}"))
        messages.success(self.request, f"Asistencia registrada: {presentes} de {len(miembros)} presentes.")
        return redirect("pva:asistencia_detalle", pk=actividad.pk)
