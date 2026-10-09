"""Tests for scripts/install.py, run with: python -m unittest discover -s scripts"""
from __future__ import annotations

import contextlib
import io
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import install

ALL_TOOLS = set(install.TOOLS)
SKILL_ROOTS = (".cursor", ".claude", ".agents")


def run(func, *args) -> str:
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        func(*args)
    return out.getvalue()


def frontmatter_name(skill_md: Path) -> str:
    for line in skill_md.read_text(encoding="utf-8").split("---", 2)[1].splitlines():
        if line.startswith("name:"):
            return line.split(":", 1)[1].strip()
    return ""


class TempHome(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.home = Path(self._tmp.name)
        patcher = mock.patch("pathlib.Path.home", return_value=self.home)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.addCleanup(self._tmp.cleanup)


class SkillPrefixesTest(unittest.TestCase):
    def test_all_tools_use_two_roots_not_three(self) -> None:
        self.assertEqual(install.skill_prefixes(ALL_TOOLS), [".claude", ".agents"])

    def test_cursor_alone_keeps_cloud_synced_root(self) -> None:
        self.assertEqual(install.skill_prefixes({"cursor"}), [".cursor"])

    def test_cursor_and_codex_share_agents_root(self) -> None:
        self.assertEqual(install.skill_prefixes({"cursor", "codex"}), [".agents"])

    def test_claude_alone(self) -> None:
        self.assertEqual(install.skill_prefixes({"claude"}), [".claude"])

    def test_unknown_tool_is_rejected(self) -> None:
        with self.assertRaises(Exception):
            install.parse_tools("cursor,vscode")


class InstallGlobalTest(TempHome):
    def test_second_run_is_a_noop(self) -> None:
        run(install.install_global, False, False, ALL_TOOLS)
        second = run(install.install_global, False, False, ALL_TOOLS).splitlines()[:-1]
        self.assertTrue(second)
        self.assertTrue(all(line.startswith("SKIP identical") for line in second), second)

    def test_no_copy_in_cursor_skill_root_by_default(self) -> None:
        run(install.install_global, False, False, ALL_TOOLS)
        self.assertFalse((self.home / ".cursor" / "skills").exists())
        self.assertTrue((self.home / ".cursor" / "agents" / "implementation-engineer.md").is_file())

    def test_drift_is_preserved_without_update(self) -> None:
        run(install.install_global, False, False, ALL_TOOLS)
        target = self.home / ".agents" / "skills" / "raider-governance" / "SKILL.md"
        target.write_text("local customization", encoding="utf-8")
        output = run(install.install_global, False, False, ALL_TOOLS)
        self.assertIn("DRIFT preserved", output)
        self.assertEqual(target.read_text(encoding="utf-8"), "local customization")

    def test_update_backs_up_outside_every_skill_root(self) -> None:
        run(install.install_global, False, False, ALL_TOOLS)
        target = self.home / ".agents" / "skills" / "raider-governance" / "SKILL.md"
        target.write_text("local customization", encoding="utf-8")
        run(install.install_global, False, True, ALL_TOOLS)

        backups = list((self.home / install.BACKUP_DIRNAME).rglob("raider-governance/SKILL.md"))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_text(encoding="utf-8"), "local customization")
        for root in SKILL_ROOTS:
            for skill_md in (self.home / root / "skills").rglob("SKILL.md"):
                self.assertEqual(frontmatter_name(skill_md), skill_md.parent.name, skill_md)

    def test_dry_run_writes_nothing(self) -> None:
        run(install.install_global, True, True, ALL_TOOLS)
        self.assertEqual(list(self.home.iterdir()), [])


class CompareLocalTest(TempHome):
    def test_flags_redundant_and_superseded_without_modifying(self) -> None:
        legacy_skill = self.home / ".cursor" / "skills" / "raider-governance"
        legacy_skill.mkdir(parents=True)
        (legacy_skill / "SKILL.md").write_text("---\nname: raider-governance\n---\n", encoding="utf-8")
        agents = self.home / ".cursor" / "agents"
        agents.mkdir(parents=True)
        (agents / "senior-project-manager.md").write_text("old", encoding="utf-8")
        (agents / "my-own-agent.md").write_text("mine", encoding="utf-8")

        output = run(install.compare_local, ALL_TOOLS)

        self.assertIn("REDUNDANT", output)
        self.assertIn(str(legacy_skill), output)
        self.assertIn("SUPERSEDED by project-manager.md", output)
        self.assertIn(f"LOCAL-ONLY (preserve) {agents / 'my-own-agent.md'}", output)
        self.assertTrue((agents / "senior-project-manager.md").is_file())
        self.assertTrue(legacy_skill.is_dir())


class InitProjectTest(TempHome):
    def test_project_skills_use_minimal_roots_and_backups_stay_out_of_repo(self) -> None:
        repo = self.home / "repo"
        repo.mkdir()
        subprocess.run(["git", "init", "-q", str(repo)], check=True)
        run(install.init_project, repo, False, False, ALL_TOOLS)
        self.assertFalse((repo / ".cursor" / "skills").exists())
        self.assertTrue((repo / ".agents" / "skills" / "raider-governance" / "SKILL.md").is_file())

        (repo / "AGENTS.md").write_text("project rules", encoding="utf-8")
        run(install.init_project, repo, False, True, ALL_TOOLS)
        self.assertFalse(any(p.name.startswith(install.BACKUP_DIRNAME) for p in repo.iterdir()))
        self.assertTrue(list((self.home / install.BACKUP_DIRNAME).rglob("AGENTS.md")))


class CheckTest(unittest.TestCase):
    def test_repository_configuration_passes(self) -> None:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(install.check(), 0, out.getvalue())


if __name__ == "__main__":
    unittest.main()
