from pathlib import Path
import xml.etree.ElementTree as ET
import sys, collections, re
p=Path(sys.argv[1])
ns={
 'p':'http://schemas.openxmlformats.org/presentationml/2006/main',
 'a':'http://schemas.openxmlformats.org/drawingml/2006/main',
 'r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
}
root=ET.parse(p).getroot()
shapes={}
for sp in root.findall('.//p:sp', ns):
    cNvPr=sp.find('./p:nvSpPr/p:cNvPr', ns)
    if cNvPr is None: continue
    sid=cNvPr.attrib.get('id')
    name=cNvPr.attrib.get('name')
    geom=sp.find('./p:spPr/a:prstGeom', ns)
    prst=geom.attrib.get('prst') if geom is not None else ''
    texts=[]
    for t in sp.findall('.//a:t', ns):
        if t.text: texts.append(t.text)
    shapes[sid]={'name':name,'prst':prst,'text':' '.join(texts)[:80]}
print('SHAPES')
for sid in sorted(shapes, key=lambda x:int(x)):
    s=shapes[sid]
    print(f"{sid:>3} | {s['name']:<22} | {s['prst']:<10} | {s['text']}")
print('\nANIMATION TARGET SUMMARY')
counts=collections.Counter()
for spTgt in root.findall('.//p:spTgt', ns):
    sid=spTgt.attrib.get('spid')
    counts[sid]+=1
for sid,n in counts.most_common():
    s=shapes.get(sid,{})
    print(f"{sid:>3} x{n:<3} | {s.get('name','?'):<22} | {s.get('prst',''):<10} | {s.get('text','')}")
print('\nANIMATION EFFECTS')
for i,eff in enumerate(root.findall('.//p:animEffect', ns),1):
    cBhvr=eff.find('./p:cBhvr', ns)
    sid=''
    if cBhvr is not None:
        spTgt=cBhvr.find('.//p:spTgt', ns)
        if spTgt is not None: sid=spTgt.attrib.get('spid','')
    s=shapes.get(sid,{})
    print(f"{i:>2} sid={sid:>3} presetClass={eff.attrib.get('presetClass','')} presetID={eff.attrib.get('presetID','')} filter={eff.attrib.get('filter','')} transition={eff.attrib.get('transition','')} text={s.get('text','')}")
print('\nSET TARGETS')
for i,setel in enumerate(root.findall('.//p:set', ns),1):
    cBhvr=setel.find('./p:cBhvr', ns)
    sid=''
    attr=''
    if cBhvr is not None:
        spTgt=cBhvr.find('.//p:spTgt', ns)
        if spTgt is not None: sid=spTgt.attrib.get('spid','')
        attrName=cBhvr.find('.//p:attrName', ns)
        if attrName is not None and attrName.text: attr=attrName.text
    s=shapes.get(sid,{})
    if i <= 120:
        print(f"{i:>2} sid={sid:>3} attr={attr:<18} text={s.get('text','')}")
