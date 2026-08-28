let mapData = null;
let currentBuilding = null;
let currentFloor = null;
let selectedAsset = null;
let activeCategoryFilter = 'all';
let showGeofenceRadius = true;
let movementTimer = null;
let toastTimer = null;

const $ = selector => document.querySelector(selector);
const $$ = selector => document.querySelectorAll(selector);

function showToast(msg) {
  const toast = $('#toast');
  if (!toast) return;
  toast.innerHTML = msg;
  toast.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove('show'), 3000);
}

async function initAssetTracking() {
  try {
    mapData = await UDHMapStore.load();

    // Start Live Clock
    setInterval(updateClock, 1000);
    updateClock();

    // Populate Building Selector
    const bSelect = $('#map-building-select');
    bSelect.innerHTML = mapData.buildings.map(b => `<option value="${b.id}">${b.name}</option>`).join('');

    bSelect.onchange = onBuildingChange;
    $('#map-floor-select').onchange = onFloorChange;

    setupEventListeners();
    onBuildingChange();

    // Select first asset by default
    if (mapData.assets && mapData.assets.length > 0) {
      selectAsset(mapData.assets[0]);
    }
  } catch (err) {
    console.error('Asset tracking init failed:', err);
    showToast('⚠️ ไม่สามารถโหลดข้อมูลพัสดุได้');
  }
}

function updateClock() {
  const clock = $('#live-clock');
  if (clock) {
    const now = new Date();
    clock.textContent = now.toTimeString().split(' ')[0];
  }
}

function setupEventListeners() {
  // Category Pill Filter
  $$('.category-pills .pill').forEach(pill => {
    pill.onclick = () => {
      $$('.category-pills .pill').forEach(p => p.classList.remove('active'));
      pill.classList.add('active');
      activeCategoryFilter = pill.dataset.cat;
      renderAssetList();
    };
  });

  // Search input
  $('#asset-search').oninput = renderAssetList;

  // Dismiss alert banner
  $('#dismiss-alert-btn').onclick = () => {
    $('#alert-banner').style.display = 'none';
    showToast('🔇 ระงับการแจ้งเตือน Geofence ชั่วคราวแล้ว');
  };

  // Toggle Geofence circles
  $('#btn-toggle-geofence').onclick = () => {
    showGeofenceRadius = !showGeofenceRadius;
    $('#btn-toggle-geofence').classList.toggle('active', showGeofenceRadius);
    renderMapCanvas();
    showToast(showGeofenceRadius ? '🛡️ เปิดแสดงรัศมี Geofence Safe Zone' : '🙈 ซ่อนรัศมี Geofence');
  };

  // Telemetry refresh
  $('#btn-refresh-telemetry').onclick = () => {
    renderAssetList();
    renderMapCanvas();
    showToast('📡 ดึงค่าพิกัด Telemetry ล่าสุดสำเร็จ');
  };

  // Ping Asset Button
  $('#btn-ping-asset').onclick = () => {
    if (!selectedAsset) return;
    showToast(`🔊 ส่งสัญญาณ Ping ไปยังแท็ก <b>${selectedAsset.code}</b> (ไฟ LED กะพริบ + เสียงร้อง)`);
  };

  // History Log Modal
  $('#btn-history-log').onclick = () => {
    if (!selectedAsset) return;
    $('#history-modal').showModal();
  };
  $('#close-history-modal').onclick = () => $('#history-modal').close();

  // Simulation Buttons
  $('#btn-simulate-move').onclick = simulateAssetTransit;
  $('#btn-simulate-breach').onclick = simulateGeofenceBreach;
}

function onBuildingChange() {
  const bId = $('#map-building-select').value;
  currentBuilding = mapData.buildings.find(b => b.id === bId);

  const fSelect = $('#map-floor-select');
  fSelect.innerHTML = currentBuilding.floors.map(f => `<option value="${f.id}">${f.shortName || f.name}</option>`).join('');

  currentFloor = currentBuilding.floors[0];
  renderAssetList();
  renderMapCanvas();
}

function onFloorChange() {
  const fId = $('#map-floor-select').value;
  currentFloor = currentBuilding.floors.find(f => f.id === fId);
  renderMapCanvas();
}

function getFilteredAssets() {
  if (!mapData || !Array.isArray(mapData.assets)) return [];
  const q = $('#asset-search').value.trim().toLowerCase();

  return mapData.assets.filter(asset => {
    const matchCat = activeCategoryFilter === 'all' || asset.category === activeCategoryFilter;
    const matchSearch = !q || `${asset.name} ${asset.code} ${asset.serialNumber || ''} ${asset.category}`.toLowerCase().includes(q);
    return matchCat && matchSearch;
  });
}

