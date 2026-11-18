(function () {
  function hideLoader() {
    var loader = document.getElementById('loader');
    if (loader) {
      loader.classList.add('hidden');
    }
  }

  // Ocultar en cuanto el DOM esté listo: sin espera artificial
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', hideLoader);
  } else {
    hideLoader();
  }

  // Al volver con «Atrás» desde la caché del navegador, la página no debe quedar tapada
  window.addEventListener('pageshow', hideLoader);

  // Fallback: ocultar después de 2 segundos máximo
  setTimeout(hideLoader, 2000);

  /* Ya no se tapa la página al hacer clic en un enlace ni al enviar un formulario:
     la navegación es rápida y los botones muestran su propio indicador de carga
     (interaccion.js), así el usuario no pierde de vista lo que estaba haciendo. */
})();
