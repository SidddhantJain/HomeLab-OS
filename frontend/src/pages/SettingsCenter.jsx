import React, { useState, useEffect } from 'react';
import { SettingsSDK } from '../sdk/SettingsSDK';

export default function SettingsCenterPage() {
  const [theme, setTheme] = useState('dark');
  const [language, setLanguage] = useState('en');
  const [msg, setMsg] = useState('');

  useEffect(() => {
    SettingsSDK.get().then(data => {
      if (data) {
        if (data.theme) setTheme(data.theme);
        if (data.language) setLanguage(data.language);
      }
    }).catch(err => console.error(err));
  }, []);

  const handleSave = async (e) => {
    e.preventDefault();
    try {
      await SettingsSDK.update({ theme, language });
      setMsg('Settings updated successfully.');
    } catch (err) {
      setMsg('Failed to update settings.');
    }
  };

  return (
    <div style={{ padding: '24px', color: '#fff', fontFamily: 'sans-serif' }}>
      <h1 style={{ fontSize: '28px', fontWeight: 'bold', marginBottom: '8px' }}>Central Settings Center</h1>
      <p style={{ color: '#aaa', marginBottom: '24px' }}>System Preferences, Appearance, & Platform Configuration</p>

      {msg && <div style={{ padding: '12px', background: 'rgba(0,255,136,0.1)', border: '1px solid #00ff88', borderRadius: '6px', marginBottom: '20px' }}>{msg}</div>}

      <form onSubmit={handleSave} style={{ background: 'rgba(255,255,255,0.05)', padding: '24px', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.1)', maxWidth: '500px' }}>
        <div style={{ marginBottom: '16px' }}>
          <label style={{ display: 'block', marginBottom: '6px', color: '#ccc' }}>Appearance Theme</label>
          <select value={theme} onChange={e => setTheme(e.target.value)} style={{ width: '100%', padding: '10px', background: '#111', color: '#fff', border: '1px solid rgba(255,255,255,0.2)', borderRadius: '4px' }}>
            <option value="dark">Dark Theme (Default)</option>
            <option value="light">Light Theme</option>
            <option value="auto">System Auto Sync</option>
          </select>
        </div>
        <div style={{ marginBottom: '24px' }}>
          <label style={{ display: 'block', marginBottom: '6px', color: '#ccc' }}>Language</label>
          <select value={language} onChange={e => setLanguage(e.target.value)} style={{ width: '100%', padding: '10px', background: '#111', color: '#fff', border: '1px solid rgba(255,255,255,0.2)', borderRadius: '4px' }}>
            <option value="en">English (US)</option>
            <option value="es">Spanish</option>
            <option value="de">German</option>
          </select>
        </div>
        <button type="submit" style={{ padding: '10px 20px', background: '#00d2ff', border: 'none', borderRadius: '4px', color: '#000', fontWeight: 'bold', cursor: 'pointer' }}>
          Save Configuration
        </button>
      </form>
    </div>
  );
}
