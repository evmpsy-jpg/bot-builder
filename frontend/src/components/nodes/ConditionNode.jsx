import { Handle, Position } from 'reactflow';

export default function ConditionNode({ data }) {
  const nodeStyle = {
    padding: '8px 16px',
    boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
    borderRadius: '6px',
    background: 'white',
    border: '2px solid #eab308',
    minWidth: '200px'
  };

  const labelStyle = {
    fontSize: '12px',
    color: '#6b7280',
    marginBottom: '4px'
  };

  const selectStyle = {
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
        <div style={labelStyle}>❓ Condition</div>
        <select className="nodrag" style={selectStyle}>
          <option>User input contains...</option>
          <option>User role is...</option>
          <option>Time is...</option>
        </select>
      </div>
      <Handle type="source" position={Position.Bottom} id="true" style={{ left: '30%' }} />
      <Handle type="source" position={Position.Bottom} id="false" style={{ left: '70%' }} />
    </div>
  );
}
