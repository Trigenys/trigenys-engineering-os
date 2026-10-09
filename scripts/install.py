#!/usr/bin/env python3
"""Safe local installer for Trigenys Engineering OS (no network, no dependencies)."""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import shutil
import sys
from pathlib import Path

import teos_checks

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

EXPECTED_SKILLS = 44
EXPECTED_AGENTS = 19
TOOLS = ("cursor", "claude", "codex")
BACKUP_DIRNAME = ".teos-backups"

# Profiles renamed upstream; an older local copy keeps loading next to the new one.
SUPERSEDED_AGENTS = {
    "devsecops-security-architect.md": "devsecops-architect.md",
    "senior-project-manager.md": "project-manager.md",
    "principal-qa-automation-engineer.md": "qa-automation-engineer.md",
    "ux-ui-cx-strategist.md": "ux-cx-strategist.md",
}


def skill_prefixes(tools: set[str]) -> list[str]:
    """Smallest set of skill roots covering the selected tools.

    Claude Code reads only .claude/skills and Codex only .agents/skills, while
    Cursor reads .cursor, .claude and .agents. Installing in every root would make
    Cursor load each Skill several times.
    """
    prefixes: list[str] = []
    if "claude" in tools:
        prefixes.append(".claude")
    if "codex" in tools:
        prefixes.append(".agents")
    if "cursor" in tools and not prefixes:
        # Only ~/.cursor/skills is synced to Cursor Cloud Agents.
        prefixes.append(".cursor")
    return prefixes


def parse_tools(value: str) -> set[str]:
    tools = {t.strip() for t in value.split(",") if t.strip()}
    unknown = tools - set(TOOLS)
    if not tools or unknown:
        raise argparse.ArgumentTypeError(
            f"--tools expects a comma-separated subset of {','.join(TOOLS)}")
    return tools

def walkthrough_keys() -> list[str]:
    return teos_checks.required_keys(ROOT / "docs" / "walkthrough" / "TEMPLATE.md")


def validate_project(directory: Path) -> int:
    """Read-only: walkthrough metadata and research notes of a project using TEOS."""
    target = directory.expanduser().resolve()
    if not target.is_dir():
        raise ValueError(f"Not a directory: {target}")
    problems = (teos_checks.walkthrough_problems(target, walkthrough_keys())
                + teos_checks.research_problems(target))
    for problem in problems:
        print("FAIL:", problem)
    print(f"Project validation {'FAILED' if problems else 'PASSED'}: {target} (no files modified)")
    return 1 if problems else 0


def check() -> int:
    problems: list[str] = []
    skill_files = sorted(SKILLS.glob("*/SKILL.md"))
    agent_files = sorted(CURSOR_AGENTS.glob("*.md"))
    for f in skill_files:
        problems.extend(teos_checks.skill_problems(f))
    for f in agent_files:
        problems.extend(teos_checks.agent_problems(f))
    raider_path = ROOT / "docs" / "raider" / "RAIDER.md"
    problems.extend(teos_checks.raider_provenance_problems(raider_path))
    problems.extend(teos_checks.walkthrough_problems(ROOT, walkthrough_keys()))
    problems.extend(teos_checks.research_problems(ROOT))
    if raider_path.is_file():
        raider = raider_path.read_text(encoding="utf-8")
        for principle in ("## R — Reusable", "## A — Agnostic", "## I — Idempotent",
                          "## D — Durable / Non-regressive", "## E — Engineering-grade",
                          "## R — Retroactive", "## Definition of Done RAIDER",
                          "Failure Memory / Continuous Learning"):
            if principle not in raider:
                problems.append(f"Canonical RAIDER principle missing: {principle}")
    for relative in ["AGENTS.md", "CLAUDE.md", *DOC_FILES]:
        if not (ROOT / relative).is_file():
            problems.append(f"{relative}: manquant")
    print(f"Found {len(skill_files)} skills, {len(agent_files)} Cursor agents")
    if problems:
        for problem in problems:
            print("FAIL:", problem)
        return 1
    if len(skill_files) != EXPECTED_SKILLS or len(agent_files) != EXPECTED_AGENTS:
        print(f"WARN: expected {EXPECTED_SKILLS} skills and {EXPECTED_AGENTS} agents; "
              "inspect pending files")
        return 1
    print("Static configuration check PASSED")
    print("Runtime model availability, online research and agent routing NOT VERIFIED")
    return 0

def _content_digest(path: Path) -> str:
    """Stable content fingerprint across files and entire Skill directories."""
    h = hashlib.sha256()
    if path.is_file():
        h.update(b"file\\0")
        h.update(path.read_bytes())
    elif path.is_dir():
        h.update(b"directory\\0")
        for child in sorted(p for p in path.rglob("*") if p.is_file()):
            h.update(child.relative_to(path).as_posix().encode("utf-8"))
            h.update(b"\\0")
            h.update(child.read_bytes())
            h.update(b"\\0")
    else:
        h.update(b"unknown\\0")
    return h.hexdigest()


def canonical_skills() -> list[Path]:
    return [d for d in sorted(SKILLS.iterdir()) if d.is_dir() and (d / "SKILL.md").is_file()]


def skill_operations(base: Path, tools: set[str]) -> list[tuple[Path, Path]]:
    return [(skill, base / prefix / "skills" / skill.name)
            for skill in canonical_skills() for prefix in skill_prefixes(tools)]


def global_operations(tools: set[str]) -> list[tuple[Path, Path]]:
    home = Path.home()
    ops = skill_operations(home, tools)
    if "cursor" in tools:
        for agent in sorted(CURSOR_AGENTS.glob("*.md")):
            ops.append((agent, home / ".cursor" / "agents" / agent.name))
    return ops


