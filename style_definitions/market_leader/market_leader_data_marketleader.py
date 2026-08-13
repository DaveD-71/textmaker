# ============================================================
# Market Leader Design System — Single Authoritative Data Source
# Publisher: Pearson
# Source PDFs: Market_Leader_ADV/ELEM/INT/PREINT/UPINT_-_Course_Book.pdf
#              (plus Market_Leader_UPINT_-__Practice_File.pdf as a
#              secondary companion-book reference — see PRACTICE_FILE_FINDINGS)
# ============================================================
#
# All values confirmed from Pearson vector PDF sample chapters — one Unit 1
# Course Book sample per level (5 levels: Elementary, Pre-Intermediate,
# Intermediate, Upper-Intermediate, Advanced), plus one Practice File sample
# kept as a secondary reference for a companion-book-type finding.
#
# DATA QUALITY MARKERS:
#   VECTOR  — exact value from PDF vector layer (fontname/size/rect/CMYK)
#   PIXEL   — pixel-sampled from rendered PDF on screen
#   ESTIMATE — not yet confirmed from source (flag for review)
#
# Version history:
#   1.0  2026-08-13  Initial extraction from 5 Market Leader sample PDFs
#   1.1  2026-08-13  Corrected Upper-Intermediate: replaced Practice File
#                    (monochrome, wrong book type) with genuine Course Book
#                    sample. Confirmed UPINT accent = #2B6CD8, identical to
#                    Advanced (exact CMYK match, verified not a coincidence).
#                    Practice File findings retained separately.
# ============================================================

VERSION      = "1.1"
VERSION_DATE = "2026-08-13"
VERSION_NOTE = "Corrected Upper-Intermediate to genuine Course Book sample (was Practice File)"


# ══════════════════════════════════════════════════════════════
# SECTION 1 — PAGE DIMENSIONS
# ══════════════════════════════════════════════════════════════
# All 5 sample PDFs are unwrapped — no promotional shell. Page canvas
# IS the content area. Confirmed identical across all 5 files: VECTOR.
#
# IMPORTANT — two scale tiers were found in the underlying InDesign
# typesetting even though the exported page canvas is identical:
#   Tier A (ADV, INT, UPINT):    body text set at 9.02–9.03pt etc.
#   Tier B (ELEM, PREINT):       same roles set ~1.01x larger (9.12pt etc.)
# This is a real, confirmed difference between print runs/reprints of
# different levels, not a measurement error (ratio is consistently
# 0.990 across every matched role — see SECTION 5 notes).
# SOURCE_W/H below describe the shared page canvas; TYPE_SCALE values
# are Tier A (ADV/INT/UPINT), with Tier B noted inline.

SOURCE_W = 209.9   # mm — page canvas width, confirmed identical all 5 PDFs [VECTOR]
SOURCE_H = 297.0   # mm — page canvas height (= A4)                        [VECTOR]

TARGET_W = 210.0   # mm — A4 width
TARGET_H = 297.0   # mm — A4 height

_scale_w = TARGET_W / SOURCE_W if SOURCE_W > 0 else 1.0
_scale_h = TARGET_H / SOURCE_H if SOURCE_H > 0 else 1.0
SCALE = (_scale_w + _scale_h) / 2   # ≈ 1.0005 — page canvas is already ~A4

PAGE_W = SOURCE_W * SCALE
PAGE_H = SOURCE_H * SCALE


def pw(mm_val):
    return f"{mm_val / PAGE_W * 100:.2f}%"

def ph(mm_val):
    return f"{mm_val / PAGE_H * 100:.2f}%"

def s(val):
    return round(val * SCALE, 2)

def smm(val):
    return f"{s(val)}mm"

def spt(val):
    return f"{s(val):.2f}pt"

def mm(val):
    return f"{val}mm"

def pt(val):
    return f"{val}pt"


