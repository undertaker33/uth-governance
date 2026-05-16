---
name: uth-onboarding
description: Use only when the user explicitly asks to initialize, enable, or take over a project with UTH governance, or when an installation flow explicitly calls project onboarding. Creates the project-level .uth-governance/project.json marker, minimal governance docs, new-project scaffold, or existing-project documentation backup and handoff snapshot. Do not use for ordinary development, debugging, review, Git, standalone docs cleanup, or automatic routing in projects that have not been explicitly onboarded.
---

# UTH Onboarding

## Purpose

Use `uth-onboarding` to make a target project UTH-enabled.

This skill owns only the first project-level handoff into UTH:

- choose `new-project` or `existing-project`
- create `.uth-governance/project.json`
- create the minimal docs structure
- copy bundled hook tools into the target project
- protect existing project documentation before changing it
- create an existing-project handoff snapshot
- hand existing projects to `uth-docs` for deeper documentation governance

Do not use this skill automatically. It must be triggered by the user explicitly, or by an installation flow that explicitly says it is initializing a target project.

## Modes

State one mode before writing:

- `new-project`: empty, new, or intentionally blank project that needs the UTH docs skeleton.
- `existing-project`: project already has code, docs, an `AGENTS.md`, old task documents, or historical governance material.

If the mode is unclear, ask one concise question. Do not create files until the mode is clear.

## Entry Conditions

Use this skill when the user explicitly says:

- initialize UTH in this project
- enable UTH for this project
- onboard this project
- take over this existing project with UTH
- create the initial UTH docs structure
- run `/uth-onboarding`

Do not use this skill when:

- the user asks for ordinary implementation; use `uth-dev` only after the project is enabled
- the user reports a bug; use `uth-debug` only after the project is enabled
- the user asks for review; use `uth-review` only after the project is enabled
- the user asks for standalone docs cleanup in an already enabled project; use `uth-docs`
- the user asks for Git closure; use `uth-git`
- the project is missing `.uth-governance/project.json` but the user did not explicitly ask to enable UTH

Installation alone is not project onboarding. A global install must not create project docs or the project marker.

## Minimal Reads

For both modes, read only enough to identify the project and existing docs:

```text
AGENTS.md, if present
README.md or equivalent root entry doc, if present
docs/README.md, if present
docs/current-state.md, if present
package/build/workspace/module declaration files
git status and a small recent git log, if this is a Git repo
top-level directory tree
```

Do not read the full source tree. Onboarding may create only an initial `current-state.md` index; it must not claim full source understanding.

## Project Marker

After the minimal project handoff succeeds, create:

```text
.uth-governance/project.json
```

Use this shape:

```json
{
  "schema": "uth-governance-project/v1",
  "enabled": true,
  "onboarded_at": "YYYY-MM-DDTHH:mm:ss+08:00",
  "onboarding_mode": "new-project | existing-project",
  "docs_root": "docs",
  "entrypoints": {
    "agent": "AGENTS.md",
    "docs": "docs/README.md",
    "current_state": "docs/current-state.md",
    "context": "docs/context/README.md"
  }
}
```

The marker is project state. It is what allows `uth-governance` to route other `uth-*` scenes automatically in this project.

## Hook Tools

Project hook tools are project-local. During onboarding, copy the bundled asset:

```text
assets/uth-hooks/
```

to the target project:

```text
tools/uth-hooks/
```

Do not use a global hook-tools directory. The project-local hook runner is:

```text
tools/uth-hooks/uth-hook.py
```

## New Project Workflow

For `new-project`:

1. Create the minimal UTH docs scaffold from `references/project-scaffold.md`.
2. Copy `assets/uth-hooks/` to target project `tools/uth-hooks/`.
3. Create a lightweight root `AGENTS.md` only if missing, or append only the minimal project entry if the user allows updating an existing one.
4. Create `.uth-governance/project.json`.
5. Create `docs/current-state.md` as an initial index.
6. Do not invent tech stack, module boundaries, commands, or architecture facts.
7. Mark unknown facts as `TBD` or `Needs uth-docs`.

Do not create a formal task package during new-project onboarding unless the user explicitly asks.

## Existing Project Backup

