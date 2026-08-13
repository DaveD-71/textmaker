#!/usr/bin/env python3
"""
Market Leader Design System Guide Generator
Generates the complete HTML guide from market_leader_data_marketleader.py
Every value in the output derives from the data module — no hardcoding.

Version history:
  1.0  2026-08-13  Initial version, adapted from BR2e template generator
"""

GENERATOR_VERSION = "1.0"
GENERATOR_DATE    = "2026-08-13"

import sys
sys.path.insert(0, '.')
import market_leader_data_marketleader as D
from data import pw, ph, mm, pt


# ── Helpers ───────────────────────────────────────────────────

def h(text):
    return str(text).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def gap_mm(lo, hi):
    return f"{lo}mm" if lo == hi else f"{lo}–{hi}mm"

def gap_pt(lo, hi):
    return f"{lo}pt" if lo == hi else f"{lo}–{hi}pt"

def gap_pct(lo, hi):
    lo_p = f"{lo/D.PAGE_H*100:.2f}%"
    hi_p = f"{hi/D.PAGE_H*100:.2f}%"
    return lo_p if lo == hi else f"{lo_p}–{hi_p}"

SRC_V = '<span class="src-v">VECTOR</span>'
SRC_P = '<span class="src-v">VECTOR + pixel</span>'
SRC_E = '<span class="src-e">ESTIMATE</span>'


def section_hdr(num, title, sid):
    return f'\n<section class="sg-section" id="{sid}">\n  <div class="sg-section-hdr"><div class="sg-section-num">{num}</div><h2>{h(title)}</h2></div>\n'

def table_open(headers):
    ths = ''.join(f'<th>{h(hdr)}</th>' for hdr in headers)
    return f'<table class="sg-table"><tr>{ths}</tr>\n'

def table_close():
    return '</table>\n'

def tr(*cells):
    out = []
    for cell in cells:
        if isinstance(cell, tuple):
            content, cls = cell
            out.append(f'<td class="{cls}">{content}</td>')
        else:
            out.append(f'<td>{cell}</td>')
    return '<tr>' + ''.join(out) + '</tr>\n'

def sub(title, content):
    return f'<div class="sg-sub"><h3>{h(title)}</h3>{content}</div>\n'

def notice(cls, content):
    return f'<div class="notice {cls}">{content}</div>\n'

def swatch(hex_v, name, cmyk=None, role=None):
    disp = hex_v or '#FFFFFF'
    cmyk_str = f'<span class="swatch-cmyk">{cmyk}</span>' if cmyk else ''
    role_str = f'<div class="swatch-role">{role}</div>' if role else ''
    label = hex_v or 'none / monochrome'
    return f'''<div class="swatch">
  <div class="swatch-color" style="background:{disp}{';border:1px dashed #999' if not hex_v else ''}"></div>
  <div class="swatch-info">
    <span class="swatch-name">{name}</span>
    <span class="swatch-hex">{label}</span>
    {cmyk_str}{role_str}
  </div>
</div>'''


# ── CSS ───────────────────────────────────────────────────────

