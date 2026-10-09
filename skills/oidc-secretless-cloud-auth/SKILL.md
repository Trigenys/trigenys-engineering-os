---
name: oidc-secretless-cloud-auth
description: Configure short-lived GitHub OIDC identity for AWS and AppFactory instead of proliferating persistent cloud credentials. Use when auditing or changing this workflow class.
---

# oidc-secretless-cloud-auth

## Workflow
1. Define the caller identity: repository, immutable workflow reference, protected environment, branch/ref and requested audience. Document who can dispatch.
2. Prefer GitHub OIDC to long-lived cloud tokens when supported. For AWS use identity provider and IAM role trust conditions scoped to GitHub `sub`, `aud`, repository/branch/environment. For AppFactory follow its existing verified `audience=appfactory-api` and trusted-workflow allowlist.
3. Grant `id-token: write` only to token-requesting jobs and minimal `contents`/deployment permissions. Constrain resource access by deployment role, environment and explicit repo ownership.
4. Authenticate only after trusted code provenance is established. Never accept PR-controlled workflow files as authorized callers. Avoid logging JWT values and secrets.
5. Verify rejected claims: wrong audience, wrong repo, feature branch, expired token, unauthorized workflow, rogue environment and replay attempt.
6. Design credentials rotation and revocation, approval for modifying trust policies, and audit trails for access.
## Output
Threat model, IAM/OIDC trust specification, least privilege matrix, positive/negative claim tests and emergency rollback.
## Sources
- https://github.com/Trigenys/appfactory/blob/main/docs/mutation-authentication.md
- https://github.com/EagleFox31/atelier2026/blob/main/.github/workflows/deploy.yml
- https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/about-security-hardening-with-openid-connect


## TEOS shared requirements
Follow canonical RAIDER when available; mark unknown formal controls PENDING. Record dated evidence and sources, write a unique docs/walkthrough for nontrivial work, coordinate Git branches/worktrees, avoid unnecessary tools and costs. Never claim execution or deployment without a run record. No production, destructive, privilege or paid changes without authorization.
