(function () {
  function hideLoader() {
    var loader = document.getElementById('loader');
    if (loader) {
      loader.classList.add('hidden');
    }
  }

  // Ocultar cuando el DOM esté listo
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      setTimeout(hideLoader, 300);
    });
  } else {
    setTimeout(hideLoader, 300);
  }

  // Fallback: ocultar después de 2 segundos máximo
  setTimeout(hideLoader, 2000);

  window.addEventListener('beforeunload', function () {
    var loader = document.getElementById('loader');
    if (loader) {
      loader.classList.remove('hidden');
    }
  });

  document.addEventListener('click', function (e) {
    var link = e.target.closest('a');
    if (!link) return;

    var href = link.getAttribute('href');
    if (!href) return;

    if (href.indexOf('#') === 0) return;
    if (href.indexOf('mailto:') === 0) return;
    if (href.indexOf('tel:') === 0) return;
    if (link.target === '_blank') return;
    if (href.indexOf('javascript:') === 0) return;
    if (link.hasAttribute('data-no-loader')) return;

    var loader = document.getElementById('loader');
    if (loader) loader.classList.remove('hidden');
  });

  document.addEventListener('submit', function (e) {
    var form = e.target;
    if (form.tagName !== 'FORM') return;
    if (form.hasAttribute('data-no-loader')) return;

    var loader = document.getElementById('loader');
    if (loader) loader.classList.remove('hidden');
  });
})();
