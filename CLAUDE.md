# Pasadu orchestration adapter for Claude Code

For substantive Thai government procurement questions, follow the workflow and safety limits in `AGENTS.md`, translating Codex agent names to the project agents under `.claude/agents/`:

1. Call `legal-retriever` first.
2. Draft direct retrieval or summary answers in the main conversation.
3. Call `legal-analyst` for ordinary legal application or interpretation.
4. Call `legal-analyst-complex` only for a concrete conflict, ambiguity, multi-provision reconciliation, or difficult fact-to-law chain.
5. Run `python -B scripts/pasadu/cite_check.py` before the final answer.

All Claude agents inherit the user's selected model. Retrieval uses low effort; legal analysis, citation support, and interpretation use high effort. If subagents are unavailable, execute the same sequence in the main conversation without weakening the guardrails.
