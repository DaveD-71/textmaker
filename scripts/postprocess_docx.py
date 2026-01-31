"""
Claude edit
Post-process a DOCX produced by Pandoc to ensure:
- a section break is inserted immediately after the Table of Contents
- page numbering restarts at 1 for the following section
- page numbers are removed from TOC pages
- section breaks (nextPage) are inserted before each H1 heading
"""
# pylint: disable=protected-access,broad-exception-caught
try:
    from docx import Document  # type: ignore[reportMissingImports]
    from docx.oxml import OxmlElement  # type: ignore[reportMissingImports]
    from docx.oxml.ns import qn  # type: ignore[reportMissingImports]
except ImportError as exc:
    raise RuntimeError(
        'Missing dependency: python-docx is required. Install with `pip install python-docx`.'
    ) from exc


NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}


def _insert_section_break_before_paragraph(paragraph, restart_numbering=False, start_page=1):
    """
    Insert a nextPage section break BEFORE a paragraph by attaching sectPr
    to the PREVIOUS paragraph (that's how Word section breaks work).

    If restart_numbering=True, the new section will restart page numbering at start_page.
    """
    # Get the document and find the paragraph's position
    doc_element = paragraph._element.getparent()
    paragraphs = list(doc_element.iterchildren())

    try:
        current_index = paragraphs.index(paragraph._element)
    except ValueError:
        return False

    if current_index == 0:
        # Can't insert section break before first paragraph
        return False

    # Get the previous paragraph
    prev_p = paragraphs[current_index - 1]

    # Ensure previous paragraph has pPr
    p_pr = prev_p.find(qn('w:pPr'))
    if p_pr is None:
        p_pr = OxmlElement('w:pPr')
        prev_p.insert(0, p_pr)

    # Remove existing sectPr to avoid duplicates
    for sect in list(p_pr.findall(qn('w:sectPr'))):
        try:
            p_pr.remove(sect)
        except Exception:
            pass

    # Create new sectPr with nextPage type
    sect_pr = OxmlElement('w:sectPr')
    type_el = OxmlElement('w:type')
    type_el.set(qn('w:val'), 'nextPage')
    sect_pr.append(type_el)

    # Add page number restart if requested
    if restart_numbering:
        pg_num_type = OxmlElement('w:pgNumType')
        pg_num_type.set(qn('w:start'), str(start_page))
        sect_pr.append(pg_num_type)

    p_pr.append(sect_pr)
    return True


def _apply_next_page_section_to_paragraph(paragraph, start_page=None):
    """Attach a nextPage sectPr (and optional page-number restart) to an existing paragraph."""
    p_pr = paragraph._p.find(qn('w:pPr'))
    if p_pr is None:
        p_pr = OxmlElement('w:pPr')
        paragraph._p.insert(0, p_pr)

    # Remove existing sectPr to avoid multiple
    for sect in list(p_pr.findall(qn('w:sectPr'))):
        try:
            p_pr.remove(sect)
        except Exception:
            pass

    sect_pr = OxmlElement('w:sectPr')
    type_el = OxmlElement('w:type')
    type_el.set(qn('w:val'), 'nextPage')
    sect_pr.append(type_el)

    if start_page is not None:
        pg_num_type = OxmlElement('w:pgNumType')
        pg_num_type.set(qn('w:start'), str(start_page))
        sect_pr.append(pg_num_type)

    p_pr.append(sect_pr)


def _remove_page_numbers_from_footer(footer):
    """Remove PAGE field codes from a footer to suppress page numbers."""
    try:
        for para in footer.paragraphs:
            runs_to_remove = []
            for run in para.runs:
                # Check if run contains PAGE field
                run_elem = run._element
                fld_simple = run_elem.find('.//w:fldSimple', NS)
                fld_char = run_elem.find('.//w:fldChar', NS)
                instr_text = run_elem.find('.//w:instrText', NS)

                # If it's a field related to page numbers, mark for removal
                if fld_simple is not None:
                    instr = fld_simple.get(qn('w:instr'), '')
                    if 'PAGE' in instr.upper():
                        runs_to_remove.append(run)
                elif instr_text is not None:
                    if 'PAGE' in (instr_text.text or '').upper():
                        runs_to_remove.append(run)
                elif fld_char is not None:
                    # Part of a complex field - check if any instrText nearby contains PAGE
                    all_instr = run_elem.findall('.//w:instrText', NS)
                    for it in all_instr:
                        if 'PAGE' in (it.text or '').upper():
                            runs_to_remove.append(run)
                            break

            # Remove the marked runs
            for run in runs_to_remove:
                para._element.remove(run._element)
    except Exception as e:
        print(f"Warning: Could not remove page numbers from footer: {e}")


