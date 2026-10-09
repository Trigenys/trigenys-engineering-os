# Engineering lessons learned

This file is the default RAIDER failure-memory location for this service.

Record meaningful failures and near misses with:

- context and impact;
- root cause;
- resolution;
- recurrence-prevention guardrail;
- generalized lesson when applicable.

Before risky work that resembles a known incident, search this file first.

## 2026-10-09 — Installer backups and copies loaded as duplicate Skills (near miss)

- **Context**: reconciling a local TEOS installation with this repository, before running `install-global --update` on a real machine.
- **Impact if it had run**: every replaced Skill backed up as `<name>.bak-<stamp>/SKILL.md` inside the skill folder; each Skill also copied into `.cursor/skills`, `.claude/skills` and `.agents/skills`. Cursor would have loaded up to four entries per Skill name, and Claude Code would have exposed each backup as its own `/name.bak-…` skill.
- **Root cause**: the installer treated skill folders as plain storage. Cursor walks skill roots recursively and reads three of them; Claude Code turns every sub-folder into a skill.
- **Resolution**: backups go to `~/.teos-backups/<stamp>/`; Skills go to the fewest roots covering the selected `--tools`; `compare-local` reports `REDUNDANT` Skills and `SUPERSEDED` agents.
- **Prevention**: `scripts/test_install.py` asserts that after `--update` every `SKILL.md` under a skill root has a frontmatter name equal to its folder, and that a default install creates no `.cursor/skills` copy. Run in TEOS Skills CI.
- **Generalized lesson**: a folder scanned by a tool is configuration, not storage. Backups, drafts and alternative copies go outside every folder a consumer tool discovers.
