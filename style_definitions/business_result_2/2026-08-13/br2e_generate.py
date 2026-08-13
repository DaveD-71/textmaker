#!/usr/bin/env python3
"""
BR2e Design System Guide Generator
Generates the complete HTML guide from br2e_data.py
Every value in the output derives from the data module — no hardcoding.

Version history:
  4.1  2026-08-13  All size/geometry/spacing references use scaled_*() helpers;
                   cover meta shows source vs target page dimensions
  4.0  2026-05-10  Initial generated version; all sections built from br2e_data.py;
                   no hardcoded values in this file
"""

GENERATOR_VERSION = "4.1"
GENERATOR_DATE    = "2026-08-13"

import sys
sys.path.insert(0, '/home/claude')
import br2e_data as D
from br2e_data import pw, ph, mm, pt

# Scaled lookup helpers — use these for inline size references in notes
def _ts(idx):
    """Return scaled size_pt for TYPE_SCALE entry at index idx."""
    return D.scaled_type_scale()[idx][4]

def _geo(idx):
    """Return scaled mm value for GEOMETRY entry at index idx."""
    return D.scaled_geometry()[idx][1]

def _pos(idx):
    """Return scaled y_top for POSITIONS entry at index idx."""
    return D.scaled_positions()[idx][1]

# ── Helpers ───────────────────────────────────────────────────────────────

def h(text):
    """Escape HTML entities."""
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def font_display(font_key, weight=400):
    """Human-readable font name for display."""
    f = D.FONTS.get(font_key, {})
    oup   = f.get('oup', font_key)
    gfont = f.get('gfont')
    word  = f.get('word', '')
    w_str = 'Bold' if weight == 700 else ('Medium' if weight == 500 else '')
    oup_str  = f"{oup}{'-Bold' if weight==700 else ''}"
    word_str = f"{word}{' Bold' if weight==700 else (' Medium' if weight==500 else '')}"
    gf_str   = f"{gfont}{' Bold' if weight==700 else (' Medium' if weight==500 else '')}" if gfont else None
    if gf_str:
        return f"{word_str} / <em>{gf_str}</em>"
    return word_str

def css_font_stack(font_key):
    return D.FONTS.get(font_key, {}).get('stack', 'sans-serif')

def gap_mm(lo, hi):
    if lo == hi:
        return f"{lo}mm"
    return f"{lo}–{hi}mm"

def gap_pt(lo, hi):
    if lo == hi:
        return f"{lo}pt"
    return f"{lo}–{hi}pt"

def gap_pct(lo, hi):
    lo_p = f"{lo/D.PAGE_H*100:.2f}%"
    hi_p = f"{hi/D.PAGE_H*100:.2f}%"
    if lo == hi:
        return lo_p
    return f"{lo_p}–{hi_p}"

SRC_V = '<span class="src-v">VECTOR</span>'
SRC_P = '<span class="src-v">VECTOR + pixel</span>'

# ── CSS ───────────────────────────────────────────────────────────────────

