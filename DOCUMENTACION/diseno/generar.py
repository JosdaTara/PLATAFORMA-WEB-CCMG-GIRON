"""Genera Wireframes_PVA.html y Mockups_PVA.html desde una sola definición de pantallas.

Cada pantalla se escribe una vez; el wireframe y el mockup comparten el mismo HTML y solo cambian
de hoja de estilo (wireframe.css / mockup.css). Así ambos conjuntos tienen la misma estructura,
los mismos identificadores y el mismo orden.

Uso:  python generar.py
"""
import re
from pathlib import Path

AQUI = Path(__file__).parent
TITULO_PROYECTO = "Plataforma Web para la gestión y seguimiento del plan vida abundante de la iglesia CCMG de Girón"
VERSION = "Versión del proyecto: rama main, commit 020758b (24/11/2026)"


# ======================================================================
# Piezas de interfaz
# ======================================================================
def ic(nombre):
    return f'<i class="bi bi-{nombre}" aria-hidden="true"></i>'


def btn(texto, tipo="pri", icono=None, extra=""):
    i = ic(icono) if icono else ""
    return f'<span class="btn {tipo} {extra}">{i}{texto}</span>'


def badge(texto, tipo="ok", icono=None):
    i = ic(icono) if icono else ""
    return f'<span class="badge {tipo}">{i}{texto}</span>'


def fld(etiqueta, valor="", ph=False, cls="", ayuda="", err="", sel=False, area=False):
    v = f'<span class="ph">{valor}</span>' if ph else f"<span>{valor}</span>"
    flecha = ic("chevron-down") if sel else ""
    a = " area" if area else ""
    ay = f'<div class="ayuda">{ayuda}</div>' if ayuda else ""
    er = f'<div class="err-txt">{ic("exclamation-circle")}{err}</div>' if err else ""
    return f'<div class="fld"><label>{etiqueta}</label><div class="inp{a} {cls}">{v}{flecha}</div>{ay}{er}</div>'


def check(texto, si=False):
    marca = "✓" if si else ""
    return f'<div class="check"><span class="cb {"si" if si else ""}">{marca}</span><span>{texto}</span></div>'


def tabla(cols, filas, der=(), clase=""):
    th = "".join(f'<th class="{"der" if i in der else ""}">{c}</th>' for i, c in enumerate(cols))
    cuerpo = ""
    for f in filas:
        cls = ""
        if isinstance(f, tuple) and f and f[0] == "__total__":
            cls, f = "total", f[1]
        tds = ""
        for i, c in enumerate(f):
            k = "der" if i in der else ""
            if i == len(f) - 1 and isinstance(c, str) and c.startswith('<span class="btn'):
                k = "acc"
            tds += f'<td class="{k}">{c}</td>'
        cuerpo += f'<tr class="{cls}">{tds}</tr>'
    return f'<table class="tbl {clase}"><thead><tr>{th}</tr></thead><tbody>{cuerpo}</tbody></table>'


def stats(items):
    h = "".join(
        f'<div class="stat"><div><div class="et">{e}</div><div class="num">{n}</div></div><div class="ico">{ic(i)}</div></div>'
        for e, n, i in items)
    return f'<div class="stats">{h}</div>'


def cab(titulo, sub="", acciones=""):
    s = f"<p>{sub}</p>" if sub else ""
    a = f'<div class="acciones">{acciones}</div>' if acciones else ""
    return f'<div class="cab"><div><h1>{titulo}</h1>{s}</div>{a}</div>'


def alerta(texto, tipo="ok", icono="check-circle"):
    return f'<div class="alerta {tipo}"><span class="ico">{ic(icono)}</span><span>{texto}</span></div>'


def apilada(registros):
    """Tabla reorganizada como tarjetas en el teléfono (clase tabla-apilada de la plataforma)."""
    h = ""
    for titulo, pares in registros:
        filas = "".join(f'<div class="par"><span>{a}</span><span>{b}</span></div>' for a, b in pares)
        h += f'<div class="reg"><div class="tit">{titulo}</div>{filas}</div>'
    return f'<div class="apilada">{h}</div>'


# Menús reales por rol (orden tomado de la plataforma)
M_PASTOR = [("speedometer2", "Inicio"), ("person-plus", "Personas nuevas"), ("houses", "Casas de Vida"), ("map", "Áreas"),
            ("upload", "Importar datos"), ("check2-square", "Asistencia"), ("clipboard-check", "Seguimiento"),
            ("file-earmark-text", "Reportes"), ("people", "Usuarios"), ("cash-coin", "Ofrendas"), ("person-circle", "Mi perfil")]
M_SA = M_PASTOR[:10] + [("shield-check", "Auditoría"), ("person-circle", "Mi perfil")]
M_EQUIPO = [("speedometer2", "Inicio"), ("person-plus", "Personas nuevas"), ("houses", "Casas de Vida"), ("check2-square", "Asistencia"),
            ("clipboard-check", "Seguimiento"), ("file-earmark-text", "Reportes"), ("person-circle", "Mi perfil")]
M_FORM = [("speedometer2", "Inicio"), ("mortarboard", "Procesos de formación"), ("people", "Participantes"),
          ("calendar-check", "Actividades y asistencia"), ("clipboard-check", "Seguimiento"), ("file-earmark-text", "Reportes"),
          ("person-circle", "Mi perfil")]


def side(modulo, menu, activo, cambiar=False):
    items = "".join(
        f'<a class="{"act" if t == activo else ""}">{ic(i)}{t}</a>' for i, t in menu)
    cm = f'<div class="salir" style="background:transparent;border:0">{ic("arrow-left-right")}Cambiar de módulo</div>' if cambiar else ""
    return (f'<aside class="side"><div class="marca"><span class="logo blanco"></span><div class="nom">CCMG · Girón</div>'
            f'<div class="mod">{modulo}</div></div><nav>{items}</nav>{cm}<div class="salir">{ic("box-arrow-left")}Cerrar sesión</div></aside>')


def escritorio(side_html, tag, usuario, rol, cuerpo, extra="", alto=False):
    clase = " largo" if alto == "largo" else " alto" if alto else ""
    return (f'<div class="escritorio{clase}"><div class="pantalla"><div class="app">{side_html}<div class="main">'
            f'<div class="top"><span class="tag">{ic("houses" if "Casas" in tag else "mortarboard" if "Formación" in tag else "gear")} {tag}</span>'
            f'<span class="tema">{ic("moon-stars")}</span><span class="quien"><b>{usuario}</b><small>{rol}</small></span></div>'
            f'<div class="cuerpo">{cuerpo}</div></div></div>{extra}</div></div>')


def movil(usuario, rol, cuerpo, extra=""):
    return (f'<div class="movil"><div class="pantalla"><div class="m-top"><span class="hamb" style="width:40px;height:40px;border-radius:10px;display:grid;place-items:center;border:1px solid #ccc">{ic("list")}</span>'
            f'<span class="logo"></span><span class="tema" style="width:38px;height:38px;border-radius:10px;display:grid;place-items:center;border:1px solid #ccc;margin-left:8px">{ic("moon-stars")}</span>'
            f'<span class="quien"><b>{usuario}</b><small>{rol}</small></span></div><div class="m-cuerpo">{cuerpo}</div>{extra}</div></div>')


def pieza(html, ancho=560):
    return f'<div class="pieza" style="width:{ancho}px"><div class="pantalla" style="padding:20px">{html}</div></div>'


# ======================================================================
# Pantallas (P01–P25)
# ======================================================================
SA = ("Super Admin Demo", "Super Administrador")
PASTOR = ("Pastor Demo", "Pastor")
SUP = ("Carlos Supervisor", "Supervisor de Área")
LIDER = ("María Líder", "Líder de Casa de Vida")
COORD = ("Laura Coordinadora", "Coordinador de Formación")

PERSONAS = [("Julián Prueba Demo", "301 444 5566", "Casa Esperanza", "17/11/2026", badge("Activo") + " " + badge("Autorización pendiente", "pend")),
            ("Andrés Rojas", "300 123 4503", "Casa Esperanza", "31/08/2026", badge("Activo")),
            ("Lucía Gómez", "300 123 4502", "Casa Esperanza", "31/08/2026", badge("Activo")),
            ("José Núñez", "300 123 4501", "Casa Esperanza", "31/08/2026", badge("Activo")),
            ("Ana María Pérez", "300 123 4500", "Casa Esperanza", "31/08/2026", badge("Activo"))]


