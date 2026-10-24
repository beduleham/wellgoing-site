/* ============================================================
   WELLGOING — effects.js  (화면 효과 7가지)
   1 페이지 전환 커튼   2 헤드라인 줄 마스크 리빌   3 섹션 배경 크로스페이드
   4 풀블리드 사진 패럴랙스   5 AI 5단계 스크롤 연동   6 사진 클립 리빌
   7 버튼·링크 호버 (CSS)
   끄고 싶은 효과는 아래 FX 객체에서 false 로 바꾸면 됩니다.
   ============================================================ */
const FX = { curtain: true, maskReveal: true, bgFade: true, parallax: true, stepSync: true, clipReveal: true };
const REDUCE = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const EASE = 'cubic-bezier(.2,.7,.2,1)';

/* 1. 페이지 전환 커튼 ------------------------------------------ */
(function curtain() {
  if (!FX.curtain) return;
  const el = document.querySelector('.curtain');
  if (!el) return;
  const play = (cont) => { const l = el.querySelector('.ld'); if (!l) return; l.classList.remove('is-play', 'is-cont'); void l.getBoundingClientRect(); l.classList.add('is-play'); if (cont) l.classList.add('is-cont'); };
  const entering = document.documentElement.classList.contains('is-entering');
  if (entering) play(true);
  // 들어올 때: 커튼이 화면을 덮은 상태에서 위로 걷힘
  if (entering) {
    setTimeout(() => {
      el.classList.add('is-leaving');
      document.documentElement.classList.remove('is-entering');
      setTimeout(() => el.classList.remove('is-leaving', 'is-cover'), 700);
    }, 380);
  }
  // 나갈 때: 내부 링크 클릭 → 커튼이 아래에서 올라온 뒤 이동
  document.addEventListener('click', (e) => {
    const a = e.target.closest('a[href]');
    if (!a) return;
    const href = a.getAttribute('href');
    if (!href || href.startsWith('#') || href.startsWith('mailto:') || href.startsWith('tel:') || a.target === '_blank' || /^https?:/.test(href)) return;
    if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    e.preventDefault();
    if (REDUCE) { location.href = href; return; }
    try { sessionStorage.setItem('wgNav', '1'); } catch (_) {}
    el.classList.add('is-cover'); play();
    setTimeout(() => { location.href = href; }, 620);
  });
  // 뒤로가기 캐시에서 복귀하면 커튼 제거
  window.addEventListener('pageshow', (e) => { if (e.persisted) el.classList.remove('is-cover', 'is-leaving'); });
})();

/* 2. 헤드라인 줄 마스크 리빌 ------------------------------------ */
(function maskReveal() {
  if (!FX.maskReveal || REDUCE) return;
  const targets = document.querySelectorAll('h1.d-xl, h1.d-lg, h1.k-hero, h2.d-lg, h2.d-md, h2.k-h1, h3.k-h1, p.d-lg, p.k-hero, p.k-h1');
  targets.forEach((el) => {
    if (el.closest('.phone') || el.querySelector('img')) return;
    const parts = el.innerHTML.split(/<br\s*\/?>/i);
    el.innerHTML = parts.map((p, i) => `<span class="ln"><span class="ln__in" style="transition-delay:${i * 90}ms">${p}</span></span>`).join('');
    el.classList.add('mask');
  });
  const io = new IntersectionObserver((es) => es.forEach((en) => { if (en.isIntersecting || en.boundingClientRect.bottom < 0) { en.target.classList.add('is-in'); io.unobserve(en.target); } }), { threshold: 0.2 });
  document.querySelectorAll('.mask').forEach((el) => io.observe(el));
})();

/* 3. 섹션 배경 크로스페이드 ------------------------------------- */
(function bgFade() {
  if (!FX.bgFade) return;
  const main = document.querySelector('main.page');
  if (!main) return;
  const secs = [...main.querySelectorAll(':scope > section')].filter((s) => s.getAttribute('data-theme') !== 'mist' && !s.classList.contains('mani'));
  if (secs.length < 2) return;
  // 배경이 투명한 섹션(rgba(0,0,0,0))은 건너뜁니다 — 검정으로 잘못 읽히는 것을 방지
  const parse = (c) => { const m = (c.match(/\d+(\.\d+)?/g) || []).map(Number); if (m.length < 3 || (m.length > 3 && m[3] === 0)) return null; return m.slice(0, 3); };
  const items = secs.map((s) => ({ el: s, rgb: parse(getComputedStyle(s).backgroundColor) })).filter((it) => it.rgb);
  if (items.length < 2) return;
  items.forEach((it) => { it.el.style.background = 'transparent'; });
  const mix = (a, b, t) => a.map((v, i) => Math.round(v + (b[i] - v) * t));
  const paint = () => {
    const vh = window.innerHeight, line = vh * 0.66, span = vh * 0.26;
    let color = items[0].rgb;
    for (let i = 0; i < items.length; i++) {
      const r = items[i].el.getBoundingClientRect();
      const t = Math.min(1, Math.max(0, (line - r.top) / span));
      if (t <= 0) break;
      color = mix(color, items[i].rgb, t);
    }
    main.style.backgroundColor = `rgb(${color.join(',')})`;
  };
  paint();
  let tick = false;
  window.addEventListener('scroll', () => { if (!tick) { tick = true; requestAnimationFrame(() => { paint(); tick = false; }); } }, { passive: true });
  window.addEventListener('resize', paint);
})();

