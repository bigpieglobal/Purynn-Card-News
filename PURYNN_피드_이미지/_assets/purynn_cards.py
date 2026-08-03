"""
PURYNN daily cardnews rendering toolkit.

Reference implementation of the renderer described in SKILL.md STEP 4.
Pillow + numpy only. Fonts: Liberation Sans (present in the Higgsfield sandbox).

Layout contract
---------------
- Canvas 1080x1440, margin 110.
- Logo top-left: alpha-bbox-trimmed wordmark resized to 226x119, pasted at (117, 91),
  whitened on the dark CTA card.
- Text TOP-LEFT (label @ y=400 + underline, headline, one body line),
  product BOTTOM-RIGHT. Nothing sits under the headline/body.
- restore_brand_teal() is MANDATORY on every AI product scene.

Typical use (one card):
    im = new_canvas()                       # or photo_bg(...) / scene_panel(...)
    place_logo(im, LOGO)
    draw_text_block(im, "BARRIER CARE", "Your barrier,\nsimplified", "One clean layer at a time.", 1)
    place_cutout(im, "toner.png", height=760, cx=820, bottom=1320)
    im.save("01_cover.png")
"""

import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- constants
W, H = 1080, 1440
MARGIN = 110

NAVY   = (20, 52, 82)
TEAL   = (0, 170, 200)
TEAL_D = (0, 128, 150)
SOFT   = (232, 246, 249)
WHITE  = (255, 255, 255)
GREY   = (140, 154, 168)
BODY   = (92, 106, 122)

LABEL_Y   = 400
HEADLINE_Y = 452
LOGO_XY   = (117, 91)
LOGO_SIZE = (226, 119)

_FONT_DIRS = [
    "/usr/share/fonts/truetype/liberation",
    "/usr/share/fonts/truetype/liberation2",
]


def _font_path(bold):
    name = "LiberationSans-Bold.ttf" if bold else "LiberationSans-Regular.ttf"
    for d in _FONT_DIRS:
        p = os.path.join(d, name)
        if os.path.exists(p):
            return p
    # last resort: let PIL find a default
    return None


def font(size, bold=False):
    p = _font_path(bold)
    return ImageFont.truetype(p, size) if p else ImageFont.load_default()


# ---------------------------------------------------------------- canvas
def new_canvas(bg=WHITE):
    return Image.new("RGB", (W, H), bg)


def brand_gradient_bg(tone="soft"):
    """Plain brand background used when AI scene generation is skipped.
    Soft teal wash at the top fading to white — keeps text legible top-left."""
    top = SOFT if tone == "soft" else tuple(
        int(a + (255 - a) * 0.55) for a in TEAL
    )
    arr = np.zeros((H, W, 3), np.float32)
    for c in range(3):
        col = np.linspace(top[c], 255, H, dtype=np.float32)
        arr[:, :, c] = col[:, None]
    return Image.fromarray(arr.astype("uint8"), "RGB")


# ---------------------------------------------------------------- alpha helpers
def _trim_alpha(im):
    """Crop an RGBA image to its non-transparent bounding box."""
    im = im.convert("RGBA")
    alpha = im.split()[-1]
    bbox = alpha.getbbox()
    return im.crop(bbox) if bbox else im


def _fit(im, box_w, box_h):
    """Resize preserving aspect to fit inside (box_w, box_h)."""
    w, h = im.size
    s = min(box_w / w, box_h / h)
    return im.resize((max(1, round(w * s)), max(1, round(h * s))), Image.LANCZOS)


# ---------------------------------------------------------------- logo
def load_logo(path):
    """Trim the padded stored wordmark by alpha bbox, then resize to 226x119."""
    logo = _trim_alpha(Image.open(path))
    return _fit(logo, *LOGO_SIZE)


def place_logo(im, logo, white=False):
    logo = logo.convert("RGBA")
    if white:
        arr = np.array(logo)
        opaque = arr[:, :, 3] > 0
        arr[opaque, 0:3] = 255
        logo = Image.fromarray(arr, "RGBA")
    im.paste(logo, LOGO_XY, logo)
    return im