# ══════════════════════════════════════════════════════════════
# SECTION 2 — STRUCTURAL COLOURS
# ══════════════════════════════════════════════════════════════
# Fixed colours used across all 5 levels regardless of accent colour.
# Confirmed by finding the SAME hex recurring across independent PDFs
# for the same functional role.

COLOURS = {
    'body_text': {
        'hex':  '#000000',
        'cmyk': 'C0 M0 Y0 K100',
        'role': 'Primary body text, instructions, answers — all levels',
    },
    'audio_ref': {
        'hex':  '#3F3F3F',
        'cmyk': 'C0 M0 Y0 K75 (approx, greyscale)',
        'role': 'CD/audio track references (e.g. "CD1.2") and running-header '
                'footer text — confirmed identical hex in ADV, ELEM, INT, PREINT, UPINT',
    },
    'grey_tab': {
        'hex':  '#E5E5E5',
        'cmyk': 'C0 M0 Y0 K10',
        'role': 'Sidebar section tab background (e.g. vertical "LANGUAGE WORK" '
                'tab in Practice File); generic 10% grey utility fill for '
                'tables/rules — confirmed in ELEM (x133), UPINT (vertical tab)',
    },
    'production_slug': {
        'hex':  '#000000',
        'cmyk': None,
        'role': 'Tiny 5.7pt Helvetica production/imprint code in page gutter '
                '(e.g. "ML_ADV_U1, 03.indd") — not part of the reader-facing design',
    },
}

# NOTE: several one-off "special feature" heading colours were found
# (e.g. #D80000 crimson in ADV's "Decoding the silent signals" box,
# #FF4C0C in PREINT, #2CB2B2 in INT, #00E062 in ELEM) using display
# fonts AvenirLTStd-Heavy / RockwellStd-Bold / DIN-Bold. These vary
# unit-by-unit and are NOT part of the fixed level-accent system —
# they read as editorial/magazine-style feature styling chosen per
# article, not a brand token. Documented here for completeness but
# excluded from COLOURS/PPT_THEME as non-systematic. [VECTOR, unit-local]
EDITORIAL_ACCENTS_OBSERVED = [
    ('ADV',    '#D80000', 'AvenirLTStd-Heavy', '"Decoding the silent signals" box title'),
    ('ELEM',   '#00E062', 'RockwellStd-Bold',  'Business-card mini-graphic accent'),
    ('INT',    '#2CB2B2', 'DIN-Bold',          '"A luxury luggage manufacturer…" intro'),
    ('PREINT', '#FF4C0C', 'DIN-Bold',          '"An international drinks company…" intro'),
    ('UPINT',  '#BFFF7A', 'Impact',            '"The price of success" case-study cover headline (68.26pt, on photo)'),
]


# ══════════════════════════════════════════════════════════════
# SECTION 3 — LEVEL ACCENT COLOURS
# ══════════════════════════════════════════════════════════════
# The colour that changes between levels. Confirmed VECTOR-exact from
# the small (4.7×4.7mm) square activity-letter tag boxes ("A", "B", "C"…)
# which recur dozens of times per book — the single most reliable,
# unambiguous source of the level accent colour. Cross-confirmed against
# the running-header/footer text colour and the MEDIUM-CAPS exercise
# number colour, which match exactly in every file.
#
# Screen hex IS the CMYK→sRGB value here because these are pure flat
# vector fills (not photographic/gradient elements), so the naive
# conversion is reliable — unlike BR2e's photo-blended header bands.

