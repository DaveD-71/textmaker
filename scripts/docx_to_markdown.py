"""
DOCX → Markdown splitter with media extraction and reference style export.

- Converts a DOCX to a single markdown file via pandoc.
- Splits the markdown into per-unit files (default: Heading 1 sections).
- Extracts embedded media to an assets folder.
- Optionally writes a reference DOCX that preserves the source styles for reuse.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Set, Tuple
from zipfile import ZipFile, ZIP_DEFLATED
from xml.etree import ElementTree

try:
    from docx import Document  # type: ignore[reportMissingImports]
except ImportError as exc:
    raise RuntimeError(
        'Missing dependency: python-docx is required. Install with `pip install python-docx`.'
    ) from exc

from .ocr_utils import check_tesseract
from .local_io import stage_input_file, sync_dir, sync_file
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

W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
XML_NS = 'http://www.w3.org/XML/1998/namespace'


def _w_tag(local_name: str) -> str:
    return f'{{{W_NS}}}{local_name}'


ElementTree.register_namespace('w', W_NS)
ElementTree.register_namespace('xml', XML_NS)


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
    ocr_lang: Optional[str] = None,
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
    if ocr_lang:
        base_cmd += ['--ocr-lang', ocr_lang]
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


def extract_all_media_assets(docx_path: Path, assets_dir: Path) -> int:
    """
    Copy every media payload from the DOCX package into assets/media.

    This supplements pandoc's --extract-media output, which may omit media used
    only in headers/footers.
    """
    media_out_dir = assets_dir / 'media'
    media_out_dir.mkdir(parents=True, exist_ok=True)
    copied = 0

    with ZipFile(docx_path, 'r') as docx_zip:
        for name in docx_zip.namelist():
            if not name.startswith('word/media/'):
                continue
            rel_path = Path(name[len('word/media/') :])
            if not rel_path.name:
                continue
            target = media_out_dir / rel_path
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists():
                continue
            target.write_bytes(docx_zip.read(name))
            copied += 1

    return copied


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


def _iter_style_refs_from_content(root: ElementTree.Element) -> Set[str]:
    """Collect style ids referenced by content XML nodes."""
    refs: Set[str] = set()
    for tag_name in ('pStyle', 'rStyle', 'tblStyle'):
        for elem in root.findall(f'.//w:{tag_name}', {'w': W_NS}):
            style_id = (elem.get(_w_tag('val')) or '').strip()
            if style_id:
                refs.add(style_id)
    return refs


def _collect_referenced_style_ids(docx_zip: ZipFile, keep_headers: bool) -> Set[str]:
    """
    Gather style ids actively referenced by document content parts.

    We always include the main document body. Header/footer style refs are included
    only when --preserve-headers is enabled.
    """
    style_ids: Set[str] = set()
    part_names = {'word/document.xml'}
    if keep_headers:
        for name in docx_zip.namelist():
            if re.match(r'word/(header|footer)\d+\.xml$', name):
                part_names.add(name)

    for part_name in sorted(part_names):
        try:
            root = ElementTree.fromstring(docx_zip.read(part_name))
        except (KeyError, ElementTree.ParseError):
            continue
        style_ids.update(_iter_style_refs_from_content(root))

    return style_ids


def _build_blank_document_xml_preserving_layout(source_document_xml: bytes) -> bytes:
    """
    Create a minimal document.xml that preserves source section/page settings.

    If source section properties are missing, fall back to explicit A4 settings.
    """
    root = ElementTree.fromstring(source_document_xml)
    body = root.find(_w_tag('body'))
    if body is None:
        raise RuntimeError('Invalid DOCX package: word/document.xml missing w:body')

    source_sectpr = body.find(_w_tag('sectPr'))

    for child in list(body):
        body.remove(child)

    para = ElementTree.Element(_w_tag('p'))
    run = ElementTree.SubElement(para, _w_tag('r'))
    text = ElementTree.SubElement(run, _w_tag('t'))
    text.text = ''
    body.append(para)

    if source_sectpr is not None:
        body.append(source_sectpr)
    else:
        sectpr = ElementTree.Element(_w_tag('sectPr'))
        # A4 in twips; default to A4 rather than Letter.
        ElementTree.SubElement(
            sectpr,
            _w_tag('pgSz'),
            {_w_tag('w'): '11906', _w_tag('h'): '16838'},
        )
        ElementTree.SubElement(
            sectpr,
            _w_tag('pgMar'),
            {
                _w_tag('top'): '1440',
                _w_tag('right'): '1440',
                _w_tag('bottom'): '1440',
                _w_tag('left'): '1440',
                _w_tag('header'): '720',
                _w_tag('footer'): '720',
                _w_tag('gutter'): '0',
            },
        )
        body.append(sectpr)

    return ElementTree.tostring(root, encoding='utf-8', xml_declaration=True)


def _prune_styles_xml(styles_xml: bytes, used_style_ids: Set[str]) -> bytes:
    """
    Remove unused style definitions from styles.xml.

    Keep:
    - styles referenced by content
    - default styles
    - mandatory baseline styles
    - transitive style dependencies (basedOn/next/link)
    """
    root = ElementTree.fromstring(styles_xml)
    styles = root.findall(_w_tag('style'))
    style_by_id: Dict[str, ElementTree.Element] = {}
    for style in styles:
        style_id = (style.get(_w_tag('styleId')) or '').strip()
        if style_id:
            style_by_id[style_id] = style

    keep_ids: Set[str] = set(used_style_ids)
    keep_ids.update({'Normal', 'DefaultParagraphFont', 'TableNormal', 'NoList'})

    for style in styles:
        is_default = (style.get(_w_tag('default')) or '').strip()
        if is_default in {'1', 'true', 'on'}:
            style_id = (style.get(_w_tag('styleId')) or '').strip()
            if style_id:
                keep_ids.add(style_id)

    changed = True
    while changed:
        changed = False
        for style_id in list(keep_ids):
            style = style_by_id.get(style_id)
            if style is None:
                continue
            for dep_tag in ('basedOn', 'next', 'link'):
                dep = style.find(_w_tag(dep_tag))
                dep_id = (dep.get(_w_tag('val')) or '').strip() if dep is not None else ''
                if dep_id and dep_id not in keep_ids:
                    keep_ids.add(dep_id)
                    changed = True

    for style in styles:
        style_id = (style.get(_w_tag('styleId')) or '').strip()
        if style_id and style_id not in keep_ids:
            root.remove(style)

    latent = root.find(_w_tag('latentStyles'))
    if latent is not None:
        root.remove(latent)

    return ElementTree.tostring(root, encoding='utf-8', xml_declaration=True)


def create_reference_docx(source_docx: Path, reference_out: Path, keep_headers: bool = False) -> Path:
    """
    Create a reference DOCX that preserves styles from the source document but has no body content.

    Implementation: copy the source DOCX, then replace word/document.xml with a blank document
    to strip content while keeping custom styles, numbering, and themes intact.

    If keep_headers is True, we copy header/footer parts from the source to retain style references.
    """
    reference_out.parent.mkdir(parents=True, exist_ok=True)

    with ZipFile(source_docx, 'r') as zf_src:
        source_document_xml = zf_src.read('word/document.xml')
        blank_document_xml = _build_blank_document_xml_preserving_layout(source_document_xml)
        used_style_ids = _collect_referenced_style_ids(zf_src, keep_headers=keep_headers)
        pruned_styles_xml = None
        pruned_styles_with_effects_xml = None
        if 'word/styles.xml' in zf_src.namelist():
            pruned_styles_xml = _prune_styles_xml(zf_src.read('word/styles.xml'), used_style_ids)
        if 'word/stylesWithEffects.xml' in zf_src.namelist():
            pruned_styles_with_effects_xml = _prune_styles_xml(
                zf_src.read('word/stylesWithEffects.xml'),
                used_style_ids,
            )

    # Rebuild the zip package instead of appending entries. This avoids duplicate
    # word/document.xml records and keeps the output package deterministic.
    with tempfile.TemporaryDirectory() as tmpdir:
        rebuilt_path = Path(tmpdir) / 'reference_rebuilt.docx'
        with ZipFile(source_docx, 'r') as zf_src, ZipFile(
            rebuilt_path, 'w', compression=ZIP_DEFLATED
        ) as zf_out:
            for name in zf_src.namelist():
                if name == 'word/document.xml':
                    zf_out.writestr(name, blank_document_xml)
                    continue
                if name == 'word/styles.xml' and pruned_styles_xml is not None:
                    zf_out.writestr(name, pruned_styles_xml)
                    continue
                if name == 'word/stylesWithEffects.xml' and pruned_styles_with_effects_xml is not None:
                    zf_out.writestr(name, pruned_styles_with_effects_xml)
                    continue
                if not keep_headers and (name.startswith('word/header') or name.startswith('word/footer')):
                    continue
                zf_out.writestr(name, zf_src.read(name))

        shutil.copyfile(rebuilt_path, reference_out)

    return reference_out


class ShapeAsset:
    def __init__(
        self,
        index: int,
        alt_text: str,
        text: str,
        asset_path: Optional[Path],
        link_path: str,
        paragraph_index: int,
        kind: str,
        hidden: bool,
        canonical_index: int,
        duplicate_of: Optional[int] = None,
    ) -> None:
        self.index = index
        self.alt_text = alt_text
        self.text = text
        self.asset_path = asset_path
        self.link_path = link_path
        self.paragraph_index = paragraph_index
        self.kind = kind
        self.hidden = hidden
        self.canonical_index = canonical_index
        self.duplicate_of = duplicate_of


def _shape_kind(shape_elem) -> str:
    if shape_elem.tag == f"{{{SHAPE_NS['w']}}}drawing":
        return 'drawing'
    if shape_elem.tag == f"{{{SHAPE_NS['w']}}}pict":
        return 'pict'
    return 'unknown'


def _shape_is_hidden(shape_elem) -> bool:
    doc_pr = shape_elem.find('.//wp:docPr', SHAPE_NS)
    if doc_pr is not None:
        hidden = (doc_pr.get('hidden') or '').strip().lower()
        if hidden in {'1', 'true', 'on'}:
            return True
    v_shape = shape_elem.find('.//v:shape', SHAPE_NS)
    if v_shape is not None:
        style = (v_shape.get('style') or '').replace(' ', '').lower()
        if 'visibility:hidden' in style:
            return True
    return False


def _shape_rel_ids(shape_elem) -> Tuple[str, ...]:
    rel_ids: Set[str] = set()
    for blip in shape_elem.findall('.//a:blip', SHAPE_NS):
        embed = blip.get(f"{{{SHAPE_NS['r']}}}embed")
        link = blip.get(f"{{{SHAPE_NS['r']}}}link")
        if embed:
            rel_ids.add(embed)
        if link:
            rel_ids.add(link)
    return tuple(sorted(rel_ids))


def _shape_extent_key(shape_elem) -> str:
    extent = shape_elem.find('.//wp:extent', SHAPE_NS)
    if extent is not None:
        return f"{extent.get('cx') or ''}x{extent.get('cy') or ''}"
    v_shape = shape_elem.find('.//v:shape', SHAPE_NS)
    if v_shape is not None:
        return (v_shape.get('style') or '').replace(' ', '').lower()
    return ''


def _extract_text_from_txbx(txbx) -> str:
    paragraphs = []
    for p in txbx.findall('.//w:p', SHAPE_NS):
        chunks = [t.text for t in p.findall('.//w:t', SHAPE_NS) if t.text]
        if chunks:
            paragraphs.append(''.join(chunks).strip())
    return '\n'.join(line for line in paragraphs if line)


def _get_shape_alt_text(shape_elem) -> str:
    doc_pr = shape_elem.find('.//wp:docPr', SHAPE_NS)
    if doc_pr is not None:
        desc = (doc_pr.get('descr') or '').strip()
        title = (doc_pr.get('title') or '').strip()
        if desc or title:
            return desc or title

    v_shape = shape_elem.find('.//v:shape', SHAPE_NS)
    if v_shape is not None:
        for key in ('alt', 'title', 'alttext'):
            val = (v_shape.get(key) or '').strip()
            if val:
                return val

    return ''


def extract_shapes(docx_path: Path, assets_dir: Path, assets_link_base: Path) -> List[ShapeAsset]:
    shapes: List[ShapeAsset] = []
    shape_assets_dir = assets_dir / 'shapes'
    shape_elements: List[Tuple[int, str, int, object]] = []

    with ZipFile(docx_path, 'r') as docx_zip:
        part_names = ['word/document.xml']
        for name in docx_zip.namelist():
            if re.match(r'word/(header|footer)\d+\.xml$', name):
                part_names.append(name)

        raw_index = 0
        for part_name in sorted(set(part_names)):
            try:
                part_xml = docx_zip.read(part_name)
            except KeyError:
                continue
            root = ElementTree.fromstring(part_xml)
            for para_idx, para in enumerate(root.findall('.//w:p', SHAPE_NS), start=1):
                for elem in para.findall('.//w:drawing', SHAPE_NS):
                    raw_index += 1
                    shape_elements.append((raw_index, part_name, para_idx, elem))
                for elem in para.findall('.//w:pict', SHAPE_NS):
                    raw_index += 1
                    shape_elements.append((raw_index, part_name, para_idx, elem))

    if not shape_elements:
        return shapes

    shape_assets_dir.mkdir(parents=True, exist_ok=True)

    canonical_by_signature: Dict[Tuple, ShapeAsset] = {}
    canonical_by_raw_index: Dict[int, ShapeAsset] = {}

    for idx, source_part, para_idx, shape in shape_elements:
        alt_text = _get_shape_alt_text(shape)
        hidden = _shape_is_hidden(shape)
        kind = _shape_kind(shape)
        text_chunks = []
        for txbx in shape.findall('.//w:txbxContent', SHAPE_NS):
            text_chunks.append(_extract_text_from_txbx(txbx))
        text = '\n'.join(chunk for chunk in text_chunks if chunk).strip()

        signature = (
            source_part,
            para_idx,
            alt_text.strip().lower(),
            text.strip(),
            _shape_rel_ids(shape),
            _shape_extent_key(shape),
        )

        duplicate_of: Optional[int] = None
        canonical = canonical_by_signature.get(signature)
        if canonical is not None:
            duplicate_of = canonical.index
        elif hidden:
            # Hidden shapes are often fallback copies; alias to canonical when possible.
            fallback_signature = signature[:-1]
            for sig, candidate in canonical_by_signature.items():
                if sig[:-1] == fallback_signature:
                    canonical = candidate
                    duplicate_of = candidate.index
                    break

        if canonical is not None:
            shape_record = ShapeAsset(
                index=idx,
                alt_text=alt_text,
                text=text,
                asset_path=canonical.asset_path,
                link_path=canonical.link_path,
                paragraph_index=para_idx,
                kind=kind,
                hidden=hidden,
                canonical_index=canonical.canonical_index,
                duplicate_of=duplicate_of,
            )
            shapes.append(shape_record)
            canonical_by_raw_index[idx] = canonical
        else:
            asset_name = f'shape-{idx:03d}.xml'
            asset_path = shape_assets_dir / asset_name
            xml_payload = ElementTree.tostring(shape, encoding='unicode')
            asset_path.write_text(xml_payload, encoding='utf-8')
            link_path = (assets_link_base / 'shapes' / asset_name).as_posix()

            shape_record = ShapeAsset(
                index=idx,
                alt_text=alt_text,
                text=text,
                asset_path=asset_path,
                link_path=link_path,
                paragraph_index=para_idx,
                kind=kind,
                hidden=hidden,
                canonical_index=idx,
            )
            shapes.append(shape_record)
            canonical_by_signature[signature] = shape_record
            canonical_by_raw_index[idx] = shape_record

        meta_name = f'shape-{idx:03d}.json'
        meta_path = shape_assets_dir / meta_name
        record = shapes[-1]
        metadata = {
            'shape_index': idx,
            'canonical_shape_index': record.canonical_index,
            'duplicate_of': record.duplicate_of,
            'kind': kind,
            'hidden': hidden,
            'paragraph_index': para_idx,
            'alt_text': alt_text,
            'text_excerpt': text[:200],
            'xml_link_path': record.link_path,
            'source_part': source_part,
        }
        meta_path.write_text(json.dumps(metadata, ensure_ascii=True, indent=2), encoding='utf-8')

    return shapes


def _format_shape_text(text: str) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return ''
    prefixed = ['Shape text: ' + lines[0]]
    prefixed.extend(lines[1:])
    return '\n'.join(f'> {line}' for line in prefixed)


def _format_shape_inline_text(text: str) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return ''
    joined = '; '.join(lines)
    return f'Shape text: {joined}'


def replace_shape_markers(paths: Iterable[Path], shapes: List[ShapeAsset], mode: str = 'link') -> None:
    if not shapes:
        return
    shape_by_index = {shape.index: shape for shape in shapes}
    pattern = re.compile(r'\[\[SHAPE:(\d+)(?:\|([^\]]*))?\]\]')

    for path in paths:
        text = path.read_text(encoding='utf-8')

        def _replace(match: re.Match) -> str:
            shape_idx = int(match.group(1))
            marker_label = (match.group(2) or '').strip()
            shape = shape_by_index.get(shape_idx)
            if shape is None:
                return match.group(0)
            label = shape.alt_text or marker_label or f'shape-{shape.index:03d}'
            blockquote = _format_shape_text(shape.text)
            if mode == 'placeholder':
                return f'*[shape: {label}]*'
            if mode == 'inline-text-only':
                inline_text = _format_shape_inline_text(shape.text)
                if inline_text:
                    return inline_text
                return f'*[shape: {label}]*'

            link = f'[{label}]({shape.link_path})'
            if blockquote:
                return f'{link}\n\n{blockquote}'
            return link

        new_text = pattern.sub(_replace, text)
        path.write_text(new_text, encoding='utf-8')


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
        '--ocr-lang',
        help='Enable OCR during conversion with the provided Tesseract languages (e.g. "eng+jpn").',
    )
    parser.add_argument(
        '--preserve-headers',
        action='store_true',
        help='When writing reference-out, keep headers/footers from the source.',
    )
    parser.add_argument(
        '--shape-output',
        choices=['link', 'placeholder', 'inline-text-only'],
        default='link',
        help='How shape markers render in markdown: link (default), placeholder, inline-text-only.',
    )
    parser.add_argument(
        '--no-local-staging',
        action='store_true',
        help='Disable default behavior that stages conversion in a local temp folder before syncing outputs.',
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
    if not source_docx.is_file():
        print(f'Input path must be a DOCX file, not a directory: {source_docx}')
        sys.exit(1)
    if source_docx.suffix.lower() != '.docx':
        print(f'Input file must have .docx extension: {source_docx}')
        sys.exit(1)
    original_source_docx = source_docx

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

    run_source_docx = source_docx
    run_output_dir = output_dir
    run_assets_dir = assets_dir
    run_md_dir = md_dir
    staging_ctx: tempfile.TemporaryDirectory[str] | None = None
    if not args.no_local_staging:
        staging_ctx = tempfile.TemporaryDirectory(prefix='textmaker-docx-')
        staging_root = Path(staging_ctx.name)
        run_source_docx = stage_input_file(source_docx, staging_root / 'input')
        run_output_dir = staging_root / 'out'
        run_output_dir.mkdir(parents=True, exist_ok=True)
        run_assets_dir = (run_output_dir / assets_arg) if not assets_arg.is_absolute() else (staging_root / 'assets')
        run_assets_dir.mkdir(parents=True, exist_ok=True)
        run_md_dir = run_output_dir / '.md'
        run_md_dir.mkdir(parents=True, exist_ok=True)
        print(f'Local staging enabled: {run_source_docx}')

    temp_md = run_output_dir / '_full.md'
    temp_docx = run_output_dir / '_preprocessed.docx'

    check_pandoc(args.pandoc_bin)
    if args.ocr_lang:
        check_tesseract()

    # Preprocess DOCX to add sentinel markers for unsupported elements
    preprocess_docx(run_source_docx, temp_docx)

    run_pandoc_to_markdown(
        input_docx=temp_docx,
        output_dir=run_output_dir,
        output_md=temp_md,
        assets_arg=str(assets_arg),
        pandoc_bin=args.pandoc_bin,
        ocr_lang=args.ocr_lang,
    )
    copied_media_assets = extract_all_media_assets(temp_docx, run_assets_dir)

    md_text = temp_md.read_text(encoding='utf-8')
    front_matter, sections = split_markdown_by_heading(
        md_text,
        level=args.unit_heading_level,
    )
    written_files: List[Path] = []
    if front_matter:
        front_path = run_md_dir / '00-front-matter.md'
        front_path.write_text((front_matter.strip('\n') + '\n'), encoding='utf-8')
        written_files.append(front_path)
    written_files.extend(write_sections_to_files(sections, run_md_dir, start_index=1))

    rewrite_asset_links(written_files, assets_arg, assets_link_base)

    shapes = extract_shapes(temp_docx, run_assets_dir, assets_link_base)
    replace_shape_markers(written_files, shapes, mode=args.shape_output)
    duplicate_shapes = sum(1 for s in shapes if s.duplicate_of is not None)
    hidden_shapes = sum(1 for s in shapes if s.hidden)

    # Replace sentinel markers in all written markdown files
    postprocess_many(written_files)

    if not args.keep_temp_md:
        temp_md.unlink(missing_ok=True)
        temp_docx.unlink(missing_ok=True)

    ref_path = Path(args.reference_out) if args.reference_out else (output_dir / 'reference.docx')
    if ref_path:
        run_ref_path = ref_path
        if staging_ctx is not None:
            run_ref_path = run_output_dir / 'reference.docx'
        create_reference_docx(run_source_docx, run_ref_path, keep_headers=args.preserve_headers)
        if staging_ctx is not None:
            sync_file(run_ref_path, ref_path)
        print(f'Wrote reference styles to {ref_path}')

    if staging_ctx is not None:
        sync_dir(run_md_dir, md_dir)
        sync_dir(run_assets_dir, assets_dir)
        staging_ctx.cleanup()

    print(f'Wrote {len(written_files)} markdown file(s) to {md_dir}')
    print(f'Assets extracted to {assets_dir}')
    if copied_media_assets:
        print(f'Added {copied_media_assets} package media asset(s) from DOCX parts (including headers/footers).')
    print(
        f'Processed {len(shapes)} shape marker(s); '
        f'{duplicate_shapes} duplicate fallback shape(s) aliased; '
        f'{hidden_shapes} hidden shape(s) detected.'
    )

    # Move the source DOCX into the same-named folder last, after all processing.
    if original_source_docx.parent != desired_parent:
        moved_path = desired_parent / original_source_docx.name
        if moved_path != original_source_docx:
            original_source_docx.replace(moved_path)


if __name__ == '__main__':
    main()
