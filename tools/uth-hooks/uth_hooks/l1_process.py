from __future__ import annotations

import re
from typing import Any

from .common import CODE_CHANGING_SCENES, as_bool, check_document_preflight, result


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

FORMAL_DEV_IMPLEMENTATION_MODES = {"formal-dev", "todo-implementation"}
FORMAL_DEV_DESIGN_ONLY_MODES = {"todo-breakdown", "handoff-from-design"}
DOCUMENT_WRITE_INTENT_KEYS = {
    "docs_write_intent",
    "document_write_intent",
    "governed_markdown_write",
    "markdown_write_intent",
    "task_document_write_intent",
}
WEB_DESIGN_TARGETS = {
    "web",
    "web-page",
    "web-ui",
    "webapp",
    "web-app",
    "website",
    "frontend",
    "frontend-web",
    "browser-ui",
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

    findings.extend(check_subagent_issue_loop(ctx))

    findings.extend(check_formal_dev_package(ctx))

    if document_write_intent_present(ctx):
        findings.extend(check_document_preflight(ctx))

    findings.extend(check_web_design_method_skill(ctx))

    if ctx.get("mode") == "light-dev":
        findings.extend(check_light_dev_model_boundary(ctx, worker))

    if as_bool(ctx.get("require_uth_sp_decision", ctx.get("active_scene") in CODE_CHANGING_SCENES)):
        uth_sp = ctx.get("uth_sp", {})
        if not as_bool(uth_sp.get("decision_recorded")):
            findings.append(result("BLOCK", "uth-sp-decision-missing", "Sub-scene must record UTH-SP trigger decision before execution."))
        else:
            findings.append(result("PASS", "uth-sp-decision-recorded", "UTH-SP trigger decision is recorded."))

    return findings or [result("PASS", "l1-pass", "L1 process gate passed.")]


def check_formal_dev_package(ctx: dict[str, Any]) -> list[dict[str, Any]]:
    if ctx.get("active_scene") != "uth-dev":
        return []
    mode = ctx.get("mode")
    if mode not in FORMAL_DEV_IMPLEMENTATION_MODES | FORMAL_DEV_DESIGN_ONLY_MODES:
        return []

    findings: list[dict[str, Any]] = []
    if not task_package_present(ctx):
        findings.append(
            result(
                "BLOCK",
                "formal-task-package-missing",
                "Formal development requires an active docs/work/D* task package before execution.",
            )
        )
    if not accepted_design_present(ctx):
        findings.append(
            result(
                "BLOCK",
                "formal-design-missing",
                "Formal development requires an accepted task-package Design before Todo or implementation work.",
            )
        )
    if mode in FORMAL_DEV_IMPLEMENTATION_MODES and not active_todo_present(ctx):
        findings.append(
            result(
                "BLOCK",
                "formal-todo-missing",
                "Formal implementation requires a current task-package Todo before code work.",
            )
        )

    if findings:
        return findings
    return [result("PASS", "formal-task-package-evidence-present", "Formal task package, accepted Design, and required Todo evidence are present.")]


def task_package_present(ctx: dict[str, Any]) -> bool:
    if any(text_value(ctx, key) for key in ("task_package", "task_package_path", "formal_task_package", "associated_task_package")):
        return True
    task_package = ctx.get("task_package")
    if isinstance(task_package, dict):
        return any(text_value(task_package, key) for key in ("path", "id", "package_path")) or as_bool(task_package.get("created"))
    return as_bool(ctx.get("formal_task_package_created"))


def accepted_design_present(ctx: dict[str, Any]) -> bool:
    if any(text_value(ctx, key) for key in ("accepted_design_path", "accepted_design")):
        return True
    design = ctx.get("design")
    if isinstance(design, dict):
        if text_value(design, "accepted_path") or text_value(design, "accepted_design_path"):
            return True
        if (text_value(design, "path") or as_bool(design.get("written"))) and as_bool(design.get("accepted")):
            return True
    if (text_value(ctx, "design_path") or as_bool(ctx.get("design_written"))) and as_bool(ctx.get("design_accepted")):
        return True
    return False


def active_todo_present(ctx: dict[str, Any]) -> bool:
    if any(text_value(ctx, key) for key in ("active_todo", "current_todo", "todo_path", "associated_todo", "todo_id")):
        return True
    todo = ctx.get("todo")
    if isinstance(todo, dict):
        return any(text_value(todo, key) for key in ("path", "id", "todo_path")) or as_bool(todo.get("written"))
    return as_bool(ctx.get("todo_written"))


def text_value(ctx: dict[str, Any], key: str) -> str:
    value = ctx.get(key)
    if value is None:
        return ""
    return str(value).strip()


def document_write_intent_present(ctx: dict[str, Any]) -> bool:
    if any(as_bool(ctx.get(key)) for key in DOCUMENT_WRITE_INTENT_KEYS):
        return True
    writeback = ctx.get("writeback")
    if isinstance(writeback, dict):
        return any(as_bool(writeback.get(key)) for key in DOCUMENT_WRITE_INTENT_KEYS)
    return False


def check_web_design_method_skill(ctx: dict[str, Any]) -> list[dict[str, Any]]:
    if ctx.get("active_scene") != "uth-design" or not web_page_design_intent(ctx):
        return []
    if ui_ux_pro_max_invoked(ctx):
        return [result("PASS", "web-design-uiux-skill-invoked", "Web page design has invoked ui-ux-pro-max.")]
    return [
        result(
            "BLOCK",
            "web-design-uiux-skill-missing",
            "Web page design in uth-design requires ui-ux-pro-max; Android UI/UX design is exempt.",
        )
    ]


def web_page_design_intent(ctx: dict[str, Any]) -> bool:
    if as_bool(ctx.get("web_page_design") or ctx.get("web_ui_design") or ctx.get("website_design")):
        return True
    targets = [
        str(ctx.get(key, "")).strip().lower().replace("_", "-").replace(" ", "-")
        for key in ("design_target", "ui_target", "surface", "platform")
        if ctx.get(key)
    ]
    if any("android" in target for target in targets):
        return False
    return any(
        target in WEB_DESIGN_TARGETS
        or "web" in target
        or "website" in target
        or "frontend" in target
        or "browser-ui" in target
        for target in targets
    )


def ui_ux_pro_max_invoked(ctx: dict[str, Any]) -> bool:
    if as_bool(ctx.get("ui_ux_pro_max_invoked") or ctx.get("uiux_pro_max_invoked")):
        return True
    for key in ("ui_ux_pro_max", "uiux_pro_max"):
        value = ctx.get(key)
        if isinstance(value, dict) and as_bool(value.get("invoked") or value.get("active")):
            return True
    return False


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

    if source == "uth-design" and target == "uth-dev":
        if not as_bool(transition.get("explicit_handoff")):
            findings.append(result("BLOCK", "design-dev-handoff-missing", "design -> dev requires explicit uth-dev handoff."))
        elif not as_bool(
            transition.get("user_confirmed")
            or transition.get("user_confirmed_handoff")
            or transition.get("confirmed_by_user")
        ):
            findings.append(result("ASK", "design-dev-user-confirmation-missing", "design -> dev must stop and get explicit user confirmation before entering uth-dev."))
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


def check_subagent_issue_loop(ctx: dict[str, Any]) -> list[dict[str, Any]]:
    loops = subagent_issue_loops(ctx)
    if not loops:
        return []

    findings: list[dict[str, Any]] = []
    for loop in loops:
        if not subagent_issue_loop_active(loop):
            continue

        origin_worker = first_text(
            loop,
            "origin_worker_id",
            "owner_worker_id",
            "task_owner_worker_id",
            "worker_id",
            "origin_worker",
        )
        evaluator = first_text(
            loop,
            "finding_evaluator_id",
            "origin_evaluator_id",
            "reviewer_id",
            "evaluator_id",
            "issue_evaluator_id",
            "finding_author_id",
        )
        fix_worker = first_text(loop, "fix_worker_id", "assigned_fix_worker_id", "repair_worker_id")
        recheck_evaluator = first_text(
            loop,
            "recheck_evaluator_id",
            "recheck_reviewer_id",
            "reviewer_recheck_id",
            "verification_evaluator_id",
        )

        if not origin_worker or not evaluator:
            findings.append(
                result(
                    "BLOCK",
                    "subagent-issue-owner-missing",
                    "Subagent issue loop requires origin worker id and finding evaluator id.",
                )
            )
            continue

        if fix_required(loop) and not fix_worker:
            findings.append(
                result(
                    "BLOCK",
                    "subagent-fix-worker-missing",
                    "Reviewer finding must be routed back to the worker that produced the faulty output.",
                )
            )
        elif fix_worker and fix_worker != origin_worker:
            findings.append(
                result(
                    "BLOCK",
                    "subagent-fix-worker-mismatch",
                    "Reviewer finding must be fixed by the original worker that produced the faulty output.",
                )
            )

        if recheck_required(loop) and not recheck_evaluator:
            findings.append(
                result(
                    "BLOCK",
                    "subagent-recheck-evaluator-missing",
                    "Completed subagent fix must return to the evaluator that raised the finding.",
                )
            )
        elif recheck_evaluator and recheck_evaluator != evaluator:
            findings.append(
                result(
                    "BLOCK",
                    "subagent-recheck-evaluator-mismatch",
                    "Subagent finding must be rechecked by the evaluator that raised it.",
                )
            )

        if issue_closure_claimed(loop) and not as_bool(loop.get("recheck_completed") or loop.get("recheck_passed")):
            findings.append(
                result(
                    "BLOCK",
                    "subagent-issue-loop-open",
                    "Subagent finding cannot be closed or advanced until the original evaluator rechecks it.",
                )
            )

    return findings or [result("PASS", "subagent-issue-loop-pass", "Subagent issue loop keeps origin worker fix and origin evaluator recheck.")]


def subagent_issue_loops(ctx: dict[str, Any]) -> list[dict[str, Any]]:
    raw = ctx.get("subagent_issue_loop") or ctx.get("subagent_issue_loops") or ctx.get("review_issue_loop")
    if isinstance(raw, dict):
        return [raw]
    if isinstance(raw, list):
        return [item for item in raw if isinstance(item, dict)]
    return []


def subagent_issue_loop_active(loop: dict[str, Any]) -> bool:
    if as_bool(loop.get("issue_found") or loop.get("finding_found") or loop.get("issues_found")):
        return True
    return any(
        key in loop
        for key in (
            "origin_worker_id",
            "owner_worker_id",
            "task_owner_worker_id",
            "finding_evaluator_id",
            "origin_evaluator_id",
            "reviewer_id",
            "evaluator_id",
            "fix_worker_id",
            "recheck_evaluator_id",
            "issue_closed",
        )
    )


def fix_required(loop: dict[str, Any]) -> bool:
    return as_bool(
        loop.get("issue_found")
        or loop.get("finding_found")
        or loop.get("issues_found")
        or loop.get("fix_assigned")
        or loop.get("fix_started")
        or loop.get("fix_completed")
        or loop.get("issue_closed")
        or loop.get("mark_task_complete")
        or loop.get("moving_to_next_task")
    )


def recheck_required(loop: dict[str, Any]) -> bool:
    return as_bool(
        loop.get("fix_completed")
        or loop.get("issue_closed")
        or loop.get("mark_task_complete")
        or loop.get("moving_to_next_task")
    )


def issue_closure_claimed(loop: dict[str, Any]) -> bool:
    return as_bool(
        loop.get("issue_closed")
        or loop.get("finding_closed")
        or loop.get("mark_task_complete")
        or loop.get("moving_to_next_task")
    )


def first_text(ctx: dict[str, Any], *keys: str) -> str:
    for key in keys:
        value = text_value(ctx, key)
        if value:
            return value
    return ""
