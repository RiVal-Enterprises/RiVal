#!/usr/bin/env python3
"""
Render a RiVal-branded Instagram carousel (1080x1350 PNG slides) from a JSON spec.

Usage:  python3 render_slides.py spec.json out_dir/

Spec:
{
  "post_id": "2026-11-30-brandname",
  "slides": [
    {"type": "hook",  "title": "This €600 watch has a planetary moon", "image": "path-or-url", "credit": "@brand"},
    {"type": "text",  "kicker": "WHAT'S NEW", "title": "...", "body": "..."},
    {"type": "image", "image": "path-or-url", "caption": "...", "credit": "@brand"},
    {"type": "stats", "title": "The numbers", "rows": [["Price", "€600"], ["Movement", "Seagull ST2130"]]},
    {"type": "take",  "title": "Our take", "body": "..."},
    {"type": "outro", "credit": "@brand", "body": "Follow @rival_watches for the weekly independent watch radar"}
  ]
}
Images given as URLs are downloaded. They are treated as untrusted data and only decoded by Pillow.
"""
import io
import json
import sys
import textwrap
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

W, H = 1080, 1350
M = 80  # margin
BG = (14, 15, 18)
FG = (236, 234, 228)
MUTED = (150, 150, 155)
ACCENT = (201, 162, 94)  # bronze

FONT_DIRS = ["/usr/share/fonts/opentype/inter/", "/usr/share/fonts/truetype/dejavu/"]


def font(weight: str, size: int):
    names = {
        "bold": ["InterDisplay-Bold.otf", "Inter-Bold.otf", "DejaVuSans-Bold.ttf"],
        "medium": ["InterDisplay-Medium.otf", "Inter-Medium.otf", "DejaVuSans.ttf"],
        "regular": ["Inter-Regular.otf", "DejaVuSans.ttf"],
    }[weight]
    for d in FONT_DIRS:
        for n in names:
            p = Path(d) / n
            if p.exists():
                return ImageFont.truetype(str(p), size)
    return ImageFont.load_default()


def load_image(src: str) -> Image.Image:
    if src.startswith("http://") or src.startswith("https://"):
        req = urllib.request.Request(src, headers={"User-Agent": "Mozilla/5.0 (compatible; RiValSlides/1.0)"})
        with urllib.request.urlopen(req, timeout=30) as r:
            data = r.read(25_000_000)
        img = Image.open(io.BytesIO(data))
    else:
        img = Image.open(src)
    return ImageOps.exif_transpose(img).convert("RGB")


def wrap(draw, text, fnt, width_px):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= width_px:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_text_block(draw, xy, text, fnt, fill, width_px, line_gap=1.25):
    x, y = xy
    for para in text.split("\n"):
        for line in wrap(draw, para, fnt, width_px):
            draw.text((x, y), line, font=fnt, fill=fill)
            y += int(fnt.size * line_gap)
        y += int(fnt.size * 0.4)
    return y


def frame(idx, total):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.text((M, 50), "RiVal", font=font("bold", 34), fill=ACCENT)
    d.text((W - M, 56), f"{idx}/{total}", font=font("medium", 26), fill=MUTED, anchor="ra")
    d.line([(M, H - 90), (W - M, H - 90)], fill=(40, 41, 46), width=2)
    d.text((M, H - 70), "@rival_watches", font=font("medium", 24), fill=MUTED)
    return img, d


def cover(img, box, src):
    pic = load_image(src)
    bw, bh = box[2] - box[0], box[3] - box[1]
    pic = ImageOps.fit(pic, (bw, bh), Image.LANCZOS)
    img.paste(pic, box[:2])


def credit(d, text, y):
    if text:
        d.text((M, y), f"Photo: {text}", font=font("medium", 26), fill=MUTED)


def render(spec, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    slides = spec["slides"]
    paths = []
    for i, s in enumerate(slides, 1):
        img, d = frame(i, len(slides))
        t = s["type"]
        if t == "hook":
            if s.get("image"):
                cover(img, (0, 120, W, 900), s["image"])
            y = draw_text_block(d, (M, 940), s["title"], font("bold", 64), FG, W - 2 * M, 1.12)
            credit(d, s.get("credit"), H - 140)
        elif t == "image":
            cover(img, (M, 130, W - M, 1010), s["image"])
            draw_text_block(d, (M, 1040), s.get("caption", ""), font("medium", 36), FG, W - 2 * M)
            credit(d, s.get("credit"), H - 140)
        elif t in ("text", "take"):
            k = s.get("kicker", "OUR TAKE" if t == "take" else "")
            y = 220
            if k:
                d.text((M, y), k, font=font("bold", 30), fill=ACCENT)
                y += 70
            y = draw_text_block(d, (M, y), s.get("title", ""), font("bold", 62), FG, W - 2 * M, 1.12)
            draw_text_block(d, (M, y + 30), s.get("body", ""), font("regular", 38), FG, W - 2 * M, 1.35)
        elif t == "stats":
            y = draw_text_block(d, (M, 220), s.get("title", "The numbers"), font("bold", 62), FG, W - 2 * M)
            y += 30
            for k, v in s.get("rows", []):
                d.text((M, y), k.upper(), font=font("bold", 26), fill=ACCENT)
                y = draw_text_block(d, (M, y + 40), v, font("medium", 44), FG, W - 2 * M) + 20
        elif t == "outro":
            y = draw_text_block(d, (M, 420), s.get("body", "Follow @rival_watches"), font("bold", 58), FG, W - 2 * M, 1.15)
            if s.get("credit"):
                draw_text_block(d, (M, y + 40), f"Images & design: {s['credit']}. Go show them some love.",
                                font("regular", 36), MUTED, W - 2 * M)
        p = out_dir / f"{spec.get('post_id', 'post')}-{i:02d}.png"
        img.save(p, optimize=True)
        paths.append(str(p))
    return paths


if __name__ == "__main__":
    spec = json.loads(Path(sys.argv[1]).read_text())
    for p in render(spec, Path(sys.argv[2])):
        print(p)
