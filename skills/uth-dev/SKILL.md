---
name: uth-dev
description: Use in a UTH-enabled project, identified by .uth-governance/project.json, or when the user explicitly invokes uth-dev, for incremental feature, UI, API, field, behavior, Todo implementation, or bounded development work. Controls light-vs-formal development routing, minimal context loading, Todo writeback, worker-subagent prompt writeback, UTH-SP method-skill gates, Feedback/current-state writeback for formal tasks, LW-Work records for lightweight tasks, and handoff to review/debug/git. Stay silent in projects without the UTH marker unless the user explicitly asks to enable UTH first. Do not use for pure design, unknown bug diagnosis, code review, documentation governance, or Git/release closure.
---

# uth-dev

## Purpose

Use this skill for bounded incremental development.

This scene owns:

- light development
- formal task-package development
- Todo creation after accepted Design
- Todo implementation
- worker subagent dispatch
- development verification
- development-scene document writeback

Do not use this scene for architecture design, unknown bug diagnosis, review, standalone docs governance, or Git/release closure.

## Trigger Conditions

Use `uth-dev` when the user asks to:

- implement a clear change
- add a button, field, page, route, API, or entrypoint
- complete a Todo
- continue from an accepted Design
- modify bounded behavior
- connect an existing capability
- add tests for a defined behavior
- make a small UI, text, config, or display change with clear expected result

Do not use `uth-dev` when the request is mainly design/evaluation, unknown-bug diagnosis, review/acceptance, docs governance, Git/release closure, or pure read-only explanation. Hand off to the matching UTH scene.

## Modes

State one mode at the start:

- `light-dev`: small clear change without formal task package.
- `formal-dev`: development inside a formal `DYYMMDDXX-*` task package.
- `todo-breakdown`: create Todo files from an accepted Design.
- `todo-implementation`: implement a specific Todo.
- `handoff-from-design`: receive accepted Design from `uth-design`, then choose `todo-breakdown` or `formal-dev`.

## Entry Protocol

Start with:

- `Scene: uth-dev`
- mode
- user goal
- allowed change scope
- forbidden change scope
- existing task package, if any
- whether worker subagent is needed
- UTH-SP method-skill trigger decision
- document writeback decision
- Git write status: none in this scene

If requirement, scope, acceptance criteria, or impact is unclear, use `uth-sp-brainstorming` before implementation.

Do not start coding while ambiguity remains.

## Document Lookup

Do not call `uth-context-trace` by default.

First locate docs structure:

1. Read `AGENTS.md`, if present.
2. Read the docs entry README, usually `docs/README.md`, if present.
3. Read `docs/current-state.md`, if located by the docs entrypoint or needed.
4. For formal work, read the current task-package Design and current Todo.
5. For light work, read only current-state, relevant context, nearby README, code, and tests.

Do not enter `docs/archive/` by default. Archived task packages and archived LW records are not active development inputs. Use archive only when the user explicitly references archived evidence or `uth-context-trace` identifies a narrow archived source.

Call `uth-context-trace` only when:

- the user mentions historical Design, Todo, Feedback, worker Prompt, Run Log, LW, ADR, or commit
- the task may belong to an existing formal task package
- implementation conflicts with documents
- prior debug/review handed over an evidence chain
- worker output or rework needs prompt/task boundary tracing

Do not call `uth-context-trace` for simple code-location search.

## Reading Rules

For `light-dev`, read only:

- `AGENTS.md`
- docs entry README, if present
- `docs/current-state.md`
- relevant `docs/context/*.md`, only when module is clear or entrypoint points there
- directly related code and tests
- nearby README or local test instructions

For `formal-dev` / `todo-implementation`, read:

- `AGENTS.md`
- docs entry README
- `docs/current-state.md`
- current task-package `00-DYYMMDDXX-design.md`
- current Todo
- relevant `docs/context/*.md`
- directly related code and tests

Read on demand:

- `docs/development.md`
- `docs/architecture.md`
- API/data/UI docs relevant to the task
- current Todo Feedback only for continuation or rework
- related worker Prompt only for worker handoff or rework
- related Run Log only for failed verification or handoff
- archived task package or archived LW record only when explicitly traced and needed to understand historical scope

Default to not reading:

- all docs
- old Design
- old Feedback
- old Run Log
- old worker Prompt
- `docs/archive/`, unless archive is explicitly in scope
- unrelated ADR
- unrelated changelog
- unrelated modules

Historical and archived docs are evidence, not current facts. They do not override `docs/current-state.md`, `docs/context/`, or the active Design/Todo.

## UTH-SP Flow

Use:

