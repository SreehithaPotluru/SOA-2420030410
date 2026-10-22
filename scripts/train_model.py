"""
Optional training helper for a CSV with two columns: url,label.
Use labels: 1 = legitimate, 0 = phishing. This is a simple starter pipeline.
It does not directly train on the original numeric-only PhiUSIIL feature table.
"""
import argparse
import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
import joblib
from backend.detector import extract_features

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", default="data/urls.csv")
    args = parser.parse_args()
    df = pd.read_csv(args.csv)
    if not {"url", "label"}.issubset(df.columns):
        raise ValueError("CSV must contain columns named 'url' and 'label'.")
    X = pd.DataFrame([extract_features(str(u)) for u in df["url"]])
    if "host" in X:
        X = X.drop(columns=["host"])
    y = df["label"].astype(int)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    model = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("classifier", RandomForestClassifier(n_estimators=150, random_state=42, class_weight="balanced"))
    ])
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    print("Accuracy:", round(accuracy_score(y_test, pred), 4))
    print(classification_report(y_test, pred))
    os.makedirs("backend/model", exist_ok=True)
    joblib.dump({"model": model, "columns": list(X.columns)}, "backend/model/phishing_model.joblib")
    print("Saved backend/model/phishing_model.joblib")

if __name__ == "__main__":
    main()
