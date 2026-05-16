from __future__ import annotations

import argparse
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image


WHITE_THRESHOLD = 245
MIN_COMPONENT_AREA = 500
PADDING = 2
EXPECTED_COMPONENT_COUNT = 36
EXPECTED_ROW_ITEMS = 9

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

ROW_PREFIXES = [
    "tag_outline",
    "tag_filled",
    "icon_outline",
    "icon_filled",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Split an icon asset sheet into individual transparent PNGs."
        )
    )
    parser.add_argument(
        "input_png",
        help="Path to the source PNG file.",
    )
    return parser.parse_args()


def is_background_white(rgb: np.ndarray) -> np.ndarray:
    return (
        (rgb[:, :, 0] >= WHITE_THRESHOLD)
        & (rgb[:, :, 1] >= WHITE_THRESHOLD)
        & (rgb[:, :, 2] >= WHITE_THRESHOLD)
    )


def flood_fill_outer_background(white_mask: np.ndarray) -> np.ndarray:
    h, w = white_mask.shape
    visited = np.zeros((h, w), dtype=bool)
    q = deque()

    def add(y, x):
        if 0 <= y < h and 0 <= x < w and white_mask[y, x] and not visited[y, x]:
            visited[y, x] = True
            q.append((y, x))

    for x in range(w):
        add(0, x)
        add(h - 1, x)

    for y in range(h):
        add(y, 0)
        add(y, w - 1)

    while q:
        y, x = q.popleft()

        add(y - 1, x)
        add(y + 1, x)
        add(y, x - 1)
        add(y, x + 1)

    return visited


def find_components(alpha: np.ndarray) -> list[dict]:
    h, w = alpha.shape
    foreground = alpha > 0

    visited = np.zeros((h, w), dtype=bool)
    components: list[dict] = []

    for y in range(h):
        for x in range(w):

            if not foreground[y, x] or visited[y, x]:
                continue

            q = deque([(y, x)])
            visited[y, x] = True

            min_x = max_x = x
            min_y = max_y = y
            area = 0

            while q:
                cy, cx = q.popleft()
                area += 1

                min_x = min(min_x, cx)
                max_x = max(max_x, cx)
                min_y = min(min_y, cy)
                max_y = max(max_y, cy)

                for ny, nx in (
                    (cy - 1, cx),
                    (cy + 1, cx),
                    (cy, cx - 1),
                    (cy, cx + 1),
                ):
                    if (
                        0 <= ny < h
                        and 0 <= nx < w
                        and foreground[ny, nx]
                        and not visited[ny, nx]
                    ):
                        visited[ny, nx] = True
                        q.append((ny, nx))

            if area >= MIN_COMPONENT_AREA:
                components.append(
                    {
                        "bbox": (min_x, min_y, max_x + 1, max_y + 1),
                        "area": area,
                        "cx": (min_x + max_x) / 2,
                        "cy": (min_y + max_y) / 2,
                    }
                )

    return components


def group_rows(components: list[dict], expected_rows: int = 4) -> list[list[dict]]:

    components = sorted(components, key=lambda c: c["cy"])

    rows: list[list[dict]] = [[] for _ in range(expected_rows)]

    split_size = len(components) // expected_rows

    for i in range(expected_rows):

        start = i * split_size

        end = (
            (i + 1) * split_size
            if i < expected_rows - 1
            else len(components)
        )

        rows[i] = components[start:end]

    return [sorted(row, key=lambda c: c["cx"]) for row in rows]


def padded_bbox(
    bbox: tuple[int, int, int, int],
    width: int,
    height: int,
    padding: int,
) -> tuple[int, int, int, int]:

    left, top, right, bottom = bbox

    return (
        max(0, left - padding),
        max(0, top - padding),
        min(width, right + padding),
        min(height, bottom + padding),
    )


def main():

    args = parse_args()
    input_file = Path(args.input_png)

    if not input_file.exists():
        print(f"\nERROR: File not found:\n{input_file}\n")
        raise SystemExit(1)

    output_dir = (
        input_file.parent
        / f"{input_file.stem}_assets"
    )

    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\nLoading: {input_file}")

    img = Image.open(input_file).convert("RGBA")

    arr = np.array(img)

    rgb = arr[:, :, :3]
    alpha = arr[:, :, 3]

    white_mask = is_background_white(rgb)

    outer_background = flood_fill_outer_background(white_mask)

    alpha[outer_background] = 0

    arr[:, :, 3] = alpha

    transparent_img = Image.fromarray(arr, "RGBA")

    transparent_img.save(output_dir / "full_transparent.png")

    print("Created transparent master image")

    components = find_components(alpha)

    print(f"Detected {len(components)} components")

    if len(components) != EXPECTED_COMPONENT_COUNT:
        print(
            f"WARNING: Expected {EXPECTED_COMPONENT_COUNT} components. "
            "Check thresholds or source image."
        )

    rows = group_rows(components, expected_rows=4)

    for row_index, row in enumerate(rows):

        prefix = ROW_PREFIXES[row_index]

        if len(row) != EXPECTED_ROW_ITEMS:
            print(
                f"WARNING: Row {row_index + 1} "
                f"contains {len(row)} items"
            )

        for item_index, component in enumerate(row):

            if item_index >= len(CATEGORIES):
                filename = (
                    f"{prefix}_extra_{item_index + 1}.png"
                )
            else:
                filename = (
                    f"{prefix}_{CATEGORIES[item_index]}.png"
                )

            crop_box = padded_bbox(
                component["bbox"],
                transparent_img.width,
                transparent_img.height,
                PADDING,
            )

            cropped = transparent_img.crop(crop_box)

            output_path = output_dir / filename

            cropped.save(output_path)

            print(f"Saved: {filename}")

    print("\nDone.")
    print(f"Output folder:\n{output_dir.resolve()}\n")


if __name__ == "__main__":
    main()
