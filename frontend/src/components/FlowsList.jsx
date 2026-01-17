import { useState, useEffect } from 'react';
import { flowsApi } from '../api/flowsApi';

export default function FlowsList({ botId, currentFlowId, onSelectFlow, onNewFlow, onDeleteFlow }) {
  const [flows, setFlows] = useState([]);
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    loadFlows();
  }, [botId]);

  const loadFlows = async () => {
    try {
      const data = await flowsApi.listFlows(botId);
      setFlows(data.flows || []);
    } catch (error) {
      console.error('Failed to load flows:', error);
    }
  };

  const handleActivate = async (flowId) => {
    try {
      await flowsApi.activateFlow(botId, flowId);
      await loadFlows();
    } catch (error) {
      console.error('Failed to activate flow:', error);
    }
  };

  const handleDelete = async (flowId) => {
    if (confirm('Are you sure you want to delete this flow?')) {
      try {
        await onDeleteFlow(flowId);
        await loadFlows();
      } catch (error) {
        console.error('Failed to delete flow:', error);
      }
    }
  };

  return (
    <div style={containerStyle}>
      <button style={toggleButtonStyle} onClick={() => setIsOpen(!isOpen)}>
        📋 Flows ({flows.length})
      </button>

      {isOpen && (
        <div style={dropdownStyle}>
          <div style={headerStyle}>
            <h4 style={titleStyle}>My Flows</h4>
            <button style={newButtonStyle} onClick={onNewFlow}>
              ➕ New Flow
            </button>
          </div>

          <div style={listStyle}>
            {flows.length === 0 ? (
              <div style={emptyStyle}>No flows yet. Create one!</div>
            ) : (
              flows.map((flow) => (
                <div
                  key={flow.flow_id}
                  style={{
                    ...itemStyle,
                    background: flow.flow_id === currentFlowId ? '#dbeafe' : 'white'
                  }}
                >
                  <div style={itemContentStyle}>
                    <div style={itemNameStyle}>
                      {flow.name}
                      {flow.is_active && (
                        <span style={activeTagStyle}>Active</span>
                      )}
                    </div>
                    <div style={itemDateStyle}>
                      Updated: {new Date(flow.updated_at).toLocaleString()}
                    </div>
                  </div>
                  
                  <div style={actionsStyle}>
                    <button
                      style={loadButtonStyle}
                      onClick={() => onSelectFlow(flow.flow_id)}
                      title="Load this flow"
                    >
                      📂
                    </button>
                    
                    {!flow.is_active && (
                      <button
                        style={activateButtonStyle}
                        onClick={() => handleActivate(flow.flow_id)}
                        title="Set as active"
                      >
                        ⭐
                      </button>
                    )}
                    
                    <button
                      style={deleteButtonStyle}
                      onClick={() => handleDelete(flow.flow_id)}
                      title="Delete flow"
                    >
                      🗑️
                    </button>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      )}
    </div>
  );
}

const containerStyle = {
  position: 'absolute',
  top: '16px',
  left: '240px',
  zIndex: 10
};

const toggleButtonStyle = {
  padding: '10px 16px',
  background: '#3b82f6',
  color: 'white',
  border: 'none',
  borderRadius: '8px',
  cursor: 'pointer',
  fontSize: '14px',
  fontWeight: '600',
  boxShadow: '0 4px 6px rgba(0,0,0,0.1)'
};

const dropdownStyle = {
  position: 'absolute',
  top: '48px',
  left: 0,
  background: 'white',
  borderRadius: '8px',
  boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
  border: '2px solid #e5e7eb',
  minWidth: '400px',
  maxHeight: '500px',
  overflow: 'auto'
};

const headerStyle = {
  padding: '16px',
  borderBottom: '2px solid #e5e7eb',
  display: 'flex',
  justifyContent: 'space-between',
  alignItems: 'center'
};

const titleStyle = {
  margin: 0,
  fontSize: '16px',
  fontWeight: 'bold',
  color: '#374151'
};

const newButtonStyle = {
  padding: '6px 12px',
  background: '#10b981',
  color: 'white',
  border: 'none',
  borderRadius: '6px',
  cursor: 'pointer',
  fontSize: '12px',
  fontWeight: '600'
};

const listStyle = {
  padding: '8px'
};

const emptyStyle = {
  padding: '20px',
  textAlign: 'center',
  color: '#9ca3af',
  fontSize: '14px'
};

const itemStyle = {
  padding: '12px',
  marginBottom: '8px',
  borderRadius: '6px',
  border: '2px solid #e5e7eb',
  display: 'flex',
  justifyContent: 'space-between',
  alignItems: 'center'
};

const itemContentStyle = {
  flex: 1
};

const itemNameStyle = {
  fontSize: '14px',
  fontWeight: '600',
  color: '#374151',
  marginBottom: '4px',
  display: 'flex',
  alignItems: 'center',
  gap: '8px'
};

const activeTagStyle = {
  padding: '2px 8px',
  background: '#10b981',
  color: 'white',
  borderRadius: '4px',
  fontSize: '10px',
  fontWeight: 'bold'
};

const itemDateStyle = {
  fontSize: '11px',
  color: '#9ca3af'
};

const actionsStyle = {
  display: 'flex',
  gap: '4px'
};

const loadButtonStyle = {
  padding: '6px 10px',
  background: '#3b82f6',
  color: 'white',
  border: 'none',
  borderRadius: '4px',
  cursor: 'pointer',
  fontSize: '14px'
};

const activateButtonStyle = {
  padding: '6px 10px',
  background: '#f59e0b',
  color: 'white',
  border: 'none',
  borderRadius: '4px',
  cursor: 'pointer',
  fontSize: '14px'
};

const deleteButtonStyle = {
  padding: '6px 10px',
  background: '#ef4444',
  color: 'white',
  border: 'none',
  borderRadius: '4px',
  cursor: 'pointer',
  fontSize: '14px'
};
