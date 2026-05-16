---
name: uth-docs
description: Use in a UTH-enabled project, identified by .uth-governance/project.json, for standalone documentation governance, documentation cleanup, AGENTS.md or docs/_governance maintenance, current-state cleanup, docs/context bootstrap or sync from commits, git ranges, stable code, or workspace changes, archive cleanup, snapshots, documentation migration, or the automatic follow-up after uth-onboarding existing-project handoff, including explicit uth-docs requests inside an enabled project. Maintains current facts and documentation structure without code edits, tests, Git writes, or skill changes. Stay silent in projects without the UTH marker unless the user explicitly asks to enable UTH first. Do not use for normal development Feedback, debugging fixes, architecture decision content, code review, or Git/release closure.
---

# UTH Docs

## Purpose

Use `uth-docs` for a dedicated documentation-governance window. Optimize what docs are read and written, keep current facts clean, and prevent task logs from becoming permanent context.

This skill governs documentation only. It does not implement code, run tests, commit, push, tag, release, or edit `skills/`.

If code, tests, or build files would need changes, stop and route to the proper implementation/debug scene. `uth-docs` closeout is documentation-only.

When this scene modifies governed Markdown, use `uth-utf8-guard` before and after the write.

## Modes

Choose one mode before reading broadly:

- `rules-maintenance`: update `AGENTS.md`, `docs/_governance/`, or templates.
- `context-bootstrap`: create the initial `docs/context/` structure.
- `context-sync`: update module context from user-specified commits, git ranges, stable code, or workspace changes.
- `state-cleanup`: clean `docs/current-state.md` by removing stale facts and stale indexes.
- `archive-cleanup`: move explicitly completed task packages and LW documents into archive.
- `snapshot`: save a historical state snapshot.
- `migration`: move old Design/Todo/Feedback/run docs into the current UTH layout.
- `onboarding-followup`: continue from an `uth-onboarding` existing-project handoff snapshot.

If the mode is unclear, do read-only analysis first and ask before writing.

## Read Protocol

Always start with the minimum routing context:

```text
AGENTS.md
docs/README.md
docs/current-state.md
docs/_governance/README.md
```

Then read only what the selected mode needs:

- rules-maintenance: relevant files under `docs/_governance/`, templates, and user-specified files.
- context-bootstrap: `docs/context/README.md` if present, directory tree, README, build/config files, and key entry points.
- context-sync: `docs/context/README.md`, affected module context files, user-specified commits or git range, and only the code/docs needed to verify current facts.
- state-cleanup: `docs/current-state.md`, active task package indexes, and context README/module files as needed.
- archive-cleanup: `docs/current-state.md`, completed `docs/work/D*` packages, and completed `docs/LW-Work/LW*` docs.
- snapshot: `docs/current-state.md` and the minimum files needed to describe the snapshot.
- migration: old source docs plus target templates.
- onboarding-followup: `docs/snapshots/ONB*-existing-project-handoff.md`, `docs/current-state.md`, old docs named by the snapshot, and only the code/config needed to confirm current facts.

Do not default to reading all of `docs/`, all task packages, old Design docs, old Feedback, run logs, worker Prompts, or LW records.

## Write Rules

Allowed writes:

```text
AGENTS.md
README.md
docs/README.md
docs/_governance/
docs/current-state.md
docs/context/
docs/work/              # migration or archive preparation only
docs/archive/
docs/state/snapshots/
docs/decisions/README.md or indexes only
docs/changelogs/README.md or indexes only
```

Forbidden writes:

```text
source code
tests
build outputs
source/test/build edits of any kind
skills/
skills/uth-sp-*/
git metadata
ADR decision content
release changelog content
```

Do not run validation commands or tests in this skill. If existing validation evidence is referenced, mark it as existing evidence and not reverified.

## UTF-8 Guard

Before and after modifying any governed Markdown, call `uth-utf8-guard` or run its equivalent checker.

Required for:

- `AGENTS.md`
- root `README.md`
- `docs/**/*.md`
- task-package Markdown
- governance templates and manuals

The guard must check UTF-8 decoding, obvious mojibake, and Markdown fence balance. If the guard fails, repair the document before closeout.

