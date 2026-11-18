
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".nav-link").forEach(link => {
    link.addEventListener("click", function() {
      document.querySelectorAll(".nav-link").forEach(l => l.classList.remove("active"));
      this.classList.add("active");
    });
  });

  const loader = document.getElementById("loader");
  if (loader) {
    setTimeout(() => {
      loader.classList.add("hidden");
      setTimeout(() => loader.remove(), 300);
    }, 400);
  }

  const navLinks = document.querySelectorAll(".nav-link-close");
  const navCollapse = document.getElementById("navbarNav");
  navLinks.forEach(l => l.addEventListener("click", () => {
    if (window.innerWidth < 992 && navCollapse?.classList.contains("show")) {
      const bs = bootstrap.Collapse.getOrCreateInstance(navCollapse);
      bs.hide();
    }
  }));

  /* ---- Barra inferior del celular: marca la sección que se está viendo ---- */
  const itemsInferior = document.querySelectorAll(".nav-inferior__item");
  if (itemsInferior.length && "IntersectionObserver" in window) {
    const marcar = (id) => itemsInferior.forEach(a => {
      const activo = a.dataset.seccion === id;
      a.classList.toggle("activo", activo);
      if (activo) a.setAttribute("aria-current", "location"); else a.removeAttribute("aria-current");
    });
    const visibles = new Map();
    const espia = new IntersectionObserver((entries) => {
      entries.forEach(e => visibles.set(e.target.id, e.isIntersecting ? e.intersectionRatio : 0));
      let mejor = null, valor = 0;
      visibles.forEach((v, id) => { if (v > valor) { valor = v; mejor = id; } });
      if (mejor) marcar(mejor);
    }, { threshold: [0, .15, .35, .6], rootMargin: "-20% 0px -35% 0px" });
    itemsInferior.forEach(a => {
      const sec = document.getElementById(a.dataset.seccion);
      if (sec) espia.observe(sec);
      a.addEventListener("click", () => marcar(a.dataset.seccion));
    });
    marcar("inicio");
  }

  /* ---- Aparición progresiva al hacer scroll ---- */
  const animados = document.querySelectorAll(".reveal, .stagger, .fade-up");
  const reducirMovimiento = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  if (reducirMovimiento || !("IntersectionObserver" in window)) {
    /* Accesibilidad: mostrar todo sin animación */
    animados.forEach(el => el.classList.add("visible"));
  } else {
    const obs = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          e.target.classList.add("visible");
          obs.unobserve(e.target);
        }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });

    animados.forEach(el => obs.observe(el));
  }

  const form = document.getElementById("formContacto");
  if (form) {
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      if (!form.checkValidity()) {
        form.classList.add("was-validated");
        return;
      }
      const ok = document.getElementById("okContacto");
      if (ok) ok.classList.remove("d-none");
      form.reset();
      form.classList.remove("was-validated");
    });
  }
});
