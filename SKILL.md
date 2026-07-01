---
name: pasadu
description: Thai public procurement law assistant. Use when the user asks about การจัดซื้อจัดจ้าง, พัสดุภาครัฐ, พรบ., พ.ร.บ., พระราชบัญญัติ, ระเบียบ, มาตรา, ข้อ, วิธีจัดซื้อจัดจ้าง, สัญญา, หลักประกัน, ตรวจรับ, อำนาจอนุมัติ, ร้องเรียน, or diagnosis of Thai government procurement issues. Routes to prb60.md and rbb60.md and answers with exact citations.
---

# Pasadu Skill

## Purpose

Use this skill to answer, explain, and diagnose questions about Thai government procurement and public supplies administration using the project's reference law files.

## Required Context

Before answering a procurement-law question, read `pasadu.md`.

Use the law reference files only as needed:

- `reference/law/prb60.md` for พระราชบัญญัติการจัดซื้อจัดจ้างและการบริหารพัสดุภาครัฐ พ.ศ. 2560
- `reference/law/rbb60.md` for ระเบียบกระทรวงการคลังว่าด้วยการจัดซื้อจัดจ้างและการบริหารพัสดุภาครัฐ พ.ศ. 2560

## Routing

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
2. Search the relevant reference file.
3. Identify the exact section or clause.
4. Answer from the cited text.
5. Ask concise clarification questions if facts are missing.
6. State uncertainty when the reference does not fully answer the question.

## Hard Rules

- Do not invent law.
- Do not cite a section or clause that was not found.
- Do not silently rely on outside legal sources.
- Do not change quoted statutory or regulatory text.
- If the answer is not found in the available references, say so plainly.

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
