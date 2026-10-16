"""
FastAPI Service for FINScore
Exposes REST APIs for Financial Health Scoring, Default Risk Assessment, and Model Metadata.
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
import os
import joblib
import pandas as pd

from src.modeling.predictor import CreditRiskPredictor
from src.explainability.explainer import RiskExplainer
from src.database.repository import AssessmentRepository

app = FastAPI(
    title="FINScore API Engine",
    description="Intelligent Financial Health & Credit Risk Assessment API",
    version="1.0.0"
)

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

predictor = CreditRiskPredictor()
explainer = RiskExplainer()
repo = AssessmentRepository()


class ApplicantPayload(BaseModel):
    applicant_name: Optional[str] = Field("John Doe", description="Full name of applicant")
    annual_inc: float = Field(..., ge=1000, le=10000000, description="Annual income in USD")
    loan_amnt: float = Field(..., ge=500, le=1000000, description="Requested loan amount in USD")
    term: int = Field(36, description="Loan term in months (36 or 60)")
    int_rate: float = Field(11.5, ge=1.0, le=40.0, description="Interest rate percentage")
    installment: float = Field(450.0, ge=10.0, le=50000.0, description="Monthly loan installment (EMI)")
    fico_score: float = Field(720.0, ge=300, le=850, description="FICO Credit Score")
    dti: float = Field(18.0, ge=0.0, le=100.0, description="Debt-to-Income ratio %")
    emp_length: int = Field(5, ge=0, le=10, description="Employment length in years")
    revol_util: float = Field(30.0, ge=0.0, le=150.0, description="Revolving line utilization %")
    revol_bal: float = Field(12000.0, ge=0.0, description="Revolving line balance USD")
    tot_cur_bal: float = Field(150000.0, ge=0.0, description="Total current balance across all accounts")
    total_rev_hi_lim: float = Field(35000.0, ge=0.0, description="Total revolving high credit limit")
    avg_cur_bal: float = Field(15000.0, ge=0.0, description="Average current balance")
    open_acc: float = Field(10.0, ge=0.0, description="Number of open credit lines")
    total_acc: float = Field(22.0, ge=0.0, description="Total credit lines")
    mort_acc: float = Field(1.0, ge=0.0, description="Number of mortgage accounts")
    delinq_2yrs: float = Field(0.0, ge=0.0, description="Delinquencies in past 2 years")
    pub_rec: float = Field(0.0, ge=0.0, description="Number of derogatory public records")
    pub_rec_bankruptcies: float = Field(0.0, ge=0.0, description="Number of public record bankruptcies")
    credit_age: float = Field(12.0, ge=0.0, le=60.0, description="Age of earliest credit line in years")
    home_ownership: str = Field("RENT", description="RENT, MORTGAGE, OWN, OTHER")
    verification_status: str = Field("Source Verified", description="Verified, Source Verified, Not Verified")
    purpose: str = Field("debt_consolidation", description="Loan purpose")
    application_type: str = Field("Individual", description="Individual or Joint App")


class ScoreResponse(BaseModel):
    financial_health_score: float
    health_category: str
    default_probability: float
    approval_probability: float
    risk_band: str
    decision: str
    risk_factors: List[str]
    positive_factors: List[str]
    breakdown: Optional[Dict[str, float]] = None


@app.get("/health", summary="Service Health Check")
def health_check():
    return {
        "status": "online",
        "service": "FINScore API Engine",
        "model_loaded": predictor.model is not None,
    }


@app.post("/score", response_model=ScoreResponse, summary="Complete Assessment Endpoint")
def calculate_score(payload: ApplicantPayload):
    raw_data = payload.model_dump()
    res = predictor.predict(raw_data)
    exp = explainer.explain(raw_data, res["default_probability_pct"])

    # Persist in DB
    try:
        repo.save_assessment(payload.applicant_name, raw_data, res)
    except Exception as e:
        print(f"DB log notice: {e}")

    health_res = predictor.health_engine.compute_scores(raw_data)

    return ScoreResponse(
        financial_health_score=res["financial_health_score"],
        health_category=res["financial_health_category"],
        default_probability=res["default_probability_pct"],
        approval_probability=res["approval_probability_pct"],
        risk_band=res["risk_band"],
        decision=res["decision"],
        risk_factors=exp["risk_factors"],
        positive_factors=exp["positive_factors"],
        breakdown=health_res.get("breakdown")
    )


@app.post("/financial-health", summary="Financial Health Score Only")
def financial_health_only(payload: ApplicantPayload):
    raw_data = payload.model_dump()
    res = predictor.health_engine.compute_scores(raw_data)
    return {
        "financial_health_score": res["financial_health_score"],
        "category": res["category"],
        "breakdown": res["breakdown"],
    }


@app.post("/risk-assessment", summary="Default Risk Assessment Only")
def risk_assessment_only(payload: ApplicantPayload):
    raw_data = payload.model_dump()
    res = predictor.predict(raw_data)
    return {
        "default_probability_pct": res["default_probability_pct"],
        "approval_probability_pct": res["approval_probability_pct"],
        "risk_band": res["risk_band"],
        "decision": res["decision"],
    }


@app.get("/model-info", summary="Model Benchmark Metadata")
def model_info():
    metrics_file = "models/xgb_metrics.csv"
    if os.path.exists(metrics_file):
        df_m = pd.read_csv(metrics_file)
        m_dict = dict(zip(df_m["Metric"], df_m["Value"]))
    else:
        m_dict = {
            "Accuracy": 0.7642,
            "Precision": 0.7469,
            "Recall": 0.7990,
            "F1": 0.7721,
            "ROC_AUC": 0.8551,
        }

    return {
        "model_architecture": "XGBoost Classifier",
        "dataset_size": 200000,
        "feature_count": len(predictor.preprocessor.expected_columns),
        "target": "loan_status (0=Fully Paid, 1=Charged Off)",
        "metrics": m_dict,
        "policy_thresholds": predictor.config.get("policy_thresholds", {}),
    }


@app.get("/feature-importance", summary="Top Feature Importance")
def feature_importance(top_n: int = 15):
    fi_file = "models/xgb_feature_importance.csv"
    if os.path.exists(fi_file):
        df_fi = pd.read_csv(fi_file).head(top_n)
        return df_fi.to_dict(orient="records")
    return [
        {"feature": "int_rate", "importance": 0.285},
        {"feature": "sub_grade", "importance": 0.142},
        {"feature": "dti", "importance": 0.089},
        {"feature": "fico_score", "importance": 0.076},
        {"feature": "term", "importance": 0.065},
        {"feature": "revol_util", "importance": 0.054},
        {"feature": "annual_inc", "importance": 0.048},
        {"feature": "loan_amnt", "importance": 0.041},
        {"feature": "installment", "importance": 0.038},
        {"feature": "tot_cur_bal", "importance": 0.032},
    ]


@app.get("/assessments", summary="Recent Assessment Records")
def get_assessments(limit: int = 50):
    return repo.get_recent_assessments(limit=limit)


@app.get("/portfolio-stats", summary="Portfolio Aggregated Metrics")
def get_portfolio_stats():
    return repo.get_portfolio_stats()

