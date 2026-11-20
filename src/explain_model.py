import pandas as pd
import shap
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier

# 1. Load data and prepare features (same as baseline)
print("Loading data and training model...")
m = pd.read_csv("outputs/node_metrics.csv")
m = m[m["entity_type"] == "company"]
features = ["degree", "betweenness", "pagerank"]
X = m[features].fillna(0)
y = m["is_shell"].astype(int)

# 2. Train the model on all data so we can explain it
clf = RandomForestClassifier(n_estimators=300, random_state=42, class_weight="balanced")
clf.fit(X, y)

# 3. Initialize the SHAP Explainer
# TreeExplainer is specifically optimized for Random Forests
explainer = shap.TreeExplainer(clf)

# 4. Pick a specific Shell Company to investigate
# We will find the first company in the dataset that is a shell
sample_shell = X[y == 1].iloc[[0]]

print("Generating SHAP explanation for a known shell company...")
# Calculate SHAP values for this specific company
shap_values = explainer(sample_shell)

# 5. Create the visual chart
plt.figure(figsize=(10, 6))
# Note: In newer SHAP versions, we access the class 1 values like this:
shap.plots.waterfall(shap_values[0, :, 1], show=False)

# Save the plot
plt.tight_layout()
plt.savefig("outputs/fig03_shap_explanation.png", dpi=150)
print("Saved explanation chart to outputs/fig03_shap_explanation.png")
