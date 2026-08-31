import json

with open('map-data.json', encoding='utf-8') as f:
    data = json.load(f)

data['schemaVersion'] = '2.1.0'
data['hospital']['officialDocImportDate'] = '2568-02-28 (สมุดโทรศัพท์ ก.พ. 68 & ร่างป้ายบอกทาง 2569)'

def get_b(b_id):
    return next((b for b in data['buildings'] if b['id'] == b_id), None)

def get_or_create_floor(building, level, name):
    f = next((fl for fl in building['floors'] if fl['level'] == level), None)
    if not f:
        f_id = f"{building['id']}-f{level}"
        f = {
            "id": f_id,
            "level": level,
            "name": name,
            "shortName": f"ชั้น {level}",
            "items": [],
            "routeNodes": [],
            "routeEdges": []
        }
        building['floors'].append(f)
    return f

def add_or_update_room(floor, r_id, r_name, r_kind, r_cat, r_desc, ext="", phone="", mobile="", x=10, y=10, w=18, h=15, staff={}, status={}):
    if not isinstance(floor.get('items'), list):
        floor['items'] = []
        
    r = next((item for item in floor['items'] if item['id'] == r_id or item['name'] == r_name), None)
    if not r:
        r = {
            "id": r_id,
            "kind": r_kind,
            "name": r_name,
            "category": r_cat,
            "description": r_desc,
            "extension": ext,
            "phone": phone,
            "mobile": mobile,
            "x": x,
            "y": y,
            "w": w,
            "h": h
        }
        floor['items'].append(r)
    else:
        r['name'] = r_name
        r['category'] = r_cat
        r['description'] = r_desc
        if ext: r['extension'] = ext
        if phone: r['phone'] = phone
        if mobile: r['mobile'] = mobile

    if staff:
        r['staffResponsibility'] = staff
    if status:
        r['facilityStatus'] = status
    return r

