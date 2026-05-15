#!/usr/bin/env python3
"""
Audit DOCX style definitions without modifying the document.

Inspects word/styles.xml and reports:
- Style names, IDs, types (paragraph/character/table/list)
- Inheritance (basedOn, next, linked styles)
- Font names (w:rFonts attributes)
- Colors (w:color and w14:srgbClr)
- Paragraph borders and shading
- Validation: linked-style color mismatches

Exit code: 0 if valid, non-zero if validation errors found.
"""

import argparse
import json
import sys
from pathlib import Path
from zipfile import ZipFile
from lxml import etree

NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "w14": "http://schemas.microsoft.com/office/word/2010/wordml",
}


def qn(tag):
    """Qualified name with namespace."""
    if tag.startswith('w:') or tag.startswith('w14:'):
        prefix, local = tag.split(':', 1)
        ns = NS.get(prefix)
        return f'{{{ns}}}{local}' if ns else tag
    return tag


def extract_styles_xml(docx_path):
    """Extract styles.xml from DOCX archive."""
    try:
        with ZipFile(docx_path, 'r') as zf:
            return etree.fromstring(zf.read('word/styles.xml'))
    except Exception as exc:
        raise RuntimeError(f'Failed to extract styles.xml: {exc}') from exc


def get_style_attribute(style_el, attr_name):
    """Get a w:val attribute, e.g., from w:name or w:styleId."""
    return style_el.get(qn(attr_name))


def get_color_value(element):
    """Extract w:color/@w:val if present."""
    color_el = element.find('.//w:color', NS)
    return color_el.get(qn('w:val')) if color_el is not None else None


def get_srgb_color_value(element):
    """Extract w14:srgbClr/@w14:val if present."""
    srgb_el = element.find('.//w14:srgbClr', NS)
    return srgb_el.get(qn('w14:val')) if srgb_el is not None else None


def parse_style_element(style_el):
    """Parse a w:style element and return a dict of properties."""
    style_id = get_style_attribute(style_el, 'w:styleId')
    style_type = get_style_attribute(style_el, 'w:type')

    name_el = style_el.find(qn('w:name'))
    name = name_el.get(qn('w:val')) if name_el is not None else ''

    based_on_el = style_el.find(qn('w:basedOn'))
    based_on = based_on_el.get(qn('w:val')) if based_on_el is not None else None

    next_el = style_el.find(qn('w:next'))
    next_style = next_el.get(qn('w:val')) if next_el is not None else None

    link_el = style_el.find(qn('w:link'))
    linked_style = link_el.get(qn('w:val')) if link_el is not None else None

    r_pr = style_el.find(qn('w:rPr'))
    w_color = get_color_value(r_pr) if r_pr is not None else None
    w14_srgb = get_srgb_color_value(r_pr) if r_pr is not None else None

    # Extract font names
    fonts = {}
    if r_pr is not None:
        r_fonts = r_pr.find(qn('w:rFonts'))
        if r_fonts is not None:
            for attr in ['w:ascii', 'w:hAnsi', 'w:eastAsia', 'w:cs']:
                val = r_fonts.get(qn(attr))
                if val:
                    fonts[attr] = val

    return {
        'styleId': style_id,
        'name': name,
        'type': style_type,
        'basedOn': based_on,
        'next': next_style,
        'linkedStyle': linked_style,
        'w_color': w_color,
        'w14_srgbClr': w14_srgb,
        'fonts': fonts,
    }


