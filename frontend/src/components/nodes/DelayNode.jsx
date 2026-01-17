import { Handle, Position } from 'reactflow';

export default function DelayNode({ data }) {
  return (
    <div style={{
      padding: '10px',
      border: '2px solid #f59e0b',
      borderRadius: '8px',
      background: 'white',
      minWidth: '150px'
    }}>
      <Handle type="target" position={Position.Top} />
      <div style={{ fontWeight: 'bold', marginBottom: '5px' }}>⏰ Delay</div>
      <div style={{ fontSize: '12px', color: '#666' }}>{data.label}</div>
      <Handle type="source" position={Position.Bottom} />
    </div>
  );
}
