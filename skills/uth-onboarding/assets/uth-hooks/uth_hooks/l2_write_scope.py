from __future__ import annotations

from pathlib import Path
from typing import Any

from .common import as_bool, get_paths, match_pattern, matches_any, normalize_path, result

def scene_allowed_patterns(ctx: dict[str, Any], config: dict[str, Any]) -> list[str]:
    active_scene = ctx.get("active_scene")
    patterns: list[str] = []
    patterns.extend(config.get("default_allowed_writes", []))
    patterns.extend(config.get("scene_write_rules", {}).get(active_scene, []))
    patterns.extend(ctx.get("allowed_writes", []))
    for expansion in ctx.get("scope_expansions", []):
        if isinstance(expansion, str):
            patterns.append(expansion)
        elif expansion.get("approved_by_user") and expansion.get("path"):
            patterns.append(expansion["path"])
    return patterns


def skill_maintenance_allowed(ctx: dict[str, Any]) -> bool:
    return (
        as_bool(ctx.get("skill_creator_active"))
        or as_bool(ctx.get("explicit_skill_maintenance"))
        or ctx.get("active_scene") == "skill-creator"
    )


def uth_sp_maintenance_allowed(ctx: dict[str, Any]) -> bool:
    return skill_maintenance_allowed(ctx) and as_bool(ctx.get("explicit_uth_sp_maintenance"))


def check_hard_forbidden(path: str, ctx: dict[str, Any]) -> dict[str, Any] | None:
    active_scene = ctx.get("active_scene")

    if match_pattern(path, ".git/**"):
        return result("BLOCK", "git-dir-write", "Direct writes under .git are forbidden.", path)

    if match_pattern(path, "skills/uth-sp-*/**"):
        if uth_sp_maintenance_allowed(ctx):
            return result("PASS", "uth-sp-skill-maintenance", "UTH-SP skill maintenance write is explicitly allowed.", path)
        return result(
            "BLOCK",
            "uth-sp-skill-write-blocked",
            "skills/uth-sp-*/** requires explicit UTH-SP maintenance and skill-creator flow.",
            path,
        )

    if match_pattern(path, "skills/**"):
        if skill_maintenance_allowed(ctx):
            return result("PASS", "skill-maintenance", "Skill maintenance write is explicitly allowed.", path)
        return result("BLOCK", "skill-write-blocked", "skills/** writes require explicit skill maintenance.", path)

    if match_pattern(path, "docs/context/**") and active_scene not in {"uth-docs", "uth-onboarding"}:
        return result("BLOCK", "context-write-blocked", "docs/context/** is writable only in uth-docs or uth-onboarding.", path)

    if match_pattern(path, "docs/archive/**") and active_scene not in {"uth-docs", "uth-onboarding"}:
        return result("BLOCK", "archive-write-blocked", "docs/archive/** is writable only in uth-docs or uth-onboarding.", path)

    if match_pattern(path, "docs/decisions/ADR-*.md") and active_scene != "uth-design":
        return result("BLOCK", "adr-write-blocked", "ADR body/status writes require uth-design.", path)

    if match_pattern(path, "docs/changelogs/**") and active_scene not in {"uth-git", "uth-onboarding"}:
        return result("BLOCK", "changelog-write-blocked", "docs/changelogs/** writes require uth-git or uth-onboarding for scaffold indexes.", path)

    return None


