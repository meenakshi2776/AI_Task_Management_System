import os
import joblib
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)


# =========================================================
# 1. Load Dataset
# =========================================================

DATA_PATH = "data/processed/task_dataset_cleaned.csv"

df = pd.read_csv(DATA_PATH)

print("Dataset loaded successfully")
print("Total records:", len(df))


# =========================================================
# 2. Convert dates
# =========================================================

df["Created_Date"] = pd.to_datetime(
    df["Created_Date"]
)

df["Deadline"] = pd.to_datetime(
    df["Deadline"]
)


# =========================================================
# 3. Feature Engineering
# =========================================================

# Calculate number of days available for the task

df["Days_To_Deadline"] = (
    df["Deadline"] - df["Created_Date"]
).dt.days


# Calculate remaining work

df["Remaining_Hours"] = (
    df["Estimated_Hours"]
    - df["Completed_Hours"]
)


# Calculate completion percentage

df["Completion_Percentage"] = (
    df["Completed_Hours"]
    / df["Estimated_Hours"].replace(0, 1)
) * 100


# =========================================================
# 4. Encode categorical variables
# =========================================================

category_mapping = {
    "Bug": 0,
    "Feature": 1,
    "Documentation": 2,
    "Testing": 3,
    "Database": 4,
    "UI/UX": 5,
    "Backend": 6,
    "Frontend": 7,
    "DevOps": 8,
    "Security": 9
}

status_mapping = {
    "Pending": 0,
    "In Progress": 1,
    "Completed": 2,
    "On Hold": 3
}


df["Category_Code"] = (
    df["Category"]
    .map(category_mapping)
)


df["Status_Code"] = (
    df["Status"]
    .map(status_mapping)
)


# =========================================================
# 5. Create ML features
# =========================================================

feature_columns = [
    "Estimated_Hours",
    "Completed_Hours",
    "Remaining_Hours",
    "Completion_Percentage",
    "Days_To_Deadline",
    "Category_Code",
    "Status_Code"
]


X = df[feature_columns]

y = df["Priority"]


# =========================================================
# 6. Train/Test Split
# =========================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))


# =========================================================
# 7. Random Forest Model
# =========================================================

priority_model = RandomForestClassifier(
    n_estimators=200,
    max_depth=12,
    random_state=42,
    class_weight="balanced"
)


# Train model

priority_model.fit(
    X_train,
    y_train
)


# =========================================================
# 8. Predictions
# =========================================================

y_pred = priority_model.predict(
    X_test
)


# =========================================================
# 9. Evaluation
# =========================================================

accuracy = accuracy_score(
    y_test,
    y_pred
)

precision = precision_score(
    y_test,
    y_pred,
    average="weighted"
)

recall = recall_score(
    y_test,
    y_pred,
    average="weighted"
)

f1 = f1_score(
    y_test,
    y_pred,
    average="weighted"
)


print("\n==============================")
print("PRIORITY PREDICTION RESULTS")
print("==============================")

print("Accuracy :", round(accuracy, 4))
print("Precision:", round(precision, 4))
print("Recall   :", round(recall, 4))
print("F1 Score :", round(f1, 4))


# =========================================================
# 10. Detailed Classification Report
# =========================================================

print("\n==============================")
print("CLASSIFICATION REPORT")
print("==============================")

print(
    classification_report(
        y_test,
        y_pred
    )
)


# =========================================================
# 11. Feature Importance
# =========================================================

importance = pd.DataFrame({
    "Feature": feature_columns,
    "Importance": priority_model.feature_importances_
})

importance = importance.sort_values(
    by="Importance",
    ascending=False
)

print("\n==============================")
print("FEATURE IMPORTANCE")
print("==============================")

print(
    importance.to_string(
        index=False
    )
)


# =========================================================
# 12. Save Model
# =========================================================

os.makedirs(
    "models",
    exist_ok=True
)


joblib.dump(
    priority_model,
    "models/priority_predictor.pkl"
)


joblib.dump(
    category_mapping,
    "models/category_mapping.pkl"
)


joblib.dump(
    status_mapping,
    "models/status_mapping.pkl"
)


joblib.dump(
    feature_columns,
    "models/priority_features.pkl"
)


print("\nPriority prediction model saved successfully!")

print("models/priority_predictor.pkl")