from __future__ import annotations

import argparse
import json
import math
import re

from common import (
    INDEX_ROOT,
    REFERENCE_SECTION_NUMBER_PATTERN,
    character_ngrams,
    display_source,
    focus_phrases,
    format_citation,
    normalize_digits,
    normalize_search_text,
    read_json,
    tokenize,
)
from route_query import route_query


DOMAIN_KEYWORDS = [
    "วิธีเฉพาะเจาะจง",
    "วิธีคัดเลือก",
    "วิธีประกาศเชิญชวนทั่วไป",
    "ประกวดราคาอิเล็กทรอนิกส์",
    "ตลาดอิเล็กทรอนิกส์",
    "e-bidding",
    "e-market",
    "สอบราคา",
    "คณะกรรมการตรวจรับ",
    "ตรวจรับ",
    "คณะกรรมการซื้อหรือจ้าง",
    "หลักประกัน",
    "สัญญา",
    "บริหารสัญญา",
    "บริหารพัสดุ",
    "อุทธรณ์",
    "ร้องเรียน",
    "ราคากลาง",
    "คุณสมบัติ",
    "ผู้ยื่นข้อเสนอ",
    "จ้างที่ปรึกษา",
    "จ้างออกแบบ",
    "ควบคุมงานก่อสร้าง",
    "การประเมินผลการปฏิบัติงานของผู้ประกอบการ",
    "คะแนนความเสียหาย",
    "คะแนนความเสียหายสะสม",
    "การระงับการยื่นข้อเสนอ",
    "การระงับการทำสัญญา",
    "อันตรายสาหัส",
    "ทรัพย์สินเสียหาย",
    "ว 214",
    "คุณสมบัติผู้ยื่นเสนอราคา",
    "คุณสมบัติผู้ยื่นข้อเสนอ",
    "กฎกระทรวงเจาะจง",
    "วงเงินเล็กน้อย",
    "ไม่ทำข้อตกลงเป็นหนังสือ",
    "กรรมการตรวจรับคนเดียว",
    "กฎกระทรวงอุทธรณ์",
    "ว 367",
    "ไม่เข้าข่ายที่จะใช้สิทธิอุทธรณ์",
]

def requested_clause(query: str) -> tuple[str, str] | None:
    match = re.search(rf"(มาตรา|ข้อ|หัวข้อ)\s*({REFERENCE_SECTION_NUMBER_PATTERN})", query)
    if not match:
        return None
    label, number = match.groups()
    return label, normalize_digits(number)


def score_chunk(
    query_tokens: list[str],
    query_phrases: list[str],
    chunk: dict[str, object],
) -> float:
    text = str(chunk.get("search_text", ""))
    text_lower = normalize_search_text(text)
    tokens = tokenize(text)
    if not tokens:
        return 0.0

    token_counts: dict[str, int] = {}
    for token in tokens:
        token_counts[token] = token_counts.get(token, 0) + 1

    score = 0.0
    for token in query_tokens:
        count = token_counts.get(token, 0)
        if count:
            score += 1.0 + math.log(count)

    title = normalize_search_text(str(chunk.get("title", "")))
    heading = normalize_search_text(" ".join(chunk.get("heading_path", [])))
    for token in query_tokens:
        if token in title:
            score += 3.0
        if token in heading:
            score += 1.5
        if len(token) > 3 and token in text_lower:
            score += 2.0

    for phrase in query_phrases:
        if phrase in text_lower:
            score += 12.0 + min(len(phrase), 20)
        if phrase in title:
            score += 8.0
        if phrase in heading:
            score += 6.0

        phrase_grams = character_ngrams(phrase)
        if phrase_grams:
            overlap = sum(gram in text_lower for gram in phrase_grams) / len(phrase_grams)
            if overlap >= 0.45:
                score += overlap * 12.0

    query_joined = " ".join(query_tokens)
    for keyword in DOMAIN_KEYWORDS:
        keyword_lower = normalize_search_text(keyword)
        if keyword_lower in query_joined and keyword_lower in text_lower:
            score += 8.0
            if keyword_lower in title:
                score += 6.0
            if keyword_lower in heading:
                score += 4.0
    if (
        normalize_search_text("อุทธรณ์") in query_joined
        and chunk.get("source") == "reference/law/prb60.md"
        and normalize_digits(str(chunk.get("clause_no", ""))) in {"114", "115", "116", "117", "118", "119"}
    ):
        score += 20.0
    if (
        any(normalize_search_text(keyword) in query_joined for keyword in ["เฉพาะเจาะจง", "เจาะจง"])
        and chunk.get("source") == "reference/law/prb60.md"
        and normalize_digits(str(chunk.get("clause_no", ""))) == "56"
    ):
        score += 20.0
    source = chunk.get("source")
    clause_no = normalize_digits(str(chunk.get("clause_no", "")))
    if source == "reference/law/ministerial-regulations/mr-specific-2560.md":
        if (
            any(normalize_search_text(keyword) in query_joined for keyword in ["เฉพาะเจาะจง", "เจาะจง"])
            and any(normalize_search_text(keyword) in query_joined for keyword in ["กรณีใด", "ใช้ได้", "วงเงิน"])
            and clause_no == "1"
        ):
            score += 20.0
        if normalize_search_text("ไม่ทำข้อตกลงเป็นหนังสือ") in query_joined and clause_no == "4":
            score += 20.0
        if any(normalize_search_text(keyword) in query_joined for keyword in ["กรรมการตรวจรับคนเดียว", "ผู้ตรวจรับพัสดุคนเดียว"]) and clause_no == "5":
            score += 20.0
    if (
        source == "reference/law/ministerial-regulations/mr-appeal-exclusions-2568.md"
        and any(normalize_search_text(keyword) in query_joined for keyword in ["อุทธรณ์ไม่ได้", "กฎกระทรวงอุทธรณ์"])
        and clause_no == "3"
    ):
        score += 20.0
    return score


