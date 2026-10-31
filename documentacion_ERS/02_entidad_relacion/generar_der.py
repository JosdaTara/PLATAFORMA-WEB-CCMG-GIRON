"""Genera los diagramas entidad-relación (Graphviz DOT) de la plataforma PVA – CCMG Girón.

Fuente única del modelo: las tablas ENTIDADES y RELACIONES de este archivo, transcritas de
DOCUMENTACION/03_diseno/base_datos/esquema.sql y cambios/*.sql. No modifica la base de datos.

Uso:  python generar_der.py          -> escribe der-00 ... der-04 (.dot) en esta carpeta
Luego: dot -Tsvg der-00-general.dot -o der-00-general.svg   (renderizar.sh lo hace para todos)

Notación (pata de gallo, Information Engineering):
    ||  exactamente uno      |o  cero o uno      o{  cero o muchos
Atributo en negrita = NOT NULL. PK = clave primaria, FK = clave foránea, UK = única.
"""
from pathlib import Path

AQUI = Path(__file__).parent

# Módulo -> (título del grupo, color de cabecera). El color codifica el módulo.
MODULOS = {
    "seg": ("Seguridad y auditoría", "#D6E4F0"),
    "est": ("PVA – Estructura", "#D5EDD6"),
    "ope": ("PVA – Operación", "#FCE8C8"),
    "for": ("Escuelas de Formación", "#E8DDF2"),
}

