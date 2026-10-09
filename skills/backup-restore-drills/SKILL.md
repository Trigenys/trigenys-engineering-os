---
name: backup-restore-drills
description: Design encrypted offsite database snapshots and demonstrate recoverability with periodic restore exercises. Use when auditing or changing this workflow class.
---

# backup-restore-drills

## Workflow
1. Inventory stateful assets (Neon/Postgres, R2/object store, D1, user uploads, queues and secrets references); classify RPO/RTO and data sensitivity.
2. Confirm backup prerequisites and ownership, destination independent from primary service, encryption and retention. Avoid real data in logs and public CI artifacts.
3. Implement opt-in scheduled backups with dedicated scoped credentials; ensure concurrency safety, checksums, manifests and immutable retention where needed.
4. Verify backup completion and data shape, then **periodically perform a restore into an isolated non-production environment** with sanitized test data to validate actual recovery.
5. Test failure notifications, missing credentials, partial snapshots, corrupt archives and restore permissions. Document billing/storage impacts and required approvals.
6. Distinguish `configured`, `scheduled`, `last successful backup` and `restore proven`—the first three do not imply the fourth.
## Output
Backup runbook, retention policy, RPO/RTO, test restore evidence, alerting and cost estimate.
## Sources
- https://github.com/EagleFox31/RoadmapMentor/blob/main/.github/workflows/neon-r2-backup.yml


## TEOS shared requirements
Follow canonical RAIDER when available; mark unknown formal controls PENDING. Record dated evidence and sources, write a unique docs/walkthrough for nontrivial work, coordinate Git branches/worktrees, avoid unnecessary tools and costs. Never claim execution or deployment without a run record. No production, destructive, privilege or paid changes without authorization.