def compare_local(tools: set[str]) -> int:
    """Read-only compare against existing installations; no secrets are read out.

    Returns the number of entries that differ from the expected installed state.
    """
    home = Path.home()
    stats = {"SAME": 0, "MISSING": 0, "DIFFERENT": 0}
    for src, dst in global_operations(tools):
        if not dst.exists():
            status = "MISSING"
        elif _content_digest(src) == _content_digest(dst):
            status = "SAME"
        else:
            status = "DIFFERENT"
        stats[status] += 1
        print(f"{status} {dst}")
    known_skills = {skill.name for skill in canonical_skills()}
    targets = skill_prefixes(tools)
    redundant = 0
    for prefix in (".cursor", ".claude", ".agents"):
        folder = home / prefix / "skills"
        if not folder.is_dir():
            continue
        for path in sorted(folder.iterdir()):
            if not path.is_dir():
                continue
            if path.name not in known_skills:
                print(f"LOCAL-ONLY (preserve) {path}")
            elif prefix not in targets:
                redundant += 1
                print(f"REDUNDANT (Cursor also loads it from {', '.join(targets)}; "
                      f"review, then remove manually) {path}")
    folder = home / ".cursor" / "agents"
    superseded = 0
    if folder.is_dir():
        known = {src.name for src in CURSOR_AGENTS.glob("*.md")}
        for path in sorted(folder.glob("*.md")):
            if path.name in SUPERSEDED_AGENTS:
                superseded += 1
                print(f"SUPERSEDED by {SUPERSEDED_AGENTS[path.name]} "
                      f"(review, then remove manually) {path}")
            elif path.name not in known:
                print(f"LOCAL-ONLY (preserve) {path}")
    extra = home / ".cursor" / "trigenys-engineering-os"
    if extra.exists():
        print(f"LOCAL-ONLY OS framework (not modified) {extra}")
    print(f"Comparison: {stats['SAME']} same, {stats['MISSING']} missing, "
          f"{stats['DIFFERENT']} different, {redundant} redundant, "
          f"{superseded} superseded. No files modified.")
    return stats["MISSING"] + stats["DIFFERENT"] + redundant + superseded


def backup_path(dst: Path, stamp: str) -> Path:
    """Backups live outside every skill root: Cursor scans skill roots recursively and
    Claude Code turns any sibling folder into a skill."""
    home = Path.home()
    try:
        relative = dst.relative_to(home)
    except ValueError:
        relative = Path(*dst.parts[1:])
    candidate = home / BACKUP_DIRNAME / stamp / relative
    index = 1
    while candidate.exists():
        candidate = home / BACKUP_DIRNAME / f"{stamp}-{index}" / relative
        index += 1
    return candidate


def copy_safely(src: Path, dst: Path, dry_run: bool, update: bool, stamp: str) -> str:
    if not src.exists():
        return f"MISSING {src}"
    if dst.exists() and _content_digest(src) == _content_digest(dst):
        return f"SKIP identical {dst}"
    if dst.exists() and not update:
        return f"DRIFT preserved {dst} (review with compare-local before --update)"
    if dst.exists() and update:
        backup = backup_path(dst, stamp)
        if not dry_run:
            backup.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(dst), str(backup))
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

def run_stamp() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def install_global(dry_run: bool, update: bool, tools: set[str]) -> None:
    stamp = run_stamp()
    for src, dst in global_operations(tools):
        print(copy_safely(src, dst, dry_run, update, stamp))
    print("Local user settings were not altered. Cursor model selection still requires verification.")

def init_project(directory: Path, dry_run: bool, update: bool, tools: set[str]) -> None:
    target = directory.expanduser().resolve()
    if not target.is_dir() or not (target / ".git").exists():
        raise ValueError("Choose an existing local Git working tree with --path")
    operations: list[tuple[Path, Path]] = []
    for fname in ("AGENTS.md", "CLAUDE.md"):
        operations.append((ROOT / fname, target / fname))
    for relative in DOC_FILES:
        operations.append((ROOT / relative, target / relative))
    operations.extend(skill_operations(target, tools))
    if "cursor" in tools:
        for agent in sorted(CURSOR_AGENTS.glob("*.md")):
            operations.append((agent, target / ".cursor" / "agents" / agent.name))
    stamp = run_stamp()
    for src, dst in operations:
        print(copy_safely(src, dst, dry_run, update, stamp))
    print("Project bootstrap complete; no cloud calls, Git commits, dependency installs or deployments.")

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("check")
    tools_help = ("Comma-separated tools to serve (default: cursor,claude,codex). "
                  "Skills go to the fewest roots those tools read.")
    compare = commands.add_parser("compare-local")
    compare.add_argument("--tools", type=parse_tools, default=set(TOOLS), help=tools_help)
    compare.add_argument("--strict", action="store_true",
                         help="Exit 1 unless 0 missing, different, redundant and superseded")
    project = commands.add_parser("validate-project")
    project.add_argument("--path", type=Path, required=True)
    for mode in ("install-global", "init-project"):
        p = commands.add_parser(mode)
        p.add_argument("--dry-run", action="store_true")
        p.add_argument("--update", action="store_true",
                       help=f"Replace differing paths after a backup in ~/{BACKUP_DIRNAME}/")
        p.add_argument("--tools", type=parse_tools, default=set(TOOLS), help=tools_help)
        if mode == "init-project":
            p.add_argument("--path", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "check":
        return check()
    if args.command == "compare-local":
        deviations = compare_local(args.tools)
        return 1 if args.strict and deviations else 0
    try:
        if args.command == "validate-project":
            return validate_project(args.path)
        if args.command == "install-global":
            install_global(args.dry_run, args.update, args.tools)
        elif args.command == "init-project":
            init_project(args.path, args.dry_run, args.update, args.tools)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
