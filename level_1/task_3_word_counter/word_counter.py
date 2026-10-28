"""Count words in a UTF-8 text file."""
from __future__ import annotations

import argparse
import re
from pathlib import Path


WORD_PATTERN = re.compile(r"\b[\w']+\b", re.UNICODE)


def count_words(path: Path) -> int:
    """Read *path* and return its number of words."""
    return len(WORD_PATTERN.findall(path.read_text(encoding="utf-8")))


def main() -> int:
    parser = argparse.ArgumentParser(description="Count words in a text file.")
    parser.add_argument("file", type=Path)
    args = parser.parse_args()
    try:
        print(f"Word count: {count_words(args.file)}")
    except FileNotFoundError:
        print(f"Error: file not found: {args.file}")
        return 1
    except UnicodeDecodeError:
        print("Error: the file is not valid UTF-8 text.")
        return 1
    except OSError as error:
        print(f"Error reading file: {error}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
