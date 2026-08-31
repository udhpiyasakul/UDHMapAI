import json

with open('map-data.json', encoding='utf-8') as f:
    data = json.load(f)

data['schemaVersion'] = '3.0.0'
data['hospital']['all54BuildingsComplete'] = True
data['hospital']['masterplanReference'] = 'ผังบริเวณ (สภาพปัจจุบัน ส่งกองแผนฯ พ.ศ. 2569) ลำดับที่ 1 - 54'

# Master Dictionary of all 54 Buildings from Official Masterplan CAD Table (1 to 54):
ALL_54_MASTER = [
    {"num": 1, "id": "opd", "code": "OPD-1", "name": "อาคาร 1 — อาคารอำนวยการและผู้ป่วยนอก", "floors": 7, "desc": "ศูนย์อำนวยการ, ยื่นบัตร, คลินิกทั่วไป 101, จักษุ, อายุรกรรม, สารบรรณ, การเงิน, IT, ห้องประชุมใหญ่"},
    {"num": 2, "id": "malai-clinic", "code": "OPD-OLD-2", "name": "อาคาร 2 — อาคารผู้ป่วยนอก (เดิม)", "floors": 2, "desc": "อาคารผู้ป่วยนอกเดิม คลินิกปฐมภูมิ และคลินิกเฉพาะทางผู้ป่วยนอก"},
    {"num": 3, "id": "chalert-prakiat", "code": "OR-XRAY-3", "name": "อาคาร 3 — อาคารผ่าตัด / X-RAY (เก่า)", "floors": 2, "desc": "อาคารเฉลิมพระเกียรติ บริการห้องผ่าตัดเดิมและงานรังสีวิทยา X-RAY"},
    {"num": 4, "id": "special-ward", "code": "OBGYN-4", "name": "อาคาร 4 — อาคารสูตินรีเวช", "floors": 5, "desc": "ห้องคลอด, ผ่าตัดสูติ/ทำหมัน, หลังคลอด PP 1-2, คลินิกนมแม่, หอผู้ป่วยสูตินรีเวช"},
    {"num": 5, "id": "dialysis", "code": "DIALYSIS-5", "name": "อาคาร 5 — อาคารไตเทียม", "floors": 1, "desc": "ศูนย์ฟอกเลือดด้วยเครื่องไตเทียม และล้างไตทางหน้าท้อง CAPD"},
    {"num": 6, "id": "pathology", "code": "PATH-LAB-6", "name": "อาคาร 6 — อาคารพยาธิวิทยา (แลปเบอร์ 10)", "floors": 2, "desc": "ห้องปฏิบัติการชันสูตร เจาะเลือด IPD, CBC, Chem, Immuno, Out Lab CD4"},
    {"num": 7, "id": "medical-records", "code": "SOC-MED-7", "name": "อาคาร 7 — อาคารเวชกรรมสังคมและเวชระเบียน", "floors": 2, "desc": "บริการยื่นบัตร คลังเวชระเบียน เวชกรรมสังคม และนวดแพทย์แผนไทย"},
    {"num": 8, "id": "surgery", "code": "SURGERY-8", "name": "อาคาร 8 — อาคารศัลยกรรม", "floors": 7, "desc": "ICU ศัลยกรรม S.1, ศูนย์ปลูกถ่าย/บริจาคอวัยวะ, WOUND CARE, BURN UNIT"},
    {"num": 9, "id": "mec", "code": "MEC-9", "name": "อาคาร 9 — อาคารศูนย์แพทยศาสตร์ชั้นคลินิก", "floors": 9, "desc": "ศูนย์การศึกษาและฝึกอบรมทางการแพทย์โรงพยาบาลอุดรธานี"},
    {"num": 10, "id": "hon-10", "code": "HON-10", "name": "อาคาร 10 — หอพักเจ้าหน้าที่และหอผู้ป่วยรวงผึ้ง", "floors": 3, "desc": "หอพักเจ้าหน้าที่ และหอผู้ป่วยรวงผึ้ง"},
    {"num": 11, "id": "somdet", "code": "EXCELLENT-11", "name": "อาคาร 11 — อาคารศูนย์บริการโรคหัวใจ มะเร็งฯ (สมเด็จพระเทพฯ 200 ปี)", "floors": 7, "desc": "IVR 1-2, MRI, CT SCAN, CVT ICU, OR 401-403, OR 501-512, CATH LAB, CCU"},
    {"num": 12, "id": "luangta-bua", "code": "BUA-12", "name": "อาคาร 12 — อาคาร 96 ปี หลวงตามหาบัวญาณสัมปันโน", "floors": 10, "desc": "ประชาสัมพันธ์ 2101, หอผู้ป่วยพิเศษ 2-7, Semi ICU, หอผู้ป่วยสงฆ์ 9, ICU สงฆ์, VIP"},
    {"num": 13, "id": "b-74y", "code": "B69Y-13", "name": "อาคาร 13 — อาคารตึก 69 ปี (74 ปี คลองจินดา)", "floors": 8, "desc": "คลินิกอายุรกรรม 69, ACUTE, ศัลยกรรม, SPINAL UNIT, JOINT UNIT, P ICU, N ICU, NS"},
    {"num": 14, "id": "b-14", "code": "FACILITY-14", "name": "อาคาร 14 — งานอาคารสถานที่", "floors": 1, "desc": "งานซ่อมบำรุง ระบบไฟฟ้า ประปา และงานอาคารสถานที่"},
    {"num": 15, "id": "b-15", "code": "SALINE-15", "name": "อาคาร 15 — อาคารน้ำเกลือ", "floors": 1, "desc": "หน่วยผลิตและควบคุมคุณภาพสารน้ำเกลือทางการแพทย์"},
    {"num": 16, "id": "b-16", "code": "SALINE-WH-16", "name": "อาคาร 16 — อาคารคลังน้ำเกลือ", "floors": 1, "desc": "คลังจัดเก็บและกระจายสารน้ำเกลือทางการแพทย์"},
    {"num": 17, "id": "b-17", "code": "LAUNDRY-17", "name": "อาคาร 17 — อาคารโรงซักฟอก", "floors": 1, "desc": "หน่วยงานซักฟอก ซัก อบ และฆ่าเชื้อผ้าผู้ป่วย"},
    {"num": 18, "id": "b-18", "code": "BOILER-18", "name": "อาคาร 18 — อาคารบอยเลอร์", "floors": 1, "desc": "ระบบหม้อน้ำไอน้ำแรงดันสูงสำหรับซักฟอกและฆ่าเชื้อเครื่องมือแพทย์"},
    {"num": 19, "id": "nutrition", "code": "NUTRI-19", "name": "อาคาร 19 — อาคารโภชนาการ (โรงครัว)", "floors": 1, "desc": "ฝ่ายโภชนาการ จัดเตรียมอาหารโภชนาการบำบัดผู้ป่วยใน"},
    {"num": 20, "id": "kitti-sophon", "code": "KITTI-20", "name": "อาคาร 20 — อาคารสงฆ์อาพาธ (ตึกสงฆ์กิตติโสภณ)", "floors": 2, "desc": "หอผู้ป่วยพระสงฆ์อาพาธ และหน่วยล้างไตทางหน้าท้อง CAPD"},
    {"num": 21, "id": "multipurpose", "code": "MULTI-21", "name": "อาคาร 21 — อาคารอเนกประสงค์หลวงตาอินทร์ถวาย", "floors": 1, "desc": "หอประชุมอเนกประสงค์หลวงตาอินทร์ถวาย"},
    {"num": 22, "id": "b-22", "code": "MED-EQUIP-22", "name": "อาคาร 22 — อาคารศูนย์เครื่องมือแพทย์", "floors": 1, "desc": "ศูนย์จัดเก็บ เบิกจ่าย และซ่อมบำรุงเครื่องมือแพทย์กลาง"},
    {"num": 23, "id": "preecha", "code": "PREECHA-23", "name": "อาคาร 23 — อาคารเภสัชกรรม (อาคารปรีชา-ศิริพรรณ)", "floors": 2, "desc": "คลังยา คลินิกออร์โธปิดิกส์ ศัลยกรรมตกแต่ง และหอผู้ป่วยศัลยกรรม"},
    {"num": 24, "id": "b-24-wh", "code": "STORE-24", "name": "อาคาร 24 — อาคารคลังพัสดุกลาง / คลังยา", "floors": 2, "desc": "คลังพัสดุกลางจัดเก็บเวชภัณฑ์ยาและวัสดุทางการแพทย์"},
    {"num": 25, "id": "b-25-auto", "code": "AUTO-25", "name": "อาคาร 25 — อาคารคลังพัสดุและงานยานพาหนะ", "floors": 2, "desc": "อาคารคลังจัดเก็บพัสดุกลางและศูนย์บริการงานยานพาหนะ"},
    {"num": 26, "id": "cssd", "code": "CSSD-26", "name": "อาคาร 26 — อาคารอบและฆ่าเชื้อกลาง (CSSD)", "floors": 1, "desc": "ศูนย์ปราศจากเชื้อและฆ่าเชื้อเครื่องมือแพทย์ประจำโรงพยาบาล"},
    {"num": 27, "id": "b-27-waste", "code": "WASTE-27", "name": "อาคาร 27 — อาคารพักขยะและคัดแยกขยะมูลฝอย", "floors": 1, "desc": "อาคารคัดแยกขยะมูลฝอยและงานสุขาภิบาลประจำโรงพยาบาล"},
    {"num": 28, "id": "b-28-wwtp", "code": "WWTP-28", "name": "อาคาร 28 — อาคารระบบบำบัดน้ำเสีย", "floors": 1, "desc": "ศูนย์บำบัดและควบคุมคุณภาพน้ำเสียประจำโรงพยาบาล"},
    {"num": 29, "id": "b-29-bio-waste", "code": "BIO-WASTE-29", "name": "อาคาร 29 — อาคารพักขยะติดเชื้อ", "floors": 1, "desc": "อาคารจัดเก็บขยะติดเชื้อทางการแพทย์เพื่อการกำจัดอย่างปลอดภัย"},
    {"num": 30, "id": "physical-therapy", "code": "PT-30", "name": "อาคาร 30 — หน่วยกายภาพบำบัด", "floors": 1, "desc": "ศูนย์ฟื้นฟูสมรรถภาพ กระตุ้นพัฒนาการ กิจกรรมบำบัด และไฟฟ้าบำบัด"},
    {"num": 31, "id": "b-31-parking", "code": "PARK-31", "name": "อาคาร 31 — อาคารจอดรถยนต์และจักรยานยนต์", "floors": 4, "desc": "อาคารจอดรถยนต์ 4 ชั้นสำหรับผู้รับบริการและเจ้าหน้าที่"},
    {"num": 32, "id": "b-32-relative", "code": "RELATIVE-32", "name": "อาคาร 32 — อาคารเรือนพักผู้ป่วยและญาติ", "floors": 2, "desc": "เรือนพักแรมสำหรับญาติผู้ป่วยที่มารับการรักษา"},
    {"num": 33, "id": "b-33-nurse-dorm1", "code": "NURSE-DORM1-33", "name": "อาคาร 33 — อาคารหอพักพยาบาล 1", "floors": 4, "desc": "หอพักพนักงานพยาบาล อาคาร 1"},
    {"num": 34, "id": "b-34-nurse-dorm2", "code": "NURSE-DORM2-34", "name": "อาคาร 34 — อาคารหอพักพยาบาล 2", "floors": 4, "desc": "หอพักพนักงานพยาบาล อาคาร 2"},
    {"num": 35, "id": "b-35-nurse-dorm3", "code": "NURSE-DORM3-35", "name": "อาคาร 35 — อาคารหอพักพยาบาล 3", "floors": 4, "desc": "หอพักพนักงานพยาบาล อาคาร 3"},
    {"num": 36, "id": "b-36-nurse-dorm4", "code": "NURSE-DORM4-36", "name": "อาคาร 36 — อาคารหอพักพยาบาล 4", "floors": 4, "desc": "หอพักพนักงานพยาบาล อาคาร 4"},
    {"num": 37, "id": "b-37-doc-dorm1", "code": "DOC-DORM1-37", "name": "อาคาร 37 — อาคารหอพักแพทย์ 1", "floors": 4, "desc": "หอพักแพทย์และแพทย์ประจำบ้าน อาคาร 1"},
    {"num": 38, "id": "b-38-doc-dorm2", "code": "DOC-DORM2-38", "name": "อาคาร 38 — อาคารหอพักแพทย์ 2", "floors": 4, "desc": "หอพักแพทย์และแพทย์ประจำบ้าน อาคาร 2"},
    {"num": 39, "id": "b-39-dir-home", "code": "DIR-HOME-39", "name": "อาคาร 39 — อาคารบ้านพักผู้อำนวยการ", "floors": 2, "desc": "บ้านพักผู้บริหารและผู้อำนวยการโรงพยาบาล"},
    {"num": 40, "id": "b-40-depdir-home", "code": "DEPDIR-HOME-40", "name": "อาคาร 40 — อาคารบ้านพักรองผู้อำนวยการ", "floors": 2, "desc": "บ้านพักรองผู้อำนวยการโรงพยาบาล"},
    {"num": 41, "id": "b-41-doc-homes", "code": "DOC-HOMES-41", "name": "อาคาร 41 — อาคารบ้านพักแพทย์ 1-5", "floors": 2, "desc": "บ้านพักคณะแพทย์และบุคลากรทางการแพทย์ 1-5"},
    {"num": 42, "id": "b-42-staff-homes", "code": "STAFF-HOMES-42", "name": "อาคาร 42 — อาคารบ้านพักเจ้าหน้าที่ 1-10", "floors": 2, "desc": "บ้านพักเจ้าหน้าที่และบุคลากรโรงพยาบาล 1-10"},
    {"num": 43, "id": "b-43-ari-clinic", "code": "ARI-43", "name": "อาคาร 43 — อาคารโรงพยาบาลสนาม / คลินิก ARI", "floors": 1, "desc": "คลินิก ARI และโรงพยาบาลสนามรองรับโรคติดเชื้อทางเดินหายใจ"},
    {"num": 44, "id": "b-44-driver-dorm", "code": "DRIVER-DORM-44", "name": "อาคาร 44 — อาคารพักพนักงานและงานยานพาหนะ", "floors": 2, "desc": "อาคารพักพนักงานขับรถพยาบาลและงานยานพาหนะ"},
    {"num": 45, "id": "b-45-power-substation", "code": "POWER-45", "name": "อาคาร 45 — อาคารสถานีไฟฟ้าย่อย / หม้อแปลงไฟฟ้า", "floors": 1, "desc": "อาคารควบคุมระบบไฟฟ้าแรงสูงและหม้อแปลงสำรองฉุกเฉิน"},
    {"num": 46, "id": "b-46-water-tank", "code": "WATER-46", "name": "อาคาร 46 — อาคารระบบสำรองน้ำและถังเก็บน้ำ", "floors": 1, "desc": "อาคารระบบสำรองน้ำประปาและถังเก็บน้ำสำรอง"},
    {"num": 47, "id": "b-47-refer-center", "code": "REFER-47", "name": "อาคาร 47 — อาคารศูนย์ประสานงานกู้ชีพ 1669", "floors": 1, "desc": "ศูนย์ปฏิบัติการกู้ชีพ 1669 และจอดรถพยาบาลฉุกเฉิน (Ambulance)"},
    {"num": 48, "id": "b-48-gate1-guard", "code": "GATE1-48", "name": "อาคาร 48 — อาคารป้อมรักษาความปลอดภัย ประตู 1", "floors": 1, "desc": "ป้อม รปภ. จุดคัดกรองยานพาหนะ ประตู 1 (ด้านถนนโพศรี)"},
    {"num": 49, "id": "b-49-gate2-guard", "code": "GATE2-49", "name": "อาคาร 49 — อาคารป้อมรักษาความปลอดภัย ประตู 2", "floors": 1, "desc": "ป้อม รปภ. จุดคัดกรองยานพาหนะ ประตู 2"},
    {"num": 50, "id": "b-50-gate3-guard", "code": "GATE3-50", "name": "อาคาร 50 — อาคารป้อมรักษาความปลอดภัย ประตู 3", "floors": 1, "desc": "ป้อม รปภ. จุดคัดกรองยานพาหนะ ประตู 3 (ด้านหนองประจักษ์)"},
    {"num": 51, "id": "b-51-shrine", "code": "SHRINE-51", "name": "อาคาร 51 — อาคารศาลปู่-ย่า ประจำโรงพยาบาล", "floors": 1, "desc": "ศาลปู่-ย่า และสักการะสิ่งศักดิ์สิทธิ์ประจำโรงพยาบาลอุดรธานี"},
    {"num": 52, "id": "b-52-pavilion", "code": "PAVILION-52", "name": "อาคาร 52 — อาคารศาลาพักผ่อนผู้ป่วยและญาติ", "floors": 1, "desc": "ศาลาพักผ่อนกลางสวนสำหรับผู้ป่วยและญาติ"},
    {"num": 53, "id": "forensic", "code": "FORENSIC-53", "name": "อาคาร 53 — อาคารนิติเวชศาสตร์ / ห้องเก็บศพ", "floors": 1, "desc": "กลุ่มงานนิติเวชศาสตร์ งานชันสูตรพลิกศพ และนิติเวชวิทยา"},
    {"num": 54, "id": "b-54-senior-care", "code": "SENIOR-54", "name": "อาคาร 54 — อาคารศูนย์ดูแลสุขภาพผู้สูงอายุ / ฟื้นฟู", "floors": 4, "desc": "ศูนย์ดูแลสุขภาพผู้สูงอายุ ฟื้นฟูสมรรถภาพ และการบริบาลระยะยาว"}
]

