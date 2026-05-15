#!/usr/bin/env python3
"""Install UTH Governance skills globally."""

from __future__ import annotations

import argparse
import os
import shutil
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Report:
    actions: list[str] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)

    def action(self, message: str) -> None:
        self.actions.append(message)

    def skip(self, message: str) -> None:
        self.skipped.append(message)

    def print(self) -> None:
        print("UTH Governance install report")
        print()
        print("Actions:")
        for item in self.actions or ["None"]:
            print(f"- {item}")
        print()
        print("Skipped:")
        for item in self.skipped or ["None"]:
            print(f"- {item}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Install UTH Governance skills globally.")
    parser.add_argument("--source", default=None, help="UTH package root. Defaults to this script's parent repository.")
    parser.add_argument("--runtime", choices=["codex", "claude", "opencode", "custom"], default="codex")
    parser.add_argument("--skills-dir", default=None, help="Override skill install directory.")
    parser.add_argument("--skip-skills", action="store_true", help="Do not install skills.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing UTH skill directories.")
    parser.add_argument("--dry-run", action="store_true", help="Print planned changes without writing files.")
    return parser.parse_args()


def package_root(args: argparse.Namespace) -> Path:
    root = Path(args.source).expanduser().resolve() if args.source else Path(__file__).resolve().parents[1]
    required = ["AGENTS.md", "skills"]
    missing = [item for item in required if not (root / item).exists()]
    if missing:
        raise SystemExit(f"Source is not a UTH package root: {root}; missing {', '.join(missing)}")
    return root


def default_skills_dir(runtime: str) -> Path:
    home = Path.home()
    if runtime == "codex":
        base = os.environ.get("CODEX_HOME")
        return Path(base).expanduser() / "skills" if base else home / ".codex" / "skills"
    if runtime == "claude":
        return home / ".claude" / "skills"
    if runtime == "opencode":
        base = os.environ.get("OPENCODE_CONFIG_DIR")
        return Path(base).expanduser() / "skills" if base else home / ".config" / "opencode" / "skills"
    raise SystemExit("--runtime custom requires --skills-dir")


def ensure_dir(path: Path, report: Report, dry_run: bool) -> None:
    if path.exists():
        return
    report.action(f"create directory {path}")
    if not dry_run:
        path.mkdir(parents=True, exist_ok=True)


def copy_directory(src: Path, dst: Path, *, force: bool, dry_run: bool, report: Report) -> None:
    if src.resolve() == dst.resolve():
        report.skip(f"source and destination are identical: {dst}")
        return
    if dst.exists() and not force:
        report.skip(f"exists; use --force to overwrite: {dst}")
        return
    if dst.exists() and force:
        report.action(f"overwrite directory {dst}")
        if not dry_run:
            shutil.rmtree(dst)
    else:
        report.action(f"copy directory {src} -> {dst}")
    if not dry_run:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(src, dst)


def install_skills(source: Path, skills_dir: Path, args: argparse.Namespace, report: Report) -> None:
    ensure_dir(skills_dir, report, args.dry_run)
    for src in sorted((source / "skills").iterdir()):
        if src.is_dir() and src.name.startswith("uth-"):
            copy_directory(src, skills_dir / src.name, force=args.force, dry_run=args.dry_run, report=report)


def main() -> int:
    args = parse_args()
    source = package_root(args)
    skills_dir = None if args.skip_skills else Path(args.skills_dir).expanduser().resolve() if args.skills_dir else default_skills_dir(args.runtime)
    report = Report()

    if skills_dir is not None:
        install_skills(source, skills_dir, args, report)

    report.print()
    print()
    print(f"Source: {source}")
    print(f"Skills directory: {skills_dir if skills_dir is not None else '<skipped>'}")
    print("Hook tools: not installed globally; uth-onboarding copies them into the target project.")
    print("Project initialization: not performed; run /uth-onboarding in the target project.")
    print("Dry run: yes" if args.dry_run else "Dry run: no")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
