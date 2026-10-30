from django.shortcuts import render
from nucleo.permissions import module_required
from nucleo.utils import sesion_js


@module_required("ESCUELAS_FORMACION")
def panel_escuelas(request):
    return render(
        request,
        "panel-escuelas-formacion.html",
        {"user": request.user, "sesion_js": sesion_js(request.user)},
    )