LEVELS = {
    'elem': {
        'name':   'Elementary',
        'cefr':   'A2 (approx.)',
        'hex':    '#E58900',
        'cmyk':   'C0 M40 Y100 K10',
        'desc':   'Orange/amber',
        'bg':     '#FCF2E3',
        'source': 'VECTOR — 4.7×4.7mm tag-box rects (×33) + running header '
                  'text + MetaPlusMedium-Caps exercise numbers, all identical hex',
    },
    'preint': {
        'name':   'Pre-intermediate',
        'cefr':   'B1 (approx.)',
        'hex':    '#00B235',
        'cmyk':   'C100 M0 Y70 K30',
        'desc':   'Green',
        'bg':     '#DEF7E6',
        'source': 'VECTOR — 4.7×4.7mm tag-box rects (×29) + running header '
                  'text + exercise numbers, all identical hex',
    },
    'int': {
        'name':   'Intermediate',
        'cefr':   'B1+ (approx.)',
        'hex':    '#A52142',
        'cmyk':   'C0 M80 Y60 K35',
        'desc':   'Crimson/maroon',
        'bg':     '#F6E2E7',
        'source': 'VECTOR — 4.7×4.7mm tag-box rects (×19) + running header '
                  'text + exercise numbers, all identical hex',
    },
    'upint': {
        'name':   'Upper-intermediate',
        'cefr':   'B2 (approx.)',
        'hex':    '#2B6CD8',
        'cmyk':   'C80 M50 Y0 K15',
        'desc':   'Royal blue — CONFIRMED IDENTICAL to Advanced\'s accent (exact '
                  'same CMYK tuple, not a rounding coincidence; see note below)',
        'bg':     '#E7EEFB',
        'source': 'VECTOR — Course Book sample (Market_Leader_UPINT_-_Course_Book.pdf), '
                  '4.7×4.7mm tag-box rects (×31) + running header text + '
                  'MetaPlusMedium-Caps exercise numbers, all identical hex',
    },
    'adv': {
        'name':   'Advanced',
        'cefr':   'C1 (approx.)',
        'hex':    '#2B6CD8',
        'cmyk':   'C80 M50 Y0 K15',
        'desc':   'Royal blue',
        'bg':     '#E7EEFB',
        'source': 'VECTOR — 4.7×4.7mm tag-box rects (×25) + running header '
                  'text + exercise numbers, all identical hex',
    },
    # Confirmed finding: Upper-Intermediate and Advanced share the exact same
    # accent hex/CMYK — verified by comparing raw (unrounded) CMYK float tuples
    # from the vector layer of both PDFs: (0.8, 0.5, 0.0, 0.15) in both files,
    # and confirmed visually by rendering both unit-opening pages. This is a
    # genuine design choice (adjacent upper levels sharing a colour), not a
    # measurement artefact — Elementary/Pre-int/Intermediate each have a
    # distinct, unique hue, so this parity is specific to Upper-Int/Advanced.
    #
    # All 5 Market Leader levels are now sampled from genuine Course Books.
    # A separate note on the Upper-Intermediate PRACTICE FILE (a different
    # book from the Course Book) is kept below in PRACTICE_FILE_FINDINGS —
    # that section of the series is monochrome by design, which remains a
    # valid and interesting finding in its own right, just not a level-accent
    # data point.
}


# ── Practice File observation (separate from level accents) ────
# The Upper-Intermediate PRACTICE FILE (Market_Leader_UPINT_-__Practice_File.pdf,
# a companion workbook distinct from the Course Book) was found to be printed
# in black + 10% grey only — no saturated tag-box rects anywhere in that PDF,
# only a greyscale ramp (#000000…#FFFFFF) plus a plain #E5E5E5 vertical
# "LANGUAGE WORK" section tab. This is a genuine, confirmed design finding
# about that companion book type, independent of the level accent system
# documented in LEVELS above (which is now sampled from genuine Course Books
# for all 5 levels).
PRACTICE_FILE_FINDINGS = {
    'accent': None,
    'note': 'Practice File / Language Work sections are monochrome by design '
            '(black + #E5E5E5 grey only) — confirmed in the Upper-Intermediate '
            'Practice File sample. Not yet confirmed whether this holds for '
            'Practice Files at other levels. Also uses a smaller big-unit-number '
            'size (45.15pt vs 57.00pt in Course Books) — a distinct, reduced cover '
            'template for this companion book type.',
    'source': 'VECTOR — Market_Leader_UPINT_-__Practice_File.pdf, no saturated '
              'rects found anywhere in the document',
}


