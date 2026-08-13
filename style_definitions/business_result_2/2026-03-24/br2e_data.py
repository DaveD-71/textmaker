# ============================================================
# BR2e Design System — Single Authoritative Data Source
# All values confirmed from OUP vector PDF (BR2_Intermediate_unit_sample_OUP.pdf)
# Colours pixel-sampled from OUP PDF displayed on iPhone
# Version: 4.1
# ============================================================

VERSION = "4.1"

# ── Page dimensions ──────────────────────────────────────────
PAGE_W = 174.6   # mm — content area width (confirmed from vector)
PAGE_H = 247.0   # mm — content area height (confirmed from vector)

def pw(mm):
    """Percentage of page width, 2 decimal places."""
    return f"{mm / PAGE_W * 100:.2f}%"

def ph(mm):
    """Percentage of page height, 2 decimal places."""
    return f"{mm / PAGE_H * 100:.2f}%"

def mm(val):
    """Format mm value with suffix."""
    return f"{val}mm"

def pt(val):
    """Format pt value."""
    return f"{val}pt"


# ── Structural colours — exact CMYK from vector PDF ─────────
COLOURS = {
    'teal':       {'hex': '#0097B2', 'cmyk': 'C100 M15 Y0 K30',  'role': 'Section heads, col headers, 3.9pt rules, Tip borders'},
    'amber':      {'hex': '#FFA526', 'cmyk': 'C0 M35 Y85 K0',    'role': 'Outcomes header, TP sub-heads, audio refs, accent stripe'},
    'amber_mid':  {'hex': '#FFC97C', 'cmyk': 'C0 M21 Y51 K0',    'role': 'Alt outcomes rows, TP horizontal rules'},
    'amber_lt':   {'hex': '#FFE4BD', 'cmyk': 'C0 M10 Y26 K0',    'role': 'Outcomes body cells (primary)'},
    'amber_bg':   {'hex': '#FFE8C8', 'cmyk': 'C0 M9 Y21 K0',     'role': 'TP large background panel'},
    'amber_tint': {'hex': '#FFD292', 'cmyk': 'C0 M17 Y42 K0',    'role': 'TP organogram mid-tint cells'},
    'blue_lt':    {'hex': '#DEF3F7', 'cmyk': 'C10 M1 Y0 K3',     'role': 'Primary table row bg, Key Expressions bg'},
    'blue_mid':   {'hex': '#BFE8EF', 'cmyk': 'C20 M3 Y0 K6',     'role': 'Secondary row bg, Language Point bg'},
    'blue_sp':    {'hex': '#D4EBF3', 'cmyk': 'C17 M7 Y4 K0',     'role': 'Starting Point sidebar bg'},
    'blue_teal2': {'hex': '#72BFD8', 'cmyk': 'C55 M25 Y15 K0',   'role': '0.4pt decorative rules'},
    'rule_teal':  {'hex': '#A2DDE8', 'cmyk': 'C30 M4 Y0 K9',     'role': 'Table cell hairline rules 0.8pt'},
    'hdr_band':   {'hex': '#6C7F7F', 'cmyk': 'C15 M0 Y0 K50',    'role': 'Running header band (all pages)'},
    'charcoal':   {'hex': '#3C4C4C', 'cmyk': 'C21 M0 Y0 K70',    'role': 'Viewpoint band, unit number block bg, activity numbers'},
    'crimson':    {'hex': '#CC0051', 'cmyk': 'C0 M100 Y60 K20',   'role': 'TP title, crossref ❯❯, Practice file refs'},
    'slate':      {'hex': '#536666', 'cmyk': 'C19 M0 Y0 K60',    'role': 'Language Point header text'},
    'rule_grey':  {'hex': '#A2B2B2', 'cmyk': None,                'role': 'Crossref underline rule 0.8pt'},
}

