# Publisher Design System Extraction — Process Guide

A methodology for reverse-engineering a complete, accurate design system
from a commercially published textbook PDF.

Developed through the BR2e (Oxford University Press Business Result 2nd Edition)
project. All lessons learned are documented here as a reusable process.

---

## Overview

The goal is to extract every typographic, colour, spacing, and layout value
from a publisher's PDF with sufficient accuracy and confidence to reproduce
the design system in Word, CSS, and PowerPoint. The output is a Python data
file (`data.py`) containing all confirmed values, and a generator script
(`generate.py`) that produces a complete HTML style guide from that data.

---

## Phase 1 — Source File Assessment

### 1.1 Identify the best available PDF

Not all PDFs are equal. In order of preference:

1. **Native vector PDF** (e.g. exported directly from InDesign) — font names,
   exact point sizes, exact CMYK values, and precise coordinates are all
   embedded in the file and readable programmatically. This is the gold standard.
2. **High-resolution raster scan** — fonts and sizes must be estimated visually;
   colours are unreliable. Use only as a supplement.
3. **Low-resolution scan** — largely unusable for precision extraction.

Check the PDF type before starting:
```python
import pdfplumber
with pdfplumber.open('file.pdf') as pdf:
    page = pdf.pages[0]
    chars = page.chars
    print(chars[0])  # if fontname and size are present, it's vector
```

If `fontname` and `size` fields are populated, you have a vector PDF.
If `chars` is empty or contains only image objects, it's a scanned raster.

### 1.2 Identify the most information-rich pages

Not all pages are equally useful:
- **Unit opening pages** — show the full structural layout, header band, unit
  number block, accent stripe, photo, and Starting Point box
- **Interior activity pages** — show body text, section headings, activity
  numbering, crossrefs, Key Expressions sidebar
- **Contents table** — shows the complete typographic hierarchy at small sizes
- **Back cover / product listing page** — often shows all level accent colours
  as large flat vector rectangles — the best source for colour data
- **Talking Point / special section pages** — show slab serif font and
  two-column layout variants

Prioritise pages that show each component at its largest and clearest.

### 1.3 Check for a promotional wrapper

OUP and some other publishers wrap sample PDFs in an A4 promotional shell.
The actual book trim size sits inside this wrapper. Always measure the content
area rectangle, not the wrapper dimensions.

```python
# Find the white background rectangle that defines the content area
for r in page.rects:
    fill = r.get('non_stroking_color')
    # Look for large white rects — these define the content boundary
```

---

## Phase 2 — Colour Extraction

### 2.1 Extract structural colours from vector layer

For vector PDFs, colours are stored as exact CMYK tuples on rect and char objects.
Convert CMYK to hex for display:

```python
def cmyk_to_hex(c, m, y, k):
    r = round((1 - c) * (1 - k) * 255)
    g = round((1 - m) * (1 - k) * 255)
    b = round((1 - y) * (1 - k) * 255)
    return f"#{r:02X}{g:02X}{b:02X}"
```

Extract from rects:
```python
for r in page.rects:
    fill = r.get('non_stroking_color')
    if isinstance(fill, tuple) and len(fill) == 4:
        hex_v = cmyk_to_hex(*fill)
        # Record: hex, CMYK, position, dimensions
```

### 2.2 Identify the level accent colour system

Most ELT publishers use a level-differentiated colour system where one colour
(or family) changes between levels while all others remain fixed.

- Look for the back cover / product listing page — it typically shows all
  levels together as large flat colour blocks
- Extract the CMYK values from the vector rects on that page
- Cross-check: the same colour should appear on the unit opening page as the
  accent stripe and/or header band

### 2.3 CRITICAL — naive CMYK→sRGB is not screen-accurate

The mathematical formula `R=(1-C)(1-K)×255` gives a theoretically correct
but screen-inaccurate result. The reason: PDF viewers (iOS, macOS, Acrobat)
apply an ICC colour profile (typically Fogra39 for European print) when
rendering CMYK to screen. This produces:
- Significantly different hues (up to 30° shift observed)
- Lower saturation
- Different lightness

**The CMYK values are correct for print. They are not correct for screen.**

For screen-accurate hex values, pixel-sample the rendered PDF directly:

```python
from PIL import Image
import numpy as np

# Render the PDF page to an image (use a PDF viewer screenshot)
# Sample the solid colour area with most-saturated pixels
img = Image.open('screenshot.png').convert('RGB')
arr = np.array(img)
# ... sample the relevant region
```

**Best sampling sources (in order of reliability):**
1. Large flat vector-filled rectangles rendered on screen (most reliable)
2. Large title text at full size with no background bleed
3. Thumbnail book covers (unreliable — photos mix with the accent band)

**Document both values:**
- CMYK: from the vector layer (for print)
- Screen hex: from pixel sampling (for digital/screen use)

