"""
Post-process markdown produced by docx_to_markdown to restore sentinel markers.

Transforms:
- [[PAGEBREAK]] -> \\pagebreak
- [[SECTIONBREAK]] -> \\pagebreak (section semantics are not in markdown; page break is the closest analogue)
- [[LINEBREAK]] -> <br>
- [[REF:id|label]] or [[REF:id]] -> textual reference placeholder
- [[SHAPE:alt]] -> italic placeholder to note missing shape
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable


PAGEBREAK = r'\\pagebreak'


def _replace_markers(text: str) -> str:
    text = text.replace('[[PAGEBREAK]]', PAGEBREAK)
    text = text.replace('[[SECTIONBREAK]]', PAGEBREAK)
    text = text.replace('[[LINEBREAK]]', '<br>')

    def _ref_repl(match):
        ref_id = match.group(1) or ''
        label = match.group(2) or ''
        if label:
            return f'{label} (ref: {ref_id})'
        return f'[{ref_id}]'

    text = re.sub(r'\[\[REF:([^\]|]+)\|?([^\]]*)\]\]', _ref_repl, text)

    def _shape_repl(match):
        alt = match.group(1).strip()
        return f'*[shape: {alt}]*' if alt else '*[shape]*'

    text = re.sub(r'\[\[SHAPE:([^\]]*)\]\]', _shape_repl, text)
    return text


def postprocess_markdown_file(path: Path) -> None:
    text = path.read_text(encoding='utf-8')
    new_text = _replace_markers(text)
    path.write_text(new_text, encoding='utf-8')


def postprocess_many(paths: Iterable[Path]) -> None:
    for p in paths:
        postprocess_markdown_file(p)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Replace sentinel markers in markdown outputs.')
    parser.add_argument('files', nargs='+', help='Markdown files to post-process')
    args = parser.parse_args()

    postprocess_many([Path(p) for p in args.files])
