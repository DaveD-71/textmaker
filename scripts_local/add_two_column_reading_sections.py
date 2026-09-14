"""
Insert per-topic 2-column section breaks into an LTF student-edition DOCX,
matching the IR project's exact pattern (see
`books/_lets-talk-finance-shared/house-style.md` section 1.4):

  - Section ends right after "### X.Y.2. Reading" heading paragraph
    (closes the single-column section that held the topic title + Goal).
  - A new CONTINUOUS section, cols=2, opens and spans the Reading body
    paragraphs, closing right after the LAST paragraph of the Reading
    (i.e. right before "### X.Y.3. Vocabulary Focus").
  - A new CONTINUOUS section, cols=1 (default), opens for Vocabulary Focus
    onward, running through Reading/Discussion Questions and Source Notes,
    until the next topic's Heading 2 (or end of document).

Section break is implemented the python-docx way: give the LAST paragraph
of the section a sectPr in its pPr (this is what closes that section);
the following paragraph starts the next section implicitly.

Usage: python add_two_column_reading_sections.py <docx_path> [out_path] [--topics N]
Defaults out_path to docx_path (in place) and expected topic count to 20.
"""
import copy
import sys
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


def _get_body_sectpr(doc):
    """The document's final sectPr (body-level, not paragraph-level)."""
    body = doc.element.body
    return body.find(qn('w:sectPr'))


def _make_sectpr(base_sectpr, *, section_type, cols_num=None):
    """Clone a base sectPr's page geometry and set type + column count."""
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


def process_book(docx_path, out_path, expected_topics=20):
    doc = Document(docx_path)
    base_sectpr = _get_body_sectpr(doc)
    if base_sectpr is None:
        raise RuntimeError("Could not find document body sectPr to use as a geometry template")

    paras = doc.paragraphs

    # Identify topic Heading 2 boundaries (## X.Y. Title -> Heading 2 style), excluding the
    # front-matter "How This Resource Is Organized" pseudo-topic (no Reading/Vocabulary Focus).
    topic_starts = [
        i for i, p in enumerate(paras)
        if p.style and p.style.name == 'Heading 2' and 'How This Resource Is Organized' not in p.text
    ]
    if not topic_starts:
        raise RuntimeError("No Heading 2 (topic) paragraphs found")
    if len(topic_starts) != expected_topics:
        raise RuntimeError(
            f"Expected {expected_topics} topics, found {len(topic_starts)} Heading 2 paragraphs. "
            "Refusing to proceed with a mismatched document structure."
        )

    inserted = 0
    for t_idx, start in enumerate(topic_starts):
        end = topic_starts[t_idx + 1] if t_idx + 1 < len(topic_starts) else len(paras)

        reading_heading_idx = None
        vocab_heading_idx = None
        for i in range(start, end):
            p = paras[i]
            if p.style and p.style.name == 'Heading 3':
                if '. Reading' in p.text and reading_heading_idx is None:
                    reading_heading_idx = i
                elif '. Vocabulary Focus' in p.text and vocab_heading_idx is None:
                    vocab_heading_idx = i

        if reading_heading_idx is None or vocab_heading_idx is None:
            print(f"  SKIP topic at para {start} ({paras[start].text!r}): could not find Reading/Vocabulary Focus headings")
            continue

        close_single_at = reading_heading_idx
        close_two_col_at = vocab_heading_idx - 1

        if close_two_col_at <= close_single_at:
            print(f"  SKIP topic at para {start}: no Reading body paragraphs between heading and Vocabulary Focus")
            continue

        sectpr_single = _make_sectpr(base_sectpr, section_type='continuous', cols_num=1)
        sectpr_twocol = _make_sectpr(base_sectpr, section_type='continuous', cols_num=2)

        _set_paragraph_sectpr(paras[close_single_at], sectpr_single)
        _set_paragraph_sectpr(paras[close_two_col_at], sectpr_twocol)
        inserted += 2

    expected_breaks = expected_topics * 2
    if inserted != expected_breaks:
        raise RuntimeError(
            f"Expected {expected_breaks} section breaks ({expected_topics} topics x 2), "
            f"only inserted {inserted}. Refusing to save a partially-processed document."
        )

    doc.save(out_path)
    print(f"Inserted {inserted} section breaks ({inserted // 2} topics) -> {out_path}")


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    expected_topics = 20
    for a in sys.argv[1:]:
        if a.startswith('--topics='):
            expected_topics = int(a.split('=', 1)[1])
    docx_path = args[0]
    out_path = args[1] if len(args) > 1 else docx_path
    process_book(docx_path, out_path, expected_topics=expected_topics)
