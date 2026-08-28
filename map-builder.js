let data, building, floor, selected, tool = 'select', sequence = 1, timer;

// Dragging state
let isDragging = false;
let isResizing = false;
let dragTarget = null;
let startX = 0, startY = 0;
let initX = 0, initY = 0, initW = 0, initH = 0;

const $ = (id) => document.querySelector(id);
const canvas = $('#canvas');

function toast(text) {
  const t = $('#toast');
  t.textContent = text;
  t.classList.add('show');
  clearTimeout(timer);
  timer = setTimeout(() => t.classList.remove('show'), 2200);
}

function persist(text = 'บันทึกใน Browser แล้ว') {
  UDHMapStore.save(data);
  $('#saved').textContent = text;
}

function findFloor(bId, fId) {
  building = data.buildings.find((item) => item.id === bId);
  if (!building) building = data.buildings[0];
  floor = building.floors.find((item) => item.id === fId);
  if (!floor) floor = building.floors[0];
}

function renderTree() {
  $('#tree').innerHTML = data.buildings
    .map(
      (b) => `
    <div class="tree-building">
      <button data-building="${b.id}">▾ ${b.name}</button>
      ${b.floors
        .map(
          (f) => `
        <button class="tree-floor ${floor && f.id === floor.id ? 'active' : ''}" data-building="${b.id}" data-floor="${f.id}">
          ${f.shortName || f.name}
        </button>
      `
        )
        .join('')}
    </div>
  `
    )
    .join('');
}

function getPoiIcon(item) {
  const cat = (item.category || '').toLowerCase();
  const name = (item.name || '').toLowerCase();

  if (cat.includes('ลิฟต์') || cat.includes('elevator') || name.includes('ลิฟต์')) return '🛗';
  if (cat.includes('บันได') || cat.includes('stairs') || name.includes('บันได')) return '🪜';
  if (cat.includes('ห้องน้ำ') || cat.includes('toilet') || cat.includes('สิ่งอำนวย') || name.includes('ห้องน้ำ')) return '🚽';
  if (cat.includes('ยา') || name.includes('ยา')) return '💊';
  if (cat.includes('ฉุกเฉิน') || name.includes('er')) return '🚨';
  return '📍';
}

function renderCanvas() {
  canvas.querySelectorAll('.item, .route-node-item').forEach((node) => node.remove());
  $('#breadcrumb').textContent = `${building.name} / ${floor.name}`;
  $('#title').textContent = `ออกแบบแผนที่ ${floor.name}`;

  // 1. Render items (rooms & pois)
  if (Array.isArray(floor.items)) {
    floor.items.forEach((item) => {
      const node = document.createElement('div');
      node.className = `item ${item.kind} ${selected && selected.id === item.id ? 'selected' : ''}`;
      node.dataset.id = item.id;
      node.style.left = `${item.x}%`;
      node.style.top = `${item.y}%`;

      if (item.kind === 'room') {
        node.style.width = `${item.w || 18}%`;
        node.style.height = `${item.h || 15}%`;
        const phoneBadge = item.extension ? ` <span class="ext-badge">☎️${item.extension}</span>` : '';
        const cleanStatus = item.facilityStatus?.cleaningStatus === 'cleaning_in_progress' ? ' 🟡' : item.facilityStatus?.cleaningStatus === 'pending_sanitize' ? ' 🔴' : '';
        node.innerHTML = `
          <b>${item.name}${phoneBadge}${cleanStatus}</b>
          <small>${item.category || 'ยังไม่กำหนด'}</small>
          <div class="resize-handle" title="ลากเพื่อย่อ/ขยายขนาดห้อง"></div>
        `;
      } else {
        const icon = getPoiIcon(item);
        node.innerHTML = `${icon}<small>${item.name}</small>`;
      }
      canvas.append(node);
    });
  }

  // 2. Render routeNodes
  if (Array.isArray(floor.routeNodes)) {
    floor.routeNodes.forEach((nodeItem) => {
      const node = document.createElement('div');
      node.className = `route-node-item ${selected && selected.id === nodeItem.id ? 'selected' : ''}`;
      node.dataset.id = nodeItem.id;
      node.style.left = `${nodeItem.x}%`;
      node.style.top = `${nodeItem.y}%`;
      let nodeIcon = '🛣️';
      if (nodeItem.isElevator) nodeIcon = '🛗';
      else if (nodeItem.isStairs) nodeIcon = '🪜';
      node.innerHTML = `${nodeIcon}<small>${nodeItem.name}</small>`;
      canvas.append(node);
    });
  }
}