# ══════════════════════════════════════════════════════════════
# SECTION 4 — FONTS
# ══════════════════════════════════════════════════════════════
# Exact PostScript names confirmed from vector PDF fontname fields,
# stripped of subset prefixes (e.g. 'AAAAAB+MetaPlusBold-Caps').
# Confirmed identical family choice (Meta + Times) across all 5 levels;
# only the decorative "unit title" display font varies per level (see notes).

FONTS = {
    'sans': {
        'oup':   'Meta (Normal/Bold/Medium × Roman/Italic/Caps)',
        'word':  'Meta (fallback: Segoe UI)',
        'gfont': 'Fira Sans',
        'stack': "'Fira Sans', 'Meta', 'Segoe UI', Arial, sans-serif",
    },
    'body': {
        'oup':   'Times (Roman/Bold/Italic)',
        'word':  'Times New Roman',
        'gfont': 'Tinos',
        'stack': "'Tinos', 'Times New Roman', Times, Georgia, serif",
    },
    'hand': {
        'oup':   'ZemkeHandITC',
        'word':  'Segoe Script (fallback)',
        'gfont': 'Caveat',
        'stack': "'Caveat', 'Segoe Script', cursive",
    },
    # Unit-title / decorative display font — VARIES BY LEVEL, not fixed:
    #   ADV:    (title itself set in MetaPlusMedium-Roman 41.8pt, no separate display face)
    #   ELEM:   RockwellStd-Bold / RockwellStd-Light (slab serif) also present
    #   INT:    DIN-Bold used for feature intro headings
    #   PREINT: Frutiger-Cn / Frutiger-BoldCnIt (condensed) used for feature headings
    #   UPINT (Course Book): DIN-Bold, BetonT-Bold/ExtrBold, Impact, HelveticaNeueLT-Light/Bold
    #           used for case-study/feature headings — same "each level differs" pattern
    #   UPINT (Practice File, companion book — not a level accent source, see
    #           PRACTICE_FILE_FINDINGS): GoudyOldStyleT family (old-style serif) for
    #           reading texts, BellMTBold for the course-advert display heading
    'display_varies_by_level': {
        'note': 'No single fixed display face — each level book draws its editorial '
                'feature headings from a different face (Rockwell / DIN / Frutiger '
                'Condensed / Beton / Impact). Unit titles themselves use the same '
                'MetaPlusMedium-Roman as body sans, just at 42pt.',
    },
}


# ══════════════════════════════════════════════════════════════
# SECTION 5 — TYPE SCALE
# ══════════════════════════════════════════════════════════════
# Values below are Tier A (ADV / INT / UPINT), confirmed VECTOR-exact.
# Tier B (ELEM / PREINT) uses the same roles at a consistent ×1.0101
# scale factor (e.g. 9.02pt → 9.12pt, 10.45pt → 10.56pt, 8.55pt → 8.64pt,
# 13.30pt → 13.44pt) — confirmed across 4+ matched roles, not rounding noise.
#
# Format: (key, role, font_key, weight, size_pt, colour_key, colour_hex, display_px, notes)

