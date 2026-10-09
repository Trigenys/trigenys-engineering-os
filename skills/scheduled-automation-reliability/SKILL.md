---
name: scheduled-automation-reliability
description: Engineer reliable GitHub scheduled jobs for feeds, registries and recurring checks with alerts and anti-duplication. Use when auditing or changing this workflow class.
---

# scheduled-automation-reliability

## Workflow
1. Identify schedule cadence, UTC/timezone semantics, worst-case duration, clock drift, concurrency and idempotency key.
2. Separate `workflow_dispatch` maintenance from scheduled production execution; use environment variables or opt-in flags to control potentially billable jobs.
3. Validate data freshness, duplicates, incremental reconciliation, API rate limits, pagination, retries with exponential backoff and upstream changes.
4. Write structured success/failure metrics, alert responsibly after meaningful failures, avoid spam and secret leakage. Include timeout and artifact retention policy.
5. Test the job with fixtures for empty, stale, partial, duplicated, schema drift and throttled upstream responses. Keep human approval for destructive cleanup.
6. After a run, check last updated data in the destination, not merely a green Action check.
## Output
Scheduler specification, monitoring, data-freshness SLO, fixture tests and recovery runbook.
## Public examples
- https://github.com/EagleFox31/project-registry/blob/main/.github/workflows/refresh.yml
- https://github.com/EagleFox31/xeption237/blob/main/.github/workflows/render-market-sources.yml


## TEOS shared requirements
Follow canonical RAIDER when available; mark unknown formal controls PENDING. Record dated evidence and sources, write a unique docs/walkthrough for nontrivial work, coordinate Git branches/worktrees, avoid unnecessary tools and costs. Never claim execution or deployment without a run record. No production, destructive, privilege or paid changes without authorization.
