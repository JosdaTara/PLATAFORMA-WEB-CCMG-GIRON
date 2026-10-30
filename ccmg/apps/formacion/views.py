"""Módulo Escuelas de Formación: Pasos de Vida, Escuelas Vida, Módulos de Liderazgo y Misiones (RF18–RF22)."""
import datetime

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import Count, Prefetch, Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, FormView, ListView, TemplateView, UpdateView, View

from nucleo import exportar
from nucleo.mixins import ModuleRequiredMixin
from nucleo.permissions import module_required, puede_gestionar_ofrendas
from nucleo.utils import ROLES_COORD, ROLES_ETIQUETA, ROLES_PASTOR, es_superadmin, registrar_auditoria, rol_real, sesion_js
from pva import periodos
from pva.alcance import es_pastor, rol_de
from pva.forms import GenerarReporteForm
from pva.models import ACTIVO, INACTIVO, Actividad, Asistencia, Participante, Seguimiento
from pva.views import CambiarEstadoView

from .alcance import (
    TIPO_MODULO,
    actividades_formacion,
    participantes_formacion,
    procesos_visibles,
    seguimientos_formacion,
)
from .forms import (
    ActividadFormacionForm,
    DatosParticipanteForm,
    InscribirExistenteForm,
    NuevoParticipanteFormacionForm,
    ProcesoForm,
    SeguimientoFormacionForm,
    inscribir,
    inscritos_activos,
)
from .models import InscripcionFormacion, ProcesoFormacion

ROLES_NOMBRE = ROLES_ETIQUETA


def menu_formacion(user, seccion):
    panel = reverse("formacion:panel")
    items = [
        ("inicio", "Inicio", "speedometer2", panel + "#inicio"),
        ("procesos", "Procesos de formación", "mortarboard", reverse("formacion:procesos")),
        ("participantes", "Participantes", "people", reverse("formacion:participantes")),
        ("asistencia", "Actividades y asistencia", "check2-square", reverse("formacion:actividades")),
        ("seguimiento", "Seguimiento", "clipboard-check", reverse("formacion:seguimientos")),
        ("reportes", "Reportes", "file-earmark-text", reverse("formacion:reportes")),
    ]
    if puede_gestionar_ofrendas(user):
        items.append(("ofrendas", "Ofrendas", "cash-coin", reverse("ofrendas:index")))
    if es_pastor(user):
        items.append(("usuarios", "Usuarios", "person-gear", reverse("cuentas:usuarios_list")))
    if es_superadmin(user):
        items.append(("auditoria", "Auditoría", "journal-text", reverse("cuentas:auditoria")))
    items.append(("perfil", "Mi perfil", "person-circle", panel + "#perfil"))
    return [{"id": i, "t": t, "icono": ic, "url": url, "activo": i == seccion} for i, t, ic, url in items]


class PanelFormacionMixin(ModuleRequiredMixin):
    """Acceso al módulo (Pastor y Coordinador de Formación) y barra lateral."""

    required_module = "ESCUELAS_FORMACION"
    seccion = None

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and rol_de(request.user) not in (ROLES_PASTOR, ROLES_COORD):
            raise PermissionDenied("No tienes acceso al módulo Escuelas de Formación.")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        ctx["menu"] = menu_formacion(user, self.seccion)
        ctx["rol_nombre"] = ROLES_NOMBRE.get(rol_real(user), "")
        ctx["es_pastor"] = es_pastor(user)
        return ctx


def _con_porcentaje(presentes, registros):
    return round(presentes * 100 / registros) if registros else None


def _anotar_asistencia(qs):
    return qs.annotate(
        presentes=Count("asistencia", filter=Q(asistencia__presente=True)),
        total=Count("asistencia"),
    )


# ----------------------------------------------------------------- Panel


