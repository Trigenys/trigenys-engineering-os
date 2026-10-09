---
name: artifact-provenance-sbom
description: Verify SBOM contents, release checksums, signatures and supply-chain attestations for distributed artifacts. Use when auditing or changing this workflow class.
---

# artifact-provenance-sbom

## Workflow
1. Enumerate binary/image outputs, lockfiles and target environments. Pin reviewed dependency graph and source SHA.
2. Generate SBOM (CycloneDX/SPDX as appropriate) for backend/frontend/desktop images; compare packages to actual distributed artifact when supported.
3. Write cryptographic SHA-256 manifest; explicitly distinguish digest from cryptographic signature. If signing or attestations are requested, use authorized keys/identity and verifiable signed provenance.
4. Verify signature trust chain, exact SHA, GitHub release tag/source commit mapping, installer integrity, provenance accessibility and CI artifact retention.
5. Warn when optional signing secrets are absent: `UNSIGNED` must not be reported as `SIGNED`. Identify incomplete supply-chain coverage rather than claiming compliance.
6. Keep signing keys isolated from untrusted PRs. Publish only nonsecret provenance metadata with releases.
## Output
SBOM report, checksums, signing status, provenance and reproducible verification steps.
## Sources
- https://github.com/EagleFox31/appfactory-project-automation/blob/main/.github/workflows/release-tauri-desktop.yml
- https://slsa.dev/


## TEOS shared requirements
Follow canonical RAIDER when available; mark unknown formal controls PENDING. Record dated evidence and sources, write a unique docs/walkthrough for nontrivial work, coordinate Git branches/worktrees, avoid unnecessary tools and costs. Never claim execution or deployment without a run record. No production, destructive, privilege or paid changes without authorization.
