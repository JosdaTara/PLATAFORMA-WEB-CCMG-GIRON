"""Reportes del módulo Casas de Vida.

Flujo (RN06, RN07, RN19): el Líder o su equipo envían el reporte semanal de la Casa de Vida
al Supervisor de Área; el Supervisor envía al Pastor un reporte general mensual de su Área;
el Pastor, último receptor, consulta los reportes y genera reportes consolidados.
"""
import datetime

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import Count, Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, FormView, TemplateView

from nucleo import exportar
from nucleo.utils import ROLES_APOYO, ROLES_LIDER, ROLES_PASTOR, ROLES_SUPERVISOR, registrar_auditoria

from . import periodos
from .alcance import (
    area_del_supervisor,
    casa_para_reportar,
    reportes_casa_visibles,
    reportes_generales_visibles,
    rol_de,
)
from .forms import EnviarReporteCasaForm, EnviarReporteGeneralForm, GenerarReporteForm, reportes_casa_pendientes
from .models import ACTIVO, Actividad, CasaVida, CasaVidaMiembro, Reporte, Seguimiento
from .views import PanelCasasMixin


def resumen_actividades(casa, inicio, fin):
    """Actividades de la casa en el rango con su asistencia."""
    actividades = list(
        Actividad.objects.filter(id_casa_vida=casa, fecha__range=(inicio, fin))
        .annotate(presentes=Count("asistencia", filter=Q(asistencia__presente=True)), total=Count("asistencia"))
        .select_related("id_responsable")
        .order_by("fecha", "id_actividad")
    )
    presentes = sum(a.presentes for a in actividades)
    registros = sum(a.total for a in actividades)
    return {
        "actividades": actividades,
        "presentes": presentes,
        "registros": registros,
        "porcentaje": round(presentes * 100 / registros) if registros else 0,
    }


def _tabla_actividades(ctx):
    return exportar.Tabla(
        "Actividades y asistencia",
        [("Fecha", exportar.FECHA), ("Actividad", exportar.TEXTO), ("Presentes", exportar.ENTERO),
         ("Registros", exportar.ENTERO), ("Registró", exportar.TEXTO)],
        [[a.fecha, a.titulo, a.presentes, a.total, a.id_responsable.nombre_completo if a.id_responsable else ""]
         for a in ctx["actividades"]],
        total=["Total", f"Asistencia {ctx['porcentaje']}%", ctx["presentes"], ctx["registros"], ""] if ctx["actividades"] else None,
        vacio="No hay asistencia registrada en esta semana.",
    )


def solo_roles(*roles):
    """Restringe una vista de clase a ciertos roles (403 para los demás)."""

    class RolesMixin:
        def dispatch(self, request, *args, **kwargs):
            if request.user.is_authenticated and rol_de(request.user) not in roles:
                raise PermissionDenied("Tu rol no puede realizar esta acción.")
            return super().dispatch(request, *args, **kwargs)

    return RolesMixin


class ReporteListView(PanelCasasMixin, TemplateView):
    """Consulta de reportes según el rol (RF15)."""

    template_name = "pva/reportes_lista.html"
    seccion = "reportes"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        rol = rol_de(user)
        ctx["rol"] = rol
        ctx["reportes_casa"] = reportes_casa_visibles(user).order_by("-fecha_inicio", "-id_reporte")[:50]
        ctx["reportes_generales"] = reportes_generales_visibles(user).order_by("-fecha_inicio", "-id_reporte")[:50]

        if rol in (ROLES_LIDER, ROLES_APOYO):
            casa = casa_para_reportar(user)
            ctx["casa"] = casa
            if casa:
                semana = periodos.semana(datetime.date.today())
                ctx["semana_actual"] = semana
                ctx["reporte_semana"] = (
                    Reporte.objects.filter(tipo_reporte=Reporte.CASA_VIDA, id_casa_vida=casa, periodo=semana.etiqueta)
                    .select_related("id_usuario_envia")
                    .first()
                )
        elif rol == ROLES_SUPERVISOR:
            area = area_del_supervisor(user)
            ctx["area"] = area
            if area:
                ctx["pendientes_general"] = Reporte.objects.filter(
                    tipo_reporte=Reporte.CASA_VIDA, id_casa_vida__id_area=area, id_reporte_general__isnull=True
                ).count()
        return ctx