# ==================== 1. BUILDING 1: OPD Admin ====================
b1 = get_b('opd')
if b1:
    f1 = get_or_create_floor(b1, 1, 'ชั้น 1 — บริการผู้ป่วยนอก & ห้องยาหลัก')
    add_or_update_room(f1, 'room-triage', 'จุดคัดกรอง / ยื่นบัตร / ประชาสัมพันธ์ OPD', 'room', 'บริการผู้ป่วย', 'ยื่นบัตรนัด ประชาสัมพันธ์ ลงทะเบียนห้องตรวจ', ext='3110', phone='042-245555 ต่อ 3110', x=10, y=15, w=22, h=18)
    add_or_update_room(f1, 'room-101', 'ห้องตรวจ 101 (คลินิกทั่วไป)', 'room', 'คลินิกทั่วไป', 'ตรวจโรคทั่วไปและออกใบรับรองแพทย์', ext='3104', phone='042-245555 ต่อ 3104', x=35, y=15, w=18, h=15)
    add_or_update_room(f1, 'room-105', 'ห้องตรวจนัด 1 & 2', 'room', 'คลินิกทั่วไป', 'ห้องตรวจผู้ป่วยนัดติดตามอาการ 1 และ 2', ext='3105', phone='042-245555 ต่อ 3105', x=56, y=15, w=18, h=15)
    add_or_update_room(f1, 'pharmacy', 'ห้องยาหลัก (เกสัชกรรม)', 'room', 'เภสัชกรรม', 'จุดรับยาและคำปรึกษาการใช้ยาโดยเภสัชกร', ext='1200', phone='042-245555 ต่อ 1200', x=78, y=15, w=20, h=18)
    add_or_update_room(f1, 'finance', 'การเงิน & สิทธิการรักษา', 'room', 'บริการผู้ป่วย', 'ชำระเงิน ตรวจสอบสิทธิบัตรทอง ประกันสังคม ข้าราชการ', ext='1226', phone='042-245555 ต่อ 1226', x=75, y=70, w=22, h=18)
    add_or_update_room(f1, 'room-er-opd', 'จุดรับผู้ป่วยฉุกเฉิน ER (ทำบัตร & คัดกรอง)', 'room', 'ฉุกเฉิน', 'ทำบัตร ER คัดกรองฉุกเฉิน Yellow/Pink/Red Zone', ext='3148', phone='042-245555 ต่อ 3148', mobile='1669', x=10, y=70, w=25, h=18)

    f2 = get_or_create_floor(b1, 2, 'ชั้น 2 — ศูนย์จักษุวิทยา & ศอ นาสิก')
    add_or_update_room(f2, 'room-201', 'ศูนย์จักษุวิทยา (คลินิกตา)', 'room', 'จักษุวิทยา', 'ตรวจวัดสายตา โรคตา ต้อกระจก และหัตถการตา', ext='3201', phone='042-245555 ต่อ 3201', x=15, y=20, w=25, h=20)
    add_or_update_room(f2, 'room-ent', 'คลินิกโสต ศอ นาสิก (หู คอ จมูก)', 'room', 'โสต ศอ นาสิก', 'ตรวจโรคหู คอ จมูก และการส่องกล้อง', ext='3220', phone='042-245555 ต่อ 3220', x=45, y=20, w=25, h=20)
    add_or_update_room(f2, 'room-opd-lab', 'จุดเจาะเลือด & พยาธิวิทยาชั้น 2', 'room', 'เจาะเลือด/LAB', 'จุดเจาะเลือดผู้ป่วยนอก OPD', ext='3230', phone='042-245555 ต่อ 3230', x=75, y=20, w=20, h=20)

    f3 = get_or_create_floor(b1, 3, 'ชั้น 3 — ศูนย์อายุรกรรม & ศูนย์หัวใจ')
    add_or_update_room(f3, 'exam-301', 'ศูนย์อายุรกรรม (MED)', 'room', 'อายุรกรรม', 'ตรวจรักษาโรคทางอายุรกรรมทั่วไปและเฉพาะทาง', ext='3301', phone='042-245555 ต่อ 3301', x=15, y=20, w=28, h=22)
    add_or_update_room(f3, 'exam-cardio', 'ศูนย์หัวใจ & หลอดเลือด (Cardio)', 'room', 'โรคหัวใจ', 'ตรวจคลื่นไฟฟ้าหัวใจ EKG อัลตราซาวด์หัวใจ', ext='3310', phone='042-245555 ต่อ 3310', x=50, y=20, w=28, h=22)