def p01():
    nav = ('<div class="pub-nav"><span class="logo-p"><span class="logo blanco"></span>CCMG Girón</span>'
           '<a>Inicio</a><a>Quiénes somos</a><a>Plan Vida Abundante</a><a>Formación</a><a>Contacto</a>'
           f'<span class="tema" style="width:38px;height:38px;border-radius:10px;display:grid;place-items:center;border:1px solid rgba(255,255,255,.5)">{ic("moon-stars")}</span>'
           f'{btn("Iniciar sesión", "oro", "box-arrow-in-right")}</div>')
    hero = ('<div class="hero"><div class="foto f1"></div><div class="velo-h"></div><div class="tx"><span class="logo blanco logo-g" style="display:block"></span>'
            '<h1>Bienvenido<br>a la iglesia<br><span class="acento">CCMG de Girón</span></h1>'
            '<p>Una comunidad que adora, crece y sirve. Conoce el Plan Vida Abundante y encuentra tu Casa de Vida.</p>'
            f'{btn("Conocer el PVA", "oro", None, "lg")}</div></div>')
    franja = ('<div class="franja">'
              f'<div class="card"><h3 class="sec">{ic("houses")} Casas de Vida</h3><p style="margin:0;font-size:14px">Grupos en los hogares para acompañar a cada persona.</p></div>'
              f'<div class="card"><h3 class="sec">{ic("mortarboard")} Escuelas de Formación</h3><p style="margin:0;font-size:14px">Pasos de Vida, Escuelas Vida, Liderazgo y Misiones.</p></div>'
              f'<div class="card"><h3 class="sec">{ic("geo-alt")} Contacto</h3><p style="margin:0;font-size:14px">Horarios de culto y ubicación en Girón.</p></div></div>')
    d = f'<div class="escritorio"><div class="pantalla">{nav}{hero}{franja}</div></div>'
    m = ('<div class="movil"><div class="pantalla"><div class="m-pub-top"><span class="logo blanco"></span>CCMG Girón'
         f'<span style="margin-left:auto">{btn("Ingresar", "oro", None, "sm")}</span></div>'
         '<div class="m-hero"><div class="foto f1"></div><div class="tx"><span class="logo blanco" style="width:60px;height:60px;display:block;margin:0 auto"></span>'
         '<h1>Bienvenido a la iglesia <span class="acento">CCMG de Girón</span></h1><p>Una comunidad que adora, crece y sirve.</p>'
         f'{btn("Conocer el PVA", "oro")}</div></div>'
         f'<div class="barra-inf"><div class="act">{ic("house")}Inicio</div><div>{ic("people")}Nosotros</div><div>{ic("houses")}PVA</div><div>{ic("mortarboard")}Formación</div><div>{ic("envelope")}Contacto</div></div></div></div>')
    return [("Escritorio", d, "z60"), ("Móvil · secciones en barra inferior", m, "z52")]


def login_tarjeta(error=False):
    e = alerta("Usuario o contraseña incorrectos.", "err", "exclamation-triangle") if error else ""
    return ('<div class="tarj"><span class="logo"></span><div class="nom">CCMG Girón</div><div class="sub">Plataforma Plan Vida Abundante</div>' + e +
            fld("Usuario o correo", "maria.lider@iglesia.example", cls="mal" if error else "") +
            fld("Contraseña", "••••••••••••••••", cls="mal" if error else "", ayuda="Mínimo 15 caracteres.") +
            btn("Ingresar", "pri", None, "blk lg") +
            '<div class="links"><a>← Volver al inicio</a><a>¿Olvidaste tu contraseña?</a></div></div>')


def p02():
    d = f'<div class="escritorio"><div class="pantalla"><div class="login"><div class="banner"><div class="foto f2"></div></div><div class="lado">{login_tarjeta()}</div></div></div></div>'
    m = f'<div class="movil"><div class="pantalla login" style="display:block"><div class="m-login">{login_tarjeta(True)}</div></div></div>'
    return [("Escritorio", d, "z60"), ("Móvil · estado: credenciales incorrectas", m, "z52")]


def p03():
    sol = ('<div class="tarj"><span class="logo"></span><h2>Recuperar contraseña</h2><p class="txt">Escribe el correo de tu cuenta y te enviaremos un enlace para crear una nueva.</p>'
           + fld("Correo electrónico", "maria.lider@iglesia.example") + btn("Enviar enlace", "pri", None, "blk lg") +
           '<div class="links" style="justify-content:center"><a>← Volver al inicio de sesión</a></div></div>')
    env = ('<div class="tarj" style="text-align:center"><span class="logo"></span><h2>Revisa tu correo</h2>'
           f'<div style="font-size:40px;margin:6px 0 10px">{ic("envelope-check")}</div>'
           '<p class="txt">Si el correo está registrado en la plataforma, en unos minutos recibirás un mensaje de CCMG Girón con un enlace para crear tu nueva contraseña.</p>'
           '<p class="txt" style="font-weight:600">El enlace vence en 60 minutos y sirve una sola vez.</p>'
           + btn("Volver al inicio de sesión", "pri", None, "blk") + '<div class="links" style="justify-content:center"><a>¿No llegó? Solicitar otro enlace</a></div></div>')
    d = f'<div class="escritorio"><div class="pantalla"><div class="login"><div class="banner"><div class="foto f2"></div></div><div class="lado">{sol}</div></div></div></div>'
    e = f'<div class="pieza" style="width:520px"><div class="pantalla"><div class="login"><div class="lado" style="padding:30px 0">{env}</div></div></div></div>'
    return [("Escritorio · solicitud", d, "z60"), ("Estado: enlace enviado", e, "z60")]


def p04():
    mod = lambda n, et, cls, icono, t, desc, items, b: (
        f'<div class="mod"><span class="et {cls}">{ic(icono)} {et}</span><div class="ico {cls}">{ic(icono)}</div><h2>{t}</h2>'
        f'<div style="font-size:15px">{desc}</div><ul>' + "".join(f"<li>{ic('check-circle')}{x}</li>" for x in items) + f"</ul>{b}</div>")
    d = ('<div class="escritorio alto"><div class="pantalla"><div class="selector"><div class="caja"><div class="cab-s"><span class="logo blanco"></span>'
         '<h1>Selecciona un módulo</h1><p>Casas de Vida y Escuelas de Formación son módulos independientes.</p>'
         f'<span class="chip-u">{ic("person-badge")}<b>Pastor Demo</b> · Pastor</span></div><div class="mods">'
         + mod(1, "MÓDULO 1", "v", "houses", "Casas de Vida", "Acompañamiento cercano a cada persona y a su grupo.",
               ["Participantes y miembros", "Casas de Vida y líderes", "Asistencia y seguimiento", "Ofrendas y reportes"], btn("Ingresar", "pri", "arrow-right"))
         + mod(2, "MÓDULO 2", "o", "mortarboard", "Escuelas de Formación", "Procesos formativos y discipulado de la congregación.",
               ["Procesos de formación", "Inscripciones", "Actividades y asistencia", "Seguimiento y reportes"], btn("Ingresar", "oro", "arrow-right"))
         + f'</div><div class="pie-s">{btn("Gestión de usuarios", "sec", "people")}{btn("Cerrar sesión", "ghost", "box-arrow-left")}</div></div></div></div></div>')
    return [("Escritorio", d, "z74")]


USUARIOS = [("Pastor Demo", "pastor@demo.test", "Pastor", "24/11/2026 14:35", badge("Activo")),
            ("Carlos Supervisor", "supervisor@demo.test", "Supervisor de Área", "24/11/2026 14:40", badge("Activo")),
            ("María Líder", "lider@demo.test", "Líder de Casa de Vida", "24/11/2026 14:40", badge("Activo")),
            ("Pedro Anfitrión", "apoyo@demo.test", "Apoyo de Casa de Vida", "30/10/2026 11:57", badge("Activo")),
            ("Laura Coordinadora", "coordinador@demo.test", "Coordinador de Formación", "24/11/2026 14:40", badge("Activo")),
            ("Rosa Prueba", "rosa@demo.test", "Coordinador de Formación", "Nunca", badge("Inactivo", "neu"))]


def p05():
    filas = []
    for n, c, r, u, e in USUARIOS:
        acc = btn("Editar", "out", "pencil", "sm") + (btn("Reactivar", "sec", "arrow-counterclockwise", "sm") if "Inactivo" in e else btn("Desactivar", "dan", "slash-circle", "sm"))
        filas.append((f"<b>{n}</b>", c, r, u, e, acc))
    cuerpo = (alerta("Usuario creado correctamente.") +
              cab("Gestión de usuarios", "Cuentas de la plataforma, su rol y su asignación.", btn("Crear usuario", "pri", "person-plus")) +
              tabla(["Nombre", "Correo", "Rol", "Último acceso", "Estado", "Acciones"], filas))
    d = escritorio(side("Administración", M_SA, "Usuarios", True), "Gestión de usuarios", *SA, cuerpo)
    return [("Escritorio · estado: confirmación después de guardar", d, "z74")]


def form_usuario(error):
    e = dict(cls="mal", err="Las dos contraseñas no coinciden.") if error else {}
    return ('<div class="card"><div class="sec-tit">Datos de la cuenta</div><div class="grid2">'
            + fld("Nombre completo *", "Rosa Martínez") + fld("Correo electrónico *", "rosa.martinez@iglesia.example")
            + fld("Nombre de usuario (opcional)", "rosa.m") + fld("Rol *", "Supervisor de Área", sel=True) + "</div>"
            + check("Autorizado como responsable de ofrendas") + "</div>"
            '<div class="card"><div class="sec-tit">Asignación</div><div class="grid2">' + fld("Área que supervisa *", "Área Sur", sel=True) + "</div></div>"
            '<div class="card"><div class="sec-tit">Contraseña</div><div class="sec-desc">Asigna la contraseña con la que el usuario entrará por primera vez.</div><div class="grid2">'
            + fld("Contraseña *", "••••••••••••••••", ayuda="Mínimo 15 caracteres.") + fld("Confirmar contraseña *", "•••••••••••••••", **e) + "</div>"
            + f'<div style="margin:-4px 0 10px">{btn("Generar una contraseña segura", "ghost", "magic")}</div>'
            + check("Pedir que la cambie al iniciar sesión por primera vez", True) + "</div>"
            + f'<div class="acciones">{btn("Guardar", "pri", "check-lg")}{btn("Cancelar", "sec")}</div>')