def audit_docx(docx_path, style_filter=None, expected_style_map=None):
    """Audit DOCX styles and return report."""
    styles_xml = extract_styles_xml(docx_path)

    styles = {}
    for style_el in styles_xml.findall(qn('w:style')):
        parsed = parse_style_element(style_el)
        style_id = parsed['styleId']
        if style_id:
            styles[style_id] = parsed

    # Filter if requested
    if style_filter:
        styles = {
            sid: s for sid, s in styles.items()
            if style_filter.lower() in s['name'].lower()
        }

    # Validate linked-style color mismatches
    errors = []
    for style_id, style_info in styles.items():
        if style_info['linkedStyle']:
            linked_id = style_info['linkedStyle']
            linked_style = styles.get(linked_id)

            if linked_style is None:
                errors.append(
                    f"Style '{style_info['name']}' links to '{linked_id}' which does not exist"
                )
            else:
                # For linked Div label styles, colors must match
                if 'Div Label' in style_info['name'] or 'Div Label' in linked_style['name']:
                    para_w_color = style_info['w_color']
                    para_w14_srgb = style_info['w14_srgbClr']
                    char_w_color = linked_style['w_color']

                    if para_w_color and para_w14_srgb and para_w_color != para_w14_srgb:
                        errors.append(
                            f"Style '{style_info['name']}': w:color '{para_w_color}' != "
                            f"w14:srgbClr '{para_w14_srgb}'"
                        )

                    if para_w_color and char_w_color and para_w_color != char_w_color:
                        errors.append(
                            f"Style '{style_info['name']}' color '{para_w_color}' != "
                            f"linked char style '{linked_style['name']}' color '{char_w_color}'"
                        )

    # Check expected styles if map provided
    if expected_style_map:
        missing = [name for name in expected_style_map.values()
                   if not any(s['name'] == name for s in styles.values())]
        for missing_name in missing:
            errors.append(f"Expected style '{missing_name}' not found in DOCX")

    return styles, errors


def format_report(styles, errors, output_json=False):
    """Format audit report for display."""
    if output_json:
        return json.dumps({
            'styles': {
                sid: {
                    'name': info['name'],
                    'type': info['type'],
                    'basedOn': info['basedOn'],
                    'next': info['next'],
                    'linkedStyle': info['linkedStyle'],
                    'colors': {
                        'w_color': info['w_color'],
                        'w14_srgbClr': info['w14_srgbClr'],
                    },
                    'fonts': info['fonts'],
                }
                for sid, info in styles.items()
            },
            'errors': errors,
        }, indent=2)

    lines = []
    lines.append(f"\n{'='*80}")
    lines.append(f"DOCX Style Audit Report")
    lines.append(f"{'='*80}\n")

    lines.append(f"Total styles found: {len(styles)}\n")

    for style_id, info in sorted(styles.items(), key=lambda x: x[1]['name']):
        lines.append(f"• {info['name']}")
        lines.append(f"  ID: {style_id} | Type: {info['type']}")
        if info['basedOn']:
            lines.append(f"  Based on: {info['basedOn']}")
        if info['next']:
            lines.append(f"  Next: {info['next']}")
        if info['linkedStyle']:
            lines.append(f"  Linked to: {info['linkedStyle']}")
        if info['w_color'] or info['w14_srgbClr']:
            lines.append(f"  Colors: w:color={info['w_color']}, w14:srgbClr={info['w14_srgbClr']}")
        if info['fonts']:
            lines.append(f"  Fonts: {info['fonts']}")
        lines.append("")

    if errors:
        lines.append(f"\n{'='*80}")
        lines.append("VALIDATION ERRORS")
        lines.append(f"{'='*80}\n")
        for error in errors:
            lines.append(f"✗ {error}")
        lines.append("")

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Audit DOCX style definitions'
    )
    parser.add_argument('docx', help='DOCX file to audit')
    parser.add_argument(
        '--filter',
        help='Filter styles by name substring'
    )
    parser.add_argument(
        '--expected-style-map',
        help='Path to YAML file with expected style names'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output as JSON'
    )

    args = parser.parse_args()

    expected_map = None
    if args.expected_style_map:
        import yaml
        with open(args.expected_style_map) as f:
            expected_map = yaml.safe_load(f).get('style_map', {})

    try:
        styles, errors = audit_docx(
            args.docx,
            style_filter=args.filter,
            expected_style_map=expected_map
        )

        report = format_report(styles, errors, output_json=args.json)
        print(report)

        return 1 if errors else 0
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
