"""
Add a centered "p. [PAGE]" footer to every section of an LTF DOCX, matching
the IR reference doc's footer exactly (Footer style, centered, "p." literal
text followed by a PAGE field).

OOXML footers cascade: a section without its own footerReference continues
using the nearest preceding section's footer. So it is enough to set the
footer content once, on doc.sections[0] via python-docx's `footer` property
(which creates a footerReference automatically the first time it's touched)
-- python-docx handles the relationship wiring; we only need to set content.

The IR reference doc leaves its title-page section (section 0, the front
matter before Part 1) with no footer at all, and sets the "p. [PAGE]"
footer starting from section 1 onward. This script replicates that: it
skips the title page and sets the footer starting at the first section
whose content is NOT the front matter (i.e. section index 1, assuming the
front matter is a single un-split section, which is the case for our
student-edition build before the per-topic 2-column sections are inserted
-- run this BEFORE add_two_column_reading_sections.py, or pass
--start-section explicitly if the section count has already changed).

Usage: python add_page_number_footer.py <docx_path> [out_path] [--start-section=1]
"""
import sys
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx import Document


def _clear_paragraph_content(paragraph) -> None:
    for child in list(paragraph._p):
        if child.tag != qn('w:pPr'):
            paragraph._p.remove(child)


def _add_page_field(paragraph) -> None:
    fld_simple = OxmlElement('w:fldSimple')
    fld_simple.set(qn('w:instr'), 'PAGE')
    run_elem = OxmlElement('w:r')
    run_elem.append(fld_simple)
    paragraph._p.append(run_elem)


def process(docx_path, out_path, start_section=1):
    doc = Document(docx_path)
    if 'Footer' not in [s.name for s in doc.styles]:
        raise RuntimeError("Reference DOCX has no 'Footer' style")
    footer_style = doc.styles['Footer']

    if start_section >= len(doc.sections):
        raise RuntimeError(
            f"start_section={start_section} is out of range; document has only {len(doc.sections)} section(s)"
        )

    section = doc.sections[start_section]
    section.footer.is_linked_to_previous = False
    para = section.footer.paragraphs[0]
    _clear_paragraph_content(para)
    para.style = footer_style
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    para.add_run('p. ')
    _add_page_field(para)

    doc.save(out_path)
    print(
        f"Added centered page-number footer to section {start_section} "
        f"(title page section 0 stays footer-free, cascades to all later sections) -> {out_path}"
    )


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    start_section = 1
    for a in sys.argv[1:]:
        if a.startswith('--start-section='):
            start_section = int(a.split('=', 1)[1])
    docx_path = args[0]
    out_path = args[1] if len(args) > 1 else docx_path
    process(docx_path, out_path, start_section=start_section)
