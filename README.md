# 웰고잉 홈페이지 (정적 사이트)

빌드 도구 없이 바로 열리는 HTML/CSS/JS 사이트입니다. 폴더째 호스팅에 올리면 됩니다.

## 구조
- `index.html` 메인 · `about.html` 회사 소개 · `ai-care.html` AI 케어 · `products.html` 제품 · `bichae-body-shield.html` 바디쉴드 상세 · `partnership.html` 파트너십 · `contact.html` 문의 · `privacy.html` · `terms.html`
- `assets/css/style.css` — 색·글꼴·여백은 파일 맨 위 토큰만 고치면 전체에 반영
- `assets/js/main.js` — 헤더, 모바일 메뉴, 기본 리빌, 카운트업, 문의 폼. 맨 위 `WG.FORM_ENDPOINT`에 폼 수신 주소 입력
- `assets/js/effects.js` — 화면 효과 6종(페이지 전환 커튼, 헤드라인 마스크, 배경 크로스페이드, 패럴랙스, AI 단계 연동, 사진 클립). 맨 위 `FX` 에서 하나씩 끌 수 있음. 버튼·링크 호버는 style.css 끝부분
- `assets/img` `assets/video` `assets/fonts` — 이미지·영상·영문 서체 (국문 Pretendard는 CDN)
- `_build/` — 디자인 캔버스 구성안에서 페이지를 생성한 스크립트. 사이트 운영에는 필요 없음
- `en/` — 영문 페이지 9개. 직접 고치지 말고 `_build/en/tr_*.py`(번역 사전)를 고친 뒤 `python3 _build/en/build_en.py` 로 다시 생성 (한국어 페이지 수정 후에도 다시 실행)
- `_build/seo.py` + `_build/site.json` — 공유 카드(og:image)·canonical·hreflang·파비콘·JSON-LD·sitemap·robots 를 전 페이지에 일괄 적용. **도메인이 바뀌면 site.json 의 base 만 고치고 `python3 _build/seo.py`** (순서: build_en.py → seo.py)
- `assets/og/` — 카카오톡·문자·슬랙 공유 카드 1200×630 (KR/EN × 기본·AI케어·바디쉴드·파트너십). 다시 만들려면 `node _build/og/render.js`
- `assets/icons/` — 파비콘·아이폰 홈화면 아이콘·manifest (`node _build/icons/render.js`)
- `404.html` — Vercel이 없는 주소에 자동으로 보여줌 · `vercel.json` — 보안·캐시 헤더
- `_build/TODO.md` — 오픈 전 확인 목록

## 배포
- 저장소: github.com/beduleham/wellgoing-site (`main`)
- 호스팅: Vercel — https://wellgoing-site.vercel.app (Framework Preset: Other, 빌드 없음)
- `main`에 push하면 Vercel이 자동으로 재배포합니다. 수정 → 커밋 → push 가 전부입니다.
- 도메인 연결: Vercel 프로젝트 → Settings → Domains 에 `wellgoing.kr` 추가 후, 도메인 DNS에 A `@` → `76.76.21.21`, CNAME `www` → `cname.vercel-dns.com`

## 수정하는 법
- 문구: 해당 html 파일에서 글자를 찾아 바꾸면 됩니다. 섹션마다 `<!-- S04 AI CARE -->` 같은 주석이 있습니다.
- 섹션 색: 섹션 태그의 `data-theme="forest"`를 지우면 크림, 넣으면 녹색.
- 사진 교체: `assets/img`에 같은 이름으로 덮어쓰기.
