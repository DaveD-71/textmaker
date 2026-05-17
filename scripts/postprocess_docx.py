"""
Post-process a DOCX produced by Pandoc to ensure:
- a section break is inserted immediately after the Table of Contents
- page numbering restarts at 1 for the following section
- page numbers are removed from TOC pages
- section breaks (nextPage) are inserted before each H1 heading
- Quick Parts are inserted through Word COM from a real template when available

Semantic label rendering (emoji, character styles, unit title tables) is opt-in;
pass --apply-semantic-labels to enable it. Style definitions are never created or
redefined here — all style management belongs in manage_docx_styles.py.
"""
# pylint: disable=protected-access,broad-exception-caught
import argparse
import copy
import csv
import ctypes
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable

try:
    from docx import Document  # type: ignore[reportMissingImports]
    from docx.enum.style import WD_STYLE_TYPE  # type: ignore[reportMissingImports]
    from docx.enum.text import WD_ALIGN_PARAGRAPH  # type: ignore[reportMissingImports]
    from docx.oxml import OxmlElement  # type: ignore[reportMissingImports]
    from docx.oxml.ns import qn  # type: ignore[reportMissingImports]
    from docx.oxml.table import CT_Tbl  # type: ignore[reportMissingImports]
    from docx.oxml.text.paragraph import CT_P  # type: ignore[reportMissingImports]
    from docx.table import Table  # type: ignore[reportMissingImports]
    from docx.text.paragraph import Paragraph  # type: ignore[reportMissingImports]
except ImportError as exc:
    raise RuntimeError(
        'Missing dependency: python-docx is required. Install with `pip install python-docx`.'
    ) from exc

try:
    import pythoncom  # type: ignore[reportMissingImports]
    import win32com.client  # type: ignore[reportMissingImports]
except ImportError:
    pythoncom = None
    win32com = None


NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

WHY_LABEL = 'Why this works:'
CHECK_LABELS = ('Before you write:',)
LEARN_LABELS = (
    'Teaching point:',
    'Key principle:',
    'Writing goal:',
    'Transfer reminder:',
    'Role reminder:',
    'Planning reminder:',
)
NOTE_LABELS = (
    'Note:',
    'Note on',
    'Additional note:',
    'How to use the checklist:',
    'Rubric note:',
    'Self-study note:',
)
BAD_MODEL_HEADINGS = {
    'Original Version',
    'Original Version (too direct)',
    'Original (Disjointed)',
}
GOOD_MODEL_HEADINGS = {
    'Revised Version',
    'Revised Version (diplomatic)',
    'Revised (Cohesive)',
}
NEUTRAL_MODEL_SOURCE_STYLES = {
    'Block Text',
    'Quote',
    'Intense Quote',
}
QUOTED_MODEL_RE = re.compile(r'^[\u201c"].+[\u201d"]$')
WORD_COUNT_RE = re.compile(
    r'\b(?:approximately|about|around)?\s*\d+\s*(?:[-\u2013\u2014]\s*\d+)?\s*words?\b',
    re.IGNORECASE,
)
UNIT_HEADING_RE = re.compile(r'^Unit\s+(\d+)\s+[-\u2013\u2014]\s+(.+)$')
MODULE_HEADING_RE = re.compile(r'^Module\s+\d+\s+[-\u2013\u2014]\s+.+$')
ALPHA_ORDINAL_RE = re.compile(r'^([A-Z])\.\s+\S+')
ACTIVITY_CODE_SUFFIX_RE = re.compile(r'\s+\(([A-H]\d)(?:[^)]*)\)\s*(?:[★*])?\s*$')
MODULE_UNIT_RANGE_SUFFIX_RE = re.compile(
    r'\s+\(Units?\s+\d+\s*[-\u2013\u2014]\s*\d+\)\s*$',
    re.IGNORECASE,
)

SEMANTIC_DIV_EMOJI = {
    # Style IDs match reference DOCX "Div Label *" paragraph styles
    'DivLabelProcess': '🧭',
    'DivLabelLanguage': '💬',
    'DivLabelPrinciple': '💡',
    'DivLabelTransfer': '🔁',
    'DivLabelTeaching': '📘',
    'DivLabelNote': '🗒️',
    'DivLabelBase': 'ℹ️',           # fallback for guidance-step, reference-support, etc.
    'DivLabelActivityInput': '📥',
    'DivLabelActivityAnalysis': '🔎',
    'DivLabelActivityLanguageControl': '🔤',
    'DivLabelActivityRewrite': '🔄',
    'DivLabelActivityEdit': '✏️',
    'DivLabelActivityDraft': '📝',
    'DivLabelWorkedExample': '🧩',
    'DivLabelExample': '📌',
    'DivLabelPlaceholder': '⬜',
    'DivLabelSelfStudy': '📚',
    'DivLabelAnnotation': '🏷️',
    'DivLabelModel': '📄',
    'DivLabelBad': '❌',
    'DivLabelGood': '✅',
}

# Maps paragraph style ID → tag_filled_*.png filename stem.
# example-good and example-bad share the example tag image.
DIV_TAG_ICON_STEMS = {
    'DivLabelLearn':       'tag_filled_learn',
    'DivLabelLanguage':    'tag_filled_language',
    'DivLabelStructure':   'tag_filled_structure',
    'DivLabelNotice':      'tag_filled_notice',
    'DivLabelWrite':       'tag_filled_write',
    'DivLabelRewrite':     'tag_filled_rewrite',
    'DivLabelRevise':      'tag_filled_revise',
    'DivLabelEdit':        'tag_filled_edit',
    'DivLabelExample':     'tag_filled_example',
    'DivLabelExampleGood': 'tag_filled_example',
    'DivLabelExampleBad':  'tag_filled_example',
}

# Height (in EMU) at which to render the tag icon inline.
# 457200 EMU = 36pt — tall enough to be readable, short enough not to dominate.
DIV_TAG_ICON_HEIGHT_EMU = 457200

def _resolve_div_tag_icon(style_id: str, reference_doc_path) -> 'Path | None':
    """Return the Path to the filled tag icon PNG for style_id, or None if not found.

    Looks for div-tags-icons-2_assets/ as a sibling of the reference DOCX file.
    """
    stem = DIV_TAG_ICON_STEMS.get(style_id)
    if not stem or not reference_doc_path:
        return None
    ref_dir = Path(reference_doc_path).parent
    icon_path = ref_dir / 'div-tags-icons-2_assets' / f'{stem}.png'
    return icon_path if icon_path.exists() else None


def build_semantic_div_label_styles(reference_doc_path=None):
    """
    Build a mapping from paragraph style ID to character style name for semantic Div label runs.

    Keys are paragraph style IDs (e.g. 'DivLabelProcess'); values are the linked character
    style names (e.g. 'Div Label Process Char') used to colour the label run.
    """
    if not reference_doc_path:
        return {}

    ref_doc = Document(reference_doc_path)
    styles = ref_doc.styles
    mapping = {}
    for style in styles:
        if style.type != WD_STYLE_TYPE.PARAGRAPH:
            continue
        if not style.name.startswith('Div Label '):
            continue
        char_style_name = style.name + ' Char'
        char_style = _get_style_by_name_or_id(styles, char_style_name, WD_STYLE_TYPE.CHARACTER)
        if char_style is not None:
            mapping[style.style_id] = char_style_name
    return mapping


# SEMANTIC_DIV_LABEL_STYLES will be set in apply_semantic_div_labels

LEARN_SEMANTIC_STYLE_IDS: set[str] = set()  # Learn base conversion removed

SEMANTIC_DIV_STYLE_IDS = set(SEMANTIC_DIV_EMOJI)

DEFAULT_BUILDING_BLOCK_TEMPLATE = (
    Path(os.environ.get('APPDATA', str(Path.home() / 'AppData' / 'Roaming')))
    / 'Microsoft'
    / 'Templates'
    / 'Normal.dotm'
)
BUILDING_BLOCK_NAMES = {'unit': ('Call Out - Unit Title', 'Unit Tile')}

WORD_COLLAPSE_START = 1
WORD_COLLAPSE_END = 0
WORD_PAGE_BREAK = 7
WORD_ALERTS_NONE = 0
WORD_DO_NOT_SAVE_CHANGES = 0
WORD_SAVE_CHANGES = -1