The screen hex is the **primary authority** for digital work.
The naive formula value should **not** be used.

### 2.4 Verify colours across multiple sources

A colour is confirmed when it appears consistently in:
- The vector layer CMYK
- The pixel-sampled screen render
- Multiple page locations

Note any discrepancies and explain them (compression artefacts, JPEG blending,
ICC rendering, etc.).

---

## Phase 3 — Typography Extraction

### 3.1 Extract exact font names and sizes from vector layer

This is the most reliable part of vector PDF extraction. Every character object
carries its exact fontname and size as specified in InDesign:

```python
for char in page.chars:
    fontname = char.get('fontname', '')  # e.g. 'NewsGothicMTStd-Bold'
    size = float(char.get('size', 0))   # exact pt value e.g. 11.64
    colour = char.get('non_stroking_color')
```

**Critical warning:** Early versions of this project incorrectly identified
fonts as Helvetica from OCR of greyscale scans. Always use the vector
`fontname` field — never OCR or visual estimation.

### 3.2 Group by font + size + colour combination

Each unique (fontname, size, colour) combination typically represents one
typographic role. Build a complete inventory:

```python
from collections import defaultdict
combos = defaultdict(lambda: {'count': 0, 'sample': ''})
for char in page.chars:
    key = (char['fontname'], round(char['size'], 2), colour_hex(char))
    combos[key]['count'] += 1
    combos[key]['sample'] += char.get('text', '')
```

Sort by frequency to identify the most-used roles first.

### 3.3 Identify roles from context

Use position, colour, and surrounding content to assign each combo a role:
- High y-position + white + large = running header
- Teal + bold + medium size = section heading
- Body-width + serif + small = reading text
- Sidebar-width + sans + very small = Key Expressions

### 3.4 Confirm exact sizes — never round

The vector layer gives sizes to two decimal places (e.g. 11.64pt, not 11.6pt).
Always use the exact value. Rounded values introduce inconsistencies when the
same value appears in multiple locations.

Common rounding errors found in this project:
- 11.6pt instead of 11.64pt
- 10.8pt instead of 10.81pt
- 9.1pt instead of 9.15pt
- 8.7pt instead of 8.73pt
- 8.1pt instead of 8.11pt
- 7.5pt instead of 7.48pt
- 7.1pt instead of 7.07pt

---

## Phase 4 — Layout and Spacing Extraction

### 4.1 Measure from vector coordinates

Every text character and rectangle has exact x/y coordinates in the PDF.
Convert from points to mm:

```python
PT_TO_MM = 25.4 / 72

x_mm = float(char['x0']) * PT_TO_MM
y_mm = float(char['top']) * PT_TO_MM
```

Apply the wrapper offset if the content area is inset from the PDF page edge.

### 4.2 Measure line spacing from consecutive y-positions

Leading is the distance between baseline of one line and baseline of the next.
Measure from the `top` values of consecutive characters on consecutive lines:

```python
# Sort chars by y-position, group into lines, measure gaps
leading_mm = y_line2 - y_line1  # in mm
leading_pt = leading_mm / 25.4 * 72
```

### 4.3 Distinguish positions from sizes

A common error: labelling a y-position as a height percentage.
- A **height** is the physical size of a component (e.g. sidebar = 48.2mm tall)
- A **position** is where something sits (e.g. section heading is at y=16.5mm)

Heights → express as "X% of page height"
Positions → express as "X% from top" (not "X% height")

### 4.4 Document recto vs verso separately

Many measurements differ between right-hand (recto) and left-hand (verso) pages
due to the gutter margin. Always note which page orientation a measurement
comes from, and confirm whether it applies to both.

---

## Phase 5 — Data File Construction

### 5.1 Single source of truth principle

Every confirmed value lives in `data.py` exactly once. No value should
ever be hardcoded in the generator. If a font size appears in five places
in the style guide output, all five read from the same dict entry.

### 5.2 Separate source values from scaled output

Store original source values (from the PDF) in the data file.
Apply scaling at read time via helper functions. Never overwrite source values.

```python
SOURCE_W = 174.6  # original PDF content width
TARGET_W = 210.0  # your target page width
SCALE = TARGET_W / SOURCE_W  # computed automatically

def scaled_type_scale():
    return [(key, role, font, weight, round(size * SCALE, 2), ...)
            for key, role, font, weight, size, ... in TYPE_SCALE]
```

### 5.3 Version every change

Add a version history comment block at the top of `data.py`.
Record what changed and when. This makes it possible to trace where
any value came from and when it was confirmed or corrected.

---

## Phase 6 — Verification and Audit

### 6.1 Audit every section independently

Do not assume that fixing a value in one location fixes it everywhere.
Audit each of these locations separately:
- Type scale table
- Type specimens
- Component notes/descriptions
- Word style map
- CSS reference / design tokens
- PowerPoint notes
- Any prose descriptions

