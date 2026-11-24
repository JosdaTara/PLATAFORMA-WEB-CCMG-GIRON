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
    '<h1 class="m-0">' + t + '</h1>' + (extra || '') + '</div>';
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

/* ------------------------------ Mi perfil ------------------------------
   Común a los dos módulos. El nombre se guarda en el servidor (cuentas:perfil);
   la contraseña se cambia en su propia página (cuentas:cambiar_password). */
function vistaPerfil(s, modulo) {
  const info = (typeof ROLES_INFO !== 'undefined') ? ROLES_INFO[s.rol] : null;
  return titulo('Mi perfil') +
    '<div class="card p-4 border-0 shadow-sm" style="max-width:560px">' +
    '<form id="formPerfil" novalidate onsubmit="guardarPerfilComun(event)">' +
    '<div class="mb-3"><label class="form-label" for="perfilNombre">Nombre completo</label>' +
    '<input class="form-control" id="perfilNombre" name="nombre" maxlength="150" required autocomplete="name" value="' + esc(s.nombre) + '">' +
    '<div class="invalid-feedback" id="perfilError"></div></div>' +
    '<div class="mb-3"><label class="form-label" for="perfilRol">Rol</label><input class="form-control" id="perfilRol" value="' + esc(info ? info.nombre : (s.rolNombre || s.rol)) + '" disabled></div>' +
    '<div class="mb-4"><label class="form-label" for="perfilModulo">Módulo</label><input class="form-control" id="perfilModulo" value="' + esc(modulo) + '" disabled></div>' +
    '<div class="d-flex flex-wrap gap-2">' +
    '<button type="submit" class="btn btn-ccmg" id="perfilGuardar">Guardar cambios</button>' +
    (s.urlCambiarPassword ? '<a class="btn btn-outline-secondary" href="' + esc(s.urlCambiarPassword) + '"><i class="bi bi-key me-1" aria-hidden="true"></i>Cambiar contraseña</a>' : '') +
    '</div></form></div>';
}

function guardarPerfilComun(evento) {
  if (evento) evento.preventDefault();
  const sesion = sesionActual();
  const input = document.getElementById('perfilNombre');
  const error = document.getElementById('perfilError');
  const btn = document.getElementById('perfilGuardar');
  const token = document.querySelector('#logoutForm input[name="csrfmiddlewaretoken"]');
  if (!sesion || !input || !sesion.urlPerfil || !token) return;

  const mostrarError = function (texto) {
    input.classList.add('is-invalid');
    if (error) error.textContent = texto;
    input.focus();
  };
  input.classList.remove('is-invalid');
  const nombre = input.value.trim();
  if (!nombre) { mostrarError('Escribe tu nombre completo.'); return; }

  const datos = new URLSearchParams({ nombre: nombre });
  const peticion = fetch(sesion.urlPerfil, {
    method: 'POST',
    headers: { 'X-CSRFToken': token.value, 'X-Requested-With': 'XMLHttpRequest' },
    body: datos,
    credentials: 'same-origin'
  }).then(function (r) {
    return r.json().catch(function () { return {}; }).then(function (j) { return { ok: r.ok, datos: j }; });
  });
  const listo = (btn && window.CCMG) ? CCMG.botonCargando(btn, peticion, 'Guardando…') : peticion;
  listo.then(function (res) {
    if (!res.ok || !res.datos.nombre) {
      mostrarError(res.datos.error || 'No se pudo guardar. Intenta de nuevo.');
      return;
    }
    // Refleja el nombre guardado en la barra superior y en los datos de sesión de la página.
    sesion.nombre = res.datos.nombre;
    const el = document.getElementById('ccmg-sesion');
    if (el) el.textContent = JSON.stringify(sesion);
    const barra = document.getElementById('nombre');
    if (barra) barra.textContent = sesion.nombre;
    input.value = sesion.nombre;
    avisar('Nombre actualizado.');
  }).catch(function () {
    mostrarError('No se pudo guardar. Revisa tu conexión e intenta de nuevo.');
  });
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

/* Convierte aaaa-mm-dd en dd/mm/aaaa para mostrar */
function fechaCorta(iso) {
  const p = String(iso || '').split('-');
  return p.length === 3 ? p[2] + '/' + p[1] + '/' + p[0] : esc(iso);
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
  const filtrar = function () {
    const q = input.value.toLowerCase().trim();
    table.querySelectorAll('tbody tr').forEach(function (tr) {
      tr.style.display = tr.textContent.toLowerCase().indexOf(q) !== -1 ? '' : 'none';
    });
  };
  /* Debounce: no se recorre la tabla en cada tecla, sino al dejar de escribir */
  input.addEventListener('input', window.CCMG && CCMG.debounce ? CCMG.debounce(filtrar, 250) : filtrar);
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
    elRol.textContent = sesion.rolNombre || (info ? info.nombre : sesion.rol);
  }

  /* Solo el Pastor puede cambiar de módulo */
  const cambiar = document.getElementById('cambiarModulo');
  if (cambiar) cambiar.classList.toggle('d-none', sesion.rol !== 'pastor');

  /* Menú permitido según el rol (control de acceso) */
  let permitidos = cfg.menu.filter(function (m) { return m.r.indexOf(sesion.rol) !== -1; });

  /* Bitácora de auditoría: solo el Super Administrador */
  if (sesion.auditoria) {
    const pos = permitidos.findIndex(function (m) { return m.id === 'perfil'; });
    permitidos.splice(pos === -1 ? permitidos.length : pos, 0,
      { id: 'auditoria', t: 'Auditoría', i: 'journal-text', url: sesion.auditoria, r: [sesion.rol] });
  }

  /* Ofrendas: módulo aparte para el Pastor o el responsable que él autorice (RN14) */
  if (sesion.ofrendas) {
    const perfil = permitidos.findIndex(function (m) { return m.id === 'perfil'; });
    const ofrendas = { id: 'ofrendas', t: 'Ofrendas', i: 'cash-coin', url: sesion.ofrendas, r: [sesion.rol] };
    permitidos.splice(perfil === -1 ? permitidos.length : perfil, 0, ofrendas);
  }

  /* Las secciones con `url` son páginas de Django; el resto se pinta aquí.
     Mientras carga la página de Django se muestra un skeleton en la vista (no el overlay). */
  menu.innerHTML = permitidos.map(function (m) {
    return '<a href="' + (m.url || '#' + m.id) + '" data-id="' + m.id + '"' + (m.url ? ' data-no-loader' : '') +
      '><i class="bi bi-' + m.i + ' me-2"></i>' + m.t + '</a>';
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
