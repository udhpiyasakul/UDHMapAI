let mapData = null;
let pathfinder = null;
let currentBuilding = null;
let currentFloor = null;
let startNodeId = 'entry';
let destinationPlace = null;
let isWheelchairOnly = false;
let toastTimer = null;

const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => document.querySelectorAll(selector);

function showToast(message) {
  const toast = $('#toast');
  if (!toast) return;
  toast.innerHTML = message;
  toast.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove('show'), 3000);
}

async function initApp() {
  try {
    mapData = await UDHMapStore.load();
    pathfinder = new UDHPathfinder(mapData);

    const params = new URLSearchParams(window.location.search);
    if (params.has('startNode')) {
      startNodeId = params.get('startNode');
    }
    if (params.has('wheelchair')) {
      isWheelchairOnly = params.get('wheelchair') === 'true';
    }

    const buildingSelect = $('#building-select');
    buildingSelect.innerHTML = mapData.buildings
      .map((b) => `<option value="${b.id}">${b.name}</option>`)
      .join('');

    const reqBuilding = params.get('building');
    if (reqBuilding && mapData.buildings.some((b) => b.id === reqBuilding)) {
      buildingSelect.value = reqBuilding;
    }

    setupEventListeners();
    onBuildingChange();

    if (params.has('destRoom')) {
      const destRoomId = params.get('destRoom');
      const all = getAllPlaces();
      const target = all.find((p) => p.id === destRoomId);
      if (target) {
        selectDestination(target);
      }
    }
  } catch (error) {
    console.error('App initialization error:', error);
    showToast(`⚠️ ${error.message} — กรุณารันผ่าน Local Server`);
  }
}

function setupEventListeners() {
  $('#building-select').onchange = onBuildingChange;
  $('#floor-select').onchange = onFloorChange;

  const queryInput = $('#query');
  queryInput.oninput = handleSearch;
  queryInput.onfocus = handleSearch;

  $('#mode-standard').onclick = () => setWheelchairMode(false);
  $('#mode-wheelchair').onclick = () => setWheelchairMode(true);

  $('#change-start-btn').onclick = () => {
    startNodeId = startNodeId === 'entry' ? 'somdet-entry' : 'entry';
    const nodeObj = pathfinder.nodes.get(startNodeId);
    showToast(`📍 เปลี่ยนจุดเริ่มต้นเป็น: <b>${nodeObj ? nodeObj.name : startNodeId}</b>`);
    updateStartNodeDisplay();
    if (destinationPlace) recalculateRoute();
  };

  $('#navigate-btn').onclick = () => {
    if (!destinationPlace) return;
    const destNode = getDestinationNode(destinationPlace);
    const url = `navigation.html?start=${startNodeId}&dest=${destNode ? destNode.id : ''}&placeId=${destinationPlace.id}&wheelchair=${isWheelchairOnly}`;
    window.location.href = url;
  };

  // Report buttons
  $('#btn-report-cleaning').onclick = () => {
    if (!destinationPlace) return;
    showToast(`🧹 แจ้งทีมแม่บ้านทำความสะอาดเร่งด่วนสำหรับ: <b>${destinationPlace.name}</b> เรียบร้อยแล้ว (Ticket #CLN-${Date.now().toString().slice(-4)})`);
  };

  $('#btn-report-maintenance').onclick = () => {
    if (!destinationPlace) return;
    showToast(`🛠️ แจ้งศูนย์ช่างซ่อมบำรุงอุปกรณ์สำหรับ: <b>${destinationPlace.name}</b> เรียบร้อยแล้ว (Ticket #MNT-${Date.now().toString().slice(-4)})`);
  };
}

function setWheelchairMode(enabled) {
  isWheelchairOnly = enabled;
  $('#mode-standard').classList.toggle('active', !enabled);
  $('#mode-wheelchair').classList.toggle('active', enabled);
  showToast(enabled ? '♿ เปิดใช้งานโหมดรถเข็น (หลีกเลี่ยงบันได)' : '🚶‍♂️ เปิดใช้งานโหมดเดินปกติ');
  if (destinationPlace) {
    recalculateRoute();
  }
}

