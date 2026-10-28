/* =====================================================================
   CCMG PVA · Panel del módulo ESCUELAS DE FORMACIÓN
   Roles con acceso: pastor, coord (Coordinador de Formación)
   Corresponde a los RF de procesos formativos, inscripciones,
   actividades, asistencia, seguimiento y reportes.
   ===================================================================== */

/* ------------------------- Datos de ejemplo ------------------------- */
const PROCESOS = [
  { id: 1, nombre: 'Escuelas Vida', tipo: 'Escuela', facilitador: 'Sandra León', inicio: '2026-09-05', estado: 'En curso', cupo: 30 },
  { id: 2, nombre: 'Módulos de Liderazgo', tipo: 'Módulo', facilitador: 'Luis Rojas', inicio: '2026-08-17', estado: 'En curso', cupo: 25 },
  { id: 3, nombre: 'Pasos de Vida', tipo: 'Escuela', facilitador: 'Ana Gómez', inicio: '2026-10-03', estado: 'En curso', cupo: 20 },
  { id: 4, nombre: 'Misiones', tipo: 'Módulo', facilitador: 'Pedro Silva', inicio: '2026-11-07', estado: 'Inscripciones', cupo: 18 },
  { id: 5, nombre: 'Escuelas Vida · Grupo 2026-1', tipo: 'Escuela', facilitador: 'Marta Ruiz', inicio: '2026-02-08', estado: 'Finalizado', cupo: 28 }
];

const INSCRIPCIONES = [
  { id: 1, participante: 'María Pérez', proceso: 'Escuelas Vida', fecha: '2026-09-01', estado: 'Aprobada' },
  { id: 2, participante: 'Carlos Díaz', proceso: 'Módulos de Liderazgo', fecha: '2026-08-12', estado: 'Aprobada' },
  { id: 3, participante: 'Luisa Fernández', proceso: 'Pasos de Vida', fecha: '2026-09-28', estado: 'Aprobada' },
  { id: 4, participante: 'Andrés Molina', proceso: 'Escuelas Vida', fecha: '2026-09-03', estado: 'En revisión' },
  { id: 5, participante: 'Sofía Ramírez', proceso: 'Misiones', fecha: '2026-10-20', estado: 'En revisión' },
  { id: 6, participante: 'Camila Rojas', proceso: 'Escuelas Vida', fecha: '2026-09-04', estado: 'Aprobada' }
];

const ACTIVIDADES_ESC = [
  { id: 1, proceso: 'Escuelas Vida', fecha: '2026-10-17', tema: 'Identidad en Cristo', facilitador: 'Sandra León', asistentes: 22 },
  { id: 2, proceso: 'Módulos de Liderazgo', fecha: '2026-10-18', tema: 'Liderazgo de servicio', facilitador: 'Luis Rojas', asistentes: 14 },
  { id: 3, proceso: 'Pasos de Vida', fecha: '2026-10-19', tema: 'Primeros pasos en la fe', facilitador: 'Ana Gómez', asistentes: 16 },
  { id: 4, proceso: 'Escuelas Vida', fecha: '2026-10-10', tema: 'La Palabra como fundamento', facilitador: 'Sandra León', asistentes: 20 }
];

const SEGUIMIENTOS_ESC = [
  { id: 1, participante: 'Andrés Molina', proceso: 'Escuelas Vida', tipo: 'Académico', fecha: '2026-10-14', responsable: 'Sandra León', observacion: 'Se recomienda nivelación de la unidad 2.', estado: 'En proceso' },
  { id: 2, participante: 'Camila Rojas', proceso: 'Escuelas Vida', tipo: 'Pastoral', fecha: '2026-10-11', responsable: 'Sandra León', observacion: 'Acompañamiento por inasistencia a dos sesiones.', estado: 'Pendiente' },
  { id: 3, participante: 'Carlos Díaz', proceso: 'Módulos de Liderazgo', tipo: 'Académico', fecha: '2026-10-09', responsable: 'Luis Rojas', observacion: 'Cumplió con el trabajo final del módulo.', estado: 'Cerrado' }
];

const REPORTES_ESC = [
  { id: 1, periodo: '2026-10', proceso: 'Escuelas Vida', enviado: '2026-10-21', estado: 'Enviado' },
  { id: 2, periodo: '2026-10', proceso: 'Módulos de Liderazgo', enviado: '2026-10-21', estado: 'Enviado' },
  { id: 3, periodo: '2026-09', proceso: 'Pasos de Vida', enviado: '2026-09-29', estado: 'Revisado' }
];