def _insert_section_break_before_paragraph(paragraph, restart_numbering=False, start_page=1):
    """
    Insert a nextPage section break BEFORE a paragraph by attaching sectPr
    to the PREVIOUS paragraph (that's how Word section breaks work).

    If restart_numbering=True, the new section will restart page numbering at start_page.
    """
    doc_element = paragraph._element.getparent()
    paragraphs = list(doc_element.iterchildren())

    try:
        current_index = paragraphs.index(paragraph._element)
    except ValueError:
        return False

    if current_index == 0:
        return False

    prev_p = paragraphs[current_index - 1]
    p_pr = prev_p.find(qn('w:pPr'))
    if p_pr is None:
        p_pr = OxmlElement('w:pPr')
        prev_p.insert(0, p_pr)

    for sect in list(p_pr.findall(qn('w:sectPr'))):
        try:
            p_pr.remove(sect)
        except Exception:
            pass

    sect_pr = OxmlElement('w:sectPr')
    type_el = OxmlElement('w:type')
    type_el.set(qn('w:val'), 'nextPage')
    sect_pr.append(type_el)

    if restart_numbering:
        pg_num_type = OxmlElement('w:pgNumType')
        pg_num_type.set(qn('w:start'), str(start_page))
        sect_pr.append(pg_num_type)

    p_pr.append(sect_pr)
    return True


def _apply_next_page_section_to_paragraph(paragraph, start_page=None):
    """Attach a nextPage sectPr (and optional page-number restart) to an existing paragraph."""
    p_pr = paragraph._p.find(qn('w:pPr'))
    if p_pr is None:
        p_pr = OxmlElement('w:pPr')
        paragraph._p.insert(0, p_pr)

    for sect in list(p_pr.findall(qn('w:sectPr'))):
        try:
            p_pr.remove(sect)
        except Exception:
            pass

    sect_pr = OxmlElement('w:sectPr')
    type_el = OxmlElement('w:type')
    type_el.set(qn('w:val'), 'nextPage')
    sect_pr.append(type_el)

    if start_page is not None:
        pg_num_type = OxmlElement('w:pgNumType')
        pg_num_type.set(qn('w:start'), str(start_page))
        sect_pr.append(pg_num_type)

    p_pr.append(sect_pr)


def _remove_page_numbers_from_footer(footer):
    """Remove PAGE field codes from a footer to suppress page numbers."""
    try:
        for para in footer.paragraphs:
            runs_to_remove = []
            for run in para.runs:
                run_elem = run._element
                fld_simple = run_elem.find('.//w:fldSimple', NS)
                fld_char = run_elem.find('.//w:fldChar', NS)
                instr_text = run_elem.find('.//w:instrText', NS)

                if fld_simple is not None:
                    instr = fld_simple.get(qn('w:instr'), '')
                    if 'PAGE' in instr.upper():
                        runs_to_remove.append(run)
                elif instr_text is not None:
                    if 'PAGE' in (instr_text.text or '').upper():
                        runs_to_remove.append(run)
                elif fld_char is not None:
                    all_instr = run_elem.findall('.//w:instrText', NS)
                    for it in all_instr:
                        if 'PAGE' in (it.text or '').upper():
                            runs_to_remove.append(run)
                            break

            for run in runs_to_remove:
                para._element.remove(run._element)
    except Exception as exc:
        print(f'Warning: Could not remove page numbers from footer: {exc}')


def _is_heading_1(paragraph):
    """Check if paragraph is styled as Heading 1."""
    style = paragraph.style
    if style and 'Heading 1' in style.name:
        return True
    if hasattr(style, 'style_id') and style.style_id == 'Heading1':
        return True
    return False


def insert_section_breaks_before_h1(doc, skip_first=True, restart_first=False):
    """Insert nextPage section breaks before each H1 heading."""
    paragraphs = list(doc.paragraphs)
    h1_count = 0
    sections_added = 0

    for para in paragraphs:
        if _is_heading_1(para):
            h1_count += 1
            if skip_first and h1_count == 1:
                continue

            restart = restart_first and h1_count == 1
            try:
                success = _insert_section_break_before_paragraph(
                    para,
                    restart_numbering=restart,
                    start_page=1,
                )
                if success:
                    sections_added += 1
            except Exception as exc:
                print(f"Warning: Could not insert section break before H1 '{para.text}': {exc}")

    return sections_added


def _qn_attr(nsmap, attr):
    return f'{{{nsmap.get("w")}}}{attr}'


def _build_num_format_map(doc):
    """Map numId/ilvl to numFmt (e.g., bullet, decimal)."""
    try:
        num_part = doc.part.numbering_part.element
    except Exception:
        return {}
    nsmap = num_part.nsmap

    abstract_map = {}
    for abs_num in num_part.findall('w:abstractNum', nsmap):
        abs_id = abs_num.get(_qn_attr(nsmap, 'abstractNumId'))
        lvl_map = {}
        for lvl in abs_num.findall('w:lvl', nsmap):
            ilvl = lvl.get(_qn_attr(nsmap, 'ilvl'))
            numfmt_el = lvl.find('w:numFmt', nsmap)
            if ilvl is not None and numfmt_el is not None:
                lvl_map[ilvl] = numfmt_el.get(_qn_attr(nsmap, 'val'))
        if abs_id is not None:
            abstract_map[abs_id] = lvl_map

    num_map = {}
    for num in num_part.findall('w:num', nsmap):
        num_id = num.get(_qn_attr(nsmap, 'numId'))
        abs_el = num.find('w:abstractNumId', nsmap)
        if num_id is None or abs_el is None:
            continue
        abs_id = abs_el.get(_qn_attr(nsmap, 'val'))
        num_map[num_id] = abstract_map.get(abs_id, {})

    return num_map


def _numbering_element(doc):
    try:
        return doc.part.numbering_part.element
    except Exception:
        return None


def _num_id_from_style(style) -> str | None:
    style_el = getattr(style, '_element', None)
    if style_el is None:
        return None
    num_id_el = style_el.find('.//w:numPr/w:numId', NS)
    return num_id_el.get(qn('w:val')) if num_id_el is not None else None


def _paragraph_num_id(paragraph) -> str | None:
    p_pr = paragraph._p.find(qn('w:pPr'))
    num_pr = p_pr.find(qn('w:numPr')) if p_pr is not None else None
    if num_pr is None:
        return None
    num_id_el = num_pr.find(qn('w:numId'))
    return num_id_el.get(qn('w:val')) if num_id_el is not None else None


def _abstract_num_id_for_num(numbering, num_id: str) -> str | None:
    nsmap = numbering.nsmap
    for num in numbering.findall('w:num', nsmap):
        if num.get(_qn_attr(nsmap, 'numId')) != str(num_id):
            continue
        abstract_el = num.find('w:abstractNumId', nsmap)
        if abstract_el is not None:
            return abstract_el.get(_qn_attr(nsmap, 'val'))
    return None


def _next_num_id(numbering) -> str:
    nsmap = numbering.nsmap
    used = []
    for num in numbering.findall('w:num', nsmap):
        num_id = num.get(_qn_attr(nsmap, 'numId'))
        if num_id and num_id.isdigit():
            used.append(int(num_id))
    return str((max(used) if used else 0) + 1)


def _create_restarted_num_id(doc, base_num_id: str, start_value: int, ilvl: str = '0') -> str | None:
    numbering = _numbering_element(doc)
    if numbering is None:
        return None
    abstract_num_id = _abstract_num_id_for_num(numbering, base_num_id)
    if abstract_num_id is None:
        return None

    new_num_id = _next_num_id(numbering)
    num = OxmlElement('w:num')
    num.set(qn('w:numId'), new_num_id)

    abstract = OxmlElement('w:abstractNumId')
    abstract.set(qn('w:val'), abstract_num_id)
    num.append(abstract)

    lvl_override = OxmlElement('w:lvlOverride')
    lvl_override.set(qn('w:ilvl'), ilvl)
    start_override = OxmlElement('w:startOverride')
    start_override.set(qn('w:val'), str(start_value))
    lvl_override.append(start_override)
    num.append(lvl_override)

    numbering.append(num)
    return new_num_id


def _apply_direct_num_id(paragraph, num_id: str, ilvl: str = '0') -> bool:
    p_pr = paragraph._p.get_or_add_pPr()
    existing = p_pr.find(qn('w:numPr'))
    if existing is not None:
        p_pr.remove(existing)

    num_pr = OxmlElement('w:numPr')
    ilvl_el = OxmlElement('w:ilvl')
    ilvl_el.set(qn('w:val'), ilvl)
    num_id_el = OxmlElement('w:numId')
    num_id_el.set(qn('w:val'), str(num_id))
    num_pr.append(ilvl_el)
    num_pr.append(num_id_el)
    p_pr.append(num_pr)
    return True