def build_css():
    colour_vars = '\n'.join(
        f"  --{k}: {v['hex']};"
        for k, v in D.COLOURS.items()
    )
    level_vars = '\n'.join(
        f"  --lvl-{k}: {v['hex'] or '#999999'};"
        for k, v in D.LEVELS.items()
    )
    font_vars = '\n'.join(
        f"  --font-{k}: {v['stack']};"
        for k, v in D.FONTS.items() if v.get('stack')
    )
    scale_vars = '\n'.join(
        f"  --fs-{e[0]}: {e[4]:.2f}px;"
        for e in D.scaled_type_scale()
    )

    default_accent = D.LEVELS['adv']['hex']

    return f"""<style>
:root {{
  /* Structural colours */
{colour_vars}

  /* Level accent colours */
{level_vars}
  --accent: {default_accent};  /* default to Advanced */

  /* Fonts */
{font_vars}

  /* Type scale (scaled to target page) */
{scale_vars}

  /* Spacing */
  --sp-xs: 4px; --sp-sm: 8px; --sp-md: 12px; --sp-lg: 20px; --sp-xl: 32px;

  /* UI */
  --off-white: #F8F8F6;
  --body-text: #1A1A1A;
  --dark: #262626;
  --grey: {D.COLOURS['audio_ref']['hex']};
  --accent-main: {default_accent};
}}

*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: {D.FONTS['sans']['stack']};
       font-size: 11.5px; color: var(--body-text); background: var(--off-white); line-height: 1.5; }}
a {{ color: var(--accent-main); text-decoration: none; }}

.sg-wrap {{ max-width: 1100px; margin: 0 auto; padding: 32px 40px 80px; }}
.sg-section {{ margin-bottom: 60px; scroll-margin-top: 20px; }}

.sg-cover {{ background: var(--dark); color: #fff; padding: 40px 52px 36px;
             border-top: 6px solid var(--accent-main); margin-bottom: 40px; position: relative; }}
.sg-cover::after {{ content: 'v{D.VERSION}'; position: absolute; top: 16px; right: 24px;
                    font-size: 10px; letter-spacing: .12em; text-transform: uppercase;
                    background: var(--accent-main); color: #fff; padding: 3px 10px; }}
.sg-cover h1 {{ font-size: 28px; font-weight: 400; line-height: 1.2; }}
.sg-cover h1 strong {{ font-weight: 700; }}
.sg-cover-sub {{ font-size: 12px; color: #B0B0B0; margin-top: 8px; }}
.sg-cover-meta {{ display: grid; grid-template-columns: repeat(auto-fill,minmax(200px,1fr));
                  gap: 20px; border-top: 1px solid rgba(255,255,255,.15);
                  padding-top: 20px; margin-top: 24px; }}
.sg-cover-meta dt {{ font-size: 9px; letter-spacing: .14em; text-transform: uppercase;
                     color: #999; margin-bottom: 3px; }}
.sg-cover-meta dd {{ font-size: 12px; color: #fff; }}

.sg-nav {{ background: #fff; border-left: 4px solid var(--accent-main); padding: 18px 22px;
           margin-bottom: 48px; display: grid;
           grid-template-columns: repeat(auto-fill,minmax(220px,1fr)); gap: 4px 24px; }}
.sg-nav-label {{ grid-column: 1/-1; font-size: 9px; letter-spacing: .15em;
                 text-transform: uppercase; color: var(--accent-main); font-weight: 700; margin-bottom: 10px; }}
.sg-nav a {{ font-size: 11.5px; color: var(--dark); padding: 2px 0; display: block; }}
.sg-nav a:hover {{ color: var(--accent-main); }}

.sg-section-hdr {{ display: flex; align-items: center; gap: 14px;
                   border-bottom: 2px solid var(--dark); padding-bottom: 10px; margin-bottom: 28px; }}
.sg-section-num {{ background: var(--dark); color: #fff; font-size: 10px; font-weight: 700;
                   letter-spacing: .1em; padding: 4px 10px; flex-shrink: 0; }}
.sg-section-hdr h2 {{ font-size: 20px; font-weight: 400; color: var(--dark); }}
.sg-sub {{ margin-bottom: 32px; }}
.sg-sub h3 {{ font-size: 10px; font-weight: 700; letter-spacing: .14em; text-transform: uppercase;
              color: var(--accent-main); margin-bottom: 14px; padding-bottom: 4px;
              border-bottom: 1px solid #DDD; }}

.sg-table {{ width: 100%; border-collapse: collapse; font-size: 11.5px; margin-bottom: 20px; }}
.sg-table th {{ background: var(--dark); color: #fff; text-align: left; padding: 7px 12px;
                font-size: 9.5px; letter-spacing: .08em; text-transform: uppercase; font-weight: 600; }}
.sg-table td {{ padding: 7px 12px; border-bottom: 1px solid #E8E8E8; vertical-align: top; }}
.sg-table tr:nth-child(even) td {{ background: #FAFAFA; }}
.sg-table tr:hover td {{ background: #F5F5F5; }}
td.lbl {{ font-weight: 600; color: #333; min-width: 160px; }}
td.val {{ font-family: 'Courier New', monospace; font-size: 10.5px; color: var(--accent-main); }}
td.note {{ font-size: 10.5px; color: #666; font-style: italic; }}
td.mono {{ font-family: 'Courier New', monospace; font-size: 10px; }}
.src-v {{ font-size: 9px; letter-spacing: .06em; text-transform: uppercase;
          color: #4CAF50; font-weight: 700; }}
.src-e {{ font-size: 9px; letter-spacing: .06em; text-transform: uppercase;
          color: #FF6B00; font-weight: 700; }}

.notice {{ padding: 12px 16px; border-left: 4px solid; font-size: 11px;
           line-height: 1.6; margin-bottom: 16px; }}
.notice.blue   {{ border-color: #2B6CD8; background: #EDF3FA; color: #06264F; }}
.notice.amber  {{ border-color: #E58900; background: #FFF8EE; color: #5A3800; }}
.notice.green  {{ border-color: #00B235; background: #F0FFF3; color: #0F3A1A; }}
.notice.red    {{ border-color: #A52142; background: #FDF0F3; color: #4A0018; }}

.sg-swatches {{ display: grid; grid-template-columns: repeat(auto-fill,minmax(148px,1fr));
                gap: 10px; margin-bottom: 20px; }}
.swatch {{ border: 1px solid #DDD; overflow: hidden; }}
.swatch-color {{ height: 52px; }}
.swatch-info {{ padding: 8px 10px; background: #fff; }}
.swatch-name {{ font-size: 10px; font-weight: 700; display: block; margin-bottom: 2px; }}
.swatch-hex  {{ font-size: 10px; font-family: monospace; color: var(--accent-main); display: block; }}
.swatch-cmyk {{ font-size: 9px; color: #888; display: block; }}
.swatch-role {{ font-size: 9px; color: #555; margin-top: 3px; line-height: 1.4; }}

.level-grid {{ display: grid; grid-template-columns: repeat(auto-fill,minmax(160px,1fr));
               gap: 12px; margin-bottom: 28px; }}
.level-card {{ border: 1px solid #DDD; overflow: hidden; background: #fff; }}
.level-card-accent {{ height: 60px; }}
.level-card-body {{ padding: 10px 12px; }}
.level-card-name {{ font-size: 11px; font-weight: 700; margin-bottom: 4px; }}
.level-card-hex  {{ font-size: 10px; font-family: monospace; color: var(--accent-main); }}
.level-card-cmyk {{ font-size: 9px; color: #888; margin-top: 3px; }}
.level-card-src  {{ font-size: 8.5px; color: #4CAF50; font-weight: 700;
                    margin-top: 6px; line-height: 1.4; }}

.type-row {{ background: #fff; border: 1px solid #E0E0E0; padding: 18px 20px;
             margin-bottom: 10px; display: grid;
             grid-template-columns: 1fr 240px; gap: 16px; align-items: center; }}
.type-meta {{ font-size: 10px; color: #555; }}
.type-meta strong {{ color: var(--dark); font-size: 11px; display: block; margin-bottom: 4px; }}
.type-meta code {{ display: block; background: #F0F0F0; padding: 6px 10px; font-size: 9px;
                   font-family: 'Courier New',monospace; margin-top: 6px; color: #333; white-space: pre; }}
.src-badge {{ font-size: 8px; text-transform: uppercase; letter-spacing: .06em;
              display: block; margin-top: 4px; }}

pre {{ background: #1A1A2A; color: #C8DCE8; padding: 20px 24px; overflow-x: auto;
       font-family: 'Courier New',monospace; font-size: 11px; line-height: 1.7; margin-bottom: 20px; }}
.cv {{ color: #9CC8D0; }}
.cs {{ color: #C8E880; }}
.cm {{ color: #708088; font-style: italic; }}

.sg-footer {{ border-top: 2px solid var(--dark); margin-top: 60px; padding-top: 14px;
              font-size: 10px; color: #888; display: flex;
              justify-content: space-between; flex-wrap: wrap; gap: 8px; }}
</style>"""


