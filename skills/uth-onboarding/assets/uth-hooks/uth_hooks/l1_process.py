from __future__ import annotations

import re
from typing import Any

from .common import CODE_CHANGING_SCENES, as_bool, result


LIGHT_DEV_MODEL_LIMITS: dict[str, dict[str, int]] = {
    "claude-opus-4.7": {"changed_files": 8, "modules": 2, "implementation_steps": 4},
    "gpt-5.5": {"changed_files": 8, "modules": 2, "implementation_steps": 4},
    "claude-opus-4.6": {"changed_files": 5, "modules": 1, "implementation_steps": 3},
    "gpt-5.4": {"changed_files": 5, "modules": 1, "implementation_steps": 3},
    "deepseek-v4-pro": {"changed_files": 5, "modules": 1, "implementation_steps": 3},
    "mimo-v2.5-pro": {"changed_files": 5, "modules": 1, "implementation_steps": 3},
    "kimi-k2.6": {"changed_files": 5, "modules": 1, "implementation_steps": 3},
    "gpt-5.3-codex-spark": {"changed_files": 3, "modules": 1, "implementation_steps": 2},
    "deepseek-v4-flash": {"changed_files": 3, "modules": 1, "implementation_steps": 2},
}

MODEL_ALIASES = {
    "claude-opus4.6": "claude-opus-4.6",
    "claude-opus4.7": "claude-opus-4.7",
    "opus-4.6": "claude-opus-4.6",
    "opus-4.7": "claude-opus-4.7",
    "opus4.6": "claude-opus-4.6",
    "opus4.7": "claude-opus-4.7",
    "gpt5.4": "gpt-5.4",
    "gpt5.5": "gpt-5.5",
    "gpt5.3-codex-spark": "gpt-5.3-codex-spark",
    "gpt5.3codex-spark": "gpt-5.3-codex-spark",
    "gpt-5.3codex-spark": "gpt-5.3-codex-spark",
    "kimi-k2-6": "kimi-k2.6",
    "k2.6": "kimi-k2.6",
}

LIGHT_DEV_FORMAL_TRIGGER_FIELDS = {
    "ambiguous_requirements": "requirements are ambiguous",
    "acceptance_unclear": "acceptance criteria are unclear",
    "requires_design": "design decision is required",
    "requires_formal_todo": "formal Todo is required",
    "new_feature_surface": "new feature surface is required",
    "public_api_or_contract_change": "public API or contract changes",
    "database_schema_or_migration": "database schema or migration changes",
    "auth_permission_security": "auth, permission, or security behavior changes",
    "architecture_or_module_boundary": "architecture or module boundary changes",
    "new_dependency_or_build_logic": "new dependency or build logic changes",
    "cross_module_state_or_data_flow": "cross-module state or data-flow changes",
    "external_integration_or_protocol": "external integration or protocol changes",
    "concurrency_state_machine_or_permission_rules": "concurrency, state machine, or permission rules change",
    "data_loss_or_user_visible_risk": "data-loss or high user-visible risk exists",
    "requires_worker_or_parallel_agents": "worker or parallel agents are required",
}


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

    if ctx.get("mode") == "light-dev":
        findings.extend(check_light_dev_model_boundary(ctx, worker))

    if as_bool(ctx.get("require_uth_sp_decision", ctx.get("active_scene") in CODE_CHANGING_SCENES)):
        uth_sp = ctx.get("uth_sp", {})
        if not as_bool(uth_sp.get("decision_recorded")):
            findings.append(result("BLOCK", "uth-sp-decision-missing", "Sub-scene must record UTH-SP trigger decision before execution."))
        else:
            findings.append(result("PASS", "uth-sp-decision-recorded", "UTH-SP trigger decision is recorded."))

    return findings or [result("PASS", "l1-pass", "L1 process gate passed.")]


