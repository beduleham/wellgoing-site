// 파비콘·앱 아이콘 생성: node _build/icons/render.js → assets/icons/
// 크림 모노그램 on 포레스트 배경 (앱 아이콘), 투명 배경 올리브 모노그램 (파비콘)
const { chromium } = require('playwright');
const path = require('path'); const fs = require('fs');
const ROOT = path.resolve(__dirname, '../..');
const OUT = path.join(ROOT, 'assets/icons'); fs.mkdirSync(OUT, { recursive: true });
const svg = (fill) => fs.readFileSync(path.join(ROOT, `assets/img/wellgoing-monogram-${fill}.svg`), 'utf8').replace(/width="\d+" height="\d+"/, 'width="100%" height="100%"');
const page_html = (bg, fill, pad) => `<!doctype html><body style="margin:0;background:${bg};width:100vw;height:100vh;display:grid;place-items:center"><div style="width:${100 - pad * 2}%;height:${100 - pad * 2}%">${svg(fill)}</div></body>`;
const SET = [
  { name: 'favicon-32.png', size: 32, bg: 'transparent', fill: 'olive', pad: 2 },
  { name: 'favicon-16.png', size: 16, bg: 'transparent', fill: 'olive', pad: 0 },
  { name: 'apple-touch-icon.png', size: 180, bg: '#233128', fill: 'cream', pad: 18 },
  { name: 'icon-192.png', size: 192, bg: '#233128', fill: 'cream', pad: 18 },
  { name: 'icon-512.png', size: 512, bg: '#233128', fill: 'cream', pad: 18 },
  { name: 'icon-maskable-512.png', size: 512, bg: '#233128', fill: 'cream', pad: 26 },
];
(async () => {
  const b = await chromium.launch();
  for (const s of SET) {
    const ctx = await b.newContext({ viewport: { width: s.size, height: s.size }, deviceScaleFactor: 1 });
    const p = await ctx.newPage(); await p.setContent(page_html(s.bg, s.fill, s.pad));
    await p.screenshot({ path: path.join(OUT, s.name), omitBackground: s.bg === 'transparent' });
    await ctx.close(); console.log('ok', s.name);
  }
  await b.close();
})();
