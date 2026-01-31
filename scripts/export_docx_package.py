# export_docx_package.py
# v3.3 — .docx → JSON/CSV package exporter
# - Full style inheritance (provenance) + theme-aware color resolution
# - Paragraph & run formatting (bold/italic/underline, borders, shading, alignment)
# - Tables: grid, row heights, cell props (borders, shading, vMerge/gridSpan), positioning
# - Text inside table cells fully captured with unique para_ids and container back-links
# - Global para_id for every paragraph (body/header/footer/table cells)
# - Assets: images + textboxes (anchors, positions, sizes, textbox content)
# - Sections, numbering, theme, settings
# - Fields: PAGE/NUMPAGES/DATE/... (simple + complex) with locations
# - CSVs: styles_summary, sections, paragraphs (incl. table cell paragraphs), tables, table_cells (with first_para_id), assets, fields

# - This older module has largely been replaced but is kept for reference and backward compatibility.

import argparse, csv, json, os, zipfile
from pathlib import Path
from collections import OrderedDict
from lxml import etree
from docx import Document

WNS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
    "v": "urn:schemas-microsoft-com:vml",
    "o": "urn:schemas-microsoft-com:office:office",
    "wpg": "http://schemas.microsoft.com/office/word/2010/wordprocessingGroup",
    "wps": "http://schemas.microsoft.com/office/word/2010/wordprocessingShape",
    "w14": "http://schemas.microsoft.com/office/word/2010/wordml",
}


# ---------------- Utilities / Units ----------------
def twips_to_pt(v):
    return round(int(v) / 20.0, 2) if v and str(v).isdigit() else None


def twips_to_cm(v):
    return round(int(v) / 567.0, 3) if v and str(v).isdigit() else None


def emu_to_cm(v):
    return round(int(v) / 360000.0, 3) if v and str(v).isdigit() else None


def safe_snip(s, n=160):
    if not s:
        return ""
    return " ".join(s.replace("\r", " ").replace("\n", " ").split())[:n]


def read_part(zf, path):
    try:
        with zf.open(path) as f:
            return etree.parse(f)
    except KeyError:
        return None


def list_rels(zf, part_path):
    p = Path(part_path)
    rels_path = str(p.parent / "_rels" / (p.name + ".rels"))
    x = read_part(zf, rels_path)
    out = {}
    if x is not None:
        for r in x.getroot().findall("r:Relationship", namespaces=WNS):
            out[r.get("Id")] = {"target": r.get("Target"), "type": r.get("Type")}
    return out


def get_local(tag):
    return tag.split("}", 1)[-1] if "}" in tag else tag


def present(node, q):
    return node.find(q, namespaces=WNS) is not None


# ---------------- Global paragraph ID generator ----------------
class ParaIdGen:
    def __init__(self):
        self.n = 0

    def next(self):
        self.n += 1
        return f"p{self.n:06d}"


PARA_IDS = ParaIdGen()


# ---------------- Theme ----------------
def parse_theme(zf):
    x = read_part(zf, "word/theme/theme1.xml")
    out = {
        "colors": {},
        "fonts": {
            "majorLatin": None,
            "minorLatin": None,
            "majorEastAsia": None,
            "minorEastAsia": None,
            "majorCs": None,
            "minorCs": None,
        },
    }
    if x is None:
        return out
    root = x.getroot()
    scheme = root.find(".//a:clrScheme", namespaces=WNS)
    if scheme is not None:
        idx = 0
        for clr in scheme:
            local = get_local(clr.tag)
            key = clr.get("name") or local or f"color_{idx}"
            idx += 1
            hexv = None
            srgb = clr.find(".//a:srgbClr", namespaces=WNS)
            if srgb is not None:
                v = srgb.get("val") or srgb.get("lastClr")
                if v:
                    hexv = "#" + v.lstrip("#")
            if hexv:
                out["colors"][key] = hexv
            else:
                sc = clr.find(".//a:schemeClr", namespaces=WNS)
                out["colors"][key] = (
                    "theme:" + sc.get("val")
                    if sc is not None and sc.get("val")
                    else None
                )
    fnts = root.find(".//a:fontScheme", namespaces=WNS)
    if fnts is not None:
        major = fnts.find(".//a:majorFont", namespaces=WNS)
        minor = fnts.find(".//a:minorFont", namespaces=WNS)

        def pick(node, tag):
            if node is None:
                return None
            n = node.find(f"a:{tag}", namespaces=WNS)
            return n.get("typeface") if n is not None else None

        out["fonts"]["majorLatin"] = pick(major, "latin")
        out["fonts"]["minorLatin"] = pick(minor, "latin")
        out["fonts"]["majorEastAsia"] = pick(major, "ea")
        out["fonts"]["minorEastAsia"] = pick(minor, "ea")
        out["fonts"]["majorCs"] = pick(major, "cs")
        out["fonts"]["minorCs"] = pick(minor, "cs")
    return out


def resolve_theme_color(theme_map, key):
    if not key:
        return None
    m = theme_map.get("colors", {}) or {}
    return m.get(key) or m.get("theme:" + str(key)) or None


# ---------------- Borders & shading ----------------
def extract_borders(container_node, tag):
    out = {}
    if container_node is None:
        return out
    b = container_node.find(f"w:{tag}", namespaces=WNS)
    if b is None:
        return out
    for side in ["top", "bottom", "left", "right", "between", "insideH", "insideV"]:
        el = b.find(f"w:{side}", namespaces=WNS)
        if el is not None:
            val = el.get(f"{{{WNS['w']}}}val")
            sz = el.get(f"{{{WNS['w']}}}sz")
            sp = el.get(f"{{{WNS['w']}}}space")
            col = el.get(f"{{{WNS['w']}}}color")
            tcl = el.get(f"{{{WNS['w']}}}themeColor")
            out[side] = {
                "val": val,
                "sz_pt": (float(sz) / 8.0) if sz else None,
                "space_pt": float(sp) if sp else None,
                "color": (
                    ("#" + col)
                    if col and col != "auto"
                    else ("auto" if col == "auto" else None)
                ),
                "themeColor": tcl,
            }
    return out


def extract_shading(node):
    if node is None:
        return {}
    sh = node.find("w:shd", namespaces=WNS)
    if sh is None:
        return {}
    out = {}
    for k in ["val", "fill", "color", "themeFill", "themeFillTint", "themeFillShade"]:
        v = sh.get(f"{{{WNS['w']}}}{k}")
        if v:
            out[k] = (
                ("#" + v)
                if k in ("fill", "color") and v != "auto"
                else (v if v != "auto" else "auto")
            )
    return out


