# Shared work contract

This directory defines the human-readable coordination protocol that Cursor, Claude Code and Codex can all consult. It is not a remote locking server.

- `protocol.md` — scope, ownership, Git worktrees, integration gates and conflict handling.
- `handoffs/` — per-task handoff notes when created.
- `conflicts/` — documented ownership or integration conflicts when created.
- `docs/walkthrough/` — independent dated work records, one file per agent intervention.

Use GitHub Issues and PRs for cross-machine task assignment rather than assuming an updated local Markdown file is universally visible.