# ── Level accent colours ─────────────────────────────────────
# Screen hex: pixel-sampled from OUP PDF on iPhone
# CMYK: exact from vector PDF layer
LEVELS = {
    'starter': {
        'name':   'Starter',
        'cefr':   'A1',
        'hex':    '#5C4A85',
        'cmyk':   'C70 M80 Y0 K10',
        'desc':   'Indigo-purple',
        'bg':     '#CECBD7',
        'source': 'pixel-sampled IMG_5827',
    },
    'elem': {
        'name':   'Elementary',
        'cefr':   'A2',
        'hex':    '#BF5E3B',
        'cmyk':   'C0 M80 Y100 K10',
        'desc':   'Terracotta-red',
        'bg':     '#E7D1C5',
        'source': 'pixel-sampled IMG_5827',
    },
    'preint': {
        'name':   'Pre-intermediate',
        'cefr':   'B1',
        'hex':    '#3C7964',
        'cmyk':   'C90 M20 Y70 K20',
        'desc':   'Dark teal-green',
        'bg':     '#C0D7D2',
        'source': 'pixel-sampled IMG_5827',
    },
    'int': {
        'name':   'Intermediate',
        'cefr':   'B1+',
        'hex':    '#D1A624',
        'cmyk':   'C15 M30 Y100 K5',
        'desc':   'Gold/mustard',
        'bg':     '#E6DBBA',
        'source': 'pixel-sampled IMG_5825 cover gold band (~20,000 pixels)',
    },
    'ui': {
        'name':   'Upper-intermediate',
        'cefr':   'B2',
        'hex':    '#458B99',
        'cmyk':   'C100 M0 Y30 K20',
        'desc':   'Muted teal',
        'bg':     '#BFD6DB',
        'source': 'pixel-sampled IMG_5827',
    },
    'adv': {
        'name':   'Advanced',
        'cefr':   'C1',
        'hex':    '#973478',
        'cmyk':   'C35 M100 Y15 K0',
        'desc':   'Dark magenta',
        'bg':     '#DBC4D8',
        'source': 'pixel-sampled IMG_5827',
    },
}

# ── Typography — exact from PDF fontname + size fields ───────
# size_pt: exact value from PDF vector layer
# display_px: screen display size in the guide (scaled up for legibility)
# css_font: font stack for CSS use
FONTS = {
    'body':    {
        'oup':   'PalatinoLTStd-Roman',
        'word':  'Palatino Linotype',
        'gfont': 'Lora',
        'stack': "'Lora', 'Palatino Linotype', Palatino, Georgia, serif",
    },
    'sans':    {
        'oup':   'NewsGothicMTStd',
        'word':  'News Gothic MT',
        'gfont': 'Barlow Condensed',
        'stack': "'Barlow Condensed', 'News Gothic MT', 'Arial Narrow', Arial, sans-serif",
    },
    'slab':    {
        'oup':   'CaeciliaLTStd',
        'word':  'PMN Caecilia',
        'gfont': 'Rokkitt',
        'stack': "'Rokkitt', 'PMN Caecilia', Caecilia, Rockwell, Georgia, serif",
    },
    'page_num':{
        'oup':   'TheSerifBold-Plain',
        'word':  'Georgia Bold',
        'gfont': None,
        'stack': "'TheSerif Bold', Georgia, serif",
    },
    'schedule':{
        'oup':   'TektonPro-BoldCond',
        'word':  'Tekton Pro Bold Condensed',
        'gfont': None,
        'stack': "'Tekton Pro', sans-serif",
    },
    'article': {
        'oup':   'CentennialLTStd-Roman',
        'word':  'Linotype Centennial',
        'gfont': None,
        'stack': "'Linotype Centennial', Georgia, serif",
    },
}

