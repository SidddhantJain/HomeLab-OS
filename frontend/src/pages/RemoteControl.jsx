import React, { useState } from 'react';
import { RemoteSDK } from '../sdk/RemoteSDK';

export default function RemoteControl() {
  const [terminalInput, setTerminalInput] = useState('');
  const [terminalOutput, setTerminalOutput] = useState(['homelab-shell$ Welcome to HomeLab Remote Terminal']);
  const [actionMessage, setActionMessage] = useState('');
  const [files, setFiles] = useState([
    { name: 'workspace-alpha', is_dir: true, size: 4096 },
    { name: 'readme.md', is_dir: false, size: 1024 },
    { name: 'backup-2026-07-31.tar.gz', is_dir: false, size: 10485760 }
  ]);

  const handleAction = async (cmd) => {
    try {
      const res = await RemoteSDK.executeCommand(cmd);
      setActionMessage(`[Command '${cmd}'] ${res.output || 'Success'}`);
    } catch (err) {
      setActionMessage(`Failed to execute '${cmd}'`);
    }
  };

  const handleTerminalSubmit = async (e) => {
    e.preventDefault();
    if (!terminalInput.trim()) return;

    const cmd = terminalInput;
    setTerminalInput('');
    setTerminalOutput(prev => [...prev, `homelab-shell$ ${cmd}`]);

    try {
      const res = await RemoteSDK.executeTerminalCommand(cmd);
      if (res.status === 'REJECTED') {
        setTerminalOutput(prev => [...prev, `ERROR: ${res.error}`]);
      } else {
        setTerminalOutput(prev => [...prev, res.output || 'Command executed']);
      }
    } catch (err) {
      setTerminalOutput(prev => [...prev, 'Command execution failed.']);
    }
  };

  return (
    <div style={{ padding: '24px', color: '#fff', fontFamily: 'sans-serif' }}>
      <h1 style={{ fontSize: '28px', fontWeight: 'bold', marginBottom: '8px' }}>HomeLab Remote Control</h1>
      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '24px' }}>
        <span style={{ color: '#aaa' }}>Server: Dell Inspiron 5558 —</span>
        <span style={{ color: '#00ff88', fontWeight: 'bold' }}>ONLINE 🟢</span>
      </div>

      {actionMessage && (
        <div style={{ padding: '12px', background: 'rgba(0,210,255,0.1)', border: '1px solid #00d2ff', borderRadius: '6px', marginBottom: '24px' }}>
          {actionMessage}
        </div>
      )}

      {/* QUICK ACTIONS */}
      <h2 style={{ fontSize: '18px', color: '#00d2ff', marginBottom: '12px' }}>REMOTE ACTIONS</h2>
      <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap', marginBottom: '32px' }}>
        <button onClick={() => handleAction('restart_service')} style={{ padding: '10px 20px', background: '#00d2ff', border: 'none', borderRadius: '6px', color: '#000', fontWeight: 'bold', cursor: 'pointer' }}>
          Restart Services
        </button>
        <button onClick={() => handleAction('start_backup')} style={{ padding: '10px 20px', background: '#00ff88', border: 'none', borderRadius: '6px', color: '#000', fontWeight: 'bold', cursor: 'pointer' }}>
          Start Backup
        </button>
        <button onClick={() => handleAction('lock_vault')} style={{ padding: '10px 20px', background: '#ffaa00', border: 'none', borderRadius: '6px', color: '#000', fontWeight: 'bold', cursor: 'pointer' }}>
          Lock Vault
        </button>
        <button onClick={() => handleAction('maintenance_mode')} style={{ padding: '10px 20px', background: '#ff4444', border: 'none', borderRadius: '6px', color: '#fff', fontWeight: 'bold', cursor: 'pointer' }}>
          Maintenance Mode
        </button>
      </div>

      {/* WEB TERMINAL */}
      <h2 style={{ fontSize: '18px', color: '#00d2ff', marginBottom: '12px' }}>SANDBOXED WEB TERMINAL</h2>
      <div style={{ background: '#0a0a0a', border: '1px solid rgba(255,255,255,0.15)', borderRadius: '8px', padding: '16px', marginBottom: '32px' }}>
        <div style={{ height: '180px', overflowY: 'auto', fontFamily: 'monospace', fontSize: '14px', marginBottom: '12px' }}>
          {terminalOutput.map((line, idx) => (
            <div key={idx} style={{ color: line.startsWith('ERROR:') ? '#ff4444' : '#00ff88' }}>{line}</div>
          ))}
        </div>
        <form onSubmit={handleTerminalSubmit} style={{ display: 'flex', gap: '8px' }}>
          <input
            type="text"
            value={terminalInput}
            onChange={(e) => setTerminalInput(e.target.value)}
            placeholder="Type terminal command..."
            style={{ flex: 1, padding: '10px', background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.2)', borderRadius: '4px', color: '#fff', fontFamily: 'monospace' }}
          />
          <button type="submit" style={{ padding: '10px 20px', background: '#00d2ff', border: 'none', borderRadius: '4px', color: '#000', fontWeight: 'bold', cursor: 'pointer' }}>
            Run
          </button>
        </form>
      </div>

      {/* FILE MANAGER */}
      <h2 style={{ fontSize: '18px', color: '#00d2ff', marginBottom: '12px' }}>REMOTE FILE MANAGER (/projects)</h2>
      <div style={{ background: 'rgba(255, 255, 255, 0.05)', padding: '16px', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.1)' }}>
        {files.map((f, idx) => (
          <div key={idx} style={{ display: 'flex', justifyContent: 'space-between', padding: '8px 0', borderBottom: idx < files.length - 1 ? '1px solid rgba(255,255,255,0.05)' : 'none' }}>
            <span>{f.is_dir ? '📁' : '📄'} {f.name}</span>
            <span style={{ color: '#aaa' }}>{f.size} B</span>
          </div>
        ))}
      </div>
    </div>
  );
}
