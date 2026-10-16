import React from 'react';

interface Props {
  breakdown?: Record<string, number>;
}

const DEFAULT_BREAKDOWN = {
  debt_service_score: 85,
  credit_score_health: 90,
  income_loan_ratio_score: 75,
  revolving_util_score: 80,
  liquidity_score: 70,
  credit_history_score: 88,
  delinquency_cleanliness_score: 100,
};

const LABELS: Record<string, string> = {
  debt_service_score: 'Debt Service Capacity (DTI)',
  credit_score_health: 'Credit Score Standing (FICO)',
  income_loan_ratio_score: 'Income-to-Loan Ratio',
  revolving_util_score: 'Revolving Line Utilization',
  liquidity_score: 'Liquidity & Buffer Reserve',
  credit_history_score: 'Credit History Age',
  delinquency_cleanliness_score: 'Clean Credit Track Record',
};

export const HealthBreakdown: React.FC<Props> = ({ breakdown }) => {
  const data = breakdown || DEFAULT_BREAKDOWN;

  const getBarColor = (score: number) => {
    if (score >= 80) return 'bg-emerald-500';
    if (score >= 65) return 'bg-teal-500';
    if (score >= 50) return 'bg-amber-500';
    if (score >= 35) return 'bg-orange-500';
    return 'bg-rose-500';
  };

  return (
    <div className="space-y-4 font-body">
      <h4 className="text-sm font-bold uppercase tracking-wider text-slate-800 font-header">
        7-Factor Health Dimension Analysis
      </h4>
      <div className="space-y-3">
        {Object.entries(data).map(([key, val]) => {
          const label = LABELS[key] || key.replace(/_/g, ' ');
          const score = typeof val === 'number' ? Math.min(Math.max(val, 0), 100) : 50;
          return (
            <div key={key} className="space-y-1">
              <div className="flex justify-between text-xs font-medium">
                <span className="text-slate-700 font-medium">{label}</span>
                <span className="text-slate-900 font-bold">{score.toFixed(0)}/100</span>
              </div>
              <div className="w-full bg-slate-100 h-2.5 rounded-full overflow-hidden border border-slate-200">
                <div
                  className={`h-full ${getBarColor(score)} transition-all duration-700 ease-out`}
                  style={{ width: `${score}%` }}
                />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
