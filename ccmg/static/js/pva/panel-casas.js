/* =====================================================================
   CCMG PVA · Panel del módulo CASAS DE VIDA
   Roles con acceso: pastor, supervisor, lider, apoyo
   Corresponde a los RF de Casas de Vida, participantes, asistencia,
   seguimiento, ofrendas y reportes.
   ===================================================================== */

/* ---------------------------------------------------------------------
   Datos del módulo.
   Sin registros de demostración: lo que se muestre debe venir de la base
   de datos o de lo que registre el usuario.
   --------------------------------------------------------------------- */
const CASAS = [];
const PARTICIPANTES = [];
const ACTIVIDADES = [];
const SEGUIMIENTOS = [];
const OFRENDAS = [];
const REPORTES = [];

/* Resumen y rutas calculados en el servidor según el alcance del rol (pva.views.panel_casas) */
function leerJSON(id, porDefecto) {
  const el = document.getElementById(id);
  try { return el ? JSON.parse(el.textContent) : porDefecto; } catch (e) { return porDefecto; }
}
const RESUMEN = leerJSON('pva-resumen', { participantes: 0, casas: 0, casasActivas: 0, asistenciaPromedio: 0, actividades: [] });
const URLS_PVA = leerJSON('pva-urls', {});

let siguienteId = 100;
function nuevoId() { return ++siguienteId; }

function opcionesCasas(seleccionada) {
  if (!CASAS.length) {
    return '<option value="">Sin casas de vida registradas</option>';
  }
  return CASAS.map(function (c) {
    return '<option' + (c.nombre === seleccionada ? ' selected' : '') + '>' + esc(c.nombre) + '</option>';
  }).join('');
}

function opcionesParticipantes() {
  if (!PARTICIPANTES.length) {
    return '<option value="">Sin participantes registrados</option>';
  }
  return PARTICIPANTES.map(function (p) {
    return '<option>' + esc(p.nombre) + '</option>';
  }).join('');
}

function dinero(n) {
  return '$' + Number(n).toLocaleString('es-CO');
}

/* --------------------------- Acciones --------------------------- */
function guardarSeguimiento(ev) {
  ev.preventDefault();
  const f = ev.target;
  SEGUIMIENTOS.push({
    id: nuevoId(),
    participante: f.participante.value,
    casa: f.casa.value,
    tipo: f.tipo.value,
    fecha: f.fecha.value,
    responsable: f.responsable.value.trim(),
    observacion: f.observacion.value.trim(),
    estado: 'En proceso'
  });
  avisar('Seguimiento registrado.');
  refrescar();
  return false;
}

function guardarOfrenda(ev) {
  ev.preventDefault();
  const f = ev.target;
  OFRENDAS.push({
    id: nuevoId(),
    fecha: f.fecha.value,
    casa: f.casa.value,
    concepto: f.concepto.value.trim(),
    valor: Number(f.valor.value),
    metodo: f.metodo.value
  });
  avisar('Ofrenda registrada.');
  refrescar();
  return false;
}

function enviarReporte(ev) {
  ev.preventDefault();
  const f = ev.target;
  REPORTES.unshift({
    id: nuevoId(),
    periodo: f.periodo.value,
    casa: f.casa.value,
    enviado: hoyISO(),
    estado: 'Enviado'
  });
  avisar('Reporte enviado al Pastor.');
  refrescar();
  return false;
}