function onBuildingChange() {
  const bId = $('#building-select').value;
  currentBuilding = mapData.buildings.find((b) => b.id === bId);

  const floorSelect = $('#floor-select');
  floorSelect.innerHTML = currentBuilding.floors
    .map((f) => `<option value="${f.id}">${f.shortName || f.name}</option>`)
    .join('');

  currentFloor = currentBuilding.floors[0];
  renderCanvasItems();
}

function onFloorChange() {
  const fId = $('#floor-select').value;
  currentFloor = currentBuilding.floors.find((f) => f.id === fId);
  renderCanvasItems();
  if (destinationPlace) {
    drawRouteOverlay();
  }
}

function renderCanvasItems() {
  const canvas = $('#canvas');
  canvas.querySelectorAll('.map-room-node, .map-poi-node').forEach((el) => el.remove());

  if (!currentFloor || !Array.isArray(currentFloor.items)) return;

  currentFloor.items.forEach((item) => {
    const node = document.createElement('div');
    node.className = `map-item-pin ${item.kind === 'room' ? 'map-room-node' : 'map-poi-node'}`;
    node.style.left = `${item.x}%`;
    node.style.top = `${item.y}%`;

    if (item.kind === 'room') {
      node.style.width = `${item.w || 20}%`;
      node.style.height = `${item.h || 18}%`;
      const extTag = item.extension ? `<small class="ext-tag">☎️${item.extension}</small>` : '';
      node.innerHTML = `
        <span class="room-title">${item.name}</span>
        <small class="room-cat">${item.category || ''}</small>
        ${extTag}
      `;
    } else {
      let icon = '📍';
      if (item.category === 'ลิฟต์') icon = '🛗';
      else if (item.category === 'บันได') icon = '🪜';
      else if (item.category === 'สิ่งอำนวยความสะดวก') icon = '🚽';
      node.innerHTML = `<span class="poi-icon">${icon}</span><small class="poi-title">${item.name}</small>`;
    }

    node.onclick = () => {
      const place = { ...item, building: currentBuilding, floor: currentFloor };
      selectDestination(place);
    };

    canvas.appendChild(node);
  });

  updateStartNodeDisplay();
}

function updateStartNodeDisplay() {
  const startNode = pathfinder ? pathfinder.nodes.get(startNodeId) : null;
  const label = $('#start-location-label');
  if (label) {
    label.innerHTML = startNode
      ? `<b>${startNode.name}</b> · ${startNode.buildingName} ${startNode.floorName}`
      : 'ประตูทางเข้าหลัก · อาคารผู้ป่วยนอก ชั้น 1';
  }

  const userMarker = $('#you-marker');
  if (userMarker) {
    if (startNode && startNode.floorId === currentFloor.id) {
      userMarker.style.left = `${startNode.x}%`;
      userMarker.style.top = `${startNode.y}%`;
      userMarker.style.display = 'block';
    } else {
      userMarker.style.display = 'none';
    }
  }
}

function getAllPlaces() {
  if (!mapData) return [];
  return mapData.buildings.flatMap((b) =>
    b.floors.flatMap((f) =>
      f.items.map((item) => ({
        ...item,
        building: b,
        floor: f
      }))
    )
  );
}

