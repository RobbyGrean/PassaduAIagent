---
name: pasadu
description: Use when the user says "/pasadu" or asks about Thai government procurement law: การจัดซื้อจัดจ้าง, พัสดุภาครัฐ, พรบ., พ.ร.บ., พระราชบัญญัติ, ระเบียบ, ระเบียบฉบับที่ 3, มาตรา, ข้อ, ข้อ 190-191, วิธีจัดซื้อจัดจ้าง, สัญญา, หลักประกัน, ตรวจรับ, ประเมินผลผู้ประกอบการ, คะแนนความเสียหาย, อำนาจอนุมัติ, ร้องเรียน, or diagnosis of Thai government procurement issues. Uses pasadu.md, routes to prb60.md/rbb60.md/rbb60-3.md, retrieves exact clauses, and answers with verified citations.
---

# Pasadu Skill

## Purpose

Use this skill to answer, explain, and diagnose questions about Thai government procurement and public supplies administration using the project's reference law files.

## Repository

The source of truth for this skill is:

`C:\Users\PC\Documents\Pasadu AI Creation\PassaduAIagent`

When this skill is installed under `C:\Users\PC\.codex\skills\pasadu`, still use the repository above for `pasadu.md` and all law reference files.

## Required Context

Before answering a procurement-law question, read:

`C:\Users\PC\Documents\Pasadu AI Creation\PassaduAIagent\pasadu.md`

Use the law reference files only as needed:

- `C:\Users\PC\Documents\Pasadu AI Creation\PassaduAIagent\reference\law\prb60.md` for พระราชบัญญัติการจัดซื้อจัดจ้างและการบริหารพัสดุภาครัฐ พ.ศ. 2560
- `C:\Users\PC\Documents\Pasadu AI Creation\PassaduAIagent\reference\law\rbb60.md` for ระเบียบกระทรวงการคลังว่าด้วยการจัดซื้อจัดจ้างและการบริหารพัสดุภาครัฐ พ.ศ. 2560
- `C:\Users\PC\Documents\Pasadu AI Creation\PassaduAIagent\reference\law\rbb60-3.md` for ระเบียบกระทรวงการคลังว่าด้วยการจัดซื้อจัดจ้างและการบริหารพัสดุภาครัฐ (ฉบับที่ 3) พ.ศ. 2569 โดยเฉพาะหมวด 7 ข้อ 190-191 เรื่องการประเมินผลการปฏิบัติงานของผู้ประกอบการงานก่อสร้าง คะแนนความเสียหาย และการระงับการยื่นข้อเสนอหรือทำสัญญา

## Retrieval Scripts

When available, use the repository scripts to avoid reading entire reference files for one question:

- `scripts/pasadu/build_index.py` builds `data/index/*.json` from `prb60.md`, `rbb60.md`, and `rbb60-3.md`.
- `scripts/pasadu/route_query.py` decides the primary source and fallback source.
- `scripts/pasadu/retrieve.py` returns the most relevant clauses with file and clause citations.
- `scripts/pasadu/answer_context.py` builds an LLM-ready context from `pasadu.md`, the user question, and retrieved references.
- `scripts/pasadu/cite_check.py` checks whether final citations exist in the index.

If the index is missing or stale, run `build_index.py` first. If scripts cannot run, fall back to manual search in the same routing order and still verify every citation against the reference files.

## Routing

Default policy:

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
5. If no relevant clause is found, search the fallback source.
6. Identify the exact section or clause.
7. Answer from the cited text.
8. Ask concise clarification questions if facts are missing.
9. State uncertainty when the reference does not fully answer the question.

For direct questions such as "มาตรา 56 คืออะไร", "ข้อ 78 ว่าอย่างไร", or "ข้อ 190/3 ประเมินอะไร", do not ask the mode question first; retrieve and answer directly.

## Hard Rules

- Do not invent law.
- Do not cite a section or clause that was not found.
- Do not silently rely on outside legal sources.
- Do not change quoted statutory or regulatory text.
- If the answer is not found in the available references, say so plainly.
- Do not treat manuals, circulars, rulings, FAQ, examples, or checklists as higher authority than the Act or Regulation. When those references are added later, label them as supporting practical guidance unless the user asks otherwise.
- When references conflict, explain the conflict and prioritize the Regulation for operational steps, except contract administration issues where the Act must be checked first under this skill's routing policy.
- Treat summaries inside `rbb60-3.md` as supporting explanation only. For legal answers, cite the regulation clauses or annex tables, not the summary section alone.
- Use the citation form `reference/law/rbb60-3.md ข้อ ...`, including slash clauses such as `reference/law/rbb60-3.md ข้อ 190/3`.

## Preferred Output

For most answers, use this shape:

```text
คำตอบสั้น:
...

อ้างอิง:
- reference/law/... ข้อ/มาตรา ...

หมายเหตุ:
...
```

For diagnosis, use this shape:

```text
วินิจฉัยเบื้องต้น:
...

ตัวบทที่เกี่ยวข้อง:
- reference/law/... ข้อ/มาตรา ...

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