def _alpha_marker_start_value(marker: str) -> int:
    return ord(marker.upper()) - ord('A') + 1


def _get_style_by_name_or_id(styles, target, style_type=None):
    """Fetch a style by name or style_id; returns None if missing."""
    try:
        style = styles[target]
        if style_type is None or getattr(style, 'type', None) == style_type:
            return style
    except Exception:
        pass
    for st in styles:
        if getattr(st, 'name', None) == target or getattr(st, 'style_id', None) == target:
            if style_type is not None and getattr(st, 'type', None) != style_type:
                continue
            return st
    return None


def _require_style(styles, target):
    style = _get_style_by_name_or_id(styles, target)
    if not style:
        raise RuntimeError(f'Required style is missing from the reference DOCX: {target}')
    return style


def _require_character_style(styles, target):
    style = _get_style_by_name_or_id(styles, target, WD_STYLE_TYPE.CHARACTER)
    if not style:
        raise RuntimeError(f'Required character style is missing from the reference DOCX: {target}')
    return style


def _normalize_text(text: str) -> str:
    return ' '.join(text.split())


def _clean_word_text(text: str) -> str:
    return _normalize_text(text.replace('\r', ' ').replace('\x07', ' '))


def _starts_with_any(text: str, prefixes: Iterable[str]) -> bool:
    return any(text.startswith(prefix) for prefix in prefixes)


def _is_heading(paragraph) -> bool:
    style = paragraph.style
    return bool(style and getattr(style, 'name', '').startswith('Heading'))


def _is_list_paragraph(paragraph) -> bool:
    style_name = getattr(paragraph.style, 'name', '') if paragraph.style else ''
    if style_name.startswith('List '):
        return True
    p_pr = paragraph._p.find(qn('w:pPr'))
    if p_pr is None:
        return False
    return p_pr.find(qn('w:numPr')) is not None


def _is_candidate_after_list(text: str) -> bool:
    if not text:
        return False
    if len(text) <= 220:
        return True
    lowered = text.lower()
    return (
        lowered.startswith('then discuss:')
        or lowered.startswith('discuss:')
        or lowered.startswith('reflect:')
        or lowered.startswith('then reflect:')
        or lowered.startswith('reflection:')
        or lowered.startswith('example:')
        or lowered.startswith('examples:')
        or lowered.startswith('practice ')
        or lowered.startswith('next step:')
        or lowered.startswith('next steps:')
        or lowered.startswith('in pairs')
        or lowered.startswith('working in pairs')
    )


def _is_candidate_after_text_block(text: str) -> bool:
    if not text:
        return False
    if len(text) <= 160 and not text.endswith('.'):
        return True
    lowered = text.lower()
    return (
        lowered.startswith('practice ')
        or lowered.startswith('reflect:')
        or lowered.startswith('then reflect:')
        or lowered.startswith('reflection:')
        or lowered.startswith('example:')
        or lowered.startswith('examples:')
    )


def _find_previous_text_paragraph(paragraphs, index):
    for offset in range(index - 1, -1, -1):
        para = paragraphs[offset]
        if _normalize_text(para.text):
            return para
    return None


def _apply_style_if_available(paragraph, style_name: str) -> bool:
    style = _get_style_by_name_or_id(paragraph.part.styles, style_name)
    if not style:
        return False
    paragraph.style = style
    return True


def _paragraph_style_id(paragraph) -> str:
    style = paragraph.style
    return getattr(style, 'style_id', '') if style else ''


def _paragraph_style_name(paragraph) -> str:
    style = paragraph.style
    return getattr(style, 'name', '') if style else ''


def _has_explicit_paragraph_style(paragraph) -> bool:
    p_pr = paragraph._p.find(qn('w:pPr'))
    return bool(p_pr is not None and p_pr.find(qn('w:pStyle')) is not None)


def _iter_all_paragraphs(parent) -> Iterable[Paragraph]:
    """Yield paragraphs in the document body and inside tables."""
    for paragraph in parent.paragraphs:
        yield paragraph
    for table in parent.tables:
        for row in table.rows:
            for cell in row.cells:
                yield from _iter_all_paragraphs(cell)


def _iter_story_paragraphs(doc) -> Iterable[Paragraph]:
    yield from _iter_all_paragraphs(doc)
    for section in doc.sections:
        yield from _iter_all_paragraphs(section.header)
        yield from _iter_all_paragraphs(section.first_page_header)
        yield from _iter_all_paragraphs(section.even_page_header)
        yield from _iter_all_paragraphs(section.footer)
        yield from _iter_all_paragraphs(section.first_page_footer)
        yield from _iter_all_paragraphs(section.even_page_footer)


def _set_run_font(run, font_name: str) -> None:
    r_pr = run._r.get_or_add_rPr()
    r_fonts = r_pr.rFonts
    if r_fonts is None:
        r_fonts = OxmlElement('w:rFonts')
        r_pr.insert(0, r_fonts)
    for attr in ('w:ascii', 'w:hAnsi', 'w:eastAsia', 'w:cs'):
        r_fonts.set(qn(attr), font_name)


def _set_run_color(run, color_value: str | None) -> None:
    if not color_value:
        return
    r_pr = run._r.get_or_add_rPr()
    color = r_pr.find(qn('w:color'))
    if color is None:
        color = OxmlElement('w:color')
        r_pr.append(color)
    color.set(qn('w:val'), color_value)


def _style_color_value(style) -> str | None:
    if style is None:
        return None
    style_el = getattr(style, '_element', None)
    if style_el is None:
        return None
    color = style_el.find('.//w:rPr/w:color', NS)
    if color is None:
        color = style_el.find('.//w:color', NS)
    if color is None:
        return None
    return color.get(qn('w:val'))


def _run_color_value(run) -> str | None:
    color = run._r.find('.//w:color', NS)
    if color is None:
        return None
    return color.get(qn('w:val'))


def _insert_run_after_properties(paragraph, run) -> None:
    paragraph._p.remove(run._r)
    p_pr = paragraph._p.find(qn('w:pPr'))
    if p_pr is None:
        paragraph._p.insert(0, run._r)
    else:
        paragraph._p.insert(list(paragraph._p).index(p_pr) + 1, run._r)


def _set_run_non_italic(run) -> None:
    run.font.italic = False
    r_pr = run._r.get_or_add_rPr()
    for tag in ('w:i', 'w:iCs'):
        italic = r_pr.find(qn(tag))
        if italic is None:
            italic = OxmlElement(tag)
            r_pr.append(italic)
        italic.set(qn('w:val'), '0')


def _set_run_non_bold(run) -> None:
    run.font.bold = False
    r_pr = run._r.get_or_add_rPr()
    for tag in ('w:b', 'w:bCs'):
        bold = r_pr.find(qn(tag))
        if bold is not None:
            r_pr.remove(bold)


def _is_strong_label_run(run) -> bool:
    if run.bold is True:
        return True
    r_pr = run._r.find(qn('w:rPr'))
    if r_pr is None:
        return False
    if r_pr.find(qn('w:b')) is not None:
        return True
    r_style = r_pr.find(qn('w:rStyle'))
    if r_style is None:
        return False
    return r_style.get(qn('w:val')) in {'Strong', 'StrongChar'}


def _label_base_paragraph_style(styles):
    return _get_style_by_name_or_id(styles, 'Label Base Para') or _require_style(
        styles,
        'Label Para',
    )


def _find_semantic_label_run(paragraph):
    for index, run in enumerate(paragraph.runs):
        if not run.text or not run.text.strip():
            continue
        if _is_strong_label_run(run):
            return index, run
    return None, None


def _find_run_index(paragraph, target_run) -> int | None:
    target_el = target_run._r
    for index, run in enumerate(paragraph.runs):
        if run._r is target_el:
            return index
    return None


def _normalize_learn_label_text(style_id: str, run) -> bool:
    updated = run.text
    if style_id in LEARN_SEMANTIC_STYLE_IDS:
        match = re.match(r'^\s*Learn(?:\s*[-\u2013\u2014:]\s*|\s+)(.+?)\s*$', updated)
        if match:
            updated = match.group(1)
    updated = updated.rstrip()
    if updated.endswith(':'):
        updated = updated[:-1].rstrip()
    if updated == run.text:
        return False
    run.text = updated
    return True


