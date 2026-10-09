# Cross-project CI/CD and operations Skill map

**Revision:** 2026-10-09 · **Audience:** Cursor, Claude Code, Codex and AppFactory · **Status:** reference playbook (not self-executing)

TEOS retains the 26 foundational Skills and adds 16 focused Skills based on inspected GitHub Actions workflows, publicly documented production patterns and failure modes.

| Workflow task | Focused Skill | Public precedent |
|---|---|---|
| Secure event, token, concurrency and action versions | [github-actions-secure-workflows](../../skills/github-actions-secure-workflows/SKILL.md) | [Atelier UX guardrails](https://github.com/EagleFox31/atelier2026/blob/main/.github/workflows/ux-guardrails.yml) |
| Shared workflow_call interfaces, appfactory versioning | [reusable-workflow-platform](../../skills/reusable-workflow-platform/SKILL.md) | [AppFactory automation](https://github.com/EagleFox31/appfactory-project-automation) |
| Impact graph and fail-safe targeted PR CI | [impact-aware-ci-engineering](../../skills/impact-aware-ci-engineering/SKILL.md) | [Sims Mod Health](https://github.com/Trigenys/sims-mod-health/blob/main/.github/workflows/impact-aware-ci.yml) |
| GitHub OIDC, IAM and credential minimization | [oidc-secretless-cloud-auth](../../skills/oidc-secretless-cloud-auth/SKILL.md) | [AppFactory auth](https://github.com/Trigenys/appfactory/blob/main/docs/mutation-authentication.md) |
| Release gates, promotion, deploy and rollback | [release-promotion-rollback](../../skills/release-promotion-rollback/SKILL.md) | [Atelier AWS deployment](https://github.com/EagleFox31/atelier2026/blob/main/.github/workflows/deploy.yml) |
| Windows build, installer tests, MSI/ZIP | [windows-desktop-packaging](../../skills/windows-desktop-packaging/SKILL.md) | [Tauri release](https://github.com/EagleFox31/appfactory-project-automation/blob/main/.github/workflows/release-tauri-desktop.yml) |
| Visual diffs, screenshots, Playwright | [visual-regression-ux-evidence](../../skills/visual-regression-ux-evidence/SKILL.md) | [Visual evidence](https://github.com/Trigenys/sims-mod-health/blob/main/.github/workflows/visual-evidence.yml) |
| Neon/R2/offsite backup and restore drill | [backup-restore-drills](../../skills/backup-restore-drills/SKILL.md) | [RoadmapMentor backup](https://github.com/EagleFox31/RoadmapMentor/blob/main/.github/workflows/neon-r2-backup.yml) |
| Failed Actions, incident root cause, safe reruns | [workflow-incident-triage](../../skills/workflow-incident-triage/SKILL.md) | [AppFactory Action runs](https://github.com/EagleFox31/appfactory-project-automation/actions) |
| SBOM, hashes, signature and attestations | [artifact-provenance-sbom](../../skills/artifact-provenance-sbom/SKILL.md) | [AppFactory Tauri release](https://github.com/EagleFox31/appfactory-project-automation/blob/main/.github/workflows/release-tauri-desktop.yml) |
| Schedules, ingestion, freshness, alerting | [scheduled-automation-reliability](../../skills/scheduled-automation-reliability/SKILL.md) | [Project registry refresh](https://github.com/EagleFox31/project-registry/blob/main/.github/workflows/refresh.yml) |
| Post-deploy smoke, logs, SLO and evidence | [production-smoke-observability](../../skills/production-smoke-observability/SKILL.md) | [Release video smoke](https://github.com/Trigenys/release-video-engine/blob/main/.github/workflows/funnel-production-smoke.yml) |
| Cloudflare Pages and Workers Builds | [cloudflare-pages-workers-delivery](../../skills/cloudflare-pages-workers-delivery/SKILL.md) | [AppFactory delivery overview](https://github.com/Trigenys/appfactory) |
| AWS OIDC, ECR/GHCR, CloudFormation, SSM | [aws-cloudformation-delivery](../../skills/aws-cloudformation-delivery/SKILL.md) | [Atelier AWS](https://github.com/EagleFox31/atelier2026/blob/main/.github/workflows/deploy.yml) |
| Repeatable benchmarks and cost per output | [performance-benchmark-unit-economics](../../skills/performance-benchmark-unit-economics/SKILL.md) | [Renderer parity](https://github.com/Trigenys/release-video-engine/blob/main/.github/workflows/media-heavy-renderer-benchmark.yml) |
| Migration integrity and compatibility gates | [database-migration-data-integrity](../../skills/database-migration-data-integrity/SKILL.md) | [RoadmapMentor backup](https://github.com/EagleFox31/RoadmapMentor/blob/main/.github/workflows/neon-r2-backup.yml) |

## Integration and ownership

Before implementing any new YAML, inspect `EagleFox31/appfactory-project-automation` and `Trigenys/appfactory` for an existing versioned reusable workflow, provisioning pattern or governance contract. Use TEOS Skills as *instructions*, not a second competing workflow execution framework.

The matching base Skills remain authoritative for quality tests, DevSecOps, PMO, product, UX and architecture. A focused Skill supplements—not replaces—the general discipline.

## Specialized agents

- `github-actions-platform-architect`: reusable workflows, trust and CI design (review-oriented).
- `ci-failure-investigator`: failed-run triage and reproducible diagnosis (read-only).
- `release-provenance-verifier`: publication/integrity/post-deployment evidence checks (read-only).

Agent model IDs are configuration hints, not a guarantee of account eligibility, actual runtime model or included plan spend. Validate client discovery and execution separately.
