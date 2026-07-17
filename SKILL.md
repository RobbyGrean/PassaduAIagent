---
name: pasadu
description: Automatically use for questions that concern or may depend on Thai government procurement and public supplies law, including Acts, Regulations, ministerial regulations, and circular guidance in this repository. Also use when the user explicitly types /pasadu or /passadu. Load pasadu.md, route to the most specific reference, retrieve exact provisions, and answer with verified citations.
---

# Pasadu Skill

## Activation

Activate this skill automatically when the user's question concerns, appears connected to, or may require interpretation of Thai government procurement and public supplies law. The user does not need to name the skill.

Manual aliases are also valid triggers:

- `/pasadu`
- `/passadu`

Treat either alias followed by text as an explicit request to use this skill. Do not require the alias when the intent already matches the skill description.

Do not activate only because a prompt contains the generic word `กฎหมาย` or `สัญญา` when the context is clearly unrelated to Thai government procurement.

## Purpose

Use this skill to answer, explain, and diagnose questions about Thai government procurement and public supplies administration using the project's reference law files.

## Repository

The directory containing this `SKILL.md` is the source of truth for the skill.

Resolve every relative path below from that directory. Do not assume a specific Windows username, home directory, clone location, or operating system.

## Required Context

Before answering a procurement-law question, read:

`pasadu.md`

Use the law reference files only as needed:

- `reference/law/prb60.md` for พระราชบัญญัติการจัดซื้อจัดจ้างและการบริหารพัสดุภาครัฐ พ.ศ. 2560
- `reference/law/rbb60.md` for ระเบียบกระทรวงการคลังว่าด้วยการจัดซื้อจัดจ้างและการบริหารพัสดุภาครัฐ พ.ศ. 2560
- `reference/law/rbb60-3.md` for ระเบียบกระทรวงการคลังว่าด้วยการจัดซื้อจัดจ้างและการบริหารพัสดุภาครัฐ (ฉบับที่ 3) พ.ศ. 2569 โดยเฉพาะหมวด 7 ข้อ 190-191 เรื่องการประเมินผลการปฏิบัติงานของผู้ประกอบการงานก่อสร้าง คะแนนความเสียหาย และการระงับการยื่นข้อเสนอหรือทำสัญญา
- `reference/law/ministerial-regulations/mr-specific-2560.md` for กฎกระทรวงเฉพาะเจาะจงและวงเงินเล็กน้อย
- `reference/law/ministerial-regulations/mr-appeal-exclusions-2568.md` for กฎกระทรวงอุทธรณ์และเรื่องที่อุทธรณ์ไม่ได้
- `reference/circulars/circular-w367-2567.md` for ว 367 และกรณีไม่เข้าข่ายใช้สิทธิอุทธรณ์ตามมาตรา 114
- `reference/circulars/circular-w214-2563.md` for ว 214 และการกำหนดคุณสมบัติผู้ยื่นเสนอราคา

## Retrieval Scripts

When available, use the repository scripts to avoid reading entire reference files for one question:

- `scripts/pasadu/build_index.py` builds `data/index/*.json` from every registered reference source.
- `scripts/pasadu/route_query.py` decides the primary source and fallback source.
- `scripts/pasadu/retrieve.py` returns the most relevant clauses with internal source metadata and clause citations; user-facing answers must translate the source into the legal authority's name.
- `scripts/pasadu/answer_context.py` builds an LLM-ready context from `pasadu.md`, the user question, and retrieved references.
- `scripts/pasadu/cite_check.py` checks whether final citations exist in the index.

If the index is missing or stale, run `build_index.py` first. If scripts cannot run, fall back to manual search in the same routing order and still verify every citation against the reference files.

## Routing

Default policy:

- Route `ว 214` or questions about `การกำหนดคุณสมบัติผู้ยื่นเสนอราคา` to `reference/circulars/circular-w214-2563.md` first.
- Route every `เจาะจง` or `เฉพาะเจาะจง` question in authority order: `prb60.md` section 56, `mr-specific-2560.md`, then `rbb60.md`. Use the same chain for `วงเงินเล็กน้อย`, `ไม่ทำข้อตกลงเป็นหนังสือ`, or `กรรมการ/ผู้ตรวจรับคนเดียว`.
- Route general appeal questions to `prb60.md` sections 114-119 together with the appeal ministerial regulation and Circular W367.
- Route `เรื่องที่อุทธรณ์ไม่ได้` or `กฎกระทรวงอุทธรณ์` to the appeal ministerial regulation plus `prb60.md`.
- Route `ไม่เข้าข่ายที่จะใช้สิทธิอุทธรณ์ตามมาตรา 114` or `ว 367` to Circular W367 plus `prb60.md`.