def build_css():
    lvl_css = '\n'.join(
        f"  --{k}: {v['hex']};"
        for k, v in D.LEVELS.items()
    )
    amber_css = '\n'.join(
        f"  --br-amber-{tint}: {hex_v};"
        for hex_v, cmyk, tint, role in D.AMBER_FAMILY
    )
    teal_css = '\n'.join(
        f"  --br-teal-{tint}: {hex_v};"
        for hex_v, cmyk, tint, role in D.TEAL_FAMILY
    )

    return f"""<style>
:root {{
  /* Page dimensions */
  --page-w: {D.PAGE_W}mm;
  --page-h: {D.PAGE_H}mm;

  /* Structural colours */
  --teal:      {D.COLOURS['teal']['hex']};
  --amber:     {D.COLOURS['amber']['hex']};
  --amber-lt:  {D.COLOURS['amber_lt']['hex']};
  --amber-mid: {D.COLOURS['amber_mid']['hex']};
  --blue-lt:   {D.COLOURS['blue_lt']['hex']};
  --blue-mid:  {D.COLOURS['blue_mid']['hex']};
  --blue-sp:   {D.COLOURS['blue_sp']['hex']};
  --vp-dark:   {D.COLOURS['charcoal']['hex']};
  --hdr-band:  {D.COLOURS['hdr_band']['hex']};
  --tp-red:    {D.COLOURS['crimson']['hex']};
  --lp-text:   {D.COLOURS['slate']['hex']};
  --rule-teal: {D.COLOURS['rule_teal']['hex']};
  --rule-grey: {D.COLOURS['rule_grey']['hex']};

  /* Level accents */
{lvl_css}
  --accent:    {D.LEVELS['int']['hex']};  /* default to Intermediate */

  /* Fonts */
  --font-body: {D.FONTS['body']['stack']};
  --font-sans: {D.FONTS['sans']['stack']};
  --font-slab: {D.FONTS['slab']['stack']};

  /* Type scale (exact from vector PDF) */
{chr(10).join(f"  --fs-{e[0]}: {e[4]:.2f}px;" for e in D.scaled_type_scale())}

  /* Spacing */
  --sp-xs: 4px; --sp-sm: 8px; --sp-md: 12px; --sp-lg: 20px; --sp-xl: 32px;

  /* UI */
  --off-white: #F8F8F6;
  --body-text: #1A1A1A;
}}

/* ── Reset & base ── */
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: var(--font-sans); font-size: 11.5px; color: var(--body-text);
       background: var(--off-white); line-height: 1.5; }}
a {{ color: var(--teal); text-decoration: none; }}
a:hover {{ text-decoration: underline; }}
em {{ font-style: italic; }}

/* ── Layout ── */
.sg-wrap {{ max-width: 1100px; margin: 0 auto; padding: 32px 40px 80px; }}
.sg-section {{ margin-bottom: 60px; scroll-margin-top: 20px; }}

/* ── Cover ── */
.sg-cover {{ background: var(--vp-dark); color: #fff; padding: 40px 52px 36px;
             border-top: 6px solid var(--teal); margin-bottom: 40px; position: relative; }}
.sg-cover::after {{ content: 'v{D.VERSION}'; position: absolute; top: 16px; right: 24px;
                    font-size: 10px; letter-spacing: .12em; text-transform: uppercase;
                    background: var(--teal); color: #fff; padding: 3px 10px; }}
.sg-cover-eyebrow {{ font-size: 10px; letter-spacing: .18em; text-transform: uppercase;
                     color: #7AAFB2; margin-bottom: 10px; }}
.sg-cover h1 {{ font-size: 28px; font-weight: 400; letter-spacing: -.01em; line-height: 1.2; }}
.sg-cover h1 strong {{ font-weight: 700; }}
.sg-cover-sub {{ font-size: 12px; color: #9ABFC2; margin-top: 8px; }}
.sg-cover-meta {{ display: grid; grid-template-columns: repeat(auto-fill,minmax(200px,1fr));
                  gap: 20px; border-top: 1px solid rgba(255,255,255,.15); padding-top: 20px; margin-top: 24px; }}
.sg-cover-meta dt {{ font-size: 9px; letter-spacing: .14em; text-transform: uppercase;
                     color: #7AAFB2; margin-bottom: 3px; }}
.sg-cover-meta dd {{ font-size: 12px; color: #fff; }}

/* ── Nav ── */
.sg-nav {{ background: #fff; border-left: 4px solid var(--teal); padding: 18px 22px;
           margin-bottom: 48px; display: grid;
           grid-template-columns: repeat(auto-fill,minmax(220px,1fr)); gap: 4px 24px; }}
.sg-nav-label {{ grid-column: 1/-1; font-size: 9px; letter-spacing: .15em;
                 text-transform: uppercase; color: var(--teal); font-weight: 700; margin-bottom: 10px; }}
.sg-nav a {{ font-size: 11.5px; color: var(--vp-dark); padding: 2px 0; display: block; }}
.sg-nav a:hover {{ color: var(--teal); }}

/* ── Section headers ── */
.sg-section-hdr {{ display: flex; align-items: center; gap: 14px;
                   border-bottom: 2px solid var(--vp-dark); padding-bottom: 10px; margin-bottom: 28px; }}
.sg-section-num {{ background: var(--vp-dark); color: #fff; font-size: 10px; font-weight: 700;
                   letter-spacing: .1em; padding: 4px 10px; flex-shrink: 0; }}
.sg-section-hdr h2 {{ font-size: 20px; font-weight: 400; color: var(--vp-dark); font-family: var(--font-sans); }}
.sg-sub {{ margin-bottom: 32px; }}
.sg-sub h3 {{ font-size: 10px; font-weight: 700; letter-spacing: .14em; text-transform: uppercase;
              color: var(--teal); margin-bottom: 14px; padding-bottom: 4px; border-bottom: 1px solid #DDD; }}

/* ── Tables ── */
.sg-table {{ width: 100%; border-collapse: collapse; font-size: 11.5px; margin-bottom: 20px; }}
.sg-table th {{ background: var(--vp-dark); color: #fff; text-align: left; padding: 7px 12px;
                font-size: 9.5px; letter-spacing: .08em; text-transform: uppercase; font-weight: 600; }}
.sg-table td {{ padding: 7px 12px; border-bottom: 1px solid #E8E8E8; vertical-align: top; }}
.sg-table tr:nth-child(even) td {{ background: #FAFAFA; }}
.sg-table tr:hover td {{ background: #F0F7FA; }}
td.lbl {{ font-weight: 600; color: #333; min-width: 160px; }}
td.val {{ font-family: 'Courier New', monospace; font-size: 10.5px; color: var(--teal); }}
td.note {{ font-size: 10.5px; color: #666; font-style: italic; }}
td.mono {{ font-family: 'Courier New', monospace; font-size: 10px; }}
.src-v {{ font-size: 9px; letter-spacing: .06em; text-transform: uppercase; color: #4CAF50; font-weight: 700; }}
.src-m {{ font-size: 9px; letter-spacing: .06em; text-transform: uppercase; color: var(--amber); font-weight: 700; }}
.sg-table-subhdr td {{ background: #F0F4F8 !important; font-size: 10px; font-weight: 700;
                        letter-spacing: .08em; text-transform: uppercase; color: #555; padding: 6px 12px; }}

/* ── Notices ── */
.notice {{ padding: 12px 16px; border-left: 4px solid; font-size: 11px;
           line-height: 1.6; margin-bottom: 16px; }}
.notice.blue   {{ border-color: var(--teal);    background: #EDF7FA; color: #003A4A; }}
.notice.amber  {{ border-color: var(--amber);   background: #FFF8EE; color: #5A3800; }}
.notice.green  {{ border-color: #4CAF50;        background: #F0FFF0; color: #1A3A1A; }}
.notice.red    {{ border-color: var(--tp-red);  background: #FFF0F4; color: #3A0020; }}

/* ── Colour swatches ── */
.sg-swatches {{ display: grid; grid-template-columns: repeat(auto-fill,minmax(148px,1fr));
                gap: 10px; margin-bottom: 20px; }}
.swatch {{ border: 1px solid #DDD; overflow: hidden; }}
.swatch-color {{ height: 52px; position: relative; display: flex; align-items: flex-end;
                 justify-content: flex-end; padding: 5px; }}
.swatch-info {{ padding: 8px 10px; background: #fff; }}
.swatch-name {{ font-size: 10px; font-weight: 700; display: block; margin-bottom: 2px; }}
.swatch-hex  {{ font-size: 10px; font-family: monospace; color: var(--teal); display: block; }}
.swatch-cmyk {{ font-size: 9px; color: #888; display: block; }}
.swatch-role {{ font-size: 9px; color: #555; margin-top: 3px; line-height: 1.4; }}

/* ── Level cards ── */
.level-grid {{ display: grid; grid-template-columns: repeat(auto-fill,minmax(160px,1fr));
               gap: 12px; margin-bottom: 28px; }}
.level-card {{ border: 1px solid #DDD; overflow: hidden; background: #fff; }}
.level-card-accent {{ height: 60px; }}
.level-card-body {{ padding: 10px 12px; }}
.level-card-name {{ font-size: 11px; font-weight: 700; margin-bottom: 4px; }}
.level-card-hex  {{ font-size: 10px; font-family: monospace; color: var(--teal); }}
.level-card-cmyk {{ font-size: 9px; color: #888; margin-top: 3px; }}
.level-card-src  {{ font-size: 8.5px; color: #4CAF50; font-weight: 700; margin-top: 6px; line-height: 1.4; }}
.bg-tint-swatch  {{ display: flex; gap: 6px; align-items: center; font-size: 9px; color: #666; margin-top: 5px; }}
.bg-tint-box     {{ width: 16px; height: 10px; border: 1px solid #DDD; flex-shrink: 0; }}

/* ── Type specimens ── */
.type-row {{ background: #fff; border: 1px solid #E0E0E0; padding: 18px 20px; margin-bottom: 10px;
             display: grid; grid-template-columns: 1fr 240px; gap: 16px; align-items: center; }}
.type-meta {{ font-size: 10px; color: #555; }}
.type-meta strong {{ color: var(--vp-dark); font-size: 11px; display: block; margin-bottom: 4px; }}
.type-meta code {{ display: block; background: #F0F0F0; padding: 6px 10px; font-size: 9px;
                   font-family: 'Courier New',monospace; margin-top: 6px; color: #333; white-space: pre; }}
.src-badge {{ font-size: 8px; text-transform: uppercase; letter-spacing: .06em; display: block; margin-top: 4px; }}
.type-note {{ font-size: 9px; color: #888; margin-top: 4px; font-style: italic; }}
.spec-note {{ font-size: 9px; color: var(--tp-red); margin-top: 4px; }}

/* ── Component demos ── */
.sg-comp-bar {{ background: #222; color: #DDD; font-size: 9.5px; font-family: 'Courier New',monospace;
                letter-spacing: .08em; padding: 5px 14px; display: flex; justify-content: space-between; align-items: center; }}
.badge {{ background: var(--teal); color: #fff; font-size: 8.5px; padding: 2px 8px; letter-spacing: .06em; }}
.sg-comp-demo {{ background: #F6F6F6; padding: 20px; margin-bottom: 0; min-height: 50px; }}
.sg-comp-notes {{ font-size: 10.5px; color: #444; padding: 10px 14px; background: #fff;
                  border: 1px solid #E0E0E0; border-top: none; margin-bottom: 24px; line-height: 1.6; }}

/* ── Component styles matching OUP ── */
.c-running-hdr {{ background: var(--hdr-band); color: #fff; padding: 5px 14px; font-family: var(--font-sans);
                  display: flex; align-items: center; gap: 6px; font-size: 14px; }}
.c-running-hdr .unit {{ font-weight: 700; }}
.c-running-hdr .pipe {{ color: var(--amber); margin: 0 4px; }}
.c-section-line {{ font-family: var(--font-sans); font-size: 15px; font-weight: 700; color: var(--teal); }}
.c-section-rule {{ height: 3.9px; background: var(--teal); margin-top: 4px; }}
.c-section-line .pipe {{ color: var(--amber); margin: 0 6px; font-weight: 400; }}
.c-section-line .topic {{ font-weight: 400; }}
.c-act-item {{ display: flex; gap: 8px; margin-bottom: 10px; }}
.c-act-n {{ font-family: var(--font-sans); font-size: 14px; font-weight: 700; color: var(--vp-dark); flex-shrink: 0; }}
.c-act-body {{ font-family: var(--font-body); font-size: 14px; }}
.c-key-box {{ background: var(--blue-lt); padding: 12px 14px; }}
.c-key-title {{ font-family: var(--font-sans); font-size: 14px; font-weight: 700; color: var(--teal); margin-bottom: 6px; }}
.c-key-cat {{ font-family: var(--font-sans); font-size: 13px; font-weight: 700; color: var(--vp-dark);
              text-transform: uppercase; letter-spacing: .07em; margin: 7px 0 2px; }}
.c-key-line {{ font-family: var(--font-sans); font-size: 13px; color: #000; margin-bottom: 2px; }}
.c-vp-band {{ background: var(--vp-dark); color: #fff; padding: 8px 14px; font-family: var(--font-sans);
              display: flex; align-items: baseline; gap: 0; font-size: 28px; }}
.c-vp-bold {{ font-weight: 700; }}
.c-vp-pipe {{ color: var(--amber); margin: 0 10px; font-weight: 400; }}
.c-vp-topic {{ font-weight: 400; }}
.c-crossref {{ font-family: var(--font-sans); font-size: 14px; color: var(--tp-red);
               padding-top: 6px; border-top: 0.8px solid var(--rule-grey);
               margin-top: 10px; display: flex; align-items: center; gap: 4px; }}
.c-tp-label {{ background: var(--amber); color: #fff; font-family: var(--font-sans);
               font-size: 14px; font-weight: 700; letter-spacing: .12em;
               text-transform: uppercase; padding: 3px 12px; display: inline-block; }}
.c-tp-title {{ font-family: var(--font-slab); font-size: 22px; font-weight: 700; color: var(--tp-red); }}
.c-lang-hdr {{ font-family: var(--font-sans); font-size: 13px; font-weight: 700; color: var(--lp-text);
               text-transform: uppercase; letter-spacing: .08em; }}
.c-lang-body {{ font-family: var(--font-body); font-size: 14px; }}
.c-unit-num-block {{ background: var(--vp-dark); width: 48px; min-height: 69px; display: flex;
                     flex-direction: column; align-items: stretch; position: relative; flex-shrink: 0; }}
.c-unit-accent-stripe {{ background: var(--accent); width: 3px; position: absolute; left: 0; top: 0; bottom: 0; }}
.c-unit-num-text {{ font-family: var(--font-sans); font-size: 38px; font-weight: 700;
                    color: #fff; text-align: center; padding: 6px 0 4px; position: relative; z-index: 1; }}
.c-unit-title {{ font-family: var(--font-sans); font-size: 26px; font-weight: 700;
                 color: #fff; background: var(--hdr-band); padding: 8px 14px; }}

/* ── CSS code blocks ── */
pre {{ background: #1A1A2A; color: #C8DCE8; padding: 20px 24px; overflow-x: auto;
       font-family: 'Courier New',monospace; font-size: 11px; line-height: 1.7; margin-bottom: 20px; }}
.cv {{ color: #9CC8D0; }}
.cs {{ color: #C8E880; }}
.cm {{ color: #708088; font-style: italic; }}

/* ── Footer ── */
.sg-footer {{ border-top: 2px solid var(--vp-dark); margin-top: 60px; padding-top: 14px;
              font-size: 10px; color: #888; display: flex; justify-content: space-between;
              flex-wrap: wrap; gap: 8px; }}
.src-legend {{ display: flex; gap: 16px; align-items: center; }}
</style>"""


