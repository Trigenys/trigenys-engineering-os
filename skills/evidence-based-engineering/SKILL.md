---
name: evidence-based-engineering
description: Require verifiable evidence for technical, market, UX and security claims; perform targeted online research before significant decisions and record source freshness, uncertainty and validation. Use for architecture, product discovery, audits and recommendations.
---

# Evidence-based engineering

## Evidence policy
1. State the decision or testable hypothesis and identify what requires a fresh source.
2. Inspect existing code, relevant failure memory and user requirements before proposing new components; respect RAIDER **Reuse-first** and **Adopt / Adapt / Learn / Build**.
3. Research primary documentation, current standards, proven patterns and competitors when suitable browsing is available. Record dated URLs, edition/version, facts versus vendor claims and contextual applicability (including low-bandwidth/local markets).
4. For benchmarks, record tested workload, version, machine, metric, cost unit, uncertainty and source date. A benchmark score from another task is not universal evidence.
5. For architecture, enumerate feasible alternatives, costs, licensing, maintenance and adoption risks. Prefer a validated existing solution unless custom development has clear advantages.
6. A cited claim is not proof that our own code works. Validate on real representative consumer/test environments and link actual run artifacts.
7. If no web tool/connection exists, record `RESEARCH_BLOCKED` and decline to make fresh claims without evidence. Never fabricate links, prices, certifications, tests or standards compliance.

## Output
Write `docs/research/<task-id>*.md` as appropriate with question, access date, sources, evaluation matrix, decision, confidence, validation plan and limitations. Link relevant ADRs, issues and walkthroughs.

Follow `AGENTS.md`, `docs/raider/RAIDER.md`, and `docs/research/SOURCES.md`.
