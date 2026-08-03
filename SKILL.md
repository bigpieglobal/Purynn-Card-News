---
name: purynn-daily-cardnews
description: Daily PURYNN CERAPANO cardnews → images rendered in Higgsfield sandbox, uploaded as JPEG, embedded in Notion log
---

<!--
회사 계정(연구개발팀 / bigpie_up@jungdari.com) 이관 완료 2026-08-03.
플레이스홀더 9개는 아래 실제 값으로 모두 채워졌습니다. 참고용 대응표는 MIGRATION.md 부록 참조.
원본 대비 수정: 로고 비율 규칙(STEP 4 렌더러), CDN 캐시 불변성 경고(STEP 4)
-->

Create today's PURYNN Instagram cardnews, render the images in the Higgsfield cloud sandbox, and log everything (including the images) to Notion. Work fully autonomously; do not ask questions.

BRAND
- PURYNN (퓨리인): clean, minimal, sustainable K-beauty. Signature ingredient system CERAPANO™ (ceramide + panthenol). Eco: FSC paper, soy-ink. Instagram: @purynn_official. ALL content in ENGLISH.
- Tone: clean / minimal. Plenty of whitespace, short lines.
- PRODUCT LINE (exact names — use verbatim in copy):
  * CERAPANO™ Peptide Hydration Toner — 100 ml / 3.38 fl. oz.   (key `toner`)
  * CERAPANO™ Tri-Lipid Nourish Essence — 100 ml / 3.38 fl. oz. (key `essence`)
  * CERAPANO™ Retinol Firming Ampoule — 50 ml / 1.69 fl. oz.    (key `ampoule`)
  * CERAPANO™ Glutathione Mela Cream — 50 ml / 1.69 fl. oz.     (key `cream`)

PERMANENT HIGGSFIELD ASSETS (never re-upload; CDN base `C=https://d2ol7oe51mr4n9.cloudfront.net/user_2zrIhlq0Y8juUmY7o3n04KjTZBJ`)
  logo    335fd260-0463-4ea9-8e01-5ce97f8c214d      (transparent teal wordmark)
  toner   bd0b4760-35fb-48d4-8693-8c506974f0fd
  essence 0a1e7932-be79-4b95-a9aa-8446ec9c3e23
  ampoule 4b91cb95-a81b-4251-9733-5dcfc143f1d7
  cream   e224b5db-0ff6-4279-92d2-84b86af9c719
Fetch each as `$C/<media_id>.png`.
NOTE the stored logo is a PADDED image (the upload widget adds margin and distorts aspect). Do NOT scale the raw file to a fixed box. Always: trim by alpha bbox first, then resize the trimmed wordmark to 226x119 and paste at (117, 91). A flat resize to (240,132) squashes it to a 2.38 aspect; the true wordmark is ~1.90.

STEP 1 — TOPIC (no repeats)
Query data source collection://513993cb-23b6-4abc-900e-6f7f80d5827f ("PURYNN Content Log") for existing "Trend / Topic" values. Pick ONE unused topic from: ceramides 101, panthenol soothing, skin barrier basics, dehydrated vs dry skin, morning vs night routine, layering order, summer hydration, double cleansing myth, fragrance & sensitive skin, glass skin via barrier, slugging explained, Tri-Lipid explained, glutathione & tone, niacinamide benefits, squalane, transepidermal water loss, over-exfoliation signs, minimal routine for beginners, travel skincare, clean beauty & sustainability, FSC packaging, how to read an ingredient list, ampoule vs serum, when to use a sleeping mask, peptides explained, retinol for beginners, retinol + barrier pairing, humectant vs occlusive, pH and the acid mantle, seasonal routine switch, ceramide vs peptide, why alcohol-free matters, barrier care after sun, skincare for maskne, cleansing water vs oil, the case for fewer actives, sensitive skin patch testing, what "non-comedogenic" really means, moisturiser layering in humidity, night-shift skin recovery. If all are used, invent a fresh on-brand barrier-care angle.

