from django.shortcuts import render


def index(request):
    return render(request, "publico/index.html")


def privacidad(request):
    """Aviso de privacidad y política de tratamiento de datos personales (Ley 1581 de 2012)."""
    return render(request, "publico/privacidad.html")