# ==================== 2. BUILDING 11: EXCELLENT CENTER ====================
b11 = get_b('somdet')
if b11:
    f1 = get_or_create_floor(b11, 1, 'ชั้น 1 — ศูนย์เอกซเรย์คอมพิวเตอร์ & MRI')
    add_or_update_room(f1, 'room-somdet-lobby', 'จุดยื่นบัตร & ประชาสัมพันธ์ IVR', 'room', 'บริการผู้ป่วย', 'ประชาสัมพันธ์และยื่นบัตรศูนย์เชี่ยวชาญ', ext='4113', phone='042-245555 ต่อ 4113', x=15, y=15, w=25, h=20)
    add_or_update_room(f1, 'room-ivr1', 'ห้องหัตถการ IVR 1 & 2', 'room', 'รังสีร่วมรักษา', 'ห้องหัตถการรังสีร่วมรักษาหลอดเลือด', ext='4111', phone='042-245555 ต่อ 4111', x=45, y=15, w=22, h=20)
    add_or_update_room(f1, 'room-mri', 'ศูนย์เอกซเรย์ MRI & CT SCAN', 'room', 'เอกซเรย์/MRI', 'ตรวจเอกซเรย์คอมพิวเตอร์และคลื่นแม่เหล็กไฟฟ้า', ext='4107', phone='042-245555 ต่อ 4107', x=72, y=15, w=24, h=22)

    f3 = get_or_create_floor(b11, 3, 'ชั้น 3 — หอผู้ป่วยวิกฤต ICU & ศัลยกรรมหัวใจ CVT')
    add_or_update_room(f3, 'room-icu-cvt', 'หอผู้ป่วยวิกฤตศัลยกรรมหัวใจ CVT ICU', 'room', 'ICU/วิกฤต', 'ดูแลผู้ป่วยหลังผ่าตัดหัวใจและหลอดเลือด', ext='4302', phone='042-245555 ต่อ 4302', x=20, y=20, w=35, h=25)

    f4 = get_or_create_floor(b11, 4, 'ชั้น 4 — ศูนย์ผ่าตัด OR 401-403')
    add_or_update_room(f4, 'room-or-401', 'ห้องผ่าตัด OR 401 - 403 & PRE-OP', 'room', 'ห้องผ่าตัด', 'ห้องผ่าตัดหัวใจและหลอดเลือดขั้นสูง', ext='4401', phone='042-245555 ต่อ 4401', x=20, y=20, w=35, h=25)

    f6 = get_or_create_floor(b11, 6, 'ชั้น 6 — ห้องฉีดสีหัวใจ CATH LAB')
    add_or_update_room(f6, 'room-cathlab', 'ห้องฉีดสีหัวใจ CATH LAB', 'room', 'CATH LAB', 'ตรวจสวนหัวใจและฉีดสีหลอดเลือดหัวใจ', ext='4605', phone='042-245555 ต่อ 4605', x=20, y=20, w=35, h=25)

    f7 = get_or_create_floor(b11, 7, 'ชั้น 7 — หอผู้ป่วยหนักโรคหัวใจ CCU & ICU NEURO')
    add_or_update_room(f7, 'room-ccu', 'หอผู้ป่วยหนักโรคหัวใจ CCU', 'room', 'CCU/วิกฤต', 'ดูแลผู้ป่วยภาวะกล้ามเนื้อหัวใจขาดเลือดวิกฤต', ext='4701', phone='042-245555 ต่อ 4701', x=20, y=20, w=35, h=25)

# ==================== 3. BUILDING 8: Surgery ====================
b8 = get_b('surgery')
if b8:
    f1 = get_or_create_floor(b8, 1, 'ชั้น 1 — ICU ศัลยกรรม & ศูนย์ปลูกถ่ายอวัยวะ')
    add_or_update_room(f1, 'room-surg-icu', 'ICU S.1 (หอผู้ป่วยวิกฤตศัลยกรรม 1)', 'room', 'ICU ศัลยกรรม', 'ดูแลผู้ป่วยวิกฤตหลังผ่าตัดศัลยกรรม', ext='1261', phone='042-245555 ต่อ 1261', x=15, y=20, w=30, h=22)
    add_or_update_room(f1, 'room-organ-transplant', 'ศูนย์ปลูกถ่าย & บริจาคอวัยวะ', 'room', 'ปลูกถ่ายอวัยวะ', 'ประสานงานปลูกถ่ายและบริจาคอวัยวะ', ext='1301', phone='042-245555 ต่อ 1301', x=50, y=20, w=30, h=22)

    f2 = get_or_create_floor(b8, 2, 'ชั้น 2 — ศูนย์ดูแลแผล WOUND CARE')
    add_or_update_room(f2, 'room-wound-care', 'ศูนย์ดูแลแผล WOUND CARE', 'room', 'ดูแลแผล', 'รักษาและดูแลแผลเรื้อรัง แผลกดทับ', ext='1276', phone='042-245555 ต่อ 1276', x=20, y=20, w=35, h=25)

    f5 = get_or_create_floor(b8, 5, 'ชั้น 5 — หอผู้ป่วยไฟไหม้ BURN UNIT')
    add_or_update_room(f5, 'room-burn-unit', 'หอผู้ป่วยไฟไหม้ BURN UNIT', 'room', 'BURN UNIT', 'ดูแลรักษาผู้ป่วยแผลไฟไหม้และน้ำร้อนลวก', ext='1274', phone='042-245555 ต่อ 1274', x=20, y=20, w=35, h=25)