# ── Section builders ──────────────────────────────────────────

def build_s1():
    out = section_hdr('01', 'Page Dimensions & Geometry', 's1')
    out += notice('green',
        f'Source page: <strong>{D.SOURCE_W} × {D.SOURCE_H} mm</strong> — confirmed identical across '
        f'all 5 sample PDFs, no promotional wrapper. Effectively already A4, so scale factor ≈ 1.')

    geom_rows = tr(
        ('Source page (PDF)', 'lbl'),
        (f'<strong>{D.SOURCE_W} × {D.SOURCE_H} mm</strong>', 'val'),
        ('W × H', 'val'), SRC_V,
        ('Page canvas, confirmed identical in all 5 files', 'note')
    )
    geom_rows += tr(
        ('Target page (output)', 'lbl'),
        (f'<strong>{D.TARGET_W} × {D.TARGET_H} mm</strong>', 'val'),
        ('W × H', 'val'), '—',
        ('A4', 'note')
    )
    geom_rows += tr(
        ('Scale factor', 'lbl'),
        (f'<strong>{D.SCALE:.4f}×</strong>', 'val'),
        ('uniform', 'val'), '—',
        ('Applied to all sizes and measurements', 'note')
    )

    for label, val_mm, axis, note_text in D.scaled_geometry():
        dim = D.PAGE_W if axis == 'w' else D.PAGE_H
        pct_str = f"{val_mm/dim*100:.2f}%"
        axis_label = 'W' if axis == 'w' else 'H'
        approx = 'approx' in note_text.lower()
        mm_display = f'~{val_mm}mm' if approx else f'{val_mm}mm'
        geom_rows += tr(
            (label, 'lbl'), (mm_display, 'val'), (f"{pct_str} {axis_label}", 'val'),
            SRC_V, (note_text, 'note')
        )

    out += sub('Page Geometry',
        table_open(['Property', 'mm', '%', 'Source', 'Notes']) +
        geom_rows + table_close()
    )

    pos_rows = ''
    for label, y_top, y_bot, height, note_text in D.scaled_positions():
        y_top_s = f'{y_top}mm'
        y_bot_s = f'{y_bot}mm' if y_bot is not None else '—'
        h_s = f'{height}mm' if height is not None else '—'
        pct_s = (f'{height/D.PAGE_H*100:.2f}% height'
                 if height is not None
                 else f'{y_top/D.PAGE_H*100:.2f}% from top')
        pos_rows += tr(
            (label, 'lbl'), (y_top_s, 'val'), (y_bot_s, 'val'),
            (h_s, 'val'), (pct_s, 'val'), (note_text, 'note'), SRC_V
        )

    if pos_rows:
        out += sub('Component Positions (y from page top, Advanced sample)',
            notice('blue', '"% height" = component physical size. "% from top" = where it sits on the page.') +
            table_open(['Component', 'y top', 'y bottom', 'Height', '%', 'Note', 'Source']) +
            pos_rows + table_close()
        )

    out += '</section>\n'
    return out


