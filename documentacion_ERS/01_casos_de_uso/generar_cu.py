"""Genera los diagramas de casos de uso de la plataforma PVA – CCMG Girón con distribución fija.

Cada elemento tiene una posición asignada (en pulgadas, origen arriba a la izquierda), de modo que:
  - todos los actores humanos quedan en una sola columna a la izquierda;
  - los casos de uso se ordenan en filas dentro de su módulo (paquete);
  - los servicios de seguridad y los sistemas externos quedan a la derecha;
  - las líneas son rectas y no dependen del motor automático de distribución.

Uso:  python generar_cu.py      -> escribe los .dot de cada diagrama en esta carpeta
Luego Graphviz los dibuja con:  neato -n2 -Tpng archivo.dot   (renderizar.sh lo hace para todos)

Notación UML: asociación = línea continua sin flecha; «include» y «extend» = línea punteada con
flecha abierta hacia el caso de uso incluido (include) o hacia el caso base (extend).
"""
import base64
import re
from pathlib import Path

AQUI = Path(__file__).parent
PT = 72  # puntos por pulgada

COLOR = {
    "cu": ("#EAF4FB", "#2C3E50"),
    "seg": ("#FDECEC", "#8E2C2C"),
}


class Diagrama:
    def __init__(self, nombre, titulo, ancho, alto):
        self.nombre, self.titulo, self.ancho, self.alto = nombre, titulo, ancho, alto
        self.nodos, self.aristas = [], []
        self.xy = {}  # posición de cada actor y caso de uso, para anclar las líneas

    # --- utilidades de coordenadas (y crece hacia abajo en la especificación)
    def _pos(self, x, y):
        return f'"{x * PT:.1f},{(self.alto - y) * PT:.1f}!"'

    def marco(self, ident, texto, x0, y0, x1, y1, tipo="paquete"):
        """Límite del sistema (tipo='sistema') o paquete de un módulo (tipo='paquete')."""
        ancho, alto = x1 - x0, y1 - y0
        forma = "box" if tipo == "sistema" else "tab"
        borde = "#2C3E50" if tipo == "sistema" else "#8A9BA8"
        fondo = "#FFFFFF" if tipo == "sistema" else "#FAFBFC"
        grosor = 1.6 if tipo == "sistema" else 1.0
        tam = 14 if tipo == "sistema" else 12
        self.nodos.append(
            f'  {ident} [shape={forma}, label=<<B>{texto}</B>>, labelloc=t, labeljust=l, fontsize={tam}, '
            f'fontcolor="#2C3E50", style=filled, fillcolor="{fondo}", color="{borde}", penwidth={grosor}, '
            f'fixedsize=true, width={ancho:.2f}, height={alto:.2f}, pos={self._pos(x0 + ancho / 2, y0 + alto / 2)}];'
        )

    def actor(self, ident, texto, x, y, sistema=False, abstracto=False):
        img = "actor_sistema.png" if sistema else "actor.png"
        estereotipo = '<TR><TD><FONT POINT-SIZE="10" COLOR="#7A4E00">«sistema»</FONT></TD></TR>' if sistema else ""
        lineas = "<BR/>".join(texto.split("\n"))
        self.xy[ident] = (x, y)
        if abstracto:  # UML: el nombre de un actor abstracto va en cursiva
            lineas = f"<I>{lineas}</I>"
        self.nodos.append(
            f'  {ident} [shape=plain, label=<<TABLE BORDER="0" CELLSPACING="0" CELLPADDING="1">{estereotipo}'
            f'<TR><TD FIXEDSIZE="TRUE" WIDTH="26" HEIGHT="44"><IMG SRC="{img}" SCALE="TRUE"/></TD></TR>'
            f'<TR><TD><FONT POINT-SIZE="12">{lineas}</FONT></TD></TR></TABLE>>, pos={self._pos(x, y)}];'
        )

    def cu(self, ident, texto, x, y, tipo="cu", ancho=None):
        fondo, borde = COLOR[tipo]
        self.xy[ident] = (x, y)
        lineas = texto.split("\n")
        if ancho is None:
            ancho = max(1.9, 0.083 * max(len(l) for l in lineas) + 0.55)
        alto = 0.46 + 0.17 * (len(lineas) - 1)
        estereotipo = '<FONT POINT-SIZE="9" COLOR="#8E2C2C">«seguridad»</FONT><BR/>' if tipo == "seg" else ""
        if estereotipo:
            alto += 0.14
        self.nodos.append(
            f'  {ident} [shape=ellipse, label=<{estereotipo}{"<BR/>".join(lineas)}>, fontsize=12, style=filled, '
            f'fillcolor="{fondo}", color="{borde}", fixedsize=true, width={ancho:.2f}, height={alto:.2f}, '
            f'pos={self._pos(x, y)}];'
        )

    def tarjeta(self, ident, x, y, ancho, alto, titulo, codigo, lineas, cabecera):
        """Ficha de un nivel de la jerarquía: título con el rol del sistema y su descripción."""
        cuerpo = "<BR/>".join(lineas)
        self.nodos.append(
            f'  {ident} [shape=plain, label=<<TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0" CELLPADDING="6" '
            f'COLOR="#2C3E50" BGCOLOR="white" FIXEDSIZE="TRUE" WIDTH="{ancho * PT:.0f}" HEIGHT="{alto * PT:.0f}">'
            f'<TR><TD BGCOLOR="{cabecera}" ALIGN="LEFT" WIDTH="{ancho * PT - 4:.0f}"><FONT POINT-SIZE="13"><B>{titulo}</B></FONT>'
            f'<FONT POINT-SIZE="10" COLOR="#4A5A68">   rol: {codigo}</FONT></TD></TR>'
            f'<TR><TD ALIGN="LEFT" BALIGN="LEFT" VALIGN="TOP"><FONT POINT-SIZE="11">{cuerpo}</FONT></TD></TR>'
            f'</TABLE>>, pos={self._pos(x, y)}];'
        )
        self.xy[ident] = (x, y)

    def nivel(self, ident, texto, x, y, color):
        self.nodos.append(
            f'  {ident} [shape=box, style="rounded,filled", fillcolor="{color}", color="#2C3E50", fontcolor="white", '
            f'label=<<B>{texto}</B>>, fontsize=13, fixedsize=true, width=1.15, height=0.45, pos={self._pos(x, y)}];'
        )
        self.xy[ident] = (x, y)

    def texto(self, ident, texto, x, y, tam=11, color="#4A5A68"):
        self.nodos.append(
            f'  {ident} [shape=plaintext, label=<<I>{texto}</I>>, fontsize={tam}, fontcolor="{color}", '
            f'pos={self._pos(x, y)}];'
        )

    def flecha(self, a, b):
        """Flecha simple de un nivel al siguiente (orden jerárquico)."""
        o, d = self._extremos(a, b)
        self.aristas.append(f'  {o} -> {d} [arrowhead=normal, arrowsize=0.9, color="#2C3E50", penwidth=1.6];')

    def nota(self, ident, texto, x, y, ancho, alto):
        self.nodos.append(
            f'  {ident} [shape=note, label="{texto}", fontsize=10, style=filled, fillcolor="#FFFDE7", '
            f'color="#B0A060", fixedsize=true, width={ancho:.2f}, height={alto:.2f}, pos={self._pos(x, y)}];'
        )

    def _extremos(self, a, b):
        """Ancla cada línea a los costados de los nodos (este/oeste, o norte/sur si están en la misma
        columna), para que recorra el pasillo entre columnas y no atraviese otros óvalos."""
        (xa, ya), (xb, yb) = self.xy[a], self.xy[b]
        if xb > xa + 0.5:
            return f"{a}:e", f"{b}:w"
        if xb < xa - 0.5:
            return f"{a}:w", f"{b}:e"
        return (f"{a}:s", f"{b}:n") if yb > ya else (f"{a}:n", f"{b}:s")

    def asocia(self, a, b):
        o, d = self._extremos(a, b)
        self.aristas.append(f'  {o} -> {d} [dir=none, color="#555555", penwidth=1.1];')

    def generaliza(self, hijo, padre):
        """Generalización entre actores: línea continua con triángulo hueco hacia el padre."""
        o, d = self._extremos(hijo, padre)
        self.aristas.append(f'  {o} -> {d} [arrowhead=empty, arrowsize=1.1, color="#555555", penwidth=1.1];')

    def _punteada(self, origen, destino, etiqueta, puerto_destino=None):
        o, d = self._extremos(origen, destino)
        if puerto_destino:  # p. ej. "ne": llega por otra esquina para no montarse sobre otras líneas
            d = f"{destino}:{puerto_destino}"
        self.aristas.append(
            f'  {o} -> {d} [style=dashed, arrowhead=vee, arrowsize=0.8, color="#555555", '
            f'label="{etiqueta}", fontsize=9, fontcolor="#444444"];'
        )

    def include(self, base, incluido, etiqueta="«include»"):
        self._punteada(base, incluido, etiqueta)

    def extend(self, extension, base, etiqueta="«extend»", puerto=None):
        self._punteada(extension, base, etiqueta, puerto)

    def escribir(self):
        texto = "\n".join([
            f"// {self.titulo}. Generado por generar_cu.py: editar ese archivo, no este.",
            "digraph CU {",
            f'  graph [label=<<B>{self.titulo}</B>>, labelloc=t, fontsize=16, fontname="Arial", '
            f'splines=line, outputorder=nodesfirst, bgcolor=white, pad=0.25, '
            f'bb="0,0,{self.ancho * PT:.0f},{self.alto * PT:.0f}"];',
            '  node [fontname="Arial"];',
            '  edge [fontname="Arial"];',
            *self.nodos,
            *self.aristas,
            "}",
            "",
        ])
        (AQUI / f"{self.nombre}.dot").write_text(texto, encoding="utf-8")
        print("escrito", f"{self.nombre}.dot")


