"""Reportes del módulo Casas de Vida.

Flujo (RN06, RN07, RN19): el Líder o su equipo llenan el reporte de asistencia de la semana con los
totales de la reunión y queda enviado al Supervisor de Área; el Supervisor envía al Pastor un reporte
general mensual de su Área; el Pastor, último receptor, consulta los reportes y genera consolidados.
"""
import datetime
from decimal import Decimal

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import Count, F
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
from .forms import EnviarReporteGeneralForm, GenerarReporteForm, reportes_casa_pendientes
from .models import ACTIVO, Actividad, CasaVida, CasaVidaMiembro, Reporte, ReporteAsistencia, Seguimiento
from .views import PanelCasasMixin

# Columnas que se suman en los consolidados, en el orden del formato de la iglesia.
COLUMNAS_SUMA = [
    ("asistentes", "Asistentes"),
    ("lideres_servidores", "Líderes servidores"),
    ("ninos", "Niños"),
    ("nuevos", "Nuevos"),
    ("conversiones", "Conversiones"),
    ("reconciliaciones", "Reconciliaciones"),
    ("ausentes", "Ausentes"),
    ("discipulos", "Discípulos Escuelas"),
    ("vea", "VEA"),
    ("sabado", "Sábado"),
    ("dominical", "Dominical"),
]


def asistencia_de(reporte):
    """Totales de la reunión de un reporte semanal (None en reportes anteriores al cambio)."""
    try:
        return reporte.asistencia
    except ReporteAsistencia.DoesNotExist:
        return None


def sumar(asistencias):
    """Suma los totales de varias reuniones; el sábado solo cuenta donde se reporta."""
    asistencias = [a for a in asistencias if a is not None]
    total = {"reuniones": len(asistencias), "ofrenda": sum((a.ofrenda for a in asistencias), Decimal(0))}
    for campo, _ in COLUMNAS_SUMA:
        if campo == "discipulos":
            total[campo] = sum(a.total_discipulos_escuelas for a in asistencias)
        else:
            total[campo] = sum(getattr(a, campo) or 0 for a in asistencias)
    total["hay_sabado"] = any(a.sabado is not None for a in asistencias)
    return total


