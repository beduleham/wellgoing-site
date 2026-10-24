# -*- coding: utf-8 -*-
"""한국어 페이지 → /en/ 영어 페이지 생성.
사용: python3 _build/en/build_en.py
번역은 tr_*.py 의 사전(원문 HTML 조각 → 영어)을 씁니다. 한국어 페이지를 고친 뒤 다시 실행하면
영어 페이지가 다시 만들어집니다. 사전에 없는 한국어 문장은 마지막에 목록으로 출력됩니다."""
import re, sys, os, importlib.util
from bs4 import BeautifulSoup, NavigableString, Comment, Tag

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, 'en')
os.makedirs(OUT, exist_ok=True)

T, A = {}, {}
for f in ['tr_about_ai.py', 'tr_product.py', 'tr_index_rest.py']:
    spec = importlib.util.spec_from_file_location(f[:-3], os.path.join(HERE, f)); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    T.update(m.T); A.update(getattr(m, 'A', {}))

PAGES = ['index', 'about', 'ai-care', 'products', 'bichae-body-shield', 'partnership', 'contact', 'privacy', 'terms']
INLINE = {'br', 'span', 'strong', 'em', 'i', 'b', 'sup', 'sub', 'a', 'abbr', 'time', 'svg', 'path', 'rect', 'circle', 'line', 'polyline', 'g', 'small', 'u', 's', 'label'}
KO = re.compile(r'[가-힣]')
norm = lambda h: re.sub(r'\s*\n\s*', ' ', h.strip())

def inline_only(el):
    return all(isinstance(c, NavigableString) or (isinstance(c, Tag) and c.name in INLINE and inline_only(c)) for c in el.children)

missing = {}
def translate_page(p):
    html = open(os.path.join(ROOT, p + '.html'), encoding='utf-8').read()
    soup = BeautifulSoup(html, 'lxml')
    done = set()
    for t in list(soup.find_all(string=True)):
        if isinstance(t, Comment) or t.parent is None or t.find_parent('html') is None or t.parent.name in ('script', 'style') or not KO.search(str(t)): continue
        el = t.parent
        while el.name in INLINE and el.parent is not None and inline_only(el.parent) and el.parent.name not in ('body', 'html', '[document]') and not el.parent.has_attr('data-tr-each'):
            el = el.parent
        if el.name in INLINE or inline_only(el):
            if id(el) in done: continue
            done.add(id(el))
            key = norm(el.decode_contents())
            if key in T:
                el.clear(); el.append(BeautifulSoup(T[key], 'html.parser'))
            else:
                missing.setdefault(key, []).append(p)
        else:
            key = str(t).strip()
            if key in T: t.replace_with(T[key])
            else: missing.setdefault(key, []).append(p)
    # 속성
    for tag in soup.find_all(True):
        for a in ('alt', 'title', 'aria-label', 'placeholder', 'content'):
            v = tag.get(a)
            if v and KO.search(v):
                if v in A: tag[a] = A[v]
                else: missing.setdefault('[' + a + '] ' + v, []).append(p)
    out = str(soup).replace(' viewbox="', ' viewBox="').replace(' pathlength="', ' pathLength="')
    # 언어·경로·메타
    out = out.replace('<html lang="ko">', '<html lang="en">')
    out = re.sub(r'(href|src|poster|srcset|data-src|data-src-m)="assets/', r'\1="../assets/', out)
    out = out.replace('https://www.wellgoing.kr/' + p + '.html', 'https://www.wellgoing.kr/en/' + p + '.html')
    out = out.replace('content="https://www.wellgoing.kr/"', 'content="https://www.wellgoing.kr/en/"')
    # 언어 전환: 데스크톱 헤더 + 모바일 메뉴
    kr_href = '../' + ('' if p == 'index' else p + '.html')
    out = re.sub(r'<span class="hdr__lang"[^>]*>.*?</span>', f'<span class="hdr__lang"><a href="{kr_href}">KR</a> · <b>EN</b></span>', out, count=1)
    lang_m = f'<div class="mnav__lang"><a href="{kr_href}">KR</a> · <b>EN</b></div>'
    if '<div class="mnav__lang">' in out: out = re.sub(r'<div class="mnav__lang">.*?</div>', lang_m, out, count=1)
    else: out = out.replace('<div class="mnav__foot">', lang_m + '<div class="mnav__foot">', 1)
    # 전화번호 국제 표기
    out = re.sub(r'(?<!\+82 )010-3446-0524', '+82 10-3446-0524', out).replace('placeholder="010-0000-0000"', 'placeholder="+82 10-0000-0000"')
    # hreflang
    alt = f'<link rel="alternate" hreflang="ko" href="https://www.wellgoing.kr/{"" if p=="index" else p+".html"}">\n<link rel="alternate" hreflang="en" href="https://www.wellgoing.kr/en/{"" if p=="index" else p+".html"}">\n'
    out = out.replace('<link rel="icon"', alt + '<link rel="icon"', 1)
    open(os.path.join(OUT, p + '.html'), 'w', encoding='utf-8').write(out)

for p in PAGES: translate_page(p)
if missing:
    print('번역 없음:', len(missing))
    for k, v in missing.items(): print(' ', v[0], '|', k[:120])
else:
    print('모든 문장 번역됨')

# 한국어 페이지 쪽 언어 전환 링크도 연결
for p in PAGES:
    f = os.path.join(ROOT, p + '.html'); s = open(f, encoding='utf-8').read()
    en_href = 'en/' + ('' if p == 'index' else p + '.html')
    s2 = re.sub(r'<span class="hdr__lang"[^>]*>.*?</span>', f'<span class="hdr__lang"><b>KR</b> · <a href="{en_href}">EN</a></span>', s, count=1)
    if '<div class="mnav__lang">' not in s2:
        s2 = s2.replace('<div class="mnav__foot">', f'<div class="mnav__lang"><b>KR</b> · <a href="{en_href}">EN</a></div><div class="mnav__foot">', 1)
    else:
        s2 = re.sub(r'<div class="mnav__lang">.*?</div>', f'<div class="mnav__lang"><b>KR</b> · <a href="{en_href}">EN</a></div>', s2, count=1)
    if s2 != s: open(f, 'w', encoding='utf-8').write(s2)
print('KR 전환 링크 갱신')
