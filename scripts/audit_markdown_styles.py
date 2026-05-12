"""
Audit and normalize Markdown paragraph patterns before DOCX conversion.

The audit groups similar paragraph types by structure and title pattern so
format drift is visible before Pandoc and DOCX post-processing run.
"""
from __future__ import annotations

import argparse
import csv
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

try:
    from docx import Document  # type: ignore[reportMissingImports]
except ImportError:  # pragma: no cover - audit can still run in markdown-only mode
    Document = None


HEADING_RE = re.compile(r'^(#{1,6})\s+(.+?)\s*$')
BOLD_ONLY_RE = re.compile(r'^\*\*(.+?)\*\*\s*$')
DIV_OPEN_RE = re.compile(r'^:::\s*([A-Za-z0-9_-]+)?\s*$')
DIV_CLOSE_RE = re.compile(r'^:::\s*$')
NUMBERED_RE = re.compile(r'^(\d+)\.\s+(.+)$')
ALPHA_RE = re.compile(r'^([A-Z])\.\s+(.+)$')
BULLET_RE = re.compile(r'^[-*]\s+(.+)$')
TABLE_LIKE_BULLET_RE = re.compile(r'^[-*]\s+([^:]{3,48}):\s+(.+)$')
ACTIVITY_CODE_RE = re.compile(r'\s+\(([A-H]\d)(?:[^)]*)\)\s*(?:[★*])?\s*$')
PLACEHOLDER_RE = re.compile(r'\{\{PH-[^}]+}}')
HORIZONTAL_RULE_RE = re.compile(r'^\s{0,3}(?:-{3,}|\*{3,}|_{3,})\s*$')

TITLE_KEYWORDS = (
    'practice',
    'task',
    'exercise',
    'activity',
    'analysis',
    'compare',
    'checklist',
    'questions',
    'writing',
    'rewriting',
    'revision',
    'review',
    'editing',
    'model',
    'phrases',
    'problem',
    'template',
    'scenario',
    'sentence',
    'paragraph',
    'extension',
    'transformation',
)


@dataclass
class ParagraphRecord:
    line: int
    kind: str
    paragraph_type: str
    subtype: str
    form: str
    text: str
    style: str = ''
    source: str = 'markdown'


def normalize_title(text: str) -> str:
    text = re.sub(r'\s+', ' ', text.strip())
    text = ACTIVITY_CODE_RE.sub('', text).strip()
    text = text.replace('—', '-').replace('–', '-')
    text = re.sub(r'^\d+\.\s+', '', text)
    text = re.sub(r'\b[A-Z]\d\b', 'CODE', text)
    text = re.sub(r'\b\d+\b', 'N', text)
    return text.lower()


def strip_markdown_inline(text: str) -> str:
    text = re.sub(r'^\s*#+\s+', '', text.strip())
    bold = BOLD_ONLY_RE.match(text)
    if bold:
        text = bold.group(1)
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    text = re.sub(r'\*([^*]+)\*', r'\1', text)
    return text.strip()


def title_subtype(text: str, form_hint: str = '') -> str:
    title = strip_markdown_inline(text)
    title_no_code = ACTIVITY_CODE_RE.sub('', title).strip()
    lowered = title_no_code.lower()
    hint = form_hint.lower().replace(' ', '').replace('-', '')
    if re.match(r'^module\s+\d+\b', lowered):
        return 'module title'
    if re.match(r'^unit\s+\d+\b', lowered) and hint in {'heading2', ''}:
        return 'unit title'
    if lowered in {'module introduction', 'unit overview'}:
        return 'overview heading'
    if re.match(r'^[a-h]\.\s+', lowered):
        if hint in {'heading4', 'heading5'}:
            return 'alphabetic subskill heading'
        return 'unit section heading'
    if re.match(r'^(practice|task)\s+[a-z]\b', lowered):
        return 'practice/task heading'
    if 'guided skill practice' in lowered:
        return 'guided skill heading'
    if 'model revision practice' in lowered or 'model rewriting' in lowered:
        return 'model revision heading'
    if 'self-editing checklist' in lowered or 'final revision audit' in lowered:
        return 'checklist heading'
    if 'peer review' in lowered or 'structured feedback' in lowered:
        return 'peer review heading'
    if 'editing' in lowered or 'track-change' in lowered:
        return 'editing heading'
    if 'homework' in lowered:
        return 'homework heading'
    if 'extension' in lowered:
        return 'extension heading'
    if 'learn' in lowered:
        return 'learn label/title'
    if 'worked example' in lowered:
        return 'worked example label/title'
    if 'rubric' in lowered:
        return 'rubric heading'
    if lowered.startswith(('original text', 'revised text', 'original version', 'revised version')):
        return 'model text label/title'
    if re.match(r'^(pattern|step)\s+\d+', lowered) or re.match(r'^\d+\.\s+', title):
        return 'numbered subskill heading'
    if lowered.endswith(':'):
        return 'colon label/title'
    if is_activity_title(title_no_code):
        return 'activity heading'
    return 'other title'


