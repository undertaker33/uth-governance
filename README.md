# UTH Governance

UTH Governance is a lightweight engineering-governance pack for coding agents.
It focuses on when to read documents, when to write documents, what context to
load, and how to close engineering work without turning every task into a
heavyweight process.

## Install With an Agent

Ask your coding agent to install the pack by following the installation guide:

```text
Install UTH Governance from GitHub:
https://github.com/undertaker33/uth-governance.git

Follow docs/guide/installation.md from that repository.
Use runtime codex.
Do not initialize the current project during installation.
```

If the repository is private, make sure the agent's Git environment can access
GitHub first. An equivalent SSH clone URL is fine when SSH is configured.

## Manual Install

Clone the repository, then run the installer:

```bash
git clone https://github.com/undertaker33/uth-governance.git
cd uth-governance
python scripts/install.py --runtime codex
```

Use `--runtime claude`, `--runtime opencode`, or `--skills-dir <path>` when the
target agent loads skills from a different location.

The installer only installs global skills:

- UTH scene skills and UTH-SP method skills.

It does not install hook tools globally, does not create project docs, does not
edit the current project `AGENTS.md`, and does not create
`.uth-governance/project.json`.

## Enable UTH In a Project

After installation, open the target project and explicitly run:

```text
/uth-onboarding
```

or tell the agent:

```text
Use uth-onboarding to enable UTH governance for this project.
```

`uth-onboarding` creates the project-level marker, copies project-local
`tools/uth-hooks/`, and creates the minimal docs scaffold.
Other `uth-*` scenes stay silent in projects that do not have
`.uth-governance/project.json`, unless the user explicitly asks to enable UTH.
The `.uth-governance/` directory is project-local only.

## Package Contents

- `skills/`: UTH scene skills and UTH-SP method skills.
- `tools/uth-hooks/`: reference L1/L2/L3 hook runner, copied into a target project by `uth-onboarding`.
- `docs/AGENT_工程治理启动手册.md`: governance handbook.
- `docs/TEMPLATES_工程治理模板.md`: document templates.
- `docs/HOOKS_工程治理门禁手册.md`: hook gate manual.
- `docs/FLOW_全链路流程图.md`: scene and hook flow diagrams.
- `docs/guide/installation.md`: install guide for humans and agents.

Versioning belongs to the outer package folder or release artifact. Internal
handbook/template filenames intentionally do not carry version suffixes.
