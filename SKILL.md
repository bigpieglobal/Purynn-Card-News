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

STEP 2 — CONTENT + DAILY FOCUS
**4-card** outline (card 1 cover keyword-first → 2 middle cards → card 4 CTA ending "Save this · @purynn_official"), Instagram caption (3–4 short paragraphs, friendly, ends with a question), 12–16 hashtags mixing brand (#PURYNN #CERAPANO #SkinBarrier #BarrierCare #CleanBeauty) + topic + reach (#KBeauty #KoreanSkincare).

IMAGE↔CONTENT MATCHING (required) — every card's image must match what its text says. In particular, when a card is about an INGREDIENT or benefit, show the PURYNN product that delivers it, as a 연출컷 (STEP 3c). Ingredient → product map:
- humectant / hydration / peptide / water-binding → **CERAPANO™ Peptide Hydration Toner** (`toner`)
- occlusive / lipids / ceramide / barrier-seal / nourish → **CERAPANO™ Tri-Lipid Nourish Essence** (`essence`)
- retinol / firming / anti-aging / renewal → **CERAPANO™ Retinol Firming Ampoule** (`ampoule`)
- glutathione / brightening / tone / mela / dark spots → **CERAPANO™ Glutathione Mela Cream** (`cream`)
- whole CERAPANO™ system / ceramide + panthenol / pairing → toner + essence together (or all four on the CTA).
For non-ingredient cards, match literally too (a "damp skin / layering" card → model applying; a "barrier SOS" card → close-up skin/texture, etc.). Put the matched product name in that card's body so text and image agree.

DAILY FOCUS ROTATION — every day is a **4-card** carousel, but the cover + lead cards follow the weekday focus (`date +%u`: 1=Mon … 7=Sun):
- **Mon / Thu → PERSON**: cover is a beauty-model portrait; 1–2 more model/lifestyle cards, the rest ingredient/product.
- **Tue / Fri → INGREDIENT**: cover + lead cards are ingredient/texture macros (serum droplet, cream swatch, water/dew); one product card.
- **Wed / Sat → PRODUCT**: cover + lead cards are product-focused (real cutouts on the clean powder-blue set with reflections); one model or texture card for variety.
- **Sun → EDITORIAL**: a quieter recap — mostly `editorial_card` solid powder-blue text cards summarising the week's theme, plus one product/model card.
Always keep the 4-card carousel visually mixed (never 4 identical layouts); the focus just sets the cover + majority.

STEP 3 — IMAGE SOURCES (Higgsfield generate_image, model `nano_banana_2`, `aspect_ratio "3:4"`, `resolution "2k"`, ~2 credits each)
VISUAL SYSTEM — "dusty-blue editorial" (matches the approved reference grid): muted dusty/powder-blue + mist-white, cool grey-blue studio light, matte and minimalist, generous negative space in the upper-half + left for text. Every generation prompt ends with "muted dusty-blue and cool grey-blue palette, soft diffused studio light, minimalist editorial, the subject sits in the lower/right, the upper half and left side are empty soft powder-blue negative space, highly realistic, no text, no letters, no logos, no watermark".
Check `balance` first; if under 30 credits skip generation and use `editorial_card` (solid powder-blue) + `product_card` (real cutouts on MIST) only.
Up to ~5 generations per run (person + ingredient days need fresh scenes). Poll `job_display` until completed; keep the `rawUrl` values.
  (a) PERSON — text-to-image beauty portrait: "editorial beauty portrait of an East Asian female model, soft matte natural skin, minimal makeup, calm expression, positioned toward the right/lower area, left + top empty for text" + the system tail.
  (b) INGREDIENT / TEXTURE — text-to-image macro: e.g. "a single glass dropper releasing one translucent serum droplet" / "a smooth glossy white cream swatch smeared on a pale blue-grey surface" / "water beads on a glossy surface" + the system tail.
  (c) PRODUCT 연출컷 (staged scenes) — the natural, label-safe recipe (this is what the client approved):
    1. In the sandbox, flatten the REAL cutout onto a clean WHITE background (soft contact shadow), 1080x1440. ⚠️ Do NOT pass the transparent cutout straight into img2img — the alpha edge produces a torn blue-splatter glitch. The white-bg flatten prevents that. For a pair, put both bottles on one white image.
    2. `media_upload` that white-bg image (png) → PUT → `media_confirm` (image) to get a reference media_id.
    3. `generate_image` img2img with `medias:[{value:<ref media_id>,role:"image"}]`, prompt: "place the exact bottle(s) from the reference photo naturally on a smooth pale stone ledge / draped undyed linen, muted dusty-blue palette, soft diffused softbox light with a gentle natural shadow and subtle reflection, lower-right, empty upper-left, keep the bottle shape/frosted texture/cap and every printed label character identical to the reference — do not redraw, re-letter or blur any text or logo. clean seamless, no torn edges, no blue splatter, no paint, no digital artifacts, no extra text".
    4. Render text over the result with `photo_card`. Do NOT run the teal snap-back on these scenes (it would tint the dusty-blue set). QA the label; regenerate if it drifted.
  Fallbacks: quick composite via `staged_product_card` (real cutout on an AI empty set — looks slightly more "placed"); low-credit (<30) `product_card`/`product_row_card` (cutouts on flat MIST).
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

Renderer — use the EDITORIAL toolkit `PURYNN_피드_이미지/_assets/purynn_editorial.py` (Pillow + numpy, Liberation fonts). Fetch it (raw from GitHub or the mounted workspace) and write it into the Higgsfield sandbox, then compose the 4 cards with its functions. Style contract:
- Canvas 1080x1440, margin 96. Palette INK(38,48,62) SUB(112,126,142) STEEL(96,120,146) POWDER(150,174,196) MIST(233,239,245) LINE(160,180,200) WHITE.
- Typography: SERIF headline (LiberationSerif) ~82px; tracked small-caps kicker (LiberationSans-Bold 26, tracking 6) + hairline rule; SANS body 33 in SUB; a small letter-spaced `PURYNN` serif wordmark bottom-left; "n / 4" bottom-right. No teal logo PNG on cards — the wordmark is typographic.
- Card builders (each returns a 1080x1440 image; text TOP-LEFT, hero lower/right):
  * `photo_card(bg_path, kicker, title, body, idx, anchor="right", top_a, left_a, mw)` — PERSON / INGREDIENT cards over a veiled photo.
  * `product_card(kicker, title, body, idx, cutouts, bg=MIST)` — PRODUCT card; cutouts = list of (path, cx, bottom, height); real cutouts get a soft mirrored reflection.
  * `product_row_card(kicker, title, body, idx, paths)` — CTA row of all four products (even-gap packer + reflections).
  * `editorial_card(kicker, title, body, idx, bg=POWDER)` — solid dusty-blue text card (Sun recap / brand statement; light text).
- Keep title ≤ 2 short lines and body ≤ 1–2 lines; leave the lower/right clear for the hero. Products are the real cutouts (`toner/essence/ampoule/cream.png` fetched from the CDN), never AI-drawn.
- Compose the day per STEP 2's focus (person / ingredient / product / editorial), keeping the carousel visually mixed.
The older teal toolkit `purynn_cards.py` stays in the repo for reference, but `purynn_editorial.py` is the current system.

STEP 5 — SAVE LOCAL MASTERS
If a workspace folder is mounted (`ls -d /sessions/*/mnt/*/PURYNN_피드_이미지`), also render PNG masters locally with the same toolkit into `<that folder>/<topic-slug>/` as 01_cover.png … 04_cta.png (4 cards). If not mounted, skip.
NOTE the local `_assets/products/manifest.json` records that the ORIGINAL cutout files in `누끼컷/누끼/` have Toner.png and Essesnce.png SWAPPED. The copies under `_assets/products/` are the corrected ones — always use those.

STEP 6 — NOTION
`notion-create-pages` under data_source_id 513993cb-23b6-4abc-900e-6f7f80d5827f. Properties: "Trend / Topic" (title), "date:Date:start"=today (`date +%F`), Status="Ready", Format="Carousel", Slides=4, "Hero Product"=exact product name(s) featured, Caption (<br><br> between paragraphs), Hashtags, Sources="Brand content · PURYNN CERAPANO™".
Page body: `## Slides` outline, `## Caption`, `## Hashtags`, `## CTA`, then `## Cards` with the four images as markdown blocks `![01 cover](https://d2ol7oe51mr4n9.cloudfront.net/user_2zrIhlq0Y8juUmY7o3n04KjTZBJ/<media_id>.jpg)`, then a short `## Image production` note stating which product each ingredient card shows (image↔content match).

STEP 7 — QA
Read the rendered cards (local masters, or fetch the CDN JPEGs). Confirm: text fully legible, no product overlapping type, nothing clipped at the frame edge, PURYNN wordmark legible, product labels still read correctly, muted dusty-blue palette consistent across all 4 cards, cover matches today's focus, and EACH card's image matches its text (ingredient cards show the mapped product). Fix and re-render if not — remembering that a fix requires a NEW media_id (see STEP 4). Then re-fetch the Notion page and confirm the four image blocks are present.

STEP 8 — REPORT
Topic title, Notion page URL, local folder path (if mounted), Higgsfield credits used. 2–4 lines.
