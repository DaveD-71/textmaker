# ============================================================
# [TEXTBOOK NAME] Design System — Single Authoritative Data Source
# Publisher: [PUBLISHER NAME]
# Source PDF: [FILENAME.pdf]
# ============================================================
#
# HOW TO USE THIS FILE:
#   1. Replace all [PLACEHOLDER] values with confirmed data
#   2. Mark each value with its source: VECTOR, PIXEL, or ESTIMATE
#   3. Never hardcode values in generate.py — all values come from here
#   4. Run generate.py to produce the HTML style guide
#
# DATA QUALITY MARKERS (use in comments throughout):
#   VECTOR  — exact value from PDF vector layer (most reliable)
#   PIXEL   — pixel-sampled from rendered PDF on screen
#   ESTIMATE — not yet confirmed from source (flag for review)
#
# Version history:
#   1.0  [DATE]  Initial extraction from [PDF FILENAME]
# ============================================================

VERSION      = "1.0"
VERSION_DATE = "[DATE]"
VERSION_NOTE = "Initial extraction"


# ══════════════════════════════════════════════════════════════
# SECTION 1 — PAGE DIMENSIONS
# ══════════════════════════════════════════════════════════════
# Measure from the white background rectangle in the vector PDF,
# NOT from the PDF page size (which may include a promotional wrapper).
# See process guide Phase 1.3 for details.

# ── Source page dimensions (from PDF) ────────────────────────
SOURCE_W = 0.0   # mm — REPLACE with measured content area width  [ESTIMATE]
SOURCE_H = 0.0   # mm — REPLACE with measured content area height [ESTIMATE]

# ── Target page dimensions ────────────────────────────────────
# Set to your target paper size. Scale factor is computed automatically.
TARGET_W = 210.0   # mm — A4 width  (change if using different paper)
TARGET_H = 297.0   # mm — A4 height (change if using different paper)

# ── Scale factor (computed automatically — do not edit) ───────
_scale_w = TARGET_W / SOURCE_W if SOURCE_W > 0 else 1.0
_scale_h = TARGET_H / SOURCE_H if SOURCE_H > 0 else 1.0
SCALE = (_scale_w + _scale_h) / 2   # uniform scale — no distortion

# Working page dimensions at target size
PAGE_W = SOURCE_W * SCALE
PAGE_H = SOURCE_H * SCALE


# ── Helper functions ──────────────────────────────────────────

def pw(mm_val):
    """Percentage of target page width."""
    return f"{mm_val / PAGE_W * 100:.2f}%"

def ph(mm_val):
    """Percentage of target page height."""
    return f"{mm_val / PAGE_H * 100:.2f}%"

def s(val):
    """Apply scale factor to a raw value."""
    return round(val * SCALE, 2)

def smm(val):
    """Scale a mm value and format with suffix."""
    return f"{s(val)}mm"

def spt(val):
    """Scale a pt value and format."""
    return f"{s(val):.2f}pt"

def mm(val):
    """Format mm value with suffix (unscaled)."""
    return f"{val}mm"

def pt(val):
    """Format pt value (unscaled)."""
    return f"{val}pt"


# ══════════════════════════════════════════════════════════════
# SECTION 2 — STRUCTURAL COLOURS
# ══════════════════════════════════════════════════════════════
# These are the fixed colours used across all levels/editions.
# Extract CMYK from vector layer. Screen hex from pixel sampling.
# See process guide Phase 2 for extraction methodology.
#
# IMPORTANT: Do NOT use the naive CMYK→sRGB formula for screen hex.
# Pixel-sample the rendered PDF instead. See process guide Phase 2.3.
#
# Format:
#   'key': {
#       'hex':  '#RRGGBB',  # screen hex — PIXEL sampled
#       'cmyk': 'CX MX YX KX',  # exact from vector — VECTOR
#       'role': 'where this colour appears'
#   }