# Entidad -> (módulo, atributos, restricciones). Atributo: (clave, nombre, tipo, not_null)
ENTIDADES = {
    "ROL": ("seg", [
        ("PK", "id_rol", "serial", True),
        ("UK", "nombre", "varchar(50)", True),
        ("", "descripcion", "text", False),
        ("", "acceso_casas_vida", "boolean", False),
        ("", "acceso_escuelas_formacion", "boolean", False),
        ("", "creado_en", "timestamptz", False),
    ], ["nombre: PASTOR, SUPERVISOR_AREA, LIDER_CASA_VIDA,", "APOYO_CASA_VIDA, COORDINADOR_FORMACION, SUPERADMIN"]),
    "USUARIO": ("seg", [
        ("PK", "id_usuario", "serial", True),
        ("FK", "id_rol", "int", True),
        ("", "nombre_completo", "varchar(150)", True),
        ("UK", "correo", "varchar(150)", True),
        ("UK", "username", "varchar(50)", False),
        ("", "password_hash", "varchar(255)", True),
        ("", "activo", "boolean", False),
        ("", "intentos_fallidos", "int", False),
        ("", "bloqueado_hasta", "timestamptz", False),
        ("", "ultimo_acceso", "timestamptz", False),
        ("", "debe_cambiar_password", "boolean", True),
        ("", "responsable_ofrendas", "boolean", True),
        ("FK", "creado_por", "int", False),
        ("FK", "modificado_por", "int", False),
        ("", "creado_en", "timestamptz", False),
        ("", "actualizado_en", "timestamptz", False),
    ], ["UK lower(correo)"]),
    "AUDITORIA": ("seg", [
        ("PK", "id_auditoria", "serial", True),
        ("FK", "id_usuario", "int", False),
        ("", "accion", "varchar(100)", True),
        ("", "entidad", "varchar(50)", True),
        ("", "id_entidad", "int", False),
        ("", "ip", "varchar(45)", False),
        ("", "fecha", "timestamptz", False),
    ], []),
    "AREA": ("est", [
        ("PK", "id_area", "serial", True),
        ("", "nombre", "varchar(100)", True),
        ("FK UK", "id_supervisor", "int", False),
        ("", "estado", "estado_general", False),
        ("", "creado_en", "timestamptz", False),
    ], ["un supervisor dirige como máximo un Área"]),
    "CASA_VIDA": ("est", [
        ("PK", "id_casa_vida", "serial", True),
        ("", "nombre", "varchar(100)", True),
        ("FK", "id_area", "int", False),
        ("FK", "id_lider", "int", False),
        ("FK", "id_supervisor", "int", False),
        ("", "direccion", "text", False),
        ("", "estado", "estado_general", False),
        ("", "creado_en", "timestamptz", False),
        ("", "actualizado_en", "timestamptz", False),
    ], ["id_supervisor: copia redundante de AREA.id_supervisor"]),
    "CASA_VIDA_EQUIPO": ("est", [
        ("PK", "id_casa_vida_equipo", "serial", True),
        ("FK", "id_casa_vida", "int", True),
        ("FK", "id_usuario", "int", True),
        ("", "funcion", "varchar(20)", True),
        ("", "activo", "boolean", True),
        ("", "creado_en", "timestamptz", False),
    ], ["funcion: APRENDIZ, ANFITRION, MAESTRO_NINOS", "UK (id_casa_vida, id_usuario)", "UK (id_usuario) si activo"]),
    "PARTICIPANTE": ("est", [
        ("PK", "id_participante", "serial", True),
        ("", "nombres_apellidos", "varchar(150)", True),
        ("UK", "documento_identidad", "varchar(50)", True),
        ("", "fecha_nacimiento", "date", False),
        ("", "telefono", "varchar(20)", False),
        ("", "direccion", "text", False),
        ("", "autorizacion_datos", "boolean", False),
        ("", "estado", "estado_general", False),
        ("", "creado_en", "timestamptz", False),
        ("", "actualizado_en", "timestamptz", False),
    ], []),
    "CASA_VIDA_MIEMBRO": ("est", [
        ("PK", "id_casa_vida_miembro", "serial", True),
        ("FK", "id_casa_vida", "int", True),
        ("FK", "id_participante", "int", True),
        ("", "fecha_ingreso", "date", False),
        ("", "estado", "estado_general", False),
    ], ["UK (id_casa_vida, id_participante)"]),
    "OFRENDA": ("est", [
        ("PK", "id_ofrenda", "serial", True),
        ("", "fecha", "date", True),
        ("", "concepto", "varchar(150)", True),
        ("", "valor", "numeric(12,2)", True),
        ("FK", "id_casa_vida", "int", False),
        ("FK", "id_usuario_registro", "int", False),
        ("FK", "modificado_por", "int", False),
        ("", "observacion", "text", False),
        ("", "creado_en", "timestamptz", False),
        ("", "actualizado_en", "timestamptz", False),
    ], ["CHECK valor &gt; 0"]),
    "ACTIVIDAD": ("ope", [
        ("PK", "id_actividad", "serial", True),
        ("", "tipo_modulo", "tipo_modulo", True),
        ("FK", "id_casa_vida", "int", False),
        ("FK", "id_proceso_formacion", "int", False),
        ("", "titulo", "varchar(150)", True),
        ("", "fecha", "date", True),
        ("", "hora", "time", False),
        ("", "descripcion", "text", False),
        ("FK", "id_responsable", "int", False),
        ("", "creado_en", "timestamptz", False),
    ], ["CHECK arco exclusivo: casa XOR proceso"]),
    "ASISTENCIA": ("ope", [
        ("PK", "id_asistencia", "serial", True),
        ("FK", "id_actividad", "int", True),
        ("FK", "id_participante", "int", True),
        ("", "presente", "boolean", False),
        ("", "observacion", "varchar(255)", False),
        ("FK", "registrado_por", "int", False),
        ("", "fecha_registro", "timestamptz", False),
    ], ["UK (id_actividad, id_participante)"]),
    "SEGUIMIENTO": ("ope", [
        ("PK", "id_seguimiento", "serial", True),
        ("FK", "id_participante", "int", True),
        ("FK", "id_usuario", "int", True),
        ("", "tipo_modulo", "tipo_modulo", True),
        ("FK", "id_proceso_formacion", "int", False),
        ("", "fecha", "date", True),
        ("", "tipo", "varchar(20)", True),
        ("", "estado", "varchar(15)", True),
        ("", "observacion", "text", True),
        ("", "creado_en", "timestamptz", False),
        ("", "actualizado_en", "timestamptz", False),
    ], ["tipo: VISITA, LLAMADA, CONSEJERIA, OTRO", "estado: ABIERTO, EN_PROCESO, CERRADO",
        "CHECK proceso obligatorio si es de formación"]),
    "REPORTE": ("ope", [
        ("PK", "id_reporte", "serial", True),
        ("", "tipo_reporte", "varchar(20)", True),
        ("", "tipo_modulo", "tipo_modulo", True),
        ("FK", "id_usuario_envia", "int", True),
        ("FK", "id_usuario_destino", "int", False),
        ("FK", "id_casa_vida", "int", False),
        ("FK", "id_area", "int", False),
        ("FK", "id_reporte_general", "int", False),
        ("", "periodo", "varchar(20)", True),
        ("", "fecha_inicio", "date", False),
        ("", "fecha_fin", "date", False),
        ("", "observaciones", "text", False),
        ("", "ruta_archivo", "varchar(255)", False),
        ("", "enviado_en", "timestamptz", False),
    ], ["tipo_reporte: CASA_VIDA, GENERAL_AREA", "UK (id_casa_vida, periodo) si CASA_VIDA",
        "UK (id_area, periodo) si GENERAL_AREA", "CHECK fecha_inicio ≤ fecha_fin"]),
    "PROCESO_FORMACION": ("for", [
        ("PK", "id_proceso_formacion", "serial", True),
        ("", "nombre", "varchar(150)", True),
        ("", "tipo_proceso", "tipo_proceso", True),
        ("FK", "id_coordinador", "int", True),
        ("", "descripcion", "text", False),
        ("", "estado", "estado_general", False),
        ("", "creado_en", "timestamptz", False),
        ("", "actualizado_en", "timestamptz", False),
    ], ["tipo_proceso: PASOS_VIDA, ESCUELAS_VIDA,", "MODULOS_LIDERAZGO, MISIONES"]),
    "INSCRIPCION_FORMACION": ("for", [
        ("PK", "id_inscripcion", "serial", True),
        ("FK", "id_participante", "int", True),
        ("FK", "id_proceso_formacion", "int", True),
        ("", "fecha_inscripcion", "date", False),
        ("", "estado", "estado_general", False),
    ], ["UK (id_participante, id_proceso_formacion)"]),
}