- For general operational questions, search `reference/law/rbb60.md` first because day-to-day procurement practice follows the Regulation, then use `reference/law/prb60.md` as fallback or supporting authority.
- If the user explicitly asks for `มาตรา`, `พรบ.`, `พ.ร.บ.`, or `พระราชบัญญัติ`, search `reference/law/prb60.md` first, then fallback to `reference/law/rbb60.md` if not found.
- If the user explicitly asks for `ข้อ` or `ระเบียบ`, search the most specific Regulation file first. Use `reference/law/rbb60-3.md` when the question points to issue 3, ข้อ 190-191, contractor performance evaluation, damage scores, or suspension; otherwise use `reference/law/rbb60.md` first. Fall back to the other Regulation file and then to `reference/law/prb60.md` when needed.
- For contract administration issues such as บริหารสัญญา, บอกเลิกสัญญา, ตกลงยกเลิกสัญญา, แก้ไขสัญญา, เปลี่ยนแปลงสัญญา, งดหรือลดค่าปรับ, or ขยายเวลาทำการ, search `reference/law/prb60.md` first, unless the user explicitly asks for a Regulation clause.
- Do not route to `reference/law/rbb60-3.md` only because the query mentions `งานก่อสร้าง`. If the user asks a general construction procurement question, follow the normal `rbb60.md`/`prb60.md` policy first. If the answer depends on whether the project is in scope for issue 3 and the facts are missing, ask the three scope-gate questions before citing `rbb60-3.md`.
- When the scope is unknown, return `needs_scope_check = true`, use `reference/law/rbb60.md` as the source and `reference/law/prb60.md` as fallback, then ask exactly:
  1. งานก่อสร้างนี้มูลค่า 5 ล้านบาทขึ้นไป และเป็นของ 6 หน่วยงานหลักหรือไม่?
  2. งานนี้เป็นอาคารสูง อาคารขนาดใหญ่พิเศษ หรืออาคารชุมนุมคนหรือไม่?
  3. งานก่อสร้างนี้มีมูลค่าตั้งแต่ 1,000 ล้านบาทขึ้นไปหรือไม่?
- A direct question about issue 3, ข้อ 190, ข้อ 190/1-190/9, ข้อ 191, damage scores, suspension, อันตรายสาหัส, or ทรัพย์สินเสียหาย bypasses the scope gate and routes directly to `reference/law/rbb60-3.md`.

Use `reference/law/prb60.md` when the question concerns:

- พรบ., พ.ร.บ., พระราชบัญญัติ
- มาตรา
- legal authority under the Act
- principles, committees, appeals, complaints, or penalties under the Act

Use `reference/law/rbb60.md` when the question concerns:

- ระเบียบ or ข้อ
- procurement methods or operational steps
- e-market, e-bidding, selection, specific method
- contracts, guarantees, inspection, acceptance, contract administration, or supplies administration
- consulting work or design/construction supervision work

Use `reference/law/rbb60-3.md` when the question concerns:

- ระเบียบกระทรวงการคลังฯ (ฉบับที่ 3) พ.ศ. 2569, ระเบียบฉบับที่ 3, หรือ rbb60-3
- ข้อ 190, ข้อ 190/1 ถึง 190/9, หรือ ข้อ 191
- คะแนนความเสียหาย, คะแนนความเสียหายสะสม, การระงับการยื่นข้อเสนอ, การระงับการทำสัญญา, หรือระยะเวลาแบน
- อันตรายสาหัส, ทรัพย์สินเสียหาย, ประมาทเลินเล่อในงานก่อสร้าง, มาตรฐานหลักวิชาช่าง, หรือความชำรุดบกพร่อง ในบริบทการตัดคะแนนผู้ประกอบการ
- โครงการก่อสร้างที่เข้าข่ายตามระเบียบฉบับที่ 3 เช่น งานก่อสร้าง 5 ล้านบาทขึ้นไปของ 6 หน่วยงานหลัก อาคารสูง อาคารขนาดใหญ่พิเศษ อาคารชุมนุมคน หรืองานก่อสร้าง 1,000 ล้านบาทขึ้นไป

Use both files when the question needs both the Act's authority and the Regulation's operating details. For issue 3 questions, use `rbb60-3.md` for the amended rule and cite `rbb60.md` only when background from the base Regulation is needed.

## Answer Workflow

1. Classify the issue.
2. Decide whether the user needs a short text-only answer or a practical diagnosis.
3. For complex questions, ask first whether the user wants:
   - ตอบตามตัวบทเท่านั้น
   - ตอบเชิงปฏิบัติโดยอ้างคู่มือ/แนววินิจฉัยประกอบ
4. Search the primary reference source using the routing policy.
5. Search every configured fallback source before deciding that the repository lacks evidence.
6. Identify the exact section or clause.
7. Answer from the repository evidence when it fully answers the question.
8. If the repository result is `partial` or `not_found` after primary and fallback retrieval, and no missing-fact question must be answered first, the root orchestrator may enter the web search fallback described below.
9. Ask concise clarification questions if facts are missing; do not use web search to fill missing facts.
10. State uncertainty when the reference does not fully answer the question.

For direct questions such as "มาตรา 56 คืออะไร", "ข้อ 78 ว่าอย่างไร", or "ข้อ 190/3 ประเมินอะไร", do not ask the mode question first; retrieve and answer directly.

## Hard Rules

