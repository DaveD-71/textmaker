from __future__ import annotations

import sys


_COMMANDS = {
    "docx-to-markdown": "docx_to_markdown",
    "split-docx-units": "split_docx_units",
    "markdown-to-docx": "cli",
    "generate-reference": "generate_reference_docx",
    "preprocess-docx": "preprocess_docx",
    "postprocess-docx": "postprocess_docx",
    "postprocess-markdown": "postprocess_markdown",
    "export-docx-package": "export_docx_package",
    "pdf-to-markdown": "pdf_to_markdown",
    "image-to-markdown": "image_to_markdown",
<<<<<<< HEAD
    "yaml-to-audio": "yaml_to_audio",
=======
    "pptx-to-package": "pptx_converter",
>>>>>>> 58be8ce087bfa707dda3859129c32da31631ebbf
}


def _print_help() -> None:
    cmds = ",".join(sorted(_COMMANDS.keys()))
    print("usage: textmaker [-h] [{%s}]" % cmds)
    print("\ncommands:")
    for name in sorted(_COMMANDS.keys()):
        print(f"  {name}")


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] in ("-h", "--help"):
        _print_help()
        return 0

    command = argv[0]
    if command not in _COMMANDS:
        _print_help()
        return 2

    module_name = _COMMANDS[command]
    module = __import__(f"textmaker.{module_name}", fromlist=["main"])
    sys.argv = [module_name] + argv[1:]
    module.main()
    return 0


if __name__ == "__main__":
    sys.exit(main())
