"""Exportación de reportes a Excel (.xlsx) y PDF (RF27, HU-43).

Cada vista describe su reporte una sola vez como un `Documento` y este módulo lo convierte
al formato pedido. El archivo incluye el periodo, la fecha de generación y quién lo generó,
y se arma con el mismo contexto que la página, así que solo contiene lo que el rol puede ver.
"""
import datetime
import io
from dataclasses import dataclass, field
from decimal import Decimal

from django.http import Http404, HttpResponse
from django.utils import timezone
from django.utils.text import slugify

FORMATOS = ("pdf", "xlsx")
VERDE = "00674F"
AVISO_PRIVACIDAD = (
    "Documento confidencial: contiene datos personales tratados conforme a la Ley 1581 de 2012. "
    "No lo comparta fuera de los responsables del Plan Vida Abundante."
)

# Tipos de columna: definen cómo se muestra cada valor en el PDF y el formato de celda en Excel.
TEXTO, ENTERO, PORCENTAJE, PESOS, FECHA = "texto", "entero", "porcentaje", "pesos", "fecha"


@dataclass
class Tabla:
    titulo: str
    columnas: list            # [(encabezado, tipo)]
    filas: list               # listas de valores en el orden de las columnas
    total: list = None        # fila de totales opcional
    vacio: str = "Sin registros."


@dataclass
class Documento:
    titulo: str
    periodo: str
    datos: list = field(default_factory=list)    # [(etiqueta, valor)] que describen el reporte
    tablas: list = field(default_factory=list)
    nombre_archivo: str = "reporte"


def _texto(valor, tipo):
    if valor is None or valor == "":
        return "—"
    if tipo == PORCENTAJE:
        return f"{valor}%"
    if tipo == PESOS:
        return "$" + f"{Decimal(valor).quantize(Decimal('1')):,.0f}".replace(",", ".")
    if tipo == FECHA and isinstance(valor, (datetime.date, datetime.datetime)):
        return valor.strftime("%d/%m/%Y")
    if isinstance(valor, datetime.datetime):
        return timezone.localtime(valor).strftime("%d/%m/%Y %H:%M") if timezone.is_aware(valor) else valor.strftime("%d/%m/%Y %H:%M")
    if isinstance(valor, datetime.date):
        return valor.strftime("%d/%m/%Y")
    return str(valor)


def _encabezado(documento, usuario):
    generado = timezone.localtime().strftime("%d/%m/%Y %H:%M")
    quien = getattr(usuario, "nombre_completo", "") or getattr(usuario, "correo", "")
    return [("Periodo", documento.periodo), *documento.datos, ("Generado", f"{generado} por {quien}")]


# ----------------------------------------------------------------- Excel


def a_xlsx(documento, usuario):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill

    libro = Workbook()
    hoja = libro.active
    hoja.title = "Reporte"
    hoja.append([documento.titulo])
    hoja["A1"].font = Font(bold=True, size=14, color=VERDE)
    for etiqueta, valor in _encabezado(documento, usuario):
        hoja.append([etiqueta, _texto(valor, TEXTO)])
        hoja.cell(hoja.max_row, 1).font = Font(bold=True)

    anchos = {}
    for tabla in documento.tablas:
        hoja.append([])
        hoja.append([tabla.titulo])
        hoja.cell(hoja.max_row, 1).font = Font(bold=True, size=12)
        hoja.append([c[0] for c in tabla.columnas])
        for celda in hoja[hoja.max_row]:
            celda.font = Font(bold=True, color="FFFFFF")
            celda.fill = PatternFill("solid", fgColor=VERDE)
        if not tabla.filas:
            hoja.append([tabla.vacio])
        for fila in tabla.filas + ([tabla.total] if tabla.total else []):
            hoja.append([_valor_xlsx(v, tipo) for v, (_, tipo) in zip(fila, tabla.columnas)])
            for celda, (_, tipo) in zip(hoja[hoja.max_row], tabla.columnas):
                if tipo == PESOS:
                    celda.number_format = '"$"#,##0'
                elif tipo == FECHA:
                    celda.number_format = "DD/MM/YYYY"
                celda.alignment = Alignment(vertical="top", wrap_text=tipo == TEXTO)
            if fila is tabla.total:
                for celda in hoja[hoja.max_row]:
                    celda.font = Font(bold=True)
        for i, (encabezado, tipo) in enumerate(tabla.columnas, start=1):
            largo = max([len(encabezado)] + [len(_texto(f[i - 1], tipo)) for f in tabla.filas[:200]])
            anchos[i] = max(anchos.get(i, 12), min(largo + 2, 60))

    for i, ancho in anchos.items():
        hoja.column_dimensions[hoja.cell(1, i).column_letter].width = ancho
    hoja.column_dimensions["A"].width = max(anchos.get(1, 12), 18)
    hoja.append([])
    hoja.append([AVISO_PRIVACIDAD])
    hoja.cell(hoja.max_row, 1).font = Font(italic=True, size=9, color="666666")

    salida = io.BytesIO()
    libro.save(salida)
    return salida.getvalue()


