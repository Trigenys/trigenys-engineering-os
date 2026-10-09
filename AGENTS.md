# Trigenys Engineering OS — agent contract

This repository follows Trigenys RAIDER engineering principles: reusable, configuration-driven, provider-agnostic where practical, idempotent reconciliation, non-regression, least privilege, testability and adoptability. RAIDER means **Reusable, Agnostic, Idempotent, Durable / Non-regressive, Engineering-grade, Retroactive**. Apply the full [upstream canonical RAIDER document](docs/raider/RAIDER.md), including failure memory, reuse-first, scoped execution and brownfield adoption.

## Workflow
1. Read the task, past relevant failure memory, affected code, issues and documentation. For significant capabilities first assess **Adopt / Adapt / Learn / Build**.
2. For product/architecture/security/UX decisions, research relevant official standards and live competitors; cite links and access dates. If offline, mark `RESEARCH_BLOCKED`.
3. Read `docs/agent-coordination/protocol.md`. Assign one task owner, independent branches/worktrees and disjoint file scopes; otherwise serialize.
4. Make minimal, reversible changes. Do not overwrite another agent's unmerged edits.
5. Validate the affected tests in risk order and satisfy the applicable RAIDER Definition of Done: reuse, agnosticism, idempotence, durability, engineering quality, scoped CI and retroactive adoption; never claim unexecuted tests passed.
6. Write one dated `docs/walkthrough/<task-id>/<timestamp>__<agent>.md` for each nontrivial agent intervention.
7. Keep a written handoff with remaining risks and evidence.

## Constraints
- No production deployments, paid resources, secret modifications, destructive migrations or force pushes without approval.
- No fake citations, model claims, certifications or test results.
- Keep transport/persistence/provider adapters behind explicit boundaries.
- Consult and maintain `docs/engineering/lessons-learned.md` (or an explicitly discoverable equivalent) for significant failures/near misses and preventive controls.
- See `docs/quality/QUALITY-GATES.md` for test gates.
- For GitHub Actions, OIDC, deployment, backup or packaging work load matching Skills from `docs/skills/CI-SKILLS-MAP.md`; do not duplicate existing AppFactory reusable workflows.
- CI green, artifact published, deployed and production-smoke passed are separate claims requiring separate evidence.
- Cursor routing is advisory; subagent model IDs must be checked locally.