# (padre, col_padre, hijo, col_hijo, card_padre, card_hijo, etiqueta, de_negocio)
# card: "1" exactamente uno, "01" cero o uno, "0N" cero o muchos.
# de_negocio=False: FK de trazabilidad o redundante (solo en vistas detalladas).
RELACIONES = [
    ("ROL", "id_rol", "USUARIO", "id_rol", "1", "0N", "asigna", True),
    ("USUARIO", "id_usuario", "USUARIO", "creado_por", "01", "0N", "crea", False),
    ("USUARIO", "id_usuario", "USUARIO", "modificado_por", "01", "0N", "modifica", False),
    ("USUARIO", "id_usuario", "AUDITORIA", "id_usuario", "01", "0N", "realiza", True),
    ("USUARIO", "id_usuario", "AREA", "id_supervisor", "01", "01", "supervisa", True),
    ("AREA", "id_area", "CASA_VIDA", "id_area", "01", "0N", "agrupa", True),
    ("USUARIO", "id_usuario", "CASA_VIDA", "id_lider", "01", "0N", "lidera", True),
    ("USUARIO", "id_usuario", "CASA_VIDA", "id_supervisor", "01", "0N", "copia redundante", False),
    ("CASA_VIDA", "id_casa_vida", "CASA_VIDA_EQUIPO", "id_casa_vida", "1", "0N", "tiene", True),
    ("USUARIO", "id_usuario", "CASA_VIDA_EQUIPO", "id_usuario", "1", "0N", "apoya en", True),
    ("CASA_VIDA", "id_casa_vida", "CASA_VIDA_MIEMBRO", "id_casa_vida", "1", "0N", "integra", True),
    ("PARTICIPANTE", "id_participante", "CASA_VIDA_MIEMBRO", "id_participante", "1", "0N", "pertenece", True),
    ("CASA_VIDA", "id_casa_vida", "OFRENDA", "id_casa_vida", "01", "0N", "recibe", True),
    ("USUARIO", "id_usuario", "OFRENDA", "id_usuario_registro", "01", "0N", "registra", True),
    ("USUARIO", "id_usuario", "OFRENDA", "modificado_por", "01", "0N", "modifica", False),
    ("CASA_VIDA", "id_casa_vida", "ACTIVIDAD", "id_casa_vida", "01", "0N", "realiza", True),
    ("PROCESO_FORMACION", "id_proceso_formacion", "ACTIVIDAD", "id_proceso_formacion", "01", "0N", "realiza", True),
    ("USUARIO", "id_usuario", "ACTIVIDAD", "id_responsable", "01", "0N", "responsable", False),
    ("ACTIVIDAD", "id_actividad", "ASISTENCIA", "id_actividad", "1", "0N", "registra", True),
    ("PARTICIPANTE", "id_participante", "ASISTENCIA", "id_participante", "1", "0N", "asiste", True),
    ("USUARIO", "id_usuario", "ASISTENCIA", "registrado_por", "01", "0N", "registrado por", False),
    ("PARTICIPANTE", "id_participante", "SEGUIMIENTO", "id_participante", "1", "0N", "recibe", True),
    ("USUARIO", "id_usuario", "SEGUIMIENTO", "id_usuario", "1", "0N", "registra", True),
    ("PROCESO_FORMACION", "id_proceso_formacion", "SEGUIMIENTO", "id_proceso_formacion", "01", "0N", "contexto", True),
    ("USUARIO", "id_usuario", "REPORTE", "id_usuario_envia", "1", "0N", "envía", True),
    ("USUARIO", "id_usuario", "REPORTE", "id_usuario_destino", "01", "0N", "recibe", False),
    ("CASA_VIDA", "id_casa_vida", "REPORTE", "id_casa_vida", "01", "0N", "reporte de casa", True),
    ("AREA", "id_area", "REPORTE", "id_area", "01", "0N", "reporte general", True),
    ("REPORTE", "id_reporte", "REPORTE", "id_reporte_general", "01", "0N", "agrupa", True),
    ("USUARIO", "id_usuario", "PROCESO_FORMACION", "id_coordinador", "1", "0N", "coordina", True),
    ("PROCESO_FORMACION", "id_proceso_formacion", "INSCRIPCION_FORMACION", "id_proceso_formacion", "1", "0N", "inscribe", True),
    ("PARTICIPANTE", "id_participante", "INSCRIPCION_FORMACION", "id_participante", "1", "0N", "se inscribe", True),
]

