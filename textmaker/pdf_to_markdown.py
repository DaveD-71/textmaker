"""
PDF → Markdown converter with asset extraction and optional OCR.

- Extracts embedded images via pdfimages.
- Extracts text via pdftotext (default) or runs Tesseract OCR on page renders.
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
from typing import Any

from .ocr_utils import check_tesseract, run_tesseract, run_tesseract_many, tesseract_available
from .local_io import stage_input_file, sync_dir, sync_file


class PdfImageAsset:
    def __init__(
        self,
        path: Path,
        page: int | None = None,
        width_px: int | None = None,
        height_px: int | None = None,
        x_ppi: int | None = None,
        y_ppi: int | None = None,
    ) -> None:
        self.path = path
        self.page = page
        self.width_px = width_px
        self.height_px = height_px
        self.x_ppi = x_ppi
        self.y_ppi = y_ppi


_CIRCLED_NUM_MAP = {chr(0x2460 + i): str(i + 1) for i in range(20)}  # ①..⑳
_FULLWIDTH_DIGITS = str.maketrans('０１２３４５６７８９', '0123456789')


def _normalize_leading_list_marker(text: str) -> str:
    s = text.strip()
    if not s:
        return s

    # Normalize common full-width punctuation first.
    s = s.replace('（', '(').replace('）', ')')
    s = s.replace('［', '[').replace('］', ']')

    # ① / (②) / [③] -> (1) / (2) / (3)
    m = re.match(r'^[\(\[\{]?\s*([①-⑳])\s*[\)\]\}]?\s*', s)
    if m:
        n = _CIRCLED_NUM_MAP.get(m.group(1), '')
        rest = s[m.end() :].lstrip()
        return f'({n}) {rest}'.rstrip()

    # (４) / [7] / （10） -> (4) / (7) / (10)
    m = re.match(r'^[\(\[\{]?\s*([0-9０-９]+)\s*[\)\]\}]?\s*', s)
    if m:
        n = m.group(1).translate(_FULLWIDTH_DIGITS)
        rest = s[m.end() :].lstrip()
        return f'({n}) {rest}'.rstrip()

    return s


def _normalize_ocr_english_artifacts(text: str) -> str:
    s = text
    # Common OCR joins for small English words.
    replacements = {
        r'\batleast\b': 'at least',
        r'\binfact\b': 'in fact',
        r'\balot\b': 'a lot',
        r'\bacold\b': 'a cold',
        r'\bacheckup\b': 'a checkup',
        r'\bata\b': 'at a',
        r'\bona\b': 'on a',
        r'\byouexercise\b': 'you exercise',
    }
    for pat, repl in replacements.items():
        s = re.sub(pat, repl, s, flags=re.IGNORECASE)

    # Normalize item markers like "16.(D)" -> "16. (D)"
    s = re.sub(r'^(\d+)\.\s*\(([A-Za-z])\)', r'\1. (\2)', s)
    # Normalize malformed parenthesized option marker at start "(O" -> "(C)" when line starts with item number.
    s = re.sub(r'^(\d+)\.\s*\(O([^\)])', r'\1. (C)\2', s)
    return s


def _bbox_overlap(a: tuple[float, float, float, float], b: tuple[float, float, float, float]) -> float:
    ax0, atop, ax1, abot = a
    bx0, btop, bx1, bbot = b
    ix0 = max(ax0, bx0)
    itop = max(atop, btop)
    ix1 = min(ax1, bx1)
    ibot = min(abot, bbot)
    if ix1 <= ix0 or ibot <= itop:
        return 0.0
    inter = (ix1 - ix0) * (ibot - itop)
    a_area = max((ax1 - ax0) * (abot - atop), 1.0)
    return inter / a_area


def _word_in_bbox(word: dict[str, Any], bbox: tuple[float, float, float, float]) -> bool:
    wb = (float(word['x0']), float(word['top']), float(word['x1']), float(word['bottom']))
    return _bbox_overlap(wb, bbox) > 0.5


def _normalize_extracted_text(text: str) -> str:
    # Some PDFs duplicate CJK glyph runs in extraction (e.g., "アアアアパパパパ...").
    if not text:
        return text
    out: list[str] = []
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        j = i + 1
        while j < n and text[j] == ch:
            j += 1
        run_len = j - i
        # Common extraction artifact: characters repeated 3-4+ times
        # ("UUUUnnnniiiitttt", duplicated CJK glyphs, etc.).
        # Collapse aggressive runs to a single glyph.
        if run_len >= 3 and not ch.isspace():
            out.append(ch)
        elif run_len == 2 and ord(ch) > 127:
            # For non-ASCII scripts, even double runs are often duplication artifacts.
            out.append(ch)
        else:
            out.append(ch * run_len)
        i = j
    normalized = ''.join(out)
    normalized = re.sub(r'\s{2,}', ' ', normalized).strip()
    normalized = _normalize_leading_list_marker(normalized)
    normalized = _normalize_ocr_english_artifacts(normalized)
    return normalized


def _group_words_to_lines(words: list[dict[str, Any]], y_tol: float = 3.0) -> list[tuple[float, str]]:
    if not words:
        return []
    ordered = sorted(words, key=lambda w: (float(w['top']), float(w['x0'])))
    lines: list[list[dict[str, Any]]] = []
    current: list[dict[str, Any]] = []
    baseline = float(ordered[0]['top'])
    for w in ordered:
        top = float(w['top'])
        if current and abs(top - baseline) > y_tol:
            lines.append(current)
            current = [w]
            baseline = top
        else:
            current.append(w)
            baseline = (baseline + top) / 2.0
    if current:
        lines.append(current)

    out: list[tuple[float, str]] = []
    for group in lines:
        group = sorted(group, key=lambda w: float(w['x0']))
        text = ' '.join((w.get('text') or '').strip() for w in group if (w.get('text') or '').strip())
        text = _normalize_extracted_text(text)
        if not text:
            continue
        top = min(float(w['top']) for w in group)
        out.append((top, text))
    return out


def _rows_to_markdown_table(rows: list[list[str | None]]) -> str | None:
    clean_rows: list[list[str]] = []
    max_cols = 0
    for row in rows:
        if row is None:
            continue
        vals = [_normalize_extracted_text((cell or '').replace('\n', ' ').strip()) for cell in row]
        if not any(vals):
            continue
        max_cols = max(max_cols, len(vals))
        clean_rows.append(vals)
    if not clean_rows or max_cols < 2:
        return None
    padded = [r + [''] * (max_cols - len(r)) for r in clean_rows]
    header = padded[0]
    if not any(h.strip() for h in header):
        header = [f'col{idx + 1}' for idx in range(max_cols)]
        data_rows = padded
    else:
        data_rows = padded[1:] if len(padded) > 1 else []

    header_line = '| ' + ' | '.join(header) + ' |'
    sep_line = '| ' + ' | '.join(['---'] * max_cols) + ' |'
    lines = [header_line, sep_line]
    for row in data_rows:
        lines.append('| ' + ' | '.join(row) + ' |')
    return '\n'.join(lines)


def extract_structured_pages(input_pdf: Path) -> list[str] | None:
    try:
        import pdfplumber  # type: ignore
    except Exception:
        return None

    pages_out: list[str] = []
    with pdfplumber.open(str(input_pdf)) as pdf:
        for page_no, page in enumerate(pdf.pages, start=1):
            words = page.extract_words(
                x_tolerance=2,
                y_tolerance=2,
                keep_blank_chars=False,
                use_text_flow=False,
            ) or []

            blocks: list[tuple[float, str]] = []
            masked_bboxes: list[tuple[float, float, float, float]] = []

            # Tables first: they are the most structured and should survive conversion.
            try:
                tables = page.find_tables() or []
            except Exception:
                tables = []
            for t_idx, table in enumerate(tables, start=1):
                bbox = (float(table.bbox[0]), float(table.bbox[1]), float(table.bbox[2]), float(table.bbox[3]))
                md_table = _rows_to_markdown_table(table.extract())
                if md_table:
                    blocks.append((bbox[1], f'[[TABLE:page-{page_no:03d}-table-{t_idx:03d}]]\n{md_table}'))
                else:
                    blocks.append(
                        (
                            bbox[1],
                            (
                                f'[[TABLE:page-{page_no:03d}-table-{t_idx:03d}|'
                                f'bbox={bbox[0]:.1f},{bbox[1]:.1f},{bbox[2]:.1f},{bbox[3]:.1f}]]'
                            ),
                        )
                    )
                masked_bboxes.append(bbox)

            # Textboxes: detect larger rectangles carrying text that are not table regions.
            rects = page.rects or []
            textbox_count = 0
            shape_count = 0
            for rect in rects:
                bbox = (
                    float(rect.get('x0', 0.0)),
                    float(rect.get('top', 0.0)),
                    float(rect.get('x1', 0.0)),
                    float(rect.get('bottom', 0.0)),
                )
                w = bbox[2] - bbox[0]
                h = bbox[3] - bbox[1]
                if w < 80 or h < 25:
                    continue
                if any(_bbox_overlap(bbox, tb) > 0.3 for tb in masked_bboxes):
                    continue
                in_box = [wd for wd in words if _word_in_bbox(wd, bbox)]
                line_tuples = _group_words_to_lines(in_box)
                if len(line_tuples) < 2:
                    continue
                textbox_count += 1
                text_lines = [f'> {line}' for _, line in line_tuples]
                marker = f'[[TEXTBOX:page-{page_no:03d}-box-{textbox_count:03d}]]'
                blocks.append((bbox[1], marker + '\n' + '\n'.join(text_lines)))
                masked_bboxes.append(bbox)

            # Shapes: non-table, non-text larger vector rectangles.
            for rect in rects:
                bbox = (
                    float(rect.get('x0', 0.0)),
                    float(rect.get('top', 0.0)),
                    float(rect.get('x1', 0.0)),
                    float(rect.get('bottom', 0.0)),
                )
                w = bbox[2] - bbox[0]
                h = bbox[3] - bbox[1]
                area = w * h
                if area < 12000:
                    continue
                if any(_bbox_overlap(bbox, bb) > 0.3 for bb in masked_bboxes):
                    continue
                in_box = [wd for wd in words if _word_in_bbox(wd, bbox)]
                if in_box:
                    continue
                shape_count += 1
                marker = (
                    f'[[SHAPE:page-{page_no:03d}-shape-{shape_count:03d}|'
                    f'bbox={bbox[0]:.1f},{bbox[1]:.1f},{bbox[2]:.1f},{bbox[3]:.1f}]]'
                )
                blocks.append((bbox[1], marker))
                masked_bboxes.append(bbox)

            curves = page.curves or []
            for curve in curves:
                bbox = (
                    float(curve.get('x0', 0.0)),
                    float(curve.get('top', 0.0)),
                    float(curve.get('x1', 0.0)),
                    float(curve.get('bottom', 0.0)),
                )
                w = bbox[2] - bbox[0]
                h = bbox[3] - bbox[1]
                area = w * h
                if area < 20000:
                    continue
                if any(_bbox_overlap(bbox, bb) > 0.3 for bb in masked_bboxes):
                    continue
                in_curve = [wd for wd in words if _word_in_bbox(wd, bbox)]
                if in_curve:
                    continue
                shape_count += 1
                marker = (
                    f'[[SHAPE:page-{page_no:03d}-shape-{shape_count:03d}|'
                    f'bbox={bbox[0]:.1f},{bbox[1]:.1f},{bbox[2]:.1f},{bbox[3]:.1f}]]'
                )
                blocks.append((bbox[1], marker))
                masked_bboxes.append(bbox)

            plain_words = [
                wd for wd in words if not any(_word_in_bbox(wd, bb) for bb in masked_bboxes)
            ]
            for top, line in _group_words_to_lines(plain_words):
                blocks.append((top, line))

            blocks.sort(key=lambda x: x[0])
            page_lines = [blk for _, blk in blocks if blk.strip()]
            pages_out.append('\n\n'.join(page_lines).strip())

    return pages_out


def check_binary(name: str, install_url: str) -> None:
    if shutil.which(name) is None:
        print(f'Error: {name} binary not found on PATH. Install from {install_url}')
        sys.exit(2)


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


def _list_pdfimages(input_pdf: Path) -> list[dict[str, int]]:
    cmd = ['pdfimages', '-list', str(input_pdf)]
    out = subprocess.run(cmd, check=True, capture_output=True, text=True).stdout
    rows: list[dict[str, int]] = []
    # Columns are stable enough for page/width/height/x-ppi/y-ppi parsing.
    # Example prefix: page num type width height ... object ID x-ppi y-ppi ...
    pattern = re.compile(
        r'^\s*(\d+)\s+\d+\s+\S+\s+(\d+)\s+(\d+)\s+\S+\s+\d+\s+\d+\s+\S+\s+\S+\s+\d+\s+\d+\s+(\d+)\s+(\d+)'
    )
    for line in out.splitlines():
        m = pattern.match(line)
        if not m:
            continue
        rows.append(
            {
                'page': int(m.group(1)),
                'width_px': int(m.group(2)),
                'height_px': int(m.group(3)),
                'x_ppi': int(m.group(4)),
                'y_ppi': int(m.group(5)),
            }
        )
    return rows


def run_pdfimages(input_pdf: Path, assets_dir: Path, prefix: str) -> list[PdfImageAsset]:
    check_binary('pdfimages', 'https://poppler.freedesktop.org/')
    assets_dir.mkdir(parents=True, exist_ok=True)
    listed = _list_pdfimages(input_pdf)
    output_prefix = assets_dir / prefix
    cmd = [
        'pdfimages',
        '-all',
        str(input_pdf),
        str(output_prefix),
    ]
    print('Running:', ' '.join(cmd))
    subprocess.run(cmd, check=True)
    extracted = sorted(
        [p for p in assets_dir.glob(f'{prefix}*') if p.is_file()],
        key=lambda p: p.name,
    )

    assets: list[PdfImageAsset] = []
    for idx, path in enumerate(extracted):
        meta = listed[idx] if idx < len(listed) else {}
        assets.append(
            PdfImageAsset(
                path=path,
                page=meta.get('page'),
                width_px=meta.get('width_px'),
                height_px=meta.get('height_px'),
                x_ppi=meta.get('x_ppi'),
                y_ppi=meta.get('y_ppi'),
            )
        )
    return assets


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
    pages = sorted(output_dir.glob(f'{prefix}-*.png'))
    print(f'Rendered pages: {len(pages)}')
    return pages


def _asset_ref_html(asset: PdfImageAsset, assets_rel: Path) -> str:
    rel_path = (assets_rel / asset.path.name).as_posix()
    if asset.width_px and asset.height_px and asset.x_ppi and asset.y_ppi:
        w_in = asset.width_px / max(asset.x_ppi, 1)
        h_in = asset.height_px / max(asset.y_ppi, 1)
        return f'<img src="{rel_path}" style="width:{w_in:.5f}in;height:{h_in:.5f}in" />**  **'
    return f'<img src="{rel_path}" />**  **'


def build_markdown(
    text: str,
    image_assets: list[PdfImageAsset],
    assets_rel: Path,
    include_asset_markers: bool = True,
) -> str:
    pages = text.split('\f')
    return build_markdown_from_pages(pages, image_assets, assets_rel, include_asset_markers)


def build_markdown_from_pages(
    pages: list[str],
    image_assets: list[PdfImageAsset],
    assets_rel: Path,
    include_asset_markers: bool = True,
) -> str:
    lines: list[str] = []
    assets_by_page: dict[int, list[PdfImageAsset]] = {}
    unpaged_assets: list[PdfImageAsset] = []
    for asset in image_assets:
        if asset.page and asset.page > 0:
            assets_by_page.setdefault(asset.page, []).append(asset)
        else:
            unpaged_assets.append(asset)

    footer_re = re.compile(r'^[\-\u2010-\u2015\u2212\u30fc\uff0d]?\d+[\-\u2010-\u2015\u2212\u30fc\uff0d]?$')

    for page_idx, page_text in enumerate(pages, start=1):
        page_text = page_text.strip()
        page_lines = page_text.splitlines() if page_text else []
        asset_lines: list[str] = []
        for asset in assets_by_page.get(page_idx, []):
            if include_asset_markers:
                rel_path = (assets_rel / asset.path.name).as_posix()
                asset_lines.append(f'[[ASSET:{rel_path}]]')
            asset_lines.append(_asset_ref_html(asset, assets_rel))

        if page_lines:
            # Prefer inserting assets before a trailing page-number/footer line
            # such as "-8-" / "- 8 -", which should remain the last text item.
            footer_idx = -1
            scan_start = max(0, len(page_lines) - 12)
            for idx in range(len(page_lines) - 1, scan_start - 1, -1):
                normalized = re.sub(r'\s+', '', page_lines[idx].strip())
                if footer_re.match(normalized):
                    footer_idx = idx
                    break

            if asset_lines and footer_idx >= 0:
                before = page_lines[:footer_idx]
                footer_and_after = page_lines[footer_idx:]
                merged = before + [''] + asset_lines + [''] + footer_and_after
                lines.append('\n'.join(merged).strip())
            elif asset_lines:
                merged = page_lines + [''] + asset_lines
                lines.append('\n'.join(merged).strip())
            else:
                lines.append('\n'.join(page_lines).strip())
        elif asset_lines:
            lines.extend(asset_lines)

        if page_idx < len(pages):
            lines.append('')
            lines.append('[[PAGEBREAK]]')
            lines.append('')

    # Keep any unmatched assets referenced in the file (but not in a separate appendix block).
    if unpaged_assets:
        if lines and lines[-1] != '':
            lines.append('')
        for asset in unpaged_assets:
            if include_asset_markers:
                rel_path = (assets_rel / asset.path.name).as_posix()
                lines.append(f'[[ASSET:{rel_path}]]')
            lines.append(_asset_ref_html(asset, assets_rel))

    return '\n'.join(lines).strip() + '\n'


def analyze_text_quality(text: str) -> dict[str, float | int]:
    nonspace_chars = [ch for ch in text if not ch.isspace()]
    nonspace_count = len(nonspace_chars)
    if nonspace_count == 0:
        return {
            'nonspace_count': 0,
            'garble_ratio': 1.0,
            'japanese_ratio': 0.0,
            'mojibake_hits': 0,
        }

    japanese_count = 0
    mojibake_hits = 0
    mojibake_patterns = (
        '\u7e3a',  # "縺"
        '\u7e67',  # "繧"
        '\u7e5d',  # "繝"
        '\u873f',  # "蜿"
        '\uff7f',  # half-width katakana fragment often seen in mojibake
        '\ufffd',  # replacement character
        '縺',  # common mojibake lead glyph in JP text
        '繧',
        '繝',
        '縲',
        '荳',
        '螟',
        '譁',
        '隧',
    )
    for ch in nonspace_chars:
        code = ord(ch)
        if (
            0x3040 <= code <= 0x30FF  # Hiragana/Katakana
            or 0x4E00 <= code <= 0x9FFF  # CJK unified ideographs
            or 0x3400 <= code <= 0x4DBF  # CJK extension A
        ):
            japanese_count += 1
    for pat in mojibake_patterns:
        mojibake_hits += text.count(pat)

    replacement_char_count = text.count('\ufffd')
    suspicious = mojibake_hits + replacement_char_count
    garble_ratio = suspicious / max(nonspace_count, 1)

    return {
        'nonspace_count': nonspace_count,
        'garble_ratio': garble_ratio,
        'japanese_ratio': japanese_count / max(nonspace_count, 1),
        'mojibake_hits': mojibake_hits,
    }


def should_fallback_to_ocr(
    metrics: dict[str, float | int],
    min_nonspace_chars: int,
    max_garble_ratio: float,
    min_japanese_ratio: float,
    expect_japanese: bool,
) -> tuple[bool, list[str]]:
    reasons: list[str] = []

    nonspace_count = int(metrics['nonspace_count'])
    garble_ratio = float(metrics['garble_ratio'])
    japanese_ratio = float(metrics['japanese_ratio'])

    if nonspace_count < min_nonspace_chars:
        reasons.append(f'low text density ({nonspace_count} < {min_nonspace_chars})')
    if garble_ratio > max_garble_ratio:
        reasons.append(f'high garble ratio ({garble_ratio:.4f} > {max_garble_ratio:.4f})')
    if expect_japanese and japanese_ratio < min_japanese_ratio:
        reasons.append(f'low Japanese ratio ({japanese_ratio:.4f} < {min_japanese_ratio:.4f})')

    return (len(reasons) > 0), reasons


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
        '--ocr-psm',
        type=int,
        default=3,
        help='Tesseract page segmentation mode (default: 3).',
    )
    parser.add_argument(
        '--ocr-mode',
        choices=['auto', 'always', 'never'],
        default='auto',
        help='OCR mode: auto (quality-gated fallback), always, never.',
    )
    parser.add_argument(
        '--layout-mode',
        choices=['auto', 'structured', 'plain'],
        default='auto',
        help='Layout reconstruction mode: auto, structured (table/textbox recovery), or plain.',
    )
    parser.add_argument(
        '--no-ocr',
        action='store_true',
        help='Legacy alias for "--ocr-mode never".',
    )
    parser.add_argument(
        '--fallback-min-nonspace-chars',
        type=int,
        default=800,
        help='In auto mode, fallback to OCR when extracted non-space chars are below this threshold.',
    )
    parser.add_argument(
        '--fallback-max-garble-ratio',
        type=float,
        default=0.015,
        help='In auto mode, fallback to OCR when garble ratio is above this threshold.',
    )
    parser.add_argument(
        '--fallback-min-japanese-ratio',
        type=float,
        default=0.01,
        help='In auto mode, fallback to OCR when Japanese ratio is below this threshold (when Japanese is expected).',
    )
    parser.add_argument(
        '--no-asset-markers',
        action='store_true',
        help='Disable explicit [[ASSET:...]] marker lines next to inline image references.',
    )
    parser.add_argument(
        '--no-local-staging',
        action='store_true',
        help='Disable default behavior that stages conversion in a local temp folder before syncing outputs.',
    )
    args = parser.parse_args()

    ocr_mode = args.ocr_mode
    if args.no_ocr:
        ocr_mode = 'never'

    source_input_path = Path(args.input).expanduser().resolve()
    if not source_input_path.exists():
        print(f'Error: input PDF not found: {source_input_path}')
        sys.exit(1)

    base_dir = source_input_path.parent
    output_dir = Path(args.output_dir).expanduser().resolve() if args.output_dir else (base_dir / 'out').resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    assets_arg = Path(args.assets_dir)
    assets_dir = assets_arg if assets_arg.is_absolute() else (output_dir / assets_arg)
    assets_dir.mkdir(parents=True, exist_ok=True)

    output_md = Path(args.output) if args.output else (output_dir / f'{source_input_path.stem}.md')
    output_md.parent.mkdir(parents=True, exist_ok=True)

    staging_ctx: tempfile.TemporaryDirectory[str] | None = None
    run_input_path = source_input_path
    run_output_dir = output_dir
    run_assets_dir = assets_dir
    run_output_md = output_md
    if not args.no_local_staging:
        staging_ctx = tempfile.TemporaryDirectory(prefix='textmaker-pdf-')
        staging_root = Path(staging_ctx.name)
        run_input_path = stage_input_file(source_input_path, staging_root / 'input')
        run_output_dir = staging_root / 'out'
        run_output_dir.mkdir(parents=True, exist_ok=True)
        run_assets_dir = (run_output_dir / assets_arg) if not assets_arg.is_absolute() else (staging_root / 'assets')
        run_assets_dir.mkdir(parents=True, exist_ok=True)
        run_output_md = run_output_dir / output_md.name
        print(f'Local staging enabled: {run_input_path}')

    extracted_images = run_pdfimages(run_input_path, run_assets_dir, prefix='image')

    text = ''
    text_source = 'pdftotext'
    structured_pages: list[str] | None = None
    expect_japanese = bool(re.search(r'(^|[+])jpn([+]|$)', args.ocr_lang))

    if ocr_mode == 'always':
        check_tesseract()
        page_images = run_pdftoppm(run_input_path, run_output_dir / '_pages', prefix='page')
        text = run_tesseract_many(
            page_images,
            args.ocr_lang,
            psm=args.ocr_psm,
            extra_configs=['preserve_interword_spaces=1'],
        )
        text_source = 'ocr'
    else:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_txt = Path(tmpdir) / f'{source_input_path.stem}.txt'
            run_pdftotext(run_input_path, tmp_txt)
            text = tmp_txt.read_text(encoding='utf-8')

        if ocr_mode == 'auto':
            metrics = analyze_text_quality(text)
            should_fallback, reasons = should_fallback_to_ocr(
                metrics,
                min_nonspace_chars=args.fallback_min_nonspace_chars,
                max_garble_ratio=args.fallback_max_garble_ratio,
                min_japanese_ratio=args.fallback_min_japanese_ratio,
                expect_japanese=expect_japanese,
            )
            print(
                'Text quality:',
                f"nonspace={int(metrics['nonspace_count'])}",
                f"garble_ratio={float(metrics['garble_ratio']):.4f}",
                f"japanese_ratio={float(metrics['japanese_ratio']):.4f}",
                f"mojibake_hits={int(metrics['mojibake_hits'])}",
            )
            if should_fallback:
                if tesseract_available():
                    print('Auto OCR fallback triggered:', '; '.join(reasons))
                    page_images = run_pdftoppm(run_input_path, run_output_dir / '_pages', prefix='page')

                    extracted_pages = text.split('\f')
                    if len(extracted_pages) < len(page_images):
                        extracted_pages.extend([''] * (len(page_images) - len(extracted_pages)))
                    elif len(extracted_pages) > len(page_images):
                        extracted_pages = extracted_pages[: len(page_images)]

                    fallback_pages: list[int] = []
                    for idx, page_text in enumerate(extracted_pages, start=1):
                        page_metrics = analyze_text_quality(page_text)
                        page_should_fallback, _ = should_fallback_to_ocr(
                            page_metrics,
                            min_nonspace_chars=max(120, args.fallback_min_nonspace_chars // 4),
                            max_garble_ratio=args.fallback_max_garble_ratio,
                            min_japanese_ratio=args.fallback_min_japanese_ratio,
                            expect_japanese=expect_japanese,
                        )
                        if page_should_fallback:
                            fallback_pages.append(idx)

                    if fallback_pages:
                        print(
                            f'Auto OCR per-page fallback: {len(fallback_pages)}/{len(page_images)} pages '
                            f'({", ".join(str(p) for p in fallback_pages[:12])}'
                            f'{"..." if len(fallback_pages) > 12 else ""})'
                        )
                        for page_idx in fallback_pages:
                            print(f'Running OCR page replacement: {page_idx}/{len(page_images)}')
                            extracted_pages[page_idx - 1] = run_tesseract(
                                page_images[page_idx - 1],
                                args.ocr_lang,
                                psm=args.ocr_psm,
                                extra_configs=['preserve_interword_spaces=1'],
                            ).strip()
                        text = '\f\n'.join(extracted_pages)
                        text_source = 'mixed'
                    else:
                        print('Auto OCR fallback requested, but page-level quality looked acceptable; keeping pdftotext output.')
                else:
                    print('Auto OCR fallback requested but Tesseract is unavailable; using pdftotext output.')
                    print('Fallback reasons:', '; '.join(reasons))

    if args.layout_mode in {'auto', 'structured'}:
        structured_pages = extract_structured_pages(run_input_path)
        if structured_pages is None and args.layout_mode == 'structured':
            print('Structured layout mode requested, but pdfplumber is unavailable; using plain layout text.')

    assets_rel = Path('.') if assets_dir == output_md.parent else Path(
        os.path.relpath(assets_dir, output_md.parent)
    )
    if structured_pages:
        markdown = build_markdown_from_pages(
            structured_pages,
            extracted_images,
            assets_rel,
            include_asset_markers=not args.no_asset_markers,
        )
        print('Layout source: structured')
    else:
        markdown = build_markdown(
            text,
            extracted_images,
            assets_rel,
            include_asset_markers=not args.no_asset_markers,
        )
        print('Layout source: plain')
    run_output_md.write_text(markdown, encoding='utf-8')
    if staging_ctx is not None:
        sync_dir(run_assets_dir, assets_dir)
        sync_file(run_output_md, output_md)
        staging_ctx.cleanup()
    else:
        output_md = run_output_md
    print('Text source:', text_source)
    print('Wrote', output_md)


if __name__ == '__main__':
    main()
