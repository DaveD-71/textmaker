"""Convert a DOCX file to PDF using the docx2pdf library (Word COM on Windows)."""
import argparse
import sys
from pathlib import Path


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog='docx-to-pdf',
        description='Convert a DOCX file to PDF using Word COM (Windows only).',
    )
    parser.add_argument('--input', required=True, help='Input DOCX file path')
    parser.add_argument('--output', help='Output PDF file path (default: same name as input with .pdf)')
    args = parser.parse_args(argv)

    try:
        from docx2pdf import convert
    except ImportError:
        print('error: docx2pdf is not installed. Run: pip install docx2pdf', file=sys.stderr)
        return 1

    input_path = Path(args.input).resolve()
    if not input_path.exists():
        print(f'error: input file not found: {input_path}', file=sys.stderr)
        return 1

    output_path = Path(args.output).resolve() if args.output else input_path.with_suffix('.pdf')
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f'Converting {input_path} -> {output_path}')
    convert(str(input_path), str(output_path))
    print(f'Wrote {output_path}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
