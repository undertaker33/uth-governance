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
IGNORED_PARTS = {"__pycache__", ".pytest_cache"}
IGNORED_FIXTURE_PARTS = {"tests", "fixtures"}


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
    ]
    if not args.skip_git_diff_check:
        checks.append(check_git_diff())

    return 0 if all(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
