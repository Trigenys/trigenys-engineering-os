---
name: performance-benchmark-unit-economics
description: Build deterministic technical benchmarks and quantify operational unit economics for product decisions. Use when auditing or changing this workflow class.
---

# performance-benchmark-unit-economics

## Workflow
1. State hypothesis, workload, cost unit (per request/render/user/export/MB/minute), expected SLO and statistical confidence limitations.
2. Pin dataset/fixtures, machine/runner profile, dependency versions and warm-up policy. Record CPU, memory, latency distribution (p50/p95/p99 where measured), throughput and real elapsed time.
3. Compare alternatives at equal quality criteria; use matched workload with separated cold-start effects. Run enough samples for stability; report uncertainty and outliers.
4. Model direct API/compute/storage/network/license costs and the impact of retries, failed jobs and caching. Verify current provider prices from official documentation before hard cost claims.
5. Archive compact reproducible outputs, seeds and script versions. Do not publish customer data or proprietary source fixtures.
6. Promote improvements only if correctness, security and user-facing functionality remain intact.
## Output
Reproducible benchmark plan, measured table, cost model, confidence, recommendation and measurement gaps.
## Public examples
- https://github.com/Trigenys/release-video-engine/blob/main/.github/workflows/media-heavy-renderer-benchmark.yml
- https://github.com/Trigenys/release-video-engine/blob/main/.github/workflows/unit-economics.yml
- https://github.com/Trigenys/sims-mod-health/blob/main/.github/workflows/scanner-benchmark.yml


## TEOS shared requirements
Follow canonical RAIDER when available; mark unknown formal controls PENDING. Record dated evidence and sources, write a unique docs/walkthrough for nontrivial work, coordinate Git branches/worktrees, avoid unnecessary tools and costs. Never claim execution or deployment without a run record. No production, destructive, privilege or paid changes without authorization.
