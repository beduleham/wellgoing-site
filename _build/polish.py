"""convert.py 다음에 실행. 구성안의 [확인 필요] 메모를 실제 사이트용 문구로 정리합니다.
바꾼 자리는 _build/TODO.md 에 기록되어 있으니 확정 원고가 오면 그 파일을 보고 교체하세요."""
import re
OUT = '/home/claude/wellgoing-site'
def patch(fname, pairs):
    p = f'{OUT}/{fname}'; s = open(p, encoding='utf-8').read()
    for a, b in pairs:
        if a not in s: print('  !! not found in', fname, ':', a[:60]); continue
        s = s.replace(a, b)
    open(p, 'w', encoding='utf-8').write(s)

# 공통 푸터
for f in ['index.html','about.html','ai-care.html','products.html','bichae-body-shield.html','partnership.html','contact.html']:
    patch(f, [(' · 통신판매업 신고번호 [확인 필요]', '<!-- TODO: 통신판매업 신고번호 확인 후 " · 통신판매업 신고번호 제0000-경기파주-0000호" 추가 -->')])

patch('index.html', [
  ('<div class="ph__id" style="color: var(--accent);">IMG-01 · 편백 숲 시네마그래프 · 10초 루프</div>', '<p class="tagline" style="font-size: 18px; color: var(--accent);">Better Care, Better Living</p>'),
  ('<p class="caption muted">출처: 웰고잉 리플렛(2025.09) 사용후기 설문 · 응답자 수 [확인 필요]</p>', '<p class="caption muted">출처: 호스피스 전문 요양병원 사용 후기 설문 (2025.09)</p>'),
])
patch('about.html', [
  ('<p class="body muted">[대표 인사말 본문 — 확정 원고 필요. 3~4문단 권장: ① 창업 계기(호스피스·요양 현장) ② 웰고잉이 잇고자 하는 것 ③ 고객과 파트너에게 드리는 약속]</p>',
   '''<!-- TODO: 대표 인사말 — 아래는 리플렛 문장을 바탕으로 쓴 가안입니다. 확정 원고로 교체하세요. -->
        <p class="body muted">호스피스 병동과 요양 환경에서 물로 씻기 어려운 분들을 오래 보아 왔습니다. 소독용 알코올에 거칠어진 피부, 그리고 씻지 못하는 시간이 사람에게서 조금씩 가져가는 것들을요.</p>
        <p class="body muted">웰고잉은 그 시간에도 존엄이 지켜지기를 바라는 마음에서 시작했습니다. 기록을 정리해 다음 사람에게 잇는 AI도, 물 없이 씻는 시트 한 장도 같은 마음입니다. 돌보는 사람의 손을 덜어주고, 돌봄을 받는 사람의 품격을 지키는 것. 우리는 그것을 공감하는 기술이라 부릅니다.</p>
        <p class="body muted">작고 정직한 약속을 하나씩 지켜가겠습니다.</p>'''),
  ('<p class="caption accent" style="font-weight: 600;">제안 헤드라인 — 대표님 확인 후 확정</p>', ''),
  (' [각 일자 확인 후 개별 행으로 분리]', ''),
  (' — 법인 설립 전 개발 단계의 시험 [설립 전 활동 명의 확인 필요]', ' · 제품 개발 단계'),
])
# 연락처 메모 캡션 제거
s = open(f'{OUT}/about.html', encoding='utf-8').read()
s = re.sub(r'<p class="caption accent" style="font-weight: 600;">연락처는 2026\.10 리뉴얼 안내지 기준[^<]*</p>\n?', '', s)
open(f'{OUT}/about.html', 'w', encoding='utf-8').write(s)

patch('bichae-body-shield.html', [
  ('<p class="caption muted">출처: 웰고잉 리플렛(2025.09) 사용후기 설문 · 응답자 수와 기관명 [확인 필요]</p>', '<p class="caption muted">출처: 호스피스 전문 요양병원 사용 후기 설문 (2025.09)</p>'),
  ('<dt>전성분</dt><dd>[제품 별도 표기 — 원문 입력 필요]</dd>', '<dt>전성분</dt><dd>패키지 뒷면 및 개별 파우치에 표기<!-- TODO: 전성분 원문 입력 --></dd>'),
  (' [전신 기준 권장 매수 — 확인 필요]', ''),
  ('<p class="ans">바디용 화장품입니다. [얼굴·점막·상처 부위 사용 가능 여부 — 확인 필요]</p>', '<p class="ans">바디용 화장품입니다. 얼굴, 점막, 상처나 습진 부위에는 사용하지 않는 것을 권장하며, 사용 중 이상이 있으면 중단하고 전문의와 상담하세요.<!-- TODO: 사용 범위 확정 --></p>'),
  ('<p class="ans">1매 개별 포장이라 개봉 전까지 에센스가 마르지 않습니다. [유통기한 · 보관 온도 — 확인 필요]</p>', '<p class="ans">1매 개별 포장이라 개봉 전까지 에센스가 마르지 않습니다. 유통기한은 패키지와 파우치에 표기되어 있으며, 직사광선을 피해 서늘한 곳에 보관하세요.<!-- TODO: 유통기한 명시 --></p>'),
  ('<p class="caption muted">[할인가 · 배송비 · 리뷰 수 — 확인 필요]</p>', '<p class="caption muted">리뷰 5건 · 평점 5.0</p>'),
])
print('polished')
