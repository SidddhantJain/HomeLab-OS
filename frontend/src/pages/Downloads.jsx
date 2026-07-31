import React, { useState, useEffect } from 'react';
import apiClient from '../api/client';
import { DownloadSDK } from '../sdk';
import { Download, Plus, RefreshCw, CheckCircle } from 'lucide-react';

const downloadSDK = new DownloadSDK(apiClient);

const DownloadsPage = () => {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [url, setUrl] = useState('');
  const [actionLoading, setActionLoading] = useState(false);

  const fetchTasks = async () => {
    setLoading(true);
    try {
      const data = await downloadSDK.listDownloads();
      setTasks(data);
    } catch (e) {
      console.error('Failed to load download tasks:', e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  const handleEnqueue = async (e) => {
    e.preventDefault();
    if (!url) return;
    setActionLoading(true);
    try {
      await downloadSDK.enqueueDownload(url);
      setUrl('');
      fetchTasks();
    } catch (e) {
      alert('Failed to enqueue download task');
    } finally {
      setActionLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight">Download Manager</h1>
          <p className="text-slate-400 text-xs mt-1">Monitor background file downloads, specify directories, and track byte transfers.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Enqueue Form */}
        <div className="glass-card border border-slate-800 p-6 rounded-2xl bg-gradient-to-br from-slate-900/40 to-slate-950/20 h-fit">
          <h2 className="text-sm font-bold text-white mb-4 flex items-center gap-2">
            <Plus className="w-4 h-4 text-indigo-400" />
            Enqueue URL Link
          </h2>
          <form onSubmit={handleEnqueue} className="space-y-4">
            <div>
              <label className="block text-[10px] font-bold uppercase tracking-wider text-slate-400 mb-1.5">Source URL Path</label>
              <input
                type="text"
                placeholder="https://example.com/target-archive.iso"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                className="w-full px-3 py-2 rounded-xl bg-slate-950/40 border border-slate-800 text-slate-200 text-xs font-semibold outline-none focus:border-indigo-500 transition-all"
              />
            </div>
            <button
              type="submit"
              disabled={actionLoading}
              className="w-full py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-xs transition-all shadow-lg shadow-indigo-600/10 flex items-center justify-center gap-2"
            >
              <Download className="w-3.5 h-3.5" />
              Start Download Task
            </button>
          </form>
        </div>

        {/* Tasks list */}
        <div className="lg:col-span-2 space-y-4">
          {loading ? (
            <div className="flex justify-center py-12">
              <RefreshCw className="w-6 h-6 animate-spin text-indigo-500" />
            </div>
          ) : (
            tasks.map((t) => (
              <div
                key={t.id}
                className="glass-card border border-slate-800/80 p-5 rounded-2xl flex flex-col gap-3 bg-gradient-to-br from-slate-900/30 to-slate-950/10 hover:border-slate-700/60 transition-all"
              >
                <div className="flex justify-between items-start">
                  <div className="space-y-0.5 max-w-[80%]">
                    <span className="block text-xs font-bold text-white truncate">{t.url}</span>
                    <span className="block text-[10px] text-slate-500 font-mono">Location: {t.file_path}</span>
                  </div>
                  <span className={`px-2 py-0.5 rounded-full text-[9px] font-semibold ${
                    t.status === 'COMPLETED' ? 'bg-emerald-500/10 text-emerald-400' : 'bg-slate-800 text-slate-400'
                  }`}>
                    {t.status}
                  </span>
                </div>

                {/* Progress bar */}
                <div className="space-y-1">
                  <div className="flex justify-between text-[10px] text-slate-400 font-mono">
                    <span>Progress: {t.progress}%</span>
                    <span>{(t.total_size / (1024 * 1024)).toFixed(1)} MB</span>
                  </div>
                  <div className="w-full h-1.5 rounded-full bg-slate-950 overflow-hidden">
                    <div
                      className="h-full bg-indigo-600 transition-all duration-300"
                      style={{ width: `${t.progress}%` }}
                    />
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

export default DownloadsPage;
