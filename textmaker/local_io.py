"""Helpers for local staging and output sync."""
from __future__ import annotations

import shutil
from pathlib import Path


def stage_input_file(source: Path, staging_root: Path) -> Path:
    """Copy an input file to a local staging folder and return staged path."""
    staging_root.mkdir(parents=True, exist_ok=True)
    staged = staging_root / source.name
    shutil.copy2(source, staged)
    return staged


def sync_file(source: Path, dest: Path) -> None:
    """Copy a file to destination, creating parent directories."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, dest)


def sync_dir(source_dir: Path, dest_dir: Path) -> None:
    """Merge-copy a directory tree into destination."""
    if not source_dir.exists():
        return
    dest_dir.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source_dir, dest_dir, dirs_exist_ok=True)
