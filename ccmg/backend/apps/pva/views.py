import datetime

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import Count, Prefetch, Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.generic import CreateView, DetailView, FormView, ListView, RedirectView, UpdateView, View

from nucleo.autocompletar import sugerencias
from nucleo.mixins import ModuleRequiredMixin, PastorRequiredMixin
from nucleo.permissions import module_required, puede_gestionar_ofrendas
from nucleo.utils import (
    ROLES_APOYO,
    ROLES_ETIQUETA,
    ROLES_LIDER,
    ROLES_PASTOR,
    ROLES_SUPERVISOR,
    registrar_auditoria,
    es_superadmin,
    rol_real,
    sesion_js,
)

from ofrendas.models import Ofrenda

from . import periodos
from .alcance import (
    asistencias_visibles,
    casa_para_reportar,
    casas_visibles,
    es_pastor,
    participantes_visibles,
    rol_de,
    seguimientos_visibles,
)
from .forms import AreaForm, CasaVidaForm, PersonaNuevaForm, ReporteAsistenciaForm
from .models import (
    ACTIVO,
    INACTIVO,
    Actividad,
    Area,
    CasaVida,
    CasaVidaEquipo,
    CasaVidaMiembro,
    Participante,
    Reporte,
    ReporteAsistencia,
)

ROLES_NOMBRE = ROLES_ETIQUETA


