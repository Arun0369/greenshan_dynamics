/* =========================================================
   GREENSHAN DYNAMICS — MAIN APP SCRIPT
========================================================= */

document.addEventListener("DOMContentLoaded", () => {
  initLoader();
  initNavigation();
  initThemeToggle();
  initToasts();
  initLightbox();
  initCounters();
  initTextareaAutoresize(); // NEW: Premium form UX
});

/* =========================================================
   1. INTELLIGENT LOADING OVERLAY
========================================================= */
function initLoader() {
  const loader = document.getElementById("loading");
  if (!loader) return;

  const hideLoader = () => {
    if (loader.style.opacity === "0") return; // Prevent double-firing
    loader.style.opacity = "0";
    loader.style.pointerEvents = "none";
    setTimeout(() => loader.remove(), 500); // Completely remove from DOM
  };

  // Wait for all heavy media (images/videos) to fully load
  window.addEventListener('load', hideLoader);

  // Fallback: Force hide after 3 seconds in case a 3rd party script hangs
  setTimeout(hideLoader, 3000);
}

/* =========================================================
   2. NAVIGATION (MOBILE)
========================================================= */
function initNavigation() {
  const toggle = document.getElementById("nav-toggle");
  const nav = document.getElementById("main-nav");

  if (!toggle || !nav) return;

  // Force closed state on load
  nav.setAttribute("aria-hidden", "true");
  toggle.setAttribute("aria-expanded", "false");
  document.body.style.overflow = "";

  toggle.addEventListener("click", () => {
    const expanded = toggle.getAttribute("aria-expanded") === "true";
    toggle.setAttribute("aria-expanded", String(!expanded));
    nav.setAttribute("aria-hidden", String(expanded));
    
    // Prevent background scrolling when menu is open
    document.body.style.overflow = expanded ? "" : "hidden";
  });

  // Close nav when clicking a link
  nav.querySelectorAll("a").forEach(link => {
    link.addEventListener("click", () => {
      toggle.setAttribute("aria-expanded", "false");
      nav.setAttribute("aria-hidden", "true");
      document.body.style.overflow = "";
    });
  });
}

/* =========================================================
   3. THEME TOGGLE
========================================================= */
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

/* =========================================================
   4. TOAST AUTO DISMISS (SMOOTH SLIDE)
========================================================= */
function initToasts() {
  const toasts = document.querySelectorAll(".toast");

  toasts.forEach(toast => {
    const closeBtn = toast.querySelector(".toast-close");

    // Auto dismiss after 5 seconds
    setTimeout(() => {
      toast.style.transition = "all 0.4s cubic-bezier(0.25, 1, 0.5, 1)";
      toast.style.opacity = "0";
      toast.style.transform = "translateX(100%)";
      setTimeout(() => toast.remove(), 400);
    }, 5000);

    // Manual dismiss
    closeBtn?.addEventListener("click", () => {
      toast.style.opacity = "0";
      setTimeout(() => toast.remove(), 300);
    });
  });
}

/* =========================================================
   5. LIGHTBOX (IMAGES & MEDIA)
========================================================= */
function initLightbox() {
  const lightbox = document.getElementById("lightbox");
  const img = document.querySelector(".lightbox-img");
  const close = document.querySelector(".lightbox-close");

  if (!lightbox || !img || !close) return;

  document.querySelectorAll("img[data-lightbox]").forEach(image => {
    image.addEventListener("click", () => {
      img.src = image.src;
      lightbox.removeAttribute("hidden");
      document.body.style.overflow = "hidden"; // Prevent scrolling
    });
  });

  close.addEventListener("click", closeLightbox);
  
  // Close when clicking outside the image
  lightbox.addEventListener("click", e => {
    if (e.target === lightbox) closeLightbox();
  });

  function closeLightbox() {
    lightbox.setAttribute("hidden", "true");
    setTimeout(() => { img.src = ""; }, 300); // Clear source after fade
    document.body.style.overflow = "";
  }
}

/* =========================================================
   6. DASHBOARD COUNTERS (INTERSECTION OBSERVER)
========================================================= */
function initCounters() {
  const counters = document.querySelectorAll("[data-counter]");
  if (!counters.length) return;

  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;

      const el = entry.target;
      const target = parseInt(el.dataset.counter, 10) || 0;
      let current = 0;
      const step = Math.max(1, target / 60); // 60fps animation speed

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
      observer.unobserve(el); // Only animate once
    });
  }, { threshold: 0.5 });

  counters.forEach(c => observer.observe(c));
}

/* =========================================================
   7. AUTO-RESIZING TEXTAREAS (PREMIUM UX)
========================================================= */
function initTextareaAutoresize() {
  const textareas = document.querySelectorAll("textarea");
  
  textareas.forEach(textarea => {
    // Set initial height based on content
    textarea.setAttribute("style", "height:" + (textarea.scrollHeight) + "px;overflow-y:hidden;");
    
    // Adjust height on input
    textarea.addEventListener("input", function() {
      this.style.height = "auto";
      this.style.height = (this.scrollHeight) + "px";
    });
  });
}