@module_required("ESCUELAS_FORMACION")
def panel_escuelas(request):
    user = request.user
    if rol_de(user) not in (ROLES_PASTOR, ROLES_COORD):
        raise PermissionDenied("No tienes acceso al módulo Escuelas de Formación.")
    procesos = procesos_visibles(user)
    actividades = _anotar_asistencia(actividades_formacion(user)).order_by("-fecha", "-id_actividad")
    presentes = sum(a.presentes for a in actividades)
    registros = sum(a.total for a in actividades)
    resumen = {
        "procesosActivos": procesos.filter(estado=ACTIVO).count(),
        "inscritos": InscripcionFormacion.objects.filter(
            id_proceso_formacion__in=procesos, estado=ACTIVO, id_participante__estado=ACTIVO
        ).count(),
        "asistenciaPromedio": _con_porcentaje(presentes, registros) or 0,
        "seguimientosAbiertos": seguimientos_formacion(user).exclude(estado="CERRADO").count(),
        "procesos": [
            {"nombre": p.nombre, "tipo": p.get_tipo_proceso_display(), "activo": p.activo}
            for p in procesos.order_by("estado", "tipo_proceso", "nombre")[:6]
        ],
        "actividades": [
            {"proceso": a.id_proceso_formacion.nombre, "fecha": a.fecha.isoformat(), "asistentes": a.presentes}
            for a in actividades[:4]
        ],
    }
    return render(
        request,
        "formacion/panel.html",
        {"user": user, "sesion_js": sesion_js(user), "resumen_formacion": resumen,
         "urls_formacion": {m["id"]: m["url"] for m in menu_formacion(user, None)}},
    )


# ----------------------------------------------------------------- Procesos


class ProcesoListView(PanelFormacionMixin, ListView):
    template_name = "formacion/procesos_lista.html"
    context_object_name = "procesos"
    seccion = "procesos"

    def get_queryset(self):
        qs = procesos_visibles(self.request.user)
        tipo = self.request.GET.get("tipo")
        if tipo in dict(ProcesoFormacion.TIPOS):
            qs = qs.filter(tipo_proceso=tipo)
        return qs.annotate(
            inscritos=Count(
                "inscripcionformacion",
                filter=Q(inscripcionformacion__estado=ACTIVO, inscripcionformacion__id_participante__estado=ACTIVO),
                distinct=True,
            ),
            actividades=Count("actividad", distinct=True),
        ).order_by("estado", "tipo_proceso", "nombre")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["tipos"] = ProcesoFormacion.TIPOS
        ctx["tipo"] = self.request.GET.get("tipo", "")
        return ctx


class ProcesoDetailView(PanelFormacionMixin, DetailView):
    template_name = "formacion/proceso_detalle.html"
    context_object_name = "proceso"
    seccion = "procesos"

    def get_queryset(self):
        return procesos_visibles(self.request.user)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        proceso = self.object
        ctx["inscripciones"] = (
            InscripcionFormacion.objects.filter(id_proceso_formacion=proceso)
            .select_related("id_participante")
            .order_by("estado", "id_participante__nombres_apellidos")
        )
        ctx["actividades"] = _anotar_asistencia(
            Actividad.objects.filter(id_proceso_formacion=proceso).select_related("id_responsable")
        ).order_by("-fecha", "-id_actividad")[:5]
        ctx["seguimientos"] = seguimientos_formacion(self.request.user).filter(id_proceso_formacion=proceso).order_by("-fecha")[:5]
        return ctx


class ProcesoFormMixin(PanelFormacionMixin):
    model = ProcesoFormacion
    form_class = ProcesoForm
    template_name = "formacion/formulario.html"
    seccion = "procesos"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        with transaction.atomic():
            proceso = form.save(commit=False)
            if not es_pastor(self.request.user):
                proceso.id_coordinador = self.request.user
            proceso.save()
            registrar_auditoria(self.request, self.accion, proceso)
        messages.success(self.request, self.mensaje)
        return redirect("formacion:proceso_detalle", pk=proceso.pk)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(titulo=self.titulo, volver=reverse("formacion:procesos"))
        return ctx


class ProcesoCreateView(ProcesoFormMixin, CreateView):
    titulo = "Nuevo proceso de formación"
    accion = "CREAR"
    mensaje = "Proceso de formación creado correctamente."

    def get_initial(self):
        inicial = super().get_initial()
        if self.request.GET.get("tipo") in dict(ProcesoFormacion.TIPOS):
            inicial["tipo_proceso"] = self.request.GET["tipo"]
        return inicial


class ProcesoUpdateView(ProcesoFormMixin, UpdateView):
    titulo = "Editar proceso de formación"
    accion = "ACTUALIZAR"
    mensaje = "Proceso de formación actualizado correctamente."

    def get_queryset(self):
        return procesos_visibles(self.request.user)


class ProcesoEstadoView(CambiarEstadoView):
    """Solo el Pastor desactiva o reactiva procesos de formación (RN24)."""

    model = ProcesoFormacion
    url_retorno = reverse_lazy("formacion:procesos")
    nombre = "Proceso"


# ----------------------------------------------------------------- Participantes e inscripciones


