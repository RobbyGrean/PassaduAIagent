# E-CPP COST Handoff

วันที่ส่งต่อ: 2026-07-02

## เป้าหมายงาน

งานนี้คือ E-CPP COST แบบ compact ingest สำหรับเก็บข้อสอบและภาพจริงประกอบข้อสอบ

สถานะล่าสุด:

- เก็บครบแล้ว: Q1-Q10
- Batch ที่เสร็จแล้ว: `e-cpp-cost/batches/batch-01.md`
- ข้อมูลขาดตอนนี้: 0 รายการ
- ยังไม่ได้ทำ HTML
- ยังไม่ได้ทำสรุปยาว
- พร้อมเริ่มรอบถัดไป: Q11-Q20

## โครงสร้างไฟล์ที่ต้องย้ายไปเครื่องใหม่

ให้ copy ทั้งโฟลเดอร์นี้ไปเครื่องใหม่โดยคงโครงสร้างเดิม:

```text
e-cpp-cost/
  assets/
    crops/
      q01-flow.png
      q01-main.png
      q02-cost.png
      q02-main.png
      q02-standard.png
      q03-main.png
      q04-main.png
      q05-main.png
      q06-main.png
      q07-main.png
      q08-main.png
      q09-main.png
      q10-main.png
  batches/
    batch-01.md
```

ไฟล์ handoff นี้:

```text
e-cpp-cost-handoff-2026-07-02.md
```

ไฟล์ spec สำหรับทำเว็บ/print/presentation:

```text
e-cpp-cost-web-output-spec.md
```

## กรณีโหลดจาก Google Drive แบบวางไฟล์ไว้ root

ถ้าใน Google Drive วางไฟล์แบบนี้:

```text
migration ver2/
  assets/
  batches/
  e-cpp-cost-handoff-2026-07-02.md
```

ถือว่าใช้ได้เช่นกัน โฟลเดอร์ `migration ver2/` คือ root งานชั่วคราว

หลังดาวน์โหลดลงเครื่องใหม่ มี 2 วิธีเลือกอย่างใดอย่างหนึ่ง:

### วิธี A: ใช้ root ตามที่ดาวน์โหลดมา

ใช้ path แบบนี้:

```text
assets/crops/
batches/batch-01.md
e-cpp-cost-handoff-2026-07-02.md
```

ถ้าใช้วิธีนี้ เวลา prompt agent ให้บอกว่า:

```text
โฟลเดอร์งานนี้ไม่มี e-cpp-cost/ ครอบ
ให้ถือว่าโฟลเดอร์ปัจจุบันคือ root งาน
ไฟล์ batch อยู่ที่ batches/batch-01.md
ภาพอยู่ที่ assets/crops/
```

### วิธี B: สร้างโฟลเดอร์ e-cpp-cost ครอบ

สร้างโฟลเดอร์ใหม่ชื่อ `e-cpp-cost/` แล้วลาก `assets/` และ `batches/` เข้าไปไว้ข้างใน:

```text
e-cpp-cost/
  assets/
  batches/
e-cpp-cost-handoff-2026-07-02.md
```

วิธีนี้จะตรงกับ path เดิมใน handoff มากที่สุด

## Checklist หลังดาวน์โหลดลงเครื่องใหม่

ก่อนเริ่ม Q11 ให้ตรวจให้ครบ:

- มีไฟล์ handoff: `e-cpp-cost-handoff-2026-07-02.md`
- มีไฟล์ spec เว็บถ้าจะทำ output: `e-cpp-cost-web-output-spec.md`
- มี batch เดิม: `batches/batch-01.md` หรือ `e-cpp-cost/batches/batch-01.md`
- `batch-01.md` มีหัวข้อ `## ข้อ 1` ถึง `## ข้อ 10`
- มีโฟลเดอร์ภาพ: `assets/crops/` หรือ `e-cpp-cost/assets/crops/`
- ใน `crops/` มีภาพ 13 ไฟล์:
  - `q01-flow.png`
  - `q01-main.png`
  - `q02-cost.png`
  - `q02-main.png`
  - `q02-standard.png`
  - `q03-main.png`
  - `q04-main.png`
  - `q05-main.png`
  - `q06-main.png`
  - `q07-main.png`
  - `q08-main.png`
  - `q09-main.png`
  - `q10-main.png`
