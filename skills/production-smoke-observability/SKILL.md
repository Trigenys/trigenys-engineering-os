---
name: production-smoke-observability
description: Verify runtime health and user flows post-deployment with read-only production diagnostics and release correlation. Use when auditing or changing this workflow class.
---

# production-smoke-observability

## Workflow
1. Establish deployment revision, target environment, approval and rollback owner. Determine expected API/UI/CX behavior.
2. Run safe smoke checks against deployment URL: health, key API contracts, login redirect/permissions, primary conversion funnel and known failures. Use test tenants/synthetic non-billable data where authorized.
3. Correlate traces/logs, status, release hash and errors. For production logs, use read-only least-privilege access with bounded filters and time windows; never dump PII, tokens or payment payloads.
4. Define SLI/SLO, alert thresholds, sampling, false-positive handling and incident escalation. Integrate frontend and backend observability without excessive sensitive logging.
5. Distinguish `CI pass`, `deployment success`, `smoke pass` and `production steady-state observed`. A green upstream workflow does not prove user success.
6. Preserve test URLs and timestamped reports. If production endpoint cannot be reached or permissions are missing, mark `NOT VERIFIED`.
## Output
Revision, environment, tested endpoints/journeys, evidence, SLO status, errors, escalation and rollback conditions.
## Public examples
- https://github.com/EagleFox31/atelier2026/blob/main/.github/workflows/prod-logs.yml
- https://github.com/Trigenys/release-video-engine/blob/main/.github/workflows/funnel-production-smoke.yml


## TEOS shared requirements
Follow canonical RAIDER when available; mark unknown formal controls PENDING. Record dated evidence and sources, write a unique docs/walkthrough for nontrivial work, coordinate Git branches/worktrees, avoid unnecessary tools and costs. Never claim execution or deployment without a run record. No production, destructive, privilege or paid changes without authorization.