TYPE_SCALE = [
    # (key, role, font_key, weight, size_pt, colour_key, colour_hex, display_px, notes)
    ('unit_title',      'Unit title',                      'sans',  700, 34.10, None,      '#FFFFFF',  28, 'White on #6C7F7F band'),
    ('vp_title_bold',   'Viewpoint "Viewpoint N" (bold)',  'sans',  700, 24.12, None,      '#FFFFFF',  28, 'Bold part of Viewpoint band'),
    ('vp_title_reg',    'Viewpoint topic text (regular)',  'sans',  400, 24.12, None,      '#FFFFFF',  28, 'Regular part — same size, lighter weight'),
    ('vp_pipe',         'Viewpoint pipe "|"',              'sans',  400, 24.12, 'amber',   '#FFA526',  28, 'Amber separator'),
    ('tp_title',        'Talking Point title',             'slab',  700, 17.46, 'crimson', '#CC0051',  22, 'Caecilia Bold crimson'),
    ('contents_unit',   'Contents unit numbers (large)',   'sans',  700, 17.46, 'teal',    '#0097B2',  18, 'Large teal unit numbers in contents table'),
    ('page_num',        'Page number',                     'page_num',700,14.00, None,     '#FFFFFF',  18, 'TheSerif Bold white on #6C7F7F'),
    ('section_head',    'Section heading (WwW | Topic)',   'sans',  700, 11.64, 'teal',    '#0097B2',  15, 'Bold label + regular topic'),
    ('running_head',    'Running header (bold part)',       'sans',  700, 10.81, None,      '#FFFFFF',  14, '"Unit N" bold; topic regular; both 10.81pt'),
    ('act_num',         'Activity numbers',                'sans',  700, 10.40, 'charcoal','#3C4C4C',  14, ''),
    ('tp_sub',          'TP Discussion/Task sub-heads',    'sans',  700, 10.40, 'amber',   '#FFA526',  14, 'Right column of Talking Point page'),
    ('crossref_arrow',  'Crossref ❯❯ marker',              'sans',  400,  9.98, 'crimson', '#CC0051',  14, 'ZapfDingbatsStd'),
    ('tip_label',       'Tip label / Key Expr title',      'sans',  700,  9.15, 'teal',    '#0097B2',  14, ''),
    ('crossref',        'Crossref text',                   'sans',  700,  8.73, 'crimson', '#CC0051',  14, '"For more exercises…" and "Practice file N"'),
    ('audio_tag',       'Audio track reference',           'sans',  700,  8.73, 'amber',   '#FFA526',  14, '"▶5.1" etc'),
    ('act_instr',       'Activity instructions',           'body',  500,  8.11, None,      '#000000',  14, 'Palatino Medium'),
    ('lang_pt_body',    'Language Point body',             'body',  400,  8.11, None,      '#000000',  14, 'Palatino Roman in Language Point box'),
    ('contents_hdr',    'Contents section col headers',    'sans',  400,  8.11, 'teal',    '#0097B2',  13, '"Working with words" etc'),
    ('body',            'Body / reading text',             'body',  400,  7.90, None,      '#000000',  14, 'Palatino Roman'),
    ('body_bold',       'Body bold (grammar terms)',       'body',  700,  7.90, None,      '#000000',  14, ''),
    ('body_italic',     'Body italic (quotes)',            'body',  400,  7.90, None,      '#000000',  14, 'Italic'),
    ('lang_pt_hdr',     'Language Point header',           'sans',  700,  7.90, 'slate',   '#536666',  13, 'All-caps, letter-spaced'),
    ('key_cat',         'Key Expr category labels',        'sans',  700,  7.90, 'charcoal','#3C4C4C',  13, 'Bold, all-caps'),
    ('key_line_79',     'Key Expr lines (7.9pt variant)',  'sans',  400,  7.90, None,      '#000000',  13, 'Email/schedule text in exercises'),
    ('tp_title_org',    'TP organogram section header',    'slab',  700,  7.48, None,      '#FFFFFF',  13, 'Caecilia Bold white on #CC0051 bar'),
    ('tp_body',         'Talking Point body',              'slab',  400,  7.48, None,      '#000000',  13, 'Caecilia Roman'),
    ('example_lbl',     '"Example:" label',                'article',700, 7.48, None,      '#000000',  13, 'CentennialLTStd-BoldItalic'),
    ('key_line',        'Key Expressions lines',           'sans',  400,  7.07, None,      '#000000',  13, ''),
    ('tip_body',        'Tip body text',                   'sans',  400,  7.07, None,      '#000000',  13, 'Inside Tip boxes — News Gothic Regular'),
    ('article_body',    'Article drop-cap paragraph',      'article',400, 7.07, None,      '#000000',  13, 'CentennialLTStd-Roman'),
    ('schedule',        'Schedule/timetable text',         'schedule',700, 7.07, None,     '#000000',  13, 'TektonPro-BoldCond'),
    ('contents_body',   'Contents cell body text',         'sans',  400,  6.65, 'teal',    '#0097B2',  12, 'Topic names, grammar names'),
    ('contents_bold',   'Contents page range numbers',     'sans',  700,  6.65, None,      '#000000',  12, ''),
    ('superscript',     'Inline superscript/fill-in nums', 'body',  400,  5.82, None,      '#000000',  11, 'Palatino Roman small'),
]