def apply_semantic_div_labels(doc, reference_doc_path=None) -> int:
    """
    Add visual labels to semantic Div paragraphs emitted by the Pandoc Lua filter.
    """
    changed = 0
    learn_base = _get_style_by_name_or_id(doc.styles, 'Learn Base')
    # Use reference styles if available
    if reference_doc_path:
        ref_doc = Document(reference_doc_path)
        styles = ref_doc.styles
    else:
        styles = doc.styles
    
    # Build the mapping from reference styles
    semantic_div_label_styles = build_semantic_div_label_styles(reference_doc_path)
    for para in doc.paragraphs:
        style_id = _paragraph_style_id(para)
        emoji = SEMANTIC_DIV_EMOJI.get(style_id)
        has_icon = style_id in DIV_TAG_ICON_STEMS
        if not emoji and not has_icon:
            continue

        runs = para.runs
        if not runs:
            continue

        label_index, label_run = _find_semantic_label_run(para)
        if label_run is None:
            # No bold run found — take the first non-empty run (plain label text)
            for idx, run in enumerate(para.runs):
                if run.text and run.text.strip():
                    label_index, label_run = idx, run
                    break
        if label_run is None:
            continue

        if _normalize_learn_label_text(style_id, label_run):
            changed += 1

        label_style_name = semantic_div_label_styles.get(style_id)
        label_color = _run_color_value(label_run)
        if label_style_name:
            label_style = _get_style_by_name_or_id(styles, label_style_name, WD_STYLE_TYPE.CHARACTER)
            if label_style is None:
                print(f'Warning: Character style "{label_style_name}" not found in reference DOCX, skipping.')
                continue
            label_color = label_color or _style_color_value(label_style)
            if label_style and getattr(label_run.style, 'name', None) != label_style.name:
                label_run.style = label_style
                changed += 1
        _set_run_non_italic(label_run)

        # Insert tag icon + NBSP before the label text, if not already present.
        # Detection: first child <w:r> after <w:pPr> contains a <w:drawing> → icon present.
        p_children = list(para._p)
        first_run_el = next((el for el in p_children if el.tag == qn('w:r')), None)
        already_has_icon = (
            first_run_el is not None
            and first_run_el.find(qn('w:drawing')) is not None
        )

        if not already_has_icon:
            icon_path = _resolve_div_tag_icon(style_id, reference_doc_path)
            if icon_path:
                # Image run — add_picture appends <w:drawing> inside a new <w:r>
                img_run = para.add_run()
                img_run.add_picture(str(icon_path), height=DIV_TAG_ICON_HEIGHT_EMU)
                _insert_run_after_properties(para, img_run)

                # Non-breaking space run immediately after the image
                nbsp_run = para.add_run()
                nbsp_run.text = ' '
                img_idx = list(para._p).index(img_run._r)
                para._p.remove(nbsp_run._r)
                para._p.insert(img_idx + 1, nbsp_run._r)
            else:
                # Fallback to emoji + tab when no icon file is available
                emoji_run = para.add_run()
                emoji_run.text = emoji
                _set_run_font(emoji_run, 'Noto Emoji')
                _set_run_color(emoji_run, label_color)
                _set_run_non_italic(emoji_run)
                _set_run_non_bold(emoji_run)
                _insert_run_after_properties(para, emoji_run)

                tab_run = para.add_run()
                tab_run.text = '\t'
                emoji_idx = list(para._p).index(emoji_run._r)
                para._p.remove(tab_run._r)
                para._p.insert(emoji_idx + 1, tab_run._r)
            changed += 1

        if para.alignment != WD_ALIGN_PARAGRAPH.LEFT:
            para.alignment = WD_ALIGN_PARAGRAPH.LEFT
            changed += 1

        if style_id in LEARN_SEMANTIC_STYLE_IDS:
            if learn_base is not None and getattr(para.style, 'name', None) != learn_base.name:
                para.style = learn_base
                changed += 1

    return changed


def apply_body_text_to_normal_paragraphs(doc) -> int:
    """Make ordinary prose explicit Body Text instead of implicit/explicit Normal."""
    body_text = _require_style(doc.styles, 'Body Text')

    changed = 0
    for para in doc.paragraphs:
        if not _normalize_text(para.text):
            continue
        if _is_heading(para) or _is_list_paragraph(para):
            continue
        style_id = _paragraph_style_id(para)
        if style_id in SEMANTIC_DIV_EMOJI:
            continue
        style_name = _paragraph_style_name(para)
        if style_name == 'Body Text':
            continue
        if style_name == 'Normal' or not _has_explicit_paragraph_style(para):
            para.style = body_text
            changed += 1
    return changed


def strip_activity_codes_from_headings(doc) -> int:
    """Remove activity-code suffixes from visible heading/title rows."""
    changed = 0
    for para in doc.paragraphs:
        if not _is_heading(para):
            continue
        text = _normalize_text(para.text)
        updated = ACTIVITY_CODE_SUFFIX_RE.sub('', text).strip()
        if updated == text:
            continue
        for run in para.runs:
            run.text = ''
        if para.runs:
            para.runs[0].text = updated
        else:
            para.add_run(updated)
        changed += 1
    return changed


def remove_pandoc_generated_styles(doc) -> int:
    """Replace Pandoc fallback styles that are not part of the reference DOCX."""
    body_text = _require_style(doc.styles, 'Body Text')
    body_text_char = _require_style(doc.styles, 'Body Text Char')
    changed = 0

    for para in _iter_all_paragraphs(doc):
        p_pr = para._p.find(qn('w:pPr'))
        p_style = p_pr.find(qn('w:pStyle')) if p_pr is not None else None
        if p_style is not None and p_style.get(qn('w:val')) == 'Compact':
            para.style = body_text
            changed += 1

        for run in para.runs:
            r_pr = run._r.find(qn('w:rPr'))
            r_style = r_pr.find(qn('w:rStyle')) if r_pr is not None else None
            if r_style is not None and r_style.get(qn('w:val')) == 'VerbatimChar':
                run.style = body_text_char
                changed += 1

    return changed


def _style_ids(styles) -> set[str]:
    return {
        getattr(style, 'style_id', '')
        for style in styles
        if getattr(style, 'style_id', '')
    }


def purge_styles_not_in_reference(doc, reference_doc_path) -> int:
    """
    Remove generated DOCX style references and style definitions that are not
    present in the reference DOCX.
    """
    if not reference_doc_path:
        return 0
    reference_doc = Document(reference_doc_path)
    allowed_style_ids = _style_ids(reference_doc.styles)
    body_text = _require_style(doc.styles, 'Body Text')
    changed = 0

    for para in _iter_story_paragraphs(doc):
        para_style_id = _paragraph_style_id(para)
        if para_style_id and para_style_id not in allowed_style_ids:
            para.style = body_text
            changed += 1

        for run in para.runs:
            r_pr = run._r.find(qn('w:rPr'))
            r_style = r_pr.find(qn('w:rStyle')) if r_pr is not None else None
            style_id = r_style.get(qn('w:val')) if r_style is not None else ''
            if style_id and style_id not in allowed_style_ids:
                r_pr.remove(r_style)
                changed += 1

    for style in list(doc.styles):
        style_id = getattr(style, 'style_id', '')
        if style_id and style_id not in allowed_style_ids:
            style.delete()
            changed += 1

    return changed


def apply_page_breaks_before_modules_and_units(doc) -> int:
    """Start every Module and Unit heading on a new page."""
    changed = 0
    for para in doc.paragraphs:
        if _paragraph_style_name(para) not in {'Heading 1', 'Heading 2'}:
            continue
        text = _normalize_text(para.text)
        if not (MODULE_HEADING_RE.match(text) or UNIT_HEADING_RE.match(text)):
            continue
        p_pr = para._p.get_or_add_pPr()
        if p_pr.find(qn('w:pageBreakBefore')) is not None:
            continue
        p_pr.append(OxmlElement('w:pageBreakBefore'))
        changed += 1
    return changed


def normalize_module_headings(doc) -> int:
    """Strip unit ranges from module titles while preserving Heading 2 level."""
    heading_2 = _require_style(doc.styles, 'Heading 2')
    changed = 0
    for para in doc.paragraphs:
        text = _normalize_text(para.text)
        if not MODULE_HEADING_RE.match(text):
            continue
        if _paragraph_style_name(para) != 'Heading 2':
            para.style = heading_2
            changed += 1
        cleaned = MODULE_UNIT_RANGE_SUFFIX_RE.sub('', text)
        if cleaned != text and _replace_paragraph_text_preserve_format(para, cleaned):
            changed += 1
    return changed


