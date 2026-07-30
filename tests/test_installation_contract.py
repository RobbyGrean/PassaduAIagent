import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "skills" / "pasadu"


class InstallationContractTests(unittest.TestCase):
    def test_standalone_skill_has_required_runtime_files(self):
        required = [
            "SKILL.md",
            "pasadu.md",
            "agents/openai.yaml",
            "reference/law/prb60.md",
            "reference/law/rbb60.md",
            "reference/law/rbb60-3.md",
            "scripts/pasadu/evidence_packet.py",
            "scripts/pasadu/route_query.py",
            "scripts/pasadu/cite_check.py",
            "data/index/chunks.json",
            "data/index/documents.json",
            "data/release.json",
        ]
        missing = [path for path in required if not (SKILL_ROOT / path).is_file()]
        self.assertEqual(missing, [])

    def test_repository_exposes_exactly_one_installable_skill(self):
        skill_manifests = [
            path for path in REPO_ROOT.rglob("SKILL.md") if ".git" not in path.parts
        ]
        self.assertEqual(skill_manifests, [SKILL_ROOT / "SKILL.md"])

    def test_manual_fallback_assets_exist(self):
        required = [
            REPO_ROOT / "scripts" / "install-pasadu.ps1",
            REPO_ROOT / "newbie user guide" / "prompt.txt",
            REPO_ROOT / "newbie user guide" / "update-prompt.txt",
        ]
        self.assertEqual([path for path in required if not path.is_file()], [])

    def test_release_marker_is_machine_readable(self):
        release = json.loads(
            (SKILL_ROOT / "data" / "release.json").read_text(encoding="utf-8")
        )
        self.assertEqual(release["schema_version"], 1)
        self.assertRegex(release["package_release"], r"^\d{4}\.\d{2}\.\d{2}$")
        self.assertRegex(release["reference_snapshot_date"], r"^\d{4}-\d{2}-\d{2}$")
        self.assertEqual(release["source_path"], "skills/pasadu")

    def test_novice_install_does_not_require_developer_tools(self):
        guide = (
            REPO_ROOT / "newbie user guide" / "เริ่มต้นใช้งาน.txt"
        ).read_text(encoding="utf-8")
        prompt = (
            REPO_ROOT / "newbie user guide" / "prompt.txt"
        ).read_text(encoding="utf-8")
        self.assertIn("ผู้ใช้ทั่วไปไม่ต้องติดตั้ง Node.js, npm หรือ Git", guide)
        self.assertIn("ห้ามบังคับให้ติดตั้งเครื่องมือเหล่านี้", prompt)
        self.assertIn("Invoke-WebRequest", prompt)
        self.assertIn("Expand-Archive", prompt)

    def test_development_assets_are_not_inside_installable_skill(self):
        excluded = [
            "tests",
            "evals",
            "docs",
            "how2agent",
            ".codex",
            ".claude",
            ".gemini",
            "reference/ECPP",
        ]
        included = [path for path in excluded if (SKILL_ROOT / path).exists()]
        self.assertEqual(included, [])

    def test_skill_frontmatter_is_valid_and_minimal(self):
        text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\n"))
        frontmatter = text.split("---", 2)[1]
        keys = {
            line.split(":", 1)[0].strip()
            for line in frontmatter.splitlines()
            if ":" in line
        }
        self.assertEqual(keys, {"name", "description"})
        self.assertIn("name: pasadu", frontmatter)

    def test_standalone_runtime_has_no_custom_agent_dependency(self):
        runtime_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in [SKILL_ROOT / "SKILL.md", SKILL_ROOT / "pasadu.md"]
        )
        forbidden = ["legal_analyst", "legal-analyst", "gpt-5.6-luna"]
        found = [term for term in forbidden if term in runtime_text]
        self.assertEqual(found, [])

    def test_skill_commands_are_cross_platform(self):
        text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertNotIn(r"python scripts\pasadu", text)

    def test_installation_docs_do_not_use_legacy_codex_path(self):
        docs = [
            REPO_ROOT / "INSTALLATION.md",
            REPO_ROOT / "README.md",
            REPO_ROOT / "newbie user guide" / "prompt.txt",
            REPO_ROOT / "newbie user guide" / "เริ่มต้นใช้งาน.txt",
        ]
        legacy = ".codex\\skills\\pasadu"
        offenders = [
            str(path.relative_to(REPO_ROOT))
            for path in docs
            if legacy in path.read_text(encoding="utf-8")
        ]
        self.assertEqual(offenders, [])

    def test_installable_skill_stays_bounded(self):
        files = [path for path in SKILL_ROOT.rglob("*") if path.is_file()]
        total_bytes = sum(path.stat().st_size for path in files)
        self.assertLessEqual(len(files), 40)
        self.assertLessEqual(total_bytes, 5 * 1024 * 1024)


if __name__ == "__main__":
    unittest.main()
