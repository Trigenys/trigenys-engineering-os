---
name: github-actions-secure-workflows
description: Review and harden GitHub Actions event triggers, permission boundaries, third-party actions and workflow correctness. Use when auditing or changing this workflow class.
---

# github-actions-secure-workflows

## Trigger and trust matrix
1. Determine whether the workflow is PR validation, trusted main CI, release, maintenance, or production deployment. Declare event triggers explicitly and least-privilege `permissions` per job.
2. For untrusted fork PRs, use `pull_request` for code execution with read-only credentials. Avoid combining `pull_request_target` and execution of attacker-controlled checkout/build/scripts. When a privileged `pull_request_target` metadata workflow is unavoidable, checkout trusted base only and never execute PR artifacts or interpolated untrusted event input.
3. Restrict `workflow_run` privileged jobs to trusted triggering workflows and SHA; validate provenance before accepting upstream artifacts.
4. Review shell injection hazards in expressions interpolated into `run:`. Pass untrusted values via environment variables with validation, not inline executable script.
5. Set `concurrency` and `cancel-in-progress` appropriately: cancel stale PR checks, never cancel a production deployment in progress without explicit rollback design.
6. Pin high-risk third-party actions and reusable workflows to reviewed immutable SHAs wherever feasible; manage pinned dependency updates. Restrict the runner scope and cache poisoning exposure.
7. Validate GitHub Actions YAML triggers with GitHub-aware tooling (generic YAML libraries may interpret `on` as boolean). Run `actionlint` if available.
## Gates
Document threat boundary, token/secret permissions, trigger matrix, provenance of checked-out code, protected environments, pre-merge test and rollback. Never treat a green skipped job as proof an acceptance criterion ran.
## Source examples
- Public project: https://github.com/EagleFox31/atelier2026/blob/main/.github/workflows/ux-guardrails.yml
- Official: https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target
- Official: https://docs.github.com/en/actions/reference/security/secure-use


## TEOS shared requirements
Follow canonical RAIDER when available; mark unknown formal controls PENDING. Record dated evidence and sources, write a unique docs/walkthrough for nontrivial work, coordinate Git branches/worktrees, avoid unnecessary tools and costs. Never claim execution or deployment without a run record. No production, destructive, privilege or paid changes without authorization.
