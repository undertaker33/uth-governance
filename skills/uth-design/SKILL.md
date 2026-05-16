---
name: uth-design
description: Use in a UTH-enabled project, identified by .uth-governance/project.json, for architecture design, technical selection, solution comparison, feasibility analysis, exploratory planning, design review before implementation, or evaluation of whether an approach is reasonable, including explicit uth-design requests inside an enabled project. Combines readonly evaluation and formal architecture/design authoring while controlling minimal document lookup, task-package Design writeback, high-threshold ADR creation, current-state index updates, and handoff to development. Stay silent in projects without the UTH marker unless the user explicitly asks to enable UTH first. Do not use for direct coding, bug repair, post-implementation code review, standalone documentation maintenance, or Git/release closure unless the task is explicitly about design decisions.
---

# uth-design

## Purpose

Use this skill for solution evaluation and architecture/design work before implementation.

Keep the scene in design space:

- clarify the goal, constraints, scope, and acceptance criteria
- read only the context needed to evaluate or design
- compare options and risks
- create a formal task-package Design only when the work needs one
- create ADRs only for accepted, durable architecture decisions
- hand off to `uth-dev` before coding

Do not write source code, tests, changelog, release notes, or Git changes from this scene by default. A small design-assisted code patch is allowed only after an explicit user confirmation and only under the exception below.

## Trigger Conditions

Use `uth-design` when the user asks for:

- architecture design
- technical selection
- solution comparison
- feasibility analysis
- exploratory planning before implementation
- design review before coding
- evaluation of whether an existing proposal is reasonable
- module boundary, data flow, dependency direction, storage, protocol, API, deployment, or long-term tradeoff decisions

Typical user wording:

- "先设计一下"
- "先不要写代码，出个方案"
- "这个方案合理吗"
- "A 和 B 选哪个"
- "这块架构怎么拆"
- "模块边界怎么定"
- "先评估可行性"
- "这个设计有没有风险"
- "后面要开发，先把设计定下来"

Do not use this skill for:

- direct implementation of an already clear change
- bug diagnosis or repair; use `uth-debug`
- post-implementation code review or acceptance; use `uth-review`
- standalone documentation cleanup or context sync; use `uth-docs`
- commit, PR, tag, release, or branch closure; use `uth-git`
- small UI/style/text/field changes with clear target behavior; use `uth-dev`
- pure code explanation with no design decision; stay read-only

## Modes

State one mode at the start:

- `readonly-evaluation`: for "look at this", "evaluate this", "is this reasonable", or unclear scenes. Default to read-only and do not write project docs.
- `design-authoring`: for accepted or requested formal design that should guide implementation. Create or update a task-package Design.
- `decision-recording`: for durable architecture decisions already accepted by the user. Write ADR only when the threshold is met.

If the user only wants discussion or evaluation, stay in `readonly-evaluation`.

If the user asks for a formal design or a plan that will guide development, use `design-authoring`.

If the user asks to settle a long-term architecture choice, discuss first; use `decision-recording` only after acceptance.

## Entry Protocol

Start with:

- `Scene: uth-design`
- mode
- known goal
- known constraints
- expected output
- whether this round may write documents

If the goal, scope, acceptance criteria, implementation target, decision authority, or option set is ambiguous, use `uth-sp-brainstorming` first.

Do not create Design, ADR, Todo, or implementation plans while ambiguity remains.

## Document Lookup

Do not guess document locations and do not scan all docs by default.

First locate the documentation structure:

1. Read the repository agent entry, usually `AGENTS.md`, if it exists.
2. Read the docs entry README, usually `docs/README.md` or another README that explains the docs structure.
3. Read the current-state index only after the docs entrypoint confirms where it lives, usually `docs/current-state.md`.
4. Follow those entrypoints to active task packages, Design files, ADRs, context files, or governance writing rules.

Do not enter `docs/archive/` by default. Archived Designs, Todos, Feedback, runs, and LW records are historical evidence only; read them only when the user explicitly asks for prior evidence, the design depends on a known archived task, or `uth-context-trace` identifies a narrow archived source.

If the docs structure README is missing or unclear:

- read only nearby README files and directly relevant code or docs
- report that the documentation entrypoint is missing or unclear
- do not invent a new project document structure inside this scene

## Reading Rules

Prefer the smallest useful context set:

- `AGENTS.md`
- docs structure README
- current-state index
- active Design/Todo only when continuing an existing task
- relevant `docs/context/*.md` when the module is clear or linked
- relevant `docs/architecture.md`, `docs/project-overview.md`, or `docs/development.md` when needed
- relevant ADRs only for the same decision area
- archived task evidence only when a known historical decision or design needs comparison
- related code only when needed to confirm current architecture or risk
- official external docs when evaluating current third-party tools, versions, APIs, or standards

Default to not reading:

- all docs
- old Design files
- old Feedback files
- old runs
- old worker prompts
- unrelated task packages
- `docs/archive/`, unless archive is explicitly in scope
- unrelated ADRs
- unrelated changelogs
- unrelated modules

Historical and archived docs are clues, not current facts. They do not override `docs/current-state.md`, `docs/context/`, accepted ADR status, or stable project docs.

## UTH-SP Flow

Use UTH-SP method skills as the process engine, not as the document owner.

Use:

- `uth-sp-brainstorming` when requirements, scope, options, tradeoffs, or acceptance criteria are unclear
- `uth-sp-writing-plans` only after the user accepts a Design and explicitly wants an implementation plan
- `uth-sp-verification-before-completion` before claiming a Design, ADR, or plan was written and checked

