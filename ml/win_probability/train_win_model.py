import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

DATASET = (
    "ml/win_probability/win_probability_dataset.csv"
)

MODEL_FILE = (
    "models/win_probability_model.pkl"
)

df = pd.read_csv(DATASET)

X = df[
    [
        "target",
        "current_score",
        "wickets",
        "balls_remaining",
        "runs_needed",
        "required_rr"
    ]
]

y = df["won_chase"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

print("Training model...")

model.fit(
    X_train,
    y_train
)

predictions = model.predict(
    X_test
)

accuracy = accuracy_score(
    y_test,
    predictions
)

print("\n===== MODEL RESULTS =====")
print(
    f"Accuracy: {accuracy:.4f}"
)

joblib.dump(
    model,
    MODEL_FILE
)

print()
print(
    f"Model saved: {MODEL_FILE}"
)