def _is_heading_1(paragraph):
    """Check if paragraph is styled as Heading 1."""
    style = paragraph.style
    if style and 'Heading 1' in style.name:
        return True
    # Also check by style_id
    if hasattr(style, 'style_id') and style.style_id == 'Heading1':
        return True
    return False


def insert_section_breaks_before_h1(doc, skip_first=True, restart_first=False):
    """
    Insert nextPage section breaks before each H1 heading.

    Args:
        doc: Document object
        skip_first: If True, skip inserting section break before the first H1
        restart_first: If True and skip_first=False, restart page numbering at first H1
    """
    paragraphs = list(doc.paragraphs)
    h1_count = 0
    sections_added = 0

    for para in paragraphs:
        if _is_heading_1(para):
            h1_count += 1

            # Skip the first H1 if requested
            if skip_first and h1_count == 1:
                continue

            # Restart numbering on first H1 if requested (no TOC scenario)
            restart = (restart_first and h1_count == 1)

            try:
                success = _insert_section_break_before_paragraph(
                    para,
                    restart_numbering=restart,
                    start_page=1,
                )
                if success:
                    sections_added += 1
            except Exception as e:
                print(f"Warning: Could not insert section break before H1 '{para.text}': {e}")

    return sections_added


def _qn_attr(nsmap, attr):
    return f'{{{nsmap.get("w")}}}{attr}'


def _build_num_format_map(doc):
    """Map numId/ilvl to numFmt (e.g., bullet, decimal)."""
    try:
        num_part = doc.part.numbering_part.element
    except Exception:
        return {}
    nsmap = num_part.nsmap

    abstract_map = {}
    for abs_num in num_part.findall('w:abstractNum', nsmap):
        abs_id = abs_num.get(_qn_attr(nsmap, 'abstractNumId'))
        lvl_map = {}
        for lvl in abs_num.findall('w:lvl', nsmap):
            ilvl = lvl.get(_qn_attr(nsmap, 'ilvl'))
            numfmt_el = lvl.find('w:numFmt', nsmap)
            if ilvl is not None and numfmt_el is not None:
                lvl_map[ilvl] = numfmt_el.get(_qn_attr(nsmap, 'val'))
        if abs_id is not None:
            abstract_map[abs_id] = lvl_map

    num_map = {}
    for num in num_part.findall('w:num', nsmap):
        num_id = num.get(_qn_attr(nsmap, 'numId'))
        abs_el = num.find('w:abstractNumId', nsmap)
        if num_id is None or abs_el is None:
            continue
        abs_id = abs_el.get(_qn_attr(nsmap, 'val'))
        num_map[num_id] = abstract_map.get(abs_id, {})

    return num_map


def _get_style_by_name_or_id(styles, target):
    """Fetch a style by name or style_id; returns None if missing."""
    try:
        return styles[target]
    except Exception:
        pass
    for st in styles:
        if getattr(st, 'name', None) == target or getattr(st, 'style_id', None) == target:
            return st
    return None


def apply_list_styles(doc, bullet_style='List Bullet 2', number_style='List Number 2'):
    """
    Apply specific styles to bullet and numbered list paragraphs.

    Bullets -> bullet_style; others with numbering -> number_style.
    """
    num_map = _build_num_format_map(doc)
    styles = doc.styles
    bullet = _get_style_by_name_or_id(styles, bullet_style) or _get_style_by_name_or_id(
        styles,
        bullet_style.replace(' ', ''),
    )
    number = _get_style_by_name_or_id(styles, number_style) or _get_style_by_name_or_id(
        styles,
        number_style.replace(' ', ''),
    )
    if not bullet and not number:
        return 0

    applied = 0
    for para in doc.paragraphs:
        p_pr = para._p.find(qn('w:pPr'))
        if p_pr is None:
            continue
        num_pr = p_pr.find(qn('w:numPr'))
        if num_pr is None:
            continue
        num_id_el = num_pr.find(qn('w:numId'))
        ilvl_el = num_pr.find(qn('w:ilvl'))
        if num_id_el is None:
            continue
        num_id = num_id_el.get(qn('w:val'))
        ilvl = ilvl_el.get(qn('w:val')) if ilvl_el is not None else '0'
        fmt = None
        if num_id in num_map:
            fmt = num_map[num_id].get(ilvl)
        if fmt == 'bullet' and bullet:
            para.style = bullet
            applied += 1
        elif fmt and fmt != 'bullet' and number:
            para.style = number
            applied += 1
    return applied