UTH governance overrides conflicting UTH-SP defaults:

- do not invent legacy spec folders; use the project governance Design/ADR locations resolved by UTH
- do not commit automatically
- write Design/ADR only to the project governance locations resolved from the docs entrypoint and current-state

## Subagent Policy

Design normally does not use subagents.

Only dispatch subagents when:

- current code state cannot be determined locally
- design risk is high enough to need independent review
- the user explicitly asks for subagent mode

Allowed roles:

- `planner`: read-only exploration of code state, architecture constraints, or option space
- `evaluator`: read-only risk review and design critique

Do not use `worker` in this scene. Switch to `uth-dev` before worker implementation.

Do not write prompt files for `planner` or `evaluator`. Worker prompts are a development-scene artifact only.

## Write Scope

Allowed in `design-authoring`:

- `docs/work/DYYMMDDXX-任务包标题/00-DYYMMDDXX-design.md`
- `docs/current-state.md` only as an index update for active task package, active Design, or decision status

Allowed in `decision-recording`:

- `docs/decisions/ADR-XXXX-中文标题.md`, only after a durable decision is accepted
- `docs/current-state.md` only as an index update

Forbidden by default:

- source code
- tests
- Todo files; hand off to `uth-dev` for implementation breakdown
- Feedback files
- runs
- worker prompts
- `docs/context/`
- `docs/archive/`
- changelog
- Git commit, tag, push, merge, branch, or release changes
- historical Design/Feedback/runs/worker prompts

`docs/context/` is read-only here. If the design implies module-context changes, mark `Needs uth-docs scoped-sync` in closeout.

Use `uth-utf8-guard` before and after modifying governed Markdown (`docs/**/*.md`, Design, ADR, current-state, root `README.md`, or `AGENTS.md`).

## Design-Assisted Patch Exception

If design work reveals a small concrete logic error and a minimal code patch is cheaper than forcing a full debug loop, ask the user before editing code.

The confirmation must name:

- why the patch belongs in design instead of `uth-dev` or `uth-debug`
- exact files or narrow write scope
- risk
- verification command

For hook events, either `design_patch_authorized=true` or `transition.authorized_design_patch=true` represents this confirmation.

Allowed only after confirmation:

- small code patch needed to validate or unblock the design
- directly related tests, if needed

Still forbidden:

- feature implementation
- broad repair
- refactor
- dependency changes
- opportunistic cleanup

After any code patch, run the project build or compile command. Strong-governance closeout requires:

```text
compile/build: pass
warnings: 0
exceptions: 0
```

If warnings or exceptions genuinely cannot be cleared in this scene and are better handled later, ask the user whether to grant a temporary waiver. With a waiver, state the remaining warnings/exceptions and do not claim complete, passing, ready, or deliverable.

If the patch grows beyond the confirmed scope, stop and switch to `uth-dev` or `uth-debug`.

## Design Writeback

Write a formal Design only when:

- the output will guide implementation
- the user asks for formal design
- the work has meaningful scope, constraints, alternatives, risks, or acceptance criteria
- implementation should not start without a stable reference

Formal Design location:

```text
docs/work/DYYMMDDXX-任务包标题/
└─ 00-DYYMMDDXX-design.md
```

The Chinese task summary belongs in the task-package directory title and Design title. Keep the Design filename fixed as `00-DYYMMDDXX-design.md`.

Do not write a Design when:

- the user only wants quick evaluation
- the result is a small read-only opinion
- the proposal is not accepted
- the user explicitly says to discuss only

Do not create LW-Work for read-only evaluation. LW-Work is written by `uth-dev` at lightweight task completion, not during design discussion.

## ADR Threshold

Keep the ADR threshold high.

Write ADR only when all are true:

- the decision is durable
- it affects architecture, module boundaries, storage, protocol, dependency, deployment, or long-term maintenance
- real alternatives and tradeoffs were considered
- the user accepted the decision

Do not write ADR for:

- temporary plans
- ordinary implementation details
- undecided options
- single-task tradeoffs
- small UI/API/field adjustments

ADR is decision evidence, not the current fact source.

## Current-State Rules

Update `docs/current-state.md` only as an index:

- active task package changed
- active Design pointer changed
- decision status changed
- blocker or acceptance status changed

Do not write design discussion, long rationale, or process logs into current-state.

Detailed implementation progress belongs to `uth-dev`, not this scene.

## Handoff

If the user accepts the Design and wants implementation:

- hand off to `uth-dev`
- do not start coding in `uth-design`
- pass the accepted Design, constraints, open questions, risks, and acceptance criteria

If the user wants design review:

- stay read-only or use an `evaluator`
- do not modify code

If design work reveals a concrete defect:

- hand off to `uth-debug`

If design work reveals context drift:

- mark `Needs uth-docs scoped-sync`

## Closeout

If `.uth-governance/project.json` contains `document_language`, render the closeout report in that language. For `zh-CN`, use Chinese headings and Chinese prose; preserve literal paths, commands, skill names, schema values, and code identifiers.

End with:

- `Scene: uth-design`
- mode
- context read
- options or risks considered
- recommendation or open questions
- documents written, or why no document was written
- design-assisted patch: none / requested / applied, including verification if applied
- ADR status: none / proposed / written
- current-state update: yes / no
- UTF-8 guard result for governed Markdown writes
- `Needs uth-docs scoped-sync`, if applicable
- next scene: none / `uth-dev` / `uth-review` / `uth-docs` / `uth-debug`

If no files were changed, say `read-only, no files modified`.

Never imply implementation has started or succeeded from this scene.
