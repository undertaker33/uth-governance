---
name: uth-utf8-guard
description: Use when Codex will modify governed Markdown or text documentation such as AGENTS.md, root README.md, docs/**/*.md, docs/_governance templates, or task-package Markdown. Also use after such edits to verify UTF-8 decoding, mojibake risk, and Markdown fence balance. Not for ordinary source-code edits unless the file is governed documentation.
---

# UTH UTF-8 Guard

## Purpose

Use this skill as a document-encoding guard for UTH governance docs. It prevents Chinese Markdown and governance text from being written back with broken encoding or obvious mojibake.

## Trigger

Use before and after modifying:

- `AGENTS.md`
- root `README.md`
- `docs/**/*.md`
- task-package Markdown under `docs/work/`
- governed templates or manuals
- `skills/**/*.md` only when the user explicitly invoked `skill-creator`
- `skills/uth-sp-*/**/*.md` only during explicit UTH-SP maintenance

Do not use for normal code files, generated files, binary files, lock files, build outputs, or unrelated text unless the user asks.

## Guard Protocol

Before writing:

1. If the file exists, read it as bytes and confirm it decodes as UTF-8.
2. Note whether the file already has unusual encoding, replacement characters, or mojibake markers.
3. Do not normalize unrelated line endings or rewrite unrelated content.

After writing:

1. Read the file as UTF-8.
2. Check for Unicode replacement characters.
3. Check common mojibake markers using the bundled script list.
4. For Markdown, check that fenced code blocks are balanced.
5. If any check fails, block closeout and repair the document before continuing.

## Script

Use the bundled checker when possible:

```powershell
python .\skills\uth-utf8-guard\scripts\check_utf8_docs.py <path> [<path> ...]
```

It validates UTF-8 decoding, scans for mojibake markers, and checks Markdown fence parity.

## Closeout

When this guard is used, include:

```text
UTF-8 guard:
- files checked:
- result:
- repaired encoding issues:
```

If the guard was required but not run, do not claim documentation closeout is complete.