## Context Rules

`docs/context/` is the module-level current-facts layer. It is maintained only by this documentation-governance window.

Context files may contain:

- module responsibility and non-responsibility.
- key entry points, dependencies, boundaries, and verification entry points.
- stable risks that remain true in the current code.
- short links to relevant ADRs.
- major task-package links only when they have long-term impact.

Context files must not contain:

- diff logs.
- worker Prompt text.
- Feedback or Run Log copies.
- routine LW records.
- stale Design/Todo conclusions as current facts.
- detailed ADR content copied into context.

Module context may include source evidence when it is useful, but context sync must not block on a Git baseline:

```md
## Source Evidence

- Commit:
- Source: commit / git range / stable code / workspace changes / code read
- Updated at:
```

If the workspace is uncommitted, or the user explicitly asks to sync from workspace changes, record the code/diff source that was actually read or omit the section. Do not delay context or report writeback waiting for a later Git commit.

For `context-bootstrap`, simple or new projects may be split by technical boundary such as frontend, backend, data, and deployment. For complex projects, read enough of the repository to propose module boundaries, then wait for user confirmation before creating module files.

For `context-sync`, update only facts that changed: responsibilities, entry points, dependencies, boundaries, verification routes, or still-valid risks. Do not write a commit-by-commit narrative.

## Current-State Rules

`docs/current-state.md` is a current-state index, not a log.

When cleaning it:

- keep only active phase, active task packages, active Todo items, current blockers, recent high-signal changes, latest verification evidence, next step, and current fact sources.
- remove completed, abandoned, superseded, or stale task indexes unless they are still needed for active routing.
- replace old facts with current facts from `docs/context/` or stable docs.
- do not paste old Feedback, Run Logs, or commit narratives.

Because `uth-docs` is usually called when code is stable, old current-state indexes may be cleaned aggressively when the evidence is clear.

## AGENTS.md Rules

`AGENTS.md` is allowed only for stable repo-level entry instructions.

Add or update `AGENTS.md` when:

- a repository-wide rule must be known at every session start.
- an entry document or command index changes.
- the same problem appears repeatedly in development Feedback and should become a stable guardrail.

Do not put templates, task logs, single-task lessons, full governance rules, old Design summaries, or long process explanations into `AGENTS.md`.

## ADR and Changelog Boundaries

ADR content changes belong to `uth-design`, especially new decisions, superseded decisions, or decision-status changes.

`uth-docs` may only:

- fix ADR index links.
- link ADRs from context or current-state without copying details.
- mark that an ADR update is needed and route to `uth-design`.

Release changelog content belongs to `uth-git` or the release flow. `uth-docs` may maintain changelog indexes or documentation structure only.

## Archive Rules

Use archive cleanup only when the user asks for cleanup/archive and the items are clearly completed.

Recommended archive layout:

```text
docs/archive/
+-- work/
|   +-- DYYMMDDXX-task-title/
+-- LW-Work/
    +-- LWYYMMDDXX-light-task-title.md
```

Archive completed LW final records. Before moving items, ensure `docs/current-state.md` no longer treats them as active. After moving items, update indexes and links that still point to the old location.

## Onboarding Follow-up

When called from `uth-onboarding` after an existing-project handoff:

- read the onboarding snapshot first
- verify the backup zip path is recorded before migrating old docs
- classify old docs as current candidate, historical evidence, archive candidate, or discard candidate
- rebuild or propose `docs/context/` from code facts, not from old task logs alone
- clean `docs/current-state.md` so old facts do not remain active by accident
- extract only stable repeated rules from old `AGENTS.md`; do not copy the whole old file into the new one
- keep the onboarding snapshot as historical handoff evidence

## Closeout

End with:

```text
Mode:
Read:
Written:
Not touched:
UTF-8 guard:
Current-state cleanup:
Context source evidence:
Archived:
ADR/changelog boundary:
Verification:
Next route:
```

`Verification` should normally say documentation-only, no tests/checks run. If Git closure is needed, set `Next route` to `uth-git` and wait for user confirmation.

Never claim code was verified from this scene. If documentation changes reveal code drift, mark `Needs implementation/debug/review route` instead of editing code.
