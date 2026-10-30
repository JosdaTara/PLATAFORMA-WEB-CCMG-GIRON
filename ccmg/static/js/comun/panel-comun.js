/* =====================================================================
   CCMG PVA · Utilidades compartidas de los paneles de módulo
   Requiere: js/cuentas/auth.js cargado antes (usa requiereSesion y ROLES_INFO)
   ===================================================================== */

/* Escapa texto para insertarlo como HTML */
function esc(v) {
  return String(v === null || v === undefined ? '' : v).replace(/[&<>"']/g, function (c) {
    return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
  });
}

/* Tabla reutilizable */
function tabla(headers, filas, opciones) {
  opciones = opciones || {};
  const id = opciones.id ? ' id="' + opciones.id + '"' : '';
  const vacio = filas.length
    ? ''
    : '<tr><td colspan="' + headers.length + '" class="text-center text-muted py-4">Sin registros todavía.</td></tr>';

  return '<div class="table-responsive bg-white rounded shadow-sm">' +
    '<table class="table table-hover align-middle mb-0"' + id + '>' +
    '<thead><tr>' + headers.map(function (h) { return '<th>' + h + '</th>'; }).join('') + '</tr></thead>' +
    '<tbody>' + vacio + filas.map(function (r) {
      return '<tr>' + r.map(function (c) { return '<td>' + c + '</td>'; }).join('') + '</tr>';
    }).join('') + '</tbody></table></div>';
}

/* Encabezado de vista */
function titulo(t, extra) {
  return '<div class="d-flex flex-wrap justify-content-between align-items-center gap-2 mb-3">' +
    '<h3 class="m-0">' + t + '</h3>' + (extra || '') + '</div>';
}

/* Tarjeta de indicador */
function stat(etiqueta, valor, icono) {
  return '<div class="col-6 col-xl-3">' +
    '<div class="card stat p-3 h-100"><div class="d-flex justify-content-between align-items-start">' +
    '<div><small class="text-muted">' + etiqueta + '</small><div class="num">' + valor + '</div></div>' +
    '<i class="bi bi-' + icono + ' icono"></i></div></div></div>';
}

/* Etiqueta de estado */
function badge(texto, tipo) {
  const clases = {
    ok: 'bg-success-subtle text-success-emphasis',
    pendiente: 'bg-warning-subtle text-warning-emphasis',
    info: 'bg-info-subtle text-info-emphasis',
    neutro: 'bg-secondary-subtle text-secondary-emphasis'
  };
  return '<span class="badge rounded-pill ' + (clases[tipo] || clases.neutro) + '">' + esc(texto) + '</span>';
}

/* Aviso flotante (reemplaza a alert) */
function avisar(mensaje) {
  let el = document.getElementById('toastCcmg');
  if (!el) {
    el = document.createElement('div');
    el.id = 'toastCcmg';
    el.className = 'toast-ccmg';
    el.setAttribute('role', 'status');
    el.setAttribute('aria-live', 'polite');
    document.body.appendChild(el);
  }
  el.textContent = mensaje;
  el.classList.add('show');
  clearTimeout(el._temporizador);
  el._temporizador = setTimeout(function () { el.classList.remove('show'); }, 2800);
}

/* Vuelve a renderizar la vista actual (tras guardar datos) */
function refrescar() {
  window.dispatchEvent(new Event('hashchange'));
}

/* Muestra u oculta un formulario en línea */
function mostrarFormulario(id) {
  const el = document.getElementById(id);
  if (el) el.classList.toggle('d-none');
  return false;
}

/* Estado vacío */
function vacio(icono, texto) {
  return '<div class="empty-state"><i class="bi bi-' + icono + '"></i><p class="mb-0">' + texto + '</p></div>';
}

/* Devuelve la fecha de hoy en formato aaaa-mm-dd */
function hoyISO() {
  return new Date().toISOString().slice(0, 10);
}

