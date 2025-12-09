document.addEventListener('DOMContentLoaded', function() {

  // NAV TOGGLE
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

  // inViewport
  function inViewport(el, offset=80) {
    const r = el.getBoundingClientRect();
    return r.top <= (window.innerHeight || document.documentElement.clientHeight) - offset;
  }

  // revealOnScroll
  function revealOnScroll() {
    document.querySelectorAll('[data-animate]').forEach(el => {
      if (!el.classList.contains('in-view') && inViewport(el, 80)) {
        el.classList.add('in-view');
      }
    });
  }

  // animateCounters
  function animateCounters() {
    const counters = document.querySelectorAll('.counter[data-target]');
    counters.forEach(c => {
      if (c.dataset.animated) return;
      if (!inViewport(c, 0)) return;
      const target = parseInt(c.getAttribute('data-target'), 10) || 0;
      const duration = 1200;
      const start = performance.now();
      c.dataset.animated = "1";
      function tick(now) {
        const progress = Math.min(1, (now - start) / duration);
        c.textContent = Math.floor(progress * target);
        if (progress < 1) requestAnimationFrame(tick);
        else c.textContent = target;
      }
      requestAnimationFrame(tick);
    });
  }

  // LIGHTBOX (template element)
  const lb = document.getElementById('portfolioLightbox');
  const lbImg = lb && lb.querySelector('.lb-img');
  const lbClose = lb && lb.querySelector('.close-btn');

  function openLightbox(src, alt="Preview") {
    if (!lb || !lbImg) return;
    lbImg.src = src;
    lbImg.alt = alt;
    lb.classList.add('open');
    lb.setAttribute('aria-hidden','false');
    if (lbClose) lbClose.focus();
  }
  function closeLightbox() {
    if (!lb || !lbImg) return;
    lb.classList.remove('open');
    lbImg.src = '';
    lb.setAttribute('aria-hidden','true');
  }

  lbClose && lbClose.addEventListener('click', closeLightbox);
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && lb && lb.classList.contains('open')) closeLightbox();
  });
  lb && lb.addEventListener('click', function(e) {
    if (e.target === lb) closeLightbox();
  });

  // delegate preview clicks
  document.addEventListener('click', function(e) {
    const view = e.target.closest('.view-btn');
    if (view) {
      e.preventDefault();
      const src = view.getAttribute('data-src');
      const label = view.getAttribute('aria-label') || 'Preview';
      if (src) openLightbox(src, label);
      return;
    }
    const gimg = e.target.closest('.gallery-item img');
    if (gimg) {
      e.preventDefault();
      openLightbox(gimg.getAttribute('src'), gimg.getAttribute('alt') || 'Preview');
      return;
    }
  });

  // FILTERS
  document.addEventListener('click', function(e) {
    if (!e.target.matches('.filter-btn')) return;
    const btn = e.target;
    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const cat = btn.getAttribute('data-cat');
    const cards = document.querySelectorAll('.refined-grid .portfolio-card');
    cards.forEach(card => {
      const c = (card.getAttribute('data-cat') || 'all').toLowerCase();
      if (cat === 'all' || c === cat) card.style.display = '';
      else card.style.display = 'none';
    });
    setTimeout(revealOnScroll, 120);
  });

  // STICKY HEADER SHRINK + scroll animations
  const header = document.querySelector('.site-header');
  window.addEventListener('scroll', function() {
    const st = window.scrollY || window.pageYOffset;
    if (st > 80 && header) header.classList.add('shrink');
    else if (header) header.classList.remove('shrink');
    revealOnScroll();
    animateCounters();
  });

  // Smooth anchor behavior
  document.addEventListener('click', function(e) {
    const a = e.target.closest('a[href^="#"]');
    if (!a) return;
    e.preventDefault();
    const id = a.getAttribute('href').slice(1);
    const el = document.getElementById(id);
    if (el) el.scrollIntoView({behavior: 'smooth', block: 'start'});
  });

  // Contact toast
  function showToast(msg) {
    let t = document.querySelector('.toast');
    if (!t) {
      t = document.createElement('div');
      t.className = 'toast';
      document.body.appendChild(t);
    }
    t.textContent = msg;
    t.classList.add('show');
    setTimeout(()=> t.classList.remove('show'), 2800);
  }
  document.addEventListener('submit', function(e) {
    if (!e.target.matches('.contact-form')) return;
    e.preventDefault();
    const fm = e.target;
    const name = fm.querySelector('[name=name]')?.value || '';
    const email = fm.querySelector('[name=email]')?.value || '';
    const msg = fm.querySelector('[name=message]')?.value || '';
    if (!name || !email || !msg) {
      showToast('Please complete all fields');
      return;
    }
    showToast('Message sent — demo (server handles mail in production).');
    fm.reset();
  });

  // Testimonials simple slider
  (function() {
    const slider = document.querySelector('.testimonials-grid');
    if (!slider) return;
    const slides = slider.children;
    let idx = 0;
    Array.from(slides).forEach((s, i) => {
      s.style.transition = 'opacity .6s ease';
      s.style.opacity = (i === 0) ? '1' : '0';
      s.style.position = 'relative';
    });
    function advance() {
      slides[idx].style.opacity = '0';
      idx = (idx + 1) % slides.length;
      slides[idx].style.opacity = '1';
    }
    setInterval(advance, 4500);
  })();

  // initial
  revealOnScroll();
  animateCounters();
});