def label_detail_subtype(text: str) -> str:
    stripped = strip_markdown_inline(text)
    bullet_match = TABLE_LIKE_BULLET_RE.match(stripped)
    if bullet_match:
        label = bullet_match.group(1).lower()
    elif ':' in stripped:
        label = stripped.split(':', 1)[0].lower()
    else:
        return 'other label-detail'
    if re.match(r'sentence\s+\d+', label):
        return 'sentence pattern row'
    if label == 'homework target':
        return 'homework target row'
    if label in {'reflect', 'then discuss', 'discuss', 'now discuss', 'identify', 'functions', 'audiences'}:
        return 'prompt/list-introduction row'
    if label.startswith(('version ', 'direct', 'unsequenced', 'vague instruction', 'procedural instruction', 'bare announcement', 'overgeneralised', 'meeting-note wording')):
        return 'model/example row'
    if re.match(r'(step|stage|part)\s+\d+', label):
        return 'step/stage row'
    if label in {'original', 'revised', 'dense', 'segmented', 'loose justification'}:
        return 'model contrast row'
    if 'office' in label or 'source' in label or 'email' in label:
        return 'source/input row'
    return 'label-detail row'


def classify_function(text: str, form_hint: str = '') -> tuple[str, str]:
    stripped = text.strip()
    plain = strip_markdown_inline(stripped)
    lowered = plain.lower()
    hint = form_hint.lower().replace(' ', '')
    if not plain:
        return 'blank', 'blank'
    if HORIZONTAL_RULE_RE.match(stripped):
        return 'document boundary', 'horizontal rule'
    if DIV_OPEN_RE.match(stripped) or DIV_CLOSE_RE.match(stripped):
        return 'div boundary', 'div boundary'
    if hint.startswith('heading'):
        return 'title/heading', title_subtype(stripped, form_hint)
    if hint.startswith('listnumber'):
        return 'list item', 'numbered item'
    if hint.startswith('listbullet'):
        if ':' in plain and len(plain) <= 180:
            return 'table-like content', label_detail_subtype(plain)
        return 'list item', 'bullet item'
    if hint in {
        'learnnote',
        'learnprocess',
        'learnlanguage',
        'learnprinciple',
        'learntransfer',
        'learnteaching',
        'modebad',
        'modelbad',
        'modelgood',
        'workedexample',
        'selfstudy',
        'annotation',
        'example',
        'placeholder',
    }:
        return 'semantic block content', form_hint
    if stripped.startswith('|') and stripped.endswith('|'):
        return 'table row', 'markdown table row'
    if HEADING_RE.match(stripped) or BOLD_ONLY_RE.match(stripped):
        return 'title/heading', title_subtype(stripped, form_hint)
    if stripped.startswith('**') and ':' in stripped:
        return 'semantic label paragraph', title_subtype(stripped, form_hint)
    if PLACEHOLDER_RE.search(stripped):
        return 'placeholder', 'placeholder line'
    if lowered.startswith(('use this space', 'revise the text above', 'then explain', 'write your')):
        return 'writing space/prompt', 'response-space instruction'
    if lowered.startswith(('read the following', 'choose the most', 'below are', 'before submitting')):
        return 'instruction/prompt', 'activity instruction'
    if ALPHA_RE.match(stripped):
        return 'list item', 'alphabetic option item'
    if NUMBERED_RE.match(stripped):
        number = NUMBERED_RE.match(stripped).group(1)
        return 'list item', 'numbered item starts at 1' if number == '1' else 'numbered item continuation'
    if BULLET_RE.match(stripped):
        if TABLE_LIKE_BULLET_RE.match(stripped):
            return 'table-like content', label_detail_subtype(stripped)
        return 'list item', 'bullet item'
    if ':' in plain and len(plain) <= 180:
        return 'label/detail paragraph', label_detail_subtype(plain)
    if lowered.startswith(('reflect:', 'then discuss:', 'discuss:', 'now discuss:', 'for each', 'choose one')):
        return 'instruction/prompt', 'short prompt'
    if len(plain) <= 140 and not plain.endswith('.'):
        return 'instruction/prompt', 'short instruction'
    return 'body paragraph', 'body paragraph'


