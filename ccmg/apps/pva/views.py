from django.shortcuts import render
from nucleo.permissions import module_required
from nucleo.utils import sesion_js


@module_required("CASAS_VIDA")
def panel_casas(request):
    return render(
        request,
        "panel-casas-vida.html",
        {"user": request.user, "sesion_js": sesion_js(request.user)},
    )
