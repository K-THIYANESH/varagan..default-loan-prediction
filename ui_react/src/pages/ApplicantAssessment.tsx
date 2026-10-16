import React, { useState } from 'react';
import type { ApplicantInput, ScoreResponse } from '../services/api';
import { fetchScore } from '../services/api';
import { FinancialHealthGauge } from '../components/FinancialHealthGauge';
import { RiskGauge } from '../components/RiskGauge';
import { ExplainableFactors } from '../components/ExplainableFactors';
import { DecisionBadge } from '../components/DecisionBadge';
import { Play, Sparkles, RefreshCw, Upload, CheckCircle2, AlertTriangle, ShieldX, FileText } from 'lucide-react';

const INPUT_SAFE: ApplicantInput = {
  applicant_name: "Eleanor Vance (Safe / Low Risk)",
  annual_inc: 115000,
  loan_amnt: 12000,
  term: 36,
  int_rate: 6.8,
  installment: 369.5,
  fico_score: 790,
  dti: 10.5,
  emp_length: 10,
  revol_util: 14.2,
  revol_bal: 6200,
  tot_cur_bal: 245000,
  total_rev_hi_lim: 50000,
  avg_cur_bal: 28000,
  open_acc: 14,
  total_acc: 26,
  mort_acc: 2,
  delinq_2yrs: 0,
  pub_rec: 0,
  pub_rec_bankruptcies: 0,
  credit_age: 18,
  home_ownership: "MORTGAGE",
  verification_status: "Verified",
  purpose: "credit_card",
  application_type: "Individual"
};

const INPUT_MANUAL_REVIEW: ApplicantInput = {
  applicant_name: "Marcus Brody (Manual Review)",
  annual_inc: 62000,
  loan_amnt: 20000,
  term: 36,
  int_rate: 14.5,
  installment: 688.4,
  fico_score: 665,
  dti: 28.4,
  emp_length: 4,
  revol_util: 52.0,
  revol_bal: 16500,
  tot_cur_bal: 85000,
  total_rev_hi_lim: 32000,
  avg_cur_bal: 8500,
  open_acc: 9,
  total_acc: 16,
  mort_acc: 1,
  delinq_2yrs: 0,
  pub_rec: 0,
  pub_rec_bankruptcies: 0,
  credit_age: 7,
  home_ownership: "RENT",
  verification_status: "Source Verified",
  purpose: "debt_consolidation",
  application_type: "Individual"
};

const INPUT_BLOCKED: ApplicantInput = {
  applicant_name: "Victor Sterling (Blocked / High Risk)",
  annual_inc: 35000,
  loan_amnt: 30000,
  term: 60,
  int_rate: 24.9,
  installment: 878.2,
  fico_score: 570,
  dti: 45.2,
  emp_length: 1,
  revol_util: 92.5,
  revol_bal: 28500,
  tot_cur_bal: 38000,
  total_rev_hi_lim: 22000,
  avg_cur_bal: 3100,
  open_acc: 18,
  total_acc: 30,
  mort_acc: 0,
  delinq_2yrs: 3,
  pub_rec: 2,
  pub_rec_bankruptcies: 1,
  credit_age: 3,
  home_ownership: "RENT",
  verification_status: "Not Verified",
  purpose: "small_business",
  application_type: "Individual"
};

