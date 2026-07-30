# Pasadu repository workflow

These instructions apply only to substantive questions about Thai government procurement or explicit requests to run the Pasadu legal workflow. Repository development tasks do not invoke the legal workflow.

## Legal workflow

1. Reuse a prior verified evidence packet for a same-issue follow-up when it already contains the controlling provision.
2. Otherwise run one deterministic repository pass:
   `python -B skills/pasadu/scripts/pasadu/evidence_packet.py "<complete question>" --limit 3`
3. If the packet returns `needs_scope_check`, ask its scope questions and stop.
4. Analyze direct, procedural, conditional, and complex questions in the current conversation from the bounded evidence packet. This standalone skill does not require custom subagents.
5. If evidence is insufficient, run at most one targeted deterministic retry. Ask the user when facts are missing.
6. Use web search only after repository primary and fallback retrieval is complete and the result is `partial` or `not_found`.
7. Before answering, verify repository citations with:
   `python -B skills/pasadu/scripts/pasadu/cite_check.py`
8. Follow the formats and guardrails in `skills/pasadu/SKILL.md` and `skills/pasadu/pasadu.md`.

## Web fallback contract

Every answer using web search must begin with:

`คำตอบนี้ใช้ข้อมูลจาก web search ไม่ได้ใช้ฐานข้อมูลของ repository ข้อมูลมีโอกาสคลาดเคลื่อน โปรดตรวจสอบกับแหล่งทางการอีกครั้ง`

Separate `Repository source` from `Web source`. For every web source, show its owner, direct URL, access date when available, verified authority title, and exact section, clause, heading, or document number. Never invent legal authority or citation metadata.

## Development boundaries

- Do not modify legal references, index data, evals, or retrieval behavior while merely answering a legal question.
- Keep the legal workflow read-only.
- Do not expose internal filenames as final user-facing citations.
- For consequential questions, advise verification against the official original and competent authority.
