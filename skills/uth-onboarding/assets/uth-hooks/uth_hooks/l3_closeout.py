from __future__ import annotations

from typing import Any

from .common import (
    L3_SCENES,
    as_bool,
    check_code_verification,
    check_positive_claim_evidence,
    design_patch_authorized,
    get_changed_files,
    get_verification,
    has_code_change,
    has_markdown_doc_change,
    listify,
    parse_int,
    result,
)

def check_l3_closeout(ctx: dict[str, Any]) -> list[dict[str, Any]]:
    scene = ctx.get("active_scene")
    if scene not in L3_SCENES:
        return [result("BLOCK", "l3-scene-unsupported", f"L3 closeout requires one of {sorted(L3_SCENES)}.")]

    findings: list[dict[str, Any]] = []
    findings.extend(check_positive_claim_evidence(ctx))
    findings.extend(check_closeout_report_language(ctx))

    if scene == "uth-onboarding":
        findings.extend(check_l3_onboarding(ctx))
    elif scene == "uth-dev":
        findings.extend(check_l3_dev(ctx))
    elif scene == "uth-debug":
        findings.extend(check_l3_debug(ctx))
    elif scene == "uth-design":
        findings.extend(check_l3_design(ctx))
    elif scene == "uth-review":
        findings.extend(check_l3_review(ctx))
    elif scene == "uth-docs":
        findings.extend(check_l3_docs(ctx))
    elif scene == "uth-git":
        findings.extend(check_l3_git(ctx))
    elif scene == "uth-context-trace":
        findings.extend(check_l3_context_trace(ctx))

    return findings or [result("PASS", "l3-closeout-pass", "L3 closeout gate passed.")]


