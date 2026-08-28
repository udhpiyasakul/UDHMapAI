let mapData = null;

const $ = (selector) => document.querySelector(selector);

async function start() {
  try {
    mapData = await UDHMapStore.load();
    const imageCAD = mapData.campusMap?.imageUrl || 'Map.jpg';
    const imageSat90 = mapData.campusMap?.satelliteUrl || 'google-satellite-rotated90.jpg';

    $('#site-map').src = imageCAD;
    $('#satellite-bg-img').src = imageSat90;
    $('#large-map').src = imageCAD;

    setupLayerSwitcher();
    renderBuildings();

    $('#building-search').oninput = renderBuildings;
  } catch (err) {
    console.error(err);
    $('#site-map').src = 'Map.jpg';
    $('#satellite-bg-img').src = 'google-satellite-rotated90.jpg';
  }
}

function setupLayerSwitcher() {
  const btnCAD = $('#layer-cad');
  const btnSat = $('#layer-sat');
  const btnOverlay = $('#layer-overlay');
  const opacityBar = $('#opacity-control-bar');
  const rotBar = $('#rotation-selector-bar');

  const cadImg = $('#site-map');
  const satImg = $('#satellite-bg-img');
  const slider = $('#layer-opacity-range');

  const btnRot90 = $('#rot-90');
  const btnRot0 = $('#rot-0');

  btnCAD.onclick = () => {
    setActiveTab(btnCAD);
    satImg.style.display = 'none';
    cadImg.style.display = 'block';
    cadImg.style.opacity = '1';
    opacityBar.style.display = 'none';
    rotBar.style.display = 'none';
  };

  btnSat.onclick = () => {
    setActiveTab(btnSat);
    satImg.style.display = 'block';
    satImg.style.opacity = '1';
    cadImg.style.display = 'none';
    opacityBar.style.display = 'none';
    rotBar.style.display = 'flex';
  };

  btnOverlay.onclick = () => {
    setActiveTab(btnOverlay);
    satImg.style.display = 'block';
    satImg.style.opacity = '1';
    cadImg.style.display = 'block';
    cadImg.style.opacity = slider.value / 100;
    opacityBar.style.display = 'flex';
    rotBar.style.display = 'flex';
  };

  // Rotation Tabs
  btnRot90.onclick = () => {
    btnRot90.classList.add('active');
    btnRot0.classList.remove('active');
    satImg.src = 'google-satellite-rotated90.jpg';
  };

  btnRot0.onclick = () => {
    btnRot0.classList.add('active');
    btnRot90.classList.remove('active');
    satImg.src = 'google-satellite.jpg';
  };

  slider.oninput = () => {
    const opacityVal = slider.value / 100;
    $('#opacity-pct-label').textContent = `${slider.value}%`;
    cadImg.style.opacity = opacityVal;
  };

  // Modal switcher
  const modalTabCAD = $('#modal-show-cad');
  const modalTabSat90 = $('#modal-show-sat-90');
  const modalTabSat0 = $('#modal-show-sat-0');
  const largeMap = $('#large-map');

  modalTabCAD.onclick = () => {
    setModalTab(modalTabCAD);
    largeMap.src = 'Map.jpg';
    $('#modal-title').textContent = 'ผังบริเวณโรงพยาบาลอุดรธานี (Map.jpg)';
  };

  modalTabSat90.onclick = () => {
    setModalTab(modalTabSat90);
    largeMap.src = 'google-satellite-rotated90.jpg';
    $('#modal-title').textContent = 'ภาพถ่ายดาวเทียม Google Maps (หมุน 90° ขนานผัง CAD / หนองประจักษ์อยู่ด้านล่าง)';
  };

  modalTabSat0.onclick = () => {
    setModalTab(modalTabSat0);
    largeMap.src = 'google-satellite.jpg';
    $('#modal-title').textContent = 'ภาพถ่ายดาวเทียม Google Maps (0° ทิศเหนือจริง)';
  };
}

function setActiveTab(activeBtn) {
  document.querySelectorAll('.layer-tab').forEach((b) => b.classList.remove('active'));
  activeBtn.classList.add('active');
}

function setModalTab(activeBtn) {
  document.querySelectorAll('.modal-tab').forEach((b) => b.classList.remove('active'));
  activeBtn.classList.add('active');
}

function renderBuildings() {
  if (!mapData || !Array.isArray(mapData.buildings)) return;

  const q = $('#building-search').value.trim().toLowerCase();
  const filtered = mapData.buildings.filter((b) => {
    if (!q) return true;
    const text = `หมายเลข ${b.mapNumber || ''} ${b.name} ${b.code || ''} ${b.description || ''}`.toLowerCase();
    return text.includes(q);
  });

  $('#count').textContent = `${filtered.length} อาคาร`;

  const listContainer = $('#buildings');
  if (filtered.length === 0) {
    listContainer.innerHTML = `<div class="empty-msg">ไม่พบอาคารที่ตรงกับหมายเลขหรือชื่อ "${q}"</div>`;
    return;
  }

  listContainer.innerHTML = filtered
    .map(
      (b) => `
    <button class="building-card" data-id="${b.id}">
      <div class="building-num-badge">ผัง #${b.mapNumber || '?'}</div>
      <div class="building-info-col">
        <strong>${b.name}</strong>
        <p class="b-desc">${b.description || 'บริการทางการแพทย์และบริการผู้ป่วย'}</p>
        <small class="b-meta">${b.code || b.id} · มีข้อมูลแผนผัง ${b.floors ? b.floors.length : 0} ชั้น</small>
      </div>
      <span class="chevron-icon">›</span>
    </button>
  `
    )
    .join('');

  listContainer.onclick = (event) => {
    const card = event.target.closest('[data-id]');
    if (card) {
      location.href = `index.html?building=${encodeURIComponent(card.dataset.id)}`;
    }
  };
}

$('#zoom').onclick = () => $('#viewer').showModal();
$('#close').onclick = () => $('#viewer').close();

document.addEventListener('DOMContentLoaded', start);
