"""구성안(.dc.html) → 실제 페이지(.html) 변환기.
한 번 변환한 뒤에는 생성된 html을 직접 고쳐도 됩니다. 다시 돌리면 덮어씁니다."""
import re, os, sys
SRC = '/tmp/claude-0/-home-claude/79e41662-462e-5003-bcd3-3f68383d08e9/scratchpad/canvas/project'
OUT = '/home/claude/wellgoing-site'

PAGES = {
  'Main':        ('index.html',              '웰고잉 — Care, Connected by AI', '케어 현장의 기록을 AI로 잇고, 물 없이도 존엄한 위생을 지키는 비채 바디쉴드를 만듭니다.', None),
  'About':       ('about.html',              '회사 소개 — 웰고잉', '공감하는 기술로 존엄한 케어를 만드는 프리미엄 헬스케어 브랜드, 주식회사 웰고잉.', 'about'),
  'AICare':      ('ai-care.html',            'AI 케어 서비스 — 웰고잉', '장소와 담당자가 바뀌어도 케어가 이어지도록. 음성 기록을 AI가 구조화·요약해 다음 담당자에게 전달합니다.', 'ai'),
  'Products':    ('products.html',           '제품 — 웰고잉', '현장의 필요에서 출발한 케어 제품. 비채 바디쉴드와 비채 덴트쉴드.', 'products'),
  'BodyShield':  ('bichae-body-shield.html', '비채 바디쉴드 — 에센스로 씻는 샤워시트 | 웰고잉', '씻지 못하는 시간에도 피부의 존엄을 지키다. 편백수·판테놀·5종 세라마이드, 피부 자극 지수 0.00.', 'products'),
  'Partnership': ('partnership.html',        '글로벌 파트너십 — 웰고잉', '일본·미국·호주·독일, 그리고 유럽. 유통 파트너와 B2B 고객, 자체 브랜드(PB) 공급을 모집합니다.', 'partnership'),
  'Contact':     ('contact.html',            '문의 — 웰고잉', 'AI 케어 서비스 도입, 제품 구매, 해외 파트너십 문의.', 'contact'),
}
LINKS = {k: v[0] for k, v in PAGES.items()}

BLOBS = {
 '718c714467c1439eb000f3d9cbd6abf1':'shower-sheet-hero.jpg','3d64870b77092eed3d44029c4984e6f8':'hinoki-botanical.jpg',
 '374e6964cdec6a6477b4cf44f3474ca5':'essence-texture.jpg','2449eb6842c60cc1e3e7391e760138a8':'body-shield-lifestyle.jpg',
 '5fd268e11df5dfc070a52c87c1549798':'wellgoing-signature-olive.svg','dbdc04f3a2a0ac7a4a90a4ce81e3febc':'wellgoing-signature-cream.svg',
 '48904cfc4d59cff0bf6c25e189d58dbb':'wellgoing-monogram-olive.svg','500e63499cc81fd2f4d4c839a716ce67':'wellgoing-monogram-cream.svg',
 'cd6867e6cdbd243de63fdb7442e8090a':'wellgoing-wordmark-forest.svg','33abca7f7955e90cca175c6e55597799':'wellgoing-wordmark-cream.svg',
 '9bb7b6879abf8e88bd061614bea4bcb0':'packshot-front.jpg','ca6cb915dce4ee048fbe4c3f0c7aecce':'packshot-front-back.jpg','9ce946a305ed91aaf28c5e4ae27fc6ab':'package-front-flat.jpg',
 '6663d5a77d5e9c2db10ba19875db136b':'dent-shield-lineart.png',
 'e35d1d900aa547735cc9f558e666e722':'img01-forest.jpg','5828e7d1b0c0cab04559344aa3ef9595':'img02-record.jpg','ec78dbecd3c0b48a053333e3b52e38d1':'img03-room.jpg',
 '0b861cfd9061e80717c1fbe12111604c':'img05-corridor.jpg','602ac1e3cec4e73621f1b177fa70404f':'img06-hands.jpg','abf0ac6d7ca5107a31dce3a009c19aed':'img09-station.jpg',
 'd335b458300b4242f5bee050d0166e00':'img11-dent.jpg','6be2137df184289c87daaf1b7a6938b0':'img14-warehouse.jpg',
 '7649b923d4bb75eafdba170b59794781':'../video/forest-hero.mp4','f6bfc558998f838734a7fda538b68917':'img01-forest-poster.jpg','f1858794d7b9c51c06bbffe0cbdb2800':'world-map-olive.svg',
}

MAP_EMBED = '<iframe class="map-embed" title="웰고잉 위치 — 경기도 파주시 책향기로 419 웰스피아" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://maps.google.com/maps?q=%EA%B2%BD%EA%B8%B0%EB%8F%84+%ED%8C%8C%EC%A3%BC%EC%8B%9C+%EC%B1%85%ED%96%A5%EA%B8%B0%EB%A1%9C+419&z=16&output=embed"></iframe>'

