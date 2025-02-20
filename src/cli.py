"""
A CLI tool that reads folders of code and copies it to the clipboard.
"""

import argparse
import pyperclip
import logging
from pathlib import Path
from typing import List

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


def main(args: argparse.Namespace) -> None:
    files = get_files_from_inputs(args.inputs)
    logging.info("Files to process: %s", files)

    contents = [read_contents(file) for file in files]
    joined = "\n\n".join(contents)

    total_chars = len(joined)
    total_lines = joined.count("\n")

    logging.info(
        "Copied {total_lines:,} lines and {total_chars:,} chars to clipboard".format(
            total_lines=total_lines, total_chars=total_chars
        )
    )
    pyperclip.copy(joined)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    args = parse_args()
    main(args)
