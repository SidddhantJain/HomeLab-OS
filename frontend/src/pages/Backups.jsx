import React, { useState, useEffect } from 'react';
import apiClient from '../api/client';
import { BackupSDK } from '../sdk';
import { Database, Plus, RefreshCw, CheckCircle2, Play } from 'lucide-react';

const backupSDK = new BackupSDK(apiClient);

const BackupsPage = () => {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [name, setName] = useState('');
  const [source, setSource] = useState('');
  const [destination, setDestination] = useState('');
  const [actionLoading, setActionLoading] = useState(false);

  const fetchJobs = async () => {
    setLoading(true);
    try {
      const data = await backupSDK.listBackupJobs();
      setJobs(data);
    } catch (e) {
      console.error('Failed to load backup jobs:', e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchJobs();
  }, []);

  const handleTrigger = async (e) => {
    e.preventDefault();
    if (!name || !source || !destination) return;
    setActionLoading(true);
    try {
      await backupSDK.triggerBackup(name, source, destination);
      setName('');
      setSource('');
      setDestination('');
      fetchJobs();
    } catch (e) {
      alert('Failed to trigger backup run');
    } finally {
      setActionLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight">System Backups</h1>
          <p className="text-slate-400 text-xs mt-1">Configure workspace backup jobs to local directories, external HDD mounts, or network locations.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Trigger Form */}
        <div className="glass-card border border-slate-800 p-6 rounded-2xl bg-gradient-to-br from-slate-900/40 to-slate-950/20 h-fit">
          <h2 className="text-sm font-bold text-white mb-4 flex items-center gap-2">
            <Plus className="w-4 h-4 text-indigo-400" />
            Trigger Backup Job
          </h2>
          <form onSubmit={handleTrigger} className="space-y-4">
            <div>
              <label className="block text-[10px] font-bold uppercase tracking-wider text-slate-400 mb-1.5">Job Identifier</label>
              <input
                type="text"
                placeholder="e.g., Nightly Partition Sync"
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="w-full px-3 py-2 rounded-xl bg-slate-950/40 border border-slate-800 text-slate-200 text-xs font-semibold outline-none focus:border-indigo-500 transition-all"
              />
            </div>
            <div>
              <label className="block text-[10px] font-bold uppercase tracking-wider text-slate-400 mb-1.5">Source Directory</label>
              <input
                type="text"
                placeholder="e.g., /opt/homelab/workspaces"
                value={source}
                onChange={(e) => setSource(e.target.value)}
                className="w-full px-3 py-2 rounded-xl bg-slate-950/40 border border-slate-800 text-slate-200 text-xs font-semibold outline-none focus:border-indigo-500 transition-all"
              />
            </div>
            <div>
              <label className="block text-[10px] font-bold uppercase tracking-wider text-slate-400 mb-1.5">Destination Directory</label>
              <input
                type="text"
                placeholder="e.g., /mnt/homelab-storage/backups"
                value={destination}
                onChange={(e) => setDestination(e.target.value)}
                className="w-full px-3 py-2 rounded-xl bg-slate-950/40 border border-slate-800 text-slate-200 text-xs font-semibold outline-none focus:border-indigo-500 transition-all"
              />
            </div>
            <button
              type="submit"
              disabled={actionLoading}
              className="w-full py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-xs transition-all shadow-lg shadow-indigo-600/10 flex items-center justify-center gap-2"
            >
              <Play className="w-3.5 h-3.5 fill-current" />
              Run Backup Task
            </button>
          </form>
        </div>

        {/* Backups List */}
        <div className="lg:col-span-2 space-y-4">
          {loading ? (
            <div className="flex justify-center py-12">
              <RefreshCw className="w-6 h-6 animate-spin text-indigo-500" />
            </div>
          ) : (
            jobs.map((j) => (
              <div
                key={j.id}
                className="glass-card border border-slate-800/80 p-5 rounded-2xl flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-gradient-to-br from-slate-900/30 to-slate-950/10 hover:border-slate-700/60 transition-all"
              >
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="p-1.5 rounded-lg bg-indigo-500/10 text-indigo-400">
                      <Database className="w-4 h-4" />
                    </span>
                    <h3 className="text-sm font-bold text-white">{j.name}</h3>
                    <span className={`px-2 py-0.5 rounded-full text-[9px] font-semibold ${
                      j.status === 'COMPLETED' ? 'bg-emerald-500/10 text-emerald-400' : 'bg-slate-800 text-slate-400'
                    }`}>
                      {j.status}
                    </span>
                  </div>
                  <div className="flex flex-col gap-1 text-[10px] text-slate-500 pt-1 font-mono">
                    <span>Source: {j.source}</span>
                    <span>Dest: {j.destination}</span>
                    <span>Completed at: {j.completed_at || 'In progress'}</span>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default BackupsPage;