# ---------------------------------------------------------------- text
def _wrap(draw, text, fnt, max_w):
    """Greedy word-wrap. Honors explicit \\n in the source text."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for w in words[1:]:
            trial = cur + " " + w
            if draw.textlength(trial, font=fnt) <= max_w:
                cur = trial
            else:
                lines.append(cur)
                cur = w
        lines.append(cur)
    return lines


def draw_text_block(im, label, headline, body, idx, total=5, dark=False):
    """Label (@y=400 + underline) → headline (76px bold) → one body line.
    Plus 'n / total' bottom-left."""
    d = ImageDraw.Draw(im)
    head_col = WHITE if dark else NAVY
    body_col = SOFT if dark else BODY
    label_col = TEAL if dark else TEAL_D
    max_w = W - MARGIN - 470  # leave the right third for the product

    # label
    lab_font = font(32, bold=True)
    label = label.upper()
    d.text((MARGIN, LABEL_Y), label, font=lab_font, fill=label_col)
    lab_w = d.textlength(label, font=lab_font)
    uy = LABEL_Y + 44
    d.line([(MARGIN, uy), (MARGIN + max(90, lab_w), uy)], fill=TEAL, width=4)

    # headline
    h_font = font(76, bold=True)
    y = HEADLINE_Y + 40
    for line in _wrap(d, headline, h_font, max_w):
        d.text((MARGIN, y), line, font=h_font, fill=head_col)
        y += 88

    # body (one short line on product cards)
    if body:
        b_font = font(38, bold=False)
        y += 18
        for line in _wrap(d, body, b_font, max_w):
            d.text((MARGIN, y), line, font=b_font, fill=body_col)
            y += 50

    # page number
    pn_font = font(30, bold=True)
    d.text((MARGIN, H - 96), f"{idx} / {total}", font=pn_font,
           fill=SOFT if dark else GREY)
    return im


# ---------------------------------------------------------------- photo bg
def _veil(shape_hw, color, alpha_map):
    """Return an RGBA overlay of a solid color with a per-pixel alpha map."""
    h, w = shape_hw
    ov = np.zeros((h, w, 4), np.float32)
    ov[:, :, 0], ov[:, :, 1], ov[:, :, 2] = color
    ov[:, :, 3] = alpha_map * 255
    return Image.fromarray(ov.astype("uint8"), "RGBA")


def photo_bg(path, tone=SOFT, zoom=1.0, top_a=0.55, left_a=0.45,
             band_a=0.30, anchor="right"):
    """Cover-crop a photo to the canvas, then veil it so the top-left text
    stays legible. anchor='right' keeps the right side of the source
    (a centred subject drifts LEFT); anchor='left' keeps the left side."""
    src = Image.open(path).convert("RGB")
    sw, sh = src.size
    s = max(W / sw, H / sh) * zoom
    src = src.resize((round(sw * s), round(sh * s)), Image.LANCZOS)
    sw, sh = src.size
    if anchor == "right":
        x = sw - W
    elif anchor == "left":
        x = 0
    else:
        x = (sw - W) // 2
    y = (sh - H) // 2
    im = src.crop((x, y, x + W, y + H)).convert("RGBA")

    yy = np.linspace(0, 1, H)[:, None]
    xx = np.linspace(0, 1, W)[None, :]
    top = (1 - yy) * top_a * np.ones((1, W))
    left = (1 - xx) * left_a * np.ones((H, 1))
    white_a = np.clip(top + left, 0, 1)
    im = Image.alpha_composite(im, _veil((H, W), WHITE, white_a))

    band = np.clip((yy - 0.55) / 0.45, 0, 1) * band_a * np.ones((1, W))
    im = Image.alpha_composite(im, _veil((H, W), tone, band))
    return im.convert("RGB")


def scene_panel(path, tone=SOFT, height=760, ox=520, oy=560, feather=90,
                top_a=0.0, top_end=0.0):
    """Place a scene at exact coords on a tone canvas with a feathered seam.
    Use when zoom/anchor can't clear the text column without cropping."""
    base = Image.new("RGB", (W, H), tone).convert("RGBA")
    scene = Image.open(path).convert("RGB")
    scene = _fit(scene, W - ox + 200, height).convert("RGBA")
    sw, sh = scene.size
    mask = Image.new("L", (sw, sh), 255)
    m = np.array(mask, np.float32)
    for i in range(feather):
        a = int(255 * i / feather)
        if i < sh:
            m[i, :] = np.minimum(m[i, :], a)
        if i < sw:
            m[:, i] = np.minimum(m[:, i], a)
    scene.putalpha(Image.fromarray(m.astype("uint8"), "L"))
    base.alpha_composite(scene, (ox, oy))
    im = base.convert("RGB")
    if top_a:
        yy = np.linspace(0, 1, H)[:, None]
        a = np.clip((1 - yy) - (1 - top_end), 0, 1)
        a = (a / a.max()) * top_a if a.max() else a
        im = Image.alpha_composite(im.convert("RGBA"),
                                   _veil((H, W), WHITE, a * np.ones((1, W)))).convert("RGB")
    return im


# ---------------------------------------------------------------- teal fix
def restore_brand_teal(im):
    """Model dulls PURYNN teal toward (80,140,150). Snap it back."""
    arr = np.asarray(im.convert("RGB")).astype(int)
    r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]
    mask = (b - r > 35) & (b > 70) & (g > r)
    arr[mask] = [73, 180, 209]
    return Image.fromarray(arr.astype("uint8"), "RGB")


# ---------------------------------------------------------------- cutouts
def place_cutout(im, path, height=760, cx=820, bottom=1320):
    """Trim by alpha bbox, scale to `height`, paste centred at cx / bottom."""
    cut = _trim_alpha(Image.open(path))
    w, h = cut.size
    s = height / h
    cut = cut.resize((max(1, round(w * s)), height), Image.LANCZOS)
    cw = cut.size[0]
    x = round(cx - cw / 2)
    y = bottom - height
    im.paste(cut, (x, y), cut)
    return im


def place_cutout_row(im, paths, x0=205, x1=1010, bottom=1315, height=430):
    """Lay four products in a row with an EVEN gap (not hand-picked centres),
    so the wide cream jar doesn't overlap the ampoule."""
    cuts = []
    for p in paths:
        c = _trim_alpha(Image.open(p))
        w, h = c.size
        s = height / h
        cuts.append(c.resize((max(1, round(w * s)), height), Image.LANCZOS))
    widths = [c.size[0] for c in cuts]
    span = x1 - x0
    total_w = sum(widths)
    gap = (span - total_w) / (len(cuts) - 1) if len(cuts) > 1 else 0
    x = x0
    for c, w in zip(cuts, widths):
        y = bottom - c.size[1]
        im.paste(c, (round(x), y), c)
        x += w + gap
    return im
