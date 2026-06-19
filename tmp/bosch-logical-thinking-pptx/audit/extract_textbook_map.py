import fitz, re, pathlib, json, sys
pdf = pathlib.Path(sys.argv[1])
out = pathlib.Path(sys.argv[2])
doc = fitz.open(pdf)
patterns = [
    re.compile(r'\bUnit\s+([1-9])\b', re.I),
    re.compile(r'\bORE\b|\bPBSR\b|\bPCAF\b'),
    re.compile(r'Opinion|Reason|Example|Evidence|bias|fake news|discourse marker|argument', re.I),
]
rows=[]
for i,page in enumerate(doc,1):
    text=page.get_text()
    hits=[]
    for pat in patterns:
        for m in pat.finditer(text):
            hit=m.group(0)
            if hit not in hits: hits.append(hit)
    if hits:
        lines=[ln.strip() for ln in text.splitlines() if ln.strip()]
        rows.append({'page':i,'hits':hits[:20],'first_lines':lines[:25]})
(out/'textbook_page_hits.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding='utf-8')
for r in rows:
    print('PAGE',r['page'],'HITS',', '.join(r['hits'][:10]))
    for ln in r['first_lines'][:10]: print('  ',ln)
    print()
