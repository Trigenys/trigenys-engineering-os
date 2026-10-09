---
name: impact-aware-ci-engineering
description: Build safe impact-aware CI mapping changed paths to affected components and validation gates. Use when auditing or changing this workflow class.
---

# impact-aware-ci-engineering

## Workflow
1. Inspect the dependency graph, changed-file resolution, target/base SHAs and existing `.github/appfactory-impact.json`.
2. Prefer shared AppFactory impact analysis over a new ad-hoc path filter when available. Model direct surfaces, transitive dependencies, shared contracts, schema changes, infrastructure and workflow edits.
3. Enumerate required gates by surface (frontend, backend, API contracts, security, E2E, visual, desktop, deployment packaging). Define fail-safe fallback for unknown paths and changes to the impact map itself.
4. Ensure required branch checks report a **decisive result** rather than remaining perpetually pending because the whole workflow was skipped by path filters. A skipped job is not evidence of a passed test; keep a guard/aggregator gate.
5. Test synthetic diffs: empty, unrelated docs, rename, shared library, test infra, secrets policy, API schema, database migration, multi-surface and unclassified files.
6. Schedule occasional broader/full-suite runs to detect missed dependencies. Compare duration and incident rate before claiming cost savings.
## Evidence
Impact graph, fixture cases, gate matrix, fail-open/closed assessment, scheduled safety net and links to actual CI runs.
## Sources
- https://github.com/EagleFox31/appfactory-project-automation/blob/main/.github/workflows/reusable-impact-analysis.yml
- https://github.com/Trigenys/sims-mod-health/blob/main/.github/workflows/impact-aware-ci.yml
- https://github.com/EagleFox31/atelier2026/blob/main/.github/workflows/ux-guardrails.yml


## TEOS shared requirements
Follow canonical RAIDER when available; mark unknown formal controls PENDING. Record dated evidence and sources, write a unique docs/walkthrough for nontrivial work, coordinate Git branches/worktrees, avoid unnecessary tools and costs. Never claim execution or deployment without a run record. No production, destructive, privilege or paid changes without authorization.
