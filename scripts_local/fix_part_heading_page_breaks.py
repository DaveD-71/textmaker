"""
The IR reference DOCX's Heading 1 style also carries pageBreakBefore, but in
practice a Part heading (Heading 1) is immediately followed by its first
topic (Heading 2) on the SAME page in the actual IR document -- there is no
dedicated, mostly-blank "Part divider" page. Word only forces one page break
at the Heading 1 boundary; the following Heading 2's own pageBreakBefore is
what would trigger a second break immediately after, except Word collapses
adjacent page-break-before headings onto the boundary they share, so it
still looks like one break per Part+topic-1 pair in the source IR book.

For the LTF build, each Part heading is on its own paragraph immediately
before its first topic's Heading 2, and we want them on the SAME page, so
this script removes pageBreakBefore from the paragraph-level formatting of
every Heading 1 paragraph specifically (leaving the Heading 2 style's
setting alone, so topic-to-topic transitions still page-break).

Usage: python fix_part_heading_page_breaks.py <docx_path> [out_path]
"""
import sys
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


def process(docx_path, out_path):
    doc = Document(docx_path)
    changed = 0
    for p in doc.paragraphs:
        if p.style and p.style.name == 'Heading 1':
            ppr = p._p.find(qn('w:pPr'))
            if ppr is None:
                ppr = OxmlElement('w:pPr')
                p._p.insert(0, ppr)
            existing = ppr.find(qn('w:pageBreakBefore'))
            if existing is None:
                existing = OxmlElement('w:pageBreakBefore')
                ppr.append(existing)
            existing.set(qn('w:val'), '0')
            changed += 1
    doc.save(out_path)
    print(f"Disabled pageBreakBefore on {changed} Heading 1 paragraph(s) -> {out_path}")


if __name__ == '__main__':
    docx_path = sys.argv[1]
    out_path = sys.argv[2] if len(sys.argv) > 2 else docx_path
    process(docx_path, out_path)
