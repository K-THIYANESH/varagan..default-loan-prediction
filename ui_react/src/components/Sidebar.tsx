import React from 'react';
import {
  LayoutDashboard,
  UserCheck,
  Cpu,
  FileText,
  Activity
} from 'lucide-react';

export type PageTab = 'dashboard' | 'assessment' | 'model' | 'reports';

interface Props {
  activeTab: PageTab;
  setActiveTab: (tab: PageTab) => void;
}

export const Sidebar: React.FC<Props> = ({ activeTab, setActiveTab }) => {
  const menuItems: { id: PageTab; label: string; icon: React.ReactNode }[] = [
    { id: 'dashboard', label: 'Executive Dashboard', icon: <LayoutDashboard className="w-5 h-5" /> },
    { id: 'assessment', label: 'Applicant Assessment', icon: <UserCheck className="w-5 h-5" /> },
    { id: 'model', label: 'Model Intelligence', icon: <Cpu className="w-5 h-5" /> },
    { id: 'reports', label: 'Reports & DB History', icon: <FileText className="w-5 h-5" /> },
  ];

  return (
    <aside className="w-64 bg-slate-900 border-r border-slate-800 flex flex-col justify-between shrink-0 min-h-screen font-sidebar">
      <div>
        {/* Brand Header */}
        <div className="p-6 border-b border-slate-800 flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-500 to-cyan-400 flex items-center justify-center shadow-lg shadow-indigo-500/20">
            <Activity className="w-6 h-6 text-white stroke-[2.5]" />
          </div>
          <div>
            <h1 className="text-xl font-extrabold tracking-tight text-white flex items-center gap-1 font-header">
              FIN<span className="text-indigo-400">Score</span>
            </h1>
            <p className="text-[10px] uppercase font-semibold text-slate-400 tracking-wider font-sidebar">
              Risk & Health Engine
            </p>
          </div>
        </div>

        {/* Navigation Menu */}
        <nav className="p-4 space-y-1">
          {menuItems.map((item) => {
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`w-full flex items-center gap-3.5 px-4 py-3 rounded-xl font-medium text-sm transition-all duration-200 ${isActive
                  ? 'bg-indigo-600/20 text-indigo-400 border border-indigo-500/30 shadow-sm shadow-indigo-500/10 font-semibold'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
                  }`}
              >
                <span className={isActive ? 'text-indigo-400' : 'text-slate-400'}>
                  {item.icon}
                </span>
                <span className="font-sidebar">{item.label}</span>
              </button>
            );
          })}
        </nav>
      </div>

      {/* Footer Info */}
      <div className="p-4 border-t border-slate-800 m-4 rounded-xl bg-slate-800/60 text-[11px] text-slate-400 space-y-1">
        <div className="font-semibold text-slate-300 font-sidebar">FINScore Platform </div>
        <div className="flex items-center gap-1.5 text-emerald-400 font-medium font-sidebar">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          FastAPI Backend Online
        </div>
        <div className="text-slate-400 text-[10px] pt-1 font-sidebar">XGBoost ROC-AUC: 85.51%</div>
      </div>
    </aside>
  );
};
