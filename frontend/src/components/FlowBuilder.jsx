import { useCallback, useRef, useState, useEffect } from 'react';
import ReactFlow, {
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  addEdge,
} from 'reactflow';
import 'reactflow/dist/style.css';

import TextNode from './nodes/TextNode';
import ButtonNode from './nodes/ButtonNode';
import ConditionNode from './nodes/ConditionNode';
import ImageNode from './nodes/ImageNode';  
import VideoNode from './nodes/VideoNode'; 
import DelayNode from './nodes/DelayNode'; 
import Sidebar from './Sidebar';
import Toolbar from './Toolbar';
import { flowsApi } from '../api/flowsApi';
import NodeSettings from './NodeSettings';
import { validateFlow } from '../utils/flowValidator';
import ValidationResults from './ValidationResults';
import FlowsList from './FlowsList';

const nodeTypes = {
  textNode: TextNode,
  buttonNode: ButtonNode,
  conditionNode: ConditionNode,
  imageNode: ImageNode,     
  videoNode: VideoNode,      
  delayNode: DelayNode,
};

const initialNodes = [
  {
    id: '1',
    type: 'input',
    data: { label: '🚀 Start' },
    position: { x: 250, y: 25 },
  },
];

const initialEdges = [];

let id = 2;
const getId = () => `node_${id++}`;

