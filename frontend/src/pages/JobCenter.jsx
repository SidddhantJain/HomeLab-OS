import React, { useState, useEffect } from 'react';
import { JobsSDK } from '../sdk/JobsSDK';

export default function JobCenterPage() {
  const [jobs, setJobs] = useState([
    { id: '1', name: 'Daily Automated Storage Backup', job_type: 'backup', status: 'COMPLETED', progress_pct: 100 }
  ]);

  useEffect(() => {
    JobsSDK.list().then(data => {
      if (data && data.length) setJobs(data);
    }).catch(err => console.error(err));
  }, []);

  return (
    <div style={{ padding: '24px', color: '#fff', fontFamily: 'sans-serif' }}>
      <h1 style={{ fontSize: '28px', fontWeight: 'bold', marginBottom: '8px' }}>Background Job Center</h1>
      <p style={{ color: '#aaa', marginBottom: '24px' }}>Unified Progress Monitoring for Backups, Workflows, & Snapshots</p>

      <div style={{ background: 'rgba(255,255,255,0.05)', padding: '20px', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.1)' }}>
        {jobs.map((j, idx) => (
          <div key={idx} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '12px 0', borderBottom: idx < jobs.length - 1 ? '1px solid rgba(255,255,255,0.05)' : 'none' }}>
            <div>
              <div style={{ fontWeight: 'bold', fontSize: '15px' }}>{j.name}</div>
              <div style={{ color: '#888', fontSize: '12px' }}>Type: {j.job_type} • Progress: {j.progress_pct}%</div>
            </div>
            <span style={{ color: j.status === 'COMPLETED' ? '#00ff88' : '#00d2ff', fontWeight: 'bold' }}>{j.status}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
