import json

with open('map-data.json', encoding='utf-8') as f:
    data = json.load(f)

data['schemaVersion'] = '2.3.0'
data['hospital']['building1ExactImport'] = True

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
    return f

def set_floor_items(floor, items_list):
    # Preserve existing lift / stairs POIs
    vertical_pois = [i for i in floor.get('items', []) if i['name'] in ['ลิฟต์ A', 'บันได A', 'ห้องน้ำ']]
    
    formatted_items = []
    for item in items_list:
        formatted_items.append({
            "id": item['id'],
            "kind": item.get('kind', 'room'),
            "name": item['name'],
            "category": item.get('category', 'บริการผู้ป่วย'),
            "description": item.get('description', ''),
            "extension": item.get('extension', ''),
            "phone": item.get('phone', f"042-245555 ต่อ {item.get('extension', '')}" if item.get('extension') else ""),
            "mobile": item.get('mobile', ''),
            "x": item.get('x', 15),
            "y": item.get('y', 15),
            "w": item.get('w', 22),
            "h": item.get('h', 16),
            "facilityStatus": {
                "cleaningStatus": "clean",
                "cleaningStatusText": "🟢 ทำความสะอาด & ฆ่าเชื้อแล้ว",
                "lastCleanedTime": "เพิ่งทำความสะอาด",
                "openHours": "24 ชั่วโมง" if "ER" in item['name'] or "ฉุกเฉิน" in item['name'] else "08:00 - 16:30 น."
            }
        })
    
    # Re-add vertical transport POIs
    for v in vertical_pois:
        if not any(i['name'] == v['name'] for i in formatted_items):
            formatted_items.append(v)
            
    floor['items'] = formatted_items