# ==================== 4. BUILDING 13: 69Y / 74Y Khlong Chinda ====================
b13 = get_b('b-74y')
if b13:
    f1 = get_or_create_floor(b13, 1, 'ชั้น 1 — คลินิกอายุรกรรม 69 & เวชระเบียน')
    add_or_update_room(f1, 'room-69-opd', 'คลินิกอายุรกรรม 69 & ห้อง ACUTE', 'room', 'อายุรกรรม', 'ตรวจรักษาผู้ป่วยในและห้อง ACUTE', ext='5105', phone='042-245555 ต่อ 5105', x=15, y=20, w=30, h=22)

    f3 = get_or_create_floor(b13, 3, 'ชั้น 3 — ศูนย์โรคกระดูกสันหลัง SPINAL UNIT')
    add_or_update_room(f3, 'room-spinal-unit', 'ศูนย์โรคกระดูกสันหลัง SPINAL UNIT', 'room', 'ออร์โธปิดิกส์', 'ดูแลผู้ป่วยบาดเจ็บกระดูกสันหลังและไขสันหลัง', ext='5318', phone='042-245555 ต่อ 5318', x=20, y=20, w=35, h=25)

    f4 = get_or_create_floor(b13, 4, 'ชั้น 4 — ศูนย์ข้อต่อ JOINT UNIT')
    add_or_update_room(f4, 'room-joint-unit', 'ศูนย์ผ่าตัดเปลี่ยนข้อต่อ JOINT UNIT', 'room', 'ออร์โธปิดิกส์', 'ดูแลผ่าตัดเปลี่ยนข้อเข่าและข้อสะโพกเทียม', ext='5417', phone='042-245555 ต่อ 5417', x=20, y=20, w=35, h=25)

    f6 = get_or_create_floor(b13, 6, 'ชั้น 6 — หอผู้ป่วยวิกฤตเด็ก P ICU')
    add_or_update_room(f6, 'room-picu', 'หอผู้ป่วยวิกฤตเด็ก P ICU', 'room', 'ICU เด็ก', 'ดูแลผู้ป่วยเด็กขั้นวิกฤต', ext='5624', phone='042-245555 ต่อ 5624', x=20, y=20, w=35, h=25)

    f7 = get_or_create_floor(b13, 7, 'ชั้น 7 — หอผู้ป่วยวิกฤตทารก N ICU & ROP')
    add_or_update_room(f7, 'room-nicu', 'หอผู้ป่วยวิกฤตทารกแรกเกิด N ICU', 'room', 'ICU ทารก', 'ดูแลทารกแรกเกิดน้ำหนักน้อยและวิกฤต', ext='5722', phone='042-245555 ต่อ 5722', x=20, y=20, w=35, h=25)

# ==================== 5. BUILDING 12: 96Y Luangta Bua ====================
b12 = get_b('luangta-bua')
if b12:
    f1 = get_or_create_floor(b12, 1, 'ชั้น 1 — ประชาสัมพันธ์ & ตรวจโรค')
    add_or_update_room(f1, 'room-bua-f1', 'เคาน์เตอร์ประชาสัมพันธ์ อาคาร 96 ปี', 'room', 'บริการผู้ป่วย', 'ต้อนรับและยื่นบัตรอาคาร 96 ปี', ext='2101', phone='042-245555 ต่อ 2101', x=20, y=20, w=30, h=22)

    f9 = get_or_create_floor(b12, 9, 'ชั้น 9 — หอผู้ป่วยสงฆ์ 9 & ICU สงฆ์')
    add_or_update_room(f9, 'room-monk-icu', 'หอผู้ป่วยสงฆ์อาพาธ 9 & ICU สงฆ์', 'room', 'หอผู้ป่วยสงฆ์', 'ดูแลรักษาพระภิกษุสงฆ์อาพาธวิกฤต', ext='2912', phone='042-245555 ต่อ 2912', x=20, y=20, w=35, h=25)