/* 4. 풀블리드 사진 패럴랙스 ------------------------------------- */
(function parallax() {
  if (!FX.parallax || REDUCE || window.innerWidth < 960) return;
  const imgs = [...document.querySelectorAll('.mani__img, [style*="aspect-ratio"] > .photo, section > img[style*="object-fit: cover"]')]
    .filter((img) => img.parentElement.getBoundingClientRect().width >= window.innerWidth * 0.6 && !img.closest('.hero-split'));
  if (!imgs.length) return;
  imgs.forEach((img) => { img.style.willChange = 'transform'; img.style.transform = 'scale(1.1)'; });
  const run = () => {
    const vh = window.innerHeight;
    imgs.forEach((img) => {
      const r = img.parentElement.getBoundingClientRect();
      if (r.bottom < 0 || r.top > vh) return;
      const p = (r.top + r.height / 2 - vh / 2) / (vh / 2);  // -1 ~ 1
      img.style.transform = `translateY(${(-p * 40).toFixed(1)}px) scale(1.1)`;
    });
  };
  run();
  let tick = false;
  window.addEventListener('scroll', () => { if (!tick) { tick = true; requestAnimationFrame(() => { run(); tick = false; }); } }, { passive: true });
})();

/* 5. AI 5단계 ↔ 앱 화면 연동 ------------------------------------ */
(function stepSync() {
  if (!FX.stepSync) return;
  const steps = document.querySelectorAll('[data-steps] > li');
  const phones = document.querySelectorAll('.phones .phone');
  if (!steps.length || phones.length < 3) return;
  const map = [0, 0, 1, 2, 2]; // 단계 1·2 → 기록, 3 → 요약, 4·5 → 공유
  const set = (idx) => {
    steps.forEach((li, i) => li.classList.toggle('is-on', i === idx));
    phones.forEach((p, i) => { p.classList.toggle('is-active', i === map[idx]); p.classList.toggle('is-dim', i !== map[idx]); });
  };
  const io = new IntersectionObserver((es) => {
    if (window.__wgDemo) return;   // 앱 시연(10번)이 재생 중이면 시연이 강조를 맡음
    es.forEach((en) => { if (en.isIntersecting) set([...steps].indexOf(en.target)); });
  }, { rootMargin: '-45% 0px -45% 0px', threshold: 0 });
  steps.forEach((li) => io.observe(li));
  window.__wgStep = set;
  set(0);
})();

/* 6. 사진 클립 리빌 --------------------------------------------- */
(function clipReveal() {
  if (!FX.clipReveal) return;
  document.querySelectorAll('[style*="aspect-ratio"] > .photo').forEach((img) => {
    const box = img.parentElement;
    if (box.closest('.hero-split') || box.closest('.phone')) return;
    box.classList.remove('rv'); box.classList.add('clip');
  });
  if (REDUCE) { document.querySelectorAll('.clip').forEach((b) => b.classList.add('is-in')); return; }
  const io = new IntersectionObserver((es) => es.forEach((en) => { if (en.isIntersecting || en.boundingClientRect.bottom < 0) { en.target.classList.add('is-in'); io.unobserve(en.target); } }), { threshold: 0.15 });
  document.querySelectorAll('.clip').forEach((b) => io.observe(b));
})();

/* 8. 푸터 로고 선 그리기 — 보일 때 한 번 재생 ---------------------- */
(function footerLogo() {
  const l = document.querySelector('.ftr__logo .ld');
  if (!l) return;
  const io = new IntersectionObserver((es) => es.forEach((en) => { if (en.isIntersecting) { l.classList.add('is-play'); io.disconnect(); } }), { threshold: 0.5 });
  io.observe(l);
})();

