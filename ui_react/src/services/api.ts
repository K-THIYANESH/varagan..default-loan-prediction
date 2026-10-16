import axios from 'axios';

const API_BASE_URL = 'http://localhost:8050';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface ApplicantInput {
  applicant_name: string;
  annual_inc: number;
  loan_amnt: number;
  term: number;
  int_rate: number;
  installment: number;
  fico_score: number;
  dti: number;
  emp_length: number;
  revol_util: number;
  revol_bal: number;
  tot_cur_bal: number;
  total_rev_hi_lim: number;
  avg_cur_bal: number;
  open_acc: number;
  total_acc: number;
  mort_acc: number;
  delinq_2yrs: number;
  pub_rec: number;
  pub_rec_bankruptcies: number;
  credit_age: number;
  home_ownership: string;
  verification_status: string;
  purpose: string;
  application_type: string;
}

export interface ScoreResponse {
  financial_health_score: number;
  health_category: string;
  default_probability: number;
  approval_probability: number;
  risk_band: string;
  decision: string;
  risk_factors: string[];
  positive_factors: string[];
  breakdown?: Record<string, number>;
}

export interface ModelInfoResponse {
  model_architecture: string;
  dataset_size: number;
  feature_count: number;
  target: string;
  metrics: {
    Accuracy: number;
    Precision: number;
    Recall: number;
    F1: number;
    ROC_AUC: number;
  };
  policy_thresholds: Record<string, any>;
}

export interface FeatureImportanceItem {
  feature: string;
  importance: number;
}

export interface AssessmentRecord {
  id: number;
  applicant_name: string;
  timestamp: string;
  financial_health_score: number;
  financial_health_category: string;
  default_probability: number;
  approval_probability: number;
  risk_band: string;
  decision: string;
  annual_inc: number;
  loan_amnt: number;
  fico_score: number;
  dti: number;
}

export interface PortfolioStats {
  total_assessments: number;
  avg_health_score: number;
  avg_default_risk: number;
  approval_rate: number;
  risk_distribution: Record<string, number>;
}

export const fetchHealth = async () => {
  const res = await api.get('/health');
  return res.data;
};

export const fetchScore = async (data: ApplicantInput): Promise<ScoreResponse> => {
  const res = await api.post('/score', data);
  return res.data;
};

export const fetchModelInfo = async (): Promise<ModelInfoResponse> => {
  const res = await api.get('/model-info');
  return res.data;
};

export const fetchFeatureImportance = async (): Promise<FeatureImportanceItem[]> => {
  const res = await api.get('/feature-importance');
  return res.data;
};

export const fetchAssessments = async (limit: number = 50): Promise<AssessmentRecord[]> => {
  const res = await api.get(`/assessments?limit=${limit}`);
  return res.data;
};

export const fetchPortfolioStats = async (): Promise<PortfolioStats> => {
  const res = await api.get('/portfolio-stats');
  return res.data;
};
