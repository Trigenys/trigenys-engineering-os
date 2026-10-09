#!/usr/bin/env python3
"""Safe local installer for Trigenys Engineering OS (no network, no dependencies)."""
from __future__ import annotations

import argparse
import datetime as dt
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
CURSOR_AGENTS = ROOT / ".cursor" / "agents"
DOC_FILES = [
    "docs/raider/RAIDER.md",
    "docs/agent-coordination/protocol.md",
    "docs/walkthrough/TEMPLATE.md",
    "docs/quality/QUALITY-GATES.md",
    "docs/research/SOURCES.md",
]

def check() -> int:
    problems: list[str] = []
    names: set[str] = set()
    skill_files = sorted(SKILLS.glob("*/SKILL.md"))
    agent_files = sorted(CURSOR_AGENTS.glob("*.md"))
    for f in skill_files:
        text = f.read_text(encoding="utf-8")
        if not text.startswith("---\n") or "\n---\n" not in text[4:]:
            problems.append(f"{f}: frontmatter absent")
            continue
        frontmatter = text.split("---", 2)[1]
        expected_name = f.parent.name
        if f"name: {expected_name}" not in frontmatter:
            problems.append(f"{f}: name incorrect")
        if expected_name in names:
            problems.append(f"{f}: nom dupliqué")
        names.add(expected_name)
        if "description:" not in frontmatter:
            problems.append(f"{f}: description manquante")
    for f in agent_files:
        text = f.read_text(encoding="utf-8")
        if not text.startswith("---\n") or "\n---\n" not in text[4:]:
            problems.append(f"{f}: frontmatter absent")
            continue
        frontmatter = text.split("---", 2)[1]
        for field in ("name:", "description:", "model:", "readonly:"):
            if field not in frontmatter:
                problems.append(f"{f}: {field} manquant")
    for relative in ["AGENTS.md", "CLAUDE.md", *DOC_FILES]:
        if not (ROOT / relative).is_file():
            problems.append(f"{relative}: manquant")
    print(f"Found {len(skill_files)} skills, {len(agent_files)} Cursor agents")
    if problems:
        for problem in problems:
            print("FAIL:", problem)
        return 1
    if len(skill_files) != 26 or len(agent_files) != 15:
        print("WARN: expected 26 skills and 15 agents; inspect pending files")
        return 1
    print("Static configuration check PASSED")
    print("Runtime model availability, online research and agent routing NOT VERIFIED")
    return 0

def copy_safely(src: Path, dst: Path, dry_run: bool, update: bool) -> str:
    if not src.exists():
        return f"MISSING {src}"
    if dst.exists() and not update:
        return f"SKIP existing {dst}"
    if dst.exists() and update:
        stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        backup = dst.with_name(dst.name + ".bak-" + stamp)
        index = 1
        while backup.exists():
            backup = dst.with_name(dst.name + f".bak-{stamp}-{index}")
            index += 1
        if not dry_run:
            backup.parent.mkdir(parents=True, exist_ok=True)
            dst.rename(backup)
        label = f"BACKUP {dst} -> {backup}; "
    else:
        label = ""
    if dry_run:
        return label + f"WOULD COPY {src} -> {dst}"
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.is_dir():
        shutil.copytree(src, dst)
    else:
        shutil.copy2(src, dst)
    return label + f"COPIED {src} -> {dst}"

def install_global(dry_run: bool, update: bool) -> None:
    home = Path.home()
    operations: list[tuple[Path, Path]] = []
    for directory in sorted(SKILLS.iterdir()):
        if not directory.is_dir() or not (directory / "SKILL.md").exists():
            continue
        for prefix in (".cursor", ".claude", ".agents"):
            operations.append((directory, home / prefix / "skills" / directory.name))
    for agent in sorted(CURSOR_AGENTS.glob("*.md")):
        operations.append((agent, home / ".cursor" / "agents" / agent.name))
    for src, dst in operations:
        print(copy_safely(src, dst, dry_run, update))
    print("Local user settings were not altered. Cursor model selection still requires verification.")

def init_project(directory: Path, dry_run: bool, update: bool) -> None:
    target = directory.expanduser().resolve()
    if not target.is_dir() or not (target / ".git").exists():
        raise ValueError("Choose an existing local Git working tree with --path")
    operations: list[tuple[Path, Path]] = []
    for fname in ("AGENTS.md", "CLAUDE.md"):
        operations.append((ROOT / fname, target / fname))
    for relative in DOC_FILES:
        operations.append((ROOT / relative, target / relative))
    for skill in sorted(SKILLS.iterdir()):
        if not skill.is_dir() or not (skill / "SKILL.md").exists():
            continue
        for prefix in (".cursor", ".claude", ".agents"):
            operations.append((skill, target / prefix / "skills" / skill.name))
    for agent in sorted(CURSOR_AGENTS.glob("*.md")):
        operations.append((agent, target / ".cursor" / "agents" / agent.name))
    for src, dst in operations:
        print(copy_safely(src, dst, dry_run, update))
    print("Project bootstrap complete; no cloud calls, Git commits, dependency installs or deployments.")

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("check")
    for mode in ("install-global", "init-project"):
        p = commands.add_parser(mode)
        p.add_argument("--dry-run", action="store_true")
        p.add_argument("--update", action="store_true",
                       help="Explicitly replace existing paths after timestamped backups")
        if mode == "init-project":
            p.add_argument("--path", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "check":
        return check()
    try:
        if args.command == "install-global":
            install_global(args.dry_run, args.update)
        elif args.command == "init-project":
            init_project(args.path, args.dry_run, args.update)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
