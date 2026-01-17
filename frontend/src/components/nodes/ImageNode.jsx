import { Handle, Position } from 'reactflow';

export default function ImageNode({ data }) {
  return (
    <div style={{
      padding: '10px',
      border: '2px solid #9333ea',
      borderRadius: '8px',
      background: 'white',
      minWidth: '150px',
      maxWidth: '200px'
    }}>
      <Handle type="target" position={Position.Top} />
      <div style={{ fontWeight: 'bold', marginBottom: '5px' }}>📷 Image</div>
      <div style={{ 
        fontSize: '11px', 
        color: '#666',
        overflow: 'hidden',
        textOverflow: 'ellipsis',
        whiteSpace: 'nowrap'
      }}>
        {data.imageUrl ? `🔗 ${data.imageUrl.substring(0, 20)}...` : 'Click to edit...'}
      </div>
      {data.caption && (
        <div style={{ fontSize: '10px', color: '#999', marginTop: '4px' }}>
          {data.caption}
        </div>
      )}
      <Handle type="source" position={Position.Bottom} />
    </div>
  );
}