For `existing-project`, before any onboarding or docs-governance write, create a documentation backup zip under `docs/`:

```text
docs/ONBYYMMDDXX-pre-uth-docs-backup.zip
```

Back up all documentation-class files that onboarding or the first `uth-docs` pass may affect:

- root `AGENTS.md`
- root `README*`
- existing `docs/`
- old governance docs
- old Design, Todo, Feedback, Run Log, Prompt, ADR, changelog, and context docs
- module-local README or architecture docs
- agent rule files and historical collaboration instructions

Do not include `.git/`, dependency folders, build outputs, caches, or ordinary source files unless the file is documentation-class material.

## Existing Project Snapshot

For `existing-project`, create a one-time handoff snapshot:

```text
docs/snapshots/ONBYYMMDDXX-existing-project-handoff.md
```

Record:

- onboarding time
- repository snapshot
- backup zip path
- pre-onboarding docs structure
- discovered entrypoints
- discovered tech-stack clues
- discovered module-boundary clues
- old rules worth preserving
- old documentation credibility
- facts not confirmed
- required `uth-docs` follow-up

This snapshot is handoff evidence, not a daily log. Later scenes may read it through `docs/current-state.md` or the docs entrypoint when they need onboarding context.

## Current-State Rules

Onboarding writes only an initial `docs/current-state.md` index.

Allowed content:

- project name
- onboarding status
- repository snapshot
- docs entrypoints
- backup and snapshot paths
- discovered tech-stack clues
- discovered module-boundary clues
- active unknowns
- `uth-docs` follow-up items

Do not state that full architecture, full module boundaries, runtime flow, or business behavior are confirmed unless the evidence was actually read.

Use this wording when the fact needs deeper docs governance:

```text
Needs uth-docs confirmation from code facts.
```

## Existing Project Handoff To uth-docs

After `existing-project` minimal onboarding succeeds, automatically continue into `uth-docs`.

The handoff condition is:

- backup zip created
- handoff snapshot created
- `.uth-governance/project.json` created
- `tools/uth-hooks/` copied from bundled assets
- `docs/current-state.md` created or updated as an initial index
- old docs and unknown facts marked for follow-up

Then route to `uth-docs` for:

- old docs classification
- context bootstrap or sync
- current-state cleanup
- archive cleanup
- migration of old task documents
- extraction of stable old `AGENTS.md` rules

Do not ask the user to manually start `uth-docs` unless they explicitly pause onboarding.

## Write Scope

Allowed writes:

```text
.uth-governance/project.json
tools/uth-hooks/
AGENTS.md
docs/README.md
docs/current-state.md
docs/project-overview.md
docs/architecture.md
docs/development.md
docs/context/README.md
docs/work/README.md
docs/LW-Work/README.md
docs/snapshots/
docs/_governance/
docs/archive/README.md
docs/archive/work/
docs/archive/LW-Work/
docs/decisions/README.md
docs/changelogs/README.md
docs/ONBYYMMDDXX-pre-uth-docs-backup.zip
```

Forbidden writes:

```text
source code
tests
build outputs
dependency folders
Git history or branch state
ADR decision bodies, except structural README/index files
release changelog content
skills/
```

If the requested write falls outside onboarding scope, stop and ask for confirmation or route to the correct scene.

## Guards

Use `uth-utf8-guard` or an equivalent UTF-8/fence check before and after modifying governed Markdown:

```text
AGENTS.md
README.md
docs/**/*.md
```

Use project hook gates when available:

- L2 write-scope gate before writes
- L3 onboarding closeout gate before claiming minimal onboarding is complete

Do not execute Git writes.

## Closeout

End with:

```text
Scene: uth-onboarding
Mode:
Read:
Created/updated:
Hook tools:
Backup:
Snapshot:
Project marker:
Current-state:
Unconfirmed facts:
UTF-8 guard:
Git writes: none
Next route:
```

For `new-project`, `Next route` is usually `none` or `uth-docs` if more documentation governance was requested.

For `existing-project`, `Next route` must be `uth-docs` unless the user explicitly paused after minimal onboarding.

Never claim full project understanding from onboarding alone. Say `UTH minimal onboarding complete`.
