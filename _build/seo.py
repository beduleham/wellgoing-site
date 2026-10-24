# -*- coding: utf-8 -*-
"""검색엔진·공유 메타 일괄 적용. 사용: python3 _build/seo.py
- og:image/og:url/canonical/twitter/hreflang/파비콘/manifest/preload/JSON-LD 를 모든 페이지(KR + en/)에 다시 씁니다.
- 도메인이 바뀌면 _build/site.json 의 base 만 고치고 다시 실행하세요.
- 순서: build_en.py → seo.py (영문 페이지를 다시 만든 뒤 실행)"""
import re, os, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG = json.load(open(os.path.join(ROOT, '_build/site.json'), encoding='utf-8'))
BASE = CFG['base'].rstrip('/')
PAGES = ['index', 'about', 'ai-care', 'products', 'bichae-body-shield', 'partnership', 'contact', 'privacy', 'terms', '404']
OG = {'index': 'default', 'bichae-body-shield': 'bichae', 'products': 'bichae', 'ai-care': 'ai-care', 'partnership': 'partnership'}
NOINDEX = {'404'}

ORG = {
  "@context": "https://schema.org", "@type": "Organization", "name": "WELLGOING Co., Ltd.", "alternateName": "주식회사 웰고잉",
  "url": BASE + "/", "logo": BASE + "/assets/icons/icon-512.png", "email": "wellgoing@wellgoing.kr", "telephone": "+82-10-3446-0524",
  "address": {"@type": "PostalAddress", "streetAddress": "419 Chaekhyanggi-ro, 6F 603-3", "addressLocality": "Paju-si", "addressRegion": "Gyeonggi-do", "addressCountry": "KR"},
  "sameAs": ["https://smartstore.naver.com/sobisense"],
}
PRODUCT = {
  "@context": "https://schema.org", "@type": "Product", "name": "Bichae Body Shield", "alternateName": "비채 바디쉴드",
  "brand": {"@type": "Brand", "name": "WELLGOING"}, "image": [BASE + "/assets/img/shower-sheet-hero.jpg", BASE + "/assets/img/packshot-front.jpg"],
  "description": "에센스 45mL를 머금은 프리미엄 세정·보습 샤워시트. 세정·소취·보습·진정을 한 장에, 헹굼 없이. 피부 자극 지수 0.00.",
  "sku": "WG-BBS-5", "countryOfOrigin": "KR",
  "offers": {"@type": "Offer", "url": "https://smartstore.naver.com/sobisense/products/12744315211", "priceCurrency": "KRW", "price": "30000", "availability": "https://schema.org/InStock", "seller": {"@type": "Organization", "name": "WELLGOING Co., Ltd."}},
  "aggregateRating": {"@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "5"},
}

def head_block(p, lang):
    pre = 'en/' if lang == 'en' else ''
    rel = '' if p == 'index' else p + '.html'
    url = f'{BASE}/{pre}{rel}'
    og = OG.get(p, 'default') + ('-en' if lang == 'en' else '')
    asset = '../' if lang == 'en' else ''
    lines = [
        f'<link rel="canonical" href="{url}">',
        f'<link rel="alternate" hreflang="ko" href="{BASE}/{rel}">',
        f'<link rel="alternate" hreflang="en" href="{BASE}/en/{rel}">',
        f'<link rel="alternate" hreflang="x-default" href="{BASE}/{rel}">',
        f'<meta property="og:site_name" content="WELLGOING">',
        f'<meta property="og:locale" content="{"en_US" if lang == "en" else "ko_KR"}">',
        f'<meta property="og:type" content="{"product" if p == "bichae-body-shield" else "website"}">',
        f'<meta property="og:url" content="{url}">',
        f'<meta property="og:image" content="{BASE}/assets/og/og-{og}.jpg">',
        f'<meta property="og:image:width" content="1200">',
        f'<meta property="og:image:height" content="630">',
        f'<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:image" content="{BASE}/assets/og/og-{og}.jpg">',
        f'<meta name="theme-color" content="#233128">',
        f'<link rel="icon" href="{asset}assets/icons/favicon.ico" sizes="32x32">',
        f'<link rel="icon" href="{asset}assets/img/wellgoing-monogram-olive.svg" type="image/svg+xml">',
        f'<link rel="apple-touch-icon" href="{asset}assets/icons/apple-touch-icon.png">',
        f'<link rel="manifest" href="{asset}assets/icons/site.webmanifest">',
        f'<link rel="preload" href="{asset}assets/fonts/instrument-serif-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>',
    ]
    if p in NOINDEX: lines.append('<meta name="robots" content="noindex">')
    if p == 'index': lines.append('<link rel="preload" href="' + asset + 'assets/img/img01-forest-poster.webp" as="image">')
    ld = [ORG] if p in ('index', 'about', 'contact') else []
    if p == 'bichae-body-shield': ld.append(PRODUCT)
    for d in ld: lines.append('<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False) + '</script>')
    return '<!-- seo -->\n' + '\n'.join(lines) + '\n<!-- /seo -->'

STRIP = re.compile(r'^\s*(<!-- /?seo -->|<link[^>]*rel="(canonical|alternate|icon|apple-touch-icon|manifest|preload)"[^>]*>|<link[^>]*(hreflang|type="image/svg\+xml")[^>]*>|<meta[^>]*(property="og:(image|image:width|image:height|type|url|site_name|locale)"|name="(twitter:[a-z]+|theme-color|robots)")[^>]*>|<script type="application/ld\+json">.*?</script>)\s*$\n?', re.M)

def apply(path, p, lang):
    s = open(path, encoding='utf-8').read()
    head_end = s.find('</head>')
    head, rest = s[:head_end], s[head_end:]
    head = STRIP.sub('', head)
    # description 메타 바로 뒤에 삽입 (og:title/og:description 은 원래 자리 유지)
    m = re.search(r'<meta[^>]*name="description"[^>]*>\n?', head)
    i = m.end() if m else head.find('<title>')
    head = head[:i] + head_block(p, lang) + '\n' + head[i:]
    # og:description 다음에 있는 기존 og:* 는 STRIP 으로 제거됨 — og:title/description 만 남음
    open(path, 'w', encoding='utf-8').write(head + rest)

n = 0
for p in PAGES:
    for lang, d in (('ko', ''), ('en', 'en/')):
        f = os.path.join(ROOT, d, p + '.html')
        if os.path.exists(f): apply(f, p, lang); n += 1
print('seo applied to', n, 'pages, base =', BASE)

# sitemap.xml / robots.txt
urls = []
for p in PAGES:
    if p in NOINDEX: continue
    rel = '' if p == 'index' else p + '.html'
    urls.append(f'''  <url><loc>{BASE}/{rel}</loc>
    <xhtml:link rel="alternate" hreflang="ko" href="{BASE}/{rel}"/>
    <xhtml:link rel="alternate" hreflang="en" href="{BASE}/en/{rel}"/>
  </url>
  <url><loc>{BASE}/en/{rel}</loc>
    <xhtml:link rel="alternate" hreflang="ko" href="{BASE}/{rel}"/>
    <xhtml:link rel="alternate" hreflang="en" href="{BASE}/en/{rel}"/>
  </url>''')
open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + '\n'.join(urls) + '\n</urlset>\n')
open(os.path.join(ROOT, 'robots.txt'), 'w', encoding='utf-8').write(f'User-agent: *\nAllow: /\nDisallow: /_build/\n\nSitemap: {BASE}/sitemap.xml\n')
print('sitemap.xml, robots.txt written')