def header(active):
    nav = [('about','about.html','회사 소개'),('ai','ai-care.html','AI 케어'),('products','products.html','제품'),('partnership','partnership.html','파트너십')]
    li = ''.join(f'<li><a href="{h}"{" class=\"on\"" if k==active else ""}>{t}</a></li>' for k,h,t in nav)
    mli = ''.join(f'<li><a href="{h}"><span>0{i+1}</span>{t}</a></li>' for i,(k,h,t) in enumerate(nav))
    return f'''<a class="skip" href="#main">본문으로 건너뛰기</a>
<header class="hdr" data-theme="cream">
  <div class="wrap hdr__in">
    <a href="index.html" aria-label="WELLGOING 홈"><img class="hdr__logo hdr__logo--forest" src="assets/img/wellgoing-wordmark-forest.svg" alt="WELLGOING"><img class="hdr__logo hdr__logo--cream" src="assets/img/wellgoing-wordmark-cream.svg" alt=""></a>
    <ul class="hdr__nav">{li}</ul>
    <span class="hdr__lang" title="영문 페이지 준비 중"><b>KR</b> · EN</span>
    <a class="btn btn--solid btn--sm" href="contact.html">문의하기</a>
    <button class="hdr__burger" type="button" aria-label="메뉴 열기" aria-expanded="false"><svg viewBox="0 0 24 24"><path d="M3 7h18M3 12h18M3 17h18"/></svg></button>
  </div>
</header>
<nav class="mnav" aria-label="모바일 메뉴">
  <div class="mnav__top"><img src="assets/img/wellgoing-wordmark-cream.svg" alt="WELLGOING" style="height:14px"><button class="mnav__close" type="button" aria-label="메뉴 닫기"><svg viewBox="0 0 24 24"><path d="M5 5l14 14M19 5L5 19"/></svg></button></div>
  <ul class="mnav__list">{mli}<li><a href="contact.html"><span>05</span>문의</a></li></ul>
  <div class="mnav__foot"><span>010-3446-0524</span><span>wellgoing@wellgoing.kr</span><a href="https://smartstore.naver.com/sobisense/products/12744315211" style="color:#faf8f0">네이버 스마트스토어 →</a></div>
</nav>'''

FOOTER = '''<footer data-theme="forest" style="background: var(--surface); color: var(--ink);">
  <div class="wrap ftr">
    <div class="ftr__top">
      <img src="assets/img/wellgoing-signature-cream.svg" alt="WELLGOING Better Care, Better Living" style="width: 150px; height: auto; display: block;">
      <div class="ftr__cols">
        <div><h5>Company</h5><ul><li><a href="about.html">회사 소개</a></li><li><a href="about.html#cert">인증·특허</a></li><li><a href="about.html#location">오시는 길</a></li></ul></div>
        <div><h5>Business</h5><ul><li><a href="ai-care.html">AI 케어 서비스</a></li><li><a href="products.html">케어 제품</a></li><li><a href="partnership.html">글로벌 파트너십</a></li><li><a href="https://smartstore.naver.com/sobisense/products/12744315211" target="_blank" rel="noopener">스마트스토어</a></li></ul></div>
        <div><h5>Contact</h5><ul class="muted"><li><a href="tel:010-3446-0524">010-3446-0524</a></li><li><a href="mailto:wellgoing@wellgoing.kr">wellgoing@wellgoing.kr</a></li><li>경기도 파주시 책향기로 419, 6층 603-3호 (동패동, 웰스피아)</li></ul></div>
      </div>
    </div>
    <div class="ftr__bottom">
      <span>주식회사 웰고잉 · 대표 손영옥 · 사업자등록번호 129-88-03719 · 통신판매업 신고번호 [확인 필요]</span>
      <span style="display: flex; gap: 20px;"><a href="privacy.html" style="text-decoration: none;">개인정보처리방침</a><a href="terms.html" style="text-decoration: none;">이용약관</a><span>© Wellgoing Co., Ltd.</span></span>
    </div>
  </div>
</footer>'''

def shell(title, desc, body, active, fname):
    return f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://www.wellgoing.kr/assets/img/shower-sheet-hero.jpg">
