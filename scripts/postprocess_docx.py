"""
Claude edit
Post-process a DOCX produced by Pandoc to ensure:
- a section break is inserted immediately after the Table of Contents
- page numbering restarts at 1 for the following section
- page numbers are removed from TOC pages
- section breaks (nextPage) are inserted before each H1 heading
"""
try:
    from docx import Document
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.enum.section import WD_SECTION
except ImportError as exc:
    raise RuntimeError('Missing dependency: python-docx is required. Install with `pip install python-docx`.') from exc


NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}


def _make_sect_pr_with_page_start(start=1):
    sect_pr = OxmlElement('w:sectPr')
    pg_num_type = OxmlElement('w:pgNumType')
    pg_num_type.set(qn('w:start'), str(start))
    sect_pr.append(pg_num_type)
    return sect_pr


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
                    all_instr = run_elem.xpath('.//w:instrText', namespaces=NS)
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
                success = _insert_section_break_before_paragraph(para, restart_numbering=restart, start_page=1)
                if success:
                    sections_added += 1
            except Exception as e:
                print(f"Warning: Could not insert section break before H1 '{para.text}': {e}")
    
    return sections_added


def insert_section_after_toc(docx_path, has_toc=True, insert_h1_sections=True):
    """
    Post-process `docx_path` to:
    1. If has_toc: Insert section break after TOC, restart page numbering at 1, remove page numbers from TOC
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
            fld_simples = p._p.xpath('.//w:fldSimple', namespaces=NS)
            for fld in fld_simples:
                instr = fld.get(qn('w:instr')) or fld.get('instr')
                if instr and instr.strip().upper().startswith('TOC'):
                    toc_par_index = i
            # Also check for complex fldChar representation
            fld_chars = p._p.xpath('.//w:fldChar', namespaces=NS)
            if fld_chars:
                instr_texts = p._p.xpath('.//w:instrText', namespaces=NS)
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
            print("Inserted section break after TOC with page numbering restart at 1")
        except Exception as e:
            print(f"Warning: Could not insert section break after TOC: {e}")
        
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
                except:
                    pass
                
                print("Removed page numbers from TOC section")
                made_change = True
        except Exception as e:
            print(f"Warning: Could not remove page numbers from TOC: {e}")

    # Insert section breaks before H1 headings
    if insert_h1_sections:
        try:
            # With TOC: skip first H1 (already have section break after TOC)
            # Without TOC: don't skip, but restart numbering at first H1
            sections_added = insert_section_breaks_before_h1(
                doc, 
                skip_first=has_toc,
                restart_first=not has_toc
            )
            if sections_added > 0:
                print(f"Inserted {sections_added} section break(s) before H1 headings")
                made_change = True
        except Exception as e:
            print(f"Warning: Could not insert H1 section breaks: {e}")

    if made_change:
        doc.save(docx_path)
    
    return made_change


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('docx', help='DOCX file to postprocess')
    parser.add_argument('--toc', action='store_true', default=True, help='Document has TOC')
    parser.add_argument('--no-h1-sections', action='store_true', help='Skip inserting section breaks before H1s')
    args = parser.parse_args()
    
    ok = insert_section_after_toc(
        args.docx, 
        has_toc=args.toc,
        insert_h1_sections=not args.no_h1_sections
    )
    
    if ok:
        print('Post-processing complete.')
    else:
        print('No changes made.')