COLOURS = {
    # ── Primary UI colour (equivalent to BR2e teal) ───────────
    # Replace with the publisher's primary heading/UI colour
    'primary': {
        'hex':  '#000000',   # REPLACE — screen hex [ESTIMATE]
        'cmyk': 'C0 M0 Y0 K100',  # REPLACE — from vector [ESTIMATE]
        'role': '[WHERE USED — e.g. section headings, column headers]',
    },

    # ── Accent colour (equivalent to BR2e amber) ──────────────
    # The secondary highlight colour used for outcomes, labels etc.
    'accent': {
        'hex':  '#000000',   # REPLACE [ESTIMATE]
        'cmyk': 'C0 M0 Y0 K100',  # REPLACE [ESTIMATE]
        'role': '[WHERE USED]',
    },

    # ── Highlight colour (equivalent to BR2e crimson) ─────────
    # Used for special elements like Talking Point titles, crossrefs
    'highlight': {
        'hex':  '#000000',   # REPLACE [ESTIMATE]
        'cmyk': 'C0 M0 Y0 K100',  # REPLACE [ESTIMATE]
        'role': '[WHERE USED]',
    },

    # ── Header band colour ────────────────────────────────────
    'hdr_band': {
        'hex':  '#000000',   # REPLACE [ESTIMATE]
        'cmyk': 'C0 M0 Y0 K100',  # REPLACE [ESTIMATE]
        'role': 'Running header band',
    },

    # ── Dark band colour (Viewpoint/VP equivalent) ────────────
    'dark_band': {
        'hex':  '#000000',   # REPLACE [ESTIMATE]
        'cmyk': 'C0 M0 Y0 K100',  # REPLACE [ESTIMATE]
        'role': '[WHERE USED — e.g. Viewpoint section bands]',
    },

    # Add more structural colours as discovered during extraction
    # Use the BR2e project as a reference for what to look for
}


# ══════════════════════════════════════════════════════════════
# SECTION 3 — LEVEL/EDITION ACCENT COLOURS
# ══════════════════════════════════════════════════════════════
# The colour(s) that change between levels or editions.
# Both CMYK (from vector) and screen hex (pixel-sampled) required.
# See process guide Phase 2.2 and 2.3.
#
# Find the back cover / product listing page — it typically shows
# all levels together as large flat colour blocks, which is the
# best source for accurate colour extraction.

LEVELS = {
    # Template entry — replace with actual levels/editions
    'level_1': {
        'name':   '[LEVEL NAME e.g. Starter]',
        'cefr':   '[CEFR e.g. A1]',        # or equivalent descriptor
        'hex':    '#000000',                 # screen hex — PIXEL [ESTIMATE]
        'cmyk':   'C0 M0 Y0 K100',          # from vector — VECTOR [ESTIMATE]
        'desc':   '[COLOUR DESCRIPTION]',
        'bg':     '#FFFFFF',                 # background tint if any [ESTIMATE]
        'source': '[HOW CONFIRMED e.g. pixel-sampled from cover page]',
    },
    'level_2': {
        'name':   '[LEVEL NAME]',
        'cefr':   '[CEFR]',
        'hex':    '#000000',                 # [ESTIMATE]
        'cmyk':   'C0 M0 Y0 K100',          # [ESTIMATE]
        'desc':   '[COLOUR DESCRIPTION]',
        'bg':     '#FFFFFF',
        'source': '[HOW CONFIRMED]',
    },
    # Add more levels as needed
}


# ══════════════════════════════════════════════════════════════
# SECTION 4 — FONTS
# ══════════════════════════════════════════════════════════════
# OUP font names confirmed from vector PDF fontname fields.
# Google Fonts alternatives for free use in Word/CSS/PPT.
# See process guide Phase 3.1.
#
# To find fonts: check char['fontname'] values in the vector PDF.
# Strip any subset prefix (e.g. 'ABCDEF+NewsGothicMTStd-Bold' → 'NewsGothicMTStd-Bold')

