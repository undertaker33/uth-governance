---
name: uth-dev
description: Use in a UTH-enabled project, identified by .uth-governance/project.json, for incremental feature, UI, API, field, behavior, Todo implementation, or bounded development work, including explicit uth-dev requests inside an enabled project. Controls model-specific light-vs-formal development routing, minimal context loading, Todo writeback, worker-subagent prompt writeback, UTH-SP method-skill gates, Feedback/current-state writeback for formal tasks, LW-Work records for lightweight tasks, and handoff to review/debug/git. Stay silent in projects without the UTH marker unless the user explicitly asks to enable UTH first. Do not use for pure design, unknown bug diagnosis, code review, documentation governance, or Git/release closure.
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

- `light-dev`: small clear change that passes the model hard boundary without formal task package.
- `formal-dev`: development inside a formal `DYYMMDDXX-*` task package.
- `todo-breakdown`: create Todo files from an accepted Design.
- `todo-implementation`: implement a specific Todo.
- `handoff-from-design`: receive accepted Design from `uth-design`, then choose `todo-breakdown` or `formal-dev`.

## Light/Formal Hard Boundary

Do not choose `light-dev` by confidence, intuition, or "this feels small". Use these hard gates.

`light-dev` requires:

- supported `llm_model`
- explicit `task_shape.changed_files_count`
- explicit `task_shape.modules_count`
- explicit `task_shape.implementation_steps_count`
- no formal trigger flags

Supported first-batch model limits:

| `llm_model` | Max changed files | Max modules | Max implementation steps |
| --- | ---: | ---: | ---: |
| `claude-opus-4.7`, `gpt-5.5` | 8 | 2 | 4 |
| `claude-opus-4.6`, `gpt-5.4`, `deepseek-v4-pro`, `mimo-v2.5-pro`, `kimi-k2.6` | 5 | 1 | 3 |
| `gpt-5.3-codex-spark`, `deepseek-v4-flash` | 3 | 1 | 2 |

Unsupported or undeclared model means `light-dev` is blocked. Route to `formal-dev` or ask for an explicit boundary update.

These flags always force `formal-dev` for all models:

- ambiguous requirements or unclear acceptance
- required Design or formal Todo
- new feature surface
- public API, contract, database schema, or migration change
- auth, permission, security, concurrency, state machine, or data-loss risk
- architecture, module boundary, dependency, build logic, cross-module state, external integration, or protocol change
- worker or parallel-agent dispatch

Before implementing a `light-dev` candidate, run or satisfy the L1 process gate with:

```json
{
  "type": "l1-process",
  "active_scene": "uth-dev",
  "mode": "light-dev",
  "llm_model": "gpt-5.4",
  "task_shape": {
    "changed_files_count": 2,
    "modules_count": 1,
    "implementation_steps_count": 2
  },
  "uth_sp": {
    "decision_recorded": true
  }
}
```

## Entry Protocol

Start with:

- `Scene: uth-dev`
- mode
- user goal
- allowed change scope
- forbidden change scope
- `llm_model` and `task_shape`, when `light-dev` is considered
- formal trigger check result
- existing task package, if any
- formal task package evidence when mode is `formal-dev`, `todo-implementation`, `todo-breakdown`, or `handoff-from-design`
- whether worker subagent is needed
- UTH-SP method-skill trigger decision
- document writeback decision
- Git write status: none in this scene

If requirement, scope, acceptance criteria, or impact is unclear, use `uth-sp-brainstorming` before implementation.

Do not start coding while ambiguity remains.

For `formal-dev` and `todo-implementation`, do not start implementation until an active task package, accepted Design, and current Todo all exist. A formal trigger is not enough. If the accepted Design is missing, route to `uth-design`; if the Todo is missing, use `todo-breakdown` first.

Before any governed Markdown persistence from this scene, use `uth-sp-brainstorming` and record that no open user questions remain. This applies to Todo, Feedback, worker Prompt, Run Log, LW final record, and current-state index writes.

## Document Lookup

Do not call `uth-context-trace` by default.

First locate docs structure:

1. Read `AGENTS.md`, if present.
2. Read the docs entry README, usually `docs/README.md`, if present.
3. Read the localized current-state entrypoint from `.uth-governance/project.json`, if needed.
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
- localized current-state entrypoint
- relevant `docs/context/*.md`, only when module is clear or entrypoint points there
- directly related code and tests
- nearby README or local test instructions

For `formal-dev` / `todo-implementation`, read:

- `AGENTS.md`
- docs entry README
- localized current-state entrypoint
- current task-package `00-DYYMMDDXX-design.md`
- current Todo
- relevant `docs/context/*.md`
- directly related code and tests

Read on demand:

- localized development docs
- localized architecture docs
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

Historical and archived docs are evidence, not current facts. They do not override the localized current-state entrypoint, `docs/context/`, or the active Design/Todo.

## UTH-SP Flow

Use:

