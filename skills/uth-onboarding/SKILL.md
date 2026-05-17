---
name: uth-onboarding
description: Use only when the user explicitly asks to initialize, enable, or take over a project with UTH governance, or when an installation flow explicitly calls project onboarding. Creates the project marker, persists document_language, creates minimal governance docs, copies hook tools, and orchestrates existing-project takeover when requested. Do not use for ordinary development, debugging, review, Git, standalone docs cleanup, or automatic routing in projects that have not been explicitly onboarded.
---

# UTH Onboarding

## Purpose

Use `uth-onboarding` to make a target project UTH-enabled.

This skill owns project enablement and, when the user asks to take over an existing project, the complete takeover transaction orchestration.

For `existing-project`, `uth-onboarding` performs preflight safety work, routes to `uth-docs onboarding-followup` for full documentation governance, then resumes for final takeover closeout. It must not duplicate full documentation governance inside onboarding.

The `uth-docs onboarding-followup` handoff is a scene transition, not an inline subroutine. After full-takeover preflight emits the docs route, stop onboarding preflight. Do not execute old-doc classification, full baseline governance, context rebuild, current-state cleanup, or final takeover closeout while still reporting as `uth-onboarding`.

Core responsibilities:

- choose `new-project` or `existing-project`
- create `.uth-governance/project.json`
- create the minimal docs structure
- copy bundled hook tools into the target project
- resolve and persist the project documentation language before the first governed Markdown write
- protect existing project documentation before changing it
- create an existing-project handoff snapshot
- hand existing-project takeover to `uth-docs onboarding-followup` for documentation governance
- stop the preflight phase after the docs handoff instead of doing docs work inline
- complete final existing-project takeover closeout only after `uth-docs` returns full-project completion evidence

Do not use this skill automatically. It must be triggered by the user explicitly, or by an installation flow that explicitly says it is initializing a target project.

## Modes

State one mode before writing:

- `new-project`: empty, new, or intentionally blank project that needs the UTH docs skeleton.
- `existing-project`: project already has code, docs, an `AGENTS.md`, old task documents, or historical governance material.

If the mode is unclear, ask one concise question. Do not create files until the mode is clear.

## Existing Project Outcomes