FONTS = {
    'body': {
        'oup':   '[OUP BODY FONT e.g. PalatinoLTStd-Roman]',  # VECTOR [ESTIMATE]
        'word':  '[WORD NAME e.g. Palatino Linotype]',
        'gfont': '[GOOGLE FONT e.g. Lora]',
        'stack': "'[Google Font]', '[Word Font]', Georgia, serif",
    },
    'sans': {
        'oup':   '[OUP SANS FONT e.g. NewsGothicMTStd]',     # VECTOR [ESTIMATE]
        'word':  '[WORD NAME e.g. News Gothic MT]',
        'gfont': '[GOOGLE FONT e.g. Barlow Condensed]',
        'stack': "'[Google Font]', '[Word Font]', Arial, sans-serif",
    },
    # Add 'slab', 'display' etc. if publisher uses additional font families
    # Common in ELT: a slab serif for special sections (e.g. Caecilia)
}


# ══════════════════════════════════════════════════════════════
# SECTION 5 — TYPE SCALE
# ══════════════════════════════════════════════════════════════
# All sizes exact from vector PDF char['size'] field.
# NEVER use rounded values — use exact decimal values.
# See process guide Phase 3.4 for common rounding errors.
#
# Format: (key, role, font_key, weight, size_pt, colour_key, colour_hex, display_px, notes)
#   key:        unique identifier (snake_case)
#   role:       human-readable description
#   font_key:   key from FONTS dict above
#   weight:     400 (regular), 500 (medium), 700 (bold)
#   size_pt:    exact size from vector PDF — VECTOR
#   colour_key: key from COLOURS dict (or None for black/white)
#   colour_hex: hex value (redundant but useful for direct access)
#   display_px: enlarged size for HTML specimen display (~1.8× print)
#   notes:      additional context

TYPE_SCALE = [
    # ── Display / heading sizes ───────────────────────────────
    # (largest first — confirm each from vector PDF)
    ('heading_lg',   '[LARGE HEADING ROLE]',    'sans', 700,  0.00, None, '#000000', 28, '[NOTES]'),  # ESTIMATE
    ('heading_md',   '[MEDIUM HEADING ROLE]',   'sans', 700,  0.00, None, '#000000', 22, '[NOTES]'),  # ESTIMATE
    ('heading_sm',   '[SMALL HEADING ROLE]',    'sans', 700,  0.00, None, '#000000', 16, '[NOTES]'),  # ESTIMATE

    # ── UI / label sizes ──────────────────────────────────────
    ('label_lg',     '[LARGE LABEL ROLE]',      'sans', 700,  0.00, None, '#000000', 14, '[NOTES]'),  # ESTIMATE
    ('label_sm',     '[SMALL LABEL ROLE]',      'sans', 400,  0.00, None, '#000000', 13, '[NOTES]'),  # ESTIMATE

    # ── Body text sizes ───────────────────────────────────────
    ('body',         'Body / reading text',     'body', 400,  0.00, None, '#000000', 14, '[NOTES]'),  # ESTIMATE
    ('body_bold',    'Body bold',               'body', 700,  0.00, None, '#000000', 14, '[NOTES]'),  # ESTIMATE
    ('body_italic',  'Body italic',             'body', 400,  0.00, None, '#000000', 14, '[NOTES]'),  # ESTIMATE

    # ── Small / contents sizes ────────────────────────────────
    ('small',        '[SMALL TEXT ROLE]',       'sans', 400,  0.00, None, '#000000', 12, '[NOTES]'),  # ESTIMATE
]


# ══════════════════════════════════════════════════════════════
# SECTION 6 — PAGE GEOMETRY
# ══════════════════════════════════════════════════════════════
# Measurements from vector PDF coordinates (converted to mm).
# See process guide Phase 4.
#
# Format: (label, value_mm, axis, note)
#   axis: 'w' (width dimension) or 'h' (height dimension)