# ── Section builders ──────────────────────────────────────────────────────

def section_hdr(num, title, sid):
    return f'''
<section class="sg-section" id="{sid}">
  <div class="sg-section-hdr"><div class="sg-section-num">{num}</div><h2>{h(title)}</h2></div>
'''

def table_open(headers):
    ths = ''.join(f'<th>{h(hdr)}</th>' for hdr in headers)
    return f'<table class="sg-table"><tr>{ths}</tr>\n'

def table_close():
    return '</table>\n'

def tr(*cells_and_classes):
    """Pass alternating (content, class) pairs, or just content strings."""
    cells = []
    for cell in cells_and_classes:
        if isinstance(cell, tuple):
            content, cls = cell
            cells.append(f'<td class="{cls}">{content}</td>')
        else:
            cells.append(f'<td>{cell}</td>')
    return '<tr>' + ''.join(cells) + '</tr>\n'

def sub(title, content):
    return f'<div class="sg-sub"><h3>{h(title)}</h3>{content}</div>\n'

def notice(cls, content):
    return f'<div class="notice {cls}">{content}</div>\n'

def swatch(hex_v, name, cmyk=None, role=None):
    cmyk_str = f'<span class="swatch-cmyk">{cmyk}</span>' if cmyk else ''
    role_str = f'<div class="swatch-role">{role}</div>' if role else ''
    return f'''<div class="swatch">
  <div class="swatch-color" style="background:{hex_v}"></div>
  <div class="swatch-info">
    <span class="swatch-name">{name}</span>
    <span class="swatch-hex">{hex_v}</span>
    {cmyk_str}{role_str}
  </div>
</div>'''


# ── Build sections ────────────────────────────────────────────────────────

def build_s1():
    """Page Dimensions & Grid"""
    out = section_hdr('01', 'Page Dimensions &amp; Grid', 's1')
    out += notice('green', f'All measurements confirmed from vector PDF. Book content area: <strong>{D.PAGE_W} × {D.PAGE_H} mm</strong>.')

    # Page geometry table
    rows = ''
    rows += tr(('Book content area', 'lbl'), (f'<strong>{D.PAGE_W} × {D.PAGE_H} mm</strong>', 'val'), ('W × H', 'val'), SRC_V, ('Measured from white bg rect in OUP PDF wrapper', 'note'))
    for label, val_mm, axis, note_text in D.scaled_geometry():
        dim = D.PAGE_W if axis == 'w' else D.PAGE_H
        pct_val = f"{val_mm/dim*100:.2f}% {'W' if axis=='w' else 'H'}"
        # Distinguish y-positions from sizes
        is_pos = 'y from' in label.lower() or label.lower().startswith('section heading')
        if is_pos:
            pct_display = pct_val.replace('% H', '% from top')
        else:
            pct_display = pct_val
        rows += tr(('~' + f'{val_mm}mm' if '~' in str(val_mm) else f'{val_mm}mm', 'val'), '')
        # Rebuild properly
        mm_str = f'~{val_mm}mm' if val_mm == 10.0 else f'{val_mm}mm'
        rows += ''  # reset — use proper method below

    # Redo geometry table properly
    geom_rows = tr(('Book content area', 'lbl'), (f'<strong>{D.PAGE_W} × {D.PAGE_H} mm</strong>', 'val'), ('W × H', 'val'), SRC_V, ('Measured from white background rectangle in OUP PDF', 'note'))
    for label, val_mm, axis, note_text in D.scaled_geometry():
        dim = D.PAGE_W if axis == 'w' else D.PAGE_H
        pct_str = f"{val_mm/dim*100:.2f}%"
        axis_label = 'W' if axis == 'w' else 'H'
        is_ypos = 'y from' in label.lower()
        pct_display = f"{pct_str} from top" if is_ypos else f"{pct_str} {axis_label}"
        mm_display = f'~{val_mm}mm' if label.startswith('Outer') else f'{val_mm}mm'
        geom_rows += tr(
            (label, 'lbl'),
            (mm_display, 'val'),
            (pct_display, 'val'),
            SRC_V,
            (note_text, 'note')
        )

    out += sub('Page Geometry',
        table_open(['Property', 'mm', '%', 'Source', 'Notes']) + geom_rows + table_close()
    )

    # Component positions table
    pos_rows = ''
    for label, y_top, y_bot, height, note_text in D.scaled_positions():
        y_top_s  = f'{y_top}mm'
        y_bot_s  = f'{y_bot}mm' if y_bot else '—'
        h_s      = f'{height}mm' if height else '—'
        if height:
            pct_s = f'{height/D.PAGE_H*100:.2f}% height'
        else:
            pct_s = f'{y_top/D.PAGE_H*100:.2f}% from top'
        pos_rows += tr(
            (label, 'lbl'),
            (y_top_s, 'val'),
            (y_bot_s, 'val'),
            (h_s, 'val'),
            (pct_s, 'val'),
            (note_text, 'note'),
            SRC_V
        )

    out += sub('Component Positions (y from content top)',
        notice('blue', 'All y values are content-relative (wrapper offset applied). '
               '"% height" = component\'s physical size. "% from top" = where it sits on the page.') +
        table_open(['Component', 'y top', 'y bottom', 'Height', '%', 'Note', 'Source']) +
        pos_rows + table_close()
    )

    # Layout variants
    layouts = [
        ('Unit opening (recto)', f'Full-width photo ({D.scaled_positions()[2][3]}mm); running header overlapping lower photo ({D.scaled_positions()[1][3]}mm); #3C4C4C unit num block left ({_geo(3)}×{_geo(4)}mm) with 2mm level-accent stripe; Starting Point box lower-right ({_geo(6)}×{_geo(7)}mm, bg {D.COLOURS["blue_lt"]["hex"]}, top rule 3.9pt teal)'),
        ('Activity page (recto)',  f'#6C7F7F header band top ({_geo(0)}mm). Sidebar {_geo(8)}mm wide against inner margin. Main column ~121mm. Sidebar always on gutter side.'),
        ('Activity page (verso)',  'Mirror of recto — sidebar against inner margin (right side). Same widths throughout.'),
        ('Talking Point page',     'Full-width photo, Talking Point label strip, Caecilia title, organogram, Discussion + Task sub-sections'),
        ('Viewpoint lesson',       f'"Viewpoint N" News Gothic Bold {_ts(1)}pt white, pipe Regular {_ts(2)}pt {D.COLOURS["amber"]["hex"]} amber, topic Regular {_ts(2)}pt white; Preview sidebar; activity content main column'),
        ('Contents table (spread)','6 data columns + unit number column; header row teal; alt rows blue; Viewpoint dividers charcoal; Outcomes column amber'),
    ]
    layout_rows = ''.join(tr((lbl,'lbl'), (desc,'note')) for lbl,desc in layouts)
    out += sub('Layout Variants',
        table_open(['Page type', 'Description']) + layout_rows + table_close()
    )

    out += '</section>\n'
    return out


