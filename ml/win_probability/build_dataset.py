import pandas as pd
from pathlib import Path

CURATED_DIR = Path("data/curated")
OUTPUT_DIR = Path("ml/win_probability")

matches = pd.read_parquet(
    CURATED_DIR / "curated_matches.parquet"
)

deliveries = pd.read_parquet(
    CURATED_DIR / "curated_deliveries.parquet"
)

records = []

for match_id in deliveries["match_id"].unique():

    match_deliveries = deliveries[
        deliveries["match_id"] == match_id
    ]

    innings1 = match_deliveries[
        match_deliveries["innings"] == 1
    ]

    innings2 = match_deliveries[
        match_deliveries["innings"] == 2
    ]

    if len(innings1) == 0 or len(innings2) == 0:
        continue

    target = innings1["total_runs"].sum() + 1

    final_score_2 = innings2["total_runs"].sum()

    won_chase = 1 if final_score_2 >= target else 0

    innings2 = innings2.copy()

    innings2["cum_runs"] = (
        innings2["total_runs"].cumsum()
    )

    innings2["cum_wickets"] = (
        innings2["wicket"].cumsum()
    )

    innings2["balls"] = range(
        1,
        len(innings2) + 1
    )

    for _, row in innings2.iterrows():

        balls_bowled = row["balls"]

        balls_remaining = max(
            120 - balls_bowled,
            0
        )

        runs_needed = max(
            target - row["cum_runs"],
            0
        )

        rrr = 0

        if balls_remaining > 0:

            rrr = (
                runs_needed /
                (balls_remaining / 6)
            )

        records.append(
            {
                "target": target,
                "current_score": row["cum_runs"],
                "wickets": row["cum_wickets"],
                "balls_remaining": balls_remaining,
                "runs_needed": runs_needed,
                "required_rr": round(rrr, 2),
                "won_chase": won_chase
            }
        )

dataset = pd.DataFrame(records)

dataset.to_csv(
    OUTPUT_DIR / "win_probability_dataset.csv",
    index=False
)

print(dataset.head())
print()
print("Rows:", len(dataset))