import argparse
import os
import re
import unicodedata
from copy import deepcopy

import docx
from docx.oxml.ns import qn
from docx.table import Table
from docx.text.paragraph import Paragraph


def iter_block_items(parent):
    for child in parent.element.body.iterchildren():
        if child.tag == qn('w:p'):
            yield Paragraph(child, parent)
        elif child.tag == qn('w:tbl'):
            yield Table(child, parent)


def block_text(block):
    if isinstance(block, Paragraph):
        return block.text.strip()
    texts = []
    for row in block.rows:
        for cell in row.cells:
            cell_text = cell.text.strip()
            if cell_text:
                texts.append(cell_text)
    return "\n".join(texts)


def sanitize_title(title: str) -> str:
    normalized = unicodedata.normalize("NFKD", title)
    ascii_title = normalized.encode("ascii", "ignore").decode("ascii")
    ascii_title = ascii_title.replace(":", " - ")
    ascii_title = ascii_title.replace("/", " - ")
    ascii_title = ascii_title.replace("&", "and")
    ascii_title = re.sub(r"[\'\"“”‘’]", "", ascii_title)
    ascii_title = re.sub(r"[^A-Za-z0-9\s\-]", " ", ascii_title)
    ascii_title = re.sub(r"\s+", " ", ascii_title).strip()
    return ascii_title


def find_units(blocks):
    unit_starts = []
    colon_pattern = re.compile(r"^\s*(\d+)\s*:\s*(.+)$")
    number_pattern = re.compile(r"^\s*(\d+)\s*$")

    for idx, (_, text) in enumerate(blocks):
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        for i, line in enumerate(lines):
            colon_match = colon_pattern.match(line)
            if colon_match:
                unit_number = colon_match.group(1)
                unit_title = colon_match.group(2).strip()
                unit_starts.append((idx, unit_number, unit_title))
                break
            number_match = number_pattern.match(line)
            if number_match:
                unit_number = number_match.group(1)
                unit_title = None
                for j in range(i + 1, len(lines)):
                    if lines[j] != unit_number:
                        unit_title = lines[j]
                        break
                unit_starts.append((idx, unit_number, unit_title or f"Unit {unit_number}"))
                break
    return unit_starts


def remove_images(doc_to_clean):
    for element in doc_to_clean.element.body.iter():
        for child in list(element):
            if child.tag in {qn("w:drawing"), qn("w:pict")}:
                element.remove(child)


def split_docx(input_path: str, output_dir: str) -> list[tuple[str, str]]:
    doc = docx.Document(input_path)
    blocks = [(block, block_text(block)) for block in iter_block_items(doc)]
    unit_starts = find_units(blocks)
    if not unit_starts:
        raise ValueError(f"No unit markers found in {input_path}")

    unit_ranges = []
    for i, (start_idx, unit_num, unit_title) in enumerate(unit_starts):
        end_idx = unit_starts[i + 1][0] if i + 1 < len(unit_starts) else len(blocks)
        unit_ranges.append((unit_num, unit_title, start_idx, end_idx))

    first_unit_num, first_unit_title, first_start, first_end = unit_ranges[0]
    if first_start > 0:
        unit_ranges[0] = (first_unit_num, first_unit_title, 0, first_end)

    os.makedirs(output_dir, exist_ok=True)

    created = []
    for unit_num, unit_title, start_idx, end_idx in unit_ranges:
        safe_title = sanitize_title(unit_title)
        unit_dir = os.path.join(output_dir, f"Unit {unit_num} - {safe_title}")
        os.makedirs(unit_dir, exist_ok=True)
        unit_doc = docx.Document()
        if unit_doc.paragraphs:
            p = unit_doc.paragraphs[0]._element
            p.getparent().remove(p)
        for block, _text in blocks[start_idx:end_idx]:
            unit_doc.element.body.append(deepcopy(block._element))
        remove_images(unit_doc)
        out_path = os.path.join(unit_dir, f"Unit {unit_num} - {safe_title}.docx")
        unit_doc.save(out_path)
        created.append((unit_num, safe_title))
    return created


def main():
    parser = argparse.ArgumentParser(
        description="Split a DOCX into unit-level DOCX files, removing images."
    )
    parser.add_argument("input", help="Path to the source DOCX")
    parser.add_argument("output", help="Output directory for unit folders")
    args = parser.parse_args()

    created = split_docx(args.input, args.output)
    for unit_num, title in created:
        print(f"Unit {unit_num} - {title}")


if __name__ == "__main__":
    main()