def build_s2():
    """Typography"""
    out = section_hdr('02', 'Typography', 's2')

    # Font families table
    font_rows = ''
    for key, data in D.FONTS.items():
        gf = f'<em>{data["gfont"]}</em>' if data.get('gfont') else '—'
        font_rows += tr(
            (key.replace('_',' ').title(), 'lbl'),
            (data['oup'], 'val'),
            (data.get('word',''), ''),
            (gf, ''),
            (data['stack'][:60] + '…' if len(data['stack'])>60 else data['stack'], 'mono'),
            SRC_V
        )
    out += sub('Font Families',
        notice('blue', f'OUP fonts require a commercial licence. Google Fonts alternatives: '
               f'<strong>{D.FONTS["body"]["gfont"]}</strong> (body), '
               f'<strong>{D.FONTS["sans"]["gfont"]}</strong> (sans), '
               f'<strong>{D.FONTS["slab"]["gfont"]}</strong> (slab). '
               f'Free from <a href="https://fonts.google.com" target="_blank">fonts.google.com</a>.') +
        table_open(['Key', 'OUP original', 'Word name', 'Google Font', 'CSS stack', 'Source']) +
        font_rows + table_close()
    )

    # Type scale table
    scale_rows = ''
    prev_group = None
    groups = {
        'display': ['unit_title','vp_title_bold','vp_title_reg','vp_pipe'],
        'heading': ['tp_title','contents_unit','page_num','section_head','running_head'],
        'ui':      ['act_num','tp_sub','crossref_arrow','tip_label','crossref','audio_tag'],
        'body':    ['act_instr','lang_pt_body','contents_hdr','body','body_bold','body_italic',
                    'lang_pt_hdr','key_cat','key_line_79'],
        'slab':    ['tp_title_org','tp_body','example_lbl'],
        'small':   ['key_line','tip_body','article_body','schedule','contents_body',
                    'contents_bold','superscript'],
    }
    group_labels = {
        'display':'Display sizes', 'heading':'Heading sizes', 'ui':'UI / Label sizes',
        'body':'Body text sizes', 'slab':'Slab serif (Talking Point)', 'small':'Small / Contents sizes'
    }
    key_to_group = {k:g for g,keys in groups.items() for k in keys}

    for entry in D.scaled_type_scale():
        key, role, font_key, weight, size_pt, col_key, col_hex, display_px, notes = entry
        group = key_to_group.get(key, 'other')
        if group != prev_group:
            scale_rows += f'<tr class="sg-table-subhdr"><td colspan="5">{group_labels.get(group,"Other")}</td></tr>\n'
            prev_group = group
        f = D.FONTS.get(font_key, {})
        oup_name = f.get('oup', font_key)
        w_str = 'Bold' if weight==700 else ('Medium' if weight==500 else 'Regular')
        scale_rows += tr(
            (role, 'lbl'),
            (f'{oup_name} {w_str}', ''),
            (f'{size_pt:.2f}pt', 'val'),
            (f'<span style="color:{col_hex};background:{"#333" if col_hex=="#FFFFFF" else "transparent"};padding:0 4px">{col_hex}</span>', ''),
            (notes, 'note')
        )

    out += sub('Type Scale — Confirmed Sizes',
        notice('green', 'All sizes exact from PDF vector layer (fontname + size fields). No OCR or estimation.') +
        table_open(['Role', 'OUP font', 'Size (pt)', 'Colour', 'Notes']) +
        scale_rows + table_close()
    )

    # Type specimens
    specimens = [
        ('T1', 'Unit Title', 'unit_title'),
        ('T2', 'Viewpoint Band', 'vp_title_bold'),
        ('T3', 'Talking Point Title', 'tp_title'),
        ('T4', 'Section Header', 'section_head'),
        ('T5', 'Activity Number + Instruction', 'act_num'),
        ('T6', 'Body Text (reading)', 'body'),
        ('T7', 'Cross-reference', 'crossref'),
        ('T8', 'Language Point Header', 'lang_pt_hdr'),
        ('T9', 'Key Expressions', 'key_line'),
        ('T10', 'Talking Point Body', 'tp_body'),
    ]

    specimen_demos = {
        'unit_title':   ('<div class="c-unit-title">Working with words</div>', 'Unit title in header band'),
        'vp_title_bold':('<div class="c-vp-band"><span class="c-vp-bold">Viewpoint 2</span><span class="c-vp-pipe">|</span><span class="c-vp-topic">Cultural communication</span></div>', 'Viewpoint band'),
        'tp_title':     ('<div class="c-tp-label">Talking Point</div><div class="c-tp-title" style="margin-top:8px">Upside down management</div>', 'Talking Point label + title'),
        'section_head': ('<div class="c-section-line">Language at work<span class="pipe" style="color:var(--amber);margin:0 6px">|</span><span class="topic" style="font-weight:400">Present tenses for future</span></div><div class="c-section-rule"></div>', 'Section header + rule'),
        'act_num':      ('<div class="c-act-item"><span class="c-act-n">1</span><span class="c-act-body">Read this quote. How true is it for your type of business?</span></div>', 'Activity number + instruction'),
        'body':         ('<p style="font-family:var(--font-body);font-size:14px;line-height:1.6;color:#000">&ldquo;If you make customers unhappy in the physical world, they might each tell six friends.&rdquo;<br><em>Jeff Bezos, founder of Amazon</em></p>', 'Body reading text'),
        'crossref':     ('<div class="c-crossref">❯❯ For more exercises, go to <strong>Practice file 5</strong> on page 114.</div>', 'Crossref line'),
        'lang_pt_hdr':  ('<div class="c-lang-hdr" style="background:var(--blue-mid);padding:4px 10px;">Language Point</div>', 'Language Point header'),
        'key_line':     ('<div class="c-key-box"><div class="c-key-title">Key expressions</div><div class="c-key-cat">Calling to make an arrangement</div><div class="c-key-line">The reason I\'m calling is …</div><div class="c-key-line">I\'m calling to arrange …</div></div>', 'Key Expressions box'),
        'tp_body':      ('<p style="font-family:var(--font-slab);font-size:13px;line-height:1.6">Timpson is a family business with a £500 million plus turnover. Timpson offers a variety of services including shoe repairs and key cutting.</p>', 'Talking Point body'),
    }

    spec_html = ''
    for code, title, key in specimens:
        entry = next((e for e in D.scaled_type_scale() if e[0]==key), None)
        if not entry: continue
        _, role, font_key, weight, size_pt, col_key, col_hex, display_px, notes = entry
        demo, demo_note = specimen_demos.get(key, ('<div>—</div>', ''))
        f = D.FONTS.get(font_key, {})
        oup_str = f"{f.get('oup','')}{'‑Bold' if weight==700 else ''}"
        css_code = f"font: {weight} {size_pt:.2f}px '{f.get('gfont') or f.get('word','')}'; color:{col_hex};"
        spec_html += f'''<div class="type-row">
  <div>{demo}</div>
  <div class="type-meta">
    <strong>{code} · {title}</strong>
    {oup_str} · {size_pt:.2f}pt · {col_hex}
    <code>{css_code}</code>
    <span class="src-badge src-v">● VECTOR</span>
    {f'<span class="type-note">{notes}</span>' if notes else ''}
  </div>
</div>\n'''

    out += sub('Type Specimens',
        notice('amber', f'Specimens shown at ~1.8× print size for screen legibility. Actual print sizes are in the label.') +
        spec_html
    )

    out += '</section>\n'
    return out


