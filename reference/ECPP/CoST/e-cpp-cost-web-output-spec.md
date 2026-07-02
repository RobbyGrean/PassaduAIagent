# E-CPP COST Web Output Spec

วันที่จัดทำ: 2026-07-02

## เป้าหมาย

สร้างเว็บอ่านทบทวนจากข้อมูลข้อสอบ E-CPP COST ที่เก็บใน batch markdown และภาพจริงใน `assets/crops/`

ต้องรองรับ 3 รูปแบบในไฟล์เดียว:

1. Study Mode สำหรับอ่านบนมือถือ/desktop
2. Print Mode สำหรับพิมพ์ A4 หรือ save เป็น PDF
3. Presentation Mode สำหรับฉายสไลด์ 16:9

ห้ามสร้างหรือ generate ภาพใหม่ ใช้เฉพาะภาพจริงใน `assets/crops/`

## Source Data

ใช้ข้อมูลจาก:

```text
batches/batch-01.md
assets/crops/
```

ถ้าโปรเจคมีโฟลเดอร์ครอบ:

```text
e-cpp-cost/batches/batch-01.md
e-cpp-cost/assets/crops/
```

หลังมี Q11-Q20 ให้เพิ่ม:

```text
batches/batch-02.md
```

กติกา:

- ใช้เฉพาะข้อมูลใน batch
- ห้ามเดาเพิ่ม
- ถ้าข้อมูลไม่พอ ใส่ `ต้องตรวจคู่มือเพิ่ม`
- ภาพทุกภาพต้องอ้าง path จริง เช่น `../assets/crops/q10-main.png`

## Output Files

แนะนำทำเป็นไฟล์เดียวก่อน:

```text
output/knowledge-pack-01.html
```

ถ้าต้องแยกภายหลัง:

```text
output/knowledge-pack-01.html
output/summary-cards-01.html
output/presentation-01.html
```

แต่ default ให้ทำไฟล์เดียว self-contained:

- HTML, CSS, JS อยู่ในไฟล์เดียว
- รูปภาพอ้างจาก `../assets/crops/`
- เปิดผ่าน browser ได้ทันที
- ไม่ต้องมี build step
- ไม่ต้องพึ่ง internet/CDN

## Required Modes

### 1. Study Mode

ใช้สำหรับอ่านบนมือถือและ desktop

Features:

- Responsive layout
- Mobile first
- Sticky top toolbar
- Search keyword
- Filter ตามหมวด:
  - ตัวเลข
  - ขั้นตอน
  - องค์ประกอบ
  - URL
  - เกณฑ์วงเงิน
  - จุดหลอก
- Q map Q1-Q10
- Topic cards
- Collapsible sections:
  - เฉลย
  - เหตุผล
  - หลักคิด
  - จุดหลอก
  - ภาพ
- Flashcards แบบ tap-to-reveal
- Progress checklist อ่านแล้ว/ยังไม่อ่าน
- ปุ่ม Expand all
- ปุ่ม Collapse all
- ปุ่ม Print
- ปุ่ม Present
- ใช้ภาพจริงประกอบใน card

Mobile rules:

- 1 column
- ข้อความไม่ล้นจอ
- ปุ่มใหญ่พอกดง่าย
- ภาพย่อพอดีความกว้างจอ
- ใช้ `position: sticky` เฉพาะ toolbar ไม่บังเนื้อหา
- หลีกเลี่ยง layout ที่ต้อง zoom

Desktop rules:

- 2 columns ได้
- มี sidebar หรือ quick nav ได้
- content width ไม่กว้างเกินอ่านยาก

### 2. Print Mode

ใช้สำหรับพิมพ์หรือ save PDF

ต้องมี `@media print`

Features:

- A4 portrait
- ปุ่ม/toolbar/interactive controls ต้องซ่อนตอน print
- Flashcards ตอน print ต้องแสดงทั้งคำถามและคำตอบ
- Collapsible content ต้องถูกเปิดทั้งหมดตอน print
- ภาพต้องย่อพอดีหน้า ไม่ล้นกระดาษ
- ใช้สีประหยัดหมึก
- high contrast
- มี page title และวันที่/ชื่อชุด
- มีเลขหน้า ถ้าทำได้ด้วย CSS
- ใช้ `break-inside: avoid` กับ card/topic
- หลีกเลี่ยงตัด card กลางหน้า

Print sections:

1. Fast Recall
2. ตัวเลขต้องจำ
3. หลักคิดเวลาเจอโจทย์
4. Pattern ข้อสอบ
5. จุดหลอก
6. Checklist ก่อนสอบ
7. Flashcards สั้น ๆ
8. Q map Q1-Q10
9. ภาพประกอบสำคัญ

เป้าหมาย:

- A4 Cheat Sheet: 1-3 หน้า
- Full Knowledge Pack: 5-10 หน้า

### 3. Presentation Mode