/* Filtro de búsqueda en una tabla ya renderizada */
function activarBuscador(inputId, tablaId) {
  const input = document.getElementById(inputId);
  const table = document.getElementById(tablaId);
  if (!input || !table) return;
  input.addEventListener('input', function () {
    const q = input.value.toLowerCase().trim();
    table.querySelectorAll('tbody tr').forEach(function (tr) {
      tr.style.display = tr.textContent.toLowerCase().indexOf(q) !== -1 ? '' : 'none';
    });
  });
}

/* ---------------------------------------------------------------------
   Arranque del panel de módulo
   cfg = {
     modulo: 'CASAS_VIDA' | 'ESCUELAS_FORMACION',
     menu:  [{ id, t, i, r: [roles] }],
     vistas:{ id: fn(sesion) -> html },
     defaultId: 'inicio',
     alMontar: function(id, sesion)  // opcional
   }
   --------------------------------------------------------------------- */
function iniciarPanelModulo(cfg) {
  const sesion = requiereSesion(cfg.modulo);
  if (!sesion) return;                    // requiereSesion ya redirigió

  const sidebar = document.getElementById('sidebar');
  const menu = document.getElementById('menu');
  const vista = document.getElementById('vista');
  const toggle = document.getElementById('toggle');
  const salir = document.getElementById('salir');

  /* Datos del usuario en la barra superior */
  const elNombre = document.getElementById('nombre');
  const elRol = document.getElementById('rolTxt');
  if (elNombre) elNombre.textContent = sesion.nombre;
  if (elRol) {
    const info = ROLES_INFO[sesion.rol];
    elRol.textContent = info ? info.nombre : sesion.rol;
  }

  /* Solo el Pastor puede cambiar de módulo */
  const cambiar = document.getElementById('cambiarModulo');
  if (cambiar) cambiar.classList.toggle('d-none', sesion.rol !== 'pastor');

  /* Menú permitido según el rol (control de acceso) */
  let permitidos = cfg.menu.filter(function (m) { return m.r.indexOf(sesion.rol) !== -1; });

  /* Ofrendas: módulo aparte para el Pastor o el responsable que él autorice (RN14) */
  if (sesion.ofrendas) {
    const perfil = permitidos.findIndex(function (m) { return m.id === 'perfil'; });
    const ofrendas = { id: 'ofrendas', t: 'Ofrendas', i: 'cash-coin', url: sesion.ofrendas, r: [sesion.rol] };
    permitidos.splice(perfil === -1 ? permitidos.length : perfil, 0, ofrendas);
  }

  /* Las secciones con `url` son páginas de Django; el resto se pinta aquí */
  menu.innerHTML = permitidos.map(function (m) {
    return '<a href="' + (m.url || '#' + m.id) + '" data-id="' + m.id + '"><i class="bi bi-' + m.i + ' me-2"></i>' + m.t + '</a>';
  }).join('');
  permitidos = permitidos.filter(function (m) { return !m.url; });

  const ir = function () {
    let id = (location.hash || '').slice(1);

    if (!permitidos.some(function (m) { return m.id === id; })) {
      const existeDefault = permitidos.some(function (m) { return m.id === cfg.defaultId; });
      id = existeDefault ? cfg.defaultId : (permitidos[0] ? permitidos[0].id : '');
      if (location.hash !== '#' + id) { location.hash = '#' + id; return; }
    }

    menu.querySelectorAll('a').forEach(function (a) {
      a.classList.toggle('active', a.dataset.id === id);
    });

    const fn = cfg.vistas[id];
    vista.innerHTML = typeof fn === 'function' ? fn(sesion) : '';
    vista.classList.remove('vista-entra');
    void vista.offsetWidth;               // reinicia la animación
    vista.classList.add('vista-entra');

    if (sidebar) sidebar.classList.remove('abierto');
    if (typeof cfg.alMontar === 'function') cfg.alMontar(id, sesion);
  };

  window.addEventListener('hashchange', ir);
  if (toggle) toggle.addEventListener('click', function () { sidebar.classList.toggle('abierto'); });
  if (salir) salir.addEventListener('click', function (e) { e.preventDefault(); cerrarSesion(); });

  ir();
}
