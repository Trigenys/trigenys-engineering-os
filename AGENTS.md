# Trigenys Engineering OS — agent contract

This repository follows Trigenys RAIDER engineering principles: reusable, configuration-driven, provider-agnostic where practical, idempotent reconciliation, non-regression, least privilege, testability and adoptability. **Do not invent the canonical RAIDER expansion.** Refer to `docs/raider/RAIDER.md`.

## Workflow
1. Read the task and affected code, issues and documentation before making changes.
2. For product/architecture/security/UX decisions, research relevant official standards and live competitors; cite links and access dates. If offline, mark `RESEARCH_BLOCKED`.
3. Read `docs/agent-coordination/protocol.md`. Assign one task owner, independent branches/worktrees and disjoint file scopes; otherwise serialize.
4. Make minimal, reversible changes. Do not overwrite another agent's unmerged edits.
5. Validate the affected tests in risk order; never claim unexecuted tests passed.
6. Write one dated `docs/walkthrough/<task-id>/<timestamp>__<agent>.md` for each nontrivial agent intervention.
7. Keep a written handoff with remaining risks and evidence.

## Constraints
- No production deployments, paid resources, secret modifications, destructive migrations or force pushes without approval.
- No fake citations, model claims, certifications or test results.
- Keep transport/persistence/provider adapters behind explicit boundaries.
- Treat `docs/engineering/lessons-learned.md` as a risk reference when present.
- See `docs/quality/QUALITY-GATES.md` for test gates.
- For GitHub Actions, OIDC, deployment, backup or packaging work load matching Skills from `docs/skills/CI-SKILLS-MAP.md`; do not duplicate existing AppFactory reusable workflows.
- CI green, artifact published, deployed and production-smoke passed are separate claims requiring separate evidence.
- Cursor routing is advisory; subagent model IDs must be checked locally.
