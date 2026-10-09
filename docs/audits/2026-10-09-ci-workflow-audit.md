# Cross-repository GitHub Actions and deployed-infrastructure patterns

**Audit date:** 2026-10-09 (UTC) · **Scope:** repositories visible to the linked GitHub installation for Trigenys and EagleFox31, plus read-only linked Cloudflare inventory. **Publication rule:** only examples and evidence from **public repositories** are documented here; findings involving private repositories are intentionally excluded from this public file.

## Audit method and confidence

- Enumerated GitHub repository metadata and `.github/workflows/` contents where accessible.
- Read a targeted sample of release, deployment, CI, data-backup, quality, performance and governance workflow YAML.
- Checked selected recent GitHub Actions run metadata (name, status, event, conclusion, timestamp). A completed successful job **does not** by itself prove a service is operational.
- Inspected current account-bound Cloudflare Worker and Pages *resource existence*, but not all live user journeys; account-specific resource mapping is not published here.
- Did **not** run production functional tests, inspect every job log, assert backup recoverability, or review every commit and dependency in every repository.

## Patterns verified in publicly accessible workflow files

| Repository | Verified workflow technique | Evidence |
|---|---|---|
| [AppFactory Project Automation](https://github.com/EagleFox31/appfactory-project-automation) | Shared `workflow_call` building blocks, Impact-Aware CI, governance and desktop release automation | [Impact engine](https://github.com/EagleFox31/appfactory-project-automation/blob/main/.github/workflows/reusable-impact-analysis.yml), [Tauri release](https://github.com/EagleFox31/appfactory-project-automation/blob/main/.github/workflows/release-tauri-desktop.yml) |
| [Trigenys AppFactory](https://github.com/Trigenys/appfactory) | OIDC-protected repository provisioning, reusable blueprints; identity/auth policy | [Mutation authentication](https://github.com/Trigenys/appfactory/blob/main/docs/mutation-authentication.md) |
| [Atelier Maître](https://github.com/EagleFox31/atelier2026) | Explicit AWS release gate, GitHub OIDC, CloudFormation, UX Playwright impact gating, limited production log retrieval via SSM | [Deploy](https://github.com/EagleFox31/atelier2026/blob/main/.github/workflows/deploy.yml), [UX guardrails](https://github.com/EagleFox31/atelier2026/blob/main/.github/workflows/ux-guardrails.yml), [Prod logs](https://github.com/EagleFox31/atelier2026/blob/main/.github/workflows/prod-logs.yml) |
| [Sims Mod Health](https://github.com/Trigenys/sims-mod-health) | Selective per-surface CI, Rust/Windows benchmarks, visual regression evidence, security gates | [Impact CI](https://github.com/Trigenys/sims-mod-health/blob/main/.github/workflows/impact-aware-ci.yml), [Benchmarks](https://github.com/Trigenys/sims-mod-health/blob/main/.github/workflows/scanner-benchmark.yml) |
| [RoadmapMentor](https://github.com/EagleFox31/RoadmapMentor) | Opt-in Neon/R2 encrypted snapshot with bounded scheduled execution and failure alert | [Backup workflow](https://github.com/EagleFox31/RoadmapMentor/blob/main/.github/workflows/neon-r2-backup.yml) |
| [AgenStart](https://github.com/EagleFox31/AgenStart) | Windows/.NET installation, catalogue and packaging-focused tests; scheduled governance | [Install tests](https://github.com/EagleFox31/AgenStart/blob/main/.github/workflows/installation-tests.yml) |
| [Release Video Engine](https://github.com/Trigenys/release-video-engine) | Deterministic media benchmark, unit economics, production funnel smoke | [Benchmark](https://github.com/Trigenys/release-video-engine/blob/main/.github/workflows/media-heavy-renderer-benchmark.yml), [Economics](https://github.com/Trigenys/release-video-engine/blob/main/.github/workflows/unit-economics.yml), [Smoke](https://github.com/Trigenys/release-video-engine/blob/main/.github/workflows/funnel-production-smoke.yml) |
| [AgenFetch desktop](https://github.com/EagleFox31/agenfetch-desktop) | Windows installer and separately tested Python packaging with checksums | [Release workflow](https://github.com/EagleFox31/agenfetch-desktop/blob/main/.github/workflows/release.yml) |
| [Product Identity](https://github.com/Trigenys/product-identity) | AWS OIDC, ARM64 image delivery and CloudFormation from GitHub Actions | [AWS workflow](https://github.com/Trigenys/product-identity/blob/main/.github/workflows/aws-deploy.yml) |
| [Trigenys Insight](https://github.com/EagleFox31/Trigenys-Insight) | pnpm reproducible installation, lint/typecheck/unit gates | [Quality workflow](https://github.com/EagleFox31/Trigenys-Insight/blob/main/.github/workflows/quality.yml) |
| [Xeption237](https://github.com/EagleFox31/xeption237) | Scheduled external market-source refresh | [Market-source workflow](https://github.com/EagleFox31/xeption237/blob/main/.github/workflows/render-market-sources.yml) |
| [Project Registry](https://github.com/EagleFox31/project-registry) | Scheduled + on-change registry build, private audit artifact, optional Cloudflare Pages publish and verification | [Refresh](https://github.com/EagleFox31/project-registry/blob/main/.github/workflows/refresh.yml) |

## Representative run checks (snapshot 2026-10-09)

- Atelier Maître: [Deploy AWS successful on 2026-10-09](https://github.com/EagleFox31/atelier2026/actions/runs/37917339592). This is a GitHub workflow conclusion, not an application-level smoke proof.
- Sims Mod Health: [Impact-aware PR CI successful on 2026-10-05](https://github.com/Trigenys/sims-mod-health/actions/runs/37301388699).
- RoadmapMentor: [CI successful on 2026-10-09](https://github.com/EagleFox31/RoadmapMentor/actions/runs/37912811140). Restore drill **not verified**.
- Trigenys Insight: [Quality successful on 2026-10-09](https://github.com/EagleFox31/Trigenys-Insight/actions/runs/37910247105).
- AppFactory Project Automation: [CI successful on 2026-10-04](https://github.com/EagleFox31/appfactory-project-automation/actions/runs/37206364281).
- Product Identity: [AppFactory Infrastructure workflow failed on 2026-10-08](https://github.com/Trigenys/product-identity/actions/runs/37850145196). Requires log-level investigation before describing a cause.
- Xeption237: [Scheduled market-source refresh failed on 2026-10-05](https://github.com/EagleFox31/xeption237/actions/runs/37301493460). Root cause **not determined**.
- TEOS itself: [Project Automation failed on 2026-10-09](https://github.com/Trigenys/trigenys-engineering-os/actions/runs/37919208230); [same date CI success](https://github.com/Trigenys/trigenys-engineering-os/actions/runs/37919136785). Check the failure mechanism; it is not automatically attributable to the new Skill definitions.

## Engineering risks and improvements

**P0 — Separate status labels.** Track `VALIDATED`, `PACKAGE_PUBLISHED`, `DEPLOYED`, `PRODUCTION_SMOKE_PASSED`, `BACKUP_VERIFIED` and `RESTORE_VERIFIED` as different evidence classes.

**P0 — Workflow trust.** Review privileged `pull_request_target` and `workflow_run` boundaries. Do not checkout or execute untrusted PR code in a trusted/secret-bearing context. Audit action pins, IAM role trust and `GITHUB_TOKEN` permissions. Official: https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target

**P1 — Incident triage.** Inspect failing run **job logs** before proposing fixes; address production-infrastructure and scheduled-data runs according to business priority.

**P1 — Consistency.** Prefer AppFactory shared reusable Action/Workflow contracts and impact analysis rather than copy-pasting YAML. Preserve consumer-specific path/dependency graphs, quality gates and stable release SHA.

**P1 — Restore evidence.** An opt-in scheduled snapshot definition is not recovery assurance until an isolated restore is periodically exercised.

**P1 — Release integrity.** Prefer versioned artifacts, reproducible builds, SHA-256 and supply-chain provenance; verify whether signatures are real or merely optional.

**P2 — Maintainability.** Reduce duplicated CI logic, verify current action versions and add regression fixtures for impact analysis and workflow-input validation.

## TEOS improvements proposed

Added 16 task-specific Skills and 3 dedicated review-oriented Cursor agents; see [CI Skill map](../skills/CI-SKILLS-MAP.md). These instructions do **not** change workflows or infrastructure in any inspected product repository. Use PRs and documented test gates to adopt recommended improvements selectively.

Formal RAIDER stage naming is still PENDING authoritative source. See [RAIDER contract](../raider/RAIDER.md).
