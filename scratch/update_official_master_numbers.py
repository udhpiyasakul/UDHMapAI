import json

with open('map-data.json', encoding='utf-8') as f:
    data = json.load(f)

data['schemaVersion'] = '2.0.0'
data['hospital']['officialTableReference'] = 'ตารางดรรชนีหมายเลขอาคารจาก 2ผังบริเวณเริ่มต้น 1-4-69 (ส่งทีม).pdf (อาคาร 1 - 23)'

# Helper to find building by id
def get_b(b_id):
    return next((b for b in data['buildings'] if b['id'] == b_id), None)

# Update buildings strictly according to official table 1 - 23 from PDF masterplan:
# 1. อาคาร 1 — อาคารอำนวยการและผู้ป่วยนอก (7 ชั้น)
b_opd = get_b('opd')
if b_opd:
    b_opd['mapNumber'] = 1
    b_opd['code'] = 'OPD-1'
    b_opd['name'] = 'อาคาร 1 — อาคารอำนวยการและผู้ป่วยนอก (7 ชั้น)'
    b_opd['description'] = 'ศูนย์อำนวยการ เวชระเบียน คลินิกตรวจโรคทั่วไป จักษุ อายุรกรรม ER และห้องยาหลัก'

# 2. อาคาร 2 — อาคารผู้ป่วยนอก (เดิม) (2 ชั้น)
b_malai = get_b('malai-clinic')
if b_malai:
    b_malai['mapNumber'] = 2
    b_malai['code'] = 'OPD-OLD-2'
    b_malai['name'] = 'อาคาร 2 — อาคารผู้ป่วยนอก (เดิม)'
    b_malai['description'] = 'อาคารผู้ป่วยนอกเดิม คลินิกปฐมภูมิ และคลินิกเฉพาะทางผู้ป่วยนอก'

# 3. อาคาร 3 — อาคารผ่าตัด/ X-RAY(เก่า) (2 ชั้น)
b_chalerm = get_b('chalert-prakiat')
if b_chalerm:
    b_chalerm['mapNumber'] = 3
    b_chalerm['code'] = 'OR-XRAY-3'
    b_chalerm['name'] = 'อาคาร 3 — อาคารผ่าตัด / X-RAY (เก่า)'
    b_chalerm['description'] = 'อาคารเฉลิมพระเกียรติ บริการห้องผ่าตัดเดิมและงานรังสีวิทยา X-RAY'

# 4. อาคาร 4 — อาคารสูตินรีเวช (5 ชั้น)
b_ward20 = get_b('special-ward')
if b_ward20:
    b_ward20['mapNumber'] = 4
    b_ward20['code'] = 'OBGYN-4'
    b_ward20['name'] = 'อาคาร 4 — อาคารสูตินรีเวช (5 ชั้น)'
    b_ward20['description'] = 'อาคารหอผู้ป่วยสูตินรีเวช ห้องคลอด หอผู้ป่วยพิเศษ และฝากครรภ์'

# 5. อาคาร 5 — อาคารไตเทียม (1 ชั้น)
b_dialysis = get_b('dialysis')
if b_dialysis:
    b_dialysis['mapNumber'] = 5
    b_dialysis['code'] = 'DIALYSIS-5'
    b_dialysis['name'] = 'อาคาร 5 — อาคารไตเทียม (1 ชั้น)'
    b_dialysis['description'] = 'ศูนย์ฟอกเลือดด้วยเครื่องไตเทียม และล้างไตทางหน้าท้อง CAPD'

# 6. อาคาร 6 — อาคารพยาธิวิทยา (แลปเบอร์ 10) (2 ชั้น)
b_path = get_b('pathology')
if b_path:
    b_path['mapNumber'] = 6
    b_path['code'] = 'PATH-LAB-6'
    b_path['name'] = 'อาคาร 6 — อาคารพยาธิวิทยา (แลปเบอร์ 10)'
    b_path['description'] = 'ห้องปฏิบัติการชันสูตร พยาธิวิทยาคลินิก เจาะเลือด IPD ตรวจ CBC/Chem/Immuno'

# 7. อาคาร 7 — อาคารเวชกรรมสังคม / เวชระเบียน (2 ชั้น)
b_rec = get_b('medical-records')
if b_rec:
    b_rec['mapNumber'] = 7
    b_rec['code'] = 'SOC-MED-7'
    b_rec['name'] = 'อาคาร 7 — อาคารเวชกรรมสังคมและเวชระเบียน (2 ชั้น)'
    b_rec['description'] = 'บริการยื่นบัตร คลังเวชระเบียน เวชกรรมสังคม และศูนย์นวดแพทย์แผนไทย'

# 8. อาคาร 8 — อาคารศัลยกรรม (7 ชั้น)
b_surg = get_b('surgery')
if b_surg:
    b_surg['mapNumber'] = 8
    b_surg['code'] = 'SURGERY-8'
    b_surg['name'] = 'อาคาร 8 — อาคารศัลยกรรม (7 ชั้น)'
    b_surg['description'] = 'ห้องผ่าตัด หอผู้ป่วยวิกฤตศัลยกรรม (ICU S.1), BURN UNIT & WOUND CARE'