/* ----------------------------- Vistas ----------------------------- */
const VISTAS_CASAS = {

  inicio: function (s) {
    const pendientes = SEGUIMIENTOS.filter(function (x) { return x.estado !== 'Cerrado'; }).length;

    return titulo('Hola, ' + esc(s.nombre),
      '<span class="modulo-tag"><i class="bi bi-houses"></i> Módulo Casas de Vida</span>') +
      '<p class="text-muted">Resumen del módulo de Casas de Vida.</p>' +
      '<div class="row g-3">' +
      stat('Participantes', RESUMEN.participantes, 'people') +
      stat('Casas de Vida', RESUMEN.casas + ' <small class="text-muted fs-6">(' + RESUMEN.casasActivas + ' activas)</small>', 'houses') +
      stat('Asistencia promedio', RESUMEN.asistenciaPromedio + '%', 'graph-up') +
      stat('Seguimientos abiertos', pendientes, 'clipboard-check') +
      '</div>' +
      '<div class="row g-3 mt-1">' +
      '<div class="col-lg-7"><div class="card p-3 border-0 shadow-sm h-100">' +
      '<div class="d-flex justify-content-between align-items-center mb-3"><h6 class="m-0">Últimas actividades registradas</h6>' +
      (URLS_PVA.asistencia ? '<a class="small text-decoration-none" href="' + URLS_PVA.asistencia + '">Ver asistencia</a>' : '') + '</div>' +
      tabla(['Casa de Vida', 'Fecha', 'Actividad', 'Asistentes'], RESUMEN.actividades.map(function (a) {
        return [esc(a.casa), esc(a.fecha), esc(a.tipo), a.asistentes];
      })) +
      '</div></div>' +
      '<div class="col-lg-5"><div class="card p-3 border-0 shadow-sm h-100">' +
      '<h6 class="mb-3">Seguimientos recientes</h6>' +
      tabla(['Participante', 'Estado'], SEGUIMIENTOS.slice(0, 4).map(function (x) {
        const tipo = x.estado === 'Cerrado' ? 'ok' : (x.estado === 'Pendiente' ? 'pendiente' : 'info');
        return [esc(x.participante), badge(x.estado, tipo)];
      })) +
      '</div></div>' +
      '</div>';
  },

  seguimiento: function (s) {
    return titulo('Seguimiento',
      '<button class="btn btn-ccmg btn-sm" onclick="return mostrarFormulario(\'formSeguimiento\')">' +
      '<i class="bi bi-plus-lg me-1"></i>Nuevo seguimiento</button>') +
      '<div id="formSeguimiento" class="card p-3 border-0 shadow-sm mb-3 d-none">' +
      '<form onsubmit="return guardarSeguimiento(event)">' +
      '<div class="row g-3">' +
      '<div class="col-md-6"><label class="form-label">Participante</label><select name="participante" class="form-select">' + opcionesParticipantes() + '</select></div>' +
      '<div class="col-md-6"><label class="form-label">Casa de Vida</label><select name="casa" class="form-select">' + opcionesCasas() + '</select></div>' +
      '<div class="col-md-4"><label class="form-label">Tipo</label><select name="tipo" class="form-select"><option>Visita</option><option>Llamada</option><option>Consejería</option></select></div>' +
      '<div class="col-md-4"><label class="form-label">Fecha</label><input name="fecha" type="date" class="form-control" value="' + hoyISO() + '" required></div>' +
      '<div class="col-md-4"><label class="form-label">Responsable</label><input name="responsable" class="form-control" value="' + esc(s.nombre) + '" required></div>' +
      '<div class="col-12"><label class="form-label">Observaciones</label><textarea name="observacion" class="form-control" rows="2" required></textarea></div>' +
      '</div>' +
      '<div class="mt-3 d-flex gap-2"><button class="btn btn-ccmg">Guardar seguimiento</button>' +
      '<button type="button" class="btn btn-light" onclick="return mostrarFormulario(\'formSeguimiento\')">Cancelar</button></div>' +
      '</form></div>' +
      tabla(['Participante', 'Casa de Vida', 'Tipo', 'Fecha', 'Responsable', 'Observación', 'Estado'], SEGUIMIENTOS.map(function (x) {
        const tipo = x.estado === 'Cerrado' ? 'ok' : (x.estado === 'Pendiente' ? 'pendiente' : 'info');
        return [esc(x.participante), esc(x.casa), esc(x.tipo), x.fecha, esc(x.responsable), esc(x.observacion), badge(x.estado, tipo)];
      }));
  },

  ofrendas: function () {
    const total = OFRENDAS.reduce(function (a, b) { return a + b.valor; }, 0);
    return titulo('Ofrendas', '<span class="fw-semibold text-success">Total: ' + dinero(total) + '</span>') +
      '<div class="card p-3 border-0 shadow-sm mb-3">' +
      '<form onsubmit="return guardarOfrenda(event)">' +
      '<div class="row g-3">' +
      '<div class="col-md-4"><label class="form-label">Casa de Vida</label><select name="casa" class="form-select">' + opcionesCasas() + '</select></div>' +
      '<div class="col-md-4"><label class="form-label">Concepto</label><input name="concepto" class="form-control" placeholder="Ofrenda semanal" required></div>' +
      '<div class="col-md-4"><label class="form-label">Fecha</label><input name="fecha" type="date" class="form-control" value="' + hoyISO() + '" required></div>' +
      '<div class="col-md-4"><label class="form-label">Valor</label><input name="valor" type="number" min="0" class="form-control" required></div>' +
      '<div class="col-md-4"><label class="form-label">Método</label><select name="metodo" class="form-select"><option>Efectivo</option><option>Transferencia</option><option>Nequi / Daviplata</option></select></div>' +
      '<div class="col-md-4 d-flex align-items-end"><button class="btn btn-ccmg w-100">Registrar ofrenda</button></div>' +
      '</div></form></div>' +
      tabla(['Fecha', 'Casa de Vida', 'Concepto', 'Método', 'Valor'], OFRENDAS.map(function (o) {
        return [o.fecha, esc(o.casa), esc(o.concepto), esc(o.metodo), dinero(o.valor)];
      }));
  },

  reportes: function (s) {
    return titulo('Reportes',
      '<span class="modulo-tag"><i class="bi bi-file-earmark-text"></i> Consolidado del módulo</span>') +
      '<div class="card p-3 border-0 shadow-sm mb-3">' +
      '<form onsubmit="return enviarReporte(event)">' +
      '<div class="row g-3">' +
      '<div class="col-md-4"><label class="form-label">Periodo</label><input name="periodo" type="month" class="form-control" value="2026-10" required></div>' +
      '<div class="col-md-4"><label class="form-label">Casa de Vida</label><select name="casa" class="form-select">' + opcionesCasas() + '</select></div>' +
      '<div class="col-md-4 d-flex align-items-end"><button class="btn btn-oro w-100"><i class="bi bi-send me-1"></i>Enviar reporte</button></div>' +
      '</div></form>' +
      '<p class="small text-muted mb-0 mt-2">El reporte se envía al Pastor' + (s.rol === 'apoyo' ? ' por medio del Supervisor de Área' : '') + '.</p>' +
      '</div>' +
      tabla(['Periodo', 'Casa de Vida', 'Enviado', 'Estado'], REPORTES.map(function (r) {
        return [r.periodo, esc(r.casa), r.enviado, badge(r.estado, r.estado === 'Revisado' ? 'neutro' : 'ok')];
      }));
  },

  perfil: function (s) {
    const info = ROLES_INFO[s.rol];
    return titulo('Mi perfil') +
      '<div class="card p-4 border-0 shadow-sm" style="max-width:560px">' +
      '<div class="mb-3"><label class="form-label">Nombre</label><input class="form-control" id="perfilNombre" value="' + esc(s.nombre) + '"></div>' +
      '<div class="mb-3"><label class="form-label">Rol</label><input class="form-control" value="' + esc(info ? info.nombre : s.rol) + '" disabled></div>' +
      '<div class="mb-3"><label class="form-label">Módulo</label><input class="form-control" value="Casas de Vida" disabled></div>' +
      '<button class="btn btn-ccmg" onclick="guardarPerfil()">Guardar cambios</button>' +
      '</div>';
  }
};