- `uth-sp-brainstorming` when goal, scope, acceptance, or impact is unclear
- `uth-sp-test-driven-development` when changing business logic, API behavior, permission rules, state machines, core flows, or regression behavior
- `uth-sp-subagent-driven-development` when formal development uses worker subagents
- `uth-sp-verification-before-completion` before claiming complete, fixed, passing, or ready to submit

TDD may be exempted only for:

- pure style
- pure copy
- static UI adjustment without behavior change
- display-only small change
- test framework absent and limitation is reported

Do not use UTH-SP method-skill defaults to override UTH document locations or Git rules.

## Hook Gates

Respect the project hook gates when available:

- declare `Scene: uth-dev` before project action
- do not write outside the allowed development scope without user confirmation
- do not dispatch a `worker` before its Prompt is written
- use `uth-utf8-guard` before and after modifying governed Markdown (`AGENTS.md`, root `README.md`, `docs/**/*.md`, task-package Markdown, LW Todo, Feedback, Prompt, or Run Log)
- do not perform Git writes

## Code Verification Gate

After code changes, run the project build or compile command needed to prove the touched code compiles.

Strong-governance closeout requires:

```text
compile/build: pass
warnings: 0
exceptions: 0
```

Do not accept an old warning baseline by default. On the first UTH code-changing scene in a project, if the build already has warnings or exceptions, clean them to `0 / 0` before claiming the change is complete, unless the user explicitly grants a temporary waiver.

If the user grants a waiver:

- state the waiver and remaining warnings/exceptions in closeout
- do not claim the work is complete, passing, ready, or deliverable
- recommend `uth-debug` or another development pass before Git/release closure
- if cleanup is genuinely better handled later, ask the user for the waiver explicitly; otherwise clean warnings/exceptions before closeout

## Todo Granularity

Prefer fewer Todos.

A Todo is the smallest delivery slice that an Agent can complete and self-verify in one continuous development window.

Do not split Todos mechanically by file, layer, frontend/backend, or technical step.

Create one Todo when one focused coding session can complete and verify the change.

Split into multiple Todos only when:

- one window cannot safely hold the context
- multiple workers need independent write scopes
- staged validation is necessary
- risk must be isolated
- the user explicitly wants phases

Human acceptance is usually Design-level. Todo completion is Agent self-evidence, recorded through Feedback.

Do not trigger Git closure merely because one Todo is complete. For formal development, trigger the Git-closure decision only when the Design-level human acceptance boundary is reached: all required Todos for the accepted Design are completed or the user explicitly says the current Design/package is ready to commit. For light-dev, the lightweight task itself is the human acceptance boundary.

## Light Dev Documents

For `light-dev`, use only `docs/LW-Work/`.

Do not create or update lightweight development records under `docs/archive/LW-Work/`. Archive is managed only by `uth-docs`.

Create a lightweight Todo before implementation or before the first file write:

```text
docs/LW-Work/LWYYMMDDXX-中文标题-todo.md
```

After implementation, do not write the final LW record yet.

The final LW record is written only after:

1. implementation is done
2. verification status is reported
3. user authorizes Git commit
4. `uth-git` completes the commit successfully

Final record:

```text
docs/LW-Work/LWYYMMDDXX-中文标题.md
```

No commit means no final LW record.

`light-dev` does not write:

- Design
- formal Todo
- Feedback
- worker Prompt
- Run Log
- ADR
- changelog
- `docs/context/`

If light work grows beyond this shape, switch to `formal-dev`.

## Formal Dev Documents

For `formal-dev`, use the formal task package:

```text
docs/work/DYYMMDDXX-任务包标题/
├─ 00-DYYMMDDXX-design.md
├─ 10-DYYMMDDXX-T01-todo-任务名.md
├─ 11-DYYMMDDXX-T01-feedback-任务名.md
├─ prompts/
└─ runs/
```

Rules:

- Todo files are created only in `uth-dev`, not `uth-design`.
- Feedback is written for formal Todo delivery.
- Feedback records implementation, changed files, verification, risks, and remaining work; it does not require Git commit/PR/tag information.
- If Git information already exists, it may be linked, but missing Git information must not block formal development closeout.
- current-state is updated only as an index when Todo/task state changes.
- worker Prompt is written only for worker subagents.
- Run Log is written only when execution evidence needs preservation.

## Todo Breakdown

After an accepted Design, `uth-dev` may create Todo files.

Allowed:

- read accepted `00-DYYMMDDXX-design.md`
- create `10-*todo*`, `20-*todo*`, etc.
- define scope, non-goals, acceptance criteria, verification, allowed files, forbidden files
- update `docs/current-state.md` only as an active Todo/task index

Forbidden:

- changing Design casually
- writing Feedback before implementation
- implementing code during pure Todo breakdown unless the user explicitly asks to continue

## Worker Subagent Policy

`uth-dev` is the primary scene for worker subagents.

Roles:

