"""
Apply the IR reference DOCX's actual content paragraph styles to an LTF
student-edition DOCX, matching structural position (heading-relative),
since the LTF markdown source has no fenced Div classes to drive Pandoc's
style_bridge.lua mapping automatically.

Per topic, after Pandoc conversion + generic Body Text normalization:
  - Reading body paragraphs (between "### X.Y.2. Reading" and the next
    Heading 3) -> `article_body_text`.
  - The first paragraph after "### X.Y.3. Vocabulary Focus" (the
    New terms / Recycled terms line(s)) -> `First Paragraph`. If there
    are two paragraphs (New terms, then Recycled terms), only the very
    first one is First Paragraph in the IR reference; the rest stay
    article_body_text-equivalent (kept as Body Text, since the reference
    doesn't show a second distinct style for it).
  - Every paragraph under "Reading Questions", "Discussion Questions",
    and "Source Notes" headings -> `Compact` (hanging-indent numbered
    list look).

Usage: python apply_ir_content_styles.py <docx_path> [out_path] [--topics=20]
"""
import sys
from docx import Document


HEADING_SUFFIXES_COMPACT = ('. Reading Questions', '. Discussion Questions', '. Source Notes')


def process(docx_path, out_path, expected_topics=20):
    doc = Document(docx_path)
    styles = doc.styles
    for required in ('article_body_text', 'First Paragraph', 'Compact'):
        if required not in [s.name for s in styles]:
            raise RuntimeError(f"Reference DOCX is missing required style: {required}")

    paras = doc.paragraphs
    topic_starts = [
        i for i, p in enumerate(paras)
        if p.style and p.style.name == 'Heading 2' and 'How This Resource Is Organized' not in p.text
    ]
    if len(topic_starts) != expected_topics:
        raise RuntimeError(
            f"Expected {expected_topics} topics, found {len(topic_starts)}. Refusing to proceed."
        )

    body_count = 0
    first_para_count = 0
    compact_count = 0

    for t_idx, start in enumerate(topic_starts):
        end = topic_starts[t_idx + 1] if t_idx + 1 < len(topic_starts) else len(paras)

        # Map each Heading 3 in this topic's range to its index and text.
        h3_indices = [i for i in range(start, end) if paras[i].style and paras[i].style.name == 'Heading 3']

        # Match by heading text suffix, avoiding ambiguity with "Reading Questions".
        reading_h3 = None
        vocab_h3 = None
        rq_h3 = None
        dq_h3 = None
        sn_h3 = None
        for i in h3_indices:
            text = paras[i].text
            if text.endswith('. Reading'):
                reading_h3 = i
            elif text.endswith('. Vocabulary Focus'):
                vocab_h3 = i
            elif text.endswith('. Reading Questions'):
                rq_h3 = i
            elif text.endswith('. Discussion Questions'):
                dq_h3 = i
            elif text.endswith('. Source Notes'):
                sn_h3 = i

        if reading_h3 is None or vocab_h3 is None:
            print(f"  SKIP topic at para {start}: missing Reading/Vocabulary Focus heading")
            continue

        # Reading body: paragraphs strictly between reading_h3 and vocab_h3.
        for i in range(reading_h3 + 1, vocab_h3):
            if paras[i].style and paras[i].style.name != 'Heading 3':
                paras[i].style = styles['article_body_text']
                body_count += 1

        # First paragraph after Vocabulary Focus heading.
        if vocab_h3 + 1 < end and paras[vocab_h3 + 1].style.name != 'Heading 3':
            paras[vocab_h3 + 1].style = styles['First Paragraph']
            first_para_count += 1

        # Compact for Reading Questions / Discussion Questions / Source Notes bodies.
        for section_h3 in (rq_h3, dq_h3, sn_h3):
            if section_h3 is None:
                continue
            # find the next heading (of any level) after this one, within [start, end)
            next_heading = end
            for i in range(section_h3 + 1, end):
                if paras[i].style and paras[i].style.name.startswith('Heading'):
                    next_heading = i
                    break
            for i in range(section_h3 + 1, next_heading):
                paras[i].style = styles['Compact']
                compact_count += 1

    doc.save(out_path)
    print(
        f"Applied article_body_text to {body_count}, First Paragraph to {first_para_count}, "
        f"Compact to {compact_count} paragraph(s) -> {out_path}"
    )


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    expected_topics = 20
    for a in sys.argv[1:]:
        if a.startswith('--topics='):
            expected_topics = int(a.split('=', 1)[1])
    docx_path = args[0]
    out_path = args[1] if len(args) > 1 else docx_path
    process(docx_path, out_path, expected_topics=expected_topics)