ใช้ฉายสไลด์ 16:9 หน้าห้องหรือผ่านโปรเจกเตอร์

Features:

- ปุ่ม `Present`
- Fullscreen API
- Slide deck 16:9
- ข้อความใหญ่
- อ่านชัดจากระยะไกล
- 1 slide = 1 idea
- ใช้ภาพจริงประกอบ
- รูปไม่ถูก crop จนเสียข้อมูล
- progress indicator เช่น `3 / 18`
- keyboard navigation:
  - `ArrowRight` หรือ `Space`: slide ถัดไป
  - `ArrowLeft`: slide ก่อนหน้า
  - `F`: fullscreen
  - `Esc`: ออกจาก presentation/fullscreen
- Mobile swipe ซ้าย/ขวา
- ปุ่ม previous/next สำหรับ touch
- ซ่อน toolbar ปกติใน presentation

Slide sizing:

```css
.slide {
  aspect-ratio: 16 / 9;
  width: min(100vw, 177.78vh);
  height: min(56.25vw, 100vh);
}
```

Presentation typography:

- Slide title: 40-64px
- Body: 26-36px
- Keyword/number: 48-72px
- ไม่ใช้ตัวเล็กกว่า 22px ยกเว้น caption

Suggested slides:

1. Title slide: E-CPP COST Q1-Q10
2. Fast Recall: ตัวเลขสำคัญ
3. CoST คืออะไร / ชื่อเต็ม
4. องค์ประกอบ CoST 4 องค์ประกอบ
5. 40 รายการต้องเปิดเผย
6. 40 = 25 e-GP + 15 กรอกเอง
7. เกณฑ์ อปท. 5,000,000 บาทขึ้นไป
8. หน่วยงานอื่นรายงานวงเงินสูงสุด 3 รายการ
9. รายงานภายใน 15 วันทำการ
10. ขั้นตอนปกติ 5 ขั้นตอน
11. ถ้าเปลี่ยนแปลงสัญญา = 6 ขั้นตอน
12. เว็บไซต์ CoST Thailand
13. MSG / AT / IO แยกบทบาท
14. จุดหลอก: Construction vs Infrastructure
15. จุดหลอก: 15 วัน vs 15 วันทำการ
16. จุดหลอก: 5 ล้าน ตั้งแต่/เกินกว่า
17. Flashcard drill
18. Final checklist ก่อนสอบ

## Content Model

แปลงแต่ละข้อเป็น object:

```js
{
  id: "Q1",
  topic: "",
  keyword: "",
  question: "",
  choices: {
    ก: "",
    ข: "",
    ค: "",
    ง: ""
  },
  answer: "",
  images: ["../assets/crops/q01-main.png"],
  reason: "",
  memory: "",
  trap: "",
  tags: ["ตัวเลข", "CoST"]
}
```

ถ้าข้อมูลบาง field ไม่มี:

```text
ต้องตรวจคู่มือเพิ่ม
```

## Knowledge Pack Sections

### 1. แก่นความรู้

สรุป topic หลักจาก batch ไม่เรียงตามข้อ

### 2. หลักคิดเวลาเจอโจทย์

เน้นวิธีแยกโจทย์ เช่น:

- เห็น อปท. + 5 ล้าน = แจ้งทุกโครงการ
- เห็น 40 รายการ = เปิดเผยทั้งหมด
- เห็นไม่ได้ดึงจาก e-GP = 15 รายการ
- เห็นขั้นตอนปกติ = 5 ขั้นตอน
- เห็นเปลี่ยนแปลงสัญญา = 6 ขั้นตอน

### 3. Pattern ข้อสอบ

รวบ pattern จากคำถาม เช่น:

- ถามตัวเลขตรง ๆ
- ถามคำเต็ม/ชื่อเต็ม
- ถาม URL
- ถามเกณฑ์วงเงิน
- ถามจำนวนวัน
- ถามองค์ประกอบ
- ถามขั้นตอน

### 4. จุดหลอก

ต้อง highlight ชัด:

- Construction Sector vs Infrastructure Transparency Initiative
- 40 รายการ vs 25/15 รายการ
- ดึงจาก e-GP ได้ vs ต้องกรอกเอง
- 15 วัน vs 15 วันทำการ
- ตั้งแต่ 5 ล้าน vs เกิน 5 ล้าน
- อปท. vs หน่วยงานอื่น
- 5 ขั้นตอน vs 6 ขั้นตอนเมื่อมีเปลี่ยนแปลงสัญญา
- องค์ประกอบ CoST vs บทบาท AT/IO

### 5. Checklist ก่อนสอบ

ทำเป็น checkbox ใน Study Mode และเป็น list ใน Print Mode

### 6. Flashcards

Study Mode:

- tap/click เพื่อเปิดคำตอบ

Print Mode:

- แสดงหน้า/หลังพร้อมกัน

Presentation Mode:

- 1 flashcard ต่อ slide

## UI Requirements

### Toolbar