- ยังไม่มี `batch-02.md` ถือว่าปกติ ให้สร้างใหม่ตอนเริ่ม Q11

## สถานะ batch-01

`e-cpp-cost/batches/batch-01.md` มี Q1-Q10 แล้ว:

- Q1: คณะอนุกรรมการ CoST
- Q2: ข้อตกลงคุณธรรม
- Q3: เว็บไซต์ CoST
- Q4: ชื่อเต็มของโครงการ CoST
- Q5: จำนวนข้อมูลที่เจ้าหน้าที่ต้องเปิดเผยในระบบ CoST
- Q6: จำนวนรายการที่ไม่ได้ดึงจากระบบ e-GP อัตโนมัติ
- Q7: มูลค่าโครงการก่อสร้างที่ต้องแจ้งเข้าร่วม CoST
- Q8: จำนวนวันที่ต้องรายงานโครงการผ่านเว็บไซต์ CoST Thailand
- Q9: จำนวนขั้นตอนหลักในระบบ CoST Thailand
- Q10: องค์ประกอบของ CoST

## กติกาสำคัญ

- รับข้อมูลข้อสอบแบบ compact ต่อข้อ
- ห้ามเดาคำตอบเอง
- ห้าม generate ภาพใหม่
- ใช้ภาพจริงจากผู้ใช้เท่านั้น
- Copy ภาพจริงไปที่ `e-cpp-cost/assets/crops/`
- ถ้าข้อมูลไม่พอ ให้ใส่ `ต้องตรวจคู่มือเพิ่ม`
- ตอบสั้นว่าเก็บแล้ว + ข้อมูลขาด
- ยังไม่ต้องทำ HTML ระหว่าง ingest
- ยังไม่ต้องสรุปยาวระหว่าง ingest

## วิธีทำ Q11-Q20 ต่อ

ให้สร้างไฟล์ใหม่:

```text
e-cpp-cost/batches/batch-02.md
```

หัวไฟล์:

```text
# Batch 02: E-CPP COST
```

จากนั้นรับ Q11-Q20 ต่อในไฟล์นี้ ห้ามต่อท้าย `batch-01.md`

ภาพให้เก็บต่อในโฟลเดอร์เดิม:

```text
e-cpp-cost/assets/crops/
```

ตั้งชื่อภาพต่อจากเลขข้อ:

```text
q11-main.png
q12-main.png
q13-main.png
...
q20-main.png
```

ถ้าข้อหนึ่งมีหลายภาพ ให้ตั้งชื่อแบบนี้:

```text
q11-main.png
q11-flow.png
q11-standard.png
```

เลือก suffix ให้ตรงกับเนื้อหาภาพจริง

## Format รับข้อมูลต่อข้อ

```text
Q11
Topic:
Key:
ถาม:
ก:
ข:
ค:
ง:
ตอบ:
ภาพ:
เหตุ:
จำ:
หลอก:
```

สามารถรับรูปแบบยาวได้ด้วย เช่น:

```text
Q11

Topic:
Keyword:
คำถาม:
ตัวเลือก:
ก.
ข.
ค.
ง.
เฉลย:
ภาพ:
เหตุผล:
หลักคิด:
จุดหลอก:
```

ให้บันทึกลง markdown โดยใช้รูปแบบเดียวกับ `batch-01.md`

## Prompt เริ่มงานบนเครื่องใหม่

ใช้ prompt นี้ใน Codex เครื่องใหม่:

