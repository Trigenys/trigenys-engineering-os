---
name: automated-test-strategy
description: Develop reproducible unit integration API contract and E2E tests. Use proactively when the task needs this expertise.
---

# automated-test-strategy

## Workflow
Read acceptance criteria, data flows and existing test infrastructure. Build isolated fixtures, scenarios with assertions and failure paths. Run gates in order and stop expensive downstream checks if upstream blockers invalidate them. Use Playwright/Pytest/Vitest/Pact only when suitable.

## Deliverables
Executable tests, matrix linking requirements to cases, actual results.

## Shared contract
Follow `AGENTS.md`, `docs/raider/RAIDER.md`, `docs/agent-coordination/protocol.md` and `docs/quality/QUALITY-GATES.md`. For nontrivial work write a unique dated walkthrough. Search external sources for significant decisions when online tools are available; cite retrieved URLs with date, otherwise record `RESEARCH_BLOCKED`. Never invent tests, certifications, benchmarks, RAIDER acronym expansions or executed actions.
