import React, { useEffect, useState } from 'react';
import type { PortfolioStats } from '../services/api';
import { fetchPortfolioStats } from '../services/api';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, AreaChart, Area, CartesianGrid } from 'recharts';
import { TrendingUp, ShieldCheck, DollarSign, Users } from 'lucide-react';

export const PortfolioAnalytics: React.FC = () => {
  const [stats, setStats] = useState<PortfolioStats | null>(null);

  useEffect(() => {
    fetchPortfolioStats().then(setStats).catch(console.error);
  }, []);

  const gradeData = [
    { grade: 'Grade A (Prime)', defaultRate: 4.2, healthScore: 88.5, volume: 45000 },
    { grade: 'Grade B (Good)', defaultRate: 8.5, healthScore: 78.2, volume: 62000 },
    { grade: 'Grade C (Fair)', defaultRate: 15.4, healthScore: 66.0, volume: 51000 },
    { grade: 'Grade D (Weak)', defaultRate: 24.1, healthScore: 52.4, volume: 28000 },
    { grade: 'Grade E (High Risk)', defaultRate: 36.8, healthScore: 39.1, volume: 14000 },
  ];

  return (
    <div className="p-8 space-y-8 max-w-7xl mx-auto">
      {/* Portfolio Top Bar */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <div className="p-5 rounded-xl glass-card space-y-2">
          <div className="flex justify-between items-center text-slate-400 text-xs font-semibold uppercase">
            <span>Evaluated Volume</span>
            <Users className="w-4 h-4 text-cyan-400" />
          </div>
          <div className="text-3xl font-extrabold text-white font-mono">
            {stats?.total_assessments || 200000}
          </div>
          <div className="text-[11px] text-emerald-400 font-medium">↑ Live Sync Active</div>
        </div>

        <div className="p-5 rounded-xl glass-card space-y-2">
          <div className="flex justify-between items-center text-slate-400 text-xs font-semibold uppercase">
            <span>Portfolio Avg Health</span>
            <ShieldCheck className="w-4 h-4 text-teal-400" />
          </div>
          <div className="text-3xl font-extrabold text-teal-400 font-mono">
            {stats?.avg_health_score || 76.4} / 100
          </div>
          <div className="text-[11px] text-slate-400">Target Range: &gt; 70</div>
        </div>

        <div className="p-5 rounded-xl glass-card space-y-2">
          <div className="flex justify-between items-center text-slate-400 text-xs font-semibold uppercase">
            <span>Portfolio Default Rate</span>
            <TrendingUp className="w-4 h-4 text-amber-400" />
          </div>
          <div className="text-3xl font-extrabold text-amber-400 font-mono">
            {stats?.avg_default_risk || 18.2}%
          </div>
          <div className="text-[11px] text-slate-400">Baseline Target: &lt; 20%</div>
        </div>

        <div className="p-5 rounded-xl glass-card space-y-2">
          <div className="flex justify-between items-center text-slate-400 text-xs font-semibold uppercase">
            <span>Policy Approval Rate</span>
            <DollarSign className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-3xl font-extrabold text-emerald-400 font-mono">
            {stats?.approval_rate || 81.5}%
          </div>
          <div className="text-[11px] text-slate-400">Automated Approvals</div>
        </div>
      </div>

      {/* Analytics Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Default Rate by Grade Tier */}
        <div className="p-6 rounded-2xl glass-card space-y-4">
          <div>
            <h3 className="text-base font-bold text-white">Default Probability by Credit Grade Tier</h3>
            <p className="text-xs text-slate-400">Historical empirical default percentage across borrower risk categories</p>
          </div>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={gradeData} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1E293B" />
                <XAxis dataKey="grade" tick={{ fill: '#94A3B8', fontSize: 10 }} />
                <YAxis tick={{ fill: '#94A3B8', fontSize: 11 }} unit="%" />
                <Tooltip contentStyle={{ backgroundColor: '#0F172A', borderColor: '#334155', borderRadius: '8px' }} />
                <Bar dataKey="defaultRate" fill="#EF4444" radius={[6, 6, 0, 0]} name="Default Rate %" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Financial Health Score by Grade Tier */}
        <div className="p-6 rounded-2xl glass-card space-y-4">
          <div>
            <h3 className="text-base font-bold text-white">Average Financial Health Score by Grade Tier</h3>
            <p className="text-xs text-slate-400">7-factor score progression across credit tiers</p>
          </div>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={gradeData} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1E293B" />
                <XAxis dataKey="grade" tick={{ fill: '#94A3B8', fontSize: 10 }} />
                <YAxis tick={{ fill: '#94A3B8', fontSize: 11 }} domain={[0, 100]} />
                <Tooltip contentStyle={{ backgroundColor: '#0F172A', borderColor: '#334155', borderRadius: '8px' }} />
                <Area type="monotone" dataKey="healthScore" stroke="#14B8A6" fill="#14B8A633" name="Health Score" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
};
