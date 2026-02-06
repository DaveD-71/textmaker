"""
PDF → Markdown converter with asset extraction and optional OCR.

- Extracts embedded images via pdfimages.
- Extracts text via pdftotext (default) or runs Tesseract OCR on page renders.
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def check_binary(name: str, install_url: str) -> None:
    if shutil.which(name) is None:
        print(f'Error: {name} binary not found on PATH. Install from {install_url}')
        sys.exit(2)


def check_tesseract() -> None:
    check_binary('tesseract', 'https://tesseract-ocr.github.io/tessdoc/Installation.html')


def run_pdftotext(input_pdf: Path, output_txt: Path) -> None:
    check_binary('pdftotext', 'https://poppler.freedesktop.org/')
    cmd = [
        'pdftotext',
        '-layout',
        str(input_pdf),
        str(output_txt),
    ]
    print('Running:', ' '.join(cmd))
    subprocess.run(cmd, check=True)


def run_pdfimages(input_pdf: Path, assets_dir: Path, prefix: str) -> list[Path]:
    check_binary('pdfimages', 'https://poppler.freedesktop.org/')
    assets_dir.mkdir(parents=True, exist_ok=True)
    output_prefix = assets_dir / prefix
    cmd = [
        'pdfimages',
        '-all',
        str(input_pdf),
        str(output_prefix),
    ]
    print('Running:', ' '.join(cmd))
    subprocess.run(cmd, check=True)
    return sorted(assets_dir.glob(f'{prefix}*'))


def run_pdftoppm(input_pdf: Path, output_dir: Path, prefix: str) -> list[Path]:
    check_binary('pdftoppm', 'https://poppler.freedesktop.org/')
    output_dir.mkdir(parents=True, exist_ok=True)
    output_prefix = output_dir / prefix
    cmd = [
        'pdftoppm',
        '-png',
        str(input_pdf),
        str(output_prefix),
    ]
    print('Running:', ' '.join(cmd))
    subprocess.run(cmd, check=True)
    return sorted(output_dir.glob(f'{prefix}-*.png'))


def run_tesseract(images: list[Path], lang: str) -> str:
    check_tesseract()
    chunks: list[str] = []
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        for index, image_path in enumerate(images, start=1):
            output_base = tmpdir_path / f'ocr-{index:03d}'
            cmd = [
                'tesseract',
                str(image_path),
                str(output_base),
                '-l',
                lang,
            ]
            print('Running OCR:', ' '.join(cmd))
            subprocess.run(cmd, check=True)
            chunks.append(output_base.with_suffix('.txt').read_text(encoding='utf-8'))
    return '\n'.join(chunk.strip() for chunk in chunks if chunk.strip())


def build_markdown(text: str, image_paths: list[Path], assets_rel: Path) -> str:
    lines = [text.strip()] if text.strip() else []
    if image_paths:
        lines.append('')
        lines.append('## Extracted Images')
        for path in image_paths:
            rel_path = assets_rel / path.name
            lines.append(f'![{path.stem}]({rel_path.as_posix()})')
    return '\n'.join(lines).strip() + '\n'


def main() -> None:
    parser = argparse.ArgumentParser(description='Convert a PDF to markdown with assets.')
    parser.add_argument('--input', required=True, help='Input PDF file')
    parser.add_argument(
        '--output-dir',
        help='Output directory (default: "<input folder>\\out")',
    )
    parser.add_argument(
        '--assets-dir',
        default='assets',
        help='Assets folder name (relative to output-dir by default).',
    )
    parser.add_argument(
        '--output',
        help='Output markdown file path (default: "<output-dir>/<input stem>.md")',
    )
    parser.add_argument(
        '--ocr-lang',
        default='eng+jpn',
        help='Tesseract language(s) for OCR (default: "eng+jpn").',
    )
    parser.add_argument(
        '--no-ocr',
        action='store_true',
        help='Disable OCR and use pdftotext instead.',
    )
    args = parser.parse_args()

    input_path = Path(args.input).expanduser().resolve()
    if not input_path.exists():
        print(f'Error: input PDF not found: {input_path}')
        sys.exit(1)

    base_dir = input_path.parent
    output_dir = Path(args.output_dir).expanduser().resolve() if args.output_dir else (base_dir / 'out').resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    assets_arg = Path(args.assets_dir)
    assets_dir = assets_arg if assets_arg.is_absolute() else (output_dir / assets_arg)
    assets_dir.mkdir(parents=True, exist_ok=True)

    output_md = Path(args.output) if args.output else (output_dir / f'{input_path.stem}.md')
    output_md.parent.mkdir(parents=True, exist_ok=True)

    extracted_images = run_pdfimages(input_path, assets_dir, prefix='image')

    if args.ocr_lang and not args.no_ocr:
        page_images = run_pdftoppm(input_path, output_dir / '_pages', prefix='page')
        text = run_tesseract(page_images, args.ocr_lang)
    else:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_txt = Path(tmpdir) / f'{input_path.stem}.txt'
            run_pdftotext(input_path, tmp_txt)
            text = tmp_txt.read_text(encoding='utf-8')

    assets_rel = Path('.') if assets_dir == output_md.parent else Path(
        os.path.relpath(assets_dir, output_md.parent)
    )
    markdown = build_markdown(text, extracted_images, assets_rel)
    output_md.write_text(markdown, encoding='utf-8')
    print('Wrote', output_md)


if __name__ == '__main__':
    main()
