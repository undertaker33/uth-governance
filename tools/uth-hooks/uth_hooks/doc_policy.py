from __future__ import annotations

import re

HARD_ENTRY_MARKDOWN_BASENAMES = frozenset({"AGENTS.md", "README.md"})

DEFAULT_ENGLISH_DOC_BASENAMES = frozenset(
    {
        "architecture.md",
        "api-contract.md",
        "current-state.md",
        "data-model.md",
        "deployment.md",
        "development.md",
        "domain-glossary.md",
        "module-split.md",
        "project-overview.md",
        "ui-guidelines.md",
    }
)

ENGLISH_DOCUMENT_LANGUAGE_CODES = frozenset({"en", "en-us", "english"})
GLOBAL_DOC_GOVERNANCE_SCENES = frozenset({"uth-docs", "uth-onboarding"})
MODULE_CONTEXT_FILENAME_RE = re.compile(r"^\d{2}-.+\.md$", re.IGNORECASE)
MODULE_CONTEXT_PREFIX_RE = re.compile(r"^\d{2}-")
MODULE_CONTEXT_ZERO_PREFIX_RE = re.compile(r"^00-.+\.md$", re.IGNORECASE)
MODULE_SPLIT_PLAN_BASENAMES = frozenset({"00-module-split.md", "00-模块拆分.md"})
CONTEXT_OVERVIEW_BASENAMES = frozenset({"00-overview.md", "00-概览.md"})


def normalize_policy_path(path: str) -> str:
    clean = str(path).replace("\\", "/").strip()
    while clean.startswith("./"):
        clean = clean[2:]
    return clean


def path_basename(path: str) -> str:
    return normalize_policy_path(path).rsplit("/", 1)[-1]


def is_markdown_path(path: str) -> bool:
    return normalize_policy_path(path).lower().endswith((".md", ".markdown"))


def is_hard_entry_markdown_path(path: str) -> bool:
    return path_basename(path).lower() in {name.lower() for name in HARD_ENTRY_MARKDOWN_BASENAMES}


def is_governed_markdown_path(path: str) -> bool:
    normalized = normalize_policy_path(path)
    lower = normalized.lower()
    return is_markdown_path(normalized) and (
        lower.startswith("docs/")
        or path_basename(normalized).lower() in {name.lower() for name in HARD_ENTRY_MARKDOWN_BASENAMES}
    )


def is_default_english_governance_filename(path: str) -> bool:
    if not is_governed_markdown_path(path) or is_hard_entry_markdown_path(path):
        return False
    basename = path_basename(path).lower()
    unnumbered = MODULE_CONTEXT_PREFIX_RE.sub("", basename)
    return basename in {name.lower() for name in DEFAULT_ENGLISH_DOC_BASENAMES} or unnumbered in {
        name.lower() for name in DEFAULT_ENGLISH_DOC_BASENAMES
    }


def is_module_context_markdown_path(path: str) -> bool:
    normalized = normalize_policy_path(path)
    return (
        normalized.lower().startswith("docs/context/")
        and is_markdown_path(normalized)
        and not is_hard_entry_markdown_path(normalized)
    )


def module_context_filename_numbered(path: str) -> bool:
    return bool(MODULE_CONTEXT_FILENAME_RE.match(path_basename(path)))


def is_reserved_zero_module_context_path(path: str) -> bool:
    return is_module_context_markdown_path(path) and bool(MODULE_CONTEXT_ZERO_PREFIX_RE.match(path_basename(path)))


def is_module_split_plan_context_path(path: str) -> bool:
    return is_module_context_markdown_path(path) and path_basename(path).lower() in MODULE_SPLIT_PLAN_BASENAMES


def is_context_overview_path(path: str) -> bool:
    return is_module_context_markdown_path(path) and path_basename(path).lower() in CONTEXT_OVERVIEW_BASENAMES


def is_global_docs_markdown_path(path: str) -> bool:
    normalized = normalize_policy_path(path)
    lower = normalized.lower()
    return lower.startswith("docs/") and "/" not in normalized[len("docs/") :] and is_markdown_path(normalized)


def can_govern_global_docs(scene: str | None) -> bool:
    return scene in GLOBAL_DOC_GOVERNANCE_SCENES


def is_non_english_document_language(code: str | None) -> bool:
    normalized = (code or "").strip().lower()
    return bool(normalized) and normalized not in ENGLISH_DOCUMENT_LANGUAGE_CODES
