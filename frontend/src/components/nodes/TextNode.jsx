import { Handle, Position } from 'reactflow';

export default function TextNode({ data }) {
  const nodeStyle = {
    padding: '8px 16px',
    boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
    borderRadius: '6px',
    background: 'white',
    border: '2px solid #3b82f6',
    minWidth: '200px'
  };

  const labelStyle = {
    fontSize: '12px',
    color: '#6b7280',
    marginBottom: '4px'
  };

  const inputStyle = {
    fontSize: '14px',
    border: '1px solid #d1d5db',
    borderRadius: '4px',
    padding: '4px 8px',
    width: '100%'
  };

  return (
    <div style={nodeStyle}>
      <Handle type="target" position={Position.Top} />
      <div>
        <div style={labelStyle}>💬 Text Message</div>
        <input
          className="nodrag"
          style={inputStyle}
          placeholder="Enter message..."
          defaultValue={data.message}
        />
      </div>
      <Handle type="source" position={Position.Bottom} />
    </div>
  );
}