function guardarPerfil() {
  const nombre = document.getElementById('perfilNombre');
  const sesion = sesionActual();
  if (nombre && sesion) {
    sesion.nombre = nombre.value.trim() || sesion.nombre;
    // [DEMOSTRACIÓN] Datos de ejemplo - no se usan para control de acceso
    const el = document.getElementById('nombre');
    if (el) el.textContent = sesion.nombre;
  }
  avisar('Perfil actualizado.');
}

/* --------------------------- Menú del módulo --------------------------- */
const MENU_CASAS = [
  { id: 'inicio', t: 'Inicio', i: 'speedometer2', r: ['pastor', 'supervisor', 'lider', 'apoyo'] },
  { id: 'participantes', t: 'Participantes', i: 'people', url: URLS_PVA.participantes, r: ['pastor', 'supervisor', 'lider', 'apoyo'] },
  { id: 'casas', t: 'Casas de Vida', i: 'houses', url: URLS_PVA.casas, r: ['pastor', 'supervisor', 'lider', 'apoyo'] },
  { id: 'areas', t: 'Áreas', i: 'map', url: URLS_PVA.areas, r: ['pastor'] },
  { id: 'asistencia', t: 'Asistencia', i: 'check2-square', url: URLS_PVA.asistencia, r: ['pastor', 'supervisor', 'lider', 'apoyo'] },
  { id: 'seguimiento', t: 'Seguimiento', i: 'clipboard-check', r: ['pastor', 'supervisor', 'lider'] },
  { id: 'ofrendas', t: 'Ofrendas', i: 'cash-coin', r: ['pastor'] },
  { id: 'reportes', t: 'Reportes', i: 'file-earmark-text', r: ['pastor', 'supervisor', 'lider', 'apoyo'] },
  { id: 'perfil', t: 'Mi perfil', i: 'person-circle', r: ['pastor', 'supervisor', 'lider', 'apoyo'] }
];

/* ------------------------------ Arranque ------------------------------ */
document.addEventListener('DOMContentLoaded', function () {
  iniciarPanelModulo({
    modulo: 'CASAS_VIDA',
    menu: MENU_CASAS,
    vistas: VISTAS_CASAS,
    defaultId: 'inicio'
  });
});
