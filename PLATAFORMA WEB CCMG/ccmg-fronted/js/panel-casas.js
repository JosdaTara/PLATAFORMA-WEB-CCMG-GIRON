/* =====================================================================
   CCMG PVA · Panel del módulo CASAS DE VIDA
   Roles con acceso: pastor, supervisor, lider, apoyo
   Corresponde a los RF de Casas de Vida, participantes, asistencia,
   seguimiento, ofrendas y reportes.
   ===================================================================== */

/* ------------------------- Datos de ejemplo ------------------------- */
const CASAS = [
  { id: 1, nombre: 'Casa Esperanza', area: 'Norte', lider: 'Ana Gómez', supervisor: 'Luis Rojas', dia: 'Martes', hora: '7:00 p. m.', direccion: 'Cra 10 #5-20', estado: 'Activa' },
  { id: 2, nombre: 'Casa Fe', area: 'Centro', lider: 'Pedro Silva', supervisor: 'Luis Rojas', dia: 'Miércoles', hora: '7:00 p. m.', direccion: 'Cll 8 #12-4', estado: 'Activa' },
  { id: 3, nombre: 'Casa Gracia', area: 'Sur', lider: 'Marta Ruiz', supervisor: 'Sandra León', dia: 'Jueves', hora: '6:30 p. m.', direccion: 'Cra 22 #14-33', estado: 'Activa' },
  { id: 4, nombre: 'Casa Restauración', area: 'Norte', lider: 'Jorge Pineda', supervisor: 'Sandra León', dia: 'Viernes', hora: '7:00 p. m.', direccion: 'Cll 30 #9-11', estado: 'En formación' }
];

const PARTICIPANTES = [
  { id: 1, nombre: 'María Pérez', documento: '1098765432', nacimiento: '1990-05-12', telefono: '300 123 4567', casa: 'Casa Esperanza', funcion: 'Miembro', estado: 'Activo' },
  { id: 2, nombre: 'Carlos Díaz', documento: '1090123456', nacimiento: '1985-11-03', telefono: '310 987 6543', casa: 'Casa Fe', funcion: 'Miembro', estado: 'Activo' },
  { id: 3, nombre: 'Luisa Fernández', documento: '1093456789', nacimiento: '1998-02-27', telefono: '301 555 1234', casa: 'Casa Gracia', funcion: 'Aprendiz', estado: 'Activo' },
  { id: 4, nombre: 'Andrés Molina', documento: '1094567890', nacimiento: '1993-07-19', telefono: '302 444 8899', casa: 'Casa Esperanza', funcion: 'Anfitrión', estado: 'Activo' },
  { id: 5, nombre: 'Sofía Ramírez', documento: '1095678901', nacimiento: '2001-09-08', telefono: '303 222 7788', casa: 'Casa Fe', funcion: 'Maestro de niños', estado: 'Activo' },
  { id: 6, nombre: 'Julián Torres', documento: '1096789012', nacimiento: '1979-04-15', telefono: '304 111 6655', casa: 'Casa Restauración', funcion: 'Miembro', estado: 'En proceso' },
  { id: 7, nombre: 'Daniela Castro', documento: '1097890123', nacimiento: '1995-12-01', telefono: '305 333 9900', casa: 'Casa Gracia', funcion: 'Miembro', estado: 'Activo' },
  { id: 8, nombre: 'Felipe Vargas', documento: '1098901234', nacimiento: '1988-06-23', telefono: '306 777 2211', casa: 'Casa Esperanza', funcion: 'Miembro', estado: 'Activo' },
  { id: 9, nombre: 'Camila Rojas', documento: '1099012345', nacimiento: '2000-03-30', telefono: '307 888 3344', casa: 'Casa Fe', funcion: 'Aprendiz', estado: 'Activo' },
  { id: 10, nombre: 'Ricardo Peña', documento: '1091122334', nacimiento: '1975-10-11', telefono: '308 999 4455', casa: 'Casa Restauración', funcion: 'Miembro', estado: 'Inactivo' },
  { id: 11, nombre: 'Valentina Ortiz', documento: '1092233445', nacimiento: '1997-08-05', telefono: '309 123 9876', casa: 'Casa Gracia', funcion: 'Miembro', estado: 'Activo' },
  { id: 12, nombre: 'Sebastián Gil', documento: '1093344556', nacimiento: '1991-01-17', telefono: '311 456 7890', casa: 'Casa Esperanza', funcion: 'Miembro', estado: 'Activo' }
];

