from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def panel_escuelas(request):
    return render(request, "formacion/panel_escuelas.html", {"user": request.user})
