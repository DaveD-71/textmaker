"""
Minimal tests for DOCX style utilities.

Tests avoid real DOCX fixture files; they build minimal in-memory XML/DOCX structures.
"""
import io
import os
import sys
import tempfile
import zipfile
from pathlib import Path

import pytest
from lxml import etree

# Allow importing scripts directly
SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from manage_docx_styles import find_style_by_name, fix_div_label_base_next, update_color  # noqa: E402
from audit_docx_styles import audit_docx  # noqa: E402
from generate_reference_docx import create_reference_from_spec  # noqa: E402

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
W14_NS = "http://schemas.microsoft.com/office/word/2010/wordml"

_STYLES_WRAP = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<w:styles'
    ' xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'
    ' xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml">'
    "{body}"
    "</w:styles>"
)


def _styles_xml(*style_fragments: str):
    return etree.fromstring(
        _STYLES_WRAP.format(body="".join(style_fragments)).encode("utf-8")
    )


def _para(style_id, name, *, color=None, srgb=None, link=None, next_id=None):
    r_pr_parts = []
    if color:
        r_pr_parts.append(f'<w:color w:val="{color}"/>')
    if srgb:
        r_pr_parts.append(
            f'<w14:textFill><w14:solidFill>'
            f'<w14:srgbClr w14:val="{srgb}"/>'
            f'</w14:solidFill></w14:textFill>'
        )
    r_pr = f"<w:rPr>{''.join(r_pr_parts)}</w:rPr>" if r_pr_parts else ""
    link_el = f'<w:link w:val="{link}"/>' if link else ""
    next_el = f'<w:next w:val="{next_id}"/>' if next_id else ""
    return (
        f'<w:style w:type="paragraph" w:styleId="{style_id}">'
        f'<w:name w:val="{name}"/>{link_el}{next_el}{r_pr}'
        f"</w:style>"
    )


def _char(style_id, name, *, color=None, link=None):
    r_pr = f'<w:rPr><w:color w:val="{color}"/></w:rPr>' if color else ""
    link_el = f'<w:link w:val="{link}"/>' if link else ""
    return (
        f'<w:style w:type="character" w:styleId="{style_id}">'
        f'<w:name w:val="{name}"/>{link_el}{r_pr}'
        f"</w:style>"
    )


def _docx_bytes(styles_xml_str: str) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("word/styles.xml", styles_xml_str.encode("utf-8"))
        zf.writestr(
            "[Content_Types].xml",
            '<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org'
            '/package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats'
            '-package.relationships+xml"/>'
            '<Override PartName="/word/styles.xml" ContentType="application/vnd'
            '.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
            "</Types>",
        )
        zf.writestr(
            "word/document.xml",
            '<?xml version="1.0"?>'
            '<w:document xmlns:w="http://schemas.openxmlformats.org'
            '/wordprocessingml/2006/main"><w:body/></w:document>',
        )
    return buf.getvalue()


def _tmp_docx(styles_xml_str: str) -> str:
    """Write a minimal DOCX to a temp file and return its path."""
    data = _docx_bytes(styles_xml_str)
    fd, path = tempfile.mkstemp(suffix=".docx")
    try:
        os.write(fd, data)
    finally:
        os.close(fd)
    return path


# ---------------------------------------------------------------------------
# 1. RGB → hex conversion
# ---------------------------------------------------------------------------

def _rgb_to_hex(r: int, g: int, b: int) -> str:
    return f"{r:02X}{g:02X}{b:02X}"


def test_rgb_to_hex_example_from_spec():
    assert _rgb_to_hex(42, 75, 215) == "2A4BD7"


def test_rgb_to_hex_palette_samples():
    assert _rgb_to_hex(0x29, 0xD0, 0xD0) == "29D0D0"  # Cyan
    assert _rgb_to_hex(0x57, 0x57, 0x57) == "575757"  # Dk. Gray
    assert _rgb_to_hex(0xAD, 0x23, 0x23) == "AD2323"  # Red
    assert _rgb_to_hex(0x81, 0x26, 0xC0) == "8126C0"  # Purple


# ---------------------------------------------------------------------------
# 2. update_color updates all three linked-style color locations
# ---------------------------------------------------------------------------

def _linked_pair_xml(color="29D0D0", srgb="29D0D0"):
    return _STYLES_WRAP.format(
        body=(
            _para(
                "DivLabelLanguage", "Div Label Language",
                color=color, srgb=srgb, link="DivLabelLanguageChar",
            )
            + _char(
                "DivLabelLanguageChar", "Div Label Language Char",
                color=color, link="DivLabelLanguage",
            )
        )
    )


