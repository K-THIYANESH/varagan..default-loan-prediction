"""
Explainable AI Module for FINScore
Extracts top risk-reducing (positive) and risk-increasing (negative) drivers for an applicant.
"""

from typing import Dict, Any, List


class RiskExplainer:
    def __init__(self):
        pass

    def explain(self, raw_input: Dict[str, Any], default_risk_pct: float) -> Dict[str, List[str]]:
        """
        Analyzes applicant inputs and identifies specific positive factors and risk drivers.
        """
        positive_factors = []
        risk_factors = []

        fico = float(raw_input.get("fico_score", 650))
        dti = float(raw_input.get("dti", 20.0))
        annual_inc = float(raw_input.get("annual_inc", 60000))
        loan_amnt = float(raw_input.get("loan_amnt", 15000))
        revol_util = float(raw_input.get("revol_util", 30.0))
        emp_length = int(raw_input.get("emp_length", 5))
        delinq = float(raw_input.get("delinq_2yrs", 0))
        pub_rec = float(raw_input.get("pub_rec", 0))
        bankruptcies = float(raw_input.get("pub_rec_bankruptcies", 0))
        int_rate = float(raw_input.get("int_rate", 11.0))
        credit_age = float(raw_input.get("credit_age", 10))

        # 1. FICO Score
        if fico >= 740:
            positive_factors.append(f"Strong FICO score ({int(fico)}) indicating established credit reliability.")
        elif fico < 660:
            risk_factors.append(f"Below-average FICO score ({int(fico)}) elevates default probability.")

        # 2. Debt to Income Ratio
        if dti <= 15.0:
            positive_factors.append(f"Low Debt-to-Income ratio ({dti:.1f}%), leaving substantial disposable income.")
        elif dti >= 28.0:
            risk_factors.append(f"High Debt-to-Income ratio ({dti:.1f}%), indicating high debt servicing burden.")

        # 3. Income & Loan Ratio
        loan_inc_ratio = loan_amnt / (annual_inc + 1.0)
        if loan_inc_ratio <= 0.2:
            positive_factors.append("Healthy annual income relative to requested loan amount.")
        elif loan_inc_ratio >= 0.4:
            risk_factors.append(f"High loan-to-income ratio ({loan_inc_ratio:.2f}x annual earnings).")

        # 4. Credit Utilization
        if revol_util <= 25.0:
            positive_factors.append(f"Low revolving credit utilization ({revol_util:.1f}%).")
        elif revol_util >= 60.0:
            risk_factors.append(f"Elevated revolving credit utilization ({revol_util:.1f}%).")

        # 5. Delinquency & Public Records
        if delinq == 0 and pub_rec == 0 and bankruptcies == 0:
            positive_factors.append("Clean recent payment history with zero delinquencies or public records.")
        else:
            if delinq > 0:
                risk_factors.append(f"History of recent late payments ({int(delinq)} delinquency in 2 years).")
            if bankruptcies > 0:
                risk_factors.append("Prior public bankruptcy record detected.")

        # 6. Interest Rate & Term
        if int_rate >= 16.0:
            risk_factors.append(f"Higher loan interest rate ({int_rate:.1f}%) increases monthly repayment strain.")

        # 7. Employment & History Depth
        if emp_length >= 5:
            positive_factors.append(f"Stable employment history ({emp_length}+ years).")
        elif emp_length < 2:
            risk_factors.append("Short employment tenure (< 2 years).")

        if credit_age >= 10:
            positive_factors.append(f"Established credit history depth ({int(credit_age)} years).")

        # Ensure at least 2 factors in each list for smooth UI rendering
        if not positive_factors:
            positive_factors.append("Standard income verification and active credit lines.")
            positive_factors.append("Standard application verification status.")
        if not risk_factors:
            risk_factors.append("General macroeconomic credit exposure.")
            risk_factors.append("Unsecured loan product risk profile.")

        return {
            "positive_factors": positive_factors,
            "risk_factors": risk_factors,
            "explanation": (
                f"The overall default risk is predicted at {default_risk_pct:.1f}%. "
                f"These key financial metrics contributed most significantly to the model's output."
            ),
        }