def check_l3_onboarding(ctx: dict[str, Any]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    mode = ctx.get("mode")
    if mode not in {"new-project", "existing-project"}:
        findings.append(result("BLOCK", "onboarding-mode-missing", "uth-onboarding requires mode new-project or existing-project."))
    if not as_bool(ctx.get("project_marker_written")):
        findings.append(result("BLOCK", "project-marker-missing", "uth-onboarding closeout requires .uth-governance/project.json."))
    if not as_bool(ctx.get("current_state_written")):
        findings.append(result("BLOCK", "initial-current-state-missing", "uth-onboarding closeout requires initial docs/current-state.md."))
    if not as_bool(ctx.get("hook_tools_copied")):
        findings.append(result("BLOCK", "hook-tools-missing", "uth-onboarding closeout requires project-local tools/uth-hooks copied."))
    if has_markdown_doc_change(ctx) and not document_language_ready(ctx):
        findings.append(result("BLOCK", "document-language-missing", "First governed Markdown writes require a selected and persisted project document_language."))
    if has_markdown_doc_change(ctx) and not as_bool(ctx.get("utf8_guard_passed")):
        findings.append(result("BLOCK", "utf8-guard-missing", "Governed Markdown changes require UTF-8/fence guard evidence."))
    if mode == "existing-project":
        if not as_bool(ctx.get("backup_zip_created")):
            findings.append(result("BLOCK", "onboarding-backup-missing", "existing-project onboarding requires docs backup zip before docs writes."))
        if not as_bool(ctx.get("handoff_snapshot_created")):
            findings.append(result("BLOCK", "onboarding-snapshot-missing", "existing-project onboarding requires handoff snapshot under docs/snapshots/."))
        if ctx.get("next_scene") != "uth-docs" and not as_bool(ctx.get("user_paused_after_onboarding")):
            findings.append(result("BLOCK", "onboarding-docs-handoff-missing", "existing-project onboarding must hand off to uth-docs unless the user paused."))
    if as_bool(ctx.get("git_write_performed")):
        findings.append(result("BLOCK", "git-write-in-onboarding", "uth-onboarding must not perform Git writes."))
    if has_code_change(ctx) or as_bool(ctx.get("code_files_modified")):
        findings.append(result("BLOCK", "code-write-in-onboarding", "uth-onboarding must not modify source/test code."))
    return findings


def check_l3_dev(ctx: dict[str, Any]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    mode = ctx.get("mode")
    changed = get_changed_files(ctx)
    if as_bool(ctx.get("files_changed", True)) and not changed and not as_bool(ctx.get("no_files_changed")):
        findings.append(result("BLOCK", "changed-files-missing", "uth-dev closeout requires changed files or explicit no-files-changed."))

    findings.extend(check_code_verification(ctx))

    if mode == "light-dev":
        if not as_bool(ctx.get("lw_final_record_written")):
            findings.append(result("BLOCK", "lw-final-missing", "light-dev closeout requires the final LW record at task completion."))
    elif mode in {"formal-dev", "todo-implementation"}:
        if not as_bool(ctx.get("feedback_written")) and not ctx.get("feedback_not_written_reason"):
            findings.append(result("BLOCK", "feedback-missing", "formal development closeout requires Feedback or an explicit reason."))

    if as_bool(ctx.get("git_write_performed")):
        findings.append(result("BLOCK", "git-write-in-dev", "uth-dev must not perform Git writes; hand off to uth-git after user confirmation."))
    return findings


def check_l3_debug(ctx: dict[str, Any]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    if not ctx.get("root_cause") and not as_bool(ctx.get("root_cause_unknown")):
        findings.append(result("BLOCK", "root-cause-status-needed", "uth-debug closeout must state root cause or explicitly say it remains unknown."))
    if has_code_change(ctx) and not ctx.get("fix_scope"):
        findings.append(result("BLOCK", "fix-scope-missing", "Debug repair closeout requires fix scope."))
    findings.extend(check_code_verification(ctx))
    if as_bool(ctx.get("git_write_performed")):
        findings.append(result("BLOCK", "git-write-in-debug", "uth-debug must not perform Git writes; hand off to uth-git after user confirmation."))
    return findings


def check_l3_design(ctx: dict[str, Any]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    if has_code_change(ctx):
        if not design_patch_authorized(ctx):
            findings.append(result("ASK", "design-patch-authorization-needed", "Code patch in uth-design requires asking the user for explicit authorization."))
        if as_bool(ctx.get("design_patch_scope_expanded")):
            findings.append(result("BLOCK", "design-patch-scope-expanded", "Expanded code patch must switch to uth-dev or uth-debug."))
        findings.extend(check_code_verification(ctx))
    if as_bool(ctx.get("feature_implementation_started")):
        findings.append(result("BLOCK", "implementation-in-design", "Feature implementation belongs to uth-dev, not uth-design."))
    return findings


def check_l3_review(ctx: dict[str, Any]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    if has_code_change(ctx) or as_bool(ctx.get("code_files_modified")):
        findings.append(result("BLOCK", "code-write-in-review", "uth-review forbids source/test code writes; route fixes to uth-debug or uth-dev."))

    reviewing_code = as_bool(ctx.get("review_target_code_changed") or ctx.get("reviewing_code_changes"))
    recommendation = str(ctx.get("recommendation", "")).strip().lower()
    if reviewing_code and recommendation in {"pass", "accepted", "ready", "mergeable"}:
        findings.extend(check_code_verification(ctx, force=True))
    if reviewing_code and recommendation in {"pass with risk", "pass-with-risk"}:
        verification = get_verification(ctx)
        warnings = parse_int(verification.get("warnings"))
        exceptions = parse_int(verification.get("exceptions"))
        has_counts = warnings is not None and exceptions is not None
        has_risk = has_counts and (warnings > 0 or exceptions > 0)
        if has_risk and not as_bool(verification.get("waiver_granted") or ctx.get("waiver_granted") or ctx.get("review_risk_accepted")):
            findings.append(result("ASK", "review-risk-waiver-needed", "pass with risk for warnings/exceptions requires user risk waiver."))
    if as_bool(ctx.get("static_review_only")) and recommendation in {"pass", "accepted", "ready", "mergeable"}:
        findings.append(result("BLOCK", "static-review-positive-claim", "Static-only review cannot claim pass/accepted/ready; use pass with risk or needs follow-up."))
    if as_bool(ctx.get("git_write_performed")):
        findings.append(result("BLOCK", "git-write-in-review", "uth-review must not perform Git writes."))
    return findings


def check_l3_docs(ctx: dict[str, Any]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    if has_code_change(ctx) or as_bool(ctx.get("code_files_modified")):
        findings.append(result("BLOCK", "code-write-in-docs", "uth-docs is documentation-only; route code changes to implementation/debug scenes."))
    if has_markdown_doc_change(ctx) and not document_language_ready(ctx):
        findings.append(result("BLOCK", "document-language-missing", "uth-docs Markdown writes require a selected and persisted project document_language."))
    if has_markdown_doc_change(ctx) and not as_bool(ctx.get("utf8_guard_passed")):
        findings.append(result("BLOCK", "utf8-guard-missing", "Governed Markdown changes require UTF-8/fence guard evidence."))
    context_touched = as_bool(ctx.get("context_touched")) or any(path.startswith("docs/context/") for path in get_changed_files(ctx))
    if context_touched and not (ctx.get("context_source_evidence") or ctx.get("context_source_omitted_reason")):
        findings.append(result("BLOCK", "context-source-missing", "docs/context changes require source evidence or an explicit omission reason."))
    archive_touched = as_bool(ctx.get("archive_touched")) or any(path.startswith("docs/archive/") for path in get_changed_files(ctx))
    if archive_touched:
        if not as_bool(ctx.get("archive_paths_listed")):
            findings.append(result("BLOCK", "archive-paths-missing", "Archive cleanup requires before/after paths."))
        if not as_bool(ctx.get("current_state_active_cleaned")):
            findings.append(result("BLOCK", "archive-current-state-cleanup-missing", "Archive cleanup must confirm current-state no longer lists archived items as active."))
    if as_bool(ctx.get("tests_run")) or as_bool(ctx.get("compile_run")):
        findings.append(result("WARN", "docs-validation-run", "uth-docs should report documentation-only; do not claim code validation from this scene."))
    return findings


def check_l3_git(ctx: dict[str, Any]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    git_write_performed = as_bool(ctx.get("git_write_performed"))
    if not git_write_performed:
        if as_bool(ctx.get("git_plan_present")) or as_bool(ctx.get("plan_only")):
            findings.append(result("PASS", "git-plan-only", "Git plan produced; no Git writes executed."))
        else:
            findings.append(result("BLOCK", "git-plan-missing", "uth-git closeout without Git writes requires a shown plan or explicit plan-only marker."))
        return findings

    if not as_bool(ctx.get("user_git_confirmed")):
        findings.append(result("BLOCK", "git-confirmation-missing", "uth-git closeout requires explicit user confirmation for Git writes."))
    if git_write_performed and not listify(ctx.get("commands_executed")):
        findings.append(result("BLOCK", "git-commands-missing", "Git closeout requires executed commands."))
    if git_write_performed and not ctx.get("final_status"):
        findings.append(result("BLOCK", "git-final-status-missing", "Git closeout requires final branch/status summary."))
    if as_bool(ctx.get("commit_created")) and not ctx.get("commit_hash"):
        findings.append(result("BLOCK", "commit-hash-missing", "Created commit requires commit hash evidence."))
    if as_bool(ctx.get("pr_created")) and not ctx.get("pr_reference"):
        findings.append(result("BLOCK", "pr-reference-missing", "Created PR requires PR reference evidence."))
    if as_bool(ctx.get("tag_created")) and not ctx.get("tag_name"):
        findings.append(result("BLOCK", "tag-name-missing", "Created tag requires tag name evidence."))
    if as_bool(ctx.get("release_or_tag")) and not as_bool(ctx.get("changelog_ok")):
        findings.append(result("BLOCK", "release-changelog-missing", "Release/tag closeout requires changelog rule satisfaction."))
    if as_bool(ctx.get("light_dev_commit")) and not as_bool(ctx.get("lw_git_baseline_appended")):
        findings.append(result("BLOCK", "lw-git-baseline-missing", "light-dev Git closeout must append Git baseline to the existing LW final record."))
    if as_bool(ctx.get("formal_task_commit")) and not (
        as_bool(ctx.get("feedback_git_baseline_appended")) or ctx.get("feedback_git_baseline_omitted_reason")
    ):
        findings.append(result("BLOCK", "feedback-git-baseline-missing", "formal task Git closeout must append Git baseline to Feedback or state why it was omitted."))
    if as_bool(ctx.get("lw_record_included_in_git") or ctx.get("git_baseline_record_included_in_git")) and not as_bool(ctx.get("lw_second_confirmation") or ctx.get("baseline_second_confirmation")):
        findings.append(result("BLOCK", "baseline-second-confirmation-missing", "Including Git-baseline record changes in Git requires a second shown diff and confirmation."))
    if as_bool(ctx.get("formal_task_commit")) and not (ctx.get("associated_task_package") or ctx.get("associated_todo")):
        findings.append(result("BLOCK", "formal-task-link-missing", "Formal task Git closeout must record associated task package or Todo when known."))

    if as_bool(ctx.get("underlying_code_changed")):
        findings.extend(check_code_verification(ctx, force=True))
    return findings


def check_l3_context_trace(ctx: dict[str, Any]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    if get_changed_files(ctx) or as_bool(ctx.get("files_modified")):
        findings.append(result("BLOCK", "context-trace-modified-files", "uth-context-trace is read-only and must not modify files."))
    if not as_bool(ctx.get("active_and_archived_separated")):
        findings.append(result("BLOCK", "evidence-separation-missing", "Context trace must separate active/current facts from historical/archive evidence."))
    if not ctx.get("recommended_next_scene"):
        findings.append(result("BLOCK", "next-scene-missing", "Context trace should recommend the next scene or state none."))
    return findings


def document_language_ready(ctx: dict[str, Any]) -> bool:
    available = as_bool(ctx.get("document_language_available") or ctx.get("project_marker_document_language"))
    if available:
        return True
    selected = as_bool(ctx.get("document_language_selected"))
    persisted = as_bool(
        ctx.get("document_language_persisted")
        or ctx.get("project_marker_document_language")
    )
    return selected and persisted


def check_closeout_report_language(ctx: dict[str, Any]) -> list[dict[str, Any]]:
    if not closeout_language_expected(ctx):
        return []
    if as_bool(ctx.get("closeout_report_language_applied")):
        return []
    return [
        result(
            "BLOCK",
            "closeout-report-language-missing",
            "Scene closeout report must be rendered in the selected project document_language.",
        )
    ]


def closeout_language_expected(ctx: dict[str, Any]) -> bool:
    return as_bool(
        ctx.get("document_language_available")
        or ctx.get("project_marker_document_language")
        or ctx.get("document_language_selected")
        or ctx.get("document_language_persisted")
    )
