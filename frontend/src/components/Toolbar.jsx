export default function Toolbar({ onSave, onLoad, onClear, onValidate }) {
  const toolbarStyle = {
    position: 'absolute',
    top: '16px',
    right: '80px',
    zIndex: 10,
    background: 'white',
    padding: '12px',
    borderRadius: '8px',
    boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
    border: '2px solid #e5e7eb',
    display: 'flex',
    gap: '8px'
  };

  const buttonStyle = {
    padding: '8px 16px',
    borderRadius: '6px',
    border: 'none',
    fontSize: '14px',
    fontWeight: '500',
    cursor: 'pointer',
    color: 'white'
  };

  return (
    <div style={toolbarStyle}>
      <button
        onClick={onValidate}
        style={{...buttonStyle, background: '#8b5cf6'}}
        onMouseOver={(e) => e.target.style.background = '#7c3aed'}
        onMouseOut={(e) => e.target.style.background = '#8b5cf6'}
      >
        ✓ Validate
      </button>
      <button
        onClick={onSave}
        style={{...buttonStyle, background: '#3b82f6'}}
        onMouseOver={(e) => e.target.style.background = '#2563eb'}
        onMouseOut={(e) => e.target.style.background = '#3b82f6'}
      >
        💾 Save
      </button>
      <button
        onClick={onLoad}
        style={{...buttonStyle, background: '#10b981'}}
        onMouseOver={(e) => e.target.style.background = '#059669'}
        onMouseOut={(e) => e.target.style.background = '#10b981'}
      >
        📂 Load
      </button>
      <button
        onClick={onClear}
        style={{...buttonStyle, background: '#ef4444'}}
        onMouseOver={(e) => e.target.style.background = '#dc2626'}
        onMouseOut={(e) => e.target.style.background = '#ef4444'}
      >
        🗑️ Clear
      </button>
    </div>
  );
}
