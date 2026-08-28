(function () {
  const KEY = 'udh-map-data-v1';
  const clone = (value) => JSON.parse(JSON.stringify(value));
  
  function valid(data) {
    return (
      data &&
      Array.isArray(data.buildings) &&
      data.buildings.every((b) => b.id && b.name && Array.isArray(b.floors))
    );
  }

  async function load() {
    const saved = localStorage.getItem(KEY);
    if (saved) {
      try {
        const data = JSON.parse(saved);
        if (valid(data)) return data;
      } catch (err) {
        console.warn('LocalStorage data corrupt, falling back to map-data.json', err);
      }
    }
    const response = await fetch('map-data.json');
    if (!response.ok) throw new Error('ไม่สามารถโหลด map-data.json ได้');
    const data = await response.json();
    if (!valid(data)) throw new Error('โครงสร้าง map-data.json ไม่ถูกต้อง');
    return data;
  }

  function save(data) {
    if (!valid(data)) throw new Error('ข้อมูลแผนที่ไม่ถูกต้อง');
    localStorage.setItem(KEY, JSON.stringify(data));
  }

  function download(data) {
    const link = document.createElement('a');
    link.href = URL.createObjectURL(
      new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
    );
    link.download = 'map-data.json';
    link.click();
    URL.revokeObjectURL(link.href);
  }

  function getAssets(data, filter = {}) {
    if (!data || !Array.isArray(data.assets)) return [];
    let list = data.assets;
    if (filter.category) list = list.filter(a => a.category === filter.category);
    if (filter.status) list = list.filter(a => a.status === filter.status);
    if (filter.buildingId) list = list.filter(a => a.buildingId === filter.buildingId);
    if (filter.floorId) list = list.filter(a => a.floorId === filter.floorId);
    if (filter.query) {
      const q = filter.query.toLowerCase();
      list = list.filter(a =>
        a.name.toLowerCase().includes(q) ||
        a.code.toLowerCase().includes(q) ||
        (a.serialNumber && a.serialNumber.toLowerCase().includes(q))
      );
    }
    return list;
  }

  window.UDHMapStore = {
    load,
    save,
    download,
    clone,
    valid,
    getAssets,
    reset: () => localStorage.removeItem(KEY)
  };
})();
