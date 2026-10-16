import React from 'react';
import { ShieldCheck, Eye, Lock, FileCheck, CheckCircle2, Scale } from 'lucide-react';

export const ResponsibleAI: React.FC = () => {
  return (
    <div className="p-8 space-y-8 max-w-7xl mx-auto">
      {/* Header Banner */}
      <div className="p-6 rounded-2xl glass-card border-emerald-500/20 bg-gradient-to-r from-emerald-950/30 via-slate-900 to-teal-950/30 flex justify-between items-center">
        <div className="space-y-1">
          <div className="flex items-center gap-2 text-emerald-400 font-bold text-xs uppercase tracking-wider">
            <Scale className="w-4 h-4" />
            <span>Fair Lending Compliance & Governance</span>
          </div>
          <h2 className="text-2xl font-black text-white">Responsible AI Framework</h2>
          <p className="text-xs text-slate-300 max-w-2xl">
            Built from the ground up to comply with Equal Credit Opportunity Act (ECOA), Fair Credit Reporting Act (FCRA), and Model Risk Management guidelines (SR 11-7).
          </p>
        </div>

        <div className="hidden sm:flex items-center gap-2 px-4 py-2 rounded-xl bg-emerald-950/60 border border-emerald-500/30 text-emerald-300 font-semibold text-xs">
          <CheckCircle2 className="w-4 h-4 text-emerald-400" />
          <span>Audit Ready</span>
        </div>
      </div>

      {/* 4 Pillars Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Pillar 1 */}
        <div className="p-6 rounded-2xl glass-card space-y-3">
          <div className="w-10 h-10 rounded-xl bg-cyan-950 border border-cyan-500/30 flex items-center justify-center text-cyan-400">
            <Lock className="w-5 h-5" />
          </div>
          <h3 className="text-base font-bold text-white">1. Protected Class Non-Inclusion</h3>
          <p className="text-xs text-slate-300 leading-relaxed">
            The model explicitly excludes protected characteristics such as age, gender, race, religion, national origin, and marital status. Features are restricted to strictly objective financial attributes.
          </p>
        </div>

        {/* Pillar 2 */}
        <div className="p-6 rounded-2xl glass-card space-y-3">
          <div className="w-10 h-10 rounded-xl bg-teal-950 border border-teal-500/30 flex items-center justify-center text-teal-400">
            <Eye className="w-5 h-5" />
          </div>
          <h3 className="text-base font-bold text-white">2. Explainable Credit Decisions (XAI)</h3>
          <p className="text-xs text-slate-300 leading-relaxed">
            Every applicant assessment generates human-readable Adverse Action / Positive Driver explanations. Financial institutions can fulfill FCRA requirement for specific reason codes upon credit decline.
          </p>
        </div>

        {/* Pillar 3 */}
        <div className="p-6 rounded-2xl glass-card space-y-3">
          <div className="w-10 h-10 rounded-xl bg-emerald-950 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
            <FileCheck className="w-5 h-5" />
          </div>
          <h3 className="text-base font-bold text-white">3. Immutable Audit Trail</h3>
          <p className="text-xs text-slate-300 leading-relaxed">
            All assessment queries, model versions, and policy outcomes are persistently logged into an SQLite repository with timestamps and raw inputs for regulatory inspection.
          </p>
        </div>

        {/* Pillar 4 */}
        <div className="p-6 rounded-2xl glass-card space-y-3">
          <div className="w-10 h-10 rounded-xl bg-purple-950 border border-purple-500/30 flex items-center justify-center text-purple-400">
            <ShieldCheck className="w-5 h-5" />
          </div>
          <h3 className="text-base font-bold text-white">4. Continuous Model Monitoring</h3>
          <p className="text-xs text-slate-300 leading-relaxed">
            Automated monitoring for population stability index (PSI) and feature drift guarantees that credit risk scoring maintains accuracy over changing economic conditions.
          </p>
        </div>
      </div>
    </div>
  );
};
