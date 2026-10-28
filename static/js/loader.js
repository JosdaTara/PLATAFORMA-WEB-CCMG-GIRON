(function () {
  function showLoader() {
    var loader = document.getElementById('loader');
    if (loader) {
      loader.classList.remove('hidden');
    }
  }

  function hideLoader() {
    var loader = document.getElementById('loader');
    if (loader) {
      setTimeout(function () {
        loader.classList.add('hidden');
      }, 400);
    }
  }

  window.addEventListener('load', hideLoader);
  window.addEventListener('beforeunload', showLoader);

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

    showLoader();
  });

  document.addEventListener('submit', function (e) {
    var form = e.target;
    if (form.tagName === 'FORM') {
      showLoader();
    }
  });
})();