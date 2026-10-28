from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from nucleo.mixins import ModuleRequiredMixin


@login_required
def panel_casas(request):
    return render(request, "pva/panel_casas.html", {"user": request.user})