def classify_line(line: str, div_stack: list[str]) -> tuple[str, str, str]:
    stripped = line.strip()
    if not stripped:
        return 'blank', 'blank', 'blank'
    if DIV_CLOSE_RE.match(stripped):
        return 'div-close', 'div boundary', 'div-close'
    div_match = DIV_OPEN_RE.match(stripped)
    if div_match:
        div_name = div_match.group(1) or ''
        return 'div-open', f'div:{div_name}', 'div-open'
    heading_match = HEADING_RE.match(stripped)
    if heading_match:
        level = len(heading_match.group(1))
        paragraph_type, subtype = classify_function(stripped, f'heading-{level}')
        return 'heading', f'{paragraph_type}:{subtype}', f'heading-{level}'
    bold_match = BOLD_ONLY_RE.match(stripped)
    if bold_match:
        paragraph_type, subtype = classify_function(stripped, 'bold-only')
        return 'bold-title', f'{paragraph_type}:{subtype}', 'bold-only'
    if NUMBERED_RE.match(stripped):
        paragraph_type, subtype = classify_function(stripped, 'numbered')
        return 'numbered-list', f'{paragraph_type}:{subtype}', 'numbered'
    if ALPHA_RE.match(stripped):
        paragraph_type, subtype = classify_function(stripped, 'alpha-dot')
        return 'alpha-list', f'{paragraph_type}:{subtype}', 'alpha-dot'
    bullet_match = BULLET_RE.match(stripped)
    if bullet_match:
        if TABLE_LIKE_BULLET_RE.match(stripped):
            paragraph_type, subtype = classify_function(stripped, 'bullet-label-detail')
            return 'table-like-bullet', f'{paragraph_type}:{subtype}', 'bullet-label-detail'
        paragraph_type, subtype = classify_function(stripped, 'bullet')
        return 'bullet-list', f'{paragraph_type}:{subtype}', 'bullet'
    if PLACEHOLDER_RE.search(stripped):
        return 'placeholder', 'placeholder:placeholder line', 'plain-placeholder'
    if stripped.startswith('**') and ':' in stripped:
        paragraph_type, subtype = classify_function(stripped, 'strong-label')
        return 'strong-label', f'{paragraph_type}:{subtype}', 'strong-label'
    if div_stack:
        paragraph_type, subtype = classify_function(stripped, 'plain-in-div')
        if paragraph_type == 'body paragraph':
            return 'div-content', f'div-content:{div_stack[-1]}', 'plain-in-div'
        return 'div-content', f'{paragraph_type}:{subtype}', 'plain-in-div'
    if len(stripped) <= 120 and stripped.endswith(':'):
        paragraph_type, subtype = classify_function(stripped, 'plain-prompt-label')
        return 'prompt-label', f'{paragraph_type}:{subtype}', 'plain-prompt-label'
    paragraph_type, subtype = classify_function(stripped, 'plain')
    return 'body', f'{paragraph_type}:{subtype}', 'plain'


def inventory_lines(lines: list[str]) -> list[ParagraphRecord]:
    records: list[ParagraphRecord] = []
    div_stack: list[str] = []
    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()
        kind, paragraph_type, form = classify_line(line, div_stack)
        if ':' in paragraph_type:
            broad_type, subtype = paragraph_type.split(':', 1)
        else:
            broad_type, subtype = paragraph_type, paragraph_type
        records.append(ParagraphRecord(idx, kind, broad_type, subtype, form, stripped))
        if kind == 'div-open':
            match = DIV_OPEN_RE.match(stripped)
            div_stack.append((match.group(1) or 'div') if match else 'div')
        elif kind == 'div-close' and div_stack:
            div_stack.pop()
    return records


def is_activity_title(text: str) -> bool:
    lowered = text.lower()
    return any(keyword in lowered for keyword in TITLE_KEYWORDS)


def convert_bold_activity_titles(lines: list[str]) -> int:
    changed = 0
    for idx, line in enumerate(lines):
        match = BOLD_ONLY_RE.match(line.strip())
        if not match:
            continue
        title = match.group(1).strip()
        if title.lower().startswith('learn'):
            continue
        if not is_activity_title(title):
            continue
        lines[idx] = f'#### {title}'
        changed += 1
    return changed


def strip_heading_activity_codes(lines: list[str]) -> int:
    changed = 0
    for idx, line in enumerate(lines):
        match = HEADING_RE.match(line.strip())
        if not match:
            continue
        updated_title = ACTIVITY_CODE_RE.sub('', match.group(2)).strip()
        if updated_title != match.group(2):
            lines[idx] = f'{match.group(1)} {updated_title}'
            changed += 1
    return changed


