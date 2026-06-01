"""
PDF → Markdown converter with asset extraction and optional OCR.

- Extracts embedded images via pdfimages.
- Extracts text via pdftotext (default) or runs Tesseract OCR on page renders.
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
from typing import Any, cast

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


def _strip_speaker_accent_tag(text: str) -> str:
    s = text.rstrip()
    # Drop standalone speaker-accent hint lines.
    if re.fullmatch(r'[米英加豪]\s*', s):
        return ''
    # Drop leading speaker-accent hint prefix (e.g. "米       (A) ...", "英 W: ...").
    s = re.sub(r'^[米英加豪]\s{2,}', '', s)
    s = re.sub(r'^[米英加豪]\s+(?=[A-Za-z][A-Za-z0-9]{0,3}\s*:)', '', s)
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


def _normalize_extracted_text(text: str, normalize_list_markers: bool = True) -> str:
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
    if normalize_list_markers:
        normalized = _normalize_leading_list_marker(normalized)
    normalized = _normalize_ocr_english_artifacts(normalized)
    normalized = _strip_speaker_accent_tag(normalized)
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


def _shape_text_lines(words_in_shape: list[dict[str, Any]]) -> list[str]:
    lines = [line for _, line in _group_words_to_lines(words_in_shape)]
    return [ln for ln in lines if ln.strip()]


def _rows_to_markdown_table(rows: list[list[str | None]]) -> str | None:
    clean_rows: list[list[str]] = []
    max_cols = 0
    for row in rows:
        if row is None:
            continue
        vals = [
            _normalize_extracted_text((cell or '').replace('\n', ' ').strip(), normalize_list_markers=False)
            for cell in row
        ]
        # In table cells, leading "(1)" style often indicates item counters,
        # not parenthesized list markers.
        vals = [re.sub(r'^\((\d+)\)\s+', r'\1 ', v) for v in vals]
        if not any(vals):
            continue
        max_cols = max(max_cols, len(vals))
        clean_rows.append(vals)
    if not clean_rows or max_cols < 2:
        return None
    # Reject low-quality detections that are mostly prose, not tabular cells.
    nonempty_counts = [sum(1 for v in r if v.strip()) for r in clean_rows]
    rows_with_two_or_more = sum(1 for c in nonempty_counts if c >= 2)
    if rows_with_two_or_more < 2:
        return None
    if rows_with_two_or_more / max(len(clean_rows), 1) < 0.6:
        return None
    max_cell_len = max((len(v) for r in clean_rows for v in r), default=0)
    if max_cell_len > 180:
        return None
    # Reject prose-heavy captures where many cells look like long sentences.
    nonempty_cells = [v for r in clean_rows for v in r if v.strip()]
    if nonempty_cells:
        long_cells = sum(1 for v in nonempty_cells if len(v) >= 70)
        sentence_like = sum(1 for v in nonempty_cells if re.search(r'[。\.?!]$', v))
        if long_cells / len(nonempty_cells) > 0.25:
            return None
        if sentence_like / len(nonempty_cells) > 0.45:
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


def extract_structured_pages(
    input_pdf: Path,
    include_plain_words: bool = True,
    return_blocks: bool = False,
) -> list[str] | list[tuple[float, list[tuple[float, str]]]] | None:
    try:
        import pdfplumber  # type: ignore
    except Exception:
        return None

    pages_out: list[str] = []
    blocks_out: list[tuple[float, list[tuple[float, str]]]] = []
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
                bw = bbox[2] - bbox[0]
                bh = bbox[3] - bbox[1]
                if bw < 120 or bh < 25:
                    continue
                md_table = _rows_to_markdown_table(table.extract())
                if md_table:
                    blocks.append((bbox[1], f'[[TABLE:page-{page_no:03d}-table-{t_idx:03d}]]\n{md_table}'))
                else:
                    # Emit fallback table marker only for substantial regions.
                    if bw < 220 or bh < 80:
                        continue
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
                if any(_bbox_overlap(bbox, bb) > 0.3 for bb in masked_bboxes):
                    continue
                in_box = [wd for wd in words if _word_in_bbox(wd, bbox)]
                text_lines = _shape_text_lines(in_box) if in_box else []
                # Keep large shape regions by default; also keep smaller shapes when
                # they include short text labels (e.g., audio track tags).
                if area < 12000 and not (text_lines and area >= 1500):
                    continue
                shape_count += 1
                marker = (
                    f'[[SHAPE:page-{page_no:03d}-shape-{shape_count:03d}|'
                    f'bbox={bbox[0]:.1f},{bbox[1]:.1f},{bbox[2]:.1f},{bbox[3]:.1f}]]'
                )
                if text_lines:
                    shape_block = marker + '\n' + '\n'.join(f'> {line}' for line in text_lines)
                else:
                    shape_block = marker
                blocks.append((bbox[1], shape_block))
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
                if any(_bbox_overlap(bbox, bb) > 0.3 for bb in masked_bboxes):
                    continue
                in_curve = [wd for wd in words if _word_in_bbox(wd, bbox)]
                curve_text_lines = _shape_text_lines(in_curve) if in_curve else []
                if area < 20000 and not (curve_text_lines and area >= 3000):
                    continue
                shape_count += 1
                marker = (
                    f'[[SHAPE:page-{page_no:03d}-shape-{shape_count:03d}|'
                    f'bbox={bbox[0]:.1f},{bbox[1]:.1f},{bbox[2]:.1f},{bbox[3]:.1f}]]'
                )
                if curve_text_lines:
                    shape_block = marker + '\n' + '\n'.join(f'> {line}' for line in curve_text_lines)
                else:
                    shape_block = marker
                blocks.append((bbox[1], shape_block))
                masked_bboxes.append(bbox)

            if include_plain_words:
                plain_words = [
                    wd for wd in words if not any(_word_in_bbox(wd, bb) for bb in masked_bboxes)
                ]
                for top, line in _group_words_to_lines(plain_words):
                    blocks.append((top, line))

            blocks.sort(key=lambda x: x[0])
            page_lines = [blk for _, blk in blocks if blk.strip()]
            if return_blocks:
                blocks_out.append((float(page.height), [(float(top), blk) for top, blk in blocks if blk.strip()]))
            else:
                pages_out.append('\n'.join(page_lines).strip())

    if return_blocks:
        return blocks_out
    return pages_out


def _merge_marker_blocks_into_plain_page(
    plain_page_text: str,
    page_height: float,
    marker_blocks: list[tuple[float, str]],
) -> str:
    def _match_key(s: str) -> str:
        s = s.strip()
        # Keep letters/digits/CJK; strip spaces and punctuation for fuzzy matching.
        return re.sub(r'[\W_]+', '', s, flags=re.UNICODE)

    def _extract_textbox_lines(block: str) -> list[str]:
        lines = block.splitlines()
        if not lines or not lines[0].startswith('[[TEXTBOX:'):
            return []
        out: list[str] = []
        for ln in lines[1:]:
            t = ln.strip()
            if t.startswith('>'):
                t = t[1:].strip()
            if t:
                out.append(t)
        return out

    def _extract_table_keys(block: str) -> list[str]:
        lines = block.splitlines()
        if not lines or not lines[0].startswith('[[TABLE:'):
            return []
        keys: list[str] = []
        for ln in lines[1:]:
            s = ln.strip()
            if '|' not in s:
                continue
            # Skip markdown separator rows.
            if re.match(r'^\|\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?$', s):
                continue
            parts = [p.strip() for p in s.strip('|').split('|')]
            for p in parts:
                k = _match_key(p)
                if len(k) >= 2:
                    keys.append(k)
        return keys

    def _find_table_anchor_idx(
        lines: list[str],
        table_keys: list[str],
        target_idx: int,
    ) -> int | None:
        if not table_keys or not lines:
            return None
        all_key = ''.join(table_keys)
        # Use the strongest/longest keys first for anchoring.
        strong_keys = sorted({k for k in table_keys if len(k) >= 4}, key=len, reverse=True)[:8]
        if not strong_keys:
            return None

        candidates: list[int] = []
        for idx, ln in enumerate(lines):
            s = ln.strip()
            if not s or s.startswith('[[') or s.startswith('|'):
                continue
            k = _match_key(s)
            if len(k) < 4:
                continue
            hit = False
            for tk in strong_keys:
                if tk in k or k in tk:
                    hit = True
                    break
            if not hit and len(k) >= 8:
                if (k in all_key) or (all_key.find(k[: min(16, len(k))]) >= 0):
                    hit = True
            if hit:
                candidates.append(idx)
        if not candidates:
            return None
        return min(candidates, key=lambda x: abs(x - target_idx))

    def _find_textbox_span(
        lines: list[str],
        textbox_lines: list[str],
        target_idx: int,
    ) -> tuple[int, int] | None:
        if not textbox_lines:
            return None
        keys = [_match_key(ln) for ln in textbox_lines if _match_key(ln)]
        if not keys:
            return None
        first_key = keys[0]
        anchor = first_key[: max(8, min(24, len(first_key)))]
        candidates: list[int] = []
        for i, ln in enumerate(lines):
            ln_key = _match_key(ln)
            if ln_key and (anchor in ln_key or ln_key in anchor):
                candidates.append(i)
        if not candidates:
            return None
        start = min(candidates, key=lambda x: abs(x - target_idx))

        all_key = _match_key(''.join(textbox_lines))
        end = start
        max_scan = min(len(lines), start + 24)
        while end < max_scan:
            k = _match_key(lines[end])
            if not k:
                end += 1
                continue
            # Keep consuming while the line plausibly belongs to textbox text.
            if (k in all_key) or (all_key.find(k[: max(6, min(18, len(k)))]) >= 0):
                end += 1
                continue
            break
        if end <= start:
            end = start + 1
        return (start, end)

    def _remove_textbox_duplicate_lines(
        lines: list[str],
        textbox_lines: list[str],
        protected_span: tuple[int, int] | None = None,
    ) -> list[str]:
        keys = [_match_key(ln) for ln in textbox_lines if _match_key(ln)]
        long_keys = [k for k in keys if len(k) >= 8]
        if not long_keys:
            return lines
        all_key = _match_key(''.join(textbox_lines))
        out: list[str] = []
        for idx, ln in enumerate(lines):
            if protected_span is not None and protected_span[0] <= idx < protected_span[1]:
                out.append(ln)
                continue
            k = _match_key(ln)
            if not k:
                out.append(ln)
                continue
            hit = False
            for tk in long_keys:
                if tk in k or k in tk:
                    hit = True
                    break
            if not hit and len(k) >= 8:
                if (k in all_key) or (all_key.find(k[: max(8, min(16, len(k)))]) >= 0):
                    hit = True
            if hit:
                continue
            out.append(ln)
        return out

    def _remove_table_duplicate_lines(
        lines: list[str],
        table_keys: list[str],
        target_idx: int,
        window_before: int = 20,
        window_after: int = 45,
    ) -> list[str]:
        if not table_keys:
            return lines
        all_key = ''.join(table_keys)
        lo = max(0, target_idx - window_before)
        hi = min(len(lines), target_idx + window_after)
        out: list[str] = []
        for idx, ln in enumerate(lines):
            if idx < lo or idx >= hi:
                out.append(ln)
                continue
            s = ln.strip()
            if not s:
                out.append(ln)
                continue
            # Don't touch actual markdown table markup.
            if s.startswith('|') or s.startswith('[[TABLE:'):
                out.append(ln)
                continue
            # Keep answer-option and question numbering lines.
            if re.match(r'^\([A-Za-z]\)\s+', s) or re.match(r'^\d+\.\s+\([A-Za-z]\)', s):
                out.append(ln)
                continue

            k = _match_key(s)
            if len(k) < 4:
                out.append(ln)
                continue

            hit = False
            if len(k) >= 8 and (k in all_key or all_key.find(k[: min(16, len(k))]) >= 0):
                hit = True
            if not hit:
                token_hits = 0
                for tk in table_keys:
                    if len(tk) < 3:
                        continue
                    if tk in k or k in tk:
                        token_hits += 1
                    if token_hits >= 2:
                        hit = True
                        break

            if hit:
                continue
            out.append(ln)
        return out

    plain_lines = _merge_soft_wrapped_lines(plain_page_text.splitlines()) if plain_page_text else []
    # Preserve section/list separation while preventing runaway vertical gaps.
    collapsed_lines: list[str] = []
    blank_run = 0
    for ln in plain_lines:
        t = ln.rstrip()
        if t.strip():
            blank_run = 0
            collapsed_lines.append(t)
        else:
            blank_run += 1
            if blank_run <= 1:
                collapsed_lines.append('')
    plain_lines = collapsed_lines
    if not marker_blocks:
        return '\n'.join(plain_lines).strip()
    if not plain_lines:
        marker_only = [blk for _, blk in sorted(marker_blocks, key=lambda x: x[0]) if blk.strip()]
        return '\n'.join(marker_only).strip()

    lines_work = list(plain_lines)
    fallback_markers: list[tuple[float, str]] = []
    h = max(page_height, 1.0)
    # First pass: textbox markers try content-anchored replacement to avoid
    # duplicate raw text blocks and misplaced insertion.
    for top, marker in sorted(marker_blocks, key=lambda x: x[0]):
        textbox_lines = _extract_textbox_lines(marker)
        if textbox_lines:
            expected_idx = int((max(top, 0.0) / h) * max(len(lines_work), 1))
            span = _find_textbox_span(lines_work, textbox_lines, target_idx=expected_idx)
            if span is not None:
                start, end = span
                del lines_work[start:end]
                lines_work[start:start] = [marker, '']
                lines_work = _remove_textbox_duplicate_lines(
                    lines_work,
                    textbox_lines,
                    protected_span=(start, start + 2),
                )
                continue
        table_keys = _extract_table_keys(marker)
        if table_keys:
            expected_idx = int((max(top, 0.0) / h) * max(len(lines_work), 1))
            anchor_idx = _find_table_anchor_idx(lines_work, table_keys, expected_idx)
            if anchor_idx is None:
                lines_work = _remove_table_duplicate_lines(lines_work, table_keys, expected_idx)
                fallback_markers.append((top, marker))
                continue

            # Remove nearby flattened table residue, then insert at anchor.
            lines_work = _remove_table_duplicate_lines(
                lines_work,
                table_keys,
                anchor_idx,
                window_before=14,
                window_after=38,
            )
            insert_at = max(0, min(anchor_idx, len(lines_work)))
            # If anchor lands inside an option/list block, place marker
            # at the start of that block (not mid-list).
            def _is_option_or_list_line_local(s: str) -> bool:
                t = s.strip()
                return bool(
                    re.match(r'^\([A-Za-z]\)\s+', t)
                    or re.match(r'^\d+\.\s+\([A-Za-z]\)', t)
                    or re.match(r'^\(\d+\)\s*\.?\s*\([A-Za-z]\)', t)
                    or re.match(r'^\d+\.\s+\S+', t)
                )

            if insert_at < len(lines_work) and _is_option_or_list_line_local(lines_work[insert_at]):
                while insert_at > 0 and _is_option_or_list_line_local(lines_work[insert_at - 1]):
                    insert_at -= 1
            lines_work[insert_at:insert_at] = [marker, '']
            continue

        fallback_markers.append((top, marker))

    total = len(lines_work)
    slots: dict[int, list[str]] = {}

    def _is_option_or_list_line(s: str) -> bool:
        t = s.strip()
        return bool(
            re.match(r'^\([A-Za-z]\)\s+', t)
            or re.match(r'^\d+\.\s+\([A-Za-z]\)', t)
            or re.match(r'^\(\d+\)\s*\.?\s*\([A-Za-z]\)', t)
            or re.match(r'^\d+\.\s+\S+', t)
        )

    def _adjust_insertion_idx(idx: int) -> int:
        idx = max(0, min(total, idx))
        # Avoid inserting markers in the middle of option/list blocks.
        if 0 < idx < total and _is_option_or_list_line(lines_work[idx - 1]) and _is_option_or_list_line(lines_work[idx]):
            up = idx
            while up > 0 and _is_option_or_list_line(lines_work[up - 1]):
                up -= 1
            return up
        return idx

    for top, marker in sorted(fallback_markers, key=lambda x: x[0]):
        idx = int((max(top, 0.0) / h) * total)
        idx = _adjust_insertion_idx(idx)
        slots.setdefault(idx, []).append(marker)

    out: list[str] = []
    for i in range(total + 1):
        if i in slots:
            for m in slots[i]:
                if out and out[-1].strip():
                    out.append('')
                out.append(m)
                out.append('')
        if i < total:
            out.append(lines_work[i])
    return '\n'.join(out).strip()


def check_binary(name: str, install_url: str) -> None:
    if shutil.which(name) is None:
        print(f'Error: {name} binary not found on PATH. Install from {install_url}')
        sys.exit(2)


def run_pdftotext(input_pdf: Path, output_txt: Path) -> None:
    check_binary('pdftotext', 'https://poppler.freedesktop.org/')
    cmd = [
        'pdftotext',
        '-enc',
        'UTF-8',
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


def _is_list_item_line(line: str) -> bool:
    s = line.strip()
    if not s:
        return False
    if _is_alpha_option_line(s):
        return True
    if re.match(r'^[\u30a2-\u30f3\uff71-\uff9d]\s+\S+', s):
        return True
    if re.match(r'^[\(（][\u30a1-\u30f6\uff66-\uff9fA-Za-z][\)）]\s*\S+', s):
        return True
    if re.match(r'^[\-\*\+]\s+\S+', s):
        return True
    if re.match(r'^\d+\.\s+\S+', s):
        return True
    if re.match(r'^\([0-9]+\)\s*\.?\s*\S*', s):
        return True
    return False


def _is_alpha_option_line(s: str) -> bool:
    # Canonical "(A) ..." option line.
    if re.match(r'^\([A-Za-z]\)\s+\S+', s):
        return True
    # Speaker-prefixed option line, e.g. "米       (A) ...", "W1   (B) ...".
    if re.match(r'^[\u3040-\u30ff\u4e00-\u9fffA-Za-z0-9]{1,4}\s+\([A-Za-z]\)\s+\S+', s):
        return True
    return False


def _list_item_kind(line: str) -> str | None:
    s = line.strip()
    if not s:
        return None
    if _is_alpha_option_line(s):
        return 'alpha-option'
    if re.match(r'^[\u30a2-\u30f3\uff71-\uff9d]\s+\S+', s):
        return 'jp-kana'
    if re.match(r'^[\(（][\u30a1-\u30f6\uff66-\uff9fA-Za-z][\)）]\s*\S+', s):
        return 'jp-kana-paren'
    if re.match(r'^[\-\*\+]\s+\S+', s):
        return 'bullet'
    if re.match(r'^\d+\.\s+\S+', s):
        return 'ordered'
    if re.match(r'^\([0-9]+\)\s*\.?\s*\S*', s):
        return 'numbered-paren'
    return None


def _compact_blank_lines_between_list_items(md_text: str) -> str:
    lines = md_text.splitlines()
    out: list[str] = []
    for idx, line in enumerate(lines):
        if line.strip() != '':
            out.append(line)
            continue

        prev_line = ''
        next_line = ''
        j = idx - 1
        while j >= 0:
            if lines[j].strip():
                prev_line = lines[j]
                break
            j -= 1
        k = idx + 1
        while k < len(lines):
            if lines[k].strip():
                next_line = lines[k]
                break
            k += 1

        prev_kind = _list_item_kind(prev_line)
        next_kind = _list_item_kind(next_line)
        # Compact within the same list type, but keep separation between
        # option blocks and the next question number block.
        if prev_kind and next_kind and prev_kind == next_kind:
            continue
        out.append(line)
    return '\n'.join(out)


def _is_cjk_char(ch: str) -> bool:
    code = ord(ch)
    return (
        0x3040 <= code <= 0x30FF  # Hiragana/Katakana
        or 0x4E00 <= code <= 0x9FFF  # CJK unified ideographs
        or 0x3400 <= code <= 0x4DBF  # CJK extension A
        or 0xFF00 <= code <= 0xFFEF  # Fullwidth forms
    )


def _merge_soft_wrapped_lines(lines: list[str]) -> list[str]:
    if not lines:
        return lines
    out: list[str] = [lines[0]]
    for line in lines[1:]:
        prev = out[-1]
        curr = line
        if not prev.strip() or not curr.strip():
            out.append(curr)
            continue
        if prev.strip().startswith('[[') or curr.strip().startswith('[['):
            out.append(curr)
            continue
        if _is_list_item_line(curr):
            out.append(curr)
            continue
        prev_tail = prev.rstrip()
        curr_head = curr.lstrip()
        if not prev_tail or not curr_head:
            out.append(curr)
            continue
        if prev_tail[-1] in {'。', '！', '？', '.', '!', '?', ')', ']', '}', ':'}:
            out.append(curr)
            continue

        prev_cjk = _is_cjk_char(prev_tail[-1])
        curr_cjk = _is_cjk_char(curr_head[0])
        if prev_cjk and curr_cjk:
            out[-1] = prev_tail + curr_head
            continue
        out.append(curr)
    return out


def _fuzzy_key(s: str) -> str:
    return re.sub(r'[\W_]+', '', s.strip(), flags=re.UNICODE)


def _strip_plain_table_residue(md_text: str) -> str:
    lines = md_text.splitlines()
    out: list[str] = []
    i = 0
    n = len(lines)

    def _table_keys(table_lines: list[str]) -> list[str]:
        keys: list[str] = []
        for ln in table_lines:
            s = ln.strip()
            if not s.startswith('|'):
                continue
            if re.match(r'^\|\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?$', s):
                continue
            parts = [p.strip() for p in s.strip('|').split('|')]
            for p in parts:
                k = _fuzzy_key(p)
                if len(k) >= 2:
                    keys.append(k)
        return keys

    def _looks_like_residue(s: str, keys: list[str], all_key: str) -> bool:
        st = s.strip()
        if not st:
            return True
        if st.startswith('[[') or st.startswith('|'):
            return False
        if re.match(r'^\([A-Za-z]\)\s+', st):
            return False
        if re.match(r'^\d+\.\s+\([A-Za-z]\)', st):
            return False
        if re.match(r'^\-+\s*\d+\s*\-+$', st):
            return False
        if ':' in st and len(st) <= 80:
            return False
        if re.match(r'^\s{6,}\S', s):
            if re.search(r'\d', st) or ('  ' in s and len(st) <= 80):
                return True
        if re.match(r'^\d+\s*番街$', st):
            return True
        if re.match(r'^\d+\s+\S+$', st) and len(st) <= 24 and not re.search(r'[A-Za-z]', st):
            return True
        # Common raw-table spill terms in JA textbook output.
        if any(term in st for term in ('アパート', '家賃', '平方フィート', 'ドル')):
            return True
        k = _fuzzy_key(st)
        if len(k) < 4:
            return False
        if len(k) >= 8 and (k in all_key or all_key.find(k[: min(16, len(k))]) >= 0):
            return True
        hits = 0
        for tk in keys:
            if len(tk) < 3:
                continue
            if tk in k or k in tk:
                hits += 1
            if hits >= 2:
                return True
        return False

    while i < n:
        line = lines[i]
        out.append(line)
        if not line.startswith('[[TABLE:'):
            i += 1
            continue

        # Collect markdown table rows following marker.
        j = i + 1
        table_lines: list[str] = []
        while j < n and lines[j].strip().startswith('|'):
            table_lines.append(lines[j])
            out.append(lines[j])
            j += 1
        if not table_lines:
            i += 1
            continue

        keys = _table_keys(table_lines)
        all_key = ''.join(keys)
        if not keys:
            i = j
            continue

        # In many PDFs, raw flattened table text can appear a few lines after
        # the markdown table (not necessarily immediately adjacent). Scan a
        # bounded window and drop residue-like lines while keeping normal text.
        k = j
        window_end = min(n, j + 70)
        while window_end < n and lines[window_end].strip() and '[[PAGEBREAK]]' not in lines[window_end]:
            window_end += 1
            if window_end - j >= 120:
                break
        for idx in range(j, window_end):
            s = lines[idx]
            if _looks_like_residue(s, keys, all_key):
                continue
            out.append(s)
        i = window_end
    return '\n'.join(out)


def _normalize_spacing_around_lists(md_text: str) -> str:
    lines = md_text.splitlines()
    out: list[str] = []

    def is_list_item(s: str) -> bool:
        t = s.strip()
        return bool(
            _is_alpha_option_line(t)
            or re.match(r'^\(\d+\)\s*\.?\s*\([A-Za-z]\)', t)
            or re.match(r'^\d+\.\s+\([A-Za-z]\)', t)
            or re.match(r'^\d+\.\s+\S+', t)
            or re.match(r'^[\-\*\+]\s+\S+', t)
        )

    def is_title_like(s: str) -> bool:
        t = s.strip()
        return bool(
            re.match(r'^Unit\s+\d+\b', t)
            or re.match(r'^Part\s+\d+\b', t)
            or re.match(r'^Warm-up\b', t)
            or re.match(r'^Check Your Vocabulary!?$', t)
            or re.match(r'^Word Association$', t)
        )

    def is_marker_line(s: str) -> bool:
        return s.strip().startswith('[[')

    for i, line in enumerate(lines):
        cur = line.rstrip()
        prev = out[-1] if out else ''
        nxt = lines[i + 1].rstrip() if i + 1 < len(lines) else ''

        if cur.strip() and is_title_like(cur):
            prev_nonblank = ''
            for j in range(len(out) - 1, -1, -1):
                if out[j].strip():
                    prev_nonblank = out[j].strip()
                    break
            if prev_nonblank == cur.strip():
                continue

        if cur.strip() and is_title_like(cur) and prev.strip() and not is_title_like(prev):
            out.append('')

        if cur.strip() and is_marker_line(cur) and prev.strip() and not is_marker_line(prev):
            out.append('')

        if cur.strip() and is_list_item(cur) and prev.strip() and not is_list_item(prev):
            out.append('')
        out.append(cur)
        if cur.strip() and is_list_item(cur) and nxt.strip() and not is_list_item(nxt):
            out.append('')
        if cur.strip() and is_marker_line(cur) and nxt.strip() and not is_marker_line(nxt):
            out.append('')
        if cur.strip() and is_title_like(cur) and nxt.strip() and not is_title_like(nxt):
            out.append('')

    # collapse multiple blank lines down to one
    compact: list[str] = []
    blank_run = 0
    for ln in out:
        if ln.strip():
            blank_run = 0
            compact.append(ln)
        else:
            blank_run += 1
            if blank_run <= 1:
                compact.append('')
    return '\n'.join(compact).strip() + '\n'


def _strip_placeholder_markers(md_text: str) -> str:
    """Remove internal placeholder marker lines from markdown output."""
    lines = md_text.splitlines()
    out: list[str] = []
    marker_re = re.compile(r'^\[\[(SHAPE|TABLE|TEXTBOX|ASSET):')
    for line in lines:
        if marker_re.match(line.strip()):
            continue
        out.append(line)

    compact: list[str] = []
    blank_run = 0
    for ln in out:
        if ln.strip():
            blank_run = 0
            compact.append(ln)
        else:
            blank_run += 1
            if blank_run <= 1:
                compact.append('')
    return '\n'.join(compact).strip() + '\n'


def _tighten_audio_ref_spacing(md_text: str) -> str:
    lines = md_text.splitlines()
    out: list[str] = []
    for i, line in enumerate(lines):
        if line.strip() != '':
            out.append(line)
            continue
        prev_line = out[-1] if out else ''
        next_line = lines[i + 1] if i + 1 < len(lines) else ''
        if re.match(r'^\d+\.\s+\([A-Za-z]\)\s*$', prev_line.strip()) and re.match(r'^\s*A_\d+\b', next_line):
            continue
        out.append(line)
    return '\n'.join(out).strip() + '\n'


def _strip_speaker_accent_hints(md_text: str) -> str:
    lines = md_text.splitlines()
    out: list[str] = []
    for line in lines:
        s = line.rstrip()
        if re.fullmatch(r'\s*[米英加豪]\s*', s):
            continue
        s = re.sub(r'^(\s*)[米英加豪]\s{2,}', r'\1', s)
        s = re.sub(r'^(\s*)[米英加豪]\s+(?=[A-Za-z][A-Za-z0-9]{0,3}\s*:)', r'\1', s)
        out.append(s)

    compact: list[str] = []
    blank_run = 0
    for ln in out:
        if ln.strip():
            blank_run = 0
            compact.append(ln)
        else:
            blank_run += 1
            if blank_run <= 1:
                compact.append('')
    return '\n'.join(compact).strip() + '\n'


def _normalize_option_indentation(md_text: str) -> str:
    lines = md_text.splitlines()
    out: list[str] = []
    in_qa_block = False
    saw_audio_ref = False
    question_indent = 0
    for line in lines:
        stripped = line.strip()

        if re.match(r'^\d+\.\s+\([A-Za-z]\)\s*$', stripped):
            in_qa_block = True
            saw_audio_ref = False
            question_indent = 0
            out.append(line)
            continue

        if in_qa_block and re.match(r'^A_\d+\b', stripped):
            saw_audio_ref = True
            out.append(line)
            continue

        # Capture indent of the first question line after audio ref.
        if in_qa_block and saw_audio_ref and stripped and not re.match(r'^\([A-Za-z]\)\s+\S+', stripped):
            question_indent = len(line) - len(line.lstrip(' '))
            out.append(line)
            continue

        # Align option lines to question indent for the current Q/A block.
        if in_qa_block and re.match(r'^\s*\([A-Za-z]\)\s+\S+', line):
            out.append((' ' * question_indent) + line.lstrip())
            continue

        # End Q/A alignment context at clear separators.
        if stripped == '[[PAGEBREAK]]' or re.match(r'^Part\s+\d+\b', stripped) or re.match(r'^Unit\s+\d+\b', stripped):
            in_qa_block = False
            saw_audio_ref = False
            question_indent = 0

        out.append(line)
    return '\n'.join(out).strip() + '\n'


def _normalize_parenthesized_marker_spacing(md_text: str) -> str:
    lines = md_text.splitlines()
    out: list[str] = []
    for line in lines:
        updated = re.sub(r'^(\s*\(\d+\))(\S)', r'\1 \2', line)
        updated = re.sub(r'^(\s*[（\(][\u30a1-\u30f6\uff66-\uff9fA-Za-z][）\)])(\S)', r'\1 \2', updated)
        out.append(updated)
    return '\n'.join(out).strip() + '\n'


def _restore_mixed_list_structure(md_text: str) -> str:
    lines = md_text.splitlines()
    out: list[str] = []

    inline_kana_re = re.compile(r'^(\s*\(\d+\)\s+.*?)([\u30a2-\u30aa\uff71-\uff75])\s{2,}(.*)$')
    inline_kana_paren_re = re.compile(
        r'^(\s*\(\d+\)\s+.*?)([\(（][\u30a1-\u30f6\uff66-\uff9fA-Za-z][\)）])\s{2,}(.*)$'
    )
    bare_kana_re = re.compile(r'^\s*([\u30a2-\u30aa\uff71-\uff75])\s+(.*)$')
    bare_kana_paren_re = re.compile(r'^\s*([\(（][\u30a1-\u30f6\uff66-\uff9fA-Za-z][\)）])\s*(.*)$')

    for line in lines:
        stripped = line.strip()
        if not stripped:
            out.append(line)
            continue

        m_inline = inline_kana_re.match(line)
        if m_inline:
            out.append(m_inline.group(1).rstrip())
            out.append(f'    - {m_inline.group(2)} {m_inline.group(3).lstrip()}')
            continue

        m_inline_paren = inline_kana_paren_re.match(line)
        if m_inline_paren:
            out.append(m_inline_paren.group(1).rstrip())
            out.append(f'    - {m_inline_paren.group(2)} {m_inline_paren.group(3).lstrip()}')
            continue

        m_kana = bare_kana_re.match(line)
        if m_kana:
            out.append(f'    - {m_kana.group(1)} {m_kana.group(2).lstrip()}')
            continue

        m_kana_paren = bare_kana_paren_re.match(line)
        if m_kana_paren and not re.match(r'^[\(（]\d+[\)）]', stripped):
            out.append(f'    - {m_kana_paren.group(1)} {m_kana_paren.group(2).lstrip()}')
            continue

        out.append(line)

    return '\n'.join(out).strip() + '\n'


def _build_layout_manifest(
    structured_blocks: list[tuple[float, list[tuple[float, str]]]],
) -> dict[str, Any]:
    marker_re = re.compile(
        r'^\[\[(TABLE|TEXTBOX|SHAPE):([^|\]]+)(?:\|bbox=([0-9.]+),([0-9.]+),([0-9.]+),([0-9.]+))?\]\]$'
    )
    pages: list[dict[str, Any]] = []

    for page_idx, (page_height, blocks) in enumerate(structured_blocks, start=1):
        objects: list[dict[str, Any]] = []
        for top, block in blocks:
            if not block:
                continue
            raw_lines = block.splitlines()
            if not raw_lines:
                continue
            m = marker_re.match(raw_lines[0].strip())
            if not m:
                continue
            obj_type = m.group(1).lower()
            obj_id = m.group(2)
            bbox = None
            if m.group(3) is not None:
                bbox = [float(m.group(3)), float(m.group(4)), float(m.group(5)), float(m.group(6))]
            data: dict[str, Any] = {
                'type': obj_type,
                'id': obj_id,
                'top': float(top),
            }
            if bbox is not None:
                data['bbox'] = bbox
            if len(raw_lines) > 1:
                payload = [ln.rstrip() for ln in raw_lines[1:] if ln.strip()]
                if payload:
                    data['content_lines'] = payload
            objects.append(data)

        pages.append(
            {
                'page': page_idx,
                'height': float(page_height),
                'objects': objects,
            }
        )

    return {'pages': pages}


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
        page_lines = _merge_soft_wrapped_lines(page_text.splitlines()) if page_text else []
        asset_lines: list[str] = []
        for asset in assets_by_page.get(page_idx, []):
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
            lines.append(_asset_ref_html(asset, assets_rel))

    result = '\n'.join(lines).strip() + '\n'
    result = _compact_blank_lines_between_list_items(result)
    result = _strip_plain_table_residue(result)
    result = _normalize_spacing_around_lists(result)
    result = _tighten_audio_ref_spacing(result)
    result = _strip_speaker_accent_hints(result)
    result = _normalize_parenthesized_marker_spacing(result)
    result = _restore_mixed_list_structure(result)
    result = _normalize_option_indentation(result)
    result = _strip_placeholder_markers(result)
    return result


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
    output_layout = output_md.with_name(f'{output_md.stem}.layout.json')

    staging_ctx: tempfile.TemporaryDirectory[str] | None = None
    run_input_path = source_input_path
    run_output_dir = output_dir
    run_assets_dir = assets_dir
    run_output_md = output_md
    run_output_layout = output_layout
    if not args.no_local_staging:
        staging_ctx = tempfile.TemporaryDirectory(prefix='textmaker-pdf-')
        staging_root = Path(staging_ctx.name)
        run_input_path = stage_input_file(source_input_path, staging_root / 'input')
        run_output_dir = staging_root / 'out'
        run_output_dir.mkdir(parents=True, exist_ok=True)
        run_assets_dir = (run_output_dir / assets_arg) if not assets_arg.is_absolute() else (staging_root / 'assets')
        run_assets_dir.mkdir(parents=True, exist_ok=True)
        run_output_md = run_output_dir / output_md.name
        run_output_layout = run_output_dir / output_layout.name
        print(f'Local staging enabled: {run_input_path}')

    extracted_images = run_pdfimages(run_input_path, run_assets_dir, prefix='image')

    text = ''
    text_source = 'pdftotext'
    structured_pages: list[str] | None = None
    structured_blocks: list[tuple[float, list[tuple[float, str]]]] | None = None
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
        raw_struct = extract_structured_pages(run_input_path, include_plain_words=False, return_blocks=True)
        structured_blocks = cast(list[tuple[float, list[tuple[float, str]]]] | None, raw_struct)
        if structured_blocks is None and args.layout_mode == 'structured':
            print('Structured layout mode requested, but pdfplumber is unavailable; using plain layout text.')

    assets_rel = Path('.') if assets_dir == output_md.parent else Path(
        os.path.relpath(assets_dir, output_md.parent)
    )
    if structured_blocks:
        plain_pages = text.split('\f') if text else []
        if len(plain_pages) < len(structured_blocks):
            plain_pages.extend([''] * (len(structured_blocks) - len(plain_pages)))
        elif len(plain_pages) > len(structured_blocks):
            plain_pages = plain_pages[: len(structured_blocks)]

        merged_pages: list[str] = []
        for idx, (page_height, marker_blocks) in enumerate(structured_blocks):
            plain_text = plain_pages[idx] if idx < len(plain_pages) else ''
            merged_pages.append(_merge_marker_blocks_into_plain_page(plain_text, page_height, marker_blocks))

        markdown = build_markdown_from_pages(
            merged_pages,
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

    if structured_blocks is not None:
        layout_manifest = _build_layout_manifest(structured_blocks)
        run_output_layout.write_text(
            json.dumps(layout_manifest, ensure_ascii=False, indent=2) + '\n',
            encoding='utf-8',
        )
    run_output_md.write_text(markdown, encoding='utf-8')
    if staging_ctx is not None:
        sync_dir(run_assets_dir, assets_dir)
        sync_file(run_output_md, output_md)
        if run_output_layout.exists():
            sync_file(run_output_layout, output_layout)
        staging_ctx.cleanup()
    else:
        output_md = run_output_md
        output_layout = run_output_layout
    print('Text source:', text_source)
    print('Wrote', output_md)
    if output_layout.exists():
        print('Wrote', output_layout)


if __name__ == '__main__':
    main()