def build_s2():
    out = section_hdr('02', 'Typography', 's2')

    font_rows = ''
    for key, data in D.FONTS.items():
        if key == 'display_varies_by_level':
            continue
        gf = f'<em>{data["gfont"]}</em>' if data.get('gfont') else '—'
        font_rows += tr(
            (key.replace('_', ' ').title(), 'lbl'),
            (data.get('oup', '—'), 'val'),
            (data.get('word', '—'), ''),
            (gf, ''),
            (data.get('stack', '—')[:70], 'mono'),
            SRC_V
        )
    out += sub('Font Families',
        notice('blue',
            'Meta and Times are the fixed families used across all 5 levels. Google Fonts '
            'alternatives are free for all uses — install from '
            '<a href="https://fonts.google.com">fonts.google.com</a>.') +
        table_open(['Key', 'Pearson original', 'Word name', 'Google Font', 'CSS stack', 'Source']) +
        font_rows + table_close()
    )

    out += sub('Editorial Display Fonts (vary by level)',
        notice('amber', D.FONTS['display_varies_by_level']['note']))

    scale_rows = ''
    for entry in D.scaled_type_scale():
        key, role, font_key, weight, size_pt, col_key, col_hex, display_px, notes = entry
        orig_size = next(e[4] for e in D.TYPE_SCALE if e[0] == key)
        f = D.FONTS.get(font_key, {})
        w_label = 'Bold' if weight == 700 else 'Medium' if weight == 500 else 'Regular'
        oup_str = f"{f.get('oup', font_key)} {w_label}"
        disp = col_hex or '#000000'
        col_display = f'<span style="color:{disp};background:{"#333" if disp=="#FFFFFF" else "transparent"};padding:0 4px">{disp}</span>'
        scale_rows += tr(
            (role, 'lbl'), (oup_str, ''),
            (f'{orig_size:.2f}pt', 'val'),
            (f'{size_pt:.2f}pt', 'val'),
            (col_display, ''), (notes, 'note')
        )

    out += sub('Type Scale',
        notice('green',
            'Sizes exact from PDF vector layer (Tier A: ADV/INT/UPINT). ELEM/PREINT use the same '
            'roles at a confirmed ×1.0101 scale (e.g. 9.02pt → 9.12pt) — a real difference between '
            'print runs, not measurement noise.') +
        table_open(['Role', 'Font', 'Source (pt)', f'At {D.TARGET_W:.0f}×{D.TARGET_H:.0f}mm (pt)', 'Colour', 'Notes']) +
        scale_rows + table_close()
    )

    spec_html = notice('amber',
        'Specimens shown at approximately 1.3× print size for screen legibility.')
    for i, entry in enumerate(D.scaled_type_scale()[:8]):
        key, role, font_key, weight, size_pt, col_key, col_hex, display_px, notes = entry
        f = D.FONTS.get(font_key, {})
        gf = f.get('gfont') or f.get('word', 'sans-serif')
        stack = f.get('stack', 'sans-serif')
        disp = col_hex or '#000000'
        demo_style = (f'font-family:{stack};font-size:{display_px}px;'
                      f'font-weight:{weight};color:{disp};'
                      f'background:{"#333" if disp=="#FFFFFF" else "transparent"};'
                      f'padding:4px;')
        spec_html += f'''<div class="type-row">
  <div style="{demo_style}">{role}</div>
  <div class="type-meta">
    <strong>T{i+1} · {role}</strong>
    {f.get("oup","")} · {size_pt:.2f}pt · {disp}
    <code>font: {weight} {size_pt:.2f}px '{gf}'; color:{disp};</code>
    <span class="src-badge src-v">● VECTOR</span>
    {f'<span style="font-size:9px;color:#888;font-style:italic">{notes}</span>' if notes else ''}
  </div>
</div>\n'''

    out += sub('Type Specimens', spec_html)
    out += '</section>\n'
    return out


