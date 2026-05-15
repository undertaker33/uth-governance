# UTH Governance Pack

This repository is a distributable UTH engineering-governance pack, not a target project.

Keep this entry short. Full rules live in:

- `README.md`
- `docs/guide/installation.md`
- `AGENT_工程治理启动手册.md`
- `TEMPLATES_工程治理模板.md`
- `HOOKS_工程治理门禁手册.md`
- `skills/`
- `tools/uth-hooks/`
- `scripts/install.py`

Versioning belongs to the outer package folder or release artifact. Do not add
version suffixes to internal handbook/template filenames.

## When Applying This Pack

Follow `docs/guide/installation.md` and prefer `scripts/install.py` when
installing into a target project. The installation still separates three things:

1. **Skills**
   - Copy or install `skills/uth-*` and `skills/uth-sp-*` into the skill directory loaded by the target runtime.
   - If the runtime location is unknown, ask the user where that agent loads skills from.

2. **Tools**
   - Copy `tools/uth-hooks/` into the target project, or keep it as a shared central tool path.
   - The hook runner is `tools/uth-hooks/uth-hook.py`.

3. **Project Governance Docs**
    - Copy governance docs into the target project, normally under `docs/_governance/`.
    - Keep the target project root `AGENTS.md` lightweight: it should point to project facts and `uth-*` skills, not duplicate skill routing or full handbooks.
    - Do not create project docs that restate `uth-*` skill triggers or scene execution flows.

Do not copy this pack's old task packages, archives, `current-state`, or context docs as target-project facts.

## Hook Usage

The packaged hook runner accepts JSON events and returns `PASS`, `WARN`, `ASK`, or `BLOCK`.

```bash
python tools/uth-hooks/uth-hook.py --event event.json --config tools/uth-hooks/config.example.json
```

For stdin:

```bash
echo '{"type":"git-write","active_scene":"uth-git","commands":["git commit -m test"],"git_plan_present":true,"user_git_confirmed":true}' | python tools/uth-hooks/uth-hook.py --event -
```

L1/L2/L3 are implemented in the reference runner:

- L1: ambiguity, scene transitions, worker Prompt dispatch, UTH-SP trigger decision.
- L2: file write scope, Git write confirmation, UTF-8 doc guard, script guard.
- L3: scene closeout evidence gates. L3 checks supplied evidence and documented
  exceptions; it does not rerun expensive compile/test commands.

## Editing This Pack

- Use `skill-creator` when editing any `skills/**` files.
- Use explicit UTH-SP maintenance intent when editing `skills/uth-sp-*/**`.
- Run UTF-8/no-BOM checks after changing governance Markdown or scripts.
- Do not run Git writes unless the user explicitly asks for Git closure.
