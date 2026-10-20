(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];

  /* header shadow + mobile menu */
  const hdr = $('.hdr');
  const onScroll = () => hdr && hdr.classList.toggle('scrolled', scrollY > 8);
  addEventListener('scroll', onScroll, { passive: true }); onScroll();
  const mb = $('.menu-btn');
  if (mb) mb.addEventListener('click', () => {
    const open = document.body.classList.toggle('menu-open');
    mb.setAttribute('aria-expanded', open);
  });
  addEventListener('keydown', e => { if (e.key === 'Escape') document.body.classList.remove('menu-open'); });

  /* reveal on scroll */
  const io = 'IntersectionObserver' in window ? new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
  }), { rootMargin: '0px 0px -8% 0px' }) : null;
  $$('.rv').forEach(el => io ? io.observe(el) : el.classList.add('in'));

  /* gallery filters + lightbox */
  const filters = $$('.filters button');
  filters.forEach(b => b.addEventListener('click', () => {
    filters.forEach(x => x.setAttribute('aria-pressed', x === b));
    const f = b.dataset.f;
    $$('.tile').forEach(t => t.classList.toggle('hide', f !== 'all' && t.dataset.cat !== f));
  }));
  const lb = $('.lightbox');
  if (lb) {
    const img = $('img', lb);
    $$('.tile').forEach(t => t.addEventListener('click', () => {
      img.src = $('img', t).src; img.alt = $('img', t).alt; lb.classList.add('open'); $('button', lb).focus();
    }));
    const close = () => lb.classList.remove('open');
    lb.addEventListener('click', e => { if (e.target !== img) close(); });
    addEventListener('keydown', e => { if (e.key === 'Escape') close(); });
  }

  /* contact form: demo submit (on Netlify, data-netlify handles real delivery) */
  $$('form.form').forEach(f => {
    const q = new URLSearchParams(location.search);
    const msg = $('textarea', f);
    if (msg && q.get('estimate')) msg.value = q.get('estimate');
    if (q.get('type')) { const r = $(`input[name=service][value="${q.get('type')}"]`, f); if (r) r.checked = true; }
    f.addEventListener('submit', e => {
      if (location.protocol === 'file:' || !f.hasAttribute('data-netlify')) {
        e.preventDefault(); f.classList.add('sent'); $('.ok', f).scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    });
  });

  /* ================= ESTIMATOR =================
     RATES ARE SAMPLE NUMBERS FOR THIS CONCEPT ONLY.
     Messer Painting sets the real rates here (low/high per unit). */
  const RATES = {
    exterior:    { lo: 2.25, hi: 3.50, unit: 'sq ft', label: 'Full exterior' },
    intOcc:      { lo: 3.00, hi: 4.25, unit: 'sq ft', label: 'Interior (occupied)' },
    intUnocc:    { lo: 2.25, hi: 3.25, unit: 'sq ft', label: 'Interior (unoccupied)' },
    room:        { lo: 450,  hi: 650,  unit: 'room',  label: 'Single rooms (walls only)', min: 3 },
    doorSlab:    { lo: 75,   hi: 110,  unit: 'door',  label: 'Interior doors – slab only' },
    doorFull:    { lo: 140,  hi: 200,  unit: 'door',  label: 'Interior doors – slab, jamb & trim' },
    epoxy:       { lo: 5.00, hi: 8.00, unit: 'sq ft', label: 'Industrial-grade epoxy' }
  };
  const est = $('#estimator');
  if (!est) return;
  const money = n => '$' + Math.round(n).toLocaleString('en-US');
  const state = {};

  const paintRange = r => r.style.setProperty('--p', ((r.value - r.min) / (r.max - r.min) * 100) + '%');
  $$('input[type=range]', est).forEach(r => {
    const num = $(`input[type=number][data-for="${r.id}"]`, est);
    const sync = v => { r.value = v; num.value = v; paintRange(r); calc(); };
    r.addEventListener('input', () => sync(r.value));
    num.addEventListener('change', () => sync(Math.max(0, Math.min(+r.max, +num.value || 0))));
    paintRange(r);
  });
  $$('.stepper', est).forEach(s => {
    const out = $('output', s); const key = s.dataset.k; const min0 = +(s.dataset.min || 0);
    $$('button', s).forEach(b => b.addEventListener('click', () => {
      let v = +out.value + (+b.dataset.d);
      if (v < 0) v = 0;
      if (min0 && v > 0 && v < min0) v = (+b.dataset.d > 0) ? min0 : 0;
      out.value = v; calc();
    }));
  });
  $$('input[type=radio]', est).forEach(r => r.addEventListener('change', calc));

  function calc() {
    const lines = []; let lo = 0, hi = 0;
    const add = (k, qty) => {
      if (!qty) return; const R = RATES[k];
      const l = R.lo * qty, h = R.hi * qty; lo += l; hi += h;
      lines.push([`${R.label} · ${(+qty).toLocaleString()} ${R.unit}${qty > 1 && R.unit !== 'sq ft' ? 's' : ''}`, `${money(l)}–${money(h)}`]);
    };
    add('exterior', +$('#exterior').value);
    const fd = $('input[name=frontdoor]:checked', est)?.value;
    if (+$('#exterior').value > 0) lines.push(['Garage door', 'Included']);
    if (fd === 'paint') lines.push(['Front door – paint', +$('#exterior').value > 0 ? 'Included' : 'With exterior']);
    if (fd === 'stain') lines.push(['Front door – stain/refinish', 'Call for price']);
    add('intOcc', +$('#intOcc').value);
    add('intUnocc', +$('#intUnocc').value);
    add('room', +$('[data-k=room] output').value);
    add('doorSlab', +$('[data-k=doorSlab] output').value);
    add('doorFull', +$('[data-k=doorFull] output').value);
    add('epoxy', +$('#epoxy').value);

    $('#total').innerHTML = lo ? `${money(lo)}<small> – ${money(hi)}</small>` : '$0';
    $('#lines').innerHTML = lines.length
      ? lines.map(([a, b]) => `<li><span>${a}</span><span>${b}</span></li>`).join('')
      : '<li class="empty">Move a slider to start your estimate</li>';
    state.text = lines.map(([a, b]) => `• ${a}: ${b}`).join('\n') + (lo ? `\nEstimated range: ${money(lo)} – ${money(hi)}` : '');
    $('#sendEst').href = 'contact.html?type=Estimate&estimate=' + encodeURIComponent('My online estimate:\n' + (state.text || '(nothing selected yet)') + '\n\nAbout my project: ');
  }
  $('#printEst').addEventListener('click', () => window.print());
  $('#resetEst').addEventListener('click', () => {
    $$('input[type=range]', est).forEach(r => { r.value = 0; $(`input[data-for="${r.id}"]`, est).value = 0; paintRange(r); });
    $$('.stepper output', est).forEach(o => o.value = 0);
    $$('input[type=radio][value=none]', est).forEach(r => r.checked = true);
    calc();
  });
  calc();
})();
