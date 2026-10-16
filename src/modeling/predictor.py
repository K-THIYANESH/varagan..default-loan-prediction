"""
Predictor & Decision Support Engine for FINScore
Uses XGBoost model to output P(Default), Risk Bands, and Business Policy Recommendations.
"""

import os
import joblib
import yaml
import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple
from src.features.preprocessor import FeaturePreprocessor
from src.scoring.financial_health import FinancialHealthEngine


class CreditRiskPredictor:
    def __init__(
        self,
        model_path: str = "models/xgboost_model.pkl",
        threshold_path: str = "models/xgb_threshold.pkl",
        config_path: str = "config/settings.yaml",
    ):
        self.model_path = model_path
        self.model = None
        if os.path.exists(model_path):
            try:
                self.model = joblib.load(model_path)
            except Exception as e:
                print(f"Warning: Failed to load model from {model_path}: {e}")

        self.threshold = 0.43
        if os.path.exists(threshold_path):
            try:
                self.threshold = float(joblib.load(threshold_path))
            except Exception:
                pass

        self.preprocessor = FeaturePreprocessor()
        self.health_engine = FinancialHealthEngine()
        
        # Load config thresholds
        self.config = self._load_config(config_path)

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                return yaml.safe_load(f)
        return {
            "policy_thresholds": {
                "recommend_approval_max_risk": 25.0,
                "manual_review_max_risk": 45.0,
            }
        }

    def predict(self, raw_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes full pipeline:
        1. Financial Health Score (0-100)
        2. Feature preprocessor -> 83 features
        3. XGBoost prediction P(Default)
        4. Default Risk % & Approval Probability %
        5. Risk Band classification
        6. Decision Support Policy
        """
        # 1. Financial Health Score
        health_res = self.health_engine.compute_scores(raw_input)
        health_score = health_res["financial_health_score"]

        # 2. Feature Preprocessing
        df_features = self.preprocessor.transform(raw_input, health_score)

        # 3. Model Prediction
        if self.model is not None:
            y_prob = float(self.model.predict_proba(df_features)[0, 1])
        else:
            # Fallback empirical heuristic if model isn't available
            fico = float(raw_input.get("fico_score", 700))
            dti = float(raw_input.get("dti", 20.0))
            y_prob = max(0.05, min(0.95, 1.0 - (fico / 850.0) + (dti / 100.0) * 0.5))

        default_risk_pct = round(y_prob * 100.0, 1)
        approval_prob_pct = round(100.0 - default_risk_pct, 1)

        # 4. Risk Band Classification
        risk_band, risk_color = self._classify_risk_band(default_risk_pct)

        # 5. Decision Support Policy
        decision, decision_badge, decision_color = self._evaluate_policy(default_risk_pct)

        return {
            "financial_health_score": health_score,
            "financial_health_category": health_res["category"],
            "financial_health_color": health_res["color"],
            "health_breakdown": health_res["breakdown"],
            "default_probability_pct": default_risk_pct,
            "approval_probability_pct": approval_prob_pct,
            "risk_band": risk_band,
            "risk_color": risk_color,
            "decision": decision,
            "decision_badge": decision_badge,
            "decision_color": decision_color,
            "model_threshold": self.threshold,
            "df_features": df_features,
        }

    def _classify_risk_band(self, risk_pct: float) -> Tuple[str, str]:
        if risk_pct < 20.0:
            return "LOW RISK", "#10B981"       # Green
        elif risk_pct < 40.0:
            return "MODERATE RISK", "#3B82F6"  # Blue
        elif risk_pct < 60.0:
            return "HIGH RISK", "#F59E0B"      # Amber
        else:
            return "VERY HIGH RISK", "#EF4444"  # Red

    def _evaluate_policy(self, risk_pct: float) -> Tuple[str, str, str]:
        policy = self.config.get("policy_thresholds", {})
        app_max = policy.get("recommend_approval_max_risk", 25.0)
        man_max = policy.get("manual_review_max_risk", 45.0)

        if risk_pct <= app_max:
            return "RECOMMEND APPROVAL", "✓ RECOMMEND APPROVAL", "#10B981"
        elif risk_pct <= man_max:
            return "MANUAL REVIEW", "⚠ MANUAL REVIEW REQUIRED", "#F59E0B"
        else:
            return "HIGH RISK / DECLINE", "✕ HIGH RISK / DECLINE", "#EF4444"
