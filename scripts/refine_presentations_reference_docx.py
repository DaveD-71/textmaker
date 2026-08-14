"""Refine the presentations textbook reference DOCX after YAML generation.

The YAML generator creates the base paragraph, character, and table style names.
This script adds richer Word-native table-style conditions that python-docx does
not expose as a simple high-level API, then optionally opens and saves the file
through Microsoft Word COM so Word normalizes the package.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn


COLORS = {
    "deep_ink": "0B163A",
    "graphite": "152B46",
    "slate": "1F3D65",
    "purple": "A24F71",
    "purple_dark": "69334A",
    "purple_soft": "C18CA3",
    "yellow": "C98F21",
    "yellow_dark": "886116",
    "yellow_soft": "DDBB79",
    "teal": "A24F71",
    "blue": "3366A8",
    "amber": "C98F21",
    "plum": "A24F71",
    "teal_tint": "F6E5EC",
    "blue_tint": "E3EBF6",
    "amber_tint": "F7EAD2",
    "grey_tint": "EEF3F9",
    "light_grey": "F5F7FB",
    "white": "FFFFFF",
}


TABLE_STYLES = {
    "PS Phrase Bank Table": {
        "header_fill": "teal",
        "header_text": "white",
        "first_col_fill": "teal_tint",
        "band_fill": "light_grey",
        "top_rule": "teal",
    },
    "PS Vocabulary Table": {
        "header_fill": "graphite",
        "header_text": "white",
        "first_col_fill": "grey_tint",
        "band_fill": "light_grey",
        "top_rule": "graphite",
    },
    "PS Planning Table": {
        "header_fill": "slate",
        "header_text": "white",
        "first_col_fill": "light_grey",
        "band_fill": "white",
        "top_rule": "slate",
    },
    "PS Comparison Table": {
        "header_fill": "slate",
        "header_text": "white",
        "first_col_fill": "amber_tint",
        "band_fill": "blue_tint",
        "top_rule": "slate",
    },
    "PS Checklist Table": {
        "header_fill": "graphite",
        "header_text": "white",
        "first_col_fill": "grey_tint",
        "band_fill": "light_grey",
        "top_rule": "graphite",
    },
    "PS Rubric Table": {
        "header_fill": "deep_ink",
        "header_text": "white",
        "first_col_fill": "blue_tint",
        "band_fill": "light_grey",
        "top_rule": "deep_ink",
    },
    "PS Model Support Table": {
        "header_fill": "blue",
        "header_text": "white",
        "first_col_fill": "blue_tint",
        "band_fill": "light_grey",
        "top_rule": "blue",
    },
    "PS Visual Sequence Table": {
        "header_fill": "blue",
        "header_text": "white",
        "first_col_fill": "blue_tint",
        "band_fill": "light_grey",
        "top_rule": "blue",
    },
    "PS Key Vocabulary Table": {
        "header_fill": "graphite",
        "header_text": "white",
        "first_col_fill": "grey_tint",
        "band_fill": "light_grey",
        "top_rule": "graphite",
    },
    "PS QA Model Table": {
        "header_fill": "blue",
        "header_text": "white",
        "first_col_fill": "blue_tint",
        "band_fill": "light_grey",
        "top_rule": "blue",
    },
    "PS Skills Practised Table": {
        "header_fill": "teal",
        "header_text": "white",
        "first_col_fill": "teal_tint",
        "band_fill": "light_grey",
        "top_rule": "teal",
    },
    "PS Answer Key Table": {
        "header_fill": "graphite",
        "header_text": "white",
        "first_col_fill": "grey_tint",
        "band_fill": "light_grey",
        "top_rule": "graphite",
    },
    "PS Quiz Table": {
        "header_fill": "plum",
        "header_text": "white",
        "first_col_fill": "grey_tint",
        "band_fill": "light_grey",
        "top_rule": "plum",
    },
}


def color(name: str) -> str:
    return COLORS.get(name, name).lstrip("#").upper()


def remove_children(parent, tag: str) -> None:
    for child in list(parent.findall(qn(tag))):
        parent.remove(child)


def child(parent, tag: str):
    el = parent.find(qn(tag))
    if el is None:
        el = OxmlElement(tag)
        parent.append(el)
    return el


def set_rfonts(rpr, font_name: str) -> None:
    remove_children(rpr, "w:rFonts")
    rfonts = OxmlElement("w:rFonts")
    for attr in ("ascii", "hAnsi", "cs"):
        rfonts.set(qn(f"w:{attr}"), font_name)
    rpr.append(rfonts)


def set_on_off(parent, tag: str, enabled: bool) -> None:
    remove_children(parent, f"w:{tag}")
    el = OxmlElement(f"w:{tag}")
    el.set(qn("w:val"), "1" if enabled else "0")
    parent.append(el)


def set_text_props(parent, *, fill=None, text="deep_ink", font="Noto Sans Medium", size_pt=10.5, medium=True) -> None:
    rpr = child(parent, "w:rPr")
    set_rfonts(rpr, font)
    remove_children(rpr, "w:color")
    color_el = OxmlElement("w:color")
    color_el.set(qn("w:val"), color(text))
    rpr.append(color_el)
    remove_children(rpr, "w:sz")
    sz = OxmlElement("w:sz")
    sz.set(qn("w:val"), str(int(round(size_pt * 2))))
    rpr.append(sz)
    set_on_off(rpr, "b", False)
    if medium:
        # The font face carries the visual weight; avoid Word synthetic bold.
        set_on_off(rpr, "bCs", False)
    if fill:
        tcpr = child(parent, "w:tcPr")
        set_shading(tcpr, fill)


def set_para_props(parent, alignment="left", after_twips=0, single_spaced=True) -> None:
    ppr = child(parent, "w:pPr")
    remove_children(ppr, "w:jc")
    jc = OxmlElement("w:jc")
    jc.set(qn("w:val"), alignment)
    ppr.append(jc)
    remove_children(ppr, "w:spacing")
    sp = OxmlElement("w:spacing")
    sp.set(qn("w:before"), "0")
    sp.set(qn("w:after"), str(after_twips))
    if single_spaced:
        sp.set(qn("w:line"), "240")
        sp.set(qn("w:lineRule"), "auto")
    ppr.append(sp)
    remove_children(ppr, "w:suppressAutoHyphens")
    hyph = OxmlElement("w:suppressAutoHyphens")
    hyph.set(qn("w:val"), "1")
    ppr.append(hyph)


def set_shading(parent, fill: str) -> None:
    remove_children(parent, "w:shd")
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), color(fill))
    parent.append(shd)


def set_border(parent, side: str, val="single", sz=4, line_color="grey_tint") -> None:
    borders = child(parent, "w:tblBorders")
    remove_children(borders, f"w:{side}")
    border = OxmlElement(f"w:{side}")
    border.set(qn("w:val"), val)
    border.set(qn("w:sz"), str(sz))
    border.set(qn("w:space"), "0")
    border.set(qn("w:color"), color(line_color))
    borders.append(border)


def set_cell_margins(tblpr, top=80, bottom=80, left=115, right=115) -> None:
    remove_children(tblpr, "w:tblCellMar")
    mar = OxmlElement("w:tblCellMar")
    for side, value in (("top", top), ("bottom", bottom), ("left", left), ("right", right)):
        el = OxmlElement(f"w:{side}")
        el.set(qn("w:w"), str(value))
        el.set(qn("w:type"), "dxa")
        mar.append(el)
    tblpr.append(mar)


def add_conditional_style(style_el, cond_type: str):
    for existing in list(style_el.findall(qn("w:tblStylePr"))):
        if existing.get(qn("w:type")) == cond_type:
            style_el.remove(existing)
    el = OxmlElement("w:tblStylePr")
    el.set(qn("w:type"), cond_type)
    style_el.append(el)
    return el


def refine_table_style(doc: Document, name: str, spec: dict) -> None:
    style = doc.styles[name]
    style_el = style._element

    tblpr = child(style_el, "w:tblPr")
    set_cell_margins(tblpr)
    set_border(tblpr, "top", sz=10, line_color=spec["top_rule"])
    set_border(tblpr, "bottom", sz=6, line_color="slate")
    set_border(tblpr, "insideH", sz=4, line_color="grey_tint")
    set_border(tblpr, "insideV", sz=4, line_color="grey_tint")

    look = tblpr.find(qn("w:tblLook"))
    if look is None:
        look = OxmlElement("w:tblLook")
        tblpr.append(look)
    look.set(qn("w:firstRow"), "1")
    look.set(qn("w:firstColumn"), "1")
    look.set(qn("w:noHBand"), "0")
    look.set(qn("w:noVBand"), "1")
    look.set(qn("w:val"), "04A0")

    first_row = add_conditional_style(style_el, "firstRow")
    header_text = "white" if spec["header_fill"] not in {"grey_tint", "light_grey", "amber_tint", "blue_tint", "teal_tint"} else spec["header_text"]
    set_text_props(first_row, fill=spec["header_fill"], text=header_text, font="Noto Sans Medium", size_pt=10.5)
    set_para_props(first_row, alignment="left", after_twips=0, single_spaced=True)

    first_col = add_conditional_style(style_el, "firstCol")
    set_text_props(first_col, fill=spec["first_col_fill"], text="deep_ink", font="Noto Sans Medium", size_pt=10.5)
    set_para_props(first_col, alignment="left", after_twips=0)

    band = add_conditional_style(style_el, "band1Horz")
    tcpr = child(band, "w:tcPr")
    set_shading(tcpr, spec["band_fill"])
    set_para_props(band, alignment="left", after_twips=0)


def apply_table_style_refinements(path: Path) -> None:
    doc = Document(str(path))
    for name, spec in TABLE_STYLES.items():
        if name in doc.styles:
            refine_table_style(doc, name, spec)
    doc.save(str(path))


def load_colors_from_yaml(spec_path: Path) -> None:
    """Update color aliases from the YAML style spec when available."""
    try:
        import yaml  # type: ignore
    except ImportError:
        return
    if not spec_path.exists():
        return
    spec = yaml.safe_load(spec_path.read_text(encoding="utf-8"))
    if not isinstance(spec, dict):
        return
    colors = spec.get("colors", {})
    if not isinstance(colors, dict):
        return
    for key, value in colors.items():
        if isinstance(value, str):
            COLORS[str(key)] = value.lstrip("#").upper()


def normalize_with_word_com(path: Path) -> bool:
    try:
        import win32com.client  # type: ignore
    except ImportError:
        return False

    word = win32com.client.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    doc = None
    try:
        doc = word.Documents.Open(str(path), ReadOnly=False, AddToRecentFiles=False)
        doc.Save()
        return True
    finally:
        if doc is not None:
            doc.Close(False)
        word.Quit()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("docx", type=Path)
    parser.add_argument("--spec", type=Path, help="Optional YAML style spec to read color aliases from.")
    parser.add_argument("--word-com-save", action="store_true", help="Open and save with Microsoft Word COM after XML refinement.")
    args = parser.parse_args()

    path = args.docx.resolve()
    spec_path = args.spec or path.with_name("presentations_style.yaml")
    load_colors_from_yaml(spec_path)
    apply_table_style_refinements(path)
    used_com = False
    if args.word_com_save:
        used_com = normalize_with_word_com(path)
    print(f"Refined table styles in {path}")
    print(f"Word COM normalization: {'used' if used_com else 'not used'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
