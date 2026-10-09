---
name: database-migration-data-integrity
description: Plan and validate backward-compatible database migrations with rollback, CI integration and recovery evidence. Use when auditing or changing this workflow class.
---

# database-migration-data-integrity

## Workflow
1. Inventory schema, traffic/writes, application version coupling and dependent consumers. Validate risk of locks, long transactions, irreversibility and data loss.
2. Prefer expand/migrate/contract with forward/backward compatibility and phased feature flags; do not combine destructive migration with unsafe production rollout.
3. Use representative isolated test data and migration dry-runs, verify default/null constraints, indexes, data volume, timeouts and unique/foreign-key behavior.
4. Verify API/contract and authorization scenarios impacted by schema changes. Use disposable branches/databases for CI; prohibit real production secrets and writes in PR test workflows.
5. Plan point-in-time recovery/backup, permissions, monitoring and human approval. A rollback of application code may not reverse a data migration.
6. Record migration IDs, timing and actual test results; mark untested rollback as `NOT VERIFIED`.
## Output
Migration plan, risk matrix, fixture tests, data integrity checks, rollback/restore plan, staging validation.
## Sources
- https://github.com/EagleFox31/RoadmapMentor/blob/main/.github/workflows/neon-r2-backup.yml
- https://www.postgresql.org/docs/current/ddl.html


## TEOS shared requirements
Follow canonical RAIDER when available; mark unknown formal controls PENDING. Record dated evidence and sources, write a unique docs/walkthrough for nontrivial work, coordinate Git branches/worktrees, avoid unnecessary tools and costs. Never claim execution or deployment without a run record. No production, destructive, privilege or paid changes without authorization.
