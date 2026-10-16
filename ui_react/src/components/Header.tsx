import React from 'react';
import { ShieldCheck, Database, Server } from 'lucide-react';

interface Props {
  title: string;
  subtitle: string;
}

export const Header: React.FC<Props> = ({ title, subtitle }) => {
  return (
    <header className="bg-white/90 backdrop-blur-md border-b border-slate-200 px-8 py-5 flex items-center justify-between sticky top-0 z-30 shadow-xs">
      <div>
        <h2 className="text-xl font-bold text-slate-900 tracking-tight font-header">{title}</h2>
        <p className="text-xs text-slate-500 font-normal mt-0.5 font-body">{subtitle}</p>
      </div>

      <div className="flex items-center gap-4 text-xs font-body">
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-100 border border-slate-200 text-slate-700 font-medium">
          <Server className="w-4 h-4 text-indigo-600" />
          <span>FastAPI :8050</span>
        </div>
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-100 border border-slate-200 text-slate-700 font-medium">
          <Database className="w-4 h-4 text-teal-600" />
          <span>SQLite Sync</span>
        </div>
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-emerald-50 border border-emerald-200 text-emerald-700 font-semibold">
          <ShieldCheck className="w-4 h-4 text-emerald-600" />
          <span>XGBoost</span>
        </div>
      </div>
    </header>
  );
};
