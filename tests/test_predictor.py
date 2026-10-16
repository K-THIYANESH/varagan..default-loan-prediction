"""
Unit tests for Credit Risk Predictor & Decision Policy Engine
"""

import pytest
from src.modeling.predictor import CreditRiskPredictor


def test_predictor_pipeline():
    predictor = CreditRiskPredictor()
    sample_input = {
        "annual_inc": 85000,
        "loan_amnt": 12000,
        "term": 36,
        "int_rate": 9.5,
        "installment": 384.0,
        "fico_score": 740,
        "dti": 14.0,
        "emp_length": 6,
        "revol_util": 22.0,
        "revol_bal": 6000,
        "tot_cur_bal": 120000,
        "total_rev_hi_lim": 30000,
        "avg_cur_bal": 15000,
        "open_acc": 8,
        "total_acc": 18,
        "mort_acc": 1,
        "delinq_2yrs": 0,
        "pub_rec": 0,
        "pub_rec_bankruptcies": 0,
        "credit_age": 11,
        "home_ownership": "MORTGAGE",
        "verification_status": "Source Verified",
        "purpose": "credit_card",
        "application_type": "Individual"
    }

    res = predictor.predict(sample_input)

    assert "financial_health_score" in res
    assert 0.0 <= res["default_probability_pct"] <= 100.0
    assert abs(res["default_probability_pct"] + res["approval_probability_pct"] - 100.0) < 0.1
    assert res["risk_band"] in ["LOW RISK", "MODERATE RISK", "HIGH RISK", "VERY HIGH RISK"]
    assert res["decision"] in ["RECOMMEND APPROVAL", "MANUAL REVIEW", "HIGH RISK / DECLINE"]
