# FINScore: Intelligent Financial Health & Credit Risk Assessment

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![XGBoost](https://img.shields.io/badge/Model-XGBoost%20v1.2-orange.svg)](https://xgboost.readthedocs.io/)
[![FastAPI](https://img.shields.io/badge/API-FastAPI-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/UI-React%2019%20%2B%20TypeScript-cyan.svg)](https://react.dev/)
[![TailwindCSS](https://img.shields.io/badge/Styling-TailwindCSS%20v4-teal.svg)](https://tailwindcss.com/)

**FINScore** is an enterprise-oriented fintech platform that transforms applicant financial data into transparent **Financial Health Metrics (0–100)**, **ML Default-Risk Probabilities (0–100%)**, and **Business Decision Support Policy Recommendations**.

---

## 🌟 Key Features

1. **Dual Intelligence Engine**:
   - **Financial Health Score (0–100)**: Deterministic score built across 7 core financial dimensions:
     - Debt Service Capacity (DTI)
     - Credit Score Standing (FICO)
     - Income-to-Loan Ratio
     - Revolving Line Utilization
     - Liquidity & Reserve Buffer
     - Credit History Depth
     - Clean Credit Track Record
   - **Default Risk Engine**: Predictive probability $P(\text{Default})$ powered by a validated **XGBoost Classifier** (trained on 200,000 credit records with 83 features).

2. **Decision Support Policy Layer**:
   - Business rules (`config/settings.yaml`) mapping risk probabilities to actionable decisions:
     - `RECOMMEND APPROVAL` ($\le 25\%$)
     - `MANUAL REVIEW` ($25.1\% - 45\%$)
     - `HIGH RISK / DECLINE` ($> 45\%$)

3. **Enterprise React UI (`ui_react/`)**:
   - Built with Vite 8, React 19, TypeScript, Tailwind CSS v4, Lucide Icons, and Recharts.
   - Dark navy glassmorphism theme, 1-click applicant demo presets (Prime, Moderate, High Risk), SVG gauges, and 6 full navigation views.

4. **Explainable AI (XAI)**:
   - Identifies top positive risk mitigants and negative risk drivers for every applicant.

5. **FastAPI REST API (`api.py`)**:
   - Production API with endpoints `/health`, `/score`, `/financial-health`, `/risk-assessment`, `/model-info`, `/feature-importance`, `/portfolio-stats`, and `/assessments`.

6. **SQLite Audit Persistence**:
   - SQLite database logging applicant records for historical audit trails.

---

## 📊 Model Performance Benchmarks

Evaluated independently on untouched test dataset:

| Metric | Score |
| :--- | :--- |
| **ROC-AUC** | **85.51%** |
| **F1 Score** | **77.21%** |
| **Recall** | **79.90%** |
| **Precision** | **74.69%** |
| **Accuracy** | **76.42%** |

---

## 📁 Code Architecture

```
ml/
├── api.py                      # FastAPI REST Backend Service (CORS enabled)
├── requirements.txt            # Python package dependencies
├── Dockerfile                  # Container build manifest
├── finscore.db                 # Persistent SQLite database
├── config/
│   └── settings.yaml           # Thresholds, weights & risk bands
├── dataset/
│   └── processed_loan_data_200k.csv  # 200K processed historical records
├── models/
│   ├── xgboost_model.pkl       # Trained XGBoost model binary
│   ├── xgb_feature_columns.pkl # Exact 83 feature columns
│   ├── xgb_threshold.pkl       # Optimal threshold (0.43)
│   ├── xgb_metrics.csv         # Model benchmark metrics
│   └── xgb_feature_importance.csv # Feature importance gain weights
├── src/
│   ├── scoring/
│   │   └── financial_health.py # 7-component financial health scoring engine
│   ├── features/
│   │   └── preprocessor.py     # 83-feature pipeline transformation
│   ├── modeling/
│   │   └── predictor.py        # Model inference & decision support
│   ├── explainability/
│   │   └── explainer.py        # Risk drivers & positive factors extractor
│   ├── database/
│   │   └── repository.py       # SQLite persistence (`finscore.db`)
│   └── utils/
│       └── pdf_generator.py    # ReportLab PDF generator
├── tests/
│   ├── test_scoring.py         # Financial health scoring tests
│   ├── test_predictor.py       # Predictor logic tests
│   └── test_api.py             # FastAPI endpoint integration tests
└── ui_react/                   # Vite + React 19 + TypeScript Frontend
    ├── src/
    │   ├── components/         # Gauges, Badges, Headers, Sidebar
    │   ├── pages/              # Dashboard, Assessment, Portfolio, Model, AI, Reports
    │   ├── services/           # Axios API client
    │   ├── App.tsx             # Root App component
    │   └── index.css           # Tailwind v4 glassmorphism styles
    ├── package.json
    ├── tailwind.config.js
    └── vite.config.ts
```

---

## 🛠️ Quick Start & Execution

### 1. Run Automated Python Test Suite

```bash
pytest
```

### 2. Launch FastAPI Backend Service

```bash
uvicorn api:app --reload --port 8050
```
*Interactive API docs available at: `http://localhost:8050/docs`*

### 3. Launch React Frontend Application

```bash
cd ui_react
npm install
npm run dev
```
*Access React Web UI at: `http://localhost:5174`*

---

## ⚖️ Responsible AI & Governance

*This application is built to comply with Fair Lending principles (ECOA/FCRA guidelines). Features exclude protected demographic classes (age, race, gender, marital status) to maintain objective credit scoring.*
