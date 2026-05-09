"""
Post-process a DOCX produced by Pandoc to ensure:
- a section break is inserted immediately after the Table of Contents
- page numbering restarts at 1 for the following section
- page numbers are removed from TOC pages
- section breaks (nextPage) are inserted before each H1 heading
- semantic course formatting is applied consistently using custom styles
- Quick Parts are inserted through Word COM from a real template when available
"""
# pylint: disable=protected-access,broad-exception-caught
import argparse
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
WORD_COUNT_RE = re.compile(
    r'\b(?:approximately|about|around)?\s*\d+\s*(?:[-\u2013\u2014]\s*\d+)?\s*words?\b',
    re.IGNORECASE,
)
UNIT_HEADING_RE = re.compile(r'^Unit\s+(\d+)\s+[-\u2013\u2014]\s+(.+)$')
ALPHA_ORDINAL_RE = re.compile(r'^[A-Z]\.\s+\S+')

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


def _get_style_by_name_or_id(styles, target):
    """Fetch a style by name or style_id; returns None if missing."""
    try:
        return styles[target]
    except Exception:
        pass
    for st in styles:
        if getattr(st, 'name', None) == target or getattr(st, 'style_id', None) == target:
            return st
    return None


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
    return bool(re.match(r'^U\d+$', first_cell))


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

        if model_mode == 'bad' and _apply_style_if_available(para, 'Block Text Bad'):
            changed += 1
            model_mode = None
            continue

        if model_mode == 'good' and _apply_style_if_available(para, 'Block Text Good'):
            changed += 1
            model_mode = None
            continue

        if _is_module_homework_target(paragraphs, idx, text) and _apply_style_if_available(
            para,
            'Homework Words',
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


def apply_list_styles(doc, bullet_style='List Bullet 2', number_style='List Number 2'):
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
    if not bullet and not number:
        return 0

    applied = 0
    for para in doc.paragraphs:
        normalized_text = _normalize_text(para.text)
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
            if fmt and fmt != 'bullet' and number:
                para.style = number
                applied += 1
                continue

        if number and ALPHA_ORDINAL_RE.match(normalized_text):
            style_name = getattr(para.style, 'name', '') if para.style else ''
            if not style_name.startswith('Heading'):
                para.style = number
                applied += 1
    return applied


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
    _replace_cell_text(table.Cell(1, 1), f'U{int(match.group(1))}')
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
    pythoncom.CoInitialize()
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
        pythoncom.CoUninitialize()


def insert_section_after_toc(
    docx_path,
    has_toc=True,
    insert_h1_sections=True,
    reference_doc_path=None,
    semantic_formatting=True,
    building_block_template=None,
):
    """
    Post-process `docx_path` to:
    1. If has_toc: insert section break after TOC, restart page numbering at 1,
       remove page numbers from TOC
    2. Insert section breaks before H1 headings
    3. Apply semantic paragraph styles with python-docx
    4. Insert Quick Parts with Word COM when available
    """
    del reference_doc_path
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

    try:
        applied = apply_list_styles(doc)
        if applied > 0:
            print(f'Applied list styles to {applied} paragraph(s)')
            made_change = True
    except Exception as exc:
        print(f'Warning: Could not apply list styles: {exc}')

    if semantic_formatting:
        try:
            semantic_changes = apply_semantic_styles(doc)
            if semantic_changes > 0:
                print(f'Applied semantic paragraph styles to {semantic_changes} item(s)')
                made_change = True
        except Exception as exc:
            print(f'Warning: Could not apply semantic paragraph styles: {exc}')

    if made_change:
        doc.save(docx_path)

    if semantic_formatting:
        try:
            quick_part_changes = apply_quick_parts(
                docx_path,
                template_path=Path(building_block_template) if building_block_template else DEFAULT_BUILDING_BLOCK_TEMPLATE,
            )
            if quick_part_changes > 0:
                print(f'Inserted {quick_part_changes} Quick Part block(s)')
                made_change = True
                doc = Document(docx_path)
                restored_headings = restore_unit_overview_headings_after_unit_tiles(doc)
                if restored_headings > 0:
                    doc.save(docx_path)
                    print(
                        f'Restored {restored_headings} Unit Overview heading(s) after unit tiles'
                    )
        except Exception as exc:
            print(f'Warning: Could not insert Quick Parts: {exc}')

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
        '--no-semantic-formatting',
        action='store_true',
        help='Skip semantic textbook formatting rules.',
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
        semantic_formatting=not args.no_semantic_formatting,
        building_block_template=args.building_block_template,
    )

    if did_update:
        print('Post-processing complete.')
    else:
        print('No changes made.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
