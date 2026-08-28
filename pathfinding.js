/**
 * UDH Hospital Indoor Pathfinding Engine (Dijkstra Shortest Path with Multi-floor & Wheelchair routing)
 */
(function () {
  class HospitalPathfinder {
    constructor(mapData) {
      this.mapData = mapData;
      this.nodes = new Map();
      this.adjacencyList = new Map();
      this.buildGraph();
    }

    buildGraph() {
      this.nodes.clear();
      this.adjacencyList.clear();

      if (!this.mapData || !Array.isArray(this.mapData.buildings)) return;

      // 1. Collect all floor nodes
      this.mapData.buildings.forEach((building) => {
        building.floors.forEach((floor) => {
          if (Array.isArray(floor.routeNodes)) {
            floor.routeNodes.forEach((node) => {
              const fullNode = {
                ...node,
                buildingId: node.buildingId || building.id,
                buildingName: building.name,
                floorId: node.floorId || floor.id,
                floorName: floor.name,
                floorLevel: floor.level
              };
              this.nodes.set(node.id, fullNode);
              this.adjacencyList.set(node.id, []);
            });
          }

          // Intra-floor edges
          if (Array.isArray(floor.routeEdges)) {
            floor.routeEdges.forEach((edge) => {
              this.addEdge(edge.from, edge.to, edge.distance, {
                accessibleWheelchair: edge.accessibleWheelchair !== false,
                isElevator: !!edge.isElevator,
                isStairs: !!edge.isStairs
              });
            });
          }
        });
      });

      // 2. Inter-floor edges (Elevators & Stairs between floors)
      if (Array.isArray(this.mapData.interFloorEdges)) {
        this.mapData.interFloorEdges.forEach((edge) => {
          this.addEdge(edge.from, edge.to, edge.distance || 30, {
            accessibleWheelchair: edge.accessibleWheelchair !== false,
            isElevator: !!edge.isElevator,
            isStairs: !!edge.isStairs,
            isInterFloor: true
          });
        });
      }
    }

    addEdge(u, v, weight, attributes = {}) {
      if (!this.nodes.has(u) || !this.nodes.has(v)) return;
      
      const edgeUtoV = { node: v, weight, ...attributes };
      const edgeVtoU = { node: u, weight, ...attributes };

      this.adjacencyList.get(u).push(edgeUtoV);
      this.adjacencyList.get(v).push(edgeVtoU);
    }

    findShortestPath(startNodeId, targetNodeId, options = {}) {
      const wheelchairOnly = !!options.wheelchairOnly;

      if (!this.nodes.has(startNodeId) || !this.nodes.has(targetNodeId)) {
        return null;
      }

      const distances = new Map();
      const previous = new Map();
      const edgeUsed = new Map();
      const unvisited = new Set();

      this.nodes.forEach((_, id) => {
        distances.set(id, Infinity);
        unvisited.add(id);
      });

      distances.set(startNodeId, 0);

      while (unvisited.size > 0) {
        // Pick unvisited node with smallest distance
        let currentId = null;
        let smallestDistance = Infinity;

        for (const id of unvisited) {
          if (distances.get(id) < smallestDistance) {
            smallestDistance = distances.get(id);
            currentId = id;
          }
        }

        if (currentId === null || smallestDistance === Infinity) {
          break; // Remaining nodes un-reachable
        }

        if (currentId === targetNodeId) {
          break; // Target reached
        }

        unvisited.delete(currentId);

        const neighbors = this.adjacencyList.get(currentId) || [];
        for (const neighbor of neighbors) {
          if (!unvisited.has(neighbor.node)) continue;

          // Wheelchair constraint check
          if (wheelchairOnly && (!neighbor.accessibleWheelchair || neighbor.isStairs)) {
            continue;
          }

          const altDistance = distances.get(currentId) + neighbor.weight;
          if (altDistance < distances.get(neighbor.node)) {
            distances.set(neighbor.node, altDistance);
            previous.set(neighbor.node, currentId);
            edgeUsed.set(neighbor.node, neighbor);
          }
        }
      }

      if (distances.get(targetNodeId) === Infinity) {
        return null; // Path not found
      }

      // Reconstruct path
      const pathNodes = [];
      let curr = targetNodeId;
      while (curr) {
        pathNodes.unshift(this.nodes.get(curr));
        curr = previous.get(curr);
      }

      const totalDistance = distances.get(targetNodeId);
      const steps = this.generateStepInstructions(pathNodes, edgeUsed);

      return {
        totalDistance,
        estimatedMinutes: Math.max(1, Math.ceil(totalDistance / 40)),
        pathNodes,
        steps
      };
    }

    findClosestNodeToItem(item, floorId) {
      if (!item) return null;
      let candidates = Array.from(this.nodes.values()).filter(n => n.floorId === floorId);
      if (candidates.length === 0) candidates = Array.from(this.nodes.values());

      let bestNode = null;
      let minSqDist = Infinity;

      const itemX = item.x + (item.w ? item.w / 2 : 0);
      const itemY = item.y + (item.h ? item.h / 2 : 0);

      candidates.forEach((node) => {
        const dx = node.x - itemX;
        const dy = node.y - itemY;
        const sqDist = dx * dx + dy * dy;
        if (sqDist < minSqDist) {
          minSqDist = sqDist;
          bestNode = node;
        }
      });

      return bestNode;
    }

    generateStepInstructions(pathNodes, edgeUsed) {
      if (pathNodes.length <= 1) return ['คุณอยู่ที่จุดหมายแล้ว'];

      const steps = [];
      steps.push(`เริ่มต้นเดินจาก <b>${pathNodes[0].name}</b> (${pathNodes[0].floorName})`);

      for (let i = 0; i < pathNodes.length - 1; i++) {
        const curr = pathNodes[i];
        const next = pathNodes[i + 1];
        const edge = edgeUsed.get(next.id);

        if (curr.floorId !== next.floorId) {
          if (edge && edge.isElevator) {
            steps.push(`ขึ้น<b>ลิฟต์</b>จาก ${curr.floorName} ไปยัง <b>${next.floorName}</b>`);
          } else if (edge && edge.isStairs) {
            steps.push(`เดินขึ้น/ลง<b>บันได</b>ไปที่ <b>${next.floorName}</b>`);
          } else {
            steps.push(`เปลี่ยนชั้นไปยัง <b>${next.floorName}</b>`);
          }
        } else {
          const distStr = edge ? `${edge.weight} เมตร` : '';
          steps.push(`เดินตรงไป<sup>${distStr}</sup> ไปยัง <b>${next.name}</b>`);
        }
      }

      steps.push(`ถึงจุดหมายปลายทางแล้ว 🎉`);
      return steps;
    }
  }

  window.UDHPathfinder = HospitalPathfinder;
})();
