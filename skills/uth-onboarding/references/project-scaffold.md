# UTH Project Scaffold Reference

Use this reference only when `uth-onboarding` creates or repairs the minimal project governance scaffold.

## Directory Skeleton

```text
.uth-governance/
tools/
└─ uth-hooks/
docs/
├─ README.md
├─ current-state.md
├─ project-overview.md
├─ architecture.md
├─ development.md
├─ context/
│  └─ README.md
├─ work/
│  └─ README.md
├─ LW-Work/
│  └─ README.md
├─ snapshots/
├─ _governance/
│  ├─ README.md
│  ├─ agent-rules.md
│  ├─ git-workflow.md
│  ├─ subagent-workflow.md
│  ├─ writing-rules.md
│  ├─ hook-gates.md
│  ├─ state-rules.md
│  └─ adr-release-rules.md
├─ archive/
│  ├─ README.md
│  ├─ work/
│  └─ LW-Work/
├─ decisions/
│  └─ README.md
└─ changelogs/
   └─ README.md
```

## Root AGENTS.md

```md
# AGENTS.md

This file is the repository-level Agent entry. Keep it short.

## UTH Governance

- This project is UTH-enabled. Project marker: `.uth-governance/project.json`.
- For engineering work, use `uth-governance` to route to the correct `uth-*` scene.
- If the user explicitly invokes `skill-creator`, yield to `skill-creator`.
- Do not scan all docs by default. Start from `docs/README.md` and `docs/current-state.md`.
- Do not perform Git writes unless `uth-git` is active and the user has confirmed the Git plan.

## Entry Points

- Docs entry: `docs/README.md`
- Current state: `docs/current-state.md`
- Context index: `docs/context/README.md`
- Governance rules: `docs/_governance/README.md`
- Hook runner: `tools/uth-hooks/uth-hook.py`
```

## docs/README.md

```md
# Project Docs

Start here before reading project documentation. Read only the sections needed by the active `uth-*` scene.

## Current Facts

- `current-state.md`: current state index, not a log.
- `project-overview.md`: project purpose, stack clues, and high-level boundaries.
- `architecture.md`: current architecture and module boundaries.
- `development.md`: local setup, run, build, and verification commands.
- `context/`: module-level current facts.

## Work Evidence

- `work/`: formal task packages with Design, Todo, Feedback, worker Prompts, and Run Logs.
- `LW-Work/`: lightweight development final records written at task completion.

## Governance

- `_governance/`: project governance rules. This directory does not duplicate `uth-*` scene routing.
- `snapshots/`: onboarding handoff and other project snapshots.
- `archive/`: completed work and LW records that are no longer active.
- `decisions/`: ADR decision evidence, not the current fact source.
- `changelogs/`: release changelogs.
```

## docs/current-state.md

```md
# Current Project State

Updated at: YYYY-MM-DD HH:mm

## Onboarding

- UTH enabled: yes
- Mode: new-project / existing-project
- Project marker: `.uth-governance/project.json`
- Repository snapshot:
- Backup:
- Handoff snapshot:

## Current Phase

- Phase: TBD

## Active Work

| Item | Status | Notes |
| --- | --- | --- |
| None | - | - |

## Current Blockers

- None

## Recent Changes

- None

## Latest Verification

| Time | Method | Result | Notes |
| --- | --- | --- | --- |
| None | - | - | - |

## Current Fact Sources

- `docs/README.md`
- `docs/project-overview.md`
- `docs/architecture.md`
- `docs/development.md`
- `docs/context/README.md`

## Needs uth-docs

- Confirm module boundaries from code facts.
- Build or update module context.
```

## docs/project-overview.md

```md
# Project Overview

## Project Name

TBD

## Purpose

TBD

## Users

TBD

## Stack Clues

- TBD

## Module Clues

- TBD

## Non-goals

- TBD
```

## docs/architecture.md

