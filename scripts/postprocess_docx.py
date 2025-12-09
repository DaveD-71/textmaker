"""
Post-process a DOCX produced by Pandoc to ensure:
- a section break is inserted immediately after the Table of Contents
- page numbering restarts at 1 for the following section

This manipulates the underlying XML to add a <w:pgNumType w:start="1"/> inside a
<sectionProperties> (<w:sectPr>) that ends the TOC section.
"""
try:
    # type: ignore
    from docx import Document
    # type: ignore
    from docx.oxml import OxmlElement
    # type: ignore
    from docx.oxml.ns import qn
except ImportError as exc:
    raise RuntimeError('Missing dependency: python-docx is required. Install with `pip install python-docx`.') from exc


NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}


def _make_sect_pr_with_page_start(start=1):
    sect_pr = OxmlElement('w:sectPr')
    pg_num_type = OxmlElement('w:pgNumType')
    pg_num_type.set(qn('w:start'), str(start))
    sect_pr.append(pg_num_type)
    return sect_pr


def _apply_next_page_section_to_paragraph(paragraph, start_page=None):
    """Attach a nextPage sectPr (and optional page-number restart) to an existing paragraph."""
    p_pr = paragraph._p.find(qn('w:pPr'))
    if p_pr is None:
        p_pr = OxmlElement('w:pPr')
        paragraph._p.insert(0, p_pr)
    # remove existing sectPr to avoid multiple
    for sect in list(p_pr.findall('w:sectPr', NS)):
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


def insert_section_after_toc(docx_path, has_toc=True):
    """Post-process `docx_path` to insert a section break after the TOC and restart page numbering."""
    doc = Document(docx_path)
    paragraphs = list(doc.paragraphs)

    # Find the last paragraph that contains a TOC field (w:fldSimple with instr starting 'TOC')
    toc_par_index = None
    if has_toc:
        for i, p in enumerate(paragraphs):
            # search for fldSimple elements in this paragraph
            fld_simples = p._p.xpath('.//w:fldSimple', namespaces=NS)
            for fld in fld_simples:
                instr = fld.get(qn('w:instr')) or fld.get('instr')
                if instr and instr.strip().upper().startswith('TOC'):
                    toc_par_index = i
            # also check for complex fldChar representation
            fld_chars = p._p.xpath('.//w:fldChar', namespaces=NS)
            if fld_chars:
                # check if this paragraph contains instrText child anywhere up the run sequence
                instr_texts = p._p.xpath('.//w:instrText', namespaces=NS)
                for it in instr_texts:
                    if it.text and it.text.strip().upper().startswith('TOC'):
                        toc_par_index = i

    made_change = False

    if toc_par_index is not None:
        toc_par = paragraphs[toc_par_index]
        # ensure paragraph has pPr
        p_pr = toc_par._p.find(qn('w:pPr'))
        if p_pr is None:
            p_pr = OxmlElement('w:pPr')
            toc_par._p.insert(0, p_pr)

        # Attempt to suppress page numbers in the initial section (TOC) footer
        try:
            # clear PAGE fields from the first section footer runs (so TOC shows no page number)
            first_section = doc.sections[0]
            for fp in first_section.footer.paragraphs:
                # remove runs that contain a PAGE field
                runs = list(fp._p.findall('.//w:r', NS))
                for r in runs:
                    fld_simple = r.find('.//w:fldSimple', NS)
                    fld_char = r.find('.//w:fldChar', NS)
                    instr_text = r.find('.//w:instrText', NS)
                    if fld_simple is not None or fld_char is not None or instr_text is not None:
                        try:
                            fp._p.remove(r)
                        except Exception:
                            # ignore remove failures for individual runs
                            pass
        except Exception:
            # best-effort footer cleanup; continue even if it fails
            pass

        # Attach a sectPr that is a "nextPage" section with page numbering restarted at 1.
        try:
            _apply_next_page_section_to_paragraph(toc_par, start_page=1)
            made_change = True
        except Exception:
            # fallback: append sectPr to existing pPr if insertion fails
            try:
                sect_pr = _make_sect_pr_with_page_start(1)
                p_pr.append(sect_pr)
                made_change = True
            except Exception:
                pass

    if made_change:
        doc.save(docx_path)
    return made_change


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('docx', help='DOCX file to postprocess')
    args = parser.parse_args()
    ok = insert_section_after_toc(args.docx)
    if ok:
        print('Inserted section break after TOC and restarted page numbering.')
    else:
        print('No section breaks inserted.')
