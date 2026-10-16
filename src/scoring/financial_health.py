"""
Financial Health Scoring Engine
Calculates transparent 0-100 score and 7 financial dimensions.
"""

from typing import Dict, Any, Tuple


class FinancialHealthEngine:
    def __init__(self):
        # Weights for 7 key financial dimensions
        self.weights = {
            "credit_strength": 0.25,
            "debt_burden": 0.18,
            "credit_utilization": 0.15,
            "repayment_history": 0.15,
            "income_strength": 0.12,
            "loan_affordability": 0.10,
            "credit_history": 0.05,
        }

    def compute_scores(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Computes 7 sub-dimension scores (0-100) and weighted overall score.
        """
        # 1. Credit Strength (FICO: 300 to 850 range)
        fico = float(data.get("fico_score", 650))
        credit_strength = max(0.0, min(100.0, ((fico - 300) / (850 - 300)) * 100))

        # 2. Debt Burden (DTI: 0% to 50% benchmark)
        dti = float(data.get("dti", 20.0))
        debt_burden = max(0.0, min(100.0, (1 - (dti / 50.0)) * 100))

        # 3. Credit Utilization (revol_util: 0% to 100%)
        revol_util = float(data.get("revol_util", 30.0))
        credit_utilization = max(0.0, min(100.0, (1 - (revol_util / 100.0)) * 100))

        # 4. Repayment / Delinquency History
        delinq = float(data.get("delinq_2yrs", 0))
        pub_rec = float(data.get("pub_rec", 0))
        bankruptcies = float(data.get("pub_rec_bankruptcies", 0))
        
        delinq_penalty = delinq * 15.0 + pub_rec * 20.0 + bankruptcies * 30.0
        repayment_history = max(0.0, min(100.0, 100.0 - delinq_penalty))

        # 5. Income Strength (Annual Income benchmarked to $150k)
        annual_inc = float(data.get("annual_inc", 60000))
        income_strength = max(0.0, min(100.0, (annual_inc / 150000.0) * 100))

        # 6. Loan Affordability (EMI to Monthly Income ratio: benchmark 40%)
        installment = float(data.get("installment", 300))
        monthly_income = (annual_inc / 12.0) if annual_inc > 0 else 1.0
        emi_ratio = (installment / monthly_income) * 100
        loan_affordability = max(0.0, min(100.0, (1 - (emi_ratio / 40.0)) * 100))

        # 7. Credit History Depth (Credit age benchmarked to 25 years)
        credit_age = float(data.get("credit_age", 10))
        credit_history = max(0.0, min(100.0, (credit_age / 25.0) * 100))

        # Weighted Total Score
        total_score = (
            credit_strength * self.weights["credit_strength"] +
            debt_burden * self.weights["debt_burden"] +
            credit_utilization * self.weights["credit_utilization"] +
            repayment_history * self.weights["repayment_history"] +
            income_strength * self.weights["income_strength"] +
            loan_affordability * self.weights["loan_affordability"] +
            credit_history * self.weights["credit_history"]
        )

        final_score = round(max(0.0, min(100.0, total_score)), 1)
        category, color = self._get_category(final_score)

        return {
            "financial_health_score": final_score,
            "category": category,
            "color": color,
            "breakdown": {
                "Credit Strength": round(credit_strength, 1),
                "Debt Burden": round(debt_burden, 1),
                "Credit Utilization": round(credit_utilization, 1),
                "Repayment History": round(repayment_history, 1),
                "Income Strength": round(income_strength, 1),
                "Loan Affordability": round(loan_affordability, 1),
                "Credit History": round(credit_history, 1),
            }
        }

    def _get_category(self, score: float) -> Tuple[str, str]:
        if score >= 80.0:
            return "EXCELLENT", "#10B981"  # Emerald
        elif score >= 70.0:
            return "GOOD", "#3B82F6"       # Blue
        elif score >= 60.0:
            return "FAIR", "#F59E0B"       # Amber
        elif score >= 50.0:
            return "WEAK", "#EF4444"       # Red
        else:
            return "CRITICAL", "#991B1B"   # Dark Red
