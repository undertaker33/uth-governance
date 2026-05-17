---
name: uth-docs
description: "Use in a UTH-enabled project, identified by .uth-governance/project.json, for project documentation governance based on code facts, including full-project baseline, scoped diff/range/version/module docs sync, module-split governance, onboarding-followup after existing-project takeover, current-state/context/archive/snapshot/migration/rules maintenance. Docs-only; no code edits, tests, Git writes, or skill changes. Stay silent without the UTH marker unless the user asks to enable UTH first."
---

# UTH Docs

## Purpose

Use `uth-docs` as the dedicated documentation-governance window for a UTH-enabled project.

`uth-docs` is not a lightweight index generator. Its authority is the current codebase:

- first-party source code
- build, dependency, workspace, and module declarations
- application/runtime entrypoints
- test and verification entrypoints
- scripts and local development commands
- existing README, AGENTS, docs, and old governance docs

Project documents are supporting evidence. When documents conflict with code facts, code facts win and docs must be corrected, archived, or marked blocked.

This skill governs documentation only. It does not modify source code, tests, build files, Git state, or `skills/`. If documentation governance reveals a code, test, ADR-content, release, or Git problem, route to the proper scene instead of fixing it here.

When this scene modifies governed Markdown, use `uth-utf8-guard` before and after the write. When this scene writes governed Markdown or emits closeout, use the persisted project documentation language.

## Modes

Choose one mode before reading broadly:

- `full-project-baseline`: build or re-confirm the full project documentation baseline from code facts.
- `scoped-sync`: sync docs from a specified git diff, git range, commit, tag, version, module, or file scope when a trusted full-project baseline already exists.
- `module-split`: after the user allows a large-project split, write the numbered module split plan such as `docs/context/00-module-split.md` or `docs/context/00-模块拆分.md` plus the context index/report, then pause for user confirmation.
- `module-governance`: govern confirmed modules in the order specified by the numbered module split plan; do not pause between modules unless blocked or context handoff is required.
- `onboarding-followup`: continue from `uth-onboarding existing-project` takeover handoff and complete full-project documentation governance.
- `state-cleanup`: clean the localized current-state entrypoint without pretending unconfirmed facts are confirmed.
- `archive-cleanup`: archive explicitly completed task packages and LW documents.
- `rules-maintenance`: update `AGENTS.md`, `docs/_governance/`, or templates.
- `snapshot`: save a historical state snapshot.
- `migration`: move specified old Design/Todo/Feedback/run docs into the current UTH layout.

If the mode is unclear, do read-only analysis and ask one concise question before writing.

## Read Protocol

Always start with the minimum routing context:

```text
AGENTS.md
.uth-governance/project.json
docs/README.md
entrypoints.current_state from `.uth-governance/project.json`
docs/_governance/README.md
```

If `.uth-governance/project.json` is missing, stay silent unless the user explicitly asks to enable UTH first.

Then read only what the selected mode needs:

- full-project-baseline: first-party source, build/dependency/workspace/module declarations, runtime entrypoints, test and verification entrypoints, scripts/local commands, README, AGENTS, docs, old governance docs, and module-local README or architecture docs.
- scoped-sync: existing trusted baseline evidence, `docs/context/README.md`, affected numbered module context files, the explicit diff/range/commit/tag/version/module/file scope, and code/docs needed to trace the impact.
- module-split: directory structure, build configuration, module declarations, entrypoint files, existing docs, and enough source to identify candidate module boundaries.
- module-governance: confirmed numbered module split plan, module queue, current module source/config/entrypoints/tests/scripts/docs, and cross-module dependency evidence.
- onboarding-followup: onboarding handoff snapshot, backup zip record, old docs named by the snapshot, full-project baseline sources, `docs/context/`, and the localized current-state entrypoint.
- state-cleanup: localized current-state entrypoint, active package indexes, and current context files as needed.
- archive-cleanup: localized current-state entrypoint, completed `docs/work/D*` packages, and completed `docs/LW-Work/LW*` docs.
- rules-maintenance: relevant `AGENTS.md`, `docs/_governance/`, templates, and user-specified files.
- snapshot: localized current-state entrypoint plus minimum source documents needed to describe the snapshot.
- migration: old source docs, target templates, and enough code facts to avoid migrating stale facts as current truth.

Full-project baseline reads exclude `.git/`, dependency folders, build outputs, caches, generated artifacts, and binary assets unless a binary asset is itself the documentation object under governance.

Do not default to reading all task packages, old Feedback, run logs, worker Prompts, or LW records unless the selected mode makes them in scope.

## Full-Project Baseline

Use `full-project-baseline` for first documentation governance, existing-project takeover, missing baseline, invalidated baseline, or any request that claims project-wide documentation governance.

Build a trustworthy baseline from code facts:

