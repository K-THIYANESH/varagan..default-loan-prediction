# ============================================================
# LOAN DEFAULT PREDICTION USING DEEP LEARNING
# PART 1 - IMPORTS, DATA LOADING & PREPROCESSING
# ============================================================

import os
import warnings
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)

import tensorflow as tf

from tensorflow.keras.models import Sequential, load_model

from tensorflow.keras.layers import (
    Dense,
    Dropout,
    BatchNormalization,
    Input
)

from tensorflow.keras.optimizers import Adam

from tensorflow.keras.callbacks import (
    EarlyStopping,
    ModelCheckpoint,
    ReduceLROnPlateau,
    TensorBoard
)

warnings.filterwarnings("ignore")

# ============================================================
# RANDOM SEED
# ============================================================

SEED = 42

np.random.seed(SEED)

tf.random.set_seed(SEED)

# ============================================================
# CONFIGURATION
# ============================================================

DATA_PATH = "dataset/processed_loan_data_200k.csv"

MODEL_DIR = "models"

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "loan_model.keras"
)

SCALER_PATH = os.path.join(
    MODEL_DIR,
    "scaler.pkl"
)

FEATURE_PATH = os.path.join(
    MODEL_DIR,
    "feature_columns.pkl"
)

HISTORY_PATH = os.path.join(
    MODEL_DIR,
    "history.csv"
)

os.makedirs(
    MODEL_DIR,
    exist_ok=True
)

# ============================================================
# LOAD DATASET
# ============================================================

print("=" * 70)
print("Loading Processed Dataset")
print("=" * 70)

df = pd.read_csv(DATA_PATH)

print("\nDataset Loaded Successfully")

print("Dataset Shape :", df.shape)

print("\nFirst Five Rows")

print(df.head())

# ============================================================
# CHECK MISSING VALUES
# ============================================================

print("\nChecking Missing Values...")

missing = df.isnull().sum().sum()

print("Total Missing Values :", missing)

if missing != 0:

    raise Exception(
        "Dataset still contains missing values!"
    )

print("No Missing Values Found.")

# ============================================================
# TARGET VARIABLE
# ============================================================

TARGET = "loan_status"

X = df.drop(columns=[TARGET])

y = df[TARGET]

print("\nTarget Variable :", TARGET)

print("Number of Features :", X.shape[1])

# ============================================================
# CHECK FOR OBJECT COLUMNS
# ============================================================

categorical = X.select_dtypes(include="object").columns

if len(categorical) == 0:

    print("\nNo Categorical Columns Found.")

else:

    print("\nEncoding Remaining Columns...")

    X = pd.get_dummies(
        X,
        columns=categorical,
        drop_first=True
    )

# ============================================================
# SAVE FEATURE LIST
# ============================================================

joblib.dump(
    X.columns.tolist(),
    FEATURE_PATH
)

print("\nFeature Names Saved.")

# ============================================================
# TRAIN TEST SPLIT
# ============================================================

print("\nSplitting Dataset...")

X_train, X_test, y_train, y_test = train_test_split(

    X,

    y,

    test_size=0.20,

    random_state=SEED,

    stratify=y

)

print("Training Samples :", len(X_train))

print("Testing Samples  :", len(X_test))

# ============================================================
# FEATURE SCALING
# ============================================================

print("\nApplying StandardScaler...")

scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)

X_test = scaler.transform(X_test)

joblib.dump(
    scaler,
    SCALER_PATH
)

print("Scaler Saved.")

# ============================================================
# INPUT SHAPE
# ============================================================

INPUT_DIM = X_train.shape[1]

print("\nInput Dimension :", INPUT_DIM)

# ============================================================
# CALLBACKS
# ============================================================

print("\nPreparing Training Callbacks...")

early_stop = EarlyStopping(

    monitor="val_loss",

    patience=8,

    restore_best_weights=True,

    verbose=1

)

checkpoint = ModelCheckpoint(

    MODEL_PATH,

    monitor="val_accuracy",

    save_best_only=True,

    verbose=1

)

reduce_lr = ReduceLROnPlateau(

    monitor="val_loss",

    factor=0.5,

    patience=3,

    min_lr=1e-6,

    verbose=1

)

tensorboard = TensorBoard(

    log_dir="logs",

    histogram_freq=1

)

print("Callbacks Ready.")

