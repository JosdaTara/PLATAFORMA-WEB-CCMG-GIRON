/* ===== CCMG PVA - Modo claro/oscuro =====
   El tema inicial lo aplica templates/_tema.html antes de pintar. Este archivo
   atiende los botones [data-tema-toggle] y recuerda la preferencia del usuario. */
(function () {
  const root = document.documentElement;
  const STORAGE_KEY = 'ccmg-theme';

  function temaActual() {
    return root.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
  }

  function pintarBotones(tema) {
    const oscuro = tema === 'dark';
    document.querySelectorAll('[data-tema-toggle]').forEach(function (btn) {
      btn.setAttribute('aria-pressed', oscuro ? 'true' : 'false');
      btn.setAttribute('aria-label', oscuro ? 'Cambiar a modo claro' : 'Cambiar a modo oscuro');
      btn.setAttribute('title', oscuro ? 'Modo claro' : 'Modo oscuro');
      const texto = btn.hasAttribute('data-tema-texto')
        ? '<span class="d-none d-lg-inline ms-1">' + (oscuro ? 'Claro' : 'Oscuro') + '</span>'
        : '';
      btn.innerHTML = '<i class="bi bi-' + (oscuro ? 'sun' : 'moon-stars') + '" aria-hidden="true"></i>' + texto;
    });
  }

  function aplicarTema(tema) {
    root.setAttribute('data-theme', tema);
    root.setAttribute('data-bs-theme', tema);
    pintarBotones(tema);
  }

  function iniciar() {
    pintarBotones(temaActual());
    document.querySelectorAll('[data-tema-toggle]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        const nuevo = temaActual() === 'dark' ? 'light' : 'dark';
        try { localStorage.setItem(STORAGE_KEY, nuevo); } catch (e) {}
        aplicarTema(nuevo);
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', iniciar);
  } else {
    iniciar();
  }
})();
