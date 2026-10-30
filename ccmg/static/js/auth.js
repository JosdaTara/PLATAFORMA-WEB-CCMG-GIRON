/* ===== CCMG PVA - Autenticación ===== */

/* Login unificado: un solo formulario */
function iniciarLogin() {
  const form = document.getElementById('formLogin');
  if (!form) return;

  const usuario = document.getElementById('usuario');
  const clave = document.getElementById('clave');
  const error = document.getElementById('error');

  form.onsubmit = function (ev) {
    // El envío se realiza al servidor (Django). Solo validación mínima de UI.
    const u = usuario ? usuario.value.trim() : '';
    const c = clave ? clave.value : '';

    if (!u || !c) {
      ev.preventDefault();
      if (error) {
        error.textContent = 'Ingresa tu usuario y contraseña.';
        error.classList.remove('d-none');
      }
      return;
    }

    if (c.length < 15) {
      ev.preventDefault();
      if (error) {
        error.textContent = 'La contraseña debe tener al menos 15 caracteres.';
        error.classList.remove('d-none');
      }
      return;
    }
  };
}

function cerrarSesion() {
  const form = document.getElementById('logoutForm');
  if (form) {
    form.submit();
    return;
  }
  const f = document.createElement('form');
  f.method = 'POST';
  f.action = '/cuentas/logout/';

  const csrf = document.querySelector('input[name="csrfmiddlewaretoken"]');
  if (csrf) {
    const input = document.createElement('input');
    input.type = 'hidden';
    input.name = 'csrfmiddlewaretoken';
    input.value = csrf.value;
    f.appendChild(input);
  }

  document.body.appendChild(f);
  f.submit();
}
