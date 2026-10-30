from django.urls import path
from . import views

app_name = "pva"

urlpatterns = [
    path("panel/", views.panel_casas, name="panel"),
]