const ACTIVIDADES = [
  { id: 1, casa: 'Casa Esperanza', fecha: '2026-10-20', tipo: 'Reunión semanal', asistentes: 10, invitados: 2 },
  { id: 2, casa: 'Casa Fe', fecha: '2026-10-21', tipo: 'Reunión semanal', asistentes: 8, invitados: 1 },
  { id: 3, casa: 'Casa Gracia', fecha: '2026-10-22', tipo: 'Reunión semanal', asistentes: 9, invitados: 0 },
  { id: 4, casa: 'Casa Restauración', fecha: '2026-10-16', tipo: 'Reunión semanal', asistentes: 5, invitados: 3 },
  { id: 5, casa: 'Casa Esperanza', fecha: '2026-10-13', tipo: 'Reunión semanal', asistentes: 11, invitados: 1 }
];

const SEGUIMIENTOS = [
  { id: 1, participante: 'María Pérez', casa: 'Casa Esperanza', tipo: 'Visita', fecha: '2026-10-12', responsable: 'Ana Gómez', observacion: 'Acompañamiento en su proceso de consolidación.', estado: 'Cerrado' },
  { id: 2, participante: 'Julián Torres', casa: 'Casa Restauración', tipo: 'Llamada', fecha: '2026-10-18', responsable: 'Jorge Pineda', observacion: 'Se acordó retomar la asistencia semanal.', estado: 'En proceso' },
  { id: 3, participante: 'Ricardo Peña', casa: 'Casa Restauración', tipo: 'Visita', fecha: '2026-10-19', responsable: 'Jorge Pineda', observacion: 'Motivos de salud; pendiente nueva visita.', estado: 'Pendiente' },
  { id: 4, participante: 'Camila Rojas', casa: 'Casa Fe', tipo: 'Consejería', fecha: '2026-10-15', responsable: 'Pedro Silva', observacion: 'Orientación para iniciar Escuela Vida.', estado: 'Cerrado' }
];

const OFRENDAS = [
  { id: 1, fecha: '2026-10-18', casa: 'Casa Esperanza', concepto: 'Ofrenda semanal', valor: 85000, metodo: 'Efectivo' },
  { id: 2, fecha: '2026-10-18', casa: 'Casa Fe', concepto: 'Ofrenda semanal', valor: 62000, metodo: 'Transferencia' },
  { id: 3, fecha: '2026-10-11', casa: 'Casa Gracia', concepto: 'Ofrenda semanal', valor: 74000, metodo: 'Efectivo' },
  { id: 4, fecha: '2026-10-04', casa: 'Casa Restauración', concepto: 'Ofrenda especial', valor: 40000, metodo: 'Efectivo' }
];

const REPORTES = [
  { id: 1, periodo: '2026-10', casa: 'Casa Esperanza', enviado: '2026-10-21', estado: 'Enviado' },
  { id: 2, periodo: '2026-10', casa: 'Casa Fe', enviado: '2026-10-21', estado: 'Enviado' },
  { id: 3, periodo: '2026-09', casa: 'Casa Gracia', enviado: '2026-09-28', estado: 'Revisado' }
];

let siguienteId = 100;
function nuevoId() { return ++siguienteId; }

function opcionesCasas(seleccionada) {
  return CASAS.map(function (c) {
    return '<option' + (c.nombre === seleccionada ? ' selected' : '') + '>' + esc(c.nombre) + '</option>';
  }).join('');
}

function opcionesParticipantes() {
  return PARTICIPANTES.map(function (p) {
    return '<option>' + esc(p.nombre) + '</option>';
  }).join('');
}

function dinero(n) {
  return '$' + Number(n).toLocaleString('es-CO');
}

/* ----------------------- Acciones de la demo ----------------------- */
function guardarParticipante(ev) {
  ev.preventDefault();
  const f = ev.target;
  PARTICIPANTES.push({
    id: nuevoId(),
    nombre: f.nombre.value.trim(),
    documento: f.documento.value.trim(),
    nacimiento: f.nacimiento.value,
    telefono: f.telefono.value.trim(),
    casa: f.casa.value,
    funcion: f.funcion.value,
    estado: 'Activo'
  });
  avisar('Participante registrado correctamente.');
  refrescar();
  return false;
}

function guardarCasa(ev) {
  ev.preventDefault();
  const f = ev.target;
  CASAS.push({
    id: nuevoId(),
    nombre: f.nombre.value.trim(),
    area: f.area.value,
    lider: f.lider.value.trim(),
    supervisor: f.supervisor.value.trim(),
    dia: f.dia.value,
    hora: f.hora.value,
    direccion: f.direccion.value.trim(),
    estado: 'Activa'
  });
  avisar('Casa de Vida creada correctamente.');
  refrescar();
  return false;
}

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

