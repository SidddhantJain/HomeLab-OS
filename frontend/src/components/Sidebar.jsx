import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, HardDrive, Lock, FolderKanban, Settings, Cpu } from 'lucide-react';

const Sidebar = () => {
  const navItems = [
    { path: '/', label: 'Dashboard', icon: LayoutDashboard },
    { path: '/storage', label: 'Storage', icon: HardDrive },
    { path: '/vault', label: 'Private Vault', icon: Lock },
    { path: '/projects', label: 'Projects', icon: FolderKanban, disabled: true },
    { path: '/settings', label: 'Settings', icon: Settings },
  ];


  return (
    <aside className="w-64 glass-nav border-r border-slate-800 p-4 flex flex-col justify-between hidden md:flex min-h-[calc(100vh-61px)]">
      <div className="space-y-1">
        <div className="px-3 py-2 text-[10px] font-bold uppercase tracking-wider text-slate-500">
          Core Navigation
        </div>
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.path}
              to={item.disabled ? '#' : item.path}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-sm font-medium transition-all duration-200 ${
                  item.disabled
                    ? 'text-slate-600 cursor-not-allowed opacity-60'
                    : isActive
                    ? 'bg-gradient-to-r from-indigo-600 to-indigo-700 text-white shadow-lg shadow-indigo-600/20'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
                }`
              }
            >
              <Icon className="w-4 h-4" />
              <span>{item.label}</span>
              {item.disabled && (
                <span className="ml-auto text-[9px] uppercase px-1.5 py-0.5 rounded bg-slate-800 text-slate-500 font-semibold">
                  v0.2
                </span>
              )}
            </NavLink>
          );
        })}
      </div>

      <div className="p-4 rounded-xl glass-card border border-indigo-500/20 bg-gradient-to-br from-indigo-900/20 to-slate-900/40">
        <div className="flex items-center gap-2 mb-2 text-indigo-400">
          <Cpu className="w-4 h-4" />
          <span className="text-xs font-bold">Node Specification</span>
        </div>
        <p className="text-[11px] text-slate-300 font-medium">Intel i7-5500U</p>
        <p className="text-[10px] text-slate-400">8GB RAM • 240GB SSD • 1TB HDD</p>
      </div>
    </aside>
  );
};

export default Sidebar;