class ReporteDetailView(exportar.ExportableMixin, PanelCasasMixin, DetailView):
    template_name = "pva/reporte_detalle.html"
    context_object_name = "reporte"
    seccion = "reportes"

    def get_object(self, queryset=None):
        reporte = get_object_or_404(Reporte, pk=self.kwargs["pk"], tipo_modulo=Actividad.TIPO_CASA_VIDA)
        visibles = reportes_generales_visibles if reporte.es_general else reportes_casa_visibles
        if not visibles(self.request.user).filter(pk=reporte.pk).exists():
            raise Http404
        return reporte

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        r = self.object
        if r.es_general:
            filas = []
            for rc in r.reportes_casa.select_related("id_casa_vida", "id_usuario_envia").order_by("id_casa_vida__nombre", "fecha_inicio"):
                filas.append({"reporte": rc, **resumen_actividades(rc.id_casa_vida, rc.fecha_inicio, rc.fecha_fin)})
            presentes = sum(f["presentes"] for f in filas)
            registros = sum(f["registros"] for f in filas)
            ctx["filas"] = filas
            ctx["total"] = {
                "presentes": presentes,
                "registros": registros,
                "porcentaje": round(presentes * 100 / registros) if registros else 0,
            }
        else:
            ctx.update(resumen_actividades(r.id_casa_vida, r.fecha_inicio, r.fecha_fin))
        return ctx

    def documento_exportable(self, ctx):
        r = self.object
        if r.es_general:
            return exportar.Documento(
                titulo=f"Reporte general · Área {r.id_area.nombre}",
                periodo=f"{r.fecha_inicio:%d/%m/%Y} al {r.fecha_fin:%d/%m/%Y} ({r.periodo})",
                datos=[("Supervisor", r.id_usuario_envia.nombre_completo), ("Enviado", r.enviado_en),
                       ("Observaciones", r.observaciones or "—")],
                tablas=[exportar.Tabla(
                    "Reportes de las Casas de Vida",
                    [("Casa de Vida", exportar.TEXTO), ("Semana", exportar.TEXTO), ("Actividades", exportar.ENTERO),
                     ("Presentes", exportar.ENTERO), ("Registros", exportar.ENTERO), ("Asistencia", exportar.PORCENTAJE),
                     ("Observaciones del equipo", exportar.TEXTO)],
                    [[f["reporte"].id_casa_vida.nombre, f"{f['reporte'].fecha_inicio:%d/%m} – {f['reporte'].fecha_fin:%d/%m}",
                      len(f["actividades"]), f["presentes"], f["registros"], f["porcentaje"], f["reporte"].observaciones or ""]
                     for f in ctx["filas"]],
                    total=["Total", "", sum(len(f["actividades"]) for f in ctx["filas"]), ctx["total"]["presentes"],
                           ctx["total"]["registros"], ctx["total"]["porcentaje"], ""],
                )],
                nombre_archivo=f"reporte_general_{r.id_area.nombre}_{r.periodo}",
            )
        return exportar.Documento(
            titulo=f"Reporte semanal · {r.id_casa_vida.nombre}",
            periodo=f"{r.fecha_inicio:%d/%m/%Y} al {r.fecha_fin:%d/%m/%Y} ({r.periodo})",
            datos=[("Área", r.id_casa_vida.id_area.nombre if r.id_casa_vida.id_area_id else "—"),
                   ("Enviado por", r.id_usuario_envia.nombre_completo),
                   ("Enviado a", r.id_usuario_destino.nombre_completo if r.id_usuario_destino else "Supervisor de Área"),
                   ("Enviado", r.enviado_en), ("Observaciones", r.observaciones or "—")],
            tablas=[_tabla_actividades(ctx)],
            nombre_archivo=f"reporte_{r.id_casa_vida.nombre}_{r.periodo}",
        )


