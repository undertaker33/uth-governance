---
name: uth-governance
description: Use at the start of work in a UTH-enabled project, identified by .uth-governance/project.json, when Codex must decide whether the request belongs to a UTH engineering scene, when a request may span multiple scenes, or when the correct uth-* child skill is unclear. Also use when the user explicitly asks to route, classify, or apply UTH engineering governance. Stay silent in projects without .uth-governance/project.json unless the user explicitly asks to enable UTH or invokes uth-onboarding. Do not use when the user explicitly invokes skill-creator.
---

# UTH Governance

## Purpose

Use `uth-governance` as the top-level router for UTH engineering governance. It classifies the request, prevents cross-scene extra work, and immediately enters the selected child skill.

This skill is a router only. It does not execute debug, development, review, docs cleanup, Git, release, or skill-maintenance workflows.

## Hard Boundaries

- Do not modify files.
- Do not execute Git writes.
- Do not read all docs for routing.
- Do not read `docs/archive/` for routing.
- Do not invoke UTH-SP method skills from this skill.
- Do not edit `skills/`.
- If the user explicitly invokes `skill-creator`, yield completely to `skill-creator`.
- If the user asks to create or update a skill without explicitly invoking `skill-creator`, stop and ask them to invoke `skill-creator`.

## Silent Mechanism

Before routing ordinary engineering work, check for the project marker:

```text
.uth-governance/project.json
```

If the marker is missing, all `uth-*` scenes stay silent except:

- explicit `uth-onboarding`
- installation flow
- explicit user request to enable UTH, initialize UTH governance, or take over the project with UTH

The marker means the project has been onboarded and UTH routing is enabled. It is project state, not global installation state.

If the marker is missing and the user asks for ordinary development, debugging, review, docs cleanup, or Git work, answer or work as normal Codex without routing to `uth-dev`, `uth-debug`, `uth-review`, `uth-docs`, or `uth-git`.

## Required Classification

At the start of a project or repository conversation, classify the request before taking project action.

Use this layered decision:

1. Explicit `skill-creator` invocation: yield to `skill-creator`.
2. Explicit `uth-onboarding` or explicit UTH enable/takeover request: enter `uth-onboarding`.
3. Missing `.uth-governance/project.json`: stay silent and do not route other UTH scenes.
4. Explicit child UTH skill named by user: enter that child skill.
5. No project action signal and no UTH scene condition matches: answer normally; no child skill.
6. Exactly one UTH scene matches: state one short scene line, then enter that child skill.
7. Multiple scenes match: choose the first execution scene and defer later scenes to closeout.
8. Scene still unclear: stop and ask one concise clarification question.

Do not read more docs just to force a scene. If the scene cannot be determined from the user request plus minimal entry context, ask.

## Project Action Signals

A UTH scene is required when the request includes any engineering action signal:

- code or test change, implementation, feature, UI/API/config change, Todo work, or continuation of active work
- bug, failure, exception, regression, failing test, build error, wrong behavior, or root-cause request
- review, validation, acceptance, diff check, readiness check, or test execution as an acceptance gate
- architecture design, solution evaluation, technical selection, module boundary, feasibility, or design review
- documentation governance, current-state cleanup, context sync/bootstrap, archive cleanup, snapshot, or migration
- commit, branch, PR, merge, rebase, push, tag, release, changelog, or worktree closure
- request to locate Design/Todo/Feedback/worker Prompt/Run/LW/ADR/archive evidence

No UTH scene may be skipped unless no project action signal is present and no scene condition below matches.

## Scene Routing

Route to the first matching child skill:

| Request shape | Child skill |
| --- | --- |
| explicit `skill-creator` invocation | yield to `skill-creator` |
| explicit UTH project initialization, enablement, takeover, or `/uth-onboarding` | `uth-onboarding` |
| missing `.uth-governance/project.json` and no explicit UTH enablement request | no child skill |
| explicit child skill request | named child skill |
| unknown bug, failure, exception, regression, failing test, or root-cause repair | `uth-debug` |
| review, validation, acceptance, delivery check, test gate, diff review | `uth-review` |
| clear implementation, feature, UI/API/config change, Todo implementation | `uth-dev` |
| architecture design, option comparison, feasibility, technical selection, solution evaluation | `uth-design` |
| docs governance, context sync/bootstrap, current-state cleanup, archive, snapshot, migration, rules/templates | `uth-docs` |
| Git/PR/tag/release/changelog/worktree/branch closure as the primary request | `uth-git` |
| task evidence lookup, document conflict tracing, archived evidence lookup | `uth-context-trace` |
| pure explanation or casual conversation with no project action signal | no child skill |

When a request spans scenes, start with the first execution scene:

- "fix and commit" -> `uth-debug` or `uth-dev`, then hand off to `uth-git`.
- "implement and review" -> `uth-dev`, then hand off to `uth-review`.
- "update docs and commit" -> `uth-docs`, then hand off to `uth-git`.
- "review and fix" -> `uth-review` first; only switch to `uth-debug` or `uth-dev` after findings.

## Ambiguity Rule

If the scene is unclear, stop and ask one concise question.

Common unclear cases:

- bug fix vs requirement change
- design evaluation vs implementation
- review vs debug repair
- docs governance vs ordinary task writeback
- Git planning vs Git execution
- skill maintenance without explicit `skill-creator`

Do not start work until the scene is clear.

## Minimal Reading

For routing, prefer no file reads. If project entry context is necessary, read at most:

```text
AGENTS.md
docs/README.md
docs/current-state.md
```

Read `docs/current-state.md` only when active task pointers affect routing. Do not read `docs/context/`, old Design/Feedback/Run/Prompt files, `docs/archive/`, ADRs, changelogs, source files, or tests for routing.

The selected child skill owns further document loading.

## UTH-SP Boundary

Do not invoke UTH-SP method skills from `uth-governance`.

This skill only routes. UTH-SP trigger decisions belong to the selected child skill. If no child skill is selected, do not trigger UTH-SP method skills for greetings, casual talk, pure explanation, or no-op requests.

## Output Discipline

For casual or pure read-only requests with no UTH scene, do not output a routing table.

For project action requests, output one short line before entering the child skill:

```text
Scene: uth-dev - clear bounded implementation; entering uth-dev.
```

If the user explicitly asks for a scene decision, output:

```text
Scene decision:
- primary scene:
- routed skill:
- reason:
- ambiguity:
- next action:
```

For unclear scenes, output only the blocker and one question.