STEP 2 — CONTENT
5-card outline (card 1 cover keyword-first → middle cards → CTA card ending "Save this · @purynn_official"), Instagram caption (3–4 short paragraphs, friendly, ends with a question), 12–16 hashtags mixing brand (#PURYNN #CERAPANO #SkinBarrier #BarrierCare #CleanBeauty) + topic + reach (#KBeauty #KoreanSkincare). Decide which product (if any) belongs on each card.

STEP 3 — IMAGE SOURCES (Higgsfield generate_image, model `nano_banana_2`, `aspect_ratio "3:4"`, `resolution "2k"`, ~2 credits each)
Check `balance` first; if under 30 credits skip all generation and use plain brand-gradient backgrounds with direct cutouts.
Max 2 generations per run. Poll `job_display` until completed; keep the `rawUrl` values.
  (a) PRODUCT SCENE (cover / hero cards) — img2img from the real cutout. Pass `medias:[{value:"<product media_id>",role:"image"}]`. Prompt = scene description + "the bottle sits in the LOWER RIGHT third with generous empty space across the upper half and left side" + "CRITICAL: preserve the bottle's exact silhouette, proportions, frosted glass texture, cap and every printed label character exactly as in the reference image — do not redraw, re-letter, translate, restyle or blur any text or logo" + "no extra text anywhere in the frame". Verified scenes: wet stone with still-water reflection; undyed linen with recycled paper.
  (b) TEXTURE / MOOD (cards with NO product) — text-to-image, subject in the LOWER RIGHT, upper half and left empty, "no text, no letters, no logos, no labels".
NEVER ask a model to draw PURYNN packaging from text alone — it fabricates fake bottles and cartons.

STEP 4 — RENDER + UPLOAD, ALL INSIDE ONE `sandbox_exec` CALL
The LOCAL sandbox cannot reach upload.higgsfield.ai — do every image step in the Higgsfield cloud sandbox (`mcp__HIGGSFIELD__sandbox_exec`).
★ The sandbox is discarded ~10 seconds after a call returns. Download → render → PUT MUST be chained with && inside a SINGLE command. Files never survive to the next call.
★ The command field caps at 16000 chars. If the renderer plus URLs won't fit, split into two rounds, each rendering only the cards it uploads.
★ Call `media_upload` (files[], content_type image/jpeg) BEFORE the sandbox call to reserve media_ids. You do NOT need the long presigned query string — a plain `curl -X PUT -H "Content-Type: image/jpeg" --data-binary @card.jpg "https://upload.higgsfield.ai/user_2zrIhlq0Y8juUmY7o3n04KjTZBJ/<media_id>.jpg"` succeeds and keeps the command small.
★ Save JPEG quality 90 (~100–160 KB). Notion fails to render external images near 2 MB, so never upload the PNGs.
★ Verify each upload: `curl -sSI <cdn url> | grep content-length` must equal the local file size.
★ CDN OBJECTS ARE IMMUTABLE. Whatever lands on a media_id first is cached by CloudFront permanently. Re-PUTting a corrected file to the same media_id returns HTTP 200 but the CDN keeps serving the OLD image, and a cache-busting query string does NOT help. If a card needs fixing after upload, reserve a BRAND NEW media_id via `media_upload`, upload there, and update the Notion links. A content-length that matches the PREVIOUS render instead of the current one is the signature of this trap.
★ Then call `media_confirm` (type image, batch of media_ids).

Renderer (Pillow + numpy, fonts present at /usr/share/fonts/truetype/liberation{,2}/LiberationSans-{Regular,Bold}.ttf):
- Canvas 1080x1440, margin 110. Palette NAVY(20,52,82) TEAL(0,170,200) TEAL_D(0,128,150) SOFT(232,246,249) WHITE GREY(140,154,168) BODY(92,106,122).
- Every card: logo top-left — alpha-bbox-trimmed wordmark resized to 226x119, pasted at (117,84+7)=(117,91), whitened on the dark CTA card; bold TEAL_D label at y=400 + TEAL underline; bold NAVY headline 76px wrapped; regular BODY 38px supporting line; "n / 5" bottom-left.
- `photo_bg(path,tone,zoom,top_a,left_a,band_a,anchor)`: cover-crop the photo then veil it with a brand-tone gradient. anchor="right" keeps the right side (a centred subject drifts LEFT); anchor="left" keeps the left side (subject drifts RIGHT, clearing the text column).
- `scene_panel(path,tone,height,ox,oy,feather,top_a,top_end)`: place the scene at exact coordinates on a tone canvas with a feathered seam. Use when zoom/anchor cannot clear the text column without cropping a product out of frame.
- `restore_brand_teal(im)`: numpy mask `(b-r>35)&(b>70)&(g>r)` → set to (73,180,209). MANDATORY on every AI product scene — the model dulls PURYNN teal toward (80,140,150).
- Direct cutouts: trim by alpha bbox, scale to height, paste bottom-right (cx 700–950, bottom 1300–1330). CTA card shows all four products in a row — lay them out with an even-gap packer (x0≈205, x1≈1010) rather than hand-picked centres, or the wide cream jar will overlap the ampoule.
- Layout rule: text TOP-LEFT, product BOTTOM-RIGHT. Nothing may sit under the headline or body copy. Keep body copy to ONE short line on cards that carry a product, or the bottle will collide with the last text line.
A working reference implementation lives in the repo at `PURYNN_피드_이미지/_assets/purynn_cards.py` — read/download it (raw from GitHub, or from the workspace folder if mounted). If neither is reachable, reproduce the functions above.

STEP 5 — SAVE LOCAL MASTERS
If a workspace folder is mounted (`ls -d /sessions/*/mnt/*/PURYNN_피드_이미지`), also render PNG masters locally with the same toolkit into `<that folder>/<topic-slug>/` as 01_cover.png … 05_cta.png. If not mounted, skip.
NOTE the local `_assets/products/manifest.json` records that the ORIGINAL cutout files in `누끼컷/누끼/` have Toner.png and Essesnce.png SWAPPED. The copies under `_assets/products/` are the corrected ones — always use those.

STEP 6 — NOTION
`notion-create-pages` under data_source_id 513993cb-23b6-4abc-900e-6f7f80d5827f. Properties: "Trend / Topic" (title), "date:Date:start"=today (`date +%F`), Status="Ready", Format="Carousel"/"Single", Slides=5, "Hero Product"=exact product name(s), Caption (<br><br> between paragraphs), Hashtags, Sources="Brand content · PURYNN CERAPANO™".
Page body: `## Slides` outline, `## Caption`, `## Hashtags`, `## CTA`, then `## Cards` with the five images as markdown blocks `![01 cover](https://d2ol7oe51mr4n9.cloudfront.net/user_2zrIhlq0Y8juUmY7o3n04KjTZBJ/<media_id>.jpg)`, then a short `## Image production` note naming which cards were AI scenes vs direct cutouts.

STEP 7 — QA
Read the rendered cards (local masters, or fetch the CDN JPEGs). Confirm: text fully legible, no product overlapping type, nothing clipped at the frame edge, logo not squashed, product labels still read correctly on AI scenes, brand teal correct. Fix and re-render if not — remembering that a fix requires a NEW media_id (see STEP 4). Then re-fetch the Notion page and confirm the five image blocks are present.

STEP 8 — REPORT
Topic title, Notion page URL, local folder path (if mounted), Higgsfield credits used. 2–4 lines.
