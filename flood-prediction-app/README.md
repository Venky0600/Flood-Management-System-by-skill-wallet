# 🌊 Rising Waters: A Machine Learning Approach to Flood Prediction

A complete, ready-to-run machine learning flood prediction system built with
Python, Flask, and classification algorithms (Decision Tree, Random Forest,
KNN, XGBoost).

## Project Structure

```
flood-prediction-app/
├── app.py                      # Flask application (routes, prediction logic)
├── requirements.txt            # Python dependencies
├── Procfile                    # IBM Cloud Foundry start command
├── manifest.yml                # IBM Cloud Foundry deployment manifest
├── Dockerfile                  # IBM Cloud Code Engine / container deployment
├── .gitignore
├── model/
│   ├── generate_dataset.py     # Creates the synthetic flood dataset
│   ├── flood_dataset.csv       # Generated dataset (6 features + target)
│   ├── data_analysis.py        # EDA: distributions, boxplots, heatmap, pairplot
│   ├── plots/                  # Generated EDA plots (PNG)
│   ├── train_model.py          # Preprocessing + trains all 4 models + saves best
│   ├── floods.save             # Saved best model (as named in project spec)
│   ├── scaler.save             # Saved StandardScaler
│   ├── model.pkl / scaler.pkl  # Same artifacts, alternate naming
│   └── model_metadata.json     # Best model name + accuracy comparison
├── utils/
│   └── preprocessing.py        # Shared validation/scaling/prediction helpers
├── templates/
│   ├── base.html                # Shared layout + nav
│   ├── home.html                # Dashboard
│   ├── predict.html             # Prediction input form
│   ├── result.html              # Flood / No Flood result page
│   ├── history.html             # Prediction history log
│   └── about.html               # Project info
└── static/css/style.css        # Styling
```

## ⚠️ About the Dataset

No specific Kaggle file was provided, so `model/generate_dataset.py` creates a
**realistic synthetic dataset** (3,000 rows) with the exact features named in
the project brief — annual rainfall, seasonal rainfall, cloud visibility — plus
humidity, temperature, and river level, with a binary flood/no-flood label
built from a weighted, noisy risk formula (so it behaves like real weather
data, including ~2% missing values to exercise the preprocessing step).

**To use a real Kaggle dataset instead:** download it, save it as
`model/flood_dataset.csv` with the same column names (or edit `FEATURE_NAMES`
in `model/train_model.py` and `utils/preprocessing.py` to match), then re-run
`train_model.py`. With a real dataset closely matching the brief, you should
see results closer to the **96.55% XGBoost accuracy** mentioned in the spec —
on the synthetic data here, Random Forest/XGBoost land around 80–82%, which is
expected for randomly generated data with deliberate noise.

## Setup & Run Locally

```bash
# 1. Create environment
conda create -n flood-prediction python=3.10
conda activate flood-prediction

# 2. Install dependencies
pip install -r requirements.txt

# 3. (Already done, but to regenerate) Build the dataset
python model/generate_dataset.py

# 4. (Already done, but to regenerate) Run EDA
python model/data_analysis.py

# 5. (Already done, but to regenerate) Train models & save the best one
python model/train_model.py

# 6. Run the Flask app
python app.py
```

Visit **http://127.0.0.1:5000** in your browser.

> The trained model (`floods.save`) and scaler (`scaler.save`) are already
> included in this package — you do **not** need to retrain before running
> the app. Steps 3–5 above are only needed if you swap in a new dataset.

## Pages

| Route        | Description                                      |
|--------------|---------------------------------------------------|
| `/`          | Dashboard — model accuracy comparison, usage stats |
| `/predict`   | Input form for rainfall/weather readings           |
| `/predict` (POST) | Returns Flood Chance / No Flood Chance result |
| `/history`   | Log of all past predictions                        |
| `/about`     | Project overview, architecture, use-case scenarios |

## Deployment to IBM Cloud

### Option A — Cloud Foundry
```bash
ibmcloud login
ibmcloud target --cf
ibmcloud cf push
```
(Uses `manifest.yml` and `Procfile` included in this package.)

### Option B — Code Engine (Docker-based)
```bash
ibmcloud ce project create --name rising-waters
ibmcloud ce application create --name rising-waters-app \
    --build-source . --strategy dockerfile --port 8080
```
(Uses the included `Dockerfile`.)

### Option C — GitHub → IBM Cloud
```bash
git init
git add .
git commit -m "Rising Waters flood prediction app"
git remote add origin https://github.com/<your-username>/rising-waters.git
git push -u origin main
```
Then connect the repo in the IBM Cloud console (Cloud Foundry or Code Engine)
and deploy directly from GitHub.

## Architecture (matches the 6-layer diagram)

- **User Layer** — Web browser
- **Presentation Layer** — Flask templates (Home / Input Form / Result / History)
- **Application Layer** — `app.py` (routing, validation, preprocessing, prediction)
- **Machine Learning Layer** — `floods.save` (model) + `scaler.save` (scaler)
- **Data Layer** — `generate_dataset.py` → `data_analysis.py` → `train_model.py`
- **Deployment Layer** — Git → GitHub → IBM Cloud → Live Application

## Team Roles Suggestion (for a 5-person team)

| Member | Layer Ownership |
|--------|-----------------|
| Member 1 | Data Layer — dataset, EDA, preprocessing |
| Member 2 | Machine Learning Layer — model training, comparison, tuning |
| Member 3 | Application Layer — Flask routes, validation logic |
| Member 4 | Presentation Layer — templates, CSS, UX |
| Member 5 | Deployment Layer — Git/GitHub, IBM Cloud, documentation |

## Skills Demonstrated

Machine Learning Algorithms · NumPy · Matplotlib · Scikit-Learn · Supervised
Learning · Flask · K-Nearest Neighbors · Data Preprocessing · Model Evaluation
