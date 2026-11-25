"""Aviso de descarga terminada para el botón con loader.

Un archivo adjunto no recarga la página, así que el navegador no sabe cuándo llegó. El botón
de descarga añade ?descarga_token=<aleatorio>; cuando la respuesta es un adjunto, aquí se
devuelve una cookie con ese mismo valor y el JS restaura el botón al verla.
"""
import re

from django.http import JsonResponse

COOKIE = "descarga_token"
TOKEN_VALIDO = re.compile(r"^[A-Za-z0-9]{8,64}$")


def _hay_nulos(datos):
    return any("\x00" in texto for clave, valores in datos.lists() for texto in (clave, *valores))


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


class SinNulosMiddleware:
    """Quita el carácter nulo (\x00) de los parámetros de la URL y rechaza los formularios que lo traen.

    PostgreSQL no admite \x00 en un texto: sin esto, escribirlo en una búsqueda o en un formulario
    termina en un error 500. En la URL (búsquedas y filtros) se descarta sin avisar; en un envío
    (POST) se responde 400, porque ningún usuario lo escribe a propósito.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if _hay_nulos(request.GET):
            limpio = request.GET.copy()
            for clave in list(limpio.keys()):
                valores = [v.replace("\x00", "") for v in limpio.getlist(clave)]
                del limpio[clave]
                limpio.setlist(clave.replace("\x00", ""), valores)
            request.GET = limpio
        if request.method == "POST" and _hay_nulos(request.POST):
            return JsonResponse({"error": "El texto contiene caracteres no permitidos."}, status=400)
        return self.get_response(request)
