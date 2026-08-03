# PURYNN 데일리 카드뉴스 — 회사 계정 이관 기록

이관 완료 2026-08-03 · 대상 계정 **연구개발팀 (bigpie_up@jungdari.com)**

원본 이관 가이드는 4개 시스템(Higgsfield / Notion / 워크스페이스 폴더 / 스케줄)을 정의합니다.
아래는 이 저장소에서 실제로 완료된 작업과 남은 수동 단계입니다.

## ✅ 완료된 작업

### 1. Higgsfield 자산 5개 이관
구 계정 CDN(공개)에서 회사 Higgsfield 계정으로 **원본 그대로 복사**했습니다.
로컬 원본 파일 없이 공개 CDN → 신규 계정 업로드로 처리했고, 5개 모두 content-length 일치 검증 통과.

- 신규 CDN base: `https://d2ol7oe51mr4n9.cloudfront.net/user_2zrIhlq0Y8juUmY7o3n04KjTZBJ`
- 신규 업로드 base: `https://upload.higgsfield.ai/user_2zrIhlq0Y8juUmY7o3n04KjTZBJ`
- Higgsfield MCP 커넥터: 이름 기반(`mcp__HIGGSFIELD__sandbox_exec`) — UUID 아님
- 크레딧: **605 (pro)** — 구 계정 2.84 대비 충분. 월 150+ 요구사항 충족.

### 2. Notion "PURYNN Content Log" DB
동일 스키마로 회사 워크스페이스에 생성 + 과거 35개 주제명 시드(중복 방지).

- 신규 data_source_id: `966d82e0-aa69-4bb1-af02-e0dfa7eac741`
- DB URL: https://app.notion.com/p/3cecc61f56224621b3f316a6ee0c2650
- 시드된 35개 주제는 Status=`Posted`, Sources=`Migrated history · old account`.

> ⚠️ 캡션·해시태그까지 무손실로 옮기려면 구 워크스페이스에서 Export(Markdown & CSV) → Import 하세요.
> 지금은 중복 방지를 위해 **주제명만** 시드된 상태입니다.

### 3. SKILL.md
플레이스홀더 9개를 모두 실제 값으로 채워 저장소 루트에 커밋. 원본 대비 반영된 수정:
- 🐞 로고 비율: 알파 bbox 트림 후 226×119, (117,91) 배치 (렌더러에 반영)
- 🐞 CDN 캐시 불변성: 수정본은 항상 신규 media_id 발급 (STEP 4 경고문)

### 4. 렌더 툴킷
`PURYNN_피드_이미지/_assets/purynn_cards.py` — SKILL STEP 4 사양의 참조 구현.
`products/manifest.json` — 신규 media_id + Toner/Essence 스왑 경고.

## 🗓 스케줄

- 등록 완료: **매일 09:00 KST (UTC 00:00, cron `0 0 * * *`)**, fresh-session 방식.
  - Routine ID: `trig_011UeMNUajrYYfH6E8wYR1oJ` · 첫 실행 2026-08-04 09:03 KST
  - 발화 시 저장소가 클론된 새 세션에서 `SKILL.md`를 읽어 STEP 1~8을 자동 실행.

> ⚠️ **커넥터 확인 필요 (중요):** 이 방식으로 만든 Routine은 발화되는 새 세션에
> Higgsfield·Notion **커넥터(mcp__* 도구)가 붙지 않을 수 있습니다.** 그러면 렌더/업로드/
> Notion 기록이 불가해 실행이 실패합니다. 가장 확실한 방법은 **claude.ai Routines UI에서**
> 이 Routine을 열어 Higgsfield·Notion 커넥터를 연결하는 것입니다. 8/4 첫 실행 결과를 보고
> Notion에 새 페이지가 생기면 정상, 안 생기면 UI에서 커넥터를 붙여 주세요.

## ⏳ 남은 수동 단계

- [ ] **구 계정 스케줄 해제**: 두 계정이 동시에 켜져 있으면 같은 날 서로 다른 주제로
      이중 발행 + 로그 미공유로 중복이 발생합니다. 반드시 구 작업을 끄세요. (구 계정은
      이 세션에서 접근 불가 — 직접 해제해야 합니다.)
- [ ] **위 커넥터 확인** (Routines UI에서 Higgsfield·Notion 연결 확인).
- [ ] (선택) 구 Notion DB Export/Import로 캡션·해시태그 이력까지 무손실 이관.
- [ ] (선택) 회사 드라이브에 `PURYNN_피드_이미지` 폴더 사본 유지 시 원본 누끼 PNG를
      `_assets/products/`에 넣기 (STEP 5 로컬 마스터용). 스왑 주의.

## 부록 — 교체값 대응표

| 항목 | 구 계정 값 | 회사 계정 값 |
|------|-----------|-------------|
| CDN base | `…/user_320TDOQlq5eoC0Ix9LCuwou9CG5` | `…/user_2zrIhlq0Y8juUmY7o3n04KjTZBJ` |
| 업로드 base | `…/user_320TDOQlq5eoC0Ix9LCuwou9CG5` | `…/user_2zrIhlq0Y8juUmY7o3n04KjTZBJ` |
| logo media_id | `7ac3d25c-f1e0-4629-aaf0-ddebf383fa4e` | `335fd260-0463-4ea9-8e01-5ce97f8c214d` |
| toner media_id | `4bdcc594-b977-4740-8b8e-8de657f924f7` | `bd0b4760-35fb-48d4-8693-8c506974f0fd` |
| essence media_id | `bba2814f-6e5d-4cbc-bb44-b13477f3f157` | `0a1e7932-be79-4b95-a9aa-8446ec9c3e23` |
| ampoule media_id | `4ca80d62-2d26-49d7-97ac-8415f10bb8c2` | `4b91cb95-a81b-4251-9733-5dcfc143f1d7` |
| cream media_id | `7c75b4bf-266d-467a-acd8-9ade6ee5d22c` | `e224b5db-0ff6-4279-92d2-84b86af9c719` |
| Notion data_source_id | `a0f96979-3a24-4f76-81a5-1aa13e440b63` | `966d82e0-aa69-4bb1-af02-e0dfa7eac741` |
| Higgsfield MCP ID | `b8d0973c-ba93-41f3-b5a2-ddbb801438df` | `HIGGSFIELD` (이름 기반) |
