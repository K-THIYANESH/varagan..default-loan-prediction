import React, { useEffect, useState } from 'react';
import type { AssessmentRecord } from '../services/api';
import { fetchAssessments } from '../services/api';
import { Database, Search, RefreshCw } from 'lucide-react';

export const ReportsHistory: React.FC = () => {
  const [assessments, setAssessments] = useState<AssessmentRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  const loadData = async () => {
    setLoading(true);
    try {
      const data = await fetchAssessments(100);
      setAssessments(data);
    } catch (err) {
      console.error('Error loading assessments:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const filtered = assessments.filter(a =>
    a.applicant_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    a.decision.toLowerCase().includes(searchTerm.toLowerCase()) ||
    a.risk_band.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const getDecisionBadge = (decision: string) => {
    if (decision.includes('APPROVAL')) {
      return <span className="px-2.5 py-0.5 rounded-full bg-emerald-100 border border-emerald-300 text-emerald-800 font-bold text-[11px]">{decision}</span>;
    }
    if (decision.includes('REVIEW')) {
      return <span className="px-2.5 py-0.5 rounded-full bg-amber-100 border border-amber-300 text-amber-800 font-bold text-[11px]">{decision}</span>;
    }
    return <span className="px-2.5 py-0.5 rounded-full bg-rose-100 border border-rose-300 text-rose-800 font-bold text-[11px]">{decision}</span>;
  };

  return (
    <div className="p-8 space-y-8 max-w-7xl mx-auto font-body">
      {/* Header Bar */}
      <div className="flex flex-wrap items-center justify-between gap-4 p-6 rounded-2xl glass-card bg-white border border-slate-200">
        <div className="space-y-1">
          <h2 className="text-xl font-black text-slate-900 flex items-center gap-2 font-header">
            <Database className="w-5 h-5 text-indigo-600" />
            <span>Assessment History & Audit Trail</span>
          </h2>
          <p className="text-xs text-slate-500">Persistent SQLite database records of evaluated applicants</p>
        </div>

        <div className="flex items-center gap-3">
          <div className="relative">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
            <input
              type="text"
              placeholder="Search applicant or decision..."
              value={searchTerm}
              onChange={e => setSearchTerm(e.target.value)}
              className="pl-9 pr-4 py-2 rounded-xl bg-slate-50 border border-slate-300 text-xs text-slate-900 focus:outline-none focus:border-indigo-600 w-64 font-medium"
            />
          </div>

          <button
            onClick={loadData}
            className="p-2.5 rounded-xl bg-slate-100 border border-slate-300 text-slate-700 hover:bg-slate-200 transition-all"
            title="Refresh DB"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
          </button>
        </div>
      </div>

      {/* Table */}
      <div className="rounded-2xl glass-card bg-white border border-slate-200 overflow-hidden shadow-xs">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-700">
            <thead className="bg-slate-50 text-slate-600 uppercase text-[10px] font-bold tracking-wider border-b border-slate-200 font-header">
              <tr>
                <th className="py-3.5 px-4">ID</th>
                <th className="py-3.5 px-4">Applicant</th>
                <th className="py-3.5 px-4">Timestamp</th>
                <th className="py-3.5 px-4">Health Score</th>
                <th className="py-3.5 px-4">Default Risk</th>
                <th className="py-3.5 px-4">Risk Band</th>
                <th className="py-3.5 px-4">Decision</th>
                <th className="py-3.5 px-4">Loan Amount</th>
                <th className="py-3.5 px-4">FICO</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 font-medium font-body">
              {filtered.length > 0 ? (
                filtered.map((row) => (
                  <tr key={row.id} className="hover:bg-slate-50 transition-all">
                    <td className="py-3 px-4 font-mono text-slate-500">#{row.id}</td>
                    <td className="py-3 px-4 text-slate-900 font-bold">{row.applicant_name}</td>
                    <td className="py-3 px-4 text-slate-500">{row.timestamp}</td>
                    <td className="py-3 px-4 font-bold text-teal-700">
                      {row.financial_health_score.toFixed(1)} <span className="text-[10px] text-slate-500 font-normal">({row.financial_health_category})</span>
                    </td>
                    <td className="py-3 px-4 font-bold text-amber-700">{row.default_probability.toFixed(1)}%</td>
                    <td className="py-3 px-4 text-slate-700">{row.risk_band}</td>
                    <td className="py-3 px-4">{getDecisionBadge(row.decision)}</td>
                    <td className="py-3 px-4 font-mono">${row.loan_amnt.toLocaleString()}</td>
                    <td className="py-3 px-4 font-mono">{row.fico_score}</td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={9} className="py-8 text-center text-slate-400 italic">
                    No assessment records found matching criteria.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
