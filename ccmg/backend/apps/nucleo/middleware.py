"""Aviso de descarga terminada para el botón con loader.

Un archivo adjunto no recarga la página, así que el navegador no sabe cuándo llegó. El botón
de descarga añade ?descarga_token=<aleatorio>; cuando la respuesta es un adjunto, aquí se
devuelve una cookie con ese mismo valor y el JS restaura el botón al verla.
"""
import re

COOKIE = "descarga_token"
TOKEN_VALIDO = re.compile(r"^[A-Za-z0-9]{8,64}$")


class DescargaTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        token = request.GET.get(COOKIE, "")
        if token and TOKEN_VALIDO.match(token) and "attachment" in response.get("Content-Disposition", ""):
            # Sin HttpOnly: la lee el JS de la propia página. No contiene datos, solo el número aleatorio.
            response.set_cookie(COOKIE, token, max_age=60, samesite="Lax", path="/")
        return response
