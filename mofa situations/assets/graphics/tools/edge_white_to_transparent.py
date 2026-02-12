#!/usr/bin/env python3
from __future__ import annotations

import argparse
from collections import deque
from pathlib import Path

from PIL import Image


def is_near_white(r: int, g: int, b: int, a: int, threshold: int) -> bool:
    if a == 0:
        return False
    return r >= threshold and g >= threshold and b >= threshold


def edge_white_to_transparent(src: Path, dst: Path, threshold: int) -> None:
    img = Image.open(src).convert("RGBA")
    w, h = img.size
    px = img.load()

    outside = [[False for _ in range(h)] for _ in range(w)]
    q: deque[tuple[int, int]] = deque()

    def push(x: int, y: int) -> None:
        if outside[x][y]:
            return
        r, g, b, a = px[x, y]
        if is_near_white(r, g, b, a, threshold):
            outside[x][y] = True
            q.append((x, y))

    for x in range(w):
        push(x, 0)
        push(x, h - 1)
    for y in range(h):
        push(0, y)
        push(w - 1, y)

    while q:
        x, y = q.popleft()
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if nx < 0 or ny < 0 or nx >= w or ny >= h:
                continue
            if outside[nx][ny]:
                continue
            r, g, b, a = px[nx, ny]
            if is_near_white(r, g, b, a, threshold):
                outside[nx][ny] = True
                q.append((nx, ny))

    for x in range(w):
        for y in range(h):
            r, g, b, _ = px[x, y]
            if outside[x][y]:
                px[x, y] = (r, g, b, 0)
            else:
                px[x, y] = (r, g, b, 255)

    dst.parent.mkdir(parents=True, exist_ok=True)
    img.save(dst, format="PNG")


def main() -> int:
    parser = argparse.ArgumentParser(description="Make edge-connected white pixels transparent in PNG files")
    parser.add_argument("--input-dir", required=True, help="Directory containing source PNG files")
    parser.add_argument("--output-dir", required=True, help="Directory for processed PNG files")
    parser.add_argument("--threshold", type=int, default=245, help="White threshold 0-255 (default 245)")
    args = parser.parse_args()

    src_dir = Path(args.input_dir)
    out_dir = Path(args.output_dir)
    files = sorted(src_dir.glob("*.png"))
    if not files:
        print(f"No PNG files found in {src_dir}")
        return 1

    for f in files:
        edge_white_to_transparent(f, out_dir / f.name, args.threshold)
        print(f"Processed: {f.name}")

    print(f"Done. Wrote {len(files)} PNG files to: {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
