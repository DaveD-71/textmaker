"""
Generate a `reference.docx` with basic modern professional styles.
This uses `python-docx` to set Normal and Heading styles and A4 page size.
Run: python scripts/generate_reference_docx.py --out reference.docx
"""
import argparse
try:
    # type: ignore
    from docx import Document
    # type: ignore
    from docx.shared import Mm, Pt, RGBColor
    # type: ignore
    from docx.enum.style import WD_STYLE_TYPE
    # type: ignore
    from docx.oxml import OxmlElement
    # type: ignore
    from docx.oxml.ns import qn
    # type: ignore
    from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
except ModuleNotFoundError as _err:
    # Only convert missing-docx into a helpful message; bubble up other missing deps.
    if _err.name and _err.name.startswith('docx'):
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

    # Modern, clean pairing similar to VS Code Live Preview: Segoe UI for body/headings
    body_font = 'Segoe UI'
    heading_font = 'Segoe UI Semibold'

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
    pformat.space_after = Pt(8)
    pformat.line_spacing = 1.5
    pformat.first_line_indent = Mm(0)

    # Heading 1
    if 'Heading 1' in styles:
        h1 = styles['Heading 1']
        h1.font.name = heading_font
        h1.font.size = Pt(20)
        h1.font.bold = False
        h1.font.color.rgb = RGBColor(0, 0, 0)
        h1.paragraph_format.space_before = Pt(16)
        h1.paragraph_format.space_after = Pt(10)
        h1.paragraph_format.line_spacing = 1.2
        h1.paragraph_format.page_break_before = True
        _set_style_rfonts(h1, heading_font)

    # Heading 2
    if 'Heading 2' in styles:
        h2 = styles['Heading 2']
        h2.font.name = heading_font
        h2.font.size = Pt(16)
        h2.font.bold = False
        h2.font.color.rgb = RGBColor(0, 0, 0)
        h2.paragraph_format.space_before = Pt(12)
        h2.paragraph_format.space_after = Pt(8)
        h2.paragraph_format.line_spacing = 1.2
        _set_style_rfonts(h2, heading_font)

    # Heading 3
    if 'Heading 3' in styles:
        h3 = styles['Heading 3']
        h3.font.name = heading_font
        h3.font.size = Pt(13)
        h3.font.bold = False
        h3.font.color.rgb = RGBColor(0, 0, 0)
        h3.paragraph_format.space_before = Pt(10)
        h3.paragraph_format.space_after = Pt(6)
        h3.paragraph_format.line_spacing = 1.2
        _set_style_rfonts(h3, heading_font)

    # Heading 4
    if 'Heading 4' in styles:
        h4 = styles['Heading 4']
        h4.font.name = heading_font
        h4.font.size = Pt(12)
        h4.font.bold = False
        h4.font.color.rgb = RGBColor(0, 0, 0)
        h4.paragraph_format.space_before = Pt(8)
        h4.paragraph_format.space_after = Pt(4)
        h4.paragraph_format.line_spacing = 1.2
        _set_style_rfonts(h4, heading_font)

    # Heading 5
    if 'Heading 5' in styles:
        h5 = styles['Heading 5']
        h5.font.name = heading_font
        h5.font.size = Pt(11)
        h5.font.bold = False
        h5.font.color.rgb = RGBColor(0, 0, 0)
        h5.paragraph_format.space_before = Pt(6)
        h5.paragraph_format.space_after = Pt(4)
        h5.paragraph_format.line_spacing = 1.2
        _set_style_rfonts(h5, heading_font)

    # Caption style
    if 'Caption' not in styles:
        caption = styles.add_style('Caption', WD_STYLE_TYPE.PARAGRAPH)
    else:
        caption = styles['Caption']
    caption.font.name = heading_font
    caption.font.size = Pt(9)
    caption.font.italic = True
    caption.paragraph_format.space_before = Pt(4)
    caption.paragraph_format.space_after = Pt(6)
    _set_style_rfonts(caption, heading_font)

    # Block quote style
    if 'Intense Quote' in styles:
        bq = styles['Intense Quote']
    else:
        bq = styles.add_style('Intense Quote', WD_STYLE_TYPE.PARAGRAPH)
    bq.font.name = body_font
    bq.font.size = Pt(11)
    bq.paragraph_format.left_indent = Mm(6)
    bq.paragraph_format.space_before = Pt(6)
    bq.paragraph_format.space_after = Pt(6)
    bq.paragraph_format.line_spacing = 1.4
    _set_style_rfonts(bq, body_font)

    # Monospace / code style
    if 'Code' not in styles:
        code_style = styles.add_style('Code', WD_STYLE_TYPE.PARAGRAPH)
    else:
        code_style = styles['Code']
    code_style.font.name = 'Cascadia Code'
    code_style.font.size = Pt(10)
    code_style.paragraph_format.space_before = Pt(4)
    code_style.paragraph_format.space_after = Pt(4)
    _set_style_rfonts(code_style, 'Cascadia Code')

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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', default='reference.docx', help='Output path for reference DOCX')
    args = parser.parse_args()
    create_reference(args.out)
    print(f'Wrote reference docx to {args.out}')