# ---------------- rPr / pPr extractors ----------------
def extract_rPr(rPr):
    out = {}
    if rPr is None:
        return out
    rFonts = rPr.find("w:rFonts", namespaces=WNS)
    if rFonts is not None:
        for k in ["ascii", "hAnsi", "eastAsia", "cs"]:
            v = rFonts.get(f"{{{WNS['w']}}}{k}")
            if v:
                out[f"name_{k}"] = v
        for k in ["asciiTheme", "hAnsiTheme", "eastAsiaTheme", "csTheme", "cstheme"]:
            v = rFonts.get(f"{{{WNS['w']}}}{k}")
            if v:
                out[k] = v
    sz = rPr.find("w:sz", namespaces=WNS)
    if sz is not None and sz.get(f"{{{WNS['w']}}}val"):
        out["size_pt"] = float(sz.get(f"{{{WNS['w']}}}val")) / 2.0
    color = rPr.find("w:color", namespaces=WNS)
    if color is not None:
        v = color.get(f"{{{WNS['w']}}}val")
        if v and v != "auto":
            out["color_hex"] = "#" + v
        t = color.get(f"{{{WNS['w']}}}themeColor")
        if t:
            out["theme_color"] = t
    for flag in ["b", "i", "u", "caps", "smallCaps", "strike"]:
        if rPr.find(f"w:{flag}", namespaces=WNS) is not None:
            out[flag] = True
    bd = extract_borders(rPr, "bdr")
    if bd:
        out["borders"] = bd
    return out


def extract_pPr(pPr):
    out = {}
    if pPr is None:
        return out
    jc = pPr.find("w:jc", namespaces=WNS)
    if jc is not None and jc.get(f"{{{WNS['w']}}}val"):
        out["alignment"] = jc.get(f"{{{WNS['w']}}}val")
    ind = pPr.find("w:ind", namespaces=WNS)
    if ind is not None:
        for k in ["left", "right", "firstLine", "hanging"]:
            v = ind.get(f"{{{WNS['w']}}}{k}")
            if v:
                out[f"{k}_cm"] = twips_to_cm(v)
    sp = pPr.find("w:spacing", namespaces=WNS)
    if sp is not None:
        b = sp.get(f"{{{WNS['w']}}}before")
        a = sp.get(f"{{{WNS['w']}}}after")
        l = sp.get(f"{{{WNS['w']}}}line")
        if b:
            out["space_before_pt"] = twips_to_pt(b)
        if a:
            out["space_after_pt"] = twips_to_pt(a)
        if l:
            out["line_spacing_twips"] = int(l)
    ol = pPr.find("w:outlineLvl", namespaces=WNS)
    if ol is not None and ol.get(f"{{{WNS['w']}}}val"):
        out["outline_level"] = int(ol.get(f"{{{WNS['w']}}}val"))
    num = pPr.find("w:numPr", namespaces=WNS)
    if num is not None:
        il = num.find("w:ilvl", namespaces=WNS)
        ni = num.find("w:numId", namespaces=WNS)
        if il is not None and il.get(f"{{{WNS['w']}}}val"):
            out["ilvl"] = int(il.get(f"{{{WNS['w']}}}val"))
        if ni is not None and ni.get(f"{{{WNS['w']}}}val"):
            out["numId"] = int(ni.get(f"{{{WNS['w']}}}val"))
    bd = extract_borders(pPr, "pBdr")
    if bd:
        out["borders"] = bd
    sh = extract_shading(pPr)
    if sh:
        out["shading"] = sh
    return out


# ---------------- Styles (inheritance + provenance) ----------------
def parse_styles(zf):
    sx = read_part(zf, "word/styles.xml")
    out = {
        "paragraphStyles": [],
        "characterStyles": [],
        "tableStyles": [],
        "listStyles": [],
    }
    if sx is None:
        return out, {}, {"rPr": {}, "pPr": {}}
    # docDefaults
    docdef = {"rPr": {}, "pPr": {}}
    rdef = sx.find(".//w:docDefaults/w:rPrDefault/w:rPr", namespaces=WNS)
    pdef = sx.find(".//w:docDefaults/w:pPrDefault/w:pPr", namespaces=WNS)
    if rdef is not None:
        docdef["rPr"] = extract_rPr(rdef)
    if pdef is not None:
        docdef["pPr"] = extract_pPr(pdef)
    # index
    styles_by_id = {}
    for s in sx.getroot().findall("w:style", namespaces=WNS):
        stype = s.get(f"{{{WNS['w']}}}type")
        sid = s.get(f"{{{WNS['w']}}}styleId")
        name = s.find("w:name", namespaces=WNS)
        based = s.find("w:basedOn", namespaces=WNS)
        link = s.find("w:link", namespaces=WNS)
        nxt = s.find("w:next", namespaces=WNS)
        ui = s.find("w:uiPriority", namespaces=WNS)
        flags = {
            f: (s.find(f"w:{f}", namespaces=WNS) is not None)
            for f in ["hidden", "semiHidden", "unhideWhenUsed", "locked"]
        }
        rPr = s.find("w:rPr", namespaces=WNS)
        pPr = s.find("w:pPr", namespaces=WNS)
        styles_by_id[sid] = {
            "styleId": sid,
            "name": name.get(f"{{{WNS['w']}}}val") if name is not None else None,
            "type": stype,
            "basedOn": based.get(f"{{{WNS['w']}}}val") if based is not None else None,
            "linked": link.get(f"{{{WNS['w']}}}val") if link is not None else None,
            "next": nxt.get(f"{{{WNS['w']}}}val") if nxt is not None else None,
            "uiPriority": int(ui.get(f"{{{WNS['w']}}}val")) if ui is not None else None,
            "flags": flags,
            "explicit": {"rPr": extract_rPr(rPr), "pPr": extract_pPr(pPr)},
        }
    # buckets
    for sid, s in styles_by_id.items():
        pay = {
            k: s[k]
            for k in [
                "styleId",
                "name",
                "type",
                "basedOn",
                "linked",
                "next",
                "uiPriority",
                "flags",
                "explicit",
            ]
        }
        if s["type"] == "paragraph":
            out["paragraphStyles"].append(pay)
        elif s["type"] == "character":
            out["characterStyles"].append(pay)
        elif s["type"] == "table":
            out["tableStyles"].append(pay)
        elif s["type"] == "numbering":
            out["listStyles"].append(pay)
    return out, styles_by_id, docdef


