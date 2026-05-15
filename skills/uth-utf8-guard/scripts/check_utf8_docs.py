#!/usr/bin/env python3
"""Validate UTF-8 documentation integrity for UTH governance docs."""

from __future__ import annotations

import argparse
import pathlib
import re
import sys


MOJIBAKE_MARKERS = ["\ufffd", "Ã", "Â", "锟斤拷", "ï»¿"]
FENCE_RE = re.compile(r"^\s*```")


def check_file(path: pathlib.Path) -> list[str]:
    errors: list[str] = []
    if not path.exists():
        return [f"{path}: file does not exist"]
    if not path.is_file():
        return [f"{path}: not a file"]

    data = path.read_bytes()
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        return [f"{path}: invalid UTF-8 at byte {exc.start}: {exc.reason}"]

    for marker in MOJIBAKE_MARKERS:
        if marker in text:
            errors.append(f"{path}: mojibake marker found: {marker!r}")

    if path.suffix.lower() in {".md", ".markdown"}:
        fence_count = sum(1 for line in text.splitlines() if FENCE_RE.match(line))
        if fence_count % 2 != 0:
            errors.append(f"{path}: unbalanced Markdown fences ({fence_count})")

    return errors


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Check UTF-8 docs for decode, mojibake, and Markdown fence issues.")
    parser.add_argument("paths", nargs="+", help="Files to check")
    args = parser.parse_args(argv)

    all_errors: list[str] = []
    for raw_path in args.paths:
        all_errors.extend(check_file(pathlib.Path(raw_path)))

    if all_errors:
        for error in all_errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"OK: {len(args.paths)} file(s) passed UTF-8 guard")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
