import json

with open('map-data.json', encoding='utf-8') as f:
    data = json.load(f)

# Helper to find building by id
def get_b(b_id):
    return next((b for b in data['buildings'] if b['id'] == b_id), None)

# 1. Update Building 21 OPD
opd = get_b('opd')
if opd:
    opd['officialPhone'] = '042-245555'
    opd['description'] = 'ศูนย์อำนวยการ เวชระเบียน คลินิกตรวจโรคทั่วไป จักษุ อายุรกรรม ER และห้องยาหลัก'
    
    # Floor 1
    f1 = next((f for f in opd['floors'] if f['id'] == 'opd-f1'), None)
    if f1:
        # Triage
        r_triage = next((r for r in f1['items'] if r['id'] == 'room-triage'), None)
        if r_triage:
            r_triage['extension'] = '3110'
            r_triage['phone'] = '042-245555 ต่อ 3110'
            r_triage['description'] = 'จุดคัดกรอง ยื่นบัตรนัด ประชาสัมพันธ์ และสิทธิประโยชน์หลัก'
        
        # Room 101
        r_101 = next((r for r in f1['items'] if r['id'] == 'room-101'), None)
        if r_101:
            r_101['extension'] = '3104'
            r_101['phone'] = '042-245555 ต่อ 3104'
            r_101['description'] = 'คลินิกตรวจโรคทั่วไปและออกใบรับรองแพทย์ (เบอร์ภายใน 3104 / 1101)'

        # Pharmacy
        r_pharm = next((r for r in f1['items'] if r['id'] == 'pharmacy'), None)
        if r_pharm:
            r_pharm['extension'] = '1200'
            r_pharm['phone'] = '042-245555 ต่อ 1200'
            r_pharm['description'] = 'จุดรับยาและคำปรึกษาการใช้ยาโดยเภสัชกร (เบอร์ภายใน 1200 / 1156)'

        # Finance
        r_fin = next((r for r in f1['items'] if r['id'] == 'finance'), None)
        if r_fin:
            r_fin['extension'] = '1226'
            r_fin['phone'] = '042-245555 ต่อ 1226'
            r_fin['description'] = 'ชำระเงิน ตรวจสอบสิทธิบัตรทอง ประกันสังคม ข้าราชการ (เบอร์ภายใน 1226-1229)'

    # Floor 2
    f2 = next((f for f in opd['floors'] if f['id'] == 'opd-f2'), None)
    if f2:
        r_201 = next((r for r in f2['items'] if r['id'] == 'room-201'), None)
        if r_201:
            r_201['extension'] = '3201'
            r_201['phone'] = '042-245555 ต่อ 3201'
            r_201['description'] = 'ศูนย์จักษุวิทยา ตรวจวัดสายตาและต้อกระจก (เบอร์ภายใน 3201-3208)'

        r_lab = next((r for r in f2['items'] if r['id'] == 'room-lab'), None)
        if r_lab:
            r_lab['extension'] = '3230'
            r_lab['phone'] = '042-245555 ต่อ 3230'
            r_lab['description'] = 'จุดเจาะเลือดและเก็บสิ่งส่งตรวจ (เบอร์ภายใน 3230 / 2200)'

    # Floor 3
    f3 = next((f for f in opd['floors'] if f['id'] == 'opd-f3'), None)
    if f3:
        r_301 = next((r for r in f3['items'] if r['id'] == 'exam-301'), None)
        if r_301:
            r_301['extension'] = '3301'
            r_301['phone'] = '042-245555 ต่อ 3301'

        r_cardio = next((r for r in f3['items'] if r['id'] == 'exam-cardio'), None)
        if r_cardio:
            r_cardio['extension'] = '3310'
            r_cardio['phone'] = '042-245555 ต่อ 3310'

# 2. Update Building 57 ER
er = get_b('er')
if er:
    f1 = next((f for f in er['floors'] if f['id'] == 'er-f1'), None)
    if f1:
        r_er = next((r for r in f1['items'] if r['id'] == 'room-er-dept'), None)
        if r_er:
            r_er['extension'] = '1669'
            r_er['phone'] = '042-245555 ต่อ 3148'
            r_er['mobile'] = '081-1669000'
            r_er['description'] = 'รับผู้ป่วยฉุกเฉินวิกฤต 24 ชั่วโมง ศูนย์กู้ชีพ 1669 (เบอร์ภายใน 3148, 3149, 3150)'

        r_ct = next((r for r in f1['items'] if r['id'] == 'room-ctscan'), None)
        if r_ct:
            r_ct['extension'] = '1188'
            r_ct['phone'] = '042-245555 ต่อ 1188'
            r_ct['description'] = 'ศูนย์เอกซเรย์คอมพิวเตอร์ CT ER และสแกนสมอง (เบอร์ภายใน 1188 / 5702)'

# 3. Update Building 25 Somdet (EXCELLENT CENTER)
somdet = get_b('somdet')
if somdet:
    f1 = next((f for f in somdet['floors'] if f['id'] == 'somdet-f1'), None)
    if f1:
        r_somdet = next((r for r in f1['items'] if r['id'] == 'room-somdet-lobby'), None)
        if r_somdet:
            r_somdet['extension'] = '4102'
            r_somdet['phone'] = '042-245555 ต่อ 4102'
            r_somdet['description'] = 'ศูนย์ประสานงานรับรอง อาคารสมเด็จพระเทพฯ 200 ปี / EXCELLENT CENTER (เบอร์ภายใน 4102, 4113)'

# 4. Enrich extra building phone numbers
b_bua = get_b('luangta-bua')
if b_bua:
    b_bua['description'] = 'อาคารเฉลิมพระเกียรติ 96 พรรษา และหอผู้ป่วยพิเศษ (เบอร์ภายใน 2101-2107)'

b_24 = get_b('b-74y')
if b_24:
    b_24['description'] = 'อาคาร 74 ปี คลองจินดา (69 ปี) ศูนย์ออร์โธปิดิกส์ & SPINAL UNIT (เบอร์ภายใน 5110, 5318)'

b_pt = get_b('physical-therapy')
if b_pt:
    b_pt['description'] = 'หน่วยกายภาพบำบัด กระตุ้นพัฒนาการ และกิจกรรมบำบัด (เบอร์ภายใน 1192-1198)'

b_kitti = get_b('kitti-sophon')
if b_kitti:
    b_kitti['description'] = 'อาคารตึกสงฆ์กิตติโสภณ และหน่วยล้างไตทางหน้าท้อง CAPD (เบอร์ภายใน 1234, 1124)'

b_path = get_b('pathology')
if b_path:
    b_path['description'] = 'อาคารพยาธิวิทยาคลินิก ห้อง LAB เจาะเลือด IPD และตรวจ CBC/Chem (เบอร์ภายใน 1254, 1258)'

# Save updated dataset
with open('map-data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('Enriched dataset map-data.json with official Doc/ numbers successfully!')
