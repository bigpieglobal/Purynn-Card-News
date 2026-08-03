# PURYNN render toolkit (`_assets`)

- `purynn_cards.py` — Pillow/numpy rendering toolkit (see SKILL.md STEP 4).
- `products/manifest.json` — product names, sizes, and permanent Higgsfield `media_id`s.

## Binary assets live on the CDN, not in git

The logo and 4 product cutouts are **permanent Higgsfield assets** served from:

```
https://d2ol7oe51mr4n9.cloudfront.net/user_2zrIhlq0Y8juUmY7o3n04KjTZBJ/<media_id>.png
```

media_ids are in `products/manifest.json`. The daily automation always fetches them
from the CDN inside the Higgsfield sandbox — it never re-uploads them.

If you keep a local copy of the original workspace folder (`PURYNN_피드_이미지`) on a
company drive for STEP 5 local masters, drop the real `purynn_logo.png` and
`products/{toner,essence,ampoule,cream}.png` here. **Remember the swap note in
manifest.json:** in the original `누끼컷/누끼/` folder, `Toner.png` and `Essesnce.png`
are reversed — the corrected versions are the ones on the CDN / in `products/`.
