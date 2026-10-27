/* ===== CCMG PVA - Autenticación y redirección por módulo ===== */
/* Regla: Casas de Vida y Escuelas de Formación son módulos independientes.
   Solo el Pastor tiene acceso a ambos. */

const ROLES_INFO = {
  pastor:     { nombre: 'Pastor / Administrador del Sistema', modulo: 'AMBOS' },
  supervisor: { nombre: 'Supervisor de Área',                 modulo: 'CASAS_VIDA' },
  lider:      { nombre: 'Líder de Casa de Vida',              modulo: 'CASAS_VIDA' },
  apoyo:      { nombre: 'Aprendiz / Anfitrión / Maestro de Niños', modulo: 'CASAS_VIDA' },
  coord:      { nombre: 'Coordinador de Formación',           modulo: 'ESCUELAS_FORMACION' }
};

/* Devuelve el panel inicial según el rol (RNF04) */
function panelPorRol(rol) {
  const info = ROLES_INFO[rol];
  if (!info) return 'login.html';
  if (info.modulo === 'AMBOS') return 'selector-modulo.html';
  if (info.modulo === 'CASAS_VIDA') return 'panel-casas-vida.html';
  return 'panel-escuelas-formacion.html';
}

/* Login unificado: un solo formulario, redirección por rol */
function iniciarLogin() {
  const form = document.getElementById('formLogin');
  if (!form) return;

  const usuario = document.getElementById('usuario');
  const clave = document.getElementById('clave');
  const error = document.getElementById('error');
  const selRol = document.getElementById('rol');

  if (selRol) {
    selRol.innerHTML = Object.entries(ROLES_INFO)
      .map(([k, v]) => `<option value="${k}">${v.nombre}</option>`)
      .join('');
  }

  form.onsubmit = function (ev) {
    ev.preventDefault();

    const u = usuario ? usuario.value.trim() : '';
    const c = clave ? clave.value : '';

    if (!u || !c) {
      if (error) {
        error.textContent = 'Ingresa tu usuario y contraseña.';
        error.classList.remove('d-none');
      }
      return;
    }

    // RNF19: política básica de contraseñas (mínimo 8 caracteres)
    if (c.length < 8) {
      if (error) {
        error.textContent = 'La contraseña debe tener al menos 8 caracteres.';
        error.classList.remove('d-none');
      }
      return;
    }

    // RNF20: bloqueo tras 5 intentos fallidos (demo en localStorage)
    const intentosKey = 'ccmg_intentos';
    const bloqueadoKey = 'ccmg_bloqueado_hasta';
    const ahora = Date.now();
    const bloqueadoHasta = Number(localStorage.getItem(bloqueadoKey) || 0);
    if (bloqueadoHasta && ahora < bloqueadoHasta) {
      const minutos = Math.ceil((bloqueadoHasta - ahora) / 60000);
      if (error) {
        error.textContent = 'Cuenta bloqueada por intentos fallidos. Intenta nuevamente en ' + minutos + ' minuto(s).';
        error.classList.remove('d-none');
      }
      return;
    }

    // En demo se acepta cualquier usuario/contraseña válido; se registra intento exitoso
    localStorage.removeItem(intentosKey);
    localStorage.removeItem(bloqueadoKey);

    const rol = selRol ? selRol.value : 'pastor';
    sessionStorage.setItem('ccmg', JSON.stringify({ nombre: u, rol: rol }));
    window.location.href = panelPorRol(rol);
  };
}

/* Guardia de sesión. Recibe el módulo esperado: 'CASAS_VIDA' | 'ESCUELAS_FORMACION' */
function requiereSesion(moduloEsperado) {
  const raw = sessionStorage.getItem('ccmg');
  if (!raw) {
    window.location.href = 'login.html';
    return null;
  }
  const sesion = JSON.parse(raw);
  const info = ROLES_INFO[sesion.rol];

  if (!info) {
    sessionStorage.removeItem('ccmg');
    window.location.href = 'login.html';
    return null;
  }

  // El Pastor puede entrar a ambos módulos
  if (info.modulo === 'AMBOS') return sesion;

  // Un usuario de otro módulo no puede acceder (acceso cruzado bloqueado)
  if (info.modulo !== moduloEsperado) {
    window.location.href = panelPorRol(sesion.rol);
    return null;
  }

  return sesion;
}

function cerrarSesion() {
  sessionStorage.removeItem('ccmg');
  window.location.href = 'login.html';
}
