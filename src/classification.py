import os
import joblib
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report
)


# =========================================================
# 1. Load dataset
# =========================================================

DATA_PATH = "data/processed/task_dataset_cleaned.csv"

df = pd.read_csv(DATA_PATH)

print("Dataset loaded successfully")
print("Number of records:", len(df))


# =========================================================
# 2. Prepare input and target
# =========================================================

X_text = df["Cleaned_Task_Description"]
y = df["Category"]


# =========================================================
# 3. Train/Test Split
# =========================================================

X_train_text, X_test_text, y_train, y_test = train_test_split(
    X_text,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("\nTraining samples:", len(X_train_text))
print("Testing samples:", len(X_test_text))


# =========================================================
# 4. TF-IDF Vectorization
# =========================================================

tfidf = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1, 2)
)

X_train = tfidf.fit_transform(X_train_text)
X_test = tfidf.transform(X_test_text)

print("\nTF-IDF Training Shape:", X_train.shape)
print("TF-IDF Testing Shape:", X_test.shape)


# =========================================================
# 5. Naive Bayes
# =========================================================

nb_model = MultinomialNB()

nb_model.fit(
    X_train,
    y_train
)

y_pred_nb = nb_model.predict(X_test)


nb_accuracy = accuracy_score(
    y_test,
    y_pred_nb
)

nb_precision = precision_score(
    y_test,
    y_pred_nb,
    average="weighted"
)

nb_recall = recall_score(
    y_test,
    y_pred_nb,
    average="weighted"
)

nb_f1 = f1_score(
    y_test,
    y_pred_nb,
    average="weighted"
)


print("\n==============================")
print("NAIVE BAYES RESULTS")
print("==============================")

print("Accuracy :", nb_accuracy)
print("Precision:", nb_precision)
print("Recall   :", nb_recall)
print("F1 Score :", nb_f1)


# =========================================================
# 6. Linear SVM
# =========================================================

svm_model = LinearSVC(
    C=1.0,
    random_state=42
)

svm_model.fit(
    X_train,
    y_train
)

y_pred_svm = svm_model.predict(X_test)


svm_accuracy = accuracy_score(
    y_test,
    y_pred_svm
)

svm_precision = precision_score(
    y_test,
    y_pred_svm,
    average="weighted"
)

svm_recall = recall_score(
    y_test,
    y_pred_svm,
    average="weighted"
)

svm_f1 = f1_score(
    y_test,
    y_pred_svm,
    average="weighted"
)


print("\n==============================")
print("LINEAR SVM RESULTS")
print("==============================")

print("Accuracy :", svm_accuracy)
print("Precision:", svm_precision)
print("Recall   :", svm_recall)
print("F1 Score :", svm_f1)


# =========================================================
# 7. Compare Models
# =========================================================

results = pd.DataFrame({
    "Model": [
        "Multinomial Naive Bayes",
        "Linear SVM"
    ],
    "Accuracy": [
        nb_accuracy,
        svm_accuracy
    ],
    "Precision": [
        nb_precision,
        svm_precision
    ],
    "Recall": [
        nb_recall,
        svm_recall
    ],
    "F1 Score": [
        nb_f1,
        svm_f1
    ]
})

print("\n==============================")
print("MODEL COMPARISON")
print("==============================")

print(results.to_string(index=False))


# =========================================================
# 8. Select Best Model
# =========================================================

if svm_f1 >= nb_f1:
    best_model = svm_model
    best_model_name = "Linear SVM"
else:
    best_model = nb_model
    best_model_name = "Multinomial Naive Bayes"


print("\nBest Model:", best_model_name)


# =========================================================
# 9. Save Models
# =========================================================

os.makedirs(
    "models",
    exist_ok=True
)

joblib.dump(
    best_model,
    "models/task_classifier.pkl"
)

joblib.dump(
    tfidf,
    "models/tfidf_vectorizer.pkl"
)

print("\nModels saved successfully!")

print("Saved:")
print("models/task_classifier.pkl")
print("models/tfidf_vectorizer.pkl")


# =========================================================
# 10. Detailed Report
# =========================================================

print("\n==============================")
print("CLASSIFICATION REPORT")
print("==============================")

if best_model_name == "Linear SVM":
    print(
        classification_report(
            y_test,
            y_pred_svm
        )
    )
else:
    print(
        classification_report(
            y_test,
            y_pred_nb
        )
    )