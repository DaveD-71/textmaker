"""
Apply the IR reference DOCX's actual teacher-answer-book content styles to
an LTF teacher-answer-book DOCX, matching structural position, since the
LTF markdown source has no fenced Div classes.

Per topic (after "## X.Y. Title" Heading 2):
  - The "Aim:" paragraph and "Target vocabulary:" paragraph -> First Paragraph.
  - "Reading answers:" / "Discussion answers:" label paragraphs -> stay
    Body Text (Pandoc's default fallback, matches the IR reference).
  - Every numbered answer item under those labels -> Compact.
  - The "Confidentiality note:" paragraph -> First Paragraph.

Usage: python apply_ir_teacher_book_styles.py <docx_path> [out_path] [--topics=20]
"""
import sys
from docx import Document


def process(docx_path, out_path, expected_topics=20):
    doc = Document(docx_path)
    styles = doc.styles
    for required in ('First Paragraph', 'Compact'):
        if required not in [s.name for s in styles]:
            raise RuntimeError(f"Reference DOCX is missing required style: {required}")

    paras = doc.paragraphs
    topic_starts = [i for i, p in enumerate(paras) if p.style and p.style.name == 'Heading 2']
    if len(topic_starts) != expected_topics:
        raise RuntimeError(
            f"Expected {expected_topics} topics, found {len(topic_starts)}. Refusing to proceed."
        )

    first_para_count = 0
    compact_count = 0

    for t_idx, start in enumerate(topic_starts):
        end = topic_starts[t_idx + 1] if t_idx + 1 < len(topic_starts) else len(paras)

        in_answer_list = False
        for i in range(start + 1, end):
            p = paras[i]
            text = p.text.strip()

            if text.startswith('Aim:') or text.startswith('Target vocabulary:') or text.startswith('Confidentiality note:'):
                p.style = styles['First Paragraph']
                first_para_count += 1
                in_answer_list = False
                continue

            if text.startswith('Reading answers:') or text.startswith('Discussion answers:'):
                in_answer_list = True
                continue

            if in_answer_list and text:
                p.style = styles['Compact']
                compact_count += 1

    doc.save(out_path)
    print(
        f"Applied First Paragraph to {first_para_count}, Compact to {compact_count} paragraph(s) -> {out_path}"
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
