/* =====================================================================
   CCMG PVA · Interacción común: debounce, skeletons de carga, loader en
   botones, búsqueda en vivo y autocompletado.

   Marcado que entiende este archivo:
     form[data-filtro-vivo]          filtros que se aplican solos (texto con debounce, selects al cambiar)
     input[data-autocompletar="url"] sugerencias JSON {resultados:[{id,nombre,detalle,url}]}
       data-autocompletar-destino="?participante={id}"  (opcional) a dónde ir al elegir
     [data-skeleton]                 contenedor (tbody o bloque) que pasa a skeleton al filtrar/paginar
     [data-skeleton-nav]             menú cuyos enlaces ponen en skeleton [data-skeleton-pagina]
     a[data-descarga]                descarga de archivo: spinner hasta que llega (cookie descarga_token)
     data-texto-cargando="…"         texto del botón mientras trabaja (por defecto «Procesando…»)
     data-sin-loader-boton           el botón o formulario no muestra loader
   ===================================================================== */
(function () {
  'use strict';

  var CCMG = window.CCMG = window.CCMG || {};
  var REDUCIR_MOVIMIENTO = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ------------------------------------------------------------ Debounce */
  function debounce(fn, ms) {
    var t;
    function envuelta() {
      var ctx = this, args = arguments;
      clearTimeout(t);
      t = setTimeout(function () { fn.apply(ctx, args); }, ms);
    }
    envuelta.cancelar = function () { clearTimeout(t); };
    return envuelta;
  }
  CCMG.debounce = debounce;

  /* ------------------------------------------------------------ Skeletons */
  function linea(clase) {
    return '<span class="skeleton-linea' + (clase ? ' ' + clase : '') + '"></span>';
  }
  var ANCHOS = ['', 'skeleton-linea--media', 'skeleton-linea--corta'];

  function filasSkeleton(columnas, filas) {
    var html = '';
    for (var f = 0; f < filas; f++) {
      html += '<tr class="skeleton-fila" aria-hidden="true">';
      for (var c = 0; c < columnas; c++) html += '<td>' + linea(ANCHOS[(f + c) % ANCHOS.length]) + '</td>';
      html += '</tr>';
    }
    return html;
  }

  function aplicarSkeleton(el) {
    if (!el || el.hasAttribute('aria-busy')) return;
    el._contenidoOriginal = el.innerHTML;
    el.setAttribute('aria-busy', 'true');
    if (el.tagName === 'TBODY') {
      var tabla = el.closest('table');
      var columnas = tabla ? tabla.querySelectorAll('thead th').length : 0;
      el.innerHTML = filasSkeleton(columnas || 4, 6);
    } else {
      var alto = Math.max(el.offsetHeight, 160);
      el.innerHTML = '<div class="d-grid gap-3 py-2" style="min-height:' + alto + 'px" aria-hidden="true">' +
        linea('skeleton-linea--titulo') +
        '<div class="row g-3">' + [0, 1, 2, 3].map(function () {
          return '<div class="col-6 col-xl-3"><div class="skeleton skeleton-tarjeta"></div></div>';
        }).join('') + '</div>' +
        linea() + linea('skeleton-linea--media') + linea('skeleton-linea--corta') + '</div>';
    }
  }

  function skeletonPagina(destino) {
    if (!destino || destino.hasAttribute('aria-busy')) return;
    destino._contenidoOriginal = destino.innerHTML;
    destino.setAttribute('aria-busy', 'true');
    destino.innerHTML = '<div aria-hidden="true">' + linea('skeleton-linea--titulo') +
      '<div class="row g-3">' + [0, 1, 2, 3].map(function () {
        return '<div class="col-6 col-xl-3"><div class="skeleton skeleton-tarjeta"></div></div>';
      }).join('') + '</div>' +
      '<div class="skeleton skeleton-tabla"></div></div>' +
      '<span class="visually-hidden" role="status">Cargando…</span>';
  }

  function skeletonResultados() {
    document.querySelectorAll('[data-skeleton]').forEach(aplicarSkeleton);
  }

  function quitarSkeletons() {
    document.querySelectorAll('[aria-busy="true"]').forEach(function (el) {
      if (el._contenidoOriginal !== undefined) {
        el.innerHTML = el._contenidoOriginal;
        delete el._contenidoOriginal;
      }
      el.removeAttribute('aria-busy');
    });
  }

  CCMG.skeleton = aplicarSkeleton;
  CCMG.skeletonPagina = skeletonPagina;
  CCMG.quitarSkeletons = quitarSkeletons;

  /* ------------------------------------------------------------ Loader en botones */
  function botonCargando(btn, texto) {
    if (!btn || btn.classList.contains('btn-cargando')) return;
    btn._htmlOriginal = btn.innerHTML;
    btn._anchoOriginal = btn.style.minWidth;
    btn.style.minWidth = btn.offsetWidth + 'px';      // evita que el botón cambie de tamaño
    btn.classList.add('btn-cargando');
    btn.setAttribute('aria-busy', 'true');
    var etiqueta = texto || btn.getAttribute('data-texto-cargando') || 'Procesando…';
    btn.innerHTML = '<span class="spinner-border spinner-border-sm me-1" aria-hidden="true"></span>' +
      '<span role="status">' + etiqueta + '</span>';
  }

  function restaurarBoton(btn) {
    if (!btn || !btn.classList.contains('btn-cargando')) return;
    btn.innerHTML = btn._htmlOriginal;
    btn.style.minWidth = btn._anchoOriginal || '';
    btn.classList.remove('btn-cargando');
    btn.removeAttribute('aria-busy');
    if (btn._deshabilitadoPorLoader) {
      btn.disabled = false;
      delete btn._deshabilitadoPorLoader;
    }
  }

  /* Para acciones hechas en JS: muestra el loader mientras dura la promesa (o un instante). */
  CCMG.botonCargando = function (btn, promesa, texto) {
    botonCargando(btn, texto);
    var p = promesa && typeof promesa.then === 'function'
      ? promesa
      : Promise.resolve();
    return p.then(function (v) { restaurarBoton(btn); return v; },
      function (e) { restaurarBoton(btn); throw e; });
  };
  CCMG.restaurarBoton = restaurarBoton;

  /* Envío de formularios: loader en el botón y bloqueo de doble envío.
     Se escucha en burbuja para respetar confirm() y validaciones que llamen a preventDefault. */
  document.addEventListener('submit', function (e) {
    var form = e.target;
    if (form.tagName !== 'FORM') return;
    if (e.defaultPrevented) return;

    if (form._enviando) {          // segundo clic mientras la página ya está cargando
      e.preventDefault();
      return;
    }
    form._enviando = true;

    var btn = e.submitter || form.querySelector('button[type="submit"], button:not([type]), input[type="submit"]');
    if (btn && !btn.hasAttribute('data-sin-loader-boton') && !form.hasAttribute('data-sin-loader-boton') && btn.tagName === 'BUTTON') {
      botonCargando(btn);
      // Se deshabilita después del envío para que el nombre/valor del botón viaje en el formulario.
      setTimeout(function () { btn.disabled = true; btn._deshabilitadoPorLoader = true; }, 0);
    }

    if ((form.method || 'get').toLowerCase() === 'get') skeletonResultados();
  });

  /* ------------------------------------------------------------ Descargas */
  function leerCookie(nombre) {
    var m = document.cookie.match(new RegExp('(?:^|; )' + nombre + '=([^;]*)'));
    return m ? decodeURIComponent(m[1]) : null;
  }
  function borrarCookie(nombre) {
    document.cookie = nombre + '=; Max-Age=0; path=/; SameSite=Lax';
  }
  function tokenAleatorio() {
    var a = new Uint32Array(4);
    (window.crypto || window.msCrypto).getRandomValues(a);
    return Array.prototype.map.call(a, function (n) { return n.toString(36); }).join('').slice(0, 24).padEnd(8, '0');
  }

  document.addEventListener('click', function (e) {
    var enlace = e.target.closest('a[data-descarga]');
    if (!enlace || e.defaultPrevented || e.button !== 0 || e.ctrlKey || e.metaKey || e.shiftKey) return;
    if (enlace.classList.contains('btn-cargando')) { e.preventDefault(); return; }
    e.preventDefault();

    var token = tokenAleatorio();
    var url = new URL(enlace.href, location.href);
    url.searchParams.set('descarga_token', token);
    botonCargando(enlace, enlace.getAttribute('data-texto-cargando') || 'Generando…');

    var inicio = Date.now();
    var sondeo = setInterval(function () {
      var listo = leerCookie('descarga_token') === token;
      if (listo || Date.now() - inicio > 30000) {
        clearInterval(sondeo);
        if (listo) borrarCookie('descarga_token');
        restaurarBoton(enlace);
      }
    }, 250);
    location.href = url.toString();
  });

  /* ------------------------------------------------------------ Navegación con skeleton */
  function esNavegacionNormal(e, enlace) {
    var href = enlace.getAttribute('href') || '';
    return !(e.defaultPrevented || e.button !== 0 || e.ctrlKey || e.metaKey || e.shiftKey || e.altKey ||
      !href || href.charAt(0) === '#' || /^(mailto:|tel:|javascript:)/.test(href) ||
      enlace.target === '_blank' || enlace.hasAttribute('download') || enlace.hasAttribute('data-descarga'));
  }

  document.addEventListener('click', function (e) {
    var enlace = e.target.closest('a');
    if (!enlace || !esNavegacionNormal(e, enlace)) return;
    if (enlace.closest('[data-skeleton-nav]')) {
      skeletonPagina(document.querySelector('[data-skeleton-pagina]'));
    } else if (enlace.closest('.pagination')) {
      skeletonResultados();
    }
  });

  /* ------------------------------------------------------------ Búsqueda en vivo */
  /* El foco se recupera tras recargar con un marcador en el fragmento de la URL (#foco-<campo>),
     que se quita al llegar. No se usa almacenamiento del navegador. */
  var PREFIJO_FOCO = '#foco-';

  function restaurarFoco() {
    if (location.hash.indexOf(PREFIJO_FOCO) !== 0) return;
    var nombre = decodeURIComponent(location.hash.slice(PREFIJO_FOCO.length));
    history.replaceState(null, '', location.pathname + location.search);
    var input = document.querySelector('form[data-filtro-vivo] [name="' + nombre.replace(/"/g, '') + '"]');
    if (!input) return;
    input.focus();
    try {
      var fin = input.value.length;
      input.setSelectionRange(fin, fin);
    } catch (err) { /* tipos de input sin selección */ }
  }

  function enviarFiltro(form, origen) {
    var pagina = form.querySelector('[name="page"]');
    if (pagina) pagina.disabled = true;     // al cambiar el filtro se vuelve a la primera página
    // En GET el fragmento de la acción se conserva al navegar: sirve para volver a enfocar el campo.
    if (origen && origen.name && /^(text|search)$/.test(origen.type)) {
      form.action = location.pathname + PREFIJO_FOCO + encodeURIComponent(origen.name);
    }
    if (form.requestSubmit) form.requestSubmit();
    else form.submit();
  }

  function iniciarFiltroVivo(form) {
    form.querySelectorAll('input[type="text"], input[type="search"], input:not([type])').forEach(function (input) {
      if (input.hasAttribute('data-autocompletar')) return;   // ese campo sugiere; el filtro se aplica con Enter
      var ultimo = input.value.trim();
      var aplicar = debounce(function () {
        var valor = input.value.trim();
        if (valor === ultimo) return;
        if (valor.length === 1) return;     // una sola letra trae demasiados resultados
        ultimo = valor;
        enviarFiltro(form, input);
      }, 400);
      input.addEventListener('input', aplicar);
      form.addEventListener('submit', aplicar.cancelar);
    });
    form.querySelectorAll('select, input[type="date"], input[type="month"], input[type="checkbox"]').forEach(function (campo) {
      campo.addEventListener('change', function () { enviarFiltro(form, campo); });
    });
  }

  /* ------------------------------------------------------------ Autocompletado */
  var contadorAuto = 0;

  function escapar(v) {
    return String(v == null ? '' : v).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function iniciarAutocompletar(input) {
    var url = input.getAttribute('data-autocompletar');
    var destino = input.getAttribute('data-autocompletar-destino');
    var id = 'auto-' + (++contadorAuto);

    var envoltura = document.createElement('div');
    envoltura.className = 'autocompletar';
    input.parentNode.insertBefore(envoltura, input);
    envoltura.appendChild(input);

    var lista = document.createElement('ul');
    lista.id = id;
    lista.className = 'autocompletar-lista';
    lista.setAttribute('role', 'listbox');
    lista.hidden = true;
    envoltura.appendChild(lista);

    input.setAttribute('role', 'combobox');
    input.setAttribute('aria-autocomplete', 'list');
    input.setAttribute('aria-expanded', 'false');
    input.setAttribute('aria-controls', id);
    input.setAttribute('autocomplete', 'off');

    var resultados = [];
    var activo = -1;
    var peticion = null;

    function abrir() { lista.hidden = false; input.setAttribute('aria-expanded', 'true'); }
    function cerrar() {
      lista.hidden = true;
      input.setAttribute('aria-expanded', 'false');
      input.removeAttribute('aria-activedescendant');
      activo = -1;
    }

    function marcar(i) {
      var opciones = lista.querySelectorAll('[role="option"]');
      opciones.forEach(function (o, n) { o.setAttribute('aria-selected', n === i ? 'true' : 'false'); });
      activo = i;
      if (i >= 0 && opciones[i]) {
        input.setAttribute('aria-activedescendant', opciones[i].id);
        opciones[i].scrollIntoView({ block: 'nearest' });
      } else {
        input.removeAttribute('aria-activedescendant');
      }
    }

    function elegir(i) {
      var r = resultados[i];
      if (!r) return;
      cerrar();
      input.value = r.nombre;
      var ir = destino ? destino.replace('{id}', encodeURIComponent(r.id)) : r.url;
      skeletonResultados();
      location.href = new URL(ir, location.href).toString();
    }

    function pintar() {
      if (!resultados.length) {
        lista.innerHTML = '<li class="autocompletar-vacio" role="presentation">Sin coincidencias. Pulsa Enter para buscar en la lista.</li>';
      } else {
        lista.innerHTML = resultados.map(function (r, i) {
          return '<li class="autocompletar-opcion" role="option" id="' + id + '-' + i + '" aria-selected="false" data-i="' + i + '">' +
            '<span>' + escapar(r.nombre) + '</span>' + (r.detalle ? '<small>' + escapar(r.detalle) + '</small>' : '') + '</li>';
        }).join('');
      }
      activo = -1;
      abrir();
    }

    var buscar = debounce(function () {
      var q = input.value.trim();
      if (peticion) peticion.abort();
      if (q.length < 2) { cerrar(); return; }

      lista.innerHTML = '<li class="autocompletar-cargando" role="presentation" aria-label="Buscando…">' +
        linea() + linea('skeleton-linea--media') + linea('skeleton-linea--corta') + '</li>';
      abrir();

      peticion = new AbortController();
      fetch(url + (url.indexOf('?') === -1 ? '?' : '&') + 'q=' + encodeURIComponent(q), {
        headers: { 'Accept': 'application/json', 'X-Requested-With': 'XMLHttpRequest' },
        credentials: 'same-origin',
        signal: peticion.signal
      })
        .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
        .then(function (datos) {
          if (input.value.trim() !== q) return;     // el usuario siguió escribiendo
          resultados = datos.resultados || [];
          pintar();
        })
        .catch(function (err) { if (err.name !== 'AbortError') cerrar(); });
    }, 300);

    input.addEventListener('input', buscar);
    input.addEventListener('keydown', function (e) {
      if (lista.hidden) return;
      var total = resultados.length;
      if (e.key === 'ArrowDown' && total) { e.preventDefault(); marcar((activo + 1) % total); }
      else if (e.key === 'ArrowUp' && total) { e.preventDefault(); marcar(activo <= 0 ? total - 1 : activo - 1); }
      else if (e.key === 'Enter' && activo >= 0) { e.preventDefault(); elegir(activo); }
      else if (e.key === 'Escape') { e.preventDefault(); cerrar(); }
      else if (e.key === 'Enter') { buscar.cancelar(); cerrar(); }   // deja que el formulario filtre
    });
    lista.addEventListener('mousedown', function (e) {
      var op = e.target.closest('[role="option"]');
      if (!op) return;
      e.preventDefault();          // que el input no pierda el foco antes del clic
      elegir(Number(op.getAttribute('data-i')));
    });
    input.addEventListener('blur', function () { setTimeout(cerrar, 120); });

    // Al vaciar el campo se quita el filtro de texto sin tener que pulsar «Filtrar».
    var formulario = input.form;
    var inicial = input.value.trim();
    if (formulario && formulario.hasAttribute('data-filtro-vivo')) {
      input.addEventListener('input', debounce(function () {
        if (input.value.trim() === '' && inicial !== '') { inicial = ''; enviarFiltro(formulario, input); }
      }, 400));
    }
  }

  /* ------------------------------------------------------------ Tablas apiladas en el celular
     Copia el texto del encabezado de cada columna en data-label de sus celdas, para que el CSS
     muestre cada fila como una tarjeta «etiqueta: valor» por debajo de 576px. Funciona también
     con las tablas que se dibujan después (panel, filtros en vivo). Excluir: data-sin-apilar. */
  function etiquetarTabla(tabla) {
    var envoltura = tabla.closest('.table-responsive');
    if (!envoltura || envoltura.hasAttribute('data-sin-apilar') || !tabla.closest('.contenido')) return;
    var titulos = Array.prototype.map.call(tabla.querySelectorAll('thead th'), function (th) {
      return th.textContent.trim();
    });
    if (!titulos.length) return;
    envoltura.classList.add('tabla-apilada');
    tabla.querySelectorAll('tbody tr').forEach(function (tr) {
      Array.prototype.forEach.call(tr.children, function (td, i) {
        if (titulos[i] && !td.hasAttribute('colspan')) td.setAttribute('data-label', titulos[i]);
      });
    });
  }
  function etiquetarTablas(raiz) {
    (raiz || document).querySelectorAll('.table-responsive table').forEach(etiquetarTabla);
  }
  CCMG.etiquetarTablas = etiquetarTablas;

  /* ------------------------------------------------------------ Arranque */
  function iniciar() {
    document.querySelectorAll('form[data-filtro-vivo]').forEach(iniciarFiltroVivo);
    document.querySelectorAll('input[data-autocompletar]').forEach(iniciarAutocompletar);
    restaurarFoco();
    etiquetarTablas();
    var contenido = document.querySelector('.contenido');
    if (contenido && window.MutationObserver) {
      var pendiente = false;
      new MutationObserver(function () {
        if (pendiente) return;
        pendiente = true;
        requestAnimationFrame(function () { pendiente = false; etiquetarTablas(contenido); });
      }).observe(contenido, { childList: true, subtree: true });
    }
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', iniciar);
  else iniciar();

  /* Al volver con «Atrás» el navegador puede mostrar la página congelada tal como quedó:
     se devuelven botones, formularios y tablas a su estado normal. */
  window.addEventListener('pageshow', function (e) {
    if (!e.persisted) return;
    document.querySelectorAll('.btn-cargando').forEach(restaurarBoton);
    document.querySelectorAll('form').forEach(function (f) { f._enviando = false; });
    quitarSkeletons();
  });
})();