class EnviarReporteCasaView(solo_roles(ROLES_LIDER, ROLES_APOYO), PanelCasasMixin, FormView):
    """El Líder o un usuario de apoyo envían el reporte semanal al Supervisor (RF14, CU02)."""

    template_name = "pva/reporte_enviar_casa.html"
    form_class = EnviarReporteCasaForm
    seccion = "reportes"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and rol_de(request.user) in (ROLES_LIDER, ROLES_APOYO):
            self.casa = casa_para_reportar(request.user)
            if self.casa is None:
                messages.error(request, "No tienes una Casa de Vida activa asignada.")
                return redirect("pva:reportes")
        return super().dispatch(request, *args, **kwargs)

    @property
    def supervisor(self):
        return self.casa.id_area.id_supervisor if self.casa.id_area_id else None

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["casa"] = self.casa
        return kwargs

    def get_initial(self):
        return {"semana": self.request.GET.get("semana") or periodos.semana(datetime.date.today()).inicio.isoformat()}

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        form = ctx["form"]
        valor = form.data.get("semana") if form.is_bound else form.initial.get("semana")
        try:
            semana = periodos.semana(datetime.date.fromisoformat(valor))
        except (TypeError, ValueError):
            semana = periodos.semana(datetime.date.today())
        ctx.update(casa=self.casa, supervisor=self.supervisor, semana=semana)
        ctx.update(resumen_actividades(self.casa, semana.inicio, semana.fin))
        ctx["ya_enviado"] = (
            Reporte.objects.filter(tipo_reporte=Reporte.CASA_VIDA, id_casa_vida=self.casa, periodo=semana.etiqueta)
            .select_related("id_usuario_envia")
            .first()
        )
        return ctx

    def form_valid(self, form):
        if self.supervisor is None:
            form.add_error(None, "La Casa de Vida no tiene Supervisor de Área asignado. Comuníquese con el Pastor.")
            return self.form_invalid(form)
        semana = form.cleaned_data["semana"]
        with transaction.atomic():
            reporte = Reporte.objects.create(
                tipo_modulo=Actividad.TIPO_CASA_VIDA,
                tipo_reporte=Reporte.CASA_VIDA,
                id_usuario_envia=self.request.user,
                id_usuario_destino=self.supervisor,
                id_casa_vida=self.casa,
                id_area=self.casa.id_area,
                periodo=semana.etiqueta,
                fecha_inicio=semana.inicio,
                fecha_fin=semana.fin,
                observaciones=form.cleaned_data["observaciones"] or None,
            )
            registrar_auditoria(self.request, "ENVIAR_REPORTE", reporte)
        messages.success(self.request, f"Reporte de la {semana.nombre.lower()} enviado al Supervisor de Área.")
        return redirect("pva:reporte_detalle", pk=reporte.pk)


