# PassaduAIagent

ฐานความรู้และ retrieval workflow สำหรับ AI assistant ด้านการจัดซื้อจัดจ้างและการบริหารพัสดุภาครัฐของไทย

> เป้าหมายคือให้ AI ตอบจากเอกสารที่ตรวจสอบได้ อ้างมาตรา/ข้อ/หัวข้อจริง แยกลำดับฐานอำนาจ และบอกตรงไปตรงมาเมื่อข้อมูลใน repo ไม่พอ

## ภาพรวม

```text
คำถามผู้ใช้
   │
   ▼
route_query.py ── เลือกแหล่งอ้างอิงตามประเด็น
   │
   ▼
retrieve.py ───── ค้น chunk ที่เกี่ยวข้อง
   │
   ▼
answer_context.py ─ สร้าง context พร้อม guardrails
   │
   ▼
คำตอบพร้อม citation ที่ตรวจด้วย cite_check.py
```

### Multi-agent orchestration

Pasadu ใช้ root session เป็น orchestrator และเลือกเส้นทางที่ประหยัดที่สุดตามลักษณะงาน:

```text
คำถาม
  → legal-retriever: ค้นและคัดหลักฐานโดยไม่ตีความ
  → คำถามตรง: root orchestrator เรียบเรียงคำตอบ
  → ต้องวิเคราะห์: legal-analyst
  → ขัดแย้ง/กำกวม/หลายตัวบท: legal-analyst-complex
  → cite_check.py
  → คำตอบสุดท้าย
```

| Platform | Root orchestrator | Retriever | Analyst | Complex analyst |
| --- | --- | --- | --- | --- |
| Codex | GPT-5.6 Terra, medium | GPT-5.6 Luna, low | GPT-5.6 Luna, high | GPT-5.6 Luna, high |
| Claude Code | โมเดลของผู้ใช้, medium | `inherit`, low | `inherit`, high | `inherit`, high |
| Gemini CLI | โมเดลของผู้ใช้ | `inherit` | `inherit` + prompt ให้ reasoning อย่างรอบคอบ | `inherit` + prompt เชิงซับซ้อน |

ชื่อโมเดล Codex เป็น adapter ของรุ่นปัจจุบัน ส่วน Claude/Gemini ตั้งใจใช้ `inherit` เพื่อรองรับโมเดลที่ผู้ใช้มี หาก native subagents ใช้งานไม่ได้ ระบบยังทำ workflow เดิมใน main session ได้จาก `SKILL.md` และไฟล์คำสั่งประจำแพลตฟอร์ม

ระบบยึดลำดับเอกสารดังนี้:

1. พระราชบัญญัติ: หลักกฎหมายและอำนาจ
2. ระเบียบ: วิธีปฏิบัติและรายละเอียด
3. กฎกระทรวง: กฎเฉพาะที่ออกตามฐานอำนาจ
4. หนังสือเวียน: แนวทางปฏิบัติประกอบ ไม่ใช้แทนตัวบทระดับสูงกว่า

## Reference Catalog

| ประเภท | ไฟล์ | ประเด็นหลัก |
| --- | --- | --- |
| พระราชบัญญัติ | `reference/law/prb60.md` | พ.ร.บ. การจัดซื้อจัดจ้างฯ พ.ศ. 2560 |
| ระเบียบ | `reference/law/rbb60.md` | ระเบียบกระทรวงการคลังฯ พ.ศ. 2560 |
| ระเบียบ | `reference/law/rbb60-3.md` | ระเบียบฉบับที่ 3 พ.ศ. 2569; ข้อ 190-191 |
| กฎกระทรวง | `reference/law/ministerial-regulations/mr-specific-2560.md` | วิธีเฉพาะเจาะจง วงเงินเล็กน้อย ข้อตกลงเป็นหนังสือ และผู้ตรวจรับคนเดียว |
| กฎกระทรวง | `reference/law/ministerial-regulations/mr-appeal-exclusions-2568.md` | กฎกระทรวงอุทธรณ์; เรื่องที่อุทธรณ์ไม่ได้ |
| หนังสือเวียน | `reference/circulars/circular-w367-2567.md` | ว 367; กรณีไม่เข้าข่ายใช้สิทธิอุทธรณ์ตามมาตรา 114 |
| หนังสือเวียน | `reference/circulars/circular-w214-2563.md` | ว 214; คุณสมบัติผู้ยื่นเสนอราคา ผลงาน และคุณลักษณะเฉพาะ |

## Routing Matrix

| คำถามหรือคำสำคัญ | Primary source | แหล่งประกอบ |
| --- | --- | --- |
| `มาตรา`, `พรบ.`, `พระราชบัญญัติ` | `prb60.md` | `rbb60.md` |
| `ข้อ`, `ระเบียบ`, วิธีปฏิบัติทั่วไป | `rbb60.md` | `prb60.md` |
| ข้อ 190-191, คะแนนความเสียหาย, การระงับ | `rbb60-3.md` | `rbb60.md`, `prb60.md` |
| `ว 214`, คุณสมบัติผู้ยื่นเสนอราคา | `circular-w214-2563.md` | `rbb60.md`, `prb60.md` |
| `เจาะจง`, `เฉพาะเจาะจง` | `prb60.md` มาตรา 56 | กฎกระทรวงเจาะจง → `rbb60.md` |
| วงเงินเล็กน้อย | `prb60.md` มาตรา 56 | กฎกระทรวงเจาะจง → `rbb60.md` |
| ไม่ทำข้อตกลงเป็นหนังสือ, ผู้ตรวจรับคนเดียว | `prb60.md` มาตรา 56 | กฎกระทรวงเจาะจง → `rbb60.md` |
| การอุทธรณ์ทั่วไป | `prb60.md` มาตรา 114-119 | กฎกระทรวงอุทธรณ์, ว 367 |
| เรื่องที่อุทธรณ์ไม่ได้ | กฎกระทรวงอุทธรณ์ | `prb60.md` มาตรา 115 |
| ไม่เข้าข่ายใช้สิทธิอุทธรณ์ | ว 367 | `prb60.md` มาตรา 114 |