TYPE_SCALE = [
    # ── Display ────────────────────────────────────────────────
    ('unit_title',     'Unit title (on photo band)',           'sans', 500, 41.80, None, '#FFFFFF', 46, 'MetaPlusMedium-Roman; ELEM/PREINT ~42.2pt'),  # VECTOR
    ('unit_label',      '"UNIT" label above number',            'sans', 500, 16.15, None, '#FFFFFF', 18, 'MetaPlusMedium-Caps, small-caps tracking'),   # VECTOR
    ('unit_number',     'Big unit number (e.g. "1")',           'sans', 700, 57.00, None, '#FFFFFF', 60, 'MetaPlusBold-Caps; confirmed identical in ADV/INT/UPINT Course Books'), # VECTOR
    ('article_headline','FT-style reading article headline',    'body', 400, 37.05, None, '#000000', 30, "Times-Roman — used for headlines like \"It's not what you know\""), # VECTOR

    # ── Headings ───────────────────────────────────────────────
    ('section_head',    'Unit-part section heading (Networking, Writing:…)', 'sans', 700, 13.30, None, '#000000', 16, 'MetaPlusBold-Roman'),  # VECTOR
    ('box_title',       'Boxed feature title ("Useful language" etc.)', 'sans', 700, 12.35, None, '#FFFFFF', 14, 'MetaPlusBold-Caps, on colour-band fill'), # VECTOR
    ('sidebar_subhead', 'Overview sidebar sub-labels (white on dark)', 'sans', 700, 11.40, None, '#FFFFFF', 13, 'MetaPlusBold-Caps'),  # VECTOR

    # ── Body ───────────────────────────────────────────────────
    ('activity_lead',   'Activity instruction lead-in (bold)',  'sans', 700, 10.45, None, '#000000', 13, 'MetaPlusBold-Roman'),  # VECTOR
    ('handwritten',     'Facsimile handwritten model answer',   'hand', 400, 10.45, None, '#000000', 13, 'ZemkeHandITC — often tinted level-accent colour'), # VECTOR
    ('body_serif',      'Reading article body text',            'body', 400,  9.03, None, '#000000', 12, 'Times-Roman, justified columns'),  # VECTOR
    ('body_sans',       'General body / answer text',           'sans', 400,  9.02, None, '#000000', 12, 'MetaPlusNormal-Roman'),  # VECTOR
    ('body_italic',     'Italicised terms/definitions',         'sans', 400,  9.03, None, '#000000', 12, 'MetaPlusNormal-Italic'),  # VECTOR
    ('accent_letter',   'Lettered sub-items a) b) c)',          'sans', 400,  9.03, 'accent', '#2B6CD8', 12, 'MetaPlusMedium-Roman, level-accent colour (ADV shown; swaps per level)'),  # VECTOR
    ('accent_number',   'Exercise number sequences (1 2 3…)',   'sans', 500,  9.50, 'accent', '#2B6CD8', 13, 'MetaPlusMedium-Caps, level-accent colour (ADV shown; swaps per level)'),  # VECTOR

    # ── Small / labels ─────────────────────────────────────────
    ('running_header',  'Page-top running header ("UNIT 1 •• …")', 'sans', 700,  8.55, 'accent', '#2B6CD8', 11, 'MetaPlusBold-Caps, level-accent colour (ADV shown; swaps per level)'),  # VECTOR
    ('audio_track',     'CD/audio track reference ("CD1.2")',   'sans', 700,  8.55, 'audio', '#3F3F3F', 11, 'MetaPlusBold-Caps, fixed grey — all levels'),  # VECTOR
    ('form_text',       'Letter/e-mail template body',          'sans', 400,  8.08, None, '#000000', 11, 'ArialMT — used for realia/form exercises'),  # VECTOR
    ('table_body',      'Table cell text',                      'sans', 400,  8.55, None, '#000000', 11, 'Helvetica'),  # VECTOR
    ('table_header',    'Table header row',                     'sans', 700,  8.55, None, '#000000', 11, 'Helvetica-Bold'),  # VECTOR
    ('caption',         'Photo caption / credit line',          'body', 700,  8.55, None, '#000000', 11, 'Times-Bold'),  # VECTOR
    ('tiny_scale',      'Tiny numeric scale labels (10 20 30…)', 'sans', 400,  5.26, None, '#000000',  8, 'MetaPlusNormal-Caps'),  # VECTOR
    ('production_slug', 'Production/imprint code (gutter)',     'sans', 400,  5.70, None, '#000000',  8, 'Helvetica — not reader-facing'),  # VECTOR
]


# ══════════════════════════════════════════════════════════════
# SECTION 6 — PAGE GEOMETRY
# ══════════════════════════════════════════════════════════════
# Format: (label, value_mm, axis, note)

