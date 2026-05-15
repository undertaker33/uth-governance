#!/usr/bin/env python3
"""Install UTH Governance into a target project."""

from __future__ import annotations

import argparse
import shutil
from dataclasses import dataclass, field
from pathlib import Path


UTH_BLOCK_START = "<!-- UTH-GOVERNANCE:START -->"
UTH_BLOCK_END = "<!-- UTH-GOVERNANCE:END -->"


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
    parser = argparse.ArgumentParser(description="Install UTH Governance into a target project.")
    parser.add_argument("--source", default=None, help="UTH package root. Defaults to this script's parent repository.")
    parser.add_argument("--target", required=True, help="Target project root.")
    parser.add_argument("--runtime", choices=["codex", "claude", "opencode", "custom"], default="codex")
    parser.add_argument("--skills-dir", default=None, help="Override skill install directory.")
    parser.add_argument("--skip-skills", action="store_true", help="Do not install skills.")
    parser.add_argument("--skip-tools", action="store_true", help="Do not install hook tools.")
    parser.add_argument("--skip-docs", action="store_true", help="Do not create project docs or AGENTS.md block.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing UTH skill/tool directories.")
    parser.add_argument("--dry-run", action="store_true", help="Print planned changes without writing files.")
    return parser.parse_args()


def package_root(args: argparse.Namespace) -> Path:
    root = Path(args.source).expanduser().resolve() if args.source else Path(__file__).resolve().parents[1]
    required = ["AGENTS.md", "skills", "tools/uth-hooks"]
    missing = [item for item in required if not (root / item).exists()]
    if missing:
        raise SystemExit(f"Source is not a UTH package root: {root}; missing {', '.join(missing)}")
    return root


def default_skills_dir(runtime: str) -> Path:
    home = Path.home()
    if runtime == "codex":
        import os

        base = os.environ.get("CODEX_HOME")
        return Path(base).expanduser() / "skills" if base else home / ".codex" / "skills"
    if runtime == "claude":
        return home / ".claude" / "skills"
    if runtime == "opencode":
        import os

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


def install_tools(source: Path, target: Path, args: argparse.Namespace, report: Report) -> None:
    copy_directory(source / "tools" / "uth-hooks", target / "tools" / "uth-hooks", force=args.force, dry_run=args.dry_run, report=report)


def write_if_absent(path: Path, content: str, report: Report, dry_run: bool) -> None:
    if path.exists():
        report.skip(f"exists: {path}")
        return
    report.action(f"create file {path}")
    if not dry_run:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")


def append_agents_block(target: Path, report: Report, dry_run: bool) -> None:
    agents = target / "AGENTS.md"
    block = f"""

{UTH_BLOCK_START}
## UTH Governance

- Route engineering tasks through `uth-governance` and the selected `uth-*` scene skill.
- Keep this root entry lightweight. Project governance rules live in `docs/_governance/`.
- `docs/current-state.md` is an active-state index, not a log.
- Hook runner: `tools/uth-hooks/uth-hook.py`.
{UTH_BLOCK_END}
""".lstrip()
    if agents.exists():
        text = agents.read_text(encoding="utf-8")
        if UTH_BLOCK_START in text:
            report.skip(f"UTH block already present: {agents}")
            return
        new_text = text.rstrip() + "\n\n" + block
        report.action(f"append UTH block to {agents}")
    else:
        new_text = "# Project Agent Entry\n\n" + block
        report.action(f"create {agents}")
    if not dry_run:
        agents.write_text(new_text, encoding="utf-8", newline="\n")


def install_docs(target: Path, args: argparse.Namespace, report: Report) -> None:
    dirs = [
        target / "docs" / "_governance",
        target / "docs" / "work",
        target / "docs" / "work" / "LW-Work",
        target / "docs" / "context",
        target / "docs" / "archive",
        target / "docs" / "decisions",
        target / "docs" / "changelogs",
    ]
    for directory in dirs:
        ensure_dir(directory, report, args.dry_run)

    write_if_absent(
        target / "docs" / "_governance" / "README.md",
        "# Project Governance\n\nPut project-specific governance rules here. Keep scene routing and execution flow in UTH skills.\n",
        report,
        args.dry_run,
    )
    write_if_absent(
        target / "docs" / "current-state.md",
        "# Current State\n\nThis file is an active-state index only. Do not use it as a log.\n\n## Active Work\n\n- None recorded yet.\n\n## Context Index\n\n- See `docs/context/README.md`.\n\n## Governance\n\n- Project governance: `docs/_governance/README.md`\n- Hook runner: `tools/uth-hooks/uth-hook.py`\n",
        report,
        args.dry_run,
    )
    write_if_absent(
        target / "docs" / "work" / "README.md",
        "# Work Packages\n\nFormal task packages live here. Lightweight development records live under `LW-Work/`.\n",
        report,
        args.dry_run,
    )
    write_if_absent(
        target / "docs" / "context" / "README.md",
        "# Context Index\n\nSummarize stable module context here. Include a Git baseline when the context is based on committed code.\n",
        report,
        args.dry_run,
    )
    write_if_absent(
        target / "docs" / "archive" / "README.md",
        "# Archive\n\nMove confirmed-complete work packages and lightweight records here during documentation cleanup.\n",
        report,
        args.dry_run,
    )
    write_if_absent(
        target / "docs" / "decisions" / "README.md",
        "# Decisions\n\nADR files are decision evidence chains, not the current fact source.\n",
        report,
        args.dry_run,
    )
    write_if_absent(
        target / "docs" / "changelogs" / "README.md",
        "# Changelogs\n\nUser-facing release changelogs live here when the Git/release scene requires them.\n",
        report,
        args.dry_run,
    )
    append_agents_block(target, report, args.dry_run)


def main() -> int:
    args = parse_args()
    source = package_root(args)
    target = Path(args.target).expanduser().resolve()
    skills_dir = Path(args.skills_dir).expanduser().resolve() if args.skills_dir else default_skills_dir(args.runtime)
    report = Report()

    ensure_dir(target, report, args.dry_run)
    if not args.skip_skills:
        install_skills(source, skills_dir, args, report)
    if not args.skip_tools:
        install_tools(source, target, args, report)
    if not args.skip_docs:
        install_docs(target, args, report)

    report.print()
    print()
    print(f"Source: {source}")
    print(f"Target: {target}")
    print(f"Skills directory: {skills_dir}")
    print("Dry run: yes" if args.dry_run else "Dry run: no")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