function renderAssetList() {
  const container = $('#asset-list-container');
  const assets = getFilteredAssets();
  $('#asset-count-badge').textContent = `${assets.length} รายการ`;

  if (assets.length === 0) {
    container.innerHTML = `<div class="empty-list">ไม่พบพัสดุหรืออุปกรณ์ที่ตรงกับเงื่อนไข</div>`;
    return;
  }

  container.innerHTML = assets.map(asset => {
    const isSelected = selectedAsset && selectedAsset.id === asset.id;
    let statusClass = 'status-green';
    let icon = '📦';

    if (asset.status === 'alert_out_of_zone') {
      statusClass = 'status-red blink';
      icon = '🚨';
    } else if (asset.status === 'in-transit') {
      statusClass = 'status-blue';
      icon = '🚚';
    } else if (asset.category.includes('ยาราคาสูง')) {
      icon = '💊';
    } else if (asset.category.includes('เลือด')) {
      icon = '🩸';
    }

    return `
      <div class="asset-card-item ${isSelected ? 'active' : ''} ${asset.status === 'alert_out_of_zone' ? 'alert-card' : ''}" data-id="${asset.id}">
        <div class="card-top">
          <span class="card-icon">${icon}</span>
          <div class="card-title-group">
            <strong>${asset.name}</strong>
            <small>รหัส: ${asset.code} · ${asset.category}</small>
          </div>
          <span class="battery-tag">🔋 ${asset.batteryPercent || 90}%</span>
        </div>
        <div class="card-bottom">
          <span class="location-chip">📍 ${asset.roomName || asset.assignedZone || 'ไม่ระบุห้อง'}</span>
          <span class="status-badge ${statusClass}">${asset.statusText || asset.status}</span>
        </div>
      </div>
    `;
  }).join('');

  container.onclick = (e) => {
    const item = e.target.closest('.asset-card-item');
    if (!item) return;
    const found = mapData.assets.find(a => a.id === item.dataset.id);
    if (found) selectAsset(found);
  };
}

function selectAsset(asset) {
  selectedAsset = asset;
  renderAssetList();

  // Populate Right Detail Panel
  $('#detail-category-badge').textContent = asset.category || 'พัสดุราคาสูง';
  $('#detail-title').textContent = asset.name;
  $('#detail-code-serial').textContent = `รหัส: ${asset.code} | Serial: ${asset.serialNumber || 'N/A'}`;
  
  const statusDot = $('#detail-status-dot');
  statusDot.className = 'status-dot ' + (asset.status === 'alert_out_of_zone' ? 'red blink' : (asset.status === 'in-transit' ? 'blue' : 'green'));
  $('#detail-status-text').textContent = asset.statusText || asset.status;
  
  $('#detail-value').textContent = `฿${(asset.valueThb || 0).toLocaleString()}`;
  $('#detail-location-floor').textContent = `${asset.buildingId === 'somdet' ? 'อาคารสมเด็จฯ' : 'อาคารผู้ป่วยนอก'} (ชั้น ${asset.floorId || '1'})`;
  $('#detail-location-room').textContent = asset.roomName || 'ไม่ระบุห้อง';
  $('#detail-assigned-zone').textContent = asset.assignedZone || 'ไม่ได้กำหนดโซนเข้มงวด';
  $('#detail-battery').textContent = `🔋 ${asset.batteryPercent || 85}% ( Tag: ${asset.beaconTagId || 'BLE'} )`;
  $('#detail-last-update').textContent = asset.lastUpdate || '10 วินาทีที่แล้ว';

  // Custody info
  if (asset.custody) {
    $('#custody-sender').textContent = asset.custody.sender || asset.custody.responsibleOfficer || 'คลังพัสดุกลาง';
    $('#custody-receiver').textContent = asset.custody.receiver || asset.custody.department || 'หน่วยงานปลายทาง';
    $('#custody-temp').textContent = asset.custody.tempControl || 'ควบคุมอุณหภูมิห้องปกติ (15 - 25 °C)';
  }

  // Switch building & floor map to show selected asset
  if (asset.buildingId && asset.buildingId !== currentBuilding.id) {
    $('#map-building-select').value = asset.buildingId;
    onBuildingChange();
  }
  if (asset.floorId && asset.floorId !== currentFloor.id) {
    $('#map-floor-select').value = asset.floorId;
    onFloorChange();
  }

  renderMapCanvas();
}

