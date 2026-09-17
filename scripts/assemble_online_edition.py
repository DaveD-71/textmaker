"""Assemble an "AS Online" edition PDF: front cover, blank page, body,
blank page, back cover — all normalized to the body's page size.

Usage:
    python assemble_online_edition.py <front_cover.pdf> <body.pdf> <back_cover.pdf> <out.pdf>
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pymupdf


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Assemble front cover + blank + body + blank + back cover into one PDF."
    )
    parser.add_argument("front_cover", help="Path to the front-cover PDF (single page).")
    parser.add_argument("body", help="Path to the main body PDF (student edition, etc).")
    parser.add_argument("back_cover", help="Path to the back-cover PDF (single page).")
    parser.add_argument("out_pdf", help="Output path for the assembled PDF.")
    return parser.parse_args()


def _insert_scaled_page(doc: "pymupdf.Document", src_page: "pymupdf.Page", size: "pymupdf.Rect") -> None:
    new_page = doc.new_page(width=size.width, height=size.height)
    new_page.show_pdf_page(new_page.rect, src_page.parent, src_page.number)


def assemble(front_cover: Path, body: Path, back_cover: Path, out_pdf: Path) -> None:
    body_doc = pymupdf.open(str(body))
    body_size = body_doc[0].rect

    front_doc = pymupdf.open(str(front_cover))
    back_doc = pymupdf.open(str(back_cover))

    out = pymupdf.open()

    _insert_scaled_page(out, front_doc[0], body_size)
    out.new_page(width=body_size.width, height=body_size.height)  # blank
    out.insert_pdf(body_doc)
    out.new_page(width=body_size.width, height=body_size.height)  # blank
    _insert_scaled_page(out, back_doc[0], body_size)

    out_pdf.parent.mkdir(parents=True, exist_ok=True)
    out.save(str(out_pdf))

    out.close()
    front_doc.close()
    back_doc.close()
    body_doc.close()


def main() -> None:
    args = parse_args()
    front_cover = Path(args.front_cover)
    body = Path(args.body)
    back_cover = Path(args.back_cover)
    out_pdf = Path(args.out_pdf)

    for f in (front_cover, body, back_cover):
        if not f.exists():
            print(f"\nERROR: File not found:\n{f}\n")
            raise SystemExit(1)

    assemble(front_cover, body, back_cover, out_pdf)
    print(f"Assembled -> {out_pdf}")


if __name__ == "__main__":
    main()
