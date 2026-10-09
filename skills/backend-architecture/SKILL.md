---
name: backend-architecture
description: Design secure, maintainable backend contracts and domain boundaries. Use proactively when the task needs this expertise.
---

# backend-architecture

## Workflow
Inspect existing architecture and workload first; compare modular monolith, service split and event-driven approaches based on evidence. Review data consistency, migrations, idempotence, auth, failure modes, perf, observability and rollback. Prefer simple working architecture.

## Deliverables
C4/context sketch, API contracts, trade-offs, ADR and verification plan.

## Shared contract
Follow `AGENTS.md`, `docs/raider/RAIDER.md`, `docs/agent-coordination/protocol.md` and `docs/quality/QUALITY-GATES.md`. For nontrivial work write a unique dated walkthrough. Search external sources for significant decisions when online tools are available; cite retrieved URLs with date, otherwise record `RESEARCH_BLOCKED`. Never invent tests, certifications, benchmarks, RAIDER acronym expansions or executed actions.