def incrustar_imagenes(svg_path):
    """Graphviz enlaza las imágenes de los actores por ruta; las incrusta para que el SVG sea autónomo."""
    svg = Path(svg_path).read_text(encoding="utf-8")

    def a_datos(m):
        datos = base64.b64encode((AQUI / Path(m.group(2)).name).read_bytes()).decode()
        return f'{m.group(1)}"data:image/png;base64,{datos}"'

    svg = re.sub(r'((?:xlink:)?href=)"([^"]*actor(?:_sistema)?\.png)"', a_datos, svg)
    Path(svg_path).write_text(svg, encoding="utf-8")


# =====================================================================================
# Coordenadas (pulgadas). Columna 1: casos de uso asociados a actores; columna 2: casos
# incluidos o extensiones; columna 3: servicios de seguridad; a la derecha, sistemas externos.
# =====================================================================================
X_ACT = 0.8


def asociar(d, mapa):
    for actor, cus in mapa.items():
        for c in cus:
            d.asocia(actor, c)


# -------------------------------------------------------------------------------------
# CU-01 · Diagrama general
# -------------------------------------------------------------------------------------
def general():
    d = Diagrama("cu-01-general", "CU-01 · Diagrama general de casos de uso · Plataforma web PVA – CCMG Girón",
                 15.2, 17.6)
    X1, X2, X3, X_SIS = 4.1, 7.0, 10.35, 13.9

    d.marco("sistema", "Servidor web · Plataforma PVA (Django 5.2)", 2.0, 0.55, 12.4, 17.25, "sistema")
    d.marco("p_acc", "Acceso", 2.35, 1.05, 8.55, 4.35)
    d.marco("p_adm", "Administración", 2.35, 4.6, 8.55, 6.95)
    d.marco("p_pva", "Módulo PVA – Casas de Vida", 2.35, 7.2, 8.55, 12.95)
    d.marco("p_for", "Módulo Escuelas de Formación", 2.35, 13.2, 8.55, 16.95)
    d.marco("p_seg", "Servicios de seguridad", 8.85, 1.05, 12.1, 7.3)

    d.cu("pub", "Consultar información pública", X1, 1.7)
    d.cu("login", "Iniciar sesión", X1, 2.45)
    d.cu("cpass", "Cambiar contraseña", X1, 3.15)
    d.cu("logout", "Cerrar sesión", X1, 3.85)
    d.cu("rpass", "Recuperar contraseña", X2, 1.75)
    d.cu("panel", "Visualizar panel\nprincipal", X2, 3.0)

    d.cu("bita", "Consultar bitácora\nde auditoría", X1, 5.25)
    d.cu("ofr", "Gestionar ofrendas", X1, 5.95)
    d.cu("usr", "Gestionar usuarios", X1, 6.6)
    d.cu("rol", "Asignar rol", X2, 5.9)

    d.cu("casa", "Gestionar Casas de Vida", X1, 7.85)
    d.cu("part", "Gestionar participantes", X1, 8.5)
    d.cu("gen", "Generar reporte consolidado", X1, 9.15)
    d.cu("envg", "Enviar reporte general", X1, 9.85)
    d.cu("crep", "Consultar reportes", X1, 10.55)
    d.cu("ccasa", "Consultar Casas de Vida", X1, 11.2)
    d.cu("asis", "Registrar asistencia", X1, 11.85)
    d.cu("envs", "Enviar reporte semanal", X1, 12.5)
    d.cu("des", "Desactivar registro", X2, 8.15)
    d.cu("exp", "Exportar reporte", X2, 9.85)

    d.cu("proc", "Gestionar procesos\nde formación", X1, 13.85)
    d.cu("pfor", "Gestionar participantes\nde formación", X1, 14.6)
    d.cu("afor", "Registrar asistencia\nde formación", X1, 15.35)
    d.cu("rfor", "Generar reporte\nde formación", X1, 16.2)
    d.cu("ins", "Inscribir participante", X2, 14.6)

    d.cu("val", "Validar credenciales", X3, 2.45, "seg")
    d.cu("blq", "Bloquear acceso\ntemporal", X3, 3.75, "seg")
    d.cu("perm", "Verificar permisos\ndel rol", X3, 5.05, "seg")
    d.cu("bit", "Registrar en bitácora", X3, 6.6, "seg")

    d.actor("MA", "Miembro\nAsistente", X_ACT, 1.75)
    d.actor("UR", "Usuario registrado\n(cualquier rol)", X_ACT, 3.25)
    d.actor("SA", "Super\nAdministrador", X_ACT, 5.1)
    d.actor("RO", "Responsable\nde ofrendas", X_ACT, 6.4)
    d.actor("PA", "Administrador\n(Pastor)", X_ACT, 7.75)
    d.actor("SU", "Supervisor\nde Área", X_ACT, 10.0)
    d.actor("EQ", "Equipo de\nCasa de Vida", X_ACT, 12.0)
    d.actor("CO", "Coordinador de\nEscuelas de\nFormación", X_ACT, 15.0)
    d.actor("SMTP", "Servidor de\ncorreo SMTP", X_SIS, 1.9, sistema=True)
    d.actor("DB", "Servidor de base\nde datos PostgreSQL", X_SIS, 4.6, sistema=True)

    asociar(d, {
        "MA": ["pub"], "UR": ["login", "cpass", "logout"], "SA": ["bita"], "RO": ["ofr"],
        "PA": ["ofr", "usr", "casa", "part", "gen"], "SU": ["envg", "crep", "ccasa"],
        "EQ": ["crep", "ccasa", "asis", "envs"], "CO": ["proc", "pfor", "afor", "rfor"],
    })
    d.include("login", "val")
    d.include("login", "panel")
    d.include("panel", "perm")
    d.include("usr", "rol")
    d.include("usr", "bit")
    d.include("pfor", "ins")
    d.extend("rpass", "login")
    d.extend("blq", "val", "«extend»\\n5 intentos fallidos")
    d.extend("des", "casa")
    d.extend("des", "part")
    d.extend("exp", "crep")
    d.extend("exp", "gen")
    d.asocia("rpass", "SMTP")
    d.asocia("val", "DB")
    d.asocia("bit", "DB")

    d.nota("n1", "Vista general con los casos de uso\\lprincipales. El detalle de cada módulo\\l"
           "y la participación del Administrador\\len Escuelas de Formación están en\\lCU-02 a CU-05.\\l",
           13.75, 15.9, 2.6, 1.3)
    d.escribir()


