# Reconciling a pre-existing local TEOS installation

**Source of truth for shared Skills**: this public repository, `Trigenys/trigenys-engineering-os`. **Source of truth for formal RAIDER**: `EagleFox31/project-registry/RAIDER.md` at the documented upstream SHA. **Source of truth for local customizations**: the user's machine until the user approves an explicit migration.

## Why reconciliation is needed

A separate Cursor Agent reported on 2026-10-09 that it installed **28 Skills**, **15 Cursor agents**, **8 Python scripts**, `teos.ps1` and platform adaptors, in the local user profile. The GitHub TEOS repository now contains **44 canonical Skills** and **18 agent profiles**. This report is user-supplied; remote GitHub cannot verify the local file contents or runtime behavior. **Do not assume their names or content match.**

The local agent also reported finding the verified RAIDER standard via `gh api`. Our GitHub TEOS mirror has since been updated to that verified upstream text.

## Read-only reconciliation

On the Windows machine:

```powershell
git clone https://github.com/Trigenys/trigenys-engineering-os.git
cd trigenys-engineering-os
py scripts/install.py check
py scripts/install.py compare-local
py scripts/install.py install-global --dry-run
```

The compare command reports matching, divergent, missing and local-only files without modifying them. Review local-only scripts, additional adapters and `$HOME/.cursor/trigenys-engineering-os/` before any update.

## Applying updates safely

Only after reviewing the report and any conflicts:

```powershell
py scripts/install.py install-global --dry-run --update
py scripts/install.py install-global --update
```

- Identical content is an idempotent no-op.
- Differing existing files receive timestamped backups before explicit replacement.
- Non-TEOS local user skills and agents are never deleted.
- Existing `$HOME/.cursor/trigenys-engineering-os/` scripts are left untouched.
- Project application repositories are never modified by global installation.
- User Rules and runtime model selection remain manual/independently verifiable.
- The installer cannot synchronize multi-agent sessions or infer local CI success.

## Local-only additions worth upstreaming

The remote agent installed `evidence-based-engineering` and `multi-agent-handoff`; these names are now mirrored as canonical Skills in the repo. However their current remote content may differ from the local versions. The local eight Python scripts and PowerShell `teos.ps1` have **not** been reviewed or imported. To upstream them, submit a PR with their contents and tests, including credential/security reviews.

## Acceptance checks

- Confirm the Cursor Skills catalog and subagents after restarting an Agent session.
- Confirm actual subagent model execution in the agent run details, rather than trusting YAML alone.
- Run `check`, `compare-local`, and dry-runs without opening or modifying production application code.
- Validate cross-tool adapters separately in Cursor, Claude Code and Codex. Their profile/state is not shared.
- Verify RAIDER checks on a greenfield test repository and a brownfield test repository; do not claim compliance without evidence.
