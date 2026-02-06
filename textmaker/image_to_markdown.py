"""
Image → Markdown converter with OCR.

- Runs Tesseract OCR on a single image.
- Writes OCR text to a markdown file.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def check_tesseract() -> None:
    if shutil.which('tesseract') is None:
        print(
            'Error: tesseract binary not found on PATH. Install from '
            'https://tesseract-ocr.github.io/tessdoc/Installation.html'
        )
        sys.exit(2)


def run_tesseract(input_image: Path, lang: str) -> str:
    with tempfile.TemporaryDirectory() as tmpdir:
        output_base = Path(tmpdir) / 'ocr'
        cmd = [
            'tesseract',
            str(input_image),
            str(output_base),
            '-l',
            lang,
        ]
        print('Running OCR:', ' '.join(cmd))
        subprocess.run(cmd, check=True)
        return (output_base.with_suffix('.txt')).read_text(encoding='utf-8')


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

    check_tesseract()

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
