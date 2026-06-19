import fitz, pathlib, sys
pdf = pathlib.Path(sys.argv[1])
out_dir = pathlib.Path(sys.argv[2])
doc = fitz.open(pdf)
# PDF page index -> textbook page labels from extraction: PDF page 3 starts p.1, but extracted page numbers are PDF pages.
needed = list(range(1, 27))
lines=[]
for page_no in needed:
    page = doc[page_no-1]
    text = page.get_text()
    lines.append(f"\n\n===== PDF PAGE {page_no} =====\n{text}")
(out_dir/'Logical Speaking_textbook_pages_1-26.txt').write_text(''.join(lines), encoding='utf-8')
print(out_dir/'Logical Speaking_textbook_pages_1-26.txt')
