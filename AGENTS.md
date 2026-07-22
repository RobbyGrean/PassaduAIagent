# Pasadu Phase 1 orchestration

These instructions apply only when the user asks a substantive question about Thai government procurement or explicitly asks to run the Pasadu legal workflow. Ordinary repository development tasks do not require the legal agents.

## Workflow

1. For a follow-up on the same issue, reuse the prior verified evidence packet when it already contains the controlling provision. Do not route or retrieve the same evidence again.
2. Otherwise, the inherited root session runs one deterministic repository pass:
   `python -B scripts/pasadu/evidence_packet.py "<complete question>" --limit 3`
   This command routes once, checks the primary and every configured fallback source in one process, and returns bounded evidence. Do not call a retriever subagent.
3. If the packet returns `needs_scope_check`, ask its scope questions and stop. Missing facts are not a reason to browse the web.
4. The inherited root session answers direct retrieval, explanation, summarization, mechanically stated procedure, and ordinary conditional application from the verified evidence packet. Do not call an ordinary analyst subagent.
5. Use `legal_analyst_complex` only for a material conflict between authorities, unresolved ambiguity, multi-provision reconciliation, or a genuinely difficult fact-to-law chain. Send only the original question, the bounded evidence packet, and the concrete complexity reason. Never call more than one legal specialist for one answer.
6. If evidence is insufficient, run at most one targeted deterministic repository retry before considering web fallback. If facts are insufficient, ask the user and stop.
7. Enter web search fallback only when all of these are true: repository routing was completed; the primary and configured fallback sources were searched; the evidence is `partial` or `not_found` for the requested point; and no unresolved fact question requires the user first. Web search must never replace or skip repository retrieval.
8. The inherited root session, not a specialist, performs the web search. Prefer government or official owner websites and then reliable legal sources only when an official source cannot be found. Do not use remembered law or an unverified result.
9. If repository evidence answers only part of the question, label the answer sections separately as `Repository source` and `Web source`; never merge their citations or imply that a web source came from the repository. If the repository fully answers the question, do not add web material merely because web search is available.
10. Every answer that uses web search must start with this exact disclaimer, before any other content:

   `คำตอบนี้ใช้ข้อมูลจาก web search ไม่ได้ใช้ฐานข้อมูลของ repository ข้อมูลมีโอกาสคลาดเคลื่อน โปรดตรวจสอบกับแหล่งทางการอีกครั้ง`

   For every web source, show the site or owning agency, direct URL, access date when available, verified law/regulation/circular/announcement title, and the verified section, clause, heading, or document number. Mark it explicitly as `web source`. Never invent a title, clause, document number, or URL; if it cannot be verified, say so and do not use it as confirmed legal support. If web sources conflict, show both sources and explain the conflict.
11. Before answering the user, run `python -B scripts/pasadu/cite_check.py` against the repository citations in the drafted answer. Remove or correct every failing repository citation. For web-only answers, the checker may report that no repository citation was found; this is not permission to omit the web-source metadata and exact disclaimer.
12. Produce the final answer using the formats and guardrails in `SKILL.md` and `pasadu.md`. For questions affecting rights, duties, budgets, contracts, or liability, warn the user to verify the official original and the competent authority.

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
- Do not delegate routine retrieval, ordinary analysis, citation verification, or answer editing. These stay in the root session.
- Do not modify law, index, evaluation, or retrieval files while answering a legal question.
- Keep agent nesting at one level. At most one `legal_analyst_complex` specialist may be used when the complexity gate is met.
- The Codex root/input session inherits the user's selected model and reasoning effort. The optional complex specialist uses Luna high.
- At most one targeted retrieval retry is allowed. If evidence remains insufficient, fail safely instead of guessing.