class EnviarReporteGeneralView(solo_roles(ROLES_SUPERVISOR), PanelCasasMixin, FormView):
    """El Supervisor envía al Pastor el reporte general mensual de su Área (RF13, CU03)."""

    template_name = "pva/reporte_enviar_general.html"
    form_class = EnviarReporteGeneralForm
    seccion = "reportes"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and rol_de(request.user) == ROLES_SUPERVISOR:
            self.area = area_del_supervisor(request.user)
            if self.area is None:
                messages.error(request, "No tienes un Área asignada.")
                return redirect("pva:reportes")
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["area"] = self.area
        return kwargs

    def get_initial(self):
        return {"mes": self.request.GET.get("mes") or periodos.mes(datetime.date.today()).inicio.isoformat()}

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        form = ctx["form"]
        valor = form.data.get("mes") if form.is_bound else form.initial.get("mes")
        try:
            mes = periodos.mes(datetime.date.fromisoformat(valor))
        except (TypeError, ValueError):
            mes = periodos.mes(datetime.date.today())
        pendientes = list(reportes_casa_pendientes(self.area, mes).order_by("id_casa_vida__nombre", "fecha_inicio"))
        con_reporte = {r.id_casa_vida_id for r in pendientes}
        ctx.update(
            area=self.area,
            mes=mes,
            pendientes=pendientes,
            casas_sin_reporte=CasaVida.objects.filter(id_area=self.area, estado=ACTIVO).exclude(pk__in=con_reporte),
            ya_enviado=Reporte.objects.filter(
                tipo_reporte=Reporte.GENERAL_AREA, id_area=self.area, periodo=mes.etiqueta
            ).first(),
        )
        return ctx

    def form_valid(self, form):
        mes = form.cleaned_data["mes"]
        with transaction.atomic():
            reporte = Reporte.objects.create(
                tipo_modulo=Actividad.TIPO_CASA_VIDA,
                tipo_reporte=Reporte.GENERAL_AREA,
                id_usuario_envia=self.request.user,
                id_area=self.area,
                periodo=mes.etiqueta,
                fecha_inicio=mes.inicio,
                fecha_fin=mes.fin,
                observaciones=form.cleaned_data["observaciones"] or None,
            )
            incluidos = reportes_casa_pendientes(self.area, mes).update(id_reporte_general=reporte)
            registrar_auditoria(self.request, "ENVIAR_REPORTE_GENERAL", reporte)
        plural = "" if incluidos == 1 else "s"
        messages.success(
            self.request,
            f"Reporte general de {mes.nombre.lower()} enviado al Pastor con {incluidos} reporte{plural} de Casas de Vida.",
        )
        return redirect("pva:reporte_detalle", pk=reporte.pk)


