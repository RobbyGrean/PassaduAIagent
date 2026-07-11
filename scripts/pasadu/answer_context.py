from __future__ import annotations

import argparse

from common import REPO_ROOT, read_text
from retrieve import retrieve


COMPACT_RULES = """\
Use the Pasadu workflow without loading full reference files:
- Route the question with scripts/pasadu/route_query.py policy.
- Use only the retrieved references below as legal basis for the answer.
- Do not answer from memory alone.
- Do not invent law, clause numbers, circulars, or official rulings.
- Cite each legal basis as source + clause type + clause number.
- If retrieved references do not answer the question, say the answer was not found in the available project references.
- If facts are missing, ask concise follow-up questions before diagnosing.
- Keep the answer practical, in Thai, and separate summary, legal basis, reasoning, and cautions when useful.
- Treat Act and Regulation text as legal authority; label ministerial regulations and circular guidance separately.
- Do not use a circular as a substitute for its supporting Act, Regulation, or ministerial regulation.
- For web questions, use only official sources and label them as outside the project reference set.
"""


def load_rules(full_rules: bool) -> str:
    if full_rules:
        return read_text(REPO_ROOT / "pasadu.md").strip()
    return COMPACT_RULES.strip()


def build_context(query: str, limit: int = 5, full_rules: bool = False) -> str:
    rules = load_rules(full_rules)
    retrieved = retrieve(query, limit=limit)
    lines = [
        "# Pasadu Answer Context",
        "",
        "## Compact Rules" if not full_rules else "## Full Rules",
        rules,
        "",
        "## Route",
        f"sources: {', '.join(retrieved['route'].get('sources', []))}",
        f"fallback_sources: {', '.join(retrieved['route'].get('fallback_sources', []))}",
        f"used_fallback: {retrieved['route'].get('used_fallback', False)}",
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
    parser.add_argument(
        "--full-rules",
        action="store_true",
        help="Include the full pasadu.md rules instead of compact rules.",
    )
    args = parser.parse_args()
    print(build_context(args.query, limit=args.limit, full_rules=args.full_rules))


if __name__ == "__main__":
    main()