print("\nDataset Ready For Training.")

print("=" * 70)
print("END OF PART 1")
print("=" * 70)

# =====================================================
# BUILD IMPROVED DEEP LEARNING MODEL
# =====================================================

print("\n" + "="*60)
print("Building Neural Network")
print("="*60)

model = Sequential([

    Dense(
        512,
        activation="relu",
        input_shape=(INPUT_DIM,)
    ),

    BatchNormalization(),

    Dropout(0.35),

    Dense(
        256,
        activation="relu"
    ),

    BatchNormalization(),

    Dropout(0.30),

    Dense(
        128,
        activation="relu"
    ),

    BatchNormalization(),

    Dropout(0.25),

    Dense(
        64,
        activation="relu"
    ),

    BatchNormalization(),

    Dropout(0.20),

    Dense(
        32,
        activation="relu"
    ),

    Dense(
        1,
        activation="sigmoid",
        dtype="float32"
    )

])

# =====================================================
# COMPILE MODEL
# =====================================================

optimizer = Adam(
    learning_rate=0.001
)

model.compile(

    optimizer=optimizer,

    loss="binary_crossentropy",

    metrics=[
        "accuracy",
        tf.keras.metrics.AUC(name="auc"),
        tf.keras.metrics.Precision(name="precision"),
        tf.keras.metrics.Recall(name="recall")
    ]

)

print("\nModel Summary\n")

model.summary()

# =====================================================
# CALLBACKS
# =====================================================

early_stop = EarlyStopping(

    monitor="val_auc",

    mode="max",

    patience=8,

    restore_best_weights=True,

    verbose=1

)

checkpoint = ModelCheckpoint(

    MODEL_PATH,

    monitor="val_auc",

    mode="max",

    save_best_only=True,

    verbose=1

)

reduce_lr = ReduceLROnPlateau(

    monitor="val_loss",

    factor=0.5,

    patience=3,

    verbose=1,

    min_lr=1e-6

)

# =====================================================
# TRAIN MODEL
# =====================================================

print("\n" + "="*60)
print("Training Started")
print("="*60)

history = model.fit(

    X_train,

    y_train,

    validation_split=0.20,

    epochs=40,

    batch_size=512,

    callbacks=[

        early_stop,

        checkpoint,

        reduce_lr

    ],

    verbose=1

)

print("\nTraining Finished")

# =====================================================
# LOAD BEST MODEL
# =====================================================

from tensorflow.keras.models import load_model

model = load_model(MODEL_PATH)

print("\nBest Model Loaded Successfully")

# =====================================================
# PART 3 - EVALUATION & SAVE RESULTS
# =====================================================

print("\n" + "="*60)
print("Evaluating Model")
print("="*60)

# =====================================================
# PREDICTIONS
# =====================================================

y_prob = model.predict(X_test, verbose=0)

y_pred = (y_prob >= 0.5).astype(int)

# =====================================================
# METRICS
# =====================================================

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, y_prob)

print("\nModel Performance")
print("-"*50)

print(f"Accuracy  : {accuracy:.4f}")
print(f"Precision : {precision:.4f}")
print(f"Recall    : {recall:.4f}")
print(f"F1 Score  : {f1:.4f}")
print(f"ROC AUC   : {roc_auc:.4f}")

# =====================================================
# CLASSIFICATION REPORT
# =====================================================

print("\nClassification Report")
print("-"*50)

print(classification_report(
    y_test,
    y_pred
))

# =====================================================
# CONFUSION MATRIX
# =====================================================

cm = confusion_matrix(
    y_test,
    y_pred
)

print("\nConfusion Matrix\n")
print(cm)

# =====================================================
# SAVE CONFUSION MATRIX
# =====================================================

plt.figure(figsize=(6,6))

plt.imshow(cm, cmap="Blues")

plt.title("Confusion Matrix")

plt.colorbar()

plt.xticks(
    [0,1],
    ["Good Loan","Bad Loan"]
)

plt.yticks(
    [0,1],
    ["Good Loan","Bad Loan"]
)

for i in range(2):
    for j in range(2):
        plt.text(
            j,
            i,
            cm[i,j],
            ha="center",
            va="center",
            fontsize=14,
            color="black"
        )

plt.xlabel("Predicted")
plt.ylabel("Actual")

plt.tight_layout()

