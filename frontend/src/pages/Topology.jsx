import React from 'react';

export default function TopologyPage() {
  return (
    <div style={{ padding: '24px', color: '#fff', fontFamily: 'sans-serif' }}>
      <h1 style={{ fontSize: '28px', fontWeight: 'bold', marginBottom: '8px' }}>Network Topology Graph</h1>
      <p style={{ color: '#aaa', marginBottom: '24px' }}>Infrastructure Device Graph & Node Mapping</p>

      <div style={{ background: '#0a0a0a', border: '1px solid rgba(255,255,255,0.15)', borderRadius: '8px', padding: '32px', textAlign: 'center' }}>
        <div style={{ fontSize: '18px', color: '#00d2ff', fontWeight: 'bold', marginBottom: '16px' }}>WAN Internet Connection</div>
        <div style={{ fontSize: '24px', color: '#888', marginBottom: '16px' }}>↓</div>
        <div style={{ fontSize: '18px', color: '#00ff88', fontWeight: 'bold', marginBottom: '16px' }}>Main Router (192.168.1.1)</div>
        <div style={{ fontSize: '24px', color: '#888', marginBottom: '16px' }}>↓</div>
        <div style={{ display: 'flex', justifyContent: 'center', gap: '32px', flexWrap: 'wrap' }}>
          <div style={{ background: 'rgba(255,255,255,0.05)', padding: '16px 24px', borderRadius: '8px', border: '1px solid #00d2ff' }}>
            <div style={{ fontWeight: 'bold', color: '#00d2ff' }}>HomeLab OS Server</div>
            <div style={{ fontSize: '12px', color: '#aaa' }}>192.168.1.100</div>
          </div>
          <div style={{ background: 'rgba(255,255,255,0.05)', padding: '16px 24px', borderRadius: '8px', border: '1px solid #00ff88' }}>
            <div style={{ fontWeight: 'bold', color: '#00ff88' }}>Storage NAS</div>
            <div style={{ fontSize: '12px', color: '#aaa' }}>192.168.1.150</div>
          </div>
          <div style={{ background: 'rgba(255,255,255,0.05)', padding: '16px 24px', borderRadius: '8px', border: '1px solid #ffaa00' }}>
            <div style={{ fontWeight: 'bold', color: '#ffaa00' }}>Living Room TV</div>
            <div style={{ fontSize: '12px', color: '#aaa' }}>192.168.1.180</div>
          </div>
        </div>
      </div>
    </div>
  );
}
