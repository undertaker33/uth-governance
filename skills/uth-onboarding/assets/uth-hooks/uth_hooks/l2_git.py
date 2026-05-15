from __future__ import annotations

import re
from typing import Any

from .common import as_bool, result

def is_git_write_command(command: str) -> bool:
    text = command.strip()
    write_patterns = [
        r"^git\s+add\b",
        r"^git\s+commit\b",
        r"^git\s+push\b",
        r"^git\s+tag\b",
        r"^git\s+merge\b",
        r"^git\s+rebase\b",
        r"^git\s+switch\b",
        r"^git\s+checkout\b",
        r"^git\s+branch\s+(-d|-D|-m|--delete|--move|--copy|-c|-C)\b",
        r"^git\s+worktree\s+(add|remove|move|prune|repair)\b",
    ]
    return any(re.search(pattern, text) for pattern in write_patterns)


def check_git_write(ctx: dict[str, Any]) -> list[dict[str, Any]]:
    commands = ctx.get("commands", [])
    if isinstance(commands, str):
        commands = [commands]
    write_commands = [cmd for cmd in commands if is_git_write_command(cmd)]
    if not write_commands:
        return [result("PASS", "no-git-write", "No Git write command detected.")]

    findings: list[dict[str, Any]] = []
    if ctx.get("active_scene") != "uth-git":
        findings.append(result("BLOCK", "git-scene-required", "Git writes require active_scene = uth-git."))
    if not as_bool(ctx.get("git_plan_present")):
        findings.append(result("BLOCK", "git-plan-missing", "Git writes require a shown Git plan."))
    if not as_bool(ctx.get("user_git_confirmed")):
        findings.append(result("BLOCK", "git-confirmation-missing", "Git writes require explicit user confirmation."))
    if as_bool(ctx.get("release_or_tag")) and not as_bool(ctx.get("changelog_ok")):
        findings.append(result("BLOCK", "changelog-required", "Release/tag Git writes require changelog rule satisfaction."))

    if findings:
        return findings
    return [result("PASS", "git-write-allowed", "Git write gate passed.")]
