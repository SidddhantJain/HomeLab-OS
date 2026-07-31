import React, { useState, useEffect } from 'react';
import apiClient from '../api/client';
import { ProjectsSDK } from '../sdk';
import { FolderKanban, Plus, GitBranch, Terminal, RefreshCw } from 'lucide-react';

const projectsSDK = new ProjectsSDK(apiClient);

const ProjectsPage = () => {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [name, setName] = useState('');
  const [path, setPath] = useState('');
  const [description, setDescription] = useState('');

  const fetchProjects = async () => {
    setLoading(true);
    try {
      const data = await projectsSDK.list();
      setProjects(data);
    } catch (e) {
      console.error('Failed to load projects:', e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProjects();
  }, []);

  const handleRegister = async (e) => {
    e.preventDefault();
    if (!name || !path) return;
    try {
      await projectsSDK.create({ name, path, description });
      setName('');
      setPath('');
      setDescription('');
      fetchProjects();
    } catch (e) {
      alert('Failed to register project');
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight">Project Registry</h1>
          <p className="text-slate-400 text-xs mt-1">Register local workspace directories, parse language frameworks, and inspect Git branches.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Register Form */}
        <div className="glass-card border border-slate-800 p-6 rounded-2xl bg-gradient-to-br from-slate-900/40 to-slate-950/20 h-fit">
          <h2 className="text-sm font-bold text-white mb-4 flex items-center gap-2">
            <Plus className="w-4 h-4 text-indigo-400" />
            Register Project
          </h2>
          <form onSubmit={handleRegister} className="space-y-4">
            <div>
              <label className="block text-[10px] font-bold uppercase tracking-wider text-slate-400 mb-1.5">Project Name</label>
              <input
                type="text"
                placeholder="e.g., HomeLab UI"
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="w-full px-3 py-2 rounded-xl bg-slate-950/40 border border-slate-800 text-slate-200 text-xs font-semibold outline-none focus:border-indigo-500 transition-all"
              />
            </div>
            <div>
              <label className="block text-[10px] font-bold uppercase tracking-wider text-slate-400 mb-1.5">Directory Path</label>
              <input
                type="text"
                placeholder="e.g., /opt/homelab/workspaces/app"
                value={path}
                onChange={(e) => setPath(e.target.value)}
                className="w-full px-3 py-2 rounded-xl bg-slate-950/40 border border-slate-800 text-slate-200 text-xs font-semibold outline-none focus:border-indigo-500 transition-all"
              />
            </div>
            <div>
              <label className="block text-[10px] font-bold uppercase tracking-wider text-slate-400 mb-1.5">Description</label>
              <textarea
                placeholder="Repository description..."
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                className="w-full px-3 py-2 rounded-xl bg-slate-950/40 border border-slate-800 text-slate-200 text-xs font-semibold outline-none focus:border-indigo-500 transition-all h-20 resize-none"
              />
            </div>
            <button
              type="submit"
              className="w-full py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-xs transition-all shadow-lg shadow-indigo-600/10"
            >
              Link Codebase
            </button>
          </form>
        </div>

        {/* Projects List */}
        <div className="lg:col-span-2 space-y-4">
          {loading ? (
            <div className="flex justify-center py-12">
              <RefreshCw className="w-6 h-6 animate-spin text-indigo-500" />
            </div>
          ) : (
            projects.map((p) => (
              <div
                key={p.id}
                className="glass-card border border-slate-800/80 p-5 rounded-2xl flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-gradient-to-br from-slate-900/30 to-slate-950/10 hover:border-slate-700/60 transition-all"
              >
                <div className="space-y-1.5">
                  <div className="flex items-center gap-2 flex-wrap">
                    <span className="p-1.5 rounded-lg bg-indigo-500/10 text-indigo-400">
                      <FolderKanban className="w-4 h-4" />
                    </span>
                    <h3 className="text-sm font-bold text-white">{p.name}</h3>
                    <span className="px-2 py-0.5 rounded bg-slate-800 border border-slate-700 text-[10px] font-mono text-slate-300">
                      {p.language}
                    </span>
                    <span className="px-2 py-0.5 rounded bg-slate-800 border border-slate-700 text-[10px] font-mono text-slate-300">
                      {p.framework}
                    </span>
                  </div>
                  <p className="text-xs text-slate-400">{p.description || 'No description provided.'}</p>
                  <div className="flex gap-4 text-[10px] text-slate-500 pt-1 font-mono">
                    <span className="flex items-center gap-1">
                      <GitBranch className="w-3.5 h-3.5" />
                      {p.path}
                    </span>
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

export default ProjectsPage;
