import pandas as pd

# ======================================================
# CONFIGURATION
# ======================================================

INPUT_FILE = "dataset/accepted_2007_to_2018Q4.csv"
OUTPUT_FILE = "dataset/loan_data.csv"

# ======================================================
# REQUIRED COLUMNS
# ======================================================

KEEP_COLUMNS = [
    # Target
    "loan_status",
    # Loan Details
    "loan_amnt",
    "term",
    "int_rate",
    "installment",
    "purpose",
    # Applicant Details
    "annual_inc",
    "emp_length",
    "home_ownership",
    "verification_status",
    # Credit Profile
    "dti",
    "fico_range_low",
    "fico_range_high",
    "earliest_cr_line",
    # Revolving Credit
    "revol_bal",
    "revol_util",
    # Accounts
    "open_acc",
    "total_acc",
    "mort_acc",
    "pub_rec",
    "delinq_2yrs",
    "inq_last_6mths",
    # Financial Capacity
    "tot_cur_bal",
    "avg_cur_bal",
    "total_rev_hi_lim",
    "tot_hi_cred_lim",
    # Additional Features
    "grade",
    "sub_grade",
    "application_type",
    "initial_list_status",
]

# ======================================================
# LOAD DATA
# ======================================================

print("=" * 60)
print("Loading dataset...")
print("=" * 60)

df = pd.read_csv(INPUT_FILE, low_memory=False, usecols=KEEP_COLUMNS)

print("Original Shape :", df.shape)

# ======================================================
# KEEP ONLY COMPLETED LOANS
# ======================================================

df = df[df["loan_status"].isin(["Fully Paid", "Charged Off"])]

print("After loan_status filtering :", df.shape)

# ======================================================
# CONVERT TARGET
# ======================================================

df["loan_status"] = df["loan_status"].map({"Fully Paid": 0, "Charged Off": 1})

# ======================================================
# REMOVE DUPLICATES
# ======================================================

df = df.drop_duplicates()

print("After removing duplicates :", df.shape)

# ======================================================
# BALANCED DATASET
# ======================================================

good = df[df["loan_status"] == 0]
bad = df[df["loan_status"] == 1]

print("\nClass Distribution Before Sampling")
print(df["loan_status"].value_counts())

# Sample 25k from each class

good = good.sample(n=25000, random_state=42)

bad = bad.sample(n=25000, random_state=42)

df = pd.concat([good, bad])

# Shuffle

df = df.sample(frac=1, random_state=42).reset_index(drop=True)

print("\nBalanced Dataset Shape :", df.shape)

print("\nClass Distribution After Sampling")
print(df["loan_status"].value_counts())

# ======================================================
# SAVE
# ======================================================

df.to_csv(OUTPUT_FILE, index=False)

print("\nDataset saved successfully!")

print("Saved to :", OUTPUT_FILE)
