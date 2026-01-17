import { Handle, Position } from 'reactflow';

export default function ImageNode({ data }) {
  return (
    <div style={{
      padding: '10px',
      border: '2px solid #9333ea',
      borderRadius: '8px',
      background: 'white',
      minWidth: '150px'
    }}>
      <Handle type="target" position={Position.Top} />
      <div style={{ fontWeight: 'bold', marginBottom: '5px' }}>📷 Image</div>
      <div style={{ fontSize: '12px', color: '#666' }}>{data.label}</div>
      <Handle type="source" position={Position.Bottom} />
    </div>
  );
}
