import React from 'react';

const StatusIndicator = ({ status = 'running', label = 'Running' }) => {
  const isHealthy = status === 'running' || status === 'healthy' || status === 'online';

  return (
    <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-slate-800/80 border border-slate-700/60 text-xs font-medium">
      <span className="relative flex h-2.5 w-2.5">
        <span
          className={`animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 ${
            isHealthy ? 'bg-emerald-400' : 'bg-amber-400'
          }`}
        ></span>
        <span
          className={`relative inline-flex rounded-full h-2.5 w-2.5 ${
            isHealthy ? 'bg-emerald-500' : 'bg-amber-500'
          }`}
        ></span>
      </span>
      <span className={isHealthy ? 'text-emerald-400' : 'text-amber-400'}>
        {label}
      </span>
    </div>
  );
};

export default StatusIndicator;