# -------------------------------------------------------------------------------------
# CU-02 · Acceso y seguridad
# -------------------------------------------------------------------------------------
def acceso():
    d = Diagrama("cu-02-acceso-seguridad", "CU-02 · Acceso a la plataforma y servicios de seguridad", 13.6, 8.6)
    X1, X2, X3, X_SIS = 3.9, 6.7, 9.45, 12.45

    d.marco("sistema", "Servidor web · Plataforma PVA (Django 5.2)", 1.9, 0.55, 11.0, 8.3, "sistema")
    d.marco("p_acc", "Acceso", 2.2, 1.0, 8.05, 8.0)
    d.marco("p_seg", "Servicios de seguridad", 8.3, 1.0, 10.7, 8.0)

    d.cu("pub", "Consultar información\npública", X1, 1.75)
    d.cu("login", "Iniciar sesión", X1, 3.2)
    d.cu("cpass", "Cambiar contraseña", X1, 4.8)
    d.cu("logout", "Cerrar sesión", X1, 6.2)
    d.cu("rpass", "Recuperar contraseña", X2, 2.3)
    d.cu("panel", "Visualizar panel\nprincipal", X2, 3.9)

    d.cu("val", "Validar credenciales", X3, 3.2, "seg", ancho=2.2)
    d.cu("blq", "Bloquear acceso\ntemporal", X3, 4.35, "seg", ancho=2.2)
    d.cu("perm", "Verificar permisos\ndel rol", X3, 5.45, "seg", ancho=2.2)
    d.cu("bit", "Registrar en bitácora", X3, 6.5, "seg", ancho=2.2)
    d.cu("cif", "Cifrar contraseña", X3, 7.45, "seg", ancho=2.2)

    d.actor("MA", "Miembro\nAsistente", X_ACT, 1.75)
    d.actor("UR", "Usuario registrado\n(cualquier rol)", X_ACT, 4.8)
    d.actor("SMTP", "Servidor de\ncorreo SMTP", X_SIS, 1.5, sistema=True)
    d.actor("DB", "Servidor de base\nde datos PostgreSQL", X_SIS, 5.45, sistema=True)

    asociar(d, {"MA": ["pub"], "UR": ["login", "cpass", "logout"]})
    d.include("login", "val")
    d.include("login", "panel")
    d.include("login", "bit")
    d.include("panel", "perm")
    d.include("cpass", "cif")
    d.extend("rpass", "login", "«extend»\\nolvidó la contraseña")
    d.extend("blq", "val", "«extend»\\n5 intentos fallidos")
    d.asocia("rpass", "SMTP")
    d.asocia("val", "DB")
    d.asocia("bit", "DB")
    d.asocia("cif", "DB")
    d.escribir()


