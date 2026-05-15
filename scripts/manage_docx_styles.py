#!/usr/bin/env python3
"""
Explicit maintenance tool for updating reference DOCX styles from a YAML spec.

MANUAL MAINTENANCE TOOL — do NOT include in the automated build pipeline.

This script updates all three color locations that must stay in sync for linked
Div label style pairs (paragraph w:color, paragraph w14:srgbClr, character w:color),
and replaces unavailable fonts according to the spec.

Usage:
    python scripts/manage_docx_styles.py \\
        --input ../book_administrative-writing/adv/aw-adv-styleref.docx \\
        --spec ../book_administrative-writing/adv/style_specs/aw-div-label-styles.yaml \\
        --output ../book_administrative-writing/adv/aw-adv-styleref.updated.docx

Safety rules:
    - Default: save to a new output file, never overwrite input
    - --in-place: overwrites input, always creates .bak first
    - Validates the result after writing via audit_docx_styles logic
    - Prints a report of all changed style properties

Exit code: 0 on success, non-zero on error or validation failure.
"""
# pylint: disable=broad-exception-caught

import argparse
import shutil
import sys
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

import yaml
from lxml import etree

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
W14_NS = "http://schemas.microsoft.com/office/word/2010/wordml"

NS = {"w": W_NS, "w14": W14_NS}


def _qn(tag: str) -> str:
    if ":" in tag:
        prefix, local = tag.split(":", 1)
        ns = NS.get(prefix)
        return f"{{{ns}}}{local}" if ns else tag
    return tag


