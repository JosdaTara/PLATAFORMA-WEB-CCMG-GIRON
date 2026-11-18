"""Respuesta JSON común para los autocompletados de búsqueda.

El navegador consulta con debounce mientras se escribe; aquí solo se filtra el queryset que ya
viene limitado por el alcance del rol, así que nadie ve sugerencias que no podría ver en la lista.
"""
from django.db.models import Q
from django.http import JsonResponse

MIN_CARACTERES = 2
MAX_RESULTADOS = 8


def sugerencias(request, qs, campos, construir):
    """Filtra `qs` por `campos` (icontains) y devuelve hasta MAX_RESULTADOS elementos ya construidos."""
    q = request.GET.get("q", "").strip()
    if len(q) < MIN_CARACTERES:
        return JsonResponse({"resultados": []})
    filtro = Q()
    for campo in campos:
        filtro |= Q(**{f"{campo}__icontains": q})
    encontrados = qs.filter(filtro).distinct().order_by("nombres_apellidos")[:MAX_RESULTADOS]
    return JsonResponse({"resultados": [construir(obj) for obj in encontrados]})