# -------------------------------------------------------------------------------------
# CU-03 · Administración, ofrendas y auditoría
# -------------------------------------------------------------------------------------
def administracion():
    d = Diagrama("cu-03-administracion", "CU-03 · Administración, ofrendas y auditoría", 13.6, 6.9)
    X1, X2, X3, X_SIS = 3.9, 6.75, 9.5, 12.45

    d.marco("sistema", "Servidor web · Plataforma PVA (Django 5.2)", 1.9, 0.55, 11.0, 6.6, "sistema")
    d.marco("p_adm", "Administración", 2.2, 1.0, 8.1, 6.3)
    d.marco("p_seg", "Servicios de seguridad", 8.35, 1.0, 10.7, 6.3)

    d.cu("bita", "Consultar bitácora\nde auditoría", X1, 1.75)
    d.cu("ofr", "Gestionar ofrendas", X1, 2.95)
    d.cu("usr", "Gestionar usuarios", X1, 4.55)
    d.cu("exp", "Exportar reporte", X2, 2.35)
    d.cu("rol", "Asignar rol", X2, 4.55)
    d.cu("des", "Desactivar usuario", X2, 5.65)

    d.cu("bit", "Registrar en bitácora", X3, 3.4, "seg", ancho=2.2)
    d.cu("cif", "Cifrar contraseña", X3, 5.65, "seg", ancho=2.2)

    d.actor("SA", "Super Administrador\n(hereda del Administrador)", X_ACT, 1.75)
    d.actor("RO", "Responsable\nde ofrendas", X_ACT, 3.05)
    d.actor("PA", "Administrador\n(Pastor)", X_ACT, 4.55)
    d.actor("DB", "Servidor de base\nde datos PostgreSQL", X_SIS, 3.4, sistema=True)

    asociar(d, {"SA": ["bita"], "RO": ["ofr"], "PA": ["ofr", "usr"]})
    d.include("usr", "rol")
    d.include("usr", "bit")
    d.include("ofr", "bit")
    d.include("des", "bit")
    d.include("usr", "cif")
    d.extend("des", "usr")
    d.extend("exp", "bita")
    d.extend("exp", "ofr")
    d.asocia("bit", "DB")
    d.asocia("cif", "DB")
    d.nota("n1", "Solo el Super Administrador\\lasigna los roles Administrador\\ly Super Administrador.\\l"
           "El Administrador crea las\\lcuentas de los niveles 3 a 5.\\l", 12.25, 5.7, 2.3, 1.05)
    d.escribir()


