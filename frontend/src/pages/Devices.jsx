import React, { useState } from 'react';
import { DevicesSDK } from '../sdk/DevicesSDK';

export default function DevicesPage() {
  const [mac, setMac] = useState('b8:27:eb:11:22:33');
  const [friendlyName, setFriendlyName] = useState('Gaming PC');
  const [message, setMessage] = useState('');

  const handleUpdate = async (e) => {
    e.preventDefault();
    try {
      await DevicesSDK.updateAlias(mac, friendlyName);
      setMessage(`Updated device ${mac} name to '${friendlyName}'`);
    } catch (err) {
      setMessage('Failed to update friendly name');
    }
  };

  return (
    <div style={{ padding: '24px', color: '#fff', fontFamily: 'sans-serif' }}>
      <h1 style={{ fontSize: '28px', fontWeight: 'bold', marginBottom: '8px' }}>Device Inventory & Naming</h1>
      <p style={{ color: '#aaa', marginBottom: '24px' }}>Assign friendly names to network hardware</p>

      {message && (
        <div style={{ padding: '12px', background: 'rgba(0,255,136,0.1)', border: '1px solid #00ff88', borderRadius: '6px', marginBottom: '24px' }}>
          {message}
        </div>
      )}

      <form onSubmit={handleUpdate} style={{ background: 'rgba(255,255,255,0.05)', padding: '20px', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.1)', maxWidth: '500px' }}>
        <div style={{ marginBottom: '16px' }}>
          <label style={{ display: 'block', marginBottom: '6px', fontSize: '14px', color: '#ccc' }}>Device MAC Address</label>
          <input
            type="text"
            value={mac}
            onChange={(e) => setMac(e.target.value)}
            style={{ width: '100%', padding: '10px', background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.2)', borderRadius: '4px', color: '#fff' }}
          />
        </div>
        <div style={{ marginBottom: '20px' }}>
          <label style={{ display: 'block', marginBottom: '6px', fontSize: '14px', color: '#ccc' }}>Friendly Name</label>
          <input
            type="text"
            value={friendlyName}
            onChange={(e) => setFriendlyName(e.target.value)}
            style={{ width: '100%', padding: '10px', background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.2)', borderRadius: '4px', color: '#fff' }}
          />
        </div>
        <button type="submit" style={{ padding: '10px 20px', background: '#00d2ff', border: 'none', borderRadius: '4px', color: '#000', fontWeight: 'bold', cursor: 'pointer' }}>
          Save Friendly Name
        </button>
      </form>
    </div>
  );
}
