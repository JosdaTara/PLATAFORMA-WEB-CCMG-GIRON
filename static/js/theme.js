/* ===== CCMG PVA - Modo claro/oscuro ===== */
(function(){
  const root = document.documentElement;
  const STORAGE_KEY = 'ccmg-theme';
  const btn = document.getElementById('themeToggle');

  function aplicarTema(tema){
    if(tema === 'dark'){
      root.setAttribute('data-theme', 'dark');
    }else{
      root.removeAttribute('data-theme');
    }
    if(btn){
      btn.setAttribute('aria-pressed', tema === 'dark' ? 'true' : 'false');
      btn.innerHTML = tema === 'dark'
        ? '<i class="bi bi-sun"></i><span class="d-none d-lg-inline ms-1">Claro</span>'
        : '<i class="bi bi-moon-stars"></i><span class="d-none d-lg-inline ms-1">Oscuro</span>';
    }
  }

  const guardado = localStorage.getItem(STORAGE_KEY);
  if(guardado === 'dark' || guardado === 'light'){
    aplicarTema(guardado);
  }else if(window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches){
    aplicarTema('dark');
  }else{
    aplicarTema('light');
  }

  if(btn){
    btn.addEventListener('click', function(){
      const actual = root.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
      const nuevo = actual === 'dark' ? 'light' : 'dark';
      localStorage.setItem(STORAGE_KEY, nuevo);
      aplicarTema(nuevo);
    });
  }
})();
