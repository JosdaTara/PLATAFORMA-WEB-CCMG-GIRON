from django.shortcuts import redirect
from django.urls import reverse


class ForzarCambioPasswordMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            return self.get_response(request)

        user = request.user
        if not getattr(user, "debe_cambiar_password", False):
            return self.get_response(request)

        path = request.path

        if path.startswith("/static/") or path.startswith("/media/"):
            return self.get_response(request)

        allowed_paths = [
            reverse("cuentas:cambiar_password"),
            reverse("cuentas:logout"),
        ]

        if path in allowed_paths:
            return self.get_response(request)

        if path.startswith("/cuentas/recuperar/"):
            return self.get_response(request)

        return redirect("cuentas:cambiar_password")
