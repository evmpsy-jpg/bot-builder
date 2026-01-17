import { Handle, Position } from 'reactflow';

export default function TextNode({ data }) {
  return (
    <div style={{
      padding: '10px',
      border: '2px solid #3b82f6',
      borderRadius: '8px',
      background: 'white',
      minWidth: '150px',
      maxWidth: '200px'
    }}>
      <Handle type="target" position={Position.Top} />
      <div style={{ fontWeight: 'bold', marginBottom: '5px' }}>💬 Text</div>
      <div style={{ 
        fontSize: '12px', 
        color: '#666',
        overflow: 'hidden',
        textOverflow: 'ellipsis',
        whiteSpace: 'nowrap'
      }}>
        {data.text || 'Click to edit...'}
      </div>
      <Handle type="source" position={Position.Bottom} />
    </div>
  );
}
