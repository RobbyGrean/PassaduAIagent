# Pasadu orchestration adapter for Gemini CLI

For substantive Thai government procurement questions, follow the workflow and safety limits in `AGENTS.md`, translating Codex agent names to the project agents under `.gemini/agents/`:

1. Call `legal-retriever` first.
2. Draft direct retrieval or summary answers in the main conversation.
3. Call `legal-analyst` for ordinary legal application or interpretation.
4. Call `legal-analyst-complex` only for a concrete conflict, ambiguity, multi-provision reconciliation, or difficult fact-to-law chain.
5. Run `python -B scripts/pasadu/cite_check.py` before the final answer.

Gemini agents inherit the user's selected model. Gemini's agent schema does not use the Codex/Claude effort field, so the analyst prompts require careful reasoning explicitly. If subagents are unavailable, execute the same sequence in the main conversation without weakening the guardrails.
