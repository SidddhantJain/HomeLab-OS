import React, { useState, useEffect } from 'react';
import apiClient from '../api/client';
import { WorkspaceSDK } from '../sdk';
import { Layers, Plus, Archive, Trash, RefreshCw } from 'lucide-react';

const workspaceSDK = new WorkspaceSDK(apiClient);

const WorkspacePage = () => {
  const [workspaces, setWorkspaces] = useState([]);
  const [loading, setLoading] = useState(true);
  const [name, setName] = useState('');
  const [owner, setOwner] = useState('');
  const [description, setDescription] = useState('');

  const fetchWorkspaces = async () => {
    setLoading(true);
    try {
      const data = await workspaceSDK.listWorkspaces();
      setWorkspaces(data);
    } catch (e) {
      console.error('Failed to load workspaces:', e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchWorkspaces();
  }, []);

  const handleCreate = async (e) => {
    e.preventDefault();
    if (!name || !owner) return;
    try {
      await workspaceSDK.createWorkspace(name, owner, description);
      setName('');
      setOwner('');
      setDescription('');
      fetchWorkspaces();
    } catch (e) {
      alert('Failed to create workspace');
    }
  };

  const handleArchive = async (id) => {
    try {
      await workspaceSDK.archiveWorkspace(id);
      fetchWorkspaces();
    } catch (e) {
      alert('Failed to archive workspace');
    }
  };

  const handleRestore = async (id) => {
    try {
      await workspaceSDK.restoreWorkspace(id);
      fetchWorkspaces();
    } catch (e) {
      alert('Failed to restore workspace');
    }
  };

  const handleDelete = async (id) => {
    if (!confirm('Are you sure you want to delete this workspace?')) return;
    try {
      await workspaceSDK.deleteWorkspace(id);
      fetchWorkspaces();
    } catch (e) {
      alert('Failed to delete workspace');
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight">Workspace Management</h1>
          <p className="text-slate-400 text-xs mt-1">Manage project storage boundaries, ownership parameters, and size usage.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Create Form */}
        <div className="glass-card border border-slate-800 p-6 rounded-2xl bg-gradient-to-br from-slate-900/40 to-slate-950/20 h-fit">
          <h2 className="text-sm font-bold text-white mb-4 flex items-center gap-2">
            <Plus className="w-4 h-4 text-indigo-400" />
            Create Workspace
          </h2>
          <form onSubmit={handleCreate} className="space-y-4">
            <div>
              <label className="block text-[10px] font-bold uppercase tracking-wider text-slate-400 mb-1.5">Workspace Name</label>
              <input
                type="text"
                placeholder="e.g., frontend-prod"
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="w-full px-3 py-2 rounded-xl bg-slate-950/40 border border-slate-800 text-slate-200 text-xs font-semibold outline-none focus:border-indigo-500 transition-all"
              />
            </div>
            <div>
              <label className="block text-[10px] font-bold uppercase tracking-wider text-slate-400 mb-1.5">Owner</label>
              <input
                type="text"
                placeholder="e.g., admin"
                value={owner}
                onChange={(e) => setOwner(e.target.value)}
                className="w-full px-3 py-2 rounded-xl bg-slate-950/40 border border-slate-800 text-slate-200 text-xs font-semibold outline-none focus:border-indigo-500 transition-all"
              />
            </div>
            <div>
              <label className="block text-[10px] font-bold uppercase tracking-wider text-slate-400 mb-1.5">Description</label>
              <textarea
                placeholder="Brief description of the workspace usage..."
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                className="w-full px-3 py-2 rounded-xl bg-slate-950/40 border border-slate-800 text-slate-200 text-xs font-semibold outline-none focus:border-indigo-500 transition-all h-20 resize-none"
              />
            </div>
            <button
              type="submit"
              className="w-full py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-xs transition-all shadow-lg shadow-indigo-600/10"
            >
              Initialize Workspace
            </button>
          </form>
        </div>

        {/* Workspaces List */}
        <div className="lg:col-span-2 space-y-4">
          {loading ? (
            <div className="flex justify-center py-12">
              <RefreshCw className="w-6 h-6 animate-spin text-indigo-500" />
            </div>
          ) : (
            workspaces.map((w) => (
              <div
                key={w.id}
                className="glass-card border border-slate-800/80 p-5 rounded-2xl flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-gradient-to-br from-slate-900/30 to-slate-950/10 hover:border-slate-700/60 transition-all"
              >
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="p-1.5 rounded-lg bg-indigo-500/10 text-indigo-400">
                      <Layers className="w-4 h-4" />
                    </span>
                    <h3 className="text-sm font-bold text-white">{w.name}</h3>
                    <span className={`px-2 py-0.5 rounded-full text-[9px] font-semibold ${
                      w.status === 'ACTIVE' ? 'bg-emerald-500/10 text-emerald-400' : 'bg-slate-800 text-slate-400'
                    }`}>
                      {w.status}
                    </span>
                  </div>
                  <p className="text-xs text-slate-400">{w.description || 'No description provided.'}</p>
                  <div className="flex gap-4 text-[10px] text-slate-500 pt-1 font-mono">
                    <span>Owner: {w.owner}</span>
                    <span>Path: {w.storage_location}</span>
                  </div>
                </div>

                <div className="flex gap-2 w-full md:w-auto justify-end">
                  {w.status === 'ACTIVE' ? (
                    <button
                      onClick={() => handleArchive(w.id)}
                      className="p-2 rounded-lg bg-slate-800 text-slate-400 hover:bg-slate-700 hover:text-slate-200 transition-all"
                      title="Archive Workspace"
                    >
                      <Archive className="w-4 h-4" />
                    </button>
                  ) : (
                    <button
                      onClick={() => handleRestore(w.id)}
                      className="px-3 py-1.5 rounded-lg bg-indigo-500/10 text-indigo-400 hover:bg-indigo-500/20 text-[10px] font-bold transition-all"
                    >
                      Restore
                    </button>
                  )}
                  <button
                    onClick={() => handleDelete(w.id)}
                    className="p-2 rounded-lg bg-red-500/10 text-red-400 hover:bg-red-500/20 transition-all"
                    title="Delete Workspace"
                  >
                    <Trash className="w-4 h-4" />
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

export default WorkspacePage;
