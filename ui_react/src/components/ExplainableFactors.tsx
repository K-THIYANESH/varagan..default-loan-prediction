import React from 'react';
import { CheckCircle2, AlertTriangle } from 'lucide-react';

interface Props {
  positiveFactors: string[];
  riskFactors: string[];
}

export const ExplainableFactors: React.FC<Props> = ({ positiveFactors, riskFactors }) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {/* Positive Factors */}
      <div className="p-5 rounded-2xl glass-card border-emerald-200 bg-emerald-50/50">
        <div className="flex items-center gap-2 mb-3 text-emerald-700 font-bold text-xs uppercase tracking-wider font-header">
          <CheckCircle2 className="w-5 h-5 text-emerald-600" />
          <span>Positive Health Drivers</span>
        </div>
        <ul className="space-y-2 text-xs text-slate-700 font-body">
          {positiveFactors && positiveFactors.length > 0 ? (
            positiveFactors.map((factor, idx) => (
              <li key={idx} className="flex items-start gap-2">
                <span className="text-emerald-600 font-bold">•</span>
                <span>{factor}</span>
              </li>
            ))
          ) : (
            <li className="text-slate-500 italic">No significant positive drivers identified.</li>
          )}
        </ul>
      </div>

      {/* Risk Factors */}
      <div className="p-5 rounded-2xl glass-card border-rose-200 bg-rose-50/50">
        <div className="flex items-center gap-2 mb-3 text-rose-700 font-bold text-xs uppercase tracking-wider font-header">
          <AlertTriangle className="w-5 h-5 text-rose-600" />
          <span>Key Risk Drivers</span>
        </div>
        <ul className="space-y-2 text-xs text-slate-700 font-body">
          {riskFactors && riskFactors.length > 0 ? (
            riskFactors.map((factor, idx) => (
              <li key={idx} className="flex items-start gap-2">
                <span className="text-rose-600 font-bold">•</span>
                <span>{factor}</span>
              </li>
            ))
          ) : (
            <li className="text-slate-500 italic">No critical risk drivers identified.</li>
          )}
        </ul>
      </div>
    </div>
  );
};
