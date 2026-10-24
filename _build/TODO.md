# 오픈 전 확인 목록

소스 안에서 `<!-- TODO` 로 검색하면 자리를 바로 찾을 수 있습니다.

## 원고로 교체할 것
- about.html — 대표 인사말: 지금은 리플렛 문장으로 쓴 가안. 확정 원고로 교체
- about.html — 연혁 "2025–26 특허 등록·국내외 인증" 행: 각 일자 확인되면 개별 행으로 분리
- ai-care.html — 연결 대상별 설명 4개, 앱 화면 안 문구: 서비스 기획 확정 후 교체
- partnership.html — 진행 절차 5단계: 실제 운영 방식에 맞춰 확정
- bichae-body-shield.html — FAQ 06(사용 범위) · 07(유통기한), 전성분 원문

## 사실 확인
- 연락처: 010-3446-0524 / wellgoing@wellgoing.kr (2026.10 안내지 기준). 2025.09 리플렛의 010-9961-6388 / wellgoing25@gmail.com 와 다름
- 임상시험(2025.04)이 법인 설립(2025.08.13)보다 앞섬 — 연혁 표기 방식 확인
- 사용 후기 설문 응답자 수·기관명
- 통신판매업 신고번호 (푸터)
- 스토어 리뷰 인용: 아이디 마스킹 표기 또는 동의 확보

## 자료
- 회사 소개서 PDF: 지금은 '회사 소개서 요청' 메일 링크(index.html, partnership.html). PDF가 준비되면 assets/docs/ 에 올리고 링크 교체

## 도메인 연결 후
- _build/site.json 의 base 를 새 도메인으로 바꾸고 `python3 _build/seo.py` → 커밋·push
- 카카오톡 공유 캐시 초기화: https://developers.kakao.com/tool/clear/og 에 새 주소 입력
- 네이버 서치어드바이저·구글 서치콘솔에 sitemap.xml 제출

## 설정
- assets/js/main.js 맨 위 `WG.FORM_ENDPOINT` — Formspree 등 폼 수신 주소 입력 (비우면 mailto)
- 지도: 현재 구글 지도 임베드. 네이버/카카오로 바꾸려면 about.html, contact.html 의 `.map-embed` iframe 교체
- 영문 페이지(/en/): 원어민 감수 권장. 문장은 _build/en/tr_*.py 에서 고치고 build_en.py 재실행
- privacy.html, terms.html — 법무 검토 후 게시

## 스토어 쪽
- 상품 대표 이미지를 리뉴얼 패키지로 교체
- 스토어명 '소비센스' → 웰고잉 공식 명칭 검토
