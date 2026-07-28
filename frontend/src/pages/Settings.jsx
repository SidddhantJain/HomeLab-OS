import React from 'react';
import { Settings as SettingsIcon, Shield, Database, Cpu, Terminal } from 'lucide-react';

const Settings = () => {
  return (
    <div className="space-y-6">
      <div className="glass-card rounded-2xl p-6">
        <div className="flex items-center gap-3 mb-2">
          <div className="p-2.5 rounded-xl bg-indigo-600/20 border border-indigo-500/30 text-indigo-400">
            <SettingsIcon className="w-5 h-5" />
          </div>
          <div>
            <h1 className="text-xl font-extrabold text-white">Platform Settings</h1>
            <p className="text-xs text-slate-400">Manage system parameters, access control, and environment settings</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="glass-card rounded-2xl p-6">
          <div className="flex items-center gap-2 mb-4 text-indigo-400">
            <Shield className="w-4 h-4" />
            <h3 className="text-sm font-bold uppercase tracking-wider text-white">Security & Authentication</h3>
          </div>
          <div className="space-y-3 text-xs text-slate-300">
            <div className="flex justify-between items-center py-2 border-b border-slate-800">
              <span>Password Algorithm</span>
              <span className="font-mono bg-slate-800 px-2 py-0.5 rounded text-indigo-400">Bcrypt (Salt rounds 12)</span>
            </div>
            <div className="flex justify-between items-center py-2 border-b border-slate-800">
              <span>JWT Secret Key</span>
              <span className="font-mono bg-slate-800 px-2 py-0.5 rounded text-emerald-400">Configured (.env)</span>
            </div>
            <div className="flex justify-between items-center py-2">
              <span>Access Token TTL</span>
              <span className="font-mono bg-slate-800 px-2 py-0.5 rounded text-slate-200">1440 mins (24 Hours)</span>
            </div>
          </div>
        </div>

        <div className="glass-card rounded-2xl p-6">
          <div className="flex items-center gap-2 mb-4 text-emerald-400">
            <Database className="w-4 h-4" />
            <h3 className="text-sm font-bold uppercase tracking-wider text-white">Database Engine</h3>
          </div>
          <div className="space-y-3 text-xs text-slate-300">
            <div className="flex justify-between items-center py-2 border-b border-slate-800">
              <span>Database Provider</span>
              <span className="font-mono bg-slate-800 px-2 py-0.5 rounded text-emerald-400">PostgreSQL 16</span>
            </div>
            <div className="flex justify-between items-center py-2 border-b border-slate-800">
              <span>ORM & Migration Tool</span>
              <span className="font-mono bg-slate-800 px-2 py-0.5 rounded text-slate-200">SQLAlchemy 2.0 + Alembic</span>
            </div>
            <div className="flex justify-between items-center py-2">
              <span>Cache Engine</span>
              <span className="font-mono bg-slate-800 px-2 py-0.5 rounded text-cyan-400">Redis 7</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Settings;