def resolve_style_with_provenance(
    style_id, styles_by_id, doc_defaults, theme_map, memo
):
    if style_id in memo:
        return memo[style_id]
    s = styles_by_id.get(style_id)
    if not s:
        memo[style_id] = {"rPr": {}, "pPr": {}}
        return memo[style_id]
    res = {"rPr": {}, "pPr": {}}
    # explicit
    for k, v in s["explicit"]["rPr"].items():
        res["rPr"][k] = {"value": v, "source": "explicit"}
    for k, v in s["explicit"]["pPr"].items():
        res["pPr"][k] = {"value": v, "source": "explicit"}
    # inherit chain
    parent = s.get("basedOn")
    seen = set([style_id])
    while parent and parent not in seen:
        seen.add(parent)
        p = styles_by_id.get(parent)
        if not p:
            break
        for k, v in p["explicit"]["rPr"].items():
            if k not in res["rPr"]:
                res["rPr"][k] = {
                    "value": v,
                    "source": "inherited",
                    "from": (p.get("name") or p.get("styleId")),
                }
        for k, v in p["explicit"]["pPr"].items():
            if k not in res["pPr"]:
                res["pPr"][k] = {
                    "value": v,
                    "source": "inherited",
                    "from": (p.get("name") or p.get("styleId")),
                }
        parent = p.get("basedOn")
    # doc defaults
    for k, v in doc_defaults.get("rPr", {}).items():
        if k not in res["rPr"]:
            res["rPr"][k] = {"value": v, "source": "default"}
    for k, v in doc_defaults.get("pPr", {}).items():
        if k not in res["pPr"]:
            res["pPr"][k] = {"value": v, "source": "default"}
    # defaults
    for flag in ["b", "i", "u", "caps", "smallCaps", "strike"]:
        if flag not in res["rPr"]:
            res["rPr"][flag] = {"value": False, "source": "default"}
    if "alignment" not in res["pPr"]:
        res["pPr"]["alignment"] = {"value": "left", "source": "default"}
    # theme color resolve
    tc = res["rPr"].get("theme_color", {})
    themekey = tc.get("value") if isinstance(tc, dict) else None
    hexv = resolve_theme_color(
        parse_theme.colors if isinstance(parse_theme, dict) else {}, themekey
    )  # keep API safe
    # safer direct theme map use:
    hexv = resolve_theme_color(theme_map, themekey)
    if hexv:
        res["rPr"]["color_hex_resolved"] = {
            "value": hexv,
            "source": res["rPr"].get("theme_color", {}).get("source", "explicit"),
        }
    memo[style_id] = res
    return res


# ---------------- Numbering / Settings / Sections ----------------
def parse_numbering(zf):
    x = read_part(zf, "word/numbering.xml")
    out = {"abstractNums": [], "nums": []}
    if x is None:
        return out
    root = x.getroot()
    for ab in root.findall("w:abstractNum", namespaces=WNS):
        aid = int(ab.get(f"{{{WNS['w']}}}abstractNumId"))
        lvls = []
        for lvl in ab.findall("w:lvl", namespaces=WNS):
            ilvl = int(lvl.get(f"{{{WNS['w']}}}ilvl"))
            nf = lvl.find("w:numFmt", namespaces=WNS)
            nt = lvl.find("w:lvlText", namespaces=WNS)
            pPr = lvl.find("w:pPr", namespaces=WNS)
            lvls.append(
                {
                    "ilvl": ilvl,
                    "numFmt": nf.get(f"{{{WNS['w']}}}val") if nf is not None else None,
                    "lvlText": nt.get(f"{{{WNS['w']}}}val") if nt is not None else None,
                    "pPr": extract_pPr(pPr) if pPr is not None else {},
                }
            )
        out["abstractNums"].append({"abstractNumId": aid, "levels": lvls})
    for n in root.findall("w:num", namespaces=WNS):
        nid = int(n.get(f"{{{WNS['w']}}}numId"))
        a = n.find("w:abstractNumId", namespaces=WNS)
        out["nums"].append(
            {
                "numId": nid,
                "abstractNumId": (
                    int(a.get(f"{{{WNS['w']}}}val")) if a is not None else None
                ),
            }
        )
    return out


def parse_settings(zf):
    x = read_part(zf, "word/settings.xml")
    out = {}
    if x is None:
        return out
    root = x.getroot()

    def has(tag):
        return root.find(f"w:{tag}", namespaces=WNS) is not None

    def val(tag, attr="w:val"):
        n = root.find(f"w:{tag}", namespaces=WNS)
        return n.get(attr) if n is not None and n.get(attr) is not None else None

    out["evenAndOddHeaders"] = has("evenAndOddHeaders")
    out["updateFields"] = has("updateFields")
    out["mirrorMargins"] = has("mirrorMargins")
    out["trackRevisions"] = has("trackRevisions")
    out["defaultTabStopTwips"] = (
        int(val("defaultTabStop")) if val("defaultTabStop") else None
    )
    return out


def parse_sections_with_docx(docx_path):
    d = Document(docx_path)
    sections = []
    for i, sec in enumerate(d.sections, start=1):
        sections.append(
            {
                "index": i,
                "orientation": (
                    "LANDSCAPE"
                    if getattr(sec, "orientation", None) == 1
                    else "PORTRAIT"
                ),
                "page_width_cm": round(float(sec.page_width.cm), 3),
                "page_height_cm": round(float(sec.page_height.cm), 3),
                "margins_cm": {
                    "top": round(float(sec.top_margin.cm), 3),
                    "bottom": round(float(sec.bottom_margin.cm), 3),
                    "left": round(float(sec.left_margin.cm), 3),
                    "right": round(float(sec.right_margin.cm), 3),
                },
                "header_distance_cm": (
                    round(float(sec.header_distance.cm), 3)
                    if hasattr(sec, "header_distance")
                    else None
                ),
                "footer_distance_cm": (
                    round(float(sec.footer_distance.cm), 3)
                    if hasattr(sec, "footer_distance")
                    else None
                ),
                "different_first_page": getattr(
                    sec, "different_first_page_header_footer", None
                ),
                "even_and_odd": getattr(sec, "odd_and_even_pages_header_footer", None),
            }
        )
    return d, sections


def parse_section_pgnum_and_margins_ooxml(zf):
    doc = read_part(zf, "word/document.xml")
    out = []
    if doc is None:
        return out
    for idx, sp in enumerate(
        doc.getroot().findall(".//w:sectPr", namespaces=WNS), start=1
    ):
        rec = {"section_index": idx}
        pgnum = sp.find("w:pgNumType", namespaces=WNS)
        if pgnum is not None:
            fmt = pgnum.get(f"{{{WNS['w']}}}fmt")
            start = pgnum.get(f"{{{WNS['w']}}}start")
            rec["page_numbering"] = {
                "format": fmt,
                "start": int(start) if start and start.isdigit() else None,
            }
        pgmar = sp.find("w:pgMar", namespaces=WNS)
        if pgmar is not None:
            hd = pgmar.get(f"{{{WNS['w']}}}header")
            fd = pgmar.get(f"{{{WNS['w']}}}footer")
            if hd or fd:
                rec["header_footer_distance_cm"] = {
                    "header": twips_to_cm(hd) if hd else None,
                    "footer": twips_to_cm(fd) if fd else None,
                }
        out.append(rec)
    return out