# ==================== BUILDING 1: OPD ADMIN (EXACT EXCEL IMPORT) ====================
b1 = get_b('opd')
if b1:
    # Floor 1
    f1 = ensure_floor(b1, 1, 'ชั้น 1 — ผู้ป่วยนอก OPD & อุบัติเหตุ-ฉุกเฉิน ER')
    set_floor_items(f1, [
        {"id": "b1-f1-triage", "name": "จุดคัดกรอง / ยื่นบัตร / ประชาสัมพันธ์ OPD", "category": "ยื่นบัตร/คัดกรอง", "description": "ยื่นบัตรนัด ประชาสัมพันธ์ ลงทะเบียนห้องตรวจ", "extension": "3110, 3114, 3126", "x": 10, "y": 15, "w": 25, "h": 18},
        {"id": "b1-f1-r101", "name": "ห้องตรวจ 101 (คลินิกทั่วไป)", "category": "คลินิกทั่วไป", "description": "ตรวจโรคทั่วไปและออกใบรับรองแพทย์", "extension": "3104", "x": 38, "y": 15, "w": 18, "h": 15},
        {"id": "b1-f1-r105", "name": "ห้องตรวจนัด 1 & 2 (105-106)", "category": "คลินิกทั่วไป", "description": "ห้องตรวจผู้ป่วยนัดติดตามอาการ", "extension": "3105, 3106", "x": 58, "y": 15, "w": 18, "h": 15},
        {"id": "b1-f1-pharmacy", "name": "ห้องยาหลัก (เภสัชกรรม)", "category": "เภสัชกรรม", "description": "จุดรับยาและคำปรึกษาการใช้ยาโดยเภสัชกร", "extension": "1200, 1156", "x": 78, "y": 15, "w": 18, "h": 18},
        {"id": "b1-f1-er-triage", "name": "อุบัติเหตุ-ฉุกเฉิน ER (ทำบัตร & Screen ER)", "category": "ฉุกเฉินวิกฤต", "description": "ทำบัตร ER คัดกรองฉุกเฉิน Observe/Yellow/Pink/Red Zone", "extension": "3148, 3149, 3150", "mobile": "1669", "x": 10, "y": 70, "w": 28, "h": 18},
        {"id": "b1-f1-refer", "name": "ศูนย์รับ-ส่งต่อ REFER & กู้ชีพ 1669", "category": "ส่งต่อ/refer", "description": "ศูนย์ประสานงานส่งต่อผู้ป่วยและรับแจ้งเหตุ 1669", "extension": "3115, 3128, 3124", "x": 42, "y": 70, "w": 22, "h": 18},
        {"id": "b1-f1-finance", "name": "การเงิน & สิทธิประโยชน์ (UC/ประกันสังคม)", "category": "การเงิน/สิทธิ", "description": "ชำระเงิน ตรวจสอบสิทธิบัตรทอง ประกันสังคม ข้าราชการ", "extension": "1226, 3125, 3127", "x": 68, "y": 70, "w": 28, "h": 18}
    ])

    # Floor 2
    f2 = ensure_floor(b1, 2, 'ชั้น 2 — คลินิกอายุรกรรม 2 / ออร์โธปิดิกส์ / SMC')
    set_floor_items(f2, [
        {"id": "b2-f2-med2", "name": "คลินิกอายุรกรรม 2 & คัดกรอง GI Med / COPD", "category": "อายุรกรรม", "description": "ตรวจรักษาโรคทางอายุรกรรม โรคปอด COPD และทางเดินอาหาร", "extension": "3204, 3207, 3214", "x": 10, "y": 15, "w": 30, "h": 20},
        {"id": "b2-f2-ortho", "name": "คลินิกกระดูกและข้อ & ห้องใส่เฝือก", "category": "ออร์โธปิดิกส์", "description": "ตรวจโรคกระดูกและข้อ ทำหัตถการใส่เฝือก", "extension": "3216, 3217, 3218", "x": 43, "y": 15, "w": 26, "h": 20},
        {"id": "b2-f2-pharmacy2", "name": "ห้องยา OPD ชั้น 2 & ADR", "category": "เภสัชกรรม", "description": "ห้องจ่ายยาชั้น 2 และศูนย์เฝ้าระวังแพ้ยา ADR", "extension": "3232, 3233, 3240", "x": 72, "y": 15, "w": 24, "h": 20},
        {"id": "b2-f2-lab2", "name": "ห้องตรวจเลือด Lab OPD ชั้น 2", "category": "เจาะเลือด/LAB", "description": "จุดเจาะเลือดและเก็บสิ่งส่งตรวจผู้ป่วยนอกชั้น 2", "extension": "3223, 3224", "x": 10, "y": 68, "w": 25, "h": 20},
        {"id": "b2-f2-smc", "name": "คลินิกพิเศษ SMC & VIP", "category": "คลินิกพิเศษ", "description": "บริการคลินิกพิเศษเฉพาะทางนอกเวลาราชการ SMC", "extension": "3221, 3222, 3130", "x": 40, "y": 68, "w": 28, "h": 20}
    ])

    # Floor 3
    f3 = ensure_floor(b1, 3, 'ชั้น 3 — สูตินรีเวช / ทันตกรรม / กุมารเวช / จิตเวช / หัวใจ')
    set_floor_items(f3, [
        {"id": "b3-f3-obgyn", "name": "คลินิกสูตินรีเวช & คลินิกนมแม่", "category": "สูตินรีเวช", "description": "ตรวจครรภ์ ฝากครรภ์ วางแผนครอบครัว คลินิกนมแม่", "extension": "3301, 3302, 3315", "x": 10, "y": 15, "w": 26, "h": 20},
        {"id": "b3-f3-pediatric", "name": "คลินิกกุมารเวชกรรม (เด็ก) 31-35", "category": "กุมารเวชกรรม", "description": "ตรวจรักษาโรคเด็ก ฉีดวัคซีนและตรวจพัฒนาการ", "extension": "3325, 3319, 3321", "x": 39, "y": 15, "w": 26, "h": 20},
        {"id": "b3-f3-dental", "name": "คลินิกทันตกรรม ชั้น 3", "category": "ทันตกรรม", "description": "ตรวจและรักษาทางทันตกรรม ทันตกรรมหัตถการ", "extension": "3414, 3408, 3410", "x": 68, "y": 15, "w": 28, "h": 20},
        {"id": "b3-f3-psychiatric", "name": "คลินิกจิตเวช", "category": "จิตเวชศาสตร์", "description": "ให้คำปรึกษาและตรวจรักษาทางจิตเวชและสุขภาพจิต", "extension": "3333, 3334, 3336", "x": 10, "y": 68, "w": 25, "h": 20},
        {"id": "b3-f3-cardio-eho", "name": "ห้องตรวจ EKG , ECHO , EEG", "category": "ตรวจหัวใจ/คลื่นสมอง", "description": "ตรวจคลื่นไฟฟ้าหัวใจ ตรวจหัวใจด้วยคลื่นเสียง อัลตราซาวด์", "extension": "3342, 3343, 3345", "x": 38, "y": 68, "w": 28, "h": 20},
        {"id": "b3-f3-pharm3", "name": "ห้องยา ชั้น 3", "category": "เภสัชกรรม", "description": "จุดจ่ายยาผู้ป่วยนอกชั้น 3", "extension": "3332, 3349", "x": 69, "y": 68, "w": 27, "h": 20}
    ])

    # Floor 4
    f4 = ensure_floor(b1, 4, 'ชั้น 4 — คลินิกโรคหัวใจ & คลินิกเฉพาะทาง')
    set_floor_items(f4, [
        {"id": "b4-f4-cardio-clinic", "name": "คลินิกโรคหัวใจ & หลอดเลือด (ห้องตรวจ 4)", "category": "โรคหัวใจ", "description": "ตรวจรักษาโรคหัวใจ ความดันโลหิตสูง และหลอดเลือด", "extension": "3401, 3424, 3425", "x": 12, "y": 20, "w": 36, "h": 25},
        {"id": "b4-f4-special-clinic", "name": "คลินิกเฉพาะทาง / Treatment (ห้องตรวจ 5-6)", "category": "เฉพาะทาง", "description": "ห้องตรวจหัตถการเฉพาะทางและห้องพ่นยา", "extension": "3430, 3426, 3445", "x": 52, "y": 20, "w": 38, "h": 25}
    ])

    # Floor 5
    f5 = ensure_floor(b1, 5, 'ชั้น 5 — คลินิกประกันสังคม / ตรวจสุขภาพ Wellness / ทรัพยากรบุคคล')
    set_floor_items(f5, [
        {"id": "b5-f5-social-sec", "name": "คลินิกประกันสังคม & ตรวจสุขภาพ Wellness Center", "category": "ประกันสังคม/ตรวจสุขภาพ", "description": "ตรวจรักษาผู้ประกันตน และตรวจสุขภาพประจำปี Wellness Center", "extension": "3531, 3550, 3555", "x": 10, "y": 15, "w": 38, "h": 22},
        {"id": "b5-f5-hr-dept", "name": "งานบริหารทรัพยากรบุคคล (HR)", "category": "บริหารบุคคล", "description": "งานบุคลากร บรรจุ แต่งตั้ง สิทธิประโยชน์เจ้าหน้าที่", "extension": "3500, 3501, 3502", "x": 52, "y": 15, "w": 38, "h": 22},
        {"id": "b5-f5-procurement", "name": "งานพัสดุ & จัดซื้อจัดจ้าง", "category": "พัสดุ/จัดซื้อ", "description": "งานจัดซื้อ จัดจ้าง และตรวจรับพัสดุครุภัณฑ์ทางการแพทย์", "extension": "3510, 3512, 3515", "x": 10, "y": 65, "w": 38, "h": 22},
        {"id": "b5-f5-ic-strategy", "name": "งานยุทธศาสตร์ & งาน IC (ควบคุมการติดเชื้อ)", "category": "ยุทธศาสตร์/IC", "description": "จัดทำแผนยุทธศาสตร์ และเฝ้าระวังการติดเชื้อในโรงพยาบาล", "extension": "3525, 3528, 3529", "x": 52, "y": 65, "w": 38, "h": 22}
    ])

    # Floor 6 (EXACT MATCH USER SCREENSHOT!)
    f6 = ensure_floor(b1, 6, 'ชั้น 6 — เลขานุการ / สารบรรณ / บริหารทั่วไป / การพยาบาล / การเงิน')
    set_floor_items(f6, [
        {"id": "b6-f6-secretariat", "name": "งานเลขานุการ (เลขาธิการ)", "category": "เลขานุการ", "description": "งานเลขานุการผู้บริหาร ประสานงานอำนวยการ", "extension": "3600, 3601, 3602", "x": 10, "y": 12, "w": 38, "h": 16},
        {"id": "b6-f6-saraban", "name": "งานสารบรรณ (รับรองเงินเดือน/สิทธิค่ารักษา/พัสดุ/ส่งหนังสือ)", "category": "สารบรรณ", "description": "รับรองเงินเดือน สิทธิค่ารักษาพยาบาล รับ-ส่งหนังสือราชการ", "extension": "3621, 3616, 3633, 3620", "x": 52, "y": 12, "w": 40, "h": 16},
        {"id": "b6-f6-general-admin", "name": "กลุ่มงานบริหารทั่วไป (ธุรการ / แม่บ้าน / นิติกร)", "category": "บริหารทั่วไป", "description": "ธุรการทั่วไป ประชาสัมพันธ์ งานแม่บ้าน งานกฎหมายนิติกร", "extension": "3634, 3608, 3619, 3635, 3612", "x": 10, "y": 42, "w": 38, "h": 18},
        {"id": "b6-f6-nursing-admin", "name": "กลุ่มการพยาบาล (สำนักงานการพยาบาล & ห้องประชุม 1-3)", "category": "กลุ่มการพยาบาล", "description": "สำนักงานหัวหน้าพยาบาล บริหารงานพยาบาล และห้องประชุม 1-3", "extension": "3628, 3624, 3629, 3630, 3625", "x": 52, "y": 42, "w": 40, "h": 18},
        {"id": "b6-f6-finance-dept", "name": "ฝ่ายการเงินคลังและบัญชี (เงินเดือน/ค่าตอบแทน/บัญชี)", "category": "การเงินคลัง", "description": "การเงินเบิกจ่าย เงินเดือน ค่าตอบแทน บัญชี และงานลูกหนี้", "extension": "3626, 3605, 3606, 3631, 3640", "x": 10, "y": 72, "w": 38, "h": 18},
        {"id": "b6-f6-qic", "name": "ห้อง QIC (พัฒนาคุณภาพโรงพยาบาล)", "category": "พัฒนาคุณภาพ", "description": "ศูนย์พัฒนาคุณภาพโรงพยาบาล QIC", "extension": "3623", "x": 52, "y": 72, "w": 40, "h": 18}
    ])

    # Floor 7 (EXACT MATCH USER SCREENSHOT!)
    f7 = ensure_floor(b1, 7, 'ชั้น 7 — ห้องประชุมใหญ่ / ผลิตเอกสาร / ซักประวัติตรวจตา / ห้องประชุมรักษ์ธรรม')
    set_floor_items(f7, [
        {"id": "b7-f7-doc-copy", "name": "ห้องผลิตเอกสาร (Copy Print)", "category": "ผลิตเอกสาร", "description": "ศูนย์ผลิตและอัดสำเนาเอกสารทางการแพทย์", "extension": "3704", "x": 10, "y": 15, "w": 38, "h": 18},
        {"id": "b7-f7-eye-history", "name": "จุดซักประวัติตรวจตา (ชั้น 7)", "category": "จักษุวิทยา", "description": "ซักประวัติและเตรียมผู้ป่วยตรวจตาชั้น 7", "extension": "3705", "x": 52, "y": 15, "w": 38, "h": 18},
        {"id": "b7-f7-main-hall", "name": "ห้องประชุมใหญ่ชั้น 7 & ห้องควบคุมเสียง", "category": "ห้องประชุม", "description": "ห้องประชุมสัมมนาใหญ่ชั้น 7 และห้องควบคุมระบบเสียง", "extension": "3702, 3710", "x": 10, "y": 60, "w": 38, "h": 22},
        {"id": "b7-f7-rakธรรม", "name": "ห้องประชุมรักษ์ธรรม", "category": "ห้องประชุม", "description": "ห้องประชุมรักษ์ธรรม สำหรับการประชุมคณะกรรมการ", "extension": "3700", "x": 52, "y": 60, "w": 38, "h": 22}
    ])

# Sort floors by level for all buildings
for b in data['buildings']:
    b['floors'].sort(key=lambda fl: fl['level'])

with open('map-data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('Successfully imported EXACT building 1 floors 6 & 7 details from user screenshot into map-data.json!')