let siguienteIdEsc = 200;
function nuevoIdEsc() { return ++siguienteIdEsc; }

function opcionesProcesos(seleccionado) {
  return PROCESOS.map(function (p) {
    return '<option' + (p.nombre === seleccionado ? ' selected' : '') + '>' + esc(p.nombre) + '</option>';
  }).join('');
}

function opcionesParticipantesEsc() {
  return ['María Pérez', 'Carlos Díaz', 'Luisa Fernández', 'Andrés Molina', 'Sofía Ramírez',
    'Julián Torres', 'Daniela Castro', 'Felipe Vargas', 'Camila Rojas', 'Valentina Ortiz',
    'Sebastián Gil', 'Ricardo Peña'].map(function (n) {
      return '<option>' + esc(n) + '</option>';
    }).join('');
}

/* ----------------------- Acciones de la demo ----------------------- */
function guardarProceso(ev) {
  ev.preventDefault();
  const f = ev.target;
  PROCESOS.push({
    id: nuevoIdEsc(),
    nombre: f.nombre.value.trim(),
    tipo: f.tipo.value,
    facilitador: f.facilitador.value.trim(),
    inicio: f.inicio.value,
    estado: 'Inscripciones',
    cupo: Number(f.cupo.value)
  });
  avisar('Proceso de formación creado.');
  refrescar();
  return false;
}

function guardarInscripcion(ev) {
  ev.preventDefault();
  const f = ev.target;
  INSCRIPCIONES.push({
    id: nuevoIdEsc(),
    participante: f.participante.value,
    proceso: f.proceso.value,
    fecha: hoyISO(),
    estado: 'En revisión'
  });
  avisar('Inscripción registrada y enviada a revisión.');
  refrescar();
  return false;
}

function guardarActividadEsc(ev) {
  ev.preventDefault();
  const f = ev.target;
  ACTIVIDADES_ESC.push({
    id: nuevoIdEsc(),
    proceso: f.proceso.value,
    fecha: f.fecha.value,
    tema: f.tema.value.trim(),
    facilitador: f.facilitador.value.trim(),
    asistentes: 0
  });
  avisar('Actividad programada.');
  refrescar();
  return false;
}