- `worker`: may edit authorized code/tests/docs within scope
- `planner`: read-only exploration, no Prompt file
- `evaluator`: read-only acceptance, no Prompt file

Rules:

- only worker Prompt is written
- planner/evaluator Prompt is not written
- one worker owns one Prompt file
- if the same worker needs rework, append the rework instructions to the same Prompt file
- multiple workers means multiple Prompt files
- worker never performs Git writes
- multiple workers must have disjoint write scopes or separate worktrees
- without worktrees, one physical workspace has one writer
- who caused implementation problems fixes them
- who raises acceptance issues verifies them

Worker Prompt path:

```text
docs/work/DYYMMDDXX-任务包标题/prompts/PYYMMDD-HHMM-T01-worker-任务名.md
```

Append rework instructions to the same file:

```md
## Rework N - YYYY-MM-DD HH:mm

Reason:

Additional instructions:

Validation:

Return requirements:
```

Short dispatch prompt:

```text
请读取并执行：
docs/work/DYYMMDDXX-任务包标题/prompts/PYYMMDD-HHMM-T01-worker-任务名.md

不得执行 Git 写入。完成后按文件中的回传格式回复。
```

## Write Scope

Allowed in `light-dev`:

- lightweight Todo under `docs/LW-Work/`
- directly related code
- directly related tests
- minimal local config only when required by the change

Allowed in `formal-dev`:

- current Todo authorized code
- current Todo authorized tests
- current Todo Feedback
- current task-package worker prompts
- current task-package runs, when needed
- `docs/current-state.md` index updates

Forbidden by default:

- unrelated modules
- unrelated task packages
- old Design/Feedback/runs/worker prompts
- `docs/archive/`
- `docs/context/`
- ADR
- changelog
- Git commit/tag/push/merge/branch
- new dependency without explicit permission
- architecture refactor disguised as incremental work
- unauthorized feature expansion

If module responsibilities, entrypoints, dependencies, boundaries, verification methods, or long-lived risks change, mark:

```text
Needs uth-docs context-sync
```

Do not update `docs/context/` here.

## Run Log Rules

Write Run Log only when:

- multiple rounds need handoff
- worker result needs preserved execution evidence
- verification failure matters
- a complex blocker needs trace

Do not write Run Log for:

- simple light changes
- pure discussion
- no stable conclusion
- cosmetic process logging

## Current-State Rules

Update `docs/current-state.md` only when:

- active task package changes
- active Todo changes
- Todo completes or blocks
- current phase changes
- verification result affects next action

Do not write:

- long process logs
- diff summaries
- ordinary light-dev progress
- worker details
- temporary ideas

## Resume Rules

When resuming interrupted formal development:

1. Read `docs/current-state.md`.
2. Read the active Design.
3. Read the active Todo.
4. Read existing Feedback for the active Todo, if present.
5. If the active Todo has no completed Feedback, continue it.
6. If the active Todo is completed, move to the next unfinished Todo.
7. If all Todos are completed, hand off to `uth-review` for Design-level acceptance.

For `light-dev`, resume from the LW Todo under `docs/LW-Work/`.

If the only matching Todo or LW record is under `docs/archive/`, do not resume it as active work. Ask whether to create a new active task/LW Todo or route to `uth-docs` / `uth-context-trace`.

## Git Rule

`uth-dev` does not perform Git writes.

After development:

- always evaluate Git-closure handoff for `light-dev` after implementation and verification
- for formal task packages, evaluate Git-closure handoff only when the Design-level human acceptance boundary is reached, not after each Todo
- when only a Todo is complete but the Design is not yet at human acceptance, say the next Todo or review route instead of recommending Git closure
- ask whether the user wants to enter `uth-git` only when Git closure is recommended or the user explicitly asks for Git
- hand off to `uth-git` only after the user explicitly agrees
- `uth-git` owns Git write planning, user confirmation, commit execution, and final lightweight LW record writeback after a successful commit
- formal Feedback remains valid even when no Git commit has happened yet

## Closeout

End with:

- `Scene: uth-dev`
- mode
- changed files
- implementation summary
- verification command and result, including compile/build pass plus warning/exception count for code changes
- unverified items
- document writeback
- UTF-8 guard result for governed Markdown writes
- worker Prompt records, if any
- current-state update: yes/no
- `Needs uth-docs context-sync`, if applicable
- human acceptance boundary: light task reached / Design reached / Todo-only not reached / not applicable
- Git-closure decision: not suggested / suggested, waiting for user / user handed off to `uth-git`
- recommended next scene: none / `uth-review` / `uth-debug` / `uth-git` / `uth-docs`
- Git status: not executed in this scene
- risk and rollback notes

If no files changed, say:

```text
read-only, no files modified
```

If verification was not run, do not claim complete. Say:

```text
implementation attempted, not verified
```
