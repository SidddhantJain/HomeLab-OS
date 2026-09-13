import React, { useState, useEffect } from 'react';
import { 
  Server, Power, RotateCw, Globe, Play, Square, ExternalLink, 
  Cpu, HardDrive, ShieldCheck, Activity, CheckCircle2, AlertCircle, 
  Terminal, RefreshCw 
} from 'lucide-react';

const API_BASE = window.location.port === '5173' || window.location.port === '80'
  ? `http://${window.location.hostname}:8000/api/v1`
  : '/api/v1';

export default function ServerManagementPage() {
  const [services, setServices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState({});
  const [bannerMsg, setBannerMsg] = useState(null);
  const [serverStats, setServerStats] = useState({ running: 0, total: 0 });

  const fetchServices = async () => {
    try {
      const res = await fetch(`${API_BASE}/services/list`);
      if (res.ok) {
        const data = await res.json();
        setServices(data.services || []);
        setServerStats({ running: data.running_count, total: data.total });
      }
    } catch (err) {
      console.error('Failed to fetch services:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchServices();
    const interval = setInterval(fetchServices, 4000);
    return () => clearInterval(interval);
  }, []);

  const handleServiceAction = async (serviceId, action) => {
    setActionLoading(prev => ({ ...prev, [serviceId]: action }));
    try {
      const res = await fetch(`${API_BASE}/services/${action}/${serviceId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      });
      const data = await res.json();
      setBannerMsg({ type: res.ok ? 'success' : 'error', text: data.message || `Action ${action} executed.` });
      await fetchServices();
    } catch (err) {
      setBannerMsg({ type: 'error', text: `Failed to ${action} service: ${err.message}` });
    } finally {
      setActionLoading(prev => ({ ...prev, [serviceId]: null }));
      setTimeout(() => setBannerMsg(null), 5000);
    }
  };

  const handleRestartAll = async () => {
    setActionLoading(prev => ({ ...prev, all: 'restart' }));
    try {
      const res = await fetch(`${API_BASE}/services/restart-all`, { method: 'POST' });
      const data = await res.json();
      setBannerMsg({ type: 'success', text: data.message || 'Restarting all services...' });
      setTimeout(fetchServices, 3000);
    } catch (err) {
      setBannerMsg({ type: 'error', text: `Restart failed: ${err.message}` });
    } finally {
      setActionLoading(prev => ({ ...prev, all: null }));
    }
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto pb-12">
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 p-6 rounded-2xl bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 border border-indigo-500/20 shadow-2xl">
        <div>
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2.5 rounded-xl bg-indigo-600/20 text-indigo-400 border border-indigo-500/30">
              <Server className="w-7 h-7" />
            </div>
            <div>
              <h1 className="text-2xl font-black tracking-tight text-white flex items-center gap-2">
                Server & Hosted Web Management
                <span className="text-xs px-2.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 font-semibold">
                  v3.5 Live
                </span>
              </h1>
              <p className="text-sm text-slate-400">
                Turn ON, Turn OFF, restart, and monitor multi-app instances & Virtual IPs on <span className="text-indigo-300 font-mono">192.168.0.182</span>
              </p>
            </div>
          </div>
        </div>

        {/* Global Controls */}
        <div className="flex items-center gap-3">
          <button
            onClick={fetchServices}
            className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-slate-800/80 hover:bg-slate-700 text-slate-200 text-sm font-semibold border border-slate-700 transition shadow-sm"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            Refresh
          </button>
          <button
            onClick={handleRestartAll}
            disabled={actionLoading.all}
            className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-indigo-600 to-indigo-700 hover:from-indigo-500 hover:to-indigo-600 text-white text-sm font-bold shadow-lg shadow-indigo-600/30 transition disabled:opacity-50"
          >
            <RotateCw className={`w-4 h-4 ${actionLoading.all ? 'animate-spin' : ''}`} />
            {actionLoading.all ? 'Restarting...' : 'Restart All Services'}
          </button>
        </div>
      </div>

      {/* Alert Banner */}
      {bannerMsg && (
        <div className={`p-4 rounded-xl flex items-center gap-3 text-sm font-medium border ${
          bannerMsg.type === 'success' 
            ? 'bg-emerald-950/40 text-emerald-300 border-emerald-500/30' 
            : 'bg-rose-950/40 text-rose-300 border-rose-500/30'
        }`}>
          {bannerMsg.type === 'success' ? <CheckCircle2 className="w-5 h-5 text-emerald-400" /> : <AlertCircle className="w-5 h-5 text-rose-400" />}
          <span>{bannerMsg.text}</span>
        </div>
      )}

      {/* Metrics Bar */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 flex items-center justify-between">
          <div>
            <div className="text-xs text-slate-400 font-semibold uppercase tracking-wider">Active Services</div>
            <div className="text-2xl font-black text-emerald-400 mt-1">{serverStats.running} / {serverStats.total}</div>
          </div>
          <div className="p-3 rounded-xl bg-emerald-500/10 text-emerald-400">
            <Activity className="w-5 h-5" />
          </div>
        </div>

        <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 flex items-center justify-between">
          <div>
            <div className="text-xs text-slate-400 font-semibold uppercase tracking-wider">Primary Server IP</div>
            <div className="text-xl font-black text-indigo-400 font-mono mt-1">192.168.0.182</div>
          </div>
          <div className="p-3 rounded-xl bg-indigo-500/10 text-indigo-400">
            <Globe className="w-5 h-5" />
          </div>
        </div>

        <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 flex items-center justify-between">
          <div>
            <div className="text-xs text-slate-400 font-semibold uppercase tracking-wider">Virtual IP Pool</div>
            <div className="text-lg font-bold text-slate-200 font-mono mt-1">.182 – .187 (Port 80)</div>
          </div>
          <div className="p-3 rounded-xl bg-purple-500/10 text-purple-400">
            <ShieldCheck className="w-5 h-5" />
          </div>
        </div>

        <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 flex items-center justify-between">
          <div>
            <div className="text-xs text-slate-400 font-semibold uppercase tracking-wider">Process Manager</div>
            <div className="text-lg font-bold text-slate-200 mt-1">Systemd + POSIX</div>
          </div>
          <div className="p-3 rounded-xl bg-amber-500/10 text-amber-400">
            <Terminal className="w-5 h-5" />
          </div>
        </div>
      </div>

      {/* Services Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        {services.map((srv) => {
          const isBusy = actionLoading[srv.id];
          return (
            <div 
              key={srv.id}
              className={`p-6 rounded-2xl border transition-all duration-200 flex flex-col justify-between ${
                srv.is_running
                  ? 'bg-slate-900/80 border-slate-800 hover:border-indigo-500/30 shadow-lg'
                  : 'bg-slate-950/60 border-slate-900/80 opacity-80'
              }`}
            >
              <div>
                {/* Card Top */}
                <div className="flex items-start justify-between gap-3 mb-3">
                  <div>
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded bg-slate-800 text-slate-400">
                        {srv.category}
                      </span>
                      <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-indigo-950/60 text-indigo-400 border border-indigo-500/20">
                        Port {srv.port}
                      </span>
                    </div>
                    <h3 className="text-lg font-bold text-white tracking-tight">{srv.name}</h3>
                  </div>

                  {/* Status Badge */}
                  <div className={`flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold border ${
                    srv.is_running 
                      ? 'bg-emerald-500/15 text-emerald-400 border-emerald-500/30 animate-pulse'
                      : 'bg-rose-500/15 text-rose-400 border-rose-500/30'
                  }`}>
                    <span className={`w-2 h-2 rounded-full ${srv.is_running ? 'bg-emerald-400' : 'bg-rose-400'}`} />
                    {srv.is_running ? 'ONLINE' : 'STOPPED'}
                  </div>
                </div>

                <p className="text-xs text-slate-400 mb-4 leading-relaxed">{srv.description}</p>

                {/* Network & Endpoints info */}
                <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800/80 space-y-2 mb-5">
                  <div className="flex items-center justify-between text-xs">
                    <span className="text-slate-400">Virtual IP (Port 80):</span>
                    <a 
                      href={srv.vip_url} 
                      target="_blank" 
                      rel="noreferrer"
                      className="font-mono text-indigo-400 hover:text-indigo-300 flex items-center gap-1 font-semibold"
                    >
                      {srv.virtual_ip}
                      <ExternalLink className="w-3 h-3" />
                    </a>
                  </div>
                  <div className="flex items-center justify-between text-xs">
                    <span className="text-slate-400">Direct Port URL:</span>
                    <a 
                      href={srv.url} 
                      target="_blank" 
                      rel="noreferrer"
                      className="font-mono text-slate-300 hover:text-white flex items-center gap-1"
                    >
                      {srv.url}
                      <ExternalLink className="w-3 h-3" />
                    </a>
                  </div>
                  {srv.pid && (
                    <div className="flex items-center justify-between text-xs pt-1 border-t border-slate-800/60">
                      <span className="text-slate-500">PID: <span className="font-mono text-slate-400">{srv.pid}</span></span>
                      <span className="text-slate-500">CPU: <span className="font-mono text-slate-400">{srv.cpu_percent}%</span> • RAM: <span className="font-mono text-slate-400">{srv.memory_mb} MB</span></span>
                    </div>
                  )}
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex items-center gap-2 pt-3 border-t border-slate-800/80">
                {srv.is_running ? (
                  <>
                    <button
                      onClick={() => handleServiceAction(srv.id, 'stop')}
                      disabled={isBusy}
                      className="flex-1 flex items-center justify-center gap-2 py-2 px-3 rounded-xl bg-rose-500/10 hover:bg-rose-500/20 text-rose-400 text-xs font-bold border border-rose-500/30 transition disabled:opacity-50"
                    >
                      <Square className="w-3.5 h-3.5 fill-current" />
                      {isBusy === 'stop' ? 'Stopping...' : 'Turn OFF'}
                    </button>
                    <button
                      onClick={() => handleServiceAction(srv.id, 'restart')}
                      disabled={isBusy}
                      className="flex-1 flex items-center justify-center gap-2 py-2 px-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-bold border border-slate-700 transition disabled:opacity-50"
                    >
                      <RotateCw className={`w-3.5 h-3.5 ${isBusy === 'restart' ? 'animate-spin' : ''}`} />
                      {isBusy === 'restart' ? 'Restarting...' : 'Restart'}
                    </button>
                    <a
                      href={srv.vip_url || srv.url}
                      target="_blank"
                      rel="noreferrer"
                      className="py-2 px-3 rounded-xl bg-indigo-600/20 hover:bg-indigo-600/30 text-indigo-300 text-xs font-bold border border-indigo-500/30 flex items-center gap-1.5 transition"
                    >
                      <ExternalLink className="w-3.5 h-3.5" />
                      Open
                    </a>
                  </>
                ) : (
                  <>
                    <button
                      onClick={() => handleServiceAction(srv.id, 'start')}
                      disabled={isBusy}
                      className="flex-1 flex items-center justify-center gap-2 py-2 px-4 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold shadow-lg shadow-emerald-600/20 transition disabled:opacity-50"
                    >
                      <Play className="w-3.5 h-3.5 fill-current" />
                      {isBusy === 'start' ? 'Starting...' : 'Turn ON Service'}
                    </button>
                  </>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
