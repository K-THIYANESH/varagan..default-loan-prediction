"""
Unit tests for Financial Health Scoring Engine
"""

import pytest
from src.scoring.financial_health import FinancialHealthEngine


def test_financial_health_bounds():
    engine = FinancialHealthEngine()
    
    # Excellent profile
    prime_input = {
        "fico_score": 820,
        "dti": 10.0,
        "revol_util": 15.0,
        "delinq_2yrs": 0,
        "pub_rec": 0,
        "pub_rec_bankruptcies": 0,
        "annual_inc": 150000,
        "installment": 300,
        "credit_age": 20
    }
    res_prime = engine.compute_scores(prime_input)
    assert 0.0 <= res_prime["financial_health_score"] <= 100.0
    assert res_prime["category"] in ["EXCELLENT", "GOOD"]
    assert len(res_prime["breakdown"]) == 7

    # Critical profile
    poor_input = {
        "fico_score": 450,
        "dti": 48.0,
        "revol_util": 95.0,
        "delinq_2yrs": 4,
        "pub_rec": 2,
        "pub_rec_bankruptcies": 1,
        "annual_inc": 20000,
        "installment": 1200,
        "credit_age": 1
    }
    res_poor = engine.compute_scores(poor_input)
    assert 0.0 <= res_poor["financial_health_score"] <= 100.0
    assert res_poor["category"] in ["WEAK", "CRITICAL"]
    assert res_prime["financial_health_score"] > res_poor["financial_health_score"]