# ── Page geometry ─────────────────────────────────────────────
# (label, value_mm, axis)  axis: 'w' or 'h'
GEOMETRY = [
    ('Running header height (interior)',        11.6,   'h', 'y=0–11.6mm from content top'),
    ('Running header height (unit opening)',    22.1,   'h', 'y=40.3–62.4mm; overlaps photo bleed'),
    ('Photo bleed height (unit opening)',       44.5,   'h', 'y=0–44.5mm from content top'),
    ('Unit number block width',                 38.3,   'w', 'x=9.9–48.2mm'),
    ('Unit number block height',                68.7,   'h', 'y=40.3–109.0mm'),
    ('Accent stripe width',                     2.0,    'w', 'Left edge of unit number block'),
    ('Starting Point box width',                107.3,  'w', 'x=53.2–160.5mm'),
    ('Starting Point box height',               126.4,  'h', 'y=109.0–235.4mm'),
    ('Sidebar (Key Expr) width',                48.2,   'w', 'Always on gutter side'),
    ('Sidebar internal left padding',           9.9,    'w', 'All sidebar text starts at 9.9mm from box edge'),
    ('Section heading y from content top',      16.5,   'h', 'y-position — consistent across all interior pages'),
    ('Outer margin',                            10.0,   'w', 'Away from gutter side (approximate)'),
    ('Inner gutter margin (verso)',             35.4,   'w', 'Reserved for binding'),
]

# ── Component positions (y from content top) ─────────────────
POSITIONS = [
    # (label, y_top, y_bottom, height, note)
    ('Running header band (interior)',     0.0,    11.6,   11.6,  ''),
    ('Running header band (unit opening)', 40.3,   62.4,   22.1,  ''),
    ('Photo bleed (unit opening)',         0.0,    44.5,   44.5,  ''),
    ('Unit number block (unit opening)',   40.3,   109.0,  68.7,  ''),
    ('Accent stripe (unit opening)',       40.3,   109.0,  68.7,  '2mm wide, left edge of unit number block'),
    ('Starting Point box (unit opening)',  109.0,  235.4,  126.4, 'x=53.2–160.5mm'),
    ('Section heading (all interior)',     16.5,   None,   None,  'y-position only — not a height'),
    ('Talking Point label bar',            19.1,   25.8,   6.7,   'x=10.8–52.4mm'),
    ('Talking Point title',                40.5,   None,   None,  'y-position only — not a height'),
    ('Page number',                        239.25, None,   None,  'y-position — near bottom of 247.0mm page'),
]

# ── Spacing ───────────────────────────────────────────────────
# Leading values (line spacing)
LEADING = [
    # (role, mm, pt)
    ('Body reading text (Palatino 7.90pt)',         4.37, 12.4),
    ('Activity instructions (Palatino Medium 8.11pt)', 3.50,  9.9),
    ('Talking Point body (Caecilia 7.48pt)',        3.75, 10.6),
    ('Key Expressions lines (News Gothic 7.07pt)',  3.25,  9.2),
    ('Running header text (News Gothic 10.81pt)',   None, None),  # centred in 11.6mm band
]

# Component gaps
GAPS = [
    # (from_to, mm_min, mm_max, pt_min, pt_max, note)
    ('Running header bottom → Section heading',         4.9,  4.9,  13.9, 13.9,  ''),
    ('Section heading → Activity 1 number',            2.7,  8.3,   7.7, 23.5,  'Varies by section'),
    ('Between consecutive activity items',             1.9,  2.2,   5.4,  6.2,  ''),
    ('Activity instruction → continuation line',       0.6,  0.9,   1.7,  2.5,  'Same leading as body'),
    ('Last activity body → Crossref line',             3.5,  4.2,   9.9, 11.9,  ''),
    ('Before Language Point box',                      4.35, 4.35, 12.3, 12.3,  ''),
    ('After Language Point box → next activity',       5.7,  5.7,  16.2, 16.2,  ''),
    ('Running header → Talking Point label bar',       7.5,  7.5,  21.3, 21.3,  ''),
    ('Talking Point label bar → TP title',            14.7, 14.7, 41.7, 41.7,  'Large gap accommodates photo'),
]