def test_update_color_sets_w_color():
    styles_xml = etree.fromstring(_linked_pair_xml().encode("utf-8"))
    para_el = find_style_by_name(styles_xml, "Div Label Language")
    update_color(para_el, "FF0000", [])

    r_pr = para_el.find(f"{{{W_NS}}}rPr")
    color_el = r_pr.find(f"{{{W_NS}}}color")
    assert color_el is not None
    assert color_el.get(f"{{{W_NS}}}val") == "FF0000"


def test_update_color_sets_w14_srgbclr():
    styles_xml = etree.fromstring(_linked_pair_xml().encode("utf-8"))
    para_el = find_style_by_name(styles_xml, "Div Label Language")
    update_color(para_el, "FF0000", [])

    r_pr = para_el.find(f"{{{W_NS}}}rPr")
    srgb = r_pr.find(f".//{{{W14_NS}}}srgbClr")
    assert srgb is not None
    assert srgb.get(f"{{{W14_NS}}}val") == "FF0000"


def test_update_color_creates_w14_when_absent():
    xml = _STYLES_WRAP.format(body=_para(
        "DivLabelModel", "Div Label Model", color="575757", link="DivLabelModelChar"
    ))
    styles_xml = etree.fromstring(xml.encode("utf-8"))
    para_el = find_style_by_name(styles_xml, "Div Label Model")
    update_color(para_el, "AD2323", [])

    r_pr = para_el.find(f"{{{W_NS}}}rPr")
    srgb = r_pr.find(f".//{{{W14_NS}}}srgbClr")
    assert srgb is not None
    assert srgb.get(f"{{{W14_NS}}}val") == "AD2323"


def test_update_color_report_records_change():
    styles_xml = etree.fromstring(_linked_pair_xml().encode("utf-8"))
    para_el = find_style_by_name(styles_xml, "Div Label Language")
    report = []
    update_color(para_el, "FF0000", report)
    assert any("29D0D0" in line and "FF0000" in line for line in report)


# ---------------------------------------------------------------------------
# 3. Detect w:color / w14:srgbClr mismatch
# ---------------------------------------------------------------------------

def test_color_mismatch_detected():
    xml = _STYLES_WRAP.format(
        body=(
            _para(
                "DivLabelLanguage", "Div Label Language",
                color="29D0D0", srgb="FF0000",   # deliberate mismatch
                link="DivLabelLanguageChar",
            )
            + _char(
                "DivLabelLanguageChar", "Div Label Language Char",
                color="29D0D0", link="DivLabelLanguage",
            )
        )
    )
    path = _tmp_docx(xml)
    try:
        _, errors = audit_docx(path, style_filter="Div Label")
    finally:
        os.unlink(path)
    assert errors, "Expected a mismatch error but got none"
    assert any("29D0D0" in e and "FF0000" in e for e in errors)


def test_no_mismatch_when_colors_match():
    xml = _STYLES_WRAP.format(
        body=(
            _para(
                "DivLabelLanguage", "Div Label Language",
                color="29D0D0", srgb="29D0D0",
                link="DivLabelLanguageChar",
            )
            + _char(
                "DivLabelLanguageChar", "Div Label Language Char",
                color="29D0D0", link="DivLabelLanguage",
            )
        )
    )
    path = _tmp_docx(xml)
    try:
        _, errors = audit_docx(path, style_filter="Div Label")
    finally:
        os.unlink(path)
    assert errors == []


# ---------------------------------------------------------------------------
# 4. Div Label Base next style
# ---------------------------------------------------------------------------

def test_fix_div_label_base_next_corrects_wrong_value():
    styles_xml = _styles_xml(_para("DivLabelBase", "Div Label Base", next_id="Code"))
    report = []
    fix_div_label_base_next(styles_xml, report)

    style_el = find_style_by_name(styles_xml, "Div Label Base")
    next_el = style_el.find(f"{{{W_NS}}}next")
    assert next_el is not None
    assert next_el.get(f"{{{W_NS}}}val") == "DivContent"
    assert any("DivContent" in line for line in report)


def test_fix_div_label_base_next_no_change_when_correct():
    styles_xml = _styles_xml(_para("DivLabelBase", "Div Label Base", next_id="DivContent"))
    report = []
    fix_div_label_base_next(styles_xml, report)
    assert not report or all("DivContent" not in line for line in report)


def test_fix_div_label_base_next_creates_element_when_absent():
    styles_xml = _styles_xml(_para("DivLabelBase", "Div Label Base"))
    report = []
    fix_div_label_base_next(styles_xml, report)

    style_el = find_style_by_name(styles_xml, "Div Label Base")
    next_el = style_el.find(f"{{{W_NS}}}next")
    assert next_el is not None
    assert next_el.get(f"{{{W_NS}}}val") == "DivContent"