# Lado de la tabla por el que se dibuja cada autorrelación (evita cruzar entidades vecinas).
LADO_LAZO = {}

# Relaciones que se dibujan con el hijo a la izquierda del padre (solo distribución en vistas con puertos).
INVERTIR = {("USUARIO", "AUDITORIA")}

# Tamaño de letra base de la vista que se está generando (lo fija vista()).
FUENTE = 11

# Flechas de Graphviz: la primera forma es la que toca la entidad.
FLECHA = {"1": "teetee", "01": "teeodot", "0N": "crowodot"}


def tabla(nombre, modo, columnas_extra=()):
    """modo: 'claves' (solo PK/FK/UK de negocio), 'completo' o 'referencia' (PK y las FK que pide la vista)."""
    modulo, atributos, restricciones = ENTIDADES[nombre]
    color = MODULOS[modulo][1]
    if modo == "referencia":
        color = "#EEEEEE"
        atributos = [a for a in atributos if a[0] == "PK" or a[1] in columnas_extra]
        restricciones = []
    elif modo == "claves":
        fk_negocio = {r[3] for r in RELACIONES if r[2] == nombre and r[7]}
        atributos = [a for a in atributos if a[0] in ("PK", "UK", "FK UK") or (a[0] == "FK" and a[1] in fk_negocio)]
        restricciones = []
    filas = []
    for clave, col, tipo, obligatorio in atributos:
        texto = f"<B>{col}</B>" if obligatorio else col
        # La vista de claves omite el tipo de dato para ganar legibilidad; el tipo está en las vistas detalladas.
        celda_tipo = (
            f'<TD ALIGN="LEFT" PORT="{col}_e"><FONT COLOR="#666666" POINT-SIZE="{FUENTE - 1}">{tipo}</FONT></TD>'
            if modo != "claves" else f'<TD PORT="{col}_e"></TD>'
        )
        filas.append(
            f'<TR><TD ALIGN="LEFT" PORT="{col}_w"><FONT COLOR="#555555" POINT-SIZE="{FUENTE - 2}">{clave or "&#160;"}</FONT></TD>'
            f'<TD ALIGN="LEFT">{texto}</TD>{celda_tipo}</TR>'
        )
    if modo == "referencia":
        filas.append(f'<TR><TD COLSPAN="3"><FONT COLOR="#777777" POINT-SIZE="{FUENTE - 2}"><I>detalle en otra vista</I></FONT></TD></TR>')
    for r in restricciones:
        filas.append(f'<TR><TD COLSPAN="3" ALIGN="LEFT"><FONT COLOR="#666666" POINT-SIZE="{FUENTE - 2}"><I>{r}</I></FONT></TD></TR>')
    estilo = ' STYLE="dashed"' if modo == "referencia" else ""
    return (
        f'  {nombre} [label=<<TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0" CELLPADDING="4" COLOR="#555555"{estilo}>'
        f'<TR><TD COLSPAN="3" BGCOLOR="{color}"><B>{nombre}</B></TD></TR>'
        + "".join(filas)
        + "</TABLE>>];"
    )


