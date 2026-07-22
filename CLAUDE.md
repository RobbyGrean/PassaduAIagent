# Pasadu orchestration adapter for Claude Code

For substantive Thai government procurement questions, follow the workflow and safety limits in `AGENTS.md`, translating Codex agent names to the project agents under `.claude/agents/`:

1. Reuse a verified evidence packet for a same-issue follow-up.
2. Otherwise run `python -B scripts/pasadu/evidence_packet.py "<question>" --limit 3` once in the main conversation. Do not call a retriever agent.
3. Draft direct, procedural, and ordinary conditional answers in the main conversation.
4. Call `legal-analyst-complex` at most once, and only for a concrete conflict, ambiguity, multi-provision reconciliation, or difficult fact-to-law chain.
5. If repository retrieval returns `partial` or `not_found` after both primary and configured fallback sources were searched, the root conversation may use web search as an explicit fallback. Do not let any Claude subagent browse the web.
6. A web fallback answer must begin with exactly `คำตอบนี้ใช้ข้อมูลจาก web search ไม่ได้ใช้ฐานข้อมูลของ repository ข้อมูลมีโอกาสคลาดเคลื่อน โปรดตรวจสอบกับแหล่งทางการอีกครั้ง`, separate `Repository source` from `Web source`, and show owner, direct URL, access date when available, verified authority title, exact section/clause/document number, and the label `web source` for every external source.
7. Run `python -B scripts/pasadu/cite_check.py` before the final answer for repository citations. If web sources conflict or the issue affects rights, duties, budgets, contracts, or liability, show the conflict and require verification against the official original and competent authority.

The main conversation owns retrieval and ordinary reasoning. The optional complex specialist inherits the user's selected model with high effort. If the specialist is unavailable, analyze in the main conversation without weakening the guardrails.
