import React, { useState, useEffect } from 'react';
import { HealthSDK } from '../sdk/HealthSDK';

export default function HealthCenterPage() {
  const [health, setHealth] = useState({ overall_health_score: 98, status: 'EXCELLENT', metrics: { cpu_load_pct: 14.5, ram_usage_pct: 32.1 } });

  useEffect(() => {
    HealthSDK.getSummary().then(data => {
      if (data) setHealth(data);
    }).catch(err => console.error(err));
  }, []);

  return (
    <div style={{ padding: '24px', color: '#fff', fontFamily: 'sans-serif' }}>
      <h1 style={{ fontSize: '28px', fontWeight: 'bold', marginBottom: '8px' }}>Health Center & System Score</h1>
      <p style={{ color: '#aaa', marginBottom: '24px' }}>Unified System Diagnostics & Overall Health Score</p>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '20px' }}>
        <div style={{ background: 'rgba(255,255,255,0.05)', padding: '24px', borderRadius: '8px', border: '1px solid #00ff88', textAlign: 'center' }}>
          <div style={{ fontSize: '48px', fontWeight: 'bold', color: '#00ff88' }}>{health.overall_health_score}</div>
          <div style={{ fontSize: '16px', color: '#aaa', marginTop: '8px' }}>HEALTH SCORE ({health.status})</div>
        </div>
        <div style={{ background: 'rgba(255,255,255,0.05)', padding: '24px', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.1)' }}>
          <div style={{ fontSize: '14px', color: '#aaa' }}>CPU LOAD</div>
          <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#00d2ff', marginTop: '4px' }}>{health.metrics.cpu_load_pct}%</div>
        </div>
        <div style={{ background: 'rgba(255,255,255,0.05)', padding: '24px', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.1)' }}>
          <div style={{ fontSize: '14px', color: '#aaa' }}>RAM USAGE</div>
          <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#ffaa00', marginTop: '4px' }}>{health.metrics.ram_usage_pct}%</div>
        </div>
      </div>
    </div>
  );
}
