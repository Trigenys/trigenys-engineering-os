# Trigenys Engineering OS (TEOS)

**RAIDER-governed engineering skills and multi-agent collaboration toolkit** for Cursor, Claude Code and OpenAI Codex.

> Created through [Trigenys AppFactory](https://github.com/Trigenys/appfactory). Private repository. No production infrastructure is required for this toolkit.

## What lives here

- `skills/` — canonical reusable Agent Skills: product, PMO, business analysis, software architecture, DevOps, DevSecOps, UX/CX, test engineering, research, multi-agent collaboration, cost-aware routing.
- `.cursor/agents/` — Cursor specialist profiles with model routing hints. Model availability and configuration must be validated in the installed Cursor version.
- `AGENTS.md` and `CLAUDE.md` — small, compatible entry points for Codex, Claude Code, and other coding agents.
- `docs/` — RAIDER contract, collaboration protocol, walkthroughs, research and quality gates.
- `scripts/install.py` — safe local installation and project bootstrap. Never auto-overwrites an existing configuration.

**RAIDER:** The AppFactory-generated `AGENTS.md` identifies its engineering principles (reusability, configuration, provider independence, idempotency, regression control, least privilege, testability and adoptability). The canonical definition and expansion of the RAIDER acronym have not yet been established in this repository: see `docs/raider/RAIDER.md`. Do not invent it.

## Install

Clone this repository and run locally (Python 3.10+):

```bash
python scripts/install.py check
python scripts/install.py install-global --dry-run
python scripts/install.py install-global
```

To bootstrap **one explicitly selected** project:

```bash
python scripts/install.py init-project --path /path/to/my-repo --dry-run
python scripts/install.py init-project --path /path/to/my-repo
```

The installer only copies files; it does **not** connect to cloud accounts, deploy, commit, install dependencies, or configure account-level paid usage. Existing paths are skipped by default. See `--help`.

## Task workflow

1. Classify the task and select the smallest useful agent set.
2. Apply canonical RAIDER rules (or mark their unresolved parts `PENDING`).
3. For significant decisions, research the current market and applicable standards, with dated sources.
4. Agree on contracts and Git worktree/file ownership before parallel work.
5. Implement with the lowest-cost competent model.
6. Validate through applicable static, unit, integration, API/contract and E2E gates.
7. Record work in `docs/walkthrough/<task-id>/<timestamp>__<agent>.md`.
8. Obtain human review for destructive, production or paid operations.

Do not assume that Cursor, Claude Code and Codex share live state or model selectors. Their integration is through Git and tracked files, not through a magic cross-provider runtime.

## Status

The repository was bootstrapped from AppFactory's generic `typescript-api` **service** preset because AppFactory currently has no dedicated `skills/toolkit` preset. The generated Node HTTP skeleton is a bootstrap artifact, **not** a deployed TEOS service. Use `npm run check` only if validating that scaffold; TEOS itself is file-based. A dedicated AppFactory toolkit preset is a follow-up improvement.

See `docs/agent-coordination/protocol.md`, `docs/quality/QUALITY-GATES.md`, and `docs/research/SOURCES.md`.