GEOMETRY = [
    # Replace with actual measurements from the vector PDF
    ('[COMPONENT NAME]', 0.0, 'h', '[POSITION OR SIZE DESCRIPTION]'),  # ESTIMATE
    ('[COMPONENT NAME]', 0.0, 'w', '[POSITION OR SIZE DESCRIPTION]'),  # ESTIMATE
]


# ══════════════════════════════════════════════════════════════
# SECTION 7 — COMPONENT POSITIONS (y from content top)
# ══════════════════════════════════════════════════════════════
# Format: (label, y_top, y_bottom, height, note)
# Use None for y_bottom and height if only y_top is known (position-only).
# IMPORTANT: Distinguish positions from heights — see process guide Phase 4.3.

POSITIONS = [
    # (label, y_top, y_bottom, height, note)
    ('[COMPONENT]', 0.0, 0.0, 0.0, '[NOTE]'),  # ESTIMATE
]


# ══════════════════════════════════════════════════════════════
# SECTION 8 — SPACING
# ══════════════════════════════════════════════════════════════

# Line spacing (leading)
# Format: (role, leading_mm, leading_pt)
LEADING = [
    ('[BODY TEXT ROLE]', 0.0, 0.0),   # ESTIMATE — measure from consecutive y-positions
]

# Component gaps (vertical space between elements)
# Format: (from_to, mm_min, mm_max, pt_min, pt_max, note)
GAPS = [
    ('[FROM] → [TO]', 0.0, 0.0, 0.0, 0.0, '[NOTE]'),  # ESTIMATE
]

# X positions (horizontal text positions, content-relative)
# Format: (label, x_recto, x_verso, note)
X_POSITIONS = [
    ('[ELEMENT]', 0.0, 0.0, '[NOTE]'),  # ESTIMATE
]


# ══════════════════════════════════════════════════════════════
# SECTION 9 — RULES AND LINES
# ══════════════════════════════════════════════════════════════
# Format: (label, weight_pt, weight_mm, colour_hex, span, location)

RULES = [
    ('[RULE NAME]', 0.0, 0.0, '#000000', '[SPAN]', '[LOCATION]'),  # ESTIMATE
]


# ══════════════════════════════════════════════════════════════
# SECTION 10 — WORD STYLE MAP
# ══════════════════════════════════════════════════════════════
# Format: (name, font_key, weight, size_pt, colour_hex,
#          space_before, space_after, other)
# All size_pt values must match TYPE_SCALE exactly.

WORD_STYLES = [
    # Paragraph styles
    ('[STYLE_NAME]', 'sans', 700, 0.00, '#000000', 0, 0, '[NOTES]'),  # ESTIMATE
    ('[STYLE_NAME]', 'body', 400, 0.00, '#000000', 0, 8, 'Line spacing exactly [X]pt'),  # ESTIMATE
]

CHAR_STYLES = [
    # Character styles
    ('[STYLE_NAME]', 'body', 700, '#000000', '[USAGE]'),  # ESTIMATE
]


# ══════════════════════════════════════════════════════════════
# SECTION 11 — POWERPOINT THEME
# ══════════════════════════════════════════════════════════════

PPT_THEME = {
    'dk1':      '#000000',
    'lt1':      '#FFFFFF',
    'dk2':      '#000000',   # REPLACE [ESTIMATE]
    'lt2':      '#FFFFFF',   # REPLACE [ESTIMATE]
    'accent1':  None,        # level/edition accent — swap as needed
    'accent2':  '#000000',   # REPLACE [ESTIMATE]
    'accent3':  '#000000',   # REPLACE [ESTIMATE]
    'accent4':  '#000000',   # REPLACE [ESTIMATE]
    'accent5':  '#000000',   # REPLACE [ESTIMATE]
    'accent6':  '#000000',   # REPLACE [ESTIMATE]
    'hyperlink':'#000000',   # REPLACE [ESTIMATE]
}

