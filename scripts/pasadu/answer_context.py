from __future__ import annotations

import argparse

from common import REPO_ROOT, read_text
from retrieve import retrieve


def build_context(query: str, limit: int = 5) -> str:
    rules = read_text(REPO_ROOT / "pasadu.md").strip()
    retrieved = retrieve(query, limit=limit)
    lines = [
        "# Pasadu Answer Context",
        "",
        "## Rules",
        rules,
        "",
        "## User Question",
        query,
        "",
        "## Retrieved References",
    ]
    for chunk in retrieved["results"]:
        citation = f"{chunk['source']} {chunk['clause_type']} {chunk['clause_no']}"
        lines.extend(
            [
                "",
                f"### {citation}",
                f"heading_path: {' > '.join(chunk.get('heading_path', []))}",
                "",
                str(chunk.get("text", "")).strip(),
            ]
        )
    lines.extend(
        [
            "",
            "## Output Guardrail",
            "ตอบโดยใช้เฉพาะ Retrieved References ข้างต้น ถ้าไม่พบตัวบทที่ตอบคำถาม ให้ตอบว่าไม่พบในไฟล์อ้างอิงที่มี",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the context block for an LLM answer.")
    parser.add_argument("query", help="User question")
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()
    print(build_context(args.query, limit=args.limit))


if __name__ == "__main__":
    main()