def menu_casas(user, seccion):
    """Menú lateral del módulo según el rol. Las secciones aún no migradas viven en el panel JS."""
    rol = rol_de(user)
    panel = reverse("pva:panel")
    todos = [ROLES_PASTOR, ROLES_SUPERVISOR, ROLES_LIDER, ROLES_APOYO]
    items = [
        ("inicio", "Inicio", "speedometer2", panel + "#inicio", todos),
        ("participantes", "Personas nuevas", "person-plus", reverse("pva:participantes"), todos),
        ("casas", "Casas de Vida", "houses", reverse("pva:casas"), todos),
        ("areas", "Áreas", "map", reverse("pva:areas"), [ROLES_PASTOR]),
        ("importar", "Importar datos", "upload", reverse("pva:importar"), [ROLES_PASTOR]),
        ("asistencia", "Asistencia", "check2-square", reverse("pva:asistencia"), todos),
        ("seguimiento", "Seguimiento", "clipboard-check", reverse("pva:seguimientos"), [ROLES_PASTOR, ROLES_SUPERVISOR, ROLES_LIDER]),
        ("ofrendas", "Ofrendas", "cash-coin", reverse("ofrendas:index"), todos if puede_gestionar_ofrendas(user) else []),
        ("reportes", "Reportes", "file-earmark-text", reverse("pva:reportes"), todos),
        ("usuarios", "Usuarios", "person-gear", reverse("cuentas:usuarios_list"), [ROLES_PASTOR]),
        ("auditoria", "Auditoría", "journal-text", reverse("cuentas:auditoria"), todos if es_superadmin(user) else []),
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
        ctx["rol_nombre"] = ROLES_NOMBRE.get(rol_real(user), "")
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
    asistencias = asistencias_visibles(user).order_by("-fecha", "-id_reporte")
    reuniones = list(asistencias.values_list("asistentes", flat=True))
    seguimientos = seguimientos_visibles(user).order_by("-fecha", "-id_seguimiento")
    resumen = {
        "participantes": participantes_visibles(user).filter(estado=ACTIVO).count(),
        "casas": casas.count(),
        "casasActivas": casas.filter(estado=ACTIVO).count(),
        # Promedio de asistentes por reunión reportada (la asistencia ya no se marca por persona).
        "asistenciaPromedio": round(sum(reuniones) / len(reuniones)) if reuniones else 0,
        "actividades": [
            {
                "casa": a.id_reporte.id_casa_vida.nombre,
                "fecha": a.fecha.isoformat(),
                "nuevos": a.nuevos,
                "asistentes": a.asistentes,
            }
            for a in asistencias[:4]
        ],
        "seguimientosAbiertos": seguimientos.exclude(estado="CERRADO").count(),
        "seguimientos": [
            {"participante": s.id_participante.nombres_apellidos, "estado": s.get_estado_display(), "cerrado": s.estado == "CERRADO"}
            for s in seguimientos[:4]
        ],
    }
    return render(
        request,
        "pva/panel.html",
        {
            "user": user,
            "sesion_js": sesion_js(user),
            "resumen_pva": resumen,
            "urls_pva": {
                "participantes": reverse("pva:participantes"),
                "casas": reverse("pva:casas"),
                "areas": reverse("pva:areas"),
                "importar": reverse("pva:importar"),
                "usuarios": reverse("cuentas:usuarios_list"),
                "asistencia": reverse("pva:asistencia"),
                "seguimiento": reverse("pva:seguimientos"),
                "reportes": reverse("pva:reportes"),
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
            # Las casas del Área toman su Supervisor del Área (CasaVida.supervisor, RN03).
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
        ctx["miembros"] = (
            CasaVidaMiembro.objects.filter(id_casa_vida=casa, estado=ACTIVO, id_participante__estado=ACTIVO)
            .select_related("id_participante")
            .order_by("-fecha_ingreso", "id_participante__nombres_apellidos")
        )
        ctx["equipo"] = CasaVidaEquipo.objects.filter(id_casa_vida=casa, activo=True).select_related("id_usuario")
        ctx["asistencias"] = (
            ReporteAsistencia.objects.filter(id_reporte__id_casa_vida=casa)
            .select_related("id_reporte__id_usuario_envia")
            .order_by("-fecha")[:5]
        )
        ctx["puede_registrar_persona"] = casa_para_reportar(self.request.user) == casa
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


# ----------------------------------------------------------------- Personas nuevas


def _con_casa_actual(qs):
    return qs.prefetch_related(
        Prefetch(
            "casavidamiembro_set",
            queryset=CasaVidaMiembro.objects.filter(estado=ACTIVO).select_related("id_casa_vida"),
            to_attr="membresias",
        )
    )


class ParticipanteListView(PanelCasasMixin, ListView):
    """Personas nuevas que han llegado a las Casas de Vida, según el alcance del rol (RF06)."""

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
            qs = qs.filter(Q(nombres_apellidos__icontains=q) | Q(telefono__icontains=q))
        casa = g.get("casa")
        if casa and casa.isdigit():
            qs = qs.filter(casavidamiembro__id_casa_vida=casa, casavidamiembro__estado=ACTIVO)
        if es_pastor(user) and g.get("estado") in (ACTIVO, INACTIVO):
            qs = qs.filter(estado=g["estado"])
        return _con_casa_actual(qs.distinct().order_by("-creado_en", "nombres_apellidos"))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["casas_filtro"] = casas_visibles(self.request.user)
        ctx["filtros"] = self.request.GET
        ctx["casa_registro"] = casa_para_reportar(self.request.user)
        params = self.request.GET.copy()
        params.pop("page", None)
        ctx["query_sin_pagina"] = params.urlencode()
        return ctx


class ParticipanteAutocompletarView(PanelCasasMixin, View):
    """Sugerencias de personas nuevas para el buscador, con el mismo alcance por rol que la lista."""

    def get(self, request):
        def construir(p):
            casa = p.membresias[0].id_casa_vida.nombre if p.membresias else "Sin Casa de Vida"
            detalle = " · ".join(filter(None, [p.telefono, casa]))
            return {
                "id": p.pk,
                "nombre": p.nombres_apellidos,
                "detalle": detalle,
                "url": reverse("pva:participante_detalle", args=[p.pk]),
            }

        qs = _con_casa_actual(participantes_visibles(request.user))
        return sugerencias(request, qs, ("nombres_apellidos", "telefono"), construir)


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
        ctx["puede_editar"] = puede_editar_persona(self.request.user, p)
        ctx["ve_seguimiento"] = rol_de(self.request.user) in (ROLES_PASTOR, ROLES_SUPERVISOR, ROLES_LIDER)
        ctx["seguimientos"] = seguimientos_visibles(self.request.user).filter(id_participante=p)[:10]
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


def puede_editar_persona(user, persona):
    """El Pastor corrige cualquier registro; el Líder y su equipo, los de su Casa de Vida."""
    if es_pastor(user):
        return True
    casa = casa_para_reportar(user)
    membresia = persona.membresia_activa
    return bool(casa and membresia and membresia.id_casa_vida_id == casa.pk)


class PersonaNuevaCreateView(PanelCasasMixin, CreateView):
    """El Líder o un usuario de apoyo toman los datos de una persona nueva que llega (RF05, RN09).

    En la Casa de Vida no se lleva una lista fija de participantes: las personas vienen y van.
    Solo se registra a quien llega por primera vez, con su nombre y teléfono.
    """

    model = Participante
    form_class = PersonaNuevaForm
    template_name = "pva/formulario.html"
    seccion = "participantes"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if rol_de(request.user) not in (ROLES_LIDER, ROLES_APOYO):
                raise PermissionDenied("Las personas nuevas las registra el Líder o su equipo en la Casa de Vida.")
            self.casa = casa_para_reportar(request.user)
            if self.casa is None:
                messages.error(request, "Todavía no tienes una Casa de Vida asignada. Pídele al Pastor que te asigne una.")
                return redirect("pva:participantes")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        with transaction.atomic():
            persona = form.save()
            CasaVidaMiembro.objects.create(
                id_casa_vida=self.casa, id_participante=persona, fecha_ingreso=datetime.date.today()
            )
            registrar_auditoria(self.request, "CREAR", persona)
        messages.success(
            self.request, f"Se registró a {persona.nombres_apellidos} como persona nueva de {self.casa.nombre}."
        )
        return redirect("pva:participantes")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(
            titulo="Registrar persona nueva",
            subtitulo=f"Casa de Vida {self.casa.nombre} · {datetime.date.today():%d/%m/%Y}",
            volver=reverse("pva:participantes"),
        )
        return ctx


class PersonaNuevaUpdateView(PanelCasasMixin, UpdateView):
    model = Participante
    form_class = PersonaNuevaForm
    template_name = "pva/formulario.html"
    seccion = "participantes"

    def get_queryset(self):
        return participantes_visibles(self.request.user)

    def get_object(self, queryset=None):
        persona = super().get_object(queryset)
        if not puede_editar_persona(self.request.user, persona):
            raise PermissionDenied("Solo el Pastor o el equipo de su Casa de Vida corrigen estos datos.")
        return persona

    def form_valid(self, form):
        with transaction.atomic():
            persona = form.save()
            registrar_auditoria(self.request, "ACTUALIZAR", persona)
        messages.success(self.request, "Datos actualizados correctamente.")
        return redirect("pva:participante_detalle", pk=persona.pk)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(titulo="Editar persona", volver=reverse("pva:participante_detalle", args=[self.object.pk]))
        return ctx


class ParticipanteEstadoView(CambiarEstadoView):
    model = Participante
    url_retorno = reverse_lazy("pva:participantes")
    nombre = "Registro de"


# ----------------------------------------------------------------- Asistencia (reporte por totales)


class AsistenciaListView(PanelCasasMixin, ListView):
    """Reportes de asistencia de las Casas de Vida según el alcance del rol (RF10)."""

    template_name = "pva/asistencia_lista.html"
    context_object_name = "asistencias"
    paginate_by = 20
    seccion = "asistencia"

    def get_queryset(self):
        qs = asistencias_visibles(self.request.user)
        g = self.request.GET
        casa = g.get("casa")
        if casa and casa.isdigit():
            qs = qs.filter(id_reporte__id_casa_vida=casa)
        for campo, lookup in (("desde", "fecha__gte"), ("hasta", "fecha__lte")):
            try:
                qs = qs.filter(**{lookup: datetime.date.fromisoformat(g.get(campo, ""))})
            except ValueError:
                pass
        return qs.order_by("-fecha", "-id_reporte")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["casas_filtro"] = casas_visibles(self.request.user)
        ctx["filtros"] = self.request.GET
        ctx["casa_reporte"] = casa_para_reportar(self.request.user)
        params = self.request.GET.copy()
        params.pop("page", None)
        ctx["query_sin_pagina"] = params.urlencode()
        return ctx


class AsistenciaDetailView(RedirectView):
    """El detalle de la asistencia es el del reporte semanal que la contiene."""

    pattern_name = "pva:reporte_detalle"


class RegistrarAsistenciaView(PanelCasasMixin, FormView):
    """El Líder o un usuario de apoyo llenan el reporte de asistencia y queda enviado al Supervisor
    (RF09, RF14, RN05, RN06). La ofrenda se registra también en el módulo de Ofrendas (RF17)."""

    template_name = "pva/asistencia_registrar.html"
    form_class = ReporteAsistenciaForm
    seccion = "asistencia"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if rol_de(request.user) not in (ROLES_LIDER, ROLES_APOYO):
                raise PermissionDenied("Solo el Líder y los usuarios de apoyo llenan el reporte de asistencia.")
            self.casa = casa_para_reportar(request.user)
            if self.casa is None:
                messages.error(request, "Todavía no tienes una Casa de Vida asignada para reportar asistencia. Pídele al Pastor que te asigne una.")
                return redirect("pva:asistencia")
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["casa"] = self.casa
        return kwargs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        semana = periodos.semana(datetime.date.today())
        ctx.update(
            casa=self.casa,
            supervisor=self.casa.supervisor,
            semana=semana,
            ya_enviado=Reporte.objects.filter(
                tipo_reporte=Reporte.CASA_VIDA, id_casa_vida=self.casa, periodo=semana.etiqueta
            ).select_related("id_usuario_envia").first(),
        )
        return ctx

    def form_valid(self, form):
        supervisor = self.casa.supervisor
        if supervisor is None:
            form.add_error(None, "Tu Casa de Vida todavía no tiene Supervisor de Área, así que el reporte no tiene a quién llegar. Pídele al Pastor que lo asigne.")
            return self.form_invalid(form)
        datos = form.cleaned_data
        semana = periodos.semana(datos["fecha"])
        user = self.request.user
        with transaction.atomic():
            reporte = Reporte.objects.create(
                tipo_modulo=Actividad.TIPO_CASA_VIDA,
                tipo_reporte=Reporte.CASA_VIDA,
                id_usuario_envia=user,
                id_usuario_destino=supervisor,
                id_casa_vida=self.casa,
                id_area=self.casa.id_area,
                periodo=semana.etiqueta,
                fecha_inicio=semana.inicio,
                fecha_fin=semana.fin,
                observaciones=datos["observaciones"] or None,
            )
            ofrenda = None
            if datos["ofrenda"]:
                ofrenda = Ofrenda.objects.create(
                    fecha=datos["fecha"],
                    concepto=f"Ofrenda Casa de Vida {self.casa.nombre}",
                    valor=datos["ofrenda"],
                    id_casa_vida=self.casa,
                    id_usuario_registro=user,
                    observacion="Registrada desde el reporte de asistencia.",
                )
            campos = [c for c, _ in ReporteAsistencia.INDICADORES + ReporteAsistencia.ESCUELAS + ReporteAsistencia.CULTOS]
            ReporteAsistencia.objects.create(
                id_reporte=reporte,
                fecha=datos["fecha"],
                id_lider=self.casa.id_lider,
                ofrenda=datos["ofrenda"],
                id_ofrenda=ofrenda,
                **{c: datos[c] for c in campos if c in datos},
            )
            registrar_auditoria(self.request, "ENVIAR_REPORTE", reporte)
        messages.success(
            self.request, f"Reporte de asistencia del {datos['fecha']:%d/%m/%Y} enviado al Supervisor de Área."
        )
        return redirect("pva:reporte_detalle", pk=reporte.pk)
