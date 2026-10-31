from decimal import Decimal, InvalidOperation

from django import template

register = template.Library()


@register.filter
def pesos(valor):
    """Formatea un valor en pesos colombianos: 1234567.5 -> $1.234.568"""
    try:
        numero = Decimal(valor or 0).quantize(Decimal("1"))
    except (InvalidOperation, TypeError, ValueError):
        return valor
    return "$" + f"{numero:,.0f}".replace(",", ".")