class ParticipanteListView(PanelFormacionMixin, ListView):
    template_name = "formacion/participantes_lista.html"
    context_object_name = "participantes"
    paginate_by = 25
    seccion = "participantes"

    def get_queryset(self):
        user = self.request.user
        procesos = procesos_visibles(user)
        qs = participantes_formacion(user)
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(Q(nombres_apellidos__icontains=q) | Q(documento_identidad__icontains=q))
        proceso = self.request.GET.get("proceso")
        if proceso and proceso.isdigit():
            qs = qs.filter(inscripcionformacion__id_proceso_formacion=proceso)
        return qs.prefetch_related(
            Prefetch(
                "inscripcionformacion_set",
                queryset=InscripcionFormacion.objects.filter(id_proceso_formacion__in=procesos, estado=ACTIVO)
                .select_related("id_proceso_formacion"),
                to_attr="inscripciones",
            )
        ).order_by("nombres_apellidos")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["procesos_filtro"] = procesos_visibles(self.request.user).order_by("tipo_proceso", "nombre")
        ctx["filtros"] = self.request.GET
        params = self.request.GET.copy()
        params.pop("page", None)
        ctx["query_sin_pagina"] = params.urlencode()
        return ctx


class ParticipanteDetailView(PanelFormacionMixin, DetailView):
    template_name = "formacion/participante_detalle.html"
    context_object_name = "participante"
    seccion = "participantes"

    def get_queryset(self):
        return participantes_formacion(self.request.user)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        p, user = self.object, self.request.user
        ctx["inscripciones"] = InscripcionFormacion.objects.filter(
            id_participante=p, id_proceso_formacion__in=procesos_visibles(user)
        ).select_related("id_proceso_formacion").order_by("estado", "-fecha_inscripcion")
        ctx["asistencias"] = (
            Asistencia.objects.filter(id_participante=p, id_actividad__in=actividades_formacion(user))
            .select_related("id_actividad", "id_actividad__id_proceso_formacion")
            .order_by("-id_actividad__fecha")[:10]
        )
        ctx["seguimientos"] = seguimientos_formacion(user).filter(id_participante=p).order_by("-fecha")
        return ctx


class NuevoParticipanteView(PanelFormacionMixin, FormView):
    """Registro de una persona nueva e inscripción en un proceso (RF05 para el Coordinador)."""

    form_class = NuevoParticipanteFormacionForm
    template_name = "formacion/formulario.html"
    seccion = "participantes"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_initial(self):
        proceso = self.request.GET.get("proceso")
        return {"proceso": proceso} if proceso and proceso.isdigit() else {}

    def form_valid(self, form):
        with transaction.atomic():
            participante = form.save()
            inscribir(participante, form.cleaned_data["proceso"])
            registrar_auditoria(self.request, "CREAR", participante)
        messages.success(self.request, f"{participante} registrado e inscrito en {form.cleaned_data['proceso']}.")
        return redirect("formacion:participante_detalle", pk=participante.pk)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(
            titulo="Nuevo participante",
            volver=reverse("formacion:participantes"),
            enlace_extra=(reverse("formacion:inscribir"), "¿Ya está registrado? Inscribir participante existente"),
        )
        if not procesos_visibles(self.request.user).filter(estado=ACTIVO).exists():
            ctx["aviso"] = "Primero cree un proceso de formación activo para inscribir participantes."
        return ctx


class InscribirExistenteView(PanelFormacionMixin, FormView):
    form_class = InscribirExistenteForm
    template_name = "formacion/formulario.html"
    seccion = "participantes"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_initial(self):
        proceso = self.request.GET.get("proceso")
        return {"proceso": proceso} if proceso and proceso.isdigit() else {}

    def form_valid(self, form):
        participante, proceso = form.cleaned_data["participante"], form.cleaned_data["proceso"]
        with transaction.atomic():
            inscripcion = inscribir(participante, proceso)
            registrar_auditoria(self.request, "INSCRIBIR", inscripcion)
        messages.success(self.request, f"{participante} inscrito en {proceso}.")
        return redirect("formacion:proceso_detalle", pk=proceso.pk)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(titulo="Inscribir participante existente", volver=reverse("formacion:participantes"))
        return ctx


