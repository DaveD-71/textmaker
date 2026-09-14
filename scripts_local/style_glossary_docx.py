"""
Restyle an LTF glossary DOCX to match the IR project's glossary layout exactly:

  - Every entry paragraph (everything after the "Terms" heading) gets the
    `glossary_para` paragraph style from the reference DOCX (Noto Serif Light,
    justified, tight space-after) instead of the generic Body Text Pandoc
    fallback.
  - The whole entry list is wrapped in a single CONTINUOUS 2-column section,
    matching `Investor Relations Resource - Glossary.docx`'s own structure
    (front matter single-column, then one 2-column section spanning every
    entry through the last one).

Usage: python style_glossary_docx.py <docx_path> [out_path]
"""
import copy
import sys
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


def _get_body_sectpr(doc):
    body = doc.element.body
    return body.find(qn('w:sectPr'))


def _make_sectpr(base_sectpr, *, section_type, cols_num=None):
    new = copy.deepcopy(base_sectpr)
    for tag in ('w:type', 'w:cols', 'w:headerReference', 'w:footerReference', 'w:pgNumType'):
        for el in new.findall(qn(tag)):
            new.remove(el)
    type_el = OxmlElement('w:type')
    type_el.set(qn('w:val'), section_type)
    new.insert(0, type_el)
    cols_el = OxmlElement('w:cols')
    if cols_num and cols_num > 1:
        cols_el.set(qn('w:num'), str(cols_num))
        cols_el.set(qn('w:space'), '567')
    else:
        cols_el.set(qn('w:space'), '720')
    new.append(cols_el)
    return new


def _set_paragraph_sectpr(paragraph, sectpr_el):
    ppr = paragraph._p.find(qn('w:pPr'))
    if ppr is None:
        ppr = OxmlElement('w:pPr')
        paragraph._p.insert(0, ppr)
    existing = ppr.find(qn('w:sectPr'))
    if existing is not None:
        ppr.remove(existing)
    ppr.append(sectpr_el)


def process_glossary(docx_path, out_path):
    doc = Document(docx_path)
    base_sectpr = _get_body_sectpr(doc)
    if base_sectpr is None:
        raise RuntimeError("Could not find document body sectPr to use as a geometry template")

    if 'glossary_para' not in [s.name for s in doc.styles]:
        raise RuntimeError(
            "Reference DOCX has no 'glossary_para' style; this script only works "
            "when converted with the IR Glossary reference doc."
        )
    glossary_para_style = doc.styles['glossary_para']

    paras = doc.paragraphs

    # Find the "Terms" heading (Heading 2) that precedes all entries.
    terms_heading_idx = None
    for i, p in enumerate(paras):
        if p.style and p.style.name == 'Heading 2' and p.text.strip() == 'Terms':
            terms_heading_idx = i
            break
    if terms_heading_idx is None:
        raise RuntimeError("Could not find the 'Terms' Heading 2 paragraph")

    entry_start = terms_heading_idx + 1
    entry_end = len(paras)  # last entry runs to end of document

    if entry_start >= entry_end:
        raise RuntimeError("No glossary entry paragraphs found after 'Terms' heading")

    restyled = 0
    for i in range(entry_start, entry_end):
        paras[i].style = glossary_para_style
        restyled += 1

    # Close the single-column section right before the entries start (on the
    # paragraph immediately before entry_start, i.e. the "Terms" heading itself
    # stays in the single-column section with the front matter).
    sectpr_single = _make_sectpr(base_sectpr, section_type='continuous', cols_num=1)
    _set_paragraph_sectpr(paras[terms_heading_idx], sectpr_single)

    # The last entry paragraph carries no new sectPr of its own; the document's
    # existing body-level sectPr (already 2-col via base_sectpr? no -- base is
    # whatever the last section was) must become the 2-column closing section.
    body = doc.element.body
    body_sectpr = body.find(qn('w:sectPr'))
    new_body_sectpr = _make_sectpr(base_sectpr, section_type='continuous', cols_num=2)
    body.replace(body_sectpr, new_body_sectpr)

    if restyled != entry_end - entry_start:
        raise RuntimeError(f"Expected to restyle {entry_end - entry_start} paragraphs, restyled {restyled}")

    doc.save(out_path)
    print(f"Restyled {restyled} entry paragraph(s) to glossary_para, wrapped in a 2-column section -> {out_path}")


if __name__ == '__main__':
    docx_path = sys.argv[1]
    out_path = sys.argv[2] if len(sys.argv) > 2 else docx_path
    process_glossary(docx_path, out_path)
