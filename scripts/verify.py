#!/usr/bin/env python3
"""Run the UTH governance pack verification checks."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIRS = [
    ROOT / "scripts",
    ROOT / "tools" / "uth-hooks",
    ROOT / "skills" / "uth-onboarding" / "assets" / "uth-hooks",
]
NO_BOM_GLOBS = [
    "docs/**/*.md",
    "skills/**/*.md",
    "tools/**/*.py",
    "scripts/**/*.py",
]
IGNORED_PARTS = {"__pycache__", ".pytest_cache"}
IGNORED_FIXTURE_PARTS = {"tests", "fixtures"}
BOM_UTF8 = b"\xef\xbb\xbf"


def run_command(command: list[str], label: str) -> bool:
    print(f"==> {label}")
    proc = subprocess.run(command, cwd=ROOT, text=True)
    if proc.returncode == 0:
        print(f"PASS: {label}")
        return True
    print(f"FAIL: {label} (exit {proc.returncode})")
    return False


def is_git_worktree() -> bool:
    proc = subprocess.run(
        ["git", "rev-parse", "--is-inside-work-tree"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return proc.returncode == 0


def check_git_diff() -> bool:
    if not is_git_worktree():
        print("==> git diff --check")
        print("SKIP: git diff --check (not a git worktree)")
        return True
    return run_command(["git", "diff", "--check"], "git diff --check")


def should_skip_compile(path: Path) -> bool:
    parts = set(path.relative_to(ROOT).parts)
    if parts & IGNORED_PARTS:
        return True
    return IGNORED_FIXTURE_PARTS <= parts


def should_skip_no_bom(path: Path, root: Path = ROOT) -> bool:
    try:
        parts = set(path.relative_to(root).parts)
    except ValueError:
        parts = set(path.parts)
    return bool(parts & IGNORED_PARTS)


def iter_no_bom_paths(root: Path = ROOT) -> list[Path]:
    paths: list[Path] = []
    seen: set[Path] = set()
    root = root.resolve()

    for raw in (root / "README.md", root / "AGENTS.md"):
        if raw.exists() and raw.is_file() and not should_skip_no_bom(raw, root):
            resolved = raw.resolve()
            paths.append(resolved)
            seen.add(resolved)

    for pattern in NO_BOM_GLOBS:
        for path in root.glob(pattern):
            if not path.is_file() or should_skip_no_bom(path, root):
                continue
            resolved = path.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            paths.append(resolved)
    return paths


def find_bom_files(root: Path = ROOT) -> list[Path]:
    failures: list[Path] = []
    for path in iter_no_bom_paths(root):
        try:
            if path.read_bytes().startswith(BOM_UTF8):
                failures.append(path)
        except OSError:
            failures.append(path)
    return failures


def check_no_bom() -> bool:
    print("==> UTF-8 no BOM")
    failures = find_bom_files(ROOT)
    if failures:
        for path in failures:
            try:
                display = path.relative_to(ROOT)
            except ValueError:
                display = path
            print(f"FAIL: {display}: UTF-8 BOM is not allowed")
        return False
    print(f"PASS: UTF-8 no BOM ({len(iter_no_bom_paths(ROOT))} files)")
    return True


def check_python_syntax() -> bool:
    print("==> Python syntax")
    failures: list[tuple[Path, str]] = []
    seen: set[Path] = set()
    for directory in PYTHON_DIRS:
        if not directory.exists():
            continue
        for path in directory.rglob("*.py"):
            resolved = path.resolve()
            if resolved in seen or should_skip_compile(path):
                continue
            seen.add(resolved)
            try:
                source = path.read_text(encoding="utf-8")
                compile(source, str(path), "exec")
            except Exception as exc:  # noqa: BLE001 - verification should report all syntax/read failures.
                failures.append((path.relative_to(ROOT), str(exc)))
    if failures:
        for path, error in failures:
            print(f"FAIL: {path}: {error}")
        return False
    print(f"PASS: Python syntax ({len(seen)} files)")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify the UTH governance pack.")
    parser.add_argument("--skip-git-diff-check", action="store_true", help="Skip git diff --check.")
    args = parser.parse_args()

    checks = [
        run_command([sys.executable, "-m", "unittest", "discover", "-s", "tools/uth-hooks/tests", "-p", "test_*.py"], "hook unit tests"),
        run_command([sys.executable, "scripts/check_assets_sync.py"], "onboarding hook asset sync"),
        check_python_syntax(),
        check_no_bom(),
    ]
    if not args.skip_git_diff_check:
        checks.append(check_git_diff())

    return 0 if all(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