function handleSearch() {
  const q = $('#query').value.trim().toLowerCase();
  const resultsContainer = $('#results');

  if (!q) {
    resultsContainer.innerHTML = '';
    resultsContainer.classList.remove('active');
    return;
  }

  const matches = getAllPlaces()
    .filter((place) => {
      const sResp = place.staffResponsibility || {};
      const text = `${place.name} ${place.category || ''} ${place.description || ''} ${place.extension || ''} ${place.phone || ''} ${sResp.headOfDept || ''} ${sResp.dutyOfficer || ''} ${sResp.housekeeping || ''}`.toLowerCase();
      return text.includes(q);
    })
    .slice(0, 8);

  if (matches.length === 0) {
    resultsContainer.innerHTML = `<div class="no-result">ไม่พบจุดหมาย เบอร์ภายใน หรือผู้รับผิดชอบที่ตรงกับ "${q}"</div>`;
    resultsContainer.classList.add('active');
    return;
  }

  resultsContainer.innerHTML = matches
    .map(
      (place, idx) => `
      <div class="search-item" data-index="${idx}">
        <div class="search-item-info">
          <strong>${highlightQuery(place.name, q)} ${place.extension ? `<span class="ext-badge">☎️${place.extension}</span>` : ''}</strong>
          <small>${place.building.name} · ${place.floor.name} · ${place.category || 'ทั่วไป'}</small>
        </div>
        <span class="search-go-badge">เลือก ➔</span>
      </div>
    `
    )
    .join('');

  resultsContainer.classList.add('active');

  resultsContainer.onclick = (e) => {
    const itemEl = e.target.closest('.search-item');
    if (!itemEl) return;
    const index = parseInt(itemEl.dataset.index, 10);
    selectDestination(matches[index]);
    resultsContainer.classList.remove('active');
  };
}

function highlightQuery(text, query) {
  const idx = text.toLowerCase().indexOf(query.toLowerCase());
  if (idx === -1) return text;
  return `${text.substring(0, idx)}<mark>${text.substring(idx, idx + query.length)}</mark>${text.substring(idx + query.length)}`;
}

function selectDestination(place) {
  destinationPlace = place;
  $('#query').value = place.name;
  $('#destination-title').textContent = place.name;
  $('#destination-category-badge').textContent = place.category || place.kind;
  $('#destination-building-floor').textContent = `${place.building.name} · ${place.floor.name}`;
  $('#navigate-btn').disabled = false;

  // Render Photo Image & Street View Button
  const photoBox = $('#place-photo-box');
  const photoImg = $('#place-photo-img');
  const streetViewBtn = $('#streetview-btn-link');

  const imgUrl = place.imageUrl || place.building?.imageUrl;
  const svUrl = place.streetViewUrl || place.building?.streetViewUrl;

  if (imgUrl && imgUrl.trim() !== '') {
    photoImg.src = imgUrl;
    photoBox.style.display = 'block';

    if (svUrl && svUrl.trim() !== '') {
      streetViewBtn.href = svUrl;
      streetViewBtn.style.display = 'inline-block';
    } else {
      streetViewBtn.style.display = 'none';
    }
  } else {
    photoBox.style.display = 'none';
  }

  // Render Cleanliness & Hours Badge Box
  const statusBox = $('#facility-status-badge-box');
  const fStat = place.facilityStatus;
  if (fStat) {
    statusBox.style.display = 'flex';
    $('#clean-status-text').textContent = fStat.cleaningStatusText || '🟢 ทำความสะอาด & ฆ่าเชื้อแล้ว';
    $('#clean-time-text').textContent = `ฆ่าเชื้อล่าสุดเมื่อ ${fStat.lastCleanedTime || 'ไม่ระบุ'}`;
    $('#open-hours-tag').textContent = fStat.openHours || '24 ชั่วโมง';
  } else {
    statusBox.style.display = 'none';
  }

  // Render Contact Phones Box
  const contactBox = $('#place-contact-box');
  const hasPhone = place.phone && place.phone.trim() !== '';
  const hasExt = place.extension && place.extension.trim() !== '';
  const hasMobile = place.mobile && place.mobile.trim() !== '';

  if (hasPhone || hasExt || hasMobile) {
    contactBox.style.display = 'flex';
    $('#row-ext').style.display = hasExt ? 'block' : 'none';
    if (hasExt) $('#place-ext-val').textContent = place.extension;

    $('#row-phone').style.display = hasPhone ? 'block' : 'none';
    if (hasPhone) {
      const pVal = $('#place-phone-val');
      pVal.textContent = place.phone;
      pVal.href = `tel:${place.phone.replace(/[^0-9]/g, '')}`;
    }

    $('#row-mobile').style.display = hasMobile ? 'block' : 'none';
    if (hasMobile) {
      const mVal = $('#place-mobile-val');
      mVal.textContent = place.mobile;
      mVal.href = `tel:${place.mobile.replace(/[^0-9]/g, '')}`;
    }
  } else {
    contactBox.style.display = 'none';
  }

  // Render Staff Roster Card
  const staffBox = $('#place-staff-box');
  const sResp = place.staffResponsibility;
  if (sResp && (sResp.headOfDept || sResp.dutyOfficer || sResp.housekeeping)) {
    staffBox.style.display = 'block';
    $('#staff-head-name').textContent = sResp.headOfDept || 'ไม่ระบุ';
    $('#staff-duty-name').textContent = sResp.dutyOfficer || 'ไม่ระบุ';
    $('#staff-house-name').textContent = sResp.housekeeping || 'ไม่ระบุ';
  } else {
    staffBox.style.display = 'none';
  }

  if (currentBuilding.id !== place.building.id) {
    $('#building-select').value = place.building.id;
    onBuildingChange();
  }
  if (currentFloor.id !== place.floor.id) {
    $('#floor-select').value = place.floor.id;
    onFloorChange();
  }

  recalculateRoute();
}

