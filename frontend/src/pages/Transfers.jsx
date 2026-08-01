import React, { useState, useEffect } from 'react';
import { TransfersSDK } from '../sdk/TransfersSDK';

export default function TransfersPage() {
  const [transfers, setTransfers] = useState([
    { id: '1', file_name: 'ubuntu-24.04-desktop-amd64.iso', source_path: '/downloads/ubuntu.iso', destination_path: '/storage/iso/ubuntu.iso', total_bytes: 5242880000, transferred_bytes: 2621440000, status: 'IN_PROGRESS' }
  ]);

  useEffect(() => {
    TransfersSDK.list().then(data => {
      if (data && data.length) setTransfers(data);
    }).catch(err => console.error(err));
  }, []);

  return (
    <div style={{ padding: '24px', color: '#fff', fontFamily: 'sans-serif' }}>
      <h1 style={{ fontSize: '28px', fontWeight: 'bold', marginBottom: '8px' }}>File Transfer Manager</h1>
      <p style={{ color: '#aaa', marginBottom: '24px' }}>Resumable File Queue & Checksum Verification</p>

      <div style={{ background: 'rgba(255,255,255,0.05)', padding: '20px', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.1)' }}>
        {transfers.map((t, idx) => (
          <div key={idx} style={{ padding: '12px 0', borderBottom: idx < transfers.length - 1 ? '1px solid rgba(255,255,255,0.05)' : 'none' }}>
            <div style={{ fontWeight: 'bold', fontSize: '15px' }}>{t.file_name}</div>
            <div style={{ color: '#aaa', fontSize: '12px', margin: '4px 0' }}>{t.source_path} → {t.destination_path}</div>
            <div style={{ height: '6px', background: 'rgba(255,255,255,0.1)', borderRadius: '3px', overflow: 'hidden', marginTop: '8px' }}>
              <div style={{ height: '100%', width: `${(t.transferred_bytes / (t.total_bytes || 1)) * 100}%`, background: '#00d2ff' }} />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