class ParticipanteUpdateView(PanelFormacionMixin, UpdateView):
    """El Coordinador edita los datos de los participantes de sus procesos (HU-25, criterio 1)."""

    form_class = DatosParticipanteForm
    template_name = "formacion/formulario.html"
    seccion = "participantes"

    def get_queryset(self):
        return participantes_formacion(self.request.user)

    def form_valid(self, form):
        with transaction.atomic():
            participante = form.save()
            registrar_auditoria(self.request, "ACTUALIZAR", participante)
        messages.success(self.request, "Participante actualizado correctamente.")
        return redirect("formacion:participante_detalle", pk=participante.pk)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(titulo="Editar participante", volver=reverse("formacion:participante_detalle", args=[self.object.pk]))
        return ctx


class InscripcionEstadoView(PanelFormacionMixin, View):
    """Retirar o reactivar una inscripción sin borrar su historial (RN17, RN24)."""

    def post(self, request, pk, accion):
        if accion not in ("activar", "desactivar"):
            raise Http404
        inscripcion = get_object_or_404(
            InscripcionFormacion.objects.select_related("id_participante", "id_proceso_formacion"),
            pk=pk,
            id_proceso_formacion__in=procesos_visibles(request.user),
        )
        inscripcion.estado = INACTIVO if accion == "desactivar" else ACTIVO
        with transaction.atomic():
            inscripcion.save(update_fields=["estado"])
            registrar_auditoria(request, "RETIRAR" if accion == "desactivar" else "REACTIVAR", inscripcion)
        verbo = "retirado de" if accion == "desactivar" else "reincorporado a"
        messages.success(request, f"{inscripcion.id_participante} {verbo} {inscripcion.id_proceso_formacion}.")
        return redirect("formacion:proceso_detalle", pk=inscripcion.id_proceso_formacion_id)


# ----------------------------------------------------------------- Actividades y asistencia


class ActividadListView(PanelFormacionMixin, ListView):
    template_name = "formacion/actividades_lista.html"
    context_object_name = "actividades"
    paginate_by = 20
    seccion = "asistencia"

    def get_queryset(self):
        qs = actividades_formacion(self.request.user)
        g = self.request.GET
        if g.get("proceso", "").isdigit():
            qs = qs.filter(id_proceso_formacion=g["proceso"])
        if g.get("tipo") in dict(ProcesoFormacion.TIPOS):
            qs = qs.filter(id_proceso_formacion__tipo_proceso=g["tipo"])
        for campo, lookup in (("desde", "fecha__gte"), ("hasta", "fecha__lte")):
            try:
                qs = qs.filter(**{lookup: datetime.date.fromisoformat(g.get(campo, ""))})
            except ValueError:
                pass
        return _anotar_asistencia(qs).order_by("-fecha", "-id_actividad")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["procesos_filtro"] = procesos_visibles(self.request.user).order_by("tipo_proceso", "nombre")
        ctx["tipos"] = ProcesoFormacion.TIPOS
        ctx["filtros"] = self.request.GET
        params = self.request.GET.copy()
        params.pop("page", None)
        ctx["query_sin_pagina"] = params.urlencode()
        return ctx


class ActividadDetailView(PanelFormacionMixin, DetailView):
    template_name = "formacion/actividad_detalle.html"
    context_object_name = "actividad"
    seccion = "asistencia"

    def get_queryset(self):
        return actividades_formacion(self.request.user)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["asistencias"] = self.object.asistencia_set.select_related("id_participante").order_by("id_participante__nombres_apellidos")
        ctx["presentes"] = sum(1 for a in ctx["asistencias"] if a.presente)
        return ctx


class RegistrarActividadView(PanelFormacionMixin, FormView):
    """Crea la actividad de un proceso y registra la asistencia de sus inscritos (HU-26, criterio 3)."""

    form_class = ActividadFormacionForm
    template_name = "formacion/actividad_registrar.html"
    seccion = "asistencia"

    def dispatch(self, request, *args, **kwargs):
        self.proceso = None
        if request.user.is_authenticated:
            self.proceso = get_object_or_404(
                procesos_visibles(request.user).filter(estado=ACTIVO), pk=kwargs["proceso"]
            ) if rol_de(request.user) in (ROLES_PASTOR, ROLES_COORD) else None
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["proceso"] = self.proceso
        return kwargs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["proceso"] = self.proceso
        ctx["inscritos"] = inscritos_activos(self.proceso)
        if self.request.method == "POST":
            ctx["marcados"] = {p.pk for p in ctx["inscritos"] if self.request.POST.get(f"presente_{p.pk}")}
        else:
            ctx["marcados"] = {p.pk for p in ctx["inscritos"]}
        return ctx

    def form_valid(self, form):
        inscritos = list(inscritos_activos(self.proceso))
        if not inscritos:
            form.add_error(None, "El proceso no tiene participantes inscritos para registrar asistencia.")
            return self.form_invalid(form)
        user = self.request.user
        with transaction.atomic():
            actividad = Actividad.objects.create(
                tipo_modulo=TIPO_MODULO,
                id_proceso_formacion=self.proceso,
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
                for p in inscritos
            )
            registrar_auditoria(self.request, "REGISTRAR_ASISTENCIA", actividad)
        presentes = sum(1 for p in inscritos if self.request.POST.get(f"presente_{p.pk}"))
        messages.success(self.request, f"Actividad registrada: {presentes} de {len(inscritos)} presentes.")
        return redirect("formacion:actividad_detalle", pk=actividad.pk)


