# -*- coding: utf-8 -*-
"""사이트 전용 한글 폰트(Pretendard WG) 다시 만들기. 사용: python3 _build/font_subset.py
페이지에 새 글자가 생겼을 때 실행하면 assets/fonts/pretendard-wg.woff2 를 다시 만듭니다.
(실행하지 않아도 빠진 글자는 전체 Pretendard 로 자동 대체되므로 깨지지는 않습니다.)
필요: pip install fonttools brotli beautifulsoup4 lxml"""
import os, glob, subprocess
from bs4 import BeautifulSoup
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
chars = set()
for f in glob.glob(os.path.join(ROOT, '*.html')) + glob.glob(os.path.join(ROOT, 'en', '*.html')):
    soup = BeautifulSoup(open(f, encoding='utf-8').read(), 'lxml')
    for s in soup(['script', 'style']): s.decompose()
    chars |= set(soup.get_text())
    for t in soup.find_all(True):
        for a in ('alt', 'title', 'aria-label', 'placeholder', 'value'):
            if t.get(a): chars |= set(t[a])
chars |= set(open(os.path.join(ROOT, 'assets/js/main.js'), encoding='utf-8').read())
txt = os.path.join(ROOT, '_build/fonts/chars.txt')
open(txt, 'w', encoding='utf-8').write(''.join(sorted(c for c in chars if ord(c) >= 0x20)))
out = os.path.join(ROOT, 'assets/fonts/pretendard-wg.woff2')
subprocess.run(['pyftsubset', os.path.join(ROOT, '_build/fonts/PretendardVariable.woff2'), '--text-file=' + txt,
                '--unicodes=U+0020-007E,U+00A0-00FF,U+2010-2027,U+2030,U+2032-2033,U+2190-2193,U+2122,U+2103',
                '--layout-features=kern,liga,calt,ccmp,locl,mark,mkmk,tnum', '--flavor=woff2', '--output-file=' + out], check=True)
print('한글', sum('가' <= c <= '힣' for c in chars), '자 →', out, os.path.getsize(out) // 1024, 'KB')
