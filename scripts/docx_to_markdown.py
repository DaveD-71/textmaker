"""
DOCX → Markdown splitter with media extraction and reference style export.

- Converts a DOCX to a single markdown file via pandoc.
- Splits the markdown into per-unit files (default: Heading 1 sections).
- Extracts embedded media to an assets folder.
- Optionally writes a reference DOCX that preserves the source styles for reuse.
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Iterable, List, Optional, Tuple
from zipfile import ZipFile

try:
    from docx import Document
except ImportError as exc:
    raise RuntimeError(
        'Missing dependency: python-docx is required. Install with `pip install python-docx`.'
    ) from exc
from scripts.preprocess_docx import preprocess_docx
from scripts.postprocess_markdown import postprocess_many


def check_pandoc(pandoc_bin: str = 'pandoc') -> None:
    """Ensure pandoc is on PATH."""
    if shutil.which(pandoc_bin) is None:
        print('Error: pandoc binary not found on PATH. Install from https://pandoc.org/installing.html')
        sys.exit(2)


def run_pandoc_to_markdown(
    input_docx: Path,
    output_dir: Path,
    output_md: Path,
    assets_arg: str,
    pandoc_bin: str = 'pandoc',
) -> None:
    """
    Run pandoc to convert DOCX to markdown and extract media.

    assets_arg is passed directly to --extract-media; keep it relative to output_dir
    to ensure markdown references are relative.
    """
    cmd = [
        pandoc_bin,
        str(input_docx),
        '--to',
        'gfm',
        '--wrap',
        'none',
        '--atx-headers',
        '--extract-media',
        assets_arg,
        '--output',
        str(output_md),
    ]
    print('Running pandoc:', ' '.join(map(str, cmd)))
    subprocess.run(cmd, check=True, cwd=output_dir)


def slugify(title: Optional[str]) -> str:
    """Create a filesystem-friendly slug from a heading."""
    if not title:
        return 'section'
    slug = re.sub(r'[^A-Za-z0-9]+', '-', title).strip('-').lower()
    if not slug:
        return 'section'
    return slug[:60]


def split_markdown_by_heading(md_text: str, level: int = 1) -> List[Tuple[Optional[str], str]]:
    """Split markdown content into sections keyed by heading level."""
    if level < 1:
        raise ValueError('Heading level must be >= 1')
    sections: List[Tuple[Optional[str], str]] = []
    heading_prefix = '#' * level + ' '
    deeper_prefix = '#' * (level + 1) + ' '

    current_title: Optional[str] = None
    current_lines: List[str] = []

    for line in md_text.splitlines():
        if line.startswith(heading_prefix) and not line.startswith(deeper_prefix):
            if current_lines:
                sections.append((current_title, '\n'.join(current_lines).strip('\n')))
            current_title = line[len(heading_prefix) :].strip()
            current_lines = [line]
        else:
            current_lines.append(line)

    if current_lines:
        sections.append((current_title, '\n'.join(current_lines).strip('\n')))

    return sections


def write_sections_to_files(sections: Iterable[Tuple[Optional[str], str]], dest_dir: Path) -> List[Path]:
    """Write split sections to numbered markdown files."""
    written: List[Path] = []
    for idx, (title, content) in enumerate(sections, start=1):
        slug = slugify(title or 'section')
        filename = f'{idx:02d}-{slug}.md'
        path = dest_dir / filename
        path.write_text((content.strip('\n') + '\n'), encoding='utf-8')
        written.append(path)
    return written


def create_reference_docx(source_docx: Path, reference_out: Path, keep_headers: bool = False) -> Path:
    """
    Create a reference DOCX that preserves styles from the source document but has no body content.

    Implementation: copy the source DOCX, then replace word/document.xml with a blank document
    to strip content while keeping custom styles, numbering, and themes intact.

    If keep_headers is True, we copy header/footer parts from the source to retain style references.
    """
    reference_out.parent.mkdir(parents=True, exist_ok=True)

    # Build a blank document.xml once for reuse
    with tempfile.TemporaryDirectory() as tmpdir:
        blank_path = Path(tmpdir) / 'blank.docx'
        doc = Document()
        doc.add_paragraph('Reference styles extracted from source document.')
        doc.save(blank_path)
        with ZipFile(blank_path, 'r') as zf_blank:
            blank_document_xml = zf_blank.read('word/document.xml')

    shutil.copyfile(source_docx, reference_out)
    with ZipFile(reference_out, 'a') as zf_out:
        zf_out.writestr('word/document.xml', blank_document_xml)
        if keep_headers:
            with ZipFile(source_docx, 'r') as zf_src:
                for name in zf_src.namelist():
                    if name.startswith('word/header') or name.startswith('word/footer'):
                        zf_out.writestr(name, zf_src.read(name))

    return reference_out


def main() -> None:
    parser = argparse.ArgumentParser(description='Split a DOCX into markdown units and extract assets.')
    parser.add_argument('--input', required=True, help='Input DOCX file to split.')
    parser.add_argument(
        '--output-dir',
        default='docx_export',
        help='Folder to write markdown files and assets (default: docx_export).',
    )
    parser.add_argument(
        '--assets-dir',
        default='assets',
        help='Assets folder name (relative to output-dir by default).',
    )
    parser.add_argument(
        '--unit-heading-level',
        type=int,
        default=1,
        help='Heading level that marks the start of a new unit (default: 1).',
    )
    parser.add_argument(
        '--reference-out',
        help='Optional path to write a reference DOCX that reuses styles from the input.',
    )
    parser.add_argument(
        '--keep-temp-md',
        action='store_true',
        help='Keep the intermediate combined markdown file (default: delete it).',
    )
    parser.add_argument(
        '--pandoc-bin',
        default='pandoc',
        help='Pandoc executable to invoke (default: pandoc).',
    )
    parser.add_argument(
        '--preserve-headers',
        action='store_true',
        help='When writing reference-out, keep headers/footers from the source.',
    )
    args = parser.parse_args()

    source_docx = Path(args.input).expanduser().resolve()
    if not source_docx.exists():
        print(f'Input DOCX not found: {source_docx}')
        sys.exit(1)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    assets_arg = Path(args.assets_dir)
    assets_dir = assets_arg if assets_arg.is_absolute() else (output_dir / assets_arg)
    assets_dir.mkdir(parents=True, exist_ok=True)

    temp_md = output_dir / '_full.md'
    temp_docx = output_dir / '_preprocessed.docx'

    check_pandoc(args.pandoc_bin)

    # Preprocess DOCX to add sentinel markers for unsupported elements
    preprocess_docx(source_docx, temp_docx)

    run_pandoc_to_markdown(
        input_docx=temp_docx,
        output_dir=output_dir,
        output_md=temp_md,
        assets_arg=str(assets_arg),
        pandoc_bin=args.pandoc_bin,
    )

    md_text = temp_md.read_text(encoding='utf-8')
    sections = split_markdown_by_heading(md_text, level=args.unit_heading_level)
    written_files = write_sections_to_files(sections, output_dir)

    # Replace sentinel markers in all written markdown files
    postprocess_many(written_files)

    if not args.keep_temp_md:
        temp_md.unlink(missing_ok=True)
        temp_docx.unlink(missing_ok=True)

    if args.reference_out:
        ref_path = Path(args.reference_out)
        create_reference_docx(source_docx, ref_path, keep_headers=args.preserve_headers)
        print(f'Wrote reference styles to {ref_path}')

    print(f'Wrote {len(written_files)} markdown file(s) to {output_dir}')
    print(f'Assets extracted to {assets_dir}')


if __name__ == '__main__':
    main()