# ----------------------------------------------------------------- Seguimiento


class SeguimientoListView(PanelFormacionMixin, ListView):
    template_name = "formacion/seguimientos_lista.html"
    context_object_name = "seguimientos"
    paginate_by = 25
    seccion = "seguimiento"

    def get_queryset(self):
        qs = seguimientos_formacion(self.request.user)
        g = self.request.GET
        q = g.get("q", "").strip()
        if q:
            qs = qs.filter(Q(id_participante__nombres_apellidos__icontains=q) | Q(observacion__icontains=q))
        if g.get("proceso", "").isdigit():
            qs = qs.filter(id_proceso_formacion=g["proceso"])
        if g.get("participante", "").isdigit():
            qs = qs.filter(id_participante=g["participante"])
        if g.get("estado") in dict(Seguimiento.ESTADOS):
            qs = qs.filter(estado=g["estado"])
        return qs.order_by("-fecha", "-id_seguimiento")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["procesos_filtro"] = procesos_visibles(self.request.user).order_by("tipo_proceso", "nombre")
        ctx["estados"] = Seguimiento.ESTADOS
        ctx["filtros"] = self.request.GET
        params = self.request.GET.copy()
        params.pop("page", None)
        ctx["query_sin_pagina"] = params.urlencode()
        return ctx


class SeguimientoFormMixin(PanelFormacionMixin):
    form_class = SeguimientoFormacionForm
    template_name = "formacion/formulario.html"
    seccion = "seguimiento"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        with transaction.atomic():
            seguimiento = form.save(commit=False)
            if not seguimiento.pk:
                seguimiento.id_usuario = self.request.user
            seguimiento.save()
            registrar_auditoria(self.request, self.accion, seguimiento)
        messages.success(self.request, self.mensaje)
        return redirect("formacion:participante_detalle", pk=seguimiento.id_participante_id)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(titulo=self.titulo, volver=reverse("formacion:seguimientos"))
        return ctx


class SeguimientoCreateView(SeguimientoFormMixin, CreateView):
    titulo = "Nuevo seguimiento"
    accion = "CREAR"
    mensaje = "Seguimiento registrado correctamente."

    def get_initial(self):
        inicial = {}
        for campo, param in (("id_proceso_formacion", "proceso"), ("id_participante", "participante")):
            if self.request.GET.get(param, "").isdigit():
                inicial[campo] = self.request.GET[param]
        return inicial


class SeguimientoUpdateView(SeguimientoFormMixin, UpdateView):
    titulo = "Editar seguimiento"
    accion = "ACTUALIZAR"
    mensaje = "Seguimiento actualizado correctamente."

    def get_queryset(self):
        return seguimientos_formacion(self.request.user)


# ----------------------------------------------------------------- Reportes