GEOMETRY = [
    ('Page width',                    209.90, 'w', 'Confirmed identical all 5 PDFs — effectively A4'),  # VECTOR
    ('Page height',                   297.00, 'h', 'A4'),  # VECTOR
    ('Unit-opening photo band height', 48.20, 'h', 'Full-bleed photo strip behind unit title, ADV measured'),  # VECTOR (ADV)
    ('Unit number block width',        43.70, 'w', 'Dark tag block containing "UNIT" + big number, ADV'),  # VECTOR
    ('Left sidebar column width',      44.20, 'w', 'OVERVIEW sidebar column on unit-opening page'),  # VECTOR
    ('Activity tag box size',           4.70, 'w', 'Square "A" "B" "C" activity-letter tag — same on all levels'),  # VECTOR
    ('Main text column left edge',      68.0, 'w', 'Approximate — body text/activity instructions start position, ADV interior page'),  # VECTOR (approx)
]


# ══════════════════════════════════════════════════════════════
# SECTION 7 — COMPONENT POSITIONS (y from page top)
# ══════════════════════════════════════════════════════════════
# Format: (label, y_top, y_bottom, height, note)

POSITIONS = [
    ('Unit number/title band',   0.0,  36.5,  36.5, 'Photo band + "UNIT 1" + title, ADV measured'),  # VECTOR
    ('Overview sidebar',        36.5, 161.0, 124.5, 'Left column below unit tag, runs down to photo bottom'),  # VECTOR (approx)
    ('First activity tag (A)',  169.5, 174.2,  4.7, 'First "A" tag box top position, ADV'),  # VECTOR
]


# ══════════════════════════════════════════════════════════════
# SECTION 8 — SPACING
# ══════════════════════════════════════════════════════════════

# Format: (role, leading_mm, leading_pt)
LEADING = [
    ('Body/exercise text (generous, workbook-style)', 5.92, 16.78),  # VECTOR — modal gap, ADV pp.7-11
    ('List item spacing (tighter)',                    4.36, 12.36),  # VECTOR — modal gap, ADV
    ('Dense table rows',                                3.52,  9.98),  # VECTOR — modal gap, ADV p.8 table
]

# Format: (from_to, mm_min, mm_max, pt_min, pt_max, note)
GAPS = [
    ('Table row height (5-row response grid)', 9.10, 9.10, 25.80, 25.80, 'ADV p.8 agree/disagree table, VECTOR-measured'),
]

# Format: (label, x_recto, x_verso, note)
X_POSITIONS = [
    ('Activity tag box (A/B/C…)', 55.7, 55.7, 'Constant left position for all activity letters, ADV'),  # VECTOR
    ('Main text column start',    68.2, 68.2, 'Approx. body/instruction text left edge'),  # VECTOR (approx)
]


# ══════════════════════════════════════════════════════════════
# SECTION 9 — RULES AND LINES
# ══════════════════════════════════════════════════════════════
# No systematic rule/border system was found comparable to BR2e's
# 3.9pt teal underlines — Market Leader's sample chapters rely on
# whitespace, tag boxes, and colour-band fills rather than hairline
# rules for section division. Table cell borders exist but were not
# isolated to a stable weight — flagged for future confirmation.

RULES = [
    ('Table cell border', 0.0, 0.0, '#CCCCCC', 'per cell', 'ESTIMATE — not yet isolated to an exact weight'),  # ESTIMATE
]


# ══════════════════════════════════════════════════════════════
# SECTION 10 — WORD STYLE MAP
# ══════════════════════════════════════════════════════════════

