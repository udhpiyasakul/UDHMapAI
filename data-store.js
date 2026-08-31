(function () {
  const KEY = 'udh-map-data-v2';
  const clone = (value) => JSON.parse(JSON.stringify(value));
  
  function valid(data) {
    return (
      data &&
      Array.isArray(data.buildings) &&
      data.buildings.every((b) => b.id && b.name && Array.isArray(b.floors))
    );
  }

  async function load() {
    // 1. Always fetch map-data.json to compare schemaVersion
    let serverData = null;
    try {
      const response = await fetch(`map-data.json?t=${Date.now()}`);
      if (response.ok) {
        serverData = await response.json();
      }
    } catch (e) {
      console.warn('Could not fetch server map-data.json:', e);
    }

    // 2. Check LocalStorage
    const saved = localStorage.getItem(KEY);
    if (saved) {
      try {
        const localData = JSON.parse(saved);
        // If serverData has a newer or different schemaVersion, prioritize serverData
        if (serverData && valid(serverData)) {
          if (!localData.schemaVersion || localData.schemaVersion !== serverData.schemaVersion) {
            console.log('New schemaVersion detected on server. Updating LocalStorage to:', serverData.schemaVersion);
            localStorage.setItem(KEY, JSON.stringify(serverData));
            return serverData;
          }
        }
        if (valid(localData)) return localData;
      } catch (err) {
        console.warn('LocalStorage data corrupt, falling back to map-data.json', err);
      }
    }

    // Fallback to serverData
    if (serverData && valid(serverData)) {
      localStorage.setItem(KEY, JSON.stringify(serverData));
      return serverData;
    }

    throw new Error('ไม่สามารถโหลด map-data.json ได้');
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
    reset: () => {
      localStorage.removeItem(KEY);
      localStorage.removeItem('udh-map-data-v1');
    }
  };
})();