class ReporteFormacionView(exportar.ExportableMixin, PanelFormacionMixin, TemplateView):
    """Reporte por periodo de los procesos del usuario (RF15, RF16, HU-27, HU-30, HU-33)."""

    template_name = "formacion/reporte.html"
    seccion = "reportes"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        datos = self.request.GET.copy()
        datos.setdefault("tipo", "mensual")
        datos.setdefault("fecha", datetime.date.today().isoformat())
        form = GenerarReporteForm(datos)
        del form.fields["area"], form.fields["casa"]
        ctx["form"] = form
        ctx["tipos"] = ProcesoFormacion.TIPOS
        ctx["procesos_filtro"] = procesos_visibles(user).order_by("tipo_proceso", "nombre")
        ctx["filtros"] = self.request.GET
        if not form.is_valid():
            return ctx

        periodo = form.periodo
        rango = (periodo.inicio, periodo.fin)
        procesos = procesos_visibles(user)
        if self.request.GET.get("tipo_proceso") in dict(ProcesoFormacion.TIPOS):
            procesos = procesos.filter(tipo_proceso=self.request.GET["tipo_proceso"])
        if self.request.GET.get("proceso", "").isdigit():
            procesos = procesos.filter(pk=self.request.GET["proceso"])

        def por_proceso(qs, campo="id_proceso_formacion", **anotaciones):
            return {fila[campo]: fila for fila in qs.values(campo).annotate(**anotaciones)}

        actividades = por_proceso(
            Actividad.objects.filter(tipo_modulo=TIPO_MODULO, fecha__range=rango, id_proceso_formacion__in=procesos),
            n=Count("id_actividad", distinct=True),
            presentes=Count("asistencia", filter=Q(asistencia__presente=True)),
            registros=Count("asistencia"),
        )
        inscritos = por_proceso(
            InscripcionFormacion.objects.filter(id_proceso_formacion__in=procesos, estado=ACTIVO, id_participante__estado=ACTIVO),
            n=Count("id_inscripcion"),
        )
        nuevos = por_proceso(
            InscripcionFormacion.objects.filter(id_proceso_formacion__in=procesos, fecha_inscripcion__range=rango),
            n=Count("id_inscripcion"),
        )
        seguimientos = por_proceso(
            Seguimiento.objects.filter(tipo_modulo=TIPO_MODULO, fecha__range=rango, id_proceso_formacion__in=procesos),
            n=Count("id_seguimiento"),
        )
        filas = []
        for proceso in procesos.order_by("tipo_proceso", "nombre"):
            act = actividades.get(proceso.pk, {})
            if not proceso.activo and not act:
                continue
            filas.append({
                "proceso": proceso,
                "actividades": act.get("n", 0),
                "presentes": act.get("presentes", 0),
                "registros": act.get("registros", 0),
                "porcentaje": _con_porcentaje(act.get("presentes", 0), act.get("registros", 0)),
                "inscritos": inscritos.get(proceso.pk, {}).get("n", 0),
                "nuevos": nuevos.get(proceso.pk, {}).get("n", 0),
                "seguimientos": seguimientos.get(proceso.pk, {}).get("n", 0),
            })
        total = {k: sum(f[k] for f in filas) for k in ("actividades", "presentes", "registros", "inscritos", "nuevos", "seguimientos")}
        total["porcentaje"] = _con_porcentaje(total["presentes"], total["registros"])
        ctx.update(
            periodo=periodo,
            filas=filas,
            total=total,
            hay_datos=any(f["actividades"] or f["nuevos"] or f["seguimientos"] for f in filas),
        )
        return ctx

    def documento_exportable(self, ctx):
        if "periodo" not in ctx:
            return None
        g = self.request.GET
        tipo = dict(ProcesoFormacion.TIPOS).get(g.get("tipo_proceso"), "Todas")
        proceso = ctx["procesos_filtro"].filter(pk=g["proceso"]).first() if g.get("proceso", "").isdigit() else None
        return exportar.Documento(
            titulo="Reporte de Escuelas de Formación",
            periodo=f"{ctx['periodo'].nombre} ({ctx['periodo'].inicio:%d/%m/%Y} al {ctx['periodo'].fin:%d/%m/%Y})",
            datos=[("Escuela", tipo), ("Proceso", proceso or "Todos")],
            tablas=[exportar.Tabla(
                "Procesos de formación",
                [("Escuela", exportar.TEXTO), ("Proceso", exportar.TEXTO), ("Actividades", exportar.ENTERO),
                 ("Presentes", exportar.ENTERO), ("Registros", exportar.ENTERO), ("Asistencia", exportar.PORCENTAJE),
                 ("Inscritos", exportar.ENTERO), ("Nuevos", exportar.ENTERO), ("Seguimientos", exportar.ENTERO)],
                [[f["proceso"].get_tipo_proceso_display(), f["proceso"].nombre, f["actividades"], f["presentes"],
                  f["registros"], f["porcentaje"], f["inscritos"], f["nuevos"], f["seguimientos"]] for f in ctx["filas"]],
                total=["Total", "", *[ctx["total"][k] for k in ("actividades", "presentes", "registros", "porcentaje",
                                                                "inscritos", "nuevos", "seguimientos")]],
            )],
            nombre_archivo=f"reporte_formacion_{ctx['periodo'].etiqueta}",
        )
