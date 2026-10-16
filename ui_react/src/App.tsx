import { useState } from 'react';
import { Sidebar, type PageTab } from './components/Sidebar';
import { Header } from './components/Header';
import { Dashboard } from './pages/Dashboard';
import { ApplicantAssessment } from './pages/ApplicantAssessment';
import { ModelIntelligence } from './pages/ModelIntelligence';
import { ReportsHistory } from './pages/ReportsHistory';

export function App() {
  const [activeTab, setActiveTab] = useState<PageTab>('dashboard');

  const pageMeta: Record<PageTab, { title: string; subtitle: string }> = {
    dashboard: {
      title: 'Executive Dashboard Overview',
      subtitle: 'Real-time performance metrics and credit portfolio risk monitoring',
    },
    assessment: {
      title: 'Applicant Financial & Risk Assessment',
      subtitle: '7-factor Financial Health engine & XGBoost default probability evaluation',
    },
    model: {
      title: 'Model Intelligence & Feature Attributions',
      subtitle: 'XGBoost ROC-AUC benchmarks and top financial feature importance',
    },
    reports: {
      title: 'Assessment History & Reports Audit DB',
      subtitle: 'Persistent SQLite database audit trail of applicant evaluations',
    },
  };

  const currentMeta = pageMeta[activeTab];

  return (
    <div className="flex min-h-screen bg-slate-50 text-slate-800 font-body antialiased">
      {/* Sidebar with unique font-sidebar */}
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0">
        <Header title={currentMeta.title} subtitle={currentMeta.subtitle} />

        <main className="flex-1 overflow-y-auto pb-12">
          {activeTab === 'dashboard' && (
            <Dashboard onNavigateToAssessment={() => setActiveTab('assessment')} />
          )}
          {activeTab === 'assessment' && <ApplicantAssessment />}
          {activeTab === 'model' && <ModelIntelligence />}
          {activeTab === 'reports' && <ReportsHistory />}
        </main>
      </div>
    </div>
  );
}

export default App;