- Do not invent law.
- Do not cite a section or clause that was not found.
- Do not silently rely on outside legal sources. Web search is allowed only as the explicit fallback after repository routing, primary retrieval, and configured fallback retrieval are complete.
- `legal_retriever`, `legal_analyst`, and `legal_analyst_complex` must never browse the web. Only the inherited root orchestrator may run the fallback search.
- If the repository supports only part of an answer, separate `Repository source` and `Web source` sections and keep citations visibly distinct.
- Every answer using web search must begin with exactly: `คำตอบนี้ใช้ข้อมูลจาก web search ไม่ได้ใช้ฐานข้อมูลของ repository ข้อมูลมีโอกาสคลาดเคลื่อน โปรดตรวจสอบกับแหล่งทางการอีกครั้ง`
- For each web source, show the owning website or agency, direct URL, access date when available, the verified title of the Act, Regulation, ministerial regulation, circular, or announcement, and the verified section, clause, heading, or document number. Label it `web source`.
- Prefer government gazettes and official agency websites. Do not invent or infer an unverified title, clause, document number, or URL; if it cannot be verified, say that it cannot be confirmed.
- If web sources conflict, present both sources and the conflict. For issues affecting rights, duties, budgets, contracts, or liability, tell the user to verify the official original and the competent authority.
- Do not change quoted statutory or regulatory text.
- If the answer is not found in the available references, say so plainly.
- Do not treat manuals, circulars, rulings, FAQ, examples, or checklists as higher authority than the Act or Regulation. When those references are added later, label them as supporting practical guidance unless the user asks otherwise.
- Distinguish a non-appealable issue under section 115/the appeal ministerial regulation from a person or situation that does not qualify to exercise appeal rights under section 114 as described in Circular W367 item 2.
- When references conflict, explain the conflict and prioritize the Regulation for operational steps, except contract administration issues where the Act must be checked first under this skill's routing policy.
- Treat summaries inside `rbb60-3.md` as supporting explanation only. For legal answers, cite the regulation clauses or annex tables, not the summary section alone.
- In user-facing answers, cite the legal authority by its human-readable name, followed by `มาตรา`, `ข้อ`, or `หัวข้อ` and the exact number. For example: `พระราชบัญญัติการจัดซื้อจัดจ้างและการบริหารพัสดุภาครัฐ พ.ศ. 2560 มาตรา 56`, `ระเบียบกระทรวงการคลังว่าด้วยการจัดซื้อจัดจ้างและการบริหารพัสดุภาครัฐ พ.ศ. 2560 ข้อ 78`, or `หนังสือเวียน ว 214 ลงวันที่ 18 พฤษภาคม 2563 หัวข้อ 1.1.2`.
- Never expose internal repository filenames such as `prb60.md`, `rbb60.md`, or `rbb60-3.md` as the citation in the final answer. The paths remain internal metadata for retrieval and citation validation.

## Preferred Output

For most answers, use this shape:

```text
คำตอบสั้น:
...

อ้างอิง:
- ชื่อพระราชบัญญัติ/ระเบียบ/กฎกระทรวง/หนังสือเวียน ข้อ/มาตรา/หัวข้อ ...

หมายเหตุ:
...
```

When web fallback is used, put the mandatory disclaimer first and then use this additional shape:

```text
คำตอบนี้ใช้ข้อมูลจาก web search ไม่ได้ใช้ฐานข้อมูลของ repository ข้อมูลมีโอกาสคลาดเคลื่อน โปรดตรวจสอบกับแหล่งทางการอีกครั้ง

Repository source:
- ...

Web source:
- [ชื่อเว็บไซต์หรือหน่วยงาน] — [ชื่อกฎหมาย/ระเบียบ/หนังสือเวียน/ประกาศ], [มาตรา/ข้อ/หัวข้อ/เลขที่เอกสารที่ยืนยันได้]
  URL: https://...
  วันที่เข้าถึง: ... (ถ้าระบบรองรับ)
  แหล่งนี้เป็น web source ไม่ใช่ repository source

คำตอบและข้อจำกัด:
- ...
```

For diagnosis, use this shape:

```text
วินิจฉัยเบื้องต้น:
...

ตัวบทที่เกี่ยวข้อง:
- ชื่อพระราชบัญญัติ/ระเบียบ/กฎกระทรวง/หนังสือเวียน ข้อ/มาตรา/หัวข้อ ...

เหตุผล:
...

ข้อควรตรวจเพิ่ม:
- ...
```

## Context Mode Choice

At the first Pasadu interaction in a new thread, briefly tell the user that two context modes are available:

- `compact` keeps the same routing/retrieval workflow but uses compact operating rules to save tokens. This is the default.
- `full rules` includes the full `pasadu.md` rules in the generated answer context. Use it when the user wants maximum instruction detail or is auditing behavior.

Do not block direct legal questions just to ask this. If the user has not chosen a mode, proceed with `compact` and mention once that they can request `full rules` anytime.

For script usage:

```powershell
python scripts\pasadu\answer_context.py "question"
python scripts\pasadu\answer_context.py "question" --full-rules
```