def arista(r, puertos):
    padre, cp, hijo, ch, card_p, card_h, etiqueta, negocio = r
    # Con puertos, la relación sale por el lado este de la PK y entra por el oeste de la FK.
    # En una autorrelación ambos extremos usan el mismo lado (LADO_LAZO) para que el lazo quede fuera de la tabla.
    estilo = "" if negocio else ', style="dashed", color="#888888", fontcolor="#777777"'
    if puertos and padre == hijo:
        lado = LADO_LAZO.get(padre, "e")
        origen, destino = f"{padre}:{cp}_{lado}:{lado}", f"{hijo}:{ch}_{lado}:{lado}"
    elif (padre, hijo) in INVERTIR:
        # Solo cambia la distribución (el hijo queda a la izquierda); los símbolos siguen en su entidad.
        origen = f"{hijo}:{ch}_e:e" if puertos else hijo
        destino = f"{padre}:{cp}_w:w" if puertos else padre
        return (
            f'  {origen} -> {destino} [dir=both, arrowtail="{FLECHA[card_h]}", arrowhead="{FLECHA[card_p]}", '
            f'xlabel="{etiqueta}"{estilo}];'
        )
    else:
        origen = f"{padre}:{cp}_e:e" if puertos else padre
        destino = f"{hijo}:{ch}_w:w" if puertos else hijo
    return (
        f'  {origen} -> {destino} [dir=both, arrowtail="{FLECHA[card_p]}", arrowhead="{FLECHA[card_h]}", '
        f'xlabel="{etiqueta}"{estilo}];'
    )