# -------------------------------------------------------------------------------------
# CU-04 · Módulo PVA – Casas de Vida
# -------------------------------------------------------------------------------------
def casas_vida():
    d = Diagrama("cu-04-casas-vida", "CU-04 · Módulo PVA – Casas de Vida", 14.4, 12.6)
    X1, X2, X3, X_SIS = 4.1, 7.25, 10.25, 13.25
    filas = [1.5 + 0.72 * i for i in range(14)]
    r = dict(zip(["area", "casa", "part", "imp", "seg", "gen", "casis", "crep", "envg", "cseg",
                  "ccasa", "cpart", "asis", "envs"], filas))

    d.marco("sistema", "Servidor web · Plataforma PVA (Django 5.2)", 2.0, 0.55, 11.75, 12.3, "sistema")
    d.marco("p_pva", "Módulo PVA – Casas de Vida", 2.3, 1.0, 8.75, 12.0)
    d.marco("p_seg", "Servicios de seguridad", 9.0, 1.0, 11.5, 12.0)

    textos = {
        "area": "Gestionar Áreas", "casa": "Gestionar Casas de Vida", "part": "Gestionar participantes",
        "imp": "Importar datos", "seg": "Gestionar seguimiento", "gen": "Generar reporte consolidado",
        "casis": "Consultar asistencia", "crep": "Consultar reportes", "envg": "Enviar reporte general",
        "cseg": "Consultar seguimiento", "ccasa": "Consultar Casas de Vida",
        "cpart": "Consultar participantes", "asis": "Registrar asistencia", "envs": "Enviar reporte semanal",
    }
    for k, y in r.items():
        d.cu(k, textos[k], X1, y, ancho=2.45)
    d.cu("des", "Desactivar registro", X2, 1.6)
    d.cu("exp", "Exportar reporte", X2, r["casis"])
    d.cu("act", "Registrar actividad", X2, r["asis"])
    d.cu("bit", "Registrar en bitácora", X3, r["casis"], "seg", ancho=2.2)

    d.actor("PA", "Administrador\n(Pastor)", X_ACT, 3.7)
    d.actor("SU", "Supervisor\nde Área", X_ACT, 7.25)
    d.actor("LI", "Líder de\nCasa de Vida", X_ACT, 8.75)
    d.actor("EQ", "Equipo de\nCasa de Vida", X_ACT, 10.05, abstracto=True)
    d.actor("AP", "Usuario de apoyo\n(Aprendiz, Anfitrión,\nMaestro de Niños)", X_ACT, 11.45)
    d.actor("DB", "Servidor de base\nde datos PostgreSQL", X_SIS, r["casis"], sistema=True)

    asociar(d, {
        "PA": ["area", "casa", "part", "imp", "seg", "gen", "casis", "crep"],
        "SU": ["casis", "crep", "envg", "cseg", "ccasa", "cpart"],
        "LI": ["cseg"],
        "EQ": ["casis", "crep", "ccasa", "cpart", "asis", "envs"],
    })
    d.generaliza("LI", "EQ")
    d.generaliza("AP", "EQ")
    d.include("envg", "crep")
    d.include("asis", "act")
    for k in ["area", "casa", "part", "imp", "seg", "envg", "asis", "envs", "des"]:
        d.include(k, "bit")
    for k in ["area", "casa", "part"]:
        d.extend("des", k, puerto="ne")
    d.extend("exp", "crep")
    d.extend("exp", "gen")
    d.asocia("bit", "DB")
    d.escribir()


