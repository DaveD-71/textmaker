"""Split a combined front+back cover spread PDF (e.g. A3 landscape) into two
single-page PDFs (e.g. A4 portrait) at the horizontal midline.

Used to derive "AS Online" front-cover and back-cover assets from the
print-ready combined cover PDF exported from each book's cover DOCX.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pymupdf


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Split a combined front+back cover spread PDF into two single-page PDFs."
    )
    parser.add_argument("input_pdf", help="Path to the combined spread PDF (single page).")
    parser.add_argument("front_out", help="Output path for the front-cover (right) half.")
    parser.add_argument("back_out", help="Output path for the back-cover (left) half.")
    parser.add_argument(
        "--page",
        type=int,
        default=0,
        help="Page index (0-based) of the spread within input_pdf. Default: 0.",
    )
    return parser.parse_args()


def split_spread(input_pdf: Path, page_index: int, front_out: Path, back_out: Path) -> None:
    src = pymupdf.open(str(input_pdf))
    page = src[page_index]
    rect = page.rect
    half_width = rect.width / 2

    back_rect = pymupdf.Rect(rect.x0, rect.y0, rect.x0 + half_width, rect.y1)
    front_rect = pymupdf.Rect(rect.x0 + half_width, rect.y0, rect.x1, rect.y1)

    _write_half(src, page_index, back_rect, back_out)
    _write_half(src, page_index, front_rect, front_out)

    src.close()


def _write_half(src: "pymupdf.Document", page_index: int, clip_rect: "pymupdf.Rect", out_path: Path) -> None:
    doc = pymupdf.open()
    new_page = doc.new_page(width=clip_rect.width, height=clip_rect.height)
    new_page.show_pdf_page(new_page.rect, src, page_index, clip=clip_rect)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(out_path))
    doc.close()


def main() -> None:
    args = parse_args()
    input_pdf = Path(args.input_pdf)
    front_out = Path(args.front_out)
    back_out = Path(args.back_out)

    if not input_pdf.exists():
        print(f"\nERROR: File not found:\n{input_pdf}\n")
        raise SystemExit(1)

    split_spread(input_pdf, args.page, front_out, back_out)

    print(f"Front cover -> {front_out}")
    print(f"Back cover  -> {back_out}")


if __name__ == "__main__":
    main()
