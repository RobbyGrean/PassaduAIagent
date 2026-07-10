# Installation Guide — PassaduAIagent

คู่มือติดตั้ง **Pasadu** เป็น AI skill สำหรับงานจัดซื้อจัดจ้างและการบริหารพัสดุภาครัฐของไทย โดยติดตั้งทั้ง repository เพื่อให้ agent ใช้ได้ครบทั้งคำสั่ง workflow สคริปต์ค้นข้อมูล และไฟล์กฎหมายอ้างอิง

Repository: <https://github.com/RobbyGrean/PassaduAIagent>

## สารบัญ

- [Quick Start สำหรับ Codex บน Windows](#quick-start-สำหรับ-codex-บน-windows)
- [สิ่งที่ถูกติดตั้ง](#สิ่งที่ถูกติดตั้ง)
- [ข้อกำหนดก่อนติดตั้ง](#ข้อกำหนดก่อนติดตั้ง)
- [ติดตั้งบน Codex Windows App](#ติดตั้งบน-codex-windows-app)
- [ติดตั้งบน Codex CLI](#ติดตั้งบน-codex-cli)
- [ติดตั้งบน Claude Code](#ติดตั้งบน-claude-code)
- [ใช้งานบน Claudeai](#ใช้งานบน-claudeai)
- [Workflow ของ Pasadu](#workflow-ของ-pasadu)
- [ตรวจสอบการติดตั้ง](#ตรวจสอบการติดตั้ง)
- [อัปเดต](#อัปเดต)
- [แก้ปัญหา](#แก้ปัญหา)
- [ถอนการติดตั้ง](#ถอนการติดตั้ง)

---

## Quick Start สำหรับ Codex บน Windows

เปิด PowerShell แล้วรัน:

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\skills" | Out-Null
git clone https://github.com/RobbyGrean/PassaduAIagent.git "$env:USERPROFILE\.codex\skills\pasadu"
```

ปิดและเปิด Codex Windows App ใหม่ จากนั้นเริ่ม task ใหม่แล้วถามตามธรรมชาติได้ทันที:

```text
วิธีเฉพาะเจาะจงใช้ได้ในกรณีใด
```

Codex ควรเลือก `pasadu` อัตโนมัติจาก intent ของคำถาม โดยผู้ใช้ไม่ต้องจำชื่อ skill

หากต้องการบังคับเรียกแบบ manual ใช้ได้ทั้งสอง alias:

```text
/pasadu วิธีเฉพาะเจาะจงใช้ได้ในกรณีใด
/passadu วิธีเฉพาะเจาะจงใช้ได้ในกรณีใด
```

ถ้า `/pasadu` ไม่ปรากฏใน slash-command list ให้เรียก skill โดยตรงด้วย:

```text
$pasadu วิธีเฉพาะเจาะจงใช้ได้ในกรณีใด
```

> Codex ใช้ชื่อ `pasadu` และ `description` จาก YAML frontmatter เพื่อพิจารณา auto-trigger ส่วน `/pasadu` และ `/passadu` เป็น manual trigger ที่ skill รองรับ Enabled skill อาจแสดงใน slash-command list ตามเวอร์ชันและ environment ของ Codex

## สิ่งที่ถูกติดตั้ง

คำสั่ง Quick Start clone ทั้ง repository ไปที่:

```text
%USERPROFILE%\.codex\skills\pasadu\
```

ไฟล์สำคัญ:

| Path | หน้าที่ |
|---|---|
| `SKILL.md` | metadata, trigger, routing และ workflow ที่ Codex โหลด |
| `pasadu.md` | persona กติกาการตอบ และรูปแบบการวินิจฉัย |
| `reference/law/` | ตัวบทกฎหมายและระเบียบที่ใช้เป็นแหล่งอ้างอิง |
| `scripts/pasadu/` | สร้าง index, route query, retrieve และตรวจ citation |
| `data/index/` | index สำหรับค้นตัวบทอย่างรวดเร็ว |
| `evals/` | ชุดคำถามและ citation ที่คาดหวัง |
| `tests/` | tests ของ retrieval scripts |

ต้องติดตั้งทั้ง repository เพราะ `SKILL.md` เรียกใช้ไฟล์ประกอบเหล่านี้ด้วย path ภายในโฟลเดอร์เดียวกัน

## ข้อกำหนดก่อนติดตั้ง

### จำเป็น

- Codex Windows App หรือ Codex CLI
- Git
- Internet สำหรับ clone และ update repository

ตรวจ Git:

```powershell
git --version
```

### แนะนำ

- Python 3.10 ขึ้นไป สำหรับ retrieval scripts, eval และ tests

```powershell
python --version
```

การถามตอบผ่าน skill ยังทำงานได้หากไม่มี Python โดย agent สามารถค้นไฟล์ Markdown โดยตรง แต่ retrieval scripts จะใช้งานไม่ได้

---

## ติดตั้งบน Codex Windows App

### 1. เปิด PowerShell

ใช้ Windows PowerShell, PowerShell 7 หรือ Terminal ใน Codex App ได้

### 2. Clone ทั้ง repository เข้า skills directory

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\skills" | Out-Null
git clone https://github.com/RobbyGrean/PassaduAIagent.git "$env:USERPROFILE\.codex\skills\pasadu"
```

โครงสร้างที่ถูกต้องต้องเป็น:

```text
C:\Users\<ชื่อผู้ใช้>\.codex\skills\pasadu\SKILL.md
```

อย่า clone เป็นโครงสร้างซ้อนแบบนี้:

```text
...\.codex\skills\pasadu\PassaduAIagent\SKILL.md
```

### 3. ตรวจไฟล์หลัก

```powershell
Test-Path "$env:USERPROFILE\.codex\skills\pasadu\SKILL.md"
Test-Path "$env:USERPROFILE\.codex\skills\pasadu\pasadu.md"
Test-Path "$env:USERPROFILE\.codex\skills\pasadu\reference\law\prb60.md"
Test-Path "$env:USERPROFILE\.codex\skills\pasadu\reference\law\rbb60.md"
Test-Path "$env:USERPROFILE\.codex\skills\pasadu\reference\law\rbb60-3.md"
```

ทุกคำสั่งควรแสดง `True`

### 4. Reload Codex

ปิด Codex App แล้วเปิดใหม่ หรือเริ่ม task ใหม่ เพื่อให้ Codex discover skill ที่ติดตั้งเพิ่ม

### 5. ใช้งานแบบ Auto-trigger

ถามตามธรรมชาติ ไม่ต้องใส่ชื่อ skill:

```text
คณะกรรมการตรวจรับพัสดุมีหน้าที่อะไร
```

```text
ตาม พ.ร.บ. การจัดซื้อจัดจ้างฯ พ.ศ. 2560 มาตรา 56 ใช้กรณีใด
```

```text
หน่วยงานจะแก้ไขสัญญาหลังลงนามได้หรือไม่
```

Codex ต้องพิจารณาเรียก `pasadu` เองเมื่อ intent อยู่ในขอบเขตของกฎหมายและระเบียบการจัดซื้อจัดจ้างภาครัฐ

### 6. ใช้งานแบบ Manual

```text
/pasadu มาตรา 56 กล่าวถึงอะไร
/passadu มาตรา 56 กล่าวถึงอะไร
```

หรือ explicit skill mention:

```text
$pasadu มาตรา 56 กล่าวถึงอะไร
```

Manual trigger ใช้เมื่อต้องการบังคับ routing หรือทดสอบการติดตั้งเท่านั้น การใช้งานปกติควรถามตามธรรมชาติแล้วให้ Codex เลือก skill จาก description

---

## ติดตั้งบน Codex CLI

Codex CLI และ Codex App ใช้ user-level skills directory เดียวกัน จึงใช้คำสั่ง PowerShell ชุดเดียวกับ Quick Start:

```powershell
git clone https://github.com/RobbyGrean/PassaduAIagent.git "$env:USERPROFILE\.codex\skills\pasadu"
```

เปิด Codex CLI ใหม่ แล้วตรวจ skill ด้วย `/skills` หรือพิมพ์ `$` เพื่อค้นหา `pasadu`

ตัวอย่าง:

```text
$pasadu อธิบายหน้าที่ของคณะกรรมการตรวจรับพัสดุ
```

### macOS และ Linux

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/RobbyGrean/PassaduAIagent.git ~/.codex/skills/pasadu
```

---

## ติดตั้งบน Claude Code

ติดตั้งทั้ง repository เป็น user-level skill:

### Windows PowerShell

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills" | Out-Null
git clone https://github.com/RobbyGrean/PassaduAIagent.git "$env:USERPROFILE\.claude\skills\pasadu"
```

### macOS และ Linux

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/RobbyGrean/PassaduAIagent.git ~/.claude/skills/pasadu
```

เปิด Claude Code session ใหม่ แล้วลอง:

```text
/pasadu วิธีคัดเลือกใช้เมื่อใด
```

หาก Claude Code เวอร์ชันที่ใช้ไม่แสดง skill เป็น slash command ให้ระบุชื่อ skill ใน prompt:

```text
ใช้ skill pasadu ตอบว่า วิธีคัดเลือกใช้เมื่อใด
```

---

## ใช้งานบน Claude.ai

Claude.ai บนเว็บไม่สามารถอ่าน `%USERPROFILE%\.codex\skills\` หรือ clone local repository โดยตรง วิธีใช้งานคือสร้าง Claude Project แล้วเพิ่ม repository เป็น Project knowledge/context

คู่มือแบบภาพ:

<https://robbygrean.github.io/PassaduAIagent/how2agent/>

ไฟล์ขั้นต่ำที่ Project ต้องเข้าถึง:

- `SKILL.md`
- `pasadu.md`
- `reference/law/prb60.md`
- `reference/law/rbb60.md`
- `reference/law/rbb60-3.md`

กำหนด Project instructions ให้ถือข้อความที่ขึ้นต้นด้วย `/pasadu` เป็นคำสั่งเปิด workflow จาก `SKILL.md` แล้วใช้งาน:

```text
/pasadu การแก้ไขสัญญาทำได้ในกรณีใด
```

Claude.ai Project ไม่ใช่การติดตั้ง local Codex skill จึงไม่มีการรับรองว่า `/pasadu` จะเป็น native slash command ของ UI; ในช่องทางนี้ `/pasadu` ทำหน้าที่เป็นข้อความ trigger ของ Project instructions

---

## Workflow ของ Pasadu

เมื่อ Codex auto-trigger skill หรือผู้ใช้เรียก `/pasadu`/`/passadu` agent ต้องทำงานตามลำดับ:

1. โหลดกติกาจาก `SKILL.md` และ `pasadu.md`
2. จำแนกประเภทคำถามและเลือกแหล่งอ้างอิง
3. Route ไปยัง `prb60.md`, `rbb60.md` หรือ `rbb60-3.md`
4. Retrieve ตัวบทที่เกี่ยวข้องด้วย scripts หรือค้น Markdown โดยตรง
5. ตรวจว่ามาตรา/ข้อที่อ้างมีอยู่จริง
6. ตอบโดยแยกข้อเท็จจริง ตัวบท วินิจฉัย และข้อควรตรวจเพิ่มตามความเหมาะสม
7. ไม่เดาตัวบท และแจ้งตรงเมื่อข้อมูลหรือแหล่งอ้างอิงไม่พอ

Routing หลัก:

| คำถาม | แหล่งแรก |
|---|---|
| พ.ร.บ., พระราชบัญญัติ, มาตรา | `reference/law/prb60.md` |
| ระเบียบ, ข้อ, ขั้นตอนปฏิบัติ | `reference/law/rbb60.md` |
| ระเบียบฉบับที่ 3, ข้อ 190–191, คะแนนความเสียหาย | `reference/law/rbb60-3.md` |

---

## ตรวจสอบการติดตั้ง

### ตรวจการ discover skill

ใน Codex เริ่ม task ใหม่แล้วพิมพ์ `$` หรือ `/skills` และค้นหา `pasadu`

### Smoke test: Auto-trigger

เริ่มด้วยคำถามที่ไม่ระบุชื่อ skill:

```text
การจัดซื้อจัดจ้างโดยวิธีเฉพาะเจาะจงใช้ได้เมื่อใด กรุณาอ้างตัวบท
```

Codex ควรเลือก `pasadu` แล้วค้นแหล่งอ้างอิงใน repository เอง

### Smoke test: Manual trigger

```text
/pasadu มาตรา 56 กล่าวถึงอะไร กรุณาอ้างไฟล์และมาตรา
/passadu มาตรา 56 กล่าวถึงอะไร กรุณาอ้างไฟล์และมาตรา
```

คำตอบควร:

- ใช้ `reference/law/prb60.md`
- ระบุมาตราหรือข้อที่ตรวจพบ
- ไม่ตอบจากความจำล้วน
- แจ้งข้อจำกัดหากข้อมูลไม่ครบ

### ทดสอบ retrieval scripts

รันจากโฟลเดอร์ที่ติดตั้ง:

```powershell
Set-Location "$env:USERPROFILE\.codex\skills\pasadu"
python scripts\pasadu\build_index.py
python scripts\pasadu\route_query.py "มาตรา 56 กล่าวถึงอะไร"
python scripts\pasadu\retrieve.py "วิธีเฉพาะเจาะจงใช้กรณีใด" --limit 5
python -m unittest discover -s tests -v
```

---

## อัปเดต

### Codex

```powershell
git -C "$env:USERPROFILE\.codex\skills\pasadu" pull --ff-only
```

### Claude Code

```powershell
git -C "$env:USERPROFILE\.claude\skills\pasadu" pull --ff-only
```

หลัง update ให้เริ่ม task/session ใหม่

---

## แก้ปัญหา

### `destination path 'pasadu' already exists`

ติดตั้งอยู่แล้ว ให้ update แทน:

```powershell
git -C "$env:USERPROFILE\.codex\skills\pasadu" pull --ff-only
```

### ไม่พบ `/pasadu`

1. ตรวจว่า `SKILL.md` อยู่ตรง path ที่ถูกต้อง
2. ปิดแล้วเปิด Codex ใหม่
3. เริ่ม task ใหม่
4. พิมพ์ `$` แล้วเลือก `pasadu`
5. ใช้ `$pasadu <คำถาม>` เป็น explicit invocation

```powershell
Get-Content "$env:USERPROFILE\.codex\skills\pasadu\SKILL.md" -TotalCount 8
```

ส่วนหัวต้องมี:

```yaml
---
name: pasadu
description: ...
---
```

### Skill เปิดได้แต่หาไฟล์กฎหมายไม่พบ

ตรวจว่า clone มาทั้ง repository ไม่ใช่ copy เฉพาะ `SKILL.md`:

```powershell
Get-ChildItem "$env:USERPROFILE\.codex\skills\pasadu\reference\law"
```

### `python` ไม่พบ

ติดตั้ง Python 3.10 ขึ้นไป หรือใช้ skill แบบค้น Markdown โดยตรงโดยไม่รัน retrieval scripts

### Citation ไม่ตรง

สร้าง index ใหม่แล้วรัน tests:

```powershell
Set-Location "$env:USERPROFILE\.codex\skills\pasadu"
python scripts\pasadu\build_index.py
python -m unittest discover -s tests -v
```

---

## ถอนการติดตั้ง

ปิด Codex ก่อน แล้วลบเฉพาะโฟลเดอร์ skill:

```powershell
Remove-Item -LiteralPath "$env:USERPROFILE\.codex\skills\pasadu" -Recurse
```

สำหรับ Claude Code:

```powershell
Remove-Item -LiteralPath "$env:USERPROFILE\.claude\skills\pasadu" -Recurse
```

คำสั่งนี้ลบ repository ที่ clone ไว้ใน skills directory รวมทั้ง local changes ภายในโฟลเดอร์นั้น ควร commit หรือสำรองงานก่อนถอนการติดตั้ง

---

## แหล่งอ้างอิงเกี่ยวกับ Codex Skills

- OpenAI — Build skills: <https://developers.openai.com/codex/skills/>
- OpenAI — Slash commands: <https://learn.chatgpt.com/docs/reference/slash-commands>