<meta property="og:type" content="website">
<meta property="og:url" content="https://www.wellgoing.kr/{'' if fname=='index.html' else fname}">
<link rel="icon" href="assets/img/wellgoing-monogram-olive.svg" type="image/svg+xml">
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
<script>try{if(sessionStorage.getItem("wgNav")){document.documentElement.classList.add("is-entering");sessionStorage.removeItem("wgNav")}}catch(e){}</script>
<link rel="stylesheet" href="assets/css/fonts-local.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
<link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
{header(active)}
<main id="main" class="page">
{body}
</main>
{FOOTER}
<script src="assets/js/main.js"></script>
<script src="assets/js/effects.js"></script>
</body>
</html>
'''

def convert(key):
    fname, title, desc, active = PAGES[key]
    s = open(f'{SRC}/{key}.dc.html', encoding='utf-8').read()
    body = s[s.index('<div class="page"'):]
    body = body[body.index('>')+1: body.rindex('</div>\n</x-dc>')]
    # 구성안 전용 요소 제거
    body = re.sub(r'<span class="anno"[^>]*>.*?</span>\n?', '', body, flags=re.S)
    body = re.sub(r'<header class="hdr[^"]*"[^>]*>.*?</header>\n?', '', body, flags=re.S)
    body = re.sub(r'<footer data-theme="forest"[^>]*>.*?</footer>\n?', '', body, flags=re.S)
    # 메인의 S11: 푸터 부분만 떼고 CTA는 남김
    body = re.sub(r'<footer class="wrap ftr">.*?</footer>\n?', '', body, flags=re.S)
    # 지도 플레이스홀더 → 임베드
    body = re.sub(r'<div class="ph"[^>]*>\s*<span class="ph__r">[^<]*</span>\s*<span class="ph__id">IMG-08</span>.*?</div>', MAP_EMBED, body, flags=re.S)
    # 구성안 메모 캡션 제거
    body = re.sub(r'<p class="caption (?:accent|muted)"[^>]*>[^<]*(?:확인 후 확정|초안|가안|제안 문장|제안 헤드라인|추후 선택|교체 예정|임시 구성|교체 (?:필요|권장)|공통 푸터|구성안|제가 처리|스크롤에 맞춰|인쇄 파일로 만든|AI 렌더 시안|영상 대신)[^<]*</p>\n?', '', body)
    # 리소스 경로
    for k, v in BLOBS.items():
        body = body.replace(f'/_blob/{k}', f'assets/img/{v}' if not v.startswith('../') else f'assets/{v[3:]}')
    for k, v in LINKS.items():
        body = body.replace(f'{k}.dc.html', v)
    # 앵커 id
    body = body.replace('<!-- A05 CERTIFICATIONS -->\n  <section class="sec" data-theme="deep">', '<!-- A05 CERTIFICATIONS -->\n  <section class="sec" data-theme="deep" id="cert">')
    body = body.replace('<!-- A06 LOCATION -->\n  <section class="sec">', '<!-- A06 LOCATION -->\n  <section class="sec" id="location">')
    # 제품 히어로: 반응형 클래스
    body = body.replace('<div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); min-height: 880px;">', '<div class="hero-split">')
    body = body.replace('<div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); min-height: 900px;">', '<div class="hero-split" style="min-height: 900px;">')
    body = re.sub(r'<div style="padding: 120px 64px (?:64|56)px max\(32px, calc\(\(100vw - 1280px\) / 2 \+ 32px\)\); display: flex; flex-direction: column; gap: 20px;">', '<div class="hero-split__copy">', body)
    body = body.replace('<div style="position: relative;"><img class="photo" src="assets/img/shower-sheet-hero.jpg"', '<div class="hero-split__media"><img class="photo" src="assets/img/shower-sheet-hero.jpg"')
    body = body.replace('<div style="grid-column: 1 / span 12; display: grid; grid-template-columns: repeat(2, minmax(0,1fr)); column-gap: 48px;">', '<div class="cols2" style="grid-column: 1 / span 12; column-gap: 48px;">')
    body = body.replace('<ol style="grid-column: 1 / span 6; list-style: none; padding: 0; display: flex; flex-direction: column;">', '<ol data-steps class="is-sync" style="grid-column: 1 / span 6; list-style: none; padding: 0; display: flex; flex-direction: column;">')
    # 외부 링크 새 창
    body = body.replace('href="https://smartstore.naver.com/sobisense/products/12744315211"', 'href="https://smartstore.naver.com/sobisense/products/12744315211" target="_blank" rel="noopener"')
    # 폼: 실제 동작 속성
    body = body.replace('<form class="form"', '<form class="form" data-wg-form method="post" action="#"')
    body = body.replace('<a class="btn btn--solid" href="#">문의 보내기 <span>→</span></a>', '<button class="btn btn--solid" type="submit">문의 보내기 <span>→</span></button><p class="form-note" role="status"></p>')
    # 비디오 자동재생
    body = body.replace('<video src="assets/video/forest-hero.mp4"', '<video src="assets/video/forest-hero.mp4" preload="metadata"')
    # 카운트업
    body = body.replace('<p class="n-xl" style="grid-column: 1 / span 5;">0.00</p>', '<p class="n-xl" style="grid-column: 1 / span 5;" data-count="0.00">0.00</p>')
    body = body.replace('<p class="n-xl">0.00</p>', '<p class="n-xl" data-count="0.00">0.00</p>')
    html = shell(title, desc, body, active, fname)
    open(f'{OUT}/{fname}', 'w', encoding='utf-8').write(html)
    left = re.findall(r'(?:ph__id|/_blob/|\.dc\.html|anno)', html)
    print(fname, len(html), 'leftovers:', len(left))

for k in PAGES: convert(k)