function registrarAsistencia(ev) {
  ev.preventDefault();
  const f = ev.target;
  const marcados = f.querySelectorAll('input[type="checkbox"]:checked').length;
  avisar('Asistencia registrada: ' + marcados + ' personas presentes.');
  return false;
}

/* ----------------------------- Vistas ----------------------------- */
const VISTAS_CASAS = {

  inicio: function (s) {
    const activas = CASAS.filter(function (c) { return c.estado === 'Activa'; }).length;
    const totalAsistentes = ACTIVIDADES.reduce(function (a, b) { return a + b.asistentes; }, 0);
    const promedio = PARTICIPANTES.length
      ? Math.round((totalAsistentes / ACTIVIDADES.length) / PARTICIPANTES.length * 100)
      : 0;
    const pendientes = SEGUIMIENTOS.filter(function (x) { return x.estado !== 'Cerrado'; }).length;

    return titulo('Hola, ' + esc(s.nombre),
      '<span class="modulo-tag"><i class="bi bi-houses"></i> Módulo Casas de Vida</span>') +
      '<p class="text-muted">Resumen del módulo de Casas de Vida.</p>' +
      '<div class="row g-3">' +
      stat('Participantes', PARTICIPANTES.length, 'people') +
      stat('Casas de Vida', CASAS.length + ' <small class="text-muted fs-6">(' + activas + ' activas)</small>', 'houses') +
      stat('Asistencia promedio', promedio + '%', 'graph-up') +
      stat('Seguimientos abiertos', pendientes, 'clipboard-check') +
      '</div>' +
      '<div class="row g-3 mt-1">' +
      '<div class="col-lg-7"><div class="card p-3 border-0 shadow-sm h-100">' +
      '<h6 class="mb-3">Últimas actividades registradas</h6>' +
      tabla(['Casa de Vida', 'Fecha', 'Actividad', 'Asistentes'], ACTIVIDADES.slice(0, 4).map(function (a) {
        return [esc(a.casa), a.fecha, esc(a.tipo), a.asistentes];
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

  participantes: function () {
    return titulo('Participantes',
      '<button class="btn btn-ccmg btn-sm" onclick="return mostrarFormulario(\'formParticipante\')">' +
      '<i class="bi bi-plus-lg me-1"></i>Nuevo participante</button>') +
      '<div id="formParticipante" class="card p-3 border-0 shadow-sm mb-3 d-none">' +
      '<form onsubmit="return guardarParticipante(event)">' +
      '<div class="row g-3">' +
      '<div class="col-md-6"><label class="form-label">Nombres y apellidos</label><input name="nombre" class="form-control" required></div>' +
      '<div class="col-md-6"><label class="form-label">Documento de identidad</label><input name="documento" class="form-control" required></div>' +
      '<div class="col-md-6"><label class="form-label">Fecha de nacimiento</label><input name="nacimiento" type="date" class="form-control" required></div>' +
      '<div class="col-md-6"><label class="form-label">Teléfono</label><input name="telefono" type="tel" class="form-control" required></div>' +
      '<div class="col-md-6"><label class="form-label">Casa de Vida</label><select name="casa" class="form-select">' + opcionesCasas() + '</select></div>' +
      '<div class="col-md-6"><label class="form-label">Función en la Casa de Vida</label>' +
      '<select name="funcion" class="form-select"><option>Miembro</option><option>Aprendiz</option><option>Anfitrión</option><option>Maestro de niños</option></select></div>' +
      '</div>' +
      '<div class="mt-3 d-flex gap-2">' +
      '<button class="btn btn-ccmg">Guardar participante</button>' +
      '<button type="button" class="btn btn-light" onclick="return mostrarFormulario(\'formParticipante\')">Cancelar</button>' +
      '</div></form></div>' +
      '<input id="buscarParticipante" class="form-control mb-3" placeholder="Buscar por nombre, documento o Casa de Vida...">' +
      tabla(['Nombre', 'Documento', 'Teléfono', 'Casa de Vida', 'Función', 'Estado'], PARTICIPANTES.map(function (p) {
        return [
          esc(p.nombre), esc(p.documento), esc(p.telefono), esc(p.casa), esc(p.funcion),
          badge(p.estado, p.estado === 'Activo' ? 'ok' : 'pendiente')
        ];
      }), { id: 'tParticipantes' });
  },

  casas: function (s) {
    const puedeCrear = s.rol === 'pastor' || s.rol === 'supervisor';
    return titulo('Casas de Vida',
      puedeCrear
        ? '<button class="btn btn-ccmg btn-sm" onclick="return mostrarFormulario(\'formCasa\')"><i class="bi bi-plus-lg me-1"></i>Nueva casa</button>'
        : '') +
      (puedeCrear
        ? '<div id="formCasa" class="card p-3 border-0 shadow-sm mb-3 d-none">' +
          '<form onsubmit="return guardarCasa(event)">' +
          '<div class="row g-3">' +
          '<div class="col-md-6"><label class="form-label">Nombre de la Casa de Vida</label><input name="nombre" class="form-control" required></div>' +
          '<div class="col-md-6"><label class="form-label">Área</label><select name="area" class="form-select"><option>Norte</option><option>Centro</option><option>Sur</option></select></div>' +
          '<div class="col-md-6"><label class="form-label">Líder</label><input name="lider" class="form-control" required></div>' +
          '<div class="col-md-6"><label class="form-label">Supervisor</label><input name="supervisor" class="form-control" required></div>' +
          '<div class="col-md-4"><label class="form-label">Día de reunión</label><select name="dia" class="form-select"><option>Lunes</option><option>Martes</option><option>Miércoles</option><option>Jueves</option><option>Viernes</option><option>Sábado</option><option>Domingo</option></select></div>' +
          '<div class="col-md-4"><label class="form-label">Hora</label><input name="hora" class="form-control" placeholder="7:00 p. m." required></div>' +
          '<div class="col-md-4"><label class="form-label">Dirección</label><input name="direccion" class="form-control" required></div>' +
          '</div>' +
          '<div class="mt-3 d-flex gap-2"><button class="btn btn-ccmg">Guardar casa</button>' +
          '<button type="button" class="btn btn-light" onclick="return mostrarFormulario(\'formCasa\')">Cancelar</button></div>' +
          '</form></div>'
        : '') +
      tabla(['Casa de Vida', 'Área', 'Líder', 'Supervisor', 'Reunión', 'Miembros', 'Estado'], CASAS.map(function (c) {
        const miembros = PARTICIPANTES.filter(function (p) { return p.casa === c.nombre; }).length;
        return [
          esc(c.nombre), esc(c.area), esc(c.lider), esc(c.supervisor),
          esc(c.dia + ' · ' + c.hora), miembros,
          badge(c.estado, c.estado === 'Activa' ? 'ok' : 'pendiente')
        ];
      }));
  },

  asistencia: function () {
    return titulo('Registrar asistencia', '<span class="text-muted small">RF · Control de asistencia</span>') +
      '<div class="card p-3 border-0 shadow-sm mb-3">' +
      '<form onsubmit="return registrarAsistencia(event)">' +
      '<div class="row g-3 mb-3">' +
      '<div class="col-md-4"><label class="form-label">Casa de Vida</label><select class="form-select">' + opcionesCasas() + '</select></div>' +
      '<div class="col-md-4"><label class="form-label">Tipo de actividad</label><select class="form-select"><option>Reunión semanal</option><option>Visita</option><option>Actividad especial</option></select></div>' +
      '<div class="col-md-4"><label class="form-label">Fecha</label><input type="date" class="form-control" value="' + hoyISO() + '"></div>' +
      '</div>' +
      '<p class="small text-muted mb-2">Marca las personas presentes:</p>' +
      '<div class="row g-2">' +
      PARTICIPANTES.map(function (p, i) {
        return '<div class="col-md-6"><div class="form-check">' +
          '<input class="form-check-input" type="checkbox" id="as' + i + '" checked>' +
          '<label class="form-check-label" for="as' + i + '">' + esc(p.nombre) +
          ' <small class="text-muted">· ' + esc(p.casa) + '</small></label></div></div>';
      }).join('') +
      '</div>' +
      '<button class="btn btn-ccmg mt-3">Guardar asistencia</button>' +
      '</form></div>' +
      '<h6 class="mb-2">Historial de actividades</h6>' +
      tabla(['Casa de Vida', 'Fecha', 'Actividad', 'Asistentes', 'Invitados'], ACTIVIDADES.map(function (a) {
        return [esc(a.casa), a.fecha, esc(a.tipo), a.asistentes, a.invitados];
      }));
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
const MENU_CASAS = [
  { id: 'inicio', t: 'Inicio', i: 'speedometer2', r: ['pastor', 'supervisor', 'lider', 'apoyo'] },
  { id: 'participantes', t: 'Participantes', i: 'people', r: ['pastor', 'supervisor', 'lider', 'apoyo'] },
  { id: 'casas', t: 'Casas de Vida', i: 'houses', r: ['pastor', 'supervisor', 'lider', 'apoyo'] },
  { id: 'asistencia', t: 'Asistencia', i: 'check2-square', r: ['pastor', 'supervisor', 'lider', 'apoyo'] },
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
    defaultId: 'inicio',
    alMontar: function (id) {
      if (id === 'participantes') activarBuscador('buscarParticipante', 'tParticipantes');
    }
  });
});