plt.savefig(
    os.path.join(
        MODEL_DIR,
        "confusion_matrix.png"
    ),
    dpi=300
)

plt.close()

# =====================================================
# TRAINING ACCURACY
# =====================================================

plt.figure(figsize=(8,5))

plt.plot(
    history.history["accuracy"],
    label="Training"
)

plt.plot(
    history.history["val_accuracy"],
    label="Validation"
)

plt.title("Training Accuracy")

plt.xlabel("Epoch")

plt.ylabel("Accuracy")

plt.legend()

plt.grid(True)

plt.tight_layout()

plt.savefig(
    os.path.join(
        MODEL_DIR,
        "training_accuracy.png"
    ),
    dpi=300
)

plt.close()

# =====================================================
# TRAINING LOSS
# =====================================================

plt.figure(figsize=(8,5))

plt.plot(
    history.history["loss"],
    label="Training"
)

plt.plot(
    history.history["val_loss"],
    label="Validation"
)

plt.title("Training Loss")

plt.xlabel("Epoch")

plt.ylabel("Loss")

plt.legend()

plt.grid(True)

plt.tight_layout()

plt.savefig(
    os.path.join(
        MODEL_DIR,
        "training_loss.png"
    ),
    dpi=300
)

plt.close()

# =====================================================
# ROC CURVE
# =====================================================

from sklearn.metrics import roc_curve

fpr, tpr, _ = roc_curve(
    y_test,
    y_prob
)

plt.figure(figsize=(7,6))

plt.plot(
    fpr,
    tpr,
    label=f"AUC = {roc_auc:.4f}"
)

plt.plot(
    [0,1],
    [0,1],
    "--"
)

plt.xlabel("False Positive Rate")

plt.ylabel("True Positive Rate")

plt.title("ROC Curve")

plt.legend()

plt.grid(True)

plt.tight_layout()

plt.savefig(
    os.path.join(
        MODEL_DIR,
        "roc_curve.png"
    ),
    dpi=300
)

plt.close()

# =====================================================
# PRECISION RECALL CURVE
# =====================================================

from sklearn.metrics import precision_recall_curve

precisions, recalls, _ = precision_recall_curve(
    y_test,
    y_prob
)

plt.figure(figsize=(7,6))

plt.plot(
    recalls,
    precisions
)

plt.xlabel("Recall")

plt.ylabel("Precision")

plt.title("Precision Recall Curve")

plt.grid(True)

plt.tight_layout()

plt.savefig(
    os.path.join(
        MODEL_DIR,
        "precision_recall_curve.png"
    ),
    dpi=300
)

plt.close()

# =====================================================
# SAVE METRICS
# =====================================================

metrics = pd.DataFrame({

    "Metric":[
        "Accuracy",
        "Precision",
        "Recall",
        "F1 Score",
        "ROC AUC"
    ],

    "Value":[
        accuracy,
        precision,
        recall,
        f1,
        roc_auc
    ]

})

metrics.to_csv(

    os.path.join(
        MODEL_DIR,
        "model_metrics.csv"
    ),

    index=False

)

# =====================================================
# SAMPLE PREDICTIONS
# =====================================================

sample = pd.DataFrame({

    "Actual":y_test.values,

    "Prediction":y_pred.flatten(),

    "Probability":y_prob.flatten()

})

sample.head(200).to_csv(

    os.path.join(
        MODEL_DIR,
        "sample_predictions.csv"
    ),

    index=False

)

# =====================================================
# SAVE TRAINING HISTORY
# =====================================================

history_df = pd.DataFrame(history.history)

history_df.to_csv(

    os.path.join(
        MODEL_DIR,
        "training_history.csv"
    ),

    index=False

)

# =====================================================
# FINISHED
# =====================================================

print("\n"+"="*60)
print("MODEL TRAINING COMPLETED SUCCESSFULLY")
print("="*60)

print("\nGenerated Files")

print("-"*40)

print("✓ loan_model.keras")
print("✓ scaler.pkl")
print("✓ feature_columns.pkl")
print("✓ confusion_matrix.png")
print("✓ training_accuracy.png")
print("✓ training_loss.png")
print("✓ roc_curve.png")
print("✓ precision_recall_curve.png")
print("✓ training_history.csv")
print("✓ model_metrics.csv")
print("✓ sample_predictions.csv")

print("\nProject is Ready for Streamlit Deployment 🚀")
