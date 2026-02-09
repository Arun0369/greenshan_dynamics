/* ===============================
   MAIN APP SCRIPT
================================ */

document.addEventListener("DOMContentLoaded", () => {
  initLoader();
  initNavigation();
  initThemeToggle();
  initToasts();
  initLightbox();
  initCounters();
});

/* ===============================
   LOADING OVERLAY
================================ */
function initLoader() {
  const loader = document.getElementById("loading");
  if (!loader) return;

  setTimeout(() => {
    loader.style.opacity = "0";
    loader.style.pointerEvents = "none";
  }, 500);
}

/* ===============================
   NAVIGATION (MOBILE)
================================ */
function initNavigation() {
  const toggle = document.getElementById("nav-toggle");
  const nav = document.getElementById("main-nav");

  if (!toggle || !nav) return;

  // ✅ FORCE CLOSED STATE ON LOAD
  nav.setAttribute("aria-hidden", "true");
  toggle.setAttribute("aria-expanded", "false");
  document.body.style.overflow = "";

  toggle.addEventListener("click", () => {
    const expanded = toggle.getAttribute("aria-expanded") === "true";
    toggle.setAttribute("aria-expanded", String(!expanded));
    nav.setAttribute("aria-hidden", String(expanded));
    document.body.style.overflow = expanded ? "" : "hidden";
  });

  nav.querySelectorAll("a").forEach(link => {
    link.addEventListener("click", () => {
      toggle.setAttribute("aria-expanded", "false");
      nav.setAttribute("aria-hidden", "true");
      document.body.style.overflow = "";
    });
  });
}


/* ===============================
   THEME TOGGLE
================================ */
function initThemeToggle() {
  const btn = document.querySelector(".theme-toggle");
  if (!btn) return;

  const root = document.documentElement;
  const savedTheme = localStorage.getItem("theme");

  if (savedTheme) {
    root.setAttribute("data-theme", savedTheme);
  }

  btn.addEventListener("click", () => {
    const current = root.getAttribute("data-theme");
    const next = current === "dark" ? "light" : "dark";

    root.setAttribute("data-theme", next);
    localStorage.setItem("theme", next);
  });
}

/* ===============================
   TOAST AUTO DISMISS
================================ */
function initToasts() {
  const toasts = document.querySelectorAll(".toast");

  toasts.forEach(toast => {
    const closeBtn = toast.querySelector(".toast-close");

    setTimeout(() => {
      toast.style.opacity = "0";
      toast.style.transform = "translateX(100%)";
      setTimeout(() => toast.remove(), 300);
    }, 5000);

    closeBtn?.addEventListener("click", () => toast.remove());
  });
}

/* ===============================
   LIGHTBOX (IMAGES)
================================ */
function initLightbox() {
  const lightbox = document.getElementById("lightbox");
  const img = document.querySelector(".lightbox-img");
  const close = document.querySelector(".lightbox-close");

  if (!lightbox || !img || !close) return;

  document.querySelectorAll("img[data-lightbox]").forEach(image => {
    image.addEventListener("click", () => {
      img.src = image.src;
      lightbox.removeAttribute("hidden");
      document.body.style.overflow = "hidden";
    });
  });

  close.addEventListener("click", closeLightbox);
  lightbox.addEventListener("click", e => {
    if (e.target === lightbox) closeLightbox();
  });

  function closeLightbox() {
    lightbox.setAttribute("hidden", "true");
    img.src = "";
    document.body.style.overflow = "";
  }
}

/* ===============================
   DASHBOARD COUNTERS
================================ */
function initCounters() {
  const counters = document.querySelectorAll("[data-counter]");
  if (!counters.length) return;

  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;

      const el = entry.target;
      const target = parseInt(el.dataset.counter, 10) || 0;
      let current = 0;
      const step = Math.max(1, target / 60);

      const update = () => {
        current += step;
        if (current < target) {
          el.textContent = Math.floor(current);
          requestAnimationFrame(update);
        } else {
          el.textContent = target;
        }
      };

      update();
      observer.unobserve(el);
    });
  }, { threshold: 0.5 });

  counters.forEach(c => observer.observe(c));
}
