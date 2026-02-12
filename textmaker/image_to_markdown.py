"""
Image → Markdown converter with OCR.

- Runs Tesseract OCR on a single image.
- Writes OCR text to a markdown file.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .ocr_utils import run_tesseract


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True, help='Input image file')
    parser.add_argument(
        '--output',
        help='Output markdown file (default: <input stem>.md in current directory)',
    )
    parser.add_argument(
        '--ocr-lang',
        default='eng+jpn',
        help='Tesseract language(s) (default: eng+jpn)',
    )
    args = parser.parse_args()


    input_path = Path(args.input)
    if not input_path.exists():
        print(f'Error: input image not found: {input_path}')
        sys.exit(1)

    output_path = Path(args.output) if args.output else Path(f'{input_path.stem}.md')
    output_path.parent.mkdir(parents=True, exist_ok=True)

    ocr_text = run_tesseract(input_path, args.ocr_lang)
    output_path.write_text(ocr_text.strip() + '\n', encoding='utf-8')
    print('Wrote', output_path)


if __name__ == '__main__':
    main()
