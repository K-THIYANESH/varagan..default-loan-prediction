import streamlit as st
import pandas as pd
import numpy as np
import joblib
import tensorflow as tf
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# ===========================================
# PAGE CONFIG
# ===========================================

st.set_page_config(
    page_title="AI Loan Prediction System",
    page_icon="💰",
    layout="wide"
)

# ===========================================
# LOAD MODEL
# ===========================================

MODEL = tf.keras.models.load_model(
    "models/loan_model.keras"
)

SCALER = joblib.load(
    "models/scaler.pkl"
)

FEATURE_COLUMNS = joblib.load(
    "models/feature_columns.pkl"
)

# ===========================================
# TITLE
# ===========================================

st.title("🏦 AI Loan Approval Prediction")

st.markdown(
"""
Deep Learning based Loan Approval System

Predict whether a customer is likely to repay the loan using Artificial Intelligence.
"""
)

st.divider()

# ===========================================
# SIDEBAR
# ===========================================

st.sidebar.header("Loan Information")

loan_amnt = st.sidebar.number_input(
    "Loan Amount",
    1000,
    50000,
    15000
)

annual_inc = st.sidebar.number_input(
    "Annual Income",
    10000,
    500000,
    60000
)

int_rate = st.sidebar.slider(
    "Interest Rate",
    5.0,
    35.0,
    12.0
)

term = st.sidebar.selectbox(
    "Term",
    [36,60]
)

installment = st.sidebar.number_input(
    "Monthly Installment",
    50,
    3000,
    450
)

emp_length = st.sidebar.slider(
    "Employment Length",
    0,
    10,
    5
)

dti = st.sidebar.slider(
    "Debt To Income Ratio",
    0.0,
    40.0,
    15.0
)

fico_score = st.sidebar.slider(
    "FICO Score",
    500,
    850,
    700
)

revol_util = st.sidebar.slider(
    "Credit Utilization (%)",
    0.0,
    100.0,
    40.0
)

credit_age = st.sidebar.slider(
    "Credit History (Years)",
    1,
    40,
    10
)

loan_income_ratio = loan_amnt/(annual_inc+1)

emi_income_ratio = (installment*12)/(annual_inc+1)

available_credit_ratio = 0.40

financial_health_score = (
    (
        0.35*(fico_score/850)
        +
        0.20*(1-loan_income_ratio)
        +
        0.20*(1-emi_income_ratio)
        +
        0.15*(1-(revol_util/100))
        +
        0.10*(credit_age/40)
    )*100
)

predict_button = st.sidebar.button(
    "Predict Loan"
)

# ===========================================
# PREDICTION
# ===========================================