# ---------------- Assets (images + textboxes) ----------------
def asset_image_from_drawing(
    d_node, rels, context, section_index=None, paragraph_index=None, run_index=None
):
    blip = d_node.find(".//a:blip", namespaces=WNS)
    if blip is None:
        return None
    rid = blip.get(f"{{{WNS['r']}}}embed") or blip.get(f"{{{WNS['r']}}}link")
    if rid is None:
        return None
    target = rels.get(rid, {}).get("target")
    if not target:
        return None
    if not str(target).startswith("/"):
        target = str(Path("word") / target)
    asset = {
        "id": None,
        "type": "image",
        "relId": rid,
        "file": target,
        "context": context,
        "section_index": section_index,
        "paragraph_index": paragraph_index,
        "run_index": run_index,
    }
    inline = d_node.find(".//wp:inline", namespaces=WNS)
    anchor = d_node.find(".//wp:anchor", namespaces=WNS)
    if inline is not None:
        asset["anchor_type"] = "inline"
        ext = inline.find("wp:extent", namespaces=WNS)
        if ext is not None:
            asset["width_cm"] = emu_to_cm(ext.get("cx"))
            asset["height_cm"] = emu_to_cm(ext.get("cy"))
        asset["wrap_style"] = "none"
    elif anchor is not None:
        asset["anchor_type"] = "floating"
        ext = anchor.find("wp:extent", namespaces=WNS)
        if ext is not None:
            asset["width_cm"] = emu_to_cm(ext.get("cx"))
            asset["height_cm"] = emu_to_cm(ext.get("cy"))
        pos = {}
        x = anchor.find("wp:positionH/wp:posOffset", namespaces=WNS)
        y = anchor.find("wp:positionV/wp:posOffset", namespaces=WNS)
        if x is not None:
            pos["x"] = emu_to_cm(x.text)
        if y is not None:
            pos["y"] = emu_to_cm(y.text)
        asset["position_cm"] = pos or None
        wrap = None
        for tag in [
            "wrapSquare",
            "wrapTight",
            "wrapThrough",
            "wrapTopAndBottom",
            "wrapNone",
        ]:
            if anchor.find(f"wp:{tag}", namespaces=WNS) is not None:
                wrap = tag.replace("wrap", "").lower()
                break
        asset["wrap_style"] = wrap or "none"
    else:
        asset["anchor_type"] = "unknown"
    return asset


def collect_txbx_paragraphs(txbx_content, context, table_ctx=None):
    """Return list of paragraph dicts with full text and runs inside a textbox content node."""
    paras = []
    p_index = -1
    for p in txbx_content.findall(".//w:p", namespaces=WNS):
        p_index += 1
        pPr = p.find("w:pPr", namespaces=WNS)
        df_p = extract_pPr(pPr) if pPr is not None else {}
        runs_out = []
        texts = []
        r_index = -1
        for r in p.findall("w:r", namespaces=WNS):
            r_index += 1
            t = r.find("w:t", namespaces=WNS)
            tval = t.text if t is not None and t.text else ""
            texts.append(tval)
            rPr = r.find("w:rPr", namespaces=WNS)
            runs_out.append(
                {
                    "run_index": r_index,
                    "text": tval,
                    "direct_rPr": extract_rPr(rPr) if rPr is not None else {},
                }
            )
        pstyle = None
        if pPr is not None:
            ps = pPr.find("w:pStyle", namespaces=WNS)
            if ps is not None and ps.get(f"{{{WNS['w']}}}val"):
                pstyle = ps.get(f"{{{WNS['w']}}}val")
        para_id = PARA_IDS.next()
        container = {"kind": context}
        if table_ctx:
            container = {"kind": "table", **table_ctx}
        paras.append(
            {
                "para_id": para_id,
                "paragraph_index": p_index,
                "styleId": pstyle,
                "direct_pPr": df_p or None,
                "text": "".join(texts),
                "runs": runs_out or None,
                "snippet": safe_snip("".join(texts)),
                "numId": df_p.get("numId"),
                "ilvl": df_p.get("ilvl"),
                "container": container,
            }
        )
    return paras


def asset_textbox_from_drawing(
    d_node, context, section_index=None, paragraph_index=None, run_index=None
):
    """DrawingML & legacy VML textboxes."""
    # DrawingML
    txbx = d_node.find(".//wps:wsp/wps:txbx/w:txbxContent", namespaces=WNS)
    if txbx is not None:
        asset = {
            "id": None,
            "type": "textbox",
            "context": context,
            "section_index": section_index,
            "paragraph_index": paragraph_index,
            "run_index": run_index,
        }
        inline = d_node.find(".//wp:inline", namespaces=WNS)
        anchor = d_node.find(".//wp:anchor", namespaces=WNS)
        if inline is not None:
            asset["anchor_type"] = "inline"
            ext = inline.find("wp:extent", namespaces=WNS)
            if ext is not None:
                asset["width_cm"] = emu_to_cm(ext.get("cx"))
                asset["height_cm"] = emu_to_cm(ext.get("cy"))
            asset["wrap_style"] = "none"
        elif anchor is not None:
            asset["anchor_type"] = "floating"
            ext = anchor.find("wp:extent", namespaces=WNS)
            if ext is not None:
                asset["width_cm"] = emu_to_cm(ext.get("cx"))
                asset["height_cm"] = emu_to_cm(ext.get("cy"))
            pos = {}
            x = anchor.find("wp:positionH/wp:posOffset", namespaces=WNS)
            y = anchor.find("wp:positionV/wp:posOffset", namespaces=WNS)
            if x is not None:
                pos["x"] = emu_to_cm(x.text)
            if y is not None:
                pos["y"] = emu_to_cm(y.text)
            asset["position_cm"] = pos or None
            wrap = None
            for tag in [
                "wrapSquare",
                "wrapTight",
                "wrapThrough",
                "wrapTopAndBottom",
                "wrapNone",
            ]:
                if anchor.find(f"wp:{tag}", namespaces=WNS) is not None:
                    wrap = tag.replace("wrap", "").lower()
                    break
            asset["wrap_style"] = wrap or "none"
        else:
            asset["anchor_type"] = "unknown"
        asset["content"] = collect_txbx_paragraphs(txbx, context)
        return asset
    # Legacy VML
    vtx = d_node.find(".//v:shape/v:textbox/w:txbxContent", namespaces=WNS)
    if vtx is not None:
        asset = {
            "id": None,
            "type": "textbox",
            "context": context,
            "section_index": section_index,
            "paragraph_index": paragraph_index,
            "run_index": run_index,
            "anchor_type": "unknown",
        }
        asset["content"] = collect_txbx_paragraphs(vtx, context)
        return asset
    return None