function render() {
  renderTree();
  renderCanvas();

  if (selected) {
    $('#name').value = selected.name || '';
    $('#kind').value = selected.kind || (selected.x !== undefined ? 'routeNode' : 'room');
    $('#category').value = selected.category || '';
    $('#description').value = selected.description || '';
    $('#phone').value = selected.phone || '';
    $('#extension').value = selected.extension || '';
    $('#mobile').value = selected.mobile || '';
    $('#imageUrl').value = selected.imageUrl || '';
    $('#hardwareTag').value = selected.hardwareTag || selected.beaconTagId || '';

    // Position & Size Inputs
    $('#posX').value = Math.round(selected.x || 0);
    $('#posY').value = Math.round(selected.y || 0);
    $('#posW').value = Math.round(selected.w || 18);
    $('#posH').value = Math.round(selected.h || 15);
    $('#posW').disabled = selected.kind !== 'room';
    $('#posH').disabled = selected.kind !== 'room';

    // Staff Responsibilities
    const sResp = selected.staffResponsibility || {};
    $('#headOfDept').value = sResp.headOfDept || '';
    $('#dutyOfficer').value = sResp.dutyOfficer || '';
    $('#housekeeping').value = sResp.housekeeping || '';
    $('#shiftText').value = sResp.shiftText || '';

    // Facility Status
    const fStat = selected.facilityStatus || {};
    $('#cleaningStatus').value = fStat.cleaningStatus || 'clean';
    $('#lastCleanedTime').value = fStat.lastCleanedTime || '';
    $('#openHours').value = fStat.openHours || '';

    updatePhotoPreview(selected.imageUrl);
  } else {
    $('#form').reset();
    updatePhotoPreview('');
  }
}

function updatePhotoPreview(url) {
  const container = $('#photo-preview-container');
  const img = $('#photo-preview-img');
  if (url && url.trim() !== '') {
    img.src = url;
    container.style.display = 'block';
  } else {
    container.style.display = 'none';
  }
}

function choose(item) {
  selected = item;
  render();
}

async function start() {
  data = await UDHMapStore.load();
  building = data.buildings[0];
  floor = building.floors[0];
  setupEvents();
  render();
}

