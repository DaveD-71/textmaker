#!/usr/bin/env python3
"""Build the final '3 Phases of Preparation' diagram: slice the 8-icon grid
sheet (generated once by OpenAI for consistent, well-designed icon art), then
composite icons + boxes + arrows + color bars + text labels entirely in PIL,
where counting/spacing/grouping is guaranteed correct.
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parents[1] / "books" / "Presentation Skills" / "images" / "generated"
SHEET_PATH = BASE_DIR / "raw" / "01-1-icon-sheet.png"
OUT_PATH = BASE_DIR / "raw" / "01-1-three-phases.png"

GRID_COLS, GRID_ROWS = 2, 4
# Reading order in the sheet: col-major (col0 top-to-bottom, then col1 top-to-bottom)
# Sheet order: (1)Purpose (2)Message (3)Content (4)Structure (5)VisualAids (6)Drafting (7)Honing (8)Delivery
# Grid layout (2 cols x 4 rows), left column top-to-bottom then right column top-to-bottom:
SHEET_CELL_ORDER = [
    (0, 0), (0, 1), (0, 2), (0, 3),  # left column, rows 0-3 -> Purpose, Content, VisualAids, Honing... wait, need to match actual gen order
]

# Actual generation order requested was: reading order left-column-top-to-bottom
# then right-column-top-to-bottom: (1) target (2) message (3) doc (4) blocks (5) chart
# (6) pencil (7) scissors (8) person -- but the RENDERED sheet turned out to be a
# standard row-major 2x4 grid (row0: target, message | row1: doc, blocks |
# row2: chart, pencil | row3: scissors, person) based on visual inspection.
SHEET_POSITIONS_ROW_MAJOR = [
    (0, 0), (1, 0),  # row 0: target(col0), message(col1)
    (0, 1), (1, 1),  # row 1: document(col0), blocks(col1)
    (0, 2), (1, 2),  # row 2: chart(col0), pencil(col1)
    (0, 3), (1, 3),  # row 3: scissors(col0), person(col1)
]

STEPS = [
    ("Purpose", "PLANNING"),
    ("Message", "PLANNING"),
    ("Content", "PLANNING"),
    ("Structure", "PLANNING"),
    ("Visual Aids", "PLANNING"),
    ("Drafting", "WRITING"),
    ("Honing", "WRITING"),
    ("Delivery", "PRACTICE"),
]

PHASE_COLORS = {
    "PLANNING": (75, 115, 145),
    "WRITING": (198, 148, 74),
    "PRACTICE": (128, 88, 130),
}

INK = (35, 50, 62)
BOX_OUTLINE = (170, 178, 184)

WIDTH, HEIGHT = 1024, 1536
MARGIN_TOP = 40
MARGIN_BOTTOM = 40
LEFT_LABEL_W = 130
BAR_W = 14
GAP_BAR_BOX = 26
RIGHT_MARGIN = 50
BOX_GAP = 20
N_BOXES = 8


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    for c in ((r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf"),):
        if Path(c).exists():
            return ImageFont.truetype(c, size)
    return ImageFont.load_default()


ALPHA_CROP_THRESHOLD = 40  # ignore faint stray/anti-aliased pixels below this alpha when computing crop bounds


def slice_icons(sheet: Image.Image) -> list[Image.Image]:
    sw, sh = sheet.size
    cell_w, cell_h = sw // GRID_COLS, sh // GRID_ROWS
    icons = []
    for col, row in SHEET_POSITIONS_ROW_MAJOR:
        # shrink the cell slightly inward first to exclude cross-cell bleed/artifacts
        # near cell edges (e.g. a stray dot or line fragment from a neighboring icon)
        inset_x, inset_y = int(cell_w * 0.06), int(cell_h * 0.06)
        box = (
            col * cell_w + inset_x,
            row * cell_h + inset_y,
            (col + 1) * cell_w - inset_x,
            (row + 1) * cell_h - inset_y,
        )
        cell = sheet.crop(box)
        # tight-crop to actual icon content, ignoring faint/stray low-alpha pixels
        alpha = cell.getchannel("A")
        mask = alpha.point(lambda a: 255 if a >= ALPHA_CROP_THRESHOLD else 0)
        bbox = mask.getbbox()
        if bbox:
            cell = cell.crop(bbox)
        icons.append(cell)
    return icons


def main() -> None:
    sheet = Image.open(SHEET_PATH).convert("RGBA")
    icons = slice_icons(sheet)
    assert len(icons) == 8, f"Expected 8 sliced icons, got {len(icons)}"

    img = Image.new("RGBA", (WIDTH, HEIGHT), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    usable_h = HEIGHT - MARGIN_TOP - MARGIN_BOTTOM
    box_h = (usable_h - BOX_GAP * (N_BOXES - 1)) // N_BOXES
    box_x0 = LEFT_LABEL_W + BAR_W + GAP_BAR_BOX
    box_x1 = WIDTH - RIGHT_MARGIN

    font_label = load_font(32, bold=True)
    font_phase = load_font(22, bold=True)

    box_positions = []
    y = MARGIN_TOP
    for _ in range(N_BOXES):
        box_positions.append((y, y + box_h))
        y += box_h + BOX_GAP

    # Determine contiguous phase runs for the color bar
    phase_runs = []
    current_phase = None
    run_start = None
    for idx, (_, phase) in enumerate(STEPS, start=1):
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

        label_img = Image.new("RGBA", (400, 50), (0, 0, 0, 0))
        label_draw = ImageDraw.Draw(label_img)
        label_draw.text((0, 0), phase, font=font_phase, fill=color + (255,))
        rotated = label_img.rotate(90, expand=True)
        bbox = rotated.getbbox()
        if bbox:
            rotated = rotated.crop(bbox)
        rx = LEFT_LABEL_W - rotated.width - 12
        ry = (y0 + y1) // 2 - rotated.height // 2
        img.paste(rotated, (max(2, rx), ry), rotated)

    icon_target_h = int(box_h * 0.62)
    for idx, ((label, _phase), icon) in enumerate(zip(STEPS, icons), start=1):
        y0, y1 = box_positions[idx - 1]
        draw.rounded_rectangle([box_x0, y0, box_x1, y1], radius=16, outline=BOX_OUTLINE, width=2)

        iw, ih = icon.size
        scale = icon_target_h / ih
        new_size = (max(1, int(iw * scale)), max(1, int(ih * scale)))
        icon_resized = icon.resize(new_size, Image.LANCZOS)

        icon_cx = box_x0 + int((box_x1 - box_x0) * 0.15)
        icon_cy = (y0 + y1) // 2
        paste_x = icon_cx - icon_resized.width // 2
        paste_y = icon_cy - icon_resized.height // 2
        img.paste(icon_resized, (paste_x, paste_y), icon_resized)

        text_x = box_x0 + int((box_x1 - box_x0) * 0.30)
        bbox = draw.textbbox((0, 0), label, font=font_label)
        text_h = bbox[3] - bbox[1]
        text_y = (y0 + y1) // 2 - text_h // 2 - bbox[1]
        draw.text((text_x, text_y), label, font=font_label, fill=INK)

        if idx < N_BOXES:
            arrow_cx = (box_x0 + box_x1) // 2
            ay0, ay1 = y1 + 3, y1 + BOX_GAP - 3
            draw.line([arrow_cx, ay0, arrow_cx, ay1], fill=BOX_OUTLINE, width=3)
            draw.polygon(
                [(arrow_cx - 6, ay1 - 7), (arrow_cx + 6, ay1 - 7), (arrow_cx, ay1 + 2)],
                fill=BOX_OUTLINE,
            )

    img.save(OUT_PATH, format="PNG")
    print(f"Saved: {OUT_PATH}")


if __name__ == "__main__":
    main()
