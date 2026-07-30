from __future__ import annotations

import argparse

from common import REPO_ROOT, display_source, format_citation, read_text
from evidence_packet import build_evidence_packet


COMPACT_RULES = """\
Use the Pasadu workflow without loading full reference files:
- Route the question with scripts/pasadu/route_query.py policy.
- Use only the retrieved references below as legal basis for the answer.
- Do not answer from memory alone.
- Do not invent law, clause numbers, circulars, or official rulings.
- Cite each legal basis as the human-readable legal authority name + clause type + clause number.
- Never expose repository filenames in the answer. Those paths are internal retrieval metadata only.
- If retrieved references do not answer the question, say the answer was not found in the available project references.
- If facts are missing, ask concise follow-up questions before diagnosing.
- Keep the answer practical, in Thai, and separate summary, legal basis, reasoning, and cautions when useful.
- Treat Act and Regulation text as legal authority; label ministerial regulations and circular guidance separately.
- Apply the authority hierarchy: the Act supplies the legal power and scope, the Regulation supplies operating steps, ministerial regulations supply subordinate rules, and circulars are supporting guidance. If sources differ, explain the relationship and do not let a lower-level source silently override a higher-level one.
- Do not use a circular as a substitute for its supporting Act, Regulation, or ministerial regulation.
- Web search is an explicit root-orchestrator fallback only after primary and configured fallback repository sources were searched and evidence is partial or not found. Do not use web search to fill missing facts.
- If web fallback is used, start with exactly: คำตอบนี้ใช้ข้อมูลจาก web search ไม่ได้ใช้ฐานข้อมูลของ repository ข้อมูลมีโอกาสคลาดเคลื่อน โปรดตรวจสอบกับแหล่งทางการอีกครั้ง
- Separate `Repository source` and `Web source`. For each web source show its owner, direct URL, access date when available, verified authority title, exact provision/document number, and the label `web source`; never invent unverified metadata. Show conflicts and advise official verification for consequential issues.
"""


def load_rules(full_rules: bool) -> str:
    if full_rules:
        return read_text(REPO_ROOT / "pasadu.md").strip()
    return COMPACT_RULES.strip()


def build_context(query: str, limit: int = 3, full_rules: bool = False) -> str:
    rules = load_rules(full_rules)
    packet = build_evidence_packet(query, limit=limit)
    retrieved = {"route": packet["route"], "results": packet["evidence"]}
    lines = [
        "# Pasadu Answer Context",
        "",
        "## Compact Rules" if not full_rules else "## Full Rules",
        rules,
        "",
        "## Route",
        f"authorities: {', '.join(display_source(source) for source in retrieved['route'].get('sources', []))}",
        f"fallback_authorities: {', '.join(display_source(source) for source in retrieved['route'].get('fallback_sources', []))}",
        f"used_fallback: {retrieved['route'].get('used_fallback', False)}",
        f"checked_authorities: {', '.join(display_source(source) for source in packet['repository_check']['checked_sources'])}",
        "",
        "## User Question",
        query,
        "",
        "## Retrieved References",
    ]
    for chunk in retrieved["results"]:
        citation = format_citation(chunk["source"], chunk["clause_type"], chunk["clause_no"])
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
            "ใช้ Retrieved References ข้างต้นเป็นฐานของส่วน Repository source เท่านั้น หากไม่พบตัวบทที่ตอบคำถาม ให้ root orchestrator พิจารณา web fallback ตามกติกา โดยต้องใส่ disclaimer และแสดง Web source แยกต่างหาก",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the context block for an LLM answer.")
    parser.add_argument("query", help="User question")
    parser.add_argument("--limit", type=int, default=3)
    parser.add_argument(
        "--full-rules",
        action="store_true",
        help="Include the full pasadu.md rules instead of compact rules.",
    )
    args = parser.parse_args()
    print(build_context(args.query, limit=args.limit, full_rules=args.full_rules))


if __name__ == "__main__":
    main()
