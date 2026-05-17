from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from PIL import Image


# Pixels darker than this in any channel are considered content (not background).
WHITE_THRESHOLD = 245

# Minimum width of a column band to count as a real tag (filters 1-px stray bands).
MIN_COLUMN_WIDTH = 20

# Horizontal padding added on each side of a detected tag column.
H_PADDING = 4

# Vertical padding added above and below the row band.
V_PADDING = 4

CATEGORIES = [
    "learn",
    "language",
    "structure",
    "notice",
    "write",
    "rewrite",
    "revise",
    "edit",
    "example",
]

# Rows in order from top to bottom.
ROW_PREFIXES = [
    "tag_outline",
    "tag_filled",
    "icon_outline",
    "icon_filled",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Split an icon asset sheet into individual white-background PNGs."
    )
    parser.add_argument("input_png", help="Path to the source PNG file.")
    return parser.parse_args()


def find_content_bands(mask_1d: np.ndarray, min_width: int = 1) -> list[tuple[int, int]]:
    """Return (start, end) index pairs for runs of True values in mask_1d."""
    bands: list[tuple[int, int]] = []
    in_band = False
    start = 0
    for i, val in enumerate(mask_1d):
        if val and not in_band:
            start = i
            in_band = True
        elif not val and in_band:
            if i - start >= min_width:
                bands.append((start, i))
            in_band = False
    if in_band and len(mask_1d) - start >= min_width:
        bands.append((start, len(mask_1d)))
    return bands


def row_has_content(rgb: np.ndarray) -> np.ndarray:
    """Boolean array of length h — True where any pixel in that row is non-white."""
    return np.any(
        (rgb[:, :, 0] < WHITE_THRESHOLD)
        | (rgb[:, :, 1] < WHITE_THRESHOLD)
        | (rgb[:, :, 2] < WHITE_THRESHOLD),
        axis=1,
    )


def col_has_content_in_slice(rgb_slice: np.ndarray) -> np.ndarray:
    """Boolean array of length w — True where any pixel in that column slice is non-white."""
    return np.any(
        (rgb_slice[:, :, 0] < WHITE_THRESHOLD)
        | (rgb_slice[:, :, 1] < WHITE_THRESHOLD)
        | (rgb_slice[:, :, 2] < WHITE_THRESHOLD),
        axis=0,
    )


def composite_on_white(img_rgba: Image.Image) -> Image.Image:
    """Flatten an RGBA image onto a white background, returning RGB."""
    bg = Image.new("RGB", img_rgba.size, (255, 255, 255))
    bg.paste(img_rgba, mask=img_rgba.split()[3])
    return bg


def main() -> None:
    args = parse_args()
    input_file = Path(args.input_png)

    if not input_file.exists():
        print(f"\nERROR: File not found:\n{input_file}\n")
        raise SystemExit(1)

    output_dir = input_file.parent / f"{input_file.stem}_assets"
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\nLoading: {input_file}")
    img = Image.open(input_file).convert("RGBA")
    arr = np.array(img)
    rgb = arr[:, :, :3]
    img_h, img_w = rgb.shape[:2]

    # --- Detect horizontal row bands ---
    row_mask = row_has_content(rgb)
    # Merge bands that are very close together (≤ 5 px gap) to handle thin dividers.
    raw_row_bands = find_content_bands(row_mask, min_width=10)
    row_bands: list[tuple[int, int]] = []
    for band in raw_row_bands:
        if row_bands and band[0] - row_bands[-1][1] <= 5:
            row_bands[-1] = (row_bands[-1][0], band[1])
        else:
            row_bands.append(band)

    print(f"Detected {len(row_bands)} content row(s):")
    for i, (y0, y1) in enumerate(row_bands):
        print(f"  Row {i}: y={y0}–{y1}  h={y1 - y0}")

    if len(row_bands) != len(ROW_PREFIXES):
        print(
            f"WARNING: Expected {len(ROW_PREFIXES)} rows, found {len(row_bands)}. "
            "Check source image or adjust thresholds."
        )

    # --- For each row, detect column bands and crop each tag ---
    saved = 0
    for row_index, (y0, y1) in enumerate(row_bands):
        if row_index >= len(ROW_PREFIXES):
            break
        prefix = ROW_PREFIXES[row_index]

        # Use the full row height (same y for every tag in this row) + padding.
        crop_y0 = max(0, y0 - V_PADDING)
        crop_y1 = min(img_h, y1 + V_PADDING)

        row_slice = rgb[y0:y1, :, :]
        col_mask = col_has_content_in_slice(row_slice)
        col_bands = find_content_bands(col_mask, min_width=MIN_COLUMN_WIDTH)

        print(f"\n{prefix} — {len(col_bands)} item(s) detected in row {row_index}:")

        for item_index, (x0, x1) in enumerate(col_bands):
            if item_index >= len(CATEGORIES):
                name = f"extra_{item_index + 1}"
            else:
                name = CATEGORIES[item_index]

            filename = f"{prefix}_{name}.png"

            # Apply horizontal padding, clamp to image bounds.
            crop_x0 = max(0, x0 - H_PADDING)
            crop_x1 = min(img_w, x1 + H_PADDING)

            # Crop from the original RGBA image (full quality, no re-encoding artefacts).
            cropped_rgba = img.crop((crop_x0, crop_y0, crop_x1, crop_y1))

            # Composite onto white — no transparency, no edge erosion.
            cropped_rgb = composite_on_white(cropped_rgba)

            output_path = output_dir / filename
            cropped_rgb.save(output_path, format="PNG")

            w = crop_x1 - crop_x0
            h = crop_y1 - crop_y0
            print(f"  {filename}  ({w}×{h})")
            saved += 1

    print(f"\nDone — {saved} file(s) written.")
    print(f"Output folder:\n{output_dir.resolve()}\n")


if __name__ == "__main__":
    main()