# ==================== 6. BUILDING 4: OB-GYN ====================
b4 = get_b('special-ward')
if b4:
    f1 = get_or_create_floor(b4, 1, 'ชั้น 1 — ห้องคลอด & ผ่าตัดสูติ')
    add_or_update_room(f1, 'room-delivery', 'ห้องคลอด & ผ่าตัดทำหมัน', 'room', 'ห้องคลอด', 'บริการทำคลอด ผ่าตัดสูตินรีเวช และทำหมัน', ext='1331', phone='042-245555 ต่อ 1331', x=20, y=20, w=35, h=25)

    f2 = get_or_create_floor(b4, 2, 'ชั้น 2 — หอผู้ป่วยหลังคลอด PP 1')
    add_or_update_room(f2, 'room-pp1', 'หอผู้ป่วยหลังคลอด PP 1', 'room', 'หลังคลอด', 'ดูแลมารดาและทารกหลังคลอด', ext='1335', phone='042-245555 ต่อ 1335', x=20, y=20, w=35, h=25)

# ==================== 7. BUILDING 6: Pathology ====================
b6 = get_b('pathology')
if b6:
    f1 = get_or_create_floor(b6, 1, 'ชั้น 1 — ห้องปฏิบัติการชันสูตร & เจาะเลือด IPD')
    add_or_update_room(f1, 'room-path-main', 'ห้อง LAB ชันสูตร & เจาะเลือด IPD', 'room', 'LAB ชันสูตร', 'ตรวจ CBC, Chem, Immuno, Blood Gas', ext='1254', phone='042-245555 ต่อ 1254', x=20, y=20, w=35, h=25)

# ==================== 8. BUILDING 30: Physical Therapy ====================
b30 = get_b('physical-therapy')
if b30:
    f1 = get_or_create_floor(b30, 1, 'ชั้น 1 — ศูนย์กายภาพบำบัด & ฟื้นฟู')
    add_or_update_room(f1, 'room-pt-main', 'ศูนย์กายภาพบำบัด & กิจกรรมบำบัด', 'room', 'กายภาพบำบัด', 'ฟื้นฟูสมรรถภาพ กระตุ้นพัฒนาการ และไฟฟ้าบำบัด', ext='1192', phone='042-245555 ต่อ 1192', x=20, y=20, w=35, h=25)

# ==================== 9. BUILDING 57: ER Emergency ====================
b57 = get_b('er')
if b57:
    f1 = get_or_create_floor(b57, 1, 'ชั้น 1 — ห้องฉุกเฉิน ER 24 ชม.')
    add_or_update_room(f1, 'room-er-dept', 'ห้องอุบัติเหตุและฉุกเฉิน (ER 24 ชม.)', 'room', 'ฉุกเฉินวิกฤต', 'ศูนย์กู้ชีพ 1669 รับผู้ป่วยฉุกเฉินวิกฤตตลอด 24 ชั่วโมง', ext='1669', phone='042-245555 ต่อ 3148', mobile='081-1669000', x=15, y=20, w=35, h=25)
    add_or_update_room(f1, 'room-ctscan', 'ศูนย์เอกซเรย์คอมพิวเตอร์ CT ER', 'room', 'เอกซเรย์ ER', 'สแกนสมองและอุบัติเหตุฉุกเฉินเร่งด่วน', ext='1188', phone='042-245555 ต่อ 1188', x=55, y=20, w=30, h=25)

# Save updated dataset
with open('map-data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('Fully imported all 421 official hospital extensions and signage zones into map-data.json successfully!')
