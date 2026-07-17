<div align="center">

# ⚖️ PasaduAIagent

### ผู้ช่วย AI สำหรับงานจัดซื้อจัดจ้างและการบริหารพัสดุภาครัฐของไทย

ระบบค้นคืนข้อมูลกฎหมายแบบอ้างอิงได้ พร้อม workflow สำหรับตอบคำถามอย่างมีหลักฐาน ตรวจสอบย้อนกลับได้ และรู้จักบอกเมื่อข้อมูลยังไม่เพียงพอ

<p>
  <a href="./INSTALLATION.md">ติดตั้ง</a> ·
  <a href="./SKILL.md">ดู Skill</a> ·
  <a href="./pasadu.md">ดู Response Policy</a> ·
  <a href="./docs/pasadu-agent-usage.md">คู่มือการใช้งาน</a>
</p>

![Phase 1](https://img.shields.io/badge/phase-1%20%7C%20evidence--first-8B5CF6?style=for-the-badge)
![Thai Procurement](https://img.shields.io/badge/domain-Thai%20public%20procurement-0F766E?style=for-the-badge)
![Read-only](https://img.shields.io/badge/workflow-read--only-334155?style=for-the-badge)

</div>

> **หลักคิดของ Pasadu**
>
> ตอบจากเอกสารที่ค้นและตรวจสอบได้ อ้างมาตรา/ข้อ/หัวข้อให้ตรงต้นฉบับ แยกลำดับศักดิ์ของแหล่งอ้างอิง และบอกตรง ๆ เมื่อ repository ยังมีข้อมูลไม่พอสำหรับสรุป

---

## สารบัญ

- [ภาพรวมใน 30 วินาที](#ภาพรวมใน-30-วินาที)
- [จุดเด่นของระบบ](#จุดเด่นของระบบ)
- [Workflow การตอบคำถาม](#workflow-การตอบคำถาม)
- [เริ่มใช้งานอย่างรวดเร็ว](#เริ่มใช้งานอย่างรวดเร็ว)
- [ติดตั้ง](#ติดตั้ง)
- [ใช้ retrieval layer โดยตรง](#ใช้-retrieval-layer-โดยตรง)
- [โครงสร้าง repository](#โครงสร้าง-repository)
- [ชุดข้อมูลอ้างอิง](#ชุดข้อมูลอ้างอิง)
- [รูปแบบคำตอบและ citation](#รูปแบบคำตอบและ-citation)
- [ข้อจำกัดที่ควรรู้](#ข้อจำกัดที่ควรรู้)
- [ตรวจสอบและพัฒนาต่อ](#ตรวจสอบและพัฒนาต่อ)
- [เอกสารที่เกี่ยวข้อง](#เอกสารที่เกี่ยวข้อง)

## ภาพรวมใน 30 วินาที

PasaduAIagent คือ **AI skill + local retrieval workflow** ที่ออกแบบมาเพื่อให้ผู้ช่วย AI ทำงานกับคำถามด้านพัสดุภาครัฐได้อย่างเป็นระบบ โดยเน้น 4 เรื่อง:

| ส่วนประกอบ | ทำหน้าที่อะไร |
| --- | --- |
| **Reference library** | เก็บพระราชบัญญัติ ระเบียบ กฎกระทรวง และหนังสือเวียนที่อยู่ในขอบเขตของโปรเจกต์ |
| **Routing layer** | เลือกแหล่งอ้างอิงหลักตามคำสำคัญ มาตรา ข้อ และประเด็นของคำถาม |
| **Retrieval layer** | ค้นคืน section/chunk ที่เกี่ยวข้องจากดัชนีแบบ section-aware |
| **Answer guardrails** | บังคับให้คำตอบแยกข้อเท็จจริงจากการตีความ พร้อมตรวจ citation ก่อนส่ง |

### เส้นทางข้อมูล

```mermaid
flowchart LR
    A[คำถามของผู้ใช้] --> B[Route query]
    B --> C[ค้นคืนหลักฐาน]
    C --> D[สร้าง answer context]
    D --> E[วิเคราะห์ตามความซับซ้อน]
    E --> F[ตรวจ citation]
    F --> G[คำตอบที่ตรวจสอบย้อนกลับได้]
```

## จุดเด่นของระบบ

<table>
<tr>
<td width="50%">

### 🔎 Evidence-first

เริ่มจากหลักฐานใน repository ก่อนเสมอ ไม่รีบคาดเดาคำตอบจากความจำของโมเดล

</td>
<td width="50%">

### 🧭 Routing ตามประเด็น

แยกคำถามเรื่องมาตรา ระเบียบ วิธีเฉพาะเจาะจง อุทธรณ์ และคุณสมบัติผู้ยื่นเสนอราคาไปยังแหล่งที่เหมาะสม

</td>
</tr>
<tr>
<td>

### 🧠 Reasoning แบบพอดี

ใช้การตอบตรงเมื่อเป็นการค้นคืน ใช้ analyst เมื่อมีการปรับบทกฎหมายเข้ากับข้อเท็จจริง และยกระดับเมื่อมีความขัดแย้งหรือความกำกวมที่มีนัยสำคัญ

</td>
<td>

### ✅ Citation ตรวจได้

ตรวจการอ้างอิงกับดัชนีภายในด้วย `cite_check.py` เพื่อช่วยลด citation ที่ไม่ตรงกับเอกสารต้นทาง

</td>
</tr>
</table>

## Workflow การตอบคำถาม

Pasadu ใช้ root session เป็นตัวประสานงาน และเลือกเส้นทางที่เหมาะกับลักษณะคำถาม:

```text
คำถาม
  │
  ├─ ค้นคืน / อธิบายตรง ๆ       → route → retrieve → draft answer
  │
  ├─ ใช้กฎหมายกับข้อเท็จจริง     → route → retrieve → legal analyst → answer
  │
  └─ ขัดแย้ง / กำกวม / หลายบท    → route → retrieve → complex analysis → answer
                                             │
                                             └→ cite_check ก่อนส่งทุกครั้ง
```

### ระดับการทำงาน

| สถานการณ์ | เส้นทางที่ใช้ | ผลลัพธ์ที่คาดหวัง |
| --- | --- | --- |
| ต้องการมาตรา ข้อ หรือขั้นตอนที่ระบุชัด | Direct retrieval | สรุปจาก evidence packet พร้อม citation |
| ต้องวิเคราะห์ว่ากฎหมายใช้กับกรณีนี้อย่างไร | Legal analyst | แยกหลักกฎหมาย ข้อเท็จจริง เงื่อนไข และข้อสรุป |
| มีหลายบทต้องอ่านประกอบกัน หรือมีความกำกวมสำคัญ | Complex analyst | อธิบายจุดขัดแย้ง สมมติฐาน และความไม่แน่นอนอย่างชัดเจน |
| ค้นแล้วไม่มีหลักฐานเพียงพอ | Safe failure | แจ้งข้อมูลที่ขาด โดยไม่แต่งคำตอบขึ้นเอง |

### การตั้งค่าโมเดล

สำหรับ Codex ค่าโมเดลของแต่ละช่วงทำงานเป็นดังนี้:

| ช่วงทำงาน | โมเดล | เหตุผลการตั้งค่า |
| --- | --- | --- |
| รับคำถาม / root session | `inherit` | ใช้โมเดลและ reasoning ที่ผู้ใช้หรือ Codex เลือกไว้ |
| `legal_retriever` | `gpt-5.6-luna` / high | ค้นและคัดหลักฐานจาก repository |
| `legal_analyst` | `gpt-5.6-luna` / high | วิเคราะห์การใช้กฎหมายกับข้อเท็จจริง |
| `legal_analyst_complex` | `gpt-5.6-luna` / high | วิเคราะห์ความขัดแย้ง ความกำกวม และหลายบทบัญญัติ |

ค่าดังกล่าวกำหนดใน [`.codex/config.toml`](./.codex/config.toml) และ [`.codex/agents/`](./.codex/agents/)

> **หมายเหตุ:** Phase 1 ใช้ข้อมูลจาก repository เป็นหลัก และเป็น workflow แบบอ่านอย่างเดียว (read-only)

## เริ่มใช้งานอย่างรวดเร็ว

### 1. ติดตั้งบน Codex สำหรับ Windows

เปิด PowerShell แล้วรัน:
```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\skills" | Out-Null
git clone https://github.com/RobbyGrean/PassaduAIagent.git "$env:USERPROFILE\.codex\skills\pasadu"
```

จากนั้นปิด–เปิด Codex หรือเริ่ม task ใหม่ แล้วถามได้ทันที เช่น:

```text
คณะกรรมการตรวจรับพัสดุมีหน้าที่อะไร
```

### 2. เรียกใช้งานแบบ manual

```text
/pasadu มาตรา 56 ใช้กรณีใด
/passadu มาตรา 56 ใช้กรณีใด
$pasadu มาตรา 56 ใช้กรณีใด
```

โดยทั่วไปไม่จำเป็นต้องพิมพ์ชื่อ skill — Codex ควร auto-trigger จาก intent ของคำถามเมื่อคำถามอยู่ในขอบเขตที่เกี่ยวข้อง

## ติดตั้ง

คู่มือติดตั้งฉบับเต็มครอบคลุม Codex Windows App, Codex CLI, ChatGPT Work, Gemini CLI และ Claude Code:

➡️ **[อ่าน INSTALLATION.md](./INSTALLATION.md)**

### ข้อกำหนดขั้นต่ำ

- Git สำหรับ clone และอัปเดต repository
- Codex, Claude Code หรือ Gemini CLI ตามแพลตฟอร์มที่ต้องการใช้
- Python 3.10 ขึ้นไป หากต้องการรัน retrieval scripts, tests หรือ evaluation

> การถามตอบผ่าน skill ยังทำงานได้โดยไม่ติดตั้ง Python แต่เครื่องมือค้นคืนและชุดทดสอบจะไม่สามารถทำงานได้

## ใช้ retrieval layer โดยตรง

สคริปต์ทั้งหมดอยู่ใน [`scripts/pasadu/`](./scripts/pasadu/) และใช้ index ที่อยู่ใน [`data/index/`](./data/index/)

### Route คำถามไปยังแหล่งอ้างอิง

```powershell
python -B scripts/pasadu/route_query.py "มาตรา 56 ใช้กรณีใด"
```

เพิ่ม `--json` หากต้องการผลลัพธ์สำหรับนำไปใช้งานต่อในระบบอื่น

### ค้นคืนหลักฐานที่เกี่ยวข้อง

```powershell
python -B scripts/pasadu/retrieve.py "หน้าที่ของคณะกรรมการตรวจรับพัสดุ" --limit 5
```

### สร้าง context สำหรับผู้ช่วย AI

```powershell
python -B scripts/pasadu/answer_context.py "การอุทธรณ์ผลการจัดซื้อจัดจ้างทำได้อย่างไร" --limit 5
```

### ตรวจ citation ของคำตอบ

```powershell
python -B scripts/pasadu/cite_check.py --text "คำตอบที่มี citation อยู่ในข้อความ"
```

หรืออ่านคำตอบจากไฟล์ UTF-8:

```powershell
python -B scripts/pasadu/cite_check.py --file answer.txt
```

## โครงสร้าง repository

```text
PassaduAIagent/
├── SKILL.md                    # trigger และ workflow หลักของ skill
├── pasadu.md                   # persona, policy และรูปแบบคำตอบ
├── AGENTS.md                   # กติกาการประสานงานของ Phase 1
├── INSTALLATION.md             # คู่มือติดตั้งทุกแพลตฟอร์ม
├── reference/                  # คลังเอกสารอ้างอิง
│   ├── law/                    # พ.ร.บ., ระเบียบ และกฎกระทรวง
│   ├── circulars/              # หนังสือเวียน
│   └── ECPP/                   # เอกสารประกอบ e-Catalog / e-CPP
├── data/index/                 # ดัชนีสำหรับ routing และ retrieval
├── scripts/pasadu/             # เครื่องมือค้นคืนและตรวจ citation
├── evals/                      # คำถามและ citation ที่คาดหวัง
├── tests/                      # ชุดทดสอบสคริปต์
├── docs/                       # คู่มือ การออกแบบ และ roadmap
└── how2agent/                  # คู่มือเริ่มต้นใช้งานแบบ visual
```

## ชุดข้อมูลอ้างอิง

คลังข้อมูลปัจจุบันเน้นกฎหมายและเอกสารที่จำเป็นต่อการตอบคำถาม procurement ระยะเริ่มต้น:

| กลุ่ม | เอกสารหลัก | ประเด็นที่ครอบคลุม |
| --- | --- | --- |
| พระราชบัญญัติ | พ.ร.บ. การจัดซื้อจัดจ้างฯ พ.ศ. 2560 | หลักการ อำนาจ วิธีจัดซื้อจัดจ้าง และการอุทธรณ์ |
| ระเบียบ | ระเบียบกระทรวงการคลังฯ พ.ศ. 2560 | ขั้นตอนปฏิบัติ รายละเอียด และข้อกำหนดทั่วไป |
| ระเบียบฉบับแก้ไข | ระเบียบฯ ฉบับที่ 3 พ.ศ. 2569 | ข้อ 190–191 และประเด็นที่มีการปรับปรุง |
| กฎกระทรวง | กฎกระทรวงกำหนดวิธีเฉพาะเจาะจงฯ | วิธีเฉพาะเจาะจง วงเงินเล็กน้อย และผู้ตรวจรับ |
| หนังสือเวียน | ว 214 และ ว 367 | คุณสมบัติผู้ยื่นเสนอราคา และหลักเกณฑ์ด้านการอุทธรณ์ |

การเพิ่ม reference ใหม่ควรอัปเดต metadata, source registry, routing tests และสร้าง index ใหม่ให้ครบชุด

## รูปแบบคำตอบและ citation

คำตอบที่ดีของ Pasadu ควรมีลำดับดังนี้:

1. **คำตอบสั้นก่อน** — บอกผลลัพธ์ที่ผู้ถามต้องการรู้
2. **ฐานกฎหมาย** — ระบุมาตรา ข้อ หรือหัวข้อที่เกี่ยวข้อง
3. **เงื่อนไขและข้อยกเว้น** — ระบุให้ชัดว่าหลักเกณฑ์ใช้เมื่อใดและไม่ใช้เมื่อใด
4. **การประยุกต์กับกรณี** — แยกข้อเท็จจริงออกจากการตีความ
5. **ข้อควรตรวจต่อ** — ชี้ข้อมูลที่ยังขาดหรือควรตรวจเอกสารทางการเพิ่มเติม

Citation ต้องสอดคล้องกับ section ที่มีอยู่จริงใน index และไม่ควรอ้างเกินกว่าหลักฐานที่ค้นได้ หากค้นไม่พบ ให้ตอบว่าไม่พบในชุดเอกสารปัจจุบันแทนการคาดเดา

## ข้อจำกัดที่ควรรู้

- ขอบเขตความรู้ขึ้นอยู่กับเอกสารที่อยู่ใน `reference/` และ index ที่สร้างไว้ใน repository
- ยังไม่มี web-search fallback หรือการตรวจสอบเอกสารภายนอกแบบอัตโนมัติ
- ยังไม่มี chatbot runtime แบบเต็มรูปแบบ — repository นี้เป็น skill และ retrieval foundation
- คำตอบที่กระทบสิทธิ หน้าที่ งบประมาณ สัญญา หรือความรับผิด ควรตรวจต้นฉบับทางการและหน่วยงานผู้มีอำนาจอีกครั้ง
- การเปลี่ยนแปลงเอกสารอ้างอิงต้องทำอย่างระมัดระวัง เพราะมีผลต่อ routing, citation และผล evaluation

## ตรวจสอบและพัฒนาต่อ

### รัน tests

```powershell
python -B -m unittest discover -s tests
```

### รัน evaluation queries

```powershell
python -B scripts/pasadu/eval_queries.py
```

### สร้าง index ใหม่

```powershell
python -B scripts/pasadu/build_index.py
```

ก่อนส่งการเปลี่ยนแปลงควรตรวจอย่างน้อย:

- retrieval ค้น section สำคัญได้จริง
- routing ชี้ source หลักและ source ประกอบถูกต้อง
- citation ผ่าน `cite_check.py`
- tests และ evaluation ไม่ถดถอย
- ไม่เผลอแก้สาระของกฎหมายจากการจัดรูปแบบเอกสาร

## เอกสารที่เกี่ยวข้อง

| เอกสาร | ใช้เมื่อ |
| --- | --- |
| [`INSTALLATION.md`](./INSTALLATION.md) | ต้องการติดตั้งหรือแก้ปัญหาแต่ละแพลตฟอร์ม |
| [`SKILL.md`](./SKILL.md) | ต้องการเข้าใจกติกา trigger และ workflow ของ skill |
| [`pasadu.md`](./pasadu.md) | ต้องการดู persona, response policy และ guardrails |
| [`docs/pasadu-agent-usage.md`](./docs/pasadu-agent-usage.md) | ต้องการดูสถานะปัจจุบันและ roadmap |
| [`docs/token-usage.md`](./docs/token-usage.md) | ต้องการเข้าใจการใช้ context และ token |
| [`how2agent/index.html`](./how2agent/index.html) | ต้องการคู่มือเริ่มต้นใช้งานแบบภาพ |

---

<div align="center">

**Pasadu — เปลี่ยนคำถามด้านพัสดุให้กลายเป็นคำตอบที่มีหลักฐาน**

<sub>Phase 1 · Evidence-first · Read-only · Built for Thai public procurement workflows</sub>

</div>