```text
อ่าน e-cpp-cost-handoff-2026-07-02.md และ e-cpp-cost/batches/batch-01.md
งานนี้คือ E-CPP COST แบบ compact ingest
ตอนนี้เก็บ Q1-Q10 ครบแล้วใน batch-01.md
ให้เริ่มรอบใหม่โดยสร้าง e-cpp-cost/batches/batch-02.md สำหรับ Q11-Q20
copy ภาพจริงไป e-cpp-cost/assets/crops/
ห้าม generate ภาพใหม่
ห้ามเดาคำตอบเอง
ถ้าข้อมูลไม่พอให้ใส่ "ต้องตรวจคู่มือเพิ่ม"
ยังไม่ต้องทำ HTML
ยังไม่ต้องสรุปยาวระหว่าง ingest
ตอบสั้นว่าเก็บแล้ว + ข้อมูลขาด
ถ้าพร้อม ให้ตอบว่า "พร้อมรับ Q11"
```

## Prompt สรุป knowledge pack จาก Q1-Q10

ถ้าต้องการสรุป batch-01 ก่อน ให้ใช้ prompt นี้:

```text
จาก e-cpp-cost/batches/batch-01.md ช่วยสรุปเป็น knowledge pack รอบแรก
จัดตาม topic ไม่ต้องเรียงตามข้อ
แยกเป็น:
1. แก่นความรู้
2. หลักคิดเวลาเจอโจทย์
3. Pattern ข้อสอบ
4. จุดหลอก
5. Checklist ก่อนสอบ
6. Flashcards สั้น ๆ
ใช้เฉพาะข้อมูลใน batch ห้ามเดาเพิ่ม
ถ้าข้อมูลไม่พอ ใส่ "ต้องตรวจคู่มือเพิ่ม"
```

## Prompt สรุปหลังครบ Q11-Q20

หลังเก็บ Q11-Q20 ครบใน `batch-02.md` ให้ใช้:

```text
จาก e-cpp-cost/batches/batch-02.md ช่วยสรุปเป็น knowledge pack รอบสอง
จัดตาม topic ไม่ต้องเรียงตามข้อ
แยกเป็น:
1. แก่นความรู้
2. หลักคิดเวลาเจอโจทย์
3. Pattern ข้อสอบ
4. จุดหลอก
5. Checklist ก่อนสอบ
6. Flashcards สั้น ๆ
ใช้เฉพาะข้อมูลใน batch ห้ามเดาเพิ่ม
ถ้าข้อมูลไม่พอ ใส่ "ต้องตรวจคู่มือเพิ่ม"
```

## Prompt สรุปรวมหลาย batch

ถ้าต้องการรวม `batch-01.md` และ `batch-02.md`:

```text
จาก e-cpp-cost/batches/batch-01.md และ e-cpp-cost/batches/batch-02.md
ช่วยสรุปเป็น knowledge pack รวม
จัดตาม topic ไม่ต้องเรียงตามข้อ
แยกเป็น:
1. แก่นความรู้
2. หลักคิดเวลาเจอโจทย์
3. Pattern ข้อสอบ
4. จุดหลอก
5. Checklist ก่อนสอบ
6. Flashcards สั้น ๆ
ใช้เฉพาะข้อมูลใน batch ห้ามเดาเพิ่ม
ถ้าข้อมูลไม่พอ ใส่ "ต้องตรวจคู่มือเพิ่ม"
```

## หมายเหตุ

- `batch-01.md` คือก้อนปิด Q1-Q10 แล้ว อย่าเพิ่ม Q11 ต่อท้ายไฟล์นี้
- `batch-02.md` คือก้อนใหม่สำหรับ Q11-Q20
- ภาพทั้งหมดเก็บรวมใน `assets/crops/`
- หาก user ส่งภาพจาก clipboard/temp ให้ copy ไฟล์ภาพจริงเข้ามาใน `assets/crops/` ทุกครั้งก่อนตอบว่าเก็บแล้ว
