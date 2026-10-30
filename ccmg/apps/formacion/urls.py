from django.urls import path
from . import views

app_name = "formacion"

urlpatterns = [
    path("panel/", views.panel_escuelas, name="panel"),
    # Procesos (Pasos de Vida, Escuelas Vida, Módulos de Liderazgo, Misiones)
    path("procesos/", views.ProcesoListView.as_view(), name="procesos"),
    path("procesos/nuevo/", views.ProcesoCreateView.as_view(), name="proceso_crear"),
    path("procesos/<int:pk>/", views.ProcesoDetailView.as_view(), name="proceso_detalle"),
    path("procesos/<int:pk>/editar/", views.ProcesoUpdateView.as_view(), name="proceso_editar"),
    # Antes que proceso_estado: si no, «actividad» se tomaría como una acción de estado.
    path("procesos/<int:proceso>/actividad/", views.RegistrarActividadView.as_view(), name="actividad_registrar"),
    path("procesos/<int:pk>/<str:accion>/", views.ProcesoEstadoView.as_view(), name="proceso_estado"),
    # Participantes e inscripciones
    path("participantes/", views.ParticipanteListView.as_view(), name="participantes"),
    path("participantes/nuevo/", views.NuevoParticipanteView.as_view(), name="participante_crear"),
    path("participantes/inscribir/", views.InscribirExistenteView.as_view(), name="inscribir"),
    path("participantes/<int:pk>/", views.ParticipanteDetailView.as_view(), name="participante_detalle"),
    path("participantes/<int:pk>/editar/", views.ParticipanteUpdateView.as_view(), name="participante_editar"),
    path("inscripciones/<int:pk>/<str:accion>/", views.InscripcionEstadoView.as_view(), name="inscripcion_estado"),
    # Actividades y asistencia
    path("actividades/", views.ActividadListView.as_view(), name="actividades"),
    path("actividades/<int:pk>/", views.ActividadDetailView.as_view(), name="actividad_detalle"),
    # Seguimiento
    path("seguimiento/", views.SeguimientoListView.as_view(), name="seguimientos"),
    path("seguimiento/nuevo/", views.SeguimientoCreateView.as_view(), name="seguimiento_crear"),
    path("seguimiento/<int:pk>/editar/", views.SeguimientoUpdateView.as_view(), name="seguimiento_editar"),
    # Reportes
    path("reportes/", views.ReporteFormacionView.as_view(), name="reportes"),
]
