from django.urls import path
from . import views

app_name = "ofrendas"

urlpatterns = [
    path("", views.OfrendaListView.as_view(), name="index"),
    path("nueva/", views.OfrendaCreateView.as_view(), name="crear"),
    path("<int:pk>/editar/", views.OfrendaUpdateView.as_view(), name="editar"),
]
