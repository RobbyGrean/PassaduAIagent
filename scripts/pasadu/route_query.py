from __future__ import annotations

import argparse
import json
import re

from common import INDEX_ROOT, normalize_digits, read_json


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

RBB3_DIRECT_KEYWORDS = [
    "ฉบับที่ 3",
    "ฉบับ 3",
    "พ.ศ. 2569",
    "rbb60-3",
    "คะแนนความเสียหาย",
    "คะแนนความเสียหายสะสม",
    "การระงับการยื่นข้อเสนอ",
    "ระงับการยื่นข้อเสนอ",
    "การระงับการทำสัญญา",
    "ระงับการทำสัญญา",
    "แบนรับงาน",
]

RBB3_EVALUATION_KEYWORDS = [
    "การประเมินผลการปฏิบัติงานของผู้ประกอบการ",
    "ประเมินผลผู้ประกอบการ",
    "ประเมินผู้ประกอบการ",
    "ประเมินผู้รับเหมา",
    "ประเมินผลผู้รับเหมา",
]

RBB3_DAMAGE_KEYWORDS = [
    "อันตรายสาหัส",
    "ทรัพย์สินเสียหาย",
    "ประมาทเลินเล่อ",
    "หลักวิชาช่าง",
    "ความชำรุดบกพร่อง",
]

