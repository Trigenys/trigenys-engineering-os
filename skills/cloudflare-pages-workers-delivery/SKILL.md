---
name: cloudflare-pages-workers-delivery
description: Manage Cloudflare Pages/Workers production and staging from Git-connected builds without duplicating infrastructure. Use when auditing or changing this workflow class.
---

# cloudflare-pages-workers-delivery

## Workflow
1. Inventory existing Pages projects, Workers, D1, R2, Hyperdrive bindings and Git links with read-only queries. Determine source repo, production branch, preview behavior and existing ownership markers.
2. Prefer AppFactory brownfield provisioning or Cloudflare native Git build integration already in use; avoid a second concurrent deployment pipeline.
3. Define environment-sensitive config, secrets boundaries, binding names, route routing, migration plan, deployment annotations, Pages/Workers preview isolation and account quotas.
4. Validate build output directory and entrypoint; run quality gates before release and safe post-deploy smoke (HTTP checks alone are insufficient for feature readiness).
5. Never print secret values, replicate Cloudflare account tokens into consumer repositories or create resources without permission. Do not assume a Pages project exists merely because YAML references it.
6. Preserve source ownership markers, compare staging/prod and ensure rollback/reconciliation is idempotent.
## Output
Deployment topology, Git/Cloudflare ownership map, permission matrix, preview and production check plan, rollback.
## Sources
- https://github.com/Trigenys/appfactory/blob/main/README.md
- https://github.com/Trigenys/release-video-engine/blob/main/.github/workflows/funnel-production-smoke.yml
- https://developers.cloudflare.com/workers/ci-cd/builds/


## TEOS shared requirements
Follow canonical RAIDER when available; mark unknown formal controls PENDING. Record dated evidence and sources, write a unique docs/walkthrough for nontrivial work, coordinate Git branches/worktrees, avoid unnecessary tools and costs. Never claim execution or deployment without a run record. No production, destructive, privilege or paid changes without authorization.