WORD_STYLES = [
    ('ML_Unit_Title',       'sans', 500, 41.80, '#FFFFFF', 0,  0, 'On photo band; page break before'),
    ('ML_Section_Head',     'sans', 700, 13.30, '#000000', 20, 8, 'Unit-part heading e.g. "Networking"'),
    ('ML_Box_Title',        'sans', 700, 12.35, '#FFFFFF', 0,  6, 'Shading = level accent colour'),
    ('ML_Body_Text',        'sans', 400,  9.02, '#000000', 0,  8, 'Line spacing ~16.8pt (generous, workbook style)'),
    ('ML_Activity_Lead',    'sans', 700, 10.45, '#000000', 12, 4, 'Bold instruction lead-in after tag box'),
    ('ML_Activity_Tag',     'sans', 700, 10.40, '#FFFFFF', 0,  0, 'White letter on 4.7×4.7mm level-accent square'),
    ('ML_Reading_Body',     'body', 400,  9.03, '#000000', 0,  8, 'Times-Roman justified column, FT-style articles'),
    ('ML_Reading_Headline', 'body', 400, 37.05, '#000000', 0, 10, 'Times-Roman large headline'),
    ('ML_Running_Header',   'sans', 700,  8.55, None,      0,  0, 'Level-accent colour; "UNIT N •• TITLE"'),
    ('ML_Audio_Ref',        'sans', 700,  8.55, '#3F3F3F', 0,  0, 'Fixed grey — CD/audio track number'),
    ('ML_Handwritten',      'hand', 400, 10.45, '#000000', 0,  0, 'Facsimile handwriting for model answers'),
]

CHAR_STYLES = [
    ('ML_Accent_Letter', 'sans', 400, None,      'a) b) c) list markers — level accent colour'),
    ('ML_Accent_Number', 'sans', 500, None,      'Exercise numbers 1 2 3… — level accent colour'),
    ('ML_Bold_Term',     'sans', 700, '#000000', 'Bold key terms within instructions'),
    ('ML_Italic_Term',   'sans', 400, '#000000', 'Italicised technical terms'),
]


# ══════════════════════════════════════════════════════════════
# SECTION 11 — POWERPOINT THEME
# ══════════════════════════════════════════════════════════════

PPT_THEME = {
    'dk1':      '#000000',
    'lt1':      '#FFFFFF',
    'dk2':      '#3F3F3F',   # audio_ref grey — closest fixed dark structural tone
    'lt2':      '#E5E5E5',   # grey_tab
    'accent1':  None,        # level accent — swap per level (see LEVELS)
    'accent2':  '#E58900',   # Elementary orange
    'accent3':  '#00B235',   # Pre-int green
    'accent4':  '#A52142',   # Intermediate crimson
    'accent5':  '#2B6CD8',   # Advanced blue — also Upper-intermediate (identical, confirmed)
    'accent6':  '#3F3F3F',   # audio grey
    'hyperlink':'#2B6CD8',
}

PPT_FONTS = {
    'major': ('Meta Bold',  'Fira Sans',       'Headings, unit titles, labels'),
    'minor': ('Meta',       'Fira Sans',       'Body sans text, activity instructions'),
    'serif': ('Times New Roman', 'Tinos',      'Reading article body + headlines'),
}

PPT_SLIDE_SIZE = (SOURCE_W, SOURCE_H)


# ══════════════════════════════════════════════════════════════
# SECTION 12 — COLOUR TINT FAMILIES
# ══════════════════════════════════════════════════════════════
# No systematic multi-stop tint ramp (like BR2e's amber/teal families)
# was found — each level uses its single flat accent hex plus one very
# light background tint (see LEVELS[*]['bg'], pixel/vector-derived from
# the sidebar/table fills observed near unit-opening content). Market
# Leader's palette is flatter/simpler than BR2e's.