# -------------------------------------------------------------------------------------
# CU-05 · Módulo Escuelas de Formación
# -------------------------------------------------------------------------------------
def formacion():
    d = Diagrama("cu-05-escuelas-formacion", "CU-05 · Módulo Escuelas de Formación", 13.8, 8.6)
    X1, X2, X3, X_SIS = 4.1, 7.1, 9.95, 12.75
    filas = [1.6 + 0.85 * i for i in range(8)]
    r = dict(zip(["dproc", "proc", "ret", "sfor", "pfor", "afor", "rfor"], filas))

    d.marco("sistema", "Servidor web · Plataforma PVA (Django 5.2)", 2.0, 0.55, 11.35, 8.3, "sistema")
    d.marco("p_for", "Módulo Escuelas de Formación", 2.3, 1.0, 8.55, 8.0)
    d.marco("p_seg", "Servicios de seguridad", 8.8, 1.0, 11.1, 8.0)

    textos = {
        "dproc": "Desactivar proceso", "proc": "Gestionar procesos\nde formación",
        "pfor": "Gestionar participantes\nde formación", "ret": "Retirar participante\nde un proceso",
        "afor": "Registrar asistencia\nde formación", "sfor": "Gestionar seguimiento\nde formación",
        "rfor": "Generar reporte\nde formación",
    }
    for k, y in r.items():
        d.cu(k, textos[k], X1, y, ancho=2.45)
    d.cu("ins", "Inscribir participante", X2 + 0.25, r["pfor"], ancho=2.0)
    d.cu("act", "Registrar actividad", X2 + 0.25, r["afor"], ancho=2.0)
    d.cu("exp", "Exportar reporte", X2 + 0.25, r["rfor"], ancho=2.0)
    # La bitácora va arriba: el abanico de «include» sube y deja libres los casos de la columna 2.
    d.cu("bit", "Registrar en bitácora", X3, 1.9, "seg", ancho=2.1)

    d.actor("PA", "Administrador (Pastor)\n(todos los procesos)", X_ACT, 1.75)
    d.actor("CO", "Coordinador de Escuelas\nde Formación\n(procesos que coordina)", X_ACT, 4.6)
    d.actor("DB", "Servidor de base\nde datos PostgreSQL", X_SIS, 1.9, sistema=True)

    asociar(d, {"PA": ["dproc"], "CO": ["proc", "pfor", "ret", "afor", "sfor", "rfor"]})
    d.generaliza("PA", "CO")
    d.include("pfor", "ins")
    d.include("afor", "act")
    for k in ["dproc", "proc", "pfor", "ret", "afor", "sfor"]:
        d.include(k, "bit")
    d.extend("exp", "rfor")
    d.asocia("bit", "DB")
    d.nota("n1", "El Administrador hereda todos\\llos casos de uso del Coordinador\\l"
           "en este módulo y, además,\\lpuede desactivar procesos.\\l", 12.15, 7.45, 2.4, 0.9)
    d.escribir()


