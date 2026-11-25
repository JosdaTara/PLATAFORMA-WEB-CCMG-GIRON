/* =====================================================================
   CCMG PVA · Panel del módulo CASAS DE VIDA
   Roles con acceso: pastor, supervisor, lider, apoyo
   Pinta el inicio y el perfil; participantes, casas, asistencia,
   seguimiento y reportes son páginas de Django (apps/pva).
   ===================================================================== */

/* Resumen y rutas calculados en el servidor según el alcance del rol (pva.views.panel_casas) */
function leerJSON(id, porDefecto) {
  const el = document.getElementById(id);
  try { return el ? JSON.parse(el.textContent) : porDefecto; } catch (e) { return porDefecto; }
}
const RESUMEN = leerJSON('pva-resumen', { participantes: 0, casas: 0, casasActivas: 0, asistenciaPromedio: 0, actividades: [], seguimientosAbiertos: 0, seguimientos: [] });
const URLS_PVA = leerJSON('pva-urls', {});

/* Tarea semanal del Líder y su equipo: lo primero que se ve en el panel */
function tarjetaSemana(r) {
  if (!r) return '';
  if (r.enviado) {
    return '<div class="tarjeta-semana tarjeta-semana--ok mb-3">' +
      '<i class="bi bi-check2-circle tarjeta-semana__icono" aria-hidden="true"></i>' +
      '<div class="tarjeta-semana__texto"><strong>El reporte de esta semana ya está enviado.</strong>' +
      '<span>Lo envió ' + esc(r.enviadoPor) + (r.enviadoEl ? ' el ' + esc(r.enviadoEl) : '') + ' · ' + esc(r.semana) + '</span></div>' +
      '<a href="' + esc(r.urlVer) + '" class="btn btn-outline-secondary btn-flujo">Ver reporte</a></div>';
  }
  return '<div class="tarjeta-semana tarjeta-semana--pendiente mb-3">' +
    '<i class="bi bi-clipboard-plus tarjeta-semana__icono" aria-hidden="true"></i>' +
    '<div class="tarjeta-semana__texto"><strong>Falta el reporte de esta semana.</strong>' +
    '<span>' + esc(r.casa) + ' · ' + esc(r.semana) + (r.supervisor ? ' · Llega a ' + esc(r.supervisor) : '') + '</span></div>' +
    '<a href="' + esc(r.urlLlenar) + '" class="btn btn-oro btn-flujo">Llenar reporte</a></div>';
}

/* Pastor y Supervisor: qué Casas de Vida no han enviado el reporte de la semana actual */
function bloqueSinReporte(r) {
  if (!r || !r.totalActivas) return '';
  if (!r.casas.length) {
    return '<div class="tarjeta-semana tarjeta-semana--ok mb-3">' +
      '<i class="bi bi-check2-circle tarjeta-semana__icono" aria-hidden="true"></i>' +
      '<div class="tarjeta-semana__texto"><strong>Todas las casas enviaron el reporte.</strong>' +
      '<span>' + esc(r.semana) + '</span></div></div>';
  }
  return '<div class="card p-3 border-0 shadow-sm mb-3">' +
    '<h2 class="mb-1">Casas sin reporte esta semana <span class="badge rounded-pill text-bg-warning ms-1">' + r.casas.length + '</span></h2>' +
    '<p class="small text-muted mb-3">' + esc(r.semana) + '</p>' +
    tabla(['Casa de Vida', 'Líder'], r.casas.map(function (c) {
      return ['<a href="' + esc(c.url) + '" class="text-decoration-none">' + esc(c.casa) + '</a>', esc(c.lider)];
    })) +
    '</div>';
}

/* ----------------------------- Vistas ----------------------------- */
const VISTAS_CASAS = {

  inicio: function (s) {
    return titulo('Hola, ' + esc(s.nombre),
      '<span class="modulo-tag d-lg-none"><i class="bi bi-houses" aria-hidden="true"></i> Módulo Casas de Vida</span>') +
      tarjetaSemana(RESUMEN.reporteSemana) +
      bloqueSinReporte(RESUMEN.sinReporte) +
      '<p class="text-muted">Resumen del módulo de Casas de Vida.</p>' +
      '<div class="row g-3">' +
      stat('Personas nuevas', RESUMEN.participantes, 'person-plus') +
      stat('Casas de Vida', RESUMEN.casas + (RESUMEN.casasActivas === RESUMEN.casas ? '' : ' <small class="text-muted fs-6">(' + RESUMEN.casasActivas + (RESUMEN.casasActivas === 1 ? ' activa' : ' activas') + ')</small>'), 'houses') +
      stat('Asistentes por reunión', RESUMEN.asistenciaPromedio, 'graph-up') +
      stat('Seguimientos abiertos', RESUMEN.seguimientosAbiertos, 'clipboard-check') +
      '</div>' +
      '<div class="row g-3 mt-1">' +
      '<div class="col-lg-7"><div class="card p-3 border-0 shadow-sm h-100">' +
      '<div class="d-flex justify-content-between align-items-center mb-3"><h2 class="m-0">Últimos reportes de asistencia</h2>' +
      (URLS_PVA.asistencia ? '<a class="small text-decoration-none" href="' + URLS_PVA.asistencia + '">Ver asistencia</a>' : '') + '</div>' +
      tabla(['Casa de Vida', 'Fecha', 'Asistentes', 'Nuevos'], RESUMEN.actividades.map(function (a) {
        return [esc(a.casa), fechaCorta(a.fecha), a.asistentes, a.nuevos];
      })) +
      '</div></div>' +
      '<div class="col-lg-5"><div class="card p-3 border-0 shadow-sm h-100">' +
      '<h2 class="mb-3">Seguimientos recientes</h2>' +
      tabla(['Participante', 'Estado'], RESUMEN.seguimientos.map(function (x) {
        return [esc(x.participante), badge(x.estado, x.cerrado ? 'ok' : 'pendiente')];
      })) +
      '</div></div>' +
      '</div>';
  },

  perfil: function (s) {
    return vistaPerfil(s, 'Casas de Vida');
  }
};


/* --------------------------- Menú del módulo --------------------------- */
const MENU_CASAS = [
  { id: 'inicio', t: 'Inicio', i: 'speedometer2', r: ['pastor', 'supervisor', 'lider', 'apoyo'] },
  { id: 'participantes', t: 'Personas nuevas', i: 'person-plus', url: URLS_PVA.participantes, r: ['pastor', 'supervisor', 'lider', 'apoyo'] },
  { id: 'casas', t: 'Casas de Vida', i: 'houses', url: URLS_PVA.casas, r: ['pastor', 'supervisor', 'lider', 'apoyo'] },
  { id: 'areas', t: 'Áreas', i: 'map', url: URLS_PVA.areas, r: ['pastor'] },
  { id: 'importar', t: 'Importar datos', i: 'upload', url: URLS_PVA.importar, r: ['pastor'] },
  { id: 'asistencia', t: 'Asistencia', i: 'check2-square', url: URLS_PVA.asistencia, r: ['pastor', 'supervisor', 'lider', 'apoyo'] },
  { id: 'seguimiento', t: 'Seguimiento', i: 'clipboard-check', url: URLS_PVA.seguimiento, r: ['pastor', 'supervisor', 'lider'] },
  { id: 'reportes', t: 'Reportes', i: 'file-earmark-text', url: URLS_PVA.reportes, r: ['pastor', 'supervisor', 'lider', 'apoyo'] },
  { id: 'usuarios', t: 'Usuarios', i: 'person-gear', url: URLS_PVA.usuarios, r: ['pastor'] },
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
