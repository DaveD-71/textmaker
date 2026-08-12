#!/usr/bin/env python3
"""Overlay worked-example text (trunk/branches/fruit) onto the shared blank Logic
Tree illustration (05-1-logic-tree-blank.png), reusing the same base art for every
worked example instead of regenerating the tree via the API each time. Avoids the
image model's unreliable in-image text placement entirely, same approach validated
for the labeled core Logic Tree (draw_logic_tree_labels.py).
"""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parents[1] / "books" / "Presentation Skills" / "images" / "generated"
SRC_PATH = BASE_DIR / "raw" / "05-1-logic-tree-blank.png"

INK = (30, 46, 58)
LINE_W = 3

# Anchor points read directly off the shared 1024x1536 blank tree image.
TRUNK_POINT = (490, 850)
BRANCH_POINTS = [(330, 460), (640, 470), (500, 380)]  # left, right, upper-center
FRUIT_POINT = (748, 400)


def load_font(size: int, bold: bool = True) -> ImageFont.FreeTypeFont:
    candidates = [r"C:\Windows\Fonts\arialbd.ttf"] if bold else [r"C:\Windows\Fonts\arial.ttf"]
    candidates.append(r"C:\Windows\Fonts\calibrib.ttf")
    for c in candidates:
        if Path(c).exists():
            return ImageFont.truetype(c, size)
    return ImageFont.load_default()


def draw_callout(draw, side_margin, img_w, tx, ty, side, text, font, used_y):
    label_y = ty
    for used in used_y[side]:
        if abs(label_y - used) < 60:
            label_y = used + 65
    used_y[side].append(label_y)

    if side == "right":
        line_end_x = img_w - side_margin + 40
        text_x = line_end_x + 14
    else:
        line_end_x = side_margin - 40
        text_x = None

    draw.line([tx, ty, line_end_x, label_y], fill=INK, width=LINE_W)
    draw.ellipse([tx - 5, ty - 5, tx + 5, ty + 5], fill=INK)

    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    if side == "left":
        text_x = line_end_x - 14 - text_w
    draw.text((text_x, label_y - text_h // 2 - bbox[1]), text, font=font, fill=INK)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--trunk", required=True)
    ap.add_argument("--branches", required=True, nargs=3)
    ap.add_argument("--fruit", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    src = Image.open(SRC_PATH).convert("RGBA")
    src_w, src_h = src.size

    trunk_font = load_font(30)
    branch_font = load_font(26)
    fruit_font = load_font(30)

    # Measure the widest label per side so the margin is never too narrow to fit it.
    measure_img = Image.new("RGBA", (10, 10))
    measure_draw = ImageDraw.Draw(measure_img)

    def text_width(text, font):
        bbox = measure_draw.textbbox((0, 0), text, font=font)
        return bbox[2] - bbox[0]

    right_texts = [(args.trunk, trunk_font), (args.branches[1], branch_font), (args.fruit, fruit_font)]
    left_texts = [(args.branches[0], branch_font), (args.branches[2], branch_font)]
    max_right = max(text_width(t, f) for t, f in right_texts)
    max_left = max(text_width(t, f) for t, f in left_texts)
    side_margin = max(max_right, max_left) + 120  # padding for callout line + gap

    new_w = src_w + side_margin * 2
    img = Image.new("RGBA", (new_w, src_h), (255, 255, 255, 0))
    img.paste(src, (side_margin, 0), src)
    draw = ImageDraw.Draw(img)

    used_y: dict[str, list[int]] = {"left": [], "right": []}

    tx, ty = TRUNK_POINT
    draw_callout(draw, side_margin, new_w, tx + side_margin, ty, "right", args.trunk, trunk_font, used_y)

    sides = ["left", "right", "left"]
    for (bx, by), text, side in zip(BRANCH_POINTS, args.branches, sides):
        draw_callout(draw, side_margin, new_w, bx + side_margin, by, side, text, branch_font, used_y)

    fx, fy = FRUIT_POINT
    draw_callout(draw, side_margin, new_w, fx + side_margin, fy, "right", args.fruit, fruit_font, used_y)

    out_path = BASE_DIR / "raw" / args.out
    img.save(out_path, format="PNG")
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
