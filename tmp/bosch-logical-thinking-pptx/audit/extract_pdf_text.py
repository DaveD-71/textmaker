import fitz, sys, pathlib
out_dir = pathlib.Path(sys.argv[1])
for f in sys.argv[2:]:
    p = pathlib.Path(f)
    doc = fitz.open(p)
    chunks = []
    for i, page in enumerate(doc, 1):
        chunks.append(f"\n\n===== PAGE {i} =====\n")
        chunks.append(page.get_text())
    out_path = out_dir / (p.stem + '.txt')
    out_path.write_text(''.join(chunks), encoding='utf-8')
    print(out_path)