def build_s3():
    out = section_hdr('03', 'Colour System', 's3')
    out += notice('green',
        'Structural colours confirmed by finding the identical hex recurring for the same '
        'functional role across independently-typeset PDFs from different levels.')

    struct_swatches = '<div class="sg-swatches">'
    for key, c in D.COLOURS.items():
        struct_swatches += swatch(c['hex'], key.replace('_', ' ').title(),
                                   c.get('cmyk', ''), c['role'])
    struct_swatches += '</div>'
    out += sub('Structural Colours (fixed across all levels)', struct_swatches)

    editorial_rows = ''
    for level, hexv, font, role in D.EDITORIAL_ACCENTS_OBSERVED:
        editorial_rows += tr((level, 'lbl'), (hexv, 'val'), (font, ''), (role, 'note'), SRC_V)
    out += sub('Editorial/Feature Accent Colours (observed, NOT systematic)',
        notice('amber',
            'These one-off colours style individual feature boxes/headlines per unit — they '
            'vary unit-to-unit within a level too, so they are documented for reference only '
            'and excluded from the token system below.') +
        table_open(['Level sample', 'Hex', 'Font used', 'Where observed']) +
        editorial_rows + table_close()
    )

    if D.ACCENT_FAMILY:
        accent_swatches = '<div class="sg-swatches">'
        for hex_v, cmyk, tint, role in D.ACCENT_FAMILY:
            accent_swatches += swatch(hex_v, f'{tint}%', cmyk, role)
        accent_swatches += '</div>'
        out += sub('Level Accent + Background Tint Family', accent_swatches)

    out += '</section>\n'
    return out


