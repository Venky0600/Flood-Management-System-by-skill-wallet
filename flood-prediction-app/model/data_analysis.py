"""
data_analysis.py
-----------------
Performs Data Visualization & Analysis (Step 3 of the project spec):
- Univariate analysis (distribution plots)
- Multivariate analysis
- Box plots (outlier detection)
- Heat map (correlation)
- Descriptive statistics

Saves all plots into model/plots/ as PNG files.
"""

import pandas as pd
import matplotlib
matplotlib.use("Agg")  # headless rendering
import matplotlib.pyplot as plt
import seaborn as sns
import os

os.makedirs("model/plots", exist_ok=True)

df = pd.read_csv("model/flood_dataset.csv")

print("=== Descriptive Statistics ===")
print(df.describe())

print("\n=== Missing Values ===")
print(df.isnull().sum())

numeric_cols = ["annual_rainfall", "seasonal_rainfall", "cloud_visibility",
                 "humidity", "temperature", "river_level"]

# 1. Univariate analysis - distribution plots
fig, axes = plt.subplots(2, 3, figsize=(15, 8))
for ax, col in zip(axes.flatten(), numeric_cols):
    sns.histplot(df[col].dropna(), kde=True, ax=ax, color="steelblue")
    ax.set_title(f"Distribution of {col}")
plt.tight_layout()
plt.savefig("model/plots/univariate_distributions.png")
plt.close()

# 2. Box plots - outlier detection
fig, axes = plt.subplots(2, 3, figsize=(15, 8))
for ax, col in zip(axes.flatten(), numeric_cols):
    sns.boxplot(y=df[col], ax=ax, color="orange")
    ax.set_title(f"Boxplot of {col}")
plt.tight_layout()
plt.savefig("model/plots/boxplots.png")
plt.close()

# 3. Multivariate analysis - pairplot vs target
sample_df = df.dropna().sample(min(500, len(df.dropna())), random_state=42)
pairplot = sns.pairplot(sample_df, vars=numeric_cols, hue="flood_occurred",
                         palette={0: "seagreen", 1: "crimson"}, plot_kws={"alpha": 0.5})
pairplot.savefig("model/plots/multivariate_pairplot.png")
plt.close()

# 4. Heat map - correlation matrix
plt.figure(figsize=(8, 6))
sns.heatmap(df[numeric_cols + ["flood_occurred"]].corr(), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Heatmap")
plt.tight_layout()
plt.savefig("model/plots/correlation_heatmap.png")
plt.close()

print("\nAll plots saved to model/plots/")
