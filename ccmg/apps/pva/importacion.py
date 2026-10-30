"""Importación de Casas de Vida y participantes desde CSV o Excel (RF26, HU-42, RN25).

Cada fila se valida con los mismos formularios del registro manual (RN09, RN16), de modo que
las reglas no se duplican. Las filas cuyo registro ya existe se omiten en lugar de duplicarse.
"""
import csv
import datetime
import io
import unicodedata

from django.db import transaction

from cuentas.models import Usuario
from nucleo.utils import ROLES_LIDER, registrar_auditoria

from .forms import CasaVidaForm, ParticipanteForm
from .models import ACTIVO, Area, CasaVida, Participante
from .views import asignar_casa

MAX_FILAS = 2000
MAX_BYTES = 5 * 1024 * 1024

VALIDA, OMITIDA, ERROR = "valida", "omitida", "error"


class ErrorArchivo(Exception):
    """El archivo no se puede leer o no tiene las columnas obligatorias."""


# (clave, encabezado de la plantilla, obligatoria, alias aceptados)
COLUMNAS = {
    "casas": [
        ("nombre", "Nombre de la Casa de Vida", True, ["nombre", "casa", "casa de vida"]),
        ("area", "Área", True, ["area", "zona"]),
        ("direccion", "Dirección", False, ["direccion"]),
        ("lider_correo", "Correo del Líder", False, ["lider", "correo lider", "correo del lider", "email lider"]),
    ],
    "participantes": [
        ("nombres_apellidos", "Nombres y apellidos", True, ["nombres", "nombre", "nombre completo", "nombres apellidos"]),
        ("documento_identidad", "Documento de identidad", True, ["documento", "cedula", "numero de documento", "identificacion", "no documento"]),
        ("fecha_nacimiento", "Fecha de nacimiento", True, ["nacimiento", "fecha nacimiento"]),
        ("telefono", "Teléfono", True, ["celular", "telefono de contacto", "movil"]),
        ("direccion", "Dirección", True, ["direccion de residencia"]),
        ("casa_vida", "Casa de Vida", True, ["casa", "casa de vida"]),
        ("autorizacion_datos", "Autorización de datos", False, ["autorizacion", "autoriza tratamiento de datos", "tratamiento de datos"]),
    ],
}

TITULOS = {"casas": "Casas de Vida", "participantes": "Participantes"}

EJEMPLOS = {
    "casas": ["Casa Esperanza", "Norte", "Calle 10 # 5-20, Girón", "lider@correo.com"],
    "participantes": ["Ana María Pérez", "1095000000", "15/03/1990", "3001234567", "Carrera 8 # 12-30", "Casa Esperanza", "Sí"],
}


def normalizar(texto):
    texto = unicodedata.normalize("NFKD", str(texto or "")).encode("ascii", "ignore").decode()
    return " ".join(texto.lower().replace("_", " ").replace(".", " ").split())


def _mapa_encabezados(tipo, encabezados):
    """Relaciona cada columna del archivo con un campo de la plantilla."""
    alias = {}
    for clave, titulo, _, otros in COLUMNAS[tipo]:
        for nombre in [clave, titulo, *otros]:
            alias[normalizar(nombre)] = clave
    mapa = {}
    for indice, encabezado in enumerate(encabezados):
        clave = alias.get(normalizar(encabezado))
        if clave and clave not in mapa.values():
            mapa[indice] = clave
    faltantes = [titulo for clave, titulo, obligatoria, _ in COLUMNAS[tipo] if obligatoria and clave not in mapa.values()]
    if faltantes:
        raise ErrorArchivo("Faltan columnas obligatorias: " + ", ".join(faltantes) + ". Use la plantilla del sistema.")
    return mapa


def _texto(valor):
    """Convierte el valor de una celda en texto (los números de Excel llegan como float)."""
    if valor is None:
        return ""
    if isinstance(valor, datetime.datetime):
        return valor.date().isoformat()
    if isinstance(valor, datetime.date):
        return valor.isoformat()
    if isinstance(valor, float) and valor.is_integer():
        return str(int(valor))
    return str(valor).strip()


def leer_archivo(tipo, archivo):
    """Devuelve [{'fila': n, 'datos': {...}}] con los valores como texto."""
    if archivo.size > MAX_BYTES:
        raise ErrorArchivo("El archivo supera el tamaño máximo de 5 MB.")
    nombre = archivo.name.lower()
    if nombre.endswith(".xlsx"):
        filas = _leer_xlsx(archivo)
    elif nombre.endswith(".csv"):
        filas = _leer_csv(archivo)
    else:
        raise ErrorArchivo("Formato no admitido. Use un archivo CSV o Excel (.xlsx).")
    if not filas:
        raise ErrorArchivo("El archivo está vacío.")
    mapa = _mapa_encabezados(tipo, filas[0])
    resultado = []
    for numero, valores in enumerate(filas[1:], start=2):
        datos = {clave: _texto(valores[i]) if i < len(valores) else "" for i, clave in mapa.items()}
        if any(datos.values()):
            resultado.append({"fila": numero, "datos": datos})
    if not resultado:
        raise ErrorArchivo("El archivo no tiene filas con datos.")
    if len(resultado) > MAX_FILAS:
        raise ErrorArchivo(f"El archivo tiene {len(resultado)} filas; el máximo por importación es {MAX_FILAS}.")
    return resultado