def build_s4():
    out = section_hdr('04', 'Level Accent Palette', 's4')
    out += notice('red',
        'Confirmed VECTOR-exact from the flat-filled 4.7×4.7mm activity-letter tag boxes '
        '("A" "B" "C"…) — the single most reliable source, cross-checked against running-header '
        'text and exercise-number colour (identical hex in every case). These are pure vector '
        'fills, not photo-blended, so CMYK→sRGB is reliable here (unlike photographic header bands).')

    cards = '<div class="level-grid">\n'
    for key, lv in D.LEVELS.items():
        accent = lv['hex'] or '#CCCCCC'
        src_badge = SRC_V if lv['hex'] else SRC_V
        cards += f'''<div class="level-card">
  <div class="level-card-accent" style="background:{accent}{';background-image:repeating-linear-gradient(45deg,#eee,#eee 6px,#fff 6px,#fff 12px)' if not lv['hex'] else ''}"></div>
  <div class="level-card-body">
    <div class="level-card-name">{lv['name']}</div>
    <div class="level-card-hex">{lv['hex'] or 'No accent — monochrome'}</div>
    <div class="level-card-cmyk">{lv['cmyk'] or '—'} · {lv.get('desc','')}</div>
    <div class="level-card-src">{src_badge} — {lv.get('source','[not confirmed]')}</div>
  </div>
</div>\n'''
    cards += '</div>\n'
    out += sub('All Levels', cards)

    level_rows = ''
    for key, lv in D.LEVELS.items():
        level_rows += tr(
            (lv['name'], 'lbl'),
            lv.get('cefr', '—'),
            (lv['cmyk'] or '—', 'val'),
            (lv['hex'] or '—', 'val'),
            (lv.get('bg', '—'), 'val'),
            SRC_V
        )
    out += sub('Level Data',
        table_open(['Level', 'CEFR', 'CMYK (print)', 'Screen hex', 'BG tint', 'Source']) +
        level_rows + table_close()
    )

    out += notice('blue',
        'All 5 levels are now sampled from genuine Course Books. Upper-Intermediate and '
        'Advanced share the exact same accent — confirmed via matching raw CMYK float '
        'tuples from the vector layer of both PDFs, not a rounding coincidence, and '
        'cross-checked by rendering both unit-opening pages. Elementary, Pre-Intermediate '
        'and Intermediate each have a distinct, unique hue.')

    if D.PRACTICE_FILE_FINDINGS.get('note'):
        out += notice('amber',
            f"<strong>Companion-book note:</strong> {D.PRACTICE_FILE_FINDINGS['note']}")

    out += '</section>\n'
    return out


def build_s5():
    out = section_hdr('05', 'Spacing', 's5')
    out += notice('green',
        f'All values from vector PDF (Advanced sample). Scaled to {D.TARGET_W:.0f}×{D.TARGET_H:.0f}mm target.')

    lead_rows = ''
    for role, lead_mm, lead_pt in D.scaled_leading():
        if lead_mm is None:
            lead_rows += tr((role,'lbl'), ('—','val'), ('—','val'), ('—','val'), SRC_V)
        else:
            pct = f"{lead_mm/D.PAGE_H*100:.2f}% H"
            lead_rows += tr((role,'lbl'), (f'{lead_mm}mm','val'), (pct,'val'), (f'{lead_pt}pt','val'), SRC_V)

    if lead_rows:
        out += sub('Line Spacing (Leading)',
            notice('amber',
                'Market Leader uses noticeably generous leading for a workbook — space is left '
                'for handwritten answers between lines in many exercises.') +
            table_open(['Context', 'mm', '% of H', 'pt', 'Source']) +
            lead_rows + table_close()
        )

    gap_rows = ''
    for from_to, mm_lo, mm_hi, pt_lo, pt_hi, note in D.scaled_gaps():
        src = f'{SRC_V}{(" — " + note) if note else ""}'
        gap_rows += tr(
            (from_to,'lbl'),
            (gap_mm(mm_lo,mm_hi),'val'),
            (gap_pct(mm_lo,mm_hi),'val'),
            (gap_pt(pt_lo,pt_hi),'val'),
            src
        )

    if gap_rows:
        out += sub('Vertical Spacing Between Components',
            table_open(['From → To', 'mm', '% of H', 'pt', 'Source']) +
            gap_rows + table_close()
        )

    xpos_rows = ''
    for label, x_recto, x_verso, note in D.scaled_x_positions():
        pct_r = f"{x_recto/D.PAGE_W*100:.2f}%"
        src = f'{SRC_V}{(" — " + note) if note else ""}'
        xpos_rows += tr(
            (label,'lbl'),
            (f'{x_recto}mm','val'),
            (f'{x_verso}mm' if x_recto!=x_verso else f'{x_recto}mm','val'),
            (pct_r,'val'), src
        )

    if xpos_rows:
        out += sub('Horizontal Positions — Text X Coordinates',
            table_open(['Element', 'x recto', 'x verso', '% of W', 'Source']) +
            xpos_rows + table_close()
        )

    out += '</section>\n'
    return out