# X positions (content-relative)
X_POSITIONS = [
    # (label, x_recto, x_verso, note)
    ('Activity number',                              59.0,  59.0,  'Identical on both'),
    ('Activity instruction (first line)',            61.4,  61.4,  ''),
    ('Activity instruction (continuation)',          63.2,  63.2,  ''),
    ('Body / reading text',                         63.2,  63.2,  ''),
    ('Sub-item bullet (•)',                         63.2,  63.2,  ''),
    ('Sub-item text (after bullet)',                66.5,  66.5,  '3.3mm indent from bullet'),
    ('Crossref ❯❯ marker',                          59.0,  63.2,  ''),
    ('Crossref text "For more…"',                   67.0,  67.0,  ''),
    ('Section heading text',                        53.2,  57.4,  'Differ due to gutter offset'),
    ('Key Expr box text (all levels)',               9.9,   9.9,   '9.9mm padding inside 48.2mm sidebar box'),
    ('Talking Point title + body',                  16.6,  16.6,  ''),
    ('Talking Point Discussion/Task sub-heads',     82.3,  82.3,  'Right column of TP two-column layout'),
    ('Talking Point activity numbers (right col)',  82.3,  82.3,  ''),
    ('TP activity instructions (first line)',       84.7,  84.7,  ''),
    ('TP activity instructions (continuation)',     86.5,  86.5,  ''),
]

# ── Rules and lines ───────────────────────────────────────────
RULES = [
    # (label, weight_pt, weight_mm, colour_hex, span, location)
    ('Section underline rule',     3.90, 1.37, '#0097B2', '101.5mm (full text col)', 'Below section heading on all activity pages'),
    ('Table cell hairline',        0.83, 0.29, '#A2DDE8', '29.5–33.8mm per cell',   'Between rows in vocabulary/grammar tables'),
    ('Fill-in blank underline',    0.33, 0.12, '#000000', '~12–13mm',               'Short underscores for student fill-in activities'),
    ('TP organogram rule',         0.83, 0.29, '#FFA526', '10–26mm',                'Connecting lines in Talking Point organogram'),
    ('Schedule grid rule',         0.42, 0.15, '#666666', '~58–67mm per row',       'Paired horizontal rules in schedule/timetable block'),
    ('Language Point flag rule',   3.90, 1.37, '#FFA526', '52.4mm (full sidebar)',  'Top of Language Point sidebar flag — same weight as section rule'),
]

# ── Icons / symbol fonts ──────────────────────────────────────
ICONS = [
    # (symbol, char, font, size_pt, colour_hex, role)
    ('❯❯', '❯❯', 'ZapfDingbatsStd',   9.98, '#CC0051', 'Cross-reference marker before Practice file refs'),
    ('▶',  '▶',  'EuropeanPiStd-3',   8.32, '#FFA526', 'Audio track marker inline with activity numbers'),
]