- `enable-only`: user asked only to enable UTH. Stop after marker, hook tools, and initial docs scaffold. Backup zip, handoff snapshot, and `uth-docs` route are not required. The closeout must say that UTH enablement is complete and existing-project takeover is not complete.
- `full-takeover`: user asked to take over an existing project. Complete onboarding preflight, route to `uth-docs onboarding-followup`, stop the preflight phase, then resume for final takeover closeout only after independent docs-scene completion evidence.

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
localized current-state entrypoint, if present
package/build/workspace/module declaration files
git status and a small recent git log, if this is a Git repo
top-level directory tree
```

Do not read the full source tree. Onboarding may create only an initial current-state index; it must not claim full source understanding.

## Document Language Preference

Before the first governed Markdown write in a project, resolve the documentation language. This preference applies to generated governance docs and to the user-facing scene closeout report.

- If `.uth-governance/project.json` already has `document_language`, use it.
- If `document_language` is missing, ask one concise question before writing docs:
  `Which language should UTH use for project governance docs? I will save this as the project default.`
- Save the answer in `.uth-governance/project.json` as a long-term project fact.
- Render generated governance docs and the final closeout report in the selected language. Preserve commands, code identifiers, and schema keys exactly.
- Keep hard entry filenames in English: `AGENTS.md` and every directory entry `README.md`.
- Name all other generated governance Markdown files in the selected `document_language`. For `zh-CN`, use Chinese basenames such as `docs/当前状态.md`, `docs/API契约.md`, `docs/数据模型.md`, `docs/领域术语.md`, `docs/界面规则.md`, and `docs/部署.md`; for `en-US`, use English basenames such as `docs/current-state.md`.
- Record the actual localized paths in `.uth-governance/project.json` `entrypoints`; later scenes must read those entrypoints instead of assuming English filenames.
- If the selected language is `zh-CN`, the closeout headings and prose must be Chinese. Do not output English labels such as `Read`, `Created/updated`, or `Current-state`.
- Do not infer the language from the chat language or repository language on first write; ask once and persist it.

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
  "document_language": {
    "code": "zh-CN | en-US | bilingual | custom",
    "label": "Simplified Chinese | English | bilingual | user-specified label",
    "source": "user-selected",
    "selected_at": "YYYY-MM-DDTHH:mm:ss+08:00",
    "applies_to": "governance-docs-and-closeout-reports"
  },
  "entrypoints": {
    "agent": "AGENTS.md",
    "docs": "docs/README.md",
    "current_state": "docs/<localized-current-state>.md",
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

1. Resolve and persist `document_language`.
2. Create `.uth-governance/project.json` with the selected `document_language`.
3. Create the minimal UTH docs scaffold from `references/project-scaffold.md`, rendered in the selected language.
4. Copy `assets/uth-hooks/` to target project `tools/uth-hooks/`.
5. Create a lightweight root `AGENTS.md` only if missing, or append only the minimal project entry if the user allows updating an existing one.
6. Create the localized current-state document named from `document_language`, and record its path in `entrypoints.current_state`.
7. Do not invent tech stack, module boundaries, commands, or architecture facts.
8. Mark unknown facts as `TBD` or `Needs uth-docs`.

Do not create a formal task package during new-project onboarding unless the user explicitly asks.

## Existing Project Backup

For `existing-project full-takeover`, before any documentation-class file write or old-doc cleanup, migration, or classification write, create a documentation backup zip under `docs/`:

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

For `existing-project full-takeover`, create a one-time handoff snapshot:

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

This snapshot is handoff evidence, not a daily log. Later scenes may read it through the docs entrypoint and `entrypoints.current_state` when they need onboarding context.

## Current-State Rules

Onboarding writes only an initial current-state index at the localized `entrypoints.current_state` path.

Allowed content:

- project name
- onboarding status
- repository snapshot
- docs entrypoints
- backup and snapshot paths, when created
- discovered tech-stack clues
- discovered module-boundary clues
- active unknowns
- `uth-docs` follow-up items

Do not state that full architecture, full module boundaries, runtime flow, or business behavior are confirmed unless the evidence was actually read.

Use this wording when the fact needs deeper docs governance:

```text
Needs uth-docs confirmation from code facts.
```

## Existing Project Takeover Transaction

For `existing-project`, first set `takeover_scope` to `enable-only` or `full-takeover`.

Preflight:

1. Select `document_language`; persist it before the first governed Markdown write.
2. Create `.uth-governance/project.json` with the selected `document_language`.
3. Copy project-local hook tools.
4. Create the minimal docs skeleton and initial current-state index. Do not create `docs/context/00-<localized-module-split>.md`; that belongs only to `uth-docs module-split` after large-project split approval.
5. For `full-takeover`, create the backup zip before writing docs, `AGENTS.md`, `README*`, localized current-state docs, snapshots, migrations, or old-doc cleanup/classification records.
6. For `full-takeover`, create the handoff snapshot.
7. For `full-takeover`, route to `uth-docs onboarding-followup` with `origin_scene=uth-onboarding`, `origin_mode=existing-project`, `handoff_type=existing-project-takeover`, `takeover_session_id=ONBYYMMDDXX`, and `return_to=uth-onboarding`.
8. Stop the onboarding preflight phase after the route. The active scene must switch to `uth-docs`; do not continue by executing the docs checklist inline.

For `enable-only`, stop after preflight. The report may say UTH enablement is complete, but must also say existing-project takeover is not complete.

For `full-takeover`, do not ask the user to manually start `uth-docs` unless they explicitly pause onboarding. The `uth-docs onboarding-followup` route owns old docs classification, full-project documentation baseline governance, current-state cleanup, context rebuild or confirmation, archive or migration handling, and extraction of stable old `AGENTS.md` rules. Onboarding preflight must not include `docs_followup_completed`, `docs_completion_level=full-project-docs-complete`, or `return_to_onboarding`.

Final closeout:

1. Read independent `uth-docs` takeover completion evidence, such as `docs_scene_final_record`, `docs_scene_run_id`, or equivalent docs-scene closeout evidence.
2. Require `docs_completion_level=full-project-docs-complete`.
3. Require old docs classified, current-state cleaned, context rebuilt or confirmed, and no active takeover blockers.
4. Report the backup zip path to the user.
5. Only then say existing-project takeover is complete.

Final old-project takeover closeout is allowed only after `uth-docs onboarding-followup` returns full-project completion evidence. Existing-project minimal onboarding alone is not full takeover.

## Write Scope

Allowed writes:

```text
.uth-governance/project.json
tools/uth-hooks/
AGENTS.md
docs/README.md
docs/<localized-current-state>.md
docs/<localized-project-overview>.md
docs/<localized-architecture>.md
docs/<localized-development>.md
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

End with a closeout report rendered in the selected `document_language`. The field names below are semantic requirements; localize the labels and prose. For `zh-CN`, use Chinese labels and Chinese prose while keeping literal paths, commands, skill names, and schema values unchanged.

```text
Scene: uth-onboarding
Mode:
Takeover scope: enable-only | full-takeover
Takeover phase: preflight | final
Read:
Created/updated:
Hook tools:
Backup:
Snapshot:
Project marker:
Document language:
Filename language policy:
Current-state:
Unconfirmed facts:
Docs follow-up:
Docs scene evidence:
Docs completion level:
Old docs classified:
Current-state cleanup:
Context baseline:
Backup zip reported:
Takeover blockers:
UTF-8 guard:
Git writes: none
Next route:
```

For `new-project`, `Next route` is usually `none` or `uth-docs` if more documentation governance was requested.

For `existing-project enable-only`, `Next route` is usually `none`; the report must say UTH enablement is complete and existing-project takeover is not complete.

For `existing-project full-takeover` preflight, `Next route` must be `uth-docs onboarding-followup` unless the user explicitly paused after preflight.

For `existing-project full-takeover` final closeout, `Next route` is usually `none` only after docs follow-up returned independent docs-scene evidence, `docs_completion_level=full-project-docs-complete`, old docs are classified, current-state is cleaned, context is rebuilt or confirmed, no active takeover blockers remain, and the backup zip path is reported.

Never claim full project understanding from onboarding alone. Say `UTH minimal onboarding complete` only for `enable-only` or preflight. The final old-project report may say existing-project takeover is complete only after docs follow-up returns full-project completion evidence.