PPT_FONTS = {
    'major': ('[OUP FONT]', '[GOOGLE FONT]', 'Headings and labels'),
    'minor': ('[OUP FONT]', '[GOOGLE FONT]', 'Body text'),
}

PPT_SLIDE_SIZE = (SOURCE_W, SOURCE_H)  # use source dimensions for print masters


# ══════════════════════════════════════════════════════════════
# SECTION 12 — COLOUR TINT FAMILIES
# ══════════════════════════════════════════════════════════════
# If the publisher uses a systematic tint scale (like BR2e's amber/teal families),
# document it here. Format matches BR2e: (hex, cmyk, tint_pct, role)

PRIMARY_FAMILY = [
    # ('#RRGGBB', 'CX MX YX KX', tint_percent, 'role'),
    # Add entries from darkest to lightest
]

ACCENT_FAMILY = [
    # ('#RRGGBB', 'CX MX YX KX', tint_percent, 'role'),
]


# ══════════════════════════════════════════════════════════════
# SECTION 13 — PHOTO SPECIFICATIONS
# ══════════════════════════════════════════════════════════════
# Document photo placement, sizing, and DPI from the vector PDF.

PHOTOS = [
    {
        'type':     '[PHOTO TYPE e.g. Unit opening banner]',
        'page':     '[PAGE TYPE]',
        'position': '[x=Xmm, y=Ymm]',
        'size_mm':  '[W × H mm]',
        'pct':      '[W% × H%]',
        'dpi':      '[~X dpi]',
        'note':     '[NOTES]',
    },
]


# ══════════════════════════════════════════════════════════════
# SCALED ACCESS HELPERS
# ══════════════════════════════════════════════════════════════
# Use these in generate.py instead of accessing TYPE_SCALE etc. directly.
# All values are automatically scaled from source to target dimensions.

def scaled_type_scale():
    """TYPE_SCALE with sizes scaled to target page dimensions."""
    return [
        (key, role, font_key, weight, round(size_pt * SCALE, 2),
         col_key, col_hex, display_px, notes)
        for key, role, font_key, weight, size_pt,
            col_key, col_hex, display_px, notes in TYPE_SCALE
    ]

def scaled_geometry():
    """GEOMETRY with mm values scaled to target page dimensions."""
    return [
        (label, round(val_mm * SCALE, 2), axis, note)
        for label, val_mm, axis, note in GEOMETRY
    ]

def scaled_positions():
    """POSITIONS with mm values scaled to target page dimensions."""
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
    """GAPS with mm values scaled to target page dimensions."""
    return [
        (from_to,
         round(mm_lo * SCALE, 2), round(mm_hi * SCALE, 2),
         round(pt_lo * SCALE, 2), round(pt_hi * SCALE, 2),
         note)
        for from_to, mm_lo, mm_hi, pt_lo, pt_hi, note in GAPS
    ]

def scaled_x_positions():
    """X_POSITIONS with mm values scaled to target page dimensions."""
    return [
        (label,
         round(x_recto * SCALE, 2),
         round(x_verso * SCALE, 2),
         note)
        for label, x_recto, x_verso, note in X_POSITIONS
    ]

def scaled_leading():
    """LEADING with mm/pt values scaled to target page dimensions."""
    return [
        (role,
         round(lead_mm * SCALE, 2) if lead_mm is not None else None,
         round(lead_pt * SCALE, 2) if lead_pt is not None else None)
        for role, lead_mm, lead_pt in LEADING
    ]

def scaled_word_styles():
    """WORD_STYLES with point sizes scaled to target page dimensions."""
    return [
        (name, font_key, weight, round(size_pt * SCALE, 2),
         col_hex, sp_before, sp_after, other)
        for name, font_key, weight, size_pt,
            col_hex, sp_before, sp_after, other in WORD_STYLES
    ]