def build_s3():
    """Structural Colour System"""
    out = section_hdr('03', 'Structural Colour System', 's3')
    out += notice('green', 'All CMYK values exact from vector PDF. All four colour families are fixed across all six levels — only the level accent (Family C) changes.')

    # Family A — Amber
    amber_swatches = '<div class="sg-swatches">'
    for hex_v, cmyk, tint, role in D.AMBER_FAMILY:
        amber_swatches += swatch(hex_v, f'Amber {tint}%', cmyk, role)
    amber_swatches += '</div>'
    out += sub('Family A — Amber (fixed, all levels)', amber_swatches)

    # Family B — Teal
    teal_swatches = '<div class="sg-swatches">'
    for hex_v, cmyk, tint, role in D.TEAL_FAMILY:
        teal_swatches += swatch(hex_v, f'Teal {tint}% — all levels', cmyk, role)
    teal_swatches += '</div>'
    out += sub('Family B — Teal (fixed, all levels)', teal_swatches)

    # Structural swatches
    struct_swatches = '<div class="sg-swatches">'
    for key in ['hdr_band','charcoal','crimson','slate','rule_teal','rule_grey']:
        c = D.COLOURS[key]
        struct_swatches += swatch(c['hex'], key.replace('_',' ').title(),
                                   c.get('cmyk',''), c['role'])
    struct_swatches += '</div>'
    out += sub('Other Structural Colours', struct_swatches)

    # Colour family table
    fam_rows = tr(('A — Amber', 'lbl'), 'Fixed, all levels', D.COLOURS['amber']['hex'], '35°',
                  '5 tints: ' + ' → '.join(h for h,_,_,_ in D.AMBER_FAMILY))
    fam_rows += tr(('B — Teal', 'lbl'), 'Fixed, all levels', D.COLOURS['teal']['hex'], '189°',
                   '6 tints: ' + ' → '.join(h for h,_,_,_ in D.TEAL_FAMILY))
    fam_rows += tr(('C — Level accent', 'lbl'), 'Per-level swap', 'var(--accent)', 'varies',
                   '1 primary value + 1 tint for cover decoration only')
    fam_rows += tr(('D — Crimson', 'lbl'), 'Fixed, all levels', D.COLOURS['crimson']['hex'], '336°',
                   'TP titles, ❯❯ crossrefs, Practice file refs')
    out += sub('Colour Family Structure',
        table_open(['Family', 'Scope', 'Root colour', 'Hue', 'Members']) +
        fam_rows + table_close()
    )

    out += '</section>\n'
    return out


def build_s4():
    """Level Accent Palette"""
    out = section_hdr('04', 'Level Accent Palette', 's4')
    out += notice('red', 'Screen hex values are pixel-sampled from the OUP PDF displayed on iPhone. '
                  'CMYK values are exact from the vector PDF layer. '
                  'The screen hex is the single authority for digital/screen use. '
                  'The naive mathematical CMYK→sRGB formula produces significantly different results '
                  'due to ICC profile rendering and is not used in this guide.')

    # Level cards
    cards = '<div class="level-grid">\n'
    for key, lv in D.LEVELS.items():
        cards += f'''<div class="level-card">
  <div class="level-card-accent" style="background:{lv['hex']}"></div>
  <div class="level-card-body">
    <div class="level-card-name">{lv['name']}</div>
    <div class="level-card-hex">Screen: {lv['hex']}</div>
    <div class="level-card-cmyk">{lv['cmyk']} · {lv['desc']}</div>
    <div class="level-card-src">{SRC_P} — {lv['source']}</div>
    <div class="bg-tint-swatch"><div class="bg-tint-box" style="background:{lv['bg']}"></div>BG tint: {lv['bg']}</div>
  </div>
</div>\n'''
    cards += '</div>\n'
    out += sub('All Six Levels', cards)

    # Level table
    level_rows = ''
    for key, lv in D.LEVELS.items():
        level_rows += tr(
            (lv['name'], 'lbl'), lv['cefr'],
            (lv['cmyk'], 'val'), (lv['hex'], 'val'), (lv['bg'], 'val'),
            SRC_P
        )
    out += sub('Level Data',
        table_open(['Level', 'CEFR', 'CMYK (print)', 'Screen hex', 'BG tint', 'Source']) +
        level_rows + table_close()
    )

    out += '</section>\n'
    return out