def p06():
    d = escritorio(side("Administración", M_SA, "Usuarios", True), "Gestión de usuarios", *SA,
                   cab("Crear usuario", "", btn("Volver", "sec", "arrow-left", "sm")) + form_usuario(True), alto=True)
    return [("Escritorio · estado: validación del formulario", d, "z74")]


def p07():
    filas = [("24/11/2026 14:41", "Super Admin Demo", badge("INICIAR_SESION", "neu"), "Usuario", "7", "127.0.0.1"),
             ("24/11/2026 14:40", "María Líder", badge("ENVIAR_REPORTE", "neu"), "Reporte", "3", "127.0.0.1"),
             ("24/11/2026 14:40", "Laura Coordinadora", badge("REGISTRAR_ASISTENCIA", "neu"), "Actividad", "5", "127.0.0.1"),
             ("24/11/2026 14:38", "Pastor Demo", badge("CREAR", "neu"), "CasaVida", "2", "127.0.0.1"),
             ("24/11/2026 14:36", "Pastor Demo", badge("IMPORTAR", "neu"), "Participante", "—", "127.0.0.1"),
             ("24/11/2026 14:30", "María Líder", badge("ACTUALIZAR_PERFIL", "neu"), "Usuario", "4", "127.0.0.1")]
    cuerpo = (cab("Bitácora de auditoría", "Quién creó, modificó, desactivó o importó información, y cuándo.",
                  btn("PDF", "sec", "file-earmark-pdf", "sm") + btn("Excel", "sec", "file-earmark-excel", "sm")) +
              '<div class="filtros">' + fld("Usuario", "Todos", sel=True) + fld("Acción", "Todas", sel=True) + fld("Entidad", "Todas", sel=True)
              + fld("Desde", "dd/mm/aaaa", ph=True) + fld("Hasta", "dd/mm/aaaa", ph=True) + btn("Filtrar", "pri", "search") + "</div>"
              + tabla(["Fecha", "Usuario", "Acción", "Entidad", "ID", "IP"], filas))
    return [("Escritorio", escritorio(side("Administración", M_SA, "Auditoría", True), "Gestión de usuarios", *SA, cuerpo), "z74")]


def panel_cuerpo(lider=False, enviado=False):
    if lider:
        av = ('<div class="aviso-sem ok"><div class="ico">' + ic("check2-circle") + '</div><div class="tx"><b>Reporte de esta semana enviado.</b>'
              '<span>Casa Esperanza · Semana 48 · Enviado el 24/11/2026 a Carlos Supervisor</span></div>' + btn("Ver reporte", "out") + "</div>") if enviado else (
             '<div class="aviso-sem"><div class="ico">' + ic("clipboard-plus") + '</div><div class="tx"><b>Falta el reporte de esta semana.</b>'
             '<span>Casa Esperanza · Semana 48 · 23/11/2026 al 29/11/2026 · Llega a Carlos Supervisor</span></div>' + btn("Llenar reporte", "oro", None, "lg") + "</div>")
    else:
        av = ""
    n = (5, 1) if lider else (7, 2)
    return (f'<div class="cab"><div><h1>Hola, {"María Líder" if lider else "Pastor Demo"}</h1></div></div>' + av +
            '<p style="margin:0 0 12px;color:inherit;opacity:.75">Resumen del módulo de Casas de Vida.</p>' +
            stats([("Personas nuevas", n[0], "person-plus"), ("Casas de Vida", n[1], "houses"), ("Asistentes por reunión", 15, "graph-up"), ("Seguimientos abiertos", 1, "clipboard-check")]) +
            '<div class="fila"><div class="card" style="flex:1.4"><h2>Últimos reportes de asistencia</h2>' +
            tabla(["Casa de Vida", "Fecha", "Asistentes", "Nuevos"], [("Casa Esperanza", "17/11/2026", "15", "2"), ("Casa Esperanza", "10/11/2026", "13", "1")]) +
            '</div><div class="card"><h2>Seguimientos recientes</h2>' + tabla(["Participante", "Estado"], [("Lucía Gómez", badge("Abierto", "pend"))]) + "</div></div>")


def p08_movil_cuerpo():
    return ('<h1>Hola, María Líder</h1><div style="margin:12px 0"></div>' +
            '<div class="aviso-sem"><div class="ico">' + ic("clipboard-plus") + '</div><div class="tx"><b>Falta el reporte de esta semana.</b>'
            '<span>Casa Esperanza · Semana 48 · Llega a Carlos Supervisor</span></div>' + btn("Llenar reporte", "oro", None, "lg") + "</div>" +
            stats([("Personas nuevas", 5, "person-plus"), ("Casas de Vida", 1, "houses"), ("Asistentes por reunión", 15, "graph-up"), ("Seguimientos abiertos", 1, "clipboard-check")]))


def p08():
    d = escritorio(side("Casas de Vida", M_EQUIPO, "Inicio"), "Módulo Casas de Vida", *LIDER, panel_cuerpo(True))
    return [("Escritorio · Líder: falta el reporte", d, "z60"), ("Móvil", movil(*LIDER, p08_movil_cuerpo()), "z52")]


def p08b():
    d = escritorio(side("Casas de Vida", M_PASTOR, "Inicio", True), "Módulo Casas de Vida", *PASTOR, panel_cuerpo(False))
    cajon = '<div class="cajon">' + side("Casas de Vida", M_EQUIPO, "Inicio") + '<div class="resto"></div></div>'
    return [("Escritorio · Pastor (sin aviso semanal)", d, "z60"), ("Móvil · menú abierto", movil(*LIDER, p08_movil_cuerpo(), cajon), "z52")]


def p08c():
    d = escritorio(side("Casas de Vida", M_EQUIPO, "Inicio"), "Módulo Casas de Vida", *LIDER, panel_cuerpo(True, enviado=True))
    return [("Escritorio · Líder: estado reporte enviado", d, "z74")]


def p09():
    filas = [("<b>Casa Esperanza</b>", "Norte", "María Líder", "Carlos Supervisor", "5", badge("Activa"),
              btn("Ver", "sec", "eye", "sm") + btn("Editar", "out", "pencil", "sm") + btn("Desactivar", "dan", "slash-circle", "sm")),
             ("<b>Casa Fe</b>", "Sur", "—", "Sin asignar", "2", badge("Activa"),
              btn("Ver", "sec", "eye", "sm") + btn("Editar", "out", "pencil", "sm") + btn("Desactivar", "dan", "slash-circle", "sm"))]
    cuerpo = (cab("Casas de Vida", "Grupos de cada Área con su Líder y su Supervisor.", btn("Nueva Casa de Vida", "pri", "plus-lg")) +
              tabla(["Casa de Vida", "Área", "Líder", "Supervisor", "Personas nuevas", "Estado", "Acciones"], filas, der=(4,)))
    d = escritorio(side("Casas de Vida", M_PASTOR, "Casas de Vida", True), "Módulo Casas de Vida", *PASTOR, cuerpo)
    vac = pieza('<div class="card" style="margin:0"><div class="vacio"><span class="ico">' + ic("houses") + '</span><b>No tienes Casas de Vida asignadas.</b>'
                '<p>Cuando el Pastor te asigne una Casa de Vida aparecerá aquí.</p></div></div>', 520)
    return [("Escritorio · Pastor", d, "z60"), ("Estado: listado vacío (Supervisor o Líder sin asignación)", vac, "z52")]


def p10():
    cuerpo = (cab("Nueva Casa de Vida", "", btn("Volver", "sec", "arrow-left", "sm")) +
              '<div class="card" style="max-width:820px"><div class="grid2">' + fld("Nombre de la Casa de Vida *", "Casa Betania", cls="foco")
              + fld("Área *", "Sur", sel=True) + fld("Líder de Casa de Vida", "Seleccione un líder", ph=True, sel=True) + fld("Dirección", "Calle 30 # 25-14, Girón") + "</div>"
              '<div class="ayuda" style="margin:-4px 0 14px">* Campo obligatorio. El equipo de apoyo se asigna desde la gestión de usuarios.</div>'
              f'<div class="acciones">{btn("Guardar", "pri", "check-lg")}{btn("Cancelar", "sec")}</div></div>')
    d = escritorio(side("Casas de Vida", M_PASTOR, "Casas de Vida", True), "Módulo Casas de Vida", *PASTOR, cuerpo)
    ok = pieza(alerta("Casa de Vida creada correctamente.") + tabla(["Casa de Vida", "Área", "Estado"], [("<b>Casa Betania</b>", "Sur", badge("Activa"))]), 560)
    return [("Escritorio", d, "z60"), ("Estado: confirmación en la lista", ok, "z52")]