# ── Word style map ────────────────────────────────────────────
# (style_name, font_key, weight, size_pt, colour_hex, space_before, space_after, other)
WORD_STYLES = [
    ('BR_Unit_Title',      'sans',     700, 34.10, '#FFFFFF',  0,   0,  'Shading #6C7F7F full width; page break before'),
    ('BR_Section_Head',    'sans',     700, 11.64, '#0097B2', 20,   8,  'Border bottom 3.9pt #0097B2; keep with next'),
    ('BR_Body_Text',       'body',     400,  7.90, '#000000',  0,   8,  'Line spacing exactly 12pt; leading 4.37mm'),
    ('BR_Activity_Instr',  'body',     500,  8.11, '#000000', 12,   4,  'Hanging 1.8mm (first line 61.4mm, cont 63.2mm)'),
    ('BR_Activity_Num',    'sans',     700, 10.40, '#3C4C4C', 12,   4,  'Inline with BR_Activity_Instr; tab at 1.8mm'),
    ('BR_Activity_Sub',    'body',     400,  7.90, '#000000',  4,   4,  'Left indent 1.8mm; alpha label in News Gothic'),
    ('BR_Key_Expr_Title',  'sans',     700,  9.15, '#0097B2',  0,   7,  'Shading #DEF3F7'),
    ('BR_Key_Expr_Cat',    'sans',     700,  7.90, '#3C4C4C',  7,   2,  'All-caps; letter-spacing 0.07em; shading #DEF3F7'),
    ('BR_Key_Expr_Line',   'sans',     400,  7.07, '#000000',  0,   3,  'Shading #DEF3F7'),
    ('BR_Lang_Point_Body', 'body',     400,  8.11, '#000000',  0,   8,  'Shading #BFE8EF; border 0.8pt #A2DDE8'),
    ('BR_Lang_Point_Hdr',  'sans',     700,  7.90, '#536666',  4,   4,  'All-caps; letter-spacing; shading #BFE8EF'),
    ('BR_Tip_Label',       'sans',     700,  9.15, '#0097B2',  0,   3,  'Border top 3.9pt #0097B2'),
    ('BR_Tip_Body',        'sans',     400,  7.07, '#000000',  0,   6,  'News Gothic Regular — text inside Tip boxes'),
    ('BR_Talking_Title',   'slab',     700, 17.46, '#CC0051', 14,   6,  'Slab serif bold — NOT News Gothic or Palatino'),
    ('BR_Talking_Body',    'slab',     400,  7.48, '#000000',  0,   8,  'Slab serif regular'),
    ('BR_Talking_Sub',     'sans',     700, 10.40, '#FFA526', 12,   4,  'Discussion/Task sub-heads in Talking Point pages'),
    ('BR_Crossref',        'sans',     700,  8.73, '#CC0051', 12,   0,  '❯❯ prefix; border top 0.8pt #A2B2B2'),
    ('BR_Running_Head',    'sans', '700+400',10.81,'#FFFFFF',  0,   0,  'Bold for "Unit N", Regular for topic, both 10.81pt; shading #6C7F7F; pipe in #FFA526'),
    ('BR_Page_Number',     'page_num', 700, 14.00, '#FFFFFF',  0,   0,  'In footer band; centred; shading #6C7F7F'),
]

CHAR_STYLES = [
    ('BR_Bold_Key',     'body',  700, '#000000', 'Key vocabulary in reading texts'),
    ('BR_Grammar_Term', 'body',  700, '#000000', 'Grammar labels in Language Point (italic bold)'),
    ('BR_Italic_Term',  'body',  400, '#000000', 'Technical terms in Tips (italic)'),
    ('BR_Task_Verb',    'body',  700, '#000000', 'Opening verb of activity instructions (Read, Listen…)'),
    ('BR_Xref_Target',  'sans',  700, '#CC0051', '"Practice file N" and "Grammar reference" link targets'),
    ('BR_Audio_Tag',    'sans',  700, '#FFA526', 'Track references e.g. ▶5.1'),
]

# ── PPT theme slots ───────────────────────────────────────────
PPT_THEME = {
    'dk1':      '#000000',
    'lt1':      '#FFFFFF',
    'dk2':      '#3C4C4C',   # charcoal — Viewpoint bands, unit num block
    'lt2':      '#DEF3F7',   # blue-light — primary table row bg
    'accent1':  None,        # level accent — swap per level
    'accent2':  '#0097B2',   # teal
    'accent3':  '#FFA526',   # amber
    'accent4':  '#CC0051',   # crimson
    'accent5':  '#6C7F7F',   # header grey
    'accent6':  '#BFE8EF',   # blue-mid
    'hyperlink':'#0097B2',
}

PPT_FONTS = {
    'major': ('News Gothic MT', 'Barlow Condensed', 'All labels, headings, UI elements'),
    'minor': ('Palatino Linotype', 'Lora', 'All body text, activity instructions'),
    'accent':('Rockwell Bold', 'Rokkitt Bold', 'Talking Point title only'),
}

PPT_SLIDE_SIZE = (PAGE_W, PAGE_H)   # 174.6 × 247.0mm