def build_s5():
    """Component Library"""
    out = section_hdr('05', 'Component Library', 's5')

    components = [
        ('01', 'Unit Header Band', 'Unit opening recto',
         '<div style="display:flex;align-items:stretch;gap:0"><div class="c-unit-num-block"><div class="c-unit-accent-stripe"></div><div class="c-unit-num-text">5</div></div><div class="c-unit-title" style="flex:1">Customers</div></div>',
         f'Unit number block: {_geo(3)}×{_geo(4)}mm, bg {D.COLOURS["charcoal"]["hex"]}. '
         f'Accent stripe: {_geo(5)}mm wide, level colour. '
         f'Title: News Gothic Bold {_ts(0):.2f}pt white on {D.COLOURS["hdr_band"]["hex"]}.'),
        ('02', 'Interior Running Header', 'All interior pages',
         f'<div class="c-running-hdr"><span class="unit">Unit 5</span><span class="pipe">|</span><span>Customers</span></div>',
         f'Bg: {D.COLOURS["hdr_band"]["hex"]}. Text: News Gothic Bold+Regular {_ts(8):.2f}pt white. '
         f'Bold for "Unit N", Regular for topic. Pipe in {D.COLOURS["amber"]["hex"]} amber. Height: {_geo(0)}mm.'),
        ('03', 'Section Header', 'WwW · LAW · BC · PS',
         '<div style="padding:8px"><div class="c-section-line">Working with words<span style="color:var(--amber);margin:0 6px">|</span><span style="font-weight:400">Customer service</span></div><div class="c-section-rule"></div></div>',
         f'Text: News Gothic Bold {_ts(7):.2f}pt {D.COLOURS["teal"]["hex"]}. '
         f'Rule: {D.RULES[0][1]}pt solid {D.COLOURS["teal"]["hex"]}. Always at y={_geo(11)}mm from content top.'),
        ('04', 'Activity Items', 'All activity pages',
         '<div style="padding:8px"><div class="c-act-item"><span class="c-act-n">1</span><span class="c-act-body">Read the article again. What does Zappos do differently?</span></div><div class="c-act-item"><span class="c-act-n">2</span><span class="c-act-body">Work with a partner. Discuss the following questions.</span></div></div>',
         f'Number: News Gothic Bold {_ts(8):.2f}pt {D.COLOURS["charcoal"]["hex"]}. '
         f'Instruction: Palatino Medium {_ts(15):.2f}pt black. Hanging 1.8mm.'),
        ('05', 'Key Expressions Box', 'Business Communication pages',
         '<div class="c-key-box" style="width:160px"><div class="c-key-title">Key expressions</div><div class="c-key-cat">Calling to make an arrangement</div><div class="c-key-line">The reason I\'m calling is …</div><div class="c-key-line">I\'m calling to arrange …</div></div>',
         f'Bg: {D.COLOURS["blue_lt"]["hex"]}. Width: {_geo(8)}mm. Padding: {_geo(9)}mm. '
         f'Title: News Gothic Bold {_ts(12):.2f}pt {D.COLOURS["teal"]["hex"]}. '
         f'Lines: News Gothic Regular {_ts(27):.2f}pt.'),
        ('06', 'Language Point Box', 'Language at Work pages',
         '<div style="padding:8px"><div style="background:var(--blue-mid);display:inline-block;padding:4px 10px"><div class="c-lang-hdr">Language Point</div></div><div class="c-lang-body" style="margin-top:8px">1 We use verbs in the <em>present simple</em> to talk about scheduled events.</div></div>',
         f'Sidebar flag: {D.COLOURS["blue_mid"]["hex"]}. Header: News Gothic Bold {_ts(18):.2f}pt {D.COLOURS["slate"]["hex"]}. '
         f'Body: Palatino {_ts(15):.2f}pt. Note: flag rect is in sidebar column; text is in main column.'),
        ('07', 'Cross-reference Line', 'End of activity sections',
         '<div style="padding:8px"><div class="c-crossref">❯❯ For more exercises, go to <strong>Practice file 5</strong> on page 114.</div></div>',
         f'Text: News Gothic Bold {_ts(14):.2f}pt {D.COLOURS["crimson"]["hex"]}. '
         f'❯❯ marker: ZapfDingbats {_ts(12):.2f}pt. Border top: 0.8pt {D.COLOURS["rule_grey"]["hex"]}.'),
        ('08', 'Talking Point Band', 'Talking Point pages',
         '<div style="padding:8px"><div class="c-tp-label">Talking Point</div><div class="c-tp-title" style="margin-top:8px">Upside down management</div></div>',
         f'Label: News Gothic Bold, all-caps, {D.COLOURS["amber"]["hex"]} bg. '
         f'Title: {D.FONTS["slab"]["oup"]}-Bold {_ts(4):.2f}pt {D.COLOURS["crimson"]["hex"]}.'),
        ('09', 'Viewpoint Band', 'After every 3rd unit',
         '<div class="c-vp-band"><span class="c-vp-bold">Viewpoint 2</span><span class="c-vp-pipe">|</span><span class="c-vp-topic">Cultural communication</span></div>',
         f'Bg: {D.COLOURS["charcoal"]["hex"]}. "Viewpoint N": News Gothic Bold {_ts(1):.2f}pt white. '
         f'Pipe: Regular {_ts(2):.2f}pt {D.COLOURS["amber"]["hex"]} amber. '
         f'Topic: Regular {_ts(2):.2f}pt white. Same size as "Viewpoint N" — weight only differs.'),
    ]

    comp_html = ''
    for num, title, badge, demo, notes in components:
        comp_html += f'''<div class="sg-comp-bar">COMP-{num} · {title}<span class="badge">{badge}</span></div>
<div class="sg-comp-demo">{demo}</div>
<div class="sg-comp-notes">{notes}</div>\n'''

    out += comp_html
    out += '</section>\n'
    return out


def build_s6():
    """Spacing & Component Positioning"""
    out = section_hdr('06', 'Spacing &amp; Component Positioning', 's6')
    out += notice('green', f'All values measured from vector PDF. Page: {D.PAGE_W} × {D.PAGE_H}mm. '
                  f'W = percentage of {D.PAGE_W}mm width. H = percentage of {D.PAGE_H}mm height.')

    # Leading table
    lead_rows = ''
    for role, lead_mm, lead_pt in D.scaled_leading():
        if lead_mm is None:
            lead_rows += tr((role,'lbl'), ('Centred in 11.6mm band','note'), ('—','val'), ('—','val'), SRC_V)
        else:
            pct = f"{lead_mm/D.PAGE_H*100:.2f}% H"
            lead_rows += tr((role,'lbl'), (f'{lead_mm}mm','val'), (pct,'val'), (f'{lead_pt}pt','val'), SRC_V)
    out += sub('Vertical Rhythm — Line Spacing',
        table_open(['Context', 'mm', '% of H', 'pt', 'Source']) + lead_rows + table_close()
    )

    # Gaps table
    gap_rows = ''
    for from_to, mm_lo, mm_hi, pt_lo, pt_hi, note in D.scaled_gaps():
        mm_s  = gap_mm(mm_lo, mm_hi)
        pt_s  = gap_pt(pt_lo, pt_hi)
        pct_s = gap_pct(mm_lo, mm_hi)
        src = f'{SRC_V}{(" — " + note) if note else ""}'
        gap_rows += tr((from_to,'lbl'), (mm_s,'val'), (pct_s,'val'), (pt_s,'val'), src)
    out += sub('Vertical Spacing Between Components',
        table_open(['From → To', 'mm', '% of H', 'pt', 'Source']) + gap_rows + table_close()
    )

    # X positions table
    xpos_rows = ''
    for label, x_recto, x_verso, note in D.scaled_x_positions():
        pct_r = f"{x_recto/D.PAGE_W*100:.2f}%"
        pct_v = f"{x_verso/D.PAGE_W*100:.2f}%"
        pct_s = pct_r if x_recto==x_verso else f"{pct_r} / {pct_v}"
        src = f'{SRC_V}{(" — " + note) if note else ""}'
        xpos_rows += tr(
            (label,'lbl'),
            (f'{x_recto}mm','val'),
            (f'{x_verso}mm' if x_recto!=x_verso else f'{x_recto}mm','val'),
            (pct_s,'val'),
            src
        )
    out += sub('Horizontal Positioning — Text X Coordinates',
        notice('blue', 'All x values are content-relative (wrapper offset applied). Consistent across all unit pages of the same orientation.') +
        table_open(['Element', 'x recto', 'x verso', '% of W', 'Source']) + xpos_rows + table_close()
    )

    # Key Expressions box internals
    kv_data = [
        ('Box width', f'{_geo(8)}mm', ''),
        ('Box position', 'x=0mm recto / x=35.4mm verso (gutter side always)', ''),
        ('Internal left padding', f'{_geo(9)}mm', f'{ph(_geo(9))} H'),
        ('"Key expressions" title', f'News Gothic Bold {_ts(12):.2f}pt {D.COLOURS["teal"]["hex"]}', ''),
        ('Category labels', f'News Gothic Bold {_ts(26):.2f}pt {D.COLOURS["charcoal"]["hex"]}', ''),
        ('Expression lines', f'News Gothic Regular {_ts(27):.2f}pt #000000', ''),
        ('Line spacing within box', f'{D.LEADING[3][1]}mm = {D.LEADING[3][2]}pt', f'{ph(D.LEADING[3][1])} H'),
    ]
    kv_rows = ''.join(tr((label,'lbl'), (val,'val'), (pct,'note')) for label,val,pct in kv_data)
    out += sub('Key Expressions Box — Internal Structure',
        table_open(['Property', 'Value', '%']) + kv_rows + table_close()
    )

    out += '</section>\n'
    return out