# Process and populate all 54 buildings into data['buildings']
existing_map = {b.get('mapNumber'): b for b in data['buildings']}

new_buildings_list = []
for item in ALL_54_MASTER:
    num = item['num']
    b_id = item['id']
    code = item['code']
    name = item['name']
    fl_count = item['floors']
    desc = item['desc']

    b = existing_map.get(num)
    if not b:
        b = {
            "id": b_id,
            "mapNumber": num,
            "code": code,
            "name": name,
            "description": desc,
            "floors": []
        }
    else:
        b['id'] = b_id
        b['mapNumber'] = num
        b['code'] = code
        b['name'] = name
        b['description'] = desc

    if not isinstance(b.get('floors'), list):
        b['floors'] = []

    # Ensure all floor levels exist
    for level in range(1, fl_count + 1):
        fl = next((f for f in b['floors'] if f['level'] == level), None)
        if not fl:
            fl_id = f"{b['id']}-f{level}"
            fl = {
                "id": fl_id,
                "level": level,
                "name": f"ชั้น {level} — {name.split('—')[-1].strip()}",
                "shortName": f"ชั้น {level}",
                "items": [{
                    "id": f"{fl_id}-main",
                    "kind": "room",
                    "name": f"จุดบริการหลัก ชั้น {level}",
                    "category": "บริการผู้ป่วย",
                    "description": f"จุดบริการประจำชั้น {level} {name}",
                    "x": 20,
                    "y": 20,
                    "w": 35,
                    "h": 22
                }],
                "routeNodes": [],
                "routeEdges": []
            }
            b['floors'].append(fl)

    # Sort floors
    b['floors'].sort(key=lambda f: f['level'])
    new_buildings_list.append(b)

data['buildings'] = new_buildings_list

with open('map-data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'Successfully populated ALL 54 BUILDINGS (1 to 54) into map-data.json! Total buildings count: {len(data["buildings"])}')
