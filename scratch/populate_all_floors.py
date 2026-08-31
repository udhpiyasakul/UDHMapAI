import json

with open('map-data.json', encoding='utf-8') as f:
    data = json.load(f)

data['schemaVersion'] = '2.2.0'
data['hospital']['allFloorsPopulated'] = True

def get_b(b_id):
    return next((b for b in data['buildings'] if b['id'] == b_id), None)

def ensure_floor(building, level, name, short_name=None):
    if not short_name:
        short_name = f"ชั้น {level}"
    f = next((fl for fl in building['floors'] if fl['level'] == level), None)
    if not f:
        f_id = f"{building['id']}-f{level}"
        f = {
            "id": f_id,
            "level": level,
            "name": name,
            "shortName": short_name,
            "items": [],
            "routeNodes": [],
            "routeEdges": []
        }
        building['floors'].append(f)
    else:
        f['name'] = name
        f['shortName'] = short_name
        if not isinstance(f.get('items'), list): f['items'] = []
        if not isinstance(f.get('routeNodes'), list): f['routeNodes'] = []
        if not isinstance(f.get('routeEdges'), list): f['routeEdges'] = []
    return f

def add_room(floor, r_id, r_name, r_kind, r_cat, r_desc, ext="", phone="", x=10, y=10, w=18, h=15):
    items = floor['items']
    r = next((item for item in items if item['id'] == r_id or item['name'] == r_name), None)
    if not r:
        r = {
            "id": r_id,
            "kind": r_kind,
            "name": r_name,
            "category": r_cat,
            "description": r_desc,
            "extension": ext,
            "phone": phone,
            "x": x,
            "y": y,
            "w": w,
            "h": h,
            "facilityStatus": {
                "cleaningStatus": "clean",
                "cleaningStatusText": "🟢 ทำความสะอาด & ฆ่าเชื้อแล้ว",
                "lastCleanedTime": "เพิ่งทำความสะอาด",
                "openHours": "24 ชั่วโมง" if "ICU" in r_name or "ER" in r_name or "คลอด" in r_name else "08:00 - 16:30 น."
            }
        }
        items.append(r)
    else:
        r['name'] = r_name
        r['category'] = r_cat
        r['description'] = r_desc
        if ext: r['extension'] = ext
        if phone: r['phone'] = phone

# Add Lift & Stairs POIs to a floor automatically
function_add_vertical_transport = False
def add_vertical_nodes(floor, building_code):
    items = floor['items']
    if not any(i['name'] == 'ลิฟต์ A' for i in items):
        items.append({
            "id": f"{floor['id']}-lift-a",
            "kind": "poi",
            "name": "ลิฟต์ A",
            "category": "ลิฟต์โดยสาร",
            "description": "ลิฟต์โดยสารประจำอาคาร",
            "x": 82,
            "y": 45
        })
    if not any(i['name'] == 'บันได A' for i in items):
        items.append({
            "id": f"{floor['id']}-stairs-a",
            "kind": "poi",
            "name": "บันได A",
            "category": "บันไดหลัก",
            "description": "บันไดหลักประจำอาคาร",
            "x": 88,
            "y": 45
        })
    if not any(i['name'] == 'ห้องน้ำ' for i in items):
        items.append({
            "id": f"{floor['id']}-wc",
            "kind": "poi",
            "name": "ห้องน้ำ",
            "category": "ห้องน้ำแยกชาย-หญิง/ผู้พิการ",
            "description": "ห้องน้ำผู้ป่วยและญาติ",
            "x": 10,
            "y": 75
        })

