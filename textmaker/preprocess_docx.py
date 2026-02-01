"""
Preprocess a DOCX before pandoc conversion to preserve elements pandoc drops.

Approach:
- Mark page/section breaks with sentinel paragraphs.
- Preserve manual line breaks inside paragraphs.
- Expand common fields (REF, PAGEREF, HYPERLINK) into textual markers.
- Add placeholders for shapes/textboxes with alt text.

Sentinels are simple text markers that survive pandoc and are later replaced:
- [[PAGEBREAK]]
- [[SECTIONBREAK]]
- [[LINEBREAK]] inside paragraphs
- [[REF:id|label]] for cross-references
- [[SHAPE:alt text]] for shapes/text boxes carrying text or alt text
"""
from __future__ import annotations

from pathlib import Path
from typing import List

try:
    from docx import Document  # type: ignore[reportMissingImports]
    from docx.oxml import OxmlElement  # type: ignore[reportMissingImports]
    from docx.oxml.ns import qn  # type: ignore[reportMissingImports]
    from docx.text.paragraph import Paragraph  # type: ignore[reportMissingImports]
except ImportError as exc:
    raise RuntimeError('python-docx is required. Install with `pip install python-docx`.') from exc


NS = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
}


def _add_paragraph_after(paragraph, text: str):
    """Insert a paragraph immediately after the given paragraph."""
    new_p = OxmlElement('w:p')
    paragraph._p.addnext(new_p)
    new_para = Paragraph(new_p, paragraph._parent)
    if text:
        new_para.add_run(text)
    return new_para


def _paragraph_has_section_break(paragraph) -> bool:
    p_pr = paragraph._p.find(qn('w:pPr'))
    if p_pr is None:
        return False
    sect = p_pr.find(qn('w:sectPr'))
    if sect is None:
        return False
    type_el = sect.find(qn('w:type'))
    if type_el is None:
        return True  # default is nextPage
    val = type_el.get(qn('w:val'))
    return val in (None, 'nextPage', 'continuous', 'oddPage', 'evenPage')


def _paragraph_has_page_break(paragraph) -> bool:
    # Look for w:br type="page" in runs
    for run in paragraph.runs:
        brs = run._r.findall(qn('w:br'))
        for br in brs:
            if br.get(qn('w:type')) == 'page':
                return True
    return False


def _replace_line_breaks(paragraph):
    """Replace line breaks in runs with [[LINEBREAK]] text tokens."""
    for run in paragraph.runs:
        new_elems: List = []
        for child in list(run._r):
            if child.tag == qn('w:br') and child.get(qn('w:type')) != 'page':
                new_text = OxmlElement('w:t')
                new_text.text = '[[LINEBREAK]]'
                new_elems.append(new_text)
            else:
                new_elems.append(child)
        # Rebuild run children
        for child in list(run._r):
            run._r.remove(child)
        for child in new_elems:
            run._r.append(child)


def _expand_fields(paragraph):
    """Expand common field codes to textual markers."""
    fld_simp = paragraph._p.findall('.//w:fldSimple', NS)
    for fld in fld_simp:
        instr = fld.get(qn('w:instr')) or fld.get('instr') or ''
        instr_up = instr.upper()
        if instr_up.startswith('HYPERLINK '):
            # Leave hyperlinks for pandoc; skip
            continue
        label = instr.replace('"', '').strip()
        marker = f'[[REF:{label}]]'
        paragraph.add_run(marker)

    # Complex fields: gather instrText
    instr_texts = paragraph._p.findall('.//w:instrText', NS)
    for instr_el in instr_texts:
        instr = (instr_el.text or '').strip()
        if not instr:
            continue
        instr_up = instr.upper()
        if instr_up.startswith('REF ') or instr_up.startswith('PAGEREF '):
            ref_id = instr.split()[1] if len(instr.split()) > 1 else instr
            marker = f'[[REF:{ref_id}]]'
            paragraph.add_run(marker)


def _add_shape_placeholders(paragraph):
    """
    Add placeholders for drawing elements that might otherwise be dropped.

    If the paragraph contains drawing/anchor elements with alt text, add [[SHAPE:alt]].
    """
    drawings = paragraph._p.findall('.//w:drawing', NS)
    for drawing in drawings:
        doc_prs = drawing.findall('.//wp:docPr', NS)
        desc = ''
        title = ''
        if doc_prs:
            desc = doc_prs[0].get('descr') or ''
            title = doc_prs[0].get('title') or ''
        alt = desc or title
        alt = alt.strip()
        if alt:
            paragraph.add_run(f'[[SHAPE:{alt}]]')


def preprocess_docx(src: Path, dest: Path) -> Path:
    """Write a preprocessed copy of src to dest with sentinel markers inserted."""
    doc = Document(src)

    for p in list(doc.paragraphs):
        # Mark section breaks and page breaks
        has_section = _paragraph_has_section_break(p)
        has_page_break = _paragraph_has_page_break(p)

        _replace_line_breaks(p)
        _expand_fields(p)
        _add_shape_placeholders(p)

        if has_section:
            _add_paragraph_after(p, '[[SECTIONBREAK]]')
        elif has_page_break:
            _add_paragraph_after(p, '[[PAGEBREAK]]')

    doc.save(dest)
    return dest


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Insert sentinel markers into a DOCX before pandoc.'
    )
    parser.add_argument('input', help='Source DOCX')
    parser.add_argument('output', help='Destination DOCX with markers')
    args = parser.parse_args()

    preprocess_docx(Path(args.input), Path(args.output))
    print(f'Wrote preprocessed DOCX to {args.output}')
