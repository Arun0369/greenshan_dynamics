document.addEventListener('DOMContentLoaded', () => {

  /* =========================================================
     NAV TOGGLE (MOBILE)
  ========================================================= */
  const toggle = document.getElementById('nav-toggle');
  const navUl = document.querySelector('.main-nav ul');

  if (toggle && navUl) {
    toggle.setAttribute('aria-expanded', 'false');

    toggle.addEventListener('click', () => {
      navUl.classList.toggle('open');
      const expanded = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!expanded));
    });
  }

  /* =========================================================
     VIEWPORT HELPERS
  ========================================================= */
  function inViewport(el, offset = 80) {
    const r = el.getBoundingClientRect();
    return r.top <= (window.innerHeight || document.documentElement.clientHeight) - offset;
  }

  function revealOnScroll() {
    document.querySelectorAll('[data-animate]').forEach(el => {
      if (!el.classList.contains('in-view') && inViewport(el)) {
        el.classList.add('in-view');
      }
    });
  }

  /* =========================================================
     COUNTER ANIMATION (DASHBOARD)
  ========================================================= */
  function animateCounters() {
    document.querySelectorAll('.counter[data-target]').forEach(counter => {
      if (counter.dataset.animated || !inViewport(counter, 0)) return;

      const target = parseInt(counter.dataset.target, 10) || 0;
      const start = performance.now();
      const duration = 1200;
      counter.dataset.animated = '1';

      function tick(now) {
        const progress = Math.min(1, (now - start) / duration);
        counter.textContent = Math.floor(progress * target);
        if (progress < 1) requestAnimationFrame(tick);
        else counter.textContent = target;
      }

      requestAnimationFrame(tick);
    });
  }

  /* =========================================================
     TOAST STATUS MESSAGES (SUCCESS / ERROR / LOADING)
  ========================================================= */
  function showToast(message, type = 'success') {
    let toast = document.querySelector('.toast');

    if (!toast) {
      toast = document.createElement('div');
      toast.className = 'toast';
      document.body.appendChild(toast);
    }

    toast.textContent = message;
    toast.classList.remove('error', 'loading');

    if (type === 'error') toast.classList.add('error');
    if (type === 'loading') toast.classList.add('loading');

    toast.classList.add('show');

    if (type !== 'loading') {
      setTimeout(() => toast.classList.remove('show'), 2800);
    }
  }

  function hideToast() {
    const toast = document.querySelector('.toast');
    toast?.classList.remove('show');
  }

  /* =========================================================
     LIGHTBOX (IMAGES / PREVIEW)
  ========================================================= */
  const lightbox = document.getElementById('portfolioLightbox');
  const lbImg = lightbox?.querySelector('.lb-img');
  const lbClose = lightbox?.querySelector('.close-btn');

  function openLightbox(src, alt = 'Preview') {
    if (!lightbox || !lbImg) return;
    lbImg.src = src;
    lbImg.alt = alt;
    lightbox.classList.add('open');
    lightbox.setAttribute('aria-hidden', 'false');
    lbClose?.focus();
  }

  function closeLightbox() {
    if (!lightbox || !lbImg) return;
    lightbox.classList.remove('open');
    lbImg.src = '';
    lightbox.setAttribute('aria-hidden', 'true');
  }

  lbClose?.addEventListener('click', closeLightbox);

  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && lightbox?.classList.contains('open')) {
      closeLightbox();
    }
  });

  lightbox?.addEventListener('click', e => {
    if (e.target === lightbox) closeLightbox();
  });

  /* =========================================================
     DELEGATED CLICKS
  ========================================================= */
  document.addEventListener('click', e => {

    // Preview buttons
    const previewBtn = e.target.closest('.view-btn');
    if (previewBtn) {
      e.preventDefault();
      const src = previewBtn.dataset.src;
      if (src) openLightbox(src, previewBtn.getAttribute('aria-label'));
      return;
    }

    // Gallery images
    const galleryImg = e.target.closest('.gallery-item img');
    if (galleryImg) {
      e.preventDefault();
      openLightbox(galleryImg.src, galleryImg.alt);
    }
  });

  /* =========================================================
     PORTFOLIO FILTERS
  ========================================================= */
  document.addEventListener('click', e => {
    if (!e.target.classList.contains('filter-btn')) return;

    const btn = e.target;
    const category = btn.dataset.cat;

    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');

    document.querySelectorAll('.portfolio-card').forEach(card => {
      const cardCat = (card.dataset.cat || 'all').replace(/\s+/g, '-').toLowerCase();
      card.style.display =
        category === 'all' || cardCat === category ? '' : 'none';
    });

    setTimeout(revealOnScroll, 120);
  });

  /* =========================================================
     FORM STATUS FEEDBACK (ADMIN & CONTACT)
  ========================================================= */
  document.addEventListener('submit', e => {
    const form = e.target;

    if (form.matches('.contact-form, .admin-form')) {
      showToast('Processing...', 'loading');
    }
  });

  /* =========================================================
     SCROLL EVENTS
  ========================================================= */
  window.addEventListener('scroll', () => {
    revealOnScroll();
    animateCounters();
  });

  /* =========================================================
     INITIAL LOAD
  ========================================================= */
  revealOnScroll();
  animateCounters();
});
