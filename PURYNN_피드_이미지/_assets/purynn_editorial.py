"""
PURYNN editorial cardnews toolkit (v3 — "dusty-blue editorial" system).

Reference look: muted dusty/powder-blue + mist white, serif headlines,
tracked small-caps labels, hairline rules, a small letter-spaced PURYNN
wordmark at the bottom. Card types rotate by day: person / ingredient /
product / editorial. Pillow + numpy only; Liberation fonts.

Canvas 1080x1440. Text lives TOP-LEFT; the hero (model / texture / product)
sits lower/right. Products are ALWAYS the real cutouts (never AI-drawn).

Quick use:
    import purynn_editorial as E
    im = E.photo_card("model.png", "Barrier science", "Humectant\\n& Occlusive",
                      "Two jobs. One healthy barrier.", 1, anchor="right")
    im.save("01.jpg", "JPEG", quality=90)

    im = E.product_card("03 · The pairing", "Layer in\\norder",
                        "Humectant first, occlusive on top.", 4,
                        [("essence.png", 600, 1120, 500), ("toner.png", 850, 1120, 500)])

    im = E.editorial_card("CERAPANO™", "Barrier care,\\nsimplified.",
                          "Save this · @purynn_official", 5)
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1440
M = 96

# palette (muted dusty blue / editorial)
INK    = (38, 48, 62)     # serif headline
SUB    = (112, 126, 142)  # secondary text
STEEL  = (96, 120, 146)   # kicker / wordmark
POWDER = (150, 174, 196)  # solid editorial card bg
MIST   = (233, 239, 245)  # light product-set bg
LINE   = (160, 180, 200)  # hairline rule
WHITE  = (255, 255, 255)

_LIB = "/usr/share/fonts/truetype/liberation/"
SERIF = _LIB + "LiberationSerif-Regular.ttf"
SANS  = _LIB + "LiberationSans-Regular.ttf"
SANS_B = _LIB + "LiberationSans-Bold.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def trk(d, xy, text, font, fill, tracking):
    """Letter-spaced (tracked) text. Returns end x."""
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill)
        x += d.textlength(ch, font=font) + tracking
    return x


def wrap(d, text, font, max_w):
    out = []
    for para in text.split("\n"):
        words = para.split()
        if not words:
            out.append("")
            continue
        cur = words[0]
        for w in words[1:]:
            if d.textlength(cur + " " + w, font=font) <= max_w:
                cur += " " + w
            else:
                out.append(cur)
                cur = w
        out.append(cur)
    return out


def veil(im, top_a=0.55, left_a=0.5):
    """Lift the top-left with a white gradient so dark text stays legible."""
    a = np.zeros((H, W, 4), np.float32)
    a[:, :, 0:3] = 255
    yy = np.linspace(0, 1, H)[:, None]
    xx = np.linspace(0, 1, W)[None, :]
    a[:, :, 3] = np.clip((1 - yy) * top_a + (1 - xx) * left_a, 0, 1) * 255
    return Image.alpha_composite(im.convert("RGBA"),
                                 Image.fromarray(a.astype("uint8"), "RGBA")).convert("RGB")


def cover(path, anchor="right"):
    """Cover-crop a photo to the canvas. anchor keeps that side of the source."""
    s = Image.open(path).convert("RGB")
    sw, sh = s.size
    k = max(W / sw, H / sh)
    s = s.resize((round(sw * k), round(sh * k)), Image.LANCZOS)
    sw, sh = s.size
    x = sw - W if anchor == "right" else (0 if anchor == "left" else (sw - W) // 2)
    y = (sh - H) // 2
    return s.crop((x, y, x + W, y + H))


def _trim(im):
    im = im.convert("RGBA")
    b = im.split()[-1].getbbox()
    return im.crop(b) if b else im


def _scaleh(im, h):
    w0, h0 = im.size
    return im.resize((max(1, round(w0 * h / h0)), h), Image.LANCZOS)


def restore_brand_teal(im):
    """Snap dulled PURYNN teal back to (73,180,209). Run on every img2img
    product 연출컷 scene — the model shifts the teal toward grey."""
    a = np.asarray(im.convert("RGB")).astype(int)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    a[(b - r > 35) & (b > 70) & (g > r)] = [73, 180, 209]
    return Image.fromarray(a.astype("uint8"), "RGB")


def wordmark(d):
    trk(d, (M, H - 96), "PURYNN", F(SERIF, 32), STEEL, 9)


def _text_block(im, kicker, title, body, idx, mw=560, ink=INK, sub=SUB, kick=STEEL):
    d = ImageDraw.Draw(im)
    trk(d, (M, 296), kicker.upper(), F(SANS_B, 26), kick, 6)
    d.line([(M, 342), (M + 210, 342)], fill=LINE, width=2)
    tf = F(SERIF, 82)
    y = 392
    for ln in wrap(d, title, tf, mw):
        d.text((M, y), ln, font=tf, fill=ink)
        y += 90
    if body:
        bf = F(SANS, 33)
        y += 14
        for ln in wrap(d, body, bf, mw):
            d.text((M, y), ln, font=bf, fill=sub)
            y += 46
    nf = F(SANS, 24)
    n = f"{idx} / 5"
    d.text((W - M - d.textlength(n, font=nf), H - 92), n, font=nf, fill=sub)
    wordmark(d)
    return im


def _reflect(base_rgba, cut, cx, bottom, strength=0.36):
    cut = cut.convert("RGBA")
    x = round(cx - cut.width / 2)
    top = bottom - cut.height
    base_rgba.alpha_composite(cut, (x, top))
    fl = cut.transpose(Image.FLIP_TOP_BOTTOM)
    a = np.array(fl.split()[-1]).astype(np.float32)
    g = np.clip(np.linspace(strength, 0, fl.height), 0, 1)[:, None]
    fl.putalpha(Image.fromarray((a * g).astype("uint8"), "L"))
    base_rgba.alpha_composite(fl, (x, bottom))


# ------------------------------------------------------------------ card types
def photo_card(bg_path, kicker, title, body, idx, anchor="right",
               top_a=0.55, left_a=0.5, mw=560):
    """Person or ingredient card: full-bleed photo veiled for top-left text."""
    im = veil(cover(bg_path, anchor), top_a, left_a)
    return _text_block(im, kicker, title, body, idx, mw)


def product_card(kicker, title, body, idx, cutouts, bg=MIST, mw=560):
    """Product card: real cutouts with soft reflections on a light set.
    cutouts = list of (path, cx, bottom, height)."""
    im = Image.new("RGB", (W, H), bg).convert("RGBA")
    for path, cx, bottom, height in cutouts:
        _reflect(im, _scaleh(_trim(Image.open(path)), height), cx, bottom)
    im = im.convert("RGB")
    return _text_block(im, kicker, title, body, idx, mw)


def product_row_card(kicker, title, body, idx, paths, bg=MIST,
                     x0=150, x1=980, bottom=1070, height=300):
    """CTA-style row of products with an even-gap packer + reflections."""
    im = Image.new("RGB", (W, H), bg).convert("RGBA")
    cuts = [_scaleh(_trim(Image.open(p)), height) for p in paths]
    widths = [c.width for c in cuts]
    gap = (x1 - x0 - sum(widths)) / (len(cuts) - 1) if len(cuts) > 1 else 0
    x = x0
    for c in cuts:
        _reflect(im, c, x + c.width / 2, bottom, strength=0.3)
        x += c.width + gap
    im = im.convert("RGB")
    return _text_block(im, kicker, title, body, idx, mw=720)


def _contact_shadow(base_rgba, cx, by, w, alpha=0.30):
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(L).ellipse([cx - w / 2, by - 28, cx + w / 2, by + 28],
                              fill=(24, 32, 46, int(255 * alpha)))
    base_rgba.alpha_composite(L.filter(ImageFilter.GaussianBlur(26)))


def _place_on_set(base_rgba, cut, cx, bottom, refl=0.15):
    cut = cut.convert("RGBA")
    x = round(cx - cut.width / 2)
    _contact_shadow(base_rgba, cx, bottom - 6, cut.width * 1.15)
    if refl > 0:
        fl = cut.transpose(Image.FLIP_TOP_BOTTOM)
        a = np.array(fl.split()[-1]).astype(np.float32)
        g = np.clip(np.linspace(refl, 0, fl.height), 0, 1)[:, None]
        fl.putalpha(Image.fromarray((a * g).astype("uint8"), "L"))
        base_rgba.alpha_composite(fl, (x, bottom))
    base_rgba.alpha_composite(cut, (x, bottom - cut.height))


def staged_product_card(bg_path, cutouts, kicker, title, body, idx,
                        top_a=0.45, left_a=0.5, refl=0.15, mw=560):
    """PRODUCT 연출컷 (staged): real cutouts composited onto an AI-generated
    EMPTY styled set (stone ledge / linen) with contact shadow + reflection.
    Label-safe (no img2img on the bottle) and glitch-free.
    cutouts = list of (path, cx, bottom, height)."""
    im = veil(cover(bg_path, "center"), top_a, left_a).convert("RGBA")
    for path, cx, bottom, height in cutouts:
        _place_on_set(im, _scaleh(_trim(Image.open(path)), height), cx, bottom, refl)
    return _text_block(im.convert("RGB"), kicker, title, body, idx, mw)


def editorial_card(kicker, title, body, idx, bg=POWDER):
    """Solid dusty-blue text card (recap / brand statement). Light text."""
    im = Image.new("RGB", (W, H), bg)
    return _text_block(im, kicker, title, body, idx, mw=760,
                       ink=WHITE, sub=(232, 238, 244), kick=(226, 234, 241))