def ensure_alpha_block_spacing(lines: list[str]) -> int:
    changed = 0
    idx = 0
    while idx < len(lines):
        if not ALPHA_RE.match(lines[idx].strip()):
            idx += 1
            continue
        start = idx
        while idx < len(lines) and ALPHA_RE.match(lines[idx].strip()):
            idx += 1
        end = idx
        if end - start < 2:
            continue
        block: list[str] = []
        for pos in range(start, end):
            block.append(lines[pos])
            if pos != end - 1:
                block.append('')
        if lines[start:end] != block:
            lines[start:end] = block
            changed += 1
            idx = start + len(block)
    return changed


def convert_table_like_bullet_blocks(lines: list[str]) -> int:
    changed = 0
    idx = 0
    while idx < len(lines):
        match = TABLE_LIKE_BULLET_RE.match(lines[idx].strip())
        if not match:
            idx += 1
            continue
        start = idx
        rows: list[tuple[str, str]] = []
        while idx < len(lines):
            row_match = TABLE_LIKE_BULLET_RE.match(lines[idx].strip())
            if not row_match:
                break
            label = row_match.group(1).strip()
            value = row_match.group(2).strip()
            if len(label) > 48:
                break
            rows.append((label, value))
            idx += 1
        if len(rows) < 2:
            continue
        table = ['| Label | Details |', '|---|---|']
        table.extend(f'| {label} | {value} |' for label, value in rows)
        lines[start:idx] = table
        changed += 1
        idx = start + len(table)
    return changed


def _learn_class_for_label(label: str) -> str:
    lowered = label.lower()
    if any(token in lowered for token in (
        'why this works',
        'process',
        'function',
        'scenario',
        'task',
        'template',
        'part a',
        'part b',
        'part c',
        'recommendation',
        'planning',
    )):
        return 'learn-process'
    if any(token in lowered for token in ('language', 'phrase', 'expression', 'sentence', 'verb', 'structure', 'pattern', 'form', 'common', 'contrast', 'subordinator', 'example')):
        return 'learn-language'
    if any(token in lowered for token in ('principle', 'constraint', 'goal')):
        return 'learn-principle'
    if 'transfer reminder' in lowered:
        return 'learn-transfer'
    if any(token in lowered for token in ('teaching point', 'discussion', 'discuss', 'role reminder', 'how to use')):
        return 'learn-teaching'
    return 'learn-note'


def normalize_learn_div_classes_and_titles(lines: list[str]) -> int:
    """Use the Learn label text to choose a specific learn-x Div class."""
    changed = 0
    idx = 0
    while idx < len(lines):
        div_match = DIV_OPEN_RE.match(lines[idx].strip())
        if not div_match or not (div_match.group(1) or '').startswith('learn-'):
            idx += 1
            continue

        label_idx = idx + 1
        while label_idx < len(lines) and not lines[label_idx].strip():
            label_idx += 1

        if label_idx >= len(lines):
            idx += 1
            continue

        stripped_label = lines[label_idx].strip()
        label_text = ''
        bold_match = BOLD_ONLY_RE.match(stripped_label)
        heading_match = HEADING_RE.match(stripped_label)
        if bold_match:
            label_text = bold_match.group(1)
        elif heading_match and heading_match.group(2).lower().startswith('learn'):
            label_text = heading_match.group(2)
            lines[label_idx] = f'**{label_text}**'
            changed += 1
        elif stripped_label.startswith('**Learn'):
            label_text = strip_markdown_inline(stripped_label.split(':', 1)[0])

        if label_text:
            target_class = _learn_class_for_label(label_text)
            current_class = div_match.group(1) or ''
            if current_class != target_class:
                lines[idx] = f'::: {target_class}'
                changed += 1
        idx += 1
    return changed


def demote_nested_activity_headings(lines: list[str]) -> int:
    """
    Demote activity headings nested under numbered H4 subskill headings.
    Example: in a Language Focus sequence, H4 "1. ..." stays H4 while
    following H4 "Practice A ..." becomes H5 until the next H3 boundary.
    """
    changed = 0
    in_numbered_subskill = False
    for idx, line in enumerate(lines):
        match = HEADING_RE.match(line.strip())
        if not match:
            continue
        level = len(match.group(1))
        title = match.group(2).strip()
        lowered = title.lower()
        if level <= 3:
            in_numbered_subskill = False
            continue
        if level == 4 and re.match(r'^\d+\.\s+', title):
            in_numbered_subskill = True
            continue
        if level == 4 and in_numbered_subskill and is_activity_title(title):
            lines[idx] = f'##### {title}'
            changed += 1
    return changed


