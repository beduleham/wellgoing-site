// OG 공유 카드 렌더: node _build/og/render.js  → assets/og/*.jpg (1200×630)
const { chromium } = require('playwright');
const path = require('path');
const ROOT = path.resolve(__dirname, '../..');
const CARDS = [
  { out: 'og-default.jpg',     eyebrow: 'Compassionate Technology', title: 'Care, Connected by AI', ko: false, sub: '케어 현장의 기록을 AI로 잇고, 물 없이도 존엄한 위생을 지키는 제품을 만듭니다.', img: 'shower-sheet-hero.jpg' },
  { out: 'og-default-en.jpg',  eyebrow: 'Compassionate Technology', title: 'Care, Connected by AI', ko: false, sub: 'We connect the records of care with AI, and make hygiene dignified — without water.', img: 'shower-sheet-hero.jpg', en: true },
  { out: 'og-bichae.jpg',      eyebrow: 'Bichae Body Shield · Premium Shower Sheet', title: 'A Shower,<br>in One Sheet.', ko: false, sub: '에센스 45mL를 머금은 시트 한 장. 세정·소취·보습·진정을 헹굼 없이. 피부 자극 지수 0.00.', img: 'shower-sheet-hero.jpg' },
  { out: 'og-bichae-en.jpg',   eyebrow: 'Bichae Body Shield · Premium Shower Sheet', title: 'A Shower,<br>in One Sheet.', ko: false, sub: 'One sheet, 45 mL of essence. Cleansing, deodorising, moisturising and soothing — no rinsing. Irritation index 0.00.', img: 'shower-sheet-hero.jpg', en: true },
  { out: 'og-ai-care.jpg',     eyebrow: 'AI Care Continuity', title: '장소와 담당자가 바뀌어도,<br>케어는 이어지도록', ko: true, sub: '음성 기록을 AI가 구조화·요약해 다음 담당자에게 전달합니다.', img: 'img02-record.jpg' },
  { out: 'og-ai-care-en.jpg',  eyebrow: 'AI Care Continuity', title: 'When the place and<br>the people change,<br>care carries on', ko: false, sub: 'AI structures and summarises voice notes and passes them to the next carer.', img: 'img02-record.jpg', en: true },
  { out: 'og-partnership.jpg', eyebrow: 'Global Partnership', title: 'Care, Made<br>in Korea.', ko: false, sub: '일본 · 미국 · 호주 · 독일 · 유럽 — 유통 파트너와 B2B 고객, 자체 브랜드(PB) 공급을 모집합니다.', img: 'img14-warehouse.jpg' },
  { out: 'og-partnership-en.jpg', eyebrow: 'Global Partnership', title: 'Care, Made<br>in Korea.', ko: false, sub: 'Japan · US · Australia · Germany · Europe — seeking distribution partners, B2B customers and private-label supply.', img: 'img14-warehouse.jpg', en: true },
];
(async () => {
  const fs = require('fs'); fs.mkdirSync(path.join(ROOT, 'assets/og'), { recursive: true });
  const b = await chromium.launch();
  const page = await (await b.newContext({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1 })).newPage();
  await page.goto('file://' + path.join(__dirname, 'og.html'));
  for (const c of CARDS) {
    await page.evaluate((c) => {
      document.getElementById('eyebrow').textContent = c.eyebrow;
      const t = document.getElementById('title'); t.innerHTML = c.title; t.className = 'title' + (c.ko ? ' ko' : '');
      const s = document.getElementById('sub'); s.textContent = c.sub; s.className = 'sub' + (c.en ? ' en' : '');
      document.getElementById('img').src = '../../assets/img/' + c.img;
    }, c);
    await page.waitForFunction(() => document.getElementById('img').complete && document.fonts.status === 'loaded');
    await page.waitForTimeout(150);
    await page.locator('#card').screenshot({ path: path.join(ROOT, 'assets/og', c.out), type: 'jpeg', quality: 88 });
    console.log('ok', c.out);
  }
  await b.close();
})();
