#!/usr/bin/env python3
"""Check or sync onboarding hook assets against the reference hook bundle."""

from __future__ import annotations

import argparse
import hashlib
import shutil
from pathlib import Path
from typing import NamedTuple

IGNORED_DIRS = {"__pycache__", ".pytest_cache"}
IGNORED_SUFFIXES = {".pyc", ".pyo"}


class Mismatch(NamedTuple):
    path: str
    reason: str


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def should_ignore(path: Path) -> bool:
    return any(part in IGNORED_DIRS for part in path.parts) or path.suffix in IGNORED_SUFFIXES


def iter_files(root: Path) -> dict[str, Path]:
    files: dict[str, Path] = {}
    if not root.exists():
        return files
    for path in root.rglob("*"):
        rel = path.relative_to(root)
        if should_ignore(rel):
            continue
        if path.is_file():
            files[rel.as_posix()] = path
    return files


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def compare_dirs(source: Path, target: Path) -> list[Mismatch]:
    source_files = iter_files(source)
    target_files = iter_files(target)
    mismatches: list[Mismatch] = []

    for rel in sorted(source_files.keys() - target_files.keys()):
        mismatches.append(Mismatch(rel, "missing-in-target"))
    for rel in sorted(target_files.keys() - source_files.keys()):
        mismatches.append(Mismatch(rel, "extra-in-target"))
    for rel in sorted(source_files.keys() & target_files.keys()):
        if digest(source_files[rel]) != digest(target_files[rel]):
            mismatches.append(Mismatch(rel, "content-differs"))
    return mismatches


def sync_dirs(source: Path, target: Path) -> None:
    source_files = iter_files(source)
    target_files = iter_files(target)
    target.mkdir(parents=True, exist_ok=True)

    for rel, src in source_files.items():
        dst = target / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)

    for rel, dst in target_files.items():
        if rel not in source_files:
            dst.unlink()

    for path in sorted(target.rglob("*"), key=lambda item: len(item.parts), reverse=True):
        if path.is_dir() and not should_ignore(path.relative_to(target)):
            try:
                path.rmdir()
            except OSError:
                pass


def parse_args() -> argparse.Namespace:
    root = repo_root()
    parser = argparse.ArgumentParser(description="Check onboarding hook asset sync.")
    parser.add_argument("--source", type=Path, default=root / "tools" / "uth-hooks")
    parser.add_argument("--target", type=Path, default=root / "skills" / "uth-onboarding" / "assets" / "uth-hooks")
    parser.add_argument("--sync", action="store_true", help="Copy source files into target before checking.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source = args.source.resolve()
    target = args.target.resolve()

    if args.sync:
        sync_dirs(source, target)

    mismatches = compare_dirs(source, target)
    if not mismatches:
        print(f"OK: assets synchronized: {source} == {target}")
        return 0

    print(f"FAIL: assets differ: {source} != {target}")
    for item in mismatches:
        print(f"- {item.reason}: {item.path}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