function guardarSeguimientoEsc(ev) {
  ev.preventDefault();
  const f = ev.target;
  SEGUIMIENTOS_ESC.push({
    id: nuevoIdEsc(),
    participante: f.participante.value,
    proceso: f.proceso.value,
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

function enviarReporteEsc(ev) {
  ev.preventDefault();
  const f = ev.target;
  REPORTES_ESC.unshift({
    id: nuevoIdEsc(),
    periodo: f.periodo.value,
    proceso: f.proceso.value,
    enviado: hoyISO(),
    estado: 'Enviado'
  });
  avisar('Reporte enviado al Pastor.');
  refrescar();
  return false;
}

function registrarAsistenciaEsc(ev) {
  ev.preventDefault();
  const f = ev.target;
  const marcados = f.querySelectorAll('input[type="checkbox"]:checked').length;
  avisar('Asistencia registrada: ' + marcados + ' participantes presentes.');
  return false;
}

function aprobarInscripcion(id) {
  const ins = INSCRIPCIONES.find(function (x) { return x.id === id; });
  if (ins) {
    ins.estado = 'Aprobada';
    avisar('Inscripción aprobada.');
    refrescar();
  }
}

/* ----------------------------- Vistas ----------------------------- */
const VISTAS_ESCUELAS = {

  inicio: function (s) {
    const enCurso = PROCESOS.filter(function (p) { return p.estado === 'En curso'; }).length;
    const pendientes = INSCRIPCIONES.filter(function (i) { return i.estado === 'En revisión'; }).length;
    const aprobadas = INSCRIPCIONES.filter(function (i) { return i.estado === 'Aprobada'; }).length;

    return titulo('Hola, ' + esc(s.nombre),
      '<span class="modulo-tag modulo-tag--escuelas"><i class="bi bi-mortarboard"></i> Módulo Escuelas de Formación</span>') +
      '<p class="text-muted">Resumen del módulo de Escuelas de Formación.</p>' +
      '<div class="row g-3">' +
      stat('Procesos activos', enCurso, 'mortarboard') +
      stat('Inscripciones aprobadas', aprobadas, 'person-check') +
      stat('Por revisar', pendientes, 'hourglass-split') +
      stat('Actividades registradas', ACTIVIDADES_ESC.length, 'calendar-check') +
      '</div>' +
      '<div class="row g-3 mt-1">' +
      '<div class="col-lg-7"><div class="card p-3 border-0 shadow-sm h-100">' +
      '<h6 class="mb-3">Procesos de formación</h6>' +
      tabla(['Proceso', 'Tipo', 'Estado'], PROCESOS.map(function (p) {
        const tipo = p.estado === 'En curso' ? 'ok' : (p.estado === 'Inscripciones' ? 'info' : 'neutro');
        return [esc(p.nombre), esc(p.tipo), badge(p.estado, tipo)];
      })) +
      '</div></div>' +
      '<div class="col-lg-5"><div class="card p-3 border-0 shadow-sm h-100">' +
      '<h6 class="mb-3">Últimas actividades</h6>' +
      tabla(['Proceso', 'Fecha', 'Asistentes'], ACTIVIDADES_ESC.slice(0, 4).map(function (a) {
        return [esc(a.proceso), a.fecha, a.asistentes];
      })) +
      '</div></div>' +
      '</div>';
  },

  procesos: function () {
    return titulo('Procesos de formación',
      '<button class="btn btn-ccmg btn-sm" onclick="return mostrarFormulario(\'formProceso\')">' +
      '<i class="bi bi-plus-lg me-1"></i>Nuevo proceso</button>') +
      '<div id="formProceso" class="card p-3 border-0 shadow-sm mb-3 d-none">' +
      '<form onsubmit="return guardarProceso(event)">' +
      '<div class="row g-3">' +
      '<div class="col-md-6"><label class="form-label">Nombre del proceso</label><input name="nombre" class="form-control" required></div>' +
      '<div class="col-md-3"><label class="form-label">Tipo</label><select name="tipo" class="form-select"><option>Escuela</option><option>Módulo</option></select></div>' +
      '<div class="col-md-3"><label class="form-label">Cupo</label><input name="cupo" type="number" min="1" class="form-control" value="20" required></div>' +
      '<div class="col-md-6"><label class="form-label">Facilitador</label><input name="facilitador" class="form-control" required></div>' +
      '<div class="col-md-6"><label class="form-label">Fecha de inicio</label><input name="inicio" type="date" class="form-control" required></div>' +
      '</div>' +
      '<div class="mt-3 d-flex gap-2"><button class="btn btn-ccmg">Guardar proceso</button>' +
      '<button type="button" class="btn btn-light" onclick="return mostrarFormulario(\'formProceso\')">Cancelar</button></div>' +
      '</form></div>' +
      tabla(['Proceso', 'Tipo', 'Facilitador', 'Inicio', 'Inscritos', 'Cupo', 'Estado'], PROCESOS.map(function (p) {
        const inscritos = INSCRIPCIONES.filter(function (i) { return i.proceso === p.nombre; }).length;
        const tipo = p.estado === 'En curso' ? 'ok' : (p.estado === 'Inscripciones' ? 'info' : 'neutro');
        return [esc(p.nombre), esc(p.tipo), esc(p.facilitador), p.inicio, inscritos, p.cupo, badge(p.estado, tipo)];
      }));
  },

  inscripciones: function () {
    return titulo('Inscripciones',
      '<button class="btn btn-ccmg btn-sm" onclick="return mostrarFormulario(\'formInscripcion\')">' +
      '<i class="bi bi-plus-lg me-1"></i>Nueva inscripción</button>') +
      '<div id="formInscripcion" class="card p-3 border-0 shadow-sm mb-3 d-none">' +
      '<form onsubmit="return guardarInscripcion(event)">' +
      '<div class="row g-3">' +
      '<div class="col-md-6"><label class="form-label">Participante</label><select name="participante" class="form-select">' + opcionesParticipantesEsc() + '</select></div>' +
      '<div class="col-md-6"><label class="form-label">Proceso de formación</label><select name="proceso" class="form-select">' + opcionesProcesos() + '</select></div>' +
      '</div>' +
      '<div class="mt-3 d-flex gap-2"><button class="btn btn-ccmg">Registrar inscripción</button>' +
      '<button type="button" class="btn btn-light" onclick="return mostrarFormulario(\'formInscripcion\')">Cancelar</button></div>' +
      '</form></div>' +
      '<input id="buscarInscripcion" class="form-control mb-3" placeholder="Buscar por participante o proceso...">' +
      tabla(['Participante', 'Proceso', 'Fecha', 'Estado', 'Acción'], INSCRIPCIONES.map(function (i) {
        const tipo = i.estado === 'Aprobada' ? 'ok' : 'pendiente';
        const accion = i.estado === 'En revisión'
          ? '<button class="btn btn-sm btn-outline-success" onclick="aprobarInscripcion(' + i.id + ')">Aprobar</button>'
          : '<span class="text-muted small">—</span>';
        return [esc(i.participante), esc(i.proceso), i.fecha, badge(i.estado, tipo), accion];
      }), { id: 'tInscripciones' });
  },

  actividades: function () {
    return titulo('Actividades',
      '<button class="btn btn-ccmg btn-sm" onclick="return mostrarFormulario(\'formActividad\')">' +
      '<i class="bi bi-plus-lg me-1"></i>Programar actividad</button>') +
      '<div id="formActividad" class="card p-3 border-0 shadow-sm mb-3 d-none">' +
      '<form onsubmit="return guardarActividadEsc(event)">' +
      '<div class="row g-3">' +
      '<div class="col-md-6"><label class="form-label">Proceso</label><select name="proceso" class="form-select">' + opcionesProcesos() + '</select></div>' +
      '<div class="col-md-3"><label class="form-label">Fecha</label><input name="fecha" type="date" class="form-control" value="' + hoyISO() + '" required></div>' +
      '<div class="col-md-3"><label class="form-label">Facilitador</label><input name="facilitador" class="form-control" required></div>' +
      '<div class="col-12"><label class="form-label">Tema</label><input name="tema" class="form-control" required></div>' +
      '</div>' +
      '<div class="mt-3 d-flex gap-2"><button class="btn btn-ccmg">Guardar actividad</button>' +
      '<button type="button" class="btn btn-light" onclick="return mostrarFormulario(\'formActividad\')">Cancelar</button></div>' +
      '</form></div>' +
      tabla(['Proceso', 'Fecha', 'Tema', 'Facilitador', 'Asistentes'], ACTIVIDADES_ESC.map(function (a) {
        return [esc(a.proceso), a.fecha, esc(a.tema), esc(a.facilitador), a.asistentes];
      }));
  },

  asistencia: function () {
    return titulo('Asistencia a la formación', '<span class="text-muted small">RF · Control de asistencia</span>') +
      '<div class="card p-3 border-0 shadow-sm mb-3">' +
      '<form onsubmit="return registrarAsistenciaEsc(event)">' +
      '<div class="row g-3 mb-3">' +
      '<div class="col-md-5"><label class="form-label">Proceso</label><select class="form-select">' + opcionesProcesos() + '</select></div>' +
      '<div class="col-md-4"><label class="form-label">Tema de la sesión</label><input class="form-control" placeholder="Unidad / tema"></div>' +
      '<div class="col-md-3"><label class="form-label">Fecha</label><input type="date" class="form-control" value="' + hoyISO() + '"></div>' +
      '</div>' +
      '<p class="small text-muted mb-2">Participantes inscritos:</p>' +
      '<div class="row g-2">' +
      INSCRIPCIONES.map(function (i, n) {
        return '<div class="col-md-6"><div class="form-check">' +
          '<input class="form-check-input" type="checkbox" id="ae' + n + '" checked>' +
          '<label class="form-check-label" for="ae' + n + '">' + esc(i.participante) +
          ' <small class="text-muted">· ' + esc(i.proceso) + '</small></label></div></div>';
      }).join('') +
      '</div>' +
      '<button class="btn btn-ccmg mt-3">Guardar asistencia</button>' +
      '</form></div>' +
      '<h6 class="mb-2">Historial de sesiones</h6>' +
      tabla(['Proceso', 'Fecha', 'Tema', 'Asistentes'], ACTIVIDADES_ESC.map(function (a) {
        return [esc(a.proceso), a.fecha, esc(a.tema), a.asistentes];
      }));
  },

  seguimiento: function (s) {
    return titulo('Seguimiento',
      '<button class="btn btn-ccmg btn-sm" onclick="return mostrarFormulario(\'formSeguimientoEsc\')">' +
      '<i class="bi bi-plus-lg me-1"></i>Nuevo seguimiento</button>') +
      '<div id="formSeguimientoEsc" class="card p-3 border-0 shadow-sm mb-3 d-none">' +
      '<form onsubmit="return guardarSeguimientoEsc(event)">' +
      '<div class="row g-3">' +
      '<div class="col-md-6"><label class="form-label">Participante</label><select name="participante" class="form-select">' + opcionesParticipantesEsc() + '</select></div>' +
      '<div class="col-md-6"><label class="form-label">Proceso</label><select name="proceso" class="form-select">' + opcionesProcesos() + '</select></div>' +
      '<div class="col-md-4"><label class="form-label">Tipo</label><select name="tipo" class="form-select"><option>Académico</option><option>Pastoral</option><option>Disciplinar</option></select></div>' +
      '<div class="col-md-4"><label class="form-label">Fecha</label><input name="fecha" type="date" class="form-control" value="' + hoyISO() + '" required></div>' +
      '<div class="col-md-4"><label class="form-label">Responsable</label><input name="responsable" class="form-control" value="' + esc(s.nombre) + '" required></div>' +
      '<div class="col-12"><label class="form-label">Observaciones</label><textarea name="observacion" class="form-control" rows="2" required></textarea></div>' +
      '</div>' +
      '<div class="mt-3 d-flex gap-2"><button class="btn btn-ccmg">Guardar seguimiento</button>' +
      '<button type="button" class="btn btn-light" onclick="return mostrarFormulario(\'formSeguimientoEsc\')">Cancelar</button></div>' +
      '</form></div>' +
      tabla(['Participante', 'Proceso', 'Tipo', 'Fecha', 'Responsable', 'Observación', 'Estado'], SEGUIMIENTOS_ESC.map(function (x) {
        const tipo = x.estado === 'Cerrado' ? 'ok' : (x.estado === 'Pendiente' ? 'pendiente' : 'info');
        return [esc(x.participante), esc(x.proceso), esc(x.tipo), x.fecha, esc(x.responsable), esc(x.observacion), badge(x.estado, tipo)];
      }));
  },

  reportes: function () {
    return titulo('Reportes',
      '<span class="modulo-tag modulo-tag--escuelas"><i class="bi bi-file-earmark-text"></i> Consolidado del módulo</span>') +
      '<div class="card p-3 border-0 shadow-sm mb-3">' +
      '<form onsubmit="return enviarReporteEsc(event)">' +
      '<div class="row g-3">' +
      '<div class="col-md-4"><label class="form-label">Periodo</label><input name="periodo" type="month" class="form-control" value="2026-10" required></div>' +
      '<div class="col-md-4"><label class="form-label">Proceso</label><select name="proceso" class="form-select">' + opcionesProcesos() + '</select></div>' +
      '<div class="col-md-4 d-flex align-items-end"><button class="btn btn-oro w-100"><i class="bi bi-send me-1"></i>Enviar reporte</button></div>' +
      '</div></form>' +
      '<p class="small text-muted mb-0 mt-2">El reporte de formación se envía al Pastor.</p>' +
      '</div>' +
      tabla(['Periodo', 'Proceso', 'Enviado', 'Estado'], REPORTES_ESC.map(function (r) {
        return [r.periodo, esc(r.proceso), r.enviado, badge(r.estado, r.estado === 'Revisado' ? 'neutro' : 'ok')];
      }));
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
  const raw = sessionStorage.getItem('ccmg');
  if (nombre && raw) {
    const sesion = JSON.parse(raw);
    sesion.nombre = nombre.value.trim() || sesion.nombre;
    sessionStorage.setItem('ccmg', JSON.stringify(sesion));
    const el = document.getElementById('nombre');
    if (el) el.textContent = sesion.nombre;
  }
  avisar('Perfil actualizado (demo).');
}

/* --------------------------- Menú del módulo --------------------------- */
const MENU_ESCUELAS = [
  { id: 'inicio', t: 'Inicio', i: 'speedometer2', r: ['pastor', 'coord'] },
  { id: 'procesos', t: 'Procesos de formación', i: 'mortarboard', r: ['pastor', 'coord'] },
  { id: 'inscripciones', t: 'Inscripciones', i: 'person-plus', r: ['pastor', 'coord'] },
  { id: 'actividades', t: 'Actividades', i: 'calendar-event', r: ['pastor', 'coord'] },
  { id: 'asistencia', t: 'Asistencia', i: 'check2-square', r: ['pastor', 'coord'] },
  { id: 'seguimiento', t: 'Seguimiento', i: 'clipboard-check', r: ['pastor', 'coord'] },
  { id: 'reportes', t: 'Reportes', i: 'file-earmark-text', r: ['pastor', 'coord'] },
  { id: 'perfil', t: 'Mi perfil', i: 'person-circle', r: ['pastor', 'coord'] }
];

/* ------------------------------ Arranque ------------------------------ */
document.addEventListener('DOMContentLoaded', function () {
  iniciarPanelModulo({
    modulo: 'ESCUELAS_FORMACION',
    menu: MENU_ESCUELAS,
    vistas: VISTAS_ESCUELAS,
    defaultId: 'inicio',
    alMontar: function (id) {
      if (id === 'inscripciones') activarBuscador('buscarInscripcion', 'tInscripciones');
    }
  });
});
