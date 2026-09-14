"""
Transform a merged LTF student-edition markdown file for final-output
conversion: drop the "**Recycled terms:**" line entirely and the
"**New terms:**" label prefix from each topic's Vocabulary Focus section,
leaving one plain comma-separated term list -- matching the IR reference
book's actual final format (confirmed by direct inspection: the IR DOCX's
Vocabulary Focus paragraphs are a single unlabeled list with no recycled
terms shown).

This does NOT touch the per-article .md source files in drafts/articles/
(which keep New/Recycled terms for vocabulary-map.md tracking and QA) --
it only transforms the already-merged output file used for the DOCX build.

Usage: python build_ltf_student_edition_md.py <merged_md_path> [out_path]
Defaults out_path to merged_md_path (in place).
"""
import re
import sys


def transform(text: str) -> str:
    def replace_vocab_block(match: 're.Match') -> str:
        new_terms_line = match.group('new_terms').strip()
        return new_terms_line

    vocab_pattern = re.compile(
        r'\*\*New terms:\*\*\s*(?P<new_terms>.+?)\n\n\*\*Recycled terms:\*\*[^\n]*',
        re.DOTALL,
    )
    transformed, vocab_count = vocab_pattern.subn(replace_vocab_block, text)
    print(f"Replaced {vocab_count} Vocabulary Focus block(s)")

    def linkify_source_note(match: 're.Match') -> str:
        prefix = match.group('prefix').rstrip()
        url = match.group('url')
        # Strip a trailing em-dash/hyphen separator from the prefix, keep the rest.
        prefix = re.sub(r'\s*[—\-]\s*$', '', prefix)
        return f'{prefix}  \n[{url}]({url})'

    source_note_pattern = re.compile(
        r'^(?P<prefix>\d+\.\s+.+?)[ \t]*[—\-][ \t]*(?P<url>https?://\S+)[ \t]*$',
        re.MULTILINE,
    )
    transformed, url_count = source_note_pattern.subn(linkify_source_note, transformed)
    print(f"Linkified {url_count} Source Note URL(s)")

    return transformed


if __name__ == '__main__':
    md_path = sys.argv[1]
    out_path = sys.argv[2] if len(sys.argv) > 2 else md_path
    source = open(md_path, encoding='utf-8').read()
    result = transform(source)
    with open(out_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(result)
    print(f"Wrote {out_path}")