def p11():
    cuerpo = (cab("Importar datos", "Carga los datos que hoy tienes en hojas de cálculo. Antes de guardar verás una vista previa.") +
              '<div class="fila"><div class="card" style="flex:1.5"><div class="fld"><label>¿Qué vas a importar?</label>'
              '<div style="display:flex;gap:18px;font-size:14px"><span>◯ Casas de Vida</span><span><b>◉ Participantes</b></span></div></div>'
              + fld("Archivo CSV o Excel (.xlsx)", "participantes_noviembre.xlsx", ayuda="Máximo 5 MB y 2.000 filas. La primera fila debe tener los encabezados.")
              + btn("Revisar archivo", "pri", "eye", "blk") + '</div><div class="card"><h2>Plantillas</h2>'
              '<ol style="font-size:13.5px;padding-left:18px;margin:0 0 12px"><li>Registra primero las Áreas.</li><li>Importa las Casas de Vida.</li><li>Importa los participantes.</li></ol>'
              + btn("Plantilla de Casas de Vida", "sec", "download", "blk") + '<div style="height:8px"></div>' + btn("Plantilla de Participantes", "sec", "download", "blk") + "</div></div>")
    d = escritorio(side("Casas de Vida", M_PASTOR, "Importar datos", True), "Módulo Casas de Vida", *PASTOR, cuerpo)
    prev = pieza('<div class="sec-tit">Vista previa · participantes_noviembre.xlsx</div>' +
                 '<div style="display:flex;gap:8px;margin-bottom:10px">' + badge("18 filas válidas", "ok", "check-circle") + badge("2 con errores", "err", "x-circle") + "</div>" +
                 tabla(["Fila", "Nombre", "Resultado"], [("4", "Sandra Ruiz", badge("Válida")), ("9", "—", badge("Falta el nombre", "err")), ("15", "Jorge Díaz", badge("Teléfono no válido", "err"))]) +
                 f'<div class="acciones" style="margin-top:12px">{btn("Confirmar e importar 18 registros", "pri", "cloud-upload")}{btn("Cambiar archivo", "sec")}{btn("Descargar detalle de errores", "ghost", "download")}</div>', 600)
    return [("Escritorio · carga del archivo", d, "z60"), ("Estado: vista previa con errores", prev, "z52")]


def p12():
    filas = [(f"<b>{n}</b>", t, c, f, e, btn("Ver", "sec", "eye", "sm")) for n, t, c, f, e in PERSONAS]
    cuerpo = (cab("Personas nuevas", "Datos que se toman a quien llega por primera vez a una Casa de Vida.", btn("Registrar persona nueva · Casa Esperanza", "pri", "person-plus")) +
              '<div class="filtros">' + fld("Buscar", "Nombre o teléfono", ph=True) + fld("Casa de Vida", "Todas", sel=True) + btn("Filtrar", "pri", "search") + "</div>" +
              tabla(["Nombre", "Teléfono", "Casa de Vida", "Llegó", "Estado", "Acciones"], filas))
    d = escritorio(side("Casas de Vida", M_EQUIPO, "Personas nuevas"), "Módulo Casas de Vida", *LIDER, cuerpo)
    regs = [(n, [("Teléfono", t), ("Casa de Vida", c), ("Llegó", f), ("Estado", e), ("Acciones", btn("Ver", "sec", "eye", "sm"))]) for n, t, c, f, e in PERSONAS[:2]]
    m = movil(*LIDER, '<h1>Personas nuevas</h1><p style="font-size:13.5px;margin:0 0 10px;opacity:.75">Datos que se toman a quien llega por primera vez.</p>' +
              btn("Registrar persona nueva", "pri", "person-plus", "blk") + '<div style="height:12px"></div>' + apilada(regs))
    vac = pieza('<div class="card" style="margin:0"><div class="vacio"><span class="ico">' + ic("search") + '</span><b>No hay personas nuevas registradas con estos filtros.</b>'
                '<p>Cambia la búsqueda o limpia los filtros.</p>' + btn("Limpiar filtros", "sec", "x-lg") + "</div></div>", 520)
    return [("Escritorio · Líder", d, "z60"), ("Móvil · tabla en tarjetas", m, "z52"), ("Estado: sin resultados", vac, "z52")]


def form_persona(err=False):
    e = dict(cls="mal", err="Escribe un número de teléfono válido.") if err else {}
    return ('<div class="card" style="max-width:640px">' +
            fld("Nombre *", "Laura Gómez") + fld("Número de teléfono *", "300 123 45" if err else "300 123 4567", **e) +
            check("Autorizó el tratamiento de sus datos personales (Ley 1581 de 2012)", True) +
            '<div class="ayuda" style="margin:-4px 0 12px">Si no autoriza, la persona queda con autorización pendiente.</div>' +
            f'<div class="acciones">{btn("Guardar", "pri", "check-lg")}{btn("Cancelar", "sec")}</div></div>')


def p13():
    d = escritorio(side("Casas de Vida", M_EQUIPO, "Personas nuevas"), "Módulo Casas de Vida", *LIDER,
                   cab("Registrar persona nueva", "Casa de Vida Casa Esperanza · 24/11/2026", btn("Volver", "sec", "arrow-left", "sm")) + form_persona())
    m = movil(*LIDER, '<h1>Registrar persona nueva</h1><p style="font-size:13px;margin:0 0 12px;opacity:.75">Casa Esperanza · 24/11/2026</p>' + form_persona(True).replace('style="max-width:640px"', ""))
    ok = pieza(alerta("Se registró a Laura Gómez como persona nueva de Casa Esperanza."), 560)
    return [("Escritorio", d, "z60"), ("Móvil · estado: validación", m, "z52"), ("Estado: confirmación", ok, "z52")]


def form_reporte(movil_=False):
    g = "grid2" if movil_ else "grid3"
    return ('<div class="card"><div class="sec-tit">Reunión</div><div class="grid2">' + fld("Fecha de la reunión *", "24/11/2026", ayuda="Corresponde a la semana 48 (23/11 al 29/11).")
            + fld("Se envía a", "Carlos Supervisor", cls="dis") + "</div></div>"
            '<div class="card"><div class="sec-tit">Asistencia</div><div class="' + g + '">' + fld("Asistentes", "15") + fld("Asistencia niños", "5") + fld("Asistencia nuevos", "2") + "</div>"
            '<div class="sec-desc" style="margin-top:4px">Más de la reunión</div><div class="grid4">' + fld("Líderes servidores asistentes", "3") + fld("Conversiones", "1") + fld("Reconciliaciones", "0") + fld("Ausentes", "2") + "</div></div>"
            '<div class="card"><div class="sec-tit">Escuelas de Formación</div><div class="grid4">' + fld("Pasos de Vida", "2") + fld("Ciclo de Conexión", "1") + fld("Módulo de Liderazgo", "1") + fld("Seminario Bíblico", "0") + "</div>"
            '<div class="ayuda">Total de discípulos en escuelas: <b>4</b></div></div>'
            '<div class="card"><div class="sec-tit">Cultos</div><div class="grid2">' + fld("Asistencia VEA", "7") + fld("Asistencia dominical", "13") + "</div>"
            '<div class="ayuda">La asistencia del sábado solo la reportan las Áreas R21 y ZONAR21.</div></div>'
            '<div class="card"><div class="sec-tit">Informe financiero</div><div class="grid2">' + fld("Ofrenda (valor total)", "$ 185.000", ayuda="Son $185.000 · se registra también en Ofrendas.")
            + fld("Observaciones para el Supervisor", "", area=True) + "</div></div>"
            f'<div class="acciones">{btn("Revisar y enviar al Supervisor", "oro", "send", "lg")}{btn("Cancelar y volver sin enviar", "ghost")}</div>')


def modal_reporte():
    filas = [("Reunión", "Semana 48 (23/11 al 29/11)"), ("Asistentes", "15"), ("Asistencia niños", "5"), ("Asistencia nuevos", "2"),
             ("Asistencia dominical", "13"), ("Ofrenda", "$185.000")]
    lista = "".join(f"<div><span>{a}</span><b>{b}</b></div>" for a, b in filas)
    return ('<div class="velo"><div class="modal"><h3>Revisa antes de enviar</h3><div style="font-size:14px;opacity:.8">Se enviará a <b>Carlos Supervisor</b>. Después de enviarlo no se puede cambiar.</div>'
            f'<div class="lista">{lista}</div><div class="pie">{btn("Corregir algo", "sec")}{btn("Sí, enviar", "oro", "send")}</div></div></div>')


def p14():
    d = escritorio(side("Casas de Vida", M_EQUIPO, "Asistencia"), "Módulo Casas de Vida", *LIDER,
                   cab("Reporte de asistencia", "Casa Esperanza · Área Norte", btn("Volver", "sec", "arrow-left", "sm")) + form_reporte(), alto="largo")
    m = movil(*LIDER, '<h1>Reporte de asistencia</h1><p style="font-size:13px;margin:0 0 12px;opacity:.75">Casa Esperanza · Área Norte</p>' + form_reporte(True))
    return [("Escritorio · formulario lleno con datos ficticios", d, "z60"), ("Móvil · campos en dos columnas", m, "z52")]


def p14b():
    d = escritorio(side("Casas de Vida", M_EQUIPO, "Asistencia"), "Módulo Casas de Vida", *LIDER,
                   cab("Reporte de asistencia", "Casa Esperanza · Área Norte") + form_reporte(), modal_reporte())
    m = movil(*LIDER, '<h1>Reporte de asistencia</h1>' + form_reporte(True), modal_reporte().replace('class="modal"', 'class="modal" style="width:350px"'))
    return [("Escritorio · estado: confirmación antes de enviar", d, "z60"), ("Móvil", m, "z52")]


