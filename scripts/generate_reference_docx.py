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
    # Use neutral manuscript margins to better match markdown preview density.
    section.top_margin = Mm(25.4)
    section.bottom_margin = Mm(25.4)
    section.left_margin = Mm(25.4)
    section.right_margin = Mm(25.4)

    styles = doc.styles

    # VS Code markdown preview settings:
    # - markdown.preview.fontFamily defaults to a system sans stack (Segoe UI on Windows)
    # - markdown.preview.fontSize is set to 12 in this environment
    # - markdown.preview.lineHeight default is 1.6
    body_font = 'Segoe UI'
    heading_font = 'Segoe UI Semibold'
    caption_font = 'Segoe UI'
    code_font = 'Consolas'
    base_font_size_pt = 12.0
    base_line_height = 1.6

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

    def _set_shading(style, fill=None, color="auto", val="clear", theme_fill=None, theme_shade=None):
        """Apply paragraph shading to a style; pass fill=None to clear shading."""
        p_pr = _ensure_paragraph_properties(style)
        for existing in list(p_pr.findall(qn('w:shd'))):
            p_pr.remove(existing)
        if fill is None:
            return
        shd = OxmlElement('w:shd')
        shd.set(qn('w:val'), val)
        shd.set(qn('w:color'), color)
        shd.set(qn('w:fill'), fill)
        if theme_fill:
            shd.set(qn('w:themeFill'), theme_fill)
        if theme_shade:
            shd.set(qn('w:themeFillShade'), theme_shade)
        p_pr.append(shd)

    def _add_contextual_spacing(style):
        """Add w:contextualSpacing to a style's paragraph properties."""
        p_pr = _ensure_paragraph_properties(style)
        if p_pr.find(qn('w:contextualSpacing')) is None:
            p_pr.append(OxmlElement('w:contextualSpacing'))

    # Normal (body) style
    normal = styles['Normal']
    normal.font.name = body_font
    normal.font.size = Pt(base_font_size_pt)
    pformat = normal.paragraph_format
    pformat.space_before = Pt(0)
    pformat.space_after = Pt(12)
    pformat.line_spacing = base_line_height
    pformat.first_line_indent = Mm(0)
    _set_style_rfonts(normal, body_font)

    # Match markdown.css heading scale:
    # h1:2em, h2:1.5em, h3:1.25em, h4:1em, h5:0.875em, h6:0.85em
    heading_specs = (
        ('Heading 1', 24.0, 0.0, 12.0, True),
        ('Heading 2', 18.0, 18.0, 12.0, True),
        ('Heading 3', 15.0, 18.0, 12.0, False),
        ('Heading 4', 12.0, 18.0, 12.0, False),
        ('Heading 5', 10.5, 18.0, 12.0, False),
        ('Heading 6', 10.2, 18.0, 12.0, False),
    )
    for name, size_pt, before_pt, after_pt, with_bottom_rule in heading_specs:
        if name not in styles:
            continue
        heading = styles[name]
        heading.font.name = heading_font
        heading.font.size = Pt(size_pt)
        heading.font.bold = True
        heading.font.color.rgb = RGBColor(0, 0, 0)
        heading.paragraph_format.space_before = Pt(before_pt)
        heading.paragraph_format.space_after = Pt(after_pt)
        heading.paragraph_format.line_spacing = 1.25
        heading.paragraph_format.page_break_before = False
        _set_style_rfonts(heading, heading_font)
        if with_bottom_rule:
            _set_p_borders(
                heading,
                {
                    'bottom': {'val': 'single', 'sz': '6', 'space': '2', 'color': 'D0D7DE'},
                },
            )
        else:
            _set_p_borders(heading, None)

    # Caption style
    if 'Caption' not in styles:
        caption = styles.add_style('Caption', WD_STYLE_TYPE.PARAGRAPH)
    else:
        caption = styles['Caption']
    caption.font.name = caption_font
    caption.font.size = Pt(10)
    caption.font.italic = False
    caption.font.color.rgb = RGBColor(0x57, 0x57, 0x57)
    caption.paragraph_format.space_before = Pt(6)
    caption.paragraph_format.space_after = Pt(6)
    caption.paragraph_format.line_spacing = base_line_height
    _set_style_rfonts(caption, caption_font)

    # Block Text (used for markdown blockquotes)
    if 'Block Text' not in styles:
        block_text = styles.add_style('Block Text', WD_STYLE_TYPE.PARAGRAPH)
    else:
        block_text = styles['Block Text']
    block_text.base_style = styles['Normal']
    block_text.font.name = body_font
    _set_style_rfonts(block_text, body_font)
    block_text.paragraph_format.left_indent = Pt(10)
    block_text.paragraph_format.right_indent = Pt(16)
    block_text.paragraph_format.space_before = Pt(0)
    block_text.paragraph_format.space_after = Pt(12)
    block_text.paragraph_format.line_spacing = base_line_height
    _set_p_borders(
        block_text,
        {
            'left': {'val': 'single', 'sz': '30', 'space': '8', 'color': 'D0D7DE'},
        },
    )
    _set_shading(block_text, fill=None)

    # Intense Quote should follow the same subdued blockquote styling.
    if 'Intense Quote' not in styles:
        bq = styles.add_style('Intense Quote', WD_STYLE_TYPE.PARAGRAPH)
    else:
        bq = styles['Intense Quote']
    bq.base_style = block_text
    _set_style_rfonts(bq, body_font)
    _set_p_borders(
        bq,
        {
            'left': {'val': 'single', 'sz': '30', 'space': '8', 'color': 'D0D7DE'},
        },
    )
    _set_shading(bq, fill=None)

    # List styles inherit the same body typography as markdown preview.
    if 'List Paragraph' not in styles:
        list_style = styles.add_style('List Paragraph', WD_STYLE_TYPE.PARAGRAPH)
    else:
        list_style = styles['List Paragraph']
    list_style.base_style = styles['Normal']
    list_style.font.name = body_font
    list_style.font.italic = False
    list_style.paragraph_format.line_spacing = base_line_height
    list_style.paragraph_format.space_before = Pt(0)
    list_style.paragraph_format.space_after = Pt(8.4)
    _set_style_rfonts(list_style, body_font)
    _add_contextual_spacing(list_style)

    # List Bullet 2
    if 'List Bullet 2' not in styles and 'ListBullet2' not in styles:
        list_bullet2 = styles.add_style('List Bullet 2', WD_STYLE_TYPE.PARAGRAPH)
    else:
        list_bullet2 = styles['List Bullet 2'] if 'List Bullet 2' in styles else styles['ListBullet2']
    list_bullet2.base_style = styles['Normal']
    list_bullet2.paragraph_format.line_spacing = base_line_height
    list_bullet2.paragraph_format.space_before = Pt(0)
    list_bullet2.paragraph_format.space_after = Pt(8.4)
    _add_contextual_spacing(list_bullet2)

    # List Number 2
    if 'List Number 2' not in styles and 'ListNumber2' not in styles:
        list_number2 = styles.add_style('List Number 2', WD_STYLE_TYPE.PARAGRAPH)
    else:
        list_number2 = styles['List Number 2'] if 'List Number 2' in styles else styles['ListNumber2']
    list_number2.base_style = styles['Normal']
    list_number2.paragraph_format.line_spacing = base_line_height
    list_number2.paragraph_format.space_before = Pt(0)
    list_number2.paragraph_format.space_after = Pt(8.4)
    _add_contextual_spacing(list_number2)

    # Monospace / code style
    if 'Code' not in styles:
        code_style = styles.add_style('Code', WD_STYLE_TYPE.PARAGRAPH)
    else:
        code_style = styles['Code']
    code_style.base_style = styles['Normal']
    code_style.font.name = code_font
    code_style.font.size = Pt(base_font_size_pt)
    code_style.paragraph_format.space_before = Pt(12)
    code_style.paragraph_format.space_after = Pt(12)
    code_style.paragraph_format.line_spacing = 1.357
    _set_style_rfonts(code_style, code_font)
    _set_shading(code_style, fill='F6F8FA')
    _set_p_borders(
        code_style,
        {
            'top': {'val': 'single', 'sz': '6', 'space': '0', 'color': 'D0D7DE'},
            'left': {'val': 'single', 'sz': '6', 'space': '0', 'color': 'D0D7DE'},
            'bottom': {'val': 'single', 'sz': '6', 'space': '0', 'color': 'D0D7DE'},
            'right': {'val': 'single', 'sz': '6', 'space': '0', 'color': 'D0D7DE'},
        },
    )

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