# -------------------------------------------------------------------------------------
# CU-00 · Jerarquía de usuarios (niveles de autoridad, de mayor a menor)
# -------------------------------------------------------------------------------------
def jerarquia():
    d = Diagrama("cu-00-jerarquia-actores", "CU-00 · Jerarquía de usuarios de la plataforma web PVA – CCMG Girón",
                 12.3, 12.6)
    X_NIV, X_FIG, X_TAR, ANCHO = 0.95, 2.45, 7.55, 8.3
    ADMIN, OPER, SIN = "#1F3A5F", "#3D7A8C", "#8A949C"

    d.marco("g_adm", "Administración del sistema", 0.25, 0.95, 12.0, 4.25)
    d.marco("g_ope", "Operación del Plan Vida Abundante", 0.25, 4.6, 12.0, 9.85)
    d.marco("g_sin", "Sin cuenta en la plataforma", 0.25, 10.2, 12.0, 11.85)

    filas = {
        "n1": (1.95, "Nivel 1", ADMIN), "n2": (3.5, "Nivel 2", ADMIN),
        "n3": (5.6, "Nivel 3", OPER), "n4": (7.15, "Nivel 4", OPER), "n5": (8.75, "Nivel 5", OPER),
        "n6": (11.0, "Nivel 6", SIN),
    }
    for k, (y, txt, color) in filas.items():
        d.nivel(k, txt, X_NIV, y, color)
    claves = list(filas)
    for a, b in zip(claves, claves[1:]):
        d.flecha(a, b)
    d.texto("mas", "mayor autoridad", X_NIV, 1.4)
    d.texto("menos", "menor autoridad", X_NIV, 11.55)

    d.actor("SA", "Super\nAdministrador", X_FIG, 1.95)
    d.actor("AD", "Administrador\n(Pastor)", X_FIG, 3.5)
    d.actor("SU", "Supervisor\nde Área", X_FIG, 5.6)
    d.actor("CO", "Coordinador de\nEscuelas de\nFormación", X_FIG, 7.15)
    d.actor("LI", "Líder de Casa de\nVida y su equipo", X_FIG, 8.75)
    d.actor("MA", "Miembro\nAsistente", X_FIG, 11.0)

    d.tarjeta("t1", X_TAR, 1.95, ANCHO, 1.15, "Super Administrador", "SUPERADMIN", [
        "Gestiona toda la plataforma y consulta la bitácora de auditoría.",
        "<B>Es el único que crea Administradores y otros Super Administradores.</B>",
    ], "#D6E4F0")
    d.tarjeta("t2", X_TAR, 3.5, ANCHO, 1.15, "Administrador (Pastor)", "PASTOR", [
        "Administra el PVA y las Escuelas de Formación: usuarios, Áreas, Casas de Vida,",
        "participantes, ofrendas y reportes. <B>Crea las cuentas de los niveles 3 a 5</B>",
        "y autoriza al responsable de ofrendas.",
    ], "#D6E4F0")
    d.tarjeta("t3", X_TAR, 5.6, ANCHO, 1.05, "Supervisor de Área", "SUPERVISOR_AREA", [
        "Supervisa, en solo lectura, las Casas de Vida de su Área.",
        "Recibe los reportes semanales y envía el reporte general al Administrador.",
    ], "#D5ECEF")
    d.tarjeta("t4", X_TAR, 7.15, ANCHO, 1.05, "Coordinador de Escuelas de Formación", "COORDINADOR_FORMACION", [
        "Gestiona los procesos de formación que coordina (Pasos de Vida, Escuelas Vida,",
        "Módulos de Liderazgo, Misiones): participantes, asistencia, seguimiento y reportes.",
    ], "#D5ECEF")
    d.tarjeta("t5", X_TAR, 8.75, ANCHO, 1.15, "Líder de Casa de Vida y su equipo de trabajo",
              "LIDER_CASA_VIDA · APOYO_CASA_VIDA", [
                  "Consultan su Casa de Vida, registran la asistencia y envían el reporte semanal",
                  "al Supervisor de Área. Equipo de trabajo: Aprendiz, Anfitrión y Maestro de Niños.",
              ], "#D5ECEF")
    d.tarjeta("t6", X_TAR, 11.0, ANCHO, 0.85, "Miembro Asistente", "ninguno", [
        "Visitante o miembro nuevo: solo consulta la página pública de la iglesia.",
    ], "#E6E9EB")

    for a, t in [("SA", "t1"), ("AD", "t2"), ("SU", "t3"), ("CO", "t4"), ("LI", "t5"), ("MA", "t6")]:
        d.asocia(a, t)

    d.nota("n_of", "Responsable de ofrendas: no es un nivel. Es un permiso que el\\l"
           "Administrador concede a un usuario de cualquier nivel (RN14).\\l", 8.6, 12.25, 4.6, 0.5)
    d.escribir()


if __name__ == "__main__":
    jerarquia()
    general()
    acceso()
    administracion()
    casas_vida()
    formacion()


