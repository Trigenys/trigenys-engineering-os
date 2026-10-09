---
name: trigenys-engineering-os
description: Index and orchestrate Trigenys Engineering OS Skills using the current tool's discovered Skill directory. Use when coordinating multidisciplinary work, applying RAIDER governance or selecting the appropriate TEOS specialist.
---

# Trigenys Engineering OS — entry point

This is an **index/adapter**, not a replacement for the 44 canonical TEOS specialist Skills.

## Resolve the active Skills

1. Use the **current tool's native Skill discovery** to locate `raider-governance`, `engineering-orchestration`, `smart-model-routing` and a matching domain Skill.
2. When file access is available, resolve the canonical Skills **relative to this adapter's directory**: a sibling `../<skill-name>/SKILL.md` in the *same tool's Skill root*. Do not assume a user's operating system, home directory, repository path or legacy Skill location.
3. If no sibling is present, ask the tool's native Skill catalog for the named Skill and verify the content found. If it is unavailable, report `SKILL_NOT_FOUND` instead of fabricating the missing instructions.
4. Avoid loading every Skill into the context. Start with orchestration + RAIDER + model routing for nontrivial tasks, then include only the relevant domain Skills.
5. The **GitHub source of truth** for the specialists is https://github.com/Trigenys/trigenys-engineering-os/tree/main/skills. The canonical RAIDER standard is mirrored in `docs/raider/RAIDER.md`, originating from https://github.com/EagleFox31/project-registry/blob/main/RAIDER.md.

## Agent coordination

- Read and obey the task repository's `AGENTS.md` / `CLAUDE.md` when present, and follow `docs/agent-coordination/protocol.md` if TEOS was bootstrapped into that project.
- Cursor, Claude Code and Codex are **independent runtimes**. Coordinate through Git worktrees, issues/PRs, explicit file ownership and dated walkthrough handoffs; do not claim shared agent memory, locks or confirmed model selection.
- Prefer a minimal-cost competent model. T0 tasks should run directly; expensive independent specialists require a specific risk justification.
- Run applicable unit, integration, API/contract, E2E and security quality gates. Record real evidence and `NOT VERIFIED` for unexecuted checks.
- Significant product, security, UX or architecture decisions require targeted fresh research where browsing exists. Note unavailable research.

## Safe operation

Never delete or overwrite user-specific Skills, credentials, agents or projects as part of discovering TEOS. No unattended production, destructive or paid actions.

For safe installation/upgrades use `scripts/install.py` in the TEOS repository; the adapter itself does **not** install anything.
