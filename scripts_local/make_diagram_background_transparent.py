#!/usr/bin/env python3
"""Convert a flat-background diagram PNG to a transparent-background PNG.

For diagram/flowchart-type images (Logic Tree, flowcharts, etc.) whose
background is one near-uniform color. Uses a flood-fill from the four image
edges so background-colored regions enclosed by artwork (e.g. inside a loop)
are NOT accidentally punched through -- only the background actually
connected to the outer edge becomes transparent.
"""
from __future__ import annotations

import argparse
from collections import deque
from pathlib import Path

from PIL import Image


def make_transparent(input_path: Path, output_path: Path, threshold: int = 18) -> None:
    img = Image.open(input_path).convert("RGBA")
    w, h = img.size
    pixels = img.load()

    bg_r, bg_g, bg_b, _ = pixels[0, 0]  # sample the background color from a corner

    def close_to_bg(r: int, g: int, b: int) -> bool:
        return abs(r - bg_r) <= threshold and abs(g - bg_g) <= threshold and abs(b - bg_b) <= threshold

    visited = [[False] * h for _ in range(w)]
    queue: deque[tuple[int, int]] = deque()

    def try_enqueue(x: int, y: int) -> None:
        if visited[x][y]:
            return
        r, g, b, a = pixels[x, y]
        if close_to_bg(r, g, b):
            visited[x][y] = True
            queue.append((x, y))

    for x in range(w):
        try_enqueue(x, 0)
        try_enqueue(x, h - 1)
    for y in range(h):
        try_enqueue(0, y)
        try_enqueue(w - 1, y)

    while queue:
        x, y = queue.popleft()
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if 0 <= nx < w and 0 <= ny < h and not visited[nx][ny]:
                r, g, b, a = pixels[nx, ny]
                if close_to_bg(r, g, b):
                    visited[nx][ny] = True
                    queue.append((nx, ny))

    for x in range(w):
        for y in range(h):
            if visited[x][y]:
                r, g, b, a = pixels[x, y]
                pixels[x, y] = (r, g, b, 0)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path, format="PNG")
    print(f"Saved (transparent bg): {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Make a diagram's flat background transparent")
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--threshold", type=int, default=18, help="Color-distance tolerance for background match")
    args = parser.parse_args()
    make_transparent(args.input, args.output, args.threshold)


if __name__ == "__main__":
    main()