def p15():
    sec = lambda t, pares: f'<div class="card"><h2>{t}</h2><dl class="datos">' + "".join(f"<dt>{a}</dt><dd>{b}</dd>" for a, b in pares) + "</dl></div>"
    cuerpo = (alerta("Reporte de asistencia del 24/11/2026 enviado al Supervisor de Área.") +
              cab("Reporte de asistencia · Casa Esperanza", "Semana 48 · 23/11/2026 al 29/11/2026 · Enviado por María Líder",
                  btn("PDF", "sec", "file-earmark-pdf", "sm") + btn("Excel", "sec", "file-earmark-excel", "sm") + btn("Volver", "sec", "arrow-left", "sm")) +
              '<div class="grid2" style="gap:0 16px">' + sec("Asistencia", [("Asistentes", 15), ("Niños", 5), ("Nuevos", 2), ("Líderes servidores", 3), ("Conversiones", 1), ("Ausentes", 2)]) +
              "<div>" + sec("Asistencia Escuelas de Formación", [("Pasos de Vida", 2), ("Ciclo de Conexión", 1), ("Módulo de Liderazgo", 1), ("Total", 4)]) +
              sec("Cultos", [("VEA", 7), ("Dominical", 13)]) + "</div></div>" +
              '<div class="card"><h2>Informe financiero</h2><dl class="datos"><dt>Ofrenda</dt><dd>$185.000</dd></dl><div class="ayuda">' + ic("check-circle") + " Registrada en el módulo de Ofrendas.</div></div>")
    d = escritorio(side("Casas de Vida", M_EQUIPO, "Reportes"), "Módulo Casas de Vida", *LIDER, cuerpo, alto=True)
    return [("Escritorio · estado: confirmación después de enviar", d, "z74")]


def p16():
    filas = [("24/11/2026", "<b>Lucía Gómez</b>", "Llamada", "Se le invitó a la reunión del jueves.", "Pastor Demo", badge("Abierto", "pend"), btn("Editar", "out", "pencil", "sm")),
             ("18/11/2026", "<b>José Núñez</b>", "Visita", "Visita en casa con su familia.", "Pastor Demo", badge("En proceso", "neu"), btn("Editar", "out", "pencil", "sm")),
             ("02/11/2026", "<b>Ana María Pérez</b>", "Consejería", "Acompañamiento terminado.", "Pastor Demo", badge("Cerrado"), btn("Editar", "out", "pencil", "sm"))]
    cuerpo = (cab("Seguimiento de participantes", "Visitas, llamadas y consejerías a cada persona.", btn("Nuevo seguimiento", "pri", "plus-lg")) +
              '<div class="filtros">' + fld("Buscar", "Participante", ph=True) + fld("Tipo", "Todos", sel=True) + fld("Estado", "Todos", sel=True) + btn("Filtrar", "pri", "search") + "</div>" +
              tabla(["Fecha", "Participante", "Tipo", "Observaciones", "Responsable", "Estado", ""], filas))
    d = escritorio(side("Casas de Vida", M_PASTOR, "Seguimiento", True), "Módulo Casas de Vida", *PASTOR, cuerpo)
    form = pieza('<h3 class="sec" style="font-size:22px">Nuevo seguimiento</h3><div class="grid2">' + fld("Participante *", "Lucía Gómez", sel=True) + fld("Fecha *", "24/11/2026")
                 + fld("Tipo *", "Llamada", sel=True) + fld("Estado *", "Abierto", sel=True) + "</div>" + fld("Observaciones *", "Se le invitó a la reunión del jueves.", area=True)
                 + f'<div class="acciones">{btn("Guardar", "pri", "check-lg")}{btn("Cancelar", "sec")}</div>', 560)
    return [("Escritorio · lista (Pastor registra; Supervisor y Líder consultan)", d, "z60"), ("Formulario «Nuevo seguimiento»", form, "z52")]


def p17():
    cuerpo = (cab("Reportes", "Reportes semanales de tu Área y reportes generales al Pastor.", btn("Enviar reporte general al Pastor", "oro", "send")) +
              alerta("Tienes 3 reportes de Casas de Vida aún no incluidos en un reporte general.", "info", "info-circle") +
              '<div class="card"><h2>Mis reportes generales al Pastor</h2>' + tabla(["Mes", "Área", "Supervisor", "Enviado"], [("Octubre de 2026", "Norte", "Carlos Supervisor", "31/10/2026 18:02")]) + "</div>"
              '<div class="card"><h2>Reportes recibidos de las Casas de Vida</h2>' +
              tabla(["Semana", "Casa de Vida", "Envió", "Enviado", "Reporte general", ""],
                    [("16/11 – 22/11/2026", "Casa Esperanza", "María Líder", "17/11/2026 16:09", badge("Sin incluir", "pend"), btn("Ver", "sec", "eye", "sm")),
                     ("09/11 – 15/11/2026", "Casa Esperanza", "María Líder", "10/11/2026 11:57", badge("Sin incluir", "pend"), btn("Ver", "sec", "eye", "sm")),
                     ("26/10 – 01/11/2026", "Casa Esperanza", "María Líder", "27/10/2026 11:48", badge("Incluido"), btn("Ver", "sec", "eye", "sm"))]) + "</div>")
    d = escritorio(side("Casas de Vida", M_EQUIPO, "Reportes"), "Módulo Casas de Vida", *SUP, cuerpo)
    gen = pieza('<h3 class="sec" style="font-size:22px">Reporte general al Pastor</h3>' + fld("Mes", "Noviembre de 2026", sel=True,
                ayuda="Se incluyen los reportes semanales cuya semana empieza en el mes y que aún no van en otro reporte general.") +
                '<div class="sec-tit">Reportes de las Casas de Vida a incluir (2)</div>' +
                tabla(["Casa de Vida", "Fecha", "Asistentes", "Ofrenda"], [("Casa Esperanza", "17/11/2026", "15", "$185.000"), ("Casa Esperanza", "10/11/2026", "13", "$25.000")], der=(2, 3)) +
                '<div style="height:10px"></div>' + fld("Observaciones generales", "Casa Esperanza creció en asistencia; necesita apoyo con niños.", area=True) +
                btn("Enviar al Pastor", "oro", "send"), 600)
    return [("Escritorio · Supervisor", d, "z60"), ("Envío del reporte general del mes", gen, "z52")]


def p18():
    cuerpo = (cab("Generar reporte", "", btn("Volver", "sec", "arrow-left", "sm")) +
              '<div class="filtros">' + fld("Periodo", "Mensual", sel=True) + fld("Fecha de referencia", "17/11/2026") + fld("Área", "Todas", sel=True) + fld("Casa de Vida", "Todas", sel=True) + btn("Generar", "pri", "bar-chart") + "</div>"
              '<div class="cab" style="border:0;margin-bottom:8px;padding:0"><div><h1 style="font-size:24px">Noviembre de 2026</h1><p>Del 01/11/2026 al 30/11/2026 · Reportes semanales esperados por casa: 4</p></div>'
              f'<div class="acciones">{btn("PDF", "sec", "file-earmark-pdf", "sm")}{btn("Excel", "sec", "file-earmark-excel", "sm")}</div></div>' +
              stats([("Reuniones reportadas", 2, "calendar-check"), ("Asistentes", 28, "people"), ("Nuevos", 3, "person-plus"), ("Ofrenda", "$210.000", "cash-coin")]) +
              tabla(["Área", "Casa de Vida", "Reuniones", "Asistentes", "Niños", "Nuevos", "Dominical", "Ofrenda", "Reportes enviados"],
                    [("Norte", "Casa Esperanza", "2", "28", "9", "3", "25", "$210.000", "2 de 4"), ("Sur", "Casa Fe", "0", "0", "0", "0", "0", "$0", badge("0 de 4", "pend")),
                     ("__total__", ("Total", "", "2", "28", "9", "3", "25", "$210.000", "2 de 8"))], der=(2, 3, 4, 5, 6, 7)))
    d = escritorio(side("Casas de Vida", M_PASTOR, "Reportes", True), "Módulo Casas de Vida", *PASTOR, cuerpo)
    return [("Escritorio · Pastor", d, "z74")]


def p19():
    cuerpo = (cab("Ofrendas", "Registro y consulta de ofrendas de la iglesia.", btn("PDF", "sec", "file-earmark-pdf", "sm") + btn("Excel", "sec", "file-earmark-excel", "sm") + btn("Registrar ofrenda", "pri", "plus-lg")) +
              '<div class="filtros">' + fld("Concepto", "Todos", ph=True) + fld("Desde", "01/11/2026") + fld("Hasta", "30/11/2026") + fld("Casa de Vida", "Todas", sel=True) + btn("Filtrar", "pri", "search") + "</div>" +
              '<div class="stats" style="grid-template-columns:1fr 1fr 2fr">' + '<div class="stat"><div><div class="et">Total</div><div class="num">$715.500</div></div></div><div class="stat"><div><div class="et">Registros</div><div class="num">3</div></div></div><div></div></div>' +
              tabla(["Fecha", "Concepto", "Casa de Vida", "Valor", "Registró", "Observaciones", ""],
                    [("17/11/2026", "Ofrenda Casa de Vida", "Casa Esperanza", "$185.000", "María Líder", "Registrada desde el reporte de asistencia", btn("Editar", "out", "pencil", "sm")),
                     ("10/11/2026", "Ofrenda culto dominical", "General", "$450.000", "Pastor Demo", "—", btn("Editar", "out", "pencil", "sm")),
                     ("03/11/2026", "Ofrenda especial de misiones", "General", "$80.500", "Pastor Demo", "—", btn("Editar", "out", "pencil", "sm"))], der=(3,)))
    d = escritorio(side("Casas de Vida", M_PASTOR, "Ofrendas", True), "Módulo Casas de Vida", *PASTOR, cuerpo)
    form = pieza('<h3 class="sec" style="font-size:22px">Registrar ofrenda</h3><div class="grid2">' + fld("Fecha *", "24/11/2026") + fld("Concepto *", "Ofrenda culto dominical")
                 + fld("Valor (COP) *", "450.000") + fld("Casa de Vida", "General (sin Casa)", sel=True) + "</div>" + fld("Observaciones", "", area=True)
                 + f'<div class="acciones">{btn("Guardar", "pri", "check-lg")}{btn("Cancelar", "sec")}</div>', 560)
    return [("Escritorio · Pastor o responsable de ofrendas", d, "z60"), ("Formulario «Registrar ofrenda»", form, "z52")]