# ---------------- Fields (simple + complex) ----------------
def extract_fields_from_paragraph(
    p_node, context, section_index=None, paragraph_index=None
):
    fields = []
    # Simple fields
    for fld in p_node.findall(".//w:fldSimple", namespaces=WNS):
        instr = fld.get(f"{{{WNS['w']}}}instr")
        texts = [
            t.text
            for t in fld.findall(".//w:t", namespaces=WNS)
            if t is not None and t.text
        ]
        fields.append(
            {
                "context": context,
                "section_index": section_index,
                "paragraph_index": paragraph_index,
                "run_index": None,
                "scope": "simple",
                "instruction": instr,
                "display_text": "".join(texts) if texts else None,
                "type": (instr.split()[0] if instr else None),
            }
        )
    # Complex fields: scan run sequence to collect begin..end blocks
    in_field = False
    instr_buf = []
    for child in p_node.iterchildren():
        # fldChar
        if child.tag == f"{{{WNS['w']}}}r":
            # inside run, check for fldChar or instrText
            fcb = child.find("w:fldChar[@w:fldCharType='begin']", namespaces=WNS)
            fce = child.find("w:fldChar[@w:fldCharType='end']", namespaces=WNS)
            inst = child.find("w:instrText", namespaces=WNS)
            if fcb is not None:
                in_field = True
                instr_buf = []
            if inst is not None and in_field:
                instr_buf.append(inst.text or "")
            if fce is not None and in_field:
                instruction = " ".join([s for s in instr_buf if s]).strip()
                fields.append(
                    {
                        "context": context,
                        "section_index": section_index,
                        "paragraph_index": paragraph_index,
                        "run_index": None,
                        "scope": "complex",
                        "instruction": instruction,
                        "display_text": None,
                        "type": (instruction.split()[0] if instruction else None),
                    }
                )
                in_field = False
                instr_buf = []
    return fields


# ---------------- Tables (rich + full cell paragraphs) ----------------
def extract_table(tbl, rels, context, table_index, paragraph_anchor_index, fields_out):
    tPr = tbl.find("w:tblPr", namespaces=WNS)
    tblStyle = None
    align = None
    tblW = None
    borders = None
    look = {}
    shading = {}
    position = {}
    if tPr is not None:
        ts = tPr.find("w:tblStyle", namespaces=WNS)
        if ts is not None and ts.get(f"{{{WNS['w']}}}val"):
            tblStyle = ts.get(f"{{{WNS['w']}}}val")
        jc = tPr.find("w:jc", namespaces=WNS)
        if jc is not None and jc.get(f"{{{WNS['w']}}}val"):
            align = jc.get(f"{{{WNS['w']}}}val")
        tw = tPr.find("w:tblW", namespaces=WNS)
        if tw is not None and tw.get(f"{{{WNS['w']}}}w"):
            raw = tw.get(f"{{{WNS['w']}}}w")
            tblW = (
                {"twips": int(raw), "cm": twips_to_cm(raw)}
                if raw.isdigit()
                else {"raw": raw}
            )
        bdrs = extract_borders(tPr, "tblBorders")
        borders = bdrs or None
        tl = tPr.find("w:tblLook", namespaces=WNS)
        if tl is not None:
            for k in [
                "firstRow",
                "lastRow",
                "firstColumn",
                "lastColumn",
                "noHBand",
                "noVBand",
                "band1Horz",
                "band2Horz",
                "band1Vert",
                "band2Vert",
            ]:
                v = tl.get(f"{{{WNS['w']}}}{k}")
                if v:
                    look[k] = v == "1"
        shading = extract_shading(tPr) or None
    ppr = tbl.find("w:tblpPr", namespaces=WNS)
    if ppr is not None:
        x = ppr.get(f"{{{WNS['w']}}}tblpX")
        y = ppr.get(f"{{{WNS['w']}}}tblpY")
        if x:
            position["x_cm"] = twips_to_cm(x)
        if y:
            position["y_cm"] = twips_to_cm(y)
        xa = ppr.get(f"{{{WNS['w']}}}tblpXSpec")
        ya = ppr.get(f"{{{WNS['w']}}}tblpYSpec")
        if xa:
            position["x_align"] = xa
        if ya:
            position["y_align"] = ya
    grid = []
    gn = tbl.find("w:tblGrid", namespaces=WNS)
    if gn is not None:
        for gc in gn.findall("w:gridCol", namespaces=WNS):
            wv = gc.get(f"{{{WNS['w']}}}w")
            grid.append(twips_to_cm(wv) if wv and wv.isdigit() else None)
    rows_out = []
    rix = -1
    for tr in tbl.findall("w:tr", namespaces=WNS):
        rix += 1
        trPr = tr.find("w:trPr", namespaces=WNS)
        height = None
        header = False
        cant = False
        if trPr is not None:
            h = trPr.find("w:trHeight", namespaces=WNS)
            if h is not None and h.get(f"{{{WNS['w']}}}val"):
                height = twips_to_cm(h.get(f"{{{WNS['w']}}}val"))
            header = present(trPr, "w:tblHeader")
            cant = present(trPr, "w:cantSplit")
        cells_out = []
        cix = -1
        for tc in tr.findall("w:tc", namespaces=WNS):
            cix += 1
            tcPr = tc.find("w:tcPr", namespaces=WNS)
            wcm = None
            vAlign = None
            gridSpan = None
            vMerge = None
            cb = None
            cshade = None
            if tcPr is not None:
                w = tcPr.find("w:tcW", namespaces=WNS)
                if w is not None and w.get(f"{{{WNS['w']}}}w"):
                    raw = w.get(f"{{{WNS['w']}}}w")
                    wcm = twips_to_cm(raw) if raw.isdigit() else None
                va = tcPr.find("w:vAlign", namespaces=WNS)
                if va is not None and va.get(f"{{{WNS['w']}}}val"):
                    vAlign = va.get(f"{{{WNS['w']}}}val")
                gs = tcPr.find("w:gridSpan", namespaces=WNS)
                if gs is not None and gs.get(f"{{{WNS['w']}}}val"):
                    gridSpan = int(gs.get(f"{{{WNS['w']}}}val"))
                vm = tcPr.find("w:vMerge", namespaces=WNS)
                if vm is not None:
                    vMerge = vm.get(f"{{{WNS['w']}}}val") or "continue"
                cb = extract_borders(tcPr, "tcBorders")
                cshade = extract_shading(tcPr)
            # collect paragraphs inside the cell (full)
            cell_paragraphs = []
            texts = []
            pin_cell = -1
            for p in tc.findall("w:p", namespaces=WNS):
                pin_cell += 1
                # fields in cell paragraph
                fields_out.extend(extract_fields_from_paragraph(p, context, None, None))
                pPr = p.find("w:pPr", namespaces=WNS)
                df_p = extract_pPr(pPr) if pPr is not None else {}
                runs_out = []
                r_index = -1
                rtext = []
                for r in p.findall("w:r", namespaces=WNS):
                    r_index += 1
                    t = r.find("w:t", namespaces=WNS)
                    rval = t.text if t is not None and t.text else ""
                    rtext.append(rval)
                    rPr = r.find("w:rPr", namespaces=WNS)
                    runs_out.append(
                        {
                            "run_index": r_index,
                            "text": rval,
                            "direct_rPr": extract_rPr(rPr) if rPr is not None else {},
                        }
                    )
                pstyle = None
                if pPr is not None:
                    ps = pPr.find("w:pStyle", namespaces=WNS)
                    if ps is not None and ps.get(f"{{{WNS['w']}}}val"):
                        pstyle = ps.get(f"{{{WNS['w']}}}val")
                para_id = PARA_IDS.next()
                para_text = "".join(rtext)
                texts.append(para_text)
                cell_paragraphs.append(
                    {
                        "para_id": para_id,
                        "paragraph_index_in_cell": pin_cell,
                        "styleId": pstyle,
                        "direct_pPr": df_p or None,
                        "text": para_text,
                        "runs": runs_out or None,
                        "snippet": safe_snip(para_text),
                        "numId": df_p.get("numId"),
                        "ilvl": df_p.get("ilvl"),
                        "container": {
                            "kind": "table",
                            "context": context,
                            "table_index": table_index,
                            "row_index": rix,
                            "col_index": cix,
                        },
                    }
                )
            cells_out.append(
                {
                    "col_index": cix,
                    "width_cm": wcm,
                    "gridSpan": gridSpan,
                    "vMerge": vMerge,
                    "vAlign": vAlign,
                    "borders": cb or None,
                    "shading": cshade or None,
                    "snippet": safe_snip(" ".join(texts)) or None,
                    "paragraphs": cell_paragraphs or None,
                    "first_para_id": (
                        cell_paragraphs[0]["para_id"] if cell_paragraphs else None
                    ),
                }
            )
        rows_out.append(
            {
                "row_index": rix,
                "height_cm": height,
                "tblHeader": header,
                "cantSplit": cant,
                "cells": cells_out,
            }
        )
    return {
        "context": context,
        "table_index": table_index,
        "paragraph_anchor_index": paragraph_anchor_index,
        "tblPr": {
            "tblStyle": tblStyle,
            "alignment": align,
            "preferred_width": tblW,
            "borders": borders,
            "tblLook": look or None,
            "shading": shading,
        },
        "tblpPr": position or None,
        "grid_cm": grid or None,
        "row_count": len(rows_out),
        "col_count": max((len(r["cells"]) for r in rows_out), default=0),
        "rows": rows_out,
    }


