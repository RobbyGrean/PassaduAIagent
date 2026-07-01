---
name: pasadu
description: Use when the user says "/pasadu" or asks about Thai government procurement law: การจัดซื้อจัดจ้าง, พัสดุภาครัฐ, พรบ., พ.ร.บ., พระราชบัญญัติ, ระเบียบ, มาตรา, ข้อ, วิธีจัดซื้อจัดจ้าง, สัญญา, หลักประกัน, ตรวจรับ, อำนาจอนุมัติ, ร้องเรียน, or diagnosis of Thai government procurement issues. Uses pasadu.md, routes to prb60.md/rbb60.md, retrieves exact clauses, and answers with verified citations.
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

## Retrieval Scripts

When available, use the repository scripts to avoid reading entire reference files for one question:

- `scripts/pasadu/build_index.py` builds `data/index/*.json` from `prb60.md` and `rbb60.md`.
- `scripts/pasadu/route_query.py` decides the primary source and fallback source.
- `scripts/pasadu/retrieve.py` returns the most relevant clauses with file and clause citations.
- `scripts/pasadu/answer_context.py` builds an LLM-ready context from `pasadu.md`, the user question, and retrieved references.
- `scripts/pasadu/cite_check.py` checks whether final citations exist in the index.

If the index is missing or stale, run `build_index.py` first. If scripts cannot run, fall back to manual search in the same routing order and still verify every citation against the reference files.

## Routing

Default policy:

- For general operational questions, search `reference/law/rbb60.md` first because day-to-day procurement practice follows the Regulation, then use `reference/law/prb60.md` as fallback or supporting authority.
- If the user explicitly asks for `มาตรา`, `พรบ.`, `พ.ร.บ.`, or `พระราชบัญญัติ`, search `reference/law/prb60.md` first, then fallback to `reference/law/rbb60.md` if not found.
- If the user explicitly asks for `ข้อ` or `ระเบียบ`, search `reference/law/rbb60.md` first, then fallback to `reference/law/prb60.md` if not found.
- For contract administration issues such as บริหารสัญญา, บอกเลิกสัญญา, ตกลงยกเลิกสัญญา, แก้ไขสัญญา, เปลี่ยนแปลงสัญญา, งดหรือลดค่าปรับ, or ขยายเวลาทำการ, search `reference/law/prb60.md` first, unless the user explicitly asks for a Regulation clause.

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

Use both files when the question needs both the Act's authority and the Regulation's operating details.

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

For direct questions such as "มาตรา 56 คืออะไร" or "ข้อ 78 ว่าอย่างไร", do not ask the mode question first; retrieve and answer directly.

## Hard Rules

- Do not invent law.
- Do not cite a section or clause that was not found.
- Do not silently rely on outside legal sources.
- Do not change quoted statutory or regulatory text.
- If the answer is not found in the available references, say so plainly.
- Do not treat manuals, circulars, rulings, FAQ, examples, or checklists as higher authority than the Act or Regulation. When those references are added later, label them as supporting practical guidance unless the user asks otherwise.
- When references conflict, explain the conflict and prioritize the Regulation for operational steps, except contract administration issues where the Act must be checked first under this skill's routing policy.

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