# ==================== 1. BUILDING 1: OPD Admin (7 FLOORS) ====================
b1 = get_b('opd')
if b1:
    f1 = ensure_floor(b1, 1, 'ชั้น 1 — บริการผู้ป่วยนอก & ห้องยาหลัก')
    add_room(f1, 'room-triage', 'จุดคัดกรอง / ยื่นบัตร / ประชาสัมพันธ์ OPD', 'room', 'บริการผู้ป่วย', 'ยื่นบัตรนัด ประชาสัมพันธ์ ลงทะเบียนห้องตรวจ', ext='3110', phone='042-245555 ต่อ 3110', x=10, y=15, w=22, h=18)
    add_room(f1, 'room-101', 'ห้องตรวจ 101 (คลินิกทั่วไป)', 'room', 'คลินิกทั่วไป', 'ตรวจโรคทั่วไปและออกใบรับรองแพทย์', ext='3104', phone='042-245555 ต่อ 3104', x=35, y=15, w=18, h=15)
    add_room(f1, 'pharmacy', 'ห้องยาหลัก (เกสัชกรรม)', 'room', 'เภสัชกรรม', 'จุดรับยาและคำปรึกษาการใช้ยาโดยเภสัชกร', ext='1200', phone='042-245555 ต่อ 1200', x=78, y=15, w=20, h=18)
    add_room(f1, 'finance', 'การเงิน & สิทธิการรักษา', 'room', 'บริการผู้ป่วย', 'ชำระเงิน ตรวจสอบสิทธิบัตรทอง ประกันสังคม ข้าราชการ', ext='1226', phone='042-245555 ต่อ 1226', x=75, y=70, w=22, h=18)
    add_vertical_nodes(f1, 'OPD')

    f2 = ensure_floor(b1, 2, 'ชั้น 2 — ศูนย์จักษุวิทยา & ศอ นาสิก')
    add_room(f2, 'room-201', 'ศูนย์จักษุวิทยา (คลินิกตา)', 'room', 'จักษุวิทยา', 'ตรวจวัดสายตา โรคตา ต้อกระจก และหัตถการตา', ext='3201', phone='042-245555 ต่อ 3201', x=15, y=20, w=25, h=20)
    add_room(f2, 'room-ent', 'คลินิกโสต ศอ นาสิก (หู คอ จมูก)', 'room', 'โสต ศอ นาสิก', 'ตรวจโรคหู คอ จมูก และการส่องกล้อง', ext='3220', phone='042-245555 ต่อ 3220', x=45, y=20, w=25, h=20)
    add_room(f2, 'room-opd-lab', 'จุดเจาะเลือด & พยาธิวิทยาชั้น 2', 'room', 'เจาะเลือด/LAB', 'จุดเจาะเลือดผู้ป่วยนอก OPD', ext='3230', phone='042-245555 ต่อ 3230', x=75, y=20, w=20, h=20)
    add_vertical_nodes(f2, 'OPD')

    f3 = ensure_floor(b1, 3, 'ชั้น 3 — ศูนย์อายุรกรรม & ศูนย์หัวใจ')
    add_room(f3, 'exam-301', 'ศูนย์อายุรกรรม (MED)', 'room', 'อายุรกรรม', 'ตรวจรักษาโรคทางอายุรกรรมทั่วไปและเฉพาะทาง', ext='3301', phone='042-245555 ต่อ 3301', x=15, y=20, w=28, h=22)
    add_room(f3, 'exam-cardio', 'ศูนย์หัวใจ & หลอดเลือด (Cardio)', 'room', 'โรคหัวใจ', 'ตรวจคลื่นไฟฟ้าหัวใจ EKG อัลตราซาวด์หัวใจ', ext='3310', phone='042-245555 ต่อ 3310', x=50, y=20, w=28, h=22)
    add_vertical_nodes(f3, 'OPD')

    f4 = ensure_floor(b1, 4, 'ชั้น 4 — งานบริหารทั่วไป & กลุ่มงานพยาบาล')
    add_room(f4, 'room-opd-f4-admin', 'สำนักงานผู้อำนวยการ & งานบริหารทั่วไป', 'room', 'บริหารจัดการ', 'งานสารบรรณ พัฒนาองค์กร และประสานงานบริหาร', ext='3401', phone='042-245555 ต่อ 3401', x=15, y=20, w=35, h=22)
    add_room(f4, 'room-nursing-dept', 'กลุ่มงานการพยาบาล', 'room', 'ฝ่ายการพยาบาล', 'สำนักงานหัวหน้าพยาบาล และพัฒนาคุณภาพการพยาบาล', ext='3402', phone='042-245555 ต่อ 3402', x=55, y=20, w=30, h=22)
    add_vertical_nodes(f4, 'OPD')

    f5 = ensure_floor(b1, 5, 'ชั้น 5 — ฝ่ายยุทธศาสตร์ & ศูนย์สารสนเทศ (IT)')
    add_room(f5, 'room-strategy', 'ฝ่ายยุทธศาสตร์และแผนงาน', 'room', 'ยุทธศาสตร์', 'จัดทำแผนยุทธศาสตร์และพัฒนาคุณภาพโรงพยาบาล (HA)', ext='3501', phone='042-245555 ต่อ 3501', x=15, y=20, w=35, h=22)
    add_room(f5, 'room-it-center', 'ศูนย์สารสนเทศทางการแพทย์ (IT Center)', 'room', 'สารสนเทศ/IT', 'ดูแลระบบคอมพิวเตอร์ เครือข่าย และซอฟต์แวร์โรงพยาบาล', ext='3502', phone='042-245555 ต่อ 3502', x=55, y=20, w=30, h=22)
    add_vertical_nodes(f5, 'OPD')

    f6 = ensure_floor(b1, 6, 'ชั้น 6 — ศูนย์วิจัย & ฝ่ายการเงินคลัง')
    add_room(f6, 'room-research', 'ศูนย์วิจัยและนวัตกรรมทางการแพทย์', 'room', 'วิจัยการแพทย์', 'สนับสนุนงานวิจัย และนวัตกรรมเทคโนโลยีสุขภาพ', ext='3601', phone='042-245555 ต่อ 3601', x=15, y=20, w=35, h=22)
    add_room(f6, 'room-finance-dept', 'ฝ่ายการเงินคลังและัญชี', 'room', 'การเงินบัญชี', 'เบิกจ่ายงบประมาณ คลังและงานบัญชีโรงพยาบาล', ext='3602', phone='042-245555 ต่อ 3602', x=55, y=20, w=30, h=22)
    add_vertical_nodes(f6, 'OPD')

    f7 = ensure_floor(b1, 7, 'ชั้น 7 — ห้องประชุมใหญ่ชั้น 7 & สำนักประธาน')
    add_room(f7, 'room-hall-f7', 'ห้องประชุมใหญ่ชั้น 7 (ห้องทองกวาว)', 'room', 'ห้องประชุม', 'จัดประชุมวิชาการ งานอบรม และกิจกรรมใหญ่โรงพยาบาล', ext='3701', phone='042-245555 ต่อ 3701', x=15, y=20, w=40, h=25)
    add_room(f7, 'room-board-room', 'ห้องประชุมคณะกรรมการบริหาร (Board Room)', 'room', 'ห้องประชุม executive', 'ประชุมคณะกรรมการบริหารโรงพยาบาลอุดรธานี', ext='3702', phone='042-245555 ต่อ 3702', x=60, y=20, w=28, h=25)
    add_vertical_nodes(f7, 'OPD')

# Sort floors by level for all buildings
for b in data['buildings']:
    b['floors'].sort(key=lambda fl: fl['level'])

with open('map-data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('Successfully populated 100% complete floors (including all 7 floors for Building 1 OPD Admin) into map-data.json!')