def _find_unit_tile_prototype(reference_doc_path) -> object | None:
    if not reference_doc_path:
        return None
    ref_path = Path(reference_doc_path)
    if not ref_path.exists():
        return None
    try:
        ref_doc = Document(ref_path)
    except Exception:
        return None
    for table in ref_doc.tables:
        try:
            first = _clean_word_text(table.cell(0, 0).text)
            second = _clean_word_text(table.cell(0, 1).text)
        except Exception:
            continue
        if re.match(r'^(?:U0|U#|#|\d+)$', first) and 'Unit Title' in second:
            return copy.deepcopy(table._tbl)
    return None


def _clear_paragraph(paragraph) -> None:
    for child in list(paragraph._p):
        paragraph._p.remove(child)


def _make_paragraph_normal(paragraph) -> None:
    try:
        paragraph.style = paragraph.part.styles['Normal']
    except Exception:
        pass


def _make_page_break_paragraph_like(paragraph) -> None:
    _make_paragraph_normal(paragraph)
    _clear_paragraph(paragraph)
    _make_paragraph_normal(paragraph)
    p_pr = paragraph._p.get_or_add_pPr()
    spacing = p_pr.find(qn('w:spacing'))
    if spacing is None:
        spacing = OxmlElement('w:spacing')
        p_pr.append(spacing)
    spacing.set(qn('w:before'), '0')
    spacing.set(qn('w:after'), '0')
    if p_pr.find(qn('w:pageBreakBefore')) is None:
        p_pr.append(OxmlElement('w:pageBreakBefore'))


def _hide_heading_paragraph_keep_for_styleref(paragraph) -> None:
    """Hide a heading visually while keeping its text available to STYLEREF."""
    p_pr = paragraph._p.get_or_add_pPr()
    spacing = p_pr.find(qn('w:spacing'))
    if spacing is None:
        spacing = OxmlElement('w:spacing')
        p_pr.append(spacing)
    spacing.set(qn('w:before'), '0')
    spacing.set(qn('w:after'), '0')
    if p_pr.find(qn('w:pageBreakBefore')) is None:
        p_pr.append(OxmlElement('w:pageBreakBefore'))

    r_pr = p_pr.find(qn('w:rPr'))
    if r_pr is None:
        r_pr = OxmlElement('w:rPr')
        p_pr.append(r_pr)
    for tag in ('w:vanish', 'w:specVanish'):
        if r_pr.find(qn(tag)) is None:
            r_pr.append(OxmlElement(tag))

    for run in paragraph.runs:
        run_pr = run._r.get_or_add_rPr()
        for tag in ('w:vanish', 'w:specVanish'):
            if run_pr.find(qn(tag)) is None:
                run_pr.append(OxmlElement(tag))


def _new_unit_tile_table(doc, prototype_tbl):
    if prototype_tbl is None:
        raise RuntimeError(
            'Unit title table prototype was not found in the reference DOCX.'
        )
    return copy.deepcopy(prototype_tbl)


def _replace_cell_text_preserve_format(cell, text: str) -> None:
    """
    Replace visible text without rebuilding the cell content, preserving the
    cloned prototype's table, cell, paragraph, and run formatting.
    """
    text_nodes = cell._tc.findall('.//w:t', NS)
    if not text_nodes:
        cell.paragraphs[0].add_run(text)
        return
    text_nodes[0].text = text
    for node in text_nodes[1:]:
        node.text = ''


def _replace_paragraph_text_preserve_format(paragraph, text: str) -> bool:
    text_nodes = paragraph._p.findall('.//w:t', NS)
    if not text_nodes:
        paragraph.add_run(text)
        return True
    old_text = ''.join(node.text or '' for node in text_nodes)
    if old_text == text:
        return False
    text_nodes[0].text = text
    for node in text_nodes[1:]:
        node.text = ''
    return True


def _set_header_text(header, text: str) -> bool:
    if not text:
        return False
    changed = False
    target = None
    for paragraph in header.paragraphs:
        paragraph_text = _normalize_text(paragraph.text)
        if paragraph_text in {'Module X Title', 'Unit Y Title'}:
            target = paragraph
            break
        if target is None and paragraph_text:
            target = paragraph
    if target is None:
        target = header.paragraphs[0] if header.paragraphs else header.add_paragraph()
    if _replace_paragraph_text_preserve_format(target, text):
        changed = True
    return changed


def _set_header_styleref(header, style_name: str = 'Heading 2') -> bool:
    target = None
    for paragraph in header.paragraphs:
        if _normalize_text(paragraph.text):
            target = paragraph
            break
    if target is None:
        target = header.paragraphs[0] if header.paragraphs else header.add_paragraph()

    p_pr = target._p.find(qn('w:pPr'))
    saved_p_pr = copy.deepcopy(p_pr) if p_pr is not None else None
    for child in list(target._p):
        target._p.remove(child)
    if saved_p_pr is not None:
        target._p.append(saved_p_pr)

    fld = OxmlElement('w:fldSimple')
    fld.set(qn('w:instr'), f'STYLEREF  "{style_name}"  \\* MERGEFORMAT')
    run = OxmlElement('w:r')
    text = OxmlElement('w:t')
    text.text = style_name
    run.append(text)
    fld.append(run)
    target._p.append(fld)
    return True


def _module_unit_contexts(doc) -> list[tuple[str, str]]:
    contexts: list[tuple[str, str]] = []
    current_module = ''
    current_unit = ''
    for para in doc.paragraphs:
        if _paragraph_style_name(para) != 'Heading 2':
            continue
        text = _normalize_text(para.text)
        if text.startswith('Module '):
            current_module = text
            current_unit = ''
            contexts.append((current_module, current_unit))
        elif text.startswith('Unit '):
            current_unit = text
            contexts.append((current_module, current_unit))
    return contexts


def update_running_headers(doc) -> int:
    """Use separate STYLEREF fields for module and unit running headers."""
    changed = 0
    for section in doc.sections:
        section.header.is_linked_to_previous = False
        section.even_page_header.is_linked_to_previous = False
        section.first_page_header.is_linked_to_previous = False
        if _set_header_styleref(section.header, 'Heading 1'):
            changed += 1
        if _set_header_styleref(section.first_page_header, 'Heading 1'):
            changed += 1
        if _set_header_styleref(section.even_page_header, 'Heading 2'):
            changed += 1
    return changed


def replace_unit_headings_with_title_tables(doc, reference_doc_path=None) -> int:
    """
    Replace `Unit N - Title` Heading 2 paragraphs with the reference unit-title
    table prototype. This avoids slow Word COM Quick Part insertion.
    """
    prototype_tbl = _find_unit_tile_prototype(reference_doc_path)
    changed = 0
    for para in list(doc.paragraphs):
        match = UNIT_HEADING_RE.match(_normalize_text(para.text))
        if not match:
            continue

        tbl = _new_unit_tile_table(doc, prototype_tbl)
        para._p.addnext(tbl)
        table = Table(tbl, para._parent)
        _replace_cell_text_preserve_format(table.cell(0, 0), str(int(match.group(1))))
        _replace_cell_text_preserve_format(table.cell(0, 1), match.group(2))
        _make_page_break_paragraph_like(para)
        changed += 1
    return changed


def _iter_body_blocks(doc):
    for child in doc.element.body.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, doc)
        elif isinstance(child, CT_Tbl):
            yield Table(child, doc)


def _is_unit_title_table(table) -> bool:
    try:
        first_row = table.rows[0]
        first_cell = _clean_word_text(first_row.cells[0].text)
    except Exception:
        return False
    return bool(re.match(r'^(?:U)?\d+$', first_cell))


def restore_unit_overview_headings_after_unit_tiles(doc) -> int:
    """
    After unit title Quick Parts are inserted, ensure the following
    `Unit Overview` paragraph keeps its heading style.
    """
    changed = 0
    blocks = list(_iter_body_blocks(doc))
    for index, block in enumerate(blocks[:-1]):
        if not isinstance(block, Table) or not _is_unit_title_table(block):
            continue
        next_block = blocks[index + 1]
        if not isinstance(next_block, Paragraph):
            continue
        if _normalize_text(next_block.text) != 'Unit Overview':
            continue
        if _apply_style_if_available(next_block, 'Heading 3'):
            changed += 1
    return changed