def _leer_xlsx(archivo):
    from openpyxl import load_workbook

    try:
        libro = load_workbook(archivo, read_only=True, data_only=True)
    except Exception:
        raise ErrorArchivo("No se pudo leer el archivo de Excel. Verifique que sea un .xlsx válido.")
    hoja = libro.worksheets[0]
    filas = [list(f) for f in hoja.iter_rows(values_only=True)]
    libro.close()
    return filas


def _leer_csv(archivo):
    contenido = archivo.read()
    for codificacion in ("utf-8-sig", "latin-1"):
        try:
            texto = contenido.decode(codificacion)
            break
        except UnicodeDecodeError:
            continue
    primera = texto.splitlines()[0] if texto else ""
    separador = ";" if primera.count(";") > primera.count(",") else ","
    return [fila for fila in csv.reader(io.StringIO(texto), delimiter=separador)]


def _fecha(texto):
    for formato in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%d/%m/%y"):
        try:
            return datetime.datetime.strptime(texto, formato).date().isoformat()
        except ValueError:
            continue
    return texto  # el formulario mostrará el error


def _si(texto):
    return normalizar(texto) in {"si", "s", "x", "1", "true", "verdadero", "autorizado", "autoriza"}


def _errores(form):
    mensajes = []
    for campo, errores in form.errors.items():
        etiqueta = form.fields[campo].label if campo in form.fields else ""
        for e in errores:
            mensajes.append(f"{etiqueta}: {e}" if etiqueta else e)
    return mensajes


# ----------------------------------------------------------------- Validación por tipo


def _form_casa(datos):
    """Construye el formulario de Casa de Vida o devuelve (None, mensajes de error)."""
    area = Area.objects.filter(nombre__iexact=datos.get("area", ""), estado=ACTIVO).first()
    if area is None:
        return None, [f"Área: no existe un Área activa llamada «{datos.get('area', '')}». Créela primero."]
    lider = None
    if datos.get("lider_correo"):
        lider = Usuario.objects.filter(correo__iexact=datos["lider_correo"], rol__nombre=ROLES_LIDER, activo=True).first()
        if lider is None:
            return None, [f"Líder: no hay un Líder de Casa de Vida activo con el correo «{datos['lider_correo']}»."]
    form = CasaVidaForm({
        "nombre": datos.get("nombre", ""),
        "id_area": area.pk,
        "id_lider": lider.pk if lider else "",
        "direccion": datos.get("direccion", ""),
    })
    return form, []


def _form_participante(datos):
    casa = CasaVida.objects.filter(nombre__iexact=datos.get("casa_vida", ""), estado=ACTIVO).first()
    if casa is None:
        return None, [f"Casa de Vida: no existe una Casa de Vida activa llamada «{datos.get('casa_vida', '')}»."]
    form = ParticipanteForm({
        "nombres_apellidos": datos.get("nombres_apellidos", ""),
        "documento_identidad": datos.get("documento_identidad", ""),
        "fecha_nacimiento": _fecha(datos.get("fecha_nacimiento", "")),
        "telefono": datos.get("telefono", ""),
        "direccion": datos.get("direccion", ""),
        "autorizacion_datos": "on" if _si(datos.get("autorizacion_datos", "")) else "",
        "casa_vida": casa.pk,
    })
    # RN25: sin autorización se importa con autorización pendiente, no se rechaza.
    form.fields["autorizacion_datos"].required = False
    return form, []


def _ya_existe(tipo, datos):
    if tipo == "casas":
        return CasaVida.objects.filter(nombre__iexact=" ".join(datos.get("nombre", "").split())).exists()
    return Participante.objects.filter(documento_identidad__iexact=datos.get("documento_identidad", "").strip()).exists()


def _clave(tipo, datos):
    campo = "nombre" if tipo == "casas" else "documento_identidad"
    return normalizar(datos.get(campo, ""))


