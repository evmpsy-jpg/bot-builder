export function validateFlow(nodes, edges) {
  const errors = [];
  const warnings = [];

  // 1. Проверка наличия Start node
  const startNode = nodes.find(node => node.type === 'input');
  if (!startNode) {
    errors.push('❌ Flow must have a Start node');
  }

  // 2. Проверка заполненности обязательных полей
  nodes.forEach(node => {
    switch (node.type) {
      case 'textNode':
        if (!node.data.text || node.data.text.trim() === '') {
          errors.push(`❌ Text node "${node.id}" is empty`);
        }
        break;
      
      case 'imageNode':
        if (!node.data.imageUrl || node.data.imageUrl.trim() === '') {
          errors.push(`❌ Image node "${node.id}" has no image URL`);
        }
        break;
      
      case 'videoNode':
        if (!node.data.videoUrl || node.data.videoUrl.trim() === '') {
          errors.push(`❌ Video node "${node.id}" has no video URL`);
        }
        break;
      
      case 'buttonNode':
        if (!node.data.buttonText || node.data.buttonText.trim() === '') {
          errors.push(`❌ Button node "${node.id}" has no button text`);
        }
        break;
      
      case 'delayNode':
        if (!node.data.delay || node.data.delay < 1) {
          errors.push(`❌ Delay node "${node.id}" has invalid delay value`);
        }
        break;
      
      case 'conditionNode':
        if (!node.data.conditionType || !node.data.conditionValue) {
          errors.push(`❌ Condition node "${node.id}" is not configured`);
        }
        break;
    }
  });

  // 3. Проверка изолированных нод (кроме Start)
  const connectedNodeIds = new Set();
  edges.forEach(edge => {
    connectedNodeIds.add(edge.source);
    connectedNodeIds.add(edge.target);
  });

  nodes.forEach(node => {
    if (node.type !== 'input' && !connectedNodeIds.has(node.id)) {
      warnings.push(`⚠️ Node "${node.id}" is not connected`);
    }
  });

  // 4. Проверка на циклы (простая проверка)
  const hasCycle = detectCycle(nodes, edges);
  if (hasCycle) {
    warnings.push('⚠️ Flow contains a cycle (loop detected)');
  }

  // 5. Проверка что у Start есть выходящее соединение
  if (startNode) {
    const hasOutgoing = edges.some(edge => edge.source === startNode.id);
    if (!hasOutgoing) {
      errors.push('❌ Start node has no outgoing connections');
    }
  }

  return {
    isValid: errors.length === 0,
    errors,
    warnings
  };
}

// Простая проверка циклов (DFS)
function detectCycle(nodes, edges) {
  const graph = {};
  nodes.forEach(node => {
    graph[node.id] = [];
  });
  
  edges.forEach(edge => {
    if (graph[edge.source]) {
      graph[edge.source].push(edge.target);
    }
  });

  const visited = new Set();
  const recStack = new Set();

  function dfs(nodeId) {
    visited.add(nodeId);
    recStack.add(nodeId);

    for (const neighbor of (graph[nodeId] || [])) {
      if (!visited.has(neighbor)) {
        if (dfs(neighbor)) return true;
      } else if (recStack.has(neighbor)) {
        return true; // Цикл найден
      }
    }

    recStack.delete(nodeId);
    return false;
  }

  for (const nodeId in graph) {
    if (!visited.has(nodeId)) {
      if (dfs(nodeId)) return true;
    }
  }

  return false;
}
