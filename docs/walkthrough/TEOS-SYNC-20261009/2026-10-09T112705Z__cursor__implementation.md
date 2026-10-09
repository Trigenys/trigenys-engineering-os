---
task_id: TEOS-SYNC-20261009
agent: implementation
provider: cursor
model_reported: Claude Opus 5.5 (parent session, as reported by the Cursor session; not independently verified)
owner: lawry (user)
branch: agent/cursor/teos-sync-20261009
created_at_utc: 2026-10-09T11:27:05Z
related_issue: null
status: NEEDS_REVIEW
---

# Objective and acceptance criteria

Make `install-global --update` safe to run on the Windows machine that already holds a separate local TEOS install, so the repository becomes the single Skill library for Cursor, Claude Code and Codex.

- A replaced Skill is backed up outside every folder a tool scans for Skills.
- Each Skill is installed in the fewest roots that cover the selected tools.
- `compare-local` reports renamed local agents and redundant Skill copies, without deleting anything.
- Agent 14 (Implementation Engineer) of the TEOS mission exists in the repository.
- Re-running the install is a no-op.

# Initial state and scope

Repo at `be00440`. On the machine, read-only runs of `check` (PASSED, 44/18), `compare-local` (0 same / 38 different / 112 missing) and `install-global --dry-run` (112 would copy, 38 drift preserved). Scope: `scripts/install.py`, a new test file, one new agent profile, CI step, README, `LOCAL-SYNC.md`, lessons-learned. Local files on the machine were not modified.

# RAIDER evidence

- **Reusable / Agnostic**: tool selection is a `--tools` option; paths derive from `Path.home()` or `--path`.
- **Idempotent**: `test_second_run_is_a_noop`.
- **Durable**: `DRIFT preserved` behaviour kept without `--update` (`test_drift_is_preserved_without_update`). Behaviour change: the default no longer writes to `.cursor/skills`. Existing copies there are reported `REDUNDANT`, never deleted.
- **Failure memory**: near-miss entry added to `docs/engineering/lessons-learned.md`.
- **Engineering-grade**: unit tests in TEOS Skills CI.
- **Reuse-first**: stdlib `unittest`, no new dependency.
- **Retroactive**: `SUPERSEDED` / `REDUNDANT` reporting exists for brownfield installs.

# Research

- https://cursor.com/docs/skills (2026-10-09): Cursor loads `.agents/skills`, `.cursor/skills`, `~/.agents/skills`, `~/.cursor/skills`, plus `.claude/skills`, `.codex/skills` and the home equivalents for compatibility; walks skill roots recursively; only `~/.cursor/skills` syncs to Cloud Agents.
- https://code.claude.com/docs/en/skills (2026-10-09): Claude Code reads `~/.claude/skills/<name>/SKILL.md` and `.claude/skills`; the directory name becomes the command.
- https://developers.openai.com/codex/skills (2026-10-09): Codex reads `.agents/skills` up to the repo root and `$HOME/.agents/skills`; same-name skills are not merged.
- https://docs.x.ai/developers/model-capabilities/text/reasoning and a Cursor forum thread on SDK `params` (2026-10-09): `grok-4.7` effort is `reasoning_effort`, default `high`. The repository's `grok-4.7[reasoning_effort=high,fast=false]` is left unchanged.

# Decisions and architecture impact

- Default `--tools cursor,claude,codex` installs in `.claude/skills` and `.agents/skills`. Any setup that serves both Claude Code and Codex leaves two copies visible to Cursor; how Cursor handles two same-name Skills is **not verified**.
- `--tools cursor` alone keeps `.cursor/skills` for Cloud Agent sync.
- Cursor agent profiles are installed only when `cursor` is selected.
- `readonly: true` on most agents is left as is (owner decision, not a defect).

# Files changed

- `scripts/install.py` — `--tools`, `skill_prefixes`, backups in `~/.teos-backups/<stamp>/`, `REDUNDANT` / `SUPERSEDED` reporting, expected agent count 19.
- `scripts/test_install.py` — 13 unit tests.
- `.cursor/agents/implementation-engineer.md` — Agent 14.
- `.github/workflows/skills-ci.yml` — runs the unit tests.
- `.gitignore` — `__pycache__/`.
- `README.md`, `docs/installation/LOCAL-SYNC.md`, `docs/engineering/lessons-learned.md`.

# Tests

| Gate | Status | Command / Evidence |
|---|---|---|
| Static | PASSED | `python scripts/install.py check` → 44 skills, 19 agents |
| Unit | PASSED | `python -m unittest discover -s scripts -p "test_*.py"` → 13 tests OK (Python 3.14.7, Windows) |
| Integration | PASSED | `install-global --dry-run`; `init-project --dry-run` in a fresh `git init` repo, `AGENTS.md` not created; `compare-local` on the real machine: 0 same / 96 missing / 11 different / 28 redundant / 4 superseded, no file modified |
| API/Contract | N/A | no API |
| E2E | NOT RUN | real `--update` on the machine is pending user approval |
| Security | N/A | no credentials or network calls added |
| Accessibility/Performance | N/A | |

The tests were not run against the previous `install.py` (its signatures differ), so they do not by themselves demonstrate the old failure.

# Risks, limitations and remaining work

- Cursor display of the same Skill from two roots is unverified.
- On the machine, after merge: back up and remove the 28 `REDUNDANT` Skills and 4 `SUPERSEDED` agents, then `install-global --update`.
- The local scripts in `~/.cursor/trigenys-engineering-os/` are not imported; archive them once the repo install is in place.

# Handoff / next agent

Review the PR, then run the machine steps in `docs/installation/LOCAL-SYNC.md`.

# Final status

NEEDS REVIEW
