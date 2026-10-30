from django.shortcuts import render
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied

from nucleo.mixins import PastorRequiredMixin


class OfrendasIndexView(PastorRequiredMixin):
    def get(self, request, *args, **kwargs):
        return render(request, "ofrendas/en-construccion.html")


def index(request):
    if not request.user.is_authenticated:
        return redirect_to_login(request.get_full_path())
    rol = getattr(getattr(request.user, "rol", None), "nombre", None)
    if rol != "PASTOR":
        raise PermissionDenied("Solo el Pastor puede realizar esta acción.")
    return render(request, "ofrendas/en-construccion.html")
