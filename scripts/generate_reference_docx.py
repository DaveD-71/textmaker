"""
Generate a `reference.docx` with basic modern professional styles.
This uses `python-docx` to set Normal and Heading styles and A4 page size.
Run: python scripts/generate_reference_docx.py --out reference.docx
"""
# pylint: disable=protected-access,broad-exception-caught
import argparse
import sys
try:
    # type: ignore[reportMissingImports]
    from docx import Document
    # type: ignore[reportMissingImports]
    from docx.shared import Mm, Pt, RGBColor
    # type: ignore[reportMissingImports]
    from docx.enum.style import WD_STYLE_TYPE
    # type: ignore[reportMissingImports]
    from docx.oxml import OxmlElement
    # type: ignore[reportMissingImports]
    from docx.oxml.ns import qn
    # type: ignore[reportMissingImports]
    from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
except ModuleNotFoundError as _err:
    # Only convert missing-docx into a helpful message; bubble up other missing deps.
    missing_name = getattr(_err, 'name', '') or ''
    if isinstance(missing_name, str) and missing_name.startswith('docx'):
        raise RuntimeError(
            "Missing dependency: python-docx is required. Install with `pip install python-docx` and retry."
        ) from _err
    raise
except ImportError as _err:
    # For other import issues, expose the original message so environment problems surface.
    raise RuntimeError(f"Failed to import python-docx dependency: {_err}") from _err
    # end of import guard