function renderMapCanvas() {
  const pinsLayer = $('#asset-pins-layer');
  const geofenceLayer = $('#geofence-circles-layer');
  pinsLayer.innerHTML = '';
  geofenceLayer.innerHTML = '';

  if (!mapData || !currentFloor) return;

  // Filter assets located on current building and floor
  const floorAssets = mapData.assets.filter(a => a.buildingId === currentBuilding.id && a.floorId === currentFloor.id);

  floorAssets.forEach(asset => {
    // 1. Render Geofence Circle if enabled
    if (showGeofenceRadius) {
      const circle = document.createElement('div');
      circle.className = `geofence-circle ${asset.status === 'alert_out_of_zone' ? 'breached' : ''}`;
      circle.style.left = `${asset.x}%`;
      circle.style.top = `${asset.y}%`;
      geofenceLayer.appendChild(circle);
    }

    // 2. Render Pin Marker
    const isSelected = selectedAsset && selectedAsset.id === asset.id;
    const pin = document.createElement('div');
    pin.className = `asset-map-pin ${isSelected ? 'selected' : ''} ${asset.status === 'alert_out_of_zone' ? 'alert-pin' : ''}`;
    pin.style.left = `${asset.x}%`;
    pin.style.top = `${asset.y}%`;

    let icon = '📦';
    if (asset.category.includes('ยาราคาสูง')) icon = '💊';
    else if (asset.category.includes('เลือด')) icon = '🩸';
    else if (asset.category.includes('อุปกรณ์')) icon = '🫀';

    pin.innerHTML = `
      <div class="pin-badge">${icon} <b>${asset.code}</b></div>
      <div class="pin-radar-pulse"></div>
    `;

    pin.onclick = () => selectAsset(asset);
    pinsLayer.appendChild(pin);
  });
}

function simulateAssetTransit() {
  // Find in-transit parcel (e.g. HCD-9901)
  const parcel = mapData.assets.find(a => a.code === 'HCD-9901');
  if (!parcel) return;

  selectAsset(parcel);
  showToast('🚚 เริ่มการส่งสัญญาณพิกัดพัสดุยาราคาสูง #HCD-9901 ขณะขนส่ง...');

  let step = 0;
  const pathCoords = [
    { x: 64, y: 12, roomName: 'โถงคลังยา ชั้น 1' },
    { x: 76, y: 36, roomName: 'ทางเดินหน้าห้องยา' },
    { x: 76, y: 50, roomName: 'โถงลิฟต์ A (กำลังขึ้นชั้น 3)' },
    { x: 51, y: 48, roomName: 'โถงกลาง ชั้น 3', floorId: 'opd-f3' },
    { x: 80, y: 48, roomName: 'เคาน์เตอร์พยาบาล ชั้น 3 (ถึงจุดหมายแล้ว)', floorId: 'opd-f3' }
  ];

  clearInterval(movementTimer);
  movementTimer = setInterval(() => {
    if (step >= pathCoords.length) {
      clearInterval(movementTimer);
      parcel.status = 'in-use';
      parcel.statusText = '✅ จัดส่งถึงจุดหมายเรียบร้อยแล้ว';
      selectAsset(parcel);
      showToast('🎉 พัสดุยาราคาสูง #HCD-9901 จัดส่งถึงคลินิกเคมีบำบัด ชั้น 3 เรียบร้อยแล้ว');
      return;
    }

    const c = pathCoords[step];
    parcel.x = c.x;
    parcel.y = c.y;
    parcel.roomName = c.roomName;
    if (c.floorId) parcel.floorId = c.floorId;

    selectAsset(parcel);
    step++;
  }, 2000);
}

function simulateGeofenceBreach() {
  const asset = mapData.assets.find(a => a.code === 'VM-008');
  if (!asset) return;

  asset.status = 'alert_out_of_zone';
  asset.statusText = '⚠️ เคลื่อนย้ายออกนอกโซน!';
  asset.warningMessage = 'แจ้งเตือน: อุปกรณ์ถูกเคลื่อนย้ายออกจากหอผู้ป่วยอายุรกรรม ชั้น 3 ลงมายังบริเวณลิฟต์ A ชั้น 1';

  selectAsset(asset);
  $('#alert-banner').style.display = 'flex';
  $('#alert-text').textContent = asset.warningMessage;
  showToast('🚨 <b>GEOFENCE ALARM:</b> พบอุปกรณ์ราคาสูง #VM-008 เคลื่อนย้ายออกนอกเขต!');
}

document.addEventListener('DOMContentLoaded', initAssetTracking);