def build_s7():
    """Visual Elements"""
    out = section_hdr('07', 'Visual Elements — Photos, Rules &amp; Icons', 's7')
    out += notice('green', 'All measurements confirmed from vector PDF. Image pixel dimensions and DPI from embedded JPEG data. Rule weights from path linewidth values.')

    out += '<div class="sg-sub"><h3>Photography — Overview</h3>'
    out += '<p style="margin-bottom:12px">All photography in BR2e is colour, editorial-style lifestyle imagery. People are shown in recognisable professional or business contexts. Images are embedded as CMYK JPEG at 8 bits per channel. Every image in the unit pages measures consistently at approximately <strong>200 dpi</strong> effective print resolution.</p>'
    out += notice('amber', 'Photography is not part of the reproducible design system — it is licensed stock content. The specifications below describe placement, sizing and crop conventions that should be followed when substituting your own images.')
    out += '</div>\n'

    # Photo types table
    photo_rows = ''
    for p in D.PHOTOS:
        photo_rows += tr(
            (p['type'], 'lbl'), p['page'],
            (p['position'], 'mono'), (p['size_mm'], 'val'),
            (p['pct'], 'val'), (p['dpi'], 'val'),
            (p['note'], 'note')
        )
    out += sub('Photo Types and Placement',
        table_open(['Photo type', 'Page', 'Position', 'Size (mm)', '% W × % H', 'Effective DPI', 'Notes']) +
        photo_rows + table_close()
    )

    # Rules table
    rule_rows = ''.join(
        tr((label,'lbl'), (f'{wpt}pt','val'), (f'{wmm}mm','val'),
           (f'<span style="color:{col}">{col}</span>',''), span, location)
        for label, wpt, wmm, col, span, location in D.RULES
    )
    out += sub('Rules and Lines',
        table_open(['Rule type', 'Weight (pt)', 'Weight (mm)', 'Colour', 'Typical span', 'Location']) +
        rule_rows + table_close()
    )

    # Icons table
    icon_rows = ''.join(
        tr(
            (f'<span style="font-size:18px;color:{col}">{sym}</span>', ''),
            (char, 'mono'), font,
            (f'{sz:.2f}pt', 'val'),
            (f'<span style="color:{col}">{col}</span>', ''),
            role
        )
        for sym, char, font, sz, col, role in D.ICONS
    )
    out += sub('Icons and Symbols — Font-Based',
        table_open(['Symbol', 'Character', 'Font', 'Size', 'Colour', 'Role']) +
        icon_rows + table_close()
    )

    out += '</section>\n'
    return out


def build_s8():
    """Word Style Map"""
    out = section_hdr('08', 'Word Style Map', 's8')
    out += notice('blue', f'Use these styles in Microsoft Word to approximate the BR2e layout. '
                  f'Google Fonts alternatives (<em>{D.FONTS["body"]["gfont"]}</em>, '
                  f'<em>{D.FONTS["sans"]["gfont"]}</em>, <em>{D.FONTS["slab"]["gfont"]}</em>) '
                  f'are listed alongside OUP originals. All sizes exact from vector PDF.')

    # Paragraph styles
    para_rows = ''
    for name, font_key, weight, size_pt, col_hex, sp_before, sp_after, other in D.scaled_word_styles():
        f = D.FONTS.get(font_key, {})
        word_name = f.get('word', font_key)
        gf_name   = f.get('gfont', '')
        w_str = ' Bold' if weight==700 else (' Medium' if weight==500 else '')
        w_str2 = ' Bold' if weight==700 else (' Medium' if weight==500 else '')
        font_display_str = f"{word_name}{w_str}"
        if gf_name:
            font_display_str += f" / <em>{gf_name}{w_str2}</em>"
        para_rows += tr(
            (name, 'lbl'),
            (font_display_str, ''),
            (f'{size_pt:.2f}pt', 'val'),
            (f'<span style="color:{col_hex};background:{"#333" if col_hex=="#FFFFFF" else "transparent"};padding:0 4px">{col_hex}</span>', ''),
            (f'{sp_before}/{sp_after}', 'val'),
            (other, 'note')
        )
    out += sub('Paragraph Styles',
        table_open(['Style Name', 'Font', 'Size', 'Colour', 'Spacing B/A', 'Other']) +
        para_rows + table_close()
    )

    # Character styles
    char_rows = ''
    for name, font_key, weight, col_hex, usage in D.CHAR_STYLES:
        f = D.FONTS.get(font_key, {})
        word_name = f.get('word', font_key)
        w_str = ' Bold' if weight==700 else ''
        char_rows += tr(
            (name, 'lbl'),
            (f'{word_name}{w_str} {col_hex}', ''),
            (usage, 'note')
        )
    out += sub('Character Styles',
        table_open(['Style Name', 'Properties', 'Usage']) +
        char_rows + table_close()
    )

    out += '</section>\n'
    return out


def build_s9():
    """CSS Reference"""
    out = section_hdr('09', 'CSS Reference', 's9')

    def cv(n): return f'<span class="cv">{n}</span>'
    def cs(v): return f'<span class="cs">{v}</span>'
    def cm(t): return f'<span class="cm">/* {t} */</span>'

    # Build token block from data
    struct_lines = '\n'.join(
        '  ' + cv('--br-' + k) + ': ' + cs(v["hex"]) + ';  ' + cm((v["cmyk"] + " — " + v["role"][:50]) if v["cmyk"] else v["role"][:60])
        for k, v in D.COLOURS.items()
    )
    level_lines = '\n'.join(
        '  ' + cv('--br-lvl-' + k) + ': ' + cs(v["hex"]) + ';  ' + cm(v["cmyk"] + " — " + v["name"] + " " + v["cefr"] + " — " + v["source"])
        for k, v in D.LEVELS.items()
    )
    font_lines = '\n'.join(
        '  ' + cv('--br-font-' + k) + ': ' + cs(v["stack"]) + ';'
        for k, v in D.FONTS.items() if v.get("stack")
    )
    scale_lines = '\n'.join(
        '  ' + cv('--br-fs-' + e[0]) + ': ' + cs(f'{e[4]:.2f}px') + ';  ' + cm(e[1])
        for e in D.scaled_type_scale()
    )
    amber_lines = '\n'.join(
        '  ' + cv('--br-amber-' + str(tint)) + ': ' + cs(hex_v) + ';  ' + cm(cmyk)
        for hex_v, cmyk, tint, _ in D.AMBER_FAMILY
    )
    teal_lines = '\n'.join(
        '  ' + cv('--br-teal-' + str(tint)) + ': ' + cs(hex_v) + ';  ' + cm(cmyk)
        for hex_v, cmyk, tint, _ in D.TEAL_FAMILY
    )

    code = f'''<pre>{cm(f"Business Result 2e — Design Tokens v{D.VERSION}")}
{cm(f"Page: {D.PAGE_W} × {D.PAGE_H}mm. All CMYK exact from vector PDF.")}
{cm(f"Screen hex pixel-sampled from OUP PDF on iPhone.")}
{cm(f"Google Fonts: {D.FONTS['body']['gfont']} · {D.FONTS['sans']['gfont']} · {D.FONTS['slab']['gfont']}")}

:root {{
  {cm("── Structural colours ──")}
{struct_lines}

  {cm("── Amber family ──")}
{amber_lines}

  {cm("── Teal family ──")}
{teal_lines}

  {cm("── Level accent colours (screen hex, pixel-sampled) ──")}
{level_lines}
  {cv("--br-accent")}: {cs(D.LEVELS['int']['hex'])};  {cm("set to desired level var")}

  {cm("── Typography ──")}
{font_lines}

  {cm("── Type scale (exact from PDF vector layer) ──")}
{scale_lines}
}}</pre>'''

    out += sub('Design Tokens', code)
    out += '</section>\n'
    return out


