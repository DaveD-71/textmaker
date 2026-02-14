"""Shared OCR helpers for textmaker scripts."""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Iterable


def tesseract_available() -> bool:
    """Return True when Tesseract is available on PATH."""
    return shutil.which('tesseract') is not None


def check_tesseract() -> None:
    """Exit with an actionable message if Tesseract is unavailable."""
    if not tesseract_available():
        print(
            'Error: tesseract binary not found on PATH. Install from '
            'https://tesseract-ocr.github.io/tessdoc/Installation.html'
        )
        sys.exit(2)


def run_tesseract(image_path: Path, lang: str) -> str:
    """Run OCR for a single image and return extracted text."""
    check_tesseract()
    with tempfile.TemporaryDirectory() as tmpdir:
        output_base = Path(tmpdir) / 'ocr'
        cmd = ['tesseract', str(image_path), str(output_base), '-l', lang]
        print('Running OCR:', ' '.join(cmd))
        subprocess.run(cmd, check=True)
        return output_base.with_suffix('.txt').read_text(encoding='utf-8')


def run_tesseract_many(images: Iterable[Path], lang: str) -> str:
    """Run OCR on multiple images and return combined text."""
    check_tesseract()
    chunks: list[str] = []
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        for index, image_path in enumerate(images, start=1):
            output_base = tmpdir_path / f'ocr-{index:03d}'
            cmd = ['tesseract', str(image_path), str(output_base), '-l', lang]
            print('Running OCR:', ' '.join(cmd))
            subprocess.run(cmd, check=True)
            chunks.append(output_base.with_suffix('.txt').read_text(encoding='utf-8'))
    return '\n'.join(chunk.strip() for chunk in chunks if chunk.strip())