function setupEvents() {
  $('#tree').addEventListener('click', (event) => {
    const item = event.target.closest('[data-floor]');
    if (item) {
      findFloor(item.dataset.building, item.dataset.floor);
      selected = null;
      render();
    }
  });

  $('.tools').addEventListener('click', (event) => {
    const button = event.target.closest('button');
    if (!button) return;
    tool = button.dataset.tool;
    canvas.dataset.tool = tool;
    document.querySelectorAll('.tools button').forEach((node) => node.classList.toggle('active', node === button));
    $('#tip').innerHTML =
      tool === 'select'
        ? '💡 <b>คำแนะนำ:</b> สามารถคลิกค้างที่ห้อง/หมุดแล้ว <b>ลากขยับตำแหน่ง (Drag & Drop)</b> หรือย่อ/ขยายขนาดห้องได้ทันที!'
        : `คลิกบนแผนที่เพื่อ ${tool === 'room' ? 'วาดห้อง' : tool === 'poi' ? 'ปักหมุด POI (ลิฟต์/บันได/ห้องน้ำ)' : 'ปักจุดเดิน Route Node'}`;
  });

  // Mouse Down: Start Dragging / Resizing
  canvas.addEventListener('mousedown', (e) => {
    const resizeHandle = e.target.closest('.resize-handle');
    const hitEl = e.target.closest('.item, .route-node-item');

    if (resizeHandle && hitEl) {
      const allItems = [...(floor.items || []), ...(floor.routeNodes || [])];
      const targetItem = allItems.find((i) => i.id === hitEl.dataset.id);
      if (targetItem && targetItem.kind === 'room') {
        isResizing = true;
        dragTarget = targetItem;
        startX = e.clientX;
        startY = e.clientY;
        initW = targetItem.w || 18;
        initH = targetItem.h || 15;
        choose(targetItem);
        e.stopPropagation();
        e.preventDefault();
        return;
      }
    }

    if (hitEl) {
      const allItems = [...(floor.items || []), ...(floor.routeNodes || [])];
      const targetItem = allItems.find((i) => i.id === hitEl.dataset.id);
      if (targetItem) {
        isDragging = true;
        dragTarget = targetItem;
        startX = e.clientX;
        startY = e.clientY;
        initX = targetItem.x;
        initY = targetItem.y;
        hitEl.classList.add('dragging');
        choose(targetItem);
        e.stopPropagation();
        e.preventDefault();
        return;
      }
    }

    if (tool !== 'select') {
      const rect = canvas.getBoundingClientRect();
      const kind = tool;
      const x = Math.max(2, Math.min(95, ((e.clientX - rect.left) / rect.width) * 100));
      const y = Math.max(3, Math.min(95, ((e.clientY - rect.top) / rect.height) * 100));

      if (kind === 'routeNode') {
        const nodeItem = {
          id: `node-${Date.now()}-${sequence++}`,
          name: `จุดเดิน ${floor.routeNodes ? floor.routeNodes.length + 1 : 1}`,
          x: Math.round(x),
          y: Math.round(y),
          buildingId: building.id,
          floorId: floor.id
        };
        if (!Array.isArray(floor.routeNodes)) floor.routeNodes = [];
        floor.routeNodes.push(nodeItem);
        choose(nodeItem);
      } else {
        const defaultName = kind === 'room' ? 'ห้องใหม่' : 'หมุดใหม่ (ลิฟต์/บันได/จุดบริการ)';
        const item = {
          id: `${kind}-${Date.now()}-${sequence++}`,
          kind,
          name: defaultName,
          category: kind === 'poi' ? 'ลิฟต์' : '',
          phone: '',
          extension: '',
          mobile: '',
          imageUrl: '',
          x: Math.round(x - (kind === 'room' ? 9 : 2)),
          y: Math.round(y - (kind === 'room' ? 6 : 2)),
          ...(kind === 'room' ? { w: 18, h: 15 } : {})
        };
        if (!Array.isArray(floor.items)) floor.items = [];
        floor.items.push(item);
        choose(item);
      }

      persist();
      toast('เพิ่มองค์ประกอบแล้ว');
    }
  });

  // Global Mouse Move: Perform Dragging or Resizing
  window.addEventListener('mousemove', (e) => {
    if (!dragTarget) return;

    const rect = canvas.getBoundingClientRect();
    const deltaXPct = ((e.clientX - startX) / rect.width) * 100;
    const deltaYPct = ((e.clientY - startY) / rect.height) * 100;

    if (isDragging) {
      dragTarget.x = Math.max(2, Math.min(98, Math.round(initX + deltaXPct)));
      dragTarget.y = Math.max(2, Math.min(98, Math.round(initY + deltaYPct)));

      const el = canvas.querySelector(`[data-id="${dragTarget.id}"]`);
      if (el) {
        el.style.left = `${dragTarget.x}%`;
        el.style.top = `${dragTarget.y}%`;
      }
      $('#posX').value = dragTarget.x;
      $('#posY').value = dragTarget.y;
    } else if (isResizing) {
      dragTarget.w = Math.max(4, Math.min(80, Math.round(initW + deltaXPct)));
      dragTarget.h = Math.max(4, Math.min(80, Math.round(initH + deltaYPct)));

      const el = canvas.querySelector(`[data-id="${dragTarget.id}"]`);
      if (el) {
        el.style.width = `${dragTarget.w}%`;
        el.style.height = `${dragTarget.h}%`;
      }
      $('#posW').value = dragTarget.w;
      $('#posH').value = dragTarget.h;
    }
  });

  // Mouse Up: End Dragging or Resizing
  window.addEventListener('mouseup', () => {
    if (isDragging || isResizing) {
      if (dragTarget) {
        persist(`📍 ขยับตำแหน่ง/ขนาด ${dragTarget.name} เรียบร้อยแล้ว`);
      }
      isDragging = false;
      isResizing = false;
      dragTarget = null;
      renderCanvas();
    }
  });

  // Numeric Input Change Bindings
  $('#posX').oninput = () => {
    if (!selected) return;
    selected.x = parseInt($('#posX').value, 10) || 0;
    persist();
    renderCanvas();
  };
  $('#posY').oninput = () => {
    if (!selected) return;
    selected.y = parseInt($('#posY').value, 10) || 0;
    persist();
    renderCanvas();
  };
  $('#posW').oninput = () => {
    if (!selected || selected.kind !== 'room') return;
    selected.w = parseInt($('#posW').value, 10) || 18;
    persist();
    renderCanvas();
  };
  $('#posH').oninput = () => {
    if (!selected || selected.kind !== 'room') return;
    selected.h = parseInt($('#posH').value, 10) || 15;
    persist();
    renderCanvas();
  };

  $('#imageUrl').oninput = () => {
    updatePhotoPreview($('#imageUrl').value.trim());
  };

  // Form Submit
  $('#form').addEventListener('submit', (event) => {
    event.preventDefault();
    if (!selected) return toast('กรุณาเลือกองค์ประกอบ');

    selected.name = $('#name').value.trim();
    selected.kind = $('#kind').value;
    selected.category = $('#category').value.trim();
    selected.description = $('#description').value.trim();
    selected.phone = $('#phone').value.trim();
    selected.extension = $('#extension').value.trim();
    selected.mobile = $('#mobile').value.trim();
    selected.imageUrl = $('#imageUrl').value.trim();
    selected.hardwareTag = $('#hardwareTag').value.trim();

    // If POI category is elevator or stairs, check isElevator / isStairs
    if (selected.kind === 'routeNode') {
      const cat = (selected.category || selected.name || '').toLowerCase();
      selected.isElevator = cat.includes('ลิฟต์') || cat.includes('elevator');
      selected.isStairs = cat.includes('บันได') || cat.includes('stairs');
    }

    // Save Staff Responsibilities
    selected.staffResponsibility = {
      headOfDept: $('#headOfDept').value.trim(),
      dutyOfficer: $('#dutyOfficer').value.trim(),
      housekeeping: $('#housekeeping').value.trim(),
      shiftText: $('#shiftText').value.trim()
    };

    // Save Facility Status
    const statusVal = $('#cleaningStatus').value;
    let statusTxt = '🟢 ทำความสะอาด & ฆ่าเชื้อแล้ว';
    if (statusVal === 'cleaning_in_progress') statusTxt = '🟡 กำลังทำความสะอาด';
    else if (statusVal === 'pending_sanitize') statusTxt = '🔴 รอฆ่าเชื้อฉุกเฉิน';

    selected.facilityStatus = {
      cleaningStatus: statusVal,
      cleaningStatusText: statusTxt,
      lastCleanedTime: $('#lastCleanedTime').value.trim() || 'เพิ่งทำความสะอาด',
      openHours: $('#openHours').value.trim() || '24 ชั่วโมง'
    };

    persist();
    render();
    toast('💾 บันทึกรายละเอียดองค์ประกอบเรียบร้อยแล้ว');
  });

  $('#delete').onclick = () => {
    if (!selected) return;
    if (floor.items) floor.items = floor.items.filter((item) => item.id !== selected.id);
    if (floor.routeNodes) floor.routeNodes = floor.routeNodes.filter((item) => item.id !== selected.id);
    selected = null;
    persist();
    render();
    toast('ลบองค์ประกอบแล้ว');
  };

  // Add Building
  $('#add-building').onclick = () => {
    const name = prompt('ชื่ออาคารใหม่');
    if (!name) return;
    const id = `building-${Date.now()}`;
    data.buildings.push({
      id,
      code: id.toUpperCase(),
      name,
      floors: [{ id: `${id}-f1`, level: 1, name: 'ชั้น 1', shortName: 'ชั้น 1', items: [], routeNodes: [], routeEdges: [] }]
    });
    findFloor(id, `${id}-f1`);
    selected = null;
    persist();
    render();
    toast(`เพิ่มอาคาร ${name} เรียบร้อยแล้ว`);
  };

  // Add Floor Modal Manager
  $('#add-floor').onclick = () => {
    if (!building) return;
    $('#floor-modal-building-name').value = building.name;
    $('#floor-modal-name').value = `ชั้น ${building.floors.length + 1}`;
    $('#floor-modal-level').value = building.floors.length + 1;
    $('#floor-modal-mapurl').value = '';
    $('#floor-modal').showModal();
  };

  $('#close-floor-modal').onclick = () => $('#floor-modal').close();

  $('#add-floor-form').onsubmit = (e) => {
    e.preventDefault();
    const fName = $('#floor-modal-name').value.trim();
    const fLevel = parseInt($('#floor-modal-level').value, 10) || building.floors.length + 1;
    const fMapUrl = $('#floor-modal-mapurl').value.trim();

    const newFloorId = `${building.id}-f${Date.now()}`;
    const newFloor = {
      id: newFloorId,
      level: fLevel,
      name: fName,
      shortName: `ชั้น ${fLevel}`,
      mapImageUrl: fMapUrl,
      items: [],
      routeNodes: [],
      routeEdges: []
    };

    building.floors.push(newFloor);
    findFloor(building.id, newFloorId);
    selected = null;
    persist();
    render();
    $('#floor-modal').close();
    toast(`🏢 เพิ่ม ${fName} ใน ${building.name} สำเร็จแล้ว!`);
  };

  $('#export').onclick = () => {
    UDHMapStore.download(data);
    toast('ดาวน์โหลด map-data.json แล้ว');
  };

  $('#import').onchange = async (event) => {
    const file = event.target.files[0];
    if (!file) return;
    try {
      const next = JSON.parse(await file.text());
      if (!UDHMapStore.valid(next)) throw new Error();
      data = next;
      UDHMapStore.save(data);
      building = data.buildings[0];
      floor = building.floors[0];
      selected = null;
      render();
      toast('นำเข้าข้อมูลสำเร็จ');
    } catch {
      toast('ไฟล์ JSON ไม่ถูกต้อง');
    }
  };

  $('#reset').onclick = () => {
    if (confirm('ลบข้อมูลที่แก้ไขใน Browser และโหลดข้อมูลต้นฉบับใหม่?')) {
      UDHMapStore.reset();
      location.reload();
    }
  };
}

start().catch((error) => toast(`${error.message} — กรุณารันผ่าน Local Server`));