def p20():
    cuerpo = ('<div class="cab"><div><h1>Hola, Laura Coordinadora</h1></div></div><p style="margin:0 0 12px;opacity:.75">Resumen del módulo de Escuelas de Formación.</p>' +
              stats([("Procesos activos", 2, "mortarboard"), ("Inscritos", 3, "people"), ("Asistencia promedio", "67%", "graph-up"), ("Seguimientos abiertos", 0, "clipboard-check")]) +
              '<div class="fila"><div class="card" style="flex:1.3"><h2>Procesos de formación</h2>' +
              tabla(["Proceso", "Escuela", "Estado"], [("Escuela Vida Nivel 1 – 2026", "Escuelas Vida", badge("Activo")), ("Pasos de Vida – 2026", "Pasos de Vida", badge("Activo"))]) +
              '</div><div class="card"><h2>Últimas actividades</h2>' + tabla(["Proceso", "Fecha", "Asistentes"], [("Escuela Vida Nivel 1", "20/11/2026", "2 de 3")]) + "</div></div>")
    d = escritorio(side("Escuelas de Formación", M_FORM, "Inicio"), "Módulo Escuelas de Formación", *COORD, cuerpo)
    return [("Escritorio · Coordinador", d, "z74")]


def p21():
    cuerpo = (cab("Escuela Vida Nivel 1 – 2026", "Escuelas Vida · Coordina Laura Coordinadora · " + badge("Activo"), btn("Volver", "sec", "arrow-left", "sm") + btn("Editar", "out", "pencil", "sm")) +
              '<div class="fila"><div class="card" style="flex:1.3"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px"><h2 style="margin:0">Participantes inscritos</h2>'
              f'<span class="acciones">{btn("Inscribir existente", "sec", "person-check", "sm")}{btn("Nuevo participante", "pri", "person-plus", "sm")}</span></div>' +
              tabla(["Nombre", "Inscripción", "Estado", ""], [("Ana María Pérez", "02/02/2026", badge("Inscrito"), btn("Retirar", "dan", None, "sm")),
                                                              ("José Núñez", "02/02/2026", badge("Inscrito"), btn("Retirar", "dan", None, "sm")),
                                                              ("Lucía Gómez", "09/02/2026", badge("Inscrito"), btn("Retirar", "dan", None, "sm"))]) +
              '</div><div class="card"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px"><h2 style="margin:0">Seguimiento reciente</h2>' + btn("Nuevo seguimiento", "sec", "plus-lg", "sm") + "</div>"
              '<div class="vacio" style="padding:18px"><b style="font-size:14px">Sin seguimientos todavía.</b></div></div></div>'
              '<div class="card"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px"><h2 style="margin:0">Actividades y asistencia</h2>' + btn("Registrar actividad", "pri", "calendar-plus", "sm") + "</div>" +
              tabla(["Fecha", "Actividad", "Presentes", "Registró"], [("20/11/2026", "Clase 3: La oración", "2 de 3", "Laura Coordinadora"), ("13/11/2026", "Clase 2: La Palabra", "3 de 3", "Laura Coordinadora")]) + "</div>")
    d = escritorio(side("Escuelas de Formación", M_FORM, "Procesos de formación"), "Módulo Escuelas de Formación", *COORD, cuerpo, alto=True)
    return [("Escritorio · Coordinador", d, "z74")]


def p22():
    marc = "".join(check(n, s) for n, s in [("Ana María Pérez", True), ("José Núñez", False), ("Lucía Gómez", True)])
    cuerpo = (cab("Registrar actividad y asistencia", "Escuela Vida Nivel 1 – 2026", btn("Volver", "sec", "arrow-left", "sm")) +
              '<div class="card" style="max-width:860px"><div class="grid2">' + fld("Nombre de la actividad *", "Clase 3: La oración") + fld("Fecha *", "20/11/2026") + "</div>"
              + fld("Descripción", "", area=True) +
              '<div style="display:flex;justify-content:space-between;align-items:center;margin:4px 0 10px"><b style="font-size:14px">Marca los inscritos presentes (3):</b>'
              f'<span class="acciones">{btn("Marcar todos", "ghost")}{btn("Desmarcar todos", "ghost")}</span></div>' + marc +
              f'<div class="acciones" style="margin-top:6px">{btn("Guardar", "pri", "check-lg")}{btn("Cancelar", "sec")}</div></div>')
    d = escritorio(side("Escuelas de Formación", M_FORM, "Procesos de formación"), "Módulo Escuelas de Formación", *COORD, cuerpo)
    ok = pieza(alerta("Actividad registrada: 2 de 3 presentes."), 520)
    return [("Escritorio", d, "z60"), ("Estado: confirmación", ok, "z52")]


def p23():
    cuerpo = (cab("Nuevo participante", "", btn("Volver", "sec", "arrow-left", "sm")) +
              alerta("¿Ya está registrado? Inscríbelo desde «Inscribir existente».", "info", "info-circle") +
              '<div class="card" style="max-width:900px"><div class="grid2">' + fld("Nombres y apellidos *", "Sandra Ruiz Pérez") + fld("Documento de identidad *", "", cls="mal", err="Este campo es obligatorio.")
              + fld("Fecha de nacimiento *", "14/03/1998") + fld("Teléfono de contacto *", "300 555 0101") + "</div>" + fld("Dirección *", "Carrera 26 # 31-40, Girón")
              + check("Autoriza el tratamiento de sus datos personales (Ley 1581 de 2012) *", True)
              + '<div class="ayuda" style="margin:-6px 0 12px">Si es menor de edad, la autorización la otorga su representante legal.</div>'
              + '<div class="grid2">' + fld("Proceso de formación *", "Escuela Vida Nivel 1 – 2026", sel=True) + "</div>"
              f'<div class="acciones">{btn("Guardar", "pri", "check-lg")}{btn("Cancelar", "sec")}</div></div>')
    d = escritorio(side("Escuelas de Formación", M_FORM, "Participantes"), "Módulo Escuelas de Formación", *COORD, cuerpo, alto=True)
    return [("Escritorio · estado: validación de campo obligatorio", d, "z74")]


def p24():
    cuerpo = (cab("Reportes de formación") +
              '<div class="filtros">' + fld("Periodo", "Mensual", sel=True) + fld("Fecha de referencia", "24/11/2026") + fld("Escuela", "Todas", sel=True) + fld("Proceso", "Todos", sel=True) + btn("Generar", "pri", "bar-chart") + "</div>"
              '<div class="cab" style="border:0;margin-bottom:8px;padding:0"><div><h1 style="font-size:24px">Diciembre de 2026</h1><p>Del 01/12/2026 al 31/12/2026</p></div>'
              f'<div class="acciones">{btn("PDF", "sec", "file-earmark-pdf", "sm")}{btn("Excel", "sec", "file-earmark-excel", "sm")}</div></div>' +
              alerta("No hay información registrada en este periodo con los filtros elegidos.", "info", "info-circle") +
              stats([("Actividades", 0, "calendar-check"), ("Asistencia", "—", "graph-up"), ("Inscritos activos", 3, "people"), ("Nuevos inscritos", 0, "person-plus")]) +
              tabla(["Escuela", "Proceso", "Actividades", "Presentes", "Asistencia", "Inscritos", "Nuevos", "Seguimientos"],
                    [("Escuelas Vida", "Escuela Vida Nivel 1 – 2026", "0", "0", "—", "3", "0", "0"), ("Pasos de Vida", "Pasos de Vida – 2026", "0", "0", "—", "0", "0", "0")], der=(2, 3, 4, 5, 6, 7)))
    d = escritorio(side("Escuelas de Formación", M_FORM, "Reportes"), "Módulo Escuelas de Formación", *COORD, cuerpo)
    return [("Escritorio · estado: periodo sin datos", d, "z74")]


def perfil_cuerpo(err=False, ok=False):
    e = dict(cls="mal", err="Escribe tu nombre completo.") if err else {}
    return (cab("Mi perfil") + (alerta("Nombre actualizado.") if ok else "") + '<div class="card" style="max-width:560px">' +
            fld("Nombre completo", "" if err else "María Líder", **e) + fld("Rol", "Líder de Casa de Vida", cls="dis") + fld("Módulo", "Casas de Vida", cls="dis") +
            f'<div class="acciones">{btn("Guardar cambios", "pri")}{btn("Cambiar contraseña", "sec", "key")}</div></div>')


def p25():
    d = escritorio(side("Casas de Vida", M_EQUIPO, "Mi perfil"), "Módulo Casas de Vida", *LIDER, perfil_cuerpo(ok=True))
    osc = escritorio(side("Casas de Vida", M_EQUIPO, "Mi perfil"), "Módulo Casas de Vida", *LIDER, perfil_cuerpo(err=True)).replace('class="pantalla"', 'class="pantalla oscuro"', 1)
    return [("Escritorio · tema claro · confirmación", d, "z60"), ("Modo oscuro · validación", osc, "z52")]