def validar(tipo, filas):
    """Clasifica cada fila como válida, omitida (ya existe) o con error, sin guardar nada."""
    resultados, vistos = [], {}
    for fila in filas:
        datos = fila["datos"]
        clave = _clave(tipo, datos)
        if clave and clave in vistos:
            resultados.append({**fila, "estado": ERROR, "mensajes": [f"Repetida en el archivo (igual a la fila {vistos[clave]})."]})
            continue
        if clave:
            vistos[clave] = fila["fila"]
        if clave and _ya_existe(tipo, datos):
            resultados.append({**fila, "estado": OMITIDA, "mensajes": ["Ya está registrada en el sistema; no se duplica."]})
            continue
        form, mensajes = (_form_casa if tipo == "casas" else _form_participante)(datos)
        if form is not None and not form.is_valid():
            mensajes = _errores(form)
        estado = ERROR if mensajes else VALIDA
        aviso = []
        if estado == VALIDA and tipo == "participantes" and not _si(datos.get("autorizacion_datos", "")):
            aviso = ["Se importará con autorización de datos pendiente (RN25)."]
        resultados.append({**fila, "estado": estado, "mensajes": mensajes or aviso})
    return resultados


def importar(tipo, filas, request):
    """Vuelve a validar y guarda las filas válidas en una sola transacción."""
    resultados = validar(tipo, filas)
    with transaction.atomic():
        for r in resultados:
            if r["estado"] != VALIDA:
                continue
            form, _ = (_form_casa if tipo == "casas" else _form_participante)(r["datos"])
            form.is_valid()
            if tipo == "casas":
                obj = form.save()
            else:
                obj = form.save()
                asignar_casa(obj, form.cleaned_data["casa_vida"])
            # RF26: queda registrado quién importó y cuándo (RNF18).
            registrar_auditoria(request, "IMPORTAR", obj)
            r["importada"] = True
    return resultados


def contar(resultados):
    return {
        "validas": sum(1 for r in resultados if r["estado"] == VALIDA),
        "omitidas": sum(1 for r in resultados if r["estado"] == OMITIDA),
        "errores": sum(1 for r in resultados if r["estado"] == ERROR),
        "pendientes": sum(
            1 for r in resultados if r["estado"] == VALIDA and any("pendiente" in m for m in r["mensajes"])
        ),
    }


# ----------------------------------------------------------------- Archivos descargables


def plantilla_xlsx(tipo):
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill

    libro = Workbook()
    hoja = libro.active
    hoja.title = TITULOS[tipo]
    hoja.append([titulo for _, titulo, _, _ in COLUMNAS[tipo]])
    hoja.append(EJEMPLOS[tipo])
    for celda, (_, _, obligatoria, _) in zip(hoja[1], COLUMNAS[tipo]):
        celda.font = Font(bold=True, color="FFFFFF")
        celda.fill = PatternFill("solid", fgColor="00674F" if obligatoria else "8A8A8A")
        hoja.column_dimensions[celda.column_letter].width = max(18, len(celda.value) + 4)

    ayuda = libro.create_sheet("Instrucciones")
    ayuda.append(["Columna", "Obligatoria", "Notas"])
    notas = {
        "area": "Debe existir en el sistema con ese nombre.",
        "lider_correo": "Correo de un usuario con rol Líder de Casa de Vida.",
        "fecha_nacimiento": "Formato dd/mm/aaaa o aaaa-mm-dd.",
        "telefono": "Solo números, de 7 a 15 dígitos.",
        "casa_vida": "Debe existir en el sistema con ese nombre. Importe primero las Casas de Vida.",
        "autorizacion_datos": "«Sí» si autorizó el tratamiento de datos. Vacío o «No»: autorización pendiente (RN25).",
        "documento_identidad": "Si ya existe en el sistema, la fila se omite (no se duplica).",
        "nombre": "Si ya existe una Casa de Vida con ese nombre, la fila se omite.",
    }
    for clave, titulo, obligatoria, _ in COLUMNAS[tipo]:
        ayuda.append([titulo, "Sí" if obligatoria else "No", notas.get(clave, "")])
    ayuda.append([])
    ayuda.append(["Borre la fila de ejemplo de la primera hoja antes de importar."])
    for letra, ancho in (("A", 28), ("B", 12), ("C", 80)):
        ayuda.column_dimensions[letra].width = ancho

    salida = io.BytesIO()
    libro.save(salida)
    return salida.getvalue()


def detalle_csv(tipo, resultados):
    """Detalle de filas omitidas y con error para corregirlas (salida de RF26)."""
    salida = io.StringIO()
    escritor = csv.writer(salida, delimiter=";")
    columnas = COLUMNAS[tipo]
    escritor.writerow(["Fila", "Estado", "Detalle", *[titulo for _, titulo, _, _ in columnas]])
    etiquetas = {VALIDA: "Válida", OMITIDA: "Omitida", ERROR: "Error"}
    for r in resultados:
        if r["estado"] == VALIDA:
            continue
        escritor.writerow([
            r["fila"], etiquetas[r["estado"]], " | ".join(r["mensajes"]),
            *[r["datos"].get(clave, "") for clave, _, _, _ in columnas],
        ])
    return ("﻿" + salida.getvalue()).encode("utf-8")