# ---------------- Flow (full paragraphs + assets + fields) ----------------
def parse_flow_for_part(
    zf, part_path, context, assets_out, fields_out, section_index_hint=None
):
    x = read_part(zf, part_path)
    if x is None:
        return [], []
    rels = list_rels(zf, part_path)
    root = x.getroot()
    container = root.find("w:body", namespaces=WNS)
    if container is None:
        container = root  # future-proof: headers/footers have p/tbl at root

    paragraphs = []
    tables = []
    p_index = -1
    table_index = -1

    for child in container:
        lname = get_local(child.tag)
        if lname == "p":
            p_index += 1
            pPr = child.find("w:pPr", namespaces=WNS)
            df_p = extract_pPr(pPr) if pPr is not None else {}
            # fields from this paragraph
            fields_out.extend(
                extract_fields_from_paragraph(
                    child, context, section_index_hint, p_index
                )
            )
            runs_out = []
            texts = []
            r_index = -1
            for r in child.findall("w:r", namespaces=WNS):
                r_index += 1
                t = r.find("w:t", namespaces=WNS)
                rval = t.text if t is not None and t.text else ""
                texts.append(rval)
                rPr = r.find("w:rPr", namespaces=WNS)
                runs_out.append(
                    {
                        "run_index": r_index,
                        "text": rval,
                        "direct_rPr": extract_rPr(rPr) if rPr is not None else {},
                    }
                )
                # assets inside run
                for d in r.findall(".//w:drawing", namespaces=WNS):
                    img = asset_image_from_drawing(
                        d, rels, context, section_index_hint, p_index, r_index
                    )
                    if img:
                        assets_out.append(img)
                    tbx = asset_textbox_from_drawing(
                        d, context, section_index_hint, p_index, r_index
                    )
                    if tbx:
                        assets_out.append(tbx)
            # paragraph style id
            pstyle = None
            if pPr is not None:
                ps = pPr.find("w:pStyle", namespaces=WNS)
                if ps is not None and ps.get(f"{{{WNS['w']}}}val"):
                    pstyle = ps.get(f"{{{WNS['w']}}}val")
            para_id = PARA_IDS.next()
            paragraphs.append(
                {
                    "para_id": para_id,
                    "paragraph_index": p_index,
                    "styleId": pstyle,
                    "direct_pPr": df_p or None,
                    "text": "".join(texts),
                    "runs": runs_out or None,
                    "snippet": safe_snip("".join(texts)),
                    "numId": df_p.get("numId"),
                    "ilvl": df_p.get("ilvl"),
                    "container": {"kind": context},  # body/header/footer
                }
            )

        elif lname == "tbl":
            table_index += 1
            tables.append(
                extract_table(
                    child,
                    rels,
                    context,
                    table_index,
                    paragraph_anchor_index=p_index,
                    fields_out=fields_out,
                )
            )
    return paragraphs, tables


# ---------------- Headers/Footers parts ----------------
def collect_header_footer_parts(zf):
    rels = list_rels(zf, "word/document.xml")
    headers, footers = [], []
    for rid, meta in rels.items():
        t = meta.get("type", "")
        target = meta.get("target")
        if not target:
            continue
        if not target.startswith("/"):
            target = str(Path("word") / target)
        if t.endswith("/header"):
            headers.append(target)
        elif t.endswith("/footer"):
            footers.append(target)
    return headers, footers