### 6.2 Check for forbidden/stale values

After any correction, search the entire output for old values:
```python
forbidden = ['11.6pt', '10.8pt', '9.1pt', '#CDA900']  # examples
for val in forbidden:
    count = html.count(val)
    if count > 0:
        print(f"Still present: {val} ×{count}")
```

### 6.3 Check position vs height labelling

Scan all percentage values in measurement tables:
- Any row with no y_bottom should say "X% from top" not "X% height"
- Any row with a known height should say "X% height"

### 6.4 Regenerate and visually inspect

After every fix pass, regenerate the HTML guide and visually check:
- Do the colour swatches look right?
- Do the type specimens render at legible sizes?
- Are the component demos using the correct colours?
- Does the navigation work?
- Are there any visible HTML tag remnants (broken markup)?

---

## Phase 7 — Common Errors and How to Avoid Them

| Error | Cause | Fix |
|-------|-------|-----|
| Wrong font identified | Using OCR on scanned PDF | Always use vector `fontname` field |
| Rounded sizes | Manual transcription | Use exact values from `char['size']` |
| Swapped level colours | Guessing from thumbnails | Extract from vector rects on product page |
| Naive sRGB used for screen | Assuming formula = render | Pixel-sample the rendered PDF |
| Position labelled as height | Inconsistent terminology | Distinguish y_top from height |
| Value correct in one place, wrong in another | Manual edits | Single source of truth in data.py |
| Columns shifted in tables | HTML structure error | Audit table row cell counts |
| A4 vs source page confusion | Not separating source/target | Use SOURCE_W/TARGET_W separately |
| Colour confusion between levels | Too many similar hex values | Use pixel-sampled values only; remove naive |

---

## Appendix — Useful Code Patterns

### Extract all unique font combos from a page
```python
import pdfplumber
from collections import defaultdict

def colour_hex(col):
    if col is None: return '#000000'
    if len(col) == 4:
        c,m,y,k = col
        return f"#{int((1-c)*(1-k)*255):02X}{int((1-m)*(1-k)*255):02X}{int((1-y)*(1-k)*255):02X}"
    if len(col) == 3:
        return f"#{int(col[0]*255):02X}{int(col[1]*255):02X}{int(col[2]*255):02X}"
    return '#000000'

with pdfplumber.open('file.pdf') as pdf:
    combos = defaultdict(lambda: {'count':0,'sample':''})
    for page in pdf.pages[7:15]:  # unit pages
        for c in page.chars:
            fn = str(c.get('fontname','')).split('+')[-1]
            sz = round(float(c.get('size',0)), 2)
            col = colour_hex(c.get('non_stroking_color'))
            key = (fn, sz, col)
            combos[key]['count'] += 1
            combos[key]['sample'] += c.get('text','')

    for (fn, sz, col), data in sorted(combos.items(), key=lambda x: -x[1]['count']):
        if data['count'] > 10:
            print(f"{fn}  {sz}pt  {col}  ×{data['count']}  '{data['sample'][:30]}'")
```

### Extract all coloured rects from a page
```python
with pdfplumber.open('file.pdf') as pdf:
    page = pdf.pages[15]  # back cover
    PT = 25.4/72
    for r in sorted(page.rects, key=lambda x: float(x['top'])):
        fill = r.get('non_stroking_color')
        if not fill: continue
        w = (float(r['x1'])-float(r['x0']))*PT
        h = (float(r['bottom'])-float(r['top']))*PT
        if w < 10 or h < 3: continue
        if isinstance(fill, tuple) and len(fill)==4:
            c,m,y,k = fill
            hex_v = f"#{int((1-c)*(1-k)*255):02X}{int((1-m)*(1-k)*255):02X}{int((1-y)*(1-k)*255):02X}"
            print(f"{hex_v}  C{c:.2f} M{m:.2f} Y{y:.2f} K{k:.2f}  {w:.1f}×{h:.1f}mm")
```

### Pixel-sample a rendered colour from a screenshot
```python
from PIL import Image
import numpy as np
import colorsys

img = Image.open('screenshot.png').convert('RGB')
arr = np.array(img)

# Define the region of interest (in pixels)
region = arr[y1:y2, x1:x2]
flat = region.reshape(-1, 3).astype(int)

# Get most-saturated pixels (top 2%)
sat = flat.max(axis=1) - flat.min(axis=1)
threshold = np.percentile(sat, 98)
top_pixels = flat[sat >= threshold]

median = np.median(top_pixels, axis=0).astype(int)
r, g, b = median
hex_v = f"#{r:02X}{g:02X}{b:02X}"
h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
print(f"{hex_v}  H={h*360:.0f}° S={s:.2f} V={v:.2f}")
```

---

*This document should be added to the project knowledge of any new
textbook design extraction project alongside the template scripts.*
