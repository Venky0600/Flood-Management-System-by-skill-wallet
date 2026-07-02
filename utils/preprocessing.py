import joblib
import pandas as pd

# The exact feature names expected by the model
FEATURE_NAMES = [
    "Temp",
    "Humidity",
    "Cloud Cover",
    "ANNUAL",
    "Jan-Feb",
    "Mar-May",
    "Jun-Sep",
    "Oct-Dec",
    "avgjune",
    "sub"
]

# Human-readable labels for the UI and history table (Label, Unit)
FEATURE_LABELS = {
    "Temp": ("Temperature", "°C"),
    "Humidity": ("Humidity", "%"),
    "Cloud Cover": ("Cloud Cover", "%"),
    "ANNUAL": ("Annual Rainfall", "mm"),
    "Jan-Feb": ("Jan-Feb Rainfall", "mm"),
    "Mar-May": ("Mar-May Rainfall", "mm"),
    "Jun-Sep": ("Jun-Sep Rainfall", "mm"),
    "Oct-Dec": ("Oct-Dec Rainfall", "mm"),
    "avgjune": ("Average June Rainfall", "mm"),
    "sub": ("Sub-Division Index", "")
}


def load_artifacts(model_path, scaler_path):
    """Loads the serialized model and scaler."""
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    return model, scaler


def validate_form_input(form_data):
    """
    Validates that all required fields are present and numeric.
    Returns: (list_of_values, error_string)
    """
    values = []
    for feature in FEATURE_NAMES:
        raw_val = form_data.get(feature)
        if raw_val is None or raw_val.strip() == "":
            return None, f"Missing value for {FEATURE_LABELS[feature]}"
        try:
            val = float(raw_val)
            values.append(val)
        except ValueError:
            return None, f"Invalid number provided for {FEATURE_LABELS[feature]}"
    return values, None


def preprocess_and_predict(model, scaler, values):
    """
    Scales the input values and makes a prediction.
    Returns: (prediction_class, probability_of_flood)
    """
    # 1. Convert to DataFrame (so scaler receives feature names properly if it expects them)
    # The models were trained on these exact columns
    input_df = pd.DataFrame([values], columns=FEATURE_NAMES)

    # 2. Scale
    scaled_data = scaler.transform(input_df)

    # 3. Predict
    prediction = int(model.predict(scaled_data)[0])
    
    # 4. Probabilities (Index 1 is the probability of class 1 / Flood)
    probs = model.predict_proba(scaled_data)[0]
    prob = float(probs[1])

    return prediction, prob
