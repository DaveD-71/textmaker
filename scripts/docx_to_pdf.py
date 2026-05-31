"""Convert a DOCX file to PDF using Word's fixed-format export on Windows."""
import argparse
import sys
from pathlib import Path


def export_with_word(input_path: Path, output_path: Path) -> None:
    import win32com.client

    wd_export_format_pdf = 17
    wd_export_optimize_for_print = 0
    wd_export_all_document = 0
    wd_export_document_content = 0
    wd_export_create_heading_bookmarks = 1
    wd_alerts_none = 0

    word = win32com.client.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = wd_alerts_none
    doc = None
    try:
        doc = word.Documents.Open(
            str(input_path),
            ReadOnly=True,
            AddToRecentFiles=False,
            ConfirmConversions=False,
        )
        doc.Repaginate()
        doc.ExportAsFixedFormat(
            OutputFileName=str(output_path),
            ExportFormat=wd_export_format_pdf,
            OpenAfterExport=False,
            OptimizeFor=wd_export_optimize_for_print,
            Range=wd_export_all_document,
            From=1,
            To=1,
            Item=wd_export_document_content,
            IncludeDocProps=True,
            KeepIRM=True,
            CreateBookmarks=wd_export_create_heading_bookmarks,
            DocStructureTags=True,
            BitmapMissingFonts=True,
            UseISO19005_1=False,
        )
    finally:
        if doc is not None:
            doc.Close(False)
        word.Quit()


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog='docx-to-pdf',
        description='Convert a DOCX file to PDF using Word ExportAsFixedFormat (Windows only).',
    )
    parser.add_argument('--input', required=True, help='Input DOCX file path')
    parser.add_argument('--output', help='Output PDF file path (default: same name as input with .pdf)')
    args = parser.parse_args(argv)

    if sys.platform != 'win32':
        print('error: docx-to-pdf requires Microsoft Word on Windows.', file=sys.stderr)
        return 1

    input_path = Path(args.input).resolve()
    if not input_path.exists():
        print(f'error: input file not found: {input_path}', file=sys.stderr)
        return 1

    output_path = Path(args.output).resolve() if args.output else input_path.with_suffix('.pdf')
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f'Converting {input_path} -> {output_path}')
    try:
        export_with_word(input_path, output_path)
    except ImportError:
        print('error: pywin32 is not installed. Run: pip install pywin32', file=sys.stderr)
        return 1
    print(f'Wrote {output_path}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
