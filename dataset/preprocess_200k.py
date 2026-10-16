import pandas as pd

INPUT_FILE = "dataset/accepted_2007_to_2018Q4.csv"
OUTPUT_FILE = "dataset/loan_data_200k.csv"

TARGET_PER_CLASS = 100000
CHUNK_SIZE = 100000

required_columns = [
    "loan_amnt",
    "term",
    "int_rate",
    "installment",
    "grade",
    "sub_grade",
    "emp_length",
    "home_ownership",
    "annual_inc",
    "verification_status",
    "purpose",
    "dti",
    "delinq_2yrs",
    "fico_range_low",
    "fico_range_high",
    "open_acc",
    "pub_rec",
    "revol_bal",
    "revol_util",
    "total_acc",
    "initial_list_status",
    "application_type",
    "mort_acc",
    "pub_rec_bankruptcies",
    "loan_status",
    "issue_d",
    "earliest_cr_line",
    "avg_cur_bal",
    "tot_cur_bal",
    "total_rev_hi_lim",
]

good_list = []
bad_list = []

good_count = 0
bad_count = 0

print("Reading dataset in chunks...\n")

for chunk in pd.read_csv(
    INPUT_FILE,
    usecols=required_columns,
    chunksize=CHUNK_SIZE,
    low_memory=False,
):
    chunk = chunk[chunk["loan_status"].isin(["Fully Paid", "Charged Off"])]

    chunk["loan_status"] = chunk["loan_status"].map({"Fully Paid": 0, "Charged Off": 1})

    good = chunk[chunk.loan_status == 0]
    bad = chunk[chunk.loan_status == 1]

    if good_count < TARGET_PER_CLASS:
        need = TARGET_PER_CLASS - good_count
        sample = good.sample(min(len(good), need), random_state=42)
        good_list.append(sample)
        good_count += len(sample)

    if bad_count < TARGET_PER_CLASS:
        need = TARGET_PER_CLASS - bad_count
        sample = bad.sample(min(len(bad), need), random_state=42)
        bad_list.append(sample)
        bad_count += len(sample)

    print(f"Good: {good_count}   Bad: {bad_count}")

    if good_count >= TARGET_PER_CLASS and bad_count >= TARGET_PER_CLASS:
        break

df = pd.concat(good_list + bad_list)

df = df.sample(frac=1, random_state=42).reset_index(drop=True)

print(df.shape)

df.to_csv(OUTPUT_FILE, index=False)

print("Saved:", OUTPUT_FILE)
