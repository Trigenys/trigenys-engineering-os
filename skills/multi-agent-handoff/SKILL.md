---
name: multi-agent-handoff
description: Transfer ownership and verified context between Cursor, Claude Code, Codex and other independent agents without overwriting work. Use when another agent continues, reviews or integrates an incomplete task.
---

# Cross-agent handoff

## Procedure
1. Identify task/issue ID, responsible agent/provider, branch/worktree, current commit SHA and approved scope. Do not assume agent memories or tool sessions are shared.
2. Inspect `git status`, PRs, linked docs/walkthrough, pending diffs and overlapping ownership before claiming a task. Uncommitted work remains owned by its originating workspace; do not reset, clean or overwrite it.
3. Write a **new, unique** `docs/walkthrough/<task-id>/<UTC-timestamp>__<provider>__<role>.md` using the template rather than editing another agent's entry.
4. Report what was requested, completed, not done, evidence and tests actually run. Include architecture/API decisions, affected files, source links and relevant RAIDER obligations.
5. Handoff entry should state the exact next action, dependencies, blocked prerequisites, owner responsible, acceptance criteria, deployment/release approval needs and regression risks.
6. Use GitHub Issues/PRs for cross-machine ownership, not Markdown files as distributed locks. For overlapping writes stop and request one integrator or a serialized sequence.
7. If previous work is stale, reconcile with current Git state before making changes. A past message claiming success is not execution proof.

## Output
A separate handoff note in `docs/agent-coordination/handoffs/` linking the walkthrough and any PR, plus a short chat summary. No automatic production, branch merge, billing or destructive changes.

Follow `docs/agent-coordination/protocol.md` and canonical RAIDER in `docs/raider/RAIDER.md`.
