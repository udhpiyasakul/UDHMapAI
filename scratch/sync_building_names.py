import json

with open('map-data.json', encoding='utf-8') as f:
    data = json.load(f)

# Update building titles to include both official Map Number & PDF Masterplan references
updates = {
    "opd": {
        "mapNumber": 21,
        "code": "OPD-21",
        "name": "อาคาร 21 — อาคารอำนวยการและผู้ป่วยนอก (OPD)",
        "description": "ศูนย์อำนวยการ เวชระเบียน คลินิกตรวจโรคทั่วไป จักษุ อายุรกรรม ER และห้องยาหลัก"
    },
    "somdet": {
        "mapNumber": 25,
        "code": "SOMDET-25",
        "name": "อาคาร 25 — อาคารสมเด็จพระเทพฯ (200 ปี / EXCELLENT CENTER)",
        "description": "ศูนย์เชี่ยวชาญระดับสูง: หอผู้ป่วยพิเศษ, ศัลยกรรมหัวใจ CVT, CATH LAB, MRI, CT SCAN, OR"
    },
    "er": {
        "mapNumber": 57,
        "code": "ER-57",
        "name": "อาคาร 57 — อาคารอุบัติเหตุและฉุกเฉิน (อาคารปราบขลา)",
        "description": "ศูนย์รับผู้ป่วยฉุกเฉินวิกฤต 24 ชั่วโมง ศูนย์กู้ชีพ 1669, ห้อง ER, CT ER"
    },
    "mec": {
        "mapNumber": 8,
        "code": "MEC-8",
        "name": "อาคาร 8 — อาคารศูนย์แพทยศาสตร์ศึกษาชั้นคลินิก",
        "description": "ศูนย์การศึกษาและฝึกอบรมทางการแพทย์โรงพยาบาลอุดรธานี"
    },
    "kitti-sophon": {
        "mapNumber": 19,
        "code": "KITTI-19",
        "name": "อาคาร 19 — อาคารตึกสงฆ์กิตติโสภณ",
        "description": "อาคารตึกสงฆ์กิตติโสภณ และหน่วยล้างไตทางหน้าท้อง CAPD"
    },
    "preecha": {
        "mapNumber": 23,
        "code": "PREECHA-23",
        "name": "อาคาร 23 — อาคารปรีชา-ศิริพรรณ",
        "description": "หอผู้ป่วยใน ศูนย์ศัลยกรรมกระดูกและข้อ และศัลยกรรมตกแต่ง"
    },
    "b-74y": {
        "mapNumber": 24,
        "code": "B69Y-24",
        "name": "อาคาร 24 — อาคาร 69 ปี (74 ปี คลองจินดา)",
        "description": "อาคาร 69 ปี (74 ปี คลองจินดา) ศูนย์ออร์โธปิดิกส์, SPINAL UNIT, P ICU และ N ICU"
    },
    "luangta-bua": {
        "mapNumber": 55,
        "code": "BUA-55",
        "name": "อาคาร 55 — อาคาร 96 พรรษา (หลวงตาบัว ญาณสัมปันโน)",
        "description": "อาคารหอผู้ป่วย 96 พรรษา (หลวงตาบัว) หอผู้ป่วยพิเศษ และศูนย์บริการเฉพาะทาง"
    },
    "dialysis": {
        "mapNumber": 16,
        "code": "DIALYSIS-16",
        "name": "อาคาร 16 — อาคารหน่วยไตเทียม",
        "description": "ศูนย์ฟอกเลือดด้วยเครื่องไตเทียม และล้างไตทางหน้าท้อง"
    },
    "pathology": {
        "mapNumber": 18,
        "code": "PATH-18",
        "name": "อาคาร 18 — อาคารพยาธิวิทยาคลินิก (LAB)",
        "description": "ห้องปฏิบัติการชันสูตร เจาะเลือด IPD ตรวจ CBC/Chem/Immuno"
    },
    "special-ward": {
        "mapNumber": 20,
        "code": "WARD-20",
        "name": "อาคาร 20 — อาคารหอผู้ป่วยสูติ-นรีเวช (หอผู้ป่วยพิเศษ)",
        "description": "หอผู้ป่วยพิเศษ ห้องพักผู้ป่วย และห้องคลอดสูติ-นรีเวช"
    },
    "surgery": {
        "mapNumber": 22,
        "code": "SURGERY-22",
        "name": "อาคาร 22 — อาคารศัลยกรรม",
        "description": "ห้องผ่าตัด หอผู้ป่วยวิกฤตศัลยกรรม (ICU S.1), BURN UNIT & WOUND CARE"
    },
    "physical-therapy": {
        "mapNumber": 30,
        "code": "PT-30",
        "name": "อาคาร 30 — หน่วยกายภาพบำบัด",
        "description": "ศูนย์ฟื้นฟูสมรรถภาพ กระตุ้นพัฒนาการ กิจกรรมบำบัด และไฟฟ้าบำบัด"
    },
    "chalert-prakiat": {
        "mapNumber": 3,
        "code": "CHALERM-3",
        "name": "อาคาร 3 — อาคารเฉลิมพระเกียรติ",
        "description": "บริการผู้ป่วยนอก คลินิกปฐมภูมิ และห้องปฏิบัติการ"
    },
    "malai-clinic": {
        "mapNumber": 5,
        "code": "MALAI-5",
        "name": "อาคาร 5 — มาลัยคลินิก",
        "description": "คลินิกปฐมภูมิ และคลินิกเฉพาะทางผู้ป่วยนอก"
    },
    "medical-records": {
        "mapNumber": 6,
        "code": "REC-6",
        "name": "อาคาร 6 — อาคารเวชระเบียนและแพทย์แผนไทย",
        "description": "บริการยื่นบัตร คลังเวชระเบียน และศูนย์นวดแพทย์แผนไทย"
    },
    "cssd": {
        "mapNumber": 26,
        "code": "CSSD-26",
        "name": "อาคาร 26 — อาคารอบและฆ่าเชื้อกลาง (CSSD)",
        "description": "ศูนย์ปราศจากเชื้อและฆ่าเชื้อเครื่องมือแพทย์ประจำโรงพยาบาล"
    },
    "nutrition": {
        "mapNumber": 27,
        "code": "NUTRI-27",
        "name": "อาคาร 27 — อาคารโภชนาการและส่วนบริการ",
        "description": "ฝ่ายโภชนาการ จัดเตรียมอาหารผู้ป่วย และบริการสนับสนุน"
    },
    "forensic": {
        "mapNumber": 53,
        "code": "FORENSIC-53",
        "name": "อาคาร 53 — อาคารนิติเวชศาสตร์ / ห้องเก็บศพ",
        "description": "กลุ่มงานนิติเวชศาสตร์ งานชันสูตรพลิกศพ และนิติเวชวิทยา"
    },
    "multipurpose": {
        "mapNumber": 59,
        "code": "MULTI-59",
        "name": "อาคาร 59 — อาคารอเนกประสงค์และห้องประชุม",
        "description": "ห้องประชุมใหญ่ ศูนย์การเรียนรู้ และงานสัมมนาวิชาการ"
    }
}

for b in data['buildings']:
    b_id = b['id']
    if b_id in updates:
        b.update(updates[b_id])

with open('map-data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('Successfully synchronized building names and numbers with PDF Masterplan!')
