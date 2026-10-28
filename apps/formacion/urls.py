from django.urls import path
from . import views

app_name = "formacion"

urlpatterns = [
    path("panel/", views.panel_escuelas, name="panel"),
]
