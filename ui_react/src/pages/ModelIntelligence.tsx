import React, { useEffect, useState } from 'react';
import type { ModelInfoResponse, FeatureImportanceItem } from '../services/api';
import { fetchModelInfo, fetchFeatureImportance } from '../services/api';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { Cpu, Zap, Layers, BarChart2 } from 'lucide-react';

export const ModelIntelligence: React.FC = () => {
  const [modelInfo, setModelInfo] = useState<ModelInfoResponse | null>(null);
  const [features, setFeatures] = useState<FeatureImportanceItem[]>([]);

  useEffect(() => {
    fetchModelInfo().then(setModelInfo).catch(console.error);
    fetchFeatureImportance().then(setFeatures).catch(console.error);
  }, []);

  const metricsList = modelInfo?.metrics
    ? [
        { name: 'ROC-AUC', value: `${(modelInfo.metrics.ROC_AUC * 100).toFixed(2)}%`, desc: 'Overall Discrimination Power' },
        { name: 'F1 Score', value: `${(modelInfo.metrics.F1 * 100).toFixed(2)}%`, desc: 'Harmonic Mean of Precision & Recall' },
        { name: 'Recall', value: `${(modelInfo.metrics.Recall * 100).toFixed(2)}%`, desc: 'Default Capture Sensitivity' },
        { name: 'Precision', value: `${(modelInfo.metrics.Precision * 100).toFixed(2)}%`, desc: 'Positive Prediction Accuracy' },
        { name: 'Accuracy', value: `${(modelInfo.metrics.Accuracy * 100).toFixed(2)}%`, desc: 'Overall Correct Predictions' },
      ]
    : [];

  return (
    <div className="p-8 space-y-8 max-w-7xl mx-auto font-body">
      {/* Overview Banner */}
      <div className="p-6 rounded-2xl glass-card bg-white border border-slate-200 flex flex-wrap justify-between items-center gap-4">
        <div className="space-y-1">
          <div className="flex items-center gap-2 text-indigo-600 font-bold text-xs uppercase tracking-wider font-header">
            <Cpu className="w-4 h-4" />
            <span>Machine Learning Architecture</span>
          </div>
          <h2 className="text-2xl font-black text-slate-900 font-header">XGBoost Credit Risk Classifier</h2>
          <p className="text-xs text-slate-500 max-w-2xl">
            Trained on 200,000 LendingClub loan applications with 83 feature columns including one-hot encodings & engineered financial ratios.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <div className="px-4 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-center">
            <div className="text-xs text-slate-500 font-semibold font-header">Dataset Records</div>
            <div className="text-lg font-black text-indigo-600 font-mono">200,000</div>
          </div>
          <div className="px-4 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-center">
            <div className="text-xs text-slate-500 font-semibold font-header">Total Features</div>
            <div className="text-lg font-black text-teal-600 font-mono">83</div>
          </div>
        </div>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-1 sm:grid-cols-3 lg:grid-cols-5 gap-4">
        {metricsList.map((m, idx) => (
          <div key={idx} className="p-5 rounded-2xl glass-card bg-white border border-slate-200 glass-card-hover space-y-1">
            <div className="text-[11px] font-bold text-slate-500 uppercase tracking-wider font-header">{m.name}</div>
            <div className="text-2xl font-black text-slate-900 font-mono">{m.value}</div>
            <div className="text-[10px] text-slate-500 font-medium">{m.desc}</div>
          </div>
        ))}
      </div>

      {/* Feature Importance Chart */}
      <div className="p-6 rounded-2xl glass-card bg-white border border-slate-200 space-y-4">
        <div className="flex justify-between items-center">
          <div>
            <h3 className="text-base font-bold text-slate-900 flex items-center gap-2 font-header">
              <BarChart2 className="w-5 h-5 text-indigo-600" />
              <span>Top Model Features by Importance (Gain Weight)</span>
            </h3>
            <p className="text-xs text-slate-500">Relative impact of key financial variables on the XGBoost prediction</p>
          </div>
        </div>

        <div className="h-72 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={features} layout="vertical" margin={{ top: 10, right: 30, left: 80, bottom: 5 }}>
              <XAxis type="number" tick={{ fill: '#475569', fontSize: 11 }} />
              <YAxis dataKey="feature" type="category" tick={{ fill: '#0F172A', fontSize: 11 }} width={110} />
              <Tooltip contentStyle={{ backgroundColor: '#FFFFFF', borderColor: '#E2E8F0', borderRadius: '8px', color: '#0F172A', boxShadow: '0 4px 12px rgba(0,0,0,0.08)' }} />
              <Bar dataKey="importance" fill="#4F46E5" radius={[0, 6, 6, 0]} name="Importance Gain">
                {features.map((_, index) => (
                  <Cell key={`cell-${index}`} fill={index < 3 ? '#0D9488' : '#4F46E5'} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Policy Thresholds Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="p-6 rounded-2xl glass-card bg-white border border-slate-200 space-y-4">
          <h3 className="text-base font-bold text-slate-900 flex items-center gap-2 font-header">
            <Zap className="w-5 h-5 text-amber-600" />
            <span>Configured Policy Thresholds</span>
          </h3>
          <div className="space-y-3 text-xs">
            <div className="flex justify-between p-3 rounded.xl bg-slate-50 border border-slate-200">
              <span className="text-slate-700 font-medium">Auto Approval Cutoff</span>
              <span className="font-mono text-emerald-600 font-bold">Default Risk &le; 25.0%</span>
            </div>
            <div className="flex justify-between p-3 rounded-xl bg-slate-50 border border-slate-200">
              <span className="text-slate-700 font-medium">Manual Review Band</span>
              <span className="font-mono text-amber-600 font-bold">25.0% &lt; Risk &le; 45.0%</span>
            </div>
            <div className="flex justify-between p-3 rounded-xl bg-slate-50 border border-slate-200">
              <span className="text-slate-700 font-medium">Auto Decline Threshold</span>
              <span className="font-mono text-rose-600 font-bold">Default Risk &gt; 45.0%</span>
            </div>
          </div>
        </div>

        <div className="p-6 rounded-2xl glass-card bg-white border border-slate-200 space-y-4">
          <h3 className="text-base font-bold text-slate-900 flex items-center gap-2 font-header">
            <Layers className="w-5 h-5 text-teal-600" />
            <span>Feature Pipeline Overview</span>
          </h3>
          <ul className="space-y-2.5 text-xs text-slate-700 font-body">
            <li className="flex items-start gap-2">
              <span className="text-teal-600 font-bold">•</span>
              <span><strong>Numerical Transformations:</strong> Median imputation, Robust scaling for high variance assets</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-teal-600 font-bold">•</span>
              <span><strong>Categorical Encodings:</strong> One-Hot Encoding for Grade, Sub-Grade, Home Ownership, Verification</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-teal-600 font-bold">•</span>
              <span><strong>Ratio Engineering:</strong> Monthly Debt Service Ratio, Revolving utilization safety buffers</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
};
