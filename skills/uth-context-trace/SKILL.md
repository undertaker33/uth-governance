---
name: uth-context-trace
description: Use in a UTH-enabled project, identified by .uth-governance/project.json, or when the user explicitly invokes uth-context-trace, to locate task-document evidence for a request, bug, review, implementation boundary, archived work item, onboarding handoff snapshot, or documentation conflict. Finds related active or archived task package, Design, Todo, Feedback, worker Prompt, Run Log, LW-Work record, onboarding snapshot, ADR, and current fact sources by following the docs entry README and current-state index. Stay silent in projects without the UTH marker unless the user explicitly asks to enable UTH first. This is a read-only evidence tracing skill; do not use it for code-location search, implementation, review judgment, document edits, or Git changes.
---

# uth-context-trace

## Purpose

Use this skill to find the document evidence chain for a task or problem.

This skill answers:

- which task package is related
- which Design/Todo/Feedback/worker Prompt/Run Log/LW record matters
- which files are current fact sources
- which files are only historical evidence
- whether the relevant evidence is active or archived
- whether an onboarding snapshot is relevant

It does not judge code quality, locate implementation files, modify documents, or repair anything.

## Trigger Conditions

Use this skill when:

- Debug needs to reconstruct how a bug was introduced
- Review needs to confirm task boundaries or worker instructions
- the user asks which document corresponds to a request, bug, or change
- the user explicitly asks to locate archived work or old evidence
- implementation and documents disagree, and current facts must be separated from historical evidence
- a later scene needs the existing-project onboarding handoff snapshot
- another UTH skill asks for a Design/Todo/Feedback/worker Prompt/Run/LW evidence chain

Do not use this skill when:

- the task is only code location search
- the target file and change scope are already clear
- the user asks for a simple small implementation
- the user asks for broad docs cleanup; use `uth-docs`
- the user asks for code review; use `uth-review`

## Entry Protocol

Start with:

- `Scene: uth-context-trace`
- trace target: request / bug / review / task / commit / document conflict
- known anchors: user text, task id, file path, commit hash, Todo id, error text, or module
- read-only confirmation

If there is no usable anchor, ask one concise question or fall back to the docs entrypoint and current-state index. Do not scan all docs.

## Lookup Order

Follow structure, not guesses:

1. Read the repository agent entry, usually `AGENTS.md`, if it exists.
2. Read the docs entry README, usually `docs/README.md` or another README that explains the docs structure.
3. Read the current-state index only after the docs entrypoint confirms where it lives, usually `docs/current-state.md`.
4. Follow active pointers to current task packages, current Design, current Todo, current facts, or relevant ADRs.
5. Search only the likely document areas named by the entrypoint, current-state, or user-provided anchor.

Do not enter `docs/archive/` during normal tracing. Enter archive only when:

- the user explicitly asks for archived or historical evidence
- the anchor names an archived task package, archived LW record, old task id, or old commit
- active docs say the item was archived
- no active evidence exists and archive is the narrow next place to check

If the docs structure entrypoint is missing or unclear:

- report that clearly
- inspect only nearby README files and obvious `docs/work`, `docs/archive`, `docs/decisions`, `docs/context`, or `docs/changelogs` indexes if present
- do not invent missing structure or create files

## Search Scope

Allowed read targets:

- docs structure README
- current-state index
- active task package
- `docs/work/DYYMMDDXX-*/00-DYYMMDDXX-design.md`
- Todo files in the active or matching task package
- Feedback files in the active or matching task package
- `prompts/` worker prompt files only when related to the target
- `runs/` records only when related to the target
- `docs/LW-Work/` records only when the issue follows a lightweight committed change
- `docs/archive/work/` or `docs/archive/LW-Work/` only when archive is explicitly in scope
- `docs/snapshots/ONB*-existing-project-handoff.md` only when onboarding handoff context is explicitly needed or current-state points to it
- ADRs only for the same decision area
- `docs/context/*.md` only as current fact sources when relevant
- Git commit metadata only when the user or LW record points to a commit

Default to not reading:

- all docs
- all old task packages
- all archived task packages or archived LW records
- unrelated old Design files
- unrelated old Feedback files
- unrelated worker prompts
- unrelated Run Logs
- unrelated ADRs or changelogs
- source code, unless needed only to disambiguate a document pointer

## Current Fact Rules

Treat current facts as coming from:

- docs entry README
- `docs/current-state.md`
- current fact documents such as `docs/context/`, `docs/architecture.md`, `docs/development.md`, contracts, or module docs
- active task package only when current-state points to it

Treat these as historical evidence by default:

- old Design
- old Feedback
- old Run Log
- old worker Prompt
- LW record
- archived task package or archived LW record
- ADR
- onboarding handoff snapshot

Historical evidence can explain why something happened, but it does not override current fact sources.

## Write Scope

This skill is read-only.

Forbidden:

- source edits
- document edits
- current-state edits
- context edits
- ADR/changelog edits
- worker prompt creation
- Git writes
- creating task packages
- marking anything complete

If the trace reveals docs are stale or missing, report `Needs uth-docs` or `Needs uth-docs context-sync`; do not fix it here.

## Closeout

End with:

```text
Scene: uth-context-trace
Trace target:
Anchors used:
Associated task package:
Archived location:
Associated LW record:
Associated Design:
Associated Todo:
Associated Feedback:
Associated worker Prompt:
Associated Run Log:
Associated ADR:
Associated onboarding snapshot:
Evidence chain summary:
Current fact sources:
Historical-only evidence:
Missing or unclear docs:
Recommended next scene:
Files modified: none
```

If nothing was found, say what was checked and why the trace could not be established.