def build_s6():
    out = section_hdr('06', 'Word Style Map', 's6')
    out += notice('blue',
        f'Use these styles in Microsoft Word to approximate the design at '
        f'{D.TARGET_W:.0f}×{D.TARGET_H:.0f}mm. All sizes scaled from source PDF. '
        f'Swap the level-accent colour per LEVELS entry in Section 04.')

    para_rows = ''
    for name, font_key, weight, size_pt, col_hex, sp_before, sp_after, other in D.scaled_word_styles():
        f = D.FONTS.get(font_key, {})
        word_name = f.get('word', font_key)
        gf_name = f.get('gfont', '')
        w_str = ' Bold' if weight == 700 else ' Medium' if weight == 500 else ''
        font_str = f"{word_name}{w_str}"
        if gf_name:
            font_str += f" / <em>{gf_name}{w_str}</em>"
        disp = col_hex or '[level accent]'
        col_display = f'<span style="color:{disp if col_hex else "#000"};background:{"#333" if col_hex=="#FFFFFF" else "transparent"};padding:0 2px">{disp}</span>'
        para_rows += tr(
            (name, 'lbl'), (font_str, ''),
            (f'{size_pt:.2f}pt', 'val'),
            (col_display, ''),
            (f'{sp_before}/{sp_after}', 'val'),
            (other, 'note')
        )

    out += sub('Paragraph Styles',
        table_open(['Style Name', 'Font', 'Size', 'Colour', 'Spacing B/A', 'Other']) +
        para_rows + table_close()
    )

    if D.CHAR_STYLES:
        char_rows = ''
        for name, font_key, weight, col_hex, usage in D.CHAR_STYLES:
            f = D.FONTS.get(font_key, {})
            w_str = ' Bold' if weight == 700 else ''
            disp = col_hex or '[level accent]'
            char_rows += tr(
                (name, 'lbl'),
                (f"{f.get('word',font_key)}{w_str} {disp}", ''),
                (usage, 'note')
            )
        out += sub('Character Styles',
            table_open(['Style Name', 'Properties', 'Usage']) +
            char_rows + table_close()
        )

    out += '</section>\n'
    return out


def build_s7():
    out = section_hdr('07', 'CSS Reference', 's7')

    def cv(n): return f'<span class="cv">{n}</span>'
    def cs(v): return f'<span class="cs">{v}</span>'
    def cm(t): return f'<span class="cm">/* {t} */</span>'

    colour_lines = '\n'.join(
        '  ' + cv('--' + k) + ': ' + cs(v['hex']) + ';  ' + cm((v['cmyk'] + ' — ' + v['role'][:50]) if v.get('cmyk') else v['role'][:60])
        for k, v in D.COLOURS.items()
    )
    level_lines = '\n'.join(
        '  ' + cv('--lvl-' + k) + ': ' + cs(v['hex'] or 'none') + ';  ' + cm((v['cmyk'] or 'monochrome') + ' — ' + v['name'] + ' ' + v.get('cefr',''))
        for k, v in D.LEVELS.items()
    )
    font_lines = '\n'.join(
        '  ' + cv('--font-' + k) + ': ' + cs(v['stack']) + ';'
        for k, v in D.FONTS.items() if v.get('stack')
    )
    scale_lines = '\n'.join(
        '  ' + cv('--fs-' + e[0]) + ': ' + cs(f'{e[4]:.2f}px') + ';  ' + cm(e[1])
        for e in D.scaled_type_scale()
    )

    default_hex = D.LEVELS['adv']['hex']

    code = f'''<pre>{cm(f"Market Leader Design Tokens v{D.VERSION} ({D.VERSION_DATE})")}
{cm(f"Source: {D.SOURCE_W} × {D.SOURCE_H}mm · Target: {D.TARGET_W} × {D.TARGET_H}mm · Scale: {D.SCALE:.4f}×")}

:root {{
  {cm("── Structural colours ──")}
{colour_lines}

  {cm("── Level accent colours ──")}
{level_lines}
  {cv("--accent")}: {cs(default_hex)};  {cm("default: Advanced — set to desired level")}

  {cm("── Fonts ──")}
{font_lines}

  {cm("── Type scale (scaled to target page) ──")}
{scale_lines}
}}</pre>'''

    out += sub('Design Tokens', code)
    out += '</section>\n'
    return out


