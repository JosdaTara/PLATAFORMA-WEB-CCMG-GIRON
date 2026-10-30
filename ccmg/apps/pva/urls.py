from django.urls import path
from . import views, views_importacion, views_reportes, views_seguimiento

app_name = "pva"

urlpatterns = [
    path("panel/", views.panel_casas, name="panel"),
    # Áreas (solo Pastor)
    path("areas/", views.AreaListView.as_view(), name="areas"),
    path("areas/nueva/", views.AreaCreateView.as_view(), name="area_crear"),
    path("areas/<int:pk>/editar/", views.AreaUpdateView.as_view(), name="area_editar"),
    path("areas/<int:pk>/<str:accion>/", views.AreaEstadoView.as_view(), name="area_estado"),
    # Casas de Vida
    path("casas/", views.CasaListView.as_view(), name="casas"),
    path("casas/nueva/", views.CasaCreateView.as_view(), name="casa_crear"),
    path("casas/<int:pk>/", views.CasaDetailView.as_view(), name="casa_detalle"),
    path("casas/<int:pk>/editar/", views.CasaUpdateView.as_view(), name="casa_editar"),
    path("casas/<int:pk>/<str:accion>/", views.CasaEstadoView.as_view(), name="casa_estado"),
    # Participantes
    path("participantes/", views.ParticipanteListView.as_view(), name="participantes"),
    path("participantes/nuevo/", views.ParticipanteCreateView.as_view(), name="participante_crear"),
    path("participantes/<int:pk>/", views.ParticipanteDetailView.as_view(), name="participante_detalle"),
    path("participantes/<int:pk>/editar/", views.ParticipanteUpdateView.as_view(), name="participante_editar"),
    path("participantes/<int:pk>/<str:accion>/", views.ParticipanteEstadoView.as_view(), name="participante_estado"),
    # Asistencia
    path("asistencia/", views.AsistenciaListView.as_view(), name="asistencia"),
    path("asistencia/registrar/", views.RegistrarAsistenciaView.as_view(), name="asistencia_registrar"),
    path("asistencia/<int:pk>/", views.AsistenciaDetailView.as_view(), name="asistencia_detalle"),
    # Seguimiento
    path("seguimiento/", views_seguimiento.SeguimientoListView.as_view(), name="seguimientos"),
    path("seguimiento/nuevo/", views_seguimiento.SeguimientoCreateView.as_view(), name="seguimiento_crear"),
    path("seguimiento/<int:pk>/editar/", views_seguimiento.SeguimientoUpdateView.as_view(), name="seguimiento_editar"),
    # Reportes
    path("reportes/", views_reportes.ReporteListView.as_view(), name="reportes"),
    path("reportes/enviar/", views_reportes.EnviarReporteCasaView.as_view(), name="reporte_enviar_casa"),
    path("reportes/enviar-general/", views_reportes.EnviarReporteGeneralView.as_view(), name="reporte_enviar_general"),
    path("reportes/generar/", views_reportes.GenerarReporteView.as_view(), name="reporte_generar"),
    path("reportes/<int:pk>/", views_reportes.ReporteDetailView.as_view(), name="reporte_detalle"),
    # Importación de datos (solo Pastor)
    path("importar/", views_importacion.ImportarView.as_view(), name="importar"),
    path("importar/vista-previa/", views_importacion.VistaPreviaView.as_view(), name="importar_vista_previa"),
    path("importar/resultado/", views_importacion.ResultadoView.as_view(), name="importar_resultado"),
    path("importar/detalle.csv", views_importacion.DetalleErroresView.as_view(), name="importar_detalle"),
    path("importar/plantilla/<str:tipo>/", views_importacion.PlantillaView.as_view(), name="importar_plantilla"),
]
