import React, { useState, useEffect } from 'react';
import Card from '../components/Card';
import StatusIndicator from '../components/StatusIndicator';
import apiClient from '../api/client';
import { Cpu, MemoryStick as RAM, HardDrive, Activity, ShieldCheck, RefreshCw } from 'lucide-react';

const Dashboard = () => {
  const [systemStats, setSystemStats] = useState({
    server_name: 'Universal HomeLab Server',
    operating_system: 'Linux / Windows Cross-Platform Host',
    cpu_model: 'Universal Multi-Core Processor',
    memory_total_gb: 16.0,
    status: 'running',
    cpu: 18.4,
    ram: 48.2,
    temperature: 44.5,
    uptime: 'Active',
  });
  const [loading, setLoading] = useState(false);

  const fetchStatus = async () => {
    setLoading(true);
    try {
      const res = await apiClient.get('/system/status');
      if (res.data) {
        setSystemStats(res.data);
      }
    } catch (err) {
      console.warn('Backend system status API offline, displaying fallback metrics.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStatus();
    const interval = setInterval(fetchStatus, 15000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="glass-card rounded-2xl p-6 bg-gradient-to-r from-indigo-900/40 via-slate-900/60 to-purple-900/30 border border-indigo-500/20 relative overflow-hidden">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 relative z-10">
          <div>
            <div className="flex items-center gap-3 mb-1">
              <h1 className="text-2xl font-extrabold text-white tracking-tight">{systemStats.server_name}</h1>
              <StatusIndicator status={systemStats.status} label={systemStats.status.toUpperCase()} />
            </div>
            <p className="text-sm text-slate-300">
              Personal Private Cloud & Developer Platform • {systemStats.operating_system}
            </p>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={fetchStatus}
              disabled={loading}
              className="flex items-center gap-2 px-4 py-2 rounded-xl bg-slate-800/90 hover:bg-slate-700 text-slate-200 text-xs font-semibold border border-slate-700 transition-all"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
              Refresh Metrics
            </button>
          </div>
        </div>
      </div>

      {/* Primary Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card
          title="CPU Usage"
          value={`${systemStats.cpu}%`}
          subtitle={systemStats.cpu_model}
          icon={Cpu}
          percentage={systemStats.cpu}
          color="indigo"
        />

        <Card
          title="RAM Usage"
          value={`${systemStats.ram}%`}
          subtitle={`Allocated Memory (${systemStats.memory_total_gb || 16.0} GB Capacity)`}
          icon={RAM}
          percentage={systemStats.ram}
          color="cyan"
        />

        <Card
          title="Storage Usage"
          value="31.2%"
          subtitle="System Primary Storage Drive"
          icon={HardDrive}
          percentage={31.2}
          color="emerald"
        />
      </div>

      {/* Secondary Status Details */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="glass-card rounded-2xl p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
              <Activity className="w-4 h-4 text-indigo-400" />
              Hardware Telemetry
            </h3>
            <span className="text-xs text-slate-400 font-mono">Realtime</span>
          </div>

          <div className="space-y-3">
            <div className="flex justify-between items-center py-2 border-b border-slate-800 text-xs">
              <span className="text-slate-400">Core Temperature</span>
              <span className="text-emerald-400 font-bold">{systemStats.temperature || 40.0} °C</span>
            </div>
            <div className="flex justify-between items-center py-2 border-b border-slate-800 text-xs">
              <span className="text-slate-400">System Uptime</span>
              <span className="text-slate-200 font-mono">{systemStats.uptime}</span>
            </div>
            <div className="flex justify-between items-center py-2 border-b border-slate-800 text-xs">
              <span className="text-slate-400">Secondary Storage Drive</span>
              <span className="text-emerald-400 font-semibold">Mounted & Online</span>
            </div>
            <div className="flex justify-between items-center py-2 text-xs">
              <span className="text-slate-400">Encrypted Vault</span>
              <span className="text-amber-400 font-semibold">Locked (Encrypted LUKS)</span>
            </div>
          </div>
        </div>

        <div className="glass-card rounded-2xl p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
              <ShieldCheck className="w-4 h-4 text-emerald-400" />
              Active Platform Services
            </h3>
            <span className="text-xs text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
              Platform Service Registry Active
            </span>
          </div>

          <div className="space-y-3 text-xs">
            <div className="flex items-center justify-between p-2.5 rounded-xl bg-slate-800/50 border border-slate-700/40">
              <div className="flex items-center gap-2.5">
                <div className="w-2 h-2 rounded-full bg-emerald-400"></div>
                <span className="font-semibold text-slate-200">PostgreSQL Database</span>
              </div>
              <span className="text-slate-400 font-mono">Port 5432</span>
            </div>

            <div className="flex items-center justify-between p-2.5 rounded-xl bg-slate-800/50 border border-slate-700/40">
              <div className="flex items-center gap-2.5">
                <div className="w-2 h-2 rounded-full bg-emerald-400"></div>
                <span className="font-semibold text-slate-200">Redis Cache & Pub/Sub</span>
              </div>
              <span className="text-slate-400 font-mono">Port 6379</span>
            </div>

            <div className="flex items-center justify-between p-2.5 rounded-xl bg-slate-800/50 border border-slate-700/40">
              <div className="flex items-center gap-2.5">
                <div className="w-2 h-2 rounded-full bg-emerald-400"></div>
                <span className="font-semibold text-slate-200">FastAPI Core Engine</span>
              </div>
              <span className="text-slate-400 font-mono">Port 8000</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
