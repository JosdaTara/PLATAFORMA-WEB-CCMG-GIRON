from django.urls import path
from . import views

app_name = "publico"

urlpatterns = [
    path("", views.index, name="index"),
]