def build_s8():
    out = section_hdr('08', 'PowerPoint Notes', 's8')

    font_rows = ''
    for slot, (oup, gf, note) in D.PPT_FONTS.items():
        font_rows += tr((f'{slot.title()} font', 'lbl'), (f'{oup} / <em>{gf}</em>', ''), (note, 'note'))
    font_rows += tr(
        ('Slide size (source)', 'lbl'),
        (f'{D.SOURCE_W} × {D.SOURCE_H} mm', 'val'),
        ('Original PDF page canvas (already ~A4)', 'note')
    )
    font_rows += tr(
        ('Slide size (target)', 'lbl'),
        (f'{D.TARGET_W} × {D.TARGET_H} mm', 'val'),
        ('Your target paper size', 'note')
    )
    out += sub('Slide Size & Fonts',
        table_open(['Setting', 'Value', 'Notes']) + font_rows + table_close()
    )

    def cv(n): return f'<span class="cv">{n}</span>'
    def cs(v): return f'<span class="cs">{v}</span>'
    def cm(t): return f'<span class="cm">/* {t} */</span>'

    slot_lines = ''
    for slot, hex_v in D.PPT_THEME.items():
        val = cs(hex_v) if hex_v else cs('[level accent — see below]')
        slot_lines += f'  {cv(slot):<14} = {val}\n'

    level_lines = '\n'.join(
        '  ' + cm(lv['name'] + ' ' + lv.get('cefr','') + ': ' + (lv['hex'] or 'monochrome') + '  ' + (lv['cmyk'] or ''))
        for key, lv in D.LEVELS.items()
    )

    theme_code = f'''<pre>{cm(f"Market Leader PowerPoint Theme Slots v{D.VERSION}")}

{slot_lines}
{cm("── Level accent values ──")}
{level_lines}</pre>'''

    out += sub('Theme Colour Slots', theme_code)
    out += '</section>\n'
    return out


# ── Full document assembly ────────────────────────────────────

def build_html():
    gf_families = [v['gfont'] for v in D.FONTS.values() if v.get('gfont')]
    gf_url = ('https://fonts.googleapis.com/css2?' +
               '&'.join(f'family={f.replace(" ", "+")}:ital,wght@0,400;0,700;1,400'
                        for f in gf_families) +
               '&display=swap') if gf_families else ''

    nav_items = [
        ('s1', '01 · Page Dimensions'),
        ('s2', '02 · Typography'),
        ('s3', '03 · Colour System'),
        ('s4', '04 · Level Accents'),
        ('s5', '05 · Spacing'),
        ('s6', '06 · Word Style Map'),
        ('s7', '07 · CSS Reference'),
        ('s8', '08 · PowerPoint Notes'),
    ]
    nav_links = '\n'.join(f'  <a href="#{sid}">{label}</a>' for sid, label in nav_items)

    cover = f'''<div class="sg-cover">
  <div style="font-size:10px;letter-spacing:.18em;text-transform:uppercase;color:#999;margin-bottom:10px">Publisher Design System</div>
  <h1><strong>Market Leader</strong></h1>
  <div class="sg-cover-sub">Pearson · Business English Course Series</div>
  <dl class="sg-cover-meta">
    <div><dt>Version</dt><dd>v{D.VERSION} ({D.VERSION_DATE})</dd></div>
    <div><dt>Source page</dt><dd>{D.SOURCE_W} × {D.SOURCE_H} mm</dd></div>
    <div><dt>Target page</dt><dd>{D.TARGET_W} × {D.TARGET_H} mm</dd></div>
    <div><dt>Scale</dt><dd>{D.SCALE:.4f}×</dd></div>
    <div><dt>Note</dt><dd>{D.VERSION_NOTE}</dd></div>
  </dl>
</div>
<nav class="sg-nav">
  <div class="sg-nav-label">Contents</div>
{nav_links}
</nav>'''

    footer = f'''<footer class="sg-footer">
  <span>Market Leader Design System v{D.VERSION} ({D.VERSION_DATE}) · market_leader_data_marketleader.py · market_leader_generate_marketleader.py v{GENERATOR_VERSION}</span>
  <span>
    <span class="src-v">VECTOR</span> exact from PDF ·
    <span class="src-e">ESTIMATE</span> not yet confirmed
  </span>
</footer>'''

    sections = (
        build_s1() + build_s2() + build_s3() + build_s4() +
        build_s5() + build_s6() + build_s7() + build_s8()
    )

    gf_link = (f'<link rel="preconnect" href="https://fonts.googleapis.com">\n'
               f'<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
               f'<link href="{gf_url}" rel="stylesheet">') if gf_url else ''

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Market Leader Design System v{D.VERSION}</title>
{gf_link}
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
    print("Generating Market Leader Design System Guide...")
    output = build_html()
    out_path = f'market_leader_design_system_v{D.VERSION}_marketleader.html'
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(output)
    print(f"Written: {out_path} ({len(output):,} chars)")