# ======================================================================
# Inventario: id, nombre, roles, propósito, flujo, función, variantes
# ======================================================================
FLUJOS = {
    "A": "A · Acceso",
    "B": "B · Administración de cuentas",
    "C": "C · Casas de Vida: organización (Pastor)",
    "D": "D · Casas de Vida: reunión semanal (Líder y apoyo)",
    "E": "E · Seguimiento, reportes y ofrendas",
    "F": "F · Escuelas de Formación",
    "G": "G · Cuenta personal",
}
INVENTARIO = [
    ("P01", "Página pública", "Visitante (sin sesión)", "Conocer la iglesia y el PVA y entrar a la plataforma.", "A", p01, "Escritorio, móvil"),
    ("P02", "Iniciar sesión", "Todos los roles", "Entrar con correo o usuario y contraseña.", "A", p02, "Escritorio, móvil, error de credenciales"),
    ("P03", "Recuperar contraseña", "Todos los roles", "Pedir un enlace para crear una contraseña nueva.", "A", p03, "Solicitud, enlace enviado"),
    ("P04", "Selector de módulo", "Pastor, Super Administrador", "Elegir Casas de Vida o Escuelas de Formación.", "A", p04, "Escritorio"),
    ("P05", "Gestión de usuarios", "Super Administrador, Pastor", "Consultar, editar, desactivar o reactivar cuentas.", "B", p05, "Confirmación después de guardar"),
    ("P06", "Crear usuario", "Super Administrador, Pastor", "Crear una cuenta con rol, asignación y contraseña.", "B", p06, "Validación del formulario"),
    ("P07", "Bitácora de auditoría", "Super Administrador", "Ver quién hizo qué y cuándo; exportar.", "B", p07, "Escritorio"),
    ("P08", "Panel de Casas de Vida", "Pastor, Supervisor, Líder, Apoyo", "Ver el resumen y la siguiente tarea de la semana.", "C", None, "Líder (escritorio, móvil, menú), Pastor, aviso enviado"),
    ("P09", "Casas de Vida", "Pastor (gestiona); Supervisor y Líder (consultan)", "Listar, ver, editar o desactivar Casas de Vida.", "C", p09, "Listado vacío"),
    ("P10", "Nueva Casa de Vida", "Pastor", "Crear una Casa de Vida en un Área.", "C", p10, "Confirmación"),
    ("P11", "Importar datos", "Pastor", "Cargar Casas de Vida o participantes desde Excel/CSV.", "C", p11, "Vista previa con errores"),
    ("P12", "Personas nuevas", "Pastor, Supervisor, Líder, Apoyo", "Consultar a quienes llegan por primera vez.", "D", p12, "Escritorio, móvil, sin resultados"),
    ("P13", "Registrar persona nueva", "Líder, Apoyo", "Tomar nombre y teléfono de quien llega.", "D", p13, "Escritorio, móvil con validación, confirmación"),
    ("P14", "Reporte de asistencia", "Líder, Apoyo", "Llenar los totales de la reunión semanal.", "D", None, "Escritorio, móvil, confirmación antes de enviar"),
    ("P15", "Detalle del reporte", "Pastor, Supervisor, Líder, Apoyo", "Ver un reporte enviado y exportarlo.", "D", p15, "Confirmación después de enviar"),
    ("P16", "Seguimiento", "Pastor (registra); Supervisor y Líder (consultan)", "Registrar y consultar visitas, llamadas y consejerías.", "E", p16, "Lista y formulario"),
    ("P17", "Reportes del Supervisor", "Supervisor de Área", "Revisar reportes semanales y enviar el general del mes.", "E", p17, "Lista y envío del reporte general"),
    ("P18", "Generar reporte", "Pastor", "Consolidar por periodo, Área o Casa; exportar.", "E", p18, "Escritorio"),
    ("P19", "Ofrendas", "Pastor, responsable de ofrendas", "Registrar y consultar ofrendas.", "E", p19, "Lista y formulario"),
    ("P20", "Panel de Formación", "Coordinador de Formación, Pastor", "Ver el resumen de procesos y actividades.", "F", p20, "Escritorio"),
    ("P21", "Detalle del proceso", "Coordinador de Formación, Pastor", "Gestionar inscritos, seguimiento y actividades.", "F", p21, "Escritorio"),
    ("P22", "Registrar actividad y asistencia", "Coordinador de Formación, Pastor", "Registrar una clase y marcar presentes.", "F", p22, "Confirmación"),
    ("P23", "Nuevo participante", "Coordinador de Formación, Pastor", "Registrar e inscribir a un participante.", "F", p23, "Validación de campo obligatorio"),
    ("P24", "Reportes de formación", "Coordinador de Formación, Pastor", "Consultar asistencia e inscritos por periodo.", "F", p24, "Periodo sin datos"),
    ("P25", "Mi perfil", "Todos los roles con sesión", "Corregir el nombre y cambiar la contraseña.", "G", p25, "Confirmación, modo oscuro con validación"),
]
# Pantallas con dos láminas
LAMINAS_EXTRA = {"P08": [p08, p08b, p08c], "P14": [p14, p14b]}

NOTAS = {
    "P02": "Tras 5 intentos fallidos la cuenta se bloquea 15 minutos y se muestra el mismo mensaje genérico.",
    "P05": "El Pastor ve la misma lista sin el menú «Auditoría».",
    "P08": "Pastor y Super Administrador ven además «Cambiar de módulo». El Supervisor ve el mismo panel limitado a su Área.",
    "P12": "En el teléfono la tabla pasa a tarjetas (tabla-apilada de la plataforma). Solo el Pastor ve «Editar» y «Desactivar».",
    "P14": "En escritorio se muestra la página completa (se desplaza). El reporte no se guarda como borrador. Si todos los valores están en 0, la ventana pregunta «¿Seguro que la reunión fue así?».",
    "P16": "En Casas de Vida solo el Pastor registra y edita seguimientos.",
    "P19": "La ofrenda escrita en el reporte semanal se registra sola en este módulo.",
    "P25": "El modo oscuro usa los tokens [data-theme=\"dark\"] de styles.css.",
}


# ======================================================================
# Ensamblado
# ======================================================================
ANCHO_UTIL, ALTO_UTIL, HUECO = 950, 585, 26


def medidas(html):
    """Tamaño base (px virtuales) de un marco según su tipo."""
    if html.startswith('<div class="escritorio largo'):
        return 1200, 1560
    if html.startswith('<div class="escritorio alto'):
        return 1200, 980
    if html.startswith('<div class="escritorio'):
        return 1200, 760
    if html.startswith('<div class="movil'):
        return 390, 800
    m = re.search(r"width:(\d+)px", html[:120])
    return (int(m.group(1)) if m else 560), 360


def lamina(ident, nombre, rol, flujo, prop, variante, marcos, nota, tipo):
    """Coloca los marcos en fila (o el primero a la izquierda y el resto apilados) y los escala para que quepan."""
    base = []
    for cap, html, z in marcos:
        w, h = medidas(html)
        zz = int(z[1:]) / 100
        base.append((cap, html, w * zz, h * zz, zz))
    if len(base) >= 3:
        ancho = base[0][2] + max(b[2] for b in base[1:]) + HUECO
        alto = max(base[0][3], sum(b[3] + 30 for b in base[1:]))
    else:
        ancho = sum(b[2] for b in base) + HUECO * (len(base) - 1)
        alto = max(b[3] for b in base)
    f = min(1, ANCHO_UTIL / ancho, ALTO_UTIL / alto)

    def marco(b):
        cap, html, _w, _h, zz = b
        return f'<div class="marco-wrap"><div style="zoom:{zz * f:.3f}">{html}</div><div class="marco-cap">{cap}</div></div>'

    if len(base) >= 3:
        cuerpo = marco(base[0]) + '<div class="col-apilada">' + "".join(marco(b) for b in base[1:]) + "</div>"
    else:
        cuerpo = "".join(marco(b) for b in base)
    n = f'<div class="nota-lam"><b>Nota.</b> {nota}</div>' if nota else ""
    return (f'<section class="hoja" id="{ident}"><div class="lam-cab"><h2 class="lam-id">{ident} · {nombre}</h2>'
            f'<div class="lam-meta"><span><b>Rol:</b>{rol}</span><span><b>Flujo:</b>{FLUJOS[flujo]}</span><span><b>Propósito:</b>{prop}</span></div>'
            f'<span class="lam-var">{variante}</span></div><div class="lam-cuerpo">{cuerpo}</div>{n}'
            f'<div class="doc-pie"><span>{tipo} – {TITULO_PROYECTO}</span><span>{ident}</span></div></section>')


def portada(tipo, sub):
    return (f'<section class="hoja portada"><div class="p-banda"><p class="p-kicker">{"Baja fidelidad" if tipo == "Wireframes" else "Alta fidelidad"} · Diseño de interfaz</p>'
            f'<h1>{tipo} – {TITULO_PROYECTO}</h1><p class="p-sub">{sub}</p></div>'
            f'<div class="p-datos"><div><b>Versión</b>{VERSION}</div><div><b>Fecha</b>24 de noviembre de 2026</div>'
            '<div><b>Autores</b>Joshua David Tarazona Gómez · Karen Lizeth Arenas Medina</div><div><b>Pantallas</b>25 (P01–P25), 7 flujos, escritorio y móvil</div></div></section>')


