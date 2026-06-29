"""
train_model.py
---------------
Implements Steps 4, 5, and 6 of the project spec:
  4. Data Pre-processing  (missing values, outliers, encoding, scaling, split)
  5. Model Building       (Decision Tree, Random Forest, KNN, XGBoost)
  6. Best Model Selection (XGBoost saved as floods.save / scaler.save)

Per the project specification, XGBoost is the best-performing model
and is deployed in the Flask application.
"""

import pandas as pd
import numpy as np
import joblib
import json

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from xgboost import XGBClassifier
from sklearn.metrics import (
    accuracy_score, classification_report, confusion_matrix
)

FEATURE_NAMES = [
    "annual_rainfall",
    "seasonal_rainfall",
    "cloud_visibility",
    "humidity",
    "temperature",
    "river_level",
]
TARGET = "flood_occurred"

# ── Step 1: Load dataset ──────────────────────────────────────────────────────
df = pd.read_csv("model/flood_dataset.csv")
print(f"Loaded dataset: {df.shape[0]} rows, {df.shape[1]} columns")
print(f"Class distribution:\n{df[TARGET].value_counts()}\n")

# ── Step 2: Handle missing values (mean imputation for numeric features) ──────
df[FEATURE_NAMES] = df[FEATURE_NAMES].fillna(df[FEATURE_NAMES].mean())

# ── Step 3: Detect & treat outliers using IQR capping ────────────────────────
for col in FEATURE_NAMES:
    Q1, Q3 = df[col].quantile(0.25), df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower, upper = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
    df[col] = df[col].clip(lower, upper)

# ── Step 4: Split dependent / independent variables ───────────────────────────
X = df[FEATURE_NAMES]
y = df[TARGET]

# ── Step 5: Train / test split (80/20, stratified) ───────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ── Step 6: Feature scaling (StandardScaler) ──────────────────────────────────
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)

# ── Step 7: Model Building — train & compare 4 classifiers ───────────────────
models = {
    "Decision Tree": DecisionTreeClassifier(max_depth=10, random_state=42),
    "Random Forest": RandomForestClassifier(n_estimators=300, max_depth=12, random_state=42),
    "KNN":           KNeighborsClassifier(n_neighbors=5),
    "XGBoost":       XGBClassifier(
        n_estimators=500,
        max_depth=8,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        use_label_encoder=False,
        eval_metric="logloss",
        random_state=42,
    ),
}

results        = {}
trained_models = {}

print("=" * 60)
for name, model in models.items():
    model.fit(X_train_scaled, y_train)
    preds  = model.predict(X_test_scaled)
    acc    = accuracy_score(y_test, preds)
    results[name]        = acc
    trained_models[name] = model

    print(f"\n--- {name} ---")
    print(f"Accuracy : {acc * 100:.2f}%")
    print("Confusion Matrix:\n", confusion_matrix(y_test, preds))
    print("Classification Report:\n", classification_report(y_test, preds))

# ── Step 8: Best Model Selection ──────────────────────────────────────────────
# Per project specification, XGBoost is the deployed model.
# We confirm it by checking accuracy; if for any reason it isn't top,
# we still deploy it as the spec requires.
best_name_by_acc = max(results, key=results.get)
print("=" * 60)
print(f"\nHighest accuracy model : {best_name_by_acc} ({results[best_name_by_acc]*100:.2f}%)")

# Specification mandates XGBoost for deployment
DEPLOY_MODEL = "XGBoost"
best_model   = trained_models[DEPLOY_MODEL]
best_acc     = results[DEPLOY_MODEL]
print(f"Deployed model (spec)  : {DEPLOY_MODEL} ({best_acc*100:.2f}%)")

# ── Step 9: Save best model + scaler (floods.save) ────────────────────────────
joblib.dump(best_model, "model/floods.save")
joblib.dump(scaler,     "model/scaler.save")

# Also save with .pkl extension for convenience
joblib.dump(best_model, "model/model.pkl")
joblib.dump(scaler,     "model/scaler.pkl")

# Save metadata used by the Flask application
metadata = {
    "feature_names": FEATURE_NAMES,
    "best_model":    DEPLOY_MODEL,
    "best_accuracy": round(best_acc * 100, 2),
    "all_results":   {k: round(v * 100, 2) for k, v in results.items()},
}
with open("model/model_metadata.json", "w") as f:
    json.dump(metadata, f, indent=2)

print("\nSaved: model/floods.save, model/scaler.save, model/model_metadata.json")
print(f"   Deployed model : {DEPLOY_MODEL}")
print(f"   Test accuracy  : {best_acc*100:.2f}%")
