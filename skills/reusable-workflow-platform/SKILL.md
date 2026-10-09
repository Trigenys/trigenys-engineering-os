---
name: reusable-workflow-platform
description: Design centrally versioned reusable GitHub Actions workflows with safe consumer inputs and compatibility gates. Use when auditing or changing this workflow class.
---

# reusable-workflow-platform

## Workflow
1. Before adding YAML, inventory existing reusable workflows and AppFactory features. Prefer `EagleFox31/appfactory-project-automation` shared workflows for Project Automation, governance, impact analysis and releases when contracts fit.
2. Specify `on: workflow_call` inputs, types, defaults, output contract and explicitly required secrets. Keep consumer policy/config in the calling repo. Prefer named scoped secrets; do not propagate all secrets through chains by default.
3. Resolve nested reusable workflow dependencies and ensure ref pinning works for callers; validate each boundary separately.
4. Version breaking input/output changes; migrate consumers via PRs. Adopt immutable SHA pinning in sensitive deployment paths, and document source commit to consumer mapping.
5. Create contract tests with a representative consumer fixture, failure/invalid-input cases, and least-privilege permissions. Distinguish metadata automation from code build/deploy.
6. Avoid duplicating reusable logic under each application or editing vendor-managed workflows in-place.
## Output
Contract, example caller, lifecycle matrix, upgrade instructions, rollback strategy and observed workflow run evidence.
## Sources
- https://github.com/EagleFox31/appfactory-project-automation
- https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows


## TEOS shared requirements
Follow canonical RAIDER when available; mark unknown formal controls PENDING. Record dated evidence and sources, write a unique docs/walkthrough for nontrivial work, coordinate Git branches/worktrees, avoid unnecessary tools and costs. Never claim execution or deployment without a run record. No production, destructive, privilege or paid changes without authorization.