- source/build/module/runtime/test/script evidence read
- module responsibilities and non-responsibilities
- application and local-development entrypoints
- verification entrypoints
- documentation conflicts and stale facts
- current `docs/context/` and localized current-state status

Old documents are evidence, not authority. Keep facts only when current code evidence supports them. If a full baseline cannot be completed in the current window, return `blocked` or enter `module-split` after user confirmation.

## Scoped Sync

Use `scoped-sync` only when all of these are true:

- a trusted full-project documentation baseline already exists
- the user or task names an explicit diff, git range, commit, tag, version, module, or file scope
- the impact can be traced to affected modules, entrypoints, dependencies, tests, scripts, and docs
- after updates, the baseline is still trusted

If any condition is missing, first run `full-project-baseline` or pause with `blocked`. A scoped result must not be reported as full project documentation governance.

## Large Project Module Split

When the project is too large to establish a full baseline reliably in one window, explain the blocker and ask whether the user allows module split. Do not write the split plan before that approval.

After the user allows module split:

1. Read enough structure, build config, module declarations, entrypoints, and docs to identify candidate module boundaries.
2. Write or update a numbered module split plan with the module order, split rationale, source evidence, assumptions, and unfinished queue. Use `docs/context/00-module-split.md` for `en-US`; use `docs/context/00-模块拆分.md` for `zh-CN`; use the selected language for custom labels. Reserve the `00-` prefix for this split plan or context overview.
3. Write or update `docs/context/README.md`, the module index, and any necessary context report.
4. Report module list, responsibility assumptions, primary entrypoints, dependency traces, open confirmation questions, and recommended governance order.
5. Pause for user confirmation of the split result.

After confirmation, use `module-governance` and follow the numbered module split plan in order. Continue through the queue without pausing after each module. For each module:

- write its module context report
- name the module context report with a two-digit prefix in queue order: `01-...md` through `09-...md`, then `10-...md`, `11-...md`, and so on
- record code-fact source scope and excluded paths
- update `module_completed`, `module_current`, and `module_queue`
- note cross-module dependencies that still need later confirmation

Pause only when a blocker requires user input, the module split itself needs revision, or the context is too long to continue responsibly.

If context is too long, write a `docs/LW-Work/LW*.md` final record and provide a new-window prompt. The final record must include the original request, current goal, confirmed split, completed modules and context files, unfinished module queue, current module status, and next-step prompt. The new window must read that LW final record first before continuing.

## Completion Levels

Use exactly these completion levels:

- `full-project-docs-complete`: a full-project documentation baseline is established or re-confirmed.
- `scoped-docs-complete`: the specified diff/range/version/module/file scope is synced and the existing full-project baseline remains trusted.
- `blocked`: user choice, missing code facts, project size, unverified old-doc cleanup, or out-of-scene writes prevent completion.
- `partial/paused`: the user explicitly paused or asked only for a local maintenance slice.

Only `full-project-docs-complete` supports the statement `项目完整文档治理完成`.

`scoped-docs-complete` must be reported as `指定范围文档治理完成`. Do not shorten it to "complete" in a way that implies the whole project is governed.

When the user asks whether documentation governance is complete, default to the full-project interpretation unless the user explicitly asks about a named diff, range, version, module, or file scope.

## Document Language Preference

Before writing any governed Markdown, read `.uth-governance/project.json` and check `document_language`.

- If `document_language` exists, write new governance docs and closeout reports in that language.
- If it is missing, ask one concise question before the first Markdown write: `Which language should UTH use for project governance docs? I will save this as the project default.`
- Save the answer back to `.uth-governance/project.json` as `document_language` before writing other docs.
- Preserve commands, code identifiers, and schema keys exactly even when surrounding prose is localized.
- Keep hard entry filenames in English: `AGENTS.md` and every directory entry `README.md`.
- Name all other generated governance Markdown files in the selected `document_language`; for `zh-CN`, use Chinese basenames such as `docs/当前状态.md`, `docs/API契约.md`, `docs/数据模型.md`, `docs/领域术语.md`, `docs/界面规则.md`, and `docs/部署.md`; for `en-US`, use English basenames such as `docs/current-state.md`.
- For module context files, combine the required numeric prefix with the localized basename, for example `docs/context/01-backend.md` or `docs/context/01-后端.md`.
- If the selected language is `zh-CN`, closeout headings and prose must be Chinese. Do not output English labels such as `Read`, `Written`, or `Verification`.
- Do not translate existing documentation wholesale unless the user explicitly requests a language migration.
- If the user requests a one-off different language, ask whether to update the project default or only this output.

Use this marker shape:

```json
{
  "document_language": {
    "code": "zh-CN | en-US | bilingual | custom",
    "label": "Simplified Chinese | English | bilingual | user-specified label",
    "source": "user-selected",
    "selected_at": "YYYY-MM-DDTHH:mm:ss+08:00",
    "applies_to": "governance-docs-and-closeout-reports"
  }
}
```