export default function FlowBuilder() {
  const reactFlowWrapper = useRef(null);
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
  const [reactFlowInstance, setReactFlowInstance] = useState(null);
  const [botId] = useState(1);
  const [saveStatus, setSaveStatus] = useState('');
  const [selectedNode, setSelectedNode] = useState(null); 
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [validationResult, setValidationResult] = useState(null);
  const [currentFlowId, setCurrentFlowId] = useState(null);
  const [currentFlowName, setCurrentFlowName] = useState('My Bot Flow');

  const onConnect = useCallback(
    (params) => setEdges((eds) => addEdge(params, eds)),
    [setEdges],
  );

  const onDragOver = useCallback((event) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = 'move';
  }, []);

  const onDrop = useCallback(
    (event) => {
      event.preventDefault();

      const type = event.dataTransfer.getData('application/reactflow');

      if (typeof type === 'undefined' || !type) {
        return;
      }

      const position = reactFlowInstance.screenToFlowPosition({
        x: event.clientX,
        y: event.clientY,
      });

      const newNode = {
        id: getId(),
        type,
        position,
        data: { label: `${type} node` },
      };

      setNodes((nds) => nds.concat(newNode));
    },
    [reactFlowInstance, setNodes],
  );

  // Обработчик клика по ноде
  const onNodeClick = useCallback((event, node) => {
    setSelectedNode(node);
    setIsSettingsOpen(true);
  }, []);

  // Сохранение настроек ноды
  const onSaveNodeSettings = useCallback((nodeId, newData) => {
    setNodes((nds) =>
      nds.map((node) => {
        if (node.id === nodeId) {
          return {
            ...node,
            data: { ...node.data, ...newData }
          };
        }
        return node;
      })
    );
  }, [setNodes]);

  // Сохранение в API
  const onSave = useCallback(async () => {
    if (reactFlowInstance) {
      // Сначала валидируем
      const validation = validateFlow(nodes, edges);
      
      if (!validation.isValid) {
        setValidationResult(validation);
        return;
      }
      
      try {
        const flow = reactFlowInstance.toObject();
        
        const cleanNodes = flow.nodes.map(node => ({
          id: node.id,
          type: node.type,
          position: node.position,
          data: node.data || {}
        }));
        
        const cleanEdges = flow.edges.map(edge => ({
          id: edge.id,
          source: edge.source,
          target: edge.target,
          sourceHandle: edge.sourceHandle || null,
          targetHandle: edge.targetHandle || null
        }));
        
        const result = await flowsApi.saveFlow(botId, {
          nodes: cleanNodes,
          edges: cleanEdges,
          name: currentFlowName
        }, currentFlowId);
        
        // Сохраняем flow_id если это новый flow
        if (!currentFlowId && result.flow_id) {
          setCurrentFlowId(result.flow_id);
        }
        
        setSaveStatus('✅ Saved to server!');
        setTimeout(() => setSaveStatus(''), 2000);
      } catch (error) {
        console.error('Save error:', error);
        setSaveStatus('❌ Save failed!');
        setTimeout(() => setSaveStatus(''), 2000);
      }
    }
  }, [reactFlowInstance, botId, nodes, edges, currentFlowId, currentFlowName]);

  // Загрузка активного flow
  const onLoad = useCallback(async () => {
    try {
      const data = await flowsApi.listFlows(botId);
      const activeFlow = data.flows?.find(f => f.is_active);
      
      if (activeFlow) {
        onSelectFlow(activeFlow.flow_id);
      } else {
        setSaveStatus('⚠️ No active flow found!');
        setTimeout(() => setSaveStatus(''), 2000);
      }
    } catch (error) {
      console.error('Load error:', error);
      setSaveStatus('⚠️ No saved flow found!');
      setTimeout(() => setSaveStatus(''), 2000);
    }
  }, [botId]);

  // Выбор конкретного flow
  const onSelectFlow = useCallback(async (flowId) => {
    try {
      const data = await flowsApi.getFlow(botId, flowId);
      if (data && data.flow) {
        setNodes(data.flow.nodes || []);
        setEdges(data.flow.edges || []);
        setCurrentFlowId(flowId);
        setCurrentFlowName(data.name || 'Untitled Flow');
        setSaveStatus('✅ Flow loaded!');
        setTimeout(() => setSaveStatus(''), 2000);
      }
    } catch (error) {
      console.error('Load error:', error);
      setSaveStatus('❌ Failed to load flow!');
      setTimeout(() => setSaveStatus(''), 2000);
    }
  }, [botId, setNodes, setEdges]);

  // Создание нового flow
  const onNewFlow = useCallback(() => {
    if (confirm('Create a new flow? Current changes will be cleared.')) {
      setNodes(initialNodes);
      setEdges(initialEdges);
      setCurrentFlowId(null);
      setCurrentFlowName('New Flow');
      setSaveStatus('✅ New flow created!');
      setTimeout(() => setSaveStatus(''), 2000);
    }
  }, [setNodes, setEdges]);

  // Удаление flow
  const onDeleteFlow = useCallback(async (flowId) => {
    try {
      await flowsApi.deleteFlow(botId, flowId);
      
      // Если удалили текущий flow - создаём новый
      if (flowId === currentFlowId) {
        setNodes(initialNodes);
        setEdges(initialEdges);
        setCurrentFlowId(null);
        setCurrentFlowName('New Flow');
      }
      
      setSaveStatus('✅ Flow deleted!');
      setTimeout(() => setSaveStatus(''), 2000);
    } catch (error) {
      console.error('Delete error:', error);
      setSaveStatus('❌ Failed to delete flow!');
      setTimeout(() => setSaveStatus(''), 2000);
    }
  }, [botId, currentFlowId, setNodes, setEdges]);

  const onClear = useCallback(() => {
    if (confirm('Are you sure you want to clear the flow?')) {
      setNodes(initialNodes);
      setEdges(initialEdges);
      setSaveStatus('✅ Flow cleared!');
      setTimeout(() => setSaveStatus(''), 2000);
    }
  }, [setNodes, setEdges]);
  
  const onValidate = useCallback(() => {
    const validation = validateFlow(nodes, edges);
    setValidationResult(validation);
  }, [nodes, edges]);

  return (
    <div ref={reactFlowWrapper} style={{ width: '100vw', height: '100vh' }}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        onInit={setReactFlowInstance}
        onDrop={onDrop}
        onDragOver={onDragOver}
        onNodeClick={onNodeClick}
        nodeTypes={nodeTypes}
        fitView
      >
        <Controls />
        <MiniMap />
        <Background variant="dots" gap={12} size={1} />
      </ReactFlow>
      <Sidebar />
      <FlowsList
        botId={botId}
        currentFlowId={currentFlowId}
        onSelectFlow={onSelectFlow}
        onNewFlow={onNewFlow}
        onDeleteFlow={onDeleteFlow}
      />
      <Toolbar onSave={onSave} onLoad={onLoad} onClear={onClear} onValidate={onValidate}/>
      {saveStatus && (
        <div style={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          background: 'white',
          padding: '20px 40px',
          borderRadius: '8px',
          boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
          fontSize: '18px',
          fontWeight: 'bold',
          zIndex: 1000
        }}>
          {saveStatus}
        </div>
      )}
      <NodeSettings
        node={selectedNode}
        isOpen={isSettingsOpen}
        onClose={() => setIsSettingsOpen(false)}
        onSave={onSaveNodeSettings}
      />
      <ValidationResults
        validation={validationResult}
        onClose={() => setValidationResult(null)}
      />
    </div>
  );
}