def insert_section_after_toc(docx_path, has_toc=True, insert_h1_sections=True):
    """
    Post-process `docx_path` to:
    1. If has_toc: Insert section break after TOC, restart page numbering at 1, remove page numbers
       from TOC
    2. Insert section breaks before H1 headings:
       - With TOC: skip first H1 (numbering already restarted after TOC)
       - Without TOC: restart numbering at first H1
    """
    doc = Document(docx_path)
    paragraphs = list(doc.paragraphs)

    # Find the last paragraph that contains a TOC field
    toc_par_index = None
    if has_toc:
        for i, p in enumerate(paragraphs):
            # Search for fldSimple elements in this paragraph
            fld_simples = p._p.findall('.//w:fldSimple', NS)
            for fld in fld_simples:
                instr = fld.get(qn('w:instr')) or fld.get('instr')
                if instr and instr.strip().upper().startswith('TOC'):
                    toc_par_index = i
            # Also check for complex fldChar representation
            fld_chars = p._p.findall('.//w:fldChar', NS)
            if fld_chars:
                instr_texts = p._p.findall('.//w:instrText', NS)
                for it in instr_texts:
                    if it.text and it.text.strip().upper().startswith('TOC'):
                        toc_par_index = i

    made_change = False

    if toc_par_index is not None:
        toc_par = paragraphs[toc_par_index]

        # STEP 1: Insert section break after TOC with page restart
        try:
            _apply_next_page_section_to_paragraph(toc_par, start_page=1)
            made_change = True
            print('Inserted section break after TOC with page numbering restart at 1')
        except Exception as e:
            print(f'Warning: Could not insert section break after TOC: {e}')

        # STEP 2: Remove page numbers from TOC section footer
        # Must happen AFTER creating the section break so we target the correct section
        try:
            # Reload document to get updated sections
            doc.save(docx_path)
            doc = Document(docx_path)

            # The TOC is now in section 0 (before the section break we just added)
            if len(doc.sections) > 0:
                toc_section = doc.sections[0]
                _remove_page_numbers_from_footer(toc_section.footer)

                # Also try first_page_footer if it exists
                try:
                    _remove_page_numbers_from_footer(toc_section.first_page_footer)
                except Exception:
                    pass

                print('Removed page numbers from TOC section')
                made_change = True
        except Exception as e:
            print(f'Warning: Could not remove page numbers from TOC: {e}')

    # Insert section breaks before H1 headings
    if insert_h1_sections:
        try:
            # With TOC: skip first H1 (already have section break after TOC)
            # Without TOC: don't skip, but restart numbering at first H1
            sections_added = insert_section_breaks_before_h1(
                doc,
                skip_first=has_toc,
                restart_first=not has_toc,
            )
            if sections_added > 0:
                print(f'Inserted {sections_added} section break(s) before H1 headings')
                made_change = True
        except Exception as e:
            print(f'Warning: Could not insert H1 section breaks: {e}')

    # Apply list styles to bullets/numbers if available
    try:
        applied = apply_list_styles(doc)
        if applied > 0:
            print(f'Applied list styles to {applied} paragraph(s)')
            made_change = True
    except Exception as e:
        print(f'Warning: Could not apply list styles: {e}')

    if made_change:
        doc.save(docx_path)

    return made_change


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('docx', help='DOCX file to postprocess')
    parser.add_argument('--toc', action='store_true', default=True, help='Document has TOC')
    parser.add_argument(
        '--no-h1-sections',
        action='store_true',
        help='Skip inserting section breaks before H1s',
    )
    args = parser.parse_args()

    did_update = insert_section_after_toc(
        args.docx,
        has_toc=args.toc,
        insert_h1_sections=not args.no_h1_sections,
    )

    if did_update:
        print('Post-processing complete.')
    else:
        print('No changes made.')
