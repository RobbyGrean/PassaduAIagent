# Pasadu Phase 1 orchestration

These instructions apply only when the user asks a substantive question about Thai government procurement or explicitly asks to run the Pasadu legal workflow. Ordinary repository development tasks do not require the legal agents.

## Workflow

1. Send the complete user question to `legal_retriever`.
2. Require `legal_retriever` to route and search the repository's primary source and every configured fallback source before returning `found`, `partial`, or `not_found`. If it returns `needs_scope_check`, ask its required questions and stop; missing facts are not a reason to browse the web.
3. Choose the least expensive sufficient reasoning path:
   - For direct retrieval, explanation, summarization, or mechanically stated procedure, the inherited root orchestrator drafts from the evidence packet without an analyst.
   - For ordinary application of law to facts or conditional legal reasoning, send the complete evidence packet and original question to `legal_analyst` (Luna high).
   - Use `legal_analyst_complex` (Luna high with a complex-analysis contract) only for material conflicts between authorities, unresolved ambiguity, multi-provision reconciliation, or a difficult fact-to-law chain.
4. Never send the same question to both analysts routinely. Escalate from `legal_analyst` to `legal_analyst_complex` only when the ordinary analyst identifies a concrete complexity reason.
5. If an analyst returns `insufficient_facts`, ask for the missing information and stop. If the analyst returns `insufficient_evidence`, run at most one targeted repository retrieval retry before considering web fallback.
6. Enter web search fallback only when all of these are true: repository routing was completed; the primary and configured fallback sources were searched; the evidence is `partial` or `not_found` for the requested point; and no unresolved fact question requires the user first. Web search must never replace or skip repository retrieval.
7. The inherited root orchestrator, not `legal_retriever` or either analyst, performs the web search. Prefer government or official owner websites and then reliable legal sources only when an official source cannot be found. Do not use remembered law or an unverified result.
8. If repository evidence answers only part of the question, label the answer sections separately as `Repository source` and `Web source`; never merge their citations or imply that a web source came from the repository. If the repository fully answers the question, do not add web material merely because web search is available.
9. Every answer that uses web search must start with this exact disclaimer, before any other content:

   `คำตอบนี้ใช้ข้อมูลจาก web search ไม่ได้ใช้ฐานข้อมูลของ repository ข้อมูลมีโอกาสคลาดเคลื่อน โปรดตรวจสอบกับแหล่งทางการอีกครั้ง`

   For every web source, show the site or owning agency, direct URL, access date when available, verified law/regulation/circular/announcement title, and the verified section, clause, heading, or document number. Mark it explicitly as `web source`. Never invent a title, clause, document number, or URL; if it cannot be verified, say so and do not use it as confirmed legal support. If web sources conflict, show both sources and explain the conflict.
10. Before answering the user, run `python -B scripts/pasadu/cite_check.py` against the repository citations in the drafted answer. Remove or correct every failing repository citation. For web-only answers, the checker may report that no repository citation was found; this is not permission to omit the web-source metadata and exact disclaimer.
11. Produce the final answer using the formats and guardrails in `SKILL.md` and `pasadu.md`. For questions affecting rights, duties, budgets, contracts, or liability, warn the user to verify the official original and the competent authority.

Citation presentation rule: internal repository paths may be used in evidence packets and by `cite_check.py`, but the final user-facing answer must translate each path into the human-readable Act, Regulation, ministerial regulation, or circular name and cite the exact section, clause, or heading number. Never expose filenames such as `prb60.md` or `rbb60.md` as the citation.

## Web fallback output contract

When web fallback is used, keep the following structure after the mandatory disclaimer:

- `Repository source`: the repository-supported portion, or `ไม่พบหลักฐานเพียงพอจาก repository` when none was found.
- `Web source`: each externally retrieved source with owner, title, exact provision/document number, direct URL, access date when available, and the literal label `web source`.
- `คำตอบ/ข้อจำกัด`: separate synthesis, conflicts, unverifiable items, and the warning to verify with the official original and competent authority when the issue is consequential.

The final user-facing answer must use human-readable legal authority names and exact sections or clauses. Internal repository paths remain allowed only in evidence packets and citation checking.

## Phase 1 limits

- The legal workflow is read-only.
- Repository references remain the first and preferred evidence set. Web retrieval is an explicitly labeled, read-only fallback under the conditions above; it does not expand or modify repository law, index, evaluation, or citation data.
- Do not delegate to a citation-verifier or answer-editor agent; those roles are deferred to Phase 2.
- Do not modify law, index, evaluation, or retrieval files while answering a legal question.
- Keep agent nesting at one level: only the root orchestrator spawns legal agents.
- The Codex root/input session inherits the user's selected model and reasoning effort. Every legal subagent uses Luna high for retrieval, legal analysis, citation support, and interpretation.
- At most one targeted retrieval retry is allowed. If evidence remains insufficient, fail safely instead of guessing.
