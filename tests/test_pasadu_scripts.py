import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "scripts" / "pasadu"
sys.path.insert(0, str(SCRIPT_DIR))

from build_index import build_index
from cite_check import check_citations
from common import format_citation
from answer_context import build_context
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
        self.assertEqual(
            result["sources"],
            [
                "reference/law/prb60.md",
                "reference/law/ministerial-regulations/mr-specific-2560.md",
                "reference/law/rbb60.md",
            ],
        )

    def test_route_w214_by_number(self):
        result = route_query("หนังสือเวียน ว 214 กำหนดอะไร")
        self.assertEqual(result["sources"], ["reference/circulars/circular-w214-2563.md"])

    def test_route_w214_by_bidder_qualification(self):
        result = route_query("การกำหนดคุณสมบัติผู้ยื่นเสนอราคาต้องดูอะไร")
        self.assertEqual(result["sources"], ["reference/circulars/circular-w214-2563.md"])

    def test_specific_method_routes_in_authority_order(self):
        result = route_query("วิธีเฉพาะเจาะจงใช้กรณีใด")
        self.assertEqual(
            result["sources"],
            [
                "reference/law/prb60.md",
                "reference/law/ministerial-regulations/mr-specific-2560.md",
                "reference/law/rbb60.md",
            ],
        )

    def test_route_specific_method_ministerial_regulation(self):
        result = route_query("กฎกระทรวงเฉพาะเจาะจงกำหนดวงเงินเท่าไร")
        self.assertEqual(
            result["sources"],
            [
                "reference/law/prb60.md",
                "reference/law/ministerial-regulations/mr-specific-2560.md",
                "reference/law/rbb60.md",
            ],
        )

    def test_route_small_amount_inspector(self):
        result = route_query("วงเงินเล็กน้อยแต่งตั้งกรรมการตรวจรับคนเดียวได้ไหม")
        self.assertEqual(
            result["sources"],
            [
                "reference/law/prb60.md",
                "reference/law/ministerial-regulations/mr-specific-2560.md",
                "reference/law/rbb60.md",
            ],
        )

    def test_route_general_appeal_to_all_authorities(self):
        result = route_query("การอุทธรณ์ต้องดำเนินการอย่างไร")
        self.assertEqual(
            result["sources"],
            [
                "reference/law/prb60.md",
                "reference/law/ministerial-regulations/mr-appeal-exclusions-2568.md",
                "reference/circulars/circular-w367-2567.md",
            ],
        )

    def test_route_non_appealable_issue_to_ministerial_regulation(self):
        result = route_query("เรื่องที่อุทธรณ์ไม่ได้ตามกฎกระทรวงอุทธรณ์มีอะไรบ้าง")
        self.assertEqual(
            result["sources"],
            [
                "reference/law/ministerial-regulations/mr-appeal-exclusions-2568.md",
                "reference/law/prb60.md",
            ],
        )

    def test_route_no_standing_to_w367(self):
        result = route_query("กรณีใดไม่เข้าข่ายที่จะใช้สิทธิอุทธรณ์ตามมาตรา 114")
        self.assertEqual(
            result["sources"],
            ["reference/circulars/circular-w367-2567.md", "reference/law/prb60.md"],
        )

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

    def test_route_explicit_act_and_regulation_keeps_both_authorities(self):
        result = route_query("ตาม พ.ร.บ. มาตรา 93 และระเบียบข้อ 182 ต้องทำอย่างไร")
        self.assertEqual(result["sources"], ["reference/law/prb60.md", "reference/law/rbb60.md"])
        self.assertEqual(result["fallback_sources"], [])

    def test_route_rbb3_direct_clause(self):
        result = route_query("ข้อ 190/3 ประเมินอะไร")
        self.assertEqual(result["sources"], ["reference/law/rbb60-3.md"])
        self.assertEqual(result["fallback_sources"], ["reference/law/rbb60.md", "reference/law/prb60.md"])

    def test_route_general_construction_does_not_force_rbb3(self):
        result = route_query("งานก่อสร้างใช้วิธีเฉพาะเจาะจงได้ไหม")
        self.assertEqual(
            result["sources"],
            [
                "reference/law/prb60.md",
                "reference/law/ministerial-regulations/mr-specific-2560.md",
                "reference/law/rbb60.md",
            ],
        )
        self.assertNotIn("reference/law/rbb60-3.md", result["sources"])
        self.assertFalse(result["needs_scope_check"])

    def test_route_scope_gate_for_contractor_evaluation_question(self):
        result = route_query("งานก่อสร้างต้องประเมินผู้รับเหมาไหม")
        self.assertEqual(result["sources"], ["reference/law/rbb60.md"])
        self.assertEqual(result["fallback_sources"], ["reference/law/prb60.md"])
        self.assertTrue(result["needs_scope_check"])
        self.assertEqual(
            result["scope_questions"],
            [
                "งานก่อสร้างนี้มูลค่า 5 ล้านบาทขึ้นไป และเป็นของ 6 หน่วยงานหลักหรือไม่?",
                "งานนี้เป็นอาคารสูง อาคารขนาดใหญ่พิเศษ หรืออาคารชุมนุมคนหรือไม่?",
                "งานก่อสร้างนี้มีมูลค่าตั้งแต่ 1,000 ล้านบาทขึ้นไปหรือไม่?",
            ],
        )

    def test_route_scope_gate_for_issue_three_applicability_question(self):
        result = route_query("ต้องใช้ระเบียบฉบับที่ 3 ไหม")
        self.assertEqual(result["sources"], ["reference/law/rbb60.md"])
        self.assertEqual(result["fallback_sources"], ["reference/law/prb60.md"])
        self.assertTrue(result["needs_scope_check"])

    def test_route_damage_term_directly_to_rbb3(self):
        result = route_query("อันตรายสาหัสคิดคะแนนอย่างไร")
        self.assertEqual(result["sources"], ["reference/law/rbb60-3.md"])

    def test_route_property_damage_term_directly_to_rbb3(self):
        result = route_query("ทรัพย์สินเสียหายคิดคะแนนอย่างไร")
        self.assertEqual(result["sources"], ["reference/law/rbb60-3.md"])

    def test_retrieve_rbb3_fraction_clause(self):
        result = retrieve("ข้อ 190/3 ประเมินอะไร", limit=3)
        top = result["results"][0]
        self.assertEqual(top["source"], "reference/law/rbb60-3.md")
        self.assertEqual(top["clause_type"], "ข้อ")
        self.assertEqual(top["clause_no"], "190/3")

    def test_retrieve_direct_clause(self):
        result = retrieve("มาตรา 56 กล่าวถึงอะไร", limit=3)
        top = result["results"][0]
        self.assertEqual(top["source"], "reference/law/prb60.md")
        self.assertEqual(top["clause_type"], "มาตรา")
        self.assertEqual(top["clause_no"], "56")

    def test_retrieve_w214_numbered_heading(self):
        result = retrieve("ว 214 หัวข้อ 1.1.2 กำหนดอะไร", limit=3)
        top = result["results"][0]
        self.assertEqual(top["source"], "reference/circulars/circular-w214-2563.md")
        self.assertEqual(top["clause_type"], "หัวข้อ")
        self.assertEqual(top["clause_no"], "1.1.2")

    def test_retrieve_written_agreement_question_prioritizes_clause_four(self):
        result = retrieve("วงเงินเล็กน้อยไม่ทำข้อตกลงเป็นหนังสือได้ไหม", limit=3)
        ministerial = [
            item
            for item in result["results"]
            if item["source"] == "reference/law/ministerial-regulations/mr-specific-2560.md"
        ]
        self.assertTrue(ministerial)
        self.assertEqual(ministerial[0]["clause_no"], "4")

    def test_retrieve_specific_method_prioritizes_section_56(self):
        result = retrieve("วิธีเฉพาะเจาะจงใช้กรณีใด", limit=5)
        self.assertEqual(result["results"][0]["source"], "reference/law/prb60.md")
        self.assertEqual(str(result["results"][0]["clause_no"]), "56")

    def test_retrieve_non_appealable_issue_prioritizes_ministerial_clause_three(self):
        result = retrieve("เรื่องที่อุทธรณ์ไม่ได้ตามกฎกระทรวงอุทธรณ์", limit=3)
        self.assertEqual(
            result["results"][0]["source"],
            "reference/law/ministerial-regulations/mr-appeal-exclusions-2568.md",
        )
        self.assertEqual(result["results"][0]["clause_no"], "3")

    def test_retrieve_general_appeal_prioritizes_sections_114_to_119(self):
        result = retrieve("การอุทธรณ์อยู่ใน พรบ มาตราใด", limit=5)
        found_sources = {item["source"] for item in result["results"]}
        self.assertEqual(
            found_sources,
            {
                "reference/law/prb60.md",
                "reference/law/ministerial-regulations/mr-appeal-exclusions-2568.md",
                "reference/circulars/circular-w367-2567.md",
            },
        )
        prb_results = [
            item for item in result["results"] if item["source"] == "reference/law/prb60.md"
        ]
        self.assertTrue(prb_results)
        self.assertIn(str(prb_results[0]["clause_no"]), {"114", "115", "116", "117", "118", "119"})

    def test_cite_check_accepts_existing_citation(self):
        result = check_citations("อ้างอิง: reference/law/prb60.md มาตรา 56")
        self.assertTrue(result["ok"])

    def test_cite_check_accepts_human_readable_authority_citation(self):
        result = check_citations(
            "อ้างอิง: พระราชบัญญัติการจัดซื้อจัดจ้างและการบริหารพัสดุภาครัฐ พ.ศ. 2560 มาตรา 56"
        )
        self.assertTrue(result["ok"])

    def test_format_citation_hides_internal_filename(self):
        citation = format_citation("reference/law/rbb60.md", "ข้อ", "78")
        self.assertEqual(
            citation,
            "ระเบียบกระทรวงการคลังว่าด้วยการจัดซื้อจัดจ้างและการบริหารพัสดุภาครัฐ พ.ศ. 2560 ข้อ 78",
        )
        self.assertNotIn("rbb60.md", citation)

    def test_answer_context_uses_authority_names(self):
        context = build_context("มาตรา 56 กล่าวถึงอะไร", limit=1)
        self.assertIn("authorities:", context)
        self.assertIn("พระราชบัญญัติการจัดซื้อจัดจ้างและการบริหารพัสดุภาครัฐ พ.ศ. 2560 มาตรา 56", context)
        self.assertNotIn("reference/law/prb60.md มาตรา 56", context)

    def test_cite_check_accepts_rbb3_fraction_clause(self):
        result = check_citations("อ้างอิง: reference/law/rbb60-3.md ข้อ 190/3")
        self.assertTrue(result["ok"])

    def test_cite_check_accepts_circular_heading(self):
        result = check_citations(
            "อ้างอิง: reference/circulars/circular-w214-2563.md หัวข้อ 1.1.2"
        )
        self.assertTrue(result["ok"])

    def test_cite_check_rejects_missing_citation(self):
        result = check_citations("อ้างอิง: reference/law/prb60.md มาตรา 999")
        self.assertFalse(result["ok"])


if __name__ == "__main__":
    unittest.main()