def inventario(tipo):
    paginas = [("A", "B", "C", "D"), ("E", "F", "G")]
    salida = ""
    for k, flujos in enumerate(paginas):
        filas, actual = "", None
        for ident, nombre, rol, prop, flujo, _f, var in INVENTARIO:
            if flujo not in flujos:
                continue
            if flujo != actual:
                filas += f'<tr class="flujo"><td colspan="5">{FLUJOS[flujo]}</td></tr>'
                actual = flujo
            filas += f"<tr><td>{ident}</td><td><b>{nombre}</b></td><td>{rol}</td><td>{prop}</td><td>{var}</td></tr>"
        intro = ('<p class="doc-intro">Mismos nombres, identificadores y orden en los wireframes y en los mockups. '
                 'Los roles y las acciones corresponden a la versión implementada (revisada en la demostración y en el código).</p>') if k == 0 else ""
        cont = " (continuación)" if k else ""
        salida += (f'<section class="hoja"><h2 class="doc-h2">Inventario de pantallas{cont}</h2>{intro}'
                   f'<table class="inv"><thead><tr><th>ID</th><th>Pantalla</th><th>Rol que accede</th><th>Propósito</th><th>Variantes y estados</th></tr></thead><tbody>{filas}</tbody></table>'
                   f'<div class="doc-pie"><span>{tipo} – {TITULO_PROYECTO}</span><span>Inventario {k + 1}/2</span></div></section>')
    return salida


def pagina_guia(tipo):
    if tipo == "Wireframes":
        ej = lambda e, t: f'<div><div class="ej">{e}</div>{t}</div>'
        return ('<section class="hoja"><h2 class="doc-h2">Convenciones de los wireframes</h2><p class="doc-intro">Escala de grises sin fotos ni tipografía de marca. '
                'Los textos son los reales de la plataforma; los datos son ficticios. Cada forma representa un control que conserva su lugar en el mockup.</p><div class="conv">'
                + ej(btn("Acción principal", "pri"), "Botón principal (verde en el mockup).")
                + ej(btn("Acción destacada", "oro"), "Botón destacado del flujo (dorado en el mockup).")
                + ej(btn("Secundaria", "sec") + btn("Desactivar", "dan", None, "sm"), "Secundaria y acción que retira (borde discontinuo).")
                + ej(badge("Activo") + badge("Pendiente", "pend"), "Estado: borde continuo = normal; discontinuo = requiere atención.")
                + ej(f'<div class="inp" style="width:100%"><span>Valor</span></div>', "Campo de formulario con su etiqueta encima.")
                + ej(f'<div class="inp mal" style="width:100%"><span>Valor</span></div>', "Campo con error: borde discontinuo grueso + mensaje con icono.")
                + ej(f'<div class="foto" style="width:100%;height:40px"></div>', "Imagen o fotografía (caja cruzada).")
                + ej(ic("house") + " " + ic("people") + " " + ic("check2-square"), "Icono (cuadro gris). En el mockup: Bootstrap Icons 1.11.3.")
                + "</div>" + f'<div class="doc-pie"><span>{tipo} – {TITULO_PROYECTO}</span><span>Convenciones</span></div></section>')
    sw = lambda c, n, h, txt="#fff": f'<div class="muestra"><div class="c" style="background:{h}"></div><div class="t"><b>{n}</b><br><code>{h}</code></div></div>'
    return ('<section class="hoja"><h2 class="doc-h2">Identidad visual aplicada</h2><p class="doc-intro">Valores tomados de <code>ccmg/frontend/static/css/styles.css</code> (no son aproximados). '
            'Tema principal: claro. El modo oscuro se muestra en P25.</p><div class="muestras">'
            + sw(1, "Verde principal", "#00674F") + sw(1, "Verde oscuro", "#004d3b") + sw(1, "Oro", "#CBB279") + sw(1, "Arena (fondo)", "#F4F5F2")
            + sw(1, "Carbón (texto)", "#2B2D2F") + sw(1, "Texto suave", "#6B706E") + sw(1, "Borde", "#E3E5E0") + sw(1, "Oro para texto", "#8a7439")
            + sw(1, "Oscuro · fondo", "#0F1714") + sw(1, "Oscuro · superficie", "#17221E") + sw(1, "Oscuro · título", "#5CC9A7") + sw(1, "Oscuro · texto", "#E3E9E6")
            + '</div><div class="fila" style="gap:8mm;font-size:9pt"><div><div class="sec-tit" style="color:#00674F">Tipografía</div>'
            '<div style="font-family:Fraunces,serif;font-size:24pt;color:#00674F;line-height:1.1">Fraunces</div><div>Títulos de página, tarjetas y marca (600–700).</div>'
            '<div style="font-family:Figtree,sans-serif;font-size:20pt;margin-top:3mm">Figtree</div><div>Interfaz, formularios y tablas (400–800).</div></div>'
            '<div><div class="sec-tit" style="color:#00674F">Componentes</div><div class="acciones" style="margin-bottom:3mm">'
            + btn("Guardar", "pri", "check-lg") + btn("Llenar reporte", "oro") + btn("Cancelar", "sec") + btn("Desactivar", "dan", "slash-circle", "sm") + "</div>"
            + '<div class="acciones" style="margin-bottom:3mm">' + badge("Activo") + badge("Autorización pendiente", "pend") + badge("Inactivo", "neu") + badge("Falta el nombre", "err") + "</div>"
            + '<div style="max-width:120mm">' + alerta("Usuario creado correctamente.") + "</div></div>"
            '<div><div class="sec-tit" style="color:#00674F">Forma y ritmo</div><div>Radio de tarjetas 14 px y de controles 10 px.<br>Sombra suave de tarjeta.<br>Menú lateral verde con degradado y marca en oro claro.<br>Iconos: Bootstrap Icons 1.11.3.</div></div></div>'
            f'<div class="doc-pie"><span>{tipo} – {TITULO_PROYECTO}</span><span>Identidad visual</span></div></section>')


def cierre(tipo):
    return ('<section class="hoja"><h2 class="doc-h2">Revisión final y puntos por confirmar</h2><div class="fila" style="gap:9mm;font-size:9pt;line-height:1.5"><div>'
            '<div class="sec-tit">Comprobado</div><ul style="padding-left:5mm;margin:0">'
            '<li>Las 25 pantallas del inventario tienen wireframe y mockup con la misma estructura (ambos se generan del mismo HTML).</li>'
            '<li>Nombres de módulos, menús, botones, campos y mensajes tomados de la demostración y del código.</li>'
            '<li>Acciones según el rol: por ejemplo, solo el Pastor registra seguimientos en Casas de Vida, solo el Líder y el apoyo llenan el reporte y registran personas nuevas, y solo el Super Administrador ve «Auditoría».</li>'
            '<li>Variantes móviles de los flujos principales: página pública, inicio de sesión, panel con menú, lista en tarjetas y formularios.</li>'
            '<li>Estados: listado vacío, sin resultados, validación, vista previa con errores, confirmación antes de enviar y después de guardar, periodo sin datos y modo oscuro.</li>'
            '<li>Los estados se entienden por texto e icono, no solo por color.</li></ul></div><div>'
            '<div class="sec-tit">Por confirmar</div><ul style="padding-left:5mm;margin:0">'
            '<li><b>Por confirmar:</b> texto de las tarjetas inferiores de la página pública (P01); se resumió el contenido real.</li>'
            '<li><b>Por confirmar:</b> en P11 los mensajes de error por fila (por ejemplo, «Teléfono no válido») son ilustrativos; los reales dependen del archivo.</li>'
            '<li><b>Por confirmar:</b> el contenido exacto del resumen de la ventana de P14 (qué campos lista); se muestran los principales.</li>'
            '<li>Formato editable: este conjunto se entrega como HTML generado por <code>generar.py</code>. Figma necesita autorización en esta sesión y no se usó.</li></ul></div></div>'
            f'<div class="doc-pie"><span>{tipo} – {TITULO_PROYECTO}</span><span>Cierre</span></div></section>')


def documento(tipo, hoja_estilo, sub):
    laminas = []
    for ident, nombre, rol, prop, flujo, func, var in INVENTARIO:
        for k, f in enumerate(LAMINAS_EXTRA.get(ident, [func])):
            marcos = f()
            variante = marcos[0][0] if ident in LAMINAS_EXTRA else var
            laminas.append(lamina(ident, nombre, rol, flujo, prop, variante, marcos, NOTAS.get(ident) if k == 0 else None, tipo))
    fuentes = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
               '<link href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600;700;800&family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&display=swap" rel="stylesheet">'
               '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">') if tipo == "Mockups" else ""
    return (f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>{tipo} – PVA CCMG Girón</title>{fuentes}'
            f'<link rel="stylesheet" href="estructura.css"><link rel="stylesheet" href="{hoja_estilo}"></head><body>'
            + portada(tipo, sub) + inventario(tipo) + pagina_guia(tipo) + "".join(laminas) + cierre(tipo) + "</body></html>")


if __name__ == "__main__":
    (AQUI / "Wireframes_PVA.html").write_text(documento("Wireframes", "wireframe.css",
        "Estructura de cada pantalla en escala de grises: navegación, jerarquía de la información y ubicación de formularios, tablas y botones, por rol y por flujo."), encoding="utf-8")
    (AQUI / "Mockups_PVA.html").write_text(documento("Mockups", "mockup.css",
        "La misma estructura de los wireframes con la identidad real de la plataforma: paleta, tipografía Fraunces y Figtree, Bootstrap Icons y componentes."), encoding="utf-8")
    print("Generados Wireframes_PVA.html y Mockups_PVA.html")