ต้องมี:

- Search
- Filter
- Study button
- Print button
- Present button
- Expand all
- Collapse all

### Cards

Card ควรมี:

- Topic
- Keyword
- Question
- Choices
- Answer badge
- Reason
- Memory/หลักคิด
- Trap/จุดหลอก
- Images

สีแนะนำ:

- Answer: เขียวเข้ม
- Trap: แดง/ส้ม
- Memory: น้ำเงิน
- Number facts: เหลืองอ่อนหรือเส้นขอบเข้ม

ต้องไม่ใช้สีอ่อนจน print อ่านยาก

### Images

- ใช้ `loading="lazy"` ใน Study Mode
- มี alt text
- คลิกเพื่อดูภาพใหญ่ได้ใน Study Mode
- ใน Print Mode ให้ภาพอยู่ใต้หัวข้อที่เกี่ยวข้อง
- ใน Presentation Mode ให้ภาพใหญ่และไม่ crop ข้อมูลสำคัญ

## Accessibility

- ใช้ semantic HTML
- ปุ่มต้องเป็น `<button>`
- keyboard ใช้งานได้
- focus style ชัด
- contrast อ่านง่าย
- alt text สำหรับภาพ
- ไม่พึ่งสีอย่างเดียวในการสื่อความหมาย

## Print CSS Requirements

ต้องมีประมาณนี้:

```css
@media print {
  @page {
    size: A4 portrait;
    margin: 12mm;
  }

  .toolbar,
  .screen-only,
  .presentation-view {
    display: none !important;
  }

  .print-only {
    display: block !important;
  }

  body {
    background: white;
    color: #111;
  }

  .card,
  .topic-section,
  .flashcard {
    break-inside: avoid;
    box-shadow: none;
  }

  details,
  details[open] {
    display: block;
  }

  details > * {
    display: block;
  }
}
```

## JavaScript Requirements

ต้องรองรับ:

- mode switching
- search
- filters
- details expand/collapse
- flashcard reveal
- print trigger `window.print()`
- fullscreen presentation
- keyboard slide navigation
- swipe slide navigation
- local progress checklist โดยใช้ `localStorage`

ถ้า browser ไม่รองรับ fullscreen ให้ยังใช้ presentation mode ใน viewport ปกติได้

## Data Integrity Rules

- ห้ามแก้เฉลยเอง
- ห้ามเพิ่มข้อมูลนอก batch
- ห้ามใช้ภาพที่ไม่ได้อยู่ใน `assets/crops/`
- ถ้าสร้าง section สรุปแล้วไม่พบข้อมูลพอ ให้ใส่ `ต้องตรวจคู่มือเพิ่ม`
- ทุก statement สำคัญต้อง trace กลับไปหา Q ใน batch ได้
- ควรใส่ badge เช่น `จาก Q5`, `จาก Q8`

## Development Checklist

- สร้าง `output/knowledge-pack-01.html`
- เปิดบน desktop แล้ว layout ไม่แตก
- เปิด responsive mobile width 390px แล้วอ่านได้
- กด search/filter ได้
- กด flashcard reveal ได้
- กด print แล้ว preview เป็น A4
- Print preview ไม่มีปุ่ม toolbar
- Card ไม่ถูกตัดกลางหน้าแบบอ่านไม่รู้เรื่อง
- กด Present แล้วเป็น 16:9
- กด fullscreen ได้
- ใช้ keyboard เปลี่ยน slide ได้
- ภาพทุกภาพโหลดจาก `assets/crops/`
- ไม่มีการ generate ภาพใหม่

## Prompt สำหรับให้ agent สร้าง HTML

```text
อ่าน e-cpp-cost-web-output-spec.md และ batches/batch-01.md
สร้าง output/knowledge-pack-01.html จากข้อมูลใน batch-01.md เท่านั้น
ต้องเป็นไฟล์ HTML เดียว มี CSS/JS ในตัว และอ้างภาพจาก ../assets/crops/
ต้องมี 3 mode:
1. Study Mode responsive มือถือ/desktop
2. Print Mode A4 พร้อม @media print
3. Presentation Mode 16:9 พร้อม fullscreen และ keyboard navigation
ห้าม generate ภาพใหม่
ห้ามเดาข้อมูลเพิ่ม
ถ้าข้อมูลไม่พอให้ใส่ "ต้องตรวจคู่มือเพิ่ม"
หลังทำเสร็จให้บอก path ไฟล์และวิธีเปิด/print/present
```

## Prompt สำหรับเพิ่ม batch ถัดไป

```text
หลังมี batches/batch-02.md แล้ว
อัปเดต output/knowledge-pack-01.html ให้รองรับ batch-01 และ batch-02
ต้องคง Study/Print/Presentation Mode
เพิ่ม filter และ Q map ให้ครอบคลุม Q1-Q20
ใช้เฉพาะข้อมูลใน batch ห้ามเดาเพิ่ม
```