### หลักแยกเรื่องอุทธรณ์

- **เรื่องที่อุทธรณ์ไม่ได้:** ผู้ยื่นข้อเสนอมีสิทธิอุทธรณ์ตามมาตรา 114 แต่กฎหมายห้ามยกเรื่องบางประเภทขึ้นอุทธรณ์ ตามมาตรา 115 และกฎกระทรวงอุทธรณ์
- **ไม่เข้าข่ายใช้สิทธิอุทธรณ์:** บุคคลหรือสถานการณ์นั้นไม่เข้าองค์ประกอบการใช้สิทธิตามมาตรา 114 ตั้งแต่ต้น ตามแนวทาง ว 367 ข้อ 2

## โครงสร้าง Repo

```text
PassaduAIagent/
├─ SKILL.md
├─ pasadu.md
├─ AGENTS.md
├─ CLAUDE.md
├─ GEMINI.md
├─ .codex/
│  ├─ config.toml
│  └─ agents/
├─ .claude/agents/
├─ .gemini/agents/
├─ reference/
│  ├─ law/
│  │  ├─ prb60.md
│  │  ├─ rbb60.md
│  │  ├─ rbb60-3.md
│  │  └─ ministerial-regulations/
│  │     ├─ mr-specific-2560.md
│  │     └─ mr-appeal-exclusions-2568.md
│  ├─ circulars/
│  │  ├─ circular-w214-2563.md
│  │  └─ circular-w367-2567.md
│  └─ ECPP/
├─ scripts/pasadu/
│  ├─ build_index.py
│  ├─ route_query.py
│  ├─ retrieve.py
│  ├─ answer_context.py
│  ├─ cite_check.py
│  └─ eval_queries.py
├─ data/index/
├─ evals/
└─ tests/
```

## Quick Start

ต้องใช้ Python 3.10 ขึ้นไป และไม่มี third-party dependency สำหรับ retrieval scripts

```powershell
python scripts\pasadu\build_index.py
python scripts\pasadu\route_query.py "วงเงินเล็กน้อยไม่ทำข้อตกลงเป็นหนังสือได้ไหม" --json
python scripts\pasadu\retrieve.py "ว 214 กำหนดคุณสมบัติผู้ยื่นเสนอราคาอย่างไร" --limit 5
python scripts\pasadu\answer_context.py "เรื่องใดอุทธรณ์ไม่ได้"
python scripts\pasadu\cite_check.py --text "อ้างอิง: reference/circulars/circular-w214-2563.md หัวข้อ 1.1.2"
```

รัน verification suite:

```powershell
python -m unittest discover -s tests
python scripts\pasadu\eval_queries.py
```

## ส่วนประกอบหลัก

| ส่วน | หน้าที่ |
| --- | --- |
| `SKILL.md` | trigger และ routing guidance สำหรับ agent |
| `pasadu.md` | persona, policy, citation rules และข้อห้าม |
| `build_index.py` | อ่าน metadata และแตกเอกสารเป็น chunks |
| `route_query.py` | เลือก primary/fallback sources |
| `retrieve.py` | จัดอันดับมาตรา ข้อ และหัวข้อที่เกี่ยวข้อง |
| `answer_context.py` | สร้าง context พร้อมข้อกำกับการตอบ |
| `cite_check.py` | ตรวจ citation กับ index จริง |
| `eval_queries.py` | smoke eval สำหรับ routing และ retrieval |

## Citation Format

```text
reference/law/prb60.md มาตรา 114
reference/law/rbb60.md ข้อ 78
reference/law/rbb60-3.md ข้อ 190/3
reference/law/ministerial-regulations/mr-specific-2560.md ข้อ 4
reference/circulars/circular-w214-2563.md หัวข้อ 1.1.2
```

## ข้อจำกัด

- ระบบนี้เป็นฐานข้อมูลอ้างอิงและ retrieval workflow ไม่ใช่คำวินิจฉัยทางกฎหมายอย่างเป็นทางการ
- Index ครอบคลุมเฉพาะเอกสารที่ลงทะเบียนใน `scripts/pasadu/common.py`
- หนังสือเวียนเป็นแนวทางประกอบ ต้องอ่านร่วมกับฐานอำนาจจาก พ.ร.บ. ระเบียบ หรือกฎกระทรวง
- Web-search fallback และการตรวจแหล่งข้อมูลภายนอกแบบอัตโนมัติยังไม่ได้ implement
- คำตอบที่มีผลต่อกฎหมาย งบประมาณ สัญญา หรือความรับผิด ควรตรวจต้นฉบับทางการและหน่วยงานผู้มีอำนาจอีกครั้ง

## Development Rules

- ห้ามแต่งมาตรา ข้อ หนังสือเวียน หรือคำวินิจฉัย
- ถ้าไม่พบ ให้ตอบว่าไม่พบใน reference ที่มี
- ถ้าสรุป ต้องแยกจากถ้อยคำตัวบท
- ทุก citation ต้องตรวจได้จาก index
- เมื่อเพิ่ม reference ให้เพิ่ม metadata, source registry, routing tests และ regenerate `data/index/*.json`
