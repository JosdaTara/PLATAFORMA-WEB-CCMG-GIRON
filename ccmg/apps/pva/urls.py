from django.urls import path
from . import views

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
]
