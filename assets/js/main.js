/* ============================================================
   WELLGOING — main.js
   1 설정  2 헤더(스크롤·섹션 테마)  3 모바일 메뉴  4 스크롤 리빌
   5 숫자 카운트업  6 문의 폼  7 FAQ 접기
   ============================================================ */

/* 1. 설정 ------------------------------------------------------ */
const WG = {
  // 문의 폼 전송 주소. Formspree 등에서 발급받은 주소를 넣으면 폼이 바로 동작합니다.
  // 비워두면 메일 앱이 열리는 mailto 방식으로 대신 보냅니다.
  FORM_ENDPOINT: '',
  CONTACT_EMAIL: 'wellgoing@wellgoing.kr',
};

/* 2. 헤더 ------------------------------------------------------ */
(function header() {
  const hdr = document.querySelector('.hdr');
  if (!hdr) return;
  const onScroll = () => hdr.classList.toggle('is-scrolled', window.scrollY > 24);
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  // 헤더 아래에 어떤 섹션이 있는지 보고 헤더 색(테마)을 맞춥니다.
  const sections = document.querySelectorAll('[data-theme]');
  const apply = () => {
    const y = 40;
    let theme = 'cream';
    sections.forEach((s) => {
      const r = s.getBoundingClientRect();
      if (r.top <= y && r.bottom > y) theme = s.getAttribute('data-theme');
    });
    hdr.setAttribute('data-theme', theme === 'mist' ? 'cream' : theme);
  };
  apply();
  window.addEventListener('scroll', apply, { passive: true });
  window.addEventListener('resize', apply);
})();

/* 3. 모바일 메뉴 ------------------------------------------------ */
(function mobileNav() {
  const open = document.querySelector('.hdr__burger');
  const nav = document.querySelector('.mnav');
  const close = document.querySelector('.mnav__close');
  if (!open || !nav) return;
  const toggle = (on) => {
    nav.classList.toggle('is-open', on);
    document.body.style.overflow = on ? 'hidden' : '';
    open.setAttribute('aria-expanded', on ? 'true' : 'false');
  };
  open.addEventListener('click', () => toggle(true));
  close.addEventListener('click', () => toggle(false));
  nav.querySelectorAll('a').forEach((a) => a.addEventListener('click', () => toggle(false)));
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') toggle(false); });
})();

/* 4. 스크롤 리빌 ------------------------------------------------ */
(function reveal() {
  // 섹션 안의 주요 블록에 자동으로 리빌 효과를 붙입니다. 빼고 싶으면 요소에 data-no-rv 를 주세요.
  document.querySelectorAll('.sec .wrap > *, .cols2 > *, .cols3 > *, .cols4 > *, .grid12 > *, .flow > li, .stats > *, .reviews > *').forEach((el, i) => {
    if (el.closest('[data-no-rv]') || el.classList.contains('rv')) return;
    el.classList.add('rv'); if (i % 3 === 1) el.classList.add('rv-d1'); if (i % 3 === 2) el.classList.add('rv-d2');
  });
  const els = document.querySelectorAll('.rv, .photo-zoom');
  if (!('IntersectionObserver' in window) || !els.length) { els.forEach((e) => e.classList.add('is-in')); return; }
  const io = new IntersectionObserver((entries) => {
    entries.forEach((en) => { if (en.isIntersecting || en.boundingClientRect.bottom < 0) { en.target.classList.add('is-in'); io.unobserve(en.target); } });
  }, { rootMargin: '0px 0px -10% 0px', threshold: 0.1 });
  els.forEach((e) => io.observe(e));
})();

/* 5. 숫자 카운트업 (data-count="88" data-suffix="%") ------------- */
(function countUp() {
  const els = document.querySelectorAll('[data-count]');
  if (!els.length) return;
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const run = (el) => {
    const target = parseFloat(el.dataset.count);
    const decimals = (el.dataset.count.split('.')[1] || '').length;
    const suffix = el.dataset.suffix || '';
    if (reduce) { el.textContent = target.toFixed(decimals) + suffix; return; }
    const t0 = performance.now(), dur = 1200;
    const step = (t) => {
      const p = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - p, 3);
      el.textContent = (target * e).toFixed(decimals) + suffix;
      if (p < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  };
  const io = new IntersectionObserver((entries) => {
    entries.forEach((en) => { if (en.isIntersecting) { run(en.target); io.unobserve(en.target); } });
  }, { threshold: 0.4 });
  els.forEach((e) => io.observe(e));
})();

/* 6. 문의 폼 ---------------------------------------------------- */
(function forms() {
  document.querySelectorAll('form[data-wg-form]').forEach((form) => {
    const note = form.querySelector('.form-note');
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const data = new FormData(form);
      const consent = form.querySelector('input[name="consent"]');
      if (consent && !consent.checked) { show('개인정보 수집·이용에 동의해 주세요.'); return; }
      if (WG.FORM_ENDPOINT) {
        try {
          const res = await fetch(WG.FORM_ENDPOINT, { method: 'POST', body: data, headers: { Accept: 'application/json' } });
          if (res.ok) { form.reset(); show('문의가 접수되었습니다. 확인 후 회신드리겠습니다.'); }
          else show('전송에 실패했습니다. 잠시 후 다시 시도해 주세요.');
        } catch (err) { show('전송에 실패했습니다. 네트워크를 확인해 주세요.'); }
      } else {
        // 전송 주소가 없으면 메일 앱으로 내용을 넘깁니다.
        const lines = [];
        data.forEach((v, k) => { if (k !== 'consent') lines.push(`${k}: ${v}`); });
        const subject = encodeURIComponent(`[웰고잉 문의] ${data.get('type') || data.get('subject') || ''}`);
        const body = encodeURIComponent(lines.join('\n'));
        window.location.href = `mailto:${WG.CONTACT_EMAIL}?subject=${subject}&body=${body}`;
        show('메일 앱이 열립니다. 내용을 확인하고 보내주세요.');
      }
    });
    function show(msg) { if (!note) return; note.textContent = msg; note.classList.add('is-shown'); }
  });
})();

/* 7. FAQ — 하나 열면 나머지는 닫기 ------------------------------ */
(function faq() {
  const items = document.querySelectorAll('.faq details');
  items.forEach((d) => d.addEventListener('toggle', () => {
    if (d.open) items.forEach((o) => { if (o !== d) o.removeAttribute('open'); });
  }));
})();