def suspicious_numbered_starts(lines: list[str]) -> list[tuple[int, str]]:
    suspicious: list[tuple[int, str]] = []
    previous_was_numbered = False
    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()
        match = NUMBERED_RE.match(stripped)
        if match:
            if not previous_was_numbered and int(match.group(1)) != 1:
                suspicious.append((idx, stripped))
            previous_was_numbered = True
            continue
        previous_was_numbered = False
    return suspicious


def docx_inventory(docx_path: Path) -> list[ParagraphRecord]:
    if Document is None:
        raise RuntimeError('python-docx is required for --docx audit mode.')
    doc = Document(docx_path)
    records: list[ParagraphRecord] = []
    for idx, paragraph in enumerate(doc.paragraphs, start=1):
        text = ' '.join(paragraph.text.split())
        if not text:
            continue
        style = paragraph.style.name if paragraph.style is not None else ''
        paragraph_type, subtype = classify_function(text, style)
        records.append(
            ParagraphRecord(
                line=idx,
                kind='docx-paragraph',
                paragraph_type=paragraph_type,
                subtype=subtype,
                form='docx',
                text=text,
                style=style,
                source='docx',
            )
        )
    return records


def write_report(records: list[ParagraphRecord], output: Path, numbered_issues: list[tuple[int, str]]) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    by_type: dict[tuple[str, str, str], Counter[str]] = defaultdict(Counter)
    examples: dict[tuple[str, str, str, str], list[ParagraphRecord]] = defaultdict(list)
    for record in records:
        if record.kind == 'blank':
            continue
        style_or_form = record.style or record.form
        type_key = (record.source, record.paragraph_type, record.subtype)
        by_type[type_key][style_or_form] += 1
        key = (*type_key, style_or_form)
        if len(examples[key]) < 8:
            examples[key].append(record)

    with output.open('w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'source',
            'paragraph_type',
            'subtype',
            'styles_or_forms',
            'total',
            'line_or_paragraph',
            'style_or_form',
            'kind',
            'text',
        ])
        for type_key in sorted(by_type):
            forms = by_type[type_key]
            source, paragraph_type, subtype = type_key
            if len(forms) < 2:
                continue
            total = sum(forms.values())
            form_summary = '; '.join(f'{form}={count}' for form, count in forms.most_common())
            for form in forms:
                for record in examples[(*type_key, form)]:
                    writer.writerow([
                        source,
                        paragraph_type,
                        subtype,
                        form_summary,
                        total,
                        record.line,
                        form,
                        record.kind,
                        record.text,
                    ])
        for line, text in numbered_issues:
            writer.writerow([
                'markdown',
                'SUSPICIOUS_NUMBERED_START',
                'numbered item starts above 1 after boundary',
                'numbered=1',
                1,
                line,
                'numbered',
                'numbered-list',
                text,
            ])


def apply_normalizations(lines: list[str]) -> dict[str, int]:
    changes = {
        'bold_activity_titles_to_h4': convert_bold_activity_titles(lines),
        'heading_activity_codes_removed': strip_heading_activity_codes(lines),
        'alpha_blocks_spaced': ensure_alpha_block_spacing(lines),
        'table_like_bullet_blocks': convert_table_like_bullet_blocks(lines),
        'learn_divs_reclassified': normalize_learn_div_classes_and_titles(lines),
        'nested_activity_headings_demoted': demote_nested_activity_headings(lines),
    }
    return changes


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--report', required=True)
    parser.add_argument('--docx', help='Optional generated DOCX to include Word style counts by paragraph type.')
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()

    input_path = Path(args.input)
    report_path = Path(args.report)
    text = input_path.read_text(encoding='utf-8')
    lines = text.splitlines()

    records = inventory_lines(lines)
    if args.docx:
        records.extend(docx_inventory(Path(args.docx)))
    numbered_issues = suspicious_numbered_starts(lines)
    write_report(records, report_path, numbered_issues)

    if args.apply:
        changes = apply_normalizations(lines)
        updated = '\n'.join(lines) + ('\n' if text.endswith('\n') else '')
        if updated != text:
            input_path.write_text(updated, encoding='utf-8')
        print('Applied markdown normalizations:')
        for name, count in changes.items():
            print(f'- {name}: {count}')
    else:
        print(f'Wrote audit report: {report_path}')
        print(f'Suspicious numbered starts: {len(numbered_issues)}')

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
