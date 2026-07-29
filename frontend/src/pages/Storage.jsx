import React, { useState, useEffect } from 'react';
import apiClient from '../api/client';
import { StorageSDK } from '../sdk';
import { HardDrive, RefreshCw, Activity, ShieldAlert, CheckCircle } from 'lucide-react';

const storageSDK = new StorageSDK(apiClient);

const StoragePage = () => {
  const [devices, setDevices] = useState([]);
  const [health, setHealth] = useState(null);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(null);

  const fetchStorageData = async () => {
    setLoading(true);
    try {
      const devList = await storageSDK.listDevices();
      const healthData = await storageSDK.getHealth();
      setDevices(devList);
      setHealth(healthData);
    } catch (e) {
      console.error('Failed to load storage data:', e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStorageData();
  }, []);

  const handleMount = async (id) => {
    setActionLoading(id);
    try {
      await storageSDK.mountDevice(id);
      await fetchStorageData();
    } catch (e) {
      alert('Mount action failed');
    } finally {
      setActionLoading(null);
    }
  };

  const handleUnmount = async (id) => {
    setActionLoading(id);
    try {
      await storageSDK.unmountDevice(id);
      await fetchStorageData();
    } catch (e) {
      alert('Unmount action failed');
    } finally {
      setActionLoading(null);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight">Storage Pools</h1>
          <p className="text-slate-400 text-xs mt-1">Manage physical SSD arrays, partitions, and external disk mounts.</p>
        </div>
        <button
          onClick={fetchStorageData}
          disabled={loading}
          className="flex items-center gap-2 px-4 py-2 text-xs font-semibold rounded-xl bg-slate-800 text-slate-200 border border-slate-700/60 hover:bg-slate-700/80 transition-all duration-200"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
          Refresh Pools
        </button>
      </div>

      {/* Health Overview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="glass-card border border-slate-800/80 p-5 rounded-2xl flex items-center gap-4 bg-gradient-to-br from-slate-900/40 to-slate-950/20">
          <div className="p-3 rounded-xl bg-indigo-500/10 text-indigo-400">
            <HardDrive className="w-6 h-6" />
          </div>
          <div>
            <p className="text-[10px] text-slate-500 font-bold uppercase tracking-wider">Storage Status</p>
            <p className="text-lg font-bold text-white mt-0.5">{loading ? 'Scanning...' : 'Active'}</p>
          </div>
        </div>

        <div className="glass-card border border-slate-800/80 p-5 rounded-2xl flex items-center gap-4 bg-gradient-to-br from-slate-900/40 to-slate-950/20">
          <div className={`p-3 rounded-xl ${health?.status === 'healthy' ? 'bg-emerald-500/10 text-emerald-400' : 'bg-amber-500/10 text-amber-400'}`}>
            <Activity className="w-6 h-6" />
          </div>
          <div>
            <p className="text-[10px] text-slate-500 font-bold uppercase tracking-wider">SMART Diagnostic</p>
            <p className="text-lg font-bold text-white mt-0.5">
              {loading ? 'Analyzing...' : health?.status === 'healthy' ? 'ALL PASSED' : 'WARNING'}
            </p>
          </div>
        </div>

        <div className="glass-card border border-slate-800/80 p-5 rounded-2xl flex items-center gap-4 bg-gradient-to-br from-slate-900/40 to-slate-950/20">
          <div className="p-3 rounded-xl bg-indigo-500/10 text-indigo-400">
            <CheckCircle className="w-6 h-6" />
          </div>
          <div>
            <p className="text-[10px] text-slate-500 font-bold uppercase tracking-wider">Disk Health Score</p>
            <p className="text-lg font-bold text-white mt-0.5">100% Good</p>
          </div>
        </div>
      </div>

      {/* Disks Table */}
      <div className="glass-card border border-slate-800/80 rounded-2xl overflow-hidden bg-gradient-to-br from-slate-900/30 to-slate-950/10">
        <div className="px-6 py-4 border-b border-slate-800/60 bg-slate-900/20">
          <h2 className="text-sm font-bold text-white">Detected Disks & Mount points</h2>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full border-collapse text-left">
            <thead>
              <tr className="border-b border-slate-800/40 text-[10px] text-slate-500 font-bold uppercase tracking-wider">
                <th className="px-6 py-3.5">Device Name</th>
                <th className="px-6 py-3.5">Capacity</th>
                <th className="px-6 py-3.5">Filesystem</th>
                <th className="px-6 py-3.5">Mount Point</th>
                <th className="px-6 py-3.5">Type</th>
                <th className="px-6 py-3.5">Status</th>
                <th className="px-6 py-3.5 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/30 text-xs">
              {devices.map((dev) => (
                <tr key={dev.id} className="hover:bg-slate-900/20 transition-all duration-150">
                  <td className="px-6 py-4 font-semibold text-slate-200">{dev.name}</td>
                  <td className="px-6 py-4 text-slate-300">{dev.capacity_gb} GB</td>
                  <td className="px-6 py-4 text-slate-400 font-mono">{dev.filesystem || 'N/A'}</td>
                  <td className="px-6 py-4 text-slate-300 font-mono">{dev.status === 'active' ? '/mnt/homelab-storage' : 'Unmounted'}</td>
                  <td className="px-6 py-4">
                    <span className="px-2 py-0.5 rounded bg-slate-800 text-[10px] font-bold text-slate-400 uppercase border border-slate-700/50">
                      {dev.type}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <span className={`inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full text-[10px] font-semibold ${
                      dev.status === 'active' ? 'bg-emerald-500/10 text-emerald-400' : 'bg-slate-800 text-slate-400'
                    }`}>
                      <span className={`w-1.5 h-1.5 rounded-full ${dev.status === 'active' ? 'bg-emerald-400 animate-pulse' : 'bg-slate-500'}`} />
                      {dev.status === 'active' ? 'Mounted' : 'Available'}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-right">
                    {dev.status === 'active' ? (
                      <button
                        onClick={() => handleUnmount(dev.id)}
                        disabled={actionLoading !== null}
                        className="px-3 py-1.5 rounded-lg text-[10px] font-bold bg-amber-500/10 text-amber-400 hover:bg-amber-500/20 transition-all duration-200"
                      >
                        {actionLoading === dev.id ? 'Safely Closing...' : 'Unmount'}
                      </button>
                    ) : (
                      <button
                        onClick={() => handleMount(dev.id)}
                        disabled={actionLoading !== null}
                        className="px-3 py-1.5 rounded-lg text-[10px] font-bold bg-indigo-600 text-white hover:bg-indigo-700 transition-all duration-200"
                      >
                        {actionLoading === dev.id ? 'Mounting...' : 'Mount Disk'}
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default StoragePage;
