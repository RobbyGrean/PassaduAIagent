from __future__ import annotations

import argparse
import json

from retrieve import retrieve


CASES = [
    {
        "query": "วิธีเฉพาะเจาะจงใช้กรณีใด",
        "expected_source": "reference/law/rbb60.md",
    },
    {
        "query": "มาตรา 56 กล่าวถึงอะไร",
        "expected_source": "reference/law/prb60.md",
    },
    {
        "query": "คณะกรรมการตรวจรับพัสดุต้องดูจากข้อไหน",
        "expected_source": "reference/law/rbb60.md",
    },
    {
        "query": "การอุทธรณ์อยู่ใน พรบ มาตราใด",
        "expected_source": "reference/law/prb60.md",
    },
    {
        "query": "การแก้ไขสัญญาต้องเริ่มดูจากไหน",
        "expected_source": "reference/law/prb60.md",
    },
    {
        "query": "สัญญาต้องทำตามระเบียบข้อใด",
        "expected_source": "reference/law/rbb60.md",
    },
]


def run_eval() -> dict[str, object]:
    results = []
    for case in CASES:
        output = retrieve(case["query"], limit=5)
        sources = set(output["route"]["sources"])
        found_sources = {item["source"] for item in output["results"]}
        ok = case["expected_source"] in sources and case["expected_source"] in found_sources
        results.append(
            {
                "query": case["query"],
                "expected_source": case["expected_source"],
                "routed_sources": output["route"]["sources"],
                "top_citations": [
                    f"{item['source']} {item['clause_type']} {item['clause_no']}"
                    for item in output["results"][:3]
                ],
                "ok": ok,
            }
        )
    return {
        "ok": all(item["ok"] for item in results),
        "results": results,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run smoke evals for Pasadu retrieval.")
    parser.parse_args()
    result = run_eval()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
