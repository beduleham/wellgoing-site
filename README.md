# 웰고잉 홈페이지 (정적 사이트)

빌드 도구 없이 바로 열리는 HTML/CSS/JS 사이트입니다. 폴더째 호스팅에 올리면 됩니다.

## 구조
- `index.html` 메인 · `about.html` 회사 소개 · `ai-care.html` AI 케어 · `products.html` 제품 · `bichae-body-shield.html` 바디쉴드 상세 · `partnership.html` 파트너십 · `contact.html` 문의 · `privacy.html` · `terms.html`
- `assets/css/style.css` — 색·글꼴·여백은 파일 맨 위 토큰만 고치면 전체에 반영
- `assets/js/main.js` — 헤더, 모바일 메뉴, 기본 리빌, 카운트업, 문의 폼. 맨 위 `WG.FORM_ENDPOINT`에 폼 수신 주소 입력
- `assets/js/effects.js` — 화면 효과 6종(페이지 전환 커튼, 헤드라인 마스크, 배경 크로스페이드, 패럴랙스, AI 단계 연동, 사진 클립). 맨 위 `FX` 에서 하나씩 끌 수 있음. 버튼·링크 호버는 style.css 끝부분
- `assets/img` `assets/video` `assets/fonts` — 이미지·영상·영문 서체 (국문 Pretendard는 CDN)
- `_build/` — 디자인 캔버스 구성안에서 페이지를 생성한 스크립트. 사이트 운영에는 필요 없음
- `_build/TODO.md` — 오픈 전 확인 목록

## 올리는 법
Vercel / Netlify / Cloudflare Pages: 이 폴더를 그대로 드래그하거나 GitHub 저장소를 연결. 카페24 등 일반 호스팅: FTP로 폴더 내용을 루트에 업로드.

## 수정하는 법
- 문구: 해당 html 파일에서 글자를 찾아 바꾸면 됩니다. 섹션마다 `<!-- S04 AI CARE -->` 같은 주석이 있습니다.
- 섹션 색: 섹션 태그의 `data-theme="forest"`를 지우면 크림, 넣으면 녹색.
- 사진 교체: `assets/img`에 같은 이름으로 덮어쓰기.