# 9. อาคาร 9 — อาคารศูนย์แพทยศาสตร์ชั้นคลินิก (9 ชั้น)
b_mec = get_b('mec')
if b_mec:
    b_mec['mapNumber'] = 9
    b_mec['code'] = 'MEC-9'
    b_mec['name'] = 'อาคาร 9 — อาคารศูนย์แพทยศาสตร์ชั้นคลินิก (9 ชั้น)'
    b_mec['description'] = 'ศูนย์การศึกษาและฝึกอบรมทางการแพทย์โรงพยาบาลอุดรธานี'

# 11. อาคาร 11 — อาคารศูนย์บริการโรคหัวใจ มะเร็งและวินิจฉัยรักษา (7 ชั้น / สมเด็จพระเทพฯ 200 ปี / EXCELLENT CENTER)
b_somdet = get_b('somdet')
if b_somdet:
    b_somdet['mapNumber'] = 11
    b_somdet['code'] = 'EXCELLENT-11'
    b_somdet['name'] = 'อาคาร 11 — อาคารศูนย์บริการโรคหัวใจ มะเร็ง และวินิจฉัยรักษา (สมเด็จพระเทพฯ 200 ปี)'
    b_somdet['description'] = 'ศูนย์เชี่ยวชาญระดับสูง: หอผู้ป่วยพิเศษ, ศัลยกรรมหัวใจ CVT, CATH LAB, MRI, CT SCAN, OR'

# 12. อาคาร 12 — อาคาร 96 ปี หลวงตามหาบัวญาณสัมปันโน (10 ชั้น)
b_bua = get_b('luangta-bua')
if b_bua:
    b_bua['mapNumber'] = 12
    b_bua['code'] = 'BUA-12'
    b_bua['name'] = 'อาคาร 12 — อาคาร 96 ปี หลวงตามหาบัวญาณสัมปันโน (10 ชั้น)'
    b_bua['description'] = 'อาคารหอผู้ป่วย 96 ปี หลวงตามหาบัว หอผู้ป่วยพิเศษ และศูนย์บริการเฉพาะทาง'

# 13. อาคาร 13 — อาคารตึก 69 ปี (74 ปี คลองจินดา) (8 ชั้น)
b_69y = get_b('b-74y')
if b_69y:
    b_69y['mapNumber'] = 13
    b_69y['code'] = 'B69Y-13'
    b_69y['name'] = 'อาคาร 13 — อาคารตึก 69 ปี (74 ปี คลองจินดา) (8 ชั้น)'
    b_69y['description'] = 'ศูนย์ออร์โธปิดิกส์, SPINAL UNIT, P ICU และ N ICU'

# 19. อาคาร 19 — อาคารโภชนาการ (โรงครัว) (1 ชั้น)
b_nutri = get_b('nutrition')
if b_nutri:
    b_nutri['mapNumber'] = 19
    b_nutri['code'] = 'NUTRI-19'
    b_nutri['name'] = 'อาคาร 19 — อาคารโภชนาการ (โรงครัว)'
    b_nutri['description'] = 'ฝ่ายโภชนาการ จัดเตรียมอาหารผู้ป่วย และบริการสนับสนุน'

# 20. อาคาร 20 — อาคารสงฆ์อาพาธ (2 ชั้น / ตึกสงฆ์กิตติโสภณ)
b_kitti = get_b('kitti-sophon')
if b_kitti:
    b_kitti['mapNumber'] = 20
    b_kitti['code'] = 'KITTI-20'
    b_kitti['name'] = 'อาคาร 20 — อาคารสงฆ์อาพาธ (ตึกสงฆ์กิตติโสภณ) (2 ชั้น)'
    b_kitti['description'] = 'หอผู้ป่วยพระสงฆ์อาพาธ และหน่วยล้างไตทางหน้าท้อง CAPD'

# 21. อาคาร 21 — อาคารอเนกประสงค์หลวงตาอินทร์ถวาย (1 ชั้น)
b_multi = get_b('multipurpose')
if b_multi:
    b_multi['mapNumber'] = 21
    b_multi['code'] = 'MULTI-21'
    b_multi['name'] = 'อาคาร 21 — อาคารอเนกประสงค์หลวงตาอินทร์ถวาย (1 ชั้น)'
    b_multi['description'] = 'อาคารอเนกประสงค์หลวงตาอินทร์ถวาย ห้องประชุมใหญ่ ศูนย์การเรียนรู้'

# 23. อาคาร 23 — อาคารปรีชา-ศิริพรรณ / เภสัชกรรม (2 ชั้น)
b_preecha = get_b('preecha')
if b_preecha:
    b_preecha['mapNumber'] = 23
    b_preecha['code'] = 'PREECHA-23'
    b_preecha['name'] = 'อาคาร 23 — อาคารปรีชา-ศิริพรรณ (เภสัชกรรม) (2 ชั้น)'
    b_preecha['description'] = 'หอผู้ป่วยใน ศูนย์ศัลยกรรมกระดูกและข้อ และงานเภสัชกรรม'

# Sort buildings by mapNumber
data['buildings'].sort(key=lambda x: x.get('mapNumber', 99))

with open('map-data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('Updated map-data.json with official table building numbers 1 to 23 successfully!')
