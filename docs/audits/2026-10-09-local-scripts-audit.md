# Audit of the pre-repository local TEOS scripts — 2026-10-09

Scope: the 11 Python scripts and `teos.ps1` installed under `~/.cursor/trigenys-engineering-os/scripts/` on the maintainer's Windows machine before this repository existed. They were read, not executed, and are **kept in place**; nothing was deleted. Reference for comparison: `scripts/install.py` at `63ad98c`.

Decision vocabulary: RAIDER *Adopt · Adapt · Learn · Build*.

## Findings

| Local script | What it does | Tests | Repository equivalent | Decision |
|---|---|---|---|---|
| `validate_skill_config.py` | Parses frontmatter; exact `name` = folder, `[a-z0-9-]` names, description non-empty and ≤ 1024, agent `readonly` boolean, model allowlist | none | `check` used substring tests: `name: raider` passed for `name: raider-governance` | **Adapt** → `teos_checks.skill_problems` / `agent_problems`, rules from the [Agent Skills specification](https://agentskills.io/specification) (checked 2026-10-09). Model allowlist **not** ported: its IDs (`effort=high`) are stale |
| `raider_compliance_check.py` | Checks RAIDER sections and the upstream SHA in the mirror header | none | `check` verified sections, not provenance | **Adapt** → `raider_provenance_problems`: first line must cite the upstream URL with a 40-hex commit |
| `validate_walkthroughs.py` | Required walkthrough frontmatter keys for a project (`--repo`) | none | none | **Adapt** → `walkthrough_problems`; keys are read from `docs/walkthrough/TEMPLATE.md` instead of a second hard-coded list. Runs in `check` (this repo) and `validate-project --path` |
| `research_evidence_check.py` | Research notes need a URL and an ISO date unless blocked | none | protocol only (`docs/research/SOURCES.md`) | **Adapt** → `research_problems`; marker aligned on `RESEARCH_BLOCKED` from `SOURCES.md` |
| `installation_healthcheck.py` | Installed files present, then runs the two validators; reports CONFIGURED vs VERIFIED | none | `compare-local` (always exit 0) | **Adapt** → `compare-local --strict` exits 1 on any missing, different, redundant or superseded entry. Local script now reports FAIL: it expects the 28 old Skills in `~/.cursor/skills` and the 4 renamed agents |
| `install_teos.py` + `_install_content.py` (1 099 lines) | Generates 28 Skills and 15 agents from Python strings; writes the `.claude`/`.agents` adapter | none | `install-global` copies versioned files | **Do not port.** Overwrites unconditionally (no backup, no dry run); content superseded by `skills/` and `.cursor/agents/` |
| `bootstrap_project.py` | Creates `docs/` folders, `AGENTS.md`, `.cursor/rules/teos.mdc`, `CLAUDE.md`, adapter and a bootstrap report in a repo | none | `init-project` (dry run, keeps drift, backups outside the repo) | **Learn**: only the written `BOOTSTRAP-REPORT.md` is missing upstream; not worth porting alone. Local version writes without dry run |
| `teos_paths.py` | Path helpers | none | constants in `install.py` | **Do not port.** Hard-codes `~/.cursor/skills` as the Skill root, the layout this repository moved away from |
| `test_matrix_report.py` | Counts PASSED/FAILED/… words in `docs/` | none | none | **Do not port.** Counts template and prose occurrences, so the numbers are not evidence |
| `validate_agent_coordination.py` | Checks `task-registry.md` exists | none | none | **Do not port.** No semantic check (prints `semantic lock NOT claimed`) |
| `teos.ps1` | PowerShell wrapper for four scripts | none | `python scripts/install.py …` works on every OS | **Do not port** |

## Security review

- No network access, no secrets read, no shell interpolation (`subprocess.run` with an argument list).
- Data-loss risk: `install_teos.py` and `bootstrap_project.py` overwrite or create files without dry run or backup. Do not run them again; `install.py` replaces both.
- The adapter they wrote (`~/.claude/skills/trigenys-engineering-os`, `~/.agents/skills/trigenys-engineering-os`) still tells agents to load Skills from `~/.cursor/skills`, which is empty after the 2026-10-09 migration ([#7](https://github.com/Trigenys/trigenys-engineering-os/issues/7)). Follow-up: ship this adapter from the repository.

## Other local material worth reviewing (not in this change)

- `~/.cursor/trigenys-engineering-os/STANDARDS-CATALOG.md`: 84-line catalogue of official references with URLs and a 2026-10-09 check date; `skills/standards-research` has 15 lines and no reference file. Candidate: `skills/standards-research/references/standards-catalog.md` after a link check. The `standards-catalog.md` kept in the cleanup backup is only a two-line pointer to it.
- `~/.cursor/trigenys-engineering-os/` docs (`MODEL-ROUTING.md`, `AGENT-REGISTRY.md`, `QUALITY-GATES.md`, …): compare with `docs/` before archiving.
