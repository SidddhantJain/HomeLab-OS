import React from 'react';

const Card = ({ title, value, subtitle, icon: Icon, percentage, color = 'indigo', children }) => {
  const colorMap = {
    indigo: 'from-indigo-500/20 to-purple-500/10 text-indigo-400 border-indigo-500/30',
    cyan: 'from-cyan-500/20 to-blue-500/10 text-cyan-400 border-cyan-500/30',
    emerald: 'from-emerald-500/20 to-teal-500/10 text-emerald-400 border-emerald-500/30',
    amber: 'from-amber-500/20 to-orange-500/10 text-amber-400 border-amber-500/30',
  };

  return (
    <div className="glass-card rounded-2xl p-6 transition-all duration-300 hover:border-slate-600/80 hover:shadow-xl hover:shadow-indigo-500/5">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-400">{title}</h3>
          {value && <div className="text-2xl font-bold text-white mt-1">{value}</div>}
        </div>
        {Icon && (
          <div className={`p-3 rounded-xl bg-gradient-to-br ${colorMap[color] || colorMap.indigo} border`}>
            <Icon className="w-6 h-6" />
          </div>
        )}
      </div>

      {percentage !== undefined && (
        <div className="w-full bg-slate-800 rounded-full h-2 overflow-hidden mb-3">
          <div
            className={`h-full bg-gradient-to-r ${
              color === 'indigo' ? 'from-indigo-500 to-purple-500' :
              color === 'cyan' ? 'from-cyan-500 to-blue-500' :
              color === 'emerald' ? 'from-emerald-500 to-teal-500' : 'from-amber-500 to-orange-500'
            }`}
            style={{ width: `${Math.min(100, Math.max(0, percentage))}%` }}
          />
        </div>
      )}

      {subtitle && <p className="text-xs text-slate-400 font-medium">{subtitle}</p>}
      {children}
    </div>
  );
};

export default Card;
