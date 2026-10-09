---
name: aws-cloudformation-delivery
description: Apply robust AWS GitHub OIDC CloudFormation Docker image and SSM delivery practices. Use when auditing or changing this workflow class.
---

# aws-cloudformation-delivery

## Workflow
1. Inspect existing AWS role/OIDC, region, stacks, CloudFormation templates, image registry, SSM settings, budget alarms and observed runtime. Prefer existing infrastructure and reuse exact release components.
2. Run `validate-template`, static/IaC policy checks, and CloudFormation change set/plan. Surface drift, potential resource replacement and rollback implications before apply.
3. Obtain short-lived OIDC credentials via restricted trust conditions; keep scoped `permissions: id-token: write` on trusted workflow only.
4. Build and push container images with reproducible lockfiles; tag by release and immutable SHA/digest. Never substitute `latest` when promoting approved code.
5. Deploy on an explicit release gate with concurrency and human approval for risky infrastructure changes. Use SSM for production diagnostics instead of exposing SSH where suitable.
6. Confirm stack completion, service health, application smoke, rollback compatibility and CloudWatch signals. Document costs and free-tier lifecycle.
## Output
Stack plan, IAM role trust, artifacts/digests, controlled deploy record, health proof and rollback.
## Public example
- https://github.com/EagleFox31/atelier2026/blob/main/.github/workflows/deploy.yml


## TEOS shared requirements
Follow canonical RAIDER when available; mark unknown formal controls PENDING. Record dated evidence and sources, write a unique docs/walkthrough for nontrivial work, coordinate Git branches/worktrees, avoid unnecessary tools and costs. Never claim execution or deployment without a run record. No production, destructive, privilege or paid changes without authorization.
