---
name: visual-regression-ux-evidence
description: Generate reproducible visual screenshots and behavioral UX assertions across representative devices. Use when auditing or changing this workflow class.
---

# visual-regression-ux-evidence

## Workflow
1. Identify changed UI surfaces and acceptance criteria, screenshots/baselines, responsive viewports, accessible states, localization and theme variants.
2. Execute Playwright on deterministic fixtures or preview build; record explicitly whether API is simulated. Do not equate a screenshot with behavior verified in production.
3. Cover loading, empty, error, success, form validation, keyboard focus, mobile layout and reduced-motion states when applicable.
4. Compare screenshots by stable thresholds with controlled fonts/time/data. Investigate differences instead of blindly refreshing baselines.
5. Capture screenshot diffs, links to CI artifacts and author approvals for intentional visual changes. Add targeted accessibility checks.
6. Run a separate production smoke against a real deployed version where feasible, without disclosing production user data.
## Output
Baseline/diff evidence, visual approval status, automated scenario results and residual blind spots.
## Sources
- https://github.com/Trigenys/sims-mod-health/blob/main/.github/workflows/visual-evidence.yml
- https://github.com/EagleFox31/atelier2026/blob/main/.github/workflows/ux-guardrails.yml


## TEOS shared requirements
Follow canonical RAIDER when available; mark unknown formal controls PENDING. Record dated evidence and sources, write a unique docs/walkthrough for nontrivial work, coordinate Git branches/worktrees, avoid unnecessary tools and costs. Never claim execution or deployment without a run record. No production, destructive, privilege or paid changes without authorization.
