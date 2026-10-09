---
name: workflow-incident-triage
description: Diagnose failing GitHub Actions checks with evidence, distinguish regressions from authentication and runner failures. Use when auditing or changing this workflow class.
---

# workflow-incident-triage

## Workflow
1. Read the latest relevant run details and failed job **logs**, associated commit and event type; never infer a root cause from a red status alone.
2. Categorize: YAML/trigger, permission, OIDC, missing credentials, dependency installation, cache drift, flaky tests, resource exhaustion, migration, deploy, network, timeouts or unknown.
3. Reproduce in a safe local/container test or isolated workflow. Correlate with recently merged code and workflow changes. Do not make speculative fixes across unrelated components.
4. Identify actual cause and minimal correction. Avoid blanket retries; rerun only failed jobs when an intermittent runner/network issue is supported by evidence.
5. Add a regression test or deterministic guard for recurring failures, and a concise `docs/walkthrough` root cause/handoff note.
6. Escalate paid/deploy retries and privileged credential changes for approval. For scheduled jobs, verify that failure alerting exists and reaches a responsible owner.
## Output
Run URL, failed job/step, first meaningful error, cause confidence, corrective patch, reproduced result, prevented recurrence.
## Public examples
- https://github.com/EagleFox31/appfactory-project-automation/actions
- https://github.com/EagleFox31/atelier2026/actions


## TEOS shared requirements
Follow canonical RAIDER when available; mark unknown formal controls PENDING. Record dated evidence and sources, write a unique docs/walkthrough for nontrivial work, coordinate Git branches/worktrees, avoid unnecessary tools and costs. Never claim execution or deployment without a run record. No production, destructive, privilege or paid changes without authorization.
