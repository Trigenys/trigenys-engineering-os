---
name: windows-desktop-packaging
description: Automate reproducible Windows MSI EXE ZIP and desktop release installation verification. Use when auditing or changing this workflow class.
---

# windows-desktop-packaging

## Workflow
1. Determine target architecture, framework and packaging tool (Tauri, .NET/Avalonia, NSIS, Inno, PyInstaller). Prefer already standardized AppFactory packaging workflows.
2. Build on appropriate Windows runners, pin toolchain/lockfile and release SHA. Cache cautiously and avoid credentials in PR artifacts.
3. Verify program startup, silent installation, upgrade/uninstall paths, executable permissions, file association where used, Windows Defender false-positive considerations and exit codes.
4. Create versioned release assets, SHA-256 sums and provenance metadata. Require a clear distinction between `build artifact` and `published GitHub Release`.
5. Test non-admin behavior and accessibility/GUI smoke paths where relevant; avoid dangerous automatic system changes on developer machines.
6. Validate release signature if signing credentials and approval are configured; never create fake signatures or confuse checksum with cryptographic signer authenticity.
## Output
Installer manifest, CI commands, install/upgrade/uninstall results, checksums, release digest and rollback/repair instructions.
## Sources
- https://github.com/EagleFox31/appfactory-project-automation/blob/main/.github/workflows/release-tauri-desktop.yml
- https://github.com/EagleFox31/agenfetch-desktop/blob/main/.github/workflows/release.yml
- https://github.com/EagleFox31/AgenStart/blob/main/.github/workflows/installation-tests.yml


## TEOS shared requirements
Follow canonical RAIDER when available; mark unknown formal controls PENDING. Record dated evidence and sources, write a unique docs/walkthrough for nontrivial work, coordinate Git branches/worktrees, avoid unnecessary tools and costs. Never claim execution or deployment without a run record. No production, destructive, privilege or paid changes without authorization.