def create_reference(path: str):
    """Create a reference DOCX containing the project's base styles.

    The generated file can be used with Pandoc's `--reference-doc` option
    to control Word styles for converted documents.
    """
    doc = Document()
    section = doc.sections[0]
    # A4 page size
    section.page_height = Mm(297)
    section.page_width = Mm(210)
    # margins (user requested A4 portrait with top 3.5cm, other margins 3.0cm)
    section.top_margin = Mm(35)
    section.bottom_margin = Mm(30)
    section.left_margin = Mm(30)
    section.right_margin = Mm(30)

    styles = doc.styles

    # Fonts from the current reference.docx
    body_font = 'Noto Serif'
    heading1_font = 'Noto Sans Condensed ExtraBold'
    heading2_font = 'Noto Sans SemiCondensed Light'
    heading3_font = 'Noto Sans SemiCondensed SemiBold'
    heading4_font = 'Segoe UI Semibold'
    heading5_font = 'Segoe UI Semibold'
    caption_font = 'Segoe UI Semibold'
    block_font = 'Noto Sans SemiCondensed Light'
    list_font = 'Noto Serif ExtraLight'
    code_font = 'Cascadia Code'

    def _set_style_rfonts(style, font_name: str):
        """Ensure the style's run properties include explicit rFonts to override theme fonts."""
        try:
            el = style._element
            rPr = el.find(qn('w:rPr'))
            if rPr is None:
                rPr = OxmlElement('w:rPr')
                el.insert(0, rPr)
            rfonts = OxmlElement('w:rFonts')
            rfonts.set(qn('w:ascii'), font_name)
            rfonts.set(qn('w:hAnsi'), font_name)
            rfonts.set(qn('w:cs'), font_name)
            rPr.append(rfonts)
        except Exception:
            # best-effort; ignore if style internals differ
            pass

    # Normal (body) style
    normal = styles['Normal']
    normal.font.name = body_font
    normal.font.size = Pt(11)
    pformat = normal.paragraph_format
    pformat.space_before = Pt(0)
    pformat.space_after = Pt(12)
    pformat.line_spacing = 1.2  # yields w:line 288
    pformat.first_line_indent = Mm(0)
    _set_style_rfonts(normal, body_font)

    # Heading 1
    if 'Heading 1' in styles:
        h1 = styles['Heading 1']
        h1.font.name = heading1_font
        h1.font.size = Pt(24)
        h1.font.bold = False
        h1.font.color.rgb = RGBColor(0, 0, 0)
        h1.paragraph_format.space_before = Pt(30)
        h1.paragraph_format.space_after = Pt(30)
        h1.paragraph_format.line_spacing = 1.0
        h1.paragraph_format.page_break_before = False
        _set_style_rfonts(h1, heading1_font)

    # Heading 2
    if 'Heading 2' in styles:
        h2 = styles['Heading 2']
        h2.font.name = heading2_font
        h2.font.size = Pt(20)
        h2.font.bold = False
        h2.font.color.rgb = RGBColor(0, 0, 0)
        h2.paragraph_format.space_before = Pt(36)
        h2.paragraph_format.space_after = Pt(16)
        h2.paragraph_format.line_spacing = 0.8
        _set_style_rfonts(h2, heading2_font)

    # Heading 3
    if 'Heading 3' in styles:
        h3 = styles['Heading 3']
        h3.font.name = heading3_font
        h3.font.size = Pt(16)
        h3.font.bold = False
        h3.font.color.rgb = RGBColor(0, 0, 0)
        h3.paragraph_format.space_before = Pt(20)
        h3.paragraph_format.space_after = Pt(8)
        h3.paragraph_format.line_spacing = 1.0
        _set_style_rfonts(h3, heading3_font)

    # Heading 4
    if 'Heading 4' in styles:
        h4 = styles['Heading 4']
        h4.font.name = heading4_font
        h4.font.size = Pt(12)
        h4.font.bold = False
        h4.font.color.rgb = RGBColor(0, 0, 0)
        h4.paragraph_format.space_before = Pt(8)
        h4.paragraph_format.space_after = Pt(4)
        _set_style_rfonts(h4, heading4_font)

    # Heading 5
    if 'Heading 5' in styles:
        h5 = styles['Heading 5']
        h5.font.name = heading5_font
        h5.font.size = Pt(11)
        h5.font.bold = False
        h5.font.color.rgb = RGBColor(0, 0, 0)
        h5.paragraph_format.space_before = Pt(6)
        h5.paragraph_format.space_after = Pt(4)
        _set_style_rfonts(h5, heading5_font)

    # Caption style
    if 'Caption' not in styles:
        caption = styles.add_style('Caption', WD_STYLE_TYPE.PARAGRAPH)
    else:
        caption = styles['Caption']
    caption.font.name = caption_font
    caption.font.size = Pt(9)
    caption.font.italic = False
    caption.font.color.rgb = RGBColor(0x4F, 0x81, 0xBD)
    caption.paragraph_format.space_before = Pt(4)
    caption.paragraph_format.space_after = Pt(6)
    caption.paragraph_format.line_spacing = 1.0
    _set_style_rfonts(caption, caption_font)

    def _ensure_paragraph_properties(style):
        el = style._element
        p_pr = el.find(qn('w:pPr'))
        if p_pr is None:
            p_pr = OxmlElement('w:pPr')
            el.insert(0, p_pr)
        return p_pr

    def _set_p_borders(style, borders):
        """Apply paragraph borders to a style using w:pBdr."""
        p_pr = _ensure_paragraph_properties(style)
        for existing in list(p_pr.findall(qn('w:pBdr'))):
            p_pr.remove(existing)
        if not borders:
            return
        p_bdr = OxmlElement('w:pBdr')
        for side, attrs in borders.items():
            # OxmlElement expects the prefixed name (w:top), not the expanded qn()
            side_el = OxmlElement(f'w:{side}')
            for key, val in attrs.items():
                side_el.set(qn(f'w:{key}'), str(val))
            p_bdr.append(side_el)
        p_pr.append(p_bdr)

    def _set_shading(style, fill, color="auto", val="clear", theme_fill=None, theme_shade=None):
        """Apply paragraph shading to a style."""
        p_pr = _ensure_paragraph_properties(style)
        for existing in list(p_pr.findall(qn('w:shd'))):
            p_pr.remove(existing)
        shd = OxmlElement('w:shd')
        shd.set(qn('w:val'), val)
        shd.set(qn('w:color'), color)
        shd.set(qn('w:fill'), fill)
        if theme_fill:
            shd.set(qn('w:themeFill'), theme_fill)
        if theme_shade:
            shd.set(qn('w:themeFillShade'), theme_shade)
        p_pr.append(shd)

    # Block Text (base for Intense Quote)
    if 'Block Text' not in styles:
        block_text = styles.add_style('Block Text', WD_STYLE_TYPE.PARAGRAPH)
    else:
        block_text = styles['Block Text']
    block_text.base_style = styles['Normal']
    block_text.font.name = block_font
    _set_style_rfonts(block_text, block_font)
    block_text.paragraph_format.left_indent = Pt(56.7)   # ~1134 twips
    block_text.paragraph_format.right_indent = Pt(56.7)
    block_text.paragraph_format.space_before = Pt(18)
    block_text.paragraph_format.space_after = Pt(18)
    block_text.paragraph_format.line_spacing = 1.0
    _set_p_borders(
        block_text,
        {
            'top': {'val': 'single', 'sz': '8', 'space': '12', 'color': '808080', 'themeColor': 'background1', 'themeShade': '80'},
            'left': {'val': 'single', 'sz': '48', 'space': '18', 'color': '4BACC6', 'themeColor': 'accent5'},
            'bottom': {'val': 'single', 'sz': '8', 'space': '12', 'color': '808080', 'themeColor': 'background1', 'themeShade': '80'},
            'right': {'val': 'single', 'sz': '8', 'space': '18', 'color': '808080', 'themeColor': 'background1', 'themeShade': '80'},
        },
    )
    _set_shading(block_text, fill='F2F2F2', color='auto', val='clear', theme_fill='background1', theme_shade='F2')

    # Block quote style (Intense Quote) inherits Block Text and adds accent left border
    if 'Intense Quote' not in styles:
        bq = styles.add_style('Intense Quote', WD_STYLE_TYPE.PARAGRAPH)
    else:
        bq = styles['Intense Quote']
    bq.base_style = block_text
    _set_style_rfonts(bq, block_font)
    _set_p_borders(
        bq,
        {
            'left': {'val': 'single', 'sz': '48', 'space': '18', 'color': 'F79646', 'themeColor': 'accent6'},
        },
    )

    def _add_contextual_spacing(style):
        """Add w:contextualSpacing to a style's paragraph properties."""
        p_pr = _ensure_paragraph_properties(style)
        if p_pr.find(qn('w:contextualSpacing')) is None:
            p_pr.append(OxmlElement('w:contextualSpacing'))

    # List Paragraph style
    if 'List Paragraph' not in styles:
        list_style = styles.add_style('List Paragraph', WD_STYLE_TYPE.PARAGRAPH)
    else:
        list_style = styles['List Paragraph']
    list_style.base_style = styles['Normal']
    list_style.font.name = list_font
    list_style.font.italic = True
    _set_style_rfonts(list_style, list_font)
    _add_contextual_spacing(list_style)

    # List Bullet 2
    if 'List Bullet 2' not in styles and 'ListBullet2' not in styles:
        list_bullet2 = styles.add_style('List Bullet 2', WD_STYLE_TYPE.PARAGRAPH)
    else:
        list_bullet2 = styles['List Bullet 2'] if 'List Bullet 2' in styles else styles['ListBullet2']
    list_bullet2.base_style = styles['Normal']
    _add_contextual_spacing(list_bullet2)

    # List Number 2
    if 'List Number 2' not in styles and 'ListNumber2' not in styles:
        list_number2 = styles.add_style('List Number 2', WD_STYLE_TYPE.PARAGRAPH)
    else:
        list_number2 = styles['List Number 2'] if 'List Number 2' in styles else styles['ListNumber2']
    list_number2.base_style = styles['Normal']
    _add_contextual_spacing(list_number2)

    # Monospace / code style
    if 'Code' not in styles:
        code_style = styles.add_style('Code', WD_STYLE_TYPE.PARAGRAPH)
    else:
        code_style = styles['Code']
    code_style.font.name = code_font
    code_style.font.size = Pt(10)
    code_style.paragraph_format.space_before = Pt(4)
    code_style.paragraph_format.space_after = Pt(4)
    _set_style_rfonts(code_style, code_font)

    # Header placeholder (document title, editable in Word)
    header = section.header
    hdr_p = header.paragraphs[0]
    hdr_p.text = ''
    hdr_p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    hdr_p.style = styles['Normal']

    # Footer with centered page number field
    footer = section.footer
    f_p = footer.paragraphs[0]
    f_p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    # insert PAGE field
    fld_simple = OxmlElement('w:fldSimple')
    fld_simple.set(qn('w:instr'), 'PAGE')
    run_elem = OxmlElement('w:r')
    run_elem.append(fld_simple)
    f_p._p.append(run_elem)

    doc.add_paragraph('Reference docx for styles — remove this placeholder page before use.')
    doc.save(path)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', default='reference.docx', help='Output path for reference DOCX')
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    create_reference(args.out)
    print(f'Wrote reference docx to {args.out}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
