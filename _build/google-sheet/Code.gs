/**
 * 웰고잉 홈페이지 문의 → 구글 시트
 * ---------------------------------------------------------------
 * 사이트의 문의 폼(문의하기 / 파트너 문의)이 보낸 내용을 이 스프레드시트에 한 줄씩 쌓고,
 * NOTIFY_EMAIL 로 알림 메일을 보냅니다. 설정 방법은 같은 폴더의 README.md 참고.
 *
 * 시트 탭은 처음 실행할 때 자동으로 만들어집니다: 「문의」, 「파트너 문의」
 * 맨 끝 「처리 상태」 열은 신규 → 진행 중 → 완료 로 직접 바꿔가며 관리하세요.
 */

const NOTIFY_EMAIL = 'wellgoing@wellgoing.kr';   // 알림 받을 메일. 여러 명이면 쉼표로: 'a@x.com,b@y.com'. 끄려면 ''

const FORMS = {
  contact: {
    sheet: '문의',
    cols: [['_ts', '접수 시각'], ['type', '문의 유형'], ['name', '이름'], ['org', '기관·회사'], ['phone', '연락처'], ['email', '이메일'],
           ['message', '문의 내용'], ['_lang', '언어'], ['_page', '페이지'], ['_status', '처리 상태'], ['_memo', '메모']],
  },
  partner: {
    sheet: '파트너 문의',
    cols: [['_ts', '접수 시각'], ['company', '회사명'], ['country', '국가'], ['name', '담당자'], ['email', '이메일'], ['type', '협력 방식'],
           ['message', '메시지'], ['_lang', '언어'], ['_page', '페이지'], ['_status', '처리 상태'], ['_memo', '메모']],
  },
};
const STATUS = ['신규', '진행 중', '완료', '보류'];

/** 사이트에서 문의가 들어올 때 실행됩니다. */
function doPost(e) {
  const lock = LockService.getScriptLock();
  lock.waitLock(15000);
  try {
    const p = (e && e.parameter) || {};
    if (p._hp) return json_({ ok: true });                       // 스팸 봇이 채우는 숨은 칸
    if (!p.consent) return json_({ ok: false, error: 'consent' });
    const form = FORMS[p._form] ? p._form : 'contact';
    const cfg = FORMS[form];
    const sh = sheet_(cfg);
    const now = new Date();
    const row = cfg.cols.map(([k]) => k === '_ts' ? now : k === '_status' ? STATUS[0] : k === '_memo' ? '' : clean_(p[k]));
    sh.appendRow(row);
    try { notify_(cfg, p, now); } catch (mailErr) { console.warn('알림 메일 실패: ' + mailErr); }
    return json_({ ok: true });
  } catch (err) {
    console.error(err);
    return json_({ ok: false, error: String(err) });
  } finally {
    lock.releaseLock();
  }
}

/** 주소창에서 열면 연결 확인용 응답을 보여줍니다. */
function doGet() {
  return json_({ ok: true, service: 'wellgoing-form', sheet: SpreadsheetApp.getActiveSpreadsheet().getName() });
}

/** 처음 한 번 실행: 권한 승인 + 시트 탭 2개를 미리 만들어 둡니다. */
function setup() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  ss.setSpreadsheetTimeZone('Asia/Seoul');
  Object.values(FORMS).forEach(sheet_);
  const first = ss.getSheets()[0];
  if (first.getName().match(/^(Sheet1|시트1)$/) && first.getLastRow() === 0 && ss.getSheets().length > 1) ss.deleteSheet(first);
  if (NOTIFY_EMAIL) MailApp.getRemainingDailyQuota(); // 메일 권한도 같이 승인받기 위해 호출
  console.log('준비 완료: ' + ss.getUrl());
}

/* ---------- 내부 함수 ---------- */
function sheet_(cfg) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sh = ss.getSheetByName(cfg.sheet);
  if (sh) return sh;
  sh = ss.insertSheet(cfg.sheet);
  const n = cfg.cols.length;
  sh.getRange(1, 1, 1, n).setValues([cfg.cols.map((c) => c[1])])
    .setFontWeight('bold').setBackground('#233128').setFontColor('#faf8f0').setVerticalAlignment('middle');
  sh.setFrozenRows(1);
  sh.setRowHeight(1, 32);
  sh.getRange('A2:A').setNumberFormat('yyyy-mm-dd hh:mm');
  sh.getRange(2, 2, sh.getMaxRows() - 1, n - 1).setNumberFormat('@').setVerticalAlignment('top');   // 전화번호 앞자리 0 보존
  const msgCol = cfg.cols.findIndex((c) => c[0] === 'message') + 1;
  sh.setColumnWidth(1, 140);
  sh.setColumnWidth(msgCol, 380);
  sh.getRange(2, msgCol, sh.getMaxRows() - 1, 1).setWrap(true);
  const stCol = cfg.cols.findIndex((c) => c[0] === '_status') + 1;
  sh.getRange(2, stCol, sh.getMaxRows() - 1, 1).setDataValidation(
    SpreadsheetApp.newDataValidation().requireValueInList(STATUS, true).setAllowInvalid(false).build());
  const rule = (txt, bg) => SpreadsheetApp.newConditionalFormatRule().whenTextEqualTo(txt).setBackground(bg)
    .setRanges([sh.getRange(2, stCol, sh.getMaxRows() - 1, 1)]).build();
  sh.setConditionalFormatRules([rule('신규', '#e7eade'), rule('진행 중', '#fdf1d6'), rule('완료', '#eeeeee')]);
  return sh;
}

function clean_(v) {
  v = String(v == null ? '' : v).slice(0, 5000).trim();
  return /^[=+\-@]/.test(v) ? "'" + v : v;   // 수식으로 해석되지 않게
}

function notify_(cfg, p, now) {
  if (!NOTIFY_EMAIL) return;
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const who = p.name || p.company || '';
  const body = cfg.cols
    .filter(([k]) => !['_ts', '_status', '_memo'].includes(k))
    .map(([k, label]) => `${label}: ${p[k] || '-'}`).join('\n');
  const opts = {
    to: NOTIFY_EMAIL,
    subject: `[웰고잉 ${cfg.sheet}] ${p.type ? p.type + ' · ' : ''}${who}`,
    body: `${Utilities.formatDate(now, 'Asia/Seoul', 'yyyy-MM-dd HH:mm')} 홈페이지로 새 ${cfg.sheet}가 들어왔습니다.\n\n${body}\n\n시트에서 보기: ${ss.getUrl()}`,
    name: '웰고잉 홈페이지',
  };
  if (/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(p.email || '')) opts.replyTo = p.email;   // 메일에서 바로 '답장'하면 문의자에게
  MailApp.sendEmail(opts);
}

function json_(o) {
  return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON);
}