def grafo(titulo, rankdir, cuerpo, ranksep=0.9, nodesep=0.5):
    return "\n".join([
        "digraph DER {",
        f'  graph [label=<<B>{titulo}</B>>, labelloc="t", fontsize=16, fontname="Arial", rankdir={rankdir},',
        f'         nodesep={nodesep}, ranksep={ranksep}, splines=spline, pad=0.3, bgcolor="white", forcelabels=true];',
        f'  node [shape=plain, fontname="Arial", fontsize={FUENTE}];',
        f'  edge [fontname="Arial", fontsize={FUENTE - 2}, color="#555555", arrowsize=0.9, penwidth=1.1];',
        *cuerpo,
        "}",
        "",
    ])


def vista(archivo, titulo, completas, referencias=(), solo_negocio=False, agrupar=False, rankdir="LR", puertos=True, ranksep=0.9, nodesep=0.5, fuente=11):
    global FUENTE
    FUENTE = fuente
    cuerpo = []
    modo = "claves" if solo_negocio else "completo"
    visibles = set(completas) | set(referencias)
    if agrupar:
        for clave_mod, (nombre_mod, color) in MODULOS.items():
            miembros = [e for e in completas if ENTIDADES[e][0] == clave_mod]
            if not miembros:
                continue
            cuerpo.append(f'  subgraph cluster_{clave_mod} {{')
            cuerpo.append(f'    label=<<B>{nombre_mod}</B>>; fontsize={FUENTE + 1}; style="rounded"; color="#BBBBBB"; bgcolor="#FCFCFC";')
            cuerpo += ["  " + tabla(e, modo) for e in miembros]
            cuerpo.append("  }")
    else:
        cuerpo += [tabla(e, modo) for e in completas]
    aristas = [
        r for r in RELACIONES
        if r[0] in visibles and r[2] in visibles and (r[0] in completas or r[2] in completas)
        and not (solo_negocio and not r[7])
    ]
    # Una entidad de referencia muestra su PK y las FK que usan las relaciones de esta vista.
    for e in referencias:
        extra = {r[3] for r in aristas if r[2] == e}
        cuerpo.append(tabla(e, "referencia", extra))
    cuerpo += [arista(r, puertos) for r in aristas]
    (AQUI / archivo).write_text(grafo(titulo, rankdir, cuerpo, ranksep, nodesep), encoding="utf-8")
    print("escrito", archivo)


if __name__ == "__main__":
    vista("der-00-general.dot", "DER-00 · Modelo general: entidades, claves y relaciones de negocio",
          list(ENTIDADES), solo_negocio=True, agrupar=True, rankdir="TB", puertos=False,
          ranksep=0.45, nodesep=0.25, fuente=16)
    vista("der-01-seguridad-auditoria.dot", "DER-01 · Seguridad, usuarios y auditoría",
          ["ROL", "USUARIO", "AUDITORIA"])
    vista("der-02-casas-vida-estructura.dot", "DER-02 · PVA: Áreas, Casas de Vida, participantes y ofrendas",
          ["AREA", "CASA_VIDA", "CASA_VIDA_EQUIPO", "CASA_VIDA_MIEMBRO", "PARTICIPANTE", "OFRENDA"],
          referencias=["USUARIO"])
    vista("der-03-casas-vida-operacion.dot", "DER-03 · PVA: actividades, asistencia, seguimiento y reportes",
          ["ACTIVIDAD", "ASISTENCIA", "SEGUIMIENTO", "REPORTE"],
          referencias=["USUARIO", "AREA", "CASA_VIDA", "PARTICIPANTE", "PROCESO_FORMACION"])
    vista("der-04-escuelas-formacion.dot", "DER-04 · Escuelas de Formación",
          ["PROCESO_FORMACION", "INSCRIPCION_FORMACION"],
          referencias=["USUARIO", "PARTICIPANTE", "ACTIVIDAD", "SEGUIMIENTO"])
