"""Compatibility layer for legacy ``textmaker.*`` imports.

This package forwards submodule resolution to the renamed ``scripts`` package.
"""

from __future__ import annotations

from pathlib import Path


_SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
__path__ = [str(_SCRIPTS_DIR)]

