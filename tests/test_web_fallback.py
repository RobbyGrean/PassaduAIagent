import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "skills" / "pasadu"
SCRIPT_DIR = SKILL_ROOT / "scripts" / "pasadu"
sys.path.insert(0, str(SCRIPT_DIR))

from web_fallback import (  # noqa: E402
    WEB_FALLBACK_DISCLAIMER,
    validate_web_fallback_answer,
    validate_web_sources,
)


VALID_SOURCE = {
    "source_type": "web source",
    "site_or_agency": "กรมบัญชีกลาง",
    "url": "https://example.go.th/document",
    "accessed_at": "2026-07-17",
    "authority_name": "ระเบียบตัวอย่าง พ.ศ. 2560",
    "provision": "ข้อ 1",
    "verified": True,
}


class WebFallbackTests(unittest.TestCase):
    def test_valid_web_source_metadata(self):
        result = validate_web_sources([VALID_SOURCE])
        self.assertTrue(result["ok"], result["errors"])

    def test_web_answer_requires_exact_disclaimer_and_visible_metadata(self):
        answer = "\n".join(
            [
                WEB_FALLBACK_DISCLAIMER,
                "Repository source: ไม่พบหลักฐานเพียงพอจาก repository",
                "Web source: กรมบัญชีกลาง — ระเบียบตัวอย่าง พ.ศ. 2560 ข้อ 1",
                "URL: https://example.go.th/document",
                "วันที่เข้าถึง: 2026-07-17",
                "แหล่งนี้เป็น web source ไม่ใช่ repository source",
            ]
        )
        result = validate_web_fallback_answer(answer, [VALID_SOURCE], repository_partial=True)
        self.assertTrue(result["ok"], result["errors"])

    def test_web_answer_rejects_missing_disclaimer(self):
        result = validate_web_fallback_answer("คำตอบ", [VALID_SOURCE])
        self.assertFalse(result["ok"])
        self.assertIn("disclaimer", " ".join(result["errors"]))


if __name__ == "__main__":
    unittest.main()