## Write Rules

Allowed writes:

```text
.uth-governance/project.json   # document_language only
AGENTS.md
README.md
docs/README.md
docs/_governance/
entrypoints.current_state from `.uth-governance/project.json`
docs/context/
docs/LW-Work/          # module-split handoff final records only
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
build files
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

Module context Markdown files must be numbered with a two-digit prefix. Reserve `00-...md` for the module split plan or context overview, then use `01-...md` through `09-...md`, `10-...md`, and onward for module reports in governance order. `docs/context/README.md` remains the hard entry index and is not numbered.

Context files may contain:

- module responsibility and non-responsibility
- key entrypoints, dependencies, boundaries, and verification entrypoints
- stable risks that remain true in current code
- short links to relevant ADRs
- major task-package links only when they have long-term impact

Context files must not contain:

- diff logs
- worker Prompt text
- Feedback or Run Log copies
- routine LW records
- stale Design/Todo conclusions as current facts
- detailed ADR content copied into context

Context reports must identify source evidence and excluded paths when they support a baseline, scoped sync, or module governance claim.

## Current-State Rules

The localized current-state entrypoint is a current-state index, not a log. Read the actual path from `.uth-governance/project.json` `entrypoints.current_state`.

When cleaning it:

- keep only active phase, active task packages, active Todo items, current blockers, recent high-signal changes, latest verification evidence, next step, and current fact sources.
- remove completed, abandoned, superseded, or stale task indexes unless still needed for active routing.
- replace old facts with current facts from code-backed context or stable docs.
- do not paste old Feedback, Run Logs, or commit narratives.
- never turn `Needs uth-docs confirmation from code facts` into confirmed fact without code evidence.

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

Archive completed LW final records. Before moving items, ensure the localized current-state entrypoint no longer treats them as active. After moving items, update indexes and links that still point to the old location.

## Onboarding Follow-up

When called from `uth-onboarding existing-project`, `uth-docs onboarding-followup` is the documentation-governance executor for the existing-project takeover transaction.

Required behavior:

1. Read the onboarding handoff snapshot.
2. Verify the backup zip path is recorded.
3. Execute full-project baseline from code facts.
4. Classify every discovered old doc as current candidate, historical evidence, archive candidate, or discard candidate.
5. Migrate usable old docs into the current UTH layout.
6. Archive or remove unusable old docs only when the original path exists in the backup zip.
7. Rebuild or confirm `docs/context/`.
8. Clean the localized current-state entrypoint.
9. Return takeover completion evidence to `uth-onboarding`.

It must not claim full project documentation governance is complete while old docs remain unclassified, current-state still contains takeover-scope unconfirmed facts, module queues remain unfinished, or active takeover blockers exist.

The closeout returned to onboarding must include independent docs-scene evidence, such as `docs_scene_final_record`, `docs_scene_run_id`, or equivalent docs-scene closeout evidence, plus `docs_followup_completed=true`, `docs_completion_level=full-project-docs-complete`, and `return_to_onboarding=true`.

普通 `uth-docs` modes do not return to `uth-onboarding`. Return completion evidence only when the handoff fields identify an existing-project takeover: `origin_scene=uth-onboarding`, `origin_mode=existing-project`, `handoff_type=existing-project-takeover`, `takeover_session_id=ONBYYMMDDXX`, and `return_to=uth-onboarding`.

## Closeout

End with a closeout report rendered in the selected `document_language`. The field names below are semantic requirements; localize labels and prose while preserving literal paths, commands, skill names, and schema values.

```text
Mode:
Completion level:
Code-fact source scope:
Excluded paths:
Baseline status:
Scoped source:
Impact trace:
Module split:
Module split plan:
Module context numbering:
Filename language policy:
Module order followed:
Module current:
Module completed:
Module queue:
Old docs classified:
Cleanup backup verification:
Current-state cleanup:
Context reports:
UTF-8 guard:
Document language:
Verification:
Next route:
```

`Completion level: full-project-docs-complete` is required before saying `项目完整文档治理完成`.

`Completion level: scoped-docs-complete` must be reported as `指定范围文档治理完成`.

For onboarding follow-up, include old-doc classification status, cleanup backup verification, current-state cleanup, context rebuild/confirmation, active takeover blockers, and the evidence returned to `uth-onboarding`.

For module split or module governance, include module split status, current module, completed modules, remaining queue, pause status, and any `docs/LW-Work/LW*.md` handoff record.

`Verification` should normally say documentation-only, no tests/checks run. If Git closure is needed, set `Next route` to `uth-git` and wait for user confirmation.

Never claim code was verified from this scene. If documentation changes reveal code drift, mark `Needs implementation/debug/review route` instead of editing code.
