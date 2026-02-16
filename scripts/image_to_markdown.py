"""
Image → Markdown converter with OCR.

- Runs Tesseract OCR on a single image.
- Writes OCR text to a markdown file.
"""
from __future__ import annotations

import argparse
import sys
import tempfile
from pathlib import Path

from .local_io import stage_input_file, sync_file
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
    parser.add_argument(
        '--no-local-staging',
        action='store_true',
        help='Disable default behavior that stages conversion in a local temp folder before syncing outputs.',
    )
    args = parser.parse_args()


    input_path = Path(args.input).expanduser().resolve()
    if not input_path.exists():
        print(f'Error: input image not found: {input_path}')
        sys.exit(1)

    output_path = Path(args.output) if args.output else Path(f'{input_path.stem}.md')
    output_path.parent.mkdir(parents=True, exist_ok=True)

    staging_ctx: tempfile.TemporaryDirectory[str] | None = None
    run_input_path = input_path
    run_output_path = output_path
    if not args.no_local_staging:
        staging_ctx = tempfile.TemporaryDirectory(prefix='textmaker-image-')
        staging_root = Path(staging_ctx.name)
        run_input_path = stage_input_file(input_path, staging_root / 'input')
        run_output_path = staging_root / output_path.name
        print(f'Local staging enabled: {run_input_path}')

    ocr_text = run_tesseract(run_input_path, args.ocr_lang)
    run_output_path.write_text(ocr_text.strip() + '\n', encoding='utf-8')
    if staging_ctx is not None:
        sync_file(run_output_path, output_path)
        staging_ctx.cleanup()
    print('Wrote', output_path)


if __name__ == '__main__':
    main()
