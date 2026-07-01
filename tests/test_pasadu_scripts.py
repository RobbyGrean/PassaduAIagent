import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "scripts" / "pasadu"
sys.path.insert(0, str(SCRIPT_DIR))

from build_index import build_index
from cite_check import check_citations
from retrieve import retrieve
from route_query import route_query


def setUpModule():
    build_index()


class PasaduScriptTests(unittest.TestCase):
    def test_route_direct_section_to_prb(self):
        result = route_query("มาตรา 56 กล่าวถึงอะไร")
        self.assertIn("reference/law/prb60.md", result["sources"])

    def test_route_operational_question_to_rbb(self):
        result = route_query("วิธีเฉพาะเจาะจงต้องดำเนินการอย่างไร")
        self.assertIn("reference/law/rbb60.md", result["sources"])

    def test_route_defaults_to_rbb_then_prb(self):
        result = route_query("สัญญาต้องทำอย่างไร")
        self.assertEqual(result["sources"], ["reference/law/rbb60.md"])
        self.assertEqual(result["fallback_sources"], ["reference/law/prb60.md"])

    def test_route_contract_administration_exception_to_prb(self):
        result = route_query("การแก้ไขสัญญาต้องเริ่มดูจากไหน")
        self.assertEqual(result["sources"], ["reference/law/prb60.md"])
        self.assertEqual(result["fallback_sources"], ["reference/law/rbb60.md"])

    def test_route_explicit_regulation_overrides_contract_exception(self):
        result = route_query("ระเบียบข้อไหนพูดถึงการแก้ไขสัญญา")
        self.assertEqual(result["sources"], ["reference/law/rbb60.md"])

    def test_retrieve_direct_clause(self):
        result = retrieve("มาตรา 56 กล่าวถึงอะไร", limit=3)
        top = result["results"][0]
        self.assertEqual(top["source"], "reference/law/prb60.md")
        self.assertEqual(top["clause_type"], "มาตรา")
        self.assertEqual(top["clause_no"], "56")

    def test_cite_check_accepts_existing_citation(self):
        result = check_citations("อ้างอิง: reference/law/prb60.md มาตรา 56")
        self.assertTrue(result["ok"])

    def test_cite_check_rejects_missing_citation(self):
        result = check_citations("อ้างอิง: reference/law/prb60.md มาตรา 999")
        self.assertFalse(result["ok"])


if __name__ == "__main__":
    unittest.main()
