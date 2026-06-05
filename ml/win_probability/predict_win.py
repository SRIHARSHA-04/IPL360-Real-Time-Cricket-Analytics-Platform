import joblib
import pandas as pd

MODEL_FILE = (
    "models/win_probability_model.pkl"
)

model = joblib.load(
    MODEL_FILE
)

target = int(
    input("Target: ")
)

current_score = int(
    input("Current Score: ")
)

wickets = int(
    input("Wickets Lost: ")
)

balls_remaining = int(
    input("Balls Remaining: ")
)

runs_needed = (
    target - current_score
)

required_rr = (
    runs_needed /
    (balls_remaining / 6)
)

features = pd.DataFrame(
    [{
        "target": target,
        "current_score": current_score,
        "wickets": wickets,
        "balls_remaining": balls_remaining,
        "runs_needed": runs_needed,
        "required_rr": required_rr
    }]
)

probabilities = model.predict_proba(
    features
)[0]

lose_pct = round(
    probabilities[0] * 100,
    2
)

win_pct = round(
    probabilities[1] * 100,
    2
)

print()
print("===== WIN PROBABILITY =====")
print(
    f"Batting Team Win % : {win_pct}"
)
print(
    f"Bowling Team Win % : {lose_pct}"
)