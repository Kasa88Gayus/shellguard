import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score, average_precision_score
from pathlib import Path

# 1. Load our engineered features
print("Loading data...")
m = pd.read_csv("outputs/node_metrics.csv")

# Keep only companies (drop the individual people)
m = m[m["entity_type"] == "company"]

# 2. Define Features (X) and Target (y)
features = ["degree", "betweenness", "pagerank"]
X = m[features].fillna(0) 
y = m["is_shell"].astype(int)

# 3. Split the data (70% for training, 30% for testing)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

# 4. Train the Random Forest model
print("Training Random Forest model...")
clf = RandomForestClassifier(
    n_estimators=300, 
    random_state=42, 
    class_weight="balanced" 
)
clf.fit(X_train, y_train)

# 5. Make predictions on the test data
proba = clf.predict_proba(X_test)[:, 1]
pred = clf.predict(X_test)

# 6. Evaluate the results
print("\n--- MODEL EVALUATION ---")
print(classification_report(y_test, pred, target_names=["Legitimate", "Shell"]))

print(f"ROC-AUC Score: {roc_auc_score(y_test, proba):.4f}")
print(f"PR-AUC Score : {average_precision_score(y_test, proba):.4f}")

# 7. Save feature importances
importances = pd.DataFrame({
    "feature": features,
    "importance": clf.feature_importances_
}).sort_values("importance", ascending=False)

importances.to_csv("outputs/fig02_baseline_importances.csv", index=False)
print("\nFeature Importance:")
print(importances.to_string(index=False))
