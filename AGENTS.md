# Pasadu Phase 1 orchestration

These instructions apply only when the user asks a substantive question about Thai government procurement or explicitly asks to run the Pasadu legal workflow. Ordinary repository development tasks do not require the legal agents.

## Workflow

1. Send the complete user question to `legal_retriever`.
2. If it returns `needs_scope_check`, ask its required questions and stop. If it returns `not_found`, report that the current repository does not contain enough supporting law.
3. Choose the least expensive sufficient reasoning path:
   - For direct retrieval, explanation, summarization, or mechanically stated procedure, the Luna root orchestrator drafts from the evidence packet without an analyst.
   - For ordinary application of law to facts or conditional legal reasoning, send the complete evidence packet and original question to `legal_analyst` (Sol low/Light).
   - Use `legal_analyst_complex` (Sol medium) only for material conflicts between authorities, unresolved ambiguity, multi-provision reconciliation, or a difficult fact-to-law chain.
4. Never send the same question to both analysts routinely. Escalate from `legal_analyst` to `legal_analyst_complex` only when the ordinary analyst identifies a concrete complexity reason.
5. If an analyst returns `insufficient_facts` or `insufficient_evidence`, ask for the missing information or run one targeted retrieval pass.
6. Before answering the user, run `python -B scripts/pasadu/cite_check.py` against the drafted answer. Remove or correct every citation that fails.
7. Produce the final answer using the formats and guardrails in `SKILL.md` and `pasadu.md`.

## Phase 1 limits

- The legal workflow is read-only.
- Use only repository references; do not add web retrieval.
- Do not delegate to a citation-verifier or answer-editor agent; those roles are deferred to Phase 2.
- Do not modify law, index, evaluation, or retrieval files while answering a legal question.
- Keep agent nesting at one level: only the root orchestrator spawns legal agents.
- Luna low/Light is the default core. Sol is reserved for analysis, and Sol medium is reserved for demonstrably complex analysis.
- At most one targeted retrieval retry is allowed. If evidence remains insufficient, fail safely instead of guessing.