def _valor_xlsx(valor, tipo):
    if valor is None or valor == "":
        return None
    if tipo == PESOS:
        return float(valor)
    if isinstance(valor, datetime.datetime):
        return _texto(valor, tipo)
    if isinstance(valor, (int, float, Decimal, datetime.date)):
        return valor
    return str(valor)


# ----------------------------------------------------------------- PDF


def a_pdf(documento, usuario):
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import landscape, letter
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import cm
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

    estilos = getSampleStyleSheet()
    titulo = ParagraphStyle("titulo", parent=estilos["Title"], textColor=colors.HexColor("#" + VERDE), alignment=0, fontSize=16)
    celda = ParagraphStyle("celda", parent=estilos["BodyText"], fontSize=8, leading=10)
    negrita = ParagraphStyle("negrita", parent=celda, fontName="Helvetica-Bold")
    celda_bold = ParagraphStyle("celda_bold", parent=negrita, textColor=colors.white, fontSize=7, leading=9, splitLongWords=0)
    nota = ParagraphStyle("nota", parent=estilos["BodyText"], fontSize=7, textColor=colors.grey)

    def p(texto, estilo=celda):
        return Paragraph(str(texto).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br/>"), estilo)

    salida = io.BytesIO()
    pdf = SimpleDocTemplate(
        salida, pagesize=landscape(letter), leftMargin=1.5 * cm, rightMargin=1.5 * cm,
        topMargin=1.5 * cm, bottomMargin=1.5 * cm, title=documento.titulo, author="CCMG Girón · PVA",
    )
    ancho = pdf.width
    contenido = [Paragraph(documento.titulo, titulo)]

    datos = [[p(e, negrita), p(_texto(v, TEXTO))] for e, v in _encabezado(documento, usuario)]
    tabla_datos = Table(datos, colWidths=[5.5 * cm, ancho - 5.5 * cm])
    tabla_datos.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                                     ("BOTTOMPADDING", (0, 0), (-1, -1), 2), ("TOPPADDING", (0, 0), (-1, -1), 2)]))
    contenido += [tabla_datos, Spacer(1, 0.4 * cm)]

    for tabla in documento.tablas:
        contenido.append(Paragraph(tabla.titulo, estilos["Heading3"]))
        filas = [[p(c[0], celda_bold) for c in tabla.columnas]]
        filas += [[p(_texto(v, tipo)) for v, (_, tipo) in zip(f, tabla.columnas)] for f in tabla.filas]
        if tabla.total:
            filas.append([p(_texto(v, tipo), negrita) for v, (_, tipo) in zip(tabla.total, tabla.columnas)])
        if not tabla.filas:
            filas.append([p(tabla.vacio)] + [""] * (len(tabla.columnas) - 1))
        # Las columnas de texto reciben más ancho que las numéricas.
        pesos = [1.5 if tipo == TEXTO else 1 for _, tipo in tabla.columnas]
        t = Table(filas, colWidths=[ancho * w / sum(pesos) for w in pesos], repeatRows=1)
        estilo = [
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#" + VERDE)),
            ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#CCCCCC")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F5F3EE")]),
        ]
        if tabla.total:
            estilo.append(("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#E8E2D0")))
        if not tabla.filas:
            estilo.append(("SPAN", (0, 1), (-1, 1)))
        t.setStyle(TableStyle(estilo))
        contenido += [t, Spacer(1, 0.4 * cm)]

    contenido.append(Paragraph(AVISO_PRIVACIDAD, nota))

    def pie(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 7)
        canvas.setFillColor(colors.grey)
        canvas.drawString(doc.leftMargin, 0.8 * cm, "CCMG Girón · Plan Vida Abundante")
        canvas.drawRightString(doc.leftMargin + doc.width, 0.8 * cm, f"Página {doc.page}")
        canvas.restoreState()

    pdf.build(contenido, onFirstPage=pie, onLaterPages=pie)
    return salida.getvalue()


# ----------------------------------------------------------------- Respuesta HTTP


def respuesta(documento, formato, usuario):
    fecha = timezone.localdate().isoformat()
    nombre = f"{slugify(documento.nombre_archivo) or 'reporte'}_{fecha}.{formato}"
    if formato == "pdf":
        contenido, tipo = a_pdf(documento, usuario), "application/pdf"
    else:
        contenido, tipo = a_xlsx(documento, usuario), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    r = HttpResponse(contenido, content_type=tipo)
    r["Content-Disposition"] = f'attachment; filename="{nombre}"'
    return r


class ExportableMixin:
    """Si la petición trae ?formato=pdf|xlsx, devuelve el archivo en lugar de la página.

    La vista implementa `documento_exportable(context)`, construido con el mismo contexto
    de la página, por lo que el archivo respeta el alcance del rol (HU-43, criterio 2).
    """

    def render_to_response(self, context, **kwargs):
        formato = self.request.GET.get("formato")
        if formato in FORMATOS:
            documento = self.documento_exportable(context)
            if documento is None:
                raise Http404
            return respuesta(documento, formato, self.request.user)
        return super().render_to_response(context, **kwargs)
