# INSTALLATION

คู่มือนี้สรุปวิธีเริ่มใช้งาน `PassaduAIagent` ให้เหมาะกับ 2 กลุ่มหลัก:

1. คนที่อยากใช้งานเร็วผ่าน `Claude.ai` แบบฟรี
2. คนที่ต้องการนำ repo นี้ไปใช้ต่อกับ `Claude Code`, `Codex`, local AI หรือระบบ agent ของตัวเอง

## ทางเลือกที่ 1: ใช้ Claude.ai ฟรีผ่านหน้าเว็บคู่มือ

ถ้าต้องการเริ่มเร็วที่สุด ให้ใช้คู่มือแบบภาพทีละขั้นที่หน้า:

<https://robbygrean.github.io/PassaduAIagent/how2agent/>

แนวทางนี้เหมาะสำหรับ:

- ผู้ใช้ที่ยังไม่ต้องการติดตั้ง runtime เอง
- ผู้ใช้ที่อยากทดลองถามตอบใน `Claude Project`
- ผู้ใช้ที่ต้องการผูก repo นี้เข้ากับ GitHub แล้วใช้งานผ่านหน้าเว็บ

สิ่งที่ต้องใช้:

- บัญชี `Claude.ai`
- บัญชี `GitHub`
- การสร้าง `Project` ใน Claude
- การเพิ่มไฟล์จาก repo นี้เข้า Project

ไฟล์ที่ควรเลือกเข้า Project:

- `reference/`
- `scripts/`
- `README.md`
- `SKILL.md`
- `pasadu.md`

## ทางเลือกที่ 2: ใช้ repo นี้เป็นฐานสำหรับ agent ของตัวเอง

แนวทางนี้เหมาะสำหรับ:

- `Claude Code`
- `Codex`
- local AI ที่รองรับการใส่ system prompt / context file
- workflow แบบ RAG หรือ retrieval pipeline
- นักพัฒนาที่ต้องการแก้กฎการตอบ เพิ่มฐานอ้างอิง หรือสร้าง runtime เอง

### 1. Clone repository

```bash
git clone https://github.com/RobbyGrean/PassaduAIagent.git
cd PassaduAIagent
```

### 2. ทำความเข้าใจไฟล์หลัก

- `pasadu.md` คือ persona, ข้อบังคับการตอบ, รูปแบบคำตอบ, และข้อห้าม
- `SKILL.md` คือกติกาการ route งานและเลือกแหล่งอ้างอิง
- `reference/law/prb60.md` คือพระราชบัญญัติ
- `reference/law/rbb60.md` คือระเบียบหลัก
- `scripts/pasadu/` คือสคริปต์ช่วย routing, retrieval, citation check, และ eval

### 3. แนวทางใช้งานกับ Claude Code หรือ Codex

ให้นำสาระจาก `pasadu.md`, `SKILL.md`, และ reference หลักไปใส่เป็นบริบทของ agent ที่คุณสร้าง โดยยึดหลักนี้:

- ห้ามให้โมเดลตอบจากความจำล้วน
- บังคับให้ค้นจาก `prb60.md` หรือ `rbb60.md` ก่อนสรุป
- ถ้าไม่พบฐานอ้างอิง ให้ตอบตามจริงว่าไม่พบ
- ถ้าคำถามกำกวม ให้ถามข้อมูลเพิ่มก่อน
- ถ้าต้องค้นเว็บ ให้ใช้แหล่งทางการก่อน

รูปแบบการประกอบ agent ขั้นต้น:

1. โหลด `pasadu.md` เป็น system rules หลัก
2. ใช้ `SKILL.md` เป็น routing/rules supplement
3. เปิดให้ agent เข้าถึง `reference/law/prb60.md` และ `reference/law/rbb60.md`
4. ถ้าต้องการ retrieval ที่เร็วขึ้น ให้ใช้สคริปต์ใน `scripts/pasadu/`
5. บังคับรูปแบบคำตอบเป็น: ข้อสรุป, ฐานกฎหมาย, เหตุผลประกอบ, ข้อควรระวัง

### 4. ติดตั้ง Python สำหรับสคริปต์ retrieval

ถ้าต้องการใช้สคริปต์ที่มีใน repo ให้ติดตั้ง `Python 3.10+` ก่อน

ตรวจเวอร์ชัน:

```bash
python --version
```

จากนั้นลองรันสคริปต์ตามลำดับนี้:

```bash
python scripts/pasadu/build_index.py
python scripts/pasadu/route_query.py "มาตรา 56 กล่าวถึงอะไร"
python scripts/pasadu/retrieve.py "วิธีเฉพาะเจาะจงใช้กรณีใด" --limit 5
python scripts/pasadu/answer_context.py "คณะกรรมการตรวจรับพัสดุต้องดูจากข้อไหน"
python scripts/pasadu/cite_check.py --text "อ้างอิง: reference/law/prb60.md มาตรา 56"
python scripts/pasadu/eval_queries.py
```

### 5. แนวทางใช้งานกับ local AI

ถ้าคุณใช้ local AI เช่นผ่าน UI หรือ runtime ของตัวเอง ให้ตั้งค่าประมาณนี้:

- System prompt: ใช้หลักจาก `pasadu.md`
- Routing rules: ใช้หลักจาก `SKILL.md`
- Knowledge base หลัก: `reference/law/prb60.md` และ `reference/law/rbb60.md`
- Optional retrieval layer: ใช้ index/chunk จาก `scripts/pasadu/build_index.py`

แนวคิดสำคัญคือให้โมเดล “อ่านก่อนตอบ” ไม่ใช่ “เดาก่อนแล้วค่อยหาเหตุผลมารองรับ”

## คำแนะนำการใช้งานจริง

- ถ้าใช้งานในระดับทดลอง เริ่มจากหน้าเว็บคู่มือจะเร็วที่สุด
- ถ้าต้องการต่อยอดเป็น agent จริง ให้เริ่มจาก repo หลักและอ่าน `pasadu.md` กับ `SKILL.md` ก่อน
- ถ้าต้องการความแม่นยำเพิ่ม ควรเพิ่มฐานข้อมูลหนังสือเวียน แนววินิจฉัย และเอกสารจากแหล่งทางการในอนาคต

## ข้อจำกัดสำคัญ

repo นี้เป็นฐานสำหรับ AI ผู้ช่วยงานพัสดุ ไม่ใช่คำวินิจฉัยทางกฎหมายอย่างเป็นทางการ

หากคำตอบจะถูกนำไปใช้กับ:

- การอนุมัติงบประมาณ
- การจัดซื้อจัดจ้างจริง
- การทำสัญญา
- การตรวจรับ
- การวินิจฉัยข้อกฎหมายหรือความรับผิดของเจ้าหน้าที่

ควรตรวจสอบกับตัวบทและแหล่งทางการอีกครั้งเสมอ
