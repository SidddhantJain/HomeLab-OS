import React, { useState, useEffect } from 'react';
import apiClient from '../api/client';
import { SnapshotSDK, ProjectsSDK } from '../sdk';
import { Camera, RefreshCw, CheckCircle, AlertTriangle } from 'lucide-react';

const snapshotSDK = new SnapshotSDK(apiClient);
const projectsSDK = new ProjectsSDK(apiClient);

const SnapshotsPage = () => {
  const [projects, setProjects] = useState([]);
  const [selectedProjectId, setSelectedProjectId] = useState('');
  const [snapshots, setSnapshots] = useState([]);
  const [loading, setLoading] = useState(false);
  const [actionLoading, setActionLoading] = useState(false);

  useEffect(() => {
    const fetchProjects = async () => {
      try {
        const data = await projectsSDK.list();
        setProjects(data);
        if (data.length > 0) {
          setSelectedProjectId(data[0].id);
        }
      } catch (e) {
        console.error(e);
      }
    };
    fetchProjects();
  }, []);

  const fetchSnapshots = async () => {
    if (!selectedProjectId) return;
    setLoading(true);
    try {
      const data = await snapshotSDK.listSnapshots(selectedProjectId);
      setSnapshots(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSnapshots();
  }, [selectedProjectId]);

  const handleCreate = async () => {
    if (!selectedProjectId) return;
    setActionLoading(true);
    try {
      await snapshotSDK.createSnapshot(selectedProjectId);
      fetchSnapshots();
    } catch (e) {
      alert('Failed to trigger snapshot creation');
    } finally {
      setActionLoading(false);
    }
  };

  const handleRestore = async (id) => {
    if (!confirm('Are you sure you want to restore this snapshot? Active files will be overwritten.')) return;
    setActionLoading(true);
    try {
      await snapshotSDK.restoreSnapshot(id);
      fetchSnapshots();
      alert('Snapshot restored successfully!');
    } catch (e) {
      alert('Failed to restore snapshot');
    } finally {
      setActionLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight">System Snapshots</h1>
          <p className="text-slate-400 text-xs mt-1">Capture point-in-time states of workspace code containers and filesystems.</p>
        </div>
        <button
          onClick={handleCreate}
          disabled={actionLoading || !selectedProjectId}
          className="flex items-center gap-2 px-4 py-2 text-xs font-semibold rounded-xl bg-indigo-600 hover:bg-indigo-750 text-white shadow-lg transition-all"
        >
          <Camera className="w-3.5 h-3.5" />
          Create Snapshot
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Project Selector Sidebar */}
        <div className="glass-card border border-slate-800 p-5 rounded-2xl bg-gradient-to-br from-slate-900/40 to-slate-950/20 h-fit">
          <label className="block text-[10px] font-bold uppercase tracking-wider text-slate-400 mb-2">Select Target Project</label>
          <select
            value={selectedProjectId}
            onChange={(e) => setSelectedProjectId(e.target.value)}
            className="w-full px-3 py-2 rounded-xl bg-slate-950/40 border border-slate-800 text-slate-200 text-xs font-semibold outline-none focus:border-indigo-500 transition-all cursor-pointer"
          >
            {projects.map((p) => (
              <option key={p.id} value={p.id} className="bg-slate-950 text-slate-200">
                {p.name}
              </option>
            ))}
          </select>
        </div>

        {/* Snapshots List */}
        <div className="lg:col-span-3 space-y-4">
          {loading ? (
            <div className="flex justify-center py-12">
              <RefreshCw className="w-6 h-6 animate-spin text-indigo-500" />
            </div>
          ) : snapshots.length === 0 ? (
            <div className="glass-card border border-slate-800 p-8 rounded-2xl text-center space-y-2 text-slate-500">
              <AlertTriangle className="w-8 h-8 mx-auto text-amber-500/80" />
              <p className="text-xs font-semibold">No snapshots registered for this project.</p>
            </div>
          ) : (
            snapshots.map((s) => (
              <div
                key={s.id}
                className="glass-card border border-slate-800/80 p-5 rounded-2xl flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-gradient-to-br from-slate-900/30 to-slate-950/10 hover:border-slate-700/60 transition-all"
              >
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="p-1.5 rounded-lg bg-emerald-500/10 text-emerald-400">
                      <CheckCircle className="w-4 h-4" />
                    </span>
                    <h3 className="text-sm font-bold text-white">Snapshot ID: {s.id.slice(0, 8)}</h3>
                    <span className="px-2 py-0.5 rounded-full text-[9px] font-semibold bg-slate-800 text-slate-400">
                      Cycle {s.retention_cycle}
                    </span>
                  </div>
                  <p className="text-[10px] text-slate-500 font-mono">Created at: {s.created_time}</p>
                </div>

                <div>
                  <button
                    onClick={() => handleRestore(s.id)}
                    disabled={actionLoading}
                    className="px-3 py-1.5 rounded-lg bg-emerald-500/10 text-emerald-400 hover:bg-emerald-500/20 text-[10px] font-bold transition-all"
                  >
                    Restore State
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default SnapshotsPage;
