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

/* ----------------------------- Vistas ----------------------------- */
const VISTAS_CASAS = {

  inicio: function (s) {
    return titulo('Hola, ' + esc(s.nombre),
      '<span class="modulo-tag"><i class="bi bi-houses"></i> Módulo Casas de Vida</span>') +
      '<p class="text-muted">Resumen del módulo de Casas de Vida.</p>' +
      '<div class="row g-3">' +
      stat('Participantes', RESUMEN.participantes, 'people') +
      stat('Casas de Vida', RESUMEN.casas + ' <small class="text-muted fs-6">(' + RESUMEN.casasActivas + ' activas)</small>', 'houses') +
      stat('Asistencia promedio', RESUMEN.asistenciaPromedio + '%', 'graph-up') +
      stat('Seguimientos abiertos', RESUMEN.seguimientosAbiertos, 'clipboard-check') +
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
      tabla(['Participante', 'Estado'], RESUMEN.seguimientos.map(function (x) {
        return [esc(x.participante), badge(x.estado, x.cerrado ? 'ok' : 'pendiente')];
      })) +
      '</div></div>' +
      '</div>';
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
  { id: 'importar', t: 'Importar datos', i: 'upload', url: URLS_PVA.importar, r: ['pastor'] },
  { id: 'asistencia', t: 'Asistencia', i: 'check2-square', url: URLS_PVA.asistencia, r: ['pastor', 'supervisor', 'lider', 'apoyo'] },
  { id: 'seguimiento', t: 'Seguimiento', i: 'clipboard-check', url: URLS_PVA.seguimiento, r: ['pastor', 'supervisor', 'lider'] },
  { id: 'reportes', t: 'Reportes', i: 'file-earmark-text', url: URLS_PVA.reportes, r: ['pastor', 'supervisor', 'lider', 'apoyo'] },
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