```md
# Architecture

## Current Status

Needs uth-docs confirmation from code facts.

## Module Boundaries

| Module | Responsibility | Not responsible for |
| --- | --- | --- |
| TBD | TBD | TBD |

## Risks / Unknowns

- TBD
```

## docs/development.md

````md
# Development

## Environment

TBD

## Run

```bash
```

## Build

```bash
```

## Test

```bash
```

## Notes

- Needs uth-docs confirmation from code facts.
````

## docs/context/README.md

```md
# Context Index

`docs/context/` contains module-level current facts.

Do not treat old Design, Feedback, Run Logs, worker Prompts, LW records, archived docs, or ADR bodies as current facts.

## Module Map

- TBD

## Baseline

- Commit:
- Source:
- Updated at:
```

## docs/work/README.md

````md
# Work Packages

Formal task packages live here:

```text
docs/work/DYYMMDDXX-task-title/
├─ 00-DYYMMDDXX-design.md
├─ 10-DYYMMDDXX-T01-todo-task.md
├─ 11-DYYMMDDXX-T01-feedback-task.md
├─ prompts/
└─ runs/
```
````

## docs/LW-Work/README.md

````md
# Lightweight Work

Lightweight development records live here:

```text
LWYYMMDDXX-light-task.md
```

The final record is written by `uth-dev` when the lightweight task is completed. `uth-git` appends the Git baseline after a successful Git write.
````

## docs/snapshots/ONBYYMMDDXX-existing-project-handoff.md

````md
# ONBYYMMDDXX Existing Project Handoff

## Onboarding Time

YYYY-MM-DD HH:mm

## Repository Snapshot

-

## Backup

- `docs/ONBYYMMDDXX-pre-uth-docs-backup.zip`

## Pre-Onboarding Docs Structure

```text
```

## Discovered Entrypoints

-

## Tech-Stack Clues

-

## Module-Boundary Clues

-

## Old Rules Worth Preserving

-

## Old Documentation Credibility

-

## Unconfirmed Facts

-

## Required uth-docs Follow-up

-
````

## docs/_governance/README.md

```md
# Governance Rules

Project governance rules live here. Scene routing and scene execution live in the installed `uth-*` skills, not in this directory.

## Files

- `agent-rules.md`: stable agent behavior rules.
- `git-workflow.md`: Git write and release rules.
- `subagent-workflow.md`: worker/planner/evaluator coordination.
- `writing-rules.md`: Design/Todo/Feedback/LW/context write rules.
- `hook-gates.md`: L0/L1/L2/L3 gates.
- `state-rules.md`: current-state and snapshot rules.
- `adr-release-rules.md`: ADR and changelog rules.
```

## Other Governance Files

Create these files with short placeholders if no project-specific rules are known yet:

```md
# Agent Rules

- Keep project facts in current fact documents, not in old task logs.
- Do not execute Git writes without `uth-git` and user confirmation.
```

```md
# Git Workflow

Git writes require `uth-git`, a shown plan, and explicit user confirmation.
```

```md
# Subagent Workflow

Worker Prompts are persisted for `worker` roles only. `planner` and `evaluator` are read-only and do not write Prompt files.
```

```md
# Writing Rules

Use `docs/work/` for formal task packages and `docs/LW-Work/` for lightweight work. `docs/context/` is current fact context, not a task log.
```

```md
# Hook Gates

Use L1 for process, L2 for write/tool scope, and L3 for closeout evidence. Hooks check evidence; they do not replace scene skills.
```

```md
# State Rules

`docs/current-state.md` is an index, not a log. Keep stale facts out of it.
```

```md
# ADR and Release Rules

ADR records decision evidence. Changelogs belong to formal releases.
```

## Archive / Decisions / Changelogs README placeholders

```md
# Archive

Completed work that is no longer active lives here. Archive is historical evidence, not a current fact source.
```

```md
# Decisions

ADR files live here. ADR is decision evidence, not the current fact source.
```

```md
# Changelogs

Release changelogs live here. Do not use changelog files as commit logs.
```
