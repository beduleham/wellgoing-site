# -*- coding: utf-8 -*-
"""수출 지도 만들기. 사용: python3 _build/map/build_map.py
- assets/img/world-dots.svg : 점 지도(배경). 점 2,500개를 선 하나로 그려 약 20KB
- index.html / partnership.html 의 <!-- WMAP --> … <!-- /WMAP --> 사이를 지도 컴포넌트로 다시 씁니다
  (경로 선 · 거점 표시 · 글자 라벨은 HTML/SVG 라서 번역되고, 스크롤하면 선이 그려집니다)
시장을 추가·변경하려면 아래 MARKETS 만 고치고 다시 실행하세요. 좌표는 1800×880 지도 기준."""
import os, re
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
W, H = 1800, 880
HUB = (785, 284)
# (key, x, y, 라벨, 영문 보조, 라벨 위치 t/b/l/r, 수출중 여부, 곡선 제어점)
MARKETS = [
    ('jp', 848.5, 295.2, '일본', 'JAPAN', 'b', False, (813.4, 308.6)),
    ('us', 1460.0, 274.6, '미국', 'UNITED STATES', 'r', False, (1124.4, 414.3)),
    ('au', 895.5, 738.3, '호주 · 수출 중', 'AUSTRALIA', 'l', True, (758.5, 531.0)),
    ('de', 217.0, 190.4, '독일', 'GERMANY', 't', False, (486.0, 328.0)),
    ('eu', 161.5, 212.8, '유럽', 'EUROPE', 'b', False, (459.0, 373.1)),
]

# 1) 점 지도: 기존 world-map-olive.svg 의 점 좌표를 읽어 '길이 0 선 + 둥근 끝' 으로 압축
src = os.path.join(ROOT, '_build/map/world-map-source.svg')
dots = [(float(x), float(y)) for x, y in re.findall(r'<circle class="d" cx="([\d.]+)" cy="([\d.]+)"', open(src, encoding='utf-8').read())]
dots.sort(key=lambda p: (p[1], p[0]))
d, px, py = [], None, None
for x, y in dots:
    if py == y and px is not None: d.append(f'm{x - px:g} 0h0')
    else: d.append(f'M{x:g} {y:g}h0')
    px, py = x, y
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">'
       f'<path d="{"".join(d)}" fill="none" stroke="#64773f" stroke-opacity=".42" stroke-width="6.4" stroke-linecap="round"/></svg>\n')
open(os.path.join(ROOT, 'assets/img/world-dots.svg'), 'w').write(svg)
print('world-dots.svg', len(svg) // 1024, 'KB,', len(dots), 'dots')

# 2) 지도 컴포넌트
def component(alt):
    routes, marks, labels = [], [], []
    for i, (k, x, y, ko, en, side, live, (cx, cy)) in enumerate(MARKETS):
        dpath = f'M{HUB[0]} {HUB[1]}Q{cx} {cy} {x} {y}'
        routes.append(f'<path class="wmap__route" pathLength="1" style="--i:{i}" d="{dpath}"/>')
        if live: routes.append(f'<path class="wmap__flow" d="{dpath}"/>')
        marks.append(f'<g class="wmap__pt{" is-live" if live else ""}" style="--i:{i}"><circle class="wmap__ring" cx="{x}" cy="{y}" r="20"/><circle class="wmap__dot" cx="{x}" cy="{y}" r="9"/></g>')
        labels.append(f'<span class="wmap__lb wmap__lb--{side}{" is-live" if live else ""}" style="left:{x / W * 100:.2f}%;top:{y / H * 100:.2f}%;--i:{i}">{ko}<small>{en}</small></span>')
    hub = (f'<g class="wmap__pt wmap__pt--hub is-live" style="--i:-1"><circle class="wmap__ring" cx="{HUB[0]}" cy="{HUB[1]}" r="20"/>'
           f'<circle class="wmap__dot" cx="{HUB[0]}" cy="{HUB[1]}" r="10"/></g>')
    hub_lb = f'<span class="wmap__lb wmap__lb--hub wmap__lb--l" style="left:{HUB[0] / W * 100:.2f}%;top:{HUB[1] / H * 100:.2f}%;--i:-1">한국 · 본사<small>KOREA</small></span>'
    return (f'<!-- WMAP -->\n          <div class="wmap" role="img" aria-label="{alt}">'
            f'<img loading="lazy" decoding="async" src="assets/img/world-dots.svg" alt="">'
            f'<svg class="wmap__svg" viewBox="0 0 {W} {H}" aria-hidden="true">{"".join(routes)}{hub}{"".join(marks)}</svg>'
            f'<div class="wmap__labels" aria-hidden="true" data-tr-each>{hub_lb}{"".join(labels)}</div></div>\n          <!-- /WMAP -->')

ALT = '한국에서 일본, 미국, 호주, 독일, 유럽으로 이어지는 세계 지도'
for f in ['index.html', 'partnership.html']:
    p = os.path.join(ROOT, f); s = open(p, encoding='utf-8').read()
    if '<!-- WMAP -->' in s:
        s = re.sub(r'<!-- WMAP -->.*?<!-- /WMAP -->', lambda m: component(ALT), s, flags=re.S)
    else:
        s, n = re.subn(r'<img [^>]*src="assets/img/world-map-olive\.svg"[^>]*>', lambda m: component(ALT), s)
        assert n == 1, f
    open(p, 'w', encoding='utf-8').write(s)
    print('map →', f)