def _can_apply_after_list_to_paragraph(paragraph) -> bool:
    """
    Only apply After List to paragraphs that are still body-like.

    This must not override heading styles or other already-semantic paragraph
    styles coming from Pandoc/reference.docx.
    """
    if _is_heading(paragraph):
        return False
    style_name = getattr(paragraph.style, 'name', '') if paragraph.style else ''
    return style_name in {'Normal', 'Body Text', 'Block Text', 'After List'}


def _is_short_follow_on_context(paragraph) -> bool:
    if _is_heading(paragraph) or _is_list_paragraph(paragraph):
        return False
    style_name = getattr(paragraph.style, 'name', '') if paragraph.style else ''
    return style_name in {'Normal', 'Body Text', 'Block Text', 'After List'}


def _is_module_homework_target(paragraphs, index, text: str) -> bool:
    lowered = text.lower()
    if 'homework target:' not in lowered:
        return False
    if not WORD_COUNT_RE.search(text):
        return False
    prev_para = _find_previous_text_paragraph(paragraphs, index)
    if prev_para is None or not _is_heading(prev_para):
        return False
    style_name = getattr(prev_para.style, 'name', '') if prev_para.style else ''
    return style_name == 'Heading 2'


def _is_neutral_model_example(para, text: str) -> bool:
    """Neutral writing examples arrive from Pandoc as built-in quote styles."""
    if _is_heading(para) or _is_list_paragraph(para):
        return False
    style_name = _paragraph_style_name(para)
    if style_name in NEUTRAL_MODEL_SOURCE_STYLES:
        return True
    if style_name in {'Model', 'Model Bad', 'Model Good'}:
        return False
    return bool(QUOTED_MODEL_RE.match(text))


def apply_semantic_styles(doc):
    """
    Apply semantic paragraph styles that do not require Word COM.

    Quick Parts are handled separately in a Word automation pass so they can be
    inserted as real Building Blocks from the template.
    """
    changed = 0
    paragraphs = list(doc.paragraphs)
    model_mode = None

    for idx, para in enumerate(paragraphs):
        text = _normalize_text(para.text)
        if not text:
            continue

        if text in BAD_MODEL_HEADINGS:
            model_mode = 'bad'
            continue

        if text in GOOD_MODEL_HEADINGS:
            model_mode = 'good'
            continue

        if _is_heading(para):
            model_mode = None
            continue

        if model_mode == 'bad' and _apply_style_if_available(para, 'Model Bad'):
            changed += 1
            model_mode = None
            continue

        if model_mode == 'good' and _apply_style_if_available(para, 'Model Good'):
            changed += 1
            model_mode = None
            continue

        if _is_neutral_model_example(para, text) and _apply_style_if_available(para, 'Model'):
            changed += 1
            continue

        if _is_module_homework_target(paragraphs, idx, text) and _apply_style_if_available(
            para,
            'Homework Target',
        ):
            changed += 1
            continue

        prev_para = _find_previous_text_paragraph(paragraphs, idx)
        if prev_para is not None:
            should_apply_after_list = False
            if _is_list_paragraph(prev_para) and _is_candidate_after_list(text):
                should_apply_after_list = True
            elif _is_short_follow_on_context(prev_para) and _is_candidate_after_text_block(text):
                should_apply_after_list = True

            if (
                should_apply_after_list
                and _can_apply_after_list_to_paragraph(para)
                and _apply_style_if_available(para, 'After List')
            ):
                changed += 1

    return changed


def apply_list_styles(
    doc,
    bullet_style='List Bullet 2',
    number_style='List Number 2',
    alpha_style='List Number 3',
):
    """Apply specific styles to bullet and numbered list paragraphs."""
    num_map = _build_num_format_map(doc)
    styles = doc.styles
    bullet = _get_style_by_name_or_id(styles, bullet_style) or _get_style_by_name_or_id(
        styles,
        bullet_style.replace(' ', ''),
    )
    number = _get_style_by_name_or_id(styles, number_style) or _get_style_by_name_or_id(
        styles,
        number_style.replace(' ', ''),
    )
    alpha = _get_style_by_name_or_id(styles, alpha_style) or _get_style_by_name_or_id(
        styles,
        alpha_style.replace(' ', ''),
    )
    if not bullet:
        raise RuntimeError(f'Required style is missing from the reference DOCX: {bullet_style}')
    if not number:
        raise RuntimeError(f'Required style is missing from the reference DOCX: {number_style}')
    if not alpha:
        raise RuntimeError(f'Required style is missing from the reference DOCX: {alpha_style}')

    applied = 0
    alpha_base_num_id = _num_id_from_style(alpha)
    current_alpha_num_id = None
    expected_alpha_value = None
    for para in doc.paragraphs:
        normalized_text = _normalize_text(para.text)
        alpha_marker = ALPHA_ORDINAL_RE.match(normalized_text)
        p_pr = para._p.find(qn('w:pPr'))
        num_pr = p_pr.find(qn('w:numPr')) if p_pr is not None else None
        if num_pr is not None:
            num_id_el = num_pr.find(qn('w:numId'))
            ilvl_el = num_pr.find(qn('w:ilvl'))
            if num_id_el is None:
                continue
            num_id = num_id_el.get(qn('w:val'))
            ilvl = ilvl_el.get(qn('w:val')) if ilvl_el is not None else '0'
            fmt = None
            if num_id in num_map:
                fmt = num_map[num_id].get(ilvl)
            if fmt == 'bullet' and bullet:
                para.style = bullet
                applied += 1
                continue
            if fmt in {'upperLetter', 'lowerLetter', 'upperAlpha', 'lowerAlpha'}:
                para.style = alpha
                applied += 1
                current_alpha_num_id = num_id
                expected_alpha_value = None
                continue
            if fmt and fmt != 'bullet' and number:
                para.style = number
                applied += 1
                current_alpha_num_id = None
                expected_alpha_value = None
                continue

        if alpha and alpha_marker:
            style_name = getattr(para.style, 'name', '') if para.style else ''
            if not style_name.startswith('Heading'):
                para.style = alpha
                applied += 1
                marker_value = _alpha_marker_start_value(alpha_marker.group(1))
                if (
                    alpha_base_num_id
                    and (current_alpha_num_id is None or expected_alpha_value != marker_value)
                ):
                    current_alpha_num_id = _create_restarted_num_id(
                        doc,
                        alpha_base_num_id,
                        marker_value,
                    )
                if current_alpha_num_id:
                    _apply_direct_num_id(para, current_alpha_num_id)
                expected_alpha_value = marker_value + 1
                continue

        if normalized_text:
            current_alpha_num_id = None
            expected_alpha_value = None
    return applied


def _remove_prefix_from_runs(paragraph, prefix_len: int) -> bool:
    remaining = prefix_len
    changed = False
    for run in paragraph.runs:
        if remaining <= 0:
            break
        text = run.text
        if not text:
            continue
        if len(text) <= remaining:
            run.text = ''
            remaining -= len(text)
            changed = True
            continue
        run.text = text[remaining:]
        remaining = 0
        changed = True
        break
    return changed and remaining == 0


def strip_literal_alpha_markers(doc, alpha_style='List Number 3') -> int:
    """Remove source-text A./B. markers after alphabetic list styling is applied."""
    alpha = _get_style_by_name_or_id(doc.styles, alpha_style) or _get_style_by_name_or_id(
        doc.styles,
        alpha_style.replace(' ', ''),
    )
    if not alpha:
        raise RuntimeError(f'Required style is missing from the reference DOCX: {alpha_style}')

    changed = 0
    alpha_style_id = getattr(alpha, 'style_id', None)
    alpha_style_name = getattr(alpha, 'name', None)
    marker_re = re.compile(r'^\s*[A-Z]\.\s+')
    for para in doc.paragraphs:
        para_style = para.style
        if para_style is None:
            continue
        if (
            getattr(para_style, 'style_id', None) != alpha_style_id
            and getattr(para_style, 'name', None) != alpha_style_name
        ):
            continue
        match = marker_re.match(para.text)
        if not match:
            continue
        if _remove_prefix_from_runs(para, len(match.group(0))):
            changed += 1
    return changed