def check_light_dev_model_boundary(ctx: dict[str, Any], worker: dict[str, Any]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    model = normalize_model_name(extract_model_name(ctx))
    if not model or model not in LIGHT_DEV_MODEL_LIMITS:
        return [
            result(
                "BLOCK",
                "lwdev-unsupported-model",
                "light-dev requires a supported llm_model with a published hard boundary.",
            )
        ]

    task_shape = extract_task_shape(ctx)
    counts = {
        "changed_files": count_value(task_shape, "changed_files_count", "changed_files"),
        "modules": count_value(task_shape, "modules_count", "modules"),
        "implementation_steps": count_value(task_shape, "implementation_steps_count", "implementation_steps"),
    }
    missing = [name for name, value in counts.items() if value is None]
    if missing:
        findings.append(
            result(
                "BLOCK",
                "lwdev-boundary-evidence-missing",
                "light-dev requires explicit changed_files/modules/implementation_steps counts.",
            )
        )
        return findings

    limits = LIGHT_DEV_MODEL_LIMITS[model]
    if counts["changed_files"] > limits["changed_files"]:
        findings.append(
            result(
                "BLOCK",
                "lwdev-changed-files-limit",
                f"light-dev on {model} allows at most {limits['changed_files']} changed files.",
            )
        )
    if counts["modules"] > limits["modules"]:
        findings.append(
            result(
                "BLOCK",
                "lwdev-modules-limit",
                f"light-dev on {model} allows at most {limits['modules']} touched modules.",
            )
        )
    if counts["implementation_steps"] > limits["implementation_steps"]:
        findings.append(
            result(
                "BLOCK",
                "lwdev-implementation-steps-limit",
                f"light-dev on {model} allows at most {limits['implementation_steps']} implementation steps.",
            )
        )

    formal_reasons = formal_trigger_reasons(ctx, task_shape, worker)
    if formal_reasons:
        findings.append(
            result(
                "BLOCK",
                "lwdev-formal-trigger",
                "light-dev is forbidden because formal-dev trigger(s) are present: "
                + ", ".join(formal_reasons),
            )
        )

    if findings:
        return findings
    return [result("PASS", "lwdev-model-boundary-pass", f"light-dev model boundary passed for {model}.")]


def extract_model_name(ctx: dict[str, Any]) -> str | None:
    llm = ctx.get("llm")
    if isinstance(llm, dict):
        for key in ("model", "model_id", "name"):
            if llm.get(key):
                return str(llm[key])
    for key in ("llm_model", "model_id", "model"):
        if ctx.get(key):
            return str(ctx[key])
    return None


def normalize_model_name(value: str | None) -> str:
    if not value:
        return ""
    normalized = re.sub(r"[^a-z0-9.]+", "-", value.strip().lower()).strip("-")
    normalized = normalized.replace("gpt5.", "gpt-5.")
    normalized = normalized.replace("5.3codex", "5.3-codex")
    normalized = normalized.replace("opus4.", "opus-4.")
    return MODEL_ALIASES.get(normalized, normalized)


def extract_task_shape(ctx: dict[str, Any]) -> dict[str, Any]:
    task_shape: dict[str, Any] = {}
    for key in ("task_shape", "task", "work_scope"):
        value = ctx.get(key)
        if isinstance(value, dict):
            task_shape.update(value)
    for key in (
        "changed_files",
        "changed_files_count",
        "modules",
        "modules_count",
        "implementation_steps",
        "implementation_steps_count",
        *LIGHT_DEV_FORMAL_TRIGGER_FIELDS.keys(),
    ):
        if key in ctx and key not in task_shape:
            task_shape[key] = ctx[key]
    return task_shape


def count_value(task_shape: dict[str, Any], count_key: str, collection_key: str) -> int | None:
    raw_count = task_shape.get(count_key)
    if raw_count is not None:
        try:
            return int(raw_count)
        except (TypeError, ValueError):
            return None

    raw_collection = task_shape.get(collection_key)
    if isinstance(raw_collection, (list, tuple, set)):
        return len(raw_collection)
    if isinstance(raw_collection, str) and raw_collection.strip():
        return 1
    return None


def formal_trigger_reasons(ctx: dict[str, Any], task_shape: dict[str, Any], worker: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    for key, reason in LIGHT_DEV_FORMAL_TRIGGER_FIELDS.items():
        if as_bool(task_shape.get(key)) or as_bool(ctx.get(key)):
            reasons.append(reason)

    explicit_triggers = task_shape.get("formal_triggers") or ctx.get("formal_triggers") or ctx.get("light_dev_formal_triggers")
    if isinstance(explicit_triggers, str) and explicit_triggers.strip():
        reasons.append(explicit_triggers.strip())
    elif isinstance(explicit_triggers, list):
        reasons.extend(str(item) for item in explicit_triggers if str(item).strip())

    if worker.get("role") == "worker":
        reasons.append("worker dispatch is required")
    return reasons


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
