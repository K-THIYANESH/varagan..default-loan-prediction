import React from 'react';

interface Props {
  score: number;
  category: string;
}

export const FinancialHealthGauge: React.FC<Props> = ({ score, category }) => {
  const normalizedScore = Math.min(Math.max(score, 0), 100);

  const getCategoryColor = (cat: string) => {
    switch (cat.toUpperCase()) {
      case 'EXCELLENT':
        return '#059669'; // Emerald
      case 'GOOD':
        return '#0D9488'; // Teal
      case 'FAIR':
        return '#D97706'; // Amber
      case 'WEAK':
        return '#EA580C'; // Orange
      case 'CRITICAL':
      default:
        return '#DC2626'; // Red
    }
  };

  const color = getCategoryColor(category);

  return (
    <div className="flex flex-col items-center justify-center p-4 relative font-body">
      <div className="w-56 h-36 relative flex justify-center items-end overflow-hidden pb-1">
        {/* SVG Arc Gauge */}
        <svg className="w-56 h-56 transform -rotate-90" viewBox="0 0 100 100">
          {/* Background Arc */}
          <path
            d="M 10,50 A 40,40 0 0,1 90,50"
            fill="none"
            stroke="#E2E8F0"
            strokeWidth="10"
            strokeLinecap="round"
          />
          {/* Gradient Arc Fill */}
          <path
            d="M 10,50 A 40,40 0 0,1 90,50"
            fill="none"
            stroke={color}
            strokeWidth="10"
            strokeDasharray="125.6"
            strokeDashoffset={125.6 - (normalizedScore / 100) * 125.6}
            strokeLinecap="round"
            className="transition-all duration-1000 ease-out"
          />
        </svg>

        {/* Center Score Display */}
        <div className="absolute bottom-4 z-10 flex flex-col items-center text-center">
          <span className="text-3xl font-black tracking-tight text-slate-900 font-header leading-none mb-1">
            {score.toFixed(1)}
          </span>
          <span className="text-[11px] font-bold uppercase tracking-wider px-2.5 py-0.5 rounded-full border font-header whitespace-nowrap shadow-sm"
            style={{ borderColor: color, color: color, backgroundColor: `${color}20` }}>
            {category}
          </span>
        </div>
      </div>
      <div className="flex justify-between w-48 text-[10px] text-slate-500 font-medium px-2 mt-2">
        <span>0 (Critical)</span>
        <span>50 (Fair)</span>
        <span>100 (Excellent)</span>
      </div>
    </div>
  );
};
