import { useState, useEffect } from 'react';

export default function NodeSettings({ node, isOpen, onClose, onSave }) {
  const [formData, setFormData] = useState({});

  useEffect(() => {
    if (node) {
      setFormData(node.data || {});
    }
  }, [node]);

  if (!isOpen || !node) return null;

  const handleSave = () => {
    onSave(node.id, formData);
    onClose();
  };

  const renderFields = () => {
    switch (node.type) {
      case 'textNode':
        return (
          <div>
            <label style={labelStyle}>Message Text:</label>
            <textarea
              style={textareaStyle}
              value={formData.text || ''}
              onChange={(e) => setFormData({ ...formData, text: e.target.value })}
              placeholder="Enter message text..."
              rows={4}
            />
          </div>
        );

      case 'imageNode':
        return (
          <div>
            <label style={labelStyle}>Image URL:</label>
            <input
              style={inputStyle}
              type="text"
              value={formData.imageUrl || ''}
              onChange={(e) => setFormData({ ...formData, imageUrl: e.target.value })}
              placeholder="https://example.com/image.jpg"
            />
            <label style={labelStyle}>Caption (optional):</label>
            <input
              style={inputStyle}
              type="text"
              value={formData.caption || ''}
              onChange={(e) => setFormData({ ...formData, caption: e.target.value })}
              placeholder="Image caption..."
            />
          </div>
        );

      case 'videoNode':
        return (
          <div>
            <label style={labelStyle}>Video URL:</label>
            <input
              style={inputStyle}
              type="text"
              value={formData.videoUrl || ''}
              onChange={(e) => setFormData({ ...formData, videoUrl: e.target.value })}
              placeholder="https://example.com/video.mp4"
            />
            <label style={labelStyle}>Caption (optional):</label>
            <input
              style={inputStyle}
              type="text"
              value={formData.caption || ''}
              onChange={(e) => setFormData({ ...formData, caption: e.target.value })}
              placeholder="Video caption..."
            />
          </div>
        );

      case 'delayNode':
        return (
          <div>
            <label style={labelStyle}>Delay (seconds):</label>
            <input
              style={inputStyle}
              type="number"
              min="1"
              value={formData.delay || 5}
              onChange={(e) => setFormData({ ...formData, delay: parseInt(e.target.value) })}
            />
          </div>
        );

      case 'buttonNode':
        return (
          <div>
            <label style={labelStyle}>Button Text:</label>
            <input
              style={inputStyle}
              type="text"
              value={formData.buttonText || ''}
              onChange={(e) => setFormData({ ...formData, buttonText: e.target.value })}
              placeholder="Click me"
            />
            <label style={labelStyle}>Callback Data:</label>
            <input
              style={inputStyle}
              type="text"
              value={formData.callbackData || ''}
              onChange={(e) => setFormData({ ...formData, callbackData: e.target.value })}
              placeholder="button_action"
            />
          </div>
        );

      case 'conditionNode':
        return (
          <div>
            <label style={labelStyle}>Condition Type:</label>
            <select
              style={inputStyle}
              value={formData.conditionType || 'text_equals'}
              onChange={(e) => setFormData({ ...formData, conditionType: e.target.value })}
            >
              <option value="text_equals">Text equals</option>
              <option value="text_contains">Text contains</option>
              <option value="has_photo">Has photo</option>
              <option value="has_video">Has video</option>
            </select>
            <label style={labelStyle}>Value:</label>
            <input
              style={inputStyle}
              type="text"
              value={formData.conditionValue || ''}
              onChange={(e) => setFormData({ ...formData, conditionValue: e.target.value })}
              placeholder="Enter value..."
            />
          </div>
        );

      default:
        return <div>No settings available for this node type.</div>;
    }
  };

  return (
    <div style={overlayStyle} onClick={onClose}>
      <div style={modalStyle} onClick={(e) => e.stopPropagation()}>
        <h3 style={titleStyle}>⚙️ Node Settings</h3>
        <div style={contentStyle}>
          {renderFields()}
        </div>
        <div style={buttonsStyle}>
          <button style={saveButtonStyle} onClick={handleSave}>
            💾 Save
          </button>
          <button style={cancelButtonStyle} onClick={onClose}>
            ❌ Cancel
          </button>
        </div>
      </div>
    </div>
  );
}

const overlayStyle = {
  position: 'fixed',
  top: 0,
  left: 0,
  right: 0,
  bottom: 0,
  background: 'rgba(0,0,0,0.5)',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  zIndex: 1000
};

const modalStyle = {
  background: 'white',
  padding: '24px',
  borderRadius: '12px',
  minWidth: '400px',
  maxWidth: '500px',
  boxShadow: '0 10px 25px rgba(0,0,0,0.2)'
};

const titleStyle = {
  margin: '0 0 20px 0',
  fontSize: '20px',
  fontWeight: 'bold',
  color: '#374151'
};

const contentStyle = {
  marginBottom: '20px'
};

const labelStyle = {
  display: 'block',
  marginBottom: '8px',
  marginTop: '12px',
  fontSize: '14px',
  fontWeight: '600',
  color: '#374151'
};

const inputStyle = {
  width: '100%',
  padding: '10px',
  border: '2px solid #e5e7eb',
  borderRadius: '6px',
  fontSize: '14px',
  boxSizing: 'border-box'
};

const textareaStyle = {
  ...inputStyle,
  resize: 'vertical',
  fontFamily: 'inherit'
};

const buttonsStyle = {
  display: 'flex',
  gap: '10px',
  justifyContent: 'flex-end'
};

const saveButtonStyle = {
  padding: '10px 20px',
  background: '#10b981',
  color: 'white',
  border: 'none',
  borderRadius: '6px',
  cursor: 'pointer',
  fontSize: '14px',
  fontWeight: '600'
};

const cancelButtonStyle = {
  padding: '10px 20px',
  background: '#ef4444',
  color: 'white',
  border: 'none',
  borderRadius: '6px',
  cursor: 'pointer',
  fontSize: '14px',
  fontWeight: '600'
};
