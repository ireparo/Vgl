/* VG Logistics — Interacciones */
(function () {
  'use strict';

  // Mobile nav toggle
  const navToggle = document.querySelector('.nav-toggle');
  const navLinks = document.querySelector('.nav-links');
  if (navToggle && navLinks) {
    navToggle.addEventListener('click', () => {
      navLinks.classList.toggle('is-open');
      navToggle.setAttribute(
        'aria-expanded',
        navLinks.classList.contains('is-open') ? 'true' : 'false'
      );
    });
  }

  // Language switcher
  const langSwitch = document.querySelector('.lang-switch');
  const langToggle = document.querySelector('.lang-toggle');
  if (langSwitch && langToggle) {
    langToggle.addEventListener('click', (e) => {
      e.stopPropagation();
      langSwitch.classList.toggle('is-open');
    });
    document.addEventListener('click', () => langSwitch.classList.remove('is-open'));
  }

  // Active link highlight
  const path = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-links a').forEach((a) => {
    const href = a.getAttribute('href');
    if (!href) return;
    if (href === path || (path === '' && href === 'index.html')) {
      a.classList.add('is-active');
    }
  });

  // Reveal on scroll
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) {
            e.target.classList.add('is-visible');
            io.unobserve(e.target);
          }
        });
      },
      { threshold: 0.12 }
    );
    document.querySelectorAll('.fade-in').forEach((el) => io.observe(el));
  } else {
    document.querySelectorAll('.fade-in').forEach((el) => el.classList.add('is-visible'));
  }

  // KPI counter animation
  const animateNumber = (el) => {
    const target = parseFloat(el.dataset.count || el.textContent);
    const suffix = el.dataset.suffix || '';
    const duration = 1400;
    const start = performance.now();
    const tick = (now) => {
      const p = Math.min(1, (now - start) / duration);
      const eased = 1 - Math.pow(1 - p, 3);
      const val = Math.round(target * eased);
      el.textContent = val.toLocaleString('es-ES') + suffix;
      if (p < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  };
  const counters = document.querySelectorAll('[data-count]');
  if (counters.length && 'IntersectionObserver' in window) {
    const co = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting) {
          animateNumber(e.target);
          co.unobserve(e.target);
        }
      });
    });
    counters.forEach((c) => co.observe(c));
  }

  // Quote form (cliente — sin backend, abre mailto)
  const quoteForm = document.querySelector('#quote-form');
  if (quoteForm) {
    quoteForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const data = new FormData(quoteForm);
      const subject = encodeURIComponent('Solicitud de cotización web — ' + (data.get('company') || data.get('name') || ''));
      const lines = [];
      data.forEach((v, k) => { if (k !== 'gdpr') lines.push(k + ': ' + v); });
      const body = encodeURIComponent(lines.join('\n'));
      window.location.href = 'mailto:admin@vglogistics.es?subject=' + subject + '&body=' + body;
    });
  }

  // Year in footer
  const y = document.querySelector('[data-year]');
  if (y) y.textContent = new Date().getFullYear();
})();