# ---------------- CSV ----------------
def write_csv(path, headers, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(headers)
        [w.writerow(r) for r in rows]


# ---------------- Main ----------------
def main():
    ap = argparse.ArgumentParser(
        description="Export .docx → JSON package with full text, styles (inheritance), fields, numbering, sections, headers/footers settings, tables, assets (images+textboxes)."
    )
    ap.add_argument("--input", required=True)
    ap.add_argument("--outdir", default="./out")
    ap.add_argument("--format", default="json")
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    base = os.path.splitext(os.path.basename(args.input))[0]

    with zipfile.ZipFile(args.input, "r") as zf:
        theme_map = parse_theme(zf)
        styles_meta, styles_by_id, doc_defaults = parse_styles(zf)
        memo = {}
        for bucket in [
            "paragraphStyles",
            "characterStyles",
            "tableStyles",
            "listStyles",
        ]:
            for s in styles_meta.get(bucket, []):
                s["resolved_with_sources"] = resolve_style_with_provenance(
                    s["styleId"], styles_by_id, doc_defaults, theme_map, memo
                )

        numbering = parse_numbering(zf)
        settings = parse_settings(zf)
        docx_obj, sections = parse_sections_with_docx(args.input)
        # page numbering + header/footer distance from raw sectPr
        sect_pgnum = parse_section_pgnum_and_margins_ooxml(zf)
        for rec in sect_pgnum:
            idx = rec.get("section_index")
            if 1 <= idx <= len(sections):
                sections[idx - 1]["page_numbering"] = rec.get("page_numbering")
                if rec.get("header_footer_distance_cm"):
                    sections[idx - 1]["header_footer_distance_cm"] = rec[
                        "header_footer_distance_cm"
                    ]

        assets_all = []
        fields_all = []
        body_paras, body_tables = parse_flow_for_part(
            zf,
            "word/document.xml",
            "body",
            assets_all,
            fields_all,
            section_index_hint=None,
        )

        header_parts, footer_parts = collect_header_footer_parts(zf)
        header_paras_all, header_tables_all = [], []
        for hp in header_parts:
            p, t = parse_flow_for_part(
                zf, hp, "header", assets_all, fields_all, section_index_hint=None
            )
            header_paras_all.extend(p)
            header_tables_all.extend(t)
        footer_paras_all, footer_tables_all = [], []
        for fp in footer_parts:
            p, t = parse_flow_for_part(
                zf, fp, "footer", assets_all, fields_all, section_index_hint=None
            )
            footer_paras_all.extend(p)
            footer_tables_all.extend(t)

        # assign asset IDs
        for i, a in enumerate(assets_all, start=1):
            a["id"] = f"asset_{i:04d}"

        package = OrderedDict()
        package["meta"] = {
            "source_file": os.path.abspath(args.input),
            "exporter_version": "3.3",
        }
        package["settings"] = settings
        package["theme"] = theme_map
        package["styles"] = styles_meta
        package["numbering"] = numbering
        package["sections"] = sections
        package["headers"] = {
            "paragraphs": header_paras_all or None,
            "tables": header_tables_all or None,
        }
        package["footers"] = {
            "paragraphs": footer_paras_all or None,
            "tables": footer_tables_all or None,
        }
        package["body"] = {"paragraphs": body_paras, "tables": body_tables}
        package["assets"] = assets_all or None
        package["fields"] = fields_all or None

        formats = {f.strip().lower() for f in args.format.split(",")}
        if "json" in formats:
            jpath = os.path.join(args.outdir, f"{base}__package.json")
            with open(jpath, "w", encoding="utf-8") as f:
                json.dump(package, f, ensure_ascii=False, indent=2)
            print(f"[OK] Wrote JSON: {jpath}")

        if "csv" in formats:
            # --- ENHANCED styles summary (fonts + paragraph spacing/indents/level + provenance) ---
            rows = []
            tcode = {"paragraph": "P", "character": "C", "table": "T", "numbering": "N"}

            def v(d, k):
                x = d.get(k)
                return x.get("value") if isinstance(x, dict) else x

            def src(d, k):
                x = d.get(k)
                return x.get("source") if isinstance(x, dict) else ""

            for bucket in ["paragraphStyles", "characterStyles"]:
                for s in styles_meta.get(bucket, []):
                    rr = s["resolved_with_sources"]["rPr"]
                    rp = s["resolved_with_sources"]["pPr"]

                    if s["type"] == "paragraph":
                        rows.append(
                            [
                                tcode.get(s["type"], s["type"]),
                                s.get("styleId", ""),
                                s.get("name", ""),
                                v(rr, "name_ascii") or v(rr, "name_from_theme") or "",
                                v(rr, "size_pt") or "",
                                1 if v(rr, "b") else 0,
                                1 if v(rr, "i") else 0,
                                1 if v(rr, "u") else 0,
                                v(rp, "alignment") or "left",
                                # spacing / indents
                                v(rp, "space_before_pt") or "",
                                v(rp, "space_after_pt") or "",
                                v(rp, "line_spacing_twips") or "",
                                v(rp, "firstLine_cm") or "",
                                v(rp, "hanging_cm") or "",
                                v(rp, "left_cm") or "",
                                v(rp, "right_cm") or "",
                                # outline level
                                v(rp, "outline_level") or "",
                                # provenance (where each value came from)
                                src(rp, "space_before_pt"),
                                src(rp, "space_after_pt"),
                                src(rp, "line_spacing_twips"),
                                src(rp, "firstLine_cm"),
                                src(rp, "hanging_cm"),
                                src(rp, "left_cm"),
                                src(rp, "right_cm"),
                                src(rp, "outline_level"),
                                # parent link for hierarchy
                                s.get("basedOn", "") or "",
                            ]
                        )
                    else:
                        # Character styles: keep font info; pad paragraph-only columns
                        rows.append(
                            [
                                tcode.get(s["type"], s["type"]),
                                s.get("styleId", ""),
                                s.get("name", ""),
                                v(rr, "name_ascii") or v(rr, "name_from_theme") or "",
                                v(rr, "size_pt") or "",
                                1 if v(rr, "b") else 0,
                                1 if v(rr, "i") else 0,
                                1 if v(rr, "u") else 0,
                                "",
                                "",
                                "",
                                "",
                                "",
                                "",
                                "",
                                "",
                                "",
                                "",
                                "",
                                "",
                                "",
                                "",
                                "",
                                s.get("basedOn", "") or "",
                            ]
                        )

            write_csv(
                os.path.join(args.outdir, f"{base}__styles_summary.csv"),
                [
                    "type",
                    "styleId",
                    "name",
                    "font",
                    "size_pt",
                    "bold",
                    "italic",
                    "underline",
                    "align",
                    "space_before_pt",
                    "space_after_pt",
                    "line_spacing_twips",
                    "firstLine_cm",
                    "hanging_cm",
                    "left_cm",
                    "right_cm",
                    "outline_level",
                    "prov_space_before",
                    "prov_space_after",
                    "prov_line_spacing",
                    "prov_firstLine",
                    "prov_hanging",
                    "prov_left",
                    "prov_right",
                    "prov_outline_level",
                    "basedOn",
                ],
                rows,
            )

            # --- END enhanced styles summary ---

            # Sections (with page numbering)
            srows = []
            for s in sections:
                m = s.get("margins_cm", {})
                pn = s.get("page_numbering", {})
                srows.append(
                    [
                        s["index"],
                        s["orientation"],
                        s["page_width_cm"],
                        s["page_height_cm"],
                        m.get("top"),
                        m.get("bottom"),
                        m.get("left"),
                        m.get("right"),
                        s.get("header_distance_cm"),
                        s.get("footer_distance_cm"),
                        s.get("different_first_page"),
                        s.get("even_and_odd"),
                        pn.get("format"),
                        pn.get("start"),
                    ]
                )
            write_csv(
                os.path.join(args.outdir, f"{base}__sections.csv"),
                [
                    "index",
                    "orientation",
                    "page_width_cm",
                    "page_height_cm",
                    "margin_top_cm",
                    "margin_bottom_cm",
                    "margin_left_cm",
                    "margin_right_cm",
                    "header_distance_cm",
                    "footer_distance_cm",
                    "different_first",
                    "even_and_odd",
                    "page_num_format",
                    "page_num_start",
                ],
                srows,
            )

            # Paragraphs (NOW includes table cell paragraphs via container)
            prows = []

            def add_paras(src, label):
                for p in src:
                    c = p.get("container", {}) or {}
                    prows.append(
                        [
                            p.get("para_id", ""),
                            label,
                            c.get("kind", ""),
                            c.get("table_index", ""),
                            c.get("row_index", ""),
                            c.get("col_index", ""),
                            p.get(
                                "paragraph_index", ""
                            ),  # body/header/footer paragraphs
                            p.get(
                                "paragraph_index_in_cell", ""
                            ),  # cell-local index (if any)
                            p.get("styleId", ""),
                            p.get("numId", ""),
                            p.get("ilvl", ""),
                            p.get("text", ""),
                        ]
                    )

            add_paras(body_paras, "body")
            add_paras(header_paras_all, "header")
            add_paras(footer_paras_all, "footer")

            # also pull paragraphs from inside tables
            def add_cell_paras(tables, label):
                for t in tables:
                    for row in t.get("rows", []):
                        for cell in row.get("cells", []):
                            for p in cell.get("paragraphs") or []:
                                c = p.get("container", {}) or {}
                                prows.append(
                                    [
                                        p.get("para_id", ""),
                                        label,
                                        c.get("kind", ""),
                                        c.get("table_index", ""),
                                        c.get("row_index", ""),
                                        c.get("col_index", ""),
                                        "",  # no global paragraph_index in part
                                        p.get("paragraph_index_in_cell", ""),
                                        p.get("styleId", ""),
                                        p.get("numId", ""),
                                        p.get("ilvl", ""),
                                        p.get("text", ""),
                                    ]
                                )

            add_cell_paras(body_tables, "body")
            add_cell_paras(header_tables_all, "header")
            add_cell_paras(footer_tables_all, "footer")

            write_csv(
                os.path.join(args.outdir, f"{base}__paragraphs.csv"),
                [
                    "para_id",
                    "context",
                    "container_kind",
                    "table_index",
                    "row_index",
                    "col_index",
                    "paragraph_index",
                    "paragraph_index_in_cell",
                    "styleId",
                    "numId",
                    "ilvl",
                    "text",
                ],
                prows,
            )

            # Tables
            trows = []

            def add_tbls(src, label):
                for t in src:
                    pref = t["tblPr"].get("preferred_width") or {}
                    trows.append(
                        [
                            label,
                            t.get("table_index"),
                            t.get("paragraph_anchor_index"),
                            t["tblPr"].get("tblStyle", ""),
                            t["tblPr"].get("alignment", ""),
                            t.get("row_count", 0),
                            t.get("col_count", 0),
                            pref.get("cm")
                            or pref.get("twips")
                            or pref.get("raw")
                            or "",
                        ]
                    )

            add_tbls(body_tables, "body")
            add_tbls(header_tables_all, "header")
            add_tbls(footer_tables_all, "footer")
            write_csv(
                os.path.join(args.outdir, f"{base}__tables.csv"),
                [
                    "context",
                    "table_index",
                    "paragraph_anchor_index",
                    "tblStyle",
                    "alignment",
                    "rows",
                    "cols",
                    "preferred_width",
                ],
                trows,
            )

            # Table cells (add first_para_id bridge)
            crows = []

            def add_cells(src, label):
                for t in src:
                    for row in t.get("rows", []):
                        for cell in row.get("cells", []):
                            crows.append(
                                [
                                    label,
                                    t.get("table_index"),
                                    row.get("row_index"),
                                    cell.get("col_index"),
                                    cell.get("width_cm", ""),
                                    cell.get("gridSpan", ""),
                                    cell.get("vMerge", ""),
                                    cell.get("vAlign", ""),
                                    cell.get("snippet", ""),
                                    cell.get("first_para_id", ""),
                                ]
                            )

            add_cells(body_tables, "body")
            add_cells(header_tables_all, "header")
            add_cells(footer_tables_all, "footer")
            write_csv(
                os.path.join(args.outdir, f"{base}__table_cells.csv"),
                [
                    "context",
                    "table_index",
                    "row_index",
                    "col_index",
                    "width_cm",
                    "gridSpan",
                    "vMerge",
                    "vAlign",
                    "snippet",
                    "first_para_id",
                ],
                crows,
            )

            # Assets (images + textboxes)
            arows = []
            for a in assets_all:
                pos = a.get("position_cm") or {}
                arows.append(
                    [
                        a.get("id"),
                        a.get("type"),
                        a.get("context"),
                        a.get("anchor_type"),
                        a.get("file", ""),
                        a.get("relId", ""),
                        a.get("width_cm", ""),
                        a.get("height_cm", ""),
                        pos.get("x", ""),
                        pos.get("y", ""),
                        a.get("wrap_style", ""),
                        a.get("section_index", ""),
                        a.get("paragraph_index", ""),
                        a.get("run_index", ""),
                        (
                            len(a.get("content", []))
                            if a.get("type") == "textbox"
                            else ""
                        ),
                    ]
                )
            write_csv(
                os.path.join(args.outdir, f"{base}__assets.csv"),
                [
                    "id",
                    "type",
                    "context",
                    "anchor_type",
                    "file",
                    "relId",
                    "width_cm",
                    "height_cm",
                    "pos_x_cm",
                    "pos_y_cm",
                    "wrap_style",
                    "section_index",
                    "paragraph_index",
                    "run_index",
                    "textbox_paragraphs",
                ],
                arows,
            )

            # Fields CSV
            frows = []
            for fld in fields_all or []:
                frows.append(
                    [
                        fld.get("context", ""),
                        fld.get("section_index", ""),
                        fld.get("paragraph_index", ""),
                        fld.get("run_index", ""),
                        fld.get("scope", ""),
                        fld.get("type", ""),
                        fld.get("instruction", ""),
                        fld.get("display_text", ""),
                    ]
                )
            write_csv(
                os.path.join(args.outdir, f"{base}__fields.csv"),
                [
                    "context",
                    "section_index",
                    "paragraph_index",
                    "run_index",
                    "scope",
                    "type",
                    "instruction",
                    "display_text",
                ],
                frows,
            )

            print("[OK] Wrote CSVs.")


if __name__ == "__main__":
    main()