RBB3_SCOPE_KEYWORDS = [
    "5 ล้านบาท",
    "ห้าล้านบาท",
    "6 หน่วยงาน",
    "หกหน่วยงาน",
    "กรมชลประทาน",
    "กรมเจ้าท่า",
    "กรมทางหลวง",
    "กรมทางหลวงชนบท",
    "กรมทรัพยากรน้ำ",
    "กรมโยธาธิการและผังเมือง",
    "อาคารสูง",
    "อาคารขนาดใหญ่พิเศษ",
    "อาคารชุมนุมคน",
    "1,000 ล้านบาท",
    "1000 ล้านบาท",
    "พันล้านบาท",
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
SOURCE_RBB3 = "reference/law/rbb60-3.md"


def has_clause_reference(query: str, label: str) -> bool:
    return bool(re.search(rf"{label}\s*[0-9๐-๙]+(?:/[0-9๐-๙]+)?", query))


def is_rbb3_clause_reference(query: str) -> bool:
    normalized = normalize_digits(query)
    return bool(re.search(r"ข้อ\s*(?:190(?:/[1-9])?|191)(?![/0-9])", normalized))


def route_query(query: str) -> dict[str, object]:
    q = query.lower()
    scores = {SOURCE_PRB: 0, SOURCE_RBB: 0, SOURCE_RBB3: 0}
    reasons: list[str] = []
    fallback_sources: list[str] = []
    scope_questions = [
        "งานก่อสร้างนี้มูลค่า 5 ล้านบาทขึ้นไป และเป็นของ 6 หน่วยงานหลักหรือไม่?",
        "งานนี้เป็นอาคารสูง อาคารขนาดใหญ่พิเศษ หรืออาคารชุมนุมคนหรือไม่?",
        "งานก่อสร้างนี้มีมูลค่าตั้งแต่ 1,000 ล้านบาทขึ้นไปหรือไม่?",
    ]

    for keyword in PRB_KEYWORDS:
        if keyword.lower() in q:
            scores[SOURCE_PRB] += 2
            reasons.append(f"พบคำ/ประเด็นฝั่ง พ.ร.บ.: {keyword}")

    for keyword in RBB_KEYWORDS:
        if keyword.lower() in q:
            scores[SOURCE_RBB] += 2
            reasons.append(f"พบคำ/ประเด็นฝั่งระเบียบ: {keyword}")

    for keyword in RBB3_DIRECT_KEYWORDS:
        if keyword.lower() in q:
            scores[SOURCE_RBB3] += 3
            reasons.append(f"พบคำ/ประเด็นฝั่งระเบียบฉบับที่ 3: {keyword}")

    for keyword in RBB3_EVALUATION_KEYWORDS:
        if keyword.lower() in q:
            scores[SOURCE_RBB3] += 2
            reasons.append(f"พบคำ/ประเด็นการประเมินผู้ประกอบการ: {keyword}")

    for keyword in RBB3_DAMAGE_KEYWORDS:
        if keyword.lower() in q:
            scores[SOURCE_RBB3] += 2
            reasons.append(f"พบคำ/ประเด็นคะแนนความเสียหาย: {keyword}")

    for keyword in RBB3_SCOPE_KEYWORDS:
        if keyword.lower() in q:
            scores[SOURCE_RBB3] += 1
            reasons.append(f"พบคำ/ประเด็นขอบเขตระเบียบฉบับที่ 3: {keyword}")

    if has_clause_reference(query, "มาตรา"):
        scores[SOURCE_PRB] += 5
        reasons.append("พบการอ้างเลขมาตราโดยตรง")
    if has_clause_reference(query, "ข้อ"):
        scores[SOURCE_RBB] += 5
        reasons.append("พบการอ้างเลขข้อโดยตรง")
    if is_rbb3_clause_reference(query):
        scores[SOURCE_RBB3] += 7
        reasons.append("พบการอ้างข้อ 190-191 โดยตรง")

    if "สัญญา" in q or "ตรวจรับ" in q or "บริหารสัญญา" in q:
        scores[SOURCE_PRB] += 1
        scores[SOURCE_RBB] += 1
        reasons.append("ประเด็นอาจต้องอ่านทั้งหลักกฎหมายและวิธีปฏิบัติ")

    explicit_prb = has_clause_reference(query, "มาตรา") or any(
        keyword.lower() in q for keyword in ["พรบ", "พ.ร.บ", "พระราชบัญญัติ"]
    )
    explicit_rbb = has_clause_reference(query, "ข้อ") or "ระเบียบ" in q
    prb_first_contract = any(keyword.lower() in q for keyword in PRB_FIRST_CONTRACT_KEYWORDS)
    has_rbb3_direct = is_rbb3_clause_reference(query) or any(
        keyword.lower() in q for keyword in RBB3_DIRECT_KEYWORDS
    )
    has_rbb3_evaluation_context = any(
        keyword.lower() in q for keyword in RBB3_EVALUATION_KEYWORDS
    ) and ("งานก่อสร้าง" in q or "ผู้ประกอบการ" in q or "ผู้รับเหมา" in q)
    has_rbb3_damage_context = any(
        keyword.lower() in q for keyword in RBB3_DAMAGE_KEYWORDS
    )
    has_rbb3_scope_context = any(
        keyword.lower() in q for keyword in RBB3_SCOPE_KEYWORDS
    ) and ("งานก่อสร้าง" in q or "อาคาร" in q)
    asks_rbb3_applicability = (
        "งานก่อสร้าง" in q
        and any(keyword in q for keyword in ["ต้องใช้", "ใช้ระเบียบ", "เข้าข่าย"])
        and any(keyword in q for keyword in ["ฉบับที่ 3", "ฉบับ 3", "rbb60-3"])
    )
    needs_rbb3_scope_check = (
        (has_rbb3_evaluation_context or asks_rbb3_applicability)
        and not has_rbb3_scope_context
        and not is_rbb3_clause_reference(query)
    )
    explicit_rbb3 = has_rbb3_direct or has_rbb3_damage_context or has_rbb3_scope_context
    construction_only = "งานก่อสร้าง" in q and not explicit_rbb3 and not needs_rbb3_scope_check

    if needs_rbb3_scope_check:
        selected = [SOURCE_RBB]
        fallback_sources = [SOURCE_PRB]
        reasons.append("คำถามเกี่ยวกับการประเมินผู้ประกอบการงานก่อสร้าง แต่ยังไม่ทราบว่าเข้า scope ระเบียบฉบับที่ 3 จึงควรถาม scope gate ก่อน")
    elif explicit_rbb3:
        selected = [SOURCE_RBB3]
        fallback_sources = [SOURCE_RBB, SOURCE_PRB]
        reasons.append("คำถามชี้ไปที่ระเบียบฉบับที่ 3/ข้อ 190-191/คะแนนความเสียหาย จึงค้น rbb60-3.md ก่อน")
    elif construction_only:
        selected = [SOURCE_RBB]
        fallback_sources = [SOURCE_PRB]
        reasons.append("พบคำว่างานก่อสร้าง แต่ยังไม่มีบริบทระเบียบฉบับที่ 3/ข้อ 190-191/คะแนนความเสียหาย จึงไม่ route ไป rbb60-3.md")
    elif explicit_prb and not explicit_rbb:
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
        "needs_scope_check": needs_rbb3_scope_check,
        "scope_questions": scope_questions if needs_rbb3_scope_check else [],
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