function getDestinationNode(place) {
  if (!place || !pathfinder) return null;
  return pathfinder.findClosestNodeToItem(place, place.floor.id);
}

function recalculateRoute() {
  if (!destinationPlace || !pathfinder) return;

  const targetNode = getDestinationNode(destinationPlace);
  if (!targetNode) {
    showToast('⚠️ ไม่พบโหนดเชื่อมต่อสำหรับจุดหมายนี้');
    return;
  }

  const result = pathfinder.findShortestPath(startNodeId, targetNode.id, {
    wheelchairOnly: isWheelchairOnly
  });

  if (!result) {
    showToast('❌ ไม่พบเส้นทางไปยังจุดหมาย กรุณาลองเปลี่ยนโหนดเริ่มต้น');
    $('#routing-summary').style.display = 'none';
    $('#step-by-step-instructions').innerHTML = '<li class="empty-hint">ไม่พบเส้นทางเดิน</li>';
    return;
  }

  $('#routing-summary').style.display = 'flex';
  $('#route-distance').textContent = result.totalDistance;
  $('#route-time').textContent = result.estimatedMinutes;
  $('#route-accessibility').textContent = isWheelchairOnly ? 'โหมดรถเข็น ♿' : 'ทางเดินปกติ';

  const stepsList = $('#step-by-step-instructions');
  stepsList.innerHTML = result.steps
    .map((stepHtml) => `<li><span class="step-bullet">📍</span> <div>${stepHtml}</div></li>`)
    .join('');

  drawRouteOverlay(result.pathNodes);
}

function drawRouteOverlay(pathNodes = null) {
  const svgPath = $('#route-path');
  if (!svgPath) return;

  if (!pathNodes || pathNodes.length === 0) {
    svgPath.setAttribute('d', '');
    return;
  }

  const floorNodes = pathNodes.filter((n) => n.floorId === currentFloor.id);
  if (floorNodes.length < 2) {
    svgPath.setAttribute('d', '');
    return;
  }

  let dStr = `M ${floorNodes[0].x} ${floorNodes[0].y}`;
  for (let i = 1; i < floorNodes.length; i++) {
    dStr += ` L ${floorNodes[i].x} ${floorNodes[i].y}`;
  }

  svgPath.setAttribute('d', dStr);
}

document.addEventListener('DOMContentLoaded', initApp);
