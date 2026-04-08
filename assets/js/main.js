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

  // ====================================================================
  // CONFIG — Formspree endpoint
  // ====================================================================
  // Para activar el envío real de formularios:
  //   1. Crea una cuenta gratuita en https://formspree.io
  //   2. Crea un nuevo form con el email admin@vglogistics.es
  //   3. Sustituye "REPLACE_WITH_YOUR_FORM_ID" por tu ID (ej: "xyzabcde")
  // Mientras no esté configurado, el formulario cae de vuelta a mailto:
  // ====================================================================
  const FORMSPREE_ENDPOINT = 'https://formspree.io/f/REPLACE_WITH_YOUR_FORM_ID';
  const FALLBACK_EMAIL = 'admin@vglogistics.es';

  // Quote / carrier form — envío asíncrono a Formspree con fallback mailto
  const quoteForms = document.querySelectorAll('#quote-form');
  quoteForms.forEach((quoteForm) => {
    const feedback = quoteForm.querySelector('.form-feedback') || (() => {
      const div = document.createElement('div');
      div.className = 'form-feedback';
      div.setAttribute('role', 'status');
      div.setAttribute('aria-live', 'polite');
      quoteForm.appendChild(div);
      return div;
    })();

    quoteForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      feedback.className = 'form-feedback';
      feedback.textContent = '';

      const submitBtn = quoteForm.querySelector('button[type="submit"]');
      const origLabel = submitBtn ? submitBtn.textContent : '';
      if (submitBtn) { submitBtn.disabled = true; submitBtn.textContent = 'Enviando…'; }

      const data = new FormData(quoteForm);

      // Fallback a mailto si no hay endpoint configurado
      if (FORMSPREE_ENDPOINT.includes('REPLACE_WITH_YOUR_FORM_ID')) {
        const subject = encodeURIComponent('Solicitud web — ' + (data.get('company') || data.get('name') || ''));
        const lines = [];
        data.forEach((v, k) => { if (k !== 'gdpr') lines.push(k + ': ' + v); });
        const body = encodeURIComponent(lines.join('\n'));
        window.location.href = 'mailto:' + FALLBACK_EMAIL + '?subject=' + subject + '&body=' + body;
        if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = origLabel; }
        return;
      }

      try {
        const res = await fetch(FORMSPREE_ENDPOINT, {
          method: 'POST',
          body: data,
          headers: { Accept: 'application/json' }
        });
        if (res.ok) {
          feedback.className = 'form-feedback form-feedback--success';
          feedback.textContent = '✓ ¡Gracias! Hemos recibido tu solicitud. Te responderemos en menos de 24 horas laborables.';
          quoteForm.reset();
        } else {
          const json = await res.json().catch(() => ({}));
          throw new Error((json.errors && json.errors.map(err => err.message).join(', ')) || 'Error en el envío');
        }
      } catch (err) {
        feedback.className = 'form-feedback form-feedback--error';
        feedback.innerHTML = '✗ No se ha podido enviar automáticamente. Escríbenos directamente a <a href="mailto:' + FALLBACK_EMAIL + '">' + FALLBACK_EMAIL + '</a> o llámanos al <a href="tel:+34973677173">+34 973 677 173</a>.';
      } finally {
        if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = origLabel; }
      }
    });
  });

  // Year in footer
  const y = document.querySelector('[data-year]');
  if (y) y.textContent = new Date().getFullYear();
})();