def filas_detalle(asistencia):
    """Filas (indicador, valor) del reporte de asistencia, agrupadas como en el formato de la iglesia."""
    grupos = [
        ("Asistencia", [(e, getattr(asistencia, c)) for c, e in ReporteAsistencia.INDICADORES]),
        ("Asistencia Escuelas de Formación", [(e, getattr(asistencia, c)) for c, e in ReporteAsistencia.ESCUELAS]
         + [("Total discípulos escuelas", asistencia.total_discipulos_escuelas)]),
        ("Cultos", [(e, getattr(asistencia, c)) for c, e in ReporteAsistencia.CULTOS
                    if not (c == "sabado" and asistencia.sabado is None)]),
    ]
    return grupos


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
            filas = [
                {"reporte": rc, "asistencia": asistencia_de(rc)}
                for rc in r.reportes_casa.select_related("id_casa_vida", "id_usuario_envia", "asistencia")
                .order_by("id_casa_vida__nombre", "fecha_inicio")
            ]
            ctx["filas"] = filas
            ctx["total"] = sumar(f["asistencia"] for f in filas)
        else:
            asistencia = asistencia_de(r)
            ctx["asistencia"] = asistencia
            ctx["grupos"] = filas_detalle(asistencia) if asistencia else []
        return ctx

    def documento_exportable(self, ctx):
        r = self.object
        periodo = f"{r.fecha_inicio:%d/%m/%Y} al {r.fecha_fin:%d/%m/%Y} ({r.periodo})"
        if r.es_general:
            columnas = [("Casa de Vida", exportar.TEXTO), ("Fecha", exportar.FECHA)]
            columnas += [(e, exportar.ENTERO) for _, e in COLUMNAS_SUMA] + [("Ofrenda", exportar.PESOS)]
            filas = []
            for f in ctx["filas"]:
                a = f["asistencia"]
                fila = [f["reporte"].id_casa_vida.nombre, a.fecha if a else None]
                if a:
                    fila += [a.total_discipulos_escuelas if c == "discipulos" else getattr(a, c) for c, _ in COLUMNAS_SUMA]
                    fila.append(a.ofrenda)
                else:
                    fila += [None] * (len(COLUMNAS_SUMA) + 1)
                filas.append(fila)
            t = ctx["total"]
            return exportar.Documento(
                titulo=f"Reporte general · Área {r.id_area.nombre}",
                periodo=periodo,
                datos=[("Supervisor", r.id_usuario_envia.nombre_completo), ("Enviado", r.enviado_en),
                       ("Observaciones", r.observaciones or "—")],
                tablas=[exportar.Tabla(
                    "Reportes de asistencia de las Casas de Vida", columnas, filas,
                    total=["Total", "", *[t[c] for c, _ in COLUMNAS_SUMA], t["ofrenda"]],
                )],
                nombre_archivo=f"reporte_general_{r.id_area.nombre}_{r.periodo}",
            )
        a = ctx["asistencia"]
        datos = [
            ("Área", r.id_casa_vida.id_area.nombre if r.id_casa_vida.id_area_id else "—"),
            ("Fecha de la reunión", a.fecha if a else "—"),
            ("Líder", a.id_lider.nombre_completo if a and a.id_lider else "—"),
            ("Enviado por", r.id_usuario_envia.nombre_completo),
            ("Enviado a", r.id_usuario_destino.nombre_completo if r.id_usuario_destino else "Supervisor de Área"),
            ("Enviado", r.enviado_en),
            ("Observaciones", r.observaciones or "—"),
        ]
        tablas = [
            exportar.Tabla(titulo, [("Indicador", exportar.TEXTO), ("Total", exportar.ENTERO)], [list(f) for f in filas])
            for titulo, filas in ctx["grupos"]
        ]
        if a:
            tablas.append(exportar.Tabla("Informe financiero", [("Concepto", exportar.TEXTO), ("Valor", exportar.PESOS)],
                                         [["Ofrenda", a.ofrenda]]))
        return exportar.Documento(
            titulo=f"Reporte de asistencia · {r.id_casa_vida.nombre}",
            periodo=periodo,
            datos=datos,
            tablas=tablas,
            nombre_archivo=f"reporte_{r.id_casa_vida.nombre}_{r.periodo}",
        )


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
        pendientes = list(
            reportes_casa_pendientes(self.area, mes).select_related("asistencia").order_by("id_casa_vida__nombre", "fecha_inicio")
        )
        con_reporte = {r.id_casa_vida_id for r in pendientes}
        ctx.update(
            area=self.area,
            mes=mes,
            pendientes=[{"reporte": r, "asistencia": asistencia_de(r)} for r in pendientes],
            total=sumar(asistencia_de(r) for r in pendientes),
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
        ctx["columnas"] = COLUMNAS_SUMA
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

        def por_casa(qs, campo="id_casa_vida"):
            return {fila[campo]: fila["n"] for fila in qs.values(campo).annotate(n=Count("pk"))}

        asistencias = {}
        for a in ReporteAsistencia.objects.filter(fecha__range=rango, id_reporte__id_casa_vida__in=casas).select_related("id_reporte"):
            asistencias.setdefault(a.id_reporte.id_casa_vida_id, []).append(a)
        personas = por_casa(CasaVidaMiembro.objects.filter(fecha_ingreso__range=rango, id_casa_vida__in=casas))
        seguimientos = {
            fila["casa"]: fila["n"]
            for fila in Seguimiento.objects.filter(
                tipo_modulo=Actividad.TIPO_CASA_VIDA,
                fecha__range=rango,
                id_participante__casavidamiembro__estado=ACTIVO,
                id_participante__casavidamiembro__id_casa_vida__in=casas,
            ).values(casa=F("id_participante__casavidamiembro__id_casa_vida"))
            .annotate(n=Count("id_seguimiento", distinct=True))
        }
        reportes = por_casa(Reporte.objects.filter(tipo_reporte=Reporte.CASA_VIDA, fecha_inicio__range=rango, id_casa_vida__in=casas))
        semanas_esperadas = periodos.lunes_transcurridos(periodo)

        filas = []
        for casa in casas.order_by("id_area__nombre", "nombre"):
            propias = asistencias.get(casa.pk, [])
            if casa.estado != ACTIVO and not propias:
                continue
            filas.append({
                "casa": casa,
                **sumar(propias),
                "personas": personas.get(casa.pk, 0),
                "seguimientos": seguimientos.get(casa.pk, 0),
                "reportes": reportes.get(casa.pk, 0),
            })

        claves = ["reuniones", "ofrenda", "personas", "seguimientos", "reportes"] + [c for c, _ in COLUMNAS_SUMA]
        total = {k: sum((f[k] for f in filas), Decimal(0) if k == "ofrenda" else 0) for k in claves}
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
            "hay_datos": any(f["reuniones"] or f["reportes"] or f["seguimientos"] or f["personas"] for f in filas),
        }

    def documento_exportable(self, ctx):
        if "periodo" not in ctx:
            return None
        form = ctx["form"]
        filtros = [("Área", form.cleaned_data["area"] or "Todas"), ("Casa de Vida", form.cleaned_data["casa"] or "Todas"),
                   ("Reportes semanales esperados por casa", ctx["semanas_esperadas"])]
        columnas = [("Área", exportar.TEXTO), ("Casa de Vida", exportar.TEXTO), ("Reuniones", exportar.ENTERO)]
        columnas += [(e, exportar.ENTERO) for _, e in COLUMNAS_SUMA]
        columnas += [("Ofrenda", exportar.PESOS), ("Personas nuevas registradas", exportar.ENTERO),
                     ("Seguimientos", exportar.ENTERO), ("Reportes enviados", exportar.ENTERO)]
        claves = ["reuniones"] + [c for c, _ in COLUMNAS_SUMA] + ["ofrenda", "personas", "seguimientos", "reportes"]
        return exportar.Documento(
            titulo="Reporte consolidado de Casas de Vida",
            periodo=f"{ctx['periodo'].nombre} ({ctx['periodo'].inicio:%d/%m/%Y} al {ctx['periodo'].fin:%d/%m/%Y})",
            datos=filtros,
            tablas=[
                exportar.Tabla(
                    "Casas de Vida",
                    columnas,
                    [[f["casa"].id_area.nombre if f["casa"].id_area_id else "", f["casa"].nombre, *[f[k] for k in claves]]
                     for f in ctx["filas"]],
                    total=["Total", "", *[ctx["total"][k] for k in claves]],
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