def lead_in_bonuses(
    candidates: list[dict[str, object]],
    query_phrases: list[str],
) -> dict[object, float]:
    bonuses: dict[object, float] = {}
    for index, chunk in enumerate(candidates[:-1]):
        next_chunk = candidates[index + 1]
        if chunk.get("source") != next_chunk.get("source"):
            continue
        text_lines = str(chunk.get("text", "")).strip().splitlines()
        text_end = normalize_search_text(text_lines[-1]) if text_lines else ""
        if len(text_end) > 80:
            continue
        for phrase in query_phrases:
            common_suffix = 0
            for left, right in zip(reversed(text_end), reversed(phrase)):
                if left != right:
                    break
                common_suffix += 1
            if text_end.endswith(phrase) or common_suffix >= 4:
                next_id = next_chunk.get("id")
                bonuses[next_id] = (
                    bonuses.get(next_id, 0.0)
                    + 80.0
                    + min(common_suffix, 20) * 4.0
                )
    return bonuses


def search_chunks(
    query: str,
    chunks: list[dict[str, object]],
    sources: list[str],
    limit: int,
) -> list[dict[str, object]]:
    selected_sources = set(sources)
    candidates = [chunk for chunk in chunks if chunk.get("source") in selected_sources]
    clause = requested_clause(query)
    if clause:
        label, number = clause
        direct = [
            chunk
            for chunk in candidates
            if chunk.get("clause_type") == label
            and normalize_digits(str(chunk.get("clause_no"))) == number
        ]
        primary_direct = [chunk for chunk in direct if chunk.get("source") == sources[0]]
        if primary_direct:
            return primary_direct[:limit]

    query_tokens = tokenize(query)
    query_phrases = focus_phrases(query)
    lead_in_bonus = lead_in_bonuses(candidates, query_phrases)

    scored = [
        (
            score_chunk(query_tokens, query_phrases, chunk)
            + lead_in_bonus.get(chunk.get("id"), 0.0),
            chunk,
        )
        for chunk in candidates
    ]
    scored.sort(key=lambda item: item[0], reverse=True)
    results = []
    for score, chunk in scored:
        if score <= 0:
            continue
        item = dict(chunk)
        item["score"] = round(score, 3)
        results.append(item)
        if len(results) >= limit:
            break
    return results


def search_routed_sources(
    query: str,
    chunks: list[dict[str, object]],
    sources: list[str],
    limit: int,
) -> list[dict[str, object]]:
    if len(sources) <= 1:
        return search_chunks(query, chunks, sources, limit)

    results: list[dict[str, object]] = []
    seen: set[tuple[object, object]] = set()
    for source in sources:
        source_results = search_chunks(query, chunks, [source], limit)
        if not source_results:
            continue
        item = source_results[0]
        key = (item.get("source"), item.get("id"))
        seen.add(key)
        results.append(item)

    for item in search_chunks(query, chunks, sources, limit):
        key = (item.get("source"), item.get("id"))
        if key in seen:
            continue
        results.append(item)
        seen.add(key)
        if len(results) >= limit:
            break
    return results[:limit]


def retrieve(query: str, limit: int = 5) -> dict[str, object]:
    route = route_query(query)
    chunks = read_json(INDEX_ROOT / "chunks.json")
    assert isinstance(chunks, list)

    results = search_routed_sources(query, chunks, route["sources"], limit)
    used_fallback = False
    has_positive_score = any(float(item.get("score", 1)) > 0 for item in results)
    if (not results or not has_positive_score) and route.get("fallback_sources"):
        fallback_results = search_routed_sources(query, chunks, route["fallback_sources"], limit)
        fallback_positive = any(float(item.get("score", 1)) > 0 for item in fallback_results)
        if fallback_results and fallback_positive:
            results = fallback_results
            used_fallback = True

    route["used_fallback"] = used_fallback
    return {"route": route, "results": results}


def main() -> None:
    parser = argparse.ArgumentParser(description="Retrieve Pasadu law/regulation chunks for a question.")
    parser.add_argument("query", help="User question")
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if not (INDEX_ROOT / "chunks.json").exists():
        raise SystemExit("Index not found. Run: python scripts/pasadu/build_index.py")

    result = retrieve(args.query, limit=args.limit)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    print("Routed authorities:")
    for source in result["route"]["sources"]:
        print(f"- {display_source(source)}")
    if result["route"].get("used_fallback"):
        print("Used fallback authorities:")
        for source in result["route"].get("fallback_sources", []):
            print(f"- {display_source(source)}")
    print("\nResults:")
    for chunk in result["results"]:
        citation = format_citation(chunk["source"], chunk["clause_type"], chunk["clause_no"])
        print(f"- {citation} (score: {chunk.get('score', 'direct')})")
        snippet = str(chunk.get("text", "")).replace("\n", " ")
        print(f"  {snippet[:240]}")


if __name__ == "__main__":
    main()
