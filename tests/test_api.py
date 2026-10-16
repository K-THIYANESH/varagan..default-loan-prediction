"""
Unit tests for FastAPI endpoints
"""

import pytest
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert "model_loaded" in data


def test_score_endpoint():
    payload = {
        "applicant_name": "Test User",
        "annual_inc": 75000,
        "loan_amnt": 10000,
        "term": 36,
        "int_rate": 10.5,
        "installment": 325.0,
        "fico_score": 710,
        "dti": 16.5,
        "emp_length": 4,
        "revol_util": 30.0,
        "revol_bal": 8000,
        "tot_cur_bal": 100000,
        "total_rev_hi_lim": 25000,
        "avg_cur_bal": 12000,
        "open_acc": 9,
        "total_acc": 16,
        "mort_acc": 1,
        "delinq_2yrs": 0,
        "pub_rec": 0,
        "pub_rec_bankruptcies": 0,
        "credit_age": 9,
        "home_ownership": "RENT",
        "verification_status": "Source Verified",
        "purpose": "debt_consolidation",
        "application_type": "Individual"
    }

    response = client.post("/score", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert "financial_health_score" in data
    assert "health_category" in data
    assert "default_probability" in data
    assert "approval_probability" in data
    assert "risk_band" in data
    assert "decision" in data
    assert isinstance(data["risk_factors"], list)
    assert isinstance(data["positive_factors"], list)


def test_model_info_endpoint():
    response = client.get("/model-info")
    assert response.status_code == 200
    data = response.json()
    assert data["model_architecture"] == "XGBoost Classifier"
    assert "metrics" in data
