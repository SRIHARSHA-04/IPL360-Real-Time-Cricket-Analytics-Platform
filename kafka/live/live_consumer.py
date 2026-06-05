import json
import pandas as pd
import joblib

from kafka import KafkaConsumer

WIN_MODEL = joblib.load(
    "models/win_probability_model.pkl"
)

deliveries = pd.read_parquet(
    "data/curated/curated_deliveries.parquet"
)

match_id = str(
    deliveries.iloc[0]["match_id"]
)

innings1 = deliveries[
    (deliveries["match_id"].astype(str) == match_id)
    &
    (deliveries["innings"] == 1)
]

TARGET = int(
    innings1["total_runs"].sum()
) + 1

consumer = KafkaConsumer(
    "ipl_match_stream",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="latest",
    value_deserializer=lambda x: json.loads(
        x.decode("utf-8")
    )
)

current_innings = None

score = 0
wickets = 0
legal_balls = 0

print("Live Consumer Started")

for message in consumer:

    data = message.value

    innings = int(data["innings"])

    if current_innings is None:
        current_innings = innings

    if innings != current_innings:

        current_innings = innings

        score = 0
        wickets = 0
        legal_balls = 0

    score += int(data["total_runs"])

    wickets += int(data["wicket"])

    if legal_balls < 120:
        legal_balls += 1

    completed_overs = legal_balls // 6
    balls_in_over = legal_balls % 6

    state = {
        "innings": innings,
        "score": score,
        "wickets": wickets,
        "legal_balls": legal_balls,
        "display_over": f"{completed_overs}.{balls_in_over}",
        "overs_float": round(
            legal_balls / 6,
            2
        ),
        "batter": data["batter"],
        "bowler": data["bowler"],
        "runs": data["total_runs"]
    }

    if innings == 2:

        balls_remaining = max(
            120 - legal_balls,
            0
        )

        runs_needed = max(
            TARGET - score,
            0
        )

        required_rr = 0

        if balls_remaining > 0:

            required_rr = (
                runs_needed /
                (balls_remaining / 6)
            )

        match_finished = (
            runs_needed <= 0
            or
            balls_remaining == 0
        )

        features = pd.DataFrame(
            [{
                "target": TARGET,
                "current_score": score,
                "wickets": wickets,
                "balls_remaining": balls_remaining,
                "runs_needed": runs_needed,
                "required_rr": required_rr
            }]
        )

        probabilities = (
            WIN_MODEL.predict_proba(
                features
            )[0]
        )

        win_pct = round(
            probabilities[1] * 100,
            1
        )

        state.update(
            {
                "target": TARGET,
                "runs_needed": runs_needed,
                "balls_remaining": balls_remaining,
                "required_rr": round(
                    required_rr,
                    2
                ),
                "win_probability": win_pct,
                "match_finished": match_finished
            }
        )

    with open(
        "dashboard/live/live_match_state.json",
        "w"
    ) as f:

        json.dump(
            state,
            f,
            indent=4
        )

    print(state)