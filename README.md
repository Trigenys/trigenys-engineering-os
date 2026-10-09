# Trigenys Engineering OS (TEOS)

**RAIDER-governed engineering skills and multi-agent collaboration toolkit** for Cursor, Claude Code and OpenAI Codex.

> Created through [Trigenys AppFactory](https://github.com/Trigenys/appfactory). Public repository. No production infrastructure is required for this toolkit.

## What lives here

- `skills/` — **44 canonical reusable Agent Skills**: product, PMO, business analysis, architecture, DevOps, DevSecOps, UX/CX, testing, security, GitHub Actions, OIDC, delivery, Cloudflare, AWS, backup/recovery, releases and research.
- `.cursor/agents/` — **19 specialist profiles** for Cursor with model routing hints. Model availability and configuration must be validated in the installed Cursor version.
- `AGENTS.md` and `CLAUDE.md` — small, compatible entry points for Codex, Claude Code, and other coding agents.
- `docs/` — RAIDER contract, collaboration protocol, walkthroughs, research and quality gates.
- `scripts/install.py` — safe local installation and project bootstrap. Never auto-overwrites an existing configuration.

**RAIDER:** The complete [RAIDER Engineering Standard](docs/raider/RAIDER.md) is mirrored from [`EagleFox31/project-registry/RAIDER.md`](https://github.com/EagleFox31/project-registry/blob/main/RAIDER.md) at upstream blob `db1b349e129c8f147f91551ba79f6c1799481756`. RAIDER = **Reusable, Agnostic, Idempotent, Durable / Non-regressive, Engineering-grade, Retroactive**. Its Definition of Done includes failure memory, change-scoped pipelines, reuse-first reconnaissance and brownfield adoption. Keep upstream authoritative.

## Install

Clone this repository and run locally (Python 3.10+):

```bash
python scripts/install.py check
python scripts/install.py compare-local
python scripts/install.py install-global --dry-run
python scripts/install.py install-global
```

To bootstrap **one explicitly selected** project:

```bash
python scripts/install.py init-project --path /path/to/my-repo --dry-run
python scripts/install.py init-project --path /path/to/my-repo
```

Read-only verification: `compare-local --strict` exits 1 unless the installation matches the repository (0 missing, different, redundant and superseded). `validate-project --path /path/to/my-repo` checks walkthrough metadata against `docs/walkthrough/TEMPLATE.md` and that research notes cite a URL and a check date. `check` applies the same rules to this repository, plus the [Agent Skills](https://agentskills.io/specification) naming rules and the pinned RAIDER provenance.

The installer only copies files; it does **not** connect to cloud accounts, deploy, commit, install dependencies, or configure account-level paid usage. Unchanged content is a no-op; differing existing paths are reported but preserved unless you explicitly use `--update`, which first moves them to `~/.teos-backups/<UTC-stamp>/` (never inside a skill folder, where Cursor and Claude Code would load the backup as a Skill).

Skills go to the fewest folders the selected tools read (`--tools`, default `cursor,claude,codex`): Claude Code reads only `.claude/skills`, Codex only `.agents/skills`, and Cursor reads both plus `.cursor/skills`. The default therefore installs in `.claude/skills` and `.agents/skills`, not in all three. `--tools cursor` alone uses `.cursor/skills`, the only folder Cursor syncs to Cloud Agents. Cursor agent profiles are installed only when `cursor` is selected. **Compare the local installation made by another agent before updating it**. The existing local `~/.cursor/trigenys-engineering-os/` suite is not modified by this installer. See `docs/installation/LOCAL-SYNC.md` and `--help`.

## Task workflow

1. Classify the task and select the smallest useful agent set.
2. Apply the canonical RAIDER Definition of Done, documenting justified exceptions.
3. For significant decisions, research the current market and applicable standards, with dated sources.
4. Agree on contracts and Git worktree/file ownership before parallel work.
5. Implement with the lowest-cost competent model.
6. Validate through applicable static, unit, integration, API/contract and E2E gates.
7. Record work in `docs/walkthrough/<task-id>/<timestamp>__<agent>.md`.
8. Obtain human review for destructive, production or paid operations.

Do not assume that Cursor, Claude Code and Codex share live state or model selectors. Their integration is through Git and tracked files, not through a magic cross-provider runtime.

## Status

The repository was bootstrapped from AppFactory's generic `typescript-api` **service** preset because AppFactory currently has no dedicated `skills/toolkit` preset. The generated Node HTTP skeleton is a bootstrap artifact, **not** a deployed TEOS service. Use `npm run check` only if validating that scaffold; TEOS itself is file-based. A dedicated AppFactory toolkit preset is a follow-up improvement.

See `docs/agent-coordination/protocol.md`, `docs/quality/QUALITY-GATES.md`, `docs/research/SOURCES.md`, [`docs/skills/CI-SKILLS-MAP.md`](docs/skills/CI-SKILLS-MAP.md) and the public-source cross-repo audit [`docs/audits/2026-10-09-ci-workflow-audit.md`](docs/audits/2026-10-09-ci-workflow-audit.md).
