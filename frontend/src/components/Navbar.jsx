import React from 'react';
import { Server, Bell, User, LogOut } from 'lucide-react';
import StatusIndicator from './StatusIndicator';

const Navbar = ({ user, onLogout }) => {
  return (
    <header className="sticky top-0 z-30 glass-nav px-6 py-3.5 flex items-center justify-between">
      <div className="flex items-center gap-3">
        <div className="p-2 rounded-xl bg-indigo-600/20 border border-indigo-500/30 text-indigo-400">
          <Server className="w-5 h-5" />
        </div>
        <div>
          <h1 className="text-base font-bold text-white tracking-tight">HomeLab OS</h1>
          <p className="text-xs text-slate-400">Dell Inspiron 5558 • v1.0</p>
        </div>
      </div>

      <div className="flex items-center gap-4">
        <StatusIndicator status="running" label="Server Online" />
        
        <button
          aria-label="Notifications"
          className="p-2 rounded-xl bg-slate-800/80 hover:bg-slate-700/80 text-slate-300 transition-colors border border-slate-700/60"
        >
          <Bell className="w-4 h-4" />
        </button>

        {user ? (
          <div className="flex items-center gap-3 pl-3 border-l border-slate-700/60">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-indigo-500 to-purple-600 flex items-center justify-center text-white font-semibold text-xs shadow-md">
                {user.username ? user.username.substring(0, 2).toUpperCase() : 'AD'}
              </div>
              <span className="text-sm font-medium text-slate-200 hidden sm:inline">
                {user.username}
              </span>
            </div>
            <button
              onClick={onLogout}
              title="Logout"
              aria-label="Logout"
              className="p-2 rounded-xl bg-slate-800/80 hover:bg-rose-500/20 hover:text-rose-400 text-slate-400 transition-colors border border-slate-700/60"
            >
              <LogOut className="w-4 h-4" />
            </button>
          </div>
        ) : (
          <a
            href="/login"
            className="text-xs font-semibold px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white transition-all shadow-lg shadow-indigo-600/30"
          >
            Sign In
          </a>
        )}
      </div>
    </header>
  );
};

export default Navbar;
