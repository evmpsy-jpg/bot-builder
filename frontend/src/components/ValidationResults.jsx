export default function ValidationResults({ validation, onClose }) {
  if (!validation) return null;

  const { isValid, errors, warnings } = validation;

  return (
    <div style={overlayStyle} onClick={onClose}>
      <div style={modalStyle} onClick={(e) => e.stopPropagation()}>
        <h3 style={titleStyle}>
          {isValid ? '✅ Flow Validation Passed' : '❌ Flow Validation Failed'}
        </h3>
        
        {errors.length > 0 && (
          <div style={sectionStyle}>
            <h4 style={errorTitleStyle}>Errors:</h4>
            {errors.map((error, index) => (
              <div key={index} style={errorStyle}>{error}</div>
            ))}
          </div>
        )}

        {warnings.length > 0 && (
          <div style={sectionStyle}>
            <h4 style={warningTitleStyle}>Warnings:</h4>
            {warnings.map((warning, index) => (
              <div key={index} style={warningStyle}>{warning}</div>
            ))}
          </div>
        )}

        {isValid && errors.length === 0 && warnings.length === 0 && (
          <div style={successStyle}>
            All checks passed! Flow is ready to save.
          </div>
        )}

        <button style={buttonStyle} onClick={onClose}>
          Close
        </button>
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
  maxWidth: '600px',
  maxHeight: '80vh',
  overflow: 'auto',
  boxShadow: '0 10px 25px rgba(0,0,0,0.2)'
};

const titleStyle = {
  margin: '0 0 20px 0',
  fontSize: '20px',
  fontWeight: 'bold',
  color: '#374151'
};

const sectionStyle = {
  marginBottom: '16px'
};

const errorTitleStyle = {
  fontSize: '16px',
  fontWeight: 'bold',
  color: '#ef4444',
  marginBottom: '8px'
};

const warningTitleStyle = {
  fontSize: '16px',
  fontWeight: 'bold',
  color: '#f59e0b',
  marginBottom: '8px'
};

const errorStyle = {
  padding: '8px 12px',
  background: '#fee2e2',
  border: '1px solid #ef4444',
  borderRadius: '6px',
  marginBottom: '6px',
  fontSize: '14px',
  color: '#991b1b'
};

const warningStyle = {
  padding: '8px 12px',
  background: '#fef3c7',
  border: '1px solid #f59e0b',
  borderRadius: '6px',
  marginBottom: '6px',
  fontSize: '14px',
  color: '#92400e'
};

const successStyle = {
  padding: '12px',
  background: '#d1fae5',
  border: '1px solid #10b981',
  borderRadius: '6px',
  fontSize: '14px',
  color: '#065f46',
  marginBottom: '16px'
};

const buttonStyle = {
  padding: '10px 20px',
  background: '#3b82f6',
  color: 'white',
  border: 'none',
  borderRadius: '6px',
  cursor: 'pointer',
  fontSize: '14px',
  fontWeight: '600',
  width: '100%'
};
