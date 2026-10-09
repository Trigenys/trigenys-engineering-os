---
name: release-promotion-rollback
description: Establish release gates, artifact promotion, deployment concurrency and safe rollback with auditable provenance. Use when auditing or changing this workflow class.
---

# release-promotion-rollback

## Workflow
1. Separate merge-time checks from release-time deployment. Identify the exact release-trigger condition (tag, release PR, manual approval), protected environment and authorized approvers.
2. Trace source commit SHA → CI results → built image/artifact digest → release version → deployed revision. Never silently rebuild an unreviewed ref and claim equivalence.
3. Validate artifact compatibility, DB migrations, breaking contracts, immutable manifests and pre-deployment backup/rollback readiness.
4. For long-running deployments, isolate production `concurrency` and avoid overlapping rollouts. Build an explicit release gate to avoid accidental deployment after ordinary CI merges.
5. Run post-deploy health/API/user-journey smoke checks; promote only if criteria pass. On failure, follow actual rollback procedure, noting irreversible schema changes.
6. Distinguish `CI PASSED`, `RELEASE BUILT`, `DEPLOYED`, `SMOKE PASSED` and `ROLLED BACK`.
## Output
Release plan, approval record, version/digest mapping, smoke evidence, rollback drill, notes and release walkthrough.
## Sources
- https://github.com/EagleFox31/atelier2026/blob/main/.github/workflows/deploy.yml
- https://github.com/EagleFox31/appfactory-project-automation/blob/main/.github/workflows/reusable-release.yml


## TEOS shared requirements
Follow canonical RAIDER when available; mark unknown formal controls PENDING. Record dated evidence and sources, write a unique docs/walkthrough for nontrivial work, coordinate Git branches/worktrees, avoid unnecessary tools and costs. Never claim execution or deployment without a run record. No production, destructive, privilege or paid changes without authorization.
