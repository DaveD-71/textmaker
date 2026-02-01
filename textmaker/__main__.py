from __future__ import annotations

import argparse
import sys


def _add_cmd(subparsers, name, help_text, handler):
    cmd = subparsers.add_parser(name, help=help_text)
    cmd.set_defaults(_handler=handler)
    cmd.add_argument("args", nargs=argparse.REMAINDER)
    return cmd


def _run_docx_to_markdown(args):
    from .docx_to_markdown import main
    sys.argv = ["docx_to_markdown"] + (args.args or [])
    main()


def _run_split_docx_units(args):
    from .split_docx_units import main
    sys.argv = ["split_docx_units"] + (args.args or [])
    main()


def _run_markdown_to_docx(args):
    from .cli import main
    sys.argv = ["markdown_to_docx"] + (args.args or [])
    main()


def _run_generate_reference(args):
    from .generate_reference_docx import main
    sys.argv = ["generate_reference_docx"] + (args.args or [])
    main()


def _run_preprocess_docx(args):
    from .preprocess_docx import main
    sys.argv = ["preprocess_docx"] + (args.args or [])
    main()


def _run_postprocess_docx(args):
    from .postprocess_docx import main
    sys.argv = ["postprocess_docx"] + (args.args or [])
    main()


def _run_postprocess_markdown(args):
    from .postprocess_markdown import main
    sys.argv = ["postprocess_markdown"] + (args.args or [])
    main()


def _run_export_docx_package(args):
    from .export_docx_package import main
    sys.argv = ["export_docx_package"] + (args.args or [])
    main()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="textmaker")
    subparsers = parser.add_subparsers(dest="command", required=True)

    _add_cmd(
        subparsers,
        "docx-to-markdown",
        "Convert DOCX to markdown units with assets and reference styles.",
        _run_docx_to_markdown,
    )
    _add_cmd(
        subparsers,
        "split-docx-units",
        "Split a DOCX into unit-level DOCX files.",
        _run_split_docx_units,
    )
    _add_cmd(
        subparsers,
        "markdown-to-docx",
        "Convert markdown to DOCX using pandoc and a reference file.",
        _run_markdown_to_docx,
    )
    _add_cmd(
        subparsers,
        "generate-reference",
        "Generate a reference DOCX with project styles.",
        _run_generate_reference,
    )
    _add_cmd(
        subparsers,
        "preprocess-docx",
        "Insert sentinel markers into a DOCX before conversion.",
        _run_preprocess_docx,
    )
    _add_cmd(
        subparsers,
        "postprocess-docx",
        "Post-process a DOCX to insert section breaks and list styles.",
        _run_postprocess_docx,
    )
    _add_cmd(
        subparsers,
        "postprocess-markdown",
        "Replace sentinel markers in markdown outputs.",
        _run_postprocess_markdown,
    )
    _add_cmd(
        subparsers,
        "export-docx-package",
        "Export a DOCX into JSON/CSV analysis package.",
        _run_export_docx_package,
    )

    args = parser.parse_args(argv)
    handler = getattr(args, "_handler", None)
    if handler is None:
        parser.print_help()
        return 2
    handler(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
