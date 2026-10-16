"""
SQLite Database Repository for FINScore
Stores applicant assessment records and generates portfolio statistics.
"""

import sqlite3
import datetime
from typing import Dict, Any, List


class AssessmentRepository:
    def __init__(self, db_path: str = "finscore.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS assessments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    applicant_name TEXT,
                    timestamp TEXT,
                    financial_health_score REAL,
                    financial_health_category TEXT,
                    default_probability REAL,
                    approval_probability REAL,
                    risk_band TEXT,
                    decision TEXT,
                    annual_inc REAL,
                    loan_amnt REAL,
                    fico_score REAL,
                    dti REAL
                )
            """)
            conn.commit()

    def save_assessment(self, applicant_name: str, raw_input: Dict[str, Any], result: Dict[str, Any]) -> int:
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO assessments (
                    applicant_name, timestamp, financial_health_score, financial_health_category,
                    default_probability, approval_probability, risk_band, decision,
                    annual_inc, loan_amnt, fico_score, dti
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                applicant_name or "Applicant",
                now_str,
                float(result.get("financial_health_score", 0)),
                str(result.get("financial_health_category", "")),
                float(result.get("default_probability_pct", 0)),
                float(result.get("approval_probability_pct", 0)),
                str(result.get("risk_band", "")),
                str(result.get("decision", "")),
                float(raw_input.get("annual_inc", 0)),
                float(raw_input.get("loan_amnt", 0)),
                float(raw_input.get("fico_score", 0)),
                float(raw_input.get("dti", 0)),
            ))
            conn.commit()
            return cursor.lastrowid

    def get_recent_assessments(self, limit: int = 50) -> List[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM assessments ORDER BY id DESC LIMIT ?", (limit,))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def get_portfolio_stats(self) -> Dict[str, Any]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*), AVG(financial_health_score), AVG(default_probability) FROM assessments")
            count, avg_health, avg_default = cursor.fetchone()
            
            if not count or count == 0:
                return {
                    "total_assessments": 0,
                    "avg_health_score": 0.0,
                    "avg_default_risk": 0.0,
                    "approval_rate": 0.0,
                    "risk_distribution": {"LOW RISK": 0, "MODERATE RISK": 0, "HIGH RISK": 0, "VERY HIGH RISK": 0}
                }

            cursor.execute("SELECT risk_band, COUNT(*) FROM assessments GROUP BY risk_band")
            risk_counts = dict(cursor.fetchall())

            cursor.execute("SELECT COUNT(*) FROM assessments WHERE decision LIKE '%APPROVAL%'")
            approved_count = cursor.fetchone()[0]

            return {
                "total_assessments": count,
                "avg_health_score": round(avg_health or 0.0, 1),
                "avg_default_risk": round(avg_default or 0.0, 1),
                "approval_rate": round((approved_count / count) * 100.0, 1),
                "risk_distribution": {
                    "LOW RISK": risk_counts.get("LOW RISK", 0),
                    "MODERATE RISK": risk_counts.get("MODERATE RISK", 0),
                    "HIGH RISK": risk_counts.get("HIGH RISK", 0),
                    "VERY HIGH RISK": risk_counts.get("VERY HIGH RISK", 0),
                }
            }