if predict_button:

    # ---------------------------------------
    # Create Input Dictionary
    # ---------------------------------------

    input_dict = {}

    # Initialize every feature with 0
    for col in FEATURE_COLUMNS:
        input_dict[col] = 0

    # ---------------------------------------
    # Numerical Features
    # ---------------------------------------

    numeric_values = {

        "loan_amnt": loan_amnt,
        "annual_inc": annual_inc,
        "int_rate": int_rate,
        "term": term,
        "installment": installment,
        "emp_length": emp_length,
        "dti": dti,
        "fico_score": fico_score,
        "revol_util": revol_util,
        "credit_age": credit_age,
        "loan_income_ratio": loan_income_ratio,
        "emi_income_ratio": emi_income_ratio,
        "available_credit_ratio": available_credit_ratio,
        "financial_health_score": financial_health_score

    }

    for key, value in numeric_values.items():

        if key in input_dict:
            input_dict[key] = value

    # ---------------------------------------
    # Convert to DataFrame
    # ---------------------------------------

    input_df = pd.DataFrame([input_dict])

    # Arrange columns exactly as training

    input_df = input_df[FEATURE_COLUMNS]

    # ---------------------------------------
    # Scale Input
    # ---------------------------------------

    scaled_input = SCALER.transform(input_df)

    # ---------------------------------------
    # Deep Learning Prediction
    # ---------------------------------------

    probability = MODEL.predict(
        scaled_input,
        verbose=0
    )[0][0]

    prediction = 1 if probability >= 0.5 else 0

    default_probability = probability * 100

    approval_probability = (1 - probability) * 100

    # ---------------------------------------
    # Risk Level
    # ---------------------------------------

    if default_probability < 20:

        risk = "🟢 LOW"

    elif default_probability < 40:

        risk = "🟡 MODERATE"

    elif default_probability < 60:

        risk = "🟠 HIGH"

    else:

        risk = "🔴 VERY HIGH"

    # ---------------------------------------
    # Result Box
    # ---------------------------------------

    st.divider()

    st.header("Prediction Result")

    col1, col2 = st.columns(2)

    with col1:

        if prediction == 0:

            st.success("✅ LOAN APPROVED")

        else:

            st.error("❌ LOAN REJECTED")

        st.metric(
            "Default Probability",
            f"{default_probability:.2f}%"
        )

        st.metric(
            "Approval Probability",
            f"{approval_probability:.2f}%"
        )

        st.metric(
            "Risk Level",
            risk
        )

        st.metric(
            "Financial Health Score",
            f"{financial_health_score:.2f}/100"
        )

    # ---------------------------------------
    # Gauge Chart
    # ---------------------------------------

    with col2:

        fig = go.Figure(

            go.Indicator(

                mode="gauge+number",

                value=default_probability,

                title={
                    "text":"Default Probability (%)"
                },

                gauge={

                    "axis":{"range":[0,100]},

                    "bar":{"color":"red"},

                    "steps":[

                        {"range":[0,20],"color":"lightgreen"},
                        {"range":[20,40],"color":"yellow"},
                        {"range":[40,60],"color":"orange"},
                        {"range":[60,100],"color":"red"}

                    ]

                }

            )

        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# =====================================================
# MODEL PERFORMANCE
# =====================================================

st.divider()

st.header("📊 Model Performance")

try:

    metrics = pd.read_csv("models/model_metrics.csv")

    st.dataframe(
        metrics,
        use_container_width=True
    )

except:

    st.warning("Model metrics not found.")

# =====================================================
# VISUALIZATIONS
# =====================================================

st.divider()

st.header("📈 Training Visualizations")

col1, col2 = st.columns(2)

with col1:

    try:

        st.image(
            "models/training_accuracy.png",
            caption="Training Accuracy"
        )

    except:

        st.info("Training Accuracy graph not found.")

with col2:

    try:

        st.image(
            "models/training_loss.png",
            caption="Training Loss"
        )

    except:

        st.info("Training Loss graph not found.")

# =====================================================
# CONFUSION MATRIX
# =====================================================

st.divider()

st.header("🧩 Confusion Matrix")

try:

    st.image(
        "models/confusion_matrix.png",
        use_container_width=True
    )

except:

    st.info("Confusion Matrix not found.")

# =====================================================
# SAMPLE PREDICTION DOWNLOAD
# =====================================================

st.divider()

st.header("⬇ Download Prediction")

if predict_button:

    result = pd.DataFrame({

        "Loan Amount":[loan_amnt],
        "Annual Income":[annual_inc],
        "Interest Rate":[int_rate],
        "FICO Score":[fico_score],
        "DTI":[dti],
        "Prediction":[
            "Approved"
            if prediction==0
            else
            "Rejected"
        ],
        "Default Probability":[
            round(default_probability,2)
        ],
        "Financial Health":[
            round(financial_health_score,2)
        ]

    })

    csv = result.to_csv(index=False)

    st.download_button(

        "📥 Download Result",

        data=csv,

        file_name="loan_prediction.csv",

        mime="text/csv"

    )

# =====================================================
# FEATURE IMPORTANCE (Approximation)
# =====================================================

st.divider()

st.header("📌 Important Factors")

importance = pd.DataFrame({

    "Feature":[

        "FICO Score",
        "Annual Income",
        "Loan Amount",
        "Debt To Income",
        "Interest Rate",
        "Employment Length",
        "Credit History"

    ],

    "Importance":[

        0.28,
        0.20,
        0.16,
        0.13,
        0.10,
        0.08,
        0.05

    ]

})

fig, ax = plt.subplots(figsize=(8,5))

ax.barh(

    importance["Feature"],

    importance["Importance"]

)

ax.set_xlabel("Relative Importance")

ax.set_title("Major Factors Affecting Prediction")

st.pyplot(fig)

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.markdown(
"""
---
### 💰 AI Loan Approval Prediction System

Built using

- TensorFlow / Keras
- Deep Learning
- Scikit-Learn
- Streamlit
- Plotly
- Pandas
- NumPy

Developed by **Dinesh Kumar V R**

This project predicts whether a loan applicant is likely to default using a Deep Neural Network trained on Lending Club loan data.
"""
)
# =====================================================
# MODEL PERFORMANCE
# =====================================================

st.divider()

st.header("📊 Model Performance")

try:

    metrics = pd.read_csv("models/model_metrics.csv")

    st.dataframe(
        metrics,
        use_container_width=True
    )

except:

    st.warning("Model metrics not found.")

# =====================================================
# VISUALIZATIONS
# =====================================================

st.divider()

st.header("📈 Training Visualizations")

col1, col2 = st.columns(2)

with col1:

    try:

        st.image(
            "models/training_accuracy.png",
            caption="Training Accuracy"
        )

    except:

        st.info("Training Accuracy graph not found.")

with col2:

    try:

        st.image(
            "models/training_loss.png",
            caption="Training Loss"
        )

    except:

        st.info("Training Loss graph not found.")

# =====================================================
# CONFUSION MATRIX
# =====================================================

st.divider()

st.header("🧩 Confusion Matrix")

try:

    st.image(
        "models/confusion_matrix.png",
        use_container_width=True
    )

except:

    st.info("Confusion Matrix not found.")

# =====================================================
# SAMPLE PREDICTION DOWNLOAD
# =====================================================

st.divider()

st.header("⬇ Download Prediction")

if predict_button:

    result = pd.DataFrame({

        "Loan Amount":[loan_amnt],
        "Annual Income":[annual_inc],
        "Interest Rate":[int_rate],
        "FICO Score":[fico_score],
        "DTI":[dti],
        "Prediction":[
            "Approved"
            if prediction==0
            else
            "Rejected"
        ],
        "Default Probability":[
            round(default_probability,2)
        ],
        "Financial Health":[
            round(financial_health_score,2)
        ]

    })

    csv = result.to_csv(index=False)

    st.download_button(

        "📥 Download Result",

        data=csv,

        file_name="loan_prediction.csv",

        mime="text/csv"

    )

# =====================================================
# FEATURE IMPORTANCE (Approximation)
# =====================================================

st.divider()

st.header("📌 Important Factors")

importance = pd.DataFrame({

    "Feature":[

        "FICO Score",
        "Annual Income",
        "Loan Amount",
        "Debt To Income",
        "Interest Rate",
        "Employment Length",
        "Credit History"

    ],

    "Importance":[

        0.28,
        0.20,
        0.16,
        0.13,
        0.10,
        0.08,
        0.05

    ]

})

fig, ax = plt.subplots(figsize=(8,5))

ax.barh(

    importance["Feature"],

    importance["Importance"]

)

ax.set_xlabel("Relative Importance")

ax.set_title("Major Factors Affecting Prediction")

st.pyplot(fig)

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.markdown(
"""
---
### 💰 AI Loan Approval Prediction System

Built using

- TensorFlow / Keras
- Deep Learning
- Scikit-Learn
- Streamlit
- Plotly
- Pandas
- NumPy

Developed by **Dinesh Kumar V R**

This project predicts whether a loan applicant is likely to default using a Deep Neural Network trained on Lending Club loan data.
"""
)
