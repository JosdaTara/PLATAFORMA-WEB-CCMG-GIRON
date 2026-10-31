
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
