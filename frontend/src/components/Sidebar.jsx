export default function Sidebar() {
  const onDragStart = (event, nodeType) => {
    event.dataTransfer.setData('application/reactflow', nodeType);
    event.dataTransfer.effectAllowed = 'move';
  };

  const sidebarStyle = {
    position: 'absolute',
    top: '16px',
    left: '16px',
    zIndex: 10,
    background: 'white',
    padding: '16px',
    borderRadius: '8px',
    boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
    border: '2px solid #e5e7eb',
    width: '200px'
  };

  const titleStyle = {
    fontSize: '14px',
    fontWeight: 'bold',
    marginBottom: '12px',
    color: '#374151'
  };

  const itemStyle = {
    marginBottom: '8px',
    padding: '12px',
    borderRadius: '6px',
    cursor: 'move',
    fontSize: '14px'
  };

  return (
    <aside style={sidebarStyle}>
      <div style={titleStyle}>🛠️ Components</div>
      
      <div
        style={{...itemStyle, border: '2px solid #3b82f6', background: '#eff6ff'}}
        onDragStart={(event) => onDragStart(event, 'textNode')}
        draggable
      >
        💬 Text Message
      </div>
      
      <div
        style={{...itemStyle, border: '2px solid #10b981', background: '#f0fdf4'}}
        onDragStart={(event) => onDragStart(event, 'buttonNode')}
        draggable
      >
        🔘 Button
      </div>
      
      <div
        style={{...itemStyle, border: '2px solid #eab308', background: '#fefce8'}}
        onDragStart={(event) => onDragStart(event, 'conditionNode')}
        draggable
      >
        ❓ Condition
      </div>

      <div
        style={{...itemStyle, border: '2px solid #9333ea', background: '#faf5ff'}}
        onDragStart={(event) => onDragStart(event, 'imageNode')}
        draggable
      >
        📷 Image
      </div>

      <div
        style={{...itemStyle, border: '2px solid #db2777', background: '#fdf2f8'}}
        onDragStart={(event) => onDragStart(event, 'videoNode')}
        draggable
      >
        🎥 Video
      </div>

      <div
        style={{...itemStyle, border: '2px solid #f59e0b', background: '#fffbeb'}}
        onDragStart={(event) => onDragStart(event, 'delayNode')}
        draggable
      >
        ⏰ Delay
      </div>
    </aside>
  );
}
