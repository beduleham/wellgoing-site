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
// 전송 흐름: 사이트 폼 → Google Apps Script(WG.FORM_ENDPOINT) → 구글 시트에 한 줄 추가 + 담당자 메일 알림.
// 주소가 비어 있거나 전송이 실패하면 메일 앱으로 내용을 넘깁니다. 설정 방법은 _build/google-sheet/README.md
(function forms() {
  const EN = document.documentElement.lang === 'en';
  const M = EN ? {
    consent: 'Please agree to the collection and use of your personal data.',
    contact: 'Please leave a phone number or an email address so we can reply.',
    sending: 'Sending…', ok: 'Thank you — your enquiry has been received. We will be in touch shortly.',
    fail: 'Sorry, we could not send your enquiry.', mail: 'Send by email instead', mailOpen: 'Your email app will open. Please check the message and send it.',
  } : {
    consent: '개인정보 수집·이용에 동의해 주세요.',
    contact: '회신받으실 연락처나 이메일 중 하나를 남겨주세요.',
    sending: '보내는 중…', ok: '문의가 접수되었습니다. 확인 후 빠르게 회신드리겠습니다.',
    fail: '전송하지 못했습니다.', mail: '메일로 보내기', mailOpen: '메일 앱이 열립니다. 내용을 확인하고 보내주세요.',
  };
  const LABEL = { type: '유형', name: '이름', org: '기관·회사', phone: '연락처', email: '이메일', company: '회사명', country: '국가', message: '내용' };

  // 문의 유형 카드: 선택한 카드에 강조 표시
  document.querySelectorAll('.opt input[type="radio"]').forEach((r) => r.addEventListener('change', () => {
    document.querySelectorAll(`.opt input[name="${r.name}"]`).forEach((o) => o.closest('.opt').classList.toggle('is-on', o.checked));
  }));

  document.querySelectorAll('form[data-wg-form]').forEach((form) => {
    const note = form.querySelector('.form-note');
    const btn = form.querySelector('button[type="submit"]');
    const show = (msg, err, html) => { if (!note) return; note[html ? 'innerHTML' : 'textContent'] = msg; note.classList.add('is-shown'); note.classList.toggle('is-error', !!err); };
    const mailto = (data) => {
      const lines = []; data.forEach((v, k) => { if (!k.startsWith('_') && k !== 'consent' && v) lines.push(`${LABEL[k] || k}: ${v}`); });
      const subject = `[웰고잉 ${form.dataset.wgForm === 'partner' ? '파트너 문의' : '문의'}] ${data.get('type') || ''} ${data.get('name') || ''}`.trim();
      return `mailto:${WG.CONTACT_EMAIL}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(lines.join('\n'))}`;
    };

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const data = new FormData(form);
      if (data.get('_hp')) { form.reset(); show(M.ok); return; } // 스팸 봇
      if (!data.get('consent')) { show(M.consent, true); return; }
      if (form.dataset.wgForm === 'contact' && !data.get('phone') && !data.get('email')) { show(M.contact, true); form.querySelector('[name="phone"]').focus(); return; }
      data.set('_form', form.dataset.wgForm || 'contact');
      data.set('_lang', EN ? 'EN' : 'KR');
      data.set('_page', location.pathname);

      if (!WG.FORM_ENDPOINT) { location.href = mailto(data); show(M.mailOpen); return; }

      const label = btn.innerHTML; btn.disabled = true; btn.textContent = M.sending;
      const ctrl = new AbortController(); const timer = setTimeout(() => ctrl.abort(), 20000);
      try {
        const res = await fetch(WG.FORM_ENDPOINT, { method: 'POST', body: new URLSearchParams(data), signal: ctrl.signal });
        const out = await res.json().catch(() => ({}));
        if (!res.ok || out.ok === false) throw new Error(out.error || res.status);
        form.reset(); document.querySelectorAll('.opt').forEach((o, i) => o.classList.toggle('is-on', i === 0));
        show(M.ok);
      } catch (err) {
        show(`${M.fail} <a href="${mailto(data)}">${M.mail} →</a>`, true, true);
      } finally { clearTimeout(timer); btn.disabled = false; btn.innerHTML = label; }
    });
  });
})();

/* 7. FAQ — 하나 열면 나머지는 닫기 ------------------------------ */
(function faq() {
  const items = document.querySelectorAll('.faq details');
  items.forEach((d) => d.addEventListener('toggle', () => {
    if (d.open) items.forEach((o) => { if (o !== d) o.removeAttribute('open'); });
  }));
})();