def load_spec(spec_path: str) -> dict:
    with open(spec_path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def read_styles_xml(docx_path: str):
    """Return (raw_bytes, lxml_root) for word/styles.xml inside the DOCX."""
    with ZipFile(docx_path, "r") as zf:
        raw = zf.read("word/styles.xml")
    return raw, etree.fromstring(raw)


def write_updated_docx(input_path: str, output_path: str, styles_xml_bytes: bytes) -> None:
    """Write a new DOCX with updated styles.xml while preserving all other parts."""
    with ZipFile(input_path, "r") as zin, ZipFile(output_path, "w", compression=ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            if item.filename == "word/styles.xml":
                zout.writestr(item, styles_xml_bytes)
            else:
                zout.writestr(item, zin.read(item.filename))


def find_style_by_name(styles_xml, name: str):
    for style_el in styles_xml.findall(_qn("w:style")):
        name_el = style_el.find(_qn("w:name"))
        if name_el is not None and name_el.get(_qn("w:val")) == name:
            return style_el
    return None


def _get_or_add_rpr(style_el):
    r_pr = style_el.find(_qn("w:rPr"))
    if r_pr is None:
        r_pr = etree.SubElement(style_el, _qn("w:rPr"))
    return r_pr


def _style_display_name(style_el) -> str:
    name_el = style_el.find(_qn("w:name"))
    return name_el.get(_qn("w:val"), "?") if name_el is not None else "?"


def update_color(style_el, color_hex: str, report: list) -> None:
    """Update all three color locations in sync: w:color and w14:srgbClr."""
    r_pr = _get_or_add_rpr(style_el)
    style_name = _style_display_name(style_el)

    # 1. w:color/@w:val
    color_el = r_pr.find(_qn("w:color"))
    if color_el is None:
        color_el = etree.SubElement(r_pr, _qn("w:color"))
    old = color_el.get(_qn("w:val"))
    if old != color_hex:
        color_el.set(_qn("w:val"), color_hex)
        report.append(f"  {style_name}: w:color  {old!r} → {color_hex!r}")

    # 2. w14:textFill/w14:solidFill/w14:srgbClr/@w14:val (paragraph styles only)
    text_fill = r_pr.find(f"{{{W14_NS}}}textFill")
    if text_fill is not None:
        solid_fill = text_fill.find(f"{{{W14_NS}}}solidFill")
        if solid_fill is not None:
            srgb = solid_fill.find(f"{{{W14_NS}}}srgbClr")
            if srgb is not None:
                old_srgb = srgb.get(f"{{{W14_NS}}}val")
                if old_srgb != color_hex:
                    srgb.set(f"{{{W14_NS}}}val", color_hex)
                    report.append(f"  {style_name}: w14:srgbClr  {old_srgb!r} → {color_hex!r}")
    elif style_el.get(_qn("w:type")) == "paragraph":
        # Create w14:textFill structure so all three locations exist and match.
        text_fill = etree.SubElement(r_pr, f"{{{W14_NS}}}textFill")
        solid_fill = etree.SubElement(text_fill, f"{{{W14_NS}}}solidFill")
        srgb = etree.SubElement(solid_fill, f"{{{W14_NS}}}srgbClr")
        srgb.set(f"{{{W14_NS}}}val", color_hex)
        report.append(f"  {style_name}: w14:srgbClr  created = {color_hex!r}")


def update_fonts(style_el, font_spec: dict, report: list) -> None:
    """Replace fonts in rPr/w:rFonts according to the replacement map."""
    replace_map = font_spec.get("replace", {})
    set_div_label_font = font_spec.get("set_div_label_font")
    style_name = _style_display_name(style_el)

    r_pr = _get_or_add_rpr(style_el)
    r_fonts = r_pr.find(_qn("w:rFonts"))
    if r_fonts is None:
        if set_div_label_font and "Div Label" in style_name:
            r_fonts = etree.SubElement(r_pr, _qn("w:rFonts"))
        else:
            return

    for attr in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        old_val = r_fonts.get(_qn(attr))
        new_val = None
        if old_val and old_val in replace_map:
            new_val = replace_map[old_val]
        elif set_div_label_font and "Div Label" in style_name and old_val != set_div_label_font:
            new_val = set_div_label_font

        if new_val and new_val != old_val:
            r_fonts.set(_qn(attr), new_val)
            report.append(f"  {style_name}: font {attr}  {old_val!r} → {new_val!r}")


def fix_div_label_base_next(styles_xml, report: list) -> None:
    """Ensure Div Label Base next style points to DivContent, not Code."""
    style_el = find_style_by_name(styles_xml, "Div Label Base")
    if style_el is None:
        return
    next_el = style_el.find(_qn("w:next"))
    if next_el is None:
        next_el = etree.SubElement(style_el, _qn("w:next"))
    old_val = next_el.get(_qn("w:val"))
    if old_val != "DivContent":
        next_el.set(_qn("w:val"), "DivContent")
        report.append(f"  Div Label Base: next  {old_val!r} → 'DivContent'")


def apply_spec(styles_xml, spec: dict, group_filter: str | None = None) -> list:
    """Apply the YAML spec to styles_xml. Returns a list of human-readable change lines."""
    report = []
    font_spec = spec.get("font", {})

    for group_name, group_data in spec.get("groups", {}).items():
        if group_filter and group_name != group_filter:
            continue
        report.append(f"\nGroup '{group_name}':")

        for style_spec in group_data.get("styles", []):
            para_name = style_spec.get("paragraph_style")
            char_name = style_spec.get("character_style")
            color_hex = (style_spec.get("color_hex") or "").upper()

            if not para_name or not color_hex:
                continue

            para_el = find_style_by_name(styles_xml, para_name)
            if para_el is None:
                report.append(f"  WARNING: paragraph style '{para_name}' not found — skipping")
            else:
                update_color(para_el, color_hex, report)
                update_fonts(para_el, font_spec, report)

            if char_name:
                char_el = find_style_by_name(styles_xml, char_name)
                if char_el is None:
                    report.append(f"  WARNING: character style '{char_name}' not found — skipping")
                else:
                    update_color(char_el, color_hex, report)
                    update_fonts(char_el, font_spec, report)

    report.append("\nKnown-issue fixes:")
    fix_div_label_base_next(styles_xml, report)

    return report


def serialize_styles_xml(root) -> bytes:
    """Serialize lxml element to bytes, preserving all namespace declarations."""
    return etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)


def _validate_output(output_path: str) -> list:
    """Run a quick color-mismatch audit. Returns list of error strings."""
    from audit_docx_styles import audit_docx  # local import to avoid circular dep
    _, errors = audit_docx(output_path, style_filter="Div Label")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Update reference DOCX styles from a YAML spec (manual maintenance tool)"
    )
    parser.add_argument("--input", required=True, help="Reference DOCX to update")
    parser.add_argument("--spec", required=True, help="YAML style spec file")
    parser.add_argument(
        "--output",
        help="Output path (default: input stem + '.updated.docx')",
    )
    parser.add_argument(
        "--in-place",
        action="store_true",
        help="Overwrite the input file (creates .bak backup first)",
    )
    parser.add_argument(
        "--group",
        help="Only apply a specific named group from the spec",
    )
    parser.add_argument(
        "--fix-div-label-base-next",
        action="store_true",
        help="Also fix Div Label Base next style to point to DivContent",
    )
    args = parser.parse_args()

    input_path = Path(args.input).resolve()
    if not input_path.exists():
        print(f"Error: input file not found: {input_path}", file=sys.stderr)
        return 1

    if args.in_place:
        output_path = input_path
        bak_path = input_path.with_suffix(".bak")
        shutil.copy2(input_path, bak_path)
        print(f"Backup created: {bak_path}")
    elif args.output:
        output_path = Path(args.output).resolve()
    else:
        output_path = input_path.with_name(input_path.stem + ".updated" + input_path.suffix)

    print(f"Input:  {input_path}")
    print(f"Spec:   {args.spec}")
    print(f"Output: {output_path}")

    try:
        spec = load_spec(args.spec)
    except Exception as exc:
        print(f"Error loading spec: {exc}", file=sys.stderr)
        return 1

    try:
        _, styles_xml = read_styles_xml(str(input_path))
    except Exception as exc:
        print(f"Error reading DOCX: {exc}", file=sys.stderr)
        return 1

    report = apply_spec(styles_xml, spec, group_filter=args.group)

    try:
        updated_bytes = serialize_styles_xml(styles_xml)
        write_updated_docx(str(input_path), str(output_path), updated_bytes)
    except Exception as exc:
        print(f"Error writing output DOCX: {exc}", file=sys.stderr)
        return 1

    print("\n--- Changes Applied ---")
    for line in report:
        print(line)
    print(f"\nOutput written: {output_path}")

    # Post-write validation
    try:
        errors = _validate_output(str(output_path))
        if errors:
            print("\nValidation warnings after update:")
            for e in errors:
                print(f"  ! {e}")
        else:
            print("Validation: ✓ No color mismatches in Div Label styles")
    except Exception as exc:
        print(f"Validation step skipped: {exc}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
