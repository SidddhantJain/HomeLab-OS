import React, { useState, useEffect } from 'react';
import { MonitoringSDK } from '../sdk/MonitoringSDK';

export default function AdminDashboard() {
  const [metrics, setMetrics] = useState({ cpu_percent: 18.4, ram_percent: 42.1, temperature_c: 44.2, disk_percent: 35.5 });
  const [services, setServices] = useState([
    { service: 'Docker Containers', status: 'healthy' },
    { service: 'PostgreSQL Database', status: 'healthy' },
    { service: 'Vault Encryption API', status: 'healthy' },
    { service: 'Event Bus', status: 'healthy' }
  ]);

  useEffect(() => {
    MonitoringSDK.getStatus().then(data => {
      if (data) setMetrics(data);
    }).catch(err => console.error(err));
  }, []);

  return (
    <div style={{ padding: '24px', color: '#fff', fontFamily: 'sans-serif' }}>
      <h1 style={{ fontSize: '28px', fontWeight: 'bold', marginBottom: '8px' }}>HomeLab Control Center</h1>
      <p style={{ color: '#aaa', marginBottom: '24px' }}>Operational Intelligence & Server Management Hub</p>

      {/* SYSTEM SECTION */}
      <h2 style={{ fontSize: '18px', color: '#00d2ff', marginBottom: '12px' }}>SYSTEM HEALTH</h2>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '16px', marginBottom: '32px' }}>
        <div style={{ background: 'rgba(255, 255, 255, 0.05)', padding: '16px', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.1)' }}>
          <div style={{ color: '#888', fontSize: '12px' }}>CPU USAGE</div>
          <div style={{ fontSize: '24px', fontWeight: 'bold', marginTop: '4px' }}>{metrics.cpu_percent}%</div>
        </div>
        <div style={{ background: 'rgba(255, 255, 255, 0.05)', padding: '16px', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.1)' }}>
          <div style={{ color: '#888', fontSize: '12px' }}>RAM USAGE</div>
          <div style={{ fontSize: '24px', fontWeight: 'bold', marginTop: '4px' }}>{metrics.ram_percent}%</div>
        </div>
        <div style={{ background: 'rgba(255, 255, 255, 0.05)', padding: '16px', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.1)' }}>
          <div style={{ color: '#888', fontSize: '12px' }}>TEMPERATURE</div>
          <div style={{ fontSize: '24px', fontWeight: 'bold', marginTop: '4px' }}>{metrics.temperature_c} °C</div>
        </div>
        <div style={{ background: 'rgba(255, 255, 255, 0.05)', padding: '16px', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.1)' }}>
          <div style={{ color: '#888', fontSize: '12px' }}>STORAGE POOL</div>
          <div style={{ fontSize: '24px', fontWeight: 'bold', marginTop: '4px' }}>{metrics.disk_percent}%</div>
        </div>
      </div>

      {/* SERVICES SECTION */}
      <h2 style={{ fontSize: '18px', color: '#00d2ff', marginBottom: '12px' }}>SERVICES</h2>
      <div style={{ background: 'rgba(255, 255, 255, 0.05)', padding: '16px', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.1)', marginBottom: '32px' }}>
        {services.map((s, idx) => (
          <div key={idx} style={{ display: 'flex', justifyContent: 'space-between', padding: '8px 0', borderBottom: idx < services.length - 1 ? '1px solid rgba(255,255,255,0.05)' : 'none' }}>
            <span>{s.service}</span>
            <span style={{ color: '#00ff88', fontWeight: 'bold' }}>{s.status.toUpperCase()}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