- `uth-sp-brainstorming` when goal, scope, acceptance, or impact is unclear
- `uth-sp-brainstorming` before governed Markdown persistence, even when the work is otherwise clear, to confirm there are no open user questions
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
- use `uth-utf8-guard` before and after modifying governed Markdown (`AGENTS.md`, root `README.md`, `docs/**/*.md`, task-package Markdown, LW final record, Feedback, Prompt, or Run Log)
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

Do not create a separate LW Todo. Keep the lightweight task boundary in the scene entry and write one final LW record at task completion.

After implementation and verification, write or update:

```text
docs/LW-Work/LWYYMMDDXX-中文标题.md
```

The final LW record must include:

- original request
- task boundary and non-goals
- changed files
- implementation summary
- verification command and result
- unverified items
- risk and rollback notes
- Git baseline section with `pending uth-git`

Do not wait for a commit hash, PR, tag, or release before writing this record. `uth-git` appends the Git baseline later if a Git write succeeds.

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

- `formal-dev` and `todo-implementation` require an active task package, accepted Design, and current Todo before implementation.
- If formal work has no accepted Design, stop and route to `uth-design`; do not invent a Todo directly from the user request.
- If formal work has an accepted Design but no Todo, stay in `todo-breakdown` and create the Todo before code work.
- Todo files are created only in `uth-dev`, not `uth-design`.
- Feedback is written for formal Todo delivery.
- Feedback records implementation, changed files, verification, risks, and remaining work; it does not require Git commit/PR/tag information.
- If Git information already exists, it may be linked, but missing Git information must not block formal development closeout.
- current-state is updated only as an index when Todo/task state changes.
- worker Prompt is written only for worker subagents.
- Run Log is written only when execution evidence needs preservation.

## Todo Breakdown

After an accepted Design, `uth-dev` may create Todo files.

Before creating or updating Todo files, use `uth-sp-brainstorming` and confirm no user-facing questions remain. If questions remain, stop and ask the user instead of persisting the Todo.

Allowed:

- read accepted `00-DYYMMDDXX-design.md`
- create `10-*todo*`, `20-*todo*`, etc.
- define scope, non-goals, acceptance criteria, verification, allowed files, forbidden files
- update the localized current-state entrypoint only as an active Todo/task index

Forbidden:

- changing Design casually
- writing Feedback before implementation
- implementing code during pure Todo breakdown unless the user explicitly asks to continue

After Todo creation from a Design handoff, stop and ask before continuing into implementation. Do not treat Design acceptance as automatic permission to enter `formal-dev`.

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

- final LW record under `docs/LW-Work/`
- directly related code
- directly related tests
- minimal local config only when required by the change

Allowed in `formal-dev`:

- current Todo authorized code
- current Todo authorized tests
- current Todo Feedback
- current task-package worker prompts
- current task-package runs, when needed
- localized current-state entrypoint index updates

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
Needs uth-docs scoped-sync
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

Update the localized current-state entrypoint only when:

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

1. Read the localized current-state entrypoint.
2. Read the active Design.
3. Read the active Todo.
4. Read existing Feedback for the active Todo, if present.
5. If the active Todo has no completed Feedback, continue it.
6. If the active Todo is completed, move to the next unfinished Todo.
7. If all Todos are completed, hand off to `uth-review` for Design-level acceptance.

For `light-dev`, resume from the active final LW record under `docs/LW-Work/`, if one already exists; otherwise use the current user request and local diff as the task boundary.

If the only matching Todo or LW record is under `docs/archive/`, do not resume it as active work. Ask whether to create a new active LW final record or route to `uth-docs` / `uth-context-trace`.

## Git Rule

`uth-dev` does not perform Git writes.

After development:

- always evaluate Git-closure handoff for `light-dev` after implementation and verification
- for formal task packages, evaluate Git-closure handoff only when the Design-level human acceptance boundary is reached, not after each Todo
- when only a Todo is complete but the Design is not yet at human acceptance, say the next Todo or review route instead of recommending Git closure
- ask whether the user wants to enter `uth-git` only when Git closure is recommended or the user explicitly asks for Git
- hand off to `uth-git` only after the user explicitly agrees
- `uth-git` owns Git write planning, user confirmation, commit execution, and Git baseline append to the existing LW final record or formal Feedback after a successful Git write
- formal Feedback remains valid even when no Git commit has happened yet

## Closeout

If `.uth-governance/project.json` contains `document_language`, render the closeout report in that language. For `zh-CN`, use Chinese headings and Chinese prose; preserve literal paths, commands, skill names, schema values, and code identifiers.

End with:

- `Scene: uth-dev`
- mode
- changed files
- implementation summary
- verification command and result, including compile/build pass plus warning/exception count for code changes
- unverified items
- document writeback
- LW final record written, if `light-dev`
- UTF-8 guard result for governed Markdown writes
- worker Prompt records, if any
- current-state update: yes/no
- `Needs uth-docs scoped-sync`, if applicable
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
