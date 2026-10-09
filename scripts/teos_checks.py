"""Read-only content checks shared by `install.py check` and `install.py validate-project`.

Each function returns a list of problems; an empty list means the check passed.
"""
from __future__ import annotations

import re
from pathlib import Path

# https://agentskills.io/specification (name and description constraints)
SKILL_NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SKILL_NAME_MAX = 64
DESCRIPTION_MAX = 1024
AGENT_FIELDS = ("name", "description", "model", "readonly")
RAIDER_UPSTREAM = "https://github.com/EagleFox31/project-registry/blob/"
SHA = re.compile(r"\b[0-9a-f]{40}\b")
ISO_DATE = re.compile(r"\b20\d{2}-\d{2}-\d{2}\b")
URL = re.compile(r"https?://", re.IGNORECASE)
NOT_NOTES = {"readme.md", "template.md", "sources.md"}


def frontmatter(text: str) -> dict[str, str] | None:
    """Top-level `key: value` pairs of a leading YAML block, or None if absent.

    Indented lines (nested maps such as `metadata:`) are skipped.
    """
    text = text.replace("\r\n", "\n")
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 3)
    if end == -1:
        return None
    fields: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line.strip() or line[0].isspace() or line.lstrip().startswith("#"):
            continue
        key, sep, value = line.partition(":")
        if sep:
            fields[key.strip()] = value.strip().strip("\"'")
    return fields


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def skill_problems(skill_md: Path) -> list[str]:
    fields = frontmatter(_read(skill_md))
    if fields is None:
        return [f"{skill_md}: frontmatter absent"]
    folder = skill_md.parent.name
    name = fields.get("name", "")
    description = fields.get("description", "")
    problems = []
    if name != folder:
        problems.append(f"{skill_md}: name {name!r} must equal folder {folder!r}")
    if not SKILL_NAME.match(name) or len(name) > SKILL_NAME_MAX:
        problems.append(f"{skill_md}: name {name!r} violates the Agent Skills naming rules")
    if not description:
        problems.append(f"{skill_md}: description missing")
    elif len(description) > DESCRIPTION_MAX:
        problems.append(f"{skill_md}: description longer than {DESCRIPTION_MAX} characters")
    return problems


def agent_problems(agent_md: Path) -> list[str]:
    fields = frontmatter(_read(agent_md))
    if fields is None:
        return [f"{agent_md}: frontmatter absent"]
    problems = [f"{agent_md}: {field} missing" for field in AGENT_FIELDS if not fields.get(field)]
    if fields.get("name") and fields["name"] != agent_md.stem:
        problems.append(f"{agent_md}: name {fields['name']!r} must equal file name {agent_md.stem!r}")
    if fields.get("readonly") and fields["readonly"] not in {"true", "false"}:
        problems.append(f"{agent_md}: readonly must be true or false")
    return problems


def raider_provenance_problems(raider_md: Path) -> list[str]:
    """The mirror must name its upstream commit so drift can be detected."""
    first_line = _read(raider_md).lstrip().splitlines()[0] if raider_md.is_file() else ""
    if RAIDER_UPSTREAM not in first_line or not SHA.search(first_line):
        return [f"{raider_md}: first line must cite {RAIDER_UPSTREAM}<40-hex SHA>"]
    return []


def required_keys(template: Path) -> list[str]:
    fields = frontmatter(_read(template))
    if not fields:
        raise ValueError(f"{template}: template has no frontmatter")
    return list(fields)


def walkthrough_problems(root: Path, keys: list[str]) -> list[str]:
    """Every dated walkthrough carries the metadata of the template."""
    problems = []
    for path in sorted((root / "docs" / "walkthrough").rglob("*.md")):
        if path.name.lower() in NOT_NOTES:
            continue
        fields = frontmatter(_read(path))
        if fields is None:
            problems.append(f"{path}: frontmatter absent")
            continue
        problems.extend(f"{path}: {key} missing" for key in keys if key not in fields)
    return problems


def research_problems(root: Path) -> list[str]:
    """Research notes cite at least one URL and a check date, unless marked blocked."""
    problems = []
    for path in sorted((root / "docs" / "research").rglob("*.md")):
        if path.name.lower() in NOT_NOTES:
            continue
        text = _read(path)
        if "RESEARCH_BLOCKED" in text:
            continue
        if not URL.search(text):
            problems.append(f"{path}: no source URL")
        if not ISO_DATE.search(text):
            problems.append(f"{path}: no YYYY-MM-DD check date")
    return problems
