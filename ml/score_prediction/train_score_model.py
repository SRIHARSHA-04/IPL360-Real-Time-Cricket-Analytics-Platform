import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

FEATURE_FILE = (
    "ml/features/score_prediction_features.csv"
)

MODEL_FILE = (
    "models/score_predictor.pkl"
)

df = pd.read_csv(FEATURE_FILE)

X = df[
    [
        "current_score",
        "wickets",
        "overs",
        "run_rate"
    ]
]

y = df["final_score"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

print("Training model...")

model.fit(
    X_train,
    y_train
)

predictions = model.predict(X_test)

mae = mean_absolute_error(
    y_test,
    predictions
)

print("\n===== MODEL RESULTS =====")
print(f"MAE: {mae:.2f} runs")

joblib.dump(
    model,
    MODEL_FILE
)

print()
print("Model saved:")
print(MODEL_FILE)