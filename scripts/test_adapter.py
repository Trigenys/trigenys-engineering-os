"""Regression tests for the optional TEOS index adapter (not the 44 specialist Skills)."""
from __future__ import annotations

import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import install
import teos_checks


class AdapterTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.home = Path(self.tmp.name)
        p = mock.patch("pathlib.Path.home", return_value=self.home)
        p.start()
        self.addCleanup(p.stop)

    def capture(self, callback, *args):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            result = callback(*args)
        return result, out.getvalue()

    def test_adapter_is_versioned_separately_from_specialists(self):
        self.assertEqual(len(install.canonical_skills()), 44)
        self.assertEqual(
            teos_checks.skill_problems(install.TEOS_ADAPTER / "SKILL.md"), [])
        content = (install.TEOS_ADAPTER / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("../<skill-name>/SKILL.md", content)
        self.assertNotIn(".cursor/skills", content)
        self.assertIn("SKILL_NOT_FOUND", content)

    def test_multi_tool_install_reuses_only_two_roots(self):
        self.capture(install.install_adapter, False, False, set(install.TOOLS))
        self.assertTrue((self.home / ".claude" / "skills" /
                         "trigenys-engineering-os" / "SKILL.md").is_file())
        self.assertTrue((self.home / ".agents" / "skills" /
                         "trigenys-engineering-os" / "SKILL.md").is_file())
        self.assertFalse((self.home / ".cursor" / "skills").exists())

    def test_cursor_only_is_explicit(self):
        self.capture(install.install_adapter, False, False, {"cursor"})
        self.assertTrue((self.home / ".cursor" / "skills" /
                         "trigenys-engineering-os" / "SKILL.md").is_file())
        self.assertFalse((self.home / ".claude").exists())
        self.assertFalse((self.home / ".agents").exists())

    def test_compare_is_read_only_and_update_is_idempotent(self):
        deviation, _ = self.capture(install.compare_adapter, set(install.TOOLS))
        self.assertEqual(deviation, 2)
        self.capture(install.install_adapter, False, False, set(install.TOOLS))
        deviation, output = self.capture(install.compare_adapter, set(install.TOOLS))
        self.assertEqual(deviation, 0, output)
        _, second = self.capture(install.install_adapter, False, True, set(install.TOOLS))
        self.assertEqual(second.count("SKIP identical"), 2)
        self.assertFalse((self.home / install.BACKUP_DIRNAME).exists())

    def test_legacy_content_preserved_without_update_and_backed_up_with_update(self):
        old_dir = self.home / ".claude" / "skills" / "trigenys-engineering-os"
        old_dir.mkdir(parents=True)
        (old_dir / "SKILL.md").write_text(
            "---\nname: trigenys-engineering-os\ndescription: local-only\n---\n"
            "old local adapter\n", encoding="utf-8")
        _, dry = self.capture(install.install_adapter, True, True, set(install.TOOLS))
        self.assertIn("BACKUP", dry)
        self.assertFalse((self.home / install.BACKUP_DIRNAME).exists())
        _, guarded = self.capture(install.install_adapter, False, False, set(install.TOOLS))
        self.assertIn("DRIFT preserved", guarded)
        self.assertIn("old local adapter", (old_dir / "SKILL.md").read_text())
        self.capture(install.install_adapter, False, True, set(install.TOOLS))
        backups = list((self.home / install.BACKUP_DIRNAME).rglob(
            "trigenys-engineering-os/SKILL.md"))
        self.assertEqual(len(backups), 1)
        self.assertIn("old local adapter", backups[0].read_text())
        deviation, _ = self.capture(install.compare_adapter, set(install.TOOLS))
        self.assertEqual(deviation, 0)

    def test_adapter_does_not_touch_other_skills_or_agents(self):
        personal = self.home / ".claude" / "skills" / "my-private-skill" / "SKILL.md"
        personal.parent.mkdir(parents=True)
        personal.write_text("personal", encoding="utf-8")
        before = personal.read_bytes()
        self.capture(install.install_adapter, False, True, set(install.TOOLS))
        self.assertEqual(before, personal.read_bytes())
        self.assertFalse((self.home / ".cursor" / "agents").exists())


if __name__ == "__main__":
    unittest.main()