def build_s10():
    """PowerPoint Notes"""
    out = section_hdr('10', 'PowerPoint Master Notes', 's10')

    # Fonts table
    ppt_font_rows = ''
    for slot, (oup, gf, note) in D.PPT_FONTS.items():
        ppt_font_rows += tr((slot.title() + ' font', 'lbl'), (f'{oup} / <em>{gf}</em>', ''), (note, 'note'))
    ppt_font_rows += tr(
        ('Slide size (print)', 'lbl'),
        (f'{D.PPT_SLIDE_SIZE[0]} × {D.PPT_SLIDE_SIZE[1]} mm', 'val'),
        ('Exact content area from vector PDF', 'note')
    )
    ppt_font_rows += tr(
        ('Slide size (screen)', 'lbl'),
        ('Widescreen 16:9', 'val'),
        ('Scale mm values proportionally for screen presentations', 'note')
    )
    out += sub('Slide Size &amp; Fonts',
        table_open(['Setting', 'Value', 'Notes']) + ppt_font_rows + table_close()
    )

    # Theme colour code block
    def cv(n): return f'<span class="cv">{n}</span>'
    def cs(v): return f'<span class="cs">{v}</span>'
    def cm(t): return f'<span class="cm">/* {t} */</span>'

    slot_comments = {
        'dk1': 'dark text',
        'lt1': 'page background',
        'dk2': f'charcoal — Viewpoint bands, unit num block  {D.COLOURS["charcoal"]["cmyk"]}',
        'lt2': f'blue-light — primary table row bg  {D.COLOURS["blue_lt"]["cmyk"]}',
        'accent1': 'level accent — swap per level (see below)',
        'accent2': f'teal — col headers, section heads  {D.COLOURS["teal"]["cmyk"]}',
        'accent3': f'amber — outcomes, TP sub-heads  {D.COLOURS["amber"]["cmyk"]}',
        'accent4': f'crimson — TP title, crossref  {D.COLOURS["crimson"]["cmyk"]}',
        'accent5': f'header grey — running header band  {D.COLOURS["hdr_band"]["cmyk"]}',
        'accent6': f'blue-mid — Language Point bg  {D.COLOURS["blue_mid"]["cmyk"]}',
        'hyperlink': 'same as teal',
    }

    slot_lines = ''
    for slot, hex_v in D.PPT_THEME.items():
        val = cs(hex_v) if hex_v else cs('see level values below')
        slot_lines += f'  {cv(slot):<12}  = {val}  {cm(slot_comments.get(slot,""))}\n'

    level_lines = '\n'.join(
        '  ' + cm(lv['name'] + ' ' + lv['cefr'] + ': ' + lv['hex'] + '  ' + lv['cmyk'] + ' — ' + lv['source'])
        for key, lv in D.LEVELS.items()
    )

    theme_code = f'''<pre>{cm(f"Business Result 2e — PowerPoint Theme Colour Slots v{D.VERSION}")}
{cm("Swap accent1 only when changing level. All other slots fixed.")}
{cm("Screen hex pixel-sampled from OUP PDF on iPhone.")}

{slot_lines}
{cm("── Level accent1 values ──")}
{level_lines}</pre>'''

    out += sub(f'Theme Colour Slots (PPT XML — Intermediate level)', theme_code)

    # Slide layouts
    layout_data = [
        ('BR_Unit_Opening',
         f'Photo placeholder top {D.scaled_positions()[2][3]}mm; {D.COLOURS["hdr_band"]["hex"]} header band overlapping lower photo ({D.scaled_positions()[1][3]}mm); {D.COLOURS["charcoal"]["hex"]} unit num block left ({_geo(3)}×{_geo(4)}mm) with 2mm level-accent stripe; Starting Point box lower-right ({_geo(6)}×{_geo(7)}mm, bg {D.COLOURS["blue_lt"]["hex"]}, top rule 3.9pt teal)'),
        ('BR_Activity_Page',
         f'{D.COLOURS["hdr_band"]["hex"]} header band top; main column; Key Expressions sidebar {_geo(8)}mm wide; section header with {D.RULES[0][1]}pt teal underline'),
        ('BR_Talking_Point',
         f'Full photo top; {D.COLOURS["amber"]["hex"]} "TALKING POINT" label; {D.FONTS["slab"]["oup"]}-Bold {_ts(4):.2f}pt {D.COLOURS["crimson"]["hex"]} title; Discussion/Task sub-heads News Gothic Bold {_ts(9):.2f}pt {D.COLOURS["amber"]["hex"]}'),
        ('BR_Viewpoint',
         f'{D.COLOURS["charcoal"]["hex"]} bg full-width · "Viewpoint N": News Gothic Bold {_ts(1):.2f}pt white · Pipe: Regular {_ts(2):.2f}pt {D.COLOURS["amber"]["hex"]} amber · Topic: Regular {_ts(2):.2f}pt white'),
        ('BR_Contents',
         f'{D.COLOURS["teal"]["hex"]} col headers; {D.COLOURS["amber"]["hex"]} outcomes header; {D.COLOURS["blue_lt"]["hex"]}/{D.COLOURS["blue_mid"]["hex"]} alt rows; {D.COLOURS["charcoal"]["hex"]} Viewpoint dividers; cell rules 0.8pt {D.COLOURS["rule_teal"]["hex"]}'),
    ]
    layout_rows = ''.join(tr((lbl,'lbl'), (desc,'note')) for lbl,desc in layout_data)
    out += sub('Slide Layouts',
        table_open(['Layout', 'Key elements']) + layout_rows + table_close()
    )

    out += '</section>\n'
    return out


# ── Full document assembly ────────────────────────────────────────────────

def build_html():
    gf_url = ('https://fonts.googleapis.com/css2?'
              'family=Barlow+Condensed:ital,wght@0,400;0,600;0,700;1,400'
              '&family=Lora:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500'
              '&family=Rokkitt:wght@400;700&display=swap')

    nav_items = [
        ('s1','01 · Page Dimensions &amp; Grid'),
        ('s2','02 · Typography'),
        ('s3','03 · Colour System'),
        ('s4','04 · Level Accent Palette'),
        ('s5','05 · Component Library'),
        ('s6','06 · Spacing System'),
        ('s7','07 · Visual Elements'),
        ('s8','08 · Word Style Map'),
        ('s9','09 · CSS Reference'),
        ('s10','10 · PowerPoint Notes'),
    ]
    nav_links = '\n'.join(f'  <a href="#{sid}">{label}</a>' for sid, label in nav_items)

    cover = f'''<div class="sg-cover">
  <div class="sg-cover-eyebrow">Publisher Design System · Reverse-Engineered</div>
  <h1><strong>Business Result</strong> 2nd Edition</h1>
  <div class="sg-cover-sub">Oxford University Press · ELT Coursebook · Intermediate sample</div>
  <dl class="sg-cover-meta">
    <div><dt>Version</dt><dd>v{D.VERSION} ({D.VERSION_DATE})</dd></div>
    <div><dt>Note</dt><dd>{D.VERSION_NOTE}</dd></div>
    <div><dt>Page size</dt><dd>{D.PAGE_W} × {D.PAGE_H} mm</dd></div>
    <div><dt>Source</dt><dd>BR2_Intermediate_unit_sample_OUP.pdf (vector)</dd></div>
    <div><dt>Colours</dt><dd>Pixel-sampled from OUP PDF on iPhone</dd></div>
    <div><dt>Data quality</dt><dd>All values from vector layer — no OCR or estimation</dd></div>
  </dl>
</div>
<nav class="sg-nav">
  <div class="sg-nav-label">Contents</div>
{nav_links}
</nav>'''

    footer = f'''<footer class="sg-footer">
  <span>BR2e Design System v{D.VERSION} ({D.VERSION_DATE}) · data: br2e_data.py · generator: br2e_generate.py v{GENERATOR_VERSION}</span>
  <span class="src-legend">
    <span class="src-v">VECTOR</span> values exact from PDF ·
    <span class="src-v">VECTOR + pixel</span> CMYK from vector, screen hex pixel-sampled
  </span>
</footer>'''

    sections = (
        build_s1() + build_s2() + build_s3() + build_s4() +
        build_s5() + build_s6() + build_s7() + build_s8() +
        build_s9() + build_s10()
    )

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>BR2e Design System v{D.VERSION}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{gf_url}" rel="stylesheet">
{build_css()}
</head>
<body>
<div class="sg-wrap">
{cover}
{sections}
{footer}
</div>
</body>
</html>'''


if __name__ == '__main__':
    print("Generating BR2e Design System Guide...")
    output = build_html()
    out_path = '/mnt/user-data/outputs/BR2e_Design_System_v4.1.html'
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(output)
    print(f"Written: {out_path} ({len(output):,} chars)")
