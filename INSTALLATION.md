# Installation Guide — PassaduAIagent

คู่มือติดตั้ง **Pasadu** เป็น AI skill สำหรับงานจัดซื้อจัดจ้างและการบริหารพัสดุภาครัฐของไทย โดยติดตั้งทั้ง repository เพื่อให้ agent ใช้ได้ครบทั้งคำสั่ง workflow สคริปต์ค้นข้อมูล และไฟล์กฎหมายอ้างอิง

Repository: <https://github.com/RobbyGrean/PassaduAIagent>

## สารบัญ

- [Quick Start สำหรับ Codex บน Windows](#quick-start-สำหรับ-codex-บน-windows)
- [วิธีติดตั้งโดยให้ Codex ดำเนินการ](#วิธีติดตั้งโดยให้-codex-ดำเนินการ)
- [สิ่งที่ถูกติดตั้ง](#สิ่งที่ถูกติดตั้ง)
- [ข้อกำหนดก่อนติดตั้ง](#ข้อกำหนดก่อนติดตั้ง)
- [ติดตั้งบน Codex Windows App](#ติดตั้งบน-codex-windows-app)
- [ใช้งานบน ChatGPT Work](#ใช้งานบน-chatgpt-work)
- [ติดตั้งบน Codex CLI](#ติดตั้งบน-codex-cli)
- [ติดตั้งบน Gemini CLI](#ติดตั้งบน-gemini-cli)
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

## วิธีติดตั้งโดยให้ Codex ดำเนินการ

ส่วนนี้ใช้เมื่อผู้ใช้เปิด task แรกแล้ววางเนื้อหาจาก `newbie user guide/prompt.txt` ให้ Codex ดำเนินการติดตั้งแทนผู้ใช้ ผู้ใช้ไม่จำเป็นต้องอ่านหรือคัดลอกคำสั่งจากไฟล์นี้เอง

### เป้าหมายของการติดตั้ง

การติดตั้งถือว่าสำเร็จเมื่อมี repository ครบทั้งชุดอยู่ที่ user-level skill directory และมีไฟล์หลักอยู่ตรงตำแหน่งต่อไปนี้:

```text
%USERPROFILE%\.codex\skills\pasadu\SKILL.md
%USERPROFILE%\.codex\skills\pasadu\pasadu.md
%USERPROFILE%\.codex\skills\pasadu\reference\law\
%USERPROFILE%\.codex\skills\pasadu\scripts\pasadu\
```

ห้ามถือว่าสำเร็จเพียงเพราะมีไฟล์ `SKILL.md` ไฟล์เดียว และห้ามติดตั้งเป็นโครงสร้างซ้อน เช่น:

```text
%USERPROFILE%\.codex\skills\pasadu\PassaduAIagent\SKILL.md
```

### ลำดับงานที่ Codex ต้องทำ

เมื่อได้รับคำสั่งติดตั้งจาก `prompt.txt` ให้ Codex ทำตามลำดับนี้:

1. อ่าน `INSTALLATION.md` ฉบับเต็มจาก repository ก่อนลงมือ
2. ตรวจระบบปฏิบัติการและว่ามี Git หรือไม่
3. ตรวจ `%USERPROFILE%\.codex\skills\pasadu`
4. ถ้ายังไม่มีโฟลเดอร์ปลายทาง ให้ clone repository ทั้งชุดจาก `https://github.com/RobbyGrean/PassaduAIagent.git`
5. ถ้ามี repository ที่ถูกต้องอยู่แล้ว ให้ใช้ `git pull --ff-only` แทนการ clone ซ้ำ
6. ถ้าปลายทางมีไฟล์อยู่แต่ไม่ใช่ repository นี้ ห้ามลบหรือเขียนทับเอง ให้รายงานปัญหาและขออนุญาตผู้ใช้ก่อน
7. ตรวจไฟล์หลักและโครงสร้างด้วย `Test-Path` ตามหัวข้อ [ตรวจสอบการติดตั้ง](#ตรวจสอบการติดตั้ง)
8. รายงานผลตามจริง ถ้าคำสั่งใดล้มเหลวต้องระบุคำสั่งและสาเหตุ ห้ามรายงานว่าสำเร็จจากการคาดเดา

### สิ่งที่ Codex ห้ามทำระหว่างติดตั้ง

- ห้ามแก้ไข `reference/`, `data/index/`, `evals/` หรือเอกสารกฎหมายเพื่อให้ติดตั้งผ่าน
- ห้าม clone เฉพาะ `SKILL.md` หรือคัดลอกเฉพาะไฟล์บางส่วน
- ห้ามติดตั้งไปยัง workspace ชั่วคราวแล้วอ้างว่าเป็น user-level skill
- ห้ามถามให้ผู้ใช้คัดลอกคำสั่งทีละบรรทัด หาก Codex สามารถดำเนินการคำสั่งตามเอกสารได้
- ห้ามข้ามการปิดและเปิด Codex ใหม่หลังติดตั้ง

### ผลลัพธ์ที่ต้องแจ้งผู้ใช้

หลังตรวจไฟล์ครบ ให้แจ้งสรุปสั้น ๆ ว่า:

```text
PASADU_INSTALLED
ตำแหน่ง: %USERPROFILE%\.codex\skills\pasadu
ขั้นตอนถัดไป: ปิดและเปิด Codex ใหม่ แล้วเริ่ม task ใหม่
```

หลังผู้ใช้เปิด Codex ใหม่และเริ่ม task ใหม่แล้ว จึงถือว่า skill พร้อม discover และใช้งานได้ ผู้ใช้สามารถถามคำถามพัสดุตามธรรมชาติ หรือใช้ `/pasadu` หาก environment แสดง alias นี้

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

## ใช้งานบน ChatGPT Work

ChatGPT Work ใน Codex Desktop App สามารถ discover และ activate Pasadu ที่ติดตั้งไว้ใน user-level Codex skills directory ได้:

```text
%USERPROFILE%\.codex\skills\pasadu\
```

ให้ติดตั้ง Pasadu ตามหัวข้อ [ติดตั้งบน Codex Windows App](#ติดตั้งบน-codex-windows-app) ก่อน แล้วปิดและเปิด ChatGPT/Codex Desktop App ใหม่

### วิธีใช้งาน

1. เลือก `Work` จากตัวเลือกโหมดด้านบนของหน้าต่าง ChatGPT
2. เริ่มงานใหม่
3. ถามคำถามด้านพัสดุตามธรรมชาติ

ตัวอย่าง:

```text
วิธีเฉพาะเจาะจงใช้ได้ในกรณีใด กรุณาอ้างตัวบท
```

```text
เรื่องใดที่ผู้ยื่นข้อเสนออุทธรณ์ไม่ได้
```

Work จะตรวจ intent จาก `name` และ `description` ใน `SKILL.md` หากตรงกับขอบเขต Pasadu ระบบจะแสดง skill `Pasadu` และ activate skill เพื่ออ่านคำสั่งกับ reference ที่อยู่ใน directory เดียวกัน

ถ้า auto-trigger ไม่ทำงาน ให้ระบุชื่อ skill โดยตรง:

```text
ใช้ skill pasadu ตอบคำถามนี้: วงเงินเล็กน้อยไม่ทำข้อตกลงเป็นหนังสือได้ไหม
```

### `/pasadu` และ `/passadu`

Pasadu รองรับ `/pasadu` และ `/passadu` เป็นข้อความ trigger ตามกติกาใน `SKILL.md` แต่ไม่ได้หมายความว่าทั้งสองคำจะปรากฏเป็น native slash command ในเมนูของ Work ทุกเวอร์ชัน

ถ้าพิมพ์ slash command แล้ว UI ไม่รู้จัก ให้ใช้คำถามตามธรรมชาติหรือ `ใช้ skill pasadu ...` แทน ไม่จำเป็นต้องใส่ slash ทุกครั้ง

### ตรวจว่า Work โหลด skill แล้วหรือไม่

สังเกตชื่อหรือ chip `Pasadu` ในข้อความตอบ หากต้องการตรวจโดยตรง ให้ถาม:

```text
เช็กสกิล pasadu และบอกว่าอ่าน SKILL.md กับ reference อะไรได้บ้าง
```

คำตอบควรกล่าวถึง `SKILL.md`, `pasadu.md` และ reference ด้านกฎหมาย/ระเบียบ/กฎกระทรวง/หนังสือเวียนที่ติดตั้งอยู่

### ขอบเขตของ Work

- เหมาะสำหรับถามตอบ วิเคราะห์ และอธิบายงานพัสดุจาก reference ใน Pasadu
- ความสามารถรัน Python, แก้ repository, commit หรือใช้ terminal ขึ้นกับ tools ที่ Work เปิดให้ใน session นั้น
- งานพัฒนา routing, regenerate index, tests และ Git workflow ควรใช้ Codex
- งานถามตอบทั่วไปไม่ต้องเปลี่ยนไป Codex หาก Work แสดงว่า Pasadu ถูก activate แล้ว

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

## ติดตั้งบน Gemini CLI

Pasadu ใช้งานกับ Gemini CLI ได้ในรูปแบบ Agent Skill เพราะ repository มี `SKILL.md` ที่ root และรวม reference, retrieval scripts, index, tests และเอกสารประกอบไว้ใน directory เดียวกัน

Gemini CLI ค้น skill จาก:

- User scope: `~/.gemini/skills/` หรือ `~/.agents/skills/`
- Workspace scope: `.gemini/skills/` หรือ `.agents/skills/`

ควรใช้ Gemini CLI รุ่นล่าสุดที่รองรับ Agent Skills:

```powershell
npm install -g @google/gemini-cli@latest
gemini --version
```

### วิธีแนะนำ: ติดตั้งด้วย Gemini CLI

รันคำสั่งนี้จาก terminal ปกติ ไม่ใช่ภายใน interactive Gemini session:

```powershell
gemini skills install https://github.com/RobbyGrean/PassaduAIagent.git --scope user
```

Gemini จะแสดงรายละเอียดและขอ consent ก่อนติดตั้ง ตรวจข้อมูลให้เรียบร้อยแล้วจึงยืนยัน หากต้องการติดตั้งเฉพาะ workspace ปัจจุบัน ใช้:

```powershell
gemini skills install https://github.com/RobbyGrean/PassaduAIagent.git --scope workspace
```

เปิด Gemini CLI แล้วตรวจว่า discover skill ได้:

```text
/skills list all
/skills reload
```

จากนั้นถามตามธรรมชาติ เช่น:

```text
วิธีเฉพาะเจาะจงใช้ได้ในกรณีใด กรุณาอ้างตัวบท
```

หรือระบุชื่อ skill โดยตรง:

```text
ใช้ skill pasadu อธิบายว่าเรื่องใดอุทธรณ์ไม่ได้
```

Gemini จะตรวจ intent และขออนุญาต activate skill เมื่อคำถามตรงกับ description ของ Pasadu เครื่องมือ `activate_skill` ถูกเรียกโดย Gemini agent ไม่ใช่คำสั่งที่ผู้ใช้เรียกเอง

> `/pasadu` และ `/passadu` เป็น textual aliases ที่ Pasadu เข้าใจ แต่ไม่ได้สร้าง native Gemini slash command ให้อัตโนมัติ หาก Gemini แจ้งว่าไม่รู้จัก slash command ให้ถามตามธรรมชาติหรือใช้ `ใช้ skill pasadu ...` แทน

### วิธี manual: Clone เป็น user skill

วิธีนี้เหมาะเมื่ออยากควบคุมการ update ด้วย Git โดยตรง

#### Windows PowerShell

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.gemini\skills" | Out-Null
git clone https://github.com/RobbyGrean/PassaduAIagent.git "$env:USERPROFILE\.gemini\skills\pasadu"
```

#### macOS และ Linux

```bash
mkdir -p ~/.gemini/skills
git clone https://github.com/RobbyGrean/PassaduAIagent.git ~/.gemini/skills/pasadu
```

โครงสร้างที่ถูกต้อง:

```text
~/.gemini/skills/pasadu/SKILL.md
~/.gemini/skills/pasadu/pasadu.md
~/.gemini/skills/pasadu/reference/
~/.gemini/skills/pasadu/scripts/pasadu/
```

หลัง clone ให้เปิด Gemini CLI ใหม่หรือรัน `/skills reload`

### อัปเดต Gemini CLI skill ที่ clone แบบ manual

#### Windows PowerShell

```powershell
git -C "$env:USERPROFILE\.gemini\skills\pasadu" pull --ff-only
```

#### macOS และ Linux

```bash
git -C ~/.gemini/skills/pasadu pull --ff-only
```

หลัง update ให้รัน `/skills reload` หรือเริ่ม Gemini CLI session ใหม่

### ทดสอบ retrieval scripts ใน Gemini installation

```powershell
Set-Location "$env:USERPROFILE\.gemini\skills\pasadu"
python scripts\pasadu\build_index.py
python scripts\pasadu\route_query.py "วิธีเฉพาะเจาะจงใช้กรณีใด" --json
python -m unittest discover -s tests -v
```

คำถามวิธีเฉพาะเจาะจงควร route ตามลำดับ `prb60.md` มาตรา 56 → กฎกระทรวงเจาะจง → `rbb60.md`

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

## แหล่งอ้างอิงเกี่ยวกับ Agent Skills

- OpenAI — Build skills: <https://developers.openai.com/codex/skills/>
- OpenAI — Slash commands: <https://learn.chatgpt.com/docs/reference/slash-commands>
- Gemini CLI — Agent Skills: <https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/skills.md>
- Gemini CLI — Activate skill tool: <https://github.com/google-gemini/gemini-cli/blob/main/docs/tools/activate-skill.md>
