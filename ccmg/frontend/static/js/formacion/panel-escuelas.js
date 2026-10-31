/* =====================================================================
   CCMG PVA · Panel del módulo ESCUELAS DE FORMACIÓN
   Roles con acceso: pastor, coord (Coordinador de Formación)
   Pinta el inicio y el perfil; procesos, participantes, asistencia,
   seguimiento y reportes son páginas de Django (apps/formacion).
   ===================================================================== */

/* Resumen y rutas calculados en el servidor según el alcance del rol (formacion.views.panel_escuelas) */
function leerJSONEsc(id, porDefecto) {
  const el = document.getElementById(id);
  try { return el ? JSON.parse(el.textContent) : porDefecto; } catch (e) { return porDefecto; }
}
const RESUMEN_ESC = leerJSONEsc('formacion-resumen', { procesosActivos: 0, inscritos: 0, asistenciaPromedio: 0, seguimientosAbiertos: 0, procesos: [], actividades: [] });
const URLS_ESC = leerJSONEsc('formacion-urls', {});

/* ----------------------------- Vistas ----------------------------- */
const VISTAS_ESCUELAS = {

  inicio: function (s) {
    return titulo('Hola, ' + esc(s.nombre),
      '<span class="modulo-tag modulo-tag--escuelas"><i class="bi bi-mortarboard"></i> Módulo Escuelas de Formación</span>') +
      '<p class="text-muted">Resumen del módulo de Escuelas de Formación.</p>' +
      '<div class="row g-3">' +
      stat('Procesos activos', RESUMEN_ESC.procesosActivos, 'mortarboard') +
      stat('Inscritos', RESUMEN_ESC.inscritos, 'person-check') +
      stat('Asistencia promedio', RESUMEN_ESC.asistenciaPromedio + '%', 'graph-up') +
      stat('Seguimientos abiertos', RESUMEN_ESC.seguimientosAbiertos, 'clipboard-check') +
      '</div>' +
      '<div class="row g-3 mt-1">' +
      '<div class="col-lg-7"><div class="card p-3 border-0 shadow-sm h-100">' +
      '<div class="d-flex justify-content-between align-items-center mb-3"><h6 class="m-0">Procesos de formación</h6>' +
      (URLS_ESC.procesos ? '<a class="small text-decoration-none" href="' + URLS_ESC.procesos + '">Ver todos</a>' : '') + '</div>' +
      tabla(['Proceso', 'Escuela', 'Estado'], RESUMEN_ESC.procesos.map(function (p) {
        return [esc(p.nombre), esc(p.tipo), badge(p.activo ? 'Activo' : 'Inactivo', p.activo ? 'ok' : 'neutro')];
      })) +
      '</div></div>' +
      '<div class="col-lg-5"><div class="card p-3 border-0 shadow-sm h-100">' +
      '<h6 class="mb-3">Últimas actividades</h6>' +
      tabla(['Proceso', 'Fecha', 'Asistentes'], RESUMEN_ESC.actividades.map(function (a) {
        return [esc(a.proceso), fechaCorta(a.fecha), a.asistentes];
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
      '<div class="mb-3"><label class="form-label">Módulo</label><input class="form-control" value="Escuelas de Formación" disabled></div>' +
      '<button class="btn btn-ccmg" onclick="guardarPerfilEsc()">Guardar cambios</button>' +
      '</div>';
  }
};

function guardarPerfilEsc() {
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
const MENU_ESCUELAS = [
  { id: 'inicio', t: 'Inicio', i: 'speedometer2', r: ['pastor', 'coord'] },
  { id: 'procesos', t: 'Procesos de formación', i: 'mortarboard', url: URLS_ESC.procesos, r: ['pastor', 'coord'] },
  { id: 'participantes', t: 'Participantes', i: 'people', url: URLS_ESC.participantes, r: ['pastor', 'coord'] },
  { id: 'asistencia', t: 'Actividades y asistencia', i: 'check2-square', url: URLS_ESC.asistencia, r: ['pastor', 'coord'] },
  { id: 'seguimiento', t: 'Seguimiento', i: 'clipboard-check', url: URLS_ESC.seguimiento, r: ['pastor', 'coord'] },
  { id: 'reportes', t: 'Reportes', i: 'file-earmark-text', url: URLS_ESC.reportes, r: ['pastor', 'coord'] },
  { id: 'usuarios', t: 'Usuarios', i: 'person-gear', url: URLS_ESC.usuarios, r: ['pastor'] },
  { id: 'perfil', t: 'Mi perfil', i: 'person-circle', r: ['pastor', 'coord'] }
];

/* ------------------------------ Arranque ------------------------------ */
document.addEventListener('DOMContentLoaded', function () {
  iniciarPanelModulo({
    modulo: 'ESCUELAS_FORMACION',
    menu: MENU_ESCUELAS,
    vistas: VISTAS_ESCUELAS,
    defaultId: 'inicio'
  });
});
