from __future__ import annotations

import argparse
import json
import math
import re

from common import INDEX_ROOT, normalize_digits, read_json, tokenize
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
]


def requested_clause(query: str) -> tuple[str, str] | None:
    match = re.search(r"(มาตรา|ข้อ)\s*([0-9๐-๙]+(?:/[0-9๐-๙]+)?)", query)
    if not match:
        return None
    label, number = match.groups()
    return label, normalize_digits(number)


def score_chunk(query_tokens: list[str], chunk: dict[str, object]) -> float:
    text = str(chunk.get("search_text", ""))
    text_lower = text.lower()
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

    title = str(chunk.get("title", "")).lower()
    heading = " ".join(chunk.get("heading_path", [])).lower()
    for token in query_tokens:
        if token in title:
            score += 3.0
        if token in heading:
            score += 1.5
        if len(token) > 3 and token in text_lower:
            score += 2.0

    query_joined = " ".join(query_tokens)
    for keyword in DOMAIN_KEYWORDS:
        keyword_lower = keyword.lower()
        if keyword_lower in query_joined and keyword_lower in text_lower:
            score += 8.0
            if keyword_lower in title:
                score += 6.0
            if keyword_lower in heading:
                score += 4.0
    return score


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
        if direct:
            return direct[:limit]

    query_tokens = tokenize(query)
    scored = [
        (score_chunk(query_tokens, chunk), chunk)
        for chunk in candidates
    ]
    scored.sort(key=lambda item: item[0], reverse=True)
    results = []
    for score, chunk in scored:
        if score <= 0 and results:
            continue
        item = dict(chunk)
        item["score"] = round(score, 3)
        results.append(item)
        if len(results) >= limit:
            break
    return results


def retrieve(query: str, limit: int = 5) -> dict[str, object]:
    route = route_query(query)
    chunks = read_json(INDEX_ROOT / "chunks.json")
    assert isinstance(chunks, list)

    results = search_chunks(query, chunks, route["sources"], limit)
    used_fallback = False
    has_positive_score = any(float(item.get("score", 1)) > 0 for item in results)
    if (not results or not has_positive_score) and route.get("fallback_sources"):
        fallback_results = search_chunks(query, chunks, route["fallback_sources"], limit)
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

    print("Routed sources:")
    for source in result["route"]["sources"]:
        print(f"- {source}")
    if result["route"].get("used_fallback"):
        print("Used fallback sources:")
        for source in result["route"].get("fallback_sources", []):
            print(f"- {source}")
    print("\nResults:")
    for chunk in result["results"]:
        citation = f"{chunk['source']} {chunk['clause_type']} {chunk['clause_no']}"
        print(f"- {citation} (score: {chunk.get('score', 'direct')})")
        snippet = str(chunk.get("text", "")).replace("\n", " ")
        print(f"  {snippet[:240]}")


if __name__ == "__main__":
    main()