# ── Colour family tint scales ─────────────────────────────────
AMBER_FAMILY = [
    ('#FFA526', 'C0 M35 Y85 K0',   100, 'Outcomes header, accent stripe, audio refs, TP sub-heads'),
    ('#FFC97C', 'C0 M21 Y51 K0',    60, 'Alt outcomes rows, TP horizontal rules'),
    ('#FFD292', 'C0 M17 Y42 K0',    50, 'TP organogram mid-tint cells'),
    ('#FFE4BD', 'C0 M10 Y26 K0',    30, 'Outcomes body cells (primary)'),
    ('#FFE8C8', 'C0 M9 Y21 K0',     25, 'TP large background panel'),
]

TEAL_FAMILY = [
    ('#0097B2', 'C100 M15 Y0 K30', 100, 'Col headers, section text, 3.9pt rules'),
    ('#72BFD8', 'C55 M25 Y15 K0',   55, '0.4pt decorative rules'),
    ('#A2DDE8', 'C30 M4 Y0 K9',     35, '0.8pt table hairline rules'),
    ('#BFE8EF', 'C20 M3 Y0 K6',     25, 'Secondary row bg, Language Point header'),
    ('#D4EBF3', 'C17 M7 Y4 K0',     15, 'Starting Point sidebar bg'),
    ('#DEF3F7', 'C10 M1 Y0 K3',     10, 'Primary table row bg (lightest)'),
]

# ── Photo specifications ──────────────────────────────────────
PHOTOS = [
    {
        'type':     'Unit opening — full-width banner',
        'page':     'Recto (unit opening)',
        'position': 'x=−2.9mm, y=−3.1mm (bleeds)',
        'size_mm':  '177.9 × 48.2mm',
        'pct':      f'101.9% W × 19.5% H',
        'dpi':      '~200dpi',
        'note':     'Horizontal banner crop. Overlapped by header band and unit number block.',
    },
    {
        'type':     'Starting Point — portrait',
        'page':     'Recto (unit opening)',
        'position': 'x=100.0mm, y=155.7mm',
        'size_mm':  '57.6 × 75.7mm',
        'pct':      f'33.0% W × 30.6% H',
        'dpi':      '~197dpi',
        'note':     'Right-column portrait. Subject facing into page.',
    },
    {
        'type':     'Starting Point — landscape',
        'page':     'Recto (unit opening)',
        'position': 'x=100.5mm, y=201.6mm',
        'size_mm':  '56.6 × 36.2mm',
        'pct':      f'32.4% W × 14.7% H',
        'dpi':      '~199dpi',
        'note':     'Second photo below portrait.',
    },
    {
        'type':     'Sidebar column photo (recto)',
        'page':     'Recto (LAW, BC pages)',
        'position': 'x=−2.8mm, varies y',
        'size_mm':  '51.3 × 48.2–48.5mm',
        'pct':      f'29.4% W × 19.5–19.6% H',
        'dpi':      '~200dpi',
        'note':     'Fills sidebar column. Bleeds to left edge.',
    },
    {
        'type':     'Talking Point — background (upper)',
        'page':     'Verso (TP page)',
        'position': 'x=13.8mm, y=16.3mm',
        'size_mm':  '163.6 × 120.3mm',
        'pct':      f'93.7% W × 48.7% H',
        'dpi':      '~200dpi',
        'note':     'Near full-width. TP title and organogram overlay.',
    },
    {
        'type':     'Talking Point — background (lower)',
        'page':     'Verso (TP page)',
        'position': 'x=13.8mm, y=136.0mm',
        'size_mm':  '163.3 × 113.5mm',
        'pct':      f'93.5% W × 45.9% H',
        'dpi':      '~200dpi',
        'note':     'Second photo filling lower half of TP page.',
    },
    {
        'type':     'Viewpoint — article profile photo',
        'page':     'Recto + Verso (VP pages)',
        'position': 'x=6.3–10.8mm, varies y',
        'size_mm':  '41.6–42.2 × 23.4–25.6mm',
        'pct':      f'23.8–24.2% W × 9.5–10.4% H',
        'dpi':      '~200dpi',
        'note':     'Small landscape photo in sidebar area.',
    },
]
