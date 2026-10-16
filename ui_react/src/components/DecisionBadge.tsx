import React from 'react';
import { ShieldCheck, ShieldAlert, AlertOctagon } from 'lucide-react';

interface Props {
  decision: string;
}

export const DecisionBadge: React.FC<Props> = ({ decision }) => {
  const isApproved = decision.includes('APPROVAL');
  const isReview = decision.includes('REVIEW');

  let icon = <ShieldCheck className="w-8 h-8 text-emerald-600" />;
  let bgColor = 'bg-emerald-50 border-emerald-200 text-emerald-900';

  if (isReview) {
    icon = <ShieldAlert className="w-8 h-8 text-amber-600" />;
    bgColor = 'bg-amber-50 border-amber-200 text-amber-900';
  } else if (!isApproved) {
    icon = <AlertOctagon className="w-8 h-8 text-rose-600" />;
    bgColor = 'bg-rose-50 border-rose-200 text-rose-900';
  }

  return (
    <div className={`p-5 rounded-2xl border ${bgColor} flex items-center justify-between shadow-xs`}>
      <div className="flex items-center gap-4">
        {icon}
        <div>
          <div className="text-xs uppercase tracking-widest font-semibold opacity-75 font-header">
            Credit Risk Policy Engine
          </div>
          <div className="text-xl font-black tracking-tight mt-0.5 font-header">
            {decision}
          </div>
        </div>
      </div>
      <div className="hidden sm:block text-right text-xs opacity-80 font-body">
        Engine Version: <span className="font-mono font-semibold">v1.2-xgb</span><br />
        Policy Threshold: <span className="font-mono font-semibold">Configured</span>
      </div>
    </div>
  );
};
