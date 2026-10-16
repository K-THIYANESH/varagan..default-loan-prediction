import pandas as pd
import numpy as np

# ======================================================
# CONFIG
# ======================================================

INPUT_FILE = "dataset/loan_data_200k.csv"
OUTPUT_FILE = "dataset/processed_loan_data_200k.csv"

CURRENT_YEAR = 2026

print("=" * 60)
print("Feature Engineering Started")
print("=" * 60)

# ======================================================
# LOAD DATA
# ======================================================

df = pd.read_csv(INPUT_FILE)

print("Original Shape :", df.shape)

# ======================================================
# HANDLE MISSING VALUES
# ======================================================

numeric_cols = df.select_dtypes(include=np.number).columns

for col in numeric_cols:
    df[col] = df[col].fillna(df[col].median())

categorical_cols = df.select_dtypes(include="object").columns

for col in categorical_cols:
    df[col] = df[col].fillna(df[col].mode()[0])

# ======================================================
# CLEAN TERM
# ======================================================

if "term" in df.columns:
    df["term"] = df["term"].str.replace(" months", "", regex=False).astype("int16")

# ======================================================
# CLEAN EMPLOYMENT LENGTH
# ======================================================

EMP_MAP = {
    "< 1 year": 0,
    "1 year": 1,
    "2 years": 2,
    "3 years": 3,
    "4 years": 4,
    "5 years": 5,
    "6 years": 6,
    "7 years": 7,
    "8 years": 8,
    "9 years": 9,
    "10+ years": 10,
}

df["emp_length"] = df["emp_length"].map(EMP_MAP).fillna(0).astype("int8")

# ======================================================
# CLEAN INTEREST RATE
# ======================================================

df["int_rate"] = df["int_rate"].astype(str).str.replace("%", "", regex=False)

df["int_rate"] = pd.to_numeric(df["int_rate"], errors="coerce")

df["int_rate"] = df["int_rate"].fillna(df["int_rate"].median())

# ======================================================
# CLEAN REVOL UTIL
# ======================================================

df["revol_util"] = df["revol_util"].astype(str).str.replace("%", "", regex=False)

df["revol_util"] = pd.to_numeric(df["revol_util"], errors="coerce")

df["revol_util"] = df["revol_util"].fillna(df["revol_util"].median())

# ======================================================
# CREDIT AGE
# ======================================================

df["earliest_cr_line"] = pd.to_datetime(
    df["earliest_cr_line"], format="%b-%Y", errors="coerce"
)

df["credit_age"] = CURRENT_YEAR - df["earliest_cr_line"].dt.year

df["credit_age"] = df["credit_age"].fillna(df["credit_age"].median())

# ======================================================
# FICO SCORE
# ======================================================

df["fico_score"] = (df["fico_range_low"] + df["fico_range_high"]) / 2

# ======================================================
# LOAN TO INCOME RATIO
# ======================================================

df["loan_income_ratio"] = df["loan_amnt"] / (df["annual_inc"] + 1)

# ======================================================
# EMI TO INCOME RATIO
# ======================================================

df["emi_income_ratio"] = (df["installment"] * 12) / (df["annual_inc"] + 1)

# ======================================================
# AVAILABLE CREDIT RATIO
# ======================================================

if "tot_hi_cred_lim" in df.columns:
    credit_limit = df["tot_hi_cred_lim"]

elif "total_rev_hi_lim" in df.columns:
    credit_limit = df["total_rev_hi_lim"]

else:
    credit_limit = df["tot_cur_bal"]

df["available_credit_ratio"] = df["tot_cur_bal"] / (credit_limit + 1)

# ======================================================
# FINANCIAL HEALTH SCORE
# ======================================================

health = (
    0.35 * (df["fico_score"] / 850)
    + 0.20 * (1 - df["loan_income_ratio"])
    + 0.20 * (1 - df["emi_income_ratio"])
    + 0.15 * (1 - (df["revol_util"] / 100))
    + 0.10 * (df["credit_age"] / 40)
)

health = health.clip(0, 1)

df["financial_health_score"] = (health * 100).round(2)

# ======================================================
# DROP REDUNDANT FEATURES
# ======================================================

df.drop(
    columns=["fico_range_low", "fico_range_high", "earliest_cr_line", "issue_d"],
    inplace=True,
    errors="ignore",
)

# ======================================================
# ONE HOT ENCODING
# ======================================================

categorical_cols = df.select_dtypes(include="object").columns

print("\nEncoding Categorical Columns...")

df = pd.get_dummies(df, columns=categorical_cols, drop_first=True, dtype="uint8")

# ======================================================
# MEMORY OPTIMIZATION
# ======================================================

print("Optimizing Memory...")

for col in df.columns:
    if df[col].dtype == "float64":
        df[col] = df[col].astype("float32")

    elif df[col].dtype == "int64":
        df[col] = df[col].astype("int32")

# ======================================================
# SAVE
# ======================================================

df.to_csv(OUTPUT_FILE, index=False)

print("=" * 60)
print("Feature Engineering Completed")
print("=" * 60)

print("Final Shape :", df.shape)

print("\nNew Features Added")

features = [
    "credit_age",
    "fico_score",
    "loan_income_ratio",
    "emi_income_ratio",
    "available_credit_ratio",
    "financial_health_score",
]

for feature in features:
    print("✓", feature)

print("\nDataset Saved Successfully")
print("Location :", OUTPUT_FILE)

print("\nDone!")
