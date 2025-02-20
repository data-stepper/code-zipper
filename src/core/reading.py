from collections import defaultdict
from pathlib import Path


def read_contents(file: Path) -> str:
    lines = []
    stats = defaultdict(int)

    with open(file, "r") as f:
        for i, line in enumerate(f, 1):
            line_str = line.rstrip()
            lines.append(f"{i:4d} | {line_str}")

            stats["lines"] += 1
            stats["chars"] += len(line_str)

    lines_of_text = [
        f"File: {file} ({stats['lines']:,} lines and {stats['chars']:,} chars)",
    ]
    lines_of_text.extend(lines)

    return "\n".join(lines_of_text)
