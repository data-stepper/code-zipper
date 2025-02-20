"""
A CLI tool that reads folders of code and copies it to the clipboard.
"""

import argparse
import logging
from pathlib import Path
from typing import List

import pyperclip
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from core.reading import read_contents


def parse_args():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "inputs", nargs="+", help="Files, directories, or glob patterns to process"
    )

    return parser.parse_args()


def get_files_from_inputs(inputs: List[str]) -> List[Path]:
    paths = []

    for input_path in inputs:
        path = Path(input_path)

        if not path.exists():
            logging.error("Path %s does not exist", path)
            continue

        if path.is_file():
            paths.append(path)
        elif path.is_dir():
            # TODO: Add support for other default glob patterns
            paths.extend(path.rglob("**/*.py"))

    paths = list(sorted(set(paths)))
    logging.info("Found %s files", len(paths))
    return paths


console = Console()


def main() -> None:
    logging.basicConfig(level=logging.INFO)

    args = parse_args()
    files = get_files_from_inputs(args.inputs)

    table = Table(title="Files to Process", show_header=True, header_style="bold cyan")
    table.add_column("Filename", style="magenta")
    for file in files:
        table.add_row(str(file))
    console.print(table)

    contents = [read_contents(file) for file in files]
    joined = "\n\n".join(contents)

    total_chars = len(joined)
    total_lines = joined.count("\n") + 1

    summary = (
        f"[bold green]Success![/bold green]\n\n"
        f"Copied [bold yellow]{total_lines:,}[/bold yellow] lines and "
        f"[bold yellow]{total_chars:,}[/bold yellow] characters to clipboard."
    )
    console.print(
        Panel(summary, title="Clipboard Update", title_align="left", style="bold blue")
    )

    pyperclip.copy(joined)


if __name__ == "__main__":
    main()
