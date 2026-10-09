---
name: raider-governance
description: Enforce the verified Trigenys RAIDER Engineering Standard with explicit Reusable, Agnostic, Idempotent, Durable, Engineering-grade and Retroactive checks, including failure memory and change-scoped CI. Use for nontrivial engineering, architecture, automation and cross-repository changes.
---

# RAIDER governance

## Authoritative source and revision
- Local mirror: `docs/raider/RAIDER.md`.
- Upstream authoritative standard: https://github.com/EagleFox31/project-registry/blob/main/RAIDER.md
- Verified upstream Git blob SHA: `db1b349e129c8f147f91551ba79f6c1799481756` (verified 2026-10-09).
- Upstream updates must be explicitly compared before updating the mirror; never fabricate amendments or retroactively change already approved decisions.

## Required principles
1. **R — Reusable:** reusable cross-consumer behavior; configuration and adapters instead of copying logic.
2. **A — Agnostic:** do not hard-code repo, org, branch, stack, OS or provider when discoverable/configurable.
3. **I — Idempotent:** inspect → compute desired state → reconcile only drift; reapply converges to no-op.
4. **D — Durable / Non-regressive:** preserve supported contracts, coverage and consumer compatibility; capture **failure memory** and prevent recurrence.
5. **E — Engineering-grade:** secure, testable, maintainable, observable; **Impact-Aware CI** runs only affected gates (with safe shared dependency fan-out); before building research ecosystem and choose **Adopt / Adapt / Learn / Build**.
6. **R — Retroactive:** safe brownfield migration and adoption without destructive reset.

## Execution and review
Before significant changes, consult `docs/engineering/lessons-learned.md` if present; search maintained solutions and relevant standards. Define expected state, contracts, risk and scope; write testable acceptance criteria. Implement the smallest safe change. Validate repeat apply idempotency when applicable; test existing behavior, cross-surface changes and brownfield compatibility. Record significant failure/near miss, root cause and guardrail. Keep exceptions intentional, scoped and documented. For reusable capabilities validate one real consumer and a second different consumer when feasible.

## Evidence
Use the canonical `Definition of Done RAIDER` checklist in the local mirror. Write one dated agent-specific walkthrough for nontrivial work with changed paths, evidence, actual tests, unresolved risks, source URLs and handoff.

The documented source is not a formal external certification or a legal standard. Never claim an unperformed control passed.
