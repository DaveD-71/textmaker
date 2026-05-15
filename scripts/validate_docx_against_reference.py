#!/usr/bin/env python3
"""
Validate a generated DOCX against a reference DOCX.

Checks:
1. Every paragraph style used in generated DOCX exists in reference DOCX.
2. Every character style used exists in reference DOCX.
3. No generated style definitions exist outside the reference (unless built-in).
4. Every style from a YAML style_map exists in reference.
5. Linked styles are valid and reciprocal.

Exit code: 0 on success, non-zero on validation failure.
"""
# pylint: disable=broad-exception-caught

import argparse
import sys
from pathlib import Path
from zipfile import ZipFile

import yaml
from lxml import etree

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W_NS}

# Pandoc always generates these; they are expected even when not in the reference.
EXPECTED_EXTRA_STYLES = {
    "Normal",
    "DefaultParagraphFont",
    "TableNormal",
    "NoList",
    "Compact",       # Pandoc fallback — postprocess should clean these up
    "VerbatimChar",  # Pandoc fallback — postprocess should clean these up
}


def _qn(tag: str) -> str:
    if ":" in tag:
        prefix, local = tag.split(":", 1)
        ns = NS.get(prefix)
        return f"{{{ns}}}{local}" if ns else tag
    return tag


def _extract_xml(docx_path: str, part_name: str):
    with ZipFile(docx_path, "r") as zf:
        return etree.fromstring(zf.read(part_name))


def _style_ids(styles_xml) -> set:
    return {
        el.get(_qn("w:styleId"))
        for el in styles_xml.findall(_qn("w:style"))
        if el.get(_qn("w:styleId"))
    }


def _style_names(styles_xml) -> dict:
    result = {}
    for el in styles_xml.findall(_qn("w:style")):
        style_id = el.get(_qn("w:styleId"))
        name_el = el.find(_qn("w:name"))
        if style_id and name_el is not None:
            result[style_id] = name_el.get(_qn("w:val"), "")
    return result


def _link_map(styles_xml) -> dict:
    """Return {style_id: linked_style_id} for all styles with a w:link element."""
    result = {}
    for el in styles_xml.findall(_qn("w:style")):
        style_id = el.get(_qn("w:styleId"))
        link_el = el.find(_qn("w:link"))
        if style_id and link_el is not None:
            linked = link_el.get(_qn("w:val"))
            if linked:
                result[style_id] = linked
    return result


def _used_styles(docx_path: str) -> tuple[set, set]:
    """Return (used_para_style_ids, used_char_style_ids) from document.xml."""
    para_styles: set = set()
    char_styles: set = set()
    try:
        doc_xml = _extract_xml(docx_path, "word/document.xml")
    except Exception:
        return para_styles, char_styles

    for el in doc_xml.findall(".//w:pStyle", NS):
        val = el.get(_qn("w:val"))
        if val:
            para_styles.add(val)
    for el in doc_xml.findall(".//w:rStyle", NS):
        val = el.get(_qn("w:val"))
        if val:
            char_styles.add(val)

    return para_styles, char_styles


def validate(generated_path: str, reference_path: str, style_map: dict | None = None) -> list:
    """Run all checks and return a list of error strings (empty = pass)."""
    errors: list = []

    ref_xml = _extract_xml(reference_path, "word/styles.xml")
    gen_xml = _extract_xml(generated_path, "word/styles.xml")

    ref_ids = _style_ids(ref_xml)
    ref_names = _style_names(ref_xml)
    ref_links = _link_map(ref_xml)
    gen_ids = _style_ids(gen_xml)
    gen_names = _style_names(gen_xml)

    used_para, used_char = _used_styles(generated_path)

    # 1. Every paragraph style used in the generated doc must exist in the reference.
    for style_id in sorted(used_para):
        if style_id not in ref_ids:
            errors.append(
                f"Paragraph style used but missing from reference: "
                f"'{gen_names.get(style_id, style_id)}'"
            )

    # 2. Every character style used in the generated doc must exist in the reference.
    for style_id in sorted(used_char):
        if style_id not in ref_ids:
            errors.append(
                f"Character style used but missing from reference: "
                f"'{gen_names.get(style_id, style_id)}'"
            )

    # 3. No extra style definitions outside the reference (beyond known built-ins).
    for style_id in sorted(gen_ids - ref_ids):
        name = gen_names.get(style_id, style_id)
        if style_id not in EXPECTED_EXTRA_STYLES and name not in EXPECTED_EXTRA_STYLES:
            errors.append(
                f"Extra style definition in generated DOCX not in reference: "
                f"'{name}' (ID: {style_id})"
            )

    # 4. Every style from YAML style_map must exist in the reference.
    if style_map:
        ref_name_set = set(ref_names.values())
        for div_class, style_name in style_map.items():
            if style_name not in ref_name_set:
                errors.append(
                    f"style_map entry '{div_class}' → '{style_name}' "
                    f"not found in reference DOCX"
                )

    # 5. Linked styles must be valid and reciprocal.
    for style_id, linked_id in ref_links.items():
        if linked_id not in ref_ids:
            errors.append(
                f"Style '{ref_names.get(style_id, style_id)}' links to "
                f"'{linked_id}' which does not exist in reference"
            )
        else:
            back = ref_links.get(linked_id)
            if back != style_id:
                errors.append(
                    f"Non-reciprocal link: '{ref_names.get(style_id, style_id)}' → "
                    f"'{ref_names.get(linked_id, linked_id)}', but back-link points to "
                    f"'{ref_names.get(back, back or 'None')}'"
                )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate a generated DOCX against a reference DOCX"
    )
    parser.add_argument("generated", help="Generated DOCX to validate")
    parser.add_argument("--reference", required=True, help="Reference DOCX")
    parser.add_argument(
        "--style-map",
        help="YAML file containing a style_map block to check against the reference",
    )
    args = parser.parse_args()

    style_map = None
    if args.style_map:
        with open(args.style_map, encoding="utf-8") as f:
            style_map = yaml.safe_load(f).get("style_map", {})

    print(f"Validating: {args.generated}")
    print(f"Reference:  {args.reference}")

    try:
        errors = validate(args.generated, args.reference, style_map=style_map)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    if errors:
        print(f"\n{len(errors)} validation error(s):\n")
        for err in errors:
            print(f"  ✗ {err}")
        return 1

    print("\n✓ Validation passed — all styles consistent with reference DOCX")
    return 0


if __name__ == "__main__":
    sys.exit(main())
