from pathlib import Path
import xml.etree.ElementTree as ET
import re, sys
ns={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
slides=sorted(Path(sys.argv[1]).glob('slide*.xml'), key=lambda p:int(re.search(r'slide(\d+)\.xml',p.name).group(1)))
for p in slides:
    root=ET.parse(p).getroot()
    texts=[]
    for sp in root.findall('.//p:sp', ns):
        cNvPr=sp.find('./p:nvSpPr/p:cNvPr', ns)
        name=cNvPr.attrib.get('name','') if cNvPr is not None else ''
        txt=' '.join(t.text for t in sp.findall('.//a:t', ns) if t.text)
        if txt.strip(): texts.append((name,txt.strip()))
    # choose likely title: Text 2 often baseSlide title; fallback longest early text
    title=''
    for name,txt in texts[:8]:
        if name.startswith('Text 2') or (len(txt)>8 and txt.upper()!=txt):
            title=txt; break
    if not title and texts: title=texts[0][1]
    print(f"{re.search(r'slide(\d+)\.xml',p.name).group(1):>2}. {title[:120]}")
