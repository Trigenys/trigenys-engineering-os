---
task_id: TEOS-ADAPTER-20261009
agent: implementation
provider: chatgpt
model_reported: not_verified
owner: TEOS repository
branch: fix/teos-adapter-discovery-20261009
created_at_utc: 2026-10-09T13:30:00Z
related_issue: 9
status: NEEDS_REVIEW
---

# Objective and acceptance criteria
Remove the obsolete hard-coded TEOS adapter Skill references to a now-empty local Skill root without changing the 44 specialist Skills or existing user profiles.

# Initial state and scope
User-supplied Cursor report: 44 Skills discoverable, 19 agent files present but discovery NOT VERIFIED; 31 existing tests pass, adapter in two roots still points to obsolete local paths. The reported smoke test is not reproduced in GitHub CI.

# RAIDER evidence (or PENDING)
Reusable: single versioned index Skill copied by tool selection. Agnostic: directory-relative sibling Skill resolution. Idempotent: repeated runs are no-ops. Durable: opt-in upgrade, backup, no deletion of existing personal Skills. Engineering-grade: dedicated unit tests, CLI validation and CI inclusion. Retroactive: read-only compare + safe brownfield replacement.

# Research (URLs, dates, applicability; or BLOCKED)
- https://agentskills.io/specification — name and description constraints (2026-10-09)
- https://github.com/Trigenys/trigenys-engineering-os/issues/7 — Windows Cursor 3.21.16 smoke test reports and migration notes (2026-10-09)

# Decisions and architecture impact
Keep the adapter OUTSIDE canonical `skills/` to preserve 44 specialist count. Provide `install-adapter` and `compare-adapter` CLI commands rather than silently modifying adapters during `install-global`. The current on-device original adapter content is not present in the repository.

# Files changed
- `adapters/trigenys-engineering-os/SKILL.md`
- `scripts/install.py`, `scripts/test_adapter.py`
- `README.md`, `docs/installation/LOCAL-SYNC.md`
- `.github/workflows/skills-ci.yml`
- this walkthrough

# Implementation notes
The adapter resolves neighboring `../<skill-name>/SKILL.md`, or uses the current tool's native Skill discovery. It never assumes an OS- or machine-specific home path. A missing Skill yields a declared error, not fabricated content.

# Tests
| Gate | Status | Command / Evidence |
|---|---|---|
| Static | NOT RUN | GitHub CI pending |
| Unit | NOT RUN | GitHub CI pending |
| Integration | NOT RUN | Real user-device install requires permission |
| API/Contract | N/A | No API |
| E2E | NOT RUN | Cursor reload and native discovery still required |
| Security | NOT RUN | PR review pending |
| Accessibility/Performance | N/A | Not an end-user visual surface |

# Risks, limitations and remaining work
Local original adapter cannot be diffed because it is not in GitHub. Cursor custom agent discovery and model honor are NOT VERIFIED. A standalone Cloud Agents sync design remains a future decision; do not create a redundant `.cursor/skills` copy on existing multi-tool installation.

# Handoff / next agent
Review the PR, CI and all local adapter backups; verify CLI dry-run; obtain explicit user authorization before replacing local adapters.

# Final status (COMPLETED / PARTIAL / BLOCKED / NEEDS REVIEW)
NEEDS REVIEW
