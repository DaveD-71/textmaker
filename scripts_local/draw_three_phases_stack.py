#!/usr/bin/env python3
"""Draw the '3 Phases of Preparation' vertical-stack diagram entirely with PIL.

Pure geometry (equal boxes, color bars, simple icons, text) -- no image-model
call needed. If this doesn't look good enough, fall back to OpenAI generation
for the base shapes and PIL only for text (see image_register.json history).
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT_PATH = Path(__file__).resolve().parents[1] / "books" / "Presentation Skills" / "images" / "generated" / "raw" / "01-1-three-phases.png"

WIDTH, HEIGHT = 1024, 1536
MARGIN_TOP = 60
MARGIN_BOTTOM = 60
LEFT_LABEL_W = 140   # phase name column
BAR_W = 14           # color bar width
GAP_BAR_BOX = 30
RIGHT_MARGIN = 60
BOX_GAP = 22
N_BOXES = 8

BG = (250, 248, 242)
INK = (30, 46, 58)          # dark blue-gray for text/icons/arrows
BOX_FILL = (255, 255, 255)
BOX_OUTLINE = (60, 80, 96)

PHASE_COLORS = {
    "PLANNING": (58, 107, 137),   # muted blue
    "WRITING": (181, 136, 74),    # muted amber/brown
    "PRACTICE": (122, 84, 130),   # muted plum
}

STEPS = [
    ("Purpose", "target"),
    ("Message", "message"),
    ("Content", "document"),
    ("Structure", "blocks"),
    ("Visual Aids", "chart"),
    ("Drafting", "pencil"),
    ("Honing", "scissors"),
    ("Delivery", "person"),
]

PHASE_FOR_BOX = {
    1: "PLANNING", 2: "PLANNING", 3: "PLANNING", 4: "PLANNING", 5: "PLANNING",
    6: "WRITING", 7: "WRITING",
    8: "PRACTICE",
}


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\calibrib.ttf" if bold else r"C:\Windows\Fonts\calibri.ttf",
    ]
    for c in candidates:
        if Path(c).exists():
            return ImageFont.truetype(c, size)
    return ImageFont.load_default()


def draw_icon(draw: ImageDraw.ImageDraw, kind: str, cx: int, cy: int, r: int) -> None:
    lw = max(2, r // 8)
    if kind == "target":
        for radius in (r, int(r * 0.62), int(r * 0.24)):
            draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], outline=INK, width=lw)
    elif kind == "message":
        # speech bubble with a small star
        bw, bh = int(r * 2.0), int(r * 1.5)
        x0, y0 = cx - bw // 2, cy - bh // 2
        draw.rounded_rectangle([x0, y0, x0 + bw, y0 + bh], radius=int(r * 0.4), outline=INK, width=lw)
        tail = [(cx - int(r * 0.2), y0 + bh), (cx - int(r * 0.5), y0 + bh + int(r * 0.5)), (cx + int(r * 0.15), y0 + bh)]
        draw.polygon(tail, fill=BG, outline=INK)
        # simple 4-point star
        star_r = int(r * 0.35)
        sx, sy = cx, cy - int(r * 0.05)
        pts = []
        import math
        for i in range(8):
            rad = star_r if i % 2 == 0 else star_r * 0.4
            ang = math.pi / 4 * i - math.pi / 2
            pts.append((sx + rad * math.cos(ang), sy + rad * math.sin(ang)))
        draw.polygon(pts, outline=INK, width=lw)
    elif kind == "document":
        w, h = int(r * 1.3), int(r * 1.8)
        x0, y0 = cx - w // 2, cy - h // 2
        draw.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=int(r * 0.15), outline=INK, width=lw)
        for i in range(3):
            ly = y0 + h * (0.3 + i * 0.22)
            draw.line([x0 + w * 0.18, ly, x0 + w * 0.82, ly], fill=INK, width=lw)
    elif kind == "blocks":
        s = int(r * 0.85)
        positions = [(cx - s, cy - s // 2), (cx + int(s * 0.1), cy - s // 2), (cx - int(s * 0.45), cy + int(s * 0.4))]
        for (bx, by) in positions:
            draw.rounded_rectangle([bx, by, bx + s, by + s], radius=int(s * 0.15), outline=INK, width=lw)
    elif kind == "chart":
        w, h = int(r * 1.8), int(r * 1.4)
        x0, y0 = cx - w // 2, cy - h // 2
        draw.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=int(r * 0.15), outline=INK, width=lw)
        bar_w = w * 0.15
        heights = [0.3, 0.55, 0.8]
        for i, hh in enumerate(heights):
            bx0 = x0 + w * (0.2 + i * 0.25)
            by1 = y0 + h * 0.85
            by0 = by1 - h * 0.6 * hh
            draw.rectangle([bx0, by0, bx0 + bar_w, by1], outline=INK, width=lw)
    elif kind == "pencil":
        length = int(r * 2.0)
        x0, y0 = cx - int(length * 0.35), cy + int(length * 0.35)
        x1, y1 = cx + int(length * 0.35), cy - int(length * 0.35)
        draw.line([x0, y0, x1, y1], fill=INK, width=lw * 2)
        draw.polygon([(x1, y1), (x1 - lw * 2, y1 + lw * 4), (x1 + lw * 2, y1 + lw * 2)], fill=INK)
    elif kind == "scissors":
        draw.line([cx - r * 0.7, cy - r * 0.6, cx + r * 0.6, cy + r * 0.7], fill=INK, width=lw)
        draw.line([cx - r * 0.7, cy + r * 0.6, cx + r * 0.6, cy - r * 0.7], fill=INK, width=lw)
        for ex, ey in [(cx - r * 0.7, cy - r * 0.6), (cx - r * 0.7, cy + r * 0.6)]:
            draw.ellipse([ex - r * 0.28, ey - r * 0.28, ex + r * 0.28, ey + r * 0.28], outline=INK, width=lw)
    elif kind == "person":
        head_r = int(r * 0.42)
        draw.ellipse([cx - head_r, cy - r, cx + head_r, cy - r + head_r * 2], outline=INK, width=lw)
        body_w = int(r * 1.3)
        body_top = cy - r + head_r * 2 + int(r * 0.15)
        draw.rounded_rectangle(
            [cx - body_w // 2, body_top, cx + body_w // 2, cy + r * 0.8],
            radius=int(r * 0.2), outline=INK, width=lw,
        )


def main() -> None:
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)

    usable_h = HEIGHT - MARGIN_TOP - MARGIN_BOTTOM
    box_h = (usable_h - BOX_GAP * (N_BOXES - 1)) // N_BOXES
    box_x0 = LEFT_LABEL_W + BAR_W + GAP_BAR_BOX
    box_x1 = WIDTH - RIGHT_MARGIN

    font_label = load_font(34, bold=True)
    font_phase = load_font(24, bold=True)

    box_positions = []
    y = MARGIN_TOP
    for i in range(N_BOXES):
        box_positions.append((y, y + box_h))
        y += box_h + BOX_GAP

    # color bar segments (one per phase run)
    phase_runs = []
    current_phase = None
    run_start = None
    for idx in range(1, N_BOXES + 1):
        phase = PHASE_FOR_BOX[idx]
        if phase != current_phase:
            if current_phase is not None:
                phase_runs.append((current_phase, run_start, idx - 1))
            current_phase = phase
            run_start = idx
    phase_runs.append((current_phase, run_start, N_BOXES))

    for phase, start_box, end_box in phase_runs:
        y0 = box_positions[start_box - 1][0]
        y1 = box_positions[end_box - 1][1]
        color = PHASE_COLORS[phase]
        draw.rounded_rectangle([LEFT_LABEL_W, y0, LEFT_LABEL_W + BAR_W, y1], radius=BAR_W // 2, fill=color)

        # vertical phase label, centered on the run
        label_img = Image.new("RGBA", (400, 60), (0, 0, 0, 0))
        label_draw = ImageDraw.Draw(label_img)
        label_draw.text((0, 0), phase, font=font_phase, fill=color + (255,))
        rotated = label_img.rotate(90, expand=True)
        bbox = rotated.getbbox()
        if bbox:
            rotated = rotated.crop(bbox)
        rx = LEFT_LABEL_W - rotated.width - 14
        ry = (y0 + y1) // 2 - rotated.height // 2
        img.paste(rotated, (max(4, rx), ry), rotated)

    icon_r = int(box_h * 0.30)
    for idx, (label, icon_kind) in enumerate(STEPS, start=1):
        y0, y1 = box_positions[idx - 1]
        draw.rounded_rectangle([box_x0, y0, box_x1, y1], radius=18, fill=BOX_FILL, outline=BOX_OUTLINE, width=3)

        icon_cx = box_x0 + int((box_x1 - box_x0) * 0.16)
        icon_cy = (y0 + y1) // 2
        draw_icon(draw, icon_kind, icon_cx, icon_cy, icon_r)

        text_x = box_x0 + int((box_x1 - box_x0) * 0.30)
        text_bbox = draw.textbbox((0, 0), label, font=font_label)
        text_h = text_bbox[3] - text_bbox[1]
        text_y = (y0 + y1) // 2 - text_h // 2 - text_bbox[1]
        draw.text((text_x, text_y), label, font=font_label, fill=INK)

        if idx < N_BOXES:
            arrow_cx = (box_x0 + box_x1) // 2
            arrow_y0 = y1 + 4
            arrow_y1 = y1 + BOX_GAP - 4
            draw.line([arrow_cx, arrow_y0, arrow_cx, arrow_y1], fill=BOX_OUTLINE, width=3)
            draw.polygon(
                [
                    (arrow_cx - 7, arrow_y1 - 8),
                    (arrow_cx + 7, arrow_y1 - 8),
                    (arrow_cx, arrow_y1 + 2),
                ],
                fill=BOX_OUTLINE,
            )

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT_PATH, format="PNG")
    print(f"Saved: {OUT_PATH}")


if __name__ == "__main__":
    main()
