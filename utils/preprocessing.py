"""
utils/preprocessing.py
-----------------------
Shared preprocessing helpers used by the Flask Application Layer.
"""

import joblib
import numpy as np

FEATURE_NAMES = [
    "annual_rainfall",
    "seasonal_rainfall",
    "cloud_visibility",
    "humidity",
    "temperature",
    "river_level",
]

FEATURE_LABELS = {
    "annual_rainfall": ("Annual Rainfall", "mm"),
    "seasonal_rainfall": ("Seasonal (Monsoon) Rainfall", "mm"),
    "cloud_visibility": ("Cloud Visibility", "km"),
    "humidity": ("Humidity", "%"),
    "temperature": ("Temperature", "°C"),
    "river_level": ("River Level", "m"),
}


def load_artifacts(model_path="model/floods.save", scaler_path="model/scaler.save"):
    """Load the trained model and scaler from disk."""
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    return model, scaler


def validate_form_input(form_data):
    """
    Validate raw Flask form input.
    Returns (values: list[float], error: str|None)
    """
    values = []
    for feature in FEATURE_NAMES:
        raw = form_data.get(feature, "").strip()
        if raw == "":
            return None, f"Missing value for {FEATURE_LABELS[feature][0]}."
        try:
            val = float(raw)
        except ValueError:
            return None, f"Invalid number for {FEATURE_LABELS[feature][0]}."
        if val < 0:
            return None, f"{FEATURE_LABELS[feature][0]} cannot be negative."
        values.append(val)
    return values, None


def preprocess_and_predict(model, scaler, values):
    """Scale input values and run prediction + probability."""
    arr = np.array(values).reshape(1, -1)
    scaled = scaler.transform(arr)
    prediction = int(model.predict(scaled)[0])
    probability = float(model.predict_proba(scaled)[0][1])
    return prediction, probability
