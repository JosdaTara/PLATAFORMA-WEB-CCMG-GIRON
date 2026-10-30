"""Periodos de reporte: semana (lunes a domingo), mes y año (RF13, RF14, RF16)."""
import calendar
import datetime
from typing import NamedTuple

MESES = [
    "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
]


class Periodo(NamedTuple):
    etiqueta: str          # valor guardado en reporte.periodo, p. ej. 2026-S44, 2026-10, 2026
    inicio: datetime.date
    fin: datetime.date
    nombre: str            # texto para mostrar

    def contiene(self, fecha):
        return self.inicio <= fecha <= self.fin


def semana(fecha):
    inicio = fecha - datetime.timedelta(days=fecha.weekday())
    fin = inicio + datetime.timedelta(days=6)
    anio, numero, _ = fecha.isocalendar()
    return Periodo(
        f"{anio}-S{numero:02d}", inicio, fin,
        f"Semana {numero} · {inicio:%d/%m/%Y} al {fin:%d/%m/%Y}",
    )


def mes(fecha):
    inicio = fecha.replace(day=1)
    fin = fecha.replace(day=calendar.monthrange(fecha.year, fecha.month)[1])
    return Periodo(f"{fecha:%Y-%m}", inicio, fin, f"{MESES[fecha.month - 1].capitalize()} de {fecha.year}")


def anio(fecha):
    return Periodo(
        str(fecha.year), datetime.date(fecha.year, 1, 1), datetime.date(fecha.year, 12, 31), f"Año {fecha.year}"
    )


POR_TIPO = {"semanal": semana, "mensual": mes, "anual": anio}


def semanas_recientes(cantidad, hoy=None):
    """Semanas desde la actual hacia atrás."""
    hoy = hoy or datetime.date.today()
    return [semana(hoy - datetime.timedelta(weeks=i)) for i in range(cantidad)]


def meses_recientes(cantidad, hoy=None):
    """Meses desde el actual hacia atrás."""
    fecha = (hoy or datetime.date.today()).replace(day=1)
    meses = []
    for _ in range(cantidad):
        meses.append(mes(fecha))
        fecha = (fecha - datetime.timedelta(days=1)).replace(day=1)
    return meses


def lunes_transcurridos(periodo, hoy=None):
    """Semanas del periodo que ya empezaron (reportes semanales esperados)."""
    hoy = hoy or datetime.date.today()
    fin = min(periodo.fin, hoy)
    lunes = periodo.inicio + datetime.timedelta(days=(7 - periodo.inicio.weekday()) % 7)
    if lunes > fin:
        return 0
    return (fin - lunes).days // 7 + 1
