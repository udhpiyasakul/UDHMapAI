# สรุปข้อมูลก่อนพัฒนา: UDH Hospital Indoor Navigation

## 1. เป้าหมายระบบ

ระบบแผนที่ภายในโรงพยาบาลสำหรับผู้ป่วยค้นหาอาคาร ชั้น ห้องตรวจ และรับเส้นทางเดิน โดยเจ้าหน้าที่สามารถสร้างหรือแก้ไขแผนที่ได้เอง และรองรับการติดตามทรัพย์สินในอนาคต

ระยะแรกใช้งานแบบ **Static Web App + JSON** โดยไม่ต้องมี Beacon, Host เฉพาะ หรือ Database และใช้ QR Code ตามจุดสำคัญเป็นตำแหน่งเริ่มต้น

## 2. หน้าจอระบบ

| กลุ่มผู้ใช้ | หน้าจอ | สถานะ |
|---|---|---|
| ผู้ป่วย | หน้าหลัก/แผนที่ | มี Mockup |
| ผู้ป่วย | เลือกอาคาร | มี Mockup |
| ผู้ป่วย | QR Check-in / ใบนัด | มี Mockup |
| ผู้ป่วย | นำทางเต็มหน้าจอ | มี Mockup |
| ผู้ป่วย | ค้นหาห้อง/แผนก | ควรเพิ่ม |
| ผู้ป่วย | เส้นทางข้ามอาคาร/เปลี่ยนชั้น | ควรเพิ่ม |
| ผู้ดูแล | Map Studio สร้างแผนที่ | มี Mockup |
| ผู้ดูแล | จัดการอาคารและชั้น | ควรเพิ่ม |
| ผู้ดูแล | Import / Export JSON | ควรเพิ่ม |
| เจ้าหน้าที่ | Asset Tracking | มี Mockup; ใช้เมื่อมีอุปกรณ์ระบุตำแหน่ง |
| ผู้ดูแล | Beacon / Geofence | ทำเมื่อมีงบอุปกรณ์ |

## 3. ฟังก์ชัน MVP

- เพิ่มอาคาร ชั้น ห้อง และจุดสนใจ (POI) เช่น ลิฟต์ ห้องน้ำ ห้องยา
- กำหนดเส้นทางเดิน
- ค้นหาจุดหมาย
- เลือกจุดเริ่มต้นหรือสแกน QR Code
- แสดงเส้นทางแบบทีละขั้น
- Import และ Export ไฟล์ `map-data.json`
- เผยแพร่ผ่าน Static Hosting

### สิ่งที่ไม่อยู่ใน MVP

- ระบุตำแหน่งผู้ป่วยอัตโนมัติ
- สลับชั้นอัตโนมัติ
- ติดตามทรัพย์สินแบบเรียลไทม์
- Beacon, UWB และ Geofence

## 4. Data Structure แบบ JSON

```json
{
  "version": "1.0",
  "hospital": {
    "id": "udh",
    "name": "โรงพยาบาลอุดรธานี"
  },
  "buildings": [
    {
      "id": "opd",
      "code": "OPD",
      "name": "อาคารผู้ป่วยนอก",
      "floors": [
        {
          "id": "opd-f1",
          "level": 1,
          "name": "ชั้น 1",
          "mapImageUrl": "maps/opd-f1.svg",
          "rooms": [],
          "pois": [],
          "routeNodes": [],
          "routeEdges": []
        }
      ]
    }
  ]
}
```

## 5. Data Dictionary

| ข้อมูล | ตัวอย่าง | คำอธิบาย |
|---|---|---|
| `building.id` | `opd` | รหัสอาคารที่ไม่ซ้ำ |
| `building.code` | `OPD` | รหัสย่ออาคาร |
| `building.name` | อาคารผู้ป่วยนอก | ชื่อที่แสดงผู้ใช้ |
| `floor.id` | `opd-f1` | รหัสชั้น |
| `floor.level` | `1` | เลขชั้นสำหรับเรียงลำดับ |
| `floor.mapImageUrl` | `maps/opd-f1.svg` | ไฟล์พื้นหลังแผนที่ |
| `room.id` | `opd-f1-301` | รหัสห้อง |
| `room.name` | ห้องตรวจ 301 | ชื่อห้อง |
| `room.type` | `clinic` | ประเภทห้อง |
| `room.polygon` | `[{"x": 10, "y": 20}]` | ขอบเขตห้องบนแผนที่ |
| `poi.id` | `opd-f1-elevator-a` | รหัสจุดสนใจ |
| `poi.type` | `elevator` | ประเภท เช่น lift, toilet, pharmacy |
| `poi.position` | `{ "x": 70, "y": 45 }` | ตำแหน่งบนแผนที่ |
| `routeNode.id` | `opd-f1-n01` | จุดเชื่อมเส้นทาง |
| `routeEdge` | `from`, `to`, `distance` | เส้นเชื่อมของเส้นทาง |
| `qr.startNodeId` | `opd-f1-n01` | จุดเริ่มต้นหลังสแกน QR |

## 6. Database ในอนาคต

เมื่อมีผู้ดูแลหลายคนหรือข้อมูลมากขึ้น ให้ย้ายข้อมูลจาก JSON สู่ฐานข้อมูล โดยมีตารางหลักดังนี้:

```text
buildings
floors
rooms
pois
route_nodes
route_edges
qr_locations
users
assets
beacons
asset_location_logs
```

ความสัมพันธ์:

```text
Building → Floors → Rooms / POIs / Route Nodes
Route Nodes → Route Edges
QR Location → Route Node
```

## 7. แผนการพัฒนา

1. สร้างไฟล์ `map-data.json` เป็นแหล่งข้อมูลกลาง
2. เพิ่มความสามารถใน Map Studio: เพิ่ม/ลบอาคาร ชั้น ห้อง POI และเส้นทาง
3. เพิ่ม Import/Export JSON
4. ให้หน้าผู้ป่วยอ่านแผนที่และค้นหาจาก JSON เดียวกัน
5. ใช้ QR Code ระบุจุดเริ่มต้น
6. เมื่อพร้อม ให้ย้ายข้อมูลไปยังฐานข้อมูลแบบ Serverless พร้อมระบบสิทธิ์ผู้ดูแล

> ห้ามเก็บข้อมูลผู้ป่วยจริง เช่น HN, ชื่อผู้ป่วย หรือใบนัด ใน Static JSON ที่เผยแพร่สู่สาธารณะ