export const ApplicantAssessment: React.FC = () => {
  const [formData, setFormData] = useState<ApplicantInput>(INPUT_SAFE);
  const [result, setResult] = useState<ScoreResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [fileName, setFileName] = useState<string | null>(null);

  const handleChange = (field: keyof ApplicantInput, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleProfileSelect = (profile: ApplicantInput, profileName: string) => {
    setFormData(profile);
    setFileName(`input/${profileName}`);
  };

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setFileName(file.name);
    const reader = new FileReader();
    reader.onload = async (event) => {
      try {
        const text = event.target?.result as string;
        let data: Partial<ApplicantInput> = {};

        if (file.name.endsWith('.json')) {
          data = JSON.parse(text);
        } else if (file.name.endsWith('.csv')) {
          // Simple CSV line parser
          const lines = text.split('\n').map(l => l.trim()).filter(Boolean);
          if (lines.length >= 2) {
            const headers = lines[0].split(',').map(h => h.trim().replace(/^"|"$/g, ''));
            const values = lines[1].split(',').map(v => v.trim().replace(/^"|"$/g, ''));
            headers.forEach((h, i) => {
              const val = values[i];
              if (val !== undefined) {
                // @ts-ignore
                data[h] = isNaN(Number(val)) ? val : Number(val);
              }
            });
          }
        }

        const merged: ApplicantInput = { ...formData, ...data };
        setFormData(merged);

        // Auto trigger assessment after uploading file
        setLoading(true);
        setError(null);
        const res = await fetchScore(merged);
        setResult(res);
      } catch (err) {
        console.error('File parsing error:', err);
        setError('Error reading file. Please upload a valid JSON or CSV applicant data file.');
      } finally {
        setLoading(false);
      }
    };
    reader.readAsText(file);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const res = await fetchScore(formData);
      setResult(res);
    } catch (err: any) {
      console.error('Scoring error:', err);
      setError('Failed to connect to FINScore API server. Ensure backend is running at http://localhost:8050');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-8 space-y-8 max-w-7xl mx-auto font-body">
      {/* Input Presets & File Upload Bar */}
      <div className="p-6 rounded-2xl glass-card border border-slate-200 bg-white space-y-4">
        <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-100 pb-4">
          <div>
            <h3 className="text-base font-bold text-slate-900 font-header flex items-center gap-2">
              <FileText className="w-5 h-5 text-indigo-600" />
              <span>Input Folder & Profile Selection</span>
            </h3>
            <p className="text-xs text-slate-500">
              Select pre-configured profiles from the system input folder or upload custom applicant data files.
            </p>
          </div>

          {/* Direct Input Folder Profiles */}
          <div className="flex flex-wrap gap-2.5">
            <button
              type="button"
              onClick={() => handleProfileSelect(INPUT_SAFE, 'safe_applicant.json')}
              className="px-3.5 py-2 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-700 text-xs font-semibold hover:bg-emerald-100 transition-all flex items-center gap-2"
            >
              <CheckCircle2 className="w-4 h-4 text-emerald-600" />
              <span>Safe Applicant (Approval)</span>
            </button>

            <button
              type="button"
              onClick={() => handleProfileSelect(INPUT_MANUAL_REVIEW, 'manual_review_applicant.json')}
              className="px-3.5 py-2 rounded-xl bg-amber-50 border border-amber-200 text-amber-700 text-xs font-semibold hover:bg-amber-100 transition-all flex items-center gap-2"
            >
              <AlertTriangle className="w-4 h-4 text-amber-600" />
              <span>Manual Review Applicant</span>
            </button>

            <button
              type="button"
              onClick={() => handleProfileSelect(INPUT_BLOCKED, 'blocked_applicant.json')}
              className="px-3.5 py-2 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 text-xs font-semibold hover:bg-rose-100 transition-all flex items-center gap-2"
            >
              <ShieldX className="w-4 h-4 text-rose-600" />
              <span>Blocked Applicant (Decline)</span>
            </button>
          </div>
        </div>

        {/* File Upload Section */}
        <div className="flex flex-wrap items-center justify-between gap-4 pt-1">
          <div className="flex items-center gap-3">
            <label className="cursor-pointer px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-semibold shadow-sm flex items-center gap-2 transition-all">
              <Upload className="w-4 h-4" />
              <span>Upload Applicant File (.json / .csv)</span>
              <input
                type="file"
                accept=".json,.csv"
                onChange={handleFileUpload}
                className="hidden"
              />
            </label>
            {fileName && (
              <span className="text-xs font-mono px-3 py-1 rounded-lg bg-slate-100 text-slate-700 border border-slate-200">
                Loaded: {fileName}
              </span>
            )}
          </div>
          <span className="text-[11px] text-slate-400 italic">
            Supports JSON & CSV applicant records directly from the input directory.
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Form Column */}
        <div className="lg:col-span-5 space-y-6">
          <form onSubmit={handleSubmit} className="p-6 rounded-2xl glass-card bg-white border border-slate-200 space-y-6">
            <h3 className="text-base font-bold text-slate-900 border-b border-slate-100 pb-3 flex items-center justify-between font-header">
              <span>Applicant Data Entry</span>
              <span className="text-xs text-slate-500 font-normal">25 Parameters</span>
            </h3>

            {/* Applicant Name */}
            <div className="space-y-1">
              <label className="text-xs font-semibold text-slate-700">Applicant Full Name</label>
              <input
                type="text"
                value={formData.applicant_name}
                onChange={e => handleChange('applicant_name', e.target.value)}
                className="w-full px-3.5 py-2 rounded-xl bg-slate-50 border border-slate-300 text-slate-900 text-xs focus:outline-none focus:border-indigo-600 font-medium"
              />
            </div>

            {/* 1. Income & Loan */}
            <div className="space-y-3 pt-2">
              <span className="text-[11px] font-bold uppercase tracking-wider text-indigo-600 font-header">1. Core Loan Details</span>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-[11px] text-slate-600 font-medium">Annual Income ($)</label>
                  <input
                    type="number"
                    value={formData.annual_inc}
                    onChange={e => handleChange('annual_inc', parseFloat(e.target.value) || 0)}
                    className="w-full px-3 py-1.5 rounded-lg bg-slate-50 border border-slate-300 text-xs text-slate-900 font-semibold"
                  />
                </div>
                <div>
                  <label className="text-[11px] text-slate-600 font-medium">Requested Loan ($)</label>
                  <input
                    type="number"
                    value={formData.loan_amnt}
                    onChange={e => handleChange('loan_amnt', parseFloat(e.target.value) || 0)}
                    className="w-full px-3 py-1.5 rounded-lg bg-slate-50 border border-slate-300 text-xs text-slate-900 font-semibold"
                  />
                </div>
              </div>

              <div className="grid grid-cols-3 gap-3">
                <div>
                  <label className="text-[11px] text-slate-600 font-medium">Term (Mo)</label>
                  <select
                    value={formData.term}
                    onChange={e => handleChange('term', parseInt(e.target.value))}
                    className="w-full px-2.5 py-1.5 rounded-lg bg-slate-50 border border-slate-300 text-xs text-slate-900 font-medium"
                  >
                    <option value={36}>36 Months</option>
                    <option value={60}>60 Months</option>
                  </select>
                </div>
                <div>
                  <label className="text-[11px] text-slate-600 font-medium">Interest %</label>
                  <input
                    type="number"
                    step="0.1"
                    value={formData.int_rate}
                    onChange={e => handleChange('int_rate', parseFloat(e.target.value) || 0)}
                    className="w-full px-3 py-1.5 rounded-lg bg-slate-50 border border-slate-300 text-xs text-slate-900 font-semibold"
                  />
                </div>
                <div>
                  <label className="text-[11px] text-slate-600 font-medium">Installment ($)</label>
                  <input
                    type="number"
                    value={formData.installment}
                    onChange={e => handleChange('installment', parseFloat(e.target.value) || 0)}
                    className="w-full px-3 py-1.5 rounded-lg bg-slate-50 border border-slate-300 text-xs text-slate-900 font-semibold"
                  />
                </div>
              </div>
            </div>

            {/* 2. Credit Profile */}
            <div className="space-y-3 pt-2">
              <span className="text-[11px] font-bold uppercase tracking-wider text-teal-600 font-header">2. Credit Profile</span>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-[11px] text-slate-600 font-medium">FICO Score</label>
                  <input
                    type="number"
                    value={formData.fico_score}
                    onChange={e => handleChange('fico_score', parseFloat(e.target.value) || 0)}
                    className="w-full px-3 py-1.5 rounded-lg bg-slate-50 border border-slate-300 text-xs text-slate-900 font-semibold"
                  />
                </div>
                <div>
                  <label className="text-[11px] text-slate-600 font-medium">DTI Ratio (%)</label>
                  <input
                    type="number"
                    step="0.1"
                    value={formData.dti}
                    onChange={e => handleChange('dti', parseFloat(e.target.value) || 0)}
                    className="w-full px-3 py-1.5 rounded-lg bg-slate-50 border border-slate-300 text-xs text-slate-900 font-semibold"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-[11px] text-slate-600 font-medium">Revolving Util (%)</label>
                  <input
                    type="number"
                    step="0.1"
                    value={formData.revol_util}
                    onChange={e => handleChange('revol_util', parseFloat(e.target.value) || 0)}
                    className="w-full px-3 py-1.5 rounded-lg bg-slate-50 border border-slate-300 text-xs text-slate-900 font-semibold"
                  />
                </div>
                <div>
                  <label className="text-[11px] text-slate-600 font-medium">Credit Age (Yrs)</label>
                  <input
                    type="number"
                    value={formData.credit_age}
                    onChange={e => handleChange('credit_age', parseFloat(e.target.value) || 0)}
                    className="w-full px-3 py-1.5 rounded-lg bg-slate-50 border border-slate-300 text-xs text-slate-900 font-semibold"
                  />
                </div>
              </div>
            </div>

            {/* 3. Assets & Ratios */}
            <div className="space-y-3 pt-2">
              <span className="text-[11px] font-bold uppercase tracking-wider text-purple-600 font-header">3. Assets & Ratios</span>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-[11px] text-slate-600 font-medium">Total Current Bal ($)</label>
                  <input
                    type="number"
                    value={formData.tot_cur_bal}
                    onChange={e => handleChange('tot_cur_bal', parseFloat(e.target.value) || 0)}
                    className="w-full px-3 py-1.5 rounded-lg bg-slate-50 border border-slate-300 text-xs text-slate-900 font-semibold"
                  />
                </div>
                <div>
                  <label className="text-[11px] text-slate-600 font-medium">Revolving High Lim ($)</label>
                  <input
                    type="number"
                    value={formData.total_rev_hi_lim}
                    onChange={e => handleChange('total_rev_hi_lim', parseFloat(e.target.value) || 0)}
                    className="w-full px-3 py-1.5 rounded-lg bg-slate-50 border border-slate-300 text-xs text-slate-900 font-semibold"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-[11px] text-slate-600 font-medium">Home Ownership</label>
                  <select
                    value={formData.home_ownership}
                    onChange={e => handleChange('home_ownership', e.target.value)}
                    className="w-full px-2.5 py-1.5 rounded-lg bg-slate-50 border border-slate-300 text-xs text-slate-900 font-medium"
                  >
                    <option value="MORTGAGE">MORTGAGE</option>
                    <option value="RENT">RENT</option>
                    <option value="OWN">OWN</option>
                    <option value="OTHER">OTHER</option>
                  </select>
                </div>
                <div>
                  <label className="text-[11px] text-slate-600 font-medium">Verification Status</label>
                  <select
                    value={formData.verification_status}
                    onChange={e => handleChange('verification_status', e.target.value)}
                    className="w-full px-2.5 py-1.5 rounded-lg bg-slate-50 border border-slate-300 text-xs text-slate-900 font-medium"
                  >
                    <option value="Verified">Verified</option>
                    <option value="Source Verified">Source Verified</option>
                    <option value="Not Verified">Not Verified</option>
                  </select>
                </div>
              </div>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading}
              className="w-full py-3.5 rounded-xl bg-gradient-to-r from-indigo-600 to-indigo-700 hover:from-indigo-500 hover:to-indigo-600 text-white font-bold text-sm shadow-md shadow-indigo-500/20 flex items-center justify-center gap-2 transition-all disabled:opacity-50"
            >
              {loading ? (
                <>
                  <RefreshCw className="w-4 h-4 animate-spin" />
                  <span>Evaluating Risk Engine...</span>
                </>
              ) : (
                <>
                  <Play className="w-4 h-4 fill-current" />
                  <span>Run FINScore Assessment</span>
                </>
              )}
            </button>
          </form>
        </div>

        {/* Output Column */}
        <div className="lg:col-span-7 space-y-6">
          {error && (
            <div className="p-4 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 text-xs font-medium">
              {error}
            </div>
          )}

          {result ? (
            <div className="space-y-6">
              {/* Decision Badge */}
              <DecisionBadge decision={result.decision} />

              {/* Gauges Row */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Financial Health Gauge */}
                <div className="p-5 rounded-2xl glass-card bg-white border border-slate-200 flex flex-col justify-between items-center text-center">
                  <span className="text-xs font-bold uppercase tracking-wider text-slate-600 font-header">
                    Financial Health Score
                  </span>
                  <FinancialHealthGauge
                    score={result.financial_health_score}
                    category={result.health_category}
                  />
                </div>

                {/* Default Risk Gauge */}
                <div className="p-5 rounded-2xl glass-card bg-white border border-slate-200 flex flex-col justify-between items-center text-center">
                  <span className="text-xs font-bold uppercase tracking-wider text-slate-600 font-header">
                    Default Risk Assessment
                  </span>
                  <RiskGauge
                    defaultProb={result.default_probability}
                    approvalProb={result.approval_probability}
                    riskBand={result.risk_band}
                  />
                </div>
              </div>

              {/* Risk & Positive Factors */}
              <ExplainableFactors
                positiveFactors={result.positive_factors}
                riskFactors={result.risk_factors}
              />
            </div>
          ) : (
            <div className="p-12 rounded-2xl glass-card bg-white border-dashed border-slate-300 flex flex-col items-center justify-center text-center space-y-4 min-h-[480px]">
              <div className="w-16 h-16 rounded-2xl bg-indigo-50 flex items-center justify-center text-indigo-600">
                <Sparkles className="w-8 h-8 text-indigo-600" />
              </div>
              <div className="space-y-1 max-w-sm">
                <h4 className="text-base font-bold text-slate-900 font-header">Ready for Risk Evaluation</h4>
                <p className="text-xs text-slate-500">
                  Select an applicant profile above or input customized financial details, then click "Run FINScore Assessment".
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