/* 9. How to use 선 일러스트 — 보이면 그리기 시작, 화면 밖이면 반복 동작 일시정지 ---- */
(function howTo() {
  const el = document.querySelector('.howto');
  if (!el) return;
  const io = new IntersectionObserver((es) => es.forEach((en) => {
    if (en.isIntersecting) el.classList.add('is-play');
    el.classList.toggle('is-off', !en.isIntersecting);
  }), { threshold: 0.25 });
  io.observe(el);
})();

/* 10. AI 케어 앱 시연 — 16초 주기: 기록(받아쓰기) → AI 요약 → 전달 대상 선택·전달 --------
   폰 화면이 보일 때만 재생합니다. 자바스크립트가 없거나 동작 줄이기 설정이면 완성된 정지 화면 그대로. */
(function appDemo() {
  const phones = document.querySelectorAll('.phones .phone');
  if (phones.length < 3 || REDUCE) return;
  const [p1, p2, p3] = phones;
  const wave = p1.querySelector('.phone__wave'), mic = p1.querySelector('.phone__mic'), time = p1.querySelector('.phone__time');
  const say = p1.querySelector('.phone__card p'), sayText = say ? say.textContent : '';
  const cards = p2.querySelectorAll('.phone__card');
  const togs = p3.querySelectorAll('.tog'), togOn = [...togs].map((t) => t.classList.contains('tog--on'));
  const follow = p3.querySelector('.phone__card');
  const btns = [p1, p2, p3].map((p) => p.querySelector('.phone__btn'));
  let timers = [], running = false;
  const at = (ms, fn) => timers.push(setTimeout(fn, ms));
  const stop = () => { timers.forEach(clearTimeout); timers = []; };

  function reset() {
    wave.classList.add('is-live'); mic.classList.add('is-live');
    if (time) time.textContent = '00:00';
    if (say) { say.textContent = ''; say.classList.add('is-typing'); }
    cards.forEach((c) => c.classList.add('is-hide'));
    togs.forEach((t) => t.classList.remove('tog--on'));
    if (follow) follow.classList.add('is-hide');
    btns.forEach((b) => b && b.classList.remove('is-done'));
  }
  const step = (i) => window.__wgStep && window.__wgStep(i);   // 왼쪽 5단계 + 폰 강조를 이야기에 맞춤
  function run() {
    stop(); reset(); step(0); at(900, () => step(1)); at(5600, () => step(2)); at(9300, () => step(3)); at(11600, () => step(4));
    // 1) 기록: 0 ~ 5.2초 — 받아쓰기 + 타이머 00:00 → 00:42
    const n = sayText.length, dur = 4600;
    for (let i = 1; i <= n; i++) at(300 + (dur * i) / n, () => { say.textContent = sayText.slice(0, i); });
    for (let s = 1; s <= 42; s++) at(300 + (dur * s) / 42, () => { if (time) time.textContent = '00:' + String(s).padStart(2, '0'); });
    at(5200, () => { wave.classList.remove('is-live'); mic.classList.remove('is-live'); say && say.classList.remove('is-typing'); btns[0] && btns[0].classList.add('is-done'); });
    // 2) 요약: 5.8 ~ 8.5초 — 카드가 한 장씩
    cards.forEach((c, i) => at(5800 + i * 520, () => c.classList.remove('is-hide')));
    at(8900, () => btns[1] && btns[1].classList.add('is-done'));
    // 3) 전달: 9.6 ~ 12.6초 — 받을 곳 켜기 → 후속 확인 → 전달
    let k = 0; togs.forEach((t, i) => { if (togOn[i]) at(9600 + (k++) * 600, () => t.classList.add('tog--on')); });
    at(11600, () => follow && follow.classList.remove('is-hide'));
    at(12600, () => btns[2] && btns[2].classList.add('is-done'));
    at(16000, run);
  }
  const io = new IntersectionObserver((es) => es.forEach((en) => {
    if (en.isIntersecting && !running) { running = window.__wgDemo = true; run(); }
    else if (!en.isIntersecting && running) { running = window.__wgDemo = false; stop(); }
  }), { threshold: 0.3 });
  io.observe(document.querySelector('.phones'));
})();

/* 11. 수출 지도 — 보이면 경로 그리기, 화면 밖이면 반복 동작 일시정지 ------------------ */
(function exportMap() {
  document.querySelectorAll('.wmap').forEach((el) => {
    const io = new IntersectionObserver((es) => es.forEach((en) => {
      if (en.isIntersecting) el.classList.add('is-play');
      el.classList.toggle('is-off', !en.isIntersecting);
    }), { threshold: 0.35 });
    io.observe(el);
  });
})();
