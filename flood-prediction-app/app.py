"""
app.py
-------
Application Layer — Rising Waters Flood Prediction System.

Routes:
    /            → Home Page (Dashboard)
    /predict     → Prediction Input Page (GET) + Generate Prediction (POST)
    /result/flood    → Flood Chance Result Page
    /result/noflood  → No Flood Chance Result Page
    /history     → Prediction History page
    /about       → Project / model info page
"""

import os
import json
from datetime import datetime

import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, session

from utils.preprocessing import (
    FEATURE_NAMES,
    FEATURE_LABELS,
    load_artifacts,
    validate_form_input,
    preprocess_and_predict,
)

app = Flask(__name__)
app.secret_key = "rising-waters-secret-2024"

MODEL_PATH   = os.path.join("model", "floods.save")
SCALER_PATH  = os.path.join("model", "scaler.save")
METADATA_PATH = os.path.join("model", "model_metadata.json")
LOG_FILE     = "predictions_log.csv"

# ── Load ML Layer artifacts once at startup ────────────────────────────────────
model, scaler = load_artifacts(MODEL_PATH, SCALER_PATH)

with open(METADATA_PATH) as f:
    METADATA = json.load(f)


# ── Home Page (Dashboard) ──────────────────────────────────────────────────────
@app.route("/")
def home():
    stats = get_history_stats()
    return render_template("home.html", metadata=METADATA, stats=stats)


# ── Prediction Input Page ──────────────────────────────────────────────────────
@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        values, error = validate_form_input(request.form)
        if error:
            return render_template(
                "predict.html",
                features=FEATURE_NAMES,
                labels=FEATURE_LABELS,
                error=error,
                form_values=request.form,
            )

        prediction, probability = preprocess_and_predict(model, scaler, values)
        log_prediction(values, prediction, probability)

        # Store result in session so result pages can access it
        session["last_result"] = {
            "flood":       bool(prediction == 1),
            "probability": round(probability * 100, 2),
            "inputs":      dict(zip(FEATURE_NAMES, values)),
        }

        # Route to separate result pages based on prediction
        if prediction == 1:
            return redirect(url_for("result_flood"))
        else:
            return redirect(url_for("result_noflood"))

    return render_template("predict.html", features=FEATURE_NAMES, labels=FEATURE_LABELS)


# ── Flood Chance Result Page ───────────────────────────────────────────────────
@app.route("/result/flood")
def result_flood():
    result = session.get("last_result", {})
    if not result or not result.get("flood"):
        return redirect(url_for("predict"))
    return render_template(
        "result_flood.html",
        probability=result["probability"],
        inputs=result["inputs"],
        labels=FEATURE_LABELS,
    )


# ── No Flood Chance Result Page ────────────────────────────────────────────────
@app.route("/result/noflood")
def result_noflood():
    result = session.get("last_result", {})
    if not result or result.get("flood"):
        return redirect(url_for("predict"))
    return render_template(
        "result_noflood.html",
        probability=result["probability"],
        inputs=result["inputs"],
        labels=FEATURE_LABELS,
    )


# ── Prediction History ─────────────────────────────────────────────────────────
@app.route("/history")
def history():
    records = []
    if os.path.exists(LOG_FILE):
        df = pd.read_csv(LOG_FILE)
        df = df.sort_values("timestamp", ascending=False)
        records = df.to_dict(orient="records")
    return render_template("history.html", records=records, labels=FEATURE_LABELS)


# ── About / Model Info ─────────────────────────────────────────────────────────
@app.route("/about")
def about():
    return render_template("about.html", metadata=METADATA)


# ── Helpers ────────────────────────────────────────────────────────────────────
def log_prediction(values, prediction, probability):
    row = dict(zip(FEATURE_NAMES, values))
    row["prediction"] = "Flood" if prediction == 1 else "No Flood"
    row["probability"] = round(probability * 100, 2)
    row["timestamp"]  = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    df_row = pd.DataFrame([row])
    if os.path.exists(LOG_FILE):
        df_row.to_csv(LOG_FILE, mode="a", header=False, index=False)
    else:
        df_row.to_csv(LOG_FILE, mode="w", header=True, index=False)


def get_history_stats():
    if not os.path.exists(LOG_FILE):
        return {"total": 0, "flood": 0, "no_flood": 0}
    df = pd.read_csv(LOG_FILE)
    total = len(df)
    flood = int((df["prediction"] == "Flood").sum())
    return {"total": total, "flood": flood, "no_flood": total - flood}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