class GenerarReporteView(exportar.ExportableMixin, solo_roles(ROLES_PASTOR), PanelCasasMixin, TemplateView):
    """Reporte consolidado semanal, mensual o anual del Pastor (RF16, CU04). No se guarda ni se envía."""

    template_name = "pva/reporte_generar.html"
    seccion = "reportes"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        form = GenerarReporteForm(self.request.GET or None)
        ctx["form"] = form
        if form.is_bound and form.is_valid():
            ctx.update(self.consolidar(form))
        return ctx

    def consolidar(self, form):
        periodo = form.periodo
        rango = (periodo.inicio, periodo.fin)
        casas = CasaVida.objects.select_related("id_area")
        if form.cleaned_data["area"]:
            casas = casas.filter(id_area=form.cleaned_data["area"])
        if form.cleaned_data["casa"]:
            casas = casas.filter(pk=form.cleaned_data["casa"].pk)

        def por_casa(qs, campo="id_casa_vida", **anotaciones):
            return {fila[campo]: fila for fila in qs.values(campo).annotate(**anotaciones)}

        actividades = por_casa(
            Actividad.objects.filter(tipo_modulo=Actividad.TIPO_CASA_VIDA, fecha__range=rango, id_casa_vida__in=casas),
            n=Count("id_actividad", distinct=True),
            presentes=Count("asistencia", filter=Q(asistencia__presente=True)),
            registros=Count("asistencia"),
        )
        miembros = por_casa(
            CasaVidaMiembro.objects.filter(estado=ACTIVO, id_participante__estado=ACTIVO, id_casa_vida__in=casas),
            n=Count("id_casa_vida_miembro"),
        )
        nuevos = por_casa(
            CasaVidaMiembro.objects.filter(fecha_ingreso__range=rango, id_casa_vida__in=casas),
            n=Count("id_casa_vida_miembro"),
        )
        seguimientos = por_casa(
            Seguimiento.objects.filter(
                tipo_modulo=Actividad.TIPO_CASA_VIDA,
                fecha__range=rango,
                id_participante__casavidamiembro__estado=ACTIVO,
                id_participante__casavidamiembro__id_casa_vida__in=casas,
            ),
            campo="id_participante__casavidamiembro__id_casa_vida",
            n=Count("id_seguimiento", distinct=True),
        )
        reportes = por_casa(
            Reporte.objects.filter(tipo_reporte=Reporte.CASA_VIDA, fecha_inicio__range=rango, id_casa_vida__in=casas),
            n=Count("id_reporte"),
        )
        semanas_esperadas = periodos.lunes_transcurridos(periodo)

        filas = []
        for casa in casas.order_by("id_area__nombre", "nombre"):
            act = actividades.get(casa.pk, {})
            if casa.estado != ACTIVO and not act:
                continue
            presentes, registros = act.get("presentes", 0), act.get("registros", 0)
            filas.append({
                "casa": casa,
                "actividades": act.get("n", 0),
                "presentes": presentes,
                "registros": registros,
                "porcentaje": round(presentes * 100 / registros) if registros else None,
                "participantes": miembros.get(casa.pk, {}).get("n", 0),
                "nuevos": nuevos.get(casa.pk, {}).get("n", 0),
                "seguimientos": seguimientos.get(casa.pk, {}).get("n", 0),
                "reportes": reportes.get(casa.pk, {}).get("n", 0),
            })

        total = {k: sum(f[k] for f in filas) for k in ("actividades", "presentes", "registros", "participantes", "nuevos", "seguimientos", "reportes")}
        total["porcentaje"] = round(total["presentes"] * 100 / total["registros"]) if total["registros"] else None
        generales = Reporte.objects.filter(
            tipo_reporte=Reporte.GENERAL_AREA,
            fecha_inicio__range=rango,
            id_area__in=casas.values("id_area"),
        ).select_related("id_area", "id_usuario_envia").order_by("fecha_inicio", "id_area__nombre")
        return {
            "periodo": periodo,
            "filas": filas,
            "total": total,
            "semanas_esperadas": semanas_esperadas,
            "generales": generales,
            "hay_datos": any(f["actividades"] or f["reportes"] or f["seguimientos"] or f["nuevos"] for f in filas),
        }

    def documento_exportable(self, ctx):
        if "periodo" not in ctx:
            return None
        form = ctx["form"]
        filtros = [("Área", form.cleaned_data["area"] or "Todas"), ("Casa de Vida", form.cleaned_data["casa"] or "Todas"),
                   ("Reportes semanales esperados por casa", ctx["semanas_esperadas"])]
        return exportar.Documento(
            titulo="Reporte consolidado de Casas de Vida",
            periodo=f"{ctx['periodo'].nombre} ({ctx['periodo'].inicio:%d/%m/%Y} al {ctx['periodo'].fin:%d/%m/%Y})",
            datos=filtros,
            tablas=[
                exportar.Tabla(
                    "Casas de Vida",
                    [("Área", exportar.TEXTO), ("Casa de Vida", exportar.TEXTO), ("Actividades", exportar.ENTERO),
                     ("Presentes", exportar.ENTERO), ("Registros", exportar.ENTERO), ("Asistencia", exportar.PORCENTAJE),
                     ("Participantes", exportar.ENTERO), ("Nuevos", exportar.ENTERO), ("Seguimientos", exportar.ENTERO),
                     ("Reportes enviados", exportar.ENTERO)],
                    [[f["casa"].id_area.nombre if f["casa"].id_area_id else "", f["casa"].nombre, f["actividades"], f["presentes"],
                      f["registros"], f["porcentaje"], f["participantes"], f["nuevos"], f["seguimientos"], f["reportes"]]
                     for f in ctx["filas"]],
                    total=["Total", "", *[ctx["total"][k] for k in ("actividades", "presentes", "registros", "porcentaje",
                                                                    "participantes", "nuevos", "seguimientos", "reportes")]],
                ),
                exportar.Tabla(
                    "Reportes generales de los Supervisores",
                    [("Mes", exportar.TEXTO), ("Área", exportar.TEXTO), ("Supervisor", exportar.TEXTO), ("Observaciones", exportar.TEXTO)],
                    [[r.periodo, r.id_area.nombre, r.id_usuario_envia.nombre_completo, r.observaciones or ""] for r in ctx["generales"]],
                    vacio="Ningún Supervisor ha enviado reportes generales en este periodo.",
                ),
            ],
            nombre_archivo=f"reporte_casas_de_vida_{ctx['periodo'].etiqueta}",
        )