def check_l1_process(ctx: dict[str, Any]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    if as_bool(ctx.get("no_engineering_action")):
        return [result("PASS", "no-engineering-action", "No engineering action; UTH and UTH-SP do not trigger.")]

    if as_bool(ctx.get("scene_ambiguous")) or ctx.get("active_scene") in {None, ""}:
        findings.append(result("BLOCK", "scene-ambiguous", "Scene is unclear; ask one clarifying question via uth-governance."))

    ambiguity = ctx.get("ambiguity", {})
    if as_bool(ambiguity.get("present")):
        ok = (
            as_bool(ambiguity.get("brainstorming_invoked"))
            or as_bool(ambiguity.get("resolved"))
            or bool(ambiguity.get("explicit_no_brainstorm_reason"))
        )
        if not ok:
            findings.append(result("BLOCK", "ambiguity-unresolved", "Ambiguity requires clarification, uth-sp-brainstorming, or explicit no-brainstorm reason."))

    transition = ctx.get("transition", {})
    if transition:
        findings.extend(check_transition(transition))

    worker = ctx.get("worker") or ctx.get("worker_dispatch") or {}
    if worker:
        findings.extend(check_worker_dispatch(worker, ctx))

    if as_bool(ctx.get("require_uth_sp_decision", ctx.get("active_scene") in CODE_CHANGING_SCENES)):
        uth_sp = ctx.get("uth_sp", {})
        if not as_bool(uth_sp.get("decision_recorded")):
            findings.append(result("BLOCK", "uth-sp-decision-missing", "Sub-scene must record UTH-SP trigger decision before execution."))
        else:
            findings.append(result("PASS", "uth-sp-decision-recorded", "UTH-SP trigger decision is recorded."))

    return findings or [result("PASS", "l1-pass", "L1 process gate passed.")]


def check_transition(transition: dict[str, Any]) -> list[dict[str, Any]]:
    source = transition.get("from")
    target = transition.get("to")
    authorized_design_patch = as_bool(transition.get("authorized_design_patch"))
    findings: list[dict[str, Any]] = []

    if source == "uth-design" and target == "uth-dev" and not as_bool(transition.get("explicit_handoff")):
        findings.append(result("BLOCK", "design-dev-handoff-missing", "design -> dev requires explicit uth-dev handoff."))
    if source == "uth-design" and target in {"code-patch", "uth-debug"} and not authorized_design_patch:
        findings.append(result("ASK", "design-patch-needs-confirmation", "Design-assisted code patch requires user confirmation."))
    if source == "uth-debug" and target in {"feature", "uth-dev", "uth-design"} and not as_bool(transition.get("explicit_handoff")):
        findings.append(result("BLOCK", "debug-feature-handoff-missing", "debug -> feature/design work requires explicit scene switch."))
    if source == "uth-review" and target in {"fix", "uth-dev", "uth-debug"} and not as_bool(transition.get("explicit_handoff")):
        findings.append(result("BLOCK", "review-fix-handoff-missing", "review cannot directly fix without routing to uth-debug or uth-dev."))
    if target == "uth-git" and not as_bool(transition.get("explicit_handoff")):
        findings.append(result("BLOCK", "git-handoff-missing", "Any transition to git requires explicit uth-git handoff."))

    return findings or [result("PASS", "transition-pass", "Scene transition is explicit or not restricted.")]


def check_worker_dispatch(worker: dict[str, Any], ctx: dict[str, Any]) -> list[dict[str, Any]]:
    role = worker.get("role", "")
    findings: list[dict[str, Any]] = []
    if role == "worker":
        if not as_bool(worker.get("prompt_written")) or not worker.get("prompt_path"):
            findings.append(result("BLOCK", "worker-prompt-missing", "Worker dispatch requires persisted task-package Prompt before dispatch."))
        if as_bool(worker.get("git_write_allowed")):
            findings.append(result("BLOCK", "worker-git-write", "Worker must not perform Git writes."))
        if ctx.get("mode") == "light-dev" and not as_bool(worker.get("user_confirmed_worker")):
            findings.append(result("ASK", "light-dev-worker-confirmation", "Light dev normally avoids worker dispatch; ask user or upgrade to formal task package."))
    elif role in {"planner", "evaluator"}:
        if as_bool(worker.get("prompt_written")):
            findings.append(result("WARN", "readonly-agent-prompt-written", "planner/evaluator should not persist Prompt files."))
    return findings or [result("PASS", "worker-dispatch-pass", "Worker dispatch gate passed.")]


def check_file_write(ctx: dict[str, Any], config: dict[str, Any], project: Path) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    allowed = scene_allowed_patterns(ctx, config)
    for raw in get_paths(ctx):
        path = normalize_path(raw, project)
        hard = check_hard_forbidden(path, ctx)
        if hard:
            findings.append(hard)
            continue
        if matches_any(path, config.get("extra_hard_forbidden", [])):
            findings.append(result("BLOCK", "extra-hard-forbidden", "Path matches project extra_hard_forbidden.", path))
            continue
        if allowed and matches_any(path, allowed):
            findings.append(result("PASS", "write-allowed", "Path is within current allowed write scope.", path))
        else:
            findings.append(result("ASK", "write-scope-expansion", "Path is outside current allowed write scope; ask user for temporary expansion.", path))
    return findings or [result("BLOCK", "no-write-paths", "file-write event requires paths.")]
