import joblib
import pandas as pd

MODEL_FILE = "models/score_predictor.pkl"

model = joblib.load(
    MODEL_FILE
)

current_score = int(
    input("Current Score: ")
)

wickets = int(
    input("Wickets Lost: ")
)

overs = float(
    input("Overs Completed: ")
)

run_rate = current_score / overs

features = pd.DataFrame(
    [
        {
            "current_score": current_score,
            "wickets": wickets,
            "overs": overs,
            "run_rate": run_rate
        }
    ]
)

prediction = model.predict(
    features
)[0]

print()
print("===== SCORE PREDICTION =====")
print(
    f"Predicted Final Score: "
    f"{round(prediction)}"
)