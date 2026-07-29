import React, { useState, useEffect } from 'react';
import apiClient from '../api/client';
import { VaultSDK } from '../sdk';
import { Lock, Unlock, Shield, AlertCircle, RefreshCw } from 'lucide-react';

const vaultSDK = new VaultSDK(apiClient);

const VaultPage = () => {
  const [status, setStatus] = useState(null);
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [actionLoading, setActionLoading] = useState(false);

  const fetchStatus = async () => {
    setLoading(true);
    setError('');
    try {
      const data = await vaultSDK.getStatus();
      setStatus(data);
    } catch (e) {
      console.error('Failed to query vault status:', e);
      setError('Could not query secure vault module status.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStatus();
  }, []);

  const handleUnlock = async (e) => {
    e.preventDefault();
    if (!password) return;
    setError('');
    setActionLoading(true);
    try {
      const res = await vaultSDK.unlock(password);
      if (res.status === 'unlocked') {
        setStatus(res);
        setPassword('');
        await fetchStatus();
      } else {
        setError(res.message || 'Incorrect vault decryption credentials.');
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Incorrect vault decryption credentials.');
    } finally {
      setActionLoading(false);
    }
  };

  const handleLock = async () => {
    setError('');
    setActionLoading(true);
    try {
      const res = await vaultSDK.lock();
      if (res.status === 'locked') {
        setStatus(res);
        await fetchStatus();
      }
    } catch (err) {
      setError('Safely unmounting LUKS device failed.');
    } finally {
      setActionLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[400px] gap-3 text-slate-400">
        <RefreshCw className="w-6 h-6 animate-spin text-indigo-500" />
        <span className="text-xs font-semibold">Connecting to secure keystore...</span>
      </div>
    );
  }

  const isUnlocked = status?.status === 'UNLOCKED';

  return (
    <div className="max-w-2xl mx-auto space-y-6 mt-6">
      <div className="text-center space-y-2">
        <div className="inline-flex p-3.5 rounded-2xl bg-indigo-500/10 text-indigo-400 mb-2 border border-indigo-500/20">
          <Shield className="w-6 h-6" />
        </div>
        <h1 className="text-2xl font-bold text-white tracking-tight">Private Crypt Vault</h1>
        <p className="text-xs text-slate-400 max-w-sm mx-auto">
          LUKS2 encrypted block level filesystem storage targetting secure personal configurations, logs, and SSH keys.
        </p>
      </div>

      {error && (
        <div className="p-4 rounded-xl border border-red-500/20 bg-red-500/5 text-red-400 flex items-center gap-3 text-xs font-medium">
          <AlertCircle className="w-4 h-4 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {isUnlocked ? (
        /* UNLOCKED STATE */
        <div className="glass-card border border-emerald-500/20 bg-gradient-to-br from-emerald-950/10 to-slate-950/20 rounded-3xl p-8 text-center space-y-6">
          <div className="inline-flex p-4 rounded-full bg-emerald-500/10 text-emerald-400 ring-8 ring-emerald-500/5 animate-pulse">
            <Unlock className="w-8 h-8" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-emerald-400">Vault Partition Active</h2>
            <p className="text-[11px] text-slate-400 mt-1">Containers have been decrypted and mapped to directory path.</p>
          </div>

          <div className="grid grid-cols-2 gap-4 border border-slate-800/80 bg-slate-900/20 rounded-2xl p-4 text-left text-xs font-medium">
            <div>
              <p className="text-slate-500 font-bold uppercase text-[9px] tracking-wider">Mount Point</p>
              <p className="font-mono text-slate-200 mt-1">{status?.mount_location || '/mnt/vault'}</p>
            </div>
            <div>
              <p className="text-slate-500 font-bold uppercase text-[9px] tracking-wider">Volume Capacity</p>
              <p className="text-slate-200 mt-1">{status?.capacity || 100} GB</p>
            </div>
          </div>

          <button
            onClick={handleLock}
            disabled={actionLoading}
            className="w-full py-3 rounded-xl bg-slate-800 hover:bg-slate-700/80 text-white font-bold text-xs transition-all duration-200 border border-slate-700"
          >
            {actionLoading ? 'Locking Container...' : 'Lock and Secure Vault'}
          </button>
        </div>
      ) : (
        /* LOCKED STATE */
        <div className="glass-card border border-slate-800 p-8 rounded-3xl space-y-6 bg-gradient-to-br from-slate-900/40 to-slate-950/20">
          <div className="text-center space-y-3">
            <div className="inline-flex p-4 rounded-full bg-slate-800 text-slate-500">
              <Lock className="w-8 h-8" />
            </div>
            <div>
              <h2 className="text-sm font-bold text-white">Vault Partition Locked</h2>
              <p className="text-[11px] text-slate-500 mt-1">Input encryption credentials to open LUKS2 filesystem block.</p>
            </div>
          </div>

          <form onSubmit={handleUnlock} className="space-y-4">
            <div>
              <label className="block text-[10px] font-bold uppercase tracking-wider text-slate-400 mb-2">Vault Passphrase</label>
              <input
                type="password"
                placeholder="Enter LUKS master password..."
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-3 rounded-xl bg-slate-950/40 border border-slate-800 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 text-slate-200 placeholder-slate-600 text-xs font-semibold outline-none transition-all duration-150"
              />
            </div>

            <button
              type="submit"
              disabled={actionLoading || !password}
              className="w-full py-3 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-xs transition-all duration-200 shadow-lg shadow-indigo-600/10 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {actionLoading ? 'Decrypting Image...' : 'Decrypt and Unlock Vault'}
            </button>
          </form>
        </div>
      )}
    </div>
  );
};

export default VaultPage;
