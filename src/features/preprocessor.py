"""
Feature Preprocessor for FINScore
Converts raw user inputs into the exact 83 numerical features required by XGBoost.
"""

import os
import joblib
import pandas as pd
import numpy as np
from typing import Dict, Any, List


class FeaturePreprocessor:
    def __init__(self, feature_columns_path: str = "models/xgb_feature_columns.pkl"):
        if os.path.exists(feature_columns_path):
            self.expected_columns: List[str] = joblib.load(feature_columns_path)
        else:
            self.expected_columns = []

    def transform(self, input_data: Dict[str, Any], financial_health_score: float) -> pd.DataFrame:
        """
        Transforms raw dictionary into a single-row DataFrame aligned with self.expected_columns.
        """
        data = input_data.copy()

        # Extract base numerical fields with sensible defaults
        loan_amnt = float(data.get("loan_amnt", 15000))
        term = int(data.get("term", 36))
        int_rate = float(data.get("int_rate", 11.5))
        installment = float(data.get("installment", 495.0))
        emp_length = int(data.get("emp_length", 5))
        annual_inc = float(data.get("annual_inc", 75000))
        dti = float(data.get("dti", 18.0))
        delinq_2yrs = float(data.get("delinq_2yrs", 0))
        open_acc = float(data.get("open_acc", 10))
        pub_rec = float(data.get("pub_rec", 0))
        revol_bal = float(data.get("revol_bal", 12000))
        revol_util = float(data.get("revol_util", 35.0))
        total_acc = float(data.get("total_acc", 22))
        tot_cur_bal = float(data.get("tot_cur_bal", 150000))
        total_rev_hi_lim = float(data.get("total_rev_hi_lim", 35000))
        avg_cur_bal = float(data.get("avg_cur_bal", 15000))
        mort_acc = float(data.get("mort_acc", 1))
        pub_rec_bankruptcies = float(data.get("pub_rec_bankruptcies", 0))
        credit_age = float(data.get("credit_age", 12))
        fico_score = float(data.get("fico_score", 710))

        # Derived engineered features
        loan_income_ratio = loan_amnt / (annual_inc + 1.0)
        emi_income_ratio = (installment * 12.0) / (annual_inc + 1.0)
        available_credit_ratio = tot_cur_bal / (total_rev_hi_lim + 1.0)

        feature_dict = {
            "loan_amnt": loan_amnt,
            "term": term,
            "int_rate": int_rate,
            "installment": installment,
            "emp_length": emp_length,
            "annual_inc": annual_inc,
            "dti": dti,
            "delinq_2yrs": delinq_2yrs,
            "open_acc": open_acc,
            "pub_rec": pub_rec,
            "revol_bal": revol_bal,
            "revol_util": revol_util,
            "total_acc": total_acc,
            "tot_cur_bal": tot_cur_bal,
            "total_rev_hi_lim": total_rev_hi_lim,
            "avg_cur_bal": avg_cur_bal,
            "mort_acc": mort_acc,
            "pub_rec_bankruptcies": pub_rec_bankruptcies,
            "credit_age": credit_age,
            "fico_score": fico_score,
            "loan_income_ratio": loan_income_ratio,
            "emi_income_ratio": emi_income_ratio,
            "available_credit_ratio": available_credit_ratio,
            "financial_health_score": financial_health_score,
        }

        # Initialize all categorical dummy columns to 0
        df = pd.DataFrame([feature_dict])

        # Categoricals to encode
        grade = str(data.get("grade", "B")).upper()
        sub_grade = str(data.get("sub_grade", "B2")).upper()
        home_ownership = str(data.get("home_ownership", "RENT")).upper()
        verification_status = str(data.get("verification_status", "Source Verified"))
        purpose = str(data.get("purpose", "debt_consolidation")).lower()
        initial_list_status = str(data.get("initial_list_status", "w")).lower()
        application_type = str(data.get("application_type", "Individual"))

        # Map dummy variables
        dummy_mappings = {
            f"grade_{grade}": 1,
            f"sub_grade_{sub_grade}": 1,
            f"home_ownership_{home_ownership}": 1,
            f"verification_status_{verification_status}": 1,
            f"purpose_{purpose}": 1,
        }

        if initial_list_status == "w":
            dummy_mappings["initial_list_status_w"] = 1

        if application_type.lower() in ["joint app", "joint"]:
            dummy_mappings["application_type_Joint App"] = 1

        # Fill dummy columns into dataframe
        for col in self.expected_columns:
            if col not in df.columns:
                df[col] = dummy_mappings.get(col, 0)

        # Reorder df columns to match exact trained order
        df = df[self.expected_columns].astype("float32")
        return df
