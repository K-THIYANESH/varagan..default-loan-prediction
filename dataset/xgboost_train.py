# Optimized XGBoost training script
import os
import joblib
import warnings
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,roc_auc_score,classification_report,confusion_matrix
from xgboost import XGBClassifier

warnings.filterwarnings("ignore")

DATA_PATH="dataset/processed_loan_data_200k.csv"
MODEL_DIR="models"
os.makedirs(MODEL_DIR,exist_ok=True)

MODEL_PATH=os.path.join(MODEL_DIR,"xgboost_model.pkl")
FEATURE_PATH=os.path.join(MODEL_DIR,"xgb_feature_columns.pkl")
THRESHOLD_PATH=os.path.join(MODEL_DIR,"xgb_threshold.pkl")

print("="*60)
print("Loading Dataset")
print("="*60)
df=pd.read_csv(DATA_PATH)
print(df.shape)

TARGET="loan_status"
X=df.drop(columns=[TARGET])
y=df[TARGET]
joblib.dump(X.columns.tolist(),FEATURE_PATH)

X_train,X_test,y_train,y_test=train_test_split(
    X,y,test_size=0.2,random_state=42,stratify=y
)

neg=(y_train==0).sum()
pos=(y_train==1).sum()
scale=neg/max(pos,1)

model=XGBClassifier(
    objective="binary:logistic",
    eval_metric="auc",
    learning_rate=0.03,
    n_estimators=1200,
    max_depth=10,
    min_child_weight=5,
    gamma=0.15,
    subsample=0.9,
    colsample_bytree=0.9,
    reg_alpha=0.3,
    reg_lambda=3,
    grow_policy="lossguide",
    max_bin=512,
    tree_method="hist",
    random_state=42,
    n_jobs=-1,
    scale_pos_weight=scale
)

print("\nTraining XGBoost...\n")
model.fit(
    X_train,y_train,
    eval_set=[(X_test,y_test)],
    verbose=100
)

joblib.dump(model,MODEL_PATH)

y_prob=model.predict_proba(X_test)[:,1]

best_threshold=0.5
best_f1=0
for t in np.arange(0.30,0.71,0.01):
    pred=(y_prob>=t).astype(int)
    score=f1_score(y_test,pred)
    if score>best_f1:
        best_f1=score
        best_threshold=t

joblib.dump(best_threshold,THRESHOLD_PATH)
y_pred=(y_prob>=best_threshold).astype(int)

accuracy=accuracy_score(y_test,y_pred)
precision=precision_score(y_test,y_pred)
recall=recall_score(y_test,y_pred)
f1=f1_score(y_test,y_pred)
roc=roc_auc_score(y_test,y_prob)

print(f"\nBest Threshold: {best_threshold:.2f}")
print("Accuracy :",accuracy)
print("Precision:",precision)
print("Recall   :",recall)
print("F1 Score :",f1)
print("ROC AUC  :",roc)
print("\nClassification Report\n")
print(classification_report(y_test,y_pred))
print("Confusion Matrix")
print(confusion_matrix(y_test,y_pred))

importance=pd.DataFrame({"Feature":X.columns,"Importance":model.feature_importances_}).sort_values("Importance",ascending=False)
importance.to_csv(os.path.join(MODEL_DIR,"xgb_feature_importance.csv"),index=False)

metrics=pd.DataFrame({
"Metric":["Accuracy","Precision","Recall","F1","ROC_AUC","Best_Threshold"],
"Value":[accuracy,precision,recall,f1,roc,best_threshold]
})
metrics.to_csv(os.path.join(MODEL_DIR,"xgb_metrics.csv"),index=False)

print("\nTop 20 Features")
print(importance.head(20))
print("\nDone!")
