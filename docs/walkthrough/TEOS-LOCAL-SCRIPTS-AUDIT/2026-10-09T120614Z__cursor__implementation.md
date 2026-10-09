---
task_id: TEOS-LOCAL-SCRIPTS-AUDIT
agent: implementation
provider: cursor
model_reported: Claude Opus 5.5 (parent session, as reported by the Cursor session; not independently verified)
owner: lawry (user)
branch: agent/cursor/teos-local-scripts-audit
created_at_utc: 2026-10-09T12:06:14Z
related_issue: 7
status: NEEDS_REVIEW
---

# Objective and acceptance criteria

Audit the 11 local Python scripts and `teos.ps1` (functions, tests, security) against `scripts/install.py`, and bring what is useful into the repository by a separate PR. Delete nothing locally.

# Initial state and scope

`main` at `63ad98c`. Local scripts read only, never executed. Scope: `scripts/teos_checks.py` (new), `scripts/install.py`, tests, README, `LOCAL-SYNC.md`, audit report.

# RAIDER evidence (or PENDING)

- Reuse-first: checks adapted from the local scripts, rules taken from the Agent Skills specification rather than invented.
- Agnostic: pure Python standard library, no OS-specific path.
- Idempotent / read-only: every new check returns problems without writing; `validate_project` test asserts the tree is unchanged.
- Durable: 18 new tests; the substring bug in `check` is covered by a regression test.
- Retroactive: `compare-local --strict` and `validate-project` work on installs and projects created before this change.

# Research (URLs, dates, applicability; or BLOCKED)

- https://agentskills.io/specification (checked 2026-10-09): name 1-64 lowercase alphanumerics and single hyphens, equal to the folder; description 1-1024 characters.

# Decisions and architecture impact

See `docs/audits/2026-10-09-local-scripts-audit.md`. Walkthrough keys are read from `docs/walkthrough/TEMPLATE.md` so the template stays the single source.

# Files changed

`scripts/teos_checks.py`, `scripts/install.py`, `scripts/test_teos_checks.py`, `scripts/test_install.py`, `README.md`, `docs/installation/LOCAL-SYNC.md`, `docs/audits/2026-10-09-local-scripts-audit.md`, this walkthrough.

# Implementation notes

`check` previously accepted `name: raider-governance` for a folder `raider` (substring test). It now parses the frontmatter and compares exactly.

# Tests

| Gate | Status | Command / Evidence |
|---|---|---|
| Static | PASSED | `python scripts/install.py check` → 44 skills, 19 agents |
| Unit | PASSED | `python -m unittest discover -s scripts -p "test_*.py"` → 31 tests OK |
| Integration | PASSED | `compare-local --strict` on the real machine → exit 0 (107 same, 0 missing/different/redundant/superseded); `validate-project` on a local project → PASSED, no file modified |
| API/Contract | N/A | |
| E2E | N/A | |
| Security | PASSED | Manual review in the audit report; no network, no secrets, no writes in new code |
| Accessibility/Performance | N/A | |

# Risks, limitations and remaining work

- Frontmatter parser handles top-level scalars only (all current files); a multi-line YAML description would be read as empty and reported.
- Not done: ship the `trigenys-engineering-os` adapter from the repository; review the local `STANDARDS-CATALOG.md` for `skills/standards-research/references/`.

# Handoff / next agent

Reviewer: confirm the "do not port" decisions in the audit before the local scripts are archived.

# Final status (COMPLETED / PARTIAL / BLOCKED / NEEDS REVIEW)

NEEDS REVIEW
