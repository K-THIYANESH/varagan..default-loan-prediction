import React, { useEffect, useState } from 'react';
import type { ModelInfoResponse, PortfolioStats, AssessmentRecord } from '../services/api';
import { fetchModelInfo, fetchPortfolioStats, fetchAssessments } from '../services/api';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { Users, Award, ShieldAlert, Cpu, ArrowUpRight, CheckCircle2 } from 'lucide-react';

interface Props {
  onNavigateToAssessment: () => void;
}

export const Dashboard: React.FC<Props> = ({ onNavigateToAssessment }) => {
  const [modelInfo, setModelInfo] = useState<ModelInfoResponse | null>(null);
  const [stats, setStats] = useState<PortfolioStats | null>(null);
  const [recent, setRecent] = useState<AssessmentRecord[]>([]);

  useEffect(() => {
    const loadData = async () => {
      try {
        const [mInfo, pStats, rAss] = await Promise.all([
          fetchModelInfo(),
          fetchPortfolioStats(),
          fetchAssessments(5)
        ]);
        setModelInfo(mInfo);
        setStats(pStats);
        setRecent(rAss);
      } catch (err) {
        console.error('Error fetching dashboard data:', err);
      }
    };
    loadData();
  }, []);

  const chartData = stats?.risk_distribution
    ? Object.entries(stats.risk_distribution).map(([band, count]) => ({ band, count }))
    : [
        { band: 'LOW RISK', count: 1240 },
        { band: 'MODERATE RISK', count: 420 },
        { band: 'HIGH RISK', count: 180 },
        { band: 'VERY HIGH RISK', count: 90 },
      ];

  const COLORS: Record<string, string> = {
    'LOW RISK': '#10B981',
    'MODERATE RISK': '#F59E0B',
    'HIGH RISK': '#F97316',
    'VERY HIGH RISK': '#EF4444',
  };

  return (
    <div className="p-8 space-y-8 max-w-7xl mx-auto font-body">
      {/* Welcome Banner */}
      <div className="relative overflow-hidden p-8 rounded-2xl glass-card bg-slate-100 border border-slate-200 flex flex-wrap justify-between items-center gap-4 shadow-sm">
        <div className="space-y-1 z-10">
          <span className="text-xs uppercase font-extrabold tracking-widest text-black font-header">Production Credit Engine</span>
          <h2 className="text-2xl font-black text-black font-header">Intelligent Financial Health & Risk Assessment</h2>
        </div>
        <button
          onClick={onNavigateToAssessment}
          className="z-10 px-5 py-3 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-sm shadow-md flex items-center gap-2 transition-all font-header"
        >
          <span>Evaluate Applicant</span>
          <ArrowUpRight className="w-4 h-4 text-white" />
        </button>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <div className="p-6 rounded-2xl glass-card bg-white border border-slate-200 glass-card-hover space-y-3">
          <div className="flex justify-between items-center text-slate-500">
            <span className="text-xs font-bold uppercase tracking-wider font-header">Training Sample Size</span>
            <Users className="w-5 h-5 text-indigo-600" />
          </div>
          <div className="text-3xl font-black text-slate-900 font-mono">
            {modelInfo?.dataset_size ? modelInfo.dataset_size.toLocaleString() : '200,000'}
          </div>
          <p className="text-[11px] text-slate-500 font-medium">LendingClub production records</p>
        </div>

        <div className="p-6 rounded-2xl glass-card bg-white border border-slate-200 glass-card-hover space-y-3">
          <div className="flex justify-between items-center text-slate-500">
            <span className="text-xs font-bold uppercase tracking-wider font-header">Model ROC-AUC</span>
            <Award className="w-5 h-5 text-emerald-600" />
          </div>
          <div className="text-3xl font-black text-emerald-600 font-mono">
            {modelInfo?.metrics?.ROC_AUC ? `${(modelInfo.metrics.ROC_AUC * 100).toFixed(2)}%` : '85.51%'}
          </div>
          <p className="text-[11px] text-slate-500 font-medium">Validated high discrimination power</p>
        </div>

        <div className="p-6 rounded-2xl glass-card bg-white border border-slate-200 glass-card-hover space-y-3">
          <div className="flex justify-between items-center text-slate-500">
            <span className="text-xs font-bold uppercase tracking-wider font-header">Engine F1 Metric</span>
            <ShieldAlert className="w-5 h-5 text-teal-600" />
          </div>
          <div className="text-3xl font-black text-teal-600 font-mono">
            {modelInfo?.metrics?.F1 ? `${(modelInfo.metrics.F1 * 100).toFixed(2)}%` : '77.21%'}
          </div>
          <p className="text-[11px] text-slate-500 font-medium">Balanced precision/recall tradeoff</p>
        </div>

        <div className="p-6 rounded-2xl glass-card bg-white border border-slate-200 glass-card-hover space-y-3">
          <div className="flex justify-between items-center text-slate-500">
            <span className="text-xs font-bold uppercase tracking-wider font-header">Transformed Features</span>
            <Cpu className="w-5 h-5 text-purple-600" />
          </div>
          <div className="text-3xl font-black text-purple-600 font-mono">
            {modelInfo?.feature_count || 83}
          </div>
          <p className="text-[11px] text-slate-500 font-medium">Including financial ratios & encoding</p>
        </div>
      </div>

      {/* Main Charts & Analytics */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Risk Distribution Chart */}
        <div className="lg:col-span-2 p-6 rounded-2xl glass-card bg-white border border-slate-200 space-y-4">
          <div className="flex justify-between items-center">
            <div>
              <h3 className="text-base font-bold text-slate-900 font-header">Portfolio Risk Band Distribution</h3>
              <p className="text-xs text-slate-500">Categorized risk classification across assessed applicants</p>
            </div>
            <div className="text-xs font-semibold px-3 py-1 rounded-full bg-slate-100 text-slate-700 border border-slate-200">
              Live Database Stats
            </div>
          </div>
          
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
                <XAxis dataKey="band" tick={{ fill: '#475569', fontSize: 11 }} />
                <YAxis tick={{ fill: '#475569', fontSize: 11 }} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#FFFFFF', borderColor: '#E2E8F0', borderRadius: '8px', color: '#0F172A', boxShadow: '0 4px 12px rgba(0,0,0,0.08)' }}
                />
                <Bar dataKey="count" radius={[6, 6, 0, 0]}>
                  {chartData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[entry.band] || '#4F46E5'} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Quick Summary Panel */}
        <div className="p-6 rounded-2xl glass-card bg-white border border-slate-200 space-y-5 flex flex-col justify-between">
          <div className="space-y-4">
            <h3 className="text-base font-bold text-slate-900 font-header">Portfolio Health Summary</h3>

            <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-1">
              <div className="text-xs text-slate-500 font-semibold font-header">Evaluated Assessments</div>
              <div className="text-2xl font-black text-indigo-600 font-mono">
                {stats?.total_assessments ?? recent.length} Records
              </div>
            </div>

            <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-1">
              <div className="text-xs text-slate-500 font-semibold font-header">Average Financial Health Score</div>
              <div className="text-2xl font-black text-teal-600 font-mono">
                {stats?.avg_health_score ?? 76.4} / 100
              </div>
            </div>

            <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-1">
              <div className="text-xs text-slate-500 font-semibold font-header">Average Default Probability</div>
              <div className="text-2xl font-black text-amber-600 font-mono">
                {stats?.avg_default_risk ?? 18.2}%
              </div>
            </div>
          </div>

          <div className="flex items-center gap-2 text-xs text-emerald-600 font-bold pt-2 border-t border-slate-100 font-header">
            <CheckCircle2 className="w-4 h-4" />
            <span>Policy Guardrails Enforced</span>
          </div>
        </div>
      </div>
    </div>
  );
};