ACCENT_FAMILY = [
    # (hex, cmyk, tint_pct, role) — one entry per level, 100% + bg tint only
    ('#E58900', 'C0 M40 Y100 K10',  100, 'Elementary — full accent'),
    ('#FCF2E3', None,                12, 'Elementary — background tint (approx.)'),
    ('#00B235', 'C100 M0 Y70 K30',  100, 'Pre-intermediate — full accent'),
    ('#DEF7E6', None,                12, 'Pre-intermediate — background tint (approx.)'),
    ('#A52142', 'C0 M80 Y60 K35',   100, 'Intermediate — full accent'),
    ('#F6E2E7', None,                12, 'Intermediate — background tint (approx.)'),
    ('#2B6CD8', 'C80 M50 Y0 K15',   100, 'Upper-intermediate — full accent (identical to Advanced)'),
    ('#E7EEFB', None,                12, 'Upper-intermediate — background tint (approx.)'),
    ('#2B6CD8', 'C80 M50 Y0 K15',   100, 'Advanced — full accent (identical to Upper-intermediate)'),
    ('#E7EEFB', None,                12, 'Advanced — background tint (approx.)'),
]


# ══════════════════════════════════════════════════════════════
# SECTION 13 — PHOTO SPECIFICATIONS
# ══════════════════════════════════════════════════════════════

PHOTOS = [
    {
        'type':     'Unit-opening — full-width banner (tiled)',
        'page':     'Recto (unit opening)',
        'position': 'x≈46mm, y≈0.5mm',
        'size_mm':  '158.7 × 123.0mm (main tile) + smaller strips',
        'pct':      '75.6% W × 41.4% H',
        'dpi':      '~200dpi (estimated from px/mm)',
        'note':     'Split into 3+ image tiles across the header band and right '
                    'photo area — common PDF-export artefact, not a design feature',
    },
    {
        'type':     'Left sidebar photo (profile/interviewee)',
        'page':     'Recto (unit opening, below OVERVIEW list)',
        'position': 'x≈2.4mm, y≈36.7mm',
        'size_mm':  '43.9 × 56.1mm (+ second 43.9×56.1mm tile below)',
        'pct':      '20.9% W × 18.9% H',
        'dpi':      '~200dpi',
        'note':     'Portrait crop of the interviewee/expert used in the listening section',
    },
]


# ══════════════════════════════════════════════════════════════
# SCALED ACCESS HELPERS
# ══════════════════════════════════════════════════════════════

def scaled_type_scale():
    return [
        (key, role, font_key, weight, round(size_pt * SCALE, 2),
         col_key, col_hex, display_px, notes)
        for key, role, font_key, weight, size_pt,
            col_key, col_hex, display_px, notes in TYPE_SCALE
    ]

def scaled_geometry():
    return [
        (label, round(val_mm * SCALE, 2), axis, note)
        for label, val_mm, axis, note in GEOMETRY
    ]

def scaled_positions():
    result = []
    for label, y_top, y_bot, height, note in POSITIONS:
        result.append((
            label,
            round(y_top * SCALE, 2),
            round(y_bot * SCALE, 2) if y_bot is not None else None,
            round(height * SCALE, 2) if height is not None else None,
            note
        ))
    return result

def scaled_gaps():
    return [
        (from_to,
         round(mm_lo * SCALE, 2), round(mm_hi * SCALE, 2),
         round(pt_lo * SCALE, 2), round(pt_hi * SCALE, 2),
         note)
        for from_to, mm_lo, mm_hi, pt_lo, pt_hi, note in GAPS
    ]

def scaled_x_positions():
    return [
        (label,
         round(x_recto * SCALE, 2),
         round(x_verso * SCALE, 2),
         note)
        for label, x_recto, x_verso, note in X_POSITIONS
    ]

def scaled_leading():
    return [
        (role,
         round(lead_mm * SCALE, 2) if lead_mm is not None else None,
         round(lead_pt * SCALE, 2) if lead_pt is not None else None)
        for role, lead_mm, lead_pt in LEADING
    ]

def scaled_word_styles():
    return [
        (name, font_key, weight, round(size_pt * SCALE, 2),
         col_hex, sp_before, sp_after, other)
        for name, font_key, weight, size_pt,
            col_hex, sp_before, sp_after, other in WORD_STYLES
    ]
