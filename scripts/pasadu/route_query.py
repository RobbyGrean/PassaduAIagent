from __future__ import annotations

import argparse
import json
import re

from common import INDEX_ROOT, read_json


PRB_KEYWORDS = [
    "พรบ",
    "พ.ร.บ",
    "พระราชบัญญัติ",
    "มาตรา",
    "อำนาจตามกฎหมาย",
    "คณะกรรมการ",
    "อุทธรณ์",
    "ร้องเรียน",
    "บทกำหนดโทษ",
    "โทษ",
]

RBB_KEYWORDS = [
    "ระเบียบ",
    "ข้อ",
    "วิธีปฏิบัติ",
    "วิธีประกาศเชิญชวนทั่วไป",
    "วิธีคัดเลือก",
    "วิธีเฉพาะเจาะจง",
    "e-bidding",
    "e-market",
    "สอบราคา",
    "สัญญา",
    "หลักประกัน",
    "ตรวจรับ",
    "บริหารสัญญา",
    "บริหารพัสดุ",
    "คณะกรรมการซื้อหรือจ้าง",
    "คณะกรรมการตรวจรับ",
    "จ้างที่ปรึกษา",
    "จ้างออกแบบ",
    "ควบคุมงานก่อสร้าง",
]

PRB_FIRST_CONTRACT_KEYWORDS = [
    "บริหารสัญญา",
    "บอกเลิกสัญญา",
    "เลิกสัญญา",
    "ตกลงยกเลิกสัญญา",
    "ยกเลิกสัญญา",
    "แก้ไขสัญญา",
    "แก้ไขขสัญญา",
    "เปลี่ยนแปลงสัญญา",
    "งดหรือลดค่าปรับ",
    "ขยายเวลาทำการ",
]

SOURCE_PRB = "reference/law/prb60.md"
SOURCE_RBB = "reference/law/rbb60.md"


def has_clause_reference(query: str, label: str) -> bool:
    return bool(re.search(rf"{label}\s*[0-9๐-๙]+", query))


def route_query(query: str) -> dict[str, object]:
    q = query.lower()
    scores = {SOURCE_PRB: 0, SOURCE_RBB: 0}
    reasons: list[str] = []
    fallback_sources: list[str] = []

    for keyword in PRB_KEYWORDS:
        if keyword.lower() in q:
            scores[SOURCE_PRB] += 2
            reasons.append(f"พบคำ/ประเด็นฝั่ง พ.ร.บ.: {keyword}")

    for keyword in RBB_KEYWORDS:
        if keyword.lower() in q:
            scores[SOURCE_RBB] += 2
            reasons.append(f"พบคำ/ประเด็นฝั่งระเบียบ: {keyword}")

    if has_clause_reference(query, "มาตรา"):
        scores[SOURCE_PRB] += 5
        reasons.append("พบการอ้างเลขมาตราโดยตรง")
    if has_clause_reference(query, "ข้อ"):
        scores[SOURCE_RBB] += 5
        reasons.append("พบการอ้างเลขข้อโดยตรง")

    if "สัญญา" in q or "ตรวจรับ" in q or "บริหารสัญญา" in q:
        scores[SOURCE_PRB] += 1
        scores[SOURCE_RBB] += 1
        reasons.append("ประเด็นอาจต้องอ่านทั้งหลักกฎหมายและวิธีปฏิบัติ")

    explicit_prb = has_clause_reference(query, "มาตรา") or any(
        keyword.lower() in q for keyword in ["พรบ", "พ.ร.บ", "พระราชบัญญัติ"]
    )
    explicit_rbb = has_clause_reference(query, "ข้อ") or "ระเบียบ" in q
    prb_first_contract = any(keyword.lower() in q for keyword in PRB_FIRST_CONTRACT_KEYWORDS)

    if explicit_prb and not explicit_rbb:
        selected = [SOURCE_PRB]
        fallback_sources = [SOURCE_RBB]
        reasons.append("ผู้ใช้ถามเจาะไปที่ พ.ร.บ./มาตรา จึงค้น พ.ร.บ. ก่อน")
    elif explicit_rbb and not explicit_prb:
        selected = [SOURCE_RBB]
        fallback_sources = [SOURCE_PRB]
        reasons.append("ผู้ใช้ถามเจาะไปที่ระเบียบ/ข้อ จึงค้นระเบียบก่อน")
    elif prb_first_contract:
        selected = [SOURCE_PRB]
        fallback_sources = [SOURCE_RBB]
        reasons.append("ประเด็นบริหาร/แก้ไข/เลิกสัญญา ให้เริ่มอ่าน พ.ร.บ. ก่อนตาม policy")
    elif scores[SOURCE_RBB] > 0 or scores[SOURCE_PRB] > 0:
        selected = [SOURCE_RBB]
        fallback_sources = [SOURCE_PRB]
        reasons.append("default policy: ค้นระเบียบก่อน แล้วใช้ พ.ร.บ. ประกอบเมื่อจำเป็น")
    else:
        selected = [SOURCE_RBB]
        fallback_sources = [SOURCE_PRB]
        reasons.append("ไม่พบ keyword ชัดเจน จึงเริ่มจากระเบียบก่อนตาม default policy")

    return {
        "query": query,
        "sources": selected,
        "fallback_sources": fallback_sources,
        "scores": scores,
        "reasons": reasons,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Route a procurement question to Pasadu reference files.")
    parser.add_argument("query", help="User question")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    args = parser.parse_args()

    if not (INDEX_ROOT / "chunks.json").exists():
        raise SystemExit("Index not found. Run: python scripts/pasadu/build_index.py")

    result = route_query(args.query)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("Sources:")
        for source in result["sources"]:
            print(f"- {source}")
        print("Reasons:")
        for reason in result["reasons"]:
            print(f"- {reason}")


if __name__ == "__main__":
    main()