def _list_winword_pids() -> set[int]:
    try:
        result = subprocess.run(
            ['tasklist', '/FI', 'IMAGENAME eq WINWORD.EXE', '/FO', 'CSV', '/NH'],
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError:
        return set()

    pids: set[int] = set()
    reader = csv.reader(line for line in result.stdout.splitlines() if line.strip())
    for row in reader:
        if len(row) < 2 or row[0].strip('"').upper() == 'INFO:':
            continue
        try:
            pids.add(int(row[1]))
        except ValueError:
            continue
    return pids


def _get_process_id_from_window(hwnd: int) -> int | None:
    if not hwnd:
        return None
    pid = ctypes.c_ulong()
    ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    return int(pid.value or 0) or None


def _get_building_block_entry(word_app, template_path: Path, entry_name: str):
    template = word_app.Templates(str(template_path))
    return template.BuildingBlockEntries(entry_name)


def _get_first_available_building_block_entry(word_app, template_path: Path, entry_names) -> object:
    names = entry_names if isinstance(entry_names, (tuple, list)) else (entry_names,)
    last_exc = None
    for name in names:
        try:
            return _get_building_block_entry(word_app, template_path, name)
        except Exception as exc:
            last_exc = exc
    if last_exc is not None:
        raise last_exc
    raise RuntimeError('No Building Block names were provided.')


def _replace_cell_text(cell, text: str) -> None:
    cell.Range.Text = text


def _insert_building_block_after_paragraph(entry, paragraph, add_page_break=False):
    target_range = paragraph.Range.Duplicate
    target_range.Collapse(WORD_COLLAPSE_END)
    target_range.InsertParagraphAfter()
    try:
        target_range.Style = paragraph.Application.ActiveDocument.Styles('Normal')
    except Exception:
        pass
    if add_page_break:
        try:
            target_range.InsertBreak(WORD_PAGE_BREAK)
            target_range.Style = paragraph.Application.ActiveDocument.Styles('Normal')
        except Exception:
            pass
    target_range.Collapse(WORD_COLLAPSE_END)
    before_start = target_range.Start
    entry.Insert(Where=target_range, RichText=True)
    return before_start


def _find_table_inserted_after_position(doc, position: int):
    for index in range(1, doc.Tables.Count + 1):
        table = doc.Tables(index)
        if table.Range.Start >= position:
            return table
    return None


def _insert_unit_tile_building_block(paragraph, template_path: Path) -> bool:
    match = UNIT_HEADING_RE.match(_clean_word_text(paragraph.Range.Text))
    if not match:
        return False
    paragraph_range = paragraph.Range.Duplicate
    entry = _get_first_available_building_block_entry(
        paragraph.Application,
        template_path,
        BUILDING_BLOCK_NAMES['unit'],
    )
    insert_start = _insert_building_block_after_paragraph(entry, paragraph, add_page_break=True)
    table = _find_table_inserted_after_position(paragraph.Application.ActiveDocument, insert_start)
    if table is None:
        return False
    _replace_cell_text(table.Cell(1, 1), str(int(match.group(1))))
    _replace_cell_text(table.Cell(1, 2), match.group(2))
    paragraph_range.Delete()
    return True


def _can_apply_quick_parts(template_path: Path | None) -> bool:
    return bool(template_path and template_path.exists() and pythoncom is not None and win32com is not None)


def apply_quick_parts(docx_path, template_path: Path | None = None) -> int:
    """
    Insert real Quick Parts using a dedicated Word COM instance.

    Safety rules:
    - check for existing WINWORD.exe processes before automation starts
    - create a fresh Word instance via DispatchEx instead of attaching to an
      existing interactive session
    - close only the document and Word instance created by this function
    - never kill or terminate unrelated WINWORD.exe processes
    """
    if not _can_apply_quick_parts(template_path):
        return 0

    preexisting_pids = _list_winword_pids()
    assert pythoncom is not None
    assert win32com is not None
    pythoncom.CoInitialize()  # pylint: disable=no-member
    word = None
    doc = None
    owned_pid = None
    changes = 0
    try:
        word = win32com.client.DispatchEx('Word.Application')
        word.Visible = False
        word.DisplayAlerts = WORD_ALERTS_NONE
        owned_pid = _get_process_id_from_window(getattr(word, 'Hwnd', 0))
        if owned_pid is not None and owned_pid in preexisting_pids:
            raise RuntimeError(
                'Word automation attached to an existing WINWORD.exe process; aborting Quick Part insertion.'
            )

        doc = word.Documents.Open(str(Path(docx_path).resolve()), AddToRecentFiles=False)
        para_index = doc.Paragraphs.Count
        while para_index >= 1:
            paragraph = doc.Paragraphs(para_index)
            text = _clean_word_text(paragraph.Range.Text)
            if not text:
                para_index -= 1
                continue

            if UNIT_HEADING_RE.match(text):
                if _insert_unit_tile_building_block(paragraph, template_path):
                    changes += 1
                para_index -= 1
                continue

            para_index -= 1

        if changes > 0:
            doc.Save()
        return changes
    finally:
        if doc is not None:
            doc.Close(SaveChanges=WORD_DO_NOT_SAVE_CHANGES)
        if word is not None:
            word.Quit(SaveChanges=WORD_DO_NOT_SAVE_CHANGES)
        if pythoncom is not None:
            getattr(pythoncom, 'CoUninitialize', lambda: None)()


def apply_checklist_style(doc) -> int:
    """Apply Checklist style to list bullet items inside any edit div.

    When Pandoc converts '- [ ]' task list syntax with a reference DOCX that defines
    List Bullet 2, the output is identical to plain '- ' bullets (List Bullet 2 style,
    no checkbox glyph). We therefore apply Checklist style to all List Bullet 2 / List
    Bullet paragraphs that follow any DivLabelEdit paragraph.
    """
    checklist_style = _get_style_by_name_or_id(doc.styles, 'Checklist')
    if not checklist_style:
        return 0

    paragraphs = list(doc.paragraphs)
    changed = 0
    in_edit = False

    for para in paragraphs:
        style_id = _paragraph_style_id(para)

        if style_id == 'DivLabelEdit':
            in_edit = True
            continue

        if in_edit:
            style_name = getattr(para.style, 'name', '') if para.style else ''
            if style_name in ('List Bullet 2', 'List Bullet', 'List Bullet 3'):
                para.style = checklist_style
                changed += 1
            elif _is_heading(para) or (style_id and style_id.startswith('DivLabel')):
                in_edit = False

    return changed


def apply_example_block_styles(doc) -> int:
    """Apply AW Example Good / AW Example Bad body styles to content after div label paragraphs.

    When a DivLabelExampleGood or DivLabelExampleBad label paragraph is found,
    apply the corresponding AW Example Good / AW Example Bad style to immediately
    following Block Text / Body Text paragraphs until the next heading or div label.
    """
    good_style = _get_style_by_name_or_id(doc.styles, 'AW Example Good')
    bad_style = _get_style_by_name_or_id(doc.styles, 'AW Example Bad')
    neutral_style = _get_style_by_name_or_id(doc.styles, 'AW Example')
    if not good_style and not bad_style:
        return 0

    paragraphs = list(doc.paragraphs)
    changed = 0
    target_style = None

    for para in paragraphs:
        style_id = _paragraph_style_id(para)

        if style_id == 'DivLabelExampleGood':
            target_style = good_style
            continue
        if style_id == 'DivLabelExampleBad':
            target_style = bad_style
            continue
        if style_id == 'DivLabelExample':
            target_style = neutral_style
            continue

        if target_style is not None:
            style_name = getattr(para.style, 'name', '') if para.style else ''
            if style_name in NEUTRAL_MODEL_SOURCE_STYLES or bool(QUOTED_MODEL_RE.match(_normalize_text(para.text))):
                para.style = target_style
                changed += 1
            elif _is_heading(para) or (style_id and style_id.startswith('DivLabel')):
                target_style = None
            elif _normalize_text(para.text) and style_name not in ('Body Text', 'Normal'):
                target_style = None

    return changed


def apply_spacing_after_lists(doc, space_before_twips: int = 120) -> int:
    """Add space-before to prose paragraphs that immediately follow list paragraphs.

    Replaces the deleted 'After List' style by injecting w:spacing/@w:before directly,
    creating a visual gap between the last list item and the first prose paragraph.
    Only applies to Body Text / Normal paragraphs that immediately follow a list.
    """
    paragraphs = list(doc.paragraphs)
    changed = 0

    for idx, para in enumerate(paragraphs):
        if not _is_candidate_after_list(_normalize_text(para.text)):
            continue
        if not _can_apply_after_list_to_paragraph(para):
            continue
        prev = _find_previous_text_paragraph(paragraphs, idx)
        if prev is None or not _is_list_paragraph(prev):
            continue

        p_pr = para._p.find(qn('w:pPr'))
        if p_pr is None:
            p_pr = OxmlElement('w:pPr')
            para._p.insert(0, p_pr)
        spacing = p_pr.find(qn('w:spacing'))
        if spacing is None:
            spacing = OxmlElement('w:spacing')
            p_pr.append(spacing)
        current = spacing.get(qn('w:before'))
        if current != str(space_before_twips):
            spacing.set(qn('w:before'), str(space_before_twips))
            changed += 1

    return changed


def apply_table_styles(doc, default_style: str = 'AW Standard Table') -> int:
    """Apply AW Standard Table style to all tables that have no custom style set."""
    table_style = _get_style_by_name_or_id(doc.styles, default_style)
    if not table_style:
        return 0
    changed = 0
    for table in doc.tables:
        try:
            current = table.style.name if table.style else None
            if current in (None, 'Table Normal', 'Normal Table'):
                table.style = table_style
                changed += 1
        except Exception:
            pass
    return changed


def insert_section_after_toc(
    docx_path,
    has_toc=True,
    insert_h1_sections=True,
    reference_doc_path=None,
    apply_semantic_labels=False,
    building_block_template=None,
):
    """
    Post-process `docx_path` to:
    1. If has_toc: insert section break after TOC, restart page numbering at 1,
       remove page numbers from TOC
    2. Insert section breaks before H1 headings
    3. Apply semantic label rendering when apply_semantic_labels=True
    4. Insert Quick Parts with Word COM when available
    """
    doc = Document(docx_path)
    paragraphs = list(doc.paragraphs)

    toc_par_index = None
    if has_toc:
        for index, paragraph in enumerate(paragraphs):
            fld_simples = paragraph._p.findall('.//w:fldSimple', NS)
            for fld in fld_simples:
                instr = fld.get(qn('w:instr')) or fld.get('instr')
                if instr and instr.strip().upper().startswith('TOC'):
                    toc_par_index = index
            fld_chars = paragraph._p.findall('.//w:fldChar', NS)
            if fld_chars:
                instr_texts = paragraph._p.findall('.//w:instrText', NS)
                for instr_text in instr_texts:
                    if instr_text.text and instr_text.text.strip().upper().startswith('TOC'):
                        toc_par_index = index

    made_change = False

    if toc_par_index is not None:
        toc_par = paragraphs[toc_par_index]
        try:
            _apply_next_page_section_to_paragraph(toc_par, start_page=1)
            made_change = True
            print('Inserted section break after TOC with page numbering restart at 1')
        except Exception as exc:
            print(f'Warning: Could not insert section break after TOC: {exc}')

        try:
            doc.save(docx_path)
            doc = Document(docx_path)
            if len(doc.sections) > 0:
                toc_section = doc.sections[0]
                _remove_page_numbers_from_footer(toc_section.footer)
                try:
                    _remove_page_numbers_from_footer(toc_section.first_page_footer)
                except Exception:
                    pass
                print('Removed page numbers from TOC section')
                made_change = True
        except Exception as exc:
            print(f'Warning: Could not remove page numbers from TOC: {exc}')

    module_heading_changes = normalize_module_headings(doc)
    if module_heading_changes > 0:
        print(f'Normalized {module_heading_changes} module heading item(s)')
        made_change = True

    if insert_h1_sections:
        try:
            sections_added = insert_section_breaks_before_h1(
                doc,
                skip_first=has_toc,
                restart_first=not has_toc,
            )
            if sections_added > 0:
                print(f'Inserted {sections_added} section break(s) before H1 headings')
                made_change = True
        except Exception as exc:
            print(f'Warning: Could not insert H1 section breaks: {exc}')

    applied = apply_list_styles(doc)
    if applied > 0:
        print(f'Applied list styles to {applied} paragraph(s)')
        made_change = True

    alpha_marker_changes = strip_literal_alpha_markers(doc)
    if alpha_marker_changes > 0:
        print(f'Removed literal alphabetic markers from {alpha_marker_changes} list paragraph(s)')
        made_change = True

    checklist_changes = apply_checklist_style(doc)
    if checklist_changes > 0:
        print(f'Applied Checklist style to {checklist_changes} item(s)')
        made_change = True

    example_block_changes = apply_example_block_styles(doc)
    if example_block_changes > 0:
        print(f'Applied example block styles to {example_block_changes} paragraph(s)')
        made_change = True

    spacing_changes = apply_spacing_after_lists(doc)
    if spacing_changes > 0:
        print(f'Applied post-list spacing to {spacing_changes} paragraph(s)')
        made_change = True

    table_style_changes = apply_table_styles(doc)
    if table_style_changes > 0:
        print(f'Applied table styles to {table_style_changes} table(s)')
        made_change = True

    if apply_semantic_labels:
        semantic_changes = apply_semantic_styles(doc)
        if semantic_changes > 0:
            print(f'Applied semantic paragraph styles to {semantic_changes} item(s)')
            made_change = True

        div_label_changes = apply_semantic_div_labels(doc, reference_doc_path)
        if div_label_changes > 0:
            print(f'Updated semantic Div labels in {div_label_changes} place(s)')
            made_change = True

    body_text_changes = apply_body_text_to_normal_paragraphs(doc)
    if body_text_changes > 0:
        print(f'Applied Body Text to {body_text_changes} normal paragraph(s)')
        made_change = True

    heading_code_changes = strip_activity_codes_from_headings(doc)
    if heading_code_changes > 0:
        print(f'Removed activity codes from {heading_code_changes} heading(s)')
        made_change = True

    pandoc_style_changes = remove_pandoc_generated_styles(doc)
    if pandoc_style_changes > 0:
        print(f'Replaced Pandoc fallback styles in {pandoc_style_changes} place(s)')
        made_change = True

    purged_style_changes = purge_styles_not_in_reference(doc, reference_doc_path)
    if purged_style_changes > 0:
        print(f'Removed non-reference style usage/definitions in {purged_style_changes} place(s)')
        made_change = True

    page_break_changes = apply_page_breaks_before_modules_and_units(doc)
    if page_break_changes > 0:
        print(f'Applied page breaks before {page_break_changes} module/unit heading(s)')
        made_change = True
        doc.save(docx_path)
        doc = Document(docx_path)

    header_changes = update_running_headers(doc)
    if header_changes > 0:
        print(f'Updated running headers in {header_changes} place(s)')
        made_change = True

    if made_change:
        doc.save(docx_path)

    # Unit title table substitution — runs whenever reference_doc is available,
    # independent of apply_semantic_labels.
    unit_tile_changes = replace_unit_headings_with_title_tables(
        doc,
        reference_doc_path=reference_doc_path,
    )
    if unit_tile_changes > 0:
        doc.save(docx_path)
        print(f'Inserted {unit_tile_changes} unit title table(s)')
        made_change = True
        doc = Document(docx_path)
        restored_headings = restore_unit_overview_headings_after_unit_tiles(doc)
        if restored_headings > 0:
            doc.save(docx_path)
            print(
                f'Restored {restored_headings} Unit Overview heading(s) after unit tiles'
            )

    return made_change


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('docx', help='DOCX file to postprocess')
    parser.add_argument('--toc', action='store_true', default=True, help='Document has TOC')
    parser.add_argument(
        '--reference-doc',
        help='Reference DOCX used as the canonical source for styles and document properties.',
    )
    parser.add_argument(
        '--building-block-template',
        help='Word template containing BuildingBlockEntries used for Quick Part insertion.',
    )
    parser.add_argument(
        '--no-h1-sections',
        action='store_true',
        help='Skip inserting section breaks before H1s',
    )
    parser.add_argument(
        '--apply-semantic-labels',
        action='store_true',
        help=(
            'Apply semantic Div label rendering: insert emoji, set label character styles, '
            'normalize label text, and replace unit headings with title tables (Phase C). '
            'Off by default — structural cleanup runs regardless.'
        ),
    )
    parser.add_argument(
        '--no-semantic-formatting',
        action='store_true',
        help='Deprecated. Semantic formatting is off by default; use --apply-semantic-labels to enable it.',
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    did_update = insert_section_after_toc(
        args.docx,
        has_toc=args.toc,
        insert_h1_sections=not args.no_h1_sections,
        reference_doc_path=args.reference_doc,
        apply_semantic_labels=args.apply_semantic_labels,
        building_block_template=args.building_block_template,
    )

    if did_update:
        print('Post-processing complete.')
    else:
        print('No changes made.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
