"""Tests for scripts/teos_checks.py, run with: python -m unittest discover -s scripts -p "test_*.py" """
from __future__ import annotations

import contextlib
import io
import tempfile
import unittest
from pathlib import Path

import install
import teos_checks

WALKTHROUGH_KEYS = ["task_id", "agent", "status"]


class TempDir(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)

    def write(self, relative: str, text: str) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path


class FrontmatterTest(unittest.TestCase):
    def test_crlf_and_quotes_and_nested_maps(self) -> None:
        text = '---\r\nname: "a-b"\r\nmetadata:\r\n  version: "1"\r\n---\r\nbody'
        self.assertEqual(teos_checks.frontmatter(text), {"name": "a-b", "metadata": ""})

    def test_unterminated_block_is_absent(self) -> None:
        self.assertIsNone(teos_checks.frontmatter("---\nname: x\n"))


class SkillTest(TempDir):
    def skill(self, folder: str, name: str, description: str = "Does X. Use when Y.") -> Path:
        return self.write(f"{folder}/SKILL.md", f"---\nname: {name}\ndescription: {description}\n---\n")

    def test_valid_skill(self) -> None:
        self.assertEqual(teos_checks.skill_problems(self.skill("pdf-tools", "pdf-tools")), [])

    def test_name_prefix_of_folder_is_not_enough(self) -> None:
        problems = teos_checks.skill_problems(self.skill("raider", "raider-governance"))
        self.assertTrue(any("must equal folder" in p for p in problems), problems)

    def test_spec_naming_rules(self) -> None:
        for bad in ("PDF", "-pdf", "pdf-", "pdf--tools", "a" * 65):
            with self.subTest(name=bad):
                self.assertTrue(teos_checks.skill_problems(self.skill(bad, bad)))

    def test_description_required_and_bounded(self) -> None:
        self.assertTrue(teos_checks.skill_problems(self.skill("a", "a", "")))
        self.assertTrue(teos_checks.skill_problems(self.skill("b", "b", "x" * 1025)))
        self.assertEqual(teos_checks.skill_problems(self.skill("c", "c", "x" * 1024)), [])


class AgentTest(TempDir):
    def agent(self, file: str, name: str, readonly: str = "true") -> Path:
        return self.write(f"{file}.md", f"---\nname: {name}\ndescription: d\nmodel: inherit\n"
                                        f"readonly: {readonly}\n---\n")

    def test_valid_agent(self) -> None:
        self.assertEqual(teos_checks.agent_problems(self.agent("qa", "qa")), [])

    def test_name_must_match_file(self) -> None:
        self.assertTrue(teos_checks.agent_problems(self.agent("qa", "other")))

    def test_readonly_must_be_boolean(self) -> None:
        self.assertTrue(teos_checks.agent_problems(self.agent("qa", "qa", "yes")))

    def test_missing_model(self) -> None:
        path = self.write("qa.md", "---\nname: qa\ndescription: d\nreadonly: true\n---\n")
        self.assertIn(f"{path}: model missing", teos_checks.agent_problems(path))


class RaiderProvenanceTest(TempDir):
    def test_header_must_cite_upstream_commit(self) -> None:
        good = self.write("good.md", f"<!-- {teos_checks.RAIDER_UPSTREAM}{'a' * 40}/RAIDER.md -->\n# R")
        self.assertEqual(teos_checks.raider_provenance_problems(good), [])
        unpinned = self.write("bad.md", f"<!-- {teos_checks.RAIDER_UPSTREAM}main/RAIDER.md -->\n# R")
        self.assertTrue(teos_checks.raider_provenance_problems(unpinned))
        self.assertTrue(teos_checks.raider_provenance_problems(self.root / "absent.md"))

    def test_repository_mirror_is_pinned(self) -> None:
        self.assertEqual(teos_checks.raider_provenance_problems(
            install.ROOT / "docs" / "raider" / "RAIDER.md"), [])


class WalkthroughTest(TempDir):
    def test_missing_key_is_reported_and_template_skipped(self) -> None:
        self.write("docs/walkthrough/TEMPLATE.md", "no frontmatter")
        self.write("docs/walkthrough/T-1/ok.md", "---\ntask_id: T-1\nagent: a\nstatus: DONE\n---\n")
        bad = self.write("docs/walkthrough/T-2/bad.md", "---\ntask_id: T-2\nagent: a\n---\n")
        self.assertEqual(teos_checks.walkthrough_problems(self.root, WALKTHROUGH_KEYS),
                         [f"{bad}: status missing"])

    def test_keys_come_from_the_repository_template(self) -> None:
        keys = install.walkthrough_keys()
        self.assertIn("task_id", keys)
        self.assertIn("model_reported", keys)


class ResearchTest(TempDir):
    def test_note_needs_url_and_date_unless_blocked(self) -> None:
        self.write("docs/research/SOURCES.md", "protocol, no url")
        self.write("docs/research/ok.md", "Checked 2026-10-09 at https://example.org")
        self.write("docs/research/blocked.md", "RESEARCH_BLOCKED: offline")
        bad = self.write("docs/research/bad.md", "opinion only")
        self.assertEqual(teos_checks.research_problems(self.root),
                         [f"{bad}: no source URL", f"{bad}: no YYYY-MM-DD check date"])


class ValidateProjectTest(TempDir):
    def test_reports_failure_and_modifies_nothing(self) -> None:
        self.write("docs/walkthrough/T-1/bad.md", "no frontmatter")
        before = sorted(p.relative_to(self.root) for p in self.root.rglob("*"))
        with contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(install.validate_project(self.root), 1)
        self.assertIn("frontmatter absent", out.getvalue())
        self.assertEqual(sorted(p.relative_to(self.root) for p in self.root.rglob("*")), before)

    def test_empty_project_passes(self) -> None:
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(install.validate_project(self.root), 0)


if __name__ == "__main__":
    unittest.main()
