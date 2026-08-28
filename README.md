# UDH Hospital Indoor Navigation & High-Value Asset Tracking System

ระบบแผนที่นำทางภายในอาคาร โรงพยาบาลอุดรธานี (UDH Navigator) และระบบติดตามพัสดุการแพทย์ราคาสูง (UDH RTLS High-Value Asset & Medical Parcel Tracking System)

พัฒนาในรูปแบบ **High Performance Static Web App + Single JSON Data Store** โดยประมวลผลอัลกอริทึมคำนวณเส้นทางสั้นที่สุด (Dijkstra Shortest Path Engine) แบบ Client-Side ปลอดภัย ไร้กังวลเรื่องการตั้งค่า Database สำหรับระยะทดสอบ และสามารถเชื่อมต่อฐานข้อมูล RTLS จริงในอนาคตได้ทันที

---

## 🚀 การเปิดใช้งานบนเครื่อง Local

ต้องเปิดรันผ่าน Local Web Server เพื่อให้เว็บเบราว์เซอร์อ่านไฟล์ `map-data.json` ได้ผ่าน Fetch API:

```powershell
cd D:\Codex\UDHMapAI
python -m http.server 8080
```

เปิดเว็บเบราว์เซอร์ไปที่: [http://localhost:8080](http://localhost:8080)

---

## 📱 ระบบหน้าจอและการใช้งาน (Web Modules)

### 1. ระบบนำทางผู้ป่วย (Patient Mobile Interface)
- `index.html` — หน้าหลักนำทางผู้ป่วย: ค้นหาห้องตรวจ คลินิก จุดบริการ ชำระเงิน และห้องยา สลับโหมดเดินปกติ vs โหมดรถเข็น ♿ (เลี่ยงบันได)
- `navigation.html` — หน้าจอนำทางแบบ Turn-by-Turn: บอกทิศทางและระยะทางคงเหลือทีละก้าว พร้อมการสลับชั้นนำทางข้ามชั้น
- `check-in.html` — หน้าเช็กอินใบนัดหมาย: จำลองการสแกน QR Code เพื่อเริ่มนำทางไปยังห้องตรวจทันที
- `building-select.html` — หน้าผังบริเวณโรงพยาบาลอุดรธานี: ดูภาพรวมผังอาคารและเลือกตึกที่ต้องการ

### 2. ระบบติดตามพัสดุราคาสูงสำหรับเจ้าหน้าที่ (High-Value Asset & Parcel Tracking RTLS)
- `asset-tracking.html` — แดชบอร์ดติดตามพัสดุทางการแพทย์ราคาสูง (ยาราคาสูงเฉพาะราย, ถุงเลือดฉุกเฉิน, เครื่องช่วยหายใจ, เครื่องปั๊มสารน้ำ):
  - 📡 มอนิเตอร์พิกัดเรียลไทม์บนแผนที่ 2 มิติ พร้อมระดับแบตเตอรี่แท็ก BLE/UWB
  - 🚨 ระบบแจ้งเตือนฉุกเฉิน (Geofence Breach Alarm) เมื่อมีอุปกรณ์ย้ายออกนอกโซนประจำ
  - 🚚 ระบบติดตามห่วงโซ่พัสดุ (Chain of Custody & Temp Control) พร้อมการจำลองการจัดส่ง (Simulate Transit)

### 3. ระบบบริหารจัดการหลังบ้าน (Admin Map Studio CMS)
- `map-builder.html` — Map Studio: เพิ่ม/แก้ไขอาคาร ชั้น ห้อง จุดสนใจ (POI) และปักจุดเดิน (Route Nodes) พร้อมการผูก ID ฮาร์ดแวร์ Beacon/Asset Tag
- `map-data.json` — แหล่งข้อมูลสเปกกลางสำหรับแผนที่ พิกัด และพัสดุราคาสูง

---

## 🛠️ สถาปัตยกรรมและเทคโนโลยีสำคัญ
- **Pathfinding Engine (`pathfinding.js`)**: คำนวณเส้นทางเดินแบบสั้นที่สุดรองรับเงื่อนไข Multi-Floor และ Wheelchair Filter
- **Interactive SVG Overlay**: แสดงเส้นทางการเดินสีน้ำเงินเหนือบอร์ดแผนที่อัตโนมัติ
- **Local Data Storage Sync (`data-store.js`)**: บันทึกการเปลี่ยนแปลงข้อมูลลงใน LocalStorage ของเบราว์เซอร์ พร้อมเมนู Export / Import JSON

> ⚠️ **คำเตือนความปลอดภัย**: ห้ามเก็บข้อมูลส่วนบุคคลของผู้ป่วยจริง เช่น HN, ชื่อผู้ป่วย หรือประวัติการรักษา ลงในไฟล์ `map-data.json` ที่เผยแพร่สาธารณะ
