"""Búsqueda de texto que ignora mayúsculas y tildes, y que no revienta con caracteres inválidos.

PostgreSQL rechaza el carácter nulo (\x00) en cualquier texto (DataError → error 500), así que se
quita de lo que escribe el usuario. La comparación sin tildes usa `translate` en vez de la extensión
`unaccent`: no exige permisos de superusuario para crearla en cada base de datos (producción, demo y
pruebas) y se comporta igual en todas.
"""
from django.db.models import CharField, Q, TextField, Transform

CON_TILDES = "ÁÀÄÂÃáàäâãÉÈËÊéèëêÍÌÏÎíìïîÓÒÖÔÕóòöôõÚÙÜÛúùüûÑñÇç"
SIN_TILDES = "a" * 10 + "e" * 8 + "i" * 8 + "o" * 10 + "u" * 8 + "nn" + "cc"
_TABLA = str.maketrans(CON_TILDES, SIN_TILDES)


def quitar_nulos(texto):
    return (texto or "").replace("\x00", "")


def normalizar(texto):
    """Minúsculas, sin tildes y con los espacios sobrantes quitados (para comparar y buscar)."""
    return " ".join(quitar_nulos(texto).translate(_TABLA).lower().split())


@CharField.register_lookup
@TextField.register_lookup
class SinTildes(Transform):
    """`campo__sin_tildes__contains="gomez"` encuentra «Gómez», sin importar mayúsculas."""

    lookup_name = "sin_tildes"
    output_field = CharField()

    def as_sql(self, compiler, connection):
        sql, params = compiler.compile(self.lhs)
        return f"translate(lower({sql}), '{CON_TILDES}', '{SIN_TILDES}')", params


def filtrar_texto(qs, texto, campos):
    """Filtra `qs` por texto libre: cada palabra debe aparecer en alguno de los `campos`."""
    for palabra in normalizar(texto).split():
        filtro = Q()
        for campo in campos:
            filtro |= Q(**{f"{campo}__sin_tildes__contains": palabra})
        qs = qs.filter(filtro)
    return qs
