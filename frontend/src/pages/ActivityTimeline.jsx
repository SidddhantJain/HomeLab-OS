import React, { useState, useEffect } from 'react';
import { ActivitySDK } from '../sdk/ActivitySDK';

export default function ActivityTimelinePage() {
  const [timeline, setTimeline] = useState([
    { id: '1', title: 'HomeLab OS Platform Booted', description: 'All Phase 1-6 core services initialized.', category: 'system', severity: 'info', timestamp: new Date().toISOString() }
  ]);

  useEffect(() => {
    ActivitySDK.getTimeline().then(data => {
      if (data && data.length) setTimeline(data);
    }).catch(err => console.error(err));
  }, []);

  return (
    <div style={{ padding: '24px', color: '#fff', fontFamily: 'sans-serif' }}>
      <h1 style={{ fontSize: '28px', fontWeight: 'bold', marginBottom: '8px' }}>Unified Activity Timeline</h1>
      <p style={{ color: '#aaa', marginBottom: '24px' }}>Real-time Audit Trail & Event Execution History</p>

      <div style={{ background: 'rgba(255,255,255,0.05)', padding: '20px', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.1)' }}>
        {timeline.map((item, idx) => (
          <div key={idx} style={{ display: 'flex', gap: '16px', padding: '12px 0', borderBottom: idx < timeline.length - 1 ? '1px solid rgba(255,255,255,0.05)' : 'none' }}>
            <div style={{ minWidth: '12px', height: '12px', borderRadius: '50%', background: '#00d2ff', marginTop: '6px' }} />
            <div>
              <div style={{ fontWeight: 'bold', fontSize: '15px' }}>{item.title}</div>
              <div style={{ color: '#aaa', fontSize: '13px', margin: '4px 0' }}>{item.description}</div>
              <div style={{ color: '#666', fontSize: '11px' }}>{new Date(item.timestamp).toLocaleString()} • [{item.category.toUpperCase()}]</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
