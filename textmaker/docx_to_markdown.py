"""
DOCX → Markdown splitter with media extraction and reference style export.

- Converts a DOCX to a single markdown file via pandoc.
- Splits the markdown into per-unit files (default: Heading 1 sections).
- Extracts embedded media to an assets folder.
- Optionally writes a reference DOCX that preserves the source styles for reuse.
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Iterable, List, Optional, Tuple
from zipfile import ZipFile
from xml.etree import ElementTree

try:
    from docx import Document  # type: ignore[reportMissingImports]
except ImportError as exc:
    raise RuntimeError(
        'Missing dependency: python-docx is required. Install with `pip install python-docx`.'
    ) from exc

from .preprocess_docx import preprocess_docx
from .postprocess_markdown import postprocess_many


SHAPE_NS = {
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'v': 'urn:schemas-microsoft-com:vml',
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
    'wps': 'http://schemas.microsoft.com/office/word/2010/wordprocessingShape',
}


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
    input_arg = input_docx.name if input_docx.parent == output_dir else str(input_docx)
    output_arg = output_md.name if output_md.parent == output_dir else str(output_md)
    base_cmd = [
        pandoc_bin,
        input_arg,
        '--to',
        'gfm',
        '--wrap',
        'none',
        '--extract-media',
        assets_arg,
        '--output',
        output_arg,
    ]
    header_flags = ['--markdown-headings=atx']
    last_exc: Optional[subprocess.CalledProcessError] = None

    for header_flag in header_flags + [None]:
        cmd = base_cmd.copy()
        if header_flag:
            cmd.insert(6, header_flag)
        print('Running pandoc:', ' '.join(map(str, cmd)))
        try:
            subprocess.run(cmd, check=True, cwd=output_dir, capture_output=True, text=True)
            return
        except subprocess.CalledProcessError as exc:
            last_exc = exc
            stderr = exc.stderr or ''
            if stderr:
                print('Pandoc error output:\n', stderr.strip(), file=sys.stderr)
            if header_flag and f'Unknown option {header_flag}' in stderr:
                continue
            raise

    if last_exc:
        raise last_exc


def slugify(title: Optional[str]) -> str:
    """Create a filesystem-friendly slug from a heading."""
    if not title:
        return 'section'
    slug = re.sub(r'[^A-Za-z0-9]+', '-', title).strip('-').lower()
    if not slug:
        return 'section'
    return slug[:60]


def split_markdown_by_heading(
    md_text: str,
    level: int = 1,
) -> Tuple[Optional[str], List[Tuple[Optional[str], str]]]:
    """Split markdown content into sections keyed by heading level."""
    if level < 1:
        raise ValueError('Heading level must be >= 1')
    sections: List[Tuple[Optional[str], str]] = []
    heading_prefix = '#' * level + ' '
    deeper_prefix = '#' * (level + 1) + ' '

    current_title: Optional[str] = None
    current_lines: List[str] = []
    front_matter: Optional[str] = None

    for line in md_text.splitlines():
        if line.startswith(heading_prefix) and not line.startswith(deeper_prefix):
            if current_lines:
                if current_title is None and front_matter is None:
                    front_matter = '\n'.join(current_lines).strip('\n')
                else:
                    sections.append((current_title, '\n'.join(current_lines).strip('\n')))
            current_title = line[len(heading_prefix) :].strip()
            current_lines = [line]
        else:
            current_lines.append(line)

    if current_lines:
        if current_title is None and front_matter is None:
            front_matter = '\n'.join(current_lines).strip('\n')
        else:
            sections.append((current_title, '\n'.join(current_lines).strip('\n')))

    return front_matter, sections


def write_sections_to_files(
    sections: Iterable[Tuple[Optional[str], str]],
    dest_dir: Path,
    start_index: int = 1,
) -> List[Path]:
    """Write split sections to numbered markdown files."""
    written: List[Path] = []
    for idx, (title, content) in enumerate(sections, start=start_index):
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


class ShapeAsset:
    def __init__(self, index: int, alt_text: str, text: str, asset_path: Path, link_path: str) -> None:
        self.index = index
        self.alt_text = alt_text
        self.text = text
        self.asset_path = asset_path
        self.link_path = link_path


def _extract_text_from_txbx(txbx) -> str:
    paragraphs = []
    for p in txbx.findall('.//w:p', SHAPE_NS):
        chunks = [t.text for t in p.findall('.//w:t', SHAPE_NS) if t.text]
        if chunks:
            paragraphs.append(''.join(chunks).strip())
    return '\n'.join(line for line in paragraphs if line)


def _get_shape_alt_text(shape_elem) -> str:
    doc_pr = shape_elem.find('.//wp:docPr', SHAPE_NS)
    if doc_pr is None:
        return ''
    desc = doc_pr.get('descr') or ''
    title = doc_pr.get('title') or ''
    return (desc or title).strip()


<<<<<<< ours
def extract_shapes(docx_path: Path, assets_dir: Path, assets_arg: Path) -> List[ShapeAsset]:
=======
def extract_shapes(docx_path: Path, assets_dir: Path, assets_link_base: Path) -> List[ShapeAsset]:
>>>>>>> theirs
    shapes: List[ShapeAsset] = []
    shape_assets_dir = assets_dir / 'shapes'

    with ZipFile(docx_path, 'r') as docx_zip:
        try:
            document_xml = docx_zip.read('word/document.xml')
        except KeyError:
            return shapes

    root = ElementTree.fromstring(document_xml)
    shape_elements = [
        elem
        for elem in root.iter()
        if elem.tag in {
            f"{{{SHAPE_NS['w']}}}drawing",
            f"{{{SHAPE_NS['w']}}}pict",
        }
    ]

    if not shape_elements:
        return shapes

    shape_assets_dir.mkdir(parents=True, exist_ok=True)

    for idx, shape in enumerate(shape_elements, start=1):
        alt_text = _get_shape_alt_text(shape)
        text_chunks = []
        for txbx in shape.findall('.//w:txbxContent', SHAPE_NS):
            text_chunks.append(_extract_text_from_txbx(txbx))
        text = '\n'.join(chunk for chunk in text_chunks if chunk).strip()

        asset_name = f'shape-{idx:03d}.xml'
        asset_path = shape_assets_dir / asset_name
        xml_payload = ElementTree.tostring(shape, encoding='unicode')
        asset_path.write_text(xml_payload, encoding='utf-8')

<<<<<<< ours
        link_path = (assets_arg / 'shapes' / asset_name).as_posix()
=======
        link_path = (assets_link_base / 'shapes' / asset_name).as_posix()
>>>>>>> theirs
        shapes.append(ShapeAsset(idx, alt_text, text, asset_path, link_path))

    return shapes


def _format_shape_text(text: str) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return ''
    prefixed = ['Shape text: ' + lines[0]]
    prefixed.extend(lines[1:])
    return '\n'.join(f'> {line}' for line in prefixed)


def replace_shape_markers(paths: Iterable[Path], shapes: List[ShapeAsset]) -> None:
    if not shapes:
        return
    shape_iter = iter(shapes)
    pattern = re.compile(r'\[\[SHAPE:([^\]]*)\]\]')

    for path in paths:
        text = path.read_text(encoding='utf-8')

        def _replace(match: re.Match) -> str:
            shape = next(shape_iter, None)
            if shape is None:
                return match.group(0)
            label = shape.alt_text or match.group(1).strip() or f'shape-{shape.index:03d}'
            link = f'[{label}]({shape.link_path})'
            blockquote = _format_shape_text(shape.text)
            if blockquote:
                return f'{link}\n\n{blockquote}'
            return link

        new_text = pattern.sub(_replace, text)
        path.write_text(new_text, encoding='utf-8')


<<<<<<< ours
=======
def rewrite_asset_links(paths: Iterable[Path], assets_arg: Path, assets_link_base: Path) -> None:
    assets_token = assets_arg.as_posix().rstrip('/')
    link_base = assets_link_base.as_posix().rstrip('/')
    if not assets_token or assets_token == link_base:
        return

    needle = f'{assets_token}/'
    replacement = f'{link_base}/'

    for path in paths:
        text = path.read_text(encoding='utf-8')
        if needle not in text:
            continue
        path.write_text(text.replace(needle, replacement), encoding='utf-8')


>>>>>>> theirs
def main() -> None:
    parser = argparse.ArgumentParser(description='Split a DOCX into markdown units and extract assets.')
    parser.add_argument('input', nargs='?', help='Input DOCX file to split.')
    parser.add_argument('--input', dest='input_arg', help='Input DOCX file to split.')
    parser.add_argument(
        '--output-dir',
        default=None,
        help='Folder to write markdown files and assets (default: "<input folder>\\out").',
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
        default=None,
        help='Path to write a reference DOCX (default: "<output-dir>\\reference.docx").',
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

    input_value = args.input_arg or args.input
    if not input_value:
        print('Input DOCX is required.')
        sys.exit(1)
    source_docx = Path(input_value).expanduser().resolve()
    if not source_docx.exists():
        print(f'Input DOCX not found: {source_docx}')
        sys.exit(1)

    base_dir = source_docx.parent
    desired_parent = base_dir if base_dir.name == source_docx.stem else (base_dir / source_docx.stem)
    desired_parent.mkdir(parents=True, exist_ok=True)

    if args.output_dir:
        output_dir = Path(args.output_dir).expanduser().resolve()
    else:
        output_dir = (desired_parent / 'out').resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    assets_arg = Path(args.assets_dir)
    assets_dir = assets_arg if assets_arg.is_absolute() else (output_dir / assets_arg)
    assets_dir.mkdir(parents=True, exist_ok=True)

    md_dir = output_dir / '.md'
    md_dir.mkdir(parents=True, exist_ok=True)
    assets_link_base = Path(os.path.relpath(assets_dir, md_dir))

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
    front_matter, sections = split_markdown_by_heading(
        md_text,
        level=args.unit_heading_level,
    )
    written_files: List[Path] = []
    if front_matter:
        front_path = md_dir / '00-front-matter.md'
        front_path.write_text((front_matter.strip('\n') + '\n'), encoding='utf-8')
        written_files.append(front_path)
    written_files.extend(write_sections_to_files(sections, md_dir, start_index=1))

<<<<<<< ours
    shapes = extract_shapes(temp_docx, assets_dir, assets_arg)
=======
    rewrite_asset_links(written_files, assets_arg, assets_link_base)

    shapes = extract_shapes(temp_docx, assets_dir, assets_link_base)
>>>>>>> theirs
    replace_shape_markers(written_files, shapes)

    # Replace sentinel markers in all written markdown files
    postprocess_many(written_files)

    if not args.keep_temp_md:
        temp_md.unlink(missing_ok=True)
        temp_docx.unlink(missing_ok=True)

    ref_path = Path(args.reference_out) if args.reference_out else (output_dir / 'reference.docx')
    if ref_path:
        create_reference_docx(source_docx, ref_path, keep_headers=args.preserve_headers)
        print(f'Wrote reference styles to {ref_path}')

    print(f'Wrote {len(written_files)} markdown file(s) to {md_dir}')
    print(f'Assets extracted to {assets_dir}')

    # Move the source DOCX into the same-named folder last, after all processing.
    if source_docx.parent != desired_parent:
        moved_path = desired_parent / source_docx.name
        if moved_path != source_docx:
            source_docx.replace(moved_path)


if __name__ == '__main__':
    main()
