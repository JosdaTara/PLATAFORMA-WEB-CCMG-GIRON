from django.urls import path, include

urlpatterns = [
    path("", include("publico.urls")),
    path("cuentas/", include("cuentas.urls")),
    path("pva/", include("pva.urls")),
    path("formacion/", include("formacion.urls")),
    path("ofrendas/", include("ofrendas.urls")),
]
