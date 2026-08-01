import React, { useState, useEffect } from 'react';
import { NetworkSDK } from '../sdk/NetworkSDK';

export default function NetworkPage() {
  const [devices, setDevices] = useState([
    { ip_address: '192.168.1.1', mac_address: '70:ee:50:aa:bb:cc', hostname: 'gateway.home', friendly_name: 'Main Router', vendor: 'Netgear Inc.', is_online: true },
    { ip_address: '192.168.1.100', mac_address: '00:11:22:33:44:55', hostname: 'homelab-server', friendly_name: 'Dell Inspiron 5558 (HomeLab OS)', vendor: 'Dell Inc.', is_online: true },
    { ip_address: '192.168.1.150', mac_address: 'b8:27:eb:11:22:33', hostname: 'pi-nas', friendly_name: 'Home Storage NAS', vendor: 'Raspberry Pi Foundation', is_online: true },
    { ip_address: '192.168.1.180', mac_address: '34:29:12:88:99:00', hostname: 'living-tv.home', friendly_name: 'Living Room TV', vendor: 'Apple Inc.', is_online: true }
  ]);

  useEffect(() => {
    NetworkSDK.getDevices().then(data => {
      if (data && data.length) setDevices(data);
    }).catch(err => console.error(err));
  }, []);

  return (
    <div style={{ padding: '24px', color: '#fff', fontFamily: 'sans-serif' }}>
      <h1 style={{ fontSize: '28px', fontWeight: 'bold', marginBottom: '8px' }}>Network Management Center</h1>
      <p style={{ color: '#aaa', marginBottom: '24px' }}>Real-time LAN Discovery & Infrastructure Monitoring</p>

      <div style={{ background: 'rgba(255, 255, 255, 0.05)', padding: '16px', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.1)' }}>
        <h2 style={{ fontSize: '18px', color: '#00d2ff', marginBottom: '16px' }}>DISCOVERED LAN DEVICES ({devices.length})</h2>
        {devices.map((d, idx) => (
          <div key={idx} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '12px 0', borderBottom: idx < devices.length - 1 ? '1px solid rgba(255,255,255,0.05)' : 'none' }}>
            <div>
              <div style={{ fontWeight: 'bold', fontSize: '15px' }}>{d.friendly_name || d.hostname || d.ip_address}</div>
              <div style={{ color: '#888', fontSize: '12px' }}>IP: {d.ip_address} • MAC: {d.mac_address} • Vendor: {d.vendor}</div>
            </div>
            <div>
              <span style={{ color: d.is_online ? '#00ff88' : '#ff4444', fontWeight: 'bold' }}>{d.is_online ? 'ONLINE 🟢' : 'OFFLINE 🔴'}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
