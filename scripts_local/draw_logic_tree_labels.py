#!/usr/bin/env python3
"""Overlay the 5 Logic Tree labels + callout lines onto the OpenAI-generated
unlabeled tree illustration, using exact pixel coordinates read off the actual
generated image (1024x1536) -- avoids the image model's unreliable text/callout
placement entirely.
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parents[1] / "books" / "Presentation Skills" / "images" / "generated"
SRC_PATH = BASE_DIR / "raw" / "05-1-logic-tree-blank.png"
OUT_PATH = BASE_DIR / "raw" / "05-1-logic-tree-labeled.png"

INK = (30, 46, 58)
BG = (250, 248, 242)
LINE_W = 3
SIDE_MARGIN = 260  # extra canvas width added to each side for label text

# Each entry: label text, the point ON the original tree image the callout should
# touch (x, y in the ORIGINAL 1024-wide image's coordinate space), and which side
# the label sits on. Coordinates read directly off the 1024x1536 generated image.
CALLOUTS = [
    {"text": "FRUIT", "tree_point": (748, 400), "side": "right"},
    {"text": "BRANCHES", "tree_point": (640, 470), "side": "right"},
    {"text": "LEAVES", "tree_point": (330, 460), "side": "left"},
    {"text": "TRUNK", "tree_point": (490, 850), "side": "right"},
    {"text": "ROOTS", "tree_point": (350, 1150), "side": "left"},
]


def load_font(size: int) -> ImageFont.FreeTypeFont:
    for c in (r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\calibrib.ttf"):
        if Path(c).exists():
            return ImageFont.truetype(c, size)
    return ImageFont.load_default()


def main() -> None:
    src = Image.open(SRC_PATH).convert("RGBA")
    src_w, src_h = src.size

    # Expand canvas: add SIDE_MARGIN of transparent space on both left and right
    # (keep the whole thing RGBA/transparent end-to-end -- no opaque BG fill)
    new_w = src_w + SIDE_MARGIN * 2
    img = Image.new("RGBA", (new_w, src_h), (255, 255, 255, 0))
    img.paste(src, (SIDE_MARGIN, 0), src)
    draw = ImageDraw.Draw(img)
    font = load_font(34)

    # Track vertical positions already used per side to avoid label overlap
    used_y_by_side: dict[str, list[int]] = {"left": [], "right": []}

    for c in CALLOUTS:
        tx, ty = c["tree_point"]
        tx += SIDE_MARGIN  # shift into the expanded canvas's coordinate space
        side = c["side"]

        label_y = ty
        # nudge vertically if too close to an already-placed label on the same side
        for used in used_y_by_side[side]:
            if abs(label_y - used) < 50:
                label_y = used + 55
        used_y_by_side[side].append(label_y)

        if side == "right":
            line_end_x = new_w - SIDE_MARGIN + 40
            text_x = line_end_x + 14
        else:
            line_end_x = SIDE_MARGIN - 40
            text_x = None  # computed after measuring text width

        draw.line([tx, ty, line_end_x, label_y], fill=INK, width=LINE_W)
        draw.ellipse([tx - 5, ty - 5, tx + 5, ty + 5], fill=INK)

        text = c["text"]
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        if side == "left":
            text_x = line_end_x - 14 - text_w
        draw.text((text_x, label_y - text_h // 2 - bbox[1]), text, font=font, fill=INK)

    img.save(OUT_PATH, format="PNG")
    print(f"Saved: {OUT_PATH}")


if __name__ == "__main__":
    main()
