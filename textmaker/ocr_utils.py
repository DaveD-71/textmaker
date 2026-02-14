"""Shared OCR helpers for textmaker scripts."""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import os
from pathlib import Path
from typing import Iterable, Sequence


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


def _resolve_tessdata_dir() -> Path | None:
    """Resolve tessdata directory from env or tesseract install location."""
    env_val = os.getenv('TESSDATA_PREFIX')
    if env_val:
        env_path = Path(env_val).expanduser()
        if env_path.exists():
            if env_path.is_dir() and any(env_path.glob('*.traineddata')):
                return env_path
            td = env_path / 'tessdata'
            if td.is_dir():
                return td
            return env_path

    exe = shutil.which('tesseract')
    if exe:
        exe_dir = Path(exe).resolve().parent
        td = exe_dir / 'tessdata'
        if td.is_dir():
            return td
    return None


def run_tesseract(
    image_path: Path,
    lang: str,
    psm: int | None = None,
    extra_configs: Sequence[str] | None = None,
) -> str:
    """Run OCR for a single image and return extracted text."""
    check_tesseract()
    with tempfile.TemporaryDirectory() as tmpdir:
        output_base = Path(tmpdir) / 'ocr'
        cmd = ['tesseract', str(image_path), str(output_base), '-l', lang]
        if psm is not None:
            cmd += ['--psm', str(psm)]
        if extra_configs:
            for cfg in extra_configs:
                cmd += ['-c', cfg]
        tessdata_dir = _resolve_tessdata_dir()
        if tessdata_dir:
            cmd += ['--tessdata-dir', str(tessdata_dir)]
        print('Running OCR:', ' '.join(cmd))
        subprocess.run(cmd, check=True)
        return output_base.with_suffix('.txt').read_text(encoding='utf-8')


def run_tesseract_many(
    images: Iterable[Path],
    lang: str,
    psm: int | None = None,
    extra_configs: Sequence[str] | None = None,
) -> str:
    """Run OCR on multiple images and return combined text."""
    check_tesseract()
    image_list = list(images)
    chunks: list[str] = []
    tessdata_dir = _resolve_tessdata_dir()
    if tessdata_dir:
        print(f'Using tessdata dir: {tessdata_dir}')
    print(f'OCR pages: {len(image_list)}')
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        for index, image_path in enumerate(image_list, start=1):
            output_base = tmpdir_path / f'ocr-{index:03d}'
            cmd = ['tesseract', str(image_path), str(output_base), '-l', lang]
            if psm is not None:
                cmd += ['--psm', str(psm)]
            if extra_configs:
                for cfg in extra_configs:
                    cmd += ['-c', cfg]
            if tessdata_dir:
                cmd += ['--tessdata-dir', str(tessdata_dir)]
            print(f'Running OCR [{index}/{len(image_list)}]:', ' '.join(cmd))
            subprocess.run(cmd, check=True)
            chunks.append(output_base.with_suffix('.txt').read_text(encoding='utf-8').strip())
    # Preserve page boundaries for downstream layout/asset placement logic.
    # pdf_to_markdown splits pages on form-feed ("\f"), so keep that contract.
    return '\f\n'.join(chunk for chunk in chunks if chunk)