# ---------------------------------------------------------------------------
# 5. Style audit exits non-zero (reports errors) when expected styles missing
# ---------------------------------------------------------------------------

def test_audit_reports_missing_expected_style():
    xml = _STYLES_WRAP.format(body=_para("Normal", "Normal"))
    path = _tmp_docx(xml)
    try:
        _, errors = audit_docx(path, expected_style_map={"learn-language": "Div Label Language"})
    finally:
        os.unlink(path)
    assert any("Div Label Language" in e for e in errors)


def test_audit_no_error_when_expected_style_present():
    xml = _STYLES_WRAP.format(
        body=(
            _para("Normal", "Normal")
            + _para("DivLabelLanguage", "Div Label Language")
        )
    )
    path = _tmp_docx(xml)
    try:
        _, errors = audit_docx(path, expected_style_map={"learn-language": "Div Label Language"})
    finally:
        os.unlink(path)
    assert not any("Div Label Language" in e for e in errors)


# ---------------------------------------------------------------------------
# 6. YAML style-spec reference generation
# ---------------------------------------------------------------------------

def test_generate_reference_from_yaml_spec_creates_requested_styles(tmp_path):
    spec_path = tmp_path / "styles.yaml"
    out_path = tmp_path / "reference.docx"
    spec_path.write_text(
        """
page:
  size: A4
  margins_mm:
    top: 20
    bottom: 20
    left: 18
    right: 18
fonts:
  body: Palatino Linotype
  sans: Arial
colors:
  deep_ink: "#1F2933"
  teal: "#008C8C"
  teal_tint: "#CDEDEA"
  slate: "#64748B"
defaults:
  font: body
  size_pt: 11
  color: deep_ink
  paragraph:
    space_after_pt: 6
    line_spacing: 1.25
    snap_to_grid: false
styles:
  - name: PS Body Text
    type: paragraph
    base: Normal
    font: body
    size_pt: 11
    color: deep_ink
    paragraph:
      space_after_pt: 6
      line_spacing: 1.25
  - name: PS Section Head
    type: paragraph
    base: Normal
    font: sans
    size_pt: 16
    bold: true
    color: teal
    paragraph:
      keep_with_next: true
      space_before_pt: 12
      space_after_pt: 6
    borders:
      bottom:
        val: single
        sz: 12
        space: 2
        color: teal
  - name: PS Model Box
    type: paragraph
    base: Normal
    font: body
    size_pt: 11
    color: deep_ink
    shading: teal_tint
  - name: PS Key Term
    type: character
    font: sans
    bold: true
    color: teal
  - name: PS Planning Table
    type: table
    table:
      cell_margins_mm:
        top: 1.5
        bottom: 1.5
        left: 2
        right: 2
      borders:
        top: {val: single, sz: 4, color: slate}
        left: {val: single, sz: 4, color: slate}
        bottom: {val: single, sz: 4, color: slate}
        right: {val: single, sz: 4, color: slate}
        insideH: {val: single, sz: 4, color: slate}
        insideV: {val: single, sz: 4, color: slate}
sample:
  include: true
""",
        encoding="utf-8",
    )

    create_reference_from_spec(str(spec_path), str(out_path))

    with zipfile.ZipFile(out_path) as zf:
        styles_xml = etree.fromstring(zf.read("word/styles.xml"))

    assert find_style_by_name(styles_xml, "PS Body Text") is not None
    body_text = find_style_by_name(styles_xml, "PS Body Text")
    snap = body_text.find(f".//{{{W_NS}}}snapToGrid")
    assert snap is not None
    assert snap.get(f"{{{W_NS}}}val") == "0"
    section_head = find_style_by_name(styles_xml, "PS Section Head")
    assert section_head is not None
    assert section_head.find(f".//{{{W_NS}}}keepNext") is not None
    border = section_head.find(f".//{{{W_NS}}}pBdr/{{{W_NS}}}bottom")
    assert border is not None
    assert border.get(f"{{{W_NS}}}color") == "008C8C"

    model_box = find_style_by_name(styles_xml, "PS Model Box")
    shading = model_box.find(f".//{{{W_NS}}}shd")
    assert shading is not None
    assert shading.get(f"{{{W_NS}}}fill") == "CDEDEA"

    key_term = find_style_by_name(styles_xml, "PS Key Term")
    assert key_term is not None
    assert key_term.get(f"{{{W_NS}}}type") == "character"

    planning_table = find_style_by_name(styles_xml, "PS Planning Table")
    assert planning_table is not None
    assert planning_table.get(f"{{{W_NS}}}type") == "table